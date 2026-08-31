# ADR-0001: Public Community Monorepo

Status: Accepted

Date: 2026-08-31

Owner: Marco Porcellato

Supersedes: None

Superseded in part by: ADR-0003 for repository-owned licensing

## Context

Trama needs a discoverable community surface and shared development of its
Community applications, adapters, contracts, and Nodi experience. Public
visibility improves review and learning, but it cannot protect secret
implementation or credentials.

## Decision

Use one public monorepo for Community code. Keep the history clean and exclude
Pro source, Brain internals, vault content, credentials, and private build
inputs. Use package boundaries, ownership, path-aware CI, and explicit
contracts. ADR-0003 replaces the original Apache-2.0 licensing choice with
PolyForm Noncommercial 1.0.0 and a separate commercial path.

## Alternatives

- A private monorepo would simplify secrecy but reduce community trust and contribution.
- A public mixed-license monorepo may be evaluated later, but visible commercial source is not secret and requires a new packaging decision.
- A public Community repository plus private Pro repository remains available if secrecy is required.

## Consequences

The Community build is easy to inspect, test, and package for permitted
noncommercial purposes. Pro cannot be smuggled into the public tree through an
assumed overlay. Commercial use remains governed separately. Additional
repository or packaging work may be needed later.

## Reversal

Do not make published history private as a secrecy measure. Reversal means freezing the public contract and creating a new private repository, after an explicit security and licensing review.
