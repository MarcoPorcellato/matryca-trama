"""Bounded POSIX process mechanics for the restricted synthetic client."""

from __future__ import annotations

import errno
import os
import selectors
import signal
import subprocess
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass

DEFAULT_STDOUT_LIMIT = 4 * 1024 * 1024
DEFAULT_STDERR_LIMIT = 512
_CLEANUP_SECONDS = 5.0


@dataclass(frozen=True)
class ProcessResult:
    """Bounded output and terminal evidence from one owned child."""

    stdout: bytes
    stderr: bytes
    returncode: int
    child_reaped: bool
    group_probe_errno: int
    cleanup_succeeded: bool
    cleanup_exception: BaseException | None
    observations: tuple[str, ...]
    events: tuple[str, ...]


class ProcessFailure(RuntimeError):
    """A non-retryable invocation failure with retained cleanup evidence."""

    retryable = False

    def __init__(
        self,
        reason: str,
        *,
        stdout: bytes,
        stderr: bytes,
        returncode: int | None,
        child_reaped: bool,
        signal_errno: int | None,
        group_probe_errno: int | None,
        cleanup_succeeded: bool,
        cleanup_exception: BaseException | None,
        observations: tuple[str, ...],
        events: tuple[str, ...],
    ) -> None:
        super().__init__(reason)
        self.reason = reason
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.child_reaped = child_reaped
        self.signal_errno = signal_errno
        self.group_probe_errno = group_probe_errno
        self.cleanup_succeeded = cleanup_succeeded
        self.cleanup_exception = cleanup_exception
        self.observations = observations
        self.events = events


