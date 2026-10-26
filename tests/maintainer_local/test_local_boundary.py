"""Offline controls for the separate maintainer-local synthetic entry."""

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent


def load_support():
    source = HERE / "local_support.py"
    if not source.is_file():
        raise AssertionError("MA local boundary is not implemented")
    spec = importlib.util.spec_from_file_location("ma_local_support", source)
    if spec is None or spec.loader is None:
        raise AssertionError("MA local module unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LocalBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.module = load_support()

    def test_ci_refusal_precedes_root_access(self):
        for environment in ({"CI": "true"}, {"GITHUB_ACTIONS": "true"}):
            with (
                patch.dict(os.environ, environment, clear=True),
                patch.object(self.module.os, "lstat", side_effect=AssertionError("root touched")),
            ):
                with self.assertRaisesRegex(RuntimeError, "local-only"):
                    self.module.require_local_context()

    def test_wrong_runtime_is_not_an_approximate_producer_tuple(self):
        with (
            patch.dict(os.environ, {}, clear=True),
            patch.object(self.module.platform, "system", return_value="Darwin"),
            patch.object(self.module.platform, "machine", return_value="arm64"),
        ):
            for version in ("3.12.13", "3.12.15", "3.13.15"):
                with (
                    patch.object(self.module.platform, "python_version", return_value=version),
                    self.assertRaisesRegex(RuntimeError, "runtime"),
                ):
                    self.module.require_local_context()
            with patch.object(self.module.platform, "python_version", return_value="3.12.14"):
                self.module.require_local_context()

    def test_arbitrary_root_is_rejected_before_metadata_or_content(self):
        with (
            patch.object(self.module.os, "lstat", side_effect=AssertionError("root touched")),
            self.assertRaisesRegex(RuntimeError, "task root"),
        ):
            self.module.admit_root(Path("/not-a-task/synthetic"), fresh=False)

    def test_existing_owned_root_requires_private_mode_and_no_symlink(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary).resolve()
            root = parent / "trama-ma-owned"
            root.mkdir(mode=0o700)
            with patch.object(self.module, "TEMP_PARENT", parent):
                self.assertEqual(self.module.admit_root(root, fresh=False), root)
                with self.assertRaises(RuntimeError):
                    self.module.admit_root(root, fresh=True)
                root.chmod(0o777)
                with self.assertRaises(RuntimeError):
                    self.module.admit_root(root, fresh=False)
                root.chmod(0o700)
                alias = parent / "trama-ma-alias"
                alias.symlink_to(root, target_is_directory=True)
                with self.assertRaises(RuntimeError):
                    self.module.admit_root(alias, fresh=False)

    def test_owner_only_root_rejects_read_or_search_access_for_others(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary).resolve()
            root = parent / "trama-ma-permissions"
            root.mkdir(mode=0o700)
            with patch.object(self.module, "TEMP_PARENT", parent):
                for mode in (0o755, 0o750, 0o704, 0o701):
                    with self.subTest(mode=mode):
                        root.chmod(mode)
                        with self.assertRaises(RuntimeError):
                            self.module.admit_root(root, fresh=False)

    def test_task_reads_reject_links_fifo_and_oversize_before_content(self):
        self.assertTrue(hasattr(self.module, "read_task_file"))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            root.chmod(0o700)
            artifacts = root / "artifacts"
            artifacts.mkdir()
            leaf = artifacts / "receipt.json"
            leaf.write_bytes(b"{}")
            self.assertEqual(self.module.read_task_file(root, "artifacts/receipt.json", 32), b"{}")
            leaf.unlink()
            leaf.symlink_to(root / "never-read")
            with self.assertRaises(RuntimeError):
                self.module.read_task_file(root, "artifacts/receipt.json", 32)
            leaf.unlink()
            os.mkfifo(leaf)
            with self.assertRaises(RuntimeError):
                self.module.read_task_file(root, "artifacts/receipt.json", 32)
            leaf.unlink()
            leaf.write_bytes(b"x" * 33)
            with self.assertRaises(RuntimeError):
                self.module.read_task_file(root, "artifacts/receipt.json", 32)
            artifacts.rename(root / "preserved-artifacts")
            artifacts.symlink_to(root / "preserved-artifacts", target_is_directory=True)
            with self.assertRaises(RuntimeError):
                self.module.read_task_file(root, "artifacts/receipt.json", 32)

    def test_nonexistent_root_is_only_a_fresh_provisioning_candidate(self):
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary).resolve()
            root = parent / "trama-ma-fresh"
            with patch.object(self.module, "TEMP_PARENT", parent):
                self.assertEqual(self.module.admit_root(root, fresh=True), root)
                self.assertFalse(root.exists())
                with self.assertRaises(RuntimeError):
                    self.module.admit_root(root, fresh=False)


if __name__ == "__main__":
    unittest.main()
