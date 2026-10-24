"""Unchanged lifecycle controls for the moved synthetic-client boundary."""

import errno
import os
import signal
import sys
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from trama_plumber_client import _process as boundary


class QualificationProcessTests(unittest.TestCase):
    def test_execution_exception_retains_eperm_and_captured_output(self) -> None:
        original_read = os.read
        captured_prefix = False

        def interrupted_read(fd: int, size: int) -> bytes:
            nonlocal captured_prefix
            if captured_prefix:
                raise OSError("synthetic reader interruption")
            raw = original_read(fd, size)
            if raw == b"synthetic-prefix":
                captured_prefix = True
            return raw

        def observed_signal(pgid: int, sig: int) -> None:
            os.killpg(pgid, sig)
            if sig == signal.SIGKILL:
                raise PermissionError(errno.EPERM, "synthetic post-signal observation")

        with (
            patch.object(boundary.os, "read", side_effect=interrupted_read),
            self.assertRaisesRegex(OSError, "synthetic reader interruption") as caught,
        ):
            self.run_child(
                "import os,time; os.write(1,b'synthetic-prefix'); time.sleep(0.05); "
                "os.write(1,b'tail'); time.sleep(30)",
                killpg=observed_signal,
            )
        self.assertTrue(hasattr(caught.exception, "process_evidence"))
        evidence = caught.exception.process_evidence
        self.assertEqual(evidence.stdout, b"synthetic-prefix")
        self.assertTrue(evidence.child_reaped)
        self.assertTrue(evidence.cleanup_succeeded)
        self.assertEqual(evidence.group_probe_errno, errno.ESRCH)
        self.assertIn("signal:EPERM", evidence.observations)

    def run_child(self, code: str, **options: Any) -> boundary.ProcessResult:
        self.assertEqual(
            Path(boundary.__file__).resolve(),
            Path(__file__).resolve().parents[2]
            / "packages/plumber-client/src/trama_plumber_client/_process.py",
        )
        return boundary.run_process(
            [sys.executable, "-I", "-B", "-c", code],
            timeout_seconds=options.pop("timeout_seconds", 5),
            **options,
        )

    def test_success_requires_reap_esrch_and_closed_resources(self) -> None:
        result = self.run_child("import os; os.write(1, b'synthetic')")
        self.assertEqual(result.stdout, b"synthetic")
        self.assertEqual(result.stderr, b"")
        self.assertTrue(result.child_reaped)
        self.assertTrue(result.cleanup_succeeded)
        self.assertEqual(result.group_probe_errno, errno.ESRCH)

    def test_eperm_observation_races_zero_one_two_times_before_esrch(self) -> None:
        for count in (0, 1, 2):
            with self.subTest(races=count):
                probes = 0

                def transient_eperm(pgid: int, sig: int, limit: int = count) -> None:
                    nonlocal probes
                    if sig == 0 and probes < limit:
                        probes += 1
                        raise PermissionError(errno.EPERM, "synthetic unsignalable group")
                    return os.killpg(pgid, sig)

                result = self.run_child("pass", killpg=transient_eperm)
                self.assertTrue(result.child_reaped)
                self.assertTrue(result.cleanup_succeeded)
                self.assertEqual(result.group_probe_errno, errno.ESRCH)
                self.assertEqual(len(result.observations), count)

    def test_initial_eperm_signal_is_observation_not_cleanup_success(self) -> None:
        def deny_signal(pgid: int, sig: int) -> None:
            if sig == signal.SIGKILL:
                raise PermissionError(errno.EPERM, "synthetic signal denial")
            return os.killpg(pgid, sig)

        with self.assertRaises(boundary.ProcessFailure) as caught:
            self.run_child("import time; time.sleep(30)", timeout_seconds=0.05, killpg=deny_signal)
        failure = caught.exception
        self.assertEqual(failure.reason, "timeout")
        self.assertTrue(failure.child_reaped)
        self.assertEqual(failure.group_probe_errno, errno.ESRCH)
        self.assertTrue(failure.cleanup_succeeded)
        self.assertTrue(failure.observations)

    def test_poll_running_zero_one_two_times_for_a_zombie_only_group(self) -> None:
        for delayed_polls, expected_observations in ((0, 0), (1, 2), (2, 4)):
            with self.subTest(delayed_polls=delayed_polls):

                class Zombie:
                    returncode = None
                    calls = 0

                    def poll(self, limit: int = delayed_polls) -> int | None:
                        if self.calls < limit:
                            self.calls += 1
                            return None
                        self.returncode = 0
                        return 0

                child = Zombie()

                def group(pgid: int, sig: int, owner: Zombie = child) -> None:
                    if owner.returncode is None:
                        raise PermissionError(errno.EPERM, "synthetic zombie race")
                    raise ProcessLookupError(errno.ESRCH, "synthetic reaped group")

                observations, events = [], []
                code, gone = boundary._confirm_group_gone(
                    child, group, 123, boundary.time.monotonic() + 0.2, observations, events
                )
                self.assertEqual(code, errno.ESRCH)
                self.assertTrue(gone)
                self.assertEqual(len(observations), expected_observations)
                self.assertEqual(events, [])

    def test_eperm_until_deadline_promotes_observations_to_events(self) -> None:
        def denied_group(pgid: int, sig: int) -> None:
            if sig == 0:
                raise PermissionError(errno.EPERM, "synthetic persistent observation")
            return os.killpg(pgid, sig)

        with (
            patch.object(boundary, "_CLEANUP_SECONDS", 0.05),
            self.assertRaises(boundary.ProcessFailure) as caught,
        ):
            self.run_child("pass", killpg=denied_group)
        self.assertTrue(caught.exception.child_reaped)
        self.assertFalse(caught.exception.cleanup_succeeded)
        self.assertTrue(caught.exception.observations)
        self.assertTrue(caught.exception.events)

    def test_non_eperm_signal_errors_never_become_success(self) -> None:
        for error in (errno.EACCES, errno.EINTR, errno.EINVAL):
            with self.subTest(error=error):

                def rejected_probe(pgid: int, sig: int, code: int = error) -> None:
                    if sig == 0:
                        raise OSError(code, "synthetic fatal group error")
                    return os.killpg(pgid, sig)

                with self.assertRaises(boundary.ProcessFailure) as caught:
                    self.run_child("pass", killpg=rejected_probe)
                self.assertFalse(caught.exception.cleanup_succeeded)
                self.assertTrue(caught.exception.child_reaped)
                self.assertEqual(caught.exception.group_probe_errno, error)

    def test_observations_survive_cleanup_exception(self) -> None:
        class Abort(BaseException):
            pass

        def denied_group(pgid: int, sig: int) -> None:
            if sig == 0:
                raise PermissionError(errno.EPERM, "synthetic persistent observation")
            return os.killpg(pgid, sig)

        with (
            patch.object(boundary.time, "sleep", side_effect=Abort("synthetic interruption")),
            self.assertRaises(boundary.ProcessFailure) as caught,
        ):
            self.run_child("pass", killpg=denied_group)
        self.assertTrue(caught.exception.observations)
        self.assertTrue(caught.exception.events)
        self.assertIsInstance(caught.exception.cleanup_exception, Abort)
        self.assertTrue(caught.exception.child_reaped)

    def test_both_stream_caps_are_incremental(self) -> None:
        for fd, option in ((1, "stdout_limit"), (2, "stderr_limit")):
            with self.subTest(fd=fd):
                with self.assertRaises(boundary.ProcessFailure) as caught:
                    self.run_child(f"import os; os.write({fd}, b'x' * 2048)", **{option: 512})
                failure = caught.exception
                self.assertEqual(failure.reason, "output_limit")
                self.assertEqual(len(failure.stdout if fd == 1 else failure.stderr), 512)
                self.assertTrue(failure.cleanup_succeeded)

    def test_closed_streams_do_not_bypass_execution_timeout(self) -> None:
        with self.assertRaises(boundary.ProcessFailure) as caught:
            self.run_child(
                "import os,time; os.close(1); os.close(2); time.sleep(30)", timeout_seconds=0.05
            )
        self.assertEqual(caught.exception.reason, "timeout")
        self.assertTrue(caught.exception.cleanup_succeeded)

    def test_nonzero_exit_retains_output_and_cleanup(self) -> None:
        with self.assertRaises(boundary.ProcessFailure) as caught:
            self.run_child(
                'import os; os.write(2,b\'{"error":"source_rejected"}\\n\'); raise SystemExit(4)'
            )
        self.assertEqual(caught.exception.returncode, 4)
        self.assertEqual(caught.exception.stderr, b'{"error":"source_rejected"}\n')
        self.assertTrue(caught.exception.cleanup_succeeded)


if __name__ == "__main__":
    unittest.main()
