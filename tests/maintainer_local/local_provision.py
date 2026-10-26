"""Separate local-only provisioner; the hosted producer guard is unchanged."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import sys
from importlib.machinery import all_suffixes
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import local_support  # noqa: E402
import preflight  # noqa: E402

provision, resources = preflight.provision, preflight.resources
for module in (local_support, preflight):
    source, spec = module.__file__, module.__spec__
    if (
        not isinstance(source, str)
        or spec is None
        or not isinstance(spec.origin, str)
        or Path(source).resolve() != HERE / (module.__name__ + ".py")
        or Path(spec.origin).resolve() != Path(source).resolve()
    ):
        raise RuntimeError("MA local support origin mismatch")


def parse_root(argv: list[str]) -> Path:
    """The only selector is a task root, never a graph or optional bypass."""
    if len(argv) != 2 or argv[0] != "--root":
        raise local_support.LocalFailure("MA requires only --root and a task root")
    return Path(argv[1])


def check_startup(site: Path) -> None:
    """Inspect metadata before any post-install interpreter start."""
    if not site.is_dir() or site.is_symlink():
        raise local_support.LocalFailure("MA environment directory rejected")
    entries = 0
    customizations = {
        name + suffix
        for name in ("sitecustomize", "usercustomize")
        for suffix in ("", *all_suffixes())
    }
    for parent, directories, files in os.walk(site, followlinks=False):
        for name in directories + files:
            entries += 1
            path = Path(parent) / name
            mode = path.lstat().st_mode
            if (
                entries > 65_536
                or not (stat.S_ISREG(mode) or stat.S_ISDIR(mode))
                or name.endswith(".pth")
                or name in customizations
            ):
                raise local_support.LocalFailure("MA startup hook, link or entry bound rejected")


def environment_digest(site: Path) -> str:
    """Bind the freshly hash-installed closure without importing its modules."""
    check_startup(site)
    total = 0
    ledger = hashlib.sha256()
    for parent, directories, files in os.walk(site, followlinks=False):
        directories.sort()
        for name in sorted(files):
            path = Path(parent) / name
            metadata = path.lstat()
            resources.require(metadata.st_size <= 64 * 1024 * 1024, "MA installed file bound")
            total += metadata.st_size
            resources.require(total <= 512 * 1024 * 1024, "MA installed closure bound")
            digest = hashlib.sha256()
            count = 0
            with path.open("rb") as stream:
                while chunk := stream.read(min(262_144, metadata.st_size + 1 - count)):
                    count += len(chunk)
                    resources.require(count <= metadata.st_size, "MA installed file grew")
                    digest.update(chunk)
            after = path.lstat()
            resources.require(
                count == metadata.st_size
                and (
                    metadata.st_dev,
                    metadata.st_ino,
                    metadata.st_mode,
                    metadata.st_size,
                    metadata.st_mtime_ns,
                )
                == (after.st_dev, after.st_ino, after.st_mode, after.st_size, after.st_mtime_ns),
                "MA installed environment changed",
            )
            ledger.update(
                json.dumps(
                    [path.relative_to(site).as_posix(), metadata.st_size, digest.hexdigest()],
                    ensure_ascii=False,
                ).encode()
            )
    return ledger.hexdigest()


def base_identity() -> dict:
    executable = Path(sys.executable).resolve(strict=True)
    base = Path(sys.base_prefix).resolve(strict=True)
    resources.require(
        Path(sys.prefix).resolve() == base, "MA provisioner requires the isolated base runtime"
    )
    return {
        "prefix": str(base),
        "executable_sha256": hashlib.sha256(executable.read_bytes()).hexdigest(),
    }


def producer_interpreter(root: Path) -> Path:
    """Preserve the venv path and reject a substituted interpreter target."""
    binary = local_support.task_path(root, "producer/bin", directory=True) / "python"
    resources.require(
        binary.parent.resolve(strict=True) == binary.parent
        and binary.is_symlink()
        and binary.resolve(strict=True) == Path(sys.executable).resolve(strict=True),
        "MA producer interpreter target mismatch",
    )
    return binary


def provision_local(root: Path) -> None:
    local_support.require_local_context()
    local_support.admit_root(root, fresh=True)
    root.mkdir(mode=0o700, exist_ok=False)
    (root / "artifacts").mkdir(mode=0o700)
    state = {"complete": False, "scope": "unsupported-local-synthetic-only"}
    try:
        provision.disk_admit(root)
        inputs_raw = (preflight.QUALIFICATION / "inputs.json").read_bytes()
        inputs = resources.strict_json(inputs_raw)
        state["inputs_sha256"] = hashlib.sha256(inputs_raw).hexdigest()
        state["base"] = base_identity()
        wheel = provision.download(root, inputs["wheel"])
        gh = shutil.which("gh")
        resources.require(gh is not None, "MA attestation verifier unavailable")
        environment = {
            "PATH": os.environ.get("PATH", os.defpath),
            "GH_PROMPT_DISABLED": "1",
            "HOME": str(Path.home()),
        }
        if "GH_TOKEN" in os.environ:
            environment["GH_TOKEN"] = os.environ["GH_TOKEN"]
        # Use the same source, tag, repository and workflow policy as the hosted lane.
        provision.run_tool(
            root,
            "local-attestation",
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
        with requirements.open("xb") as stream:
            stream.write(raw)
        producer = provision.make_environment(root, "producer")
        resources.require(
            producer_interpreter(root) == producer, "MA environment spelling mismatch"
        )
        site = root / "producer/lib/python3.12/site-packages"
        check_startup(site)
        provision.install(
            root,
            "local-closure",
            producer,
            [
                "--require-hashes",
                "--default-index",
                "https://pypi.org/simple",
                "--requirements",
                str(requirements),
            ],
        )
        check_startup(site)
        provision.install(root, "local-wheel", producer, ["--no-index", str(wheel)])
        check_startup(site)
        query = (
            "import importlib.metadata as m,json,platform; "
            "assert platform.python_version()=='3.12.14'; "
            "assert m.version('matryca-plumber')=='2.1.0a3'; "
            "assert m.version('logseq-matryca-parser')=='1.9.0'; "
            "print(json.dumps({'python':'3.12.14','plumber':'2.1.0a3','parser':'1.9.0'}))"
        )
        provision.run_tool(root, "local-identity", [str(producer), "-I", "-B", "-c", query])
        state.update(
            installed_sha256=environment_digest(site),
            pyvenv_sha256=hashlib.sha256(
                local_support.read_task_file(root, "producer/pyvenv.cfg", 8192)
            ).hexdigest(),
            producer_wheel_sha256=inputs["wheel"]["sha256"],
            source_commit=inputs["source_commit"],
        )
        provision.disk_admit(root)
        state["complete"] = True
    except BaseException as error:
        state["complete"] = False
        state["error_class"] = type(error).__name__
        raise
    finally:
        provision.write_json(root / "artifacts/local-provision.json", state)


def verified_local_inputs(root: Path) -> tuple[dict, Path]:
    """Recheck fixed local inputs before the builder or producer can be used."""
    local_support.require_local_context()
    local_support.admit_root(root, fresh=False)
    receipt = resources.strict_json(
        local_support.read_task_file(root, "artifacts/local-provision.json", 65_536)
    )
    inputs_raw = (preflight.QUALIFICATION / "inputs.json").read_bytes()
    inputs = resources.strict_json(inputs_raw)
    resources.require(
        receipt.get("complete") is True
        and receipt.get("scope") == "unsupported-local-synthetic-only"
        and receipt.get("inputs_sha256") == hashlib.sha256(inputs_raw).hexdigest()
        and receipt.get("base") == base_identity()
        and receipt.get("source_commit") == inputs["source_commit"]
        and receipt.get("producer_wheel_sha256") == inputs["wheel"]["sha256"],
        "MA local provisioning binding mismatch",
    )
    wheel = local_support.task_path(
        root, "downloads/" + inputs["wheel"]["sha256"] + "/" + inputs["wheel"]["filename"]
    )
    resources.verify_file(wheel, inputs["wheel"]["sha256"], inputs["wheel"]["size"])
    resources.require(
        receipt.get("pyvenv_sha256")
        == hashlib.sha256(
            local_support.read_task_file(root, "producer/pyvenv.cfg", 8192)
        ).hexdigest()
        and receipt.get("installed_sha256")
        == environment_digest(
            local_support.task_path(root, "producer/lib/python3.12/site-packages", directory=True)
        ),
        "MA installed environment changed",
    )
    producer_interpreter(root)
    provision.disk_admit(root)
    return inputs, wheel


if __name__ == "__main__":
    try:
        provision_local(parse_root(sys.argv[1:]))
    except Exception:
        print('{"scope":"unsupported-local-synthetic-only","exit_class":"provisioning_refused"}')
        raise SystemExit(1) from None
    print('{"scope":"unsupported-local-synthetic-only","exit_class":"provisioned"}')
