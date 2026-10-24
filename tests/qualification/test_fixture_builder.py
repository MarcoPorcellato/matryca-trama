"""Only fresh authenticated synthetic fixtures receive client capabilities."""

import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import process_boundary  # noqa: F401 - establish reviewed package origins first.
import fixture_builder
from resources import QualificationFailure
from trama_plumber_client._fixture import fixture_root


class FixtureBuilderTests(unittest.TestCase):
    def test_authenticated_bytes_in_a_fresh_root_receive_a_structural_handle(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            wheel = root / "illustrative.whl"
            raw = b"- illustrative synthetic fixture\n"
            member = zipfile.ZipInfo("owned/fixtures/pages/Example.md")
            member.external_attr = 0o100600 << 16
            with zipfile.ZipFile(wheel, "w") as archive:
                archive.writestr(member, raw)
            manifest = {
                "files": {
                    "pages/Example.md": {"sha256": hashlib.sha256(raw).hexdigest()}
                }
            }
            fixture = fixture_builder.build_fixture(
                root, wheel, {"resource_prefix": "owned/"}, manifest
            )
            self.assertEqual(fixture_root(fixture), fixture.canonical_root)
            self.assertEqual(
                (Path(fixture.canonical_root) / "pages/Example.md").read_bytes(), raw
            )
            self.assertNotEqual(fixture.input_alias, fixture.canonical_root)

    def test_existing_or_escaping_builder_root_stops_before_any_member_read(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / "synthetic").symlink_to(root.parent, target_is_directory=True)
            with (
                patch.object(fixture_builder.resources, "read_member") as read,
                self.assertRaises(FileExistsError),
            ):
                fixture_builder.build_fixture(root, root / "unused.whl", {}, {})
            read.assert_not_called()

    def test_file_bound_control_is_fixed_shape_and_detects_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            graph = fixture_builder.build_file_bound_control(root)
            before = fixture_builder.file_bound_ledger(graph)
            self.assertEqual(before["files"], 1025)
            self.assertEqual(fixture_builder.file_bound_ledger(graph), before)
            (graph / "pages/synthetic-0000.md").write_bytes(b"changed")
            with self.assertRaises(QualificationFailure):
                fixture_builder.file_bound_ledger(graph)


if __name__ == "__main__":
    unittest.main()
