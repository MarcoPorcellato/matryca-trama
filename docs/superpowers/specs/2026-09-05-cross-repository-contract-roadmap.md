# Matryca Trama Cross-Repository Contract Roadmap

> **Status:** proposed long-horizon execution authority for maintainer review.
> **Canonical responsibility contract:**
> [`docs/contracts/ECOSYSTEM_RESPONSIBILITY_AND_CHANGE_CONTRACT.md`](../../contracts/ECOSYSTEM_RESPONSIBILITY_AND_CHANGE_CONTRACT.md)

## Outcome

Deliver the best evidence-backed Community roadmap for Matryca Trama while
keeping Parser, Plumber, Brain, and Knowledge responsibilities separate. The
programme succeeds when Trama has a useful, independently operable,
architecture-enforced read-only Community vertical, or when an honest
capability result proves that the selected Logseq DB route is currently a
NO-GO or upstream-blocked.

No milestone may obtain a green result by duplicating another repository's
implementation, weakening native source authority, importing private code, or
turning a planned report into a runtime claim.

## Verified starting point — 2026-09-05

| Repository | Verified `origin/main` | Relevant observed state |
| --- | --- | --- |
| Matryca Trama | `9905e8a36acb83a17a33b702a5fa620d6bfed185` | `trama.logseq.read/v1` and synthetic OG packages exist; exact hosted evidence qualifies only three read operations over owned synthetic fixtures |
| Matryca Plumber | `d347d43dad090586b10a77a53c4e0c8fd6da8e15` | DB compatibility execution plan is current; consumer evidence policy remains unchecked and its files are absent |
| Logseq Matryca Parser | `65e8e64f7f0227bcae8235069fbc3da834652744` | public package-root API is stable; version source reports `1.8.2` |
| Matryca Brain | `e69a97a8c702a773c9a3ce8307b5a667ed2be1dd` | separate product; optional Trama boundary remains research/strategy, not a runtime claim |
| Matryca Knowledge | `52500d623feecd2ec156e653be9d521383740ddb` | read-only coordination projection; Trama is not a managed source and direct source remains authoritative |

Live planning surfaces were also checked. Trama issues #2, #4, and #9,
Plumber issues #490 and #491, and Brain issue #430 were open. Issue state is
mutable and MUST be reverified before any issue or milestone update.

## Reconciled facts, proposals, and unknowns

### Facts

- The exact Trama qualification commit is
  `862c5c89157f28c1985cde6145fc2c8af04a70b4`, tree
  `f1dacc9b30c993b2b69a48c20e73281732e781b3`.
- It qualifies only `graph.identify`, `page.read`, and complete ordered
  `block.subtree.read.complete` for synthetic OG fixtures.
- The lock contains Parser `1.8.2`, within Trama and Plumber's declared Parser
  range `>=1.7.1,<2.0.0`.
- Trama's reference Plumber admission helper accepts Plumber `2.0.0`; current
  Plumber source reports `2.0.1rc3`. Cross-repository compatibility with that
  prerelease is unproven.
- No user graph, Logseq DB host, app, Nodi UI, event stream, DB-source Shadow,
  synchronization, write path, distribution, performance, or network behavior
  is qualified by the Trama evidence.
- External copyright-bearing contributions remain merge-blocked until a
  lawyer-reviewed contributor agreement or equivalent grant exists.

### Proposals

- The current Plumber plan proposes a consumer evidence profile first, then a
  Trama official-host capability spike, followed by a transport decision.
- The product strategy proposes Community, later Pro, separate Brain, and later
  Teams. It is not pricing, entitlement, source-location, or bundle authority.
- Nodi is the intended central Trama experience, but its presentation-state
  contract and runtime remain to be designed and qualified.

### Unknowns that block claims

- Whether one exact official Logseq host surface can preserve graph identity
  and return a complete ordered subtree without forbidden state change.
- Which Plumber release or prerelease should become the first supported Trama
  consumer profile.
- Whether a future Trama--Brain connection should exist and, if so, its public
  authentication, consent, revocation, data-flow, and entitlement semantics.
- The Community/Pro feature boundary, commercial terms, and source/package
  location for Pro.

## Execution model

There is one active cross-repository mutating lane. The owner change merges
before the dependent consumer branch starts. Separate repositories never share
a working branch or PR.

```text
R0 contract authority
  -> R1 Clean Architecture enforcement
  -> R2 Plumber consumer evidence policy
  -> R3 Trama official-host capability spike
  -> D1 transport selection or stop
  -> R4 contract/profile freeze
  -> R5 Trama adapter and companion shell
  -> R6 Plumber session consumer
  -> R7 exact-version qualification
  -> R8 Nodi read-only vertical
  -> R9 Community distribution
```

Read-only research, report inventory, and non-overlapping documentation MAY run
in parallel. Schema, transport, adapter, session-routing, authority, and product
changes remain serial.

## Milestones

### R0 — Accept ownership and roadmap authority

**Owner:** Matryca Trama.
**Tracking:** Trama #2, #8, #9.
**Scope:** this roadmap, the responsibility contract, current-state corrections,
and the restart-safe persistent goal.

