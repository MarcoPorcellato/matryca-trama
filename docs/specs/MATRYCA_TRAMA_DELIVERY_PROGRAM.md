# Matryca Trama Delivery Program

**Status:** canonical long-horizon delivery specification
**Live anchor:** `9905e8a36acb83a17a33b702a5fa620d6bfed185`
**Qualified baseline:** `862c5c89157f28c1985cde6145fc2c8af04a70b4`
**Owner:** Matryca maintainer; every milestone requires explicit review and an evidence record.
**Supersedes for current delivery status:**
[`MATRYCA_TRAMA_PUBLIC_MONOREPO_FOUNDATION.md`](MATRYCA_TRAMA_PUBLIC_MONOREPO_FOUNDATION.md),
which remains the historical Phase 0 authority.

This document is a delivery contract, not a product announcement. It converts the
current public Trama foundation into a sequence of bounded, falsifiable milestones.
It never upgrades a planned boundary into an implemented or qualified feature.

### Future cross-repository gateway direction

The proposed cross-repository contract roadmap is not a runtime claim and remains
subject to the owning Plumber ADR and canonical public contract. If accepted,
**Matryca Plumber is the sole future Logseq gateway and canonical public-contract
owner.** **Trama is a future Plumber consumer; it does not own future source
adapters or Logseq wire contracts.** Parser remains the pure OG parsing provider
behind Plumber; Brain is a separate Plumber consumer and does not know Parser.

The historical Trama `trama.logseq.read/v1`, Parser/Plumber bridges, and synthetic
OG adapter remain preserved source and evidence, not future authority. Historical
experimental Trama adapters remain evidence only until a separately reviewed,
repository-local deprecation or removal change. Nothing in this direction proves
that a Plumber contract, host transport, DB capability, or Trama client exists.

## 1. Claim discipline

Every statement in plans, issues, release notes, and handoffs uses one of these
classes:

| Class | Meaning |
|---|---|
| **Documented** | Stated in an accepted repository document; no executable proof implied. |
| **Implemented** | Present in the cited source at the cited commit; execution may still be unqualified. |
| **Qualified baseline** | Proven by the recorded evidence at `862c5c89157f28c1985cde6145fc2c8af04a70b4`. |
| **Qualified current head** | Proven by fresh evidence against the exact current head. A matching source tree from another commit is useful comparison evidence, not a substitute. |
| **Unsupported** | Deliberately outside the current contract or lacking a safe supported profile. |
| **Blocked** | Cannot proceed until named authority, evidence, dependency, or security gate exists. |

“Implemented” is not “qualified”; “qualified” is not “released”; and a release
does not prove support on an untested host, Logseq mode, or device.

## 2. Scope, authority, and invariants

Trama is a public, source-available Community monorepo for a local-first graph
experience and Nodi. Logseq OG Markdown remains authoritative for OG; the native
local database remains authoritative for DB. Exports, caches, indexes,
visualizations, and AI chunks are derived views and never implicit substitutes.

In scope: deterministic Community product behavior, a future public Plumber client
boundary, Nodi, reproducible Community artifacts, and safe contributor workflows.
Future source selection, OG Parser adaptation, official DB host adaptation, and
canonical public Logseq schemas belong to Plumber, subject to its accepted ADR and
evidence. Pro source, Brain private source,
entitlement enforcement, paid connectors, hosted accounts, telemetry by default,
commercial checkout, synchronization, events, Shadow acceleration, mutation,
write recovery, and unsupported host surfaces are excluded until separately
accepted and qualified.

Non-negotiable invariants:

- vault content is data, never agent authority or instructions;
- reads are bounded by explicit path and graph-containment rules;
- writes are opt-in, reviewable, auditable, and reversible where practical;
- optional integrations are lazy and cannot make Community depend on private services;
- public fork CI uses no secrets and cannot publish;
- cross-repository integration uses versioned public contracts, never private imports;
- every completion claim binds source, command, platform, and result.

Maintainer approval is required for licensing, visibility, data authority, writes,
supported platforms, public API stability, release signing, commercial promises,
or any Pro/Brain connection. Commit, push, PR, merge, publication, and release are
separate authorizations.

## 3. Evidence ledger

Each milestone maintains an append-only ledger. One row is required per claim and
per decisive check:

