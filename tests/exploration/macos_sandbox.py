"""One hosted synthetic sandbox measurement, never compatibility qualification."""

from __future__ import annotations

import argparse
import errno
import hashlib
from importlib import metadata
import os
from pathlib import Path
import platform
import socket
import sys
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
QUALIFICATION = HERE.parent / "qualification"
sys.path.insert(0, str(QUALIFICATION))
import process_boundary  # noqa: E402
import provision  # noqa: E402
import resources  # noqa: E402

for module in (process_boundary, provision, resources):
    if (
        Path(module.__file__).resolve() != QUALIFICATION / (module.__name__ + ".py")
        or Path(module.__spec__.origin).resolve() != Path(module.__file__).resolve()
    ):
        raise RuntimeError("exploration sibling origin mismatch")


class Inconclusive(RuntimeError):
    """A retained measurement limitation, not a passed qualification gate."""


def require_hosted_root(root: Path) -> None:
    resources.require(
        os.environ.get("GITHUB_ACTIONS") == "true"
        and os.environ.get("GITHUB_REPOSITORY") == "MarcoPorcellato/matryca-trama"
        and os.environ.get("GITHUB_RUN_ATTEMPT") == "1",
        "exploration is hosted-only and has no rerun authority",
    )
    expected = Path(os.path.realpath(os.environ["RUNNER_TEMP"])) / "trama-og-m3"
    resources.require(
        root == expected and root == root.resolve() and not root.is_symlink(),
        "exploration root is not the task-owned canonical root",
    )
    resources.require(root.is_dir(), "provisioned exploration root absent")


def require_cleanup(
    result: process_boundary.ProcessResult
    | process_boundary.ProcessFailure
    | SimpleNamespace,
) -> None:
    resources.require(
        result.child_reaped is True
        and result.cleanup_succeeded is True
        and result.group_probe_errno == errno.ESRCH
        and result.cleanup_exception is None
        and not result.events,
        "exploration cleanup is uncertain",
    )


def _canary_shape(value: object) -> bool:
    if type(value) is not dict or set(value) != {
        "write_succeeded",
        "network_succeeded",
        "write_errno",
        "network_errno",
    }:
        return False
    for operation in ("write", "network"):
        success, error = value[operation + "_succeeded"], value[operation + "_errno"]
        if type(success) is not bool or type(error) is not int or error < 0:
            return False
        if success != (error == 0):
            return False
    return True


def classify_canaries(
    positive: dict, confined: dict, *, marker_unchanged: bool, accepted_connections: int
) -> str:
    if not _canary_shape(positive) or not _canary_shape(confined):
        return "INCONCLUSIVE"
    if not (positive["write_succeeded"] and positive["network_succeeded"]):
        return "INCONCLUSIVE"
    if confined["write_succeeded"] or confined["network_succeeded"]:
        return "OBSERVED_ALLOW"
    if (
        marker_unchanged is True
        and accepted_connections == 0
        and confined["write_errno"] in (errno.EPERM, errno.EACCES)
        and confined["network_errno"] in (errno.EPERM, errno.EACCES)
    ):
        return "OBSERVED_DENY"
    return "INCONCLUSIVE"


def check_startup_hooks(site: Path) -> None:
    resources.require(site.is_dir() and not site.is_symlink(), "producer site rejected")
    count = 0
    for path in site.iterdir():
        count += 1
        resources.require(
            count <= 1024 and not path.is_symlink(), "producer site bound/type"
        )
        resources.require(
            not path.name.endswith(".pth")
            and path.stem not in ("sitecustomize", "usercustomize"),
            "producer startup hook rejected",
        )


def invoke(root: Path, label: str, argv: list[str]) -> process_boundary.ProcessResult:
    try:
        result = provision.run_tool(root, label, argv)
    except process_boundary.ProcessFailure as error:
        require_cleanup(error)
        if error.reason == "nonzero_exit":
            raise Inconclusive(label + "_nonzero_exit") from error
        raise
    require_cleanup(result)
    if result.stderr:
        raise Inconclusive(label + "_launcher_or_child_stderr")
    return result


def accept_pending(listener: socket.socket) -> int:
    count = 0
    while count < 4:
        try:
            connection, _ = listener.accept()
        except BlockingIOError:
            return count
        with connection:
            count += 1
    raise RuntimeError("unexpected listener connection count")


