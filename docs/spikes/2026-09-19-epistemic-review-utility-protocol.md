# Synthetic epistemic-review utility protocol

**Status:** protocol draft for independent review; no comparator experiment has run.
**Scope:** local, synthetic-only utility proxy for the private Block 2 core.
**Authority:** Block 3 preparation GO. Experiment execution remains blocked until Sol reviews this exact protocol and Astra issues ENTRY GO on its frozen hash.

This protocol tests whether the structured synthetic review output makes evidence and scope more traceable than two plain-language review baselines. It is not a real-user study, user-utility claim, performance benchmark, truth test, model-quality evaluation, or release qualification. All inputs are repository-owned synthetic fixtures. No graph, private note, external source, product runtime integration, direct network/API call, new dependency, or persistence is involved. Comparator responses are research delegations through the Codex model platform; they consume ordinary model usage and are not offline, deterministic, or cost-free.

## 1. Fixed scenarios and source binding

Use the exact fixture bytes at the selected merged Block 2 head. The test freezes both raw fixture digests and the exact rendered plain-text packet digests. `render_scenario_packet` in `tests/core/test_epistemic_review_utility.py` is the packet renderer and its UTF-8 output bytes are the prompt payload; no hand-edited paraphrase is allowed. The same test freezes the answer-key and scorecard-template digests using canonical JSON (`ensure_ascii=False`, sorted keys, compact separators). Its scenario vectors bind selected IDs, excluded IDs, scope-completeness override, exact ordered expected finding kinds/evidence IDs, outcome, and reason. Record each fixture's source revision, selected IDs, canonical comparison digest, proposal digest, and receipt fields in the private result checkpoint. Fixture-byte digest remains distinct from selected scope and canonical comparison digest.

| Scenario | Fixture and selected scope | Question under review |
| --- | --- | --- |
| Direct claim / hypothesis separation | `claim-hypothesis-gap.json`; select only `claim-1` and `hypothesis-1`; exclude `requirement-1`; override `scope_complete=False` and `requirement_ids=()`. | Can each lane distinguish explicitly declared source claim from unverified hypothesis without claiming either is true or using excluded content? |
| Possible contradiction | `possible-contradiction.json`; select both claims. | Can each lane identify the reciprocal declared incompatibility, cite both IDs, and keep it a possible comparison result rather than a truth verdict? |
| Verification gap | `claim-hypothesis-gap.json`; select claim, hypothesis, and requirement. | Can each lane identify the requirement with no selected evidence and say that evidence is not established in this scope, not absent globally? |

Every lane receives the same selected IDs, item IDs, exact text, declared kinds, evidence references, comparison metadata, and scope-completeness declaration, including the direct scenario's explicit incomplete-scope override. The structured lane receives the fixture through the existing strict test decoder and pure core. Its scorer artifact is exactly the complete `ReviewProposal` serialized by `render_structured_artifact` as UTF-8 canonical JSON: schema version, full selected-scope fields, outcome/reason, source revision and digests, and each finding's kind, evidence IDs, selected scope, rationale, and confidence label. The three exact structured-artifact digests are asserted in the focused test. Plain lanes receive the exact deterministic text-only packet bytes produced by the frozen renderer from those same fields; they receive no proposal, rationale output, expected answer, score, hidden gold, or structured-output schema. Excluded items are not included in the scenario packet. The raw fixture digest still binds the exact full fixture bytes used by the core. Fixture, plain-packet, structured-artifact, answer-key, prompt-template, and scorecard-template digests are asserted in the focused deterministic test and must be copied verbatim to the entry-review checkpoint.

## 2. Comparison lanes and fixed prompts

There are exactly three lanes and one attempt per planned model response. No retries, answer-shopping, prompt changes, tool use, web lookup, source inspection, or external data are permitted. If a required response is unavailable, malformed, or timed out, that lane and the experiment are `BLOCKED`; do not replace or omit it.

### A. Structured core

Run `_review_synthetic_scope` twice for each scenario from the same decoded input and exact fixture bytes. Retain both complete in-memory outputs locally. The two runs must have identical proposal and receipt values, including digests. These repeats test deterministic execution only; they do not measure comparative utility.