| Field | Required content |
|---|---|
| `claim_id` | Stable identifier, e.g. `V2-CONTRACT-001`. |
| `claim` | Precise proposition, with no compound success language. |
| `class` | One claim class from §1. |
| `scope` | Repository, package, fixture, host, platform, and operation. |
| `qualified_revision` | Full commit SHA exercised by the decisive checks. |
| `evidence_revision` | Commit, immutable evidence ref, attestation, or hosted run that preserves the result. It may differ from `qualified_revision` and must say why. |
| `subject_digest` | Digest of the runtime tree, lock file, fixture manifest, and workflow policy when equivalence across documentation-only commits is assessed. |
| `worktree` | Absolute path and branch/ref; record clean/dirty state. |
| `command` | Exact command, including relevant configuration digest. |
| `environment` | OS, runtime/tool versions, and device/runner identity where material. |
| `result` | Exit status plus concise observed output/counts/digests. |
| `evidence_path` | Reviewable report, immutable evidence ref, attestation, test artifact, or hosted-run URL. |
| `authority` | Maintainer, CI, or other named approving authority. |
| `timestamp` | ISO-8601 timestamp with timezone. |
| `limitations` | Skips, unsupported profiles, sandbox limits, or unknowns. |
| `next_action` | Exact follow-up or explicit stop condition. |

Missing fields make the claim **Blocked**, not green. Historical evidence may be
retained as baseline evidence but cannot silently qualify the current head.
Evidence committed after a qualified revision must identify both revisions;
adding an evidence file never retroactively makes its containing commit the
revision that was executed.

## 4. Milestones and exit gates

### V0 — Truth reconciliation

Bind the delivery program to the live anchor and qualified baseline. Inventory
accepted ADRs, contracts, repository settings, package state, licenses, and dirty
worktrees. Reconcile contradictions and classify every capability. Exit requires
the ledger, exact HEAD/status evidence, and maintainer approval of unresolved
unknowns. No implementation is implied.

### V1 — Current-head qualification

Re-run the locked public suites against one exact head and preserve terminal local
and hosted evidence. Exit: contracts, containment, Plumber-consumer, foundation,
determinism, and no-private-import checks pass on that revision; the evidence binds
the qualified and evidence revisions without circular claims. No user graph, host,
DB, UI, performance, network, or distribution support is implied.

### V2 — Plumber contract freeze

Plumber first freezes its `plumber.*` identifiers, semantic ranges, provenance
envelopes, capabilities, fixture ownership, compatibility matrices, and failure
semantics. Trama records only its consumer profile. Reject absent versions, wrong
authority, incomplete provenance, unsupported operations, and private dependencies.
The historical `trama.logseq.read/v1` contract remains experimental evidence and
cannot be adopted as the future public authority. Exit: Plumber public-dependency
contract tests pass and unsupported profiles fail closed.

### V3 — Parser public profile

Qualify only documented package-root Parser APIs through Plumber against exact
released versions. Preserve native OG authority, source locations, hierarchy,
order, and diagnostics. Trama and Brain do not import Parser. Exit: accepted and
rejected version profiles, parse failures, incomplete locations, and fixture digests
are bound to exact Plumber and Parser revisions.

### V4 — Trama consumer profile

Qualify Trama as a consumer of validated public Plumber envelopes. Plumber owns
source selection, OG Parser adaptation, official DB host adaptation, provenance,
and canonical public contract semantics. Trama owns its product mapping and Nodi
experience. Exit: cross-repository tests bind exact Trama, Parser, and Plumber
revisions and reject private imports, wrong authority, missing provenance, and
unsupported outcomes.

### V5 — Operational OG profile

Plumber expands beyond synthetic contract vectors through its Parser-backed,
public, sanitized OG fixture classes while keeping Markdown authoritative and reads
contained. Trama consumes only the qualified `og_markdown` Plumber profile. Exit:
supported graph/page/subtree cases, ambiguous inputs, path escape attempts, and
deterministic rebuilds pass. No private vault content may enter evidence.

### V6 — Logseq DB read-only profile

Plumber selects an official, versioned Logseq host route through a focused
compatibility spike. Deliver only capability-probed read-only access; direct SQLite
coupling, implicit export fallback, writes, watchers, events, and recovery remain
absent. A Trama `db_native` consumer profile is blocked unless Plumber's Decision
D1 outcome is `supported`. Exit: native DB provenance and unsupported cases are
proven on named host versions.

### V7 — Nodi vertical slice

