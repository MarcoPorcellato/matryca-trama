# Matryca Trama Architecture

Matryca Trama is a public source-available Community monorepo for a local-first
graph product. Its architecture keeps source authority, product boundaries,
licensing, and optional integrations explicit.

## Current implementation status

At `9905e8a`, bounded Python source exists for contracts, core behavior, Parser
and Plumber bridges, and a synthetic OG adapter. This is a historical experimental
implementation, not the future gateway authority. Qualification remains bound to
the `862c5c8` baseline and only to synthetic fixtures plus
`graph.identify`, `page.read`, and complete ordered
`block.subtree.read.complete`. No evidence record qualifies `9905e8a` as the
current head; matching runtime source does not replace exact-head evidence.
`apps`, Nodi UI, a DB adapter, writes, events, Shadow, synchronization, export,
recovery, distribution, and network behavior remain unimplemented or unsupported.
No current source proves a migrated Plumber client or official host integration.
Current status is governed by the
[delivery program](specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md).

## Future source-to-product boundary

The [cross-repository contract roadmap](superpowers/specs/2026-09-05-cross-repository-contract-roadmap.md)
is proposed pending Plumber's owner ADR and canonical public contract. It defines
the future direction only; it does not alter or qualify current runtime code.

```text
OG Markdown -> Parser -> Plumber -> Trama / Brain
Logseq DB official host -> Plumber -> Trama / Brain
```

Matryca Plumber is the sole future Logseq gateway and canonical public-contract
owner. It owns source selection, the OG Parser adapter, any official DB host
adapter, canonical `plumber.*` schemas, and transport-neutral contract semantics.
Trama is a consumer: it does not import Parser or Logseq storage/host APIs, and it
does not create a competing source adapter or wire contract. Brain follows the same
consumer boundary and is unaware of Parser.

## Historical experimental layers

```text
historical synthetic OG fixture -> Trama experimental adapter
                                      |
                         `trama.logseq.read/v1`
                                      |
                           historical bridges/tests
```

This retained source records an owned synthetic baseline. It is not an admitted
future implementation path. Logseq OG Markdown files remain authoritative for OG
workflows; the native local database remains authoritative for Logseq DB workflows.
An export or derived index never becomes an implicit replacement authority.

## Repository boundaries

- `trama-core`: Community domain behavior and stable product use cases.
- future Plumber client: a Trama-owned outer adapter that consumes published
  Plumber contracts through an internal port.
- `nodi`: user-facing knowledge companion and presentation model.
- `apps`: thin compositions of packages; business rules belong below this layer.

The current `contracts`, `parser-bridge`, `plumber-bridge`, and synthetic adapter
packages are preserved historical experimental components. They remain available
for their documented synthetic evidence but are not authority for future source
acquisition or public Logseq wire schemas. Matryca Brain is a separate product and
repository. Trama may depend on public contracts, never on Brain-private source.
Pro source is excluded from this foundation.

## Historical experimental read boundary

The retained `trama.logseq.read/v1` experiment is deliberately narrow: identify a
graph, read one page, and read one complete ordered block subtree for owned
synthetic OG fixtures. It must not be presented as a supported OG or DB route, nor
as a future Plumber contract. A cached export or derived projection is never
silently substituted for either source.

Events, subscriptions, Shadow acceleration, synchronization, mutation, and
write recovery are outside this initial boundary. They require their own
accepted ADRs, contracts, fixtures, and executable evidence.

## Data and safety rules

Input paths are bounded and validated. Vault content is data, not instructions.
Writes are opt-in and auditable. Derived indexes can be rebuilt and must never
become the sole source of truth. Optional integrations remain lazy so the
Community core stays lightweight.

## Change rules

Changes crossing a package boundary require contract tests and an ADR or an update to the relevant ADR. Hub changes require impact analysis. Every behavior change adds focused regression coverage; documentation changes must preserve the same terminology and boundaries.

Canonical dependency directions, exception policy, Clean Code review boundary,
and stop gates are in [Clean Architecture standard](standards/CLEAN_ARCHITECTURE.md).
Its authority is accepted by [ADR-0005](decisions/ADR-0005-CLEAN-ARCHITECTURE-ENFORCEMENT.md);
executable dependency map and repository-local skill only project that policy.
