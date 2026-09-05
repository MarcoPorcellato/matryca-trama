# Matryca Ecosystem Responsibility and Change Contract

> **Status:** superseded historical coordination draft; non-operative.
> This preserves the 2026-09-05 proposal for review history only. It grants no
> cross-repository authority, runtime acceptance, compatibility claim, or
> delivery authorization. Its normative wording records the old proposal and
> must not override accepted ADRs, repository-local contracts, or current
> owner-controlled work.

## Purpose

This contract assigns one owner to each product capability and one authority to
each shared interface. Its purpose is to prevent duplicated implementations,
private-source coupling, and cross-repository branches whose dependencies are
unclear.

The normative words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** describe the
intended repository contract. A planned interface is not a runtime or
compatibility claim until its evidence gate passes on exact versions.

## Authority order

When reports disagree, use this order:

1. exact source, tests, release artifacts, and reviewed evidence at a complete
   commit;
2. accepted ADRs and canonical contracts in the owning source repository;
3. the current execution plan for its declared scope;
4. strategy and status reports as dated proposals or observations;
5. Matryca Knowledge as a read-only coordination projection.

Every cross-repository decision MUST reverify the owning repositories' live
heads. A report or derived index MUST NOT silently override newer source.

## Repository ownership

| Repository | Sole or primary ownership | Explicit exclusions |
| --- | --- | --- |
| Matryca Trama | Community companion product, Nodi, public Trama contracts and DTOs, Logseq host lifecycle, OG and DB host adapters, capability detection, source-mode provenance, thin application composition | Parser internals, Plumber daemon/search/OCC/Shadow internals, Brain-private or Pro source, DB writes without a later accepted ADR |
| Logseq Matryca Parser | deterministic Markdown parsing, AST and graph identity, diagnostics, serialization, path safety, package-root Python API | Trama UX, Plumber orchestration, native Logseq DB sessions, product entitlement |
| Matryca Plumber | memory and search services, daemon, CLI/MCP agent surfaces, existing OG `GraphReadPort`, governed OG operations and OCC, derived Shadow read cache, future consumer-side `GraphSessionReadPort` | a second Trama companion, Nodi, Logseq host adapters, Trama wire-schema ownership, native Logseq DB writes before evidence |
| Matryca Brain | separate sovereign multi-source workspace, its ingest/RAG/governance/UI, and any Brain-side optional public integration port | Trama Community runtime, Nodi ownership, copied Trama/Plumber internals, implicit entitlement or bundled-source decisions |
| Matryca Knowledge | read-only, Git-provenanced discovery and coordination projection | canonical runtime behavior, source edits, release or compatibility authority |

## Dependency direction

```text
Logseq OG Markdown ──> Parser public API ──> Trama OG adapter
        │                                      │
        └────────────> Plumber existing OG path│
                                               v
                                  trama.logseq.read/v1
                                               │
                                               v
                                  Plumber session consumer

Logseq DB official host ──> Trama DB adapter ──┘

Brain ── optional public versioned contract only ── Trama/Plumber
Knowledge ── observes pinned public sources; never a runtime dependency
```

Plumber's existing OG path through Parser remains Plumber-owned and MUST NOT be
rewritten merely to make the diagram uniform. New Logseq DB interoperability
uses the Trama host boundary and a separate Plumber session port. A DB graph
MUST NOT fall back to an OG filesystem graph.

## Stable contract catalogue

### C1 — Parser public API profile

- **Authority:** Logseq Matryca Parser's package-root stability contract.
- **Current Trama range:** `>=1.7.1,<2.0.0`; the qualified synthetic fixture
  lock contains Parser `1.8.2`.
- **Consumers:** Trama OG adapter and Plumber's existing OG path.
- **Rule:** consumers MAY import only documented package-root symbols. They
  MUST NOT copy identity, parsing, serialization, or diagnostic rules.
- **Breaking change:** owned by Parser; requires the Parser version and
  migration policy, followed by separate consumer qualification.

### C2 — `trama.logseq.read/v1`

- **Authority:** Matryca Trama.
- **Owner:** Trama `packages/contracts` and its normative contract document.
- **Current implemented slice:** `graph.identify`, `page.read`, and
  `block.subtree.read.complete` for owned synthetic OG fixtures.
- **Producer:** a Trama host adapter.
- **Consumers:** Plumber and later optional public integrations.
- **Required result identity:** contract id/version, operation/request id,
  explicit outcome, producer identity/version, source mode and authority,
  source reference, graph binding, capability set, and evidence digest.
- **Rule:** consumers MUST reference this authority. They MUST NOT redeclare or
  fork its wire representation.

The current Trama `plumber-bridge` package is a reference admission and
conformance helper. It is not a Plumber runtime, session router, search service,
or second implementation of `GraphReadPort`.

### C3 — Plumber consumer evidence profile

- **Authority:** Matryca Plumber.
- **Purpose:** decide whether host-capability evidence is admissible for a
  Plumber integration claim.
- **Scope:** outer qualification state, exact Trama and host references,
  bounded limits, uncertainty, forbidden actions, lifecycle observations, and
  result digests.
- **Rule:** it references C2 and MUST NOT copy C2 request/result semantics.
- **Separation:** Trama runtime outcomes and Plumber qualification states are
  different namespaces and MUST NOT substitute for each other.

### C4 — Logseq host capability evidence

- **Producer:** the Trama compatibility spike using a disposable, synthetic DB
  graph and one exact official host artifact.
- **Admission:** C3 in Plumber.
- **Required proof:** stable graph identity with the application open and
  closed, exact page identity, complete ordered descendant structure, bounded
  process behavior, and zero forbidden state change.
