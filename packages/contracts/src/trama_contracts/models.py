"""Immutable DTOs for the versioned Logseq read contract."""

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum
import re
from typing import Literal


CONTRACT_ID = "trama.logseq.read/v1"
_SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


class Outcome(StrEnum):
    """Stable outcomes for the public read contract."""

    SUCCESS = "success"
    UNSUPPORTED = "unsupported"
    INCOMPATIBLE = "incompatible"
    INVALID_REQUEST = "invalid_request"
    NOT_FOUND = "not_found"
    AUTHORITY_FAILURE = "authority_failure"
    PROVENANCE_FAILURE = "provenance_failure"


@dataclass(frozen=True)
class Provenance:
    """Authority and evidence facts for a successful read result."""

    source_mode: Literal["og_markdown", "db_native"]
    authority: Literal["logseq_og_markdown", "logseq_db_native"]
    source_reference: str
    evidence_digest: str
    producer: str
    exercised_capabilities: tuple[str, ...]


@dataclass(frozen=True)
class ReadRequest:
    """Consumer request for one operation on a selected graph."""

    contract_id: str
    accepted_contract_major: int
    operation: str
    request_id: str
    graph_selector: str
    page_reference: str | None = None
    block_reference: str | None = None


@dataclass(frozen=True)
class ReadResult:
    """Producer result envelope corresponding to one read request."""

    contract_id: str
    contract_version: str
    operation: str
    request_id: str
    payload: Mapping[str, object]
    outcome: Outcome
    graph_binding: str | None
    producer: str
    capabilities: tuple[str, ...]
    provenance: Provenance | None

    @classmethod
    def success(
        cls,
        *,
        request: ReadRequest,
        contract_version: str,
        graph_binding: str | None,
        producer: str,
        capabilities: tuple[str, ...],
        payload: Mapping[str, object],
        provenance: Provenance | None,
    ) -> "ReadResult":
        """Build a success result or downgrade incomplete facts to failure."""

        result = cls._from_request(
            request=request,
            contract_version=contract_version,
            graph_binding=graph_binding,
            producer=producer,
            capabilities=capabilities,
            payload=payload,
            outcome=Outcome.SUCCESS,
            provenance=provenance,
        )
        if _has_complete_success_facts(request, result):
            return result

        return cls(
            contract_id=result.contract_id,
            contract_version=result.contract_version,
            operation=result.operation,
            request_id=result.request_id,
            payload=result.payload,
            outcome=Outcome.PROVENANCE_FAILURE,
            graph_binding=result.graph_binding,
            producer=result.producer,
            capabilities=result.capabilities,
            provenance=result.provenance,
        )

    @classmethod
    def failure(
        cls,
        outcome: Outcome,
        *,
        request: ReadRequest,
        contract_version: str,
        graph_binding: str | None,
        producer: str,
        capabilities: tuple[str, ...],
        payload: Mapping[str, object],
    ) -> "ReadResult":
        """Build an explicit non-success result for its original request."""

        if not isinstance(outcome, Outcome) or outcome is Outcome.SUCCESS:
            raise ValueError("failure outcome must be a non-success Outcome")

        return cls._from_request(
            request=request,
            contract_version=contract_version,
            graph_binding=graph_binding,
            producer=producer,
            capabilities=capabilities,
            payload=payload,
            outcome=outcome,
            provenance=None,
        )

    @classmethod
    def _from_request(
        cls,
        *,
        request: ReadRequest,
        contract_version: str,
        graph_binding: str | None,
        producer: str,
        capabilities: tuple[str, ...],
        payload: Mapping[str, object],
        outcome: Outcome,
        provenance: Provenance | None,
    ) -> "ReadResult":
        if not isinstance(request, ReadRequest):
            raise TypeError("request must be a ReadRequest")
        if not isinstance(contract_version, str):
            raise TypeError("contract_version must be a string")
        if graph_binding is not None and not _is_nonempty_text(graph_binding):
            raise ValueError("graph_binding must be non-empty when supplied")
        if not _is_nonempty_text(producer):
            raise ValueError("producer must be non-empty")
        if not _is_nonempty_text_tuple(capabilities):
            raise ValueError("capabilities must be a tuple of non-empty strings")
        if not isinstance(payload, Mapping):
            raise TypeError("payload must be a mapping")

        return cls(
            contract_id=request.contract_id,
            contract_version=contract_version,
            operation=request.operation,
            request_id=request.request_id,
            payload=payload,
            outcome=outcome,
            graph_binding=graph_binding,
            producer=producer,
            capabilities=capabilities,
            provenance=provenance,
        )


def _has_complete_success_facts(request: ReadRequest, result: ReadResult) -> bool:
    from .validation import validate_request

    provenance = result.provenance
    if validate_request(request) is not None:
        return False
    if not _is_semver_like(result.contract_version):
        return False
    if not _is_nonempty_text(result.producer):
        return False
    if not _is_nonempty_text_tuple(result.capabilities):
        return False
    if result.operation not in result.capabilities:
        return False
    if result.graph_binding is not None and not _is_nonempty_text(result.graph_binding):
        return False
    if provenance is None:
        return False
    if not _has_complete_provenance(provenance, result):
        return False
    return True


def _has_complete_provenance(provenance: Provenance, result: ReadResult) -> bool:
    authority_pairs = {
        ("og_markdown", "logseq_og_markdown"),
        ("db_native", "logseq_db_native"),
    }
    if not all(
        _is_nonempty_text(value)
        for value in (
            provenance.source_mode,
            provenance.authority,
            provenance.source_reference,
            provenance.evidence_digest,
            provenance.producer,
        )
    ):
        return False
    if (provenance.source_mode, provenance.authority) not in authority_pairs:
        return False
    if provenance.producer != result.producer:
        return False
    if not _is_nonempty_text_tuple(provenance.exercised_capabilities):
        return False
    if not set(provenance.exercised_capabilities).issubset(result.capabilities):
        return False
    return True


def _is_nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_nonempty_text_tuple(value: object) -> bool:
    return isinstance(value, tuple) and bool(value) and all(
        _is_nonempty_text(item) for item in value
    )


def _is_semver_like(value: object) -> bool:
    return isinstance(value, str) and _SEMVER_PATTERN.fullmatch(value) is not None
