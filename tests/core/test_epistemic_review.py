"""Behavior tests for the private, synthetic epistemic review core."""

from dataclasses import replace
import hashlib
import json
from pathlib import Path
import unittest

from trama_contracts._epistemic_review import FindingKind, ReviewOutcome
from trama_core import sha256_bytes
from trama_core._epistemic_review import (
    ComparisonMetadata,
    ReviewInputError,
    ReviewItem,
    ReviewItemKind,
    SyntheticReviewInput,
    _review_synthetic_scope,
)


FIXTURES = Path(__file__).parents[1] / "fixtures" / "epistemic-review"
FIXTURE_KEYS = {
    "schema_version",
    "source_revision",
    "scope_complete",
    "selected_ids",
    "requirement_ids",
    "context_ids",
    "items",
}
ITEM_KEYS = {"id", "kind", "text", "evidence_ids", "comparison"}


class FixtureDecodeError(ValueError):
    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise FixtureDecodeError("duplicate_json_key")
        result[key] = value
    return result


def _reject_nonstandard_json_constant(value: str) -> None:
    raise FixtureDecodeError("invalid_fixture_json")


def decode_fixture(raw: bytes) -> SyntheticReviewInput:
    """Test-only strict fixture decoder; core receives bytes' digest, not bytes."""

    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise FixtureDecodeError("invalid_fixture_encoding") from error
    try:
        json.loads(text, parse_constant=_reject_nonstandard_json_constant)
    except FixtureDecodeError:
        raise
    except json.JSONDecodeError as error:
        raise FixtureDecodeError("invalid_fixture_json") from error
    try:
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_nonstandard_json_constant,
        )
    except FixtureDecodeError:
        raise
    except json.JSONDecodeError as error:
        raise FixtureDecodeError("invalid_fixture_json") from error
    if not isinstance(value, dict):
        raise FixtureDecodeError("invalid_fixture_schema")
    if set(value) - FIXTURE_KEYS:
        raise FixtureDecodeError("unknown_fixture_field")
    if set(value) != FIXTURE_KEYS or value["schema_version"] != "synthetic-review-fixture/v1":
        raise FixtureDecodeError("invalid_fixture_schema")
    if (
        type(value["source_revision"]) is not str
        or type(value["scope_complete"]) is not bool
        or any(
            type(value[field]) is not list
            or any(type(item_id) is not str for item_id in value[field])
            for field in ("selected_ids", "requirement_ids", "context_ids")
        )
        or type(value["items"]) is not list
    ):
        raise FixtureDecodeError("invalid_fixture_schema")
    string_values = [value["source_revision"], *value["selected_ids"], *value["requirement_ids"], *value["context_ids"]]
    if any(not _valid_unicode(value_text) for value_text in string_values):
        raise FixtureDecodeError("invalid_fixture_schema")
    try:
        raw_items = value["items"]
        if not isinstance(raw_items, list):
            raise FixtureDecodeError("invalid_fixture_schema")
        items: list[ReviewItem] = []
        for raw_item in raw_items:
            if not isinstance(raw_item, dict):
                raise FixtureDecodeError("invalid_fixture_schema")
            if set(raw_item) - ITEM_KEYS:
                raise FixtureDecodeError("unknown_fixture_field")
            if set(raw_item) != ITEM_KEYS:
                raise FixtureDecodeError("invalid_fixture_schema")
            if (
                type(raw_item["id"]) is not str
                or type(raw_item["kind"]) is not str
                or type(raw_item["text"]) is not str
                or type(raw_item["evidence_ids"]) is not list
                or any(type(item_id) is not str for item_id in raw_item["evidence_ids"])
                or not _valid_unicode(raw_item["id"])
                or not _valid_unicode(raw_item["kind"])
                or not _valid_unicode(raw_item["text"])
                or any(not _valid_unicode(item_id) for item_id in raw_item["evidence_ids"])
            ):
                raise FixtureDecodeError("invalid_fixture_schema")
            raw_comparison = raw_item["comparison"]
            comparison = None
            if raw_comparison is not None:
                if not isinstance(raw_comparison, dict):
                    raise FixtureDecodeError("invalid_fixture_schema")
                comparison_keys = {
                    "date",
                    "context",
                    "key",
                    "subject",
                    "predicate",
                    "value",
                    "incompatible_values",
                }
                if set(raw_comparison) - comparison_keys:
                    raise FixtureDecodeError("unknown_fixture_field")
                if set(raw_comparison) != comparison_keys:
                    raise FixtureDecodeError("invalid_fixture_schema")
                if (
                    any(
                        type(raw_comparison[field]) is not str
                        for field in ("date", "context", "key", "subject", "predicate", "value")
                    )
                    or type(raw_comparison["incompatible_values"]) is not list
                    or any(type(item) is not str for item in raw_comparison["incompatible_values"])
                    or any(
                        not _valid_unicode(raw_comparison[field])
                        for field in ("date", "context", "key", "subject", "predicate", "value")
                    )
                    or any(not _valid_unicode(item) for item in raw_comparison["incompatible_values"])
                ):
                    raise FixtureDecodeError("invalid_fixture_schema")
                comparison = ComparisonMetadata(
                    raw_comparison["date"],
                    raw_comparison["context"],
                    raw_comparison["key"],
                    raw_comparison["subject"],
                    raw_comparison["predicate"],
                    raw_comparison["value"],
                    tuple(raw_comparison["incompatible_values"]),
                )
            items.append(
                ReviewItem(
                    raw_item["id"],
                    ReviewItemKind(raw_item["kind"]),
                    raw_item["text"],
                    tuple(raw_item["evidence_ids"]),
                    comparison,
                )
            )
        return SyntheticReviewInput(
            value["source_revision"],
            sha256_bytes(raw),
            tuple(value["selected_ids"]),
            value["scope_complete"],
            tuple(value["requirement_ids"]),
            tuple(value["context_ids"]),
            tuple(items),
        )
    except FixtureDecodeError:
        raise
    except (KeyError, TypeError, ValueError) as error:
        raise FixtureDecodeError("invalid_fixture_schema") from error