- **Current status:** unqualified. No production DB adapter may start before an
  accepted `supported`, `capability_no_go`, or `upstream_blocked` result.

### C5 — Nodi presentation-state contract

- **Authority:** Trama.
- **Purpose:** convert user-authorized Community state into deterministic,
  accessible Nodi presentation states.
- **Rule:** Nodi MUST depend on Trama use cases and public value objects, not on
  concrete Parser, Plumber, host, network, or Brain implementations.
- **Current status:** planned; no UI or Nodi runtime claim.

### Deferred contract lines

Events, DB-source Shadow ingestion, graph writes, and Brain connection are not
minor extensions of C2:

- events require a separate cursor, gap, ordering, reconnect, and
  resynchronization contract;
- DB-source Shadow requires a separate freshness, generation, rebuild, and
  source-binding contract;
- writes require a separate authority contract covering preview, expected
  revision, conflict rejection, atomicity, timeout reconciliation, recovery,
  and undo/redo;
- an optional Trama--Brain connection requires an accepted public contract for
  authentication, least authority, graph selection, consent, data flow,
  revocation, version skew, failure recovery, entitlement, and downgrade.

None of these lines is authorized or qualified by this document.

## Clean Architecture invariants

Within Trama:

- `packages/contracts` MUST remain independent of apps, adapters, bridges,
  Nodi, Brain, and Plumber implementation code.
- `packages/core` MUST contain domain and use-case behavior and MUST NOT import
  apps or concrete adapters.
- host adapters and Parser/Plumber bridges MUST depend inward through public
  contracts or ports; inward layers MUST NOT import them.
- `nodi` MUST be a presentation model over public use cases, not a host or
  persistence adapter.
- `apps` MUST be composition roots. Business rules MUST remain below them.
- optional integrations MUST be lazy and replaceable; Community behavior MUST
  remain useful without Brain or Pro services.

Across repositories:

- one repository owns each wire contract and fixture authority;
- consumers keep only version declarations, admission profiles, and negative
  fixtures they own;
- generated bindings, if introduced, MUST identify the canonical source commit
  and schema digest and MUST be reproducible;
- no repository may import another repository's private modules or copy source
  to avoid a versioned dependency;
- every authority or dependency-direction change requires an ADR and focused
  boundary tests.

Issue #9 defines the remaining enforcement work: repository-local standards,
deterministic import and dependency checks, review rules, and a repository-owned
development skill. Those checks implement this contract; they MUST NOT create a
second policy text.

## Change and delivery protocol

1. Reverify complete live heads and dirty state in every affected repository.
2. Name one owning repository and one canonical contract authority.
3. Change the owner first. Publish sanitized fixtures and exact evidence.
4. Merge the owner change before cutting a dependent consumer branch.
5. Update each consumer in a separate repository-local PR pinned to the exact
   owner commit, contract version, profile, and fixture digest.
6. Run focused boundary tests and that repository's full fork-safe CI.
7. Publish a compatibility claim only after every required exact-version row is
   terminal green.

Only one cross-repository mutating slice may be active at a time. Disjoint
read-only research or documentation may run in parallel, but adapter,
transport, schema, session-routing, and product work remain dependency-ordered.
There is no long-lived integration branch and no multi-repository PR.

## Version and failure rules

- A breaking schema or semantic change requires a new contract major.
- A backward-compatible field or capability requires explicit capability
  negotiation and minor-version evidence.
- A producer MUST fail explicitly on unknown major, unsupported capability,
  incomplete subtree, foreign graph binding, missing provenance, malformed or
  excessive payload, timeout, or stale session.
- A consumer MUST fail closed. It MUST NOT reconstruct success from a cache,
  export, partial payload, or different source authority.
- An exact prerelease is not compatible merely because a stable predecessor is
  accepted. It requires an explicit profile row and evidence.

## Licensing and contribution boundary

Repository-owned Community material remains under PolyForm Noncommercial
1.0.0. Commercial use requires a separate written agreement. This technical
contract does not define prices, entitlement, Pro packaging, or a Brain bundle.

External copyright-bearing code or documentation MUST NOT be merged until a
lawyer-reviewed contributor agreement or equivalent grant is active. Issues,
design discussion, review, and non-copyrightable factual observations remain
welcome under the repository's contributor policy.

## Source anchors reviewed on 2026-09-05

- `matryca-trama@9905e8a36acb83a17a33b702a5fa620d6bfed185:docs/ARCHITECTURE.md`
- `matryca-trama@9905e8a36acb83a17a33b702a5fa620d6bfed185:docs/contracts/LOGSEQ_READ_CONTRACT_V1.md`
- `matryca-trama@9905e8a36acb83a17a33b702a5fa620d6bfed185:docs/decisions/ADR-0002-TRAMA_BRAIN_PRODUCT_BOUNDARY.md`
- `matryca-trama@9905e8a36acb83a17a33b702a5fa620d6bfed185:docs/decisions/ADR-0003-SOURCE_AVAILABLE-COMMERCIAL_BOUNDARY.md`
- `logseq-matryca-parser@65e8e64f7f0227bcae8235069fbc3da834652744:docs/reference/API_STABILITY.md`
- `matryca-plumber@d347d43dad090586b10a77a53c4e0c8fd6da8e15:docs/superpowers/plans/2026-09-01-logseq-db-read-only-compatibility.md`
- `Matryca-per-Delineat@e69a97a8c702a773c9a3ce8307b5a667ed2be1dd:docs/MATRYCA_TRAMA_BRAIN_PORTFOLIO_STRATEGY.md`
- `Matryca-knowledge@52500d623feecd2ec156e653be9d521383740ddb:README.md`