def run_process(
    argv: Sequence[str],
    *,
    timeout_seconds: float,
    stdout_limit: int = DEFAULT_STDOUT_LIMIT,
    stderr_limit: int = DEFAULT_STDERR_LIMIT,
    killpg: Callable[[int, int], object] = os.killpg,
    environment: Mapping[str, str] | None = None,
) -> ProcessResult:
    """Run one explicit child with bounded bytes and terminal cleanup evidence.

    This mechanism does not select or admit a producer, retry an
    invocation, interpret a contract, or provide operating-system isolation.
    """
    if os.name != "posix":
        raise NotImplementedError("qualification process boundary is POSIX-only")
    if not argv or timeout_seconds <= 0 or stdout_limit <= 0 or stderr_limit <= 0:
        raise ValueError("argv and positive timeout/output limits are required")

    child = subprocess.Popen(
        list(argv),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
        env={"PATH": os.defpath, "PYTHONNOUSERSITE": "1", **dict(environment or {})},
        start_new_session=True,
    )
    pgid = child.pid
    stdout_fd: int | None = None
    stderr_fd: int | None = None
    captured: dict[int, bytearray] = {}
    limits: dict[int, int] = {}
    selector: selectors.BaseSelector | None = None
    reason: str | None = None
    execution_exception: BaseException | None = None
    try:
        if child.stdout is None or child.stderr is None:
            raise RuntimeError("child pipes were not created")
        stdout_fd = child.stdout.fileno()
        stderr_fd = child.stderr.fileno()
        captured = {stdout_fd: bytearray(), stderr_fd: bytearray()}
        limits = {stdout_fd: stdout_limit, stderr_fd: stderr_limit}
        selector = selectors.DefaultSelector()
        for stream in (child.stdout, child.stderr):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ)

        deadline = time.monotonic() + timeout_seconds
        while selector.get_map():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                reason = "timeout"
                break
            for key, _ in selector.select(min(remaining, 0.05)):
                fd = key.fd
                room = limits[fd] - len(captured[fd])
                try:
                    chunk = os.read(fd, min(65536, room + 1))
                except BlockingIOError:
                    continue
                if not chunk:
                    selector.unregister(key.fileobj)
                    continue
                captured[fd].extend(chunk[:room])
                if len(chunk) > room:
                    reason = "output_limit"
                    break
            if reason is not None:
                break
            if child.poll() is not None and not selector.get_map():
                break

        if reason is None:
            child.wait(timeout=max(0.0, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        reason = "timeout"
    except BaseException as error:
        reason = "exception"
        execution_exception = error

    # Every phase shares one finalization deadline. A failing phase must not
    # skip the remaining resource owners, including on BaseException.
    cleanup_deadline = time.monotonic() + _CLEANUP_SECONDS
    observations: list[str] = []
    events: list[str] = []
    signal_errno: int | None = None
    cleanup_exception: BaseException | None = None
    if reason is not None:
        signal_errno, cleanup_exception = _signal_group(killpg, pgid, signal.SIGKILL)
        _retain_signal(signal_errno, observations, events)
        if cleanup_exception is not None:
            events.append("signal_exception")
    child_reaped, reap_exception = _reap(child, cleanup_deadline)
    cleanup_exception = cleanup_exception or reap_exception
    if reap_exception is not None:
        events.append("reap_exception")
    for stream in (child.stdout, child.stderr):
        if stream is not None and not stream.closed:
            try:
                stream.close()
            except BaseException as error:
                cleanup_exception = cleanup_exception or error
                events.append("stream_close_exception")
    if selector is not None:
        try:
            selector.close()
        except BaseException as error:
            cleanup_exception = cleanup_exception or error
            events.append("selector_close_exception")
    try:
        group_probe_errno, group_gone = _confirm_group_gone(
            child, killpg, pgid, cleanup_deadline, observations, events
        )
    except BaseException as error:
        group_probe_errno = None
        group_gone = False
        cleanup_exception = cleanup_exception or error
        events.append("group_confirmation_exception")
    child_reaped = child_reaped or child.returncode is not None
    cleanup_succeeded = (
        child_reaped
        and group_gone
        and all(stream is None or stream.closed for stream in (child.stdout, child.stderr))
        and cleanup_exception is None
        and not events
    )
    if not cleanup_succeeded:
        events.extend("unresolved:" + observation for observation in observations)

    if reason is None and child.returncode != 0:
        reason = "nonzero_exit"
    if reason is None and not child_reaped:
        reason = "reap_failure"
    if reason is None and not cleanup_succeeded:
        reason = "cleanup_failure"
    if reason is not None:
        stdout = bytes(captured.get(stdout_fd, b"")) if stdout_fd is not None else b""
        stderr = bytes(captured.get(stderr_fd, b"")) if stderr_fd is not None else b""
        failure = ProcessFailure(
            reason,
            stdout=stdout,
            stderr=stderr,
            returncode=child.returncode,
            child_reaped=child_reaped,
            signal_errno=signal_errno,
            group_probe_errno=group_probe_errno,
            cleanup_succeeded=cleanup_succeeded,
            cleanup_exception=cleanup_exception,
            observations=tuple(observations),
            events=tuple(events),
        )
        if execution_exception is not None:
            execution_exception.process_evidence = failure
            execution_exception.process_cleanup = {
                "child_reaped": child_reaped,
                "signal_errno": signal_errno,
                "group_probe_errno": group_probe_errno,
                "cleanup_succeeded": cleanup_succeeded,
                "cleanup_exception": cleanup_exception,
                "observations": tuple(observations),
                "events": tuple(events),
            }
            raise execution_exception.with_traceback(execution_exception.__traceback__)
        raise failure

    assert child.returncode is not None
    assert stdout_fd is not None and stderr_fd is not None
    return ProcessResult(
        stdout=bytes(captured[stdout_fd]),
        stderr=bytes(captured[stderr_fd]),
        returncode=child.returncode,
        child_reaped=child_reaped,
        group_probe_errno=group_probe_errno,
        cleanup_succeeded=cleanup_succeeded,
        cleanup_exception=cleanup_exception,
        observations=tuple(observations),
        events=tuple(events),
    )


def _signal_group(
    killpg: Callable[[int, int], object], pgid: int, sig: int
) -> tuple[int | None, BaseException | None]:
    try:
        killpg(pgid, sig)
    except ProcessLookupError as error:
        return error.errno or errno.ESRCH, None
    except OSError as error:
        return error.errno or errno.EIO, None
    except BaseException as error:
        return None, error
    return None, None


def _reap(child: subprocess.Popen[bytes], deadline: float) -> tuple[bool, BaseException | None]:
    reap_exception: BaseException | None = None
    try:
        child.wait(timeout=min(0.05, max(0.0, deadline - time.monotonic())))
        return True, None
    except subprocess.TimeoutExpired:
        pass
    except BaseException as error:
        reap_exception = error
    try:
        child.kill()
    except BaseException as error:
        reap_exception = reap_exception or error
    try:
        child.wait(timeout=max(0.0, deadline - time.monotonic()))
        return True, reap_exception
    except BaseException as error:
        return False, reap_exception or error


def _retain_signal(code: int | None, observations: list[str], events: list[str]) -> None:
    if code == errno.EPERM:
        observations.append("signal:EPERM")
    elif code not in (None, errno.ESRCH):
        events.append("signal:" + errno.errorcode.get(code, str(code)))


def _confirm_group_gone(
    child: subprocess.Popen[bytes],
    killpg: Callable[[int, int], object],
    pgid: int,
    deadline: float,
    observations: list[str],
    events: list[str],
) -> tuple[int | None, bool]:
    last_errno: int | None = None
    while True:
        if time.monotonic() >= deadline:
            events.append("cleanup_deadline")
            return last_errno, False
        child.poll()  # Reap before probing: a zombie can keep its group present.
        try:
            killpg(pgid, 0)
        except ProcessLookupError as error:
            return error.errno or errno.ESRCH, child.returncode is not None
        except OSError as error:
            last_errno = error.errno or errno.EIO
            if last_errno == errno.ESRCH:
                return last_errno, child.returncode is not None
            if last_errno != errno.EPERM:
                events.append("group_probe:" + errno.errorcode.get(last_errno, str(last_errno)))
                return last_errno, False
            observations.append("group_probe:EPERM")
        signal_errno, error = _signal_group(killpg, pgid, signal.SIGKILL)
        _retain_signal(signal_errno, observations, events)
        if error is not None:
            raise error
        if events:
            return last_errno, False
        time.sleep(min(0.01, max(0.0, deadline - time.monotonic())))
