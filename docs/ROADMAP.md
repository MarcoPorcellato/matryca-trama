# Matryca Trama Roadmap

This roadmap summarizes the canonical
[delivery program](specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md). Status is
evidence-bound: `origin/main` was `9905e8a` when this roadmap was prepared,
while the existing qualification record binds `862c5c8`. Reverify both before
delivery. PR #14 is a mutable DB-boundary proposal, not evidence until its live
head is reviewed and integrated.

| Milestone | Outcome | Current status |
|---|---|---|
| V0 — Truth reconciliation | One claim ledger reconciles code, contracts, docs, evidence, and unsupported behavior. | **Next.** Bounded Python source exists, but current docs and evidence require reconciliation. |
| V1 — Current-head qualification | Locked local and hosted suites qualify one exact head without circular evidence claims. | **Blocked by V0.** Baseline evidence exists only for `862c5c8`. |
| V2 — Contract freeze | `trama.logseq.read/v1`, version ranges, provenance, errors, and fixture ownership become stable. | **Partially implemented; not frozen.** |
| V3 — Parser public profile | Exact public Parser versions and package-root APIs are qualified. | **Planned.** No production interoperability claim. |
| V4 — Plumber consumer profile | Exact Trama, Parser, and Plumber revisions pass public-envelope consumer tests. | **Partially implemented locally; cross-repository qualification absent.** |
| V5 — Operational OG profile | Sanitized OG fixture classes prove contained, deterministic reads beyond the minimal vectors. | **Not started.** No user-vault claim. |
| V6 — Logseq DB read-only profile | One official versioned host route supplies capability-probed native DB reads. | **Blocked.** No DB host surface selected or qualified. |
| V7 — Nodi vertical slice | Truthful deterministic state and accessible offline experience. | **Not started.** |
| V8 — Agent and plugin safety | Default-deny capabilities, provenance, previews, recovery, and adversarial evaluations. | **Not started.** |
| V9 — Reproducible distribution | Repeatable Community artifacts, SBOM, checksums, attestations, support matrix, and rollback rehearsal. | **Not started.** |
| V10 — Community release | Publish only qualified profiles and platforms under explicit maintainer authority. | **Blocked by V0–V9 and separate release approval.** |

## Deferred capabilities

Writes, events, Shadow acceleration, synchronization, export, recovery,
commercial entitlements, Pro, Brain, hosted services, and external
copyright-bearing contributions remain outside current delivery. Each requires
its own ADR or contract, threat and rights review, executable evidence, and
explicit authorization.

Work proceeds through one reviewable vertical milestone at a time. Every status
change binds an exact revision, scope, command, platform, result, limitation,
and durable evidence location.
