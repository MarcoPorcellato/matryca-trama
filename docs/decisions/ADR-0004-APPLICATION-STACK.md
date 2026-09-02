# ADR-0004: Python-First Community Application Stack

Status: Accepted — runtime admission pending qualification

Date: 2026-09-01

Owner: Marco Porcellato

Supersedes: None

Superseded by: None

## Context

Matryca Trama has an accepted public foundation and a planned read contract, but
it has no application source, package layout, or executable contract suite.
The first implementation must stay useful without private services, preserve
Logseq source authority, integrate only through public Parser and Plumber
contracts, and provide a small path to synthetic conformance evidence.

The repository's existing executable policy is Python standard-library
validation and tests. Parser and Plumber are Python projects with documented
public version boundaries. A first stack must therefore minimise new tooling
while leaving thin application surfaces and a later Nodi user interface free to
evolve independently.

## Decision

Adopt Python 3.12+ with `uv` as the first Community runtime and packaging
stack. Use a root `uv` workspace only when the first executable slice is
admitted. Keep business behavior in small public packages; applications remain
thin compositions and are not created by this decision.

The intended first package boundaries are:

```text
packages/
  contracts/             versioned DTOs, capability and error vocabulary
  trama-core/            deterministic domain behavior
  parser-bridge/         public Parser boundary
  logseq-og-adapter/     read-only OG Markdown acquisition
  plumber-bridge/        public consumer compatibility boundary
tests/
  contracts/             public synthetic conformance vectors
  fixtures/              sanitized, Trama-owned inputs and digests
  containment/           filesystem and no-private-import checks
```

`logseq-db-adapter`, `apps/`, Nodi UI code, and all user-facing packaging stay
absent until their own decisions and evidence exist. The first executable slice
may create only the packages and tests necessary for the three-operation
read-only contract.

## Qualification boundary

This ADR accepts the architecture direction, not a supported runtime or Logseq
host claim. Runtime admission remains blocked until the qualification protocol
in [Application Stack Qualification](../spikes/APPLICATION_STACK_QUALIFICATION.md)
records exact-commit evidence for its mandatory gates.

No package may claim support for an operating system, a Logseq DB host, Parser
or Plumber integration, performance, accessibility, distribution, or mutation
behavior without its own executable evidence.

## Alternatives considered

### TypeScript-first workspace

This could serve a future Nodi application, but Trama has no Node toolchain,
workspace, test runner, or executable TypeScript boundary today. It would add
bootstrap work before the first public contract test and is deferred until an
application-specific decision needs it.

### Rust-first workspace

Rust could later suit a constrained native sidecar, but Trama has no Cargo
toolchain or Rust API boundary. It would add cross-language bridge and
distribution work before proving the read-only contract. It remains a future
option behind a separate ADR.

### Documentation-only continuation

Documentation alone cannot provide the required synthetic fixture, compatibility
rejection, and containment evidence. It remains valuable for planning but does
not unblock the first executable contract slice.

## Consequences

- The first core, contract, Parser bridge, OG adapter, and Plumber bridge use
  Python package boundaries and public imports only.
- `uv` owns reproducible dependency resolution once code exists; no global
  installation or private package source is required.
- Contract fixtures remain language-neutral data. A later TypeScript or Rust
  application may consume the same versioned contract rather than duplicate
  semantics.
- A thin Nodi application is explicitly deferred; it must not drive domain
  ownership into an application layer.
- DB access, writes, events, synchronization, exports, Shadow acceleration,
  and recovery remain out of scope.

## Reversal

A new ADR may replace Python-first implementation if a recorded qualification
shows that it cannot meet mandatory Community, containment, or supported-host
requirements. The replacement must preserve public contract identifiers,
synthetic fixtures, provenance semantics, and the no-private-import rule, or
publish a versioned migration path.
