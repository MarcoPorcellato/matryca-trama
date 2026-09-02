# Logseq DB Host Bridge Refinement Design

**Status:** proposed; documentation-only decision refinement

## Purpose

Matryca Trama has a qualified Python-first synthetic OG read contract. It does
not yet ship Nodi, applications, exports, or a Logseq DB adapter. This design
preserves that foundation while defining the only circumstance in which a small
host-language component may exist: an official in-process Logseq Plugin SDK
route is the sole DB transport that passes the read-only capability spike.

No DB adapter, host bridge, or user-graph operation is introduced by this
document.

## Authority and Mode Separation

Logseq OG Markdown remains authoritative for OG workflows. Logseq DB remains
authoritative only through a qualified official host surface. These modes must
not be converted into each other by inference.

The OG adapter rejects a DB graph. A DB route never opens, queries, copies, or
mutates `db.sqlite`; it also never silently uses a Markdown mirror, cache,
export, Shadow projection, or OG parser as replacement data.

For DB read-only work, Trama evaluates three mutually exclusive candidates:

1. official Markdown Mirror;
2. official built-in CLI or MCP;
3. isolated in-process Plugin SDK bridge.

A source mode of `db_native` identifies authority, not transport permission.
Each concrete profile must declare one host surface and exact provenance.

## Python-First Boundary

Python remains Trama's implementation language for shared contracts, core
semantics, synthetic fixtures, test harnesses, OG integration, and Plumber
bridge code.

An isolated TypeScript component is permitted only after D1 selects the Plugin
SDK. It is a host transport adapter, not an application stack:

- it calls only the selected official SDK methods;
- it normalizes bounded host results into `trama.logseq.read/v1`;
- it contains no domain rules, cache, persistence, writes, credentials, UI, or
  independent graph authority;
- it fails closed on unsupported version, graph switch, missing capability,
  stale session, malformed payload, or incomplete subtree;
- it has its own pinned dependency lock and exact application/SDK evidence.

No TypeScript package is added before that decision. The existing Python-first
ADR therefore remains the governing default, with this narrow, conditional
exception.

## D1 Capability Contract

Each candidate must prove, against synthetic fixtures and one disposable DB
graph, all of the following before selection:

| Operation | Required result |
| --- | --- |
| `graph.identify` | DB mode, stable graph binding, supported host/version provenance. |
| `page.read` | Stable page ID, title, documented supported properties, bounded result. |
| `block.subtree.read.complete` | Complete ordered descendants, IDs, parent references, no duplicates, no missing children. |

Every candidate must explicitly reject direct SQLite access, user-graph use,
foreign graph binding, graph switch, stale session, unavailable host feature,
partial mirror, partial subtree, and implicit fallback.

Markdown Mirror needs extra proof that its page marker maps to the active DB
graph, that host production is fresh for the tested session, and that its
rendered hierarchy is complete. CLI and MCP require a pinned non-nightly
support profile before production selection. The Plugin SDK bridge requires a
host-bound session and minimal permission surface.

## Interface Boundary After Selection

Only a selected DB candidate may later produce the versioned Trama read
contract for a Plumber consumer. It is an additional route, not a replacement
for Plumber's direct OG integration:

```text
Logseq OG Markdown -> Plumber direct OG path

Logseq DB host
  -> selected Trama transport adapter
  -> trama.logseq.read/v1 normalized DTO
  -> optional Plumber consumer boundary
```

The DTO preserves source mode, authority, graph/session binding, capability
profile, provenance, error kind, page identity, and complete subtree ordering.
It must not expose host-private database schema, filesystem paths, raw logs, or
credentials.

## Deferred Work

Writes, events, DB-source Shadow acceleration, synchronization, exports,
recovery, application UI, Nodi, packaging, Matryca Brain connection, and
concurrent-editor claims remain out of scope. A failing D1 result is a complete
and valid outcome: Trama publishes a sanitized NO-GO record and implements no
partial DB adapter.

## Acceptance Criteria

- Current Python-first OG qualification and Plumber's direct OG path remain unchanged.
- DB support remains unavailable until one versioned D1 candidate qualifies.
- Direct SQLite access and implicit source fallback are forbidden in every path.
- A future Plugin SDK bridge, if selected, is isolated and transport-only.
- Cross-repository Plumber integration starts only after a shared contract and
  selected transport have independent, exact evidence.
