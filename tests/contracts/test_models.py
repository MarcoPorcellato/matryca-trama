"""Public contract tests for versioned Logseq read DTOs."""

from dataclasses import FrozenInstanceError
import unittest
from typing import Mapping

from trama_contracts import (
    Outcome,
    Provenance,
    ReadRequest,
    ReadResult,
    validate_request,
)


CONTRACT_ID = "trama.logseq.read/v1"
CONTRACT_VERSION = "1.2.3"
PRODUCER = "trama-logseq-og-adapter 1.2.3"
CAPABILITIES = ("graph.identify", "page.read")
GRAPH_BINDING = "fixture-digest:og-minimal"


def graph_identify_request() -> ReadRequest:
    return ReadRequest(
        contract_id=CONTRACT_ID,
        accepted_contract_major=1,
        operation="graph.identify",
        request_id="request-1",
        graph_selector="fixture:og-minimal",
    )


def complete_provenance(
    *,
    producer: str = PRODUCER,
    exercised_capabilities: tuple[str, ...] = ("graph.identify",),
) -> Provenance:
    return Provenance(
        source_mode="og_markdown",
        authority="logseq_og_markdown",
        source_reference="fixture:og-minimal",
        evidence_digest="a" * 64,
        producer=producer,
        exercised_capabilities=exercised_capabilities,
    )


class ReadContractTests(unittest.TestCase):
    def test_valid_request_is_accepted(self) -> None:
        request = ReadRequest(
            contract_id=CONTRACT_ID,
            accepted_contract_major=1,
            operation="page.read",
            request_id="request-1",
            graph_selector="fixture:og-minimal",
            page_reference="Example",
        )

        self.assertIsNone(validate_request(request))

    def test_unknown_major_is_incompatible(self) -> None:
        request = ReadRequest(
            contract_id="trama.logseq.read/v2",
            accepted_contract_major=2,
            operation="graph.identify",
            request_id="request-1",
            graph_selector="fixture:og-minimal",
        )

        self.assertIs(validate_request(request), Outcome.INCOMPATIBLE)

    def test_whitespace_request_fields_are_invalid(self) -> None:
        request = ReadRequest(
            contract_id=CONTRACT_ID,
            accepted_contract_major=1,
            operation="page.read",
            request_id=" \t",
            graph_selector="\n",
            page_reference=" ",
        )

        self.assertIs(validate_request(request), Outcome.INVALID_REQUEST)

    def test_required_operation_reference_is_invalid_when_missing(self) -> None:
        request = ReadRequest(
            contract_id=CONTRACT_ID,
            accepted_contract_major=1,
            operation="block.subtree.read.complete",
            request_id="request-1",
            graph_selector="fixture:og-minimal",
            block_reference=None,
        )

        self.assertIs(validate_request(request), Outcome.INVALID_REQUEST)

    def test_identify_request_has_no_graph_binding_field(self) -> None:
        with self.assertRaises(TypeError):
            ReadRequest(
                contract_id=CONTRACT_ID,
                accepted_contract_major=1,
                operation="graph.identify",
                request_id="request-1",
                graph_selector="fixture:og-minimal",
                graph_binding=GRAPH_BINDING,
            )

    def test_success_preserves_complete_envelope_and_provenance(self) -> None:
        request = graph_identify_request()
        payload: Mapping[str, object] = {"graph": "og-minimal"}
        provenance = complete_provenance()

        result = ReadResult.success(
            request=request,
            contract_version=CONTRACT_VERSION,
            graph_binding=GRAPH_BINDING,
            producer=PRODUCER,
            capabilities=CAPABILITIES,
            payload=payload,
            provenance=provenance,
        )

        self.assertEqual(result.contract_id, request.contract_id)
        self.assertEqual(result.contract_version, CONTRACT_VERSION)
        self.assertEqual(result.operation, request.operation)
        self.assertEqual(result.request_id, request.request_id)
        self.assertEqual(result.payload, payload)
        self.assertIs(result.outcome, Outcome.SUCCESS)
        self.assertEqual(result.graph_binding, GRAPH_BINDING)
        self.assertEqual(result.producer, PRODUCER)
        self.assertEqual(result.capabilities, CAPABILITIES)
        self.assertIs(result.provenance, provenance)
        self.assertEqual(result.provenance.source_mode, "og_markdown")
        self.assertEqual(result.provenance.authority, "logseq_og_markdown")
        self.assertEqual(result.provenance.source_reference, "fixture:og-minimal")
        self.assertEqual(result.provenance.evidence_digest, "a" * 64)
        self.assertEqual(result.provenance.producer, PRODUCER)
        self.assertEqual(
            result.provenance.exercised_capabilities,
            ("graph.identify",),
        )

        with self.assertRaises(FrozenInstanceError):
            result.producer = "different producer"  # type: ignore[misc]

    def test_success_requires_explicit_profile_metadata(self) -> None:
        with self.assertRaises(TypeError):
            ReadResult.success(
                request=graph_identify_request(),
                payload={},
            )

    def test_success_downgrades_invalid_request_to_provenance_failure(self) -> None:
        request = ReadRequest(
            contract_id=CONTRACT_ID,
            accepted_contract_major=1,
            operation="page.read",
            request_id="request-1",
            graph_selector="fixture:og-minimal",
            page_reference=" ",
        )

        result = ReadResult.success(
            request=request,
            contract_version=CONTRACT_VERSION,
            graph_binding=None,
            producer=PRODUCER,
            capabilities=CAPABILITIES,
            payload={},
            provenance=complete_provenance(),
        )

        self.assertIs(result.outcome, Outcome.PROVENANCE_FAILURE)

    def test_success_downgrades_invalid_version_to_provenance_failure(self) -> None:
        result = ReadResult.success(
            request=graph_identify_request(),
            contract_version="release-1",
            graph_binding=None,
            producer=PRODUCER,
            capabilities=CAPABILITIES,
            payload={},
            provenance=complete_provenance(),
        )

        self.assertIs(result.outcome, Outcome.PROVENANCE_FAILURE)

    def test_success_downgrades_missing_provenance_to_provenance_failure(self) -> None:
        result = ReadResult.success(
            request=graph_identify_request(),
            contract_version=CONTRACT_VERSION,
            graph_binding=None,
            producer=PRODUCER,
            capabilities=CAPABILITIES,
            payload={},
            provenance=None,
        )

        self.assertIs(result.outcome, Outcome.PROVENANCE_FAILURE)

    def test_success_downgrades_authority_mismatch_to_provenance_failure(self) -> None:
        provenance = Provenance(
            source_mode="og_markdown",
            authority="logseq_db_native",
            source_reference="fixture:og-minimal",
            evidence_digest="a" * 64,
            producer=PRODUCER,
            exercised_capabilities=("graph.identify",),
        )

        result = ReadResult.success(
            request=graph_identify_request(),
            contract_version=CONTRACT_VERSION,
            graph_binding=None,
            producer=PRODUCER,
            capabilities=CAPABILITIES,
            payload={},
            provenance=provenance,
        )

        self.assertIs(result.outcome, Outcome.PROVENANCE_FAILURE)

    def test_success_downgrades_producer_or_capability_inconsistency(self) -> None:
        cases = (
            (complete_provenance(producer="other producer"), CAPABILITIES),
            (complete_provenance(exercised_capabilities=("page.write",)), CAPABILITIES),
            (complete_provenance(exercised_capabilities=()), CAPABILITIES),
            (complete_provenance(), ("page.read",)),
        )

        for provenance, capabilities in cases:
            with self.subTest(provenance=provenance, capabilities=capabilities):
                result = ReadResult.success(
                    request=graph_identify_request(),
                    contract_version=CONTRACT_VERSION,
                    graph_binding=None,
                    producer=PRODUCER,
                    capabilities=capabilities,
                    payload={},
                    provenance=provenance,
                )

                self.assertIs(result.outcome, Outcome.PROVENANCE_FAILURE)

    def test_failure_preserves_request_envelope_without_provenance(self) -> None:
        request = ReadRequest(
            contract_id="trama.logseq.read/v2",
            accepted_contract_major=2,
            operation="page.read",
            request_id="request-2",
            graph_selector="fixture:og-minimal",
            page_reference="Missing",
        )
        payload: Mapping[str, object] = {"reason": "unsupported contract"}

        result = ReadResult.failure(
            Outcome.INCOMPATIBLE,
            request=request,
            contract_version=CONTRACT_VERSION,
            graph_binding=None,
            producer=PRODUCER,
            capabilities=CAPABILITIES,
            payload=payload,
        )

        self.assertEqual(result.contract_id, request.contract_id)
        self.assertEqual(result.operation, request.operation)
        self.assertEqual(result.request_id, request.request_id)
        self.assertEqual(result.contract_version, CONTRACT_VERSION)
        self.assertEqual(result.producer, PRODUCER)
        self.assertEqual(result.capabilities, CAPABILITIES)
        self.assertEqual(result.payload, payload)
        self.assertIs(result.outcome, Outcome.INCOMPATIBLE)
        self.assertIsNone(result.provenance)

    def test_failure_rejects_success_outcome_and_empty_producer(self) -> None:
        request = graph_identify_request()

        with self.assertRaises(ValueError):
            ReadResult.failure(
                Outcome.SUCCESS,
                request=request,
                contract_version=CONTRACT_VERSION,
                graph_binding=None,
                producer=PRODUCER,
                capabilities=CAPABILITIES,
                payload={},
            )

        with self.assertRaises(ValueError):
            ReadResult.failure(
                Outcome.NOT_FOUND,
                request=request,
                contract_version=CONTRACT_VERSION,
                graph_binding=None,
                producer=" ",
                capabilities=CAPABILITIES,
                payload={},
            )


if __name__ == "__main__":
    unittest.main()
