"""Synthetic conformance tests for the read-only OG adapter."""

from pathlib import Path, PurePosixPath
import unittest

from trama_contracts import Outcome, ReadRequest
from trama_core import canonical_json, sha256_bytes
from trama_logseq_og_adapter import (
    OgReadAdapter,
    build_og_payload,
    og_provenance,
)
from trama_parser_bridge import load_og_fixture


CONTRACT_ID = "trama.logseq.read/v1"
FIXTURES_ROOT = Path(__file__).parents[1] / "fixtures"
FIXTURE_MANIFEST = FIXTURES_ROOT / "fixture-manifest.json"
FIXTURE_DIGEST = sha256_bytes(FIXTURE_MANIFEST.read_bytes())
ROOT_BLOCK_ID = "44ec97ef-0b49-5361-bdfb-54b1a4197531"
CHILD_BLOCK_ID = "c86abb84-fa33-5fec-bf6d-1b5c637ade7f"
CAPABILITIES = (
    "graph.identify",
    "page.read",
    "block.subtree.read.complete",
)


def request(
    operation: str,
    *,
    page_reference: str | None = None,
    block_reference: str | None = None,
    contract_id: str = CONTRACT_ID,
    accepted_contract_major: int = 1,
) -> ReadRequest:
    """Create one consumer request for the selected synthetic graph."""

    return ReadRequest(
        contract_id=contract_id,
        accepted_contract_major=accepted_contract_major,
        operation=operation,
        request_id=f"request-{operation}",
        graph_selector="fixture:og-minimal",
        page_reference=page_reference,
        block_reference=block_reference,
    )


def expected_root_block() -> dict[str, object]:
    """Return hand-checked nested source order from the owned fixture."""

    return {
        "uuid": ROOT_BLOCK_ID,
        "content": "Root block",
        "properties": {},
        "children": [
            {
                "uuid": CHILD_BLOCK_ID,
                "content": "Child block",
                "properties": {},
                "children": [],
            },
        ],
    }


