# Matryca Trama Claim Ledger

This ledger records current capability claims under the
[delivery program](../specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md). It is not a
release-support matrix. Every entry must retain its exact scope, revision,
evidence, and limitations.

## Observed published baseline — 2026-10-25

- Published main: `d21f2adb2101ce5fae222f6235925c1d66ece126`, tree
  `2b2e11c5937f350139e6ee46b2dde13a750a609b`.
- Current narrow claims are recorded in the dated `PM-*` entries below. Admission,
  source implementation, specialized qualification, main CI and exploratory
  observations are distinct; none implies a Trama product release.
- Mutable state must be reverified before a later action. This documentation
  candidate is not itself a newly qualified runtime revision.

## Historical anchors and claims

- Repository head observed during planning: `9905e8a36acb83a17a33b702a5fa620d6bfed185`.
- Qualified baseline: `862c5c89157f28c1985cde6145fc2c8af04a70b4`.
- Baseline evidence:
  [`862c5c89157f28c1985cde6145fc2c8af04a70b4.md`](../spikes/evidence/python-read-contract-v1/862c5c89157f28c1985cde6145fc2c8af04a70b4.md).
- These anchors are historical observations. Reverify live state before using
  them for delivery.

- V0 anchor audit: candidate `2de8069ce450daa3b2f7ca591d09d73a951150f4`,
  tree `7104e1bdf4a272a31128d01adb13bd3fc1e8d4e7`; remote-tracking `origin/main`
  `9905e8a36acb83a17a33b702a5fa620d6bfed185`; baseline tree
  `f1dacc9b30c993b2b69a48c20e73281732e781b3`. See
  [the sanitized receipt](receipts/2026-09-05-v0-anchor-audit.md). Initial
  sandbox fetch was blocked; the coordinator subsequently refreshed remote state
  with one elevated fetch (exit 0). Current-head qualification was blocked at
  that audit; later exact-head evidence is recorded separately below.

## Claims

