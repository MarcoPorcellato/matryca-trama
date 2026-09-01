# ADR-0002: Trama and Brain Product Boundary

Status: Accepted

Date: 2026-08-31

Owner: Marco Porcellato

Supersedes: None

Superseded by: None

## Context

Trama is intended to be an approachable Logseq sidecar. Brain is a separate advanced product with different scope and privacy expectations. Combining their implementations would make licensing, releases, security, and user expectations unclear.

## Decision

Keep Trama and Brain as distinct products and repositories. Trama owns the
Community sidecar, Parser and Plumber integrations, OG/DB adapters, and Nodi.
Brain may provide separately governed capabilities through versioned public
contracts; Trama never imports Brain-private source.

## Consequences

Each product can evolve and release independently. Contract design and
compatibility testing become essential. A future commercial integration must
document authentication, data flow, licensing, and failure behavior before
implementation.

## Integration gate

Before a Trama--Brain connection is implemented, a reviewed public contract
must name its identifier, compatible version range, authentication and
authorization model, exact data flow, access selection and revocation,
licensing or entitlement boundary, upgrade and downgrade behavior, and failure
results. Tests must reject private-source imports and incompatible or
underspecified profiles. This gate applies equally when the connection is
optional: optionality does not permit implicit private coupling.

## Reversal

Only a new ADR can merge product boundaries. It must demonstrate that licensing,
security, release ownership, and offline Community behavior remain clear.
