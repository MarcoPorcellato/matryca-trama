# ADR-0005: Clean Architecture Enforcement

Status: Accepted — executable projection pending R1 tasks

Date: 2026-09-05

Owner: Marco Porcellato

Supersedes: None

Superseded by: None

## Context

Trama has accepted source-authority, product-boundary, licensing, and
Python-first decisions. As packages enter the workspace, those decisions need
one canonical dependency policy, a deterministic way to reject mechanical
violations, and a review boundary for judgment that tools cannot make.

Proposed cross-repository responsibility contract informs coordination. It is
not accepted by this ADR. Until separately accepted, Trama enforces only
accepted Trama decisions, public contracts, and current package ownership.

## Decision

Adopt [Clean Architecture standard](../standards/CLEAN_ARCHITECTURE.md) as
canonical repository policy. Dependencies point inward. Policy names allowed
packages, import roots, declarations, exception process, review rules, and stop
gates.

R1 will use repository-owned Python standard-library validator and machine-
readable dependency map as projections of policy. Validator must fail closed
for mechanical violations, report source paths and lines, and run before
behavioral contract tests in fork-safe CI. No third-party architecture linter
is required for R1.

Initial exception registry is empty. Any future exception is temporary, narrow,
reviewed, and validated against standard; it cannot waive source authority,
licensing, contribution-rights, private-source, write, secret, or publication
gates.

Clean Code remains qualitative review contract. It does not invent numeric
complexity, file-length, coverage, or style thresholds without evidence of real
maintenance risk.

Repository-local agent guidance may route work to policy. Personal or global
skill installation is deferred and requires separate filesystem and publication
authorization.

## Alternatives considered

### Review-only architecture guidance

Review remains necessary, but cannot reliably reject undeclared dependencies,
forbidden import directions, private imports, or dynamic-import bypasses.

### Third-party architecture linter for R1

No demonstrated R1 need outweighs adding a tool and its maintenance boundary.
A later ADR may adopt one after showing a gap in repository-owned validation.

### Treat cross-repository proposal as accepted

That would silently expand Trama authority. Coordination remains proposed until
its owners accept it through their own decision process.

## Consequences

- Policy is canonical; dependency map, validator, CI, and skill only project
  it. Disagreement stops work until policy and projection are reviewed together.
- R1 adds no DB access, writes, events, Shadow, synchronization, export,
  recovery, network behavior, Nodi runtime, Brain or Pro source, entitlement,
  pricing, or commercial right.
- Logseq OG Markdown remains authoritative for OG workflows; native Logseq DB
  storage remains authoritative for DB workflows. Derived data never silently
  replaces either source.
- Community material remains PolyForm Noncommercial 1.0.0. External
  copyright-bearing contributions remain merge-blocked pending lawyer-reviewed
  contributor agreement or equivalent grant.

## Reversal

A later ADR may replace the enforcement mechanism only if it preserves this
policy's fail-closed guarantees, accepted product boundaries, and public
contract authority. It must not silently accept the proposed cross-repository
responsibility contract.
