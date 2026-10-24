"""Reject altered archives, unsafe members and startup hooks before imports."""

import hashlib
import json
import tempfile
import unittest
import warnings
import zipfile
from pathlib import Path

import resources


class ResourceTests(unittest.TestCase):
    def test_hash_and_size_are_both_required(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            file = Path(root) / "synthetic.bin"
            file.write_bytes(b"abc")
            digest = hashlib.sha256(b"abc").hexdigest()
            resources.verify_file(file, digest, 3)
            for wrong_digest, wrong_size in (("0" * 64, 3), (digest, 4)):
                with (
                    self.subTest(size=wrong_size),
                    self.assertRaises(resources.QualificationFailure),
                ):
                    resources.verify_file(file, wrong_digest, wrong_size)

    def test_duplicate_zip_members_and_oversize_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            archive = Path(root) / "synthetic.whl"
            with zipfile.ZipFile(archive, "w") as z:
                z.writestr("allowlisted", b"abc")
            self.assertEqual(resources.read_member(archive, "allowlisted", limit=3), b"abc")
            with self.assertRaises(resources.QualificationFailure):
                resources.read_member(archive, "allowlisted", limit=2)
            with zipfile.ZipFile(archive, "a") as z, warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                z.writestr("allowlisted", b"other")
            with self.assertRaises(resources.QualificationFailure):
                resources.read_member(archive, "allowlisted")

    def test_only_explicit_members_are_read_and_digest_checked(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            archive = Path(root) / "synthetic.whl"
            with zipfile.ZipFile(archive, "w") as z:
                z.writestr("owner/schema.json", b"{}")
            with self.assertRaises(resources.QualificationFailure):
                resources.owner_resource(
                    archive,
                    {"resource_prefix": "owner/", "resources": {"schema.json": "0" * 64}},
                    "schema.json",
                )

    def test_static_environment_check_rejects_hooks_before_startup(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            site = Path(root)
            (site / "allowed.py").write_text("", encoding="utf-8")
            resources.check_site_packages(site, ["allowed"])
            for hook in (
                "evil.pth",
                "sitecustomize.py",
                "usercustomize.py",
                "tests.py",
                "sitecustomize.pyc",
                "foreign.so",
            ):
                with self.subTest(hook=hook):
                    file = site / hook
                    file.write_text("raise RuntimeError('must never execute')", encoding="utf-8")
                    with self.assertRaises(resources.QualificationFailure):
                        resources.check_site_packages(site, ["allowed"])
                    file.unlink()

    def test_json_rejects_duplicates_nonfinite_and_multiple_documents(self) -> None:
        for raw in (b'{"x":1,"x":2}', b'{"x":NaN}', b"{} {}", b"[]"):
            with self.subTest(raw=raw), self.assertRaises(resources.QualificationFailure):
                resources.strict_json(raw)
        self.assertEqual(resources.strict_json(b'{"x":1}\n'), {"x": 1})

    def test_fixture_ledger_rejects_symlinks_and_detects_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as root:
            graph = Path(root) / "graph"
            graph.mkdir()
            file = graph / "page.md"
            file.write_text("synthetic", encoding="utf-8")
            before = resources.fixture_ledger(graph)
            file.write_text("changed", encoding="utf-8")
            self.assertNotEqual(before, resources.fixture_ledger(graph))
            (graph / "alias.md").symlink_to(file)
            with self.assertRaises(resources.QualificationFailure):
                resources.fixture_ledger(graph)

    def test_redaction_retains_json_shape_and_original_digest(self) -> None:
        raw = b'{"id":"synthetic","path":"/runner/workspace/private"}\n'
        redacted = resources.sanitize(raw, replacements={"/runner/workspace": "<runner>"})
        self.assertEqual(json.loads(redacted)["id"], "synthetic")
        self.assertNotIn(b"/runner/workspace", redacted)
        self.assertEqual(json.loads(redacted)["path"], "<runner>/private")


if __name__ == "__main__":
    unittest.main()
