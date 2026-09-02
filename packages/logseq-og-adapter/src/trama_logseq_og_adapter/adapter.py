"""Read-only mapping from a verified synthetic OG graph to public DTOs."""

from collections.abc import Mapping

from logseq_matryca_parser import LogseqGraph, LogseqNode, LogseqPage
from trama_contracts import (
    Outcome,
    Provenance,
    ReadRequest,
    ReadResult,
    validate_request,
)
from trama_core import canonical_json, sha256_bytes


_CONTRACT_VERSION = "1.0.0"
_PRODUCER = "trama-logseq-og-adapter 1.0.0"
_CAPABILITIES = (
    "graph.identify",
    "page.read",
    "block.subtree.read.complete",
)
_SOURCE_REFERENCE = "fixture:og-minimal"


class OgReadAdapter:
    """Serve only content already parsed from one verified synthetic OG fixture."""

    def __init__(self, graph: LogseqGraph, fixture_manifest_digest: str) -> None:
        self._graph = graph
        self._fixture_manifest_digest = fixture_manifest_digest

    def identify(self, request: ReadRequest) -> ReadResult:
        """Identify the one selected synthetic OG graph."""

        return self._read(request, reference=None)

    def read_page(self, request: ReadRequest) -> ReadResult:
        """Read one page from the already loaded synthetic OG graph."""

        return self._read(request, reference=request.page_reference)

    def read_complete_subtree(self, request: ReadRequest) -> ReadResult:
        """Read one complete nested block subtree from the loaded graph."""

        return self._read(request, reference=request.block_reference)

    def _read(self, request: ReadRequest, reference: str | None) -> ReadResult:
        validation = validate_request(request)
        if validation is not None:
            return self._failure(validation, request)
        if not _is_sha256_digest(self._fixture_manifest_digest):
            return self._failure(Outcome.PROVENANCE_FAILURE, request)

        payload = build_og_payload(self._graph, request.operation, reference)
        if payload is None:
            return self._failure(Outcome.NOT_FOUND, request)

        bound_payload = {
            "graph_binding": self._fixture_manifest_digest,
            **payload,
        }
        return ReadResult.success(
            request=request,
            contract_version=_CONTRACT_VERSION,
            graph_binding=self._fixture_manifest_digest,
            producer=_PRODUCER,
            capabilities=_CAPABILITIES,
            payload=bound_payload,
            provenance=og_provenance(
                self._fixture_manifest_digest,
                bound_payload,
                producer=_PRODUCER,
                exercised_capabilities=(request.operation,),
            ),
        )

    def _failure(self, outcome: Outcome, request: ReadRequest) -> ReadResult:
        graph_binding = (
            self._fixture_manifest_digest
            if _is_sha256_digest(self._fixture_manifest_digest)
            else None
        )
        return ReadResult.failure(
            outcome,
            request=request,
            contract_version=_CONTRACT_VERSION,
            graph_binding=graph_binding,
            producer=_PRODUCER,
            capabilities=_CAPABILITIES,
            payload={"reason": outcome.value},
        )


def build_og_payload(
    graph: LogseqGraph,
    operation: str,
    reference: str | None,
) -> dict[str, object] | None:
    """Map only contract-supported public Parser values into nested data."""

    if operation == "graph.identify":
        return {
            "source_mode": "og_markdown",
            "authority": "logseq_og_markdown",
            "capabilities": _CAPABILITIES,
        }
    if operation == "page.read" and reference is not None:
        page = graph.get_page(reference)
        if page is None:
            return None
        return {"page": _page_payload(page)}
    if operation == "block.subtree.read.complete" and reference is not None:
        root_block = graph.get_node_by_uuid(reference)
        if root_block is None:
            return None
        return {"root_block": _node_payload(root_block)}
    return None


def og_provenance(
    fixture_manifest_digest: str,
    payload: Mapping[str, object],
    *,
    producer: str,
    exercised_capabilities: tuple[str, ...],
) -> Provenance:
    """Bind one synthetic read result to its canonical returned representation."""

    if not _is_sha256_digest(fixture_manifest_digest):
        raise ValueError("fixture manifest digest is invalid")
    return Provenance(
        source_mode="og_markdown",
        authority="logseq_og_markdown",
        source_reference=_SOURCE_REFERENCE,
        evidence_digest=sha256_bytes(canonical_json(payload)),
        producer=producer,
        exercised_capabilities=exercised_capabilities,
    )


def _page_payload(page: LogseqPage) -> dict[str, object]:
    return {
        "title": page.title,
        "properties": dict(page.properties),
        "root_blocks": [_node_payload(node) for node in page.root_nodes],
    }


def _node_payload(node: LogseqNode) -> dict[str, object]:
    return {
        "uuid": node.uuid,
        "content": node.content,
        "properties": dict(node.properties),
        "children": [_node_payload(child) for child in node.children],
    }


def _is_sha256_digest(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )
