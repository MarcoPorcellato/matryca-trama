# Logseq Read Contract and Adapter Implementation Plan

> **Historical plan:** checkboxes preserve the original planning and execution
> record. Current status is governed by the
> [delivery program](../../specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md).

> **Status:** planned; no runtime behavior is introduced by this document.
>
> **Source anchor:** `origin/main` at `cd9ec408ed9d4ece39d3eeaef506f4b172ab77d5`.
>
> **Related work:** [Trama #2](https://github.com/MarcoPorcellato/matryca-trama/issues/2), [Trama #4](https://github.com/MarcoPorcellato/matryca-trama/issues/4), [Matryca Brain #430](https://github.com/MarcoPorcellato/Matryca-per-Delineat/issues/430), [Tine #108](https://github.com/martinkoutecky/tine/issues/108), [Tine #109](https://github.com/martinkoutecky/tine/issues/109), and [Tine #337](https://github.com/martinkoutecky/tine/issues/337).

## Goal

Establish a versioned, public, testable foundation for Matryca Trama to expose
three read-only Logseq operations: graph identification, page read, and
complete ordered block-subtree read. The later Trama adapter remains the
host-facing producer; Matryca Plumber remains a separate consumer of the public
contract.

This plan deliberately does not implement an adapter, a GraphSession, a host
integration, a database reader, a cache, or a write path.

## Why this boundary

Logseq OG Markdown and the Logseq DB native store have different authority
models. A single contract may normalize supported reads, but it must preserve
which native authority supplied the result. This creates a small useful
interoperability surface without pretending that an export, index, Shadow
projection, or third-party process owns a graph.

The same separation keeps products coherent:

- Trama owns host-facing acquisition, capability detection, provenance, and
  the Community companion lifecycle.
- Plumber owns its consumer-side mapping, retrieval behavior, CLI/MCP runtime
  selection, and any later derived projections.
- Parser participates only through its public, versioned capability contract.
- Brain remains a separate product. A future connection is optional, public,
  versioned, and governed by ADR-0002; no Brain-private source is imported.

## Scope, non-goals, and status language

The initial contract is planned as `trama.logseq.read/v1` with these operation
identifiers:

| Operation | Required result | Explicitly excluded |
| --- | --- | --- |
| `graph.identify` | stable graph identity, source mode, authority, and capability set | graph mutation or discovery beyond the selected graph |
| `page.read` | one requested page and its provenance | page write, concurrent reconciliation, or inferred content |
| `block.subtree.read.complete` | the requested block plus its complete ordered descendant subtree and provenance | partial subtree substitution, block mutation, events, or subscriptions |

Every outcome must be classified as an accepted result, an explicit unsupported
condition, an incompatible-version result, or an authority/provenance failure.
Silence, guessing, or a fallback to a derived store is never a valid success.

The following remain deferred: events, subscriptions, background watch,
synchronization, Shadow acceleration, DB export, concurrent mutation, writes,
round-trip recovery, and any host-authoritative automation claim.

## Compatibility and provenance contract

Before runtime code, publish one compatibility matrix covering Trama, Parser,
Plumber, the selected official Logseq host surface, and the contract version.
Each profile must state the exact supported version range, enabled operations,
authority model, fixture set, and accepted failures.

Each response and failure record must carry at least:

- contract identifier and semantic version;
- producer name and released version or source revision;
- source mode (`og-markdown` or `db-native`), selected graph binding, and
  authority statement;
- advertised and exercised capability set;
- operation identifier, request identity, outcome class, and error code when
  applicable;
- sanitized fixture identifier and fixture or result digest.

Fixtures are public, synthetic, sanitized, and owned by Trama. They must prove
complete subtree order, unsupported behavior, compatibility rejection, and the
absence of an implicit write path. No fixture may contain a user vault, a local
path, a generated DB, credential material, or Brain-private content.

## External coexistence boundary

Tine Direct Files mode requires no new Trama capability for basic reading.
Until an official host contract with clear revision, conflict, locking, and
atomic-save semantics is available, Trama and Plumber make no concurrent-write
claim. A Tine session that may be active is a strict read-only condition. Tine
#337 is useful safety evidence, not permission for a second writer. Potential
future Tine CLI or MCP surfaces in #108 and #109 are host-owned options to
evaluate later, not dependencies or implementation commitments in this plan.

## Delivery sequence

### Task 1 — Record public authority and planning gates

**Files:**

- Create: this plan.
- Update: `docs/ARCHITECTURE.md`, `docs/ROADMAP.md`,
  `docs/internal/PERSISTENT_GOAL.md`, and ADR-0002.

**Acceptance evidence:** foundation validation and tests pass from the exact
planning commit. The diff contains no runtime package, dependency, host access,
or write behavior.

- [ ] Keep Trama, Plumber, Parser, and Brain ownership explicit.
- [ ] Define the three-operation initial read boundary and deferred work.
- [ ] Define minimum compatibility, provenance, fixture, and rejection rules.
- [ ] Preserve the public-only Brain integration gate.

### Task 2 — Specify the public contract in an independent PR

**Prerequisites:** Task 1 is merged and Trama issue #2 is reconciled to this
scope. Documentation may define public semantics before the application-stack
decision. Contract fixtures, tests, package paths, and an implementation claim
remain blocked until that decision provides their layout.

**Documentation files in this delivery slice:**

- `docs/contracts/LOGSEQ_READ_CONTRACT_V1.md`
- `docs/contracts/PARSER_COMPATIBILITY.md`
- `docs/contracts/PLUMBER_COMPATIBILITY.md`

**Deferred until ADR-0004:** versioned synthetic fixtures and contract tests in
the accepted application-stack layout.

**Acceptance evidence:** tests accept a complete profile and reject an unknown
version, missing provenance, wrong authority, incomplete subtree, and private
dependency. The public compatibility matrix identifies every tested component.

- [ ] Define stable DTOs, error codes, capability semantics, and version
  negotiation without naming an implementation language.
- [ ] Assign fixture ownership and digest rules.
- [ ] Define consumer conformance for Plumber without importing its internals.
- [ ] Add a no-private-import verification to the contract suite.

### Task 3 — Qualify one official host read route before adapter code

**Prerequisites:** Task 2 contract is accepted and a focused compatibility spike
has named a supported Logseq version and official host surface.

**Scope:** inspect only the selected host's documented read capability using
synthetic graphs. Record unsupported cases and source authority. Do not enable
writes, events, subscriptions, exports, or a background worker.

**Acceptance evidence:** exact host version, command or API surface, synthetic
fixture digest, source authority, operation results, and unsupported results are
recorded. An absent or incompatible host produces a typed rejection.

- [ ] Prove graph identity, page read, and complete ordered subtree read.
- [ ] Prove every result carries the Task 2 provenance envelope.
- [ ] Prove the route does not issue writes or create a derived authority.
- [ ] Submit host-specific limitations for review before implementation.

### Task 4 — Implement separate producer and consumer slices

**Prerequisites:** Task 3 is qualified; package and test locations are accepted
by the application-stack ADR.

**Trama slice:** implement the smallest host-facing read-only adapter behind
`trama.logseq.read/v1`, with synthetic contract tests and explicit unsupported
results.

**Plumber slice:** implement a consumer adapter in a separate repository PR.
It maps the public contract to Plumber's consumer port and must not make Trama
or a Tine process a new write authority.

**Acceptance evidence:** each repository independently passes its narrow tests;
the cross-repository matrix verifies exact compatible versions and public
provenance. A mismatch is rejected, not guessed.

### Task 5 — Reassess deferred capabilities one at a time

Events, subscriptions, Shadow acceleration, exports, and writes each require a
new issue, ADR, compatibility profile, threat review, synthetic fixtures, and
executable evidence. No Task 5 feature is implied by Tasks 1–4.

For writes, the additional gate must establish host authority, revision and
conflict semantics, atomic-save behavior, recovery, concurrent-process rules,
and user-visible opt-in. The absence of this gate remains a hard no-write
decision.

## Review and publication rules

- Keep every delivery slice docs-only or implementation-only; do not mix host
  selection, contract design, and runtime behavior in one PR.
- Run Trama's fork-safe foundation validator, unit tests, and whitespace check
  on the exact PR head.
- Publish only public contracts, synthetic fixtures, and sanitized evidence.
- Reverify repository state and current upstream issue status before opening a
  future PR. Issue discussion is context, not executable qualification.
- Do not add a Changelog entry until a user-visible runtime contract ships.

## Completion criteria for this plan

This planning slice is complete when the public architecture, roadmap,
persistent goal, and Brain boundary agree on the three-operation read-only
scope and its evidence gates. Runtime progress begins only with separately
reviewed Tasks 2–4.
