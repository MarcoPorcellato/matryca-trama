# Matryca Trama Architecture

Matryca Trama is a public source-available Community monorepo for a Logseq
sidecar. Its architecture keeps source authority, product boundaries, licensing,
and optional integrations explicit.

## Layers

```text
Logseq OG Markdown          Logseq DB native store
        |                            |
  OG adapter                  DB adapter
        +------------+---------------+
                     |
            versioned contracts
                     |
             trama-core ---- Nodi experience
                     |
          apps, exports, integrations
```

Logseq OG Markdown files remain authoritative for OG workflows. The native
local database remains authoritative for Logseq DB workflows. Adapters
normalize only supported representations into documented contracts, preserve
provenance, and report unsupported behavior instead of guessing. An export or
derived index never becomes an implicit replacement authority.

## Repository boundaries

- `trama-core`: Community domain behavior and stable public APIs.
- `contracts`: versioned interfaces shared with Parser and Plumber.
- `parser-bridge`: integration boundary for the public Parser capability.
- `plumber-bridge`: contract-mediated integration boundary for Plumber consumer
  capabilities. It never imports Plumber internals or becomes a second
  authority for graph content.
- `logseq-og-adapter`: explicit Logseq OG support.
- `logseq-db-adapter`: explicit Logseq DB support, initially read-only until a
  later ADR proves safe write, export, and recovery semantics.
- `nodi`: user-facing knowledge companion and presentation model.
- `apps`: thin compositions of packages; business rules belong below this layer.

Matryca Brain is a separate product and repository. Trama may depend on public
contracts, never on Brain-private source. A Plumber bridge and any future Brain
bridge are independently versioned public boundaries; neither silently widens
the other. Pro source is excluded from this foundation.

## Initial Logseq read boundary

The first adapter contract is deliberately narrow: identify a graph, read one
page, and read one complete ordered block subtree. It must state the native
authority, adapter capability set, source binding, producer version, and
unsupported-condition result for every response. The OG adapter reads
authoritative Markdown; the DB adapter reads only through a later-qualified
official Logseq host surface. A cached export or derived projection is never
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