class OgReadContractTests(unittest.TestCase):
    """Only verified synthetic OG content may produce successful reads."""

    def setUp(self) -> None:
        graph = load_og_fixture(FIXTURES_ROOT, PurePosixPath("og-minimal"))
        self.adapter = OgReadAdapter(graph, FIXTURE_DIGEST)

    def test_identify_returns_exact_selected_graph_identity(self) -> None:
        """A changed graph binding would misidentify the selected graph."""

        result = self.adapter.identify(request("graph.identify"))

        self.assertIs(result.outcome, Outcome.SUCCESS)
        self.assertEqual(result.graph_binding, FIXTURE_DIGEST)
        self.assertEqual(
            result.payload,
            {
                "graph_binding": FIXTURE_DIGEST,
                "source_mode": "og_markdown",
                "authority": "logseq_og_markdown",
                "capabilities": CAPABILITIES,
            },
        )
        self.assertEqual(result.provenance.source_reference, "fixture:og-minimal")
        self.assertEqual(result.provenance.exercised_capabilities, ("graph.identify",))

    def test_identify_reports_distribution_version_as_producer(self) -> None:
        """Producer identity must be exact package distribution name and version."""

        result = self.adapter.identify(request("graph.identify"))

        self.assertEqual(result.producer, "trama-logseq-og-adapter 0.0.0")
        self.assertEqual(
            result.provenance.producer,
            "trama-logseq-og-adapter 0.0.0",
        )

    def test_page_read_preserves_page_content_and_native_og_provenance(self) -> None:
        """Dropping page structure or authority would corrupt a successful read."""

        result = self.adapter.read_page(request("page.read", page_reference="Example"))

        self.assertIs(result.outcome, Outcome.SUCCESS)
        self.assertEqual(result.graph_binding, FIXTURE_DIGEST)
        self.assertEqual(
            result.payload,
            {
                "graph_binding": FIXTURE_DIGEST,
                "page": {
                    "title": "Example",
                    "properties": {"title": "Example"},
                    "root_blocks": [expected_root_block()],
                },
            },
        )
        self.assertEqual(result.provenance.source_mode, "og_markdown")
        self.assertEqual(result.provenance.authority, "logseq_og_markdown")
        self.assertEqual(result.provenance.source_reference, "fixture:og-minimal")
        self.assertEqual(result.provenance.exercised_capabilities, ("page.read",))

    def test_complete_subtree_keeps_nested_child_source_order(self) -> None:
        """Flattened or reordered descendants would violate complete subtree reads."""

        result = self.adapter.read_complete_subtree(
            request("block.subtree.read.complete", block_reference=ROOT_BLOCK_ID),
        )

        self.assertIs(result.outcome, Outcome.SUCCESS)
        self.assertEqual(
            result.payload,
            {
                "graph_binding": FIXTURE_DIGEST,
                "root_block": expected_root_block(),
            },
        )
        self.assertEqual(
            result.provenance.exercised_capabilities,
            ("block.subtree.read.complete",),
        )

    def test_unknown_page_is_not_found(self) -> None:
        """Returning a nearby or cached page for an absent reference is a bug."""

        result = self.adapter.read_page(request("page.read", page_reference="Missing"))

        self.assertIs(result.outcome, Outcome.NOT_FOUND)
        self.assertEqual(result.payload, {"reason": "not_found"})
        self.assertIsNone(result.provenance)

    def test_unknown_block_is_not_found(self) -> None:
        """Returning a partial subtree for an absent root is a bug."""

        result = self.adapter.read_complete_subtree(
            request("block.subtree.read.complete", block_reference="missing-block"),
        )

        self.assertIs(result.outcome, Outcome.NOT_FOUND)
        self.assertEqual(result.payload, {"reason": "not_found"})
        self.assertIsNone(result.provenance)

    def test_wrong_contract_major_is_incompatible(self) -> None:
        """Accepting a different contract major would break negotiation."""

        result = self.adapter.read_page(
            request(
                "page.read",
                page_reference="Example",
                contract_id="trama.logseq.read/v2",
                accepted_contract_major=2,
            ),
        )

        self.assertIs(result.outcome, Outcome.INCOMPATIBLE)
        self.assertEqual(result.payload, {"reason": "incompatible"})
        self.assertIsNone(result.provenance)

    def test_payload_helper_uses_only_supported_public_operations(self) -> None:
        """Unsupported operation payloads would manufacture contract content."""

        graph = load_og_fixture(FIXTURES_ROOT, PurePosixPath("og-minimal"))

        self.assertIsNone(build_og_payload(graph, "page.write", "Example"))
        self.assertEqual(
            build_og_payload(graph, "block.subtree.read.complete", ROOT_BLOCK_ID),
            {"root_block": expected_root_block()},
        )

    def test_missing_manifest_digest_is_a_provenance_failure(self) -> None:
        """A successful read without selected-fixture identity is a bug."""

        graph = load_og_fixture(FIXTURES_ROOT, PurePosixPath("og-minimal"))
        result = OgReadAdapter(graph, "").identify(request("graph.identify"))

        self.assertIs(result.outcome, Outcome.PROVENANCE_FAILURE)
        self.assertEqual(result.payload, {"reason": "provenance_failure"})
        self.assertIsNone(result.provenance)

    def test_provenance_helper_binds_canonical_payload_digest(self) -> None:
        """A changed payload digest would detach provenance from returned content."""

        payload = {
            "graph_binding": FIXTURE_DIGEST,
            "root_block": expected_root_block(),
        }

        provenance = og_provenance(
            FIXTURE_DIGEST,
            payload,
            producer="trama-logseq-og-adapter 1.0.0",
            exercised_capabilities=("block.subtree.read.complete",),
        )

        self.assertEqual(provenance.source_mode, "og_markdown")
        self.assertEqual(provenance.authority, "logseq_og_markdown")
        self.assertEqual(provenance.source_reference, "fixture:og-minimal")
        self.assertEqual(provenance.evidence_digest, sha256_bytes(canonical_json(payload)))


if __name__ == "__main__":
    unittest.main()
