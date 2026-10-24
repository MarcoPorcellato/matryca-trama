"""Hosted-only alpha.3 experiment on an authenticated disposable synthetic fixture."""

from __future__ import annotations

import argparse
import copy
from dataclasses import asdict
import hashlib
import json
import os
import platform
import sys
from importlib import metadata
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import process_boundary  # noqa: E402 - admit only the resolved sibling directory first.
import resources  # noqa: E402 - admit only the resolved sibling directory first.
import validation  # noqa: E402 - admit only the resolved sibling directory first.
import fixture_builder  # noqa: E402
from trama_core.graph_values import GraphGatewayError, GraphSnapshot  # noqa: E402
from trama_plumber_client import adapter as client_module  # noqa: E402
from trama_plumber_client import _mapping as client_mapping  # noqa: E402

for module in (process_boundary, resources, validation, fixture_builder):
    resources.require(
        Path(module.__file__).resolve() == HERE / (module.__name__ + ".py")
        and Path(module.__spec__.origin).resolve() == Path(module.__file__).resolve(),
        "qualification sibling origin mismatch",
    )

for module, package, filename in (
    (client_module, "plumber-client", "adapter.py"),
    (client_mapping, "plumber-client", "_mapping.py"),
):
    expected = (
        HERE.parents[1] / "packages" / package / "src/trama_plumber_client" / filename
    )
    resources.require(
        Path(module.__file__).resolve() == expected
        and Path(module.__spec__.origin).resolve() == expected,
        "qualification client module origin mismatch",
    )


