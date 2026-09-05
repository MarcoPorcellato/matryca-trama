from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.validate_architecture import validate_repository


REPOSITORY = Path(__file__).resolve().parents[2]
VALIDATOR = REPOSITORY / "scripts" / "validate_architecture.py"

ARCHITECTURE = """\
exceptions = []

[external]
logseq_matryca_parser = "logseq-matryca-parser"

[forbidden]
roots = ["matryca_brain", "trama_brain", "trama_pro"]

[packages."trama-contracts"]
directory = "packages/contracts"
import_root = "trama_contracts"
allowed_internal = []
allowed_external = []

[packages."trama-core"]
directory = "packages/core"
import_root = "trama_core"
allowed_internal = ["trama_contracts"]
allowed_external = []

[packages."trama-parser-bridge"]
directory = "packages/parser-bridge"
import_root = "trama_parser_bridge"
allowed_internal = ["trama_contracts", "trama_core"]
allowed_external = ["logseq_matryca_parser"]

[packages."trama-logseq-og-adapter"]
directory = "packages/logseq-og-adapter"
import_root = "trama_logseq_og_adapter"
allowed_internal = ["trama_contracts", "trama_core", "trama_parser_bridge"]
allowed_external = []

[packages."trama-plumber-bridge"]
directory = "packages/plumber-bridge"
import_root = "trama_plumber_bridge"
allowed_internal = ["trama_contracts", "trama_core"]
allowed_external = []
"""

PACKAGES = {
    "trama-contracts": ("contracts", "trama_contracts", []),
    "trama-core": ("core", "trama_core", ["trama-contracts"]),
    "trama-parser-bridge": (
        "parser-bridge",
        "trama_parser_bridge",
        ["trama-contracts", "trama-core", "logseq-matryca-parser"],
    ),
    "trama-logseq-og-adapter": (
        "logseq-og-adapter",
        "trama_logseq_og_adapter",
        ["trama-contracts", "trama-core", "trama-parser-bridge"],
    ),
    "trama-plumber-bridge": (
        "plumber-bridge",
        "trama_plumber_bridge",
        ["trama-contracts", "trama-core"],
    ),
}

EXPIRED_EXCEPTION = (
    "[[exceptions]]\n"
    'id = "old"\n'
    'package = "trama-contracts"\n'
    'import_root = "trama_core"\n'
    'path_glob = "packages/contracts/src/trama_contracts/bad.py"\n'
    'issue = "https://github.com/MarcoPorcellato/matryca-trama/issues/1"\n'
    'owner = "maintainer"\n'
    'reason = "temporary"\n'
    'created = "2000-01-01"\n'
    'expires = "2000-01-02"\n'
    'removal_condition = "remove import"\n'
)
UNUSED_EXCEPTION = EXPIRED_EXCEPTION.replace('id = "old"', 'id = "unused"').replace(
    'created = "2000-01-01"\nexpires = "2000-01-02"',
    'created = "2026-01-01"\nexpires = "2999-01-01"',
)


def write_fixture(root: Path, sources: dict[str, str] | None = None) -> None:
    (root / "architecture.toml").write_text(ARCHITECTURE, encoding="utf-8")
    for distribution, (directory, import_root, dependencies) in PACKAGES.items():
        package = root / "packages" / directory
        package.mkdir(parents=True)
        dependencies_text = ", ".join(f'"{dependency}"' for dependency in dependencies)
        (package / "pyproject.toml").write_text(
            "[project]\n"
            f'name = "{distribution}"\n'
            f"dependencies = [{dependencies_text}]\n",
            encoding="utf-8",
        )
        source = package / "src" / import_root
        source.mkdir(parents=True)
        (source / "__init__.py").write_text("", encoding="utf-8")
    for relative, content in (sources or {}).items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def codes(root: Path) -> list[str]:
    return [violation.code for violation in validate_repository(root)]


