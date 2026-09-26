# Epistemic Review — First Tranche

Status: planned documentation surface only. This note does not authorize runtime implementation, a public contract, a consumer adapter, release, or external mutation.

## Selected synthetic-note use case

Given one repository-owned fixture containing a selected set of synthetic notes, a read-only review shows why each candidate finding was produced: a source claim, an unverified hypothesis, a possible contradiction between selected claims, or a verification gap caused by missing evidence. Results retain evidence references, rationale, selected scope, and partial or unknown state. They do not turn a partial selection into a global conclusion or certify truth.

The first deliverable accepts fixture-only input supplied by tests. It does not read a graph, call Plumber or Parser, render a UI/editor/application, apply or write changes, persist a decision, access a database, use a network, or publish a stable contract.

## Vocabulary and evidence boundary

- **Source claim:** text explicitly present in the selected synthetic item; not a claim that the text is true outside that item.
- **Hypothesis:** an explicitly unverified candidate interpretation.
- **Possible contradiction:** selected claims that conflict under declared comparison rules; not proof that either source is wrong.
- **Verification gap:** required evidence absent for the selected scope; not evidence of absence or a global gap.

Every finding records evidence, rationale, and scope. Results expose partial and unknown states when selection or evidence is incomplete. Review acknowledgement is session-local and has no apply, write, persistence, graph, editor, database, or truth effect.

## Explicit exclusions

This tranche excludes graph access, Plumber, Parser, UI, editor, application shell, apply, write, persistence, network, database access, and any truth engine. It excludes real user graphs, host support, runtime, distribution, performance, and public stable support claims. No external source, private material, copied contract, LENS asset, or third-party fixture is admitted.

## Deferred dependencies and unresolved divergence

Future work is conditional on owner-published and qualified Plumber payload evidence. The roadmap tracks Plumber #582, #491, and #493, Parser #213, and Matryca-per-Delineat #430 as external/deferred dependencies; this note claims no ownership, completion, or consumer readiness for any of them.

An unresolved later-gate divergence is recorded deliberately: the current source-admission record requires topology together with `graph.read`, while the execution plan makes topology optional enrichment after payload qualification. This tranche does not reconcile the two positions and does not claim readiness for a consumer. The owning later gate must resolve the discrepancy with fresh, exact evidence.

Repository-owned material remains under PolyForm Noncommercial 1.0.0. The contributor-rights gate and lawyer-reviewed agreement/equivalent grant remain preserved; no external copyright-bearing material is merged by this tranche.
