"""Hosted-only alpha.3 experiment on an authenticated disposable synthetic fixture."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import sys
import tempfile
from importlib import metadata
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import process_boundary  # noqa: E402 - admit only the resolved sibling directory first.
import resources  # noqa: E402 - admit only the resolved sibling directory first.
import validation  # noqa: E402 - admit only the resolved sibling directory first.

for module in (process_boundary, resources, validation):
    resources.require(
        Path(module.__file__).resolve() == HERE / (module.__name__ + ".py")
        and Path(module.__spec__.origin).resolve() == Path(module.__file__).resolve(),
        "qualification sibling origin mismatch",
    )


def write_json(path: Path, value: object) -> None:
    raw = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    resources.require(len(raw) <= 65_536, "receipt byte ceiling exceeded")
    with path.open("xb") as stream:
        stream.write(raw)


def retain(
    root: Path, label: str, result: process_boundary.ProcessResult | process_boundary.ProcessFailure
) -> dict:
    replacements = {
        str(root): "<qualification-root>",
        str(HERE.parents[1]): "<checkout>",
        str(Path.home()): "<home>",
    }
    for name in ("RUNNER_TEMP", "GITHUB_WORKSPACE", "USER", "LOGNAME"):
        value = os.environ.get(name)
        if value and len(value) >= 3:
            replacements[value] = "<" + name.lower() + ">"
    evidence = {
        "returncode": result.returncode,
        "child_reaped": result.child_reaped,
        "signal_errno": getattr(result, "signal_errno", None),
        "group_probe_errno": result.group_probe_errno,
        "cleanup_succeeded": result.cleanup_succeeded,
        "observations": result.observations,
        "events": result.events,
        "reason": getattr(result, "reason", None),
        "cleanup_exception": type(result.cleanup_exception).__name__
        if result.cleanup_exception is not None
        else None,
    }
    for name in ("stdout", "stderr"):
        raw = getattr(result, name)
        evidence[name + "_sha256"] = hashlib.sha256(raw).hexdigest()
        evidence[name + "_bytes"] = len(raw)
        with (root / "artifacts" / (label + "." + name + ".txt")).open("xb") as stream:
            stream.write(resources.sanitize(raw, replacements=replacements))
    write_json(root / "artifacts" / (label + ".lifecycle.json"), evidence)
    return evidence


def invoke(
    root: Path,
    label: str,
    argv: list[str],
    *,
    expected_exit: int = 0,
    expected_error: str | None = None,
) -> dict:
    try:
        result = process_boundary.run_process(argv, timeout_seconds=180)
    except process_boundary.ProcessFailure as error:
        evidence = retain(root, label, error)
        resources.require(error.cleanup_succeeded, "process cleanup is uncertain")
        if expected_exit == 0 or error.reason != "nonzero_exit":
            raise
        resources.require(
            error.returncode == expected_exit and not error.stdout,
            "negative-control exit/output mismatch",
        )
        try:
            value = resources.strict_json(error.stderr)
            code = value.get("error", "unclassified")
        except resources.QualificationFailure:
            code = "unclassified"
        resources.require(code == expected_error, "negative-control error mismatch: " + str(code))
        evidence["expected_negative"] = code
        return evidence
    except BaseException as error:
        captured = getattr(error, "process_evidence", None)
        if isinstance(captured, process_boundary.ProcessFailure):
            try:
                retain(root, label, captured)
            except BaseException as retention_error:
                error.add_note("Evidence retention failed: " + type(retention_error).__name__)
        raise
    evidence = retain(root, label, result)
    resources.require(expected_exit == 0, "negative control unexpectedly succeeded")
    resources.require(
        not result.stderr and result.cleanup_succeeded, "positive process stderr/cleanup rejected"
    )
    return resources.strict_json(result.stdout)


def make_fixture(root: Path, wheel: Path, inputs: dict, manifest: dict) -> Path:
    parent = root / "synthetic"
    parent.mkdir()
    graph = Path(tempfile.mkdtemp(prefix="graph-", dir=parent)).resolve()
    files = manifest["files"]
    resources.require(0 < len(files) <= 1024, "fixture manifest file bound rejected")
    for logical, expected in files.items():
        path = PurePosixPath(logical)
        resources.require(
            not path.is_absolute()
            and ".." not in path.parts
            and path.parts[0] in ("pages", "journals")
            and path.suffix == ".md",
            "fixture path rejected",
        )
        raw = resources.read_member(wheel, inputs["resource_prefix"] + "fixtures/" + logical)
        resources.require(
            hashlib.sha256(raw).hexdigest() == expected["sha256"], "fixture digest mismatch"
        )
        destination = graph.joinpath(*path.parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as stream:
            stream.write(raw)
    return graph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    inputs = resources.strict_json((HERE / "inputs.json").read_bytes())
    state = {
        "complete": False,
        "scope": inputs["scope"],
        "producer_source": inputs["source_commit"],
        "producer_wheel_sha256": inputs["wheel"]["sha256"],
        "consumer_workflow_sha": os.environ.get("GITHUB_SHA"),
        "system": platform.system(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "network_isolation": False,
        "invocations": [],
        "fixture_unchanged": False,
    }
    graph = None
    before = None
    try:
        resources.require(
            os.environ.get("GITHUB_ACTIONS") == "true"
            and os.environ.get("GITHUB_REPOSITORY") == "MarcoPorcellato/matryca-trama",
            "real producer probe is hosted-only",
        )
        resources.require(
            platform.python_version() == inputs["versions"]["python"], "exact runtime mismatch"
        )
        resources.require(
            (platform.system(), platform.machine()) in (("Linux", "x86_64"), ("Darwin", "arm64")),
            "qualification platform mismatch",
        )

        def normalize(value: str) -> str:
            return value.lower().replace("_", "-")

        installed = {
            normalize(item.metadata["Name"]): item.version for item in metadata.distributions()
        }
        resources.require(
            installed == inputs["consumer_distributions"], "consumer distribution identity mismatch"
        )
        wheel = root / "downloads" / inputs["wheel"]["sha256"] / inputs["wheel"]["filename"]
        resources.verify_file(wheel, inputs["wheel"]["sha256"], inputs["wheel"]["size"])
        provision = resources.strict_json((root / "artifacts" / "provision.json").read_bytes())
        resources.require(
            provision["complete"] is True
            and provision["source_commit"] == inputs["source_commit"]
            and provision["producer_wheel_sha256"] == inputs["wheel"]["sha256"]
            and provision["consumer_startup_check"] == "pass-before-first-start",
            "provisioning evidence mismatch",
        )
        attestation = resources.strict_json((root / "artifacts" / "attestation.json").read_bytes())
        resources.require(
            type(attestation["returncode"]) is int
            and attestation["returncode"] == 0
            and attestation["cleanup_succeeded"] is True
            and attestation["child_reaped"] is True,
            "successful provenance verification record absent",
        )
        descriptor_raw = resources.owner_resource(wheel, inputs, "descriptor.json")
        descriptor = resources.strict_json(descriptor_raw)
        schemas = {
            key: resources.strict_json(
                resources.owner_resource(
                    wheel,
                    inputs,
                    "schemas/plumber.graph."
                    + ("read" if key == "read" else "topology")
                    + ".v1.json",
                )
            )
            for key in ("read", "topology")
        }
        golden = resources.strict_json(
            resources.owner_resource(wheel, inputs, "golden/topology.result.json")
        )
        fixture_manifest = resources.strict_json(
            resources.owner_resource(wheel, inputs, "fixture-manifest.json")
        )
        graph = make_fixture(root, wheel, inputs, fixture_manifest)
        alias = root / "input-alias"
        alias.symlink_to(graph, target_is_directory=True)
        resources.require(
            str(alias) != os.path.realpath(alias), "noncanonical alias was not exercised"
        )
        before = resources.fixture_ledger(graph)
        write_json(root / "artifacts" / "fixture-before.json", before)
        producer = str(root / "producer" / "bin" / "python")
        digest = inputs["resources"]["descriptor.json"]
        describe = invoke(
            root,
            "describe",
            [producer, "-I", "-B", "-m", "matryca_plumber.graph_gateway", "describe"],
        )
        state["invocations"].append("describe")
        resources.require(
            set(describe) == {"descriptor", "descriptor_sha256"}
            and describe["descriptor"] == descriptor
            and describe["descriptor_sha256"] == digest,
            "describe binding mismatch",
        )
        positive = validation.snapshot_argv(producer, alias, digest)
        resources.require(
            positive[positive.index("--graph-root") + 1] == str(graph),
            "positive alias canonicalization failed",
        )
        snapshot = invoke(root, "snapshot", positive)
        state["invocations"].append("snapshot")
        canaries = [item["value"] for item in fixture_manifest["privacy_canaries"].values()]
        validation.validate_snapshot(
            snapshot, descriptor, digest, schemas, golden, inputs["versions"], canaries
        )
        state["positive_alias_canonicalized"] = True
        state["snapshot_bindings"] = {
            "graph_id": snapshot["read"]["graph_id"],
            "session_id": snapshot["read"]["session"]["id"],
            "source_revision": snapshot["read"]["source_revision"],
        }
        invoke(
            root,
            "wrong-descriptor",
            validation.snapshot_argv(producer, alias, "0" * 64),
            expected_exit=3,
            expected_error="expectation_mismatch",
        )
        state["invocations"].append("wrong-descriptor")
        invoke(
            root,
            "raw-alias",
            validation.snapshot_argv(producer, alias, digest, canonicalize=False),
            expected_exit=4,
            expected_error="source_rejected",
        )
        state["invocations"].append("raw-alias")
        state["complete"] = True
    except BaseException as error:
        state["error"] = type(error).__name__
        state["error_detail"] = resources.sanitize(
            str(error).encode()[:512],
            replacements={str(root): "<qualification-root>", str(Path.home()): "<home>"},
        ).decode()
        raise
    finally:
        if graph is not None and before is not None:
            try:
                after = resources.fixture_ledger(graph)
                write_json(root / "artifacts" / "fixture-after.json", after)
                state["fixture_unchanged"] = before == after
            except BaseException as error:
                state["fixture_after_error"] = type(error).__name__
                state["fixture_unchanged"] = False
            state["complete"] = state["complete"] and state["fixture_unchanged"]
        write_json(root / "artifacts" / "receipt.json", state)
        resources.require(state["fixture_unchanged"] or graph is None, "synthetic fixture changed")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Synthetic qualification failed: " + type(error).__name__, file=sys.stderr)
        raise SystemExit(1) from None