class DependencyBoundaryTests(unittest.TestCase):
    def test_unregistered_package_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root)
            package = root / "packages" / "unregistered"
            (package / "src" / "unregistered").mkdir(parents=True)
            (package / "pyproject.toml").write_text(
                '[project]\nname = "unregistered"\ndependencies = []\n',
                encoding="utf-8",
            )
            self.assertIn("ARCH001", codes(root))

    def test_contracts_cannot_import_core(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {
                "packages/contracts/src/trama_contracts/bad.py": "import trama_core\n",
                "packages/contracts/src/trama_contracts/other.py": "import trama_core\n",
            })
            self.assertIn(
                (
                    Path("packages/contracts/src/trama_contracts/bad.py"),
                    1,
                    "ARCH002",
                    "forbidden internal import: trama_core",
                ),
                [
                    (violation.path, violation.line, violation.code, violation.message)
                    for violation in validate_repository(root)
                ],
            )

    def test_core_cannot_import_adapter(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {"packages/core/src/trama_core/bad.py": "import trama_logseq_og_adapter\n"})
            self.assertIn("ARCH002", codes(root))

    def test_og_adapter_cannot_import_parser_directly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {"packages/logseq-og-adapter/src/trama_logseq_og_adapter/bad.py": "from logseq_matryca_parser import LogseqGraph\n"})
            self.assertIn("ARCH004", codes(root))

    def test_allowed_internal_import_requires_manifest_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {"packages/core/src/trama_core/uses_contracts.py": "import trama_contracts\n"})
            (root / "packages/core/pyproject.toml").write_text(
                '[project]\nname = "trama-core"\ndependencies = []\n', encoding="utf-8"
            )
            self.assertIn("ARCH003", codes(root))

    def test_manifest_only_forbidden_local_dependency_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root)
            (root / "packages/core/pyproject.toml").write_text(
                '[project]\nname = "trama-core"\n'
                'dependencies = ["trama-contracts", "trama-logseq-og-adapter"]\n',
                encoding="utf-8",
            )
            self.assertIn("ARCH002", codes(root))

    def test_manifest_only_forbidden_external_dependency_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root)
            (root / "packages/core/pyproject.toml").write_text(
                '[project]\nname = "trama-core"\n'
                'dependencies = ["trama-contracts", "logseq-matryca-parser"]\n',
                encoding="utf-8",
            )
            self.assertIn("ARCH004", codes(root))

    def test_manifestless_package_source_tree_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root)
            source = root / "packages/manifestless/src/manifestless"
            source.mkdir(parents=True)
            (source / "__init__.py").write_text("", encoding="utf-8")
            self.assertIn("ARCH001", codes(root))

    def test_parser_bridge_cannot_import_parser_internal_module(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {"packages/parser-bridge/src/trama_parser_bridge/bad.py": "from logseq_matryca_parser.internal import Parser\n"})
            self.assertIn("ARCH004", codes(root))

    def test_brain_and_pro_imports_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {"packages/contracts/src/trama_contracts/bad.py": "import matryca_brain.private\nimport trama_pro.private\n"})
            self.assertEqual(codes(root).count("ARCH004"), 2)

    def test_dynamic_import_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {"packages/contracts/src/trama_contracts/bad.py": "import importlib\nimportlib.import_module('trama_core')\n"})
            self.assertIn("ARCH005", codes(root))

    def test_builtins_import_alias_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {"packages/contracts/src/trama_contracts/bad.py": "from builtins import __import__ as load\nload('trama_core')\n"})
            self.assertIn("ARCH005", codes(root))

    def test_direct_builtins_import_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {
                "packages/contracts/src/trama_contracts/bad.py": "import builtins\nbuiltins.__import__('trama_core')\n"
            })
            self.assertIn("ARCH005", codes(root))

    def test_late_importlib_alias_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {
                "packages/contracts/src/trama_contracts/bad.py": "def load():\n    loader.import_module('trama_core')\n\nimport importlib as loader\n"
            })
            self.assertIn("ARCH005", codes(root))

    def test_sys_path_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {"packages/contracts/src/trama_contracts/bad.py": "import sys\nsys.path.append('../sibling')\n"})
            self.assertIn("ARCH005", codes(root))

    def test_sys_path_import_alias_mutation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {"packages/contracts/src/trama_contracts/bad.py": "from sys import path as sibling_path\nsibling_path.insert(0, '../sibling')\n"})
            self.assertIn("ARCH005", codes(root))

    def test_delete_sys_path_entry_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {
                "packages/contracts/src/trama_contracts/bad.py": "import sys\ndel sys.path[0]\n"
            })
            self.assertIn("ARCH005", codes(root))

    def test_allowed_same_package_stdlib_inward_and_parser_root_imports_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {
                "packages/core/src/trama_core/allowed.py": "from pathlib import Path\nfrom . import local\nfrom trama_contracts import Outcome\n",
                "packages/parser-bridge/src/trama_parser_bridge/allowed.py": "from logseq_matryca_parser import LogseqGraph\n",
            })
            self.assertEqual(codes(root), [])

    def test_malformed_expired_and_unused_exceptions_are_rejected(self) -> None:
        for exceptions in ("exceptions = [{}]", EXPIRED_EXCEPTION, UNUSED_EXCEPTION):
            with self.subTest(exceptions=exceptions), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_fixture(root)
                config = (root / "architecture.toml").read_text(encoding="utf-8")
                (root / "architecture.toml").write_text(
                    config.replace("exceptions = []", exceptions), encoding="utf-8"
                )
                self.assertIn("ARCH006", codes(root))

    def test_exception_requires_public_repository_issue_url(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {
                "packages/contracts/src/trama_contracts/bad.py": "import trama_core\n"
            })
            config = (root / "architecture.toml").read_text(encoding="utf-8")
            exception = UNUSED_EXCEPTION.replace(
                'issue = "https://github.com/MarcoPorcellato/matryca-trama/issues/1"',
                'issue = "https://example.test/issues/1"',
            )
            (root / "architecture.toml").write_text(
                config.replace("exceptions = []", exception), encoding="utf-8"
            )
            self.assertIn("ARCH006", codes(root))

    def test_scoped_exception_suppresses_only_matching_source(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root, {
                "packages/contracts/src/trama_contracts/bad.py": "import trama_core\n",
                "packages/contracts/src/trama_contracts/other.py": "import trama_core\n",
            })
            config = (root / "architecture.toml").read_text(encoding="utf-8")
            exception = EXPIRED_EXCEPTION.replace('id = "old"', 'id = "scoped"').replace(
                'created = "2000-01-01"\nexpires = "2000-01-02"',
                'created = "2026-01-01"\nexpires = "2999-01-01"',
            )
            (root / "architecture.toml").write_text(
                config.replace("exceptions = []", exception), encoding="utf-8"
            )
            self.assertEqual(codes(root), ["ARCH002"])

    def test_over_broad_exception_path_glob_is_rejected(self) -> None:
        cases = (
            ("*", "bad.py"),
            ("**", "bad.py"),
            ("**/*", "bad.py"),
            ("packages/contracts/**", "bad.py"),
            ("packages/contracts/**/*.py", "bad.py"),
            ("packages/contracts/*/*.py", "bad.py"),
            ("packages/contracts/src/trama_contracts/bad?.py", "bad1.py"),
            ("packages/contracts/src/trama_contracts/[bad].py", "b.py"),
            ("packages/contracts/src/trama_contracts/bad].py", "bad].py"),
            ("/packages/contracts/src/trama_contracts/bad.py", "bad.py"),
            ("../packages/contracts/src/trama_contracts/bad.py", "bad.py"),
        )
        for path_glob, filename in cases:
            with self.subTest(path_glob=path_glob), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                write_fixture(root, {
                    f"packages/contracts/src/trama_contracts/{filename}": "import trama_core\n"
                })
                config = (root / "architecture.toml").read_text(encoding="utf-8")
                exception = EXPIRED_EXCEPTION.replace('id = "old"', 'id = "wide"').replace(
                    'created = "2000-01-01"\nexpires = "2000-01-02"',
                    'created = "2026-01-01"\nexpires = "2999-01-01"',
                ).replace(
                    'path_glob = "packages/contracts/src/trama_contracts/bad.py"',
                    f'path_glob = "{path_glob}"',
                )
                (root / "architecture.toml").write_text(
                    config.replace("exceptions = []", exception), encoding="utf-8"
                )
                self.assertIn("ARCH006", codes(root))

    def test_cli_exits_zero_only_for_clean_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_fixture(root)
            clean = subprocess.run(
                [sys.executable, str(VALIDATOR), "--root", str(root)],
                capture_output=True, check=False, text=True,
            )
            self.assertEqual(clean.returncode, 0, clean.stderr)
            (root / "packages/contracts/src/trama_contracts/bad.py").write_text(
                "import trama_core\n", encoding="utf-8"
            )
            invalid = subprocess.run(
                [sys.executable, str(VALIDATOR), "--root", str(root)],
                capture_output=True, check=False, text=True,
            )
            self.assertNotEqual(invalid.returncode, 0)
            self.assertIn("ARCH002", invalid.stderr)


if __name__ == "__main__":
    unittest.main()
