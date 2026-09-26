"""Synthetic utility-protocol vectors; no model calls or subjective claims."""

from dataclasses import dataclass, replace
import hashlib
import json
import unittest

from tests.core.test_epistemic_review import load_fixture
from trama_contracts._epistemic_review import FindingKind
from trama_core._epistemic_review import _review_synthetic_scope


SCENARIO_IDS = (
    "direct-claim-hypothesis",
    "possible-contradiction",
    "verification-gap",
)
FIXTURE_SHA256 = {
    "claim-hypothesis-gap.json": "6c60a45c9f30fc3c576a63412078c0b136a80991cb4ac95a0e0a940f75c14272",
    "possible-contradiction.json": "f47bbd5f527646fc97c08060ce3c15748e0ef806284acafb283116907033c7a5",
}
PACKET_SHA256 = {
    "direct-claim-hypothesis": "3323a9d2836656f42d5bcc55d3c145ef3a99287ebf88fa528d56566548eef149",
    "possible-contradiction": "0820f6432809684a0ea33c8341895c1eed242346e26f6c6934448772755c3690",
    "verification-gap": "18e6066c0576f7af94d8b807fa253b6859001fe54b25011f54d82f5b74971ced",
}
STRUCTURED_ARTIFACT_SHA256 = {
    "direct-claim-hypothesis": "8eca5279700dba364677f72848b9aed57e0ef64fe7602b619325b4b68af1a08c",
    "possible-contradiction": "a9d27d51f39d3c4aac9914653ff0b80aae943dedd528244e4e8df8773af28b3e",
    "verification-gap": "ddfff20e35224f9398f31949843d60319e005bd3edaaad6a0911df774dbcf301",
}
ANSWER_KEY = {
    "direct-claim-hypothesis": {
        "selected_ids": ["claim-1", "hypothesis-1"],
        "excluded_ids": ["requirement-1"],
        "scope_complete": False,
        "expected_findings": [
            {"kind": "hypothesis", "evidence_ids": ["hypothesis-1"]},
            {"kind": "source_claim", "evidence_ids": ["claim-1"]},
        ],
        "outcome": "incomplete",
        "reason": "declared_scope_incomplete/v1",
    },
    "possible-contradiction": {
        "selected_ids": ["claim-a", "claim-b"],
        "excluded_ids": [],
        "scope_complete": True,
        "expected_findings": [
            {"kind": "possible_contradiction", "evidence_ids": ["claim-a", "claim-b"]},
            {"kind": "source_claim", "evidence_ids": ["claim-a"]},
            {"kind": "source_claim", "evidence_ids": ["claim-b"]},
        ],
        "outcome": "complete_for_selected_scope",
        "reason": "",
    },
    "verification-gap": {
        "selected_ids": ["claim-1", "hypothesis-1", "requirement-1"],
        "excluded_ids": [],
        "scope_complete": True,
        "expected_findings": [
            {"kind": "hypothesis", "evidence_ids": ["hypothesis-1"]},
            {"kind": "source_claim", "evidence_ids": ["claim-1"]},
            {"kind": "verification_gap", "evidence_ids": ["requirement-1"]},
        ],
        "outcome": "incomplete",
        "reason": "required_evidence_missing/v1",
    },
}
ANSWER_KEY_SHA256 = "c3c94758fedf3d8c5fbe7b24973d82e4962b9ee84e3b75b987901b02dce2b4d5"
SCORECARD_TEMPLATE = {
    "lane_id": "structured_core|agent_mediated_plain|one_shot_plain",
    "scenario_id": "",
    "evidence_linkage": False,
    "scope_fidelity": False,
    "rationale_traceability": False,
    "uncertainty_preserved": False,
    "critical_defect": False,
}
SCORECARD_TEMPLATE_SHA256 = "e3ef6109e012be59c23bf6c3981decef493d457f7bb3b9a911ed3ab20b5e171f"
PROMPT_TEMPLATES = {
    "agent_analyst": "Review only the synthetic note packet below. In normal prose, explain what the packet explicitly states, whether it presents a possible issue or missing evidence, which item IDs support your explanation, and what remains unknown or outside the selected scope. Do not infer truth, use excluded notes, or use outside information. Do not output JSON or claim that a possible conflict proves either value true. Packet: {packet}",
    "agent_verifier": "Audit the draft against only the supplied synthetic note packet. Correct unsupported claims, missing or incorrect item IDs, scope errors, missing rationale, and any loss of uncertainty. Return one corrected plain-language answer. Do not use outside information, infer truth, add facts, or output JSON. Packet: {packet} Draft: {draft}",
    "one_shot": "Read the synthetic note packet and tell me, in normal prose, what seems explicitly stated, what may need attention, which item IDs support that view, and what cannot be concluded from the selected material. Use only this packet. Do not infer truth, use excluded notes, or use outside information. Do not output JSON. Packet: {packet}",
}
PROMPT_TEMPLATE_SHA256 = {
    "agent_analyst": "4dd2e39424c82342cf3fb0cd5cf86ee7345a16cab0594c00dbd00648636bdbec",
    "agent_verifier": "43e9d4c3329f7b5c6fc499e7a54d239576fc9c647e479a7e44f0afc665946e75",
    "one_shot": "548e2b4c501031c11f4d75bd976754557af21b454c98e87feb324575e44e9b7e",
}