def finish_fixture(
    root: Path, graph: Path | None, before: dict | None, state: dict
) -> None:
    errors: list[BaseException] = []
    if graph is not None and before is not None:
        try:
            after = resources.fixture_ledger(graph)
            provision.write_json(root / "artifacts/m3-fixture-after.json", after)
            state["fixture_unchanged"] = before == after
            resources.require(before == after, "synthetic fixture changed")
        except BaseException as error:
            state["fixture_after_error"] = type(error).__name__
            state["complete"] = False
            errors.append(error)
    try:
        provision.disk_admit(root)
    except BaseException as error:
        state["disk_error"] = type(error).__name__
        state["complete"] = False
        errors.append(error)
    try:
        provision.write_json(root / "artifacts/m3-receipt.json", state)
    except BaseException as error:
        errors.append(error)
    if errors:
        for additional in errors[1:]:
            errors[0].add_note(
                "Additional retention failure: " + type(additional).__name__
            )
        raise errors[0]


def canary_controls(root: Path, profile: Path, state: dict) -> None:
    compiler, sandbox = Path("/usr/bin/clang"), Path("/usr/bin/sandbox-exec")
    if not all(
        path.is_file() and os.access(path, os.X_OK) for path in (compiler, sandbox)
    ):
        raise Inconclusive("preinstalled_compiler_or_sandbox_unavailable")
    source = HERE / "macos_canary.c"
    state["canary_source_sha256"] = hashlib.sha256(source.read_bytes()).hexdigest()
    state["profile_sha256"] = hashlib.sha256(profile.read_bytes()).hexdigest()
    scratch = root / "canary"
    scratch.mkdir(exist_ok=False)
    binary, marker = scratch / "canary", scratch / "outside-marker"
    invoke(
        root,
        "m3-compile",
        [
            str(compiler),
            "-std=c11",
            "-Wall",
            "-Wextra",
            "-Werror",
            str(source),
            "-o",
            str(binary),
        ],
    )
    state["native_canary_sha256"] = hashlib.sha256(binary.read_bytes()).hexdigest()
    marker.write_bytes(b"baseline\n")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen(4)
        listener.setblocking(False)
        argv = [str(binary), str(marker), str(listener.getsockname()[1])]
        positive = resources.strict_json(invoke(root, "m3-positive", argv).stdout)
        connections = accept_pending(listener)
        if not (
            _canary_shape(positive)
            and positive["write_succeeded"]
            and positive["network_succeeded"]
            and connections == 1
            and marker.read_bytes() == b"m3-canary\n"
        ):
            raise Inconclusive("independent_unconfined_controls_failed")
        state["positive_canary"] = positive
        state["positive_connections"] = connections
        marker.write_bytes(b"baseline\n")
        before = resources.fixture_ledger(scratch)
        confined = resources.strict_json(
            invoke(
                root, "m3-confined", [str(sandbox), "-f", str(profile), *argv]
            ).stdout
        )
        connections = accept_pending(listener)
        after = resources.fixture_ledger(scratch)
        state["confined_canary"] = confined
        state["confined_connections"] = connections
        state["marker_unchanged"] = before == after
        state["os_canaries"] = classify_canaries(
            positive,
            confined,
            marker_unchanged=before == after,
            accepted_connections=connections,
        )
    if state["os_canaries"] != "OBSERVED_DENY":
        raise Inconclusive("candidate_profile_not_observed_deny")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    root = parser.parse_args().root.absolute()
    require_hosted_root(root)  # Before any graph read, import or producer launch.
    state = {
        "scope": "exploratory synthetic-only; non-qualifying",
        "complete": False,
        "os_canaries": "INCONCLUSIVE",
        "producer_result": "NOT_RUN",
        "network_isolation_claim": False,
        "system": platform.system(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "consumer_source": os.environ.get("GITHUB_SHA"),
        "runner_image": {
            key: os.environ.get(key, "")[:128] for key in ("ImageOS", "ImageVersion")
        },
    }
    graph, before = None, None
    primary_error: BaseException | None = None
    try:
        resources.require(
            (platform.system(), platform.machine(), platform.python_version())
            == ("Darwin", "arm64", "3.12.14"),
            "exploration runtime mismatch",
        )
        inputs = resources.strict_json((QUALIFICATION / "inputs.json").read_bytes())
        state["producer_source"] = inputs["source_commit"]
        state["producer_wheel_sha256"] = inputs["wheel"]["sha256"]
        provision.disk_admit(root)
        wheel = (
            root / "downloads" / inputs["wheel"]["sha256"] / inputs["wheel"]["filename"]
        )
        resources.verify_file(wheel, inputs["wheel"]["sha256"], inputs["wheel"]["size"])
        evidence = resources.strict_json(
            (root / "artifacts/provision.json").read_bytes()
        )
        resources.require(
            evidence["complete"] is True
            and evidence["consumer_startup_check"] == "pass-before-first-start"
            and evidence["source_commit"] == inputs["source_commit"]
            and evidence["producer_wheel_sha256"] == inputs["wheel"]["sha256"],
            "provisioning binding mismatch",
        )
        attestation = resources.strict_json(
            (root / "artifacts/attestation.json").read_bytes()
        )
        resources.require(
            attestation["returncode"] == 0, "provenance verification absent"
        )
        require_cleanup(SimpleNamespace(**attestation))

        def normalize(value: str) -> str:
            return value.lower().replace("_", "-")

        installed = {
            normalize(item.metadata["Name"]): item.version
            for item in metadata.distributions()
        }
        resources.require(
            installed == inputs["consumer_distributions"],
            "consumer environment mismatch",
        )
        check_startup_hooks(root / "producer/lib/python3.12/site-packages")
        import fixture_builder
        import validation

        for module in (fixture_builder, validation):
            resources.require(
                Path(module.__file__).resolve()
                == QUALIFICATION / (module.__name__ + ".py"),
                "fixture/validator source origin mismatch",
            )
        descriptor = resources.strict_json(
            resources.owner_resource(wheel, inputs, "descriptor.json")
        )
        manifest = resources.strict_json(
            resources.owner_resource(wheel, inputs, "fixture-manifest.json")
        )
        fixture = fixture_builder.build_fixture(root, wheel, inputs, manifest)
        graph = Path(fixture.canonical_root)
        before = resources.fixture_ledger(graph)
        provision.write_json(root / "artifacts/m3-fixture-before.json", before)
        profile = HERE / "macos-deny.sb"
        canary_controls(root, profile, state)
        producer = str(root / "producer/bin/python")
        argv = validation.snapshot_argv(
            producer, Path(fixture.input_alias), inputs["resources"]["descriptor.json"]
        )
        state["producer_result"] = "INCONCLUSIVE"
        result = invoke(
            root, "m3-producer", ["/usr/bin/sandbox-exec", "-f", str(profile), *argv]
        )
        document = resources.strict_json(result.stdout)
        schemas = {
            key: resources.strict_json(
                resources.owner_resource(
                    wheel, inputs, "schemas/plumber.graph." + key + ".v1.json"
                )
            )
            for key in ("read", "topology")
        }
        golden = resources.strict_json(
            resources.owner_resource(wheel, inputs, "golden/topology.result.json")
        )
        validation.validate_snapshot(
            document,
            descriptor,
            inputs["resources"]["descriptor.json"],
            schemas,
            golden,
            inputs["versions"],
            [item["value"] for item in manifest["privacy_canaries"].values()],
        )
        state["producer_result"] = "VALID_SYNTHETIC_RESULT"
        state["topology_result_matches_golden"] = True
        state["positive_alias_canonicalized"] = (
            str(fixture.input_alias) != argv[argv.index("--graph-root") + 1]
        )
        state["complete"] = True
    except Inconclusive as error:
        state["measurement_limitation"] = str(error)
        state["complete"] = True
    except BaseException as error:
        state["error"] = type(error).__name__
        primary_error = error
    finally:
        try:
            finish_fixture(root, graph, before, state)
        except BaseException as retention_error:
            if primary_error is None:
                raise
            primary_error.add_note(
                "Final retention failure: " + type(retention_error).__name__
            )
    if primary_error is not None:
        raise primary_error


def entrypoint() -> int:
    try:
        main()
    except BaseException:
        print(
            "Exploratory measurement failed; inspect retained sanitized evidence.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(entrypoint()) from None
