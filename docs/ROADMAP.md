# Matryca Trama Roadmap

The accepted [Plumber gateway adoption](decisions/ADR-0006-PLUMBER-GATEWAY-ADOPTION.md)
sets the future ownership direction: Trama and Brain consume only published
Plumber public contracts and remain unaware of Parser and source adapters. The
[cross-repository contract roadmap](superpowers/specs/2026-09-05-cross-repository-contract-roadmap.md)
remains a migration plan; no canonical contract artifact or consumer profile is
published by this decision.

## Current verified baseline

The resolved `origin/main` merge parent is
`70fc14c27b11e31e8f557fd70684b6a83933e7d6`; it retains
the historical experimental `trama.logseq.read/v1` source for owned synthetic
OG fixtures. Hosted evidence at `862c5c89157f28c1985cde6145fc2c8af04a70b4`
qualifies only its baseline profile:

- `graph.identify`;
- `page.read`;
- complete ordered `block.subtree.read.complete`.

User graphs, Logseq DB, writes, events, DB-source Shadow, synchronization,
export, recovery, app/UI/Nodi, distribution, performance, and network behavior
remain unsupported by that evidence. The experimental contract is historical
evidence only; a future consumer requires the separate Plumber contract and
profile gates.

## Delivery rule

Only one cross-repository mutating slice is active at a time. The owning
contract merges before a dependent consumer branch starts. Every repository
uses its own short-lived branch and PR; no long-lived integration branch or
multi-repository PR is allowed.

Disjoint read-only research and non-overlapping documentation may run in
parallel. Runtime, schema, adapter, session, authority, and product changes
remain sequential.

### First epistemic-review tranche — planned

The first tranche is a fixture-only, read-only synthetic-note review surface. It distinguishes source claims, hypotheses, possible contradictions, and verification gaps while retaining evidence, rationale, selected scope, and partial/unknown state. It excludes graph access, Plumber, Parser, UI/editor, application shell, apply/write, persistence, network, database, and truth claims. See [the tranche specification](specs/2026-09-19-epistemic-review-first-tranche.md).

External/deferred references are Plumber [#582](https://github.com/MarcoPorcellato/matryca-plumber/issues/582), [#491](https://github.com/MarcoPorcellato/matryca-plumber/issues/491), and [#493](https://github.com/MarcoPorcellato/matryca-plumber/issues/493), Parser [#213](https://github.com/MarcoPorcellato/logseq-matryca-parser/issues/213), and Matryca-per-Delineat [#430](https://github.com/MarcoPorcellato/Matryca-per-Delineat/issues/430). These links assign no ownership, do not claim completion, and do not establish consumer readiness.

The later-gate topology discrepancy remains unresolved: the current source-admission record requires topology alongside `graph.read`, while the execution plan treats topology as optional enrichment after payload qualification. This roadmap does not reconcile the positions or claim a consumer is ready. PolyForm Noncommercial and the contributor-rights gate remain in force.

## Ordered programme

### Phase 0 — Public foundation and coordination

Maintain the public repository policy, PolyForm Noncommercial boundary,
contributor licensing gate, architecture, ADRs, contracts, roadmap, and
fork-safe CI. Reconcile stale planning surfaces; do not treat the accepted
ownership decision as a runtime, host, or consumer-profile claim.

Evidence: exact-head documentation checks; unambiguous ownership and authority;
no private or Pro source; no unsupported runtime claim.

### Phase 1 — Clean Architecture enforcement

Complete issue #9 before application expansion. Add repository-owned standards,
deterministic dependency/import checks, boundary tests, a repository-local
development skill, thin personal discovery, contributor guidance, and a
reviewed exception process. The skill points to canonical policy and does not
duplicate it.

The R1 executable projection is implemented. It becomes a repository
qualification only after publication and fork-safe hosted CI records evidence
for the exact published head.

Evidence: forbidden dependency fixtures fail; allowed dependency fixtures pass;
the skill is tested; fork-safe CI enforces the stack-independent rules.

### Phase 2 — Plumber contract decision and compatibility evidence

First, Plumber must publish its ADR, canonical public contract, schemas,
fixtures, compatibility policy, and evidence profile. Parser remains the owner
of its stable package-root API. Until that publication, no consumer adopts
`trama.logseq.read/v1` as a future interface.

Evidence: exact version/profile matrix; accepted and rejected fixtures;
producer, source, binding, capability, bounds, uncertainty, and digest fields;
unsupported versions, missing provenance, direct-database access, mutation,
foreign sessions, and incomplete subtrees fail closed.

### Decision D1 — Plumber selects official host transport or stops

After the Plumber contract and capability spike are terminal, Plumber selects
exactly one supported official-host route or records `capability_no_go` or
`upstream_blocked`. Trama builds no partial DB adapter.

### Phase 3 — Trama Plumber consumer profile

After Plumber publishes the contract, Trama may implement a Plumber client adapter
behind its internal domain port. A qualified `og_markdown` Plumber profile may
support the Trama consumer independently of D1. A `db_native` consumer profile
requires D1 outcome `supported`. Trama does not import Parser or implement Logseq
OG/DB adapters. Existing experimental adapters remain historical until explicitly
deprecated or removed. A DB graph never falls back to Markdown.

Evidence: stable graph binding, one page, one complete ordered subtree,
explicit failures, bounded lifecycle, zero forbidden state change, and exact
cross-repository hosted compatibility.

### Phase 4 — Nodi

Define the Trama-owned Nodi presentation-state contract, then deliver one small
read-only vertical. Nodi depends on public Community use cases and a Plumber
client adapter, never Parser, a Logseq host, Brain, Pro, network, or telemetry
implementations.

Evidence: deterministic states, accessibility checks, honest empty/loading/
unsupported/error presentation, and independent local Community operation.

### Phase 5 — Distribution and community

Prepare reproducible Community artifacts, provenance, support matrix, examples,
onboarding, and release documentation.

Evidence: clean release rehearsal and fork-safe hosted CI. Publication remains
a separate authorization gate.

## Deferred programmes

Events, DB-source Shadow, DB writes, Brain connection, Pro packaging,
entitlement, pricing, and commercial terms each require their own re-entry gate
defined by the canonical roadmap. No deferred capability enters Trama by
implication.

Repository-owned Community material remains under PolyForm Noncommercial
1.0.0. Commercial use requires a separate written agreement. External
copyright-bearing contributions remain merge-blocked until a lawyer-reviewed
contributor agreement or equivalent grant exists.
