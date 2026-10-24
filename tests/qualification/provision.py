"""Provision disposable, hash-bound qualification environments, never a user graph."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import sys
import zipfile
from email.parser import BytesParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import process_boundary  # noqa: E402 - admit only the resolved sibling directory first.
import resources  # noqa: E402 - admit only the resolved sibling directory first.

for module in (process_boundary, resources):
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


def disk_admit(root: Path) -> None:
    hosted = os.environ.get("GITHUB_ACTIONS") == "true"
    # Local Mac admission retains 20 GB plus reserve. Disposable hosted capacity
    # is checked independently for the 1 GiB footprint plus 1 GiB reserve.
    minimum = 2 * 1_073_741_824 if hosted else 20_000_000_000 + 1_073_741_824
    resources.require(
        shutil.disk_usage(root).free >= minimum,
        "disk floor plus reserve unavailable",
    )
    size = 0
    for parent, _, files in os.walk(root, followlinks=False):
        size += sum((Path(parent) / name).lstat().st_size for name in files)
    resources.require(size <= 1_073_741_824, "task footprint ceiling exceeded")


def save_result(
    root: Path, label: str, result: process_boundary.ProcessResult | process_boundary.ProcessFailure
) -> None:
    artifacts = root / "artifacts"
    replacements = {
        str(root): "<qualification-root>",
        str(HERE.parents[1]): "<checkout>",
        str(Path.home()): "<home>",
    }
    for name in ("RUNNER_TEMP", "GITHUB_WORKSPACE", "USER", "LOGNAME"):
        value = os.environ.get(name)
        if value and len(value) >= 3:
            replacements[value] = "<" + name.lower() + ">"
    for stream in ("stdout", "stderr"):
        raw = getattr(result, stream)
        with (artifacts / (label + "." + stream + ".txt")).open("xb") as file:
            file.write(resources.sanitize(raw, replacements=replacements))
    write_json(
        artifacts / (label + ".json"),
        {
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
            "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(result.stderr).hexdigest(),
        },
    )


def run_tool(
    root: Path, label: str, argv: list[str], *, environment: dict[str, str] | None = None
) -> process_boundary.ProcessResult:
    try:
        result = process_boundary.run_process(argv, timeout_seconds=180, environment=environment)
    except process_boundary.ProcessFailure as error:
        save_result(root, label, error)
        raise
    except BaseException as error:
        captured = getattr(error, "process_evidence", None)
        if isinstance(captured, process_boundary.ProcessFailure):
            try:
                save_result(root, label, captured)
            except BaseException as retention_error:
                error.add_note("Evidence retention failed: " + type(retention_error).__name__)
        raise
    save_result(root, label, result)
    disk_admit(root)
    return result


def download(root: Path, artifact: dict) -> Path:
    directory = root / "downloads" / artifact["sha256"]
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / artifact["filename"]
    if not path.exists():
        run_tool(
            root,
            "download-" + artifact["sha256"][:16],
            [
                "curl",
                "--disable",
                "--fail",
                "--silent",
                "--show-error",
                "--location",
                "--proto",
                "=https",
                "--proto-redir",
                "=https",
                "--max-time",
                "120",
                "--max-filesize",
                str(artifact["size"]),
                "--output",
                str(path),
                artifact["url"],
            ],
        )
    resources.verify_file(path, artifact["sha256"], artifact["size"])
    return path


def inspect_dependency(wheel: Path, artifact: dict) -> dict:
    directory = artifact["name"].replace("-", "_") + "-" + artifact["version"] + ".dist-info/"
    raw = resources.read_member(wheel, directory + "METADATA")
    metadata = BytesParser().parsebytes(raw)

    def normalize(value: str) -> str:
        return value.lower().replace("_", "-")

    resources.require(
        normalize(metadata["Name"]) == normalize(artifact["name"])
        and metadata["Version"] == artifact["version"],
        "wheel metadata identity mismatch",
    )
    declared = metadata.get("License-Expression") or metadata.get("License")
    resources.require(declared == artifact["license"], "wheel license declaration mismatch")
    with zipfile.ZipFile(wheel) as archive:
        names = [
            name
            for name in archive.namelist()
            if name.startswith(directory)
            and ("license" in name.lower() or name.lower().endswith("copying"))
            and not name.endswith("/")
        ]
    resources.require(bool(names) and len(names) <= 8, "wheel license notice absent/unbounded")
    notices = {
        name: hashlib.sha256(resources.read_member(wheel, name, limit=262_144)).hexdigest()
        for name in names
    }
    return {
        "name": artifact["name"],
        "version": artifact["version"],
        "sha256": artifact["sha256"],
        "size": artifact["size"],
        "license": declared,
        "metadata_sha256": hashlib.sha256(raw).hexdigest(),
        "notices": notices,
    }


def make_environment(root: Path, name: str) -> Path:
    target = root / name
    resources.require(not target.exists(), "environment is not fresh")
    run_tool(
        root,
        "venv-" + name,
        [sys.executable, "-I", "-B", "-m", "venv", "--without-pip", str(target)],
    )
    return target / "bin" / "python"


def install(root: Path, name: str, interpreter: Path, arguments: list[str]) -> None:
    uv = shutil.which("uv")
    resources.require(uv is not None, "reviewed environment manager unavailable")
    run_tool(
        root,
        "install-" + name,
        [
            uv,
            "--no-config",
            "--cache-dir",
            str(root / "cache"),
            "--no-progress",
            "pip",
            "install",
            "--quiet",
            "--python",
            str(interpreter),
            "--no-python-downloads",
            "--only-binary",
            ":all:",
            "--no-deps",
            "--link-mode",
            "copy",
            *arguments,
        ],
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--producer", action="store_true")
    args = parser.parse_args()
    root = args.root.absolute()
    resources.require(root.parent.resolve() == root.parent, "provisioning parent must be canonical")
    root.mkdir(parents=False, exist_ok=False)
    (root / "artifacts").mkdir()
    inputs = resources.strict_json((HERE / "inputs.json").read_bytes())
    state = {
        "complete": False,
        "scope": inputs["scope"],
        "system": platform.system(),
        "machine": platform.machine(),
        "python": platform.python_version(),
        "consumer": [],
    }
    try:
        disk_admit(root)
        resources.require(
            (platform.system(), platform.machine()) in (("Linux", "x86_64"), ("Darwin", "arm64")),
            "unsupported qualification row",
        )
        if args.producer:
            resources.require(
                os.environ.get("GITHUB_ACTIONS") == "true"
                and os.environ.get("GITHUB_REPOSITORY") == "MarcoPorcellato/matryca-trama",
                "real producer provisioning is hosted-only",
            )
            resources.require(
                platform.python_version() == inputs["versions"]["python"],
                "exact probe runtime mismatch",
            )
            wheel = download(root, inputs["wheel"])
            gh = shutil.which("gh")
            resources.require(gh is not None, "attestation verifier unavailable")
            environment = {
                "PATH": os.environ.get("PATH", os.defpath),
                "GH_PROMPT_DISABLED": "1",
                "HOME": str(Path.home()),
            }
            if "GH_TOKEN" in os.environ:
                environment["GH_TOKEN"] = os.environ["GH_TOKEN"]
            run_tool(root, "attestation-version", [gh, "--version"], environment=environment)
            capabilities = run_tool(
                root,
                "attestation-capabilities",
                [gh, "attestation", "verify", "--help"],
                environment=environment,
            )
            resources.require(
                all(
                    flag in capabilities.stdout
                    for flag in (
                        b"--source-digest",
                        b"--source-ref",
                        b"--cert-identity",
                        b"--deny-self-hosted-runners",
                    )
                ),
                "runner verifier lacks required policy flags",
            )
            run_tool(
                root,
                "attestation",
                [
                    gh,
                    "attestation",
                    "verify",
                    str(wheel),
                    "--repo",
                    inputs["repository"],
                    "--source-digest",
                    inputs["source_commit"],
                    "--source-ref",
                    inputs["source_ref"],
                    "--cert-identity",
                    "https://" + inputs["signer_workflow"] + "@" + inputs["source_ref"],
                    "--deny-self-hosted-runners",
                    "--format",
                    "json",
                ],
                environment=environment,
            )
            raw = resources.owner_resource(wheel, inputs, "requirements-og-v1-parser-1.9.0.txt")
            requirements = root / "producer-requirements.txt"
            with requirements.open("xb") as file:
                file.write(raw)
            producer = make_environment(root, "producer")
            install(
                root,
                "producer-closure",
                producer,
                [
                    "--require-hashes",
                    "--default-index",
                    "https://pypi.org/simple",
                    "--requirements",
                    str(requirements),
                ],
            )
            install(root, "producer-wheel", producer, ["--no-index", str(wheel)])
            state["producer_wheel_sha256"] = inputs["wheel"]["sha256"]
            state["source_commit"] = inputs["source_commit"]
        selected = [
            artifact
            for artifact in inputs["consumer_artifacts"]
            if artifact["platform"] in ("any", platform.system())
        ]
        resources.require(
            len(selected) == 6 and len({artifact["name"] for artifact in selected}) == 6,
            "consumer wheel matrix mismatch",
        )
        wheelhouse = root / "consumer-wheels"
        wheelhouse.mkdir()
        for artifact in selected:
            wheel = download(root, artifact)
            state["consumer"].append(inspect_dependency(wheel, artifact))
            shutil.copyfile(wheel, wheelhouse / artifact["filename"])
        consumer = make_environment(root, "consumer")
        install(
            root,
            "consumer",
            consumer,
            [
                "--require-hashes",
                "--no-index",
                "--find-links",
                str(wheelhouse),
                "--requirements",
                str(HERE / "requirements.txt"),
            ],
        )
        site = (
            consumer.parent.parent
            / "lib"
            / ("python" + ".".join(platform.python_version_tuple()[:2]))
            / "site-packages"
        )
        # This is a filesystem-only check in the provisioning interpreter. No
        # consumer interpreter has started since dependency installation.
        resources.check_site_packages(site, inputs["consumer_import_roots"])
        state["consumer_startup_check"] = "pass-before-first-start"
        if not args.producer:
            run_tool(
                root,
                "unit",
                [str(consumer), "-I", "-B", "-m", "unittest", "discover", "-s", str(HERE), "-q"],
            )
        disk_admit(root)
        state["complete"] = True
    except BaseException as error:
        state["error"] = type(error).__name__
        state["error_detail"] = resources.sanitize(
            str(error).encode()[:512],
            replacements={str(root): "<qualification-root>", str(Path.home()): "<home>"},
        ).decode()
        raise
    finally:
        write_json(root / "artifacts" / "provision.json", state)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Qualification provisioning failed: " + type(error).__name__, file=sys.stderr)
        raise SystemExit(1) from None
