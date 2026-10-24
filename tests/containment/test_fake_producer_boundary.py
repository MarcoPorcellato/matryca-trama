"""Process containment tests using inert, locally generated child programs only."""

import errno
import os
import selectors
import signal
import sys
import unittest
from typing import Any
from unittest.mock import patch

from tests.fakes.fake_process_boundary import (
    FakeProcessFailure,
    FakeProcessResult,
    run_fake_process,
)


class _CleanupAbort(BaseException):
    """Prove process cleanup retains a non-Exception cleanup interruption."""


class _AbortSelector:
    """Delegate selector ownership but inject one deterministic interruption."""

    def __init__(self, abort: BaseException) -> None:
        self._selector = selectors.DefaultSelector()
        self._abort = abort

    def register(self, *args: Any, **kwargs: Any) -> Any:
        return self._selector.register(*args, **kwargs)

    def get_map(self) -> Any:
        return self._selector.get_map()

    def select(self, *args: Any, **kwargs: Any) -> Any:
        raise self._abort

    def close(self) -> None:
        self._selector.close()


@unittest.skipUnless(os.name == "posix", "the fake process boundary is POSIX-only")
class FakeProducerBoundaryTests(unittest.TestCase):
    """The test harness bounds and reaps synthetic subprocesses."""

    def run_child(self, code: str, **options: Any) -> Any:
        return run_fake_process(
            [sys.executable, "-B", "-c", code],
            timeout_seconds=options.pop("timeout_seconds", 5.0),
            **options,
        )

    def test_bounded_zero_exit_returns_only_synthetic_bytes(self) -> None:
        result = self.run_child("import os; os.write(1, b'synthetic')")

        self.assertIsInstance(result, FakeProcessResult)
        self.assertEqual(result.stdout, b"synthetic")
        self.assertEqual(result.stderr, b"")
        self.assertEqual(result.returncode, 0)
        self.assertTrue(result.child_reaped)
        self.assertEqual(result.group_probe_errno, errno.ESRCH)
        self.assertTrue(result.cleanup_succeeded)

    def test_stdout_is_captured_incrementally_only_to_four_mib(self) -> None:
        with self.assertRaises(FakeProcessFailure) as caught:
            self.run_child(
                "import os; chunk=b'x'*65536; [os.write(1, chunk) for _ in range(80)]",
                stdout_limit=4 * 1024 * 1024,
            )

        failure = caught.exception
        self.assertEqual(failure.reason, "output_limit")
        self.assertEqual(len(failure.stdout), 4 * 1024 * 1024)
        self.assertTrue(failure.child_reaped)
        self.assertEqual(failure.group_probe_errno, errno.ESRCH)

    def test_stderr_is_captured_incrementally_only_to_512_bytes(self) -> None:
        with self.assertRaises(FakeProcessFailure) as caught:
            self.run_child(
                "import os; chunk=b'e'*256; [os.write(2, chunk) for _ in range(8)]",
                stderr_limit=512,
            )

        failure = caught.exception
        self.assertEqual(failure.reason, "output_limit")
        self.assertEqual(len(failure.stderr), 512)
        self.assertTrue(failure.child_reaped)
        self.assertEqual(failure.group_probe_errno, errno.ESRCH)

    def test_timeout_kills_and_reaps_the_child_group(self) -> None:
        with self.assertRaises(FakeProcessFailure) as caught:
            self.run_child("import time; time.sleep(30)", timeout_seconds=0.1)

        failure = caught.exception
        self.assertEqual(failure.reason, "timeout")
        self.assertTrue(failure.child_reaped)
        self.assertEqual(failure.group_probe_errno, errno.ESRCH)

    def test_nonzero_exit_is_explicitly_nonretryable_and_reaped(self) -> None:
        with self.assertRaises(FakeProcessFailure) as caught:
            self.run_child("raise SystemExit(23)")

        failure = caught.exception
        self.assertEqual(failure.reason, "nonzero_exit")
        self.assertEqual(failure.returncode, 23)
        self.assertFalse(failure.retryable)
        self.assertTrue(failure.child_reaped)
        self.assertEqual(failure.group_probe_errno, errno.ESRCH)

    def test_exit_four_is_nonretryable_and_reaped(self) -> None:
        with self.assertRaises(FakeProcessFailure) as caught:
            self.run_child("raise SystemExit(4)")

        failure = caught.exception
        self.assertEqual(failure.reason, "nonzero_exit")
        self.assertEqual(failure.returncode, 4)
        self.assertFalse(failure.retryable)
        self.assertTrue(failure.child_reaped)
        self.assertEqual(failure.group_probe_errno, errno.ESRCH)

    def test_esrch_signal_race_is_confirmed_by_final_group_probe(self) -> None:
        real_killpg = os.killpg

        def killpg_with_esrch_race(pgid: int, sig: int) -> None:
            if sig == signal.SIGKILL:
                real_killpg(pgid, sig)
                raise ProcessLookupError(errno.ESRCH, "deterministic ESRCH race")
            real_killpg(pgid, sig)

        with self.assertRaises(FakeProcessFailure) as caught:
            self.run_child(
                "import os; os.write(1, b'x'*4096)",
                stdout_limit=512,
                killpg=killpg_with_esrch_race,
            )

        failure = caught.exception
        self.assertEqual(failure.reason, "output_limit")
        self.assertTrue(failure.child_reaped)
        self.assertEqual(failure.group_probe_errno, errno.ESRCH)
        self.assertTrue(failure.cleanup_succeeded)

    def test_eperm_during_group_cleanup_is_retained_not_success(self) -> None:
        real_killpg = os.killpg

        def killpg_with_cleanup_eperm(pgid: int, sig: int) -> None:
            if sig == 0:
                raise PermissionError(errno.EPERM, "deterministic cleanup observation")
            real_killpg(pgid, sig)

        with self.assertRaises(FakeProcessFailure) as caught:
            self.run_child(
                "import os; os.write(1, b'x'*4096)",
                stdout_limit=512,
                killpg=killpg_with_cleanup_eperm,
            )

        failure = caught.exception
        self.assertEqual(failure.reason, "output_limit")
        self.assertTrue(failure.child_reaped)
        self.assertEqual(failure.group_probe_errno, errno.EPERM)
        self.assertFalse(failure.cleanup_succeeded)

    def test_initial_sigkill_eperm_survives_fallback_reap_and_esrch(self) -> None:
        real_killpg = os.killpg

        def deny_initial_sigkill(pgid: int, sig: int) -> None:
            if sig == signal.SIGKILL:
                raise PermissionError(
                    errno.EPERM, "deterministic initial signal denial"
                )
            real_killpg(pgid, sig)

        with self.assertRaises(FakeProcessFailure) as caught:
            self.run_child(
                "import time; time.sleep(30)",
                timeout_seconds=0.1,
                killpg=deny_initial_sigkill,
            )

        failure = caught.exception
        self.assertEqual(failure.reason, "timeout")
        self.assertTrue(failure.child_reaped)
        self.assertEqual(failure.group_probe_errno, errno.ESRCH)
        self.assertEqual(failure.signal_errno, errno.EPERM)
        self.assertFalse(failure.cleanup_succeeded)

    def test_eperm_after_zero_exit_converts_success_to_cleanup_failure(self) -> None:
        def killpg_with_cleanup_eperm(pgid: int, sig: int) -> None:
            if sig == 0:
                raise PermissionError(errno.EPERM, "deterministic cleanup observation")
            os.killpg(pgid, sig)

        with self.assertRaises(FakeProcessFailure) as caught:
            self.run_child("pass", killpg=killpg_with_cleanup_eperm)

        failure = caught.exception
        self.assertEqual(failure.reason, "cleanup_failure")
        self.assertTrue(failure.child_reaped)
        self.assertEqual(failure.group_probe_errno, errno.EPERM)
        self.assertFalse(failure.cleanup_succeeded)

    def test_cleanup_exception_keeps_the_original_failure_and_observation(self) -> None:
        def killpg_with_cleanup_exception(pgid: int, sig: int) -> None:
            if sig == 0:
                raise OSError(errno.EIO, "deterministic cleanup exception")
            os.killpg(pgid, sig)

        with self.assertRaises(FakeProcessFailure) as caught:
            self.run_child(
                "import os; os.write(1, b'x'*4096)",
                stdout_limit=512,
                killpg=killpg_with_cleanup_exception,
            )

        failure = caught.exception
        self.assertEqual(failure.reason, "output_limit")
        self.assertTrue(failure.child_reaped)
        self.assertEqual(failure.group_probe_errno, errno.EIO)
        self.assertFalse(failure.cleanup_succeeded)

    def test_cleanup_baseexception_preserves_primary_failure_and_reaping(self) -> None:
        abort = _CleanupAbort("deterministic cleanup interruption")

        def killpg_with_cleanup_abort(pgid: int, sig: int) -> None:
            if sig == 0:
                raise abort
            os.killpg(pgid, sig)

        with self.assertRaises(FakeProcessFailure) as caught:
            self.run_child(
                "import os; os.write(1, b'x'*4096)",
                stdout_limit=512,
                killpg=killpg_with_cleanup_abort,
            )

        failure = caught.exception
        self.assertEqual(failure.reason, "output_limit")
        self.assertTrue(failure.child_reaped)
        self.assertIs(failure.cleanup_exception, abort)
        self.assertFalse(failure.cleanup_succeeded)

    def test_execution_baseexception_is_reraised_after_all_finalizers(self) -> None:
        abort = _CleanupAbort("deterministic execution interruption")
        selector = _AbortSelector(abort)
        with patch(
            "tests.fakes.fake_process_boundary.selectors.DefaultSelector",
            return_value=selector,
        ):
            with self.assertRaises(_CleanupAbort) as caught:
                self.run_child("import time; time.sleep(30)")

        self.assertIs(caught.exception, abort)
        self.assertEqual(
            caught.exception.fake_process_cleanup,
            {
                "child_reaped": True,
                "signal_errno": None,
                "group_probe_errno": errno.ESRCH,
                "cleanup_succeeded": True,
                "cleanup_exception": None,
            },
        )

    def test_setup_baseexception_after_spawn_runs_all_finalizers(self) -> None:
        abort = _CleanupAbort("deterministic setup interruption")
        with patch(
            "tests.fakes.fake_process_boundary.os.set_blocking",
            side_effect=abort,
        ):
            with self.assertRaises(_CleanupAbort) as caught:
                self.run_child("import time; time.sleep(30)")

        self.assertIs(caught.exception, abort)
        self.assertTrue(caught.exception.fake_process_cleanup["child_reaped"])
        self.assertEqual(
            caught.exception.fake_process_cleanup["group_probe_errno"], errno.ESRCH
        )
        self.assertTrue(caught.exception.fake_process_cleanup["cleanup_succeeded"])

    def test_cleanup_sleep_baseexception_is_retained_after_group_signal(self) -> None:
        abort = _CleanupAbort("deterministic cleanup wait interruption")

        def group_appears_present(pgid: int, sig: int) -> None:
            if sig == 0:
                return
            os.killpg(pgid, sig)

        with patch("tests.fakes.fake_process_boundary.time.sleep", side_effect=abort):
            with self.assertRaises(FakeProcessFailure) as caught:
                self.run_child(
                    "pass",
                    killpg=group_appears_present,
                )

        failure = caught.exception
        self.assertEqual(failure.reason, "cleanup_failure")
        self.assertTrue(failure.child_reaped)
        self.assertIs(failure.cleanup_exception, abort)
        self.assertFalse(failure.cleanup_succeeded)


if __name__ == "__main__":
    unittest.main()