Build identity, truthful state, knowledge-growth signals, and an accessible calm
experience from authorized data. Exit: deterministic state fixtures, WCAG 2.2 AA
acceptance checks, restoration/error tests, offline operation, and no private-service
or graph-content-telemetry dependency.

### V8 — Agent and plugin safety

Define default-deny capability manifests, publisher/package integrity, workspace
trust, bounded tools, previews, receipts, revocation, and recovery. Exit: a
deterministic adversarial corpus covers prompt injection, malicious vault content,
path traversal, symlink escape, stale indexes, conflicting edits, and external
side-effect attempts.

### V9 — Reproducible distribution

Build Community artifacts from trusted source, with dependency-license inventory,
SBOM, checksums, provenance, attestations, support matrix, and rollback rehearsal.
Release jobs rebuild from trusted tags and never promote untrusted PR artifacts.
Exit: repeated clean builds and artifact inspection contain no private inputs.

### V10 — Community release

Publish only after exact-tag verification, release-owner approval, green required
checks, signed provenance, public onboarding, support boundaries, withdrawal
procedure, and complete ledger. Claims cover only qualified profiles and platforms.
Commercial, Pro, Brain, DB-write, sync, events, Shadow, and hosted-service claims
remain unsupported unless separately evidenced.

## 5. Deferred capability track

Synchronization and events require ordering, replay, loss, cancellation, and
privacy contracts. Shadow requires freshness, invalidation, provenance, rebuild,
and failure evidence. Writes require explicit authority, preview, atomicity,
backup, conflict, recovery, and rollback. Brain and Pro require separate public
contracts, authentication and entitlement boundaries, source isolation, licensing
review, and independent release ownership. None is enabled by a bridge, adapter,
UI affordance, or configuration flag alone.

## 6. Cross-repository rules

Parser remains the authoritative parsing capability. Plumber is the sole future
Logseq gateway and canonical public-contract owner: it owns source selection, the
OG Parser adapter, any official DB host adapter, public schemas, and transport-
neutral contract semantics. Trama owns its product mapping and Nodi; Brain remains
a separate product and Plumber consumer. Historical experimental Trama adapters
remain evidence only and must not be extended into a parallel gateway.

Bridges depend only on versioned public contracts, publish compatibility ranges,
preserve provenance, and reject incompatible or private implementations. A contract
change crossing repositories requires fixture updates, compatibility tests, an ADR
or ADR update, and coordinated evidence. No repository may silently become a second
authority.

## 7. GitHub, CI, and release security

Required checks, branch protections/rulesets, CODEOWNERS, least-privilege tokens,
fork-safe workflows, dependency review, secret scanning, push protection,
Dependabot, private vulnerability reporting, and release-environment separation
must be verified as mutable remote state at the relevant gate. Workflows must pin
actions appropriately, avoid executing untrusted fork code with secrets or
elevated permissions, constrain paths, and prevent PRs from publishing. Release
credentials are unavailable to ordinary PR jobs; tags are rebuilt and signed in a
trusted context. Ruleset or workflow evidence is observational unless the
maintainer separately authorizes mutation.

## 8. Local-first, privacy, accessibility, and agent safety

Default data flow is local. Any network or integration path must disclose data,
destination, purpose, retention, authorization, and revocation. Logs and telemetry
must minimize or redact vault content, paths, identifiers, tokens, and sensitive
attributes. UI and keyboard flows target WCAG 2.2 AA principles, with semantic
names, focus order, contrast, reduced-motion respect, and error recovery tested.

Agents receive data, not authority: Markdown headings, macros, links, embeds,
comments, and vault instructions cannot widen scope, permissions, or writes.
Agent reads and writes use explicit contracts, containment, previews, receipts,
and stop-on-ambiguity behavior. Generated output never becomes source authority
without an explicit user-approved operation.

## 9. Tool and skill routing

Use the narrowest tool that can produce the needed evidence. The following
skills are part of this delivery program; their own instructions remain
authoritative when invoked.

