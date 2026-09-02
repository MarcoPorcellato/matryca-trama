"""Static and behavioral guards for the Python read-only contract slice."""

import ast
from pathlib import Path, PurePosixPath
import unittest

from trama_logseq_og_adapter import OgReadAdapter
from trama_parser_bridge import load_og_fixture

from trama_contracts import ReadRequest
from trama_core import canonical_json, sha256_bytes


FIXTURES_ROOT = Path(__file__).parents[1] / "fixtures"
FIXTURE_DIGEST = sha256_bytes((FIXTURES_ROOT / "fixture-manifest.json").read_bytes())
ROOT_BLOCK_ID = "44ec97ef-0b49-5361-bdfb-54b1a4197531"
CAPABILITIES = ("graph.identify", "page.read", "block.subtree.read.complete")


def request(
    operation: str,
    *,
    page_reference: str | None = None,
    block_reference: str | None = None,
) -> ReadRequest:
    return ReadRequest(
        contract_id="trama.logseq.read/v1",
        accepted_contract_major=1,
        operation=operation,
        request_id=f"request-{operation}",
        graph_selector="fixture:og-minimal",
        page_reference=page_reference,
        block_reference=block_reference,
    )


RUNTIME_ROOT = Path(__file__).parents[2] / "packages"
ALLOWED_IMPORT_ROOTS = {
    "collections", "hmac", "json", "math", "pathlib", "hashlib", "re",
    "dataclasses", "enum", "typing", "logseq_matryca_parser", "trama_core",
    "trama_contracts",
}
FORBIDDEN_CALLS = {
    "write_text",
    "write_bytes",
    "mkdir",
    "unlink",
    "rename",
    "replace",
    "rmdir",
    "copy",
    "copy2",
    "move",
    "export",
    "watch",
    "touch",
    "remove",
    "makedirs",
    "truncate",
    "chmod",
    "chown",
    "symlink",
    "link",
    "hardlink",
    "writelines",
    "dump",
    "NamedTemporaryFile",
    "TemporaryDirectory",
    "symlink_to", "hardlink_to", "link_to", "lchmod", "lchown", "__import__", "write",
    "system",
}


def violations(source: str) -> list[str]:
    """Return high-signal write/watch/export/network violations in source."""

    tree = ast.parse(source)
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.split(".", 1)[0] not in ALLOWED_IMPORT_ROOTS:
                    found.append(f"import:{alias.name}")
        elif isinstance(node, ast.ImportFrom) and node.module:
            if node.level == 0 and node.module.split(".", 1)[0] not in ALLOWED_IMPORT_ROOTS:
                found.append(f"import:{node.module}")
        elif isinstance(node, ast.Call):
            name = node.func.attr if isinstance(node.func, ast.Attribute) else (
                node.func.id if isinstance(node.func, ast.Name) else ""
            )
            if name in FORBIDDEN_CALLS:
                found.append(f"call:{name}")
            if name == "open":
                found.append("call:open")
    return found


class ReadOnlyPostureTests(unittest.TestCase):
    def test_runtime_packages_have_no_high_signal_mutation_authority(self) -> None:
        files = sorted(RUNTIME_ROOT.glob("*/src/**/*.py"))
        self.assertTrue(files)
        found = {
            f"{path.relative_to(RUNTIME_ROOT)}:{item}"
            for path in files
            for item in violations(path.read_text(encoding="utf-8"))
        }
        self.assertEqual(found, set())

    def test_scanner_rejects_synthetic_import_and_write(self) -> None:
        source = "import sqlite3\nfrom pathlib import Path\nPath('x').write_text('x')\n"
        self.assertEqual(
            violations(source),
            ["import:sqlite3", "call:write_text"],
        )

    def test_scanner_rejects_keyword_open_and_authority_primitives(self) -> None:
        source = """
import os
import io
import builtins
from pathlib import Path
Path('x').open(mode='w')
Path('x').touch()
Path('x').unlink()
Path('x').symlink_to('y')
Path('x').hardlink_to('y')
Path('x').write('x')
tempfile.NamedTemporaryFile()
archive.dump(data, 'x')
io.open('file', 'w')
builtins.open('file', 'w')
os.open('file', os.O_WRONLY)
os.system('curl https://example.invalid')
Path('x').link_to('y')
os.lchmod('x', 0o600)
os.lchown('x', 1, 1)
__import__('os')
"""
        expected = [
            "import:os", "import:io", "import:builtins", "call:open", "call:touch", "call:unlink",
            "call:symlink_to", "call:hardlink_to", "call:write", "call:NamedTemporaryFile",
            "call:dump", "call:open", "call:open", "call:open", "call:system", "call:link_to",
            "call:lchmod", "call:lchown", "call:__import__",
        ]
        self.assertEqual(violations(source), expected)

    def test_repeated_reads_have_identical_payload_and_provenance(self) -> None:
        manifest = FIXTURES_ROOT / "og-minimal"
        before = {path.relative_to(FIXTURES_ROOT): path.read_bytes() for path in FIXTURES_ROOT.rglob("*") if path.is_file()}
        observed = []
        for operation, kwargs in (
            ("graph.identify", {}),
            ("page.read", {"page_reference": "Example"}),
            ("block.subtree.read.complete", {"block_reference": ROOT_BLOCK_ID}),
        ):
            results = []
            for _ in range(2):
                graph = load_og_fixture(FIXTURES_ROOT, PurePosixPath("og-minimal"))
                adapter = OgReadAdapter(graph, FIXTURE_DIGEST)
                result = adapter.identify(request(operation)) if operation == "graph.identify" else (
                    adapter.read_page(request(operation, **kwargs)) if operation == "page.read"
                    else adapter.read_complete_subtree(request(operation, **kwargs))
                )
                results.append(result)
            def representation(result: object) -> bytes:
                provenance = result.provenance
                return canonical_json({
                    "contract_id": result.contract_id,
                    "contract_version": result.contract_version,
                    "operation": result.operation,
                    "request_id": result.request_id,
                    "payload": result.payload,
                    "outcome": result.outcome.value,
                    "graph_binding": result.graph_binding,
                    "producer": result.producer,
                    "capabilities": result.capabilities,
                    "provenance": None if provenance is None else {
                        "source_mode": provenance.source_mode,
                        "authority": provenance.authority,
                        "source_reference": provenance.source_reference,
                        "evidence_digest": provenance.evidence_digest,
                        "producer": provenance.producer,
                        "exercised_capabilities": provenance.exercised_capabilities,
                    },
                })
            self.assertEqual(representation(results[0]), representation(results[1]))
            self.assertEqual(
                results[0].provenance.evidence_digest,
                results[1].provenance.evidence_digest,
            )
            observed.append(results[0])
        self.assertEqual(before, {path.relative_to(FIXTURES_ROOT): path.read_bytes() for path in FIXTURES_ROOT.rglob("*") if path.is_file()})


if __name__ == "__main__":
    unittest.main()
