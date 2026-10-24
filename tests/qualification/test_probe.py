"""Exercise probe evidence/error classification using inert children only."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import process_boundary
import provision
import real_probe
from resources import QualificationFailure


class ProbeClassificationTests(unittest.TestCase):
    def test_managed_python_is_installed_before_both_workflow_lookups(self) -> None:
        workflow = (
            Path(__file__).resolve().parents[2]
            / ".github/workflows/plumber-og-consumer-qualification.yml"
        )
        lines = [line.strip() for line in workflow.read_text().splitlines()]
        install = "uv --no-config python install --managed-python --no-bin 3.12.14"
        lookup = 'PYTHON="$(uv python find --managed-python 3.12.14)"'
        self.assertEqual(lines.count(install), 2)
        lookups = [index for index, line in enumerate(lines) if line == lookup]
        self.assertEqual(len(lookups), 2)
        for index in lookups:
            self.assertEqual(lines[index - 1], install)

    def test_reader_exception_preserves_captured_bytes_and_cleanup(self) -> None:
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

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "artifacts").mkdir()
            argv = [
                sys.executable,
                "-I",
                "-B",
                "-c",
                "import os,time; os.write(1,b'synthetic-prefix'); time.sleep(0.05); "
                "os.write(1,b'tail'); time.sleep(30)",
            ]
            with (
                patch.object(process_boundary.os, "read", side_effect=interrupted_read),
                self.assertRaisesRegex(OSError, "synthetic reader interruption"),
            ):
                real_probe.invoke(root, "reader", argv)
            self.assertTrue((root / "artifacts/reader.stdout.txt").is_file())
            self.assertEqual(
                (root / "artifacts/reader.stdout.txt").read_bytes(), b"synthetic-prefix"
            )
            evidence = json.loads((root / "artifacts/reader.lifecycle.json").read_bytes())
            self.assertTrue(evidence["child_reaped"])
            self.assertTrue(evidence["cleanup_succeeded"])
            self.assertIs(type(evidence["returncode"]), int)

    def test_provisioning_setup_interruption_retains_terminal_evidence(self) -> None:
        class Abort(BaseException):
            pass

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "artifacts").mkdir()
            with (
                patch.object(process_boundary.os, "set_blocking", side_effect=Abort("setup")),
                self.assertRaises(Abort),
            ):
                provision.run_tool(
                    root,
                    "setup",
                    [sys.executable, "-I", "-B", "-c", "import time; time.sleep(30)"],
                )
            self.assertTrue((root / "artifacts/setup.json").is_file())
            evidence = json.loads((root / "artifacts/setup.json").read_bytes())
            self.assertTrue(evidence["child_reaped"])
            self.assertTrue(evidence["cleanup_succeeded"])
            self.assertEqual((root / "artifacts/setup.stdout.txt").read_bytes(), b"")

    def test_expected_refusal_is_a_passing_control_with_lifecycle_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "artifacts").mkdir()
            argv = [
                sys.executable,
                "-I",
                "-B",
                "-c",
                'import os; os.write(2,b\'{"error":"source_rejected"}\\n\'); raise SystemExit(4)',
            ]
            result = real_probe.invoke(
                root, "negative", argv, expected_exit=4, expected_error="source_rejected"
            )
            self.assertEqual(result["expected_negative"], "source_rejected")
            self.assertTrue(result["child_reaped"])
            self.assertTrue(result["cleanup_succeeded"])
            self.assertEqual(
                json.loads((root / "artifacts/negative.stderr.txt").read_bytes()),
                {"error": "source_rejected"},
            )

    def test_wrong_error_is_not_accepted_merely_because_exit_matches(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "artifacts").mkdir()
            argv = [
                sys.executable,
                "-I",
                "-B",
                "-c",
                'import os; os.write(2,b\'{"error":"other"}\\n\'); raise SystemExit(4)',
            ]
            with self.assertRaises(QualificationFailure):
                real_probe.invoke(
                    root, "negative", argv, expected_exit=4, expected_error="source_rejected"
                )
            self.assertTrue((root / "artifacts/negative.lifecycle.json").is_file())

    def test_shape_failure_retains_synthetic_stdout_without_rerunning(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "artifacts").mkdir()
            argv = [sys.executable, "-I", "-B", "-c", 'import os; os.write(1,b"[]\\n")']
            with self.assertRaises(QualificationFailure):
                real_probe.invoke(root, "shape", argv)
            self.assertEqual((root / "artifacts/shape.stdout.txt").read_bytes(), b"[]\n")
            self.assertTrue(
                json.loads((root / "artifacts/shape.lifecycle.json").read_bytes())[
                    "cleanup_succeeded"
                ]
            )

    def test_negative_control_must_not_succeed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "artifacts").mkdir()
            with self.assertRaises(QualificationFailure):
                real_probe.invoke(
                    root,
                    "unexpected",
                    [sys.executable, "-I", "-B", "-c", "pass"],
                    expected_exit=4,
                    expected_error="source_rejected",
                )


if __name__ == "__main__":
    unittest.main()
