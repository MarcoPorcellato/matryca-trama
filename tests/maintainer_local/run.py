"""Unsupported, synthetic-only maintainer test entry; never a graph selector."""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import local_provision  # noqa: E402

preflight = local_provision.preflight
resources, provision = preflight.resources, preflight.provision
import fixture_builder  # noqa: E402 - admitted qualification directory.
from trama_plumber_client import _fixture as fixture_module  # noqa: E402
from trama_plumber_client import _mapping as mapping  # noqa: E402
from trama_plumber_client import _profile as profile  # noqa: E402

for module, expected in (
    (local_provision, HERE / "local_provision.py"),
    (fixture_builder, preflight.QUALIFICATION / "fixture_builder.py"),
    *(
        (
            module,
            preflight.process_boundary.SOURCE
            / "trama_plumber_client"
            / (module.__name__.rsplit(".", 1)[1] + ".py"),
        )
        for module in (fixture_module, mapping, profile)
    ),
):
    if (
        Path(module.__file__).resolve() != expected
        or Path(module.__spec__.origin).resolve() != expected
    ):
        raise RuntimeError("MA runner support origin mismatch")


def public_report(state: dict, duration: float) -> dict:
    """Fixed summary only; private diagnostics never become public messages."""
    allowed = {"pass", "preflight_refused", "integrity_failure", "cleanup_uncertain", "run_refused"}
    if (
        state.get("exit_class") not in allowed
        or any(type(state.get(key)) is not int or state[key] < 0 for key in ("nodes", "edges"))
        or any(
            type(state.get(key)) is not bool for key in ("cleanup_succeeded", "fixture_unchanged")
        )
        or type(duration) not in (int, float)
        or not math.isfinite(duration)
        or duration < 0
    ):
        raise RuntimeError("MA summary shape rejected")
    return {
        "scope": "unsupported-local-synthetic-only",
        "exit_class": state["exit_class"],
        "nodes": state["nodes"],
        "edges": state["edges"],
        "duration_seconds": round(duration, 3),
        "cleanup_succeeded": state["cleanup_succeeded"],
        "fixture_unchanged": state["fixture_unchanged"],
    }


def contained_snapshot(
    root: Path, fixture: fixture_module.SyntheticFixture, state: dict, *, deadline: float
):
    """Only a builder-issued capability can reach the native preflight."""
    graph = Path(fixture_module.fixture_root(fixture))
    resources.require(fixture.task_root == str(root), "MA fixture task identity mismatch")
    sandbox_profile = preflight.run_preflight(
        root,
        graph,
        root / "producer",
        Path(sys.base_prefix).resolve(),
        state,
        deadline=deadline,
    )
    resources.require(state.get("preflight_complete") is True, "MA native preflight incomplete")
    producer = local_provision.producer_interpreter(root)
    # Preserve the venv spelling, while the sandbox also grants its verified base.
    state["producer_attempted"] = True
    return preflight.execute(
        root,
        "ma-snapshot",
        [
            "/usr/bin/sandbox-exec",
            "-f",
            str(sandbox_profile),
            str(producer),
            "-I",
            "-B",
            "-m",
            "matryca_plumber.graph_gateway",
            "snapshot",
            "--graph-root",
            str(graph),
            "--expect-descriptor-sha256",
            profile.DESCRIPTOR_SHA256,
        ],
        deadline=deadline,
        seconds=profile.MAX_SECONDS,
        stdout_limit=profile.MAX_STDOUT,
        stderr_limit=profile.MAX_STDERR,
    )


def run_local(root: Path) -> dict:
    started = time.monotonic()
    inputs, wheel = local_provision.verified_local_inputs(root)
    state: dict = {
        "exit_class": "run_refused",
        "nodes": 0,
        "edges": 0,
        "cleanup_succeeded": True,
        "fixture_unchanged": False,
        "complete": False,
    }
    # This exclusive marker makes a local run one-shot, even if preflight fails.
    with (root / "artifacts/local-run.started").open("xb"):
        pass
    graph, before = None, None
    try:
        manifest = resources.strict_json(
            resources.owner_resource(wheel, inputs, "fixture-manifest.json")
        )
        golden = resources.strict_json(
            resources.owner_resource(wheel, inputs, "golden/topology.result.json")
        )
        fixture = fixture_builder.build_fixture(root, wheel, inputs, manifest)
        graph = Path(fixture_module.fixture_root(fixture))
        before = resources.fixture_ledger(graph)
        provision.write_json(root / "artifacts/ma-fixture-before.json", before)
        result = contained_snapshot(root, fixture, state, deadline=started + 150)
        mapped = mapping.snapshot_from_bytes(result.stdout)
        document = resources.strict_json(result.stdout)
        resources.require(
            document["topology"]["result"] == golden, "MA authenticated golden mismatch"
        )
        resources.require(
            mapped.provenance.producer_source == inputs["source_commit"]
            and mapped.provenance.producer_artifact_sha256 == inputs["wheel"]["sha256"],
            "MA mapped producer binding mismatch",
        )
        state.update(
            nodes=len(mapped.topology.nodes),
            edges=len(mapped.topology.edges),
            exit_class="pass",
            complete=True,
        )
    except BaseException as error:
        state["error_class"] = type(error).__name__
        if state.get("cleanup_succeeded") is False:
            state["exit_class"] = "cleanup_uncertain"
        elif isinstance(error, preflight.PreflightRefused):
            state["exit_class"] = "preflight_refused"
        elif isinstance(error, preflight.CleanupUncertain):
            state["exit_class"] = "cleanup_uncertain"
            state["cleanup_succeeded"] = False
        else:
            state["exit_class"] = "integrity_failure"
        raise
    finally:
        if graph is not None and before is not None:
            try:
                after = resources.fixture_ledger(graph)
                provision.write_json(root / "artifacts/ma-fixture-after.json", after)
                state["fixture_unchanged"] = before == after
            except BaseException as error:
                state["fixture_after_error"] = type(error).__name__
        state["complete"] = (
            state["complete"] and state["fixture_unchanged"] and state["cleanup_succeeded"]
        )
        if not state["complete"] and state["exit_class"] == "pass":
            state["exit_class"] = "integrity_failure"
        duration = round(time.monotonic() - started, 3)
        state["duration_seconds"] = duration
        provision.write_json(root / "artifacts/local-run.json", state)
        print(json.dumps(public_report(state, duration), sort_keys=True), flush=True)
    return state


if __name__ == "__main__":
    try:
        outcome = run_local(local_provision.parse_root(sys.argv[1:]))
    except Exception:
        # The detailed exception remains private; do not emit paths or names.
        raise SystemExit(1) from None
    raise SystemExit(0 if outcome["complete"] else 1)