@dataclass(frozen=True)
class TraceabilityCard:
    evidence_linked: bool
    scope_respected: bool
    rationale_traceable: bool
    uncertainty_preserved: bool
    truth_or_global_overclaim: bool = False


def score_card(card: TraceabilityCard) -> tuple[int, bool]:
    """Return predeclared 0-4 traceability score and critical-overclaim flag."""

    if any(
        type(value) is not bool
        for value in (
            card.evidence_linked,
            card.scope_respected,
            card.rationale_traceable,
            card.uncertainty_preserved,
            card.truth_or_global_overclaim,
        )
    ):
        raise ValueError("scorecard criteria must be booleans")
    critical = card.truth_or_global_overclaim
    if critical:
        return 0, True
    return sum(
        (
            card.evidence_linked,
            card.scope_respected,
            card.rationale_traceable,
            card.uncertainty_preserved,
        )
    ), False


def utility_proxy_verdict(
    structured_scores: tuple[int, int, int] | None,
    agent_plain_scores: tuple[int, int, int] | None,
    ai_plain_scores: tuple[int, int, int] | None,
    *,
    repeats_match: bool | None,
    all_reviewer_answers_correct: bool,
    any_critical_overclaim: bool,
) -> str:
    """Apply frozen thresholds; absent comparator lane blocks the experiment."""

    if (
        type(repeats_match) is not bool
        or type(all_reviewer_answers_correct) is not bool
        or type(any_critical_overclaim) is not bool
        or structured_scores is None
        or agent_plain_scores is None
        or ai_plain_scores is None
    ):
        return "BLOCKED"
    score_vectors = (structured_scores, agent_plain_scores, ai_plain_scores)
    if any(
        type(scores) is not tuple
        or len(scores) != 3
        or any(type(score) is not int or not 0 <= score <= 4 for score in scores)
        for scores in score_vectors
    ):
        return "BLOCKED"
    if not repeats_match:
        return "NO_GO"
    if any_critical_overclaim or not all_reviewer_answers_correct:
        return "NO_GO"
    if (
        all(score >= 3 for score in structured_scores)
        and sum(structured_scores) >= 10
        and sum(structured_scores) >= sum(agent_plain_scores) + 2
        and sum(structured_scores) >= sum(ai_plain_scores) + 2
    ):
        return "PASS"
    return "NO_GO"


def render_scenario_packet(scenario_id: str, input_value: object) -> bytes:
    """Render the selected fixture facts using the frozen plain-text format."""

    selected_ids = tuple(sorted(input_value.selected_scope_ids))
    items_by_id = {item.item_id: item for item in input_value.items}
    lines = [
        f"SCENARIO: {scenario_id}",
        f"SCOPE_COMPLETE: {str(input_value.scope_complete).lower()}",
        f"SELECTED_IDS: {', '.join(selected_ids)}",
        "ITEMS:",
    ]
    for item_id in selected_ids:
        item = items_by_id[item_id]
        lines.extend(
            (
                f"ITEM: {item.item_id}",
                f"KIND: {item.kind.value}",
                f"TEXT: {json.dumps(item.text, ensure_ascii=False)}",
                "EVIDENCE_IDS: " + (", ".join(sorted(item.evidence_ids)) or "(none)"),
            )
        )
        if item.comparison is None:
            lines.append("COMPARISON: none")
        else:
            metadata = item.comparison
            fields = (
                ("date", metadata.date),
                ("context", metadata.context),
                ("key", metadata.key),
                ("subject", metadata.subject),
                ("predicate", metadata.predicate),
                ("value", metadata.value),
            )
            comparison = "; ".join(
                f"{name}={json.dumps(value, ensure_ascii=False)}" for name, value in fields
            )
            incompatible = json.dumps(list(metadata.incompatible_values), ensure_ascii=False)
            lines.append(f"COMPARISON: {comparison}; incompatible_values={incompatible}")
        lines.append("")
    return ("\n".join(lines)).encode("utf-8")