def load_fixture(name: str) -> tuple[SyntheticReviewInput, bytes]:
    raw = (FIXTURES / name).read_bytes()
    return decode_fixture(raw), raw


def _valid_unicode(value: str) -> bool:
    try:
        value.encode("utf-8", errors="strict")
    except UnicodeEncodeError:
        return False
    return True


class SyntheticReviewTests(unittest.TestCase):
    def test_claim_hypothesis_and_missing_evidence_are_fixture_declared(self) -> None:
        input_value, raw = load_fixture("claim-hypothesis-gap.json")
        proposal, receipt = _review_synthetic_scope(input_value)

        self.assertEqual(
            tuple(finding.kind for finding in proposal.findings),
            (
                FindingKind.HYPOTHESIS,
                FindingKind.SOURCE_CLAIM,
                FindingKind.VERIFICATION_GAP,
            ),
        )
        self.assertEqual(proposal.outcome, ReviewOutcome.INCOMPLETE)
        self.assertEqual(proposal.reason, "required_evidence_missing/v1")
        self.assertEqual(
            tuple(finding.rationale for finding in proposal.findings),
            (
                "declared_unverified_hypothesis/v1",
                "declared_source_claim/v1",
                "required_evidence_missing/v1",
            ),
        )
        self.assertEqual(proposal.raw_input_digest, sha256_bytes(raw))
        self.assertEqual(receipt.source_fixture_digest, sha256_bytes(raw))
        self.assertEqual(receipt.selected_scope, ("claim-1", "hypothesis-1", "requirement-1"))
        self.assertEqual(receipt.outcome, proposal.outcome)
        self.assertEqual(receipt.engine_version, "synthetic-epistemic-review/v1")
        self.assertEqual(
            proposal.canonical_comparison_digest,
            "0ce60a1ef2c8c7258f39eb6d62dba980f3f5c0919df9aad03cdbdbce71b792c4",
        )
        self.assertEqual(
            receipt.proposal_digest,
            "ddfff20e35224f9398f31949843d60319e005bd3edaaad6a0911df774dbcf301",
        )
        self.assertEqual(hashlib.sha256(raw).hexdigest(), "6c60a45c9f30fc3c576a63412078c0b136a80991cb4ac95a0e0a940f75c14272")

    def test_reciprocal_declared_incompatibility_is_possible_not_truth(self) -> None:
        input_value, _ = load_fixture("possible-contradiction.json")
        proposal, _ = _review_synthetic_scope(input_value)

        contradictions = [
            finding
            for finding in proposal.findings
            if finding.kind is FindingKind.POSSIBLE_CONTRADICTION
        ]
        self.assertEqual(len(contradictions), 1)
        self.assertEqual(contradictions[0].evidence_ids, ("claim-a", "claim-b"))
        self.assertEqual(contradictions[0].selected_scope_ids, ("claim-a", "claim-b"))
        self.assertEqual(contradictions[0].rationale, "reciprocal_declared_incompatibility/v1")
        self.assertEqual(contradictions[0].confidence_label, "comparison_rule_match")
        self.assertEqual(proposal.outcome, ReviewOutcome.COMPLETE_FOR_SELECTED_SCOPE)
        self.assertEqual(
            proposal.canonical_comparison_digest,
            "1b48cfede314118a231ba3395060c5bbce6c8748c5b76c8c2f7b6aad37de7fda",
        )
        self.assertEqual(
            _review_synthetic_scope(input_value)[1].proposal_digest,
            "a9d27d51f39d3c4aac9914653ff0b80aae943dedd528244e4e8df8773af28b3e",
        )

    def test_normalization_is_limited_to_declared_comparison_fields(self) -> None:
        fixture_data = json.loads((FIXTURES / "possible-contradiction.json").read_bytes())
        left, right = fixture_data["items"][1], fixture_data["items"][0]
        left["comparison"].update(
            {
                "context": " PROJECT-A ",
                "key": " DELIVERY-DATE ",
                "subject": " Cafe\u0301 ",
                "predicate": " DELIVERY-DATE ",
                "incompatible_values": [" 2026-02-15 "],
            }
        )
        right["comparison"].update(
            {
                "context": "project-a",
                "key": "delivery-date",
                "subject": "Caf\u00e9",
                "predicate": "delivery-date",
            }
        )
        raw = json.dumps(fixture_data, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
        proposal, _ = _review_synthetic_scope(decode_fixture(raw))

        self.assertEqual(
            sum(f.kind is FindingKind.POSSIBLE_CONTRADICTION for f in proposal.findings),
            1,
        )

    def test_item_classification_is_not_inferred_from_prose(self) -> None:
        fixture_data = json.loads((FIXTURES / "claim-hypothesis-gap.json").read_bytes())
        fixture_data["items"][0]["text"] = "Maybe this is only a hypothesis."
        raw = json.dumps(fixture_data, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
        proposal, _ = _review_synthetic_scope(decode_fixture(raw))

        claim = next(f for f in proposal.findings if f.evidence_ids == ("claim-1",))
        self.assertEqual(claim.kind, FindingKind.SOURCE_CLAIM)

    def test_different_declared_comparison_dimensions_prevent_matches(self) -> None:
        input_value, _ = load_fixture("different-date-context.json")
        proposal, _ = _review_synthetic_scope(input_value)

        self.assertFalse(
            any(
                finding.kind is FindingKind.POSSIBLE_CONTRADICTION
                for finding in proposal.findings
            )
        )
        self.assertEqual(proposal.outcome, ReviewOutcome.COMPLETE_FOR_SELECTED_SCOPE)

    def test_partial_scope_does_not_use_excluded_claim(self) -> None:
        input_value, _ = load_fixture("partial-scope.json")
        proposal, _ = _review_synthetic_scope(input_value)

        self.assertFalse(proposal.scope.scope_complete)
        self.assertEqual(proposal.outcome, ReviewOutcome.INCOMPLETE)
        self.assertEqual(proposal.reason, "declared_scope_incomplete/v1")
        self.assertEqual(proposal.scope.selected_scope_ids, ("claim-a",))
        self.assertEqual(len(proposal.findings), 1)
        self.assertEqual(proposal.findings[0].kind, FindingKind.SOURCE_CLAIM)

    def test_input_tuple_permutation_preserves_full_proposal_and_receipt(self) -> None:
        input_value, _ = load_fixture("possible-contradiction.json")
        first = _review_synthetic_scope(input_value)
        permuted = replace(input_value, items=tuple(reversed(input_value.items)))
        second = _review_synthetic_scope(permuted)

        self.assertEqual(first, second)

    def test_fixture_byte_permutation_changes_raw_binding_not_comparison(self) -> None:
        input_value, raw = load_fixture("possible-contradiction.json")
        first_proposal, first_receipt = _review_synthetic_scope(input_value)
        fixture_data = json.loads(raw)
        fixture_data["items"] = list(reversed(fixture_data["items"]))
        permuted_raw = json.dumps(
            fixture_data, ensure_ascii=False, separators=(",", ":")
        ).encode("utf-8")
        permuted_input = decode_fixture(permuted_raw)
        second_proposal, second_receipt = _review_synthetic_scope(permuted_input)

        self.assertEqual(first_proposal.findings, second_proposal.findings)
        self.assertEqual(
            first_proposal.canonical_comparison_digest,
            second_proposal.canonical_comparison_digest,
        )
        self.assertNotEqual(first_proposal.raw_input_digest, second_proposal.raw_input_digest)
        self.assertNotEqual(first_receipt.proposal_digest, second_receipt.proposal_digest)
        self.assertEqual(second_proposal.raw_input_digest, sha256_bytes(permuted_raw))
        self.assertEqual(second_receipt.source_fixture_digest, sha256_bytes(permuted_raw))

    def test_source_revision_and_raw_bytes_bind_identical_comparison_facts(self) -> None:
        first_input, first_raw = load_fixture("possible-contradiction.json")
        first_proposal, first_receipt = _review_synthetic_scope(first_input)

        fixture_data = json.loads(first_raw)
        fixture_data["source_revision"] = "fixture-revision-002"
        second_raw = json.dumps(
            fixture_data, ensure_ascii=False, separators=(",", ":")
        ).encode("utf-8")
        second_input = decode_fixture(second_raw)
        second_proposal, second_receipt = _review_synthetic_scope(second_input)

        self.assertEqual(first_proposal.findings, second_proposal.findings)
        self.assertEqual(
            first_proposal.canonical_comparison_digest,
            second_proposal.canonical_comparison_digest,
        )
        self.assertNotEqual(first_proposal.source_revision, second_proposal.source_revision)
        self.assertNotEqual(first_proposal.raw_input_digest, second_proposal.raw_input_digest)
        self.assertNotEqual(first_receipt.proposal_digest, second_receipt.proposal_digest)
        self.assertNotEqual(first_receipt.source_fixture_digest, second_receipt.source_fixture_digest)

    def test_excluded_item_changes_do_not_change_findings_or_comparison_digest(self) -> None:
        input_value, _ = load_fixture("partial-scope.json")
        first_proposal, _ = _review_synthetic_scope(input_value)
        fixture_data = json.loads((FIXTURES / "partial-scope.json").read_bytes())
        fixture_data["items"][1]["text"] = "Different excluded synthetic text."
        changed_raw = json.dumps(
            fixture_data, ensure_ascii=False, indent=2
        ).encode("utf-8") + b"\n"
        changed_input = decode_fixture(changed_raw)
        second_proposal, _ = _review_synthetic_scope(changed_input)

        self.assertEqual(first_proposal.findings, second_proposal.findings)
        self.assertEqual(
            first_proposal.canonical_comparison_digest,
            second_proposal.canonical_comparison_digest,
        )
        self.assertNotEqual(first_proposal.raw_input_digest, second_proposal.raw_input_digest)

    def test_valid_one_sided_incompatibility_is_a_nonmatch(self) -> None:
        fixture_data = json.loads((FIXTURES / "possible-contradiction.json").read_bytes())
        fixture_data["items"][0]["comparison"]["incompatible_values"] = ["unrelated-value"]
        raw = json.dumps(fixture_data, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
        input_value = decode_fixture(raw)
        result = _review_synthetic_scope(input_value)

        self.assertFalse(
            any(f.kind is FindingKind.POSSIBLE_CONTRADICTION for f in result[0].findings)
        )

    def test_missing_evidence_outside_scope_remains_a_gap(self) -> None:
        fixture_data = json.loads((FIXTURES / "partial-scope.json").read_bytes())
        fixture_data["source_revision"] = "partial-with-excluded-evidence-r1"
        fixture_data["selected_ids"] = ["claim-a", "requirement-1"]
        fixture_data["requirement_ids"] = ["requirement-1"]
        fixture_data["items"].append(
            {
                "id": "requirement-1",
                "kind": "requirement",
                "text": "Evidence for this selected requirement is needed.",
                "evidence_ids": ["claim-b"],
                "comparison": None,
            }
        )
        raw = json.dumps(fixture_data, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
        expanded = decode_fixture(raw)

        proposal, _ = _review_synthetic_scope(expanded)

        gaps = [f for f in proposal.findings if f.kind is FindingKind.VERIFICATION_GAP]
        self.assertEqual(len(gaps), 1)
        self.assertEqual(gaps[0].selected_scope_ids, ("requirement-1",))

    def test_empty_selected_scope_rejects_through_typed_error(self) -> None:
        input_value, _ = load_fixture("claim-hypothesis-gap.json")
        invalid = replace(input_value, selected_scope_ids=())

        with self.assertRaises(ReviewInputError) as caught:
            _review_synthetic_scope(invalid)

        self.assertEqual(caught.exception.code, "invalid_scope")

    def test_duplicate_scope_ids_reject_through_typed_error(self) -> None:
        input_value, _ = load_fixture("claim-hypothesis-gap.json")
        invalid = replace(input_value, selected_scope_ids=("claim-1", "claim-1"))

        with self.assertRaises(ReviewInputError) as caught:
            _review_synthetic_scope(invalid)

        self.assertEqual(caught.exception.code, "duplicate_scope_id")

    def test_wrong_scope_primitive_rejects_through_typed_error(self) -> None:
        input_value, _ = load_fixture("claim-hypothesis-gap.json")
        invalid = replace(input_value, scope_complete=1)

        with self.assertRaises(ReviewInputError) as caught:
            _review_synthetic_scope(invalid)

        self.assertEqual(caught.exception.code, "invalid_input_shape")

    def test_dangling_evidence_reference_rejects_without_receipt(self) -> None:
        input_value, _ = load_fixture("claim-hypothesis-gap.json")
        requirement = input_value.items[2]
        invalid_requirement = replace(requirement, evidence_ids=("missing-id",))
        invalid = replace(
            input_value,
            items=(input_value.items[0], input_value.items[1], invalid_requirement),
        )

        with self.assertRaises(ReviewInputError) as caught:
            _review_synthetic_scope(invalid)

        self.assertEqual(caught.exception.code, "dangling_evidence_reference")

    def test_invalid_evidence_targets_and_nested_types_reject_without_receipt(self) -> None:
        valid, _ = load_fixture("claim-hypothesis-gap.json")
        claim, hypothesis, requirement = valid.items
        comparison = ComparisonMetadata(
            "2026-01-31", "project-a", "key", "subject", "predicate", "value", ("other",)
        )
        cases = (
            (
                replace(valid, items=(claim, hypothesis, replace(requirement, evidence_ids=("requirement-1",)))),
                "item_kind_scope_mismatch",
            ),
            (
                replace(valid, items=(claim, replace(hypothesis, evidence_ids=("claim-1",)), requirement)),
                "item_kind_scope_mismatch",
            ),
            (
                replace(valid, items=(claim, hypothesis, replace(requirement, evidence_ids=("hypothesis-1",)))),
                "item_kind_scope_mismatch",
            ),
            (
                replace(
                    valid,
                    items=(
                        claim,
                        hypothesis,
                        requirement,
                        replace(requirement, item_id="requirement-2", evidence_ids=("requirement-1",)),
                    ),
                ),
                "item_kind_scope_mismatch",
            ),
            (
                replace(valid, items=(claim, replace(hypothesis, comparison=comparison), requirement)),
                "invalid_comparison_metadata",
            ),
            (replace(valid, items=(object(),)), "invalid_input_shape"),
            (
                replace(valid, items=(replace(claim, evidence_ids=["claim-1"]), hypothesis, requirement)),
                "invalid_input_shape",
            ),
            (
                replace(valid, items=(replace(claim, comparison=object()), hypothesis, requirement)),
                "invalid_input_shape",
            ),
        )
        for candidate, expected_code in cases:
            with self.subTest(expected_code=expected_code):
                with self.assertRaises(ReviewInputError) as caught:
                    _review_synthetic_scope(candidate)
                self.assertEqual(caught.exception.code, expected_code)

    def test_invalid_comparison_and_text_fail_closed(self) -> None:
        input_value, _ = load_fixture("possible-contradiction.json")
        item = input_value.items[0]
        assert item.comparison is not None
        invalid_item = replace(
            item,
            comparison=replace(item.comparison, subject=" \u00a0 "),
        )
        invalid = replace(input_value, items=(invalid_item, input_value.items[1]))

        with self.assertRaises(ReviewInputError) as caught:
            _review_synthetic_scope(invalid)

        self.assertEqual(caught.exception.code, "invalid_comparison_metadata")

    def test_provenance_fields_must_be_pairwise_distinct(self) -> None:
        input_value, _ = load_fixture("claim-hypothesis-gap.json")
        invalid = replace(input_value, source_revision=input_value.raw_input_digest)

        with self.assertRaises(ReviewInputError) as caught:
            _review_synthetic_scope(invalid)

        self.assertEqual(caught.exception.code, "invalid_provenance_binding")

        valid_input, _ = load_fixture("claim-hypothesis-gap.json")
        result, _ = _review_synthetic_scope(valid_input)
        canonical_collision = replace(
            valid_input,
            raw_input_digest=result.canonical_comparison_digest,
        )
        with self.assertRaises(ReviewInputError) as caught:
            _review_synthetic_scope(canonical_collision)
        self.assertEqual(caught.exception.code, "invalid_provenance_binding")

    def test_input_validation_codes_are_stable(self) -> None:
        valid, _ = load_fixture("claim-hypothesis-gap.json")
        source_claim, hypothesis, requirement = valid.items
        cases = (
            (replace(valid, source_revision=" "), "invalid_source_revision"),
            (replace(valid, raw_input_digest="not-a-digest"), "invalid_raw_digest"),
            (
                replace(valid, items=(source_claim, hypothesis, requirement, source_claim)),
                "duplicate_item_id",
            ),
            (
                replace(valid, selected_scope_ids=("missing",), requirement_ids=()),
                "missing_selected_item",
            ),
            (replace(valid, requirement_ids=("claim-1",)), "item_kind_scope_mismatch"),
            (
                replace(
                    valid,
                    items=(source_claim, hypothesis, replace(requirement, evidence_ids=("claim-1", "claim-1"))),
                ),
                "duplicate_evidence_reference",
            ),
            (replace(valid, items=(replace(source_claim, text=" "), hypothesis, requirement)), "invalid_text"),
        )
        for candidate, code in cases:
            with self.subTest(code=code):
                with self.assertRaises(ReviewInputError) as caught:
                    _review_synthetic_scope(candidate)
                self.assertEqual(caught.exception.code, code)

        contrad_input, _ = load_fixture("possible-contradiction.json")
        claim = contrad_input.items[0]
        assert claim.comparison is not None
        invalid_date = replace(
            claim,
            comparison=replace(
                claim.comparison,
                date="2026-02-31",
            ),
        )
        with self.assertRaises(ReviewInputError) as caught:
            _review_synthetic_scope(replace(contrad_input, items=(invalid_date, contrad_input.items[1])))
        self.assertEqual(caught.exception.code, "invalid_comparison_metadata")

        duplicate_normalized_values = replace(
            claim,
            comparison=replace(
                claim.comparison,
                incompatible_values=("A", " a "),
            ),
        )
        with self.assertRaises(ReviewInputError) as caught:
            _review_synthetic_scope(
                replace(contrad_input, items=(duplicate_normalized_values, contrad_input.items[1]))
            )
        self.assertEqual(caught.exception.code, "invalid_comparison_metadata")

    def test_complete_scope_without_findings_is_unknown(self) -> None:
        fixture_data = {
            "schema_version": "synthetic-review-fixture/v1",
            "source_revision": "context-only-r1",
            "scope_complete": True,
            "selected_ids": ["context-1", "context-2"],
            "requirement_ids": [],
            "context_ids": ["context-1", "context-2"],
            "items": [
                {"id": "context-1", "kind": "context", "text": "Context item.", "evidence_ids": ["context-2"], "comparison": None},
                {"id": "context-2", "kind": "context", "text": "Another context item.", "evidence_ids": ["context-1"], "comparison": None},
            ],
        }
        input_value = decode_fixture(json.dumps(fixture_data).encode("utf-8"))

        proposal, _ = _review_synthetic_scope(input_value)

        self.assertEqual(proposal.outcome, ReviewOutcome.UNKNOWN)
        self.assertEqual(proposal.reason, "no_candidate_findings/v1")
        self.assertEqual(proposal.findings, ())

    def test_fixture_decoder_rejects_encoding_syntax_duplicate_and_unknown_fields(self) -> None:
        cases = (
            (b"\xff", "invalid_fixture_encoding"),
            (b"{", "invalid_fixture_json"),
            (b'{"x":1,"x":2}', "duplicate_json_key"),
            (b'{"unexpected":true}', "unknown_fixture_field"),
        )
        for raw, expected_code in cases:
            with self.subTest(expected_code=expected_code):
                with self.assertRaises(FixtureDecodeError) as caught:
                    decode_fixture(raw)
                self.assertEqual(caught.exception.code, expected_code)

    def test_fixture_decoder_checks_syntax_before_duplicate_keys_and_rejects_constants(self) -> None:
        cases = (
            (b'{"x":1,"x":2} trailing', "invalid_fixture_json"),
            (b'{"x":1,"x":2}', "duplicate_json_key"),
            (b'{"x":NaN}', "invalid_fixture_json"),
            (b'{"x":Infinity}', "invalid_fixture_json"),
            (b'{"x":-Infinity}', "invalid_fixture_json"),
        )
        for raw, expected_code in cases:
            with self.subTest(expected_code=expected_code, raw=raw):
                with self.assertRaises(FixtureDecodeError) as caught:
                    decode_fixture(raw)
                self.assertEqual(caught.exception.code, expected_code)

    def test_fixture_decoder_rejects_wrong_schema_types_and_surrogate_strings(self) -> None:
        fixture_data = json.loads((FIXTURES / "claim-hypothesis-gap.json").read_bytes())
        fixture_data["scope_complete"] = 1
        with self.assertRaises(FixtureDecodeError) as caught:
            decode_fixture(json.dumps(fixture_data).encode("utf-8"))
        self.assertEqual(caught.exception.code, "invalid_fixture_schema")

        fixture_data["scope_complete"] = True
        fixture_data["items"][0]["text"] = "\ud800"
        escaped_surrogate = json.dumps(fixture_data).encode("utf-8")
        with self.assertRaises(FixtureDecodeError) as caught:
            decode_fixture(escaped_surrogate)
        self.assertEqual(caught.exception.code, "invalid_fixture_schema")


if __name__ == "__main__":
    unittest.main()
