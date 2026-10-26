"""Independent native controls for the unsupported local synthetic runner."""

from __future__ import annotations

import errno
import hashlib
import json
import os
import socket
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import TypedDict, TypeGuard

HERE = Path(__file__).resolve().parent
QUALIFICATION = HERE.parent / "qualification"
sys.path.insert(0, str(QUALIFICATION))
import process_boundary  # noqa: E402 - this repository's existing process owner.
import provision  # noqa: E402
import resources  # noqa: E402

for module in (process_boundary, provision, resources):
    if (
        Path(module.__file__).resolve() != QUALIFICATION / (module.__name__ + ".py")
        or Path(module.__spec__.origin).resolve() != Path(module.__file__).resolve()
    ):
        raise RuntimeError("MA qualification support origin mismatch")

CHANNELS = ("write", "read", "tcp4", "tcp6", "udp", "unix", "dns")


class ProbeRecord(TypedDict):
    succeeded: bool
    error: int
    resolver_error: int


class PreflightRefused(RuntimeError):
    """A native control was unavailable, malformed or not denied."""


class CleanupUncertain(RuntimeError):
    """Existing process ownership gates did not all pass."""


def _record_shape(value: object) -> TypeGuard[ProbeRecord]:
    if type(value) is not dict or set(value) != {"succeeded", "error", "resolver_error"}:
        return False
    if (
        type(value["succeeded"]) is not bool
        or type(value["error"]) is not int
        or value["error"] < 0
        or type(value["resolver_error"]) is not int
    ):
        return False
    return value["succeeded"] == (value["error"] == 0 and value["resolver_error"] == 0)


def classify_control(
    positive: object,
    negative: object,
    *,
    unchanged: bool,
    positive_observed: bool,
    negative_observed: bool,
) -> str:
    """Unavailability and unrelated errors never establish an OS denial."""
    if (
        not _record_shape(positive)
        or not _record_shape(negative)
        or any(
            type(value) is not bool for value in (unchanged, positive_observed, negative_observed)
        )
        or not positive["succeeded"]
        or not positive_observed
    ):
        return "UNTESTABLE"
    if negative["succeeded"] or negative_observed:
        return "ALLOWED"
    if not unchanged:
        return "INCONCLUSIVE"
    if negative["error"] in (errno.EPERM, errno.EACCES):
        return "DENIED"
    return "UNTESTABLE"


def confined_after_positive(
    positive: object, observed: bool, invoke: Callable[[], object]
) -> object:
    """Never execute a confined control after an unavailable positive control."""
    if not _record_shape(positive) or not positive["succeeded"] or observed is not True:
        raise PreflightRefused("MA positive native control unavailable")
    return invoke()


def require_cleanup(result: object) -> None:
    """Keep reap, ESRCH, readers and streams under the existing shared owner."""
    if (
        getattr(result, "child_reaped", None) is not True
        or getattr(result, "cleanup_succeeded", None) is not True
        or getattr(result, "group_probe_errno", None) != errno.ESRCH
        or getattr(result, "events", ("absent",))
        or getattr(result, "cleanup_exception", object()) is not None
    ):
        raise CleanupUncertain("MA process cleanup uncertain")


def profile_text(graph: Path, producer: Path, base: Path, binary: Path) -> str:
    """Generate fixed read grants, never a caller-supplied sandbox policy."""
    grants = (graph, producer, base, binary)
    for path in grants:
        if (
            not path.is_absolute()
            or any(ord(character) < 32 or character in '\\"' for character in str(path))
            or path.resolve(strict=True) != path
        ):
            raise PreflightRefused("MA read grant is not canonical")
    if not all(path.is_dir() for path in (graph, producer, base)) or not binary.is_file():
        raise PreflightRefused("MA read grant type rejected")

    def quote(path: Path) -> str:
        return json.dumps(str(path), ensure_ascii=False)

    system = ("/System", "/usr/lib", "/usr/share/locale", "/private/var/db/dyld")
    lines = [
        "(version 1)",
        "(allow default)",
        "(deny network*)",
        "(deny mach-lookup)",
        "(deny file-write*)",
        "(deny file-read*)",
        '(allow file-write-data (literal "/dev/null"))',
        '(allow file-read-data (literal "/"))',
    ]
    for path in (*grants[:3], *map(Path, system)):
        lines.append("(allow file-read* (subpath " + quote(path) + "))")
    for path in (binary, Path("/dev/null"), Path("/dev/urandom"), Path("/dev/random")):
        lines.append("(allow file-read* (literal " + quote(path) + "))")
    ancestors = {parent for path in grants for parent in path.parents}
    for path in sorted(ancestors):
        lines.append("(allow file-read-metadata (literal " + quote(path) + "))")
    return "\n".join(lines) + "\n"