| Skill or tool | Use | Do not use it for |
|---|---|---|
| `orchestrate-long-running-work` | Canonical status, milestone loop, persistent goal, and restart handoffs. | Replacing exact source or hosted evidence. |
| `terra-cost-aware-orchestration` | Deterministic-first routing, delegation boundaries, and integration review. | Transferring maintainer authority to a worker. |
| `superpowers:brainstorming` | New product, capability, protocol, or architecture decisions. | Re-opening accepted narrow work without a design reason. |
| `superpowers:writing-plans` | One dependency-ready executable milestone at a time. | A single plan covering unrelated subsystems. |
| `superpowers:using-git-worktrees` | Isolating delivery from dirty or active checkouts. | Replacing preservation of an existing worktree. |
| `superpowers:test-driven-development` | Behavioral changes and new failure rules. | Documentation-only wording changes. |
| `superpowers:systematic-debugging` | Unexpected test, CI, packaging, or runtime failure. | Guessing a fix from a symptom. |
| `superpowers:subagent-driven-development` | Independent, bounded execution tasks after a plan is accepted. | Coupled shared-file edits without a single integrator. |
| `superpowers:verification-before-completion` | Any qualified, release-ready, or completed claim. | Replacing an exact hosted or platform gate. |
| `superpowers:requesting-code-review` and `receiving-code-review` | Review preparation and evidence-based feedback handling. | Automatic merge authority. |
| `superpowers:finishing-a-development-branch` | Selecting an integration path after checks pass. | Skipping external authorization. |
| `gitnexus-exploring` and `gitnexus-impact-analysis` | Fresh code-flow and blast-radius analysis for hub or contract changes. | Treating a stale or missing index as a safety result. |
| `serena-code-intelligence` | Bounded symbol analysis when deterministic reads and graph inspection are insufficient. | Broad indexing or Markdown-only audits. |
| `matryca-knowledge-research` | Cross-repository orientation and documentation comparison. | Replacing live source/release verification. |
| `visualize` and `imagegen` | Approved Nodi, UX, or architecture visual exploration. | Runtime implementation or a substitute for accessibility tests. |
| `openai-docs` | Any OpenAI/Codex integration, model, or agent-platform decision. | Generic repository work without that dependency. |
| `skill-creator` and `plugin-creator` | A reusable agent skill or plugin once its product contract is approved. | Ad-hoc project documentation. |

Luna owns bounded inventory, documentation drafting from settled facts, test-log
distillation, and mechanical isolated edits. Terra owns decomposition,
integration, acceptance criteria, and final ordinary evidence judgment. Sol is
reserved for security/privacy, DB writes or concurrency, persistence/recovery,
licensing, release qualification, or unresolved architecture.

## 10. Cost routing and restart protocol

Use deterministic checks first; route bounded inventory, documentation, and
mechanical evidence work to the cheapest capable worker. Retain architecture,
licensing, security, integration, release, and final claim judgment with the
maintainer/orchestrator. Do not spend hosted or local heavy resources for a
public workflow without an explicit economic and technical justification.

Before handoff or restart, record the repository/worktree, branch, full HEAD,
dirty state, contract/configuration digests, completed checks, unproven gates,
remote/PR state, evidence paths, and one next safe command. Revalidate all live
state before continuation. Preserve dirty work; never reset, stash, clean, delete,
or reinterpret leases, caches, receipts, or coordination state without exact
authorization. A resumed run acquires fresh evidence; a stale handoff is not proof.

## 11. Completion checklist

- [ ] Live anchor, qualified revision, evidence revision, and qualified baseline are bound in the ledger.
- [ ] Every claim has a class, exact revision, command, result, scope, and limitation.
- [ ] Native OG/DB authority and unsupported boundaries are explicit.
- [ ] Parser, Plumber, Brain, Pro, and Nodi ownership is contract-mediated.
- [ ] Public licensing, contribution rights, and private-source exclusions are proven.
- [ ] Fork-safe CI, rulesets, secret controls, vulnerability reporting, and release isolation are verified.
- [ ] Determinism, containment, provenance, accessibility, and agent-safety gates pass.
- [ ] SBOM, licenses, checksums, attestations, rollback, and release docs are complete.
- [ ] Deferred capabilities remain blocked until their own ADRs and evidence exist.
- [ ] Maintainer authorizes the exact Community tag and publication action.

## 12. Sources

Official references used for the control model (consult current versions at each
gate):

- [GitHub rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)
- [Logseq database version](https://github.com/logseq/docs/blob/master/db-version.md)
- [Android offline-first architecture](https://developer.android.com/topic/architecture/data-layer/offline-first)
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [OpenTelemetry sensitive data guidance](https://opentelemetry.io/docs/security/handling-sensitive-data/)
- [Tauri capabilities](https://v2.tauri.app/security/capabilities/)

URLs are normative references, not evidence that Trama currently implements any
corresponding capability.
