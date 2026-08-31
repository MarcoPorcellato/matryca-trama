# Matryca Trama Public Monorepo Foundation

> **Status:** active canonical specification
>
> **Owner:** Marco Porcellato
>
> **Anchor:** repository created on 2026-08-31 from clean public history;
> verify live `origin/main` before every delivery milestone.

## Purpose and falsifiable outcome

Create a trustworthy public home for Matryca Trama that can deliver permanent
Community value to Logseq users without exposing Pro or Matryca Brain source. The
foundation succeeds when a contributor can identify the repository authority,
licence, product boundaries, planned packages, security rules, and next
evidence-gated milestone without private context.

## Decision

Matryca Trama starts as a public source-available Community monorepo under
PolyForm Noncommercial 1.0.0. Commercial use requires a separate written
licence. It does not contain Pro source, Brain implementation, private
credentials, vault data, or historical exports. Pricing, sales channels,
commercial terms, and commercial-source packaging are later decisions and must
not weaken the public boundary.

## Product and data-authority boundary

Trama is the approachable Logseq sidecar: it provides graph-aware experiences,
Nodi, and integrations for Logseq OG and Logseq DB. Matryca Brain remains a
distinct product and repository. Trama may consume stable Brain-facing
contracts in the future, but it must not import Brain's private implementation.

For Logseq OG, Markdown files remain authoritative. For Logseq DB, the native
local database remains authoritative. The first DB integration is read-only;
write or round-trip behavior requires a later ADR with recovery evidence.

## Status vocabulary

- **Accepted:** a durable decision approved by the maintainer.
- **Planned:** scoped work with an explicit exit gate, not implemented behavior.
- **Qualified:** exact-commit evidence satisfies the named gate.
- **Deferred:** deliberately excluded until its prerequisite decision exists.
- **Blocked:** cannot proceed safely without named evidence or authority.

## Repository shape

```text
matryca-trama/
  apps/                    user-facing applications
  packages/                shared Community libraries and contracts
    trama-core/
    contracts/
    nodi/
    logseq-og-adapter/
    logseq-db-adapter/
    parser-bridge/
    plumber-bridge/
  docs/
  examples/
  tests/
  .github/
```

Names describe intended boundaries, not a claim that every package already
exists. New packages require an API, ownership, licence, tests, and
documentation before publication.

## Non-negotiable invariants

- Logseq OG Markdown and the Logseq DB native store retain their respective
  authority; derived graphs, indexes, exports, and visualizations remain views.
- Parser and Plumber are consumed through versioned, documented contracts
  rather than copied internals.
- OG and DB adapters are explicit capability boundaries; neither may silently
  replace the authority of its native source.
- Nodi is a first-class Trama experience, not a dependency of Brain.
- The Community build must be reproducible without private services, secrets, or
  private packages.
- Public pull requests from forks run without secrets and cannot publish.
- Clean history is required: no import of the legacy Brain prototype or
  sensitive artifacts.

## Scope and non-goals

In scope: public governance, Community contracts, adapters, Nodi, a future thin
application shell, reproducible Community artifacts, and safe contributor
workflows. Out of scope: Pro source, entitlement enforcement, Brain source,
hosted accounts, telemetry, paid connectors, private packages, commercial
checkout, and imported legacy history.

No milestone may imply support for a Logseq format, operating system, write
path, or product integration before executable evidence exists.

## Approval boundaries

Maintainer approval is required before changing visibility, licensing, product
boundaries, data authority, write behavior, supported platforms, public API
stability, release signing, commercial promises, or any Pro/Brain integration.
External copyright-bearing contributions remain merge-blocked until a
lawyer-reviewed contributor agreement or equivalent grant exists. Commit, push,
pull request, merge, package publication, sale, and release remain separate
actions.

## Delivery gates and dependencies

Each milestone produces a reviewable commit, tests, documentation, and an
evidence note. A gate is complete only when the exact command, commit, platform,
and result are recorded.

1. **Foundation:** repository policy, licence map, ownership, fork-safe CI,
   threat boundary, and public roadmap. Exit: the foundation validator and
   hosted checks pass on the exact PR head.
2. **Contracts:** Parser and Plumber compatibility surfaces, fixtures, version
   policy, and failure semantics. Depends on Foundation. Exit: contract tests
   run from public dependencies only and reject unsupported versions.
3. **Core:** smallest deterministic Community Trama runtime with bounded filesystem
   access. Depends on Contracts. Exit: unit, integration, determinism, and
   containment tests pass on every supported platform claimed.
4. **Adapters:** OG and read-only DB capability probes plus explicit unsupported
   cases. Depends on Core. Exit: sanitized fixtures prove provenance and native
   source authority without implicit writes.
5. **Nodi:** identity, truthful state model, accessible rendering contract, and
   deterministic fixtures. Depends on Core. Exit: accessibility and state
   transition tests pass without private services or graph-content telemetry.
6. **Distribution:** reproducible Community artifacts, provenance, documentation,
   and contributor onboarding. Depends on qualified Core, adapters, and Nodi.
   Exit: clean release rehearsal from a signed tag with SBOM and attestation.

## Validation and publication rules

Pull-request checks use no repository secrets and never execute fork code with
elevated privileges. Release jobs rebuild from trusted tags rather than promote
untrusted PR artifacts. Public artifacts contain no Pro, Brain, vault, local
path, credential, model-weight, generated database, or historical-export data.
Every completion claim binds the exact commit, command, platform, and result.

## Repository settings evidence

On 2026-08-31, GitHub API verification reported Discussions enabled, wiki
disabled, secret scanning enabled, push protection enabled, Dependabot
vulnerability alerts and security updates enabled, and private vulnerability
reporting enabled. These settings are mutable remote state and must be
reverified at release and security-review gates.

## Cost-aware delegation

Use deterministic checks before language models. Delegate bounded inventory,
documentation maintenance, and mechanical changes to the cheapest capable
worker. Retain architecture, licensing, security, integration, release, and
final evidence judgment with the maintainer or primary orchestrator.

## Interruption and recovery

Before a restart or handoff, record repository, worktree, branch, exact HEAD,
dirty state, completed checks, unproven gates, remote branch/PR state, and the
next safe command. Preserve changes in a reviewable commit when authorized;
never rely on a temporary worktree as the only copy.

## Completion checklist

- [ ] Public source-available Community and commercial boundaries are explicit in README, governance, and ADRs.
- [ ] PolyForm Noncommercial coverage, Required Notice, and third-party licence boundaries are machine-checkable.
- [ ] External contribution merging is gated until dual-path rights are legally established.
- [ ] Logseq OG and DB authority models are distinct and explicit.
- [ ] Parser, Plumber, Brain, Pro, and Nodi ownership boundaries are explicit.
- [ ] Fork-safe CI and private vulnerability reporting are enabled and proven.
- [ ] Each roadmap phase has dependencies and exact exit evidence.
- [ ] No legacy history, secret, vault, private path, or generated database was imported.
- [ ] Foundation changes are committed, pushed, reviewed, and merged through a green PR.

Commercial Pro source, pricing promises, payment acceptance, or private overlays
require a new ADR covering licensing, legal and tax review, security, build
isolation, contribution rights, and user-visible behavior.
