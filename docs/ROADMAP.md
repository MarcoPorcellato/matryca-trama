# Matryca Trama Roadmap

The canonical dependency-ordered execution authority is the
[cross-repository contract roadmap](superpowers/specs/2026-09-05-cross-repository-contract-roadmap.md).
The [ecosystem responsibility and change contract](contracts/ECOSYSTEM_RESPONSIBILITY_AND_CHANGE_CONTRACT.md)
defines which repository owns each capability and how consumers change without
copying the owner.

## Current verified baseline

At Trama `9905e8a36acb83a17a33b702a5fa620d6bfed185`, the public Python workspace
implements `trama.logseq.read/v1` for owned synthetic OG fixtures. Hosted
evidence at commit `862c5c89157f28c1985cde6145fc2c8af04a70b4`
qualifies only:

- `graph.identify`;
- `page.read`;
- complete ordered `block.subtree.read.complete`.

User graphs, Logseq DB, writes, events, DB-source Shadow, synchronization,
export, recovery, app/UI/Nodi, distribution, performance, and network behavior
remain unsupported by that evidence.

## Delivery rule

Only one cross-repository mutating slice is active at a time. The owning
contract merges before a dependent consumer branch starts. Every repository
uses its own short-lived branch and PR; no long-lived integration branch or
multi-repository PR is allowed.

Disjoint read-only research and non-overlapping documentation may run in
parallel. Runtime, schema, adapter, session, authority, and product changes
remain sequential.

## Ordered programme

### Phase 0 — Public foundation and coordination

Maintain the public repository policy, PolyForm Noncommercial boundary,
contributor licensing gate, architecture, ADRs, contracts, roadmap, and
fork-safe CI. Accept the cross-repository responsibility contract and correct
stale planning surfaces before further runtime work.

Evidence: exact-head documentation checks; unambiguous ownership and authority;
no private or Pro source; no unsupported runtime claim.

### Phase 1 — Clean Architecture enforcement

Complete issue #9 before application expansion. Add repository-owned standards,
deterministic dependency/import checks, boundary tests, a repository-local
development skill, thin personal discovery, contributor guidance, and a
reviewed exception process. The skill points to canonical policy and does not
duplicate it.

The R1 implementation exists on its local branch only. It becomes a repository
qualification only after publication and fork-safe hosted CI records evidence
for the exact published head.

Evidence: forbidden dependency fixtures fail; allowed dependency fixtures pass;
the skill is tested; fork-safe CI enforces the stack-independent rules.

### Phase 2 — Shared compatibility evidence

First, Matryca Plumber owns and freezes its consumer evidence profile without
copying Trama's wire schema. Then Trama executes the official-host capability
spike. Parser remains the owner of its stable package-root API.

Evidence: exact version/profile matrix; accepted and rejected fixtures;
producer, source, binding, capability, bounds, uncertainty, and digest fields;
unsupported versions, missing provenance, direct-database access, mutation,
foreign sessions, and incomplete subtrees fail closed.

### Decision D1 — Select official host transport or stop

After the Plumber evidence policy and Trama capability spike are terminal,
select exactly one supported candidate: bundled CLI, official plugin SDK, or
MCP stdio. Otherwise record `capability_no_go` or `upstream_blocked` and build
no partial DB adapter.

### Phase 3 — Community core and Logseq adapters

After a supported D1 outcome, freeze the selected Trama profile, implement one
read-only host adapter and thin dual-mode composition shell, then add Plumber's
separate session consumer. Preserve the existing filesystem `GraphReadPort`
and OG/Shadow behavior. A DB graph never falls back to Markdown.

Evidence: stable graph binding, one page, one complete ordered subtree,
explicit failures, bounded lifecycle, zero forbidden state change, and exact
cross-repository hosted compatibility.

### Phase 4 — Nodi

Define the Trama-owned Nodi presentation-state contract, then deliver one small
read-only vertical. Nodi depends on public Community use cases, not concrete
host, Parser, Plumber, Brain, Pro, network, or telemetry implementations.

Evidence: deterministic states, accessibility checks, honest empty/loading/
unsupported/error presentation, and independent local Community operation.

### Phase 5 — Distribution and community

Prepare reproducible Community artifacts, provenance, support matrix, examples,
onboarding, and release documentation.

Evidence: clean release rehearsal and fork-safe hosted CI. Publication remains
a separate authorization gate.

## Deferred programmes

Events, DB-source Shadow, DB writes, Brain connection, Pro packaging,
entitlement, pricing, and commercial terms each require their own re-entry gate
defined by the canonical roadmap. No deferred capability enters Trama by
implication.

Repository-owned Community material remains under PolyForm Noncommercial
1.0.0. Commercial use requires a separate written agreement. External
copyright-bearing contributions remain merge-blocked until a lawyer-reviewed
contributor agreement or equivalent grant exists.
