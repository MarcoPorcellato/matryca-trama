"""Private experimental vocabulary for in-memory epistemic review only."""

from dataclasses import dataclass
from enum import StrEnum
from typing import Literal


def _require_text(value: object, name: str) -> None:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be str")
    if not value.strip():
        raise ValueError(f"{name} must be non-empty")


def _require_ids(value: object, name: str, *, allow_empty: bool = False) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{name} must be tuple")
    if not allow_empty and not value:
        raise ValueError(f"{name} must be non-empty")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"{name} must contain non-empty strings")


def _is_subset(values: tuple[str, ...], allowed: tuple[str, ...]) -> bool:
    return all(value in allowed for value in values)


def _require_findings(value: object) -> tuple["Finding", ...]:
    if not isinstance(value, tuple):
        raise TypeError("findings must be tuple")
    if any(not isinstance(item, Finding) for item in value):
        raise TypeError("findings must contain Finding")
    return value


class FindingKind(StrEnum):
    """Closed private classifications for experimental findings."""

    SOURCE_CLAIM = "source_claim"
    HYPOTHESIS = "hypothesis"
    POSSIBLE_CONTRADICTION = "possible_contradiction"
    VERIFICATION_GAP = "verification_gap"


class ReviewOutcome(StrEnum):
    """Closed review outcomes limited to a selected scope."""

    COMPLETE_FOR_SELECTED_SCOPE = "complete_for_selected_scope"
    INCOMPLETE = "incomplete"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ReviewScope:
    """Selected identifiers and declared requirement/context subsets."""

    selected_scope_ids: tuple[str, ...]
    scope_complete: bool
    requirement_ids: tuple[str, ...] = ()
    context_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        _require_ids(self.selected_scope_ids, "selected_scope_ids")
        if type(self.scope_complete) is not bool:
            raise TypeError("scope_complete must be bool")
        _require_ids(self.requirement_ids, "requirement_ids", allow_empty=True)
        _require_ids(self.context_ids, "context_ids", allow_empty=True)
        if not _is_subset(self.requirement_ids, self.selected_scope_ids):
            raise ValueError("requirement_ids must be selected")
        if not _is_subset(self.context_ids, self.selected_scope_ids):
            raise ValueError("context_ids must be selected")


@dataclass(frozen=True)
class Finding:
    """Immutable experimental observation with a non-truth confidence label."""

    kind: FindingKind
    evidence_ids: tuple[str, ...]
    selected_scope_ids: tuple[str, ...]
    rationale: str
    confidence_label: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, FindingKind):
            raise TypeError("kind must be FindingKind")
        _require_ids(self.evidence_ids, "evidence_ids")
        _require_ids(self.selected_scope_ids, "selected_scope_ids")
        _require_text(self.rationale, "rationale")
        _require_text(self.confidence_label, "confidence_label")
        match self.kind:
            case FindingKind.SOURCE_CLAIM:
                expected_label = "source_attribution_only"
            case FindingKind.HYPOTHESIS:
                expected_label = "unverified_hypothesis"
            case FindingKind.POSSIBLE_CONTRADICTION:
                expected_label = "comparison_rule_match"
            case FindingKind.VERIFICATION_GAP:
                expected_label = "not_established_in_selected_scope"
        if self.confidence_label != expected_label:
            raise ValueError("confidence_label does not match kind")


@dataclass(frozen=True)
class ReviewProposal:
    """Private experimental proposal bounded to declared in-memory scope."""

    scope: ReviewScope
    outcome: ReviewOutcome
    findings: tuple[Finding, ...]
    reason: str
    source_revision: str
    raw_input_digest: str
    canonical_comparison_digest: str

    def __post_init__(self) -> None:
        if not isinstance(self.scope, ReviewScope):
            raise TypeError("scope must be ReviewScope")
        if not isinstance(self.outcome, ReviewOutcome):
            raise TypeError("outcome must be ReviewOutcome")
        findings = _require_findings(self.findings)
        if not isinstance(self.reason, str):
            raise TypeError("reason must be str")
        _require_text(self.source_revision, "source_revision")
        _require_text(self.raw_input_digest, "raw_input_digest")
        _require_text(self.canonical_comparison_digest, "canonical_comparison_digest")
        if (
            self.source_revision == self.raw_input_digest
            or self.source_revision == self.canonical_comparison_digest
            or self.raw_input_digest == self.canonical_comparison_digest
        ):
            raise ValueError("source and digest values must be distinct")
        if any(not _is_subset(finding.selected_scope_ids, self.scope.selected_scope_ids) for finding in findings):
            raise ValueError("finding scope must be selected")
        declared_gap_scope = self.scope.requirement_ids + self.scope.context_ids
        if any(
            finding.kind is FindingKind.VERIFICATION_GAP
            and not _is_subset(finding.selected_scope_ids, declared_gap_scope)
            for finding in findings
        ):
            raise ValueError("verification gap scope must be declared")
        if self.outcome is ReviewOutcome.COMPLETE_FOR_SELECTED_SCOPE:
            if not self.scope.scope_complete:
                raise ValueError("complete outcome requires complete scope")
            if not findings:
                raise ValueError("complete outcome requires findings")
            if any(finding.kind is FindingKind.VERIFICATION_GAP for finding in findings):
                raise ValueError("complete outcome cannot include verification gap")
        elif not findings and not self.reason.strip():
            raise ValueError("empty incomplete or unknown proposal requires reason")


@dataclass(frozen=True)
class ReviewDecision:
    """Private side-effect-free disposition of one proposal digest."""

    proposal_digest: str
    disposition: Literal["acknowledge", "reject", "defer"]
    session_token: str

    def __post_init__(self) -> None:
        _require_text(self.proposal_digest, "proposal_digest")
        if not isinstance(self.disposition, str):
            raise TypeError("disposition must be str")
        if self.disposition not in ("acknowledge", "reject", "defer"):
            raise ValueError("invalid disposition")
        _require_text(self.session_token, "session_token")


def decide(
    proposal_digest: str,
    disposition: Literal["acknowledge", "reject", "defer"],
    session_token: str,
) -> ReviewDecision:
    """Return an immutable private decision without an external side effect."""

    return ReviewDecision(proposal_digest, disposition, session_token)


@dataclass(frozen=True)
class ReviewReceipt:
    """Private immutable input record without persistence behavior."""

    source_fixture_digest: str
    selected_scope: tuple[str, ...]
    engine_version: str
    proposal_digest: str
    outcome: ReviewOutcome

    def __post_init__(self) -> None:
        _require_text(self.source_fixture_digest, "source_fixture_digest")
        _require_ids(self.selected_scope, "selected_scope")
        _require_text(self.engine_version, "engine_version")
        _require_text(self.proposal_digest, "proposal_digest")
        if not isinstance(self.outcome, ReviewOutcome):
            raise TypeError("outcome must be ReviewOutcome")