Exit evidence:

- one canonical owner for every shared contract;
- accepted anti-duplication and change protocol;
- current source anchors and known drift recorded;
- `docs/ROADMAP.md`, contract index, and persistent goal point here;
- documentation and whitespace checks pass.

Stop before commit, push, issue mutation, PR, or merge unless separately
authorized.

### R1 — Make Clean Architecture enforceable

**Owner:** Matryca Trama.
**Tracking:** Trama #9.
**Dependency:** R0 accepted.

Deliver a focused design and implementation plan for stack-independent and
Python-specific rules. Then add, in small PRs:

- repository-owned architecture and coding standards;
- deterministic dependency/import boundary checks;
- contract and negative tests for public boundaries;
- a repository-local development skill that points to canonical documents;
- a thin personal discovery skill that locates the repository skill without
  copying policy;
- contributor and review guidance, with documented, time-bounded exceptions.

The design MUST update issue #9's stale statement that the application stack is
unselected: ADR-0004 and Python packages now exist. The enforcement may not
change runtime behavior or widen supported scope.

Exit evidence: exact-head checks reject at least one fixture for each forbidden
dependency direction; the repository-local skill passes its tests; public CI is
fork-safe; documentation contains no duplicate normative policy.

### R2 — Freeze Plumber consumer evidence policy

**Owner:** Matryca Plumber.
**Tracking:** Plumber #490 and #491.
**Dependency:** R1 architecture rules accepted; exact live heads reverified.

Execute Task 3 of Plumber's current DB compatibility plan. Create only the
outer consumer admission profile, unverified and negative fixtures, tests, and
baseline report. Reference exact Trama `trama.logseq.read/v1`; do not copy its
wire schema, import Trama source, or claim DB support.

Exit evidence: malformed, unpinned, incomplete, direct-database, mutating,
foreign-session, stale-session, and unbounded evidence fails closed; focused
tests and Plumber's full CI pass; the baseline labels DB capability unverified.

### R3 — Execute official-host capability spike

**Owner:** Matryca Trama.
**Tracking:** Trama #4 and Plumber #491.
**Dependency:** R2 merged and pinned.

Use a disposable synthetic DB graph. Probe only a documented, exact official
host artifact. Candidate order is bundled CLI, official plugin SDK, then MCP
stdio. A candidate advances only when the previous candidate fails a required
contract property. MCP HTTP is outside this plan.

Required proof:

- exact artifact, embedded revision, platform, fixture, command, and evidence
  digests;
- explicit graph selection and stable DB binding;
- app-open and app-closed parity without current-graph switching;
- exact page identity and complete ordered descendant structure;
- bounded output, timeout, stderr, and process lifecycle;
- unchanged graph, configuration, and server ownership fingerprints;
- no user graph, internal `db.sqlite`, mutation, sync, import, export, arbitrary
  query, or automatic server replacement.

Running a downloaded host artifact is a separate authorization gate. A
synthetic unit test is not host qualification.

### D1 — Select transport or stop

**Decision owner:** primary maintainer workflow.
**Dependency:** R2 and R3 terminal evidence.

Valid outcomes:

- `cli_supported`;
- `plugin_sdk_supported`;
- `mcp_stdio_supported`;
- `capability_no_go`;
- `upstream_blocked`.

No production adapter branch starts before D1. The selected outcome and exact
evidence MUST be recorded in Trama and referenced by Plumber. A NO-GO is a valid
terminal result and MUST NOT be bypassed with a partial adapter.

### R4 — Freeze selected contract and security profiles

**Owner sequence:** Trama contract first; Plumber consumer/security profile
second in a separate PR.
**Tracking:** Trama #2; Plumber #493.
**Dependency:** a supported D1 outcome.

Prefer a backward-compatible source-mode profile under
`trama.logseq.read/v1`. Introduce a new major only if semantics break v1.
Freeze graph/session identity, page and subtree fields, capabilities,
provenance, bounds, errors, pairing if applicable, scopes, revocation, and
privacy-safe receipts. Each consumer pins the exact owner commit and fixture
digest.

Exit evidence: owner and consumer suites accept the same positive vectors and
reject unknown versions, missing provenance, bad digests, incomplete subtrees,
foreign bindings, stale sessions, and unsupported capabilities.

### R5 — Build the single Trama read-only adapter and shell

**Owner:** Matryca Trama.
**Tracking:** Trama #4.
**Dependency:** R4 merged.

Implement only the selected official host adapter and a thin dual-mode
Community composition shell. Preserve the existing synthetic OG behavior. Do
not implement Plumber services, Brain connectivity, events, Shadow, or writes.

Exit evidence: deterministic OG/DB mode detection, graph identity, page and
complete-subtree reads, explicit unsupported results, content-free health, no
private imports, and unchanged source authority.

### R6 — Add Plumber's session consumer

**Owner:** Matryca Plumber.
**Tracking:** Plumber #17 and #493.
**Dependency:** exact R5 Trama artifact/profile.

Add a transport-neutral `GraphSessionReadPort` and session routing. Keep the
filesystem `GraphReadPort`, OG/Shadow selection, daemon, CLI, and MCP behavior
unchanged. Route graph identity first, one page second, and one complete subtree
third as independent reviewable slices.

