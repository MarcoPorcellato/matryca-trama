"""Public Parser loader contract for owned synthetic fixtures."""

from collections.abc import Iterator
from contextlib import contextmanager
import json
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import unittest

from trama_core import sha256_bytes
from trama_parser_bridge import load_og_fixture


FIXTURES_ROOT = Path(__file__).parents[1] / "fixtures"


class ParserLoaderTests(unittest.TestCase):
    """The Parser boundary loads only verified synthetic fixtures."""

    def test_loader_returns_graph_for_synthetic_root(self) -> None:
        """Missing verified loader call leaves the fixture unreadable as a graph."""

        graph = load_og_fixture(FIXTURES_ROOT, PurePosixPath("og-minimal"))

        self.assertEqual(graph.graph_path, (FIXTURES_ROOT / "og-minimal").resolve())
        self.assertIsNotNone(graph.get_page("Example"))

    def test_loader_rejects_path_outside_selected_root(self) -> None:
        """Missing containment check would allow fixture-root traversal."""

        with self.assertRaisesRegex(ValueError, "outside fixture root"):
            load_og_fixture(FIXTURES_ROOT, PurePosixPath("../outside"))

    def test_loader_rejects_unmanifested_descendant(self) -> None:
        """A Parser-readable file outside manifest coverage must not load."""

        with self._copied_fixture_root() as fixture_root:
            (fixture_root / "og-minimal" / "pages" / "Unlisted.md").write_text(
                "title:: Unlisted\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "fixture manifest coverage"):
                load_og_fixture(fixture_root, PurePosixPath("og-minimal"))

    def test_loader_rejects_missing_manifested_descendant(self) -> None:
        """A manifest entry absent from loader directory must not load."""

        with self._copied_fixture_root() as fixture_root:
            manifest_path = fixture_root / "fixture-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["files"]["og-minimal/pages/Missing.md"] = sha256_bytes(
                b"title:: Missing\n",
            )
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "fixture manifest coverage"):
                load_og_fixture(fixture_root, PurePosixPath("og-minimal"))

    def test_loader_rejects_symlinked_descendant(self) -> None:
        """A Parser-readable symlink must not enter fixture directory load."""

        with self._copied_fixture_root() as fixture_root:
            pages = fixture_root / "og-minimal" / "pages"
            (pages / "Alias.md").symlink_to(pages / "Example.md")

            with self.assertRaisesRegex(ValueError, "symlink"):
                load_og_fixture(fixture_root, PurePosixPath("og-minimal"))

    def test_loader_rejects_changed_manifested_descendant(self) -> None:
        """Every manifest-bound Parser-readable file must keep its digest."""

        with self._copied_fixture_root() as fixture_root:
            changed = fixture_root / "og-minimal" / "pages" / "Changed.md"
            unchanged = b"title:: Before change\n"
            changed.write_bytes(b"title:: After change\n")
            manifest_path = fixture_root / "fixture-manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["files"]["og-minimal/pages/Changed.md"] = sha256_bytes(unchanged)
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "fixture digest mismatch"):
                load_og_fixture(fixture_root, PurePosixPath("og-minimal"))

    @contextmanager
    def _copied_fixture_root(self) -> Iterator[Path]:
        with tempfile.TemporaryDirectory() as directory:
            fixture_root = Path(directory) / "fixtures"
            shutil.copytree(FIXTURES_ROOT, fixture_root)
            yield fixture_root


if __name__ == "__main__":
    unittest.main()