def render_structured_artifact(proposal: object) -> bytes:
    """Render the complete proposal into its frozen canonical JSON artifact."""

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
    return json.dumps(
        canonical,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


class UtilityProtocolVectorTests(unittest.TestCase):
    def test_frozen_scorer_counts_four_dimensions_and_rejects_overclaim(self) -> None:
        full = TraceabilityCard(True, True, True, True)
        incomplete = TraceabilityCard(True, True, False, True)
        overclaim = TraceabilityCard(True, True, True, True, truth_or_global_overclaim=True)

        self.assertEqual(score_card(full), (4, False))
        self.assertEqual(score_card(incomplete), (3, False))
        self.assertEqual(score_card(overclaim), (0, True))
        with self.assertRaisesRegex(ValueError, "scorecard criteria must be booleans"):
            score_card(TraceabilityCard(2, True, True, True))  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "scorecard criteria must be booleans"):
            score_card(TraceabilityCard(True, True, True, True, 1))  # type: ignore[arg-type]

    def test_frozen_verdict_requires_threshold_margin_and_correct_reviewers(self) -> None:
        passing_scores = (4, 3, 3)

        self.assertEqual(
            utility_proxy_verdict(
                passing_scores,
                (3, 2, 2),
                (3, 3, 2),
                repeats_match=True,
                all_reviewer_answers_correct=True,
                any_critical_overclaim=False,
            ),
            "PASS",
        )
        self.assertEqual(
            utility_proxy_verdict(
                passing_scores,
                (4, 3, 3),
                (3, 3, 2),
                repeats_match=True,
                all_reviewer_answers_correct=True,
                any_critical_overclaim=False,
            ),
            "NO_GO",
        )
        self.assertEqual(
            utility_proxy_verdict(
                passing_scores,
                (3, 2, 2),
                (3, 3, 2),
                repeats_match=True,
                all_reviewer_answers_correct=False,
                any_critical_overclaim=False,
            ),
            "NO_GO",
        )
        self.assertEqual(
            utility_proxy_verdict(
                passing_scores,
                None,
                (3, 3, 2),
                repeats_match=True,
                all_reviewer_answers_correct=True,
                any_critical_overclaim=False,
            ),
            "BLOCKED",
        )
        self.assertEqual(
            utility_proxy_verdict(
                passing_scores,
                (3, 2, 2),
                (3, 3, 2),
                repeats_match=False,
                all_reviewer_answers_correct=True,
                any_critical_overclaim=False,
            ),
            "NO_GO",
        )
        self.assertEqual(
            utility_proxy_verdict(
                (5, 3, 3),
                (3, 2, 2),
                (3, 3, 2),
                repeats_match=True,
                all_reviewer_answers_correct=True,
                any_critical_overclaim=False,
            ),
            "BLOCKED",
        )
        self.assertEqual(
            utility_proxy_verdict(
                (4, 3),
                (3, 2, 2),
                (3, 3, 2),
                repeats_match=True,
                all_reviewer_answers_correct=True,
                any_critical_overclaim=False,
            ),
            "BLOCKED",
        )
        self.assertEqual(
            utility_proxy_verdict(
                (True, 3, 3),
                (3, 2, 2),
                (3, 3, 2),
                repeats_match=True,
                all_reviewer_answers_correct=True,
                any_critical_overclaim=False,
            ),
            "BLOCKED",
        )

    def test_three_scenarios_repeat_core_from_identical_fixture_bytes(self) -> None:
        direct_input, direct_bytes = load_fixture("claim-hypothesis-gap.json")
        direct_input = replace(
            direct_input,
            selected_scope_ids=("claim-1", "hypothesis-1"),
            scope_complete=False,
            requirement_ids=(),
        )
        contradiction_input, contradiction_bytes = load_fixture("possible-contradiction.json")
        gap_input, gap_bytes = load_fixture("claim-hypothesis-gap.json")
        scenarios = (
            (
                "direct-claim-hypothesis",
                direct_input,
                direct_bytes,
                {FindingKind.SOURCE_CLAIM, FindingKind.HYPOTHESIS},
            ),
            (
                "possible-contradiction",
                contradiction_input,
                contradiction_bytes,
                {FindingKind.SOURCE_CLAIM, FindingKind.POSSIBLE_CONTRADICTION},
            ),
            (
                "verification-gap",
                gap_input,
                gap_bytes,
                {FindingKind.SOURCE_CLAIM, FindingKind.HYPOTHESIS, FindingKind.VERIFICATION_GAP},
            ),
        )

        for scenario_id, input_value, raw_fixture, expected_kinds in scenarios:
            with self.subTest(scenario_id=scenario_id):
                first_proposal, first_receipt = _review_synthetic_scope(input_value)
                second_proposal, second_receipt = _review_synthetic_scope(input_value)

                self.assertEqual(first_proposal, second_proposal)
                self.assertEqual(first_receipt, second_receipt)
                self.assertEqual(input_value.raw_input_digest, hashlib.sha256(raw_fixture).hexdigest())
                self.assertEqual(first_proposal.raw_input_digest, first_receipt.source_fixture_digest)
                self.assertEqual(first_receipt.selected_scope, first_proposal.scope.selected_scope_ids)
                answer = ANSWER_KEY[scenario_id]
                self.assertEqual(first_proposal.scope.scope_complete, answer["scope_complete"])
                self.assertEqual(first_proposal.outcome.value, answer["outcome"])
                self.assertEqual(first_proposal.reason, answer["reason"])
                self.assertEqual(
                    {finding.kind for finding in first_proposal.findings},
                    expected_kinds,
                )
                actual_findings = [
                    {"kind": finding.kind.value, "evidence_ids": list(finding.evidence_ids)}
                    for finding in first_proposal.findings
                ]
                self.assertEqual(actual_findings, answer["expected_findings"])

    def test_frozen_packet_answer_key_and_scorecard_hashes(self) -> None:
        direct_input, direct_bytes = load_fixture("claim-hypothesis-gap.json")
        direct_input = replace(
            direct_input,
            selected_scope_ids=("claim-1", "hypothesis-1"),
            scope_complete=False,
            requirement_ids=(),
        )
        contradiction_input, contradiction_bytes = load_fixture("possible-contradiction.json")
        gap_input, _ = load_fixture("claim-hypothesis-gap.json")
        inputs = {
            "direct-claim-hypothesis": direct_input,
            "possible-contradiction": contradiction_input,
            "verification-gap": gap_input,
        }
        for scenario_id in SCENARIO_IDS:
            packet = render_scenario_packet(scenario_id, inputs[scenario_id])
            self.assertEqual(hashlib.sha256(packet).hexdigest(), PACKET_SHA256[scenario_id])
        self.assertEqual(hashlib.sha256(direct_bytes).hexdigest(), FIXTURE_SHA256["claim-hypothesis-gap.json"])
        self.assertEqual(
            hashlib.sha256(contradiction_bytes).hexdigest(),
            FIXTURE_SHA256["possible-contradiction.json"],
        )
        canonical_json = lambda value: json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        self.assertEqual(hashlib.sha256(canonical_json(ANSWER_KEY)).hexdigest(), ANSWER_KEY_SHA256)
        self.assertEqual(
            hashlib.sha256(canonical_json(SCORECARD_TEMPLATE)).hexdigest(),
            SCORECARD_TEMPLATE_SHA256,
        )
        for prompt_id, template in PROMPT_TEMPLATES.items():
            self.assertEqual(
                hashlib.sha256(template.encode("utf-8")).hexdigest(),
                PROMPT_TEMPLATE_SHA256[prompt_id],
            )

    def test_structured_artifact_hashes_are_frozen(self) -> None:
        direct_input, _ = load_fixture("claim-hypothesis-gap.json")
        direct_input = replace(
            direct_input,
            selected_scope_ids=("claim-1", "hypothesis-1"),
            scope_complete=False,
            requirement_ids=(),
        )
        contradiction_input, _ = load_fixture("possible-contradiction.json")
        gap_input, _ = load_fixture("claim-hypothesis-gap.json")
        inputs = {
            "direct-claim-hypothesis": direct_input,
            "possible-contradiction": contradiction_input,
            "verification-gap": gap_input,
        }
        for scenario_id in SCENARIO_IDS:
            with self.subTest(scenario_id=scenario_id):
                proposal, _ = _review_synthetic_scope(inputs[scenario_id])
                digest = hashlib.sha256(render_structured_artifact(proposal)).hexdigest()
                self.assertEqual(digest, STRUCTURED_ARTIFACT_SHA256[scenario_id])


if __name__ == "__main__":
    unittest.main()
