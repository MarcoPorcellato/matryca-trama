"""Typed public-envelope admission for the Plumber boundary."""

from collections.abc import Mapping
import re

from trama_contracts import Outcome, Provenance, ReadResult


CONTRACT_ID = "trama.logseq.read/v1"
_SUPPORTED_CONTRACT_MAJOR = 1
_SUPPORTED_OPERATIONS = frozenset(
    {
        "graph.identify",
        "page.read",
        "block.subtree.read.complete",
    },
)
_STABLE_SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$",
)
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def accept_for_plumber(
    result: ReadResult,
    parser_version: str,
    plumber_version: str,
) -> Mapping[str, object]:
    """Admit one complete stable OG-native public result envelope."""

    _require_complete_result(result)
    _require_supported_versions(parser_version, plumber_version)
    return result.payload


def _require_complete_result(result: object) -> None:
    if type(result) is not ReadResult:
        raise ValueError("invalid read result")
    if type(result.outcome) is not Outcome:
        raise ValueError("invalid result outcome")
    if result.outcome is not Outcome.SUCCESS:
        raise ValueError(result.outcome.value)
    if result.contract_id != CONTRACT_ID:
        raise ValueError("incompatible contract id")
    contract_version = _stable_semver(result.contract_version)
    if contract_version is None:
        raise ValueError("incompatible contract version")
    if contract_version[0] != _SUPPORTED_CONTRACT_MAJOR:
        raise ValueError("incompatible contract version")
    if result.operation not in _SUPPORTED_OPERATIONS:
        raise ValueError("unsupported operation")
    if not _is_nonempty_text(result.request_id):
        raise ValueError("invalid request id")
    if not isinstance(result.payload, Mapping):
        raise ValueError("invalid payload")
    if not _is_nonempty_text(result.graph_binding):
        raise ValueError("invalid graph binding")
    if not _is_nonempty_text(result.producer):
        raise ValueError("invalid producer")
    if not _is_nonempty_text_tuple(result.capabilities):
        raise ValueError("invalid capabilities")
    if result.operation not in result.capabilities:
        raise ValueError("operation is not advertised")
    _require_complete_og_provenance(result)


def _require_complete_og_provenance(result: ReadResult) -> None:
    provenance = result.provenance
    if type(provenance) is not Provenance:
        raise ValueError("invalid provenance")
    if (
        provenance.source_mode != "og_markdown"
        or provenance.authority != "logseq_og_markdown"
    ):
        raise ValueError("authority is not OG-native")
    if not _is_nonempty_text(provenance.source_reference):
        raise ValueError("invalid source reference")
    if not _is_sha256(provenance.evidence_digest):
        raise ValueError("invalid evidence digest")
    if provenance.producer != result.producer:
        raise ValueError("provenance producer mismatch")
    if not _is_nonempty_text_tuple(provenance.exercised_capabilities):
        raise ValueError("invalid exercised capabilities")
    if not set(provenance.exercised_capabilities).issubset(result.capabilities):
        raise ValueError("exercised capability is not advertised")
    if result.operation not in provenance.exercised_capabilities:
        raise ValueError("operation was not exercised")


def _require_supported_versions(parser_version: object, plumber_version: object) -> None:
    parser = _stable_semver(parser_version)
    if parser is None or not ((1, 7, 1) <= parser < (2, 0, 0)):
        raise ValueError("incompatible parser version")
    plumber = _stable_semver(plumber_version)
    if plumber != (2, 0, 0):
        raise ValueError("incompatible plumber version")


def _stable_semver(value: object) -> tuple[int, int, int] | None:
    if not isinstance(value, str):
        return None
    match = _STABLE_SEMVER.fullmatch(value)
    if match is None:
        return None
    return tuple(int(part) for part in match.groups())


def _is_sha256(value: object) -> bool:
    return isinstance(value, str) and _SHA256.fullmatch(value) is not None


def _is_nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _is_nonempty_text_tuple(value: object) -> bool:
    return isinstance(value, tuple) and bool(value) and all(
        _is_nonempty_text(item) for item in value
    )