def write_json(path: Path, value: object) -> None:
    raw = (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()
    resources.require(len(raw) <= 65_536, "receipt byte ceiling exceeded")
    with path.open("xb") as stream:
        stream.write(raw)


def retain(
    root: Path,
    label: str,
    result: process_boundary.ProcessResult | process_boundary.ProcessFailure,
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
        resources.require(
            code == expected_error, "negative-control error mismatch: " + str(code)
        )
        evidence["expected_negative"] = code
        return evidence
    except BaseException as error:
        captured = getattr(error, "process_evidence", None)
        if isinstance(captured, process_boundary.ProcessFailure):
            try:
                retain(root, label, captured)
            except BaseException as retention_error:
                error.add_note(
                    "Evidence retention failed: " + type(retention_error).__name__
                )
        raise
    evidence = retain(root, label, result)
    resources.require(expected_exit == 0, "negative control unexpectedly succeeded")
    resources.require(
        not result.stderr and result.cleanup_succeeded,
        "positive process stderr/cleanup rejected",
    )
    return resources.strict_json(result.stdout)


def invoke_client(
    root: Path, label: str, client, *, graph: Path
) -> tuple[dict, GraphSnapshot | None]:
    """Retain existing reader results after termination, without a second owner."""
    captured = []
    calls = 0

    def retain_call(argv, **options):
        nonlocal calls
        calls += 1
        resources.require(calls == 1, "client retried an invocation")
        if label == "snapshot":
            resources.require(
                argv[argv.index("--graph-root") + 1] == str(graph),
                "client did not canonicalize the positive alias",
            )
        try:
            result = process_boundary.run_process(argv, **options)
        except BaseException as error:
            evidence = (
                error
                if isinstance(error, process_boundary.ProcessFailure)
                else getattr(error, "process_evidence", None)
            )
            if isinstance(evidence, process_boundary.ProcessFailure):
                try:
                    retain(root, label, evidence)
                except BaseException as retention_error:
                    error.add_note(
                        "Evidence retention failed: " + type(retention_error).__name__
                    )
            raise
        captured.append(result)
        retain(root, label, result)
        return result

    # Only the call site's reference is traced. The existing package reader
    # remains the sole lifecycle owner and runs exactly once, unchanged.
    with patch.object(client_module, "run_process", side_effect=retain_call):
        mapped = client.snapshot() if label == "snapshot" else client.describe()
    resources.require(calls == len(captured) == 1, "client invocation evidence absent")
    return resources.strict_json(captured[0].stdout), mapped


def differential_cases(document: dict, schemas: dict) -> int:
    """Evidence of agreement on these cases, never schema equivalence."""
    cases = [(copy.deepcopy(document), True)]
    for path, replacement in (
        (("read", "schema_version"), True),
        (("topology", "session", "schema_version"), 2),
        (("topology", "result", "nodes", 0, "ordinal"), -1),
        (("topology", "result", "nodes", 0, "kind"), "unknown"),
        (("topology", "result", "edges", 0, "kind"), "unknown"),
    ):
        changed = copy.deepcopy(document)
        cursor = changed
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = replacement
        cases.append((changed, False))
    changed = copy.deepcopy(document)
    changed["topology"]["result"]["unexpected"] = "not permitted"
    cases.append((changed, False))
    for value, expected in cases:
        owner_pass = mapper_pass = True
        try:
            for name in ("read", "topology"):
                validation.owner_validate(value[name], schemas[name])
        except resources.QualificationFailure:
            owner_pass = False
        try:
            client_mapping.snapshot_from_bytes(json.dumps(value).encode())
        except GraphGatewayError:
            mapper_pass = False
        resources.require(
            owner_pass is expected and mapper_pass is expected,
            "owner-schema/consumer differential disagreement",
        )
    return len(cases)


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
            platform.python_version() == inputs["versions"]["python"],
            "exact runtime mismatch",
        )
        resources.require(
            (platform.system(), platform.machine())
            in (("Linux", "x86_64"), ("Darwin", "arm64")),
            "qualification platform mismatch",
        )

        def normalize(value: str) -> str:
            return value.lower().replace("_", "-")

        installed = {
            normalize(item.metadata["Name"]): item.version
            for item in metadata.distributions()
        }
        resources.require(
            installed == inputs["consumer_distributions"],
            "consumer distribution identity mismatch",
        )
        wheel = (
            root / "downloads" / inputs["wheel"]["sha256"] / inputs["wheel"]["filename"]
        )
        resources.verify_file(wheel, inputs["wheel"]["sha256"], inputs["wheel"]["size"])
        provision = resources.strict_json(
            (root / "artifacts" / "provision.json").read_bytes()
        )
        resources.require(
            provision["complete"] is True
            and provision["source_commit"] == inputs["source_commit"]
            and provision["producer_wheel_sha256"] == inputs["wheel"]["sha256"]
            and provision["consumer_startup_check"] == "pass-before-first-start",
            "provisioning evidence mismatch",
        )
        attestation = resources.strict_json(
            (root / "artifacts" / "attestation.json").read_bytes()
        )
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
        fixture = fixture_builder.build_fixture(root, wheel, inputs, fixture_manifest)
        graph = Path(fixture.canonical_root)
        alias = Path(fixture.input_alias)
        resources.require(
            str(alias) != os.path.realpath(alias),
            "noncanonical alias was not exercised",
        )
        before = resources.fixture_ledger(graph)
        write_json(root / "artifacts" / "fixture-before.json", before)
        producer = str(root / "producer" / "bin" / "python")
        digest = inputs["resources"]["descriptor.json"]
        client = client_module.PlumberClientAdapter(
            producer, fixture, expected_resolved_python=os.path.realpath(producer)
        )
        describe, _ = invoke_client(root, "describe", client, graph=graph)
        state["invocations"].append("describe")
        resources.require(
            set(describe) == {"descriptor", "descriptor_sha256"}
            and describe["descriptor"] == descriptor
            and describe["descriptor_sha256"] == digest,
            "describe binding mismatch",
        )
        snapshot, mapped = invoke_client(root, "snapshot", client, graph=graph)
        state["invocations"].append("snapshot")
        canaries = [
            item["value"] for item in fixture_manifest["privacy_canaries"].values()
        ]
        validation.validate_snapshot(
            snapshot, descriptor, digest, schemas, golden, inputs["versions"], canaries
        )
        resources.require(isinstance(mapped, GraphSnapshot), "domain snapshot absent")
        resources.require(
            [asdict(node) for node in mapped.topology.nodes] == golden["nodes"]
            and [
                {**asdict(edge), "kind": "reference"} for edge in mapped.topology.edges
            ]
            == golden["edges"]
            and mapped.topology.id == golden["topology_id"]
            and mapped.identity.graph_id == snapshot["read"]["graph_id"]
            and mapped.identity.session_id == snapshot["read"]["session"]["id"]
            and mapped.identity.source_revision == snapshot["read"]["source_revision"]
            and mapped.provenance.producer_source == inputs["source_commit"]
            and mapped.provenance.producer_artifact_sha256 == inputs["wheel"]["sha256"],
            "mapped domain result differs from authenticated evidence",
        )
        state["owner_schema_differential_cases"] = differential_cases(snapshot, schemas)
        state["client_domain_mapping"] = "pass"
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
        oversized = fixture_builder.build_file_bound_control(root)
        bound_before = fixture_builder.file_bound_ledger(oversized)
        try:
            invoke(
                root,
                "file-bound",
                validation.snapshot_argv(producer, oversized, digest),
                expected_exit=5,
                expected_error="bounds_exceeded",
            )
            state["invocations"].append("file-bound")
        finally:
            bound_after = fixture_builder.file_bound_ledger(oversized)
            state["file_bound_control"] = {"before": bound_before, "after": bound_after}
            resources.require(
                bound_before == bound_after, "file-bound synthetic fixture changed"
            )
        state["complete"] = True
    except BaseException as error:
        state["error"] = type(error).__name__
        state["error_detail"] = resources.sanitize(
            str(error).encode()[:512],
            replacements={
                str(root): "<qualification-root>",
                str(Path.home()): "<home>",
            },
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
        resources.require(
            state["fixture_unchanged"] or graph is None, "synthetic fixture changed"
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(
            "Synthetic qualification failed: " + type(error).__name__, file=sys.stderr
        )
        raise SystemExit(1) from None
