# ADR-0007: Plumber Capability Admission by User-Facing Claim

Status: Accepted

Date: 2026-09-26

Owner: Marco Porcellato

Supersedes: None

Superseded by: None

## Context

Trama's Plumber source-admission record requires the released
`plumber.graph.read/v1` and `plumber.graph.topology/v1` profiles before the
planned consumer adapter can start. The profiles serve distinct purposes:
identity and session binding versus complete, content-free graph relationships.
Neither provides page or block text for evidence-backed review.

Plumber accepted an additive payload decision in [PR #590](https://github.com/MarcoPorcellato/matryca-plumber/pull/590), merged at
`233731cde79ceb2e26da91b935ad5a4dfd02c85c`. Its
[`plumber.graph.payload.read/v1` decision](https://github.com/MarcoPorcellato/matryca-plumber/blob/233731cde79ceb2e26da91b935ad5a4dfd02c85c/docs/decisions/2026-09-12-plumber-graph-payload-read-v1.md)
defines a separate future family for bounded page and complete-subtree text
and typed properties. It deliberately leaves `graph.read` content-free. The
decision is documentation-only: it adds no schema, fixture/TCK, released
artifact, runtime route, qualified host, or DB support.

Without a capability-specific rule, Trama could either mistake topology for
text evidence or silently omit a contract needed for the user-facing analysis
it intends to provide.

## Decision

Trama distinguishes the evidence required by each user-facing capability:

| Capability | Required Plumber profiles | Maximum claim after separate qualification |
| --- | --- | --- |
| Identity and session status | `plumber.graph.read/v1` | Bound graph, source, session, and revision identity only. |
| Graph navigation | `plumber.graph.read/v1` + `plumber.graph.topology/v1` | Complete, bounded, content-free relationships. |
| Scoped page or subtree text analysis | `plumber.graph.read/v1` + `plumber.graph.payload.read/v1` | Review of qualified complete text and declared properties in the requested scope. |
| Graph navigation with text-backed intelligence | All three profiles | The separately qualified navigation and text-analysis claims, combined only when owner-defined compatibility and graph/session/revision bindings agree. |

These rows describe semantic prerequisites, not current admission. The planned
Trama consumer implementation gate remains unchanged: released `graph.read`
and `graph.topology` artifacts are both required before the adapter work
starts. The current programme does not authorize a consumer using only one of
those two floor profiles. Any Trama feature that reads graph text or
properties additionally requires the released and separately qualified
`graph.payload.read` profile; it cannot infer content from topology.

Plumber's profiles remain orthogonal and owner-defined. `graph.read` supplies
identity/session vocabulary, topology supplies no page text or epistemic
evidence, and payload supplies no graph-wide topology. Trama neither copies
nor redefines their schemas, wire semantics, fixtures, or TCKs.

OG and DB admission are independent. OG evidence must bind Plumber's
Parser-backed source mode and its supported Parser/Logseq ranges. DB evidence
must bind a qualified official Logseq host and its supported versions. One
mode never inherits support from the other. Multiple profiles may be combined
only when their published compatibility rules and exact graph, session, and
source-revision bindings permit it.

An accepted ADR, source checkout, commit hash, open issue, or prerelease label
does not satisfy artifact publication or runtime qualification. Missing
schemas, fixtures/TCKs, provenance, compatibility matrices, or mode-specific
evidence keep the corresponding capability blocked.

## Alternatives considered

- **Put text into `graph.topology` or `graph.read`:** rejected because the
  accepted Plumber contracts keep topology content-free and the payload
  decision is explicitly additive. Trama must not widen owner semantics.
- **Start a consumer with only one of the existing read/topology floor
  profiles:** rejected because the planned adapter requires both identity and
  complete relationships. A separate reduced-profile product slice has not
  been admitted.
- **Treat the payload decision as a released capability:** rejected because
  PR #590 is documentation-only and supplies no distributable artifact,
  runtime, or host qualification.
- **Require all three profiles for every capability:** rejected because
  identity status and content-free graph navigation do not consume page or
  block text; the required profile set should match the claim, without
  weakening the combined navigation-and-intelligence claim.

## Consequences

This is a Trama-only documentation decision. It introduces no runtime feature,
dependency, schema, adapter, fixture, UI, host access, DB capability, release,
or user-graph claim. It clarifies the existing source-admission floor and the
additional requirement for text-backed analysis without weakening any gate.

The accepted product flow remains:

```text
OG Markdown -> Parser -> Plumber -> Trama / Brain
Logseq DB official host -> Plumber -> Trama / Brain
```

Trama remains read-only and unaware of Parser, Logseq source selection, and
host implementations. OG Markdown and native Logseq DB remain authoritative
for their respective modes. No silent fallback or cross-mode claim is added.

Repository-owned material remains under PolyForm Noncommercial 1.0.0. No
commercial permission is implied. External copyright-bearing contributions
remain merge-blocked until a lawyer-reviewed contributor agreement or
equivalent grant exists.

## Reversal

A change to capability composition requires a new Trama ADR tied to the exact
Plumber owner contracts and a user-facing claim. It must retain separate
source-mode qualification, fail-closed profile coherence, native source
authority, no-write behavior, the PolyForm Noncommercial boundary, and the
contributor-rights gate.
