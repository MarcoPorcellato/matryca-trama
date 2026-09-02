# Matryca Trama Roadmap

## Phase 0 — Public foundation

Deliver the public repository policy, PolyForm Noncommercial licence map,
commercial-use boundary, contributor licensing gate, CODEOWNERS, CI separation,
clean history, architecture, and contributor guide. Evidence: green policy and
documentation checks on the foundation commit.

## Phase 1 — Shared contracts

Define versioned contracts for Parser and Plumber, provenance fields,
compatibility rules, error semantics, and fixture ownership. The contract set
must publish a compatibility matrix for Trama, Parser, Plumber, and the
supported Logseq host surface; canonical contract identifiers and semantic
version ranges; accepted and rejected profiles; and sanitized fixture
ownership. Every result must carry producer identity and version, source mode
and binding, capability set, and fixture or result digest. Evidence: contract
tests run without private dependencies and reject unsupported versions.

## Phase 2 — Community core

Build the smallest deterministic Trama core around the public Parser capability. Preserve bounded filesystem behavior, stable identifiers, source locations, and reproducible outputs. Evidence: unit, integration, and reproducibility checks.

ADR-0004 selects Python 3.12+ with `uv` for the first Community implementation
direction. Runtime packages, contract tests, and platform support remain blocked
until the application-stack qualification protocol records exact-commit evidence.

## Phase 3 — Logseq adapters

Add an OG adapter and an initially read-only DB adapter with capability
detection, documented limitations, and authority-preserving fixtures. The
initial contract covers only graph identification, one page read, and one
complete ordered block-subtree read. The DB adapter selects no host surface
until a focused compatibility spike establishes an official, versioned
read-only route. Current qualification applies only to synthetic OG fixtures for
`graph.identify`, `page.read`, and complete ordered `block.subtree.read.complete`.
User graphs, DB, writes, events, Shadow, synchronization, export, recovery,
UI/Nodi, distribution, performance, and network remain unsupported. Evidence:
supported and unsupported cases are tested,
provenance is retained, and no DB write path exists without a later accepted
ADR.

## Phase 4 — Nodi

Implement Nodi as a central Trama experience: identity, state, accessible presentation, and knowledge-growth signals derived from user-authorized data. Evidence: deterministic fixtures, accessibility checks, and no private-service dependency.

## Phase 5 — Distribution and community

Publish reproducible Community artifacts, provenance, examples, onboarding,
and release documentation. Evidence: clean release rehearsal and fork-safe CI.

## Deferred decision track

Define the commercial agreement, pricing model, entitlement, contributor
agreement, and Pro packaging only after the Community boundary is stable. Public
prices are optional; self-service and private-quote sales remain valid future
options. A separate decision must choose between visible commercial source in a
mixed-license area and a private sibling repository. No Pro source, entitlement
mechanism, or Brain implementation enters this repository by implication.