def execute(
    root: Path,
    label: str,
    argv: list[str],
    *,
    deadline: float,
    seconds: float = 10,
    stdout_limit: int = 65_536,
    stderr_limit: int = 16_384,
):
    """Reuse the sole existing process owner and retain failures before rejecting."""
    remaining = deadline - time.monotonic() - 5
    if remaining <= 0:
        raise PreflightRefused("MA execution deadline exhausted")
    environment = {
        "HOME": str(root / "empty-home"),
        "TMPDIR": str(root / "native"),
        "CLANG_MODULE_CACHE_PATH": str(root / "native" / "compiler-cache"),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
    try:
        result = process_boundary.run_process(
            argv,
            timeout_seconds=min(seconds, remaining),
            stdout_limit=stdout_limit,
            stderr_limit=stderr_limit,
            environment=environment,
        )
    except BaseException as error:
        result = (
            error
            if isinstance(error, process_boundary.ProcessFailure)
            else getattr(error, "process_evidence", None)
        )
        if isinstance(result, process_boundary.ProcessFailure):
            try:
                provision.save_result(root, label, result)
            except BaseException as retention:
                error.add_note("MA evidence retention failed: " + type(retention).__name__)
            require_cleanup(result)
        raise
    provision.save_result(root, label, result)
    require_cleanup(result)
    if result.stderr:
        raise PreflightRefused("MA launcher or child stderr rejected")
    provision.disk_admit(root)
    return result


def _pending(listener: socket.socket, channel: str) -> int:
    count = 0
    while count < 4:
        try:
            if channel == "udp":
                packet, _ = listener.recvfrom(64)
                if packet != b"ma-datagram":
                    raise PreflightRefused("MA unexpected native datagram")
            else:
                connection, _ = listener.accept()
                connection.close()
            count += 1
        except BlockingIOError:
            return count
    raise PreflightRefused("MA native listener observation bound exceeded")


def finish_listener(listener: socket.socket | None, address: Path | None) -> None:
    """Finalize independently; an interruption must not skip the next step."""
    failures = []
    if listener is not None:
        try:
            listener.close()
        except BaseException as error:
            failures.append("close:" + type(error).__name__)
    if address is not None:
        try:
            address.unlink()
        except BaseException as error:
            failures.append("unlink:" + type(error).__name__)
    if failures:
        raise CleanupUncertain("MA listener cleanup uncertain: " + ",".join(failures))


def run_preflight(
    root: Path,
    graph: Path,
    producer: Path,
    base: Path,
    state: dict,
    *,
    deadline: float,
) -> Path:
    """Compile one native helper and prove all seven channels before launch."""
    compiler, sandbox = Path("/usr/bin/clang"), Path("/usr/bin/sandbox-exec")
    if not all(path.is_file() and os.access(path, os.X_OK) for path in (compiler, sandbox)):
        raise PreflightRefused("MA preinstalled native tools unavailable")
    native = root / "native"
    native.mkdir(mode=0o700, exist_ok=False)
    (root / "empty-home").mkdir(mode=0o700, exist_ok=False)
    source, binary, profile = HERE / "canary.c", native / "canary", native / "profile.sb"
    source_digest = hashlib.sha256(source.read_bytes()).hexdigest()
    execute(
        root,
        "ma-compile",
        [
            str(compiler),
            "-std=c11",
            "-Wall",
            "-Wextra",
            "-Werror",
            "-fno-modules",
            str(source),
            "-o",
            str(binary),
        ],
        deadline=deadline,
        seconds=45,
    )
    if hashlib.sha256(source.read_bytes()).hexdigest() != source_digest:
        raise resources.QualificationFailure("MA native source changed")
    binary_size = binary.stat().st_size
    binary_digest = hashlib.sha256(binary.read_bytes()).hexdigest()
    text = profile_text(graph, producer, base, binary).encode()
    with profile.open("xb") as stream:
        stream.write(text)
    profile_digest = hashlib.sha256(text).hexdigest()
    state.update(
        native_source_sha256=source_digest,
        native_binary_sha256=binary_digest,
        profile_sha256=profile_digest,
        controls={},
    )

    def probe(label: str, arguments: list[str], confined: bool) -> dict:
        resources.verify_file(binary, binary_digest, binary_size)
        resources.verify_file(profile, profile_digest, len(text))
        argv = [str(binary), *arguments]
        if confined:
            argv = [str(sandbox), "-f", str(profile), *argv]
        result = execute(root, label, argv, deadline=deadline, stdout_limit=4096)
        return resources.strict_json(result.stdout)

    for channel in CHANNELS:
        marker = native / (channel + "-marker")
        listener = None
        address = None
        bound_address = None
        try:
            if channel in ("write", "read"):
                marker.write_bytes(b"ma-private\n")
                arguments = [channel, str(marker)]
            elif channel == "dns":
                arguments = [channel]
            else:
                family = (
                    socket.AF_INET6
                    if channel == "tcp6"
                    else (socket.AF_UNIX if channel == "unix" else socket.AF_INET)
                )
                listener = socket.socket(
                    family, socket.SOCK_DGRAM if channel == "udp" else socket.SOCK_STREAM
                )
                if channel == "unix":
                    address = native / "control.sock"
                    listener.bind(str(address))
                    bound_address = address
                    arguments = [channel, str(address)]
                else:
                    listener.bind(("::1" if channel == "tcp6" else "127.0.0.1", 0))
                    arguments = [channel, str(listener.getsockname()[1])]
                if channel != "udp":
                    listener.listen(4)
                listener.setblocking(False)

            positive = probe("ma-positive-" + channel, arguments, False)
            observed = (
                _pending(listener, channel) == 1
                if listener is not None
                else (
                    marker.read_bytes() == b"ma-canary\n"
                    if channel == "write"
                    else marker.read_bytes() == b"ma-private\n"
                    if channel == "read"
                    else _record_shape(positive) and positive["succeeded"]
                )
            )
            state["controls"][channel] = {"positive": positive, "positive_observed": observed}
            if channel == "write":
                marker.write_bytes(b"ma-private\n")
            before = marker.read_bytes() if channel in ("read", "write") else None
            negative = confined_after_positive(
                positive,
                observed,
                lambda: probe("ma-confined-" + channel, arguments, True),
            )
            negative_observed = (
                _pending(listener, channel) != 0
                if listener is not None
                else (bool(_record_shape(negative) and negative["succeeded"]))
            )
            unchanged = marker.read_bytes() == before if before is not None else True
            outcome = classify_control(
                positive,
                negative,
                unchanged=unchanged,
                positive_observed=observed,
                negative_observed=negative_observed,
            )
            state["controls"][channel].update(
                negative=negative,
                outcome=outcome,
                unchanged=unchanged,
                negative_observed=negative_observed,
            )
            if outcome != "DENIED":
                raise PreflightRefused("MA native channel did not prove denial")
        finally:
            primary = sys.exception()
            try:
                finish_listener(listener, bound_address)
            except BaseException as cleanup:
                state["listener_cleanup_error"] = str(cleanup)
                state["cleanup_succeeded"] = False
                if primary is not None:
                    primary.add_note(str(cleanup))
                else:
                    raise
    state["preflight_complete"] = True
    return profile
