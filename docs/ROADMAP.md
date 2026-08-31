# Matryca Trama Roadmap

## Phase 0 — Public foundation

Deliver the public repository policy, PolyForm Noncommercial licence map,
commercial-use boundary, contributor licensing gate, CODEOWNERS, CI separation,
clean history, architecture, and contributor guide. Evidence: green policy and
documentation checks on the foundation commit.

## Phase 1 — Shared contracts

Define versioned contracts for Parser and Plumber, provenance fields, compatibility rules, error semantics, and fixture ownership. Evidence: contract tests run without private dependencies.

## Phase 2 — Community core

Build the smallest deterministic Trama core around the public Parser capability. Preserve bounded filesystem behavior, stable identifiers, source locations, and reproducible outputs. Evidence: unit, integration, and reproducibility checks.

## Phase 3 — Logseq adapters

Add an OG adapter and an initially read-only DB adapter with capability
detection, documented limitations, and authority-preserving fixtures. Evidence:
supported and unsupported cases are tested, provenance is retained, and no DB
write path exists without a later accepted ADR.

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
