"""Offline negative controls; native observations are separate evidence."""

import errno
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

HERE = Path(__file__).resolve().parent


class PreflightClassificationTests(unittest.TestCase):
    def setUp(self):
        source = HERE / "preflight.py"
        self.assertTrue(source.is_file(), "MA native preflight is not implemented")
        spec = importlib.util.spec_from_file_location("ma_preflight", source)
        if spec is None or spec.loader is None:
            self.fail("MA preflight module unavailable")
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    @staticmethod
    def record(success, error=0, resolver_error=0):
        return {
            "succeeded": success,
            "error": error,
            "resolver_error": resolver_error,
        }

    def test_permission_denial_needs_successful_positive_and_no_side_effect(self):
        for error in (errno.EPERM, errno.EACCES):
            self.assertEqual(
                self.module.classify_control(
                    self.record(True),
                    self.record(False, error),
                    unchanged=True,
                    positive_observed=True,
                    negative_observed=False,
                ),
                "DENIED",
            )

    def test_unavailable_positive_never_counts_as_denial(self):
        self.assertEqual(
            self.module.classify_control(
                self.record(False, errno.ENETUNREACH),
                self.record(False, errno.EPERM),
                unchanged=True,
                positive_observed=False,
                negative_observed=False,
            ),
            "UNTESTABLE",
        )

    def test_unrelated_errors_malformed_rows_or_mutation_refuse_the_run(self):
        for negative, unchanged, observed in (
            (self.record(False, errno.ECONNREFUSED), True, False),
            (self.record(False, 0, -2), True, False),
            (self.record(1), True, False),
            ({}, True, False),
            (self.record(False, errno.EPERM), False, False),
            (self.record(False, errno.EPERM), True, True),
        ):
            self.assertNotEqual(
                self.module.classify_control(
                    self.record(True),
                    negative,
                    unchanged=unchanged,
                    positive_observed=True,
                    negative_observed=observed,
                ),
                "DENIED",
            )

    def test_successful_confined_operation_is_forbidden(self):
        self.assertEqual(
            self.module.classify_control(
                self.record(True),
                self.record(True),
                unchanged=True,
                positive_observed=True,
                negative_observed=True,
            ),
            "ALLOWED",
        )

    def test_unavailable_positive_prevents_confined_execution(self):
        self.assertTrue(hasattr(self.module, "confined_after_positive"))
        launched = []

        def confined():
            launched.append(True)
            return self.record(False, errno.EPERM)

        with self.assertRaises(RuntimeError):
            self.module.confined_after_positive(
                self.record(False, errno.ENETUNREACH), False, confined
            )
        self.assertEqual(launched, [])
        self.assertEqual(
            self.module.confined_after_positive(self.record(True), True, confined),
            {"succeeded": False, "error": errno.EPERM, "resolver_error": 0},
        )
        self.assertEqual(launched, [True])

    def test_cleanup_requires_reap_esrch_and_every_existing_gate(self):
        self.assertTrue(hasattr(self.module, "require_cleanup"))
        good = {
            "child_reaped": True,
            "cleanup_succeeded": True,
            "group_probe_errno": errno.ESRCH,
            "events": (),
            "cleanup_exception": None,
            "observations": ("signal_eperm",),
        }
        self.module.require_cleanup(SimpleNamespace(**good))
        for change in (
            {"child_reaped": False},
            {"cleanup_succeeded": False},
            {"group_probe_errno": errno.EPERM},
            {"events": ("reader",)},
            {"cleanup_exception": RuntimeError("synthetic cleanup error")},
        ):
            with self.assertRaises(RuntimeError):
                self.module.require_cleanup(SimpleNamespace(**{**good, **change}))

    def test_profile_accepts_only_canonical_absolute_read_grants(self):
        self.assertTrue(hasattr(self.module, "profile_text"))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            graph, producer, base = (root / name for name in ("graph", "producer", "base"))
            for path in (graph, producer, base):
                path.mkdir()
            binary = root / "canary"
            binary.write_bytes(b"synthetic native-file placeholder")
            profile = self.module.profile_text(graph, producer, base, binary)
            self.assertIsInstance(profile, str)
            self.assertGreater(len(profile), 100)
            for rejected in (Path("relative"), root / 'bad"grant', root / "bad\ngrant"):
                with self.assertRaises(RuntimeError):
                    self.module.profile_text(rejected, producer, base, binary)

    def test_profile_keeps_root_read_grant_narrow(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            graph, producer, base = (root / name for name in ("graph", "producer", "base"))
            for path in (graph, producer, base):
                path.mkdir()
            binary = root / "canary"
            binary.write_bytes(b"synthetic native-file placeholder")
            lines = self.module.profile_text(graph, producer, base, binary).splitlines()
            self.assertEqual(
                [line for line in lines if line.startswith("(deny ")],
                [
                    "(deny network*)",
                    "(deny mach-lookup)",
                    "(deny file-write*)",
                    "(deny file-read*)",
                ],
            )
            expected = {
                "(allow default)",
                '(allow file-write-data (literal "/dev/null"))',
                '(allow file-read-data (literal "/"))',
            }
            for path in (
                graph,
                producer,
                base,
                Path("/System"),
                Path("/usr/lib"),
                Path("/usr/share/locale"),
                Path("/private/var/db/dyld"),
            ):
                expected.add("(allow file-read* (subpath " + json.dumps(str(path)) + "))")
            for path in (binary, Path("/dev/null"), Path("/dev/urandom"), Path("/dev/random")):
                expected.add("(allow file-read* (literal " + json.dumps(str(path)) + "))")
            for path in {
                parent for grant in (graph, producer, base, binary) for parent in grant.parents
            }:
                expected.add("(allow file-read-metadata (literal " + json.dumps(str(path)) + "))")
            self.assertCountEqual([line for line in lines if line.startswith("(allow ")], expected)

    def test_listener_finalization_attempts_every_owned_step(self):
        self.assertTrue(hasattr(self.module, "finish_listener"))
        listener, address = Mock(), Mock()
        listener.close.side_effect = KeyboardInterrupt()
        with self.assertRaises(self.module.CleanupUncertain) as caught:
            self.module.finish_listener(listener, address)
        listener.close.assert_called_once()
        address.unlink.assert_called_once()
        self.assertIn("close", str(caught.exception))

        listener.reset_mock(side_effect=True)
        address.reset_mock(side_effect=True)
        self.module.finish_listener(listener, None)
        listener.close.assert_called_once()
        address.unlink.assert_not_called()


if __name__ == "__main__":
    unittest.main()
