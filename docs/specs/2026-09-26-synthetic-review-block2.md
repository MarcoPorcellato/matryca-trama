# Synthetic epistemic review — Block 2 specification

**Status:** merged in PR #23 at `eca93f19398972ede50127ce6aaa93d78fb5d5cd`; exact PR checks and merged-main Python contracts and Foundation CI passed. This evidence qualifies only the private synthetic core. No release, real-graph, operational application, performance, user-utility, or product-support claim.
**Scope:** private, deterministic, in-memory analysis of repository-owned synthetic values only.
**Authority:** autonomous Trama programme; entry GO was issued on the reviewed contract hash recorded in the local Block 2 receipt. Current status text does not alter contract semantics.

This specification narrows Block 2 of the local programme. It does not establish an operational graph/application runtime, real-source support, a public stable contract, consumer adapter, release support, truth engine, or user-utility result. Repository-owned content remains under PolyForm Noncommercial 1.0.0. No external copyright-bearing contribution is admitted before a lawyer-reviewed contributor agreement or equivalent grant exists.

## 1. Package and side-effect boundary

Implementation, if admitted, adds one private module at `packages/core/src/trama_core/_epistemic_review.py`. It depends only on the standard library and the already-admitted `trama_contracts` and `trama_core` modules. The existing permitted `trama-core → trama-contracts` workspace dependency must be declared explicitly in package metadata. This adds no external dependency or architectural edge, package, public export, fixture loader, filesystem access, network, database, host, application, UI, persistence, or write path.

Only tests read the repository-owned JSON fixtures as exact UTF-8 bytes. The test boundary computes the SHA-256 of those exact bytes and supplies the resulting digest and opaque fixture revision separately to the pure core. The core never reads or verifies bytes it was not given. Receipt construction is in-memory; no receipt is stored or written.

Owned paths, if admitted:

- `packages/core/src/trama_core/_epistemic_review.py`
- `packages/core/pyproject.toml` (declare only the existing local `trama-contracts` workspace dependency)
- `uv.lock` (resolve that local workspace dependency; no unrelated upgrades)
- `tests/contracts/test_read_only_posture.py` (admit only the two pure standard-library import roots required by this specification, with focused positive and negative regression coverage)
- `tests/core/test_epistemic_review.py`
- `tests/fixtures/epistemic-review/claim-hypothesis-gap.json`
- `tests/fixtures/epistemic-review/possible-contradiction.json`
- `tests/fixtures/epistemic-review/different-date-context.json`
- `tests/fixtures/epistemic-review/partial-scope.json`
- this specification, `docs/specs/2026-09-19-epistemic-review-first-tranche.md`, `docs/status/CLAIM_LEDGER.md`, and `docs/ROADMAP.md`

No other path changes without a new block decision. No external dependency, architecture rule, package, DTO, public export, or version change is admitted. The contract scanner amendment is limited to adding `datetime` and `unicodedata` to its explicit `ALLOWED_IMPORT_ROOTS`; no existing forbidden import, call, or check may be removed or weakened. Add regression assertions that representative `from datetime import date` plus `date.fromisoformat(...)` and `unicodedata.normalize("NFC", ...)` have no scanner violation, and that a disallowed import and mutation call remain violations even when combined with those admitted imports. This allowlist is only a coarse static policy projection; focused behavior tests and source review remain responsible for confirming usage stays within the frozen date-validation and NFC-normalization rules.

## 2. Fixture and immutable input schema

Fixtures are strict JSON objects with exactly these top-level keys:

```json
{
  "schema_version": "synthetic-review-fixture/v1",
  "source_revision": "fixture-revision-001",
  "scope_complete": true,
  "selected_ids": ["claim-1", "requirement-1"],
  "requirement_ids": ["requirement-1"],
  "context_ids": [],
  "items": []
}
```

Unknown keys and duplicate JSON object keys are rejected by the test-only fixture decoder. Core input is a frozen typed value with `source_revision: str`, `raw_input_digest: str`, `selected_scope_ids: tuple[str, ...]`, `scope_complete: bool`, `requirement_ids: tuple[str, ...]`, `context_ids: tuple[str, ...]`, and `items: tuple[ReviewItem, ...]`. The decoder passes the test-boundary digest; it does not put raw fixture bytes into core input. Strict UTF-8 decoding rejects malformed byte sequences and JSON strings containing unpaired surrogate code points. JSON `selected_ids` maps to core `selected_scope_ids`.

Each fixture item has exactly:

```json
{
  "id": "claim-1",
  "kind": "source_claim",
  "text": "The source explicitly states this.",
  "evidence_ids": [],
  "comparison": null
}
```

`kind` is one of `source_claim`, `hypothesis`, `requirement`, or `context`. `id` is a non-empty, exact, case-sensitive string unique across all items. `text` is a non-empty Unicode string preserved exactly after JSON decoding; the raw digest separately retains the original fixture-byte distinction. Text is displayed only as fixture evidence and never analyzed for meaning. `evidence_ids` is a list of unique item IDs. Every referenced ID must resolve to a different fixture item whose kind is `source_claim` or `context`; self-references and hypothesis/requirement references are invalid. `source_claim` and `hypothesis` items must have empty `evidence_ids`; they produce only their explicitly declared classification and use their own item ID as the finding evidence reference. For selected `requirement` and `context` items, evidence is present in the selected scope only if at least one referenced item ID is also selected. An empty list or references only to excluded items means required evidence is missing and produces a gap; excluded evidence cannot support a selected-scope conclusion. This is a synthetic declared state, not an independent verification.

`selected_ids` is non-empty, unique, and references existing fixture items. Items outside `selected_ids` are excluded from findings and canonical comparison digest. `requirement_ids` and `context_ids` are unique subsets of `selected_ids`; each referenced item's kind must agree with its subset. All selected `requirement` and `context` items must be listed in the corresponding subset. `scope_complete` must be a JSON boolean and is a fixture declaration only. All items, including excluded ones, must pass structural validation. Duplicate IDs, dangling evidence IDs, kind/subset disagreement, duplicate scope IDs, missing selected items, unknown fields, invalid JSON, non-UTF-8 fixture bytes, or wrong field types reject the whole invocation.

For a `source_claim`, `hypothesis`, `requirement`, or `context`, `comparison` is either `null` or an object with exactly these keys:

```json
{
  "date": "2026-01-31",
  "context": "project-a",
  "key": "delivery-date",
  "subject": "project-a",
  "predicate": "delivery-date",
  "value": "2026-01-31",
  "incompatible_values": ["2026-02-15"]
}
```

For contradiction matching, a source-claim item's `comparison` may be `null` (no comparison candidate) or a complete object with all six scalar fields (`date`, `context`, `key`, `subject`, `predicate`, `value`) and a non-empty `incompatible_values` tuple. For every non-source-claim kind, comparison must be `null`; extra metadata is rejected. `date` is a valid Gregorian `YYYY-MM-DD` date. The other values are non-empty strings. Every `incompatible_values` entry is non-empty and unique both before and after normalization. Every normalized non-date scalar must remain non-empty. Values are fixture-declared metadata, not facts inferred from `text`.

The immutable core types are frozen dataclasses and tuples: `SyntheticReviewInput(source_revision, raw_input_digest, selected_scope_ids, scope_complete, requirement_ids, context_ids, items)`; `ReviewItem(item_id, kind, text, evidence_ids, comparison)`; and `ComparisonMetadata(date, context, key, subject, predicate, value, incompatible_values)`. `ReviewItemKind` is a closed enum with the four JSON kind values. Input dataclasses store supplied values without performing I/O. `_review_synthetic_scope` validates its complete input and rejects non-tuples, booleans in place of strings, empty identifiers, malformed digests, duplicate IDs/refs, dangling references, unsupported kinds, invalid Unicode scalar strings, and invalid scope subsets through a private `ReviewInputError` carrying one stable code from §6. Only after every input check succeeds does the core construct the existing `ReviewScope` DTO. The function accepts only `SyntheticReviewInput`; other values reject with `invalid_input_shape`.

## 3. Exact normalization and comparison rule

Original `text`, IDs, `source_revision`, and raw digest are never normalized. IDs are exact and case-sensitive. Date is validated and compared in its exact canonical ISO form.

The five non-date comparison fields (`context`, `key`, `subject`, `predicate`, and `value`, including `incompatible_values`) use this single versioned rule: Unicode NFC normalization, trim leading/trailing Unicode whitespace with Python `str.strip()`, then Unicode `str.casefold()`. No internal whitespace folding, punctuation removal, stemming, transliteration, fuzzy matching, locale-dependent comparison, or semantic inference occurs. The normalized values are used only for equality and the comparison digest; fixture strings and source text remain unchanged.

Two distinct selected `source_claim` items produce at most one `possible_contradiction` finding if and only if both have complete comparison objects; their normalized `date`, `context`, `key`, `subject`, and `predicate` are all equal; their normalized `value` fields differ; and each item's normalized `incompatible_values` explicitly contains the other's normalized `value`. This reciprocal declaration is the sole incompatibility rule. A valid one-sided declaration, similar wording, different date/context/key/subject/predicate, or any hypothesis produces no contradiction and is not an input error. No truth verdict is produced.

## 4. Findings, scope, ordering, and outcomes

The core constructs only existing private `Finding`, `FindingKind`, `ReviewScope`, `ReviewProposal`, `ReviewOutcome`, and `ReviewReceipt` values from `trama_contracts._epistemic_review`; it does not change or export those DTOs.

- Each selected `source_claim` produces `SOURCE_CLAIM`, evidence `(item.id,)`, its one-item selected scope, rationale `declared_source_claim/v1`, and confidence `source_attribution_only`.
- Each selected `hypothesis` produces `HYPOTHESIS`, evidence `(item.id,)`, its one-item selected scope, rationale `declared_unverified_hypothesis/v1`, and confidence `unverified_hypothesis`.
- Each selected requirement/context for which `set(item.evidence_ids) ∩ set(scope.selected_scope_ids)` is empty produces `VERIFICATION_GAP`, evidence `(item.id,)`, its one-item selected scope, rationale `required_evidence_missing/v1`, and confidence `not_established_in_selected_scope`. Non-empty references only to excluded items still produce a gap.
- Each qualifying pair produces one `POSSIBLE_CONTRADICTION`, evidence IDs equal to the two item IDs in ascending exact-ID order, selected scope equal to those two IDs in ascending exact-ID order, rationale `reciprocal_declared_incompatibility/v1`, and confidence `comparison_rule_match`.
- A requirement/context item with at least one evidence ID inside selected scope produces no finding. Evidence IDs are references only; the algorithm does not inspect referenced text or validate truth.

Findings are sorted by `(kind.value, selected_scope_ids, evidence_ids, rationale, confidence_label)`. Scope ID tuples and requirement/context tuples are sorted by exact Unicode code-point order in output. Pair enumeration uses the same stable ordering. No input order affects proposal fields.

Outcome is deterministic:

| Condition | Outcome | Reason |
|---|---|---|
| `scope_complete` is false | `INCOMPLETE` | `declared_scope_incomplete/v1` |
| Any verification-gap finding | `INCOMPLETE` | `required_evidence_missing/v1` |
| Scope is complete, no gaps, and at least one other finding | `COMPLETE_FOR_SELECTED_SCOPE` | empty reason |
| Scope is complete and no findings exist | `UNKNOWN` | `no_candidate_findings/v1` |

The outcome describes only the explicitly selected synthetic scope. It never states or implies that an excluded item or real graph contains no contradiction. Existing DTO validation requires a non-empty `ReviewScope`; therefore empty `selected_ids` is invalid input, not a successful empty review.

## 5. Canonical digests and receipt return

All digests are lowercase 64-character SHA-256 hex from the existing `trama_core.sha256_bytes`; no new digest library or prefix is introduced. The three provenance facts remain separate: opaque `source_revision`, exact-byte `raw_input_digest`, and `canonical_comparison_digest`. Before constructing `ReviewProposal`, the core rejects with `invalid_provenance_binding` unless these three strings are pairwise distinct, matching the existing DTO invariant. The fixture decoder/test boundary computes only the raw digest.

The canonical comparison object is exactly:

```json
{
  "schema_version": "synthetic-review-comparison/v1",
  "normalization_version": "nfc-strip-casefold/v1",
  "scope": {
    "selected_ids": [],
    "scope_complete": true,
    "requirement_ids": [],
    "context_ids": []
  },
  "items": []
}
```

The `items` list contains selected items only, sorted by exact ID. Each entry contains `id`, `kind`, sorted `evidence_ids`, and either `comparison: null` or all seven comparison fields with the five non-date fields normalized as in §3 and `incompatible_values` sorted after normalization. Item `text`, excluded items, fixture file path, raw bytes, source revision, and fixture array order are omitted. `canonical_comparison_digest` is SHA-256 of `canonical_json` of that object. Therefore changing only source prose or excluded-item content can change the raw digest while preserving the comparison digest; changing selected declared comparison metadata or scope can change the comparison digest.

Proposal digest uses this complete canonical JSON object; these key names and nesting are normative:

```json
{
  "schema_version": "synthetic-review-proposal/v1",
  "scope": {
    "selected_scope_ids": [],
    "scope_complete": true,
    "requirement_ids": [],
    "context_ids": []
  },
  "outcome": "complete_for_selected_scope",
  "reason": "",
  "source_revision": "fixture-revision-001",
  "raw_input_digest": "<64 lowercase hex characters>",
  "canonical_comparison_digest": "<64 lowercase hex characters>",
  "findings": [
    {
      "kind": "source_claim",
      "evidence_ids": ["claim-1"],
      "selected_scope_ids": ["claim-1"],
      "rationale": "declared_source_claim/v1",
      "confidence_label": "source_attribution_only"
    }
  ]
}
```

Scope ID arrays and each finding's arrays are sorted as specified in §4; `findings` uses the canonical order from §4. It is SHA-256 of existing `canonical_json` bytes. It does not include the receipt, avoiding recursive hashing.

The pure public-to-package function remains private as `_review_synthetic_scope(input_value) -> tuple[ReviewProposal, ReviewReceipt]`. It returns an immutable two-item tuple. The proposal contains the three distinct source/digest values. The receipt has `source_fixture_digest == raw_input_digest`, sorted selected IDs, `engine_version == "synthetic-epistemic-review/v1"`, the complete proposal digest, and the same outcome as the proposal. No receipt persistence or I/O exists.

## 6. Rejection semantics

Malformed or unverifiable declared input rejects the entire invocation by raising private `ReviewInputError`; no proposal or receipt is returned. Stable error codes are:

- `invalid_input_shape`
- `invalid_source_revision`
- `invalid_raw_digest`
- `invalid_scope`
- `duplicate_item_id`
- `missing_selected_item`
- `dangling_evidence_reference`
- `item_kind_scope_mismatch`
- `invalid_comparison_metadata`
- `invalid_text`
- `duplicate_scope_id`
- `duplicate_evidence_reference`
- `invalid_provenance_binding`

The test-only fixture decoder raises its own `FixtureDecodeError(code: str)` with stable codes `invalid_fixture_encoding`, `invalid_fixture_json`, `duplicate_json_key`, `unknown_fixture_field`, and `invalid_fixture_schema`. Core input validation raises `ReviewInputError(code: str)` with the codes in the list. To make the first reported code stable, validation order is: input class/container and primitive types (`invalid_input_shape`); source revision (`invalid_source_revision`); raw digest (`invalid_raw_digest`); duplicate item IDs (`duplicate_item_id`); duplicate selected/requirement/context scope IDs (`duplicate_scope_id`); invalid scope tuple/boolean shape, empty selection, or requirement/context subset (`invalid_scope`); unknown selected IDs (`missing_selected_item`); duplicate evidence references (`duplicate_evidence_reference`); dangling evidence references (`dangling_evidence_reference`); evidence target or item-kind/scope-kind mismatch (`item_kind_scope_mismatch`); invalid text (`invalid_text`); comparison fields, date, normalization, or incompatible-value uniqueness (`invalid_comparison_metadata`); then pairwise provenance binding (`invalid_provenance_binding`). A recognized item kind with an unsupported string maps to `invalid_input_shape`. Only after these checks does the core construct `ReviewScope`, so its constructor cannot leak a generic error for malformed caller input. For fixture decoding, encoding is checked first, then JSON syntax, duplicate object keys, unknown keys, then remaining schema shape/types. Neither error path returns a proposal or receipt. No malformed condition is converted into an `UNKNOWN`, `INCOMPLETE`, omitted finding, or success receipt. Valid but incomplete selected scope and valid missing evidence remain the distinct outcomes in §4.

