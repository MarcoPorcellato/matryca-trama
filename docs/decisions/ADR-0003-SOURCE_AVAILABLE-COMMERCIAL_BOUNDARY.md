# ADR-0003: Source-Available Community and Commercial Boundary

Status: Accepted

Date: 2026-08-31

Owner: Marco Porcellato

Supersedes: the Apache-2.0 repository-owned licence choice in ADR-0001

Superseded by: None

## Context

Trama should be publicly inspectable, useful for personal and noncommercial
communities, and commercially sustainable. Apache-2.0 would permit unrestricted
commercial reuse and would not reserve a commercial licensing path. Keeping all
source private would reduce trust, learning, and community visibility.

## Decision

License repository-owned Community material under PolyForm Noncommercial 1.0.0.
Require a separate written agreement for commercial use. Describe the
repository as public source-available, not open source. Keep pricing, billing,
entitlement technology, Pro packaging, and Brain bundles as later decisions.

Do not merge external copyright-bearing contributions until a lawyer-reviewed
agreement grants the permissions required for both the Community and commercial
paths. Preserve third-party licence boundaries and required notices.

## Alternatives

- Apache-2.0 maximizes reuse but cannot reserve commercial use.
- PolyForm Small Business permits commercial use below its thresholds and does
  not match the chosen separate-commercial-licence boundary.
- PolyForm Shield primarily restricts competing products and would permit much
  ordinary non-competing commercial use.
- A private-only repository protects source but weakens public trust and the
  Community path.
- Business Source License adds a time-delayed change licence and operational
  complexity that is unnecessary at this foundation stage.

## Consequences

People can inspect the source and use it for the purposes expressly permitted
by PolyForm Noncommercial. Commercial adopters need a separate licence. The
project must avoid open-source claims, create a real commercial agreement before
selling rights, and resolve contributor relicensing before accepting external
pull requests.

The commercial offer can later use public prices, private quotes, subscriptions,
perpetual terms, or bundles without changing the Community licence. Existing
signed agreements must be honoured when future prices change.

## Reversal

The licensor may offer future versions under different terms, but cannot revoke
rights already granted for published versions outside the licence terms. Any
change requires a new ADR, an effective-version boundary, migration guidance,
and legal review. Do not rewrite published history to conceal the former terms.