### B. Agent-mediated plain review

Use a fresh delegated analyst and a separate fresh delegated verifier, both GPT-6 Luna High, once per scenario. Start each with `collaboration.spawn_agent` and `fork_turns:"none"`; include only the exact fixed prompt and packet (the verifier also receives that scenario's analyst draft). Do not pass this protocol, answer key, rubric score, structured output, or repository context. The delegate must not call tools or inspect files. Inspect its complete turn/tool transcript before accepting the output; any tool call, missing transcript, or evidence of outside context makes that lane and the experiment `BLOCKED`. The platform does not technically disable tools for these delegates, so this audited no-tool condition is mandatory, not an assumed sandbox guarantee.

Analyst prompt template, UTF-8 SHA-256 `4dd2e39424c82342cf3fb0cd5cf86ee7345a16cab0594c00dbd00648636bdbec`; replace `{packet}` only with exact rendered packet text:

> Review only the synthetic note packet below. In normal prose, explain what the packet explicitly states, whether it presents a possible issue or missing evidence, which item IDs support your explanation, and what remains unknown or outside the selected scope. Do not infer truth, use excluded notes, or use outside information. Do not output JSON or claim that a possible conflict proves either value true. Packet: {packet}

Verifier prompt template, UTF-8 SHA-256 `43e9d4c3329f7b5c6fc499e7a54d239576fc9c647e479a7e44f0afc665946e75`; substitute exact rendered packet and that scenario's raw analyst draft. Record the instantiated verifier-prompt digest:

> Audit the draft against only the supplied synthetic note packet. Correct unsupported claims, missing or incorrect item IDs, scope errors, missing rationale, and any loss of uncertainty. Return one corrected plain-language answer. Do not use outside information, infer truth, add facts, or output JSON. Packet: {packet} Draft: {draft}

The verifier's final answer is the lane artifact. Preserve analyst and verifier outputs separately in the private checkpoint; record their exact model/effort, invocation date, prompt digest, packet digest, output digests, and reviewer. Delegation consumes normal model usage; no cost-free, offline, or reproducible-model claim is allowed.

### C. One-shot plain AI comparator

Use one fresh GPT-6 Luna High invocation per scenario, with no delegated verifier and no repository context beyond the packet. Start a fresh agent with `fork_turns:"none"`, send only the fixed prompt and exact packet, and inspect its complete transcript. The same no-tool/no-file-read condition applies; if it cannot be audited, mark the experiment `BLOCKED` rather than treating isolation as proven.

Prompt template, UTF-8 SHA-256 `548e2b4c501031c11f4d75bd976754557af21b454c98e87feb324575e44e9b7e`; replace `{packet}` only with exact rendered packet text:

> Read the synthetic note packet and tell me, in normal prose, what seems explicitly stated, what may need attention, which item IDs support that view, and what cannot be concluded from the selected material. Use only this packet. Do not infer truth, use excluded notes, or use outside information. Do not output JSON. Packet: {packet}

Record exact model/effort, invocation date, prompt digest, packet digest, output digest, and reviewer. The model output is an observed artifact, not a deterministic expected value.

## 3. Frozen traceability rubric and decision rule

Before any comparator call, bind the answer key for the three fixed scenarios to the selected fixture bytes. The exact key is the `ANSWER_KEY` object in the focused test, with canonical JSON SHA-256 `c3c94758fedf3d8c5fbe7b24973d82e4962b9ee84e3b75b987901b02dce2b4d5`. It lists, per scenario, selected/excluded IDs, completeness declaration, exact expected finding-kind/evidence-ID sequence, outcome, and reason. The immutable scorecard template has canonical JSON SHA-256 `e3ef6109e012be59c23bf6c3981decef493d457f7bb3b9a911ed3ab20b5e171f`; each card records scenario ID, explicit lane ID (`structured_core`, `agent_mediated_plain`, or `one_shot_plain`), four exact Boolean criteria, and critical-defect flag. The scorer is unblinded; do not claim masking or blinding. Score each frozen artifact independently for each scenario, 0 or 1 per criterion (maximum 4):

1. **Evidence linkage:** cites the exact supporting selected item IDs and does not cite an excluded or unrelated item.
2. **Scope fidelity:** stays within the selected IDs and names the selected-scope limit where it affects the conclusion.
3. **Rationale traceability:** explains why the classification, possible conflict, or gap appears using the declared kind, evidence references, or comparison metadata; a bare label is insufficient.
4. **Uncertainty:** preserves “possible,” “unverified,” “not established in selected scope,” or equivalent meaning and makes no truth/global-absence claim.

Any unsupported truth verdict or global claim is a critical defect and forces `NO_GO`, regardless of points. The scoring is explicitly unblinded and the lane identity is part of each card. The key binds to fixture evidence, not a model preference. GPT-6 Sol independently reviews the frozen input, packet and structured artifacts, answer key, prompt/scorecard templates, and completed scorecards. Corrections require recording the original and a reasoned audit trail; never alter the rubric after seeing results.

The result is:

- **`PASS` (synthetic utility proxy only):** all three core repeats match exactly; all reviewer answer checks are correct; no critical defect occurs; structured output scores at least 3/4 in every scenario and at least 10/12 overall; and its total is at least 2 points above each baseline lane.
- **`NO_GO`:** experiment is complete, but any core repeat differs, reviewer answer is incorrect, critical defect occurs, structured score misses a threshold, or structured output lacks the required margin over either baseline. Preserve result; do not widen or extract the feature to hide a negative result.
- **`BLOCKED`:** any required input, lane, exact artifact, independent scoring review, or frozen prerequisite is unavailable or invalid. No substitute, partial pass, or utility claim.

Elapsed model time, corrections, token use, and traceability defects may be recorded as observations. They do not count as human time saved, productivity, speed, or user benefit. Unit tests and model-reviewer agreement alone cannot produce `PASS`.

## 4. Test and execution boundary

`tests/core/test_epistemic_review_utility.py` validates only deterministic repeat behavior on the exact three fixture scenarios and the predeclared scoring vectors/threshold mechanics. Tests make no model calls, contain no generated comparator output, and do not assert subjective usefulness. Full experiment artifacts and raw model responses stay in the untracked local Block 3 checkpoint; only digests and bounded verdict summaries may be considered for public reporting after review.

Execution sequence:

1. Freeze protocol hash, selected base/head, test hash, fixture hashes, all three exact packet hashes, answer-key hash, scorecard-template hash, prompts/version, and selected-scope overrides in the private Block 3 checkpoint.
2. Sol reviews those exact artifacts for fairness, source equality, scoring, enforceable/auditable isolation, and hidden answer leakage. Any changed artifact invalidates the review and requires new hashes and another review.
3. Astra issues execution ENTRY GO on the complete exact-hash set. Until then, do not call comparator agents or score any output.
4. Run the exact fixed attempts once; save private raw artifacts and digest ledger; score with the explicit lane IDs under the predeclared unblinded rubric; ask Sol to review the completed evidence.
5. Run the full R1 validation family and `rtk git diff --check`; record `PASS`, `NO_GO`, or `BLOCKED` without changing the predeclared rule.
6. Astra decides the terminal Block 3 exit. `PASS` admits only the next plan-named design/admission decision; it does not authorize application code, real-graph evaluation, release, or user-utility claims.

## 5. Explicit limitations and stop rules

These metadata-rich synthetic examples may make the task artificially easy. All lanes receive the same selected source information, but the structured lane is expressly testing deterministic use of declared structure; a tie is `NO_GO`, not evidence to relax the rubric. Results generalize only to these three exact fixture scenarios and source revision.

Stop if any lane requires private graph data, a real user, direct network/provider integration or API use, a product runtime dependency, new dependency, persistence, UI, write/apply behavior, truth certification, or a changed source profile. Codex-hosted research delegation described in §2 is allowed and is not a product runtime integration. Record any other blocker; do not widen Block 3. Preserve PolyForm Noncommercial 1.0.0 and the hold on external copyright-bearing contributions absent a lawyer-reviewed contributor agreement or equivalent grant.
