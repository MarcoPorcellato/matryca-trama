"""POSIX-only, test-local subprocess boundary for inert fake programs."""

from __future__ import annotations

from dataclasses import dataclass
import errno
import os
import selectors
import signal
import subprocess
import time
from collections.abc import Callable, Sequence


DEFAULT_STDOUT_LIMIT = 4 * 1024 * 1024
DEFAULT_STDERR_LIMIT = 512
_CLEANUP_SECONDS = 1.0
_REAP_SECONDS = 1.0


@dataclass(frozen=True)
class FakeProcessResult:
    """Bounded output and terminal evidence from one synthetic child."""

    stdout: bytes
    stderr: bytes
    returncode: int
    child_reaped: bool
    group_probe_errno: int
    cleanup_succeeded: bool
    cleanup_exception: BaseException | None


class FakeProcessFailure(RuntimeError):
    """A non-retryable fake invocation failure with retained cleanup evidence."""

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


def run_fake_process(
    argv: Sequence[str],
    *,
    timeout_seconds: float,
    stdout_limit: int = DEFAULT_STDOUT_LIMIT,
    stderr_limit: int = DEFAULT_STDERR_LIMIT,
    killpg: Callable[[int, int], object] = os.killpg,
) -> FakeProcessResult:
    """Run one inert child with capped output, deadline, reaping, and group proof.

    This helper belongs only to tests. Callers supply synthetic child argv; it
    does not read graph content, access a producer, retry, or interpret output.
    """
    if os.name != "posix":
        raise NotImplementedError("fake process boundary is POSIX-only")
    if not argv or timeout_seconds <= 0 or stdout_limit <= 0 or stderr_limit <= 0:
        raise ValueError("argv and positive timeout/output limits are required")

    child = subprocess.Popen(
        list(argv),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        close_fds=True,
        env={"PATH": os.defpath, "PYTHONNOUSERSITE": "1"},
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
            raise RuntimeError("fake child pipes were not created")
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

    signal_errno: int | None = None
    cleanup_exception: BaseException | None = None
    if reason is not None:
        signal_errno, cleanup_exception = _signal_group(killpg, pgid, signal.SIGKILL)
    child_reaped, reap_exception = _reap(child)
    cleanup_exception = cleanup_exception or reap_exception
    close_exception: BaseException | None = None
    for stream in (child.stdout, child.stderr):
        if stream is not None and not stream.closed:
            try:
                stream.close()
            except BaseException as error:
                close_exception = close_exception or error
    cleanup_exception = cleanup_exception or close_exception
    if selector is not None:
        try:
            selector.close()
        except BaseException as error:
            close_exception = close_exception or error
        cleanup_exception = cleanup_exception or close_exception
    try:
        (
            group_probe_errno,
            group_gone,
            probe_errno,
            probe_exception,
        ) = _confirm_group_gone(
            killpg, pgid, deadline=time.monotonic() + _CLEANUP_SECONDS
        )
    except BaseException as error:
        group_probe_errno = None
        group_gone = False
        probe_errno = None
        probe_exception = error
    signal_errno = signal_errno or probe_errno
    cleanup_exception = cleanup_exception or probe_exception
    cleanup_succeeded = (
        child_reaped
        and group_gone
        and signal_errno in (None, errno.ESRCH)
        and cleanup_exception is None
    )

    if execution_exception is not None:
        execution_exception.fake_process_cleanup = {
            "child_reaped": child_reaped,
            "signal_errno": signal_errno,
            "group_probe_errno": group_probe_errno,
            "cleanup_succeeded": cleanup_succeeded,
            "cleanup_exception": cleanup_exception,
        }
        raise execution_exception.with_traceback(execution_exception.__traceback__)

    if reason is None and child.returncode != 0:
        reason = "nonzero_exit"
    if reason is None and not child_reaped:
        reason = "reap_failure"
    if reason is None and not cleanup_succeeded:
        reason = "cleanup_failure"
    if reason is not None:
        stdout = bytes(captured.get(stdout_fd, b"")) if stdout_fd is not None else b""
        stderr = bytes(captured.get(stderr_fd, b"")) if stderr_fd is not None else b""
        raise FakeProcessFailure(
            reason,
            stdout=stdout,
            stderr=stderr,
            returncode=child.returncode,
            child_reaped=child_reaped,
            signal_errno=signal_errno,
            group_probe_errno=group_probe_errno,
            cleanup_succeeded=cleanup_succeeded,
            cleanup_exception=cleanup_exception,
        )

    assert child.returncode is not None
    assert stdout_fd is not None and stderr_fd is not None
    return FakeProcessResult(
        stdout=bytes(captured[stdout_fd]),
        stderr=bytes(captured[stderr_fd]),
        returncode=child.returncode,
        child_reaped=child_reaped,
        group_probe_errno=group_probe_errno,
        cleanup_succeeded=cleanup_succeeded,
        cleanup_exception=cleanup_exception,
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


def _reap(child: subprocess.Popen[bytes]) -> tuple[bool, BaseException | None]:
    reap_exception: BaseException | None = None
    try:
        child.wait(timeout=_REAP_SECONDS)
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
        child.wait(timeout=_REAP_SECONDS)
        return True, reap_exception
    except BaseException as error:
        return False, reap_exception or error


def _confirm_group_gone(
    killpg: Callable[[int, int], object], pgid: int, *, deadline: float
) -> tuple[int | None, bool, int | None, BaseException | None]:
    last_errno: int | None = None
    while True:
        try:
            if time.monotonic() >= deadline:
                return last_errno, False, last_errno, None
        except BaseException as error:
            return last_errno, False, last_errno, error
        try:
            killpg(pgid, 0)
        except ProcessLookupError as error:
            return error.errno or errno.ESRCH, True, None, None
        except OSError as error:
            last_errno = error.errno or errno.EIO
            if last_errno == errno.ESRCH:
                return last_errno, True, None, None
            return last_errno, False, last_errno, None
        except BaseException as error:
            return None, False, None, error
        else:
            last_errno, cleanup_exception = _signal_group(killpg, pgid, signal.SIGKILL)
            if cleanup_exception is not None:
                return None, False, last_errno, cleanup_exception
            if last_errno not in (None, errno.ESRCH):
                return last_errno, False, last_errno, None
        try:
            time.sleep(0.01)
        except BaseException as error:
            return last_errno, False, last_errno, error
