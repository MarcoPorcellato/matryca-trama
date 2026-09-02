"""Containment and deterministic-evidence tests for synthetic fixtures."""

import json
from pathlib import Path, PurePosixPath
import tempfile
import unittest

from trama_core.digests import sha256_bytes
from trama_core.normalization import (
    canonical_json,
    resolve_fixture_path,
    verified_fixture_path,
)


FIXTURES_ROOT = Path(__file__).parents[1] / "fixtures"


class FixtureBoundaryTests(unittest.TestCase):
    """Synthetic fixture access never crosses its selected root."""

    def test_fixture_path_rejects_absolute_and_parent_escape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "inside.md").write_text("inside\n", encoding="utf-8")

            for relative in (PurePosixPath("/secret.md"), PurePosixPath("../secret.md")):
                with self.subTest(relative=relative):
                    with self.assertRaisesRegex(ValueError, "outside fixture root"):
                        resolve_fixture_path(root, relative)

    def test_fixture_path_rejects_symlink_target_outside_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary_root = Path(directory)
            root = temporary_root / "fixtures"
            root.mkdir()
            outside = temporary_root / "secret.md"
            outside.write_text("secret\n", encoding="utf-8")
            (root / "escape.md").symlink_to(outside)

            with self.assertRaisesRegex(ValueError, "outside fixture root"):
                resolve_fixture_path(root, PurePosixPath("escape.md"))

    def test_canonical_json_is_stable_for_mapping_order_and_unicode(self) -> None:
        self.assertEqual(canonical_json({"b": 2, "a": 1}), b'{"a":1,"b":2}')
        self.assertEqual(
            canonical_json({"\u00e4": "text", "z": [True, None]}),
            b'{"z":[true,null],"\xc3\xa4":"text"}',
        )

    def test_sha256_bytes_returns_standard_digest(self) -> None:
        self.assertEqual(
            sha256_bytes(b"abc"),
            "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad",
        )

    def test_verified_fixture_path_checks_manifest_before_returning_path(
        self,
    ) -> None:
        fixture = verified_fixture_path(
            FIXTURES_ROOT,
            PurePosixPath("og-minimal/pages/Example.md"),
        )

        self.assertEqual(fixture, (FIXTURES_ROOT / "og-minimal/pages/Example.md").resolve())

    def test_verified_fixture_path_rejects_manifest_digest_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pages = root / "pages"
            pages.mkdir()
            fixture = pages / "Example.md"
            fixture.write_text("synthetic fixture\n", encoding="utf-8")
            (root / "fixture-manifest.json").write_text(
                json.dumps(
                    {
                        "files": {
                            "pages/Example.md": "0" * 64,
                        },
                        "fixture_id": "temporary",
                    }
                ),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "fixture digest mismatch"):
                verified_fixture_path(root, PurePosixPath("pages/Example.md"))


if __name__ == "__main__":
    unittest.main()
