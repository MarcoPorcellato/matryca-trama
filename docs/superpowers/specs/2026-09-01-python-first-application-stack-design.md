# Python-First Application Stack Design

> **Historical design record:** preserve its original decision-time language.
> Current implementation and qualification status is governed by the
> [delivery program](../../specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md).

> **Status:** approved architecture direction; documentation-only design.
> Runtime admission remains blocked by the qualification protocol.

## Goal

Create the smallest public implementation foundation for
`trama.logseq.read/v1` without creating a Logseq DB claim, a write capability,
or an application surface. The first runtime must make public contract tests
possible while keeping future applications independent of domain ownership.

## Architecture

ADR-0004 selects Python 3.12+ and `uv`. A future root workspace contains
versioned contracts, deterministic core behavior, one public Parser bridge, one
read-only OG adapter, and one public Plumber bridge. Each package owns one
boundary; `apps/` remains absent until a Nodi/application decision exists.

```text
synthetic OG fixture
        |
logseq-og-adapter -- parser-bridge
        |
     trama-core
        |
      contracts -- plumber-bridge
```

The adapter produces only public result envelopes. It never makes a cache,
export, or derived projection authoritative. Plumber remains a consumer; Brain
remains separate and private implementation imports remain forbidden.

## First vertical slice

The first implementation may support only graph identification, one page read,
and one complete ordered block-subtree read against sanitized OG fixtures.
Requests and results retain the published version, provenance, authority, and
typed-failure semantics. Unsupported or incomplete evidence is returned as a
failure result, never guessed content.

## Error and safety model

The only public outcome classes are those in the read contract: `unsupported`,
`incompatible`, `invalid_request`, `not_found`, `authority_failure`, and
`provenance_failure`, plus success with complete provenance. Filesystem access
is constrained to a selected synthetic root during qualification. No code may
write graph content, open a native DB, start a watcher, create an index, or
implicitly fall back to an export or cache.

## Test design

Language-neutral fixtures live under `tests/fixtures`; Python tests live under
`tests/contracts` and `tests/containment`. The first suite must prove valid
reads and rejection of unsupported versions, absent provenance, wrong authority,
incomplete subtrees, private imports, path escape, and symlink escape. It also
records normalized result digests for deterministic fixture requests.

## Delivery order

1. Add package layout and public `uv` configuration only after this design is
   reviewed and the implementation plan is approved.
2. Add failing synthetic contract and containment tests.
3. Implement contracts and core before bridges and the OG adapter.
4. Qualify exact-commit evidence with the application-stack protocol.
5. Reassess a DB host only through its separate official-host spike.

## Non-goals

Nodi UI, `apps/`, DB adapters, DB host selection, events, Shadow acceleration,
synchronization, export, recovery, distribution, and all writes remain out of
scope. TypeScript and Rust remain future alternatives, not dependencies of this
slice.

## Review checklist

- Does Python-first reduce bootstrap cost without claiming a supported runtime?
- Are contracts independent of UI and private products?
- Are containment, provenance, and explicit failure behavior testable?
- Does every deferred capability remain named and blocked?

## Implementation plan

The dependency-ordered implementation plan is
[Python-first read contract implementation](../plans/2026-09-01-python-first-read-contract-implementation.md).
It remains a plan until its own execution authorization is granted.
