# Epistemic Review — First Tranche

Status: Block 1 vocabulary is merged in PR #22. Block 2 is merged in PR #23 at `eca93f19398972ede50127ce6aaa93d78fb5d5cd`; exact PR checks and merged-main Python contracts and Foundation CI passed. This evidence establishes only the private synthetic review core. Block 3 comparative utility evaluation remains pending. This document establishes no operational graph runtime, public stable contract, consumer adapter, real-graph support, user-utility result, or release support.

## Selected synthetic-note use case

Given repository-owned synthetic fixture values, the merged private deterministic core returns explicitly declared source-claim, hypothesis, possible-contradiction, and verification-gap findings with evidence, rationale, selected scope, and partial or unknown state. The initial exit review was `BLOCKED`; bounded repairs were then reviewed to Sol `PASS` and Astra technical exit `GO` for the exact candidate merged in PR #23. This remains synthetic implementation evidence, not comparative utility or user validation. Results do not turn a partial selection into a global conclusion or certify truth. Exact input, comparison, digest, rejection, and receipt semantics are recorded in the [Block 2 specification](2026-09-26-synthetic-review-block2.md).

The first deliverable accepts fixture-only input supplied by tests. It does not read a graph, call Plumber or Parser, render a UI/editor/application, apply or write changes, persist a decision, access a database, use a network, or publish a stable contract.

## Vocabulary and evidence boundary

- **Source claim:** text explicitly present in the selected synthetic item; not a claim that the text is true outside that item.
- **Hypothesis:** an explicitly unverified candidate interpretation.
- **Possible contradiction:** selected claims that conflict under declared comparison rules; not proof that either source is wrong.
- **Verification gap:** required evidence absent for the selected scope; not evidence of absence or a global gap.

Every finding records evidence, rationale, and scope. Results expose partial and unknown states when selection or evidence is incomplete. Review acknowledgement is session-local and has no apply, write, persistence, graph, editor, database, or truth effect.

## Explicit exclusions

This tranche excludes graph access, Plumber, Parser, UI, editor, application shell, apply, write, persistence, network, database access, and any truth engine. It excludes real user graphs, host support, operational graph/application runtime, distribution, performance, and public stable support claims. No external source, private material, copied contract, LENS asset, or third-party fixture is admitted.

## Deferred dependencies and admission gates

Future text-backed work is conditional on owner-published and qualified Plumber payload evidence. The roadmap tracks Plumber #582, #491, and #493, Parser #213, and Matryca-per-Delineat #430 as external/deferred dependencies; this note claims no ownership, completion, or consumer readiness for any of them.

ADR-0007 resolves the semantic profile policy: the planned Trama consumer requires both `plumber.graph.read/v1` and `plumber.graph.topology/v1`; text/property-backed analysis additionally requires `plumber.graph.payload.read/v1`. This policy does not establish released capabilities or runtime support. Admission remains pending exact owner-published schemas, fixtures/TCK, provenance, compatibility, and mode-specific evidence: OG must bind the Parser-backed source mode and supported Parser/Logseq ranges; DB must bind a qualified official host and supported versions. OG and DB remain independent, and no consumer is admitted by this tranche.

Repository-owned material remains under PolyForm Noncommercial 1.0.0. The contributor-rights gate and lawyer-reviewed agreement/equivalent grant remain preserved; no external copyright-bearing material is merged by this tranche.