## 7. Independent test matrix

Tests must freeze expected DTO fields and expected digests as literals derived independently of the implementation under test. They must include:

1. `claim-hypothesis-gap.json`: each explicitly typed claim/hypothesis and a missing-evidence requirement yield the specified findings, exact rationale IDs, and `INCOMPLETE`.
2. `possible-contradiction.json`: one reciprocal declared pair yields exactly one possible-contradiction finding with both IDs, no truth result, stable order, and expected digests.
3. `different-date-context.json`: different date, context, key, subject, or predicate independently prevents a contradiction; similar prose has no effect.
4. `partial-scope.json`: excluded claims never affect findings or comparison digest; `scope_complete=false` yields `INCOMPLETE`, never a global negative conclusion.
5. Permuting immutable input item tuples while preserving `source_revision` and `raw_input_digest` yields identical full proposal, proposal digest, and receipt; this is an in-memory determinism vector and does not assert that the supplied raw digest is verified against typed values. Separately, permuting/re-encoding fixture arrays and recomputing the raw digest preserves findings, their canonical order, and `canonical_comparison_digest`, while proposal `raw_input_digest`, proposal digest, and receipt change to bind the new exact bytes. Repeating the same exact fixture bytes yields identical proposal and receipt.
6. Two source revisions/byte encodings with identical selected normalized comparison values retain distinct revision/raw digests and the same canonical comparison digest; their proposal digests and receipts still differ because they bind source revision and raw digest.
7. Mutating an excluded valid item's text or comparison metadata leaves findings and comparison digest unchanged; the test-boundary raw digest changes.
8. Invalid JSON, invalid UTF-8, duplicate JSON object keys, unknown fields, wrong types, empty or duplicate IDs, duplicate scope/evidence IDs, unknown selected IDs, dangling evidence references, self/hypothesis/requirement evidence references, scope/kind mismatch, malformed dates, empty-after-normalization metadata, normalized duplicate incompatible values, and provenance fields that violate pairwise inequality each fail closed with the exact error code and no receipt.
9. A valid one-sided incompatibility declaration produces no contradiction and no input error; reciprocal declarations produce exactly one pair finding.
10. Empty selected scope rejects as `invalid_scope`; complete scope with no findings returns `UNKNOWN` and the stable reason.
11. Import-boundary tests prove core imports no filesystem, network, database, app, adapter, bridge, Brain, Pro, Parser, or Plumber module. Full R1 validation remains required by the local development skill.
12. `tests/contracts/test_read_only_posture.py` accepts only the two newly required pure standard-library roots `datetime` and `unicodedata` for this scope; positive examples exercise Gregorian ISO parsing and NFC normalization. Existing disallowed-import and mutation-call rejection still passes, including a combined source sample containing both admitted imports plus a prohibited import and write call. No scanner refactor or other allowlist expansion is allowed.

## 8. Entry gate

Entry gates were completed in two bounded amendments: first the existing local `trama-contracts` workspace dependency was declared in package metadata, then the read-only scanner admitted only `datetime` and `unicodedata` with positive/negative regression tests. The original contract was reviewed at spec SHA `68df0ceed6981bd442b7a333dfd6ea8cbd1c7c1d4cc2f0f2140883e87a6195b2`; the scanner-scope entry GO was bound to the status-revised spec SHA `7d8c51ce429f7d40737226ba17e87d5f514a019a0868359eea65ec5132543914`. Those rulings admit only paths and semantics in §§1 and 7. Sol's subsequent implementation exit review returned `BLOCKED` on missing adversarial/provenance vectors and strict JSON parsing precedence. Candidate repairs are in progress; fresh Sol exit review and Astra exit GO remain required. The status-only update here does not change the frozen input/output contract or widen implementation scope.
