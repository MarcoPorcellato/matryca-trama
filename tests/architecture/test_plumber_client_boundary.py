"""Allowed inward client edge and forbidden cross-layer imports."""

from pathlib import Path
import tempfile
import unittest

from scripts.validate_architecture import validate_repository
if __package__:
    from .test_dependency_boundaries import write_fixture
else:
    from test_dependency_boundaries import write_fixture


class PlumberClientArchitectureTests(unittest.TestCase):
    def make_fixture(
        self, root: Path, source: str, *, declare_core: bool = True
    ) -> None:
        write_fixture(root, {})
        with (root / "architecture.toml").open("a") as stream:
            stream.write(
                '\n[packages."trama-plumber-client"]\n'
                'directory = "packages/plumber-client"\n'
                'import_root = "trama_plumber_client"\n'
                'allowed_internal = ["trama_core"]\nallowed_external = []\n'
            )
        with (root / "pyproject.toml").open("a") as stream:
            stream.write("trama-plumber-client = { workspace = true }\n")
        package = root / "packages/plumber-client"
        module = package / "src/trama_plumber_client"
        module.mkdir(parents=True)
        (module / "__init__.py").write_text(source)
        dependencies = '["trama-core"]' if declare_core else "[]"
        (package / "pyproject.toml").write_text(
            '[project]\nname = "trama-plumber-client"\nversion = "0.0.0"\n'
            f"dependencies = {dependencies}\n"
        )

    def test_client_can_import_core_and_stdlib_but_not_other_layers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_fixture(
                root, "import trama_core\nimport os, subprocess, selectors\n"
            )
            self.assertEqual(validate_repository(root), [])
        for imported in (
            "trama_contracts",
            "trama_plumber_bridge",
            "trama_parser_bridge",
            "trama_logseq_og_adapter",
            "logseq_matryca_parser",
            "matryca_plumber",
            "matryca_brain",
            "trama_pro",
        ):
            with (
                self.subTest(imported=imported),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                self.make_fixture(root, f"import {imported}\n")
                self.assertTrue(validate_repository(root))

    def test_core_cannot_import_client_and_client_must_declare_core(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_fixture(root, "import trama_core\n", declare_core=False)
            self.assertIn(
                "ARCH003", {violation.code for violation in validate_repository(root)}
            )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_fixture(root, "")
            (root / "packages/core/src/trama_core/bad.py").write_text(
                "import trama_plumber_client\n"
            )
            self.assertIn(
                "ARCH002", {violation.code for violation in validate_repository(root)}
            )


if __name__ == "__main__":
    unittest.main()