| Claim ID | Class | Claim and scope | Qualified revision | Evidence | Limitations / next action |
|---|---|---|---|---|---|
| `ER-TRANCHE-001` | Planned | A synthetic selected-note review can classify source claims, hypotheses, possible contradictions, and verification gaps while retaining evidence, rationale, scope, partial, and unknown state. | None. | [First-tranche spec](../specs/2026-09-19-epistemic-review-first-tranche.md). | Historical plan wording: fixture-only input; no graph, Plumber, Parser, UI, editor, apply, write, persistence, network, database, runtime, truth, or stable public-contract evidence. |
| `ER-TRANCHE-002` | Unsupported | Real-graph, Plumber-consumer, Parser, UI/editor, application, persistence, network, database, truth-engine, and public stable-support claims. | None. | None. | Excluded by first-tranche scope; later gates require fresh evidence and separate authorization. |
| `ER-TRANCHE-003` | Planned | External/deferred dependency tracking for Plumber #582/#491/#493, Parser #213, and Matryca-per-Delineat #430. | None. | [Roadmap](../ROADMAP.md). | References do not assign ownership, prove completion, or establish consumer readiness. |
| `ER-TRANCHE-004` | Planned | Later-gate topology requirement remains unresolved: current source admission requires topology with `graph.read`, while the execution plan makes topology optional after payload qualification. | None. | First-tranche spec and [source-admission record](../contracts/PLUMBER_SOURCE_ADMISSION.md). | Historical planning discrepancy wording; no consumer readiness claim. See current reconciliation entry below. |
| `ER-TRANCHE-005` | Planned | The source-admission record requires `plumber.graph.read/v1` with `plumber.graph.topology/v1`. Plumber separately documents `plumber.graph.payload.read/v1`; this does not establish a released Trama text consumer. Content-free topology cannot supply page/block text. | None. | [First-tranche spec](../specs/2026-09-19-epistemic-review-first-tranche.md), [source-admission record](../contracts/PLUMBER_SOURCE_ADMISSION.md), [Plumber issue #491](https://github.com/MarcoPorcellato/matryca-plumber/issues/491), [Plumber PR #590](https://github.com/MarcoPorcellato/matryca-plumber/pull/590), and [Block 2 synthetic review specification](../specs/2026-09-26-synthetic-review-block2.md). | Later admission must reconcile required capabilities against exact published owner artifacts. No consumer is admitted here. |
| `ER-TRANCHE-006` | Planned | A private synthetic review core was proposed to return a deterministic proposal and in-memory receipt from explicitly classified fixture values. | None. | [Block 2 synthetic review specification](../specs/2026-09-26-synthetic-review-block2.md). | Historical pre-entry planning snapshot, superseded by ER-TRANCHE-007. It does not claim a graph runtime, source consumer, truth, persistence, UI, or release capability. |
| `ER-TRANCHE-007` | Candidate | A private deterministic core candidate returns a proposal and in-memory receipt for explicitly classified repository-owned synthetic values. | Historical candidate `9eb13d5352a4d32905a214457a76925006d1bb5e`; its successor merged as PR #23 at `eca93f19398972ede50127ce6aaa93d78fb5d5cd`. | [Block 2 specification](../specs/2026-09-26-synthetic-review-block2.md) and candidate-branch source/test evidence. | Historical candidate claim retained as recorded at entry; current merged implementation state is recorded separately in ER-TRANCHE-008. No operational graph runtime, real-source consumer, truth, persistence, UI, release, performance, or user-utility claim. PolyForm Noncommercial and the contributor-rights gate remain in force. |
| `ER-TRANCHE-008` | Implemented | The private deterministic core returns a proposal and in-memory receipt for explicitly classified repository-owned synthetic values. | PR #23 merged at `eca93f19398972ede50127ce6aaa93d78fb5d5cd`; exact PR checks and merged-main Python contracts/Foundation CI passed. | [Block 2 specification](../specs/2026-09-26-synthetic-review-block2.md), `_epistemic_review.py`, focused tests, and PR/main check results. | Implemented only for the repository-owned synthetic fixtures and private pure core. Does not establish an operational graph runtime, real-source consumer, truth, persistence, UI, release, performance, user utility, or product support. PolyForm Noncommercial and the contributor-rights gate remain in force. |
| `ER-TRANCHE-009` | Documented | Identity/session, graph navigation, and text-backed analysis have distinct Plumber profile prerequisites; profile composition never qualifies itself or crosses OG/DB modes. | None. | [ADR-0007](../decisions/ADR-0007-PLUMBER-CAPABILITY-ADMISSION.md), bound to Plumber PR #590 merge `233731cde79ceb2e26da91b935ad5a4dfd02c85c`. | No released payload profile, consumer adapter, host, or graph capability is admitted. The existing planned implementation gate remains read + topology; text use also requires payload. |
| `V0-FOUNDATION-001` | Documented | Public source-available foundation, PolyForm Noncommercial boundary, governance, and fork-safe policy checks exist. | Not assigned by this ledger. | Foundation specification and repository policy files. | Reverify mutable GitHub settings and exact-head checks. |
| `V0-SOURCE-001` | Implemented | `9905e8a` contains bounded Python contracts, core, Parser bridge, Plumber bridge, and synthetic OG adapter source. | None. | Repository tree at `9905e8a`. | Implementation is not current-head qualification or publication. |
| `V1-BASELINE-001` | Qualified baseline | Synthetic OG fixtures cover `graph.identify`, `page.read`, and complete ordered `block.subtree.read.complete`. | `862c5c89157f28c1985cde6145fc2c8af04a70b4` | Baseline evidence record linked above. | No user graph, host, DB, write, event, Shadow, sync, export, recovery, UI, performance, distribution, or network claim. |
| `V1-CURRENT-001` | Blocked | Qualify one exact current head with locked local and hosted evidence. | None. | No current-head evidence record. | Complete V0 reconciliation, then execute the V1 plan. |
| `V1-PR-001` | Qualified PR evidence | Synthetic OG fixtures only: `graph.identify`, `page.read`, and complete ordered `block.subtree.read.complete`. | `49aae4f21b1f466604f74a4d1d66b5cdc02933d4` | [Hosted PR-head evidence](../spikes/evidence/python-read-contract-v1/49aae4f21b1f466604f74a4d1d66b5cdc02933d4.md) | PR evidence; not merged-main or release support. Unsupported profiles remain excluded. |
| `V1-CURRENT-002` | Qualified current head | Synthetic OG fixtures only: `graph.identify`, `page.read`, and complete ordered `block.subtree.read.complete`. | `a3411df1989095abdea708526843bfcfe10b9c49` | [Main reconciliation receipt](receipts/2026-09-05-v1-main-reconciliation.md) | Dependency Review is PR-scoped; identical trees corroborate provenance only. No user vault, host, DB, write, event, sync, export, recovery, UI, performance, distribution, or release claim. |
| `V2-CONTRACT-001` | Implemented | Bounded `trama.logseq.read/v1` source and rejection tests exist. | None. | Repository tree at `9905e8a`; baseline evidence covers only the bounded slice. | Contract is not frozen or published. |
| `V3-PARSER-001` | Blocked | Qualify exact public Parser versions and package-root symbols. | None. | Candidate profile only. | Requires V1 and V2 plus cross-repository evidence. |
| `V4-PLUMBER-001` | Blocked | Qualify Trama consumption of a released public Plumber profile. | None. | Historical synthetic Trama helper tests only. | Requires the canonical Plumber artifact, immutable public profile, and exact Trama, Parser, and Plumber revisions. |
| `V5-OG-001` | Unsupported | Operational OG support beyond public synthetic fixtures. | None. | None. | Requires sanitized fixture classes and containment evidence; private vaults are forbidden. |
| `V6-DB-001` | Blocked | Official-host, read-only Logseq DB profile. | None. | PR #14 is a mutable proposal, not evidence. | Requires accepted host decision and exact-version read-only evidence. |
| `V7-NODI-001` | Unsupported | Nodi runtime and accessible UI. | None. | Design direction only. | Requires qualified data profile, state contract, and WCAG 2.2 AA evidence. |
| `V8-AGENT-001` | Unsupported | Agent and plugin execution surface. | None. | Safety requirements only. | Requires default-deny capability model and adversarial evaluation corpus. |
| `V9-DIST-001` | Unsupported | Reproducible Community artifacts. | None. | None. | Requires qualified runtime, SBOM, provenance, artifact inspection, and rehearsal. |
| `V10-RELEASE-001` | Blocked | Public Community release. | None. | None. | Requires V0–V9 evidence and separate maintainer authorization. |

### Restricted producer/client records — 2026-10-25

The preceding IDs retain their historical wording and evidence. These additions
record later facts without rewriting old receipts. **Product-M1** remains the
incomplete epistemic utility/presentation tranche; **Producer-M1/M2/M3** refer
only to the later synthetic producer/client/exploration sequence.

| Claim ID | Class | Claim and scope | Qualified revision | Evidence | Limitations / next action |
|---|---|---|---|---|---|
| `PM-ADMISSION-001` | Documented | The owner admitted jointly `plumber.graph.read/v1` and `plumber.graph.topology/v1` for the exact original Plumber `2.1.0a3` capsule. | Original producer `8c30f70e217722e719c5aedc322219ebccb87e68`; original wheel SHA-256 `e5bc586a3da76d8e11760b39c9d7ac45b62b1240f085a8a96a573b9902bfea12`. | [Owner decision](https://github.com/MarcoPorcellato/matryca-trama/issues/2#issuecomment-6383824647) and [source-admission record](../contracts/PLUMBER_SOURCE_ADMISSION.md#current-owner-admission--2026-10-24). | Exact hash-locked closure with Parser `1.9.0`, CPython `3.12.14`, Linux x86_64/macOS arm64 and authenticated disposable synthetic fixture only. Packaged `proposed`, `static-only-unqualified`, `unqualified` and `planned` labels remain unchanged. No stable, real-graph, payload, DB or OS-isolation admission. |
| `PM-M1-RECORD-001` | Documented | Producer-M1 qualification and subsequent owner admission are separate recorded events. | Original producer above; immutable evidence refs retained in the source-admission record. | [Source-admission record](../contracts/PLUMBER_SOURCE_ADMISSION.md). | The original pre-admission “consumer NOT ADMITTED” receipt remains valid for its earlier decision point. This audit did not independently rehash original runtime artifacts. |
| `PM-M2-SOURCE-001` | Implemented | Content-free `KnowledgeGraphGateway` domain port, immutable graph values and restricted `PlumberClientAdapter` outer client. | Source merged as `28e9b5dfb350c7fe875a91c2a630162d7da36582`; present at the observed main. | [PR #33](https://github.com/MarcoPorcellato/matryca-trama/pull/33), `packages/core` and `packages/plumber-client`. | Core and standard-library imports; separately provisioned producer and trusted synthetic handle only. No arbitrary roots, in-process Parser/Plumber import, app, stable API, payload or real graph. |
| `PM-M2-RECORD-001` | Documented | Successful specialized Producer-M2 synthetic qualification is recorded on its exact exercised head. | `a4463638baaca846fe731556417f1d2d660838f1`; PR-head/merge tree `6c6fc59abb2f1d2f46f85d03374b6d5f4d31cbdf`. | [Run 40112844731, attempt 2](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/40112844731/attempts/2). | Complete only for the admitted capsule. Tree equivalence is provenance evidence, not execution on another commit. Original artifacts were not downloaded or independently rehashed in this reconciliation; no new runtime attempt or current-candidate qualification. |
| `PM-MAIN-CI-001` | Documented | Foundation and Python contracts checks succeeded on the observed published main. | `d21f2adb2101ce5fae222f6235925c1d66ece126`. | [Foundation](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/40148195978), [Python contracts](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/40148195966). | Exact-main checks only; no substitution for specialized qualification, branch protection, release, user utility or supported host evidence. |
| `PM-M3-RECORD-001` | Documented | One successful exploratory macOS run and its bounded observations/cleanup were reported. | `d21f2adb2101ce5fae222f6235925c1d66ece126`. | [Run 40148317931, attempt 1](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/40148317931/attempts/1), [PR #34](https://github.com/MarcoPorcellato/matryca-trama/pull/34). | Consumed non-qualifying attempt. Public metadata and owner report were checked; original artifacts were not independently downloaded/rehashed. No supported OS isolation, comparator admission, MA completion, performance or real-data support. |

## Resolution note — 2026-09-26

`ER-TRANCHE-004` and `ER-TRANCHE-005` preserve the planning and source-admission
claims as they were recorded before capability-specific reconciliation. The
discrepancy in ER-TRANCHE-004 is resolved by [ER-TRANCHE-009](#claims) and
[ADR-0007](../decisions/ADR-0007-PLUMBER-CAPABILITY-ADMISSION.md): the planned
adapter floor remains `graph.read` plus `graph.topology`, while any
text/property-backed capability also requires the additive payload profile.
This does not admit a released profile or runtime consumer.

## Resolution note — 2026-10-25

The September resolution and `ER-TRANCHE-009` describe the earlier state.
`PM-ADMISSION-001` and the M2 records supersede only their implication that no
synthetic Plumber consumer has subsequently been admitted or implemented.
`V4-PLUMBER-001` remains blocked for the broader consumer qualification; the
synthetic exception is not its full exit. Stable mode-specific released
artifacts, schemas/TCK, provenance, compatibility and independent qualification
remain required for broader OG or DB support. Payload is additionally required
for titles, text and properties; topology supplies none of them. Plumber remains
the sole gateway, including for Brain; the admitted Trama client does not import
Parser. The retained historical Parser bridge remains experimental evidence.

Block 3 comparator utility remains blocked independently of the OG roadmap.
Producer-M3 and separate maintainer-local tooling do not satisfy it. User-facing
UI, real-graph operation, distribution and release remain unproved. PolyForm
Noncommercial and the lawyer-reviewed contributor-agreement gate are unchanged.

## Update rule

Never overwrite a historical claim to make it appear current. Add or revise an
entry only after recording the exact qualified revision, evidence revision,
subject digest where relevant, commands, platforms, results, limitations, and
authority. Negative and unsupported outcomes remain first-class evidence.