Exit evidence: every slice passes fail-closed session tests and existing
OG/Shadow regression gates. A DB graph never falls back to Markdown.

### R7 — Publish exact experimental compatibility

**Owner sequence:** Trama evidence first, then Plumber consumer evidence.
**Tracking:** Trama #2/#4; Plumber #490/#491.
**Dependency:** R5 and R6.

Publish one exact-version matrix for host artifact, Trama, Parser, Plumber,
contract/profile, fixtures, platforms, limitations, and evidence digests.
Stable `2.0.0` and prerelease `2.0.1rc3` remain separate rows.

Exit evidence: clean-install and hosted gates are terminal green at unchanged
commits; documentation labels support experimental and names exclusions.

### R8 — Deliver the first Nodi read-only vertical

**Owner:** Matryca Trama.
**Tracking:** Trama #5.
**Dependency:** qualified Community core and read adapters.

Define C5 before UI implementation. Deliver one small end-to-end experience
using only user-authorized read data and deterministic presentation states.
Nodi must remain useful without Brain, Pro, network services, or telemetry.

Exit evidence: deterministic state fixtures, accessibility checks, explicit
empty/loading/unsupported/error states, and no concrete host dependency in the
presentation model.

### R9 — Community distribution

**Owner:** Matryca Trama.
**Tracking:** Trama #6.
**Dependency:** R8 and exact supported-platform evidence.

Prepare reproducible Community artifacts, provenance, examples, onboarding,
support matrix, and release documentation. Publication, tags, packages, and
releases remain separate external authorization gates.

## Deferred programmes and re-entry gates

| Programme | Re-entry gate |
| --- | --- |
| Events and convergence | R7 complete; accepted cursor/gap/order/reconnect/resync contract |
| DB-source Shadow | snapshot and event semantics qualified; accepted generation/freshness/rebuild/fallback design |
| Host-authoritative DB writes | official expected-revision or equivalent atomic conflict evidence; accepted preview/recovery/undo ADR |
| Optional Brain connection | Community standalone; compatible released contracts; accepted ADR-0002 profile; explicit auth/consent/revocation/data-flow/licensing tests |
| Pro/commercial packaging | separate product and legal decisions; no implicit source or entitlement placement |
| External copyright-bearing contributions | lawyer-reviewed contributor agreement or equivalent grant active |

These tracks are not autonomous implementation authority.

## Issue and roadmap hygiene

After R0 is accepted and GitHub mutation is explicitly authorized:

1. update Trama #9 to acknowledge ADR-0004 and the current Python packages;
2. update #2 and #4 acceptance text to distinguish the already-qualified
   synthetic OG slice from still-unqualified cross-repository and DB work;
3. assign #2--#6 and #9 to dependency-ordered milestones or a project view;
4. cross-link Plumber #490/#491/#493/#17 without duplicating their bodies;
5. keep Brain #430 deferred and non-blocking;
6. close an issue only when its documented exit evidence is terminal.

## Autonomous execution boundary

Autonomous work MAY perform read-only verification, maintain this plan, create
bounded public synthetic fixtures, add local tests and documentation, and run
safe repository-local checks when the current milestone authorizes them.

Stop for explicit authority before:

- commit, push, PR, issue/milestone/project mutation, merge, tag, release, or
  package publication;
- external download or execution of a Logseq artifact;
- user-graph, private-data, credential, or network-service access;
- DB writes, graph mutation, events, Shadow ingestion, or recovery actions;
- Brain integration, Pro/commercial source, entitlement, pricing, or licence
  changes;
- acceptance of external copyright-bearing contributions.

## Restart checkpoint

At every interruption record:

- repository, worktree, branch, exact HEAD/base, and dirty state;
- current milestone and owning repository;
- exact source, artifact, fixture, profile, and evidence digests;
- focused and full checks with terminal outcomes;
- unproven claims and the next dependency;
- whether an external authorization gate is pending.

Never infer completion from branch names, reports, cached indexes, or delegated
summaries. Reverify exact bytes and live planning state.

## Source anchors

- `matryca-trama@9905e8a36acb83a17a33b702a5fa620d6bfed185:docs/spikes/evidence/python-read-contract-v1/862c5c89157f28c1985cde6145fc2c8af04a70b4.md`
- `matryca-trama@9905e8a36acb83a17a33b702a5fa620d6bfed185:docs/ROADMAP.md`
- `matryca-plumber@d347d43dad090586b10a77a53c4e0c8fd6da8e15:docs/superpowers/plans/2026-09-01-logseq-db-read-only-compatibility.md`
- `logseq-matryca-parser@65e8e64f7f0227bcae8235069fbc3da834652744:docs/reference/API_STABILITY.md`
- `Matryca-per-Delineat@e69a97a8c702a773c9a3ce8307b5a667ed2be1dd:docs/MATRYCA_TRAMA_BRAIN_PORTFOLIO_STRATEGY.md`
- `Matryca-knowledge@52500d623feecd2ec156e653be9d521383740ddb:README.md`
