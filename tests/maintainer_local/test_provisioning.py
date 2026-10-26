"""Offline tests for the separate local provisioner; no package acquisition."""

import importlib.util
import json
import os
import tempfile
import unittest
from importlib.machinery import all_suffixes
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent


class LocalProvisioningTests(unittest.TestCase):
    def setUp(self):
        source = HERE / "local_provision.py"
        self.assertTrue(source.is_file(), "MA local provisioning entry is absent")
        spec = importlib.util.spec_from_file_location("ma_local_provision", source)
        if spec is None or spec.loader is None:
            self.fail("MA provisioning source unavailable")
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_ci_cannot_reach_acquisition_or_arbitrary_root(self):
        with (
            patch.dict(os.environ, {"CI": "true"}, clear=True),
            patch.object(
                self.module.provision, "download", side_effect=AssertionError("download started")
            ),
            self.assertRaisesRegex(RuntimeError, "local-only"),
        ):
            self.module.provision_local(Path("/not-a-task"))

    def test_startup_hooks_are_rejected_without_importing_them(self):
        with tempfile.TemporaryDirectory() as temporary:
            site = Path(temporary).resolve()
            self.module.check_startup(site)
            for name in ("unexpected.pth", "sitecustomize.py", "usercustomize"):
                path = site / name
                path.write_text("raise AssertionError('must never execute')")
                with self.assertRaises(RuntimeError):
                    self.module.check_startup(site)
                path.unlink()
            alias = site / "unexpected-link"
            alias.symlink_to(site, target_is_directory=True)
            with self.assertRaises(RuntimeError):
                self.module.check_startup(site)

    def test_cli_never_accepts_a_graph_selector_or_optional_bypass(self):
        with self.assertRaises(RuntimeError):
            self.module.parse_root(["--graph-root", "/not-a-task"])
        with self.assertRaises(RuntimeError):
            self.module.parse_root(["--root", "/private/tmp/trama-ma-a", "--skip-preflight"])
        self.assertEqual(
            self.module.parse_root(["--root", "/private/tmp/trama-ma-a"]),
            Path("/private/tmp/trama-ma-a"),
        )

    def test_all_importable_customization_suffixes_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            site = Path(temporary).resolve()
            for prefix in ("sitecustomize", "usercustomize"):
                for suffix in all_suffixes():
                    path = site / (prefix + suffix)
                    path.write_bytes(b"synthetic bytes; must never be imported")
                    with self.subTest(name=path.name), self.assertRaises(RuntimeError):
                        self.module.check_startup(site)
                    path.unlink()

    def test_final_provisioning_failure_cannot_leave_a_success_receipt(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve() / "trama-ma-provision"

            def make_environment(selected, name):
                producer = selected / name
                (producer / "bin").mkdir(parents=True)
                (producer / "lib/python3.12/site-packages").mkdir(parents=True)
                binary = producer / "bin/python"
                binary.symlink_to(self.module.sys.executable)
                (producer / "pyvenv.cfg").write_bytes(b"synthetic configuration")
                return binary

            with (
                patch.object(self.module.local_support, "require_local_context"),
                patch.object(self.module.local_support, "admit_root"),
                patch.object(self.module, "base_identity", return_value={}),
                patch.object(
                    self.module.provision, "download", return_value=root / "synthetic.whl"
                ),
                patch.object(self.module.shutil, "which", return_value="/synthetic-gh"),
                patch.object(self.module.provision, "run_tool"),
                patch.object(self.module.resources, "owner_resource", return_value=b"synthetic"),
                patch.object(
                    self.module.provision, "make_environment", side_effect=make_environment
                ),
                patch.object(self.module.provision, "install"),
                patch.object(self.module, "environment_digest", return_value="synthetic-digest"),
                patch.object(
                    self.module.provision,
                    "disk_admit",
                    side_effect=[None, RuntimeError("disk refusal")],
                ),
            ):
                with self.assertRaisesRegex(RuntimeError, "disk refusal"):
                    self.module.provision_local(root)
                receipt = json.loads((root / "artifacts/local-provision.json").read_bytes())
                self.assertIs(receipt["complete"], False)
                with (
                    patch.object(
                        self.module.resources,
                        "verify_file",
                        side_effect=AssertionError("artifact touched"),
                    ),
                    self.assertRaises(RuntimeError),
                ):
                    self.module.verified_local_inputs(root)

    def test_producer_executable_must_resolve_to_the_verified_base(self):
        self.assertTrue(hasattr(self.module, "producer_interpreter"))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            base = root / "base-python"
            base.write_bytes(b"synthetic base placeholder")
            binary = root / "producer/bin/python"
            binary.parent.mkdir(parents=True)
            binary.symlink_to(base)
            with patch.object(self.module.sys, "executable", str(base)):
                self.assertEqual(self.module.producer_interpreter(root), binary)
                binary.unlink()
                binary.write_bytes(b"replacement must never be executed")
                with self.assertRaises(RuntimeError):
                    self.module.producer_interpreter(root)


if __name__ == "__main__":
    unittest.main()
