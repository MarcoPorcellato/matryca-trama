"""Private deterministic review of explicitly classified synthetic values."""

from dataclasses import dataclass
from datetime import date
from enum import StrEnum
import re
import unicodedata

from trama_contracts._epistemic_review import (
    Finding,
    FindingKind,
    ReviewOutcome,
    ReviewProposal,
    ReviewReceipt,
    ReviewScope,
)

from .digests import sha256_bytes
from .normalization import canonical_json


_ENGINE_VERSION = "synthetic-epistemic-review/v1"
_RAW_DIGEST_PATTERN = re.compile(r"[0-9a-f]{64}\Z")


class ReviewItemKind(StrEnum):
    """Fixture-declared review item classifications."""

    SOURCE_CLAIM = "source_claim"
    HYPOTHESIS = "hypothesis"
    REQUIREMENT = "requirement"
    CONTEXT = "context"


class ReviewInputError(ValueError):
    """Private fail-closed input error with a deterministic public-to-package code."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


@dataclass(frozen=True)
class ComparisonMetadata:
    """Explicit fixture-declared facts used only by the narrow comparison rule."""

    date: str
    context: str
    key: str
    subject: str
    predicate: str
    value: str
    incompatible_values: tuple[str, ...]


@dataclass(frozen=True)
class ReviewItem:
    """One immutable synthetic input item; its prose is never interpreted."""

    item_id: str
    kind: ReviewItemKind
    text: str
    evidence_ids: tuple[str, ...]
    comparison: ComparisonMetadata | None


@dataclass(frozen=True)
class SyntheticReviewInput:
    """Immutable parsed values and caller-supplied source provenance."""

    source_revision: str
    raw_input_digest: str
    selected_scope_ids: tuple[str, ...]
    scope_complete: bool
    requirement_ids: tuple[str, ...]
    context_ids: tuple[str, ...]
    items: tuple[ReviewItem, ...]


def _reject(code: str) -> None:
    raise ReviewInputError(code)


def _is_unicode_scalar_string(value: str) -> bool:
    try:
        value.encode("utf-8", errors="strict")
    except UnicodeEncodeError:
        return False
    return True


def _normalized(value: str) -> str:
    return unicodedata.normalize("NFC", value).strip().casefold()


def _validate_input_shape(value: object) -> SyntheticReviewInput:
    if not isinstance(value, SyntheticReviewInput):
        _reject("invalid_input_shape")
    if (
        type(value.source_revision) is not str
        or type(value.raw_input_digest) is not str
        or type(value.selected_scope_ids) is not tuple
        or type(value.scope_complete) is not bool
        or type(value.requirement_ids) is not tuple
        or type(value.context_ids) is not tuple
        or type(value.items) is not tuple
    ):
        _reject("invalid_input_shape")
    if any(type(item) is not ReviewItem for item in value.items):
        _reject("invalid_input_shape")
    for item in value.items:
        if (
            type(item.item_id) is not str
            or not isinstance(item.kind, ReviewItemKind)
            or type(item.text) is not str
            or type(item.evidence_ids) is not tuple
            or (item.comparison is not None and type(item.comparison) is not ComparisonMetadata)
        ):
            _reject("invalid_input_shape")
        if any(type(evidence_id) is not str for evidence_id in item.evidence_ids):
            _reject("invalid_input_shape")
        if any(not _is_unicode_scalar_string(evidence_id) for evidence_id in item.evidence_ids):
            _reject("invalid_input_shape")
    if any(
        type(item_id) is not str
        for item_id in value.selected_scope_ids + value.requirement_ids + value.context_ids
    ):
        _reject("invalid_scope")
    if any(
        not _is_unicode_scalar_string(item_id)
        for item_id in value.selected_scope_ids + value.requirement_ids + value.context_ids
    ):
        _reject("invalid_scope")
    return value


def _validate_metadata(metadata: ComparisonMetadata) -> None:
    if (
        type(metadata.date) is not str
        or type(metadata.context) is not str
        or type(metadata.key) is not str
        or type(metadata.subject) is not str
        or type(metadata.predicate) is not str
        or type(metadata.value) is not str
        or type(metadata.incompatible_values) is not tuple
        or any(type(item) is not str for item in metadata.incompatible_values)
    ):
        _reject("invalid_comparison_metadata")
    try:
        parsed_date = date.fromisoformat(metadata.date)
    except ValueError:
        _reject("invalid_comparison_metadata")
    if parsed_date.isoformat() != metadata.date:
        _reject("invalid_comparison_metadata")
    scalars = (
        metadata.context,
        metadata.key,
        metadata.subject,
        metadata.predicate,
        metadata.value,
        *metadata.incompatible_values,
    )
    if any(not _is_unicode_scalar_string(item) for item in scalars):
        _reject("invalid_comparison_metadata")
    if any(not _normalized(item) for item in scalars):
        _reject("invalid_comparison_metadata")
    if not metadata.incompatible_values:
        _reject("invalid_comparison_metadata")
    if len(set(metadata.incompatible_values)) != len(metadata.incompatible_values):
        _reject("invalid_comparison_metadata")
    normalized_incompatible = tuple(_normalized(item) for item in metadata.incompatible_values)
    if len(set(normalized_incompatible)) != len(normalized_incompatible):
        _reject("invalid_comparison_metadata")


def _validate_input(value: object) -> tuple[SyntheticReviewInput, ReviewScope, dict[str, ReviewItem]]:
    review_input = _validate_input_shape(value)
    if not review_input.source_revision.strip() or not _is_unicode_scalar_string(review_input.source_revision):
        _reject("invalid_source_revision")
    if _RAW_DIGEST_PATTERN.fullmatch(review_input.raw_input_digest) is None:
        _reject("invalid_raw_digest")

    item_ids = tuple(item.item_id for item in review_input.items)
    if len(set(item_ids)) != len(item_ids):
        _reject("duplicate_item_id")
    if (
        len(set(review_input.selected_scope_ids)) != len(review_input.selected_scope_ids)
        or len(set(review_input.requirement_ids)) != len(review_input.requirement_ids)
        or len(set(review_input.context_ids)) != len(review_input.context_ids)
    ):
        _reject("duplicate_scope_id")
    if (
        not review_input.selected_scope_ids
        or not all(item_id.strip() for item_id in review_input.selected_scope_ids)
        or not all(item_id.strip() for item_id in review_input.requirement_ids)
        or not all(item_id.strip() for item_id in review_input.context_ids)
        or not set(review_input.requirement_ids).issubset(review_input.selected_scope_ids)
        or not set(review_input.context_ids).issubset(review_input.selected_scope_ids)
        or set(review_input.requirement_ids).intersection(review_input.context_ids)
    ):
        _reject("invalid_scope")

    items_by_id = {item.item_id: item for item in review_input.items}
    selected_ids = set(review_input.selected_scope_ids)
    if not selected_ids.issubset(items_by_id):
        _reject("missing_selected_item")

    for item in review_input.items:
        if len(set(item.evidence_ids)) != len(item.evidence_ids):
            _reject("duplicate_evidence_reference")
    for item in review_input.items:
        if any(evidence_id not in items_by_id for evidence_id in item.evidence_ids):
            _reject("dangling_evidence_reference")

    requirements = set(review_input.requirement_ids)
    contexts = set(review_input.context_ids)
    for item in review_input.items:
        if not _is_unicode_scalar_string(item.item_id) or not item.item_id.strip():
            _reject("invalid_input_shape")
        if item.kind in (ReviewItemKind.SOURCE_CLAIM, ReviewItemKind.HYPOTHESIS):
            if item.evidence_ids:
                _reject("item_kind_scope_mismatch")
        elif item.kind is ReviewItemKind.REQUIREMENT:
            if item.item_id in selected_ids and item.item_id not in requirements:
                _reject("item_kind_scope_mismatch")
        elif item.kind is ReviewItemKind.CONTEXT:
            if item.item_id in selected_ids and item.item_id not in contexts:
                _reject("item_kind_scope_mismatch")
        if item.evidence_ids and any(
            items_by_id[evidence_id].kind not in (ReviewItemKind.SOURCE_CLAIM, ReviewItemKind.CONTEXT)
            or evidence_id == item.item_id
            for evidence_id in item.evidence_ids
        ):
            _reject("item_kind_scope_mismatch")
    if any(items_by_id[item_id].kind is not ReviewItemKind.REQUIREMENT for item_id in requirements):
        _reject("item_kind_scope_mismatch")
    if any(items_by_id[item_id].kind is not ReviewItemKind.CONTEXT for item_id in contexts):
        _reject("item_kind_scope_mismatch")

    for item in review_input.items:
        if not _is_unicode_scalar_string(item.text) or not item.text.strip():
            _reject("invalid_text")
        if item.kind is not ReviewItemKind.SOURCE_CLAIM and item.comparison is not None:
            _reject("invalid_comparison_metadata")
        if item.comparison is not None:
            _validate_metadata(item.comparison)

    try:
        scope = ReviewScope(
            tuple(sorted(review_input.selected_scope_ids)),
            review_input.scope_complete,
            tuple(sorted(review_input.requirement_ids)),
            tuple(sorted(review_input.context_ids)),
        )
    except (TypeError, ValueError):
        _reject("invalid_scope")
    return review_input, scope, items_by_id


def _canonical_comparison_metadata(metadata: ComparisonMetadata | None) -> dict[str, object] | None:
    if metadata is None:
        return None
    return {
        "date": metadata.date,
        "context": _normalized(metadata.context),
        "key": _normalized(metadata.key),
        "subject": _normalized(metadata.subject),
        "predicate": _normalized(metadata.predicate),
        "value": _normalized(metadata.value),
        "incompatible_values": sorted(_normalized(value) for value in metadata.incompatible_values),
    }


def _comparison_digest(
    review_input: SyntheticReviewInput,
    scope: ReviewScope,
    items_by_id: dict[str, ReviewItem],
) -> str:
    entries: list[dict[str, object]] = []
    for item_id in scope.selected_scope_ids:
        item = items_by_id[item_id]
        entries.append(
            {
                "id": item.item_id,
                "kind": item.kind.value,
                "evidence_ids": sorted(item.evidence_ids),
                "comparison": _canonical_comparison_metadata(item.comparison),
            }
        )
    canonical = {
        "schema_version": "synthetic-review-comparison/v1",
        "normalization_version": "nfc-strip-casefold/v1",
        "scope": {
            "selected_ids": list(scope.selected_scope_ids),
            "scope_complete": scope.scope_complete,
            "requirement_ids": list(scope.requirement_ids),
            "context_ids": list(scope.context_ids),
        },
        "items": entries,
    }
    return sha256_bytes(canonical_json(canonical))


def _finding_order(finding: Finding) -> tuple[str, tuple[str, ...], tuple[str, ...], str, str]:
    return (
        finding.kind.value,
        finding.selected_scope_ids,
        finding.evidence_ids,
        finding.rationale,
        finding.confidence_label,
    )


def _make_findings(scope: ReviewScope, items_by_id: dict[str, ReviewItem]) -> tuple[Finding, ...]:
    selected_items = tuple(items_by_id[item_id] for item_id in scope.selected_scope_ids)
    findings: list[Finding] = []
    for item in selected_items:
        if item.kind is ReviewItemKind.SOURCE_CLAIM:
            findings.append(
                Finding(
                    FindingKind.SOURCE_CLAIM,
                    (item.item_id,),
                    (item.item_id,),
                    "declared_source_claim/v1",
                    "source_attribution_only",
                )
            )
        elif item.kind is ReviewItemKind.HYPOTHESIS:
            findings.append(
                Finding(
                    FindingKind.HYPOTHESIS,
                    (item.item_id,),
                    (item.item_id,),
                    "declared_unverified_hypothesis/v1",
                    "unverified_hypothesis",
                )
            )
        elif not set(item.evidence_ids).intersection(scope.selected_scope_ids):
            findings.append(
                Finding(
                    FindingKind.VERIFICATION_GAP,
                    (item.item_id,),
                    (item.item_id,),
                    "required_evidence_missing/v1",
                    "not_established_in_selected_scope",
                )
            )

    claims = tuple(
        item
        for item in selected_items
        if item.kind is ReviewItemKind.SOURCE_CLAIM and item.comparison is not None
    )
    for index, left in enumerate(claims):
        left_metadata = left.comparison
        assert left_metadata is not None
        for right in claims[index + 1 :]:
            right_metadata = right.comparison
            assert right_metadata is not None
            left_fields = (
                left_metadata.date,
                _normalized(left_metadata.context),
                _normalized(left_metadata.key),
                _normalized(left_metadata.subject),
                _normalized(left_metadata.predicate),
            )
            right_fields = (
                right_metadata.date,
                _normalized(right_metadata.context),
                _normalized(right_metadata.key),
                _normalized(right_metadata.subject),
                _normalized(right_metadata.predicate),
            )
            left_value = _normalized(left_metadata.value)
            right_value = _normalized(right_metadata.value)
            if (
                left_fields == right_fields
                and left_value != right_value
                and right_value in {_normalized(value) for value in left_metadata.incompatible_values}
                and left_value in {_normalized(value) for value in right_metadata.incompatible_values}
            ):
                pair = tuple(sorted((left.item_id, right.item_id)))
                findings.append(
                    Finding(
                        FindingKind.POSSIBLE_CONTRADICTION,
                        pair,
                        pair,
                        "reciprocal_declared_incompatibility/v1",
                        "comparison_rule_match",
                    )
                )
    return tuple(sorted(findings, key=_finding_order))


def _proposal_digest(proposal: ReviewProposal) -> str:
    canonical = {
        "schema_version": "synthetic-review-proposal/v1",
        "scope": {
            "selected_scope_ids": list(proposal.scope.selected_scope_ids),
            "scope_complete": proposal.scope.scope_complete,
            "requirement_ids": list(proposal.scope.requirement_ids),
            "context_ids": list(proposal.scope.context_ids),
        },
        "outcome": proposal.outcome.value,
        "reason": proposal.reason,
        "source_revision": proposal.source_revision,
        "raw_input_digest": proposal.raw_input_digest,
        "canonical_comparison_digest": proposal.canonical_comparison_digest,
        "findings": [
            {
                "kind": finding.kind.value,
                "evidence_ids": list(finding.evidence_ids),
                "selected_scope_ids": list(finding.selected_scope_ids),
                "rationale": finding.rationale,
                "confidence_label": finding.confidence_label,
            }
            for finding in proposal.findings
        ],
    }
    return sha256_bytes(canonical_json(canonical))


def _review_synthetic_scope(
    input_value: SyntheticReviewInput,
) -> tuple[ReviewProposal, ReviewReceipt]:
    """Review declared synthetic items in memory and return a proposal and receipt."""

    review_input, scope, items_by_id = _validate_input(input_value)
    canonical_digest = _comparison_digest(review_input, scope, items_by_id)
    if len({review_input.source_revision, review_input.raw_input_digest, canonical_digest}) != 3:
        _reject("invalid_provenance_binding")

    findings = _make_findings(scope, items_by_id)
    has_gap = any(finding.kind is FindingKind.VERIFICATION_GAP for finding in findings)
    if not scope.scope_complete:
        outcome = ReviewOutcome.INCOMPLETE
        reason = "declared_scope_incomplete/v1"
    elif has_gap:
        outcome = ReviewOutcome.INCOMPLETE
        reason = "required_evidence_missing/v1"
    elif findings:
        outcome = ReviewOutcome.COMPLETE_FOR_SELECTED_SCOPE
        reason = ""
    else:
        outcome = ReviewOutcome.UNKNOWN
        reason = "no_candidate_findings/v1"

    proposal = ReviewProposal(
        scope,
        outcome,
        findings,
        reason,
        review_input.source_revision,
        review_input.raw_input_digest,
        canonical_digest,
    )
    proposal_digest = _proposal_digest(proposal)
    receipt = ReviewReceipt(
        review_input.raw_input_digest,
        scope.selected_scope_ids,
        _ENGINE_VERSION,
        proposal_digest,
        outcome,
    )
    return proposal, receipt
