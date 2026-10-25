# Matryca Trama Architecture

Matryca Trama is a public source-available Community monorepo for a local-first
graph product. Its architecture keeps source authority, product boundaries,
licensing, and optional integrations explicit.

## Current implementation status

Published main observed on 2026-10-25 is
`d21f2adb2101ce5fae222f6235925c1d66ece126`. It contains the internal
`KnowledgeGraphGateway.snapshot() -> GraphSnapshot` domain port, immutable
content-free graph values, and the outer `PlumberClientAdapter`. That adapter
depends on Community core and the standard library, not in-process Parser or
Plumber imports. The client accepts only the admitted authenticated disposable
synthetic fixture handle and invokes a separately provisioned producer;
arbitrary graph roots, bypass and retry paths are excluded from the client.

[Producer-M2 qualification](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/40112844731/attempts/2)
exercised `a4463638baaca846fe731556417f1d2d660838f1`, whose tree
`6c6fc59abb2f1d2f46f85d03374b6d5f4d31cbdf` also identifies the PR #33 merge
tree. This is a restricted synthetic client, not stable API or user-graph
support. Its exact admission, producer closure and unchanged packaged labels
are recorded in the [source-admission record](contracts/PLUMBER_SOURCE_ADMISSION.md#current-owner-admission--2026-10-24).
Main CI and Producer-M3 exploration are separate evidence dimensions.

The historical `trama.logseq.read/v1` implementation retains its original
`862c5c8` baseline evidence for synthetic `graph.identify`, `page.read`, and
complete ordered `block.subtree.read.complete`; it does not qualify the new
client. `apps`, Nodi UI, payload/title/text/property reads, official DB host
integration, writes, events, Shadow, synchronization, export, recovery,
distribution, and supported OS isolation remain unimplemented or unsupported.
Current status is governed by the
[delivery program](specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md).

## Accepted source-to-product boundary

The accepted [Plumber gateway adoption](decisions/ADR-0006-PLUMBER-GATEWAY-ADOPTION.md)
defines ownership. That decision and the cross-repository migration plan alone
did not create or qualify a client; the later separate owner admission and
Producer-M2 implementation establish only the restricted slice above.

```text
OG Markdown -> Parser -> Plumber -> Trama / Brain
Logseq DB official host -> Plumber -> Trama / Brain
```

Matryca Plumber is the sole Logseq gateway and canonical public-contract
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

- `trama-core`: Community domain behavior, immutable graph values and internal
  gateway port; no public API stability is claimed.
- `plumber-client`: the implemented Trama-owned outer adapter consuming the
  admitted Plumber profiles through that port, with the restricted synthetic
  input and separately provisioned producer described above.
- `nodi`: planned user-facing knowledge companion and presentation model.
- `apps`: planned thin compositions; business rules belong below this layer.

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
