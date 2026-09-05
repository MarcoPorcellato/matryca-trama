# Matryca Plumber Gateway and Cross-Repository Boundary Design

> **Status:** proposed architectural specification for maintainer review
>
> **Decision owner:** Marco Porcellato
>
> **Scope:** Logseq Matryca Parser, Matryca Plumber, and Matryca Trama;
> Matryca Brain is considered only as a separate downstream consumer.
>
> **Supersedes when accepted:** the unmerged direction that assigns Logseq host
> acquisition, OG/DB adapters, or `trama.logseq.read/v1` production to Trama.

## 1. Purpose and falsifiable outcome

This design gives each public repository one clear product responsibility and
one dependency direction. It prevents Parser, Plumber, and Trama from growing
parallel Logseq adapters, duplicate user interfaces, or incompatible graph
contracts.

The design succeeds when all of the following are true:

1. Logseq OG data reaches every downstream product only through Parser and
   Plumber.
2. Logseq DB data reaches every downstream product only through a qualified
   official Logseq adapter owned by Plumber.
3. Trama and Brain can use Plumber without importing Parser or knowing which
   source adapter produced a normalized graph result.
4. Parser remains a protocol-neutral parsing library without a product user
   interface.
5. Plumber retains a small operator console for monitoring, configuration, and
   governed maintenance operations.
6. Trama owns graph exploration, user-facing intelligence, analysis, and the
   full knowledge experience.
7. Contract, compatibility, provenance, and failure behavior are tested from
   exact released versions without private imports or copied implementations.

This document defines architecture and migration intent. It does not claim that
the new contracts, adapters, UI boundaries, Logseq DB support, performance, or
distribution are implemented or qualified.

## 2. Verified starting anchors

The following remote anchors were fetched and verified on 2026-09-05:

| Repository | `origin/main` | Relevant observed state |
| --- | --- | --- |
| Matryca Trama | `70fc14c27b11e31e8f557fd70684b6a83933e7d6` | Contains the experimental `trama.logseq.read/v1` producer, Parser bridge, OG adapter, and Plumber consumer helper. These are not published production interfaces. |
| Matryca Plumber | `af9b1dfb1cf89e2a4160020ce565be3f617be16a` | Already owns the OG Parser-backed runtime, CLI, MCP, daemon, Shadow read path, and Sovereign UI. Its current DB plan incorrectly assigns Logseq host acquisition to Trama. No Logseq DB execution or support claim exists. |
| Logseq Matryca Parser | `65e8e64f7f0227bcae8235069fbc3da834652744` | Owns the stable package-root parsing API and still exposes LENS through documentation and the `visualize` CLI. |

Matryca Knowledge observed Brain public source at
`e69a97a8c702a773c9a3ce8307b5a667ed2be1dd`. This is a coordination reference,
not an implementation anchor for this three-repository programme. Brain state
must be fetched and reverified before M7 begins.

The active Trama design worktree is clean at
`a0699e4db6fd49a5413207afd70fce006c377e85` before this specification edit.
It is based on an older Trama main and must be reconciled with the verified
remote anchor before publication. Existing local work and commits must not be
reset, rewritten, or discarded during that reconciliation.

## 3. Accepted product topology

### 3.1 Data flow

```text
Logseq OG Markdown
        |
        v
Logseq Matryca Parser
        |
        v
Matryca Plumber
        +-------------------+
        |                   |
        v                   v
Matryca Trama          Matryca Brain

Logseq DB official host surface
        |
        v
Matryca Plumber
        +-------------------+
        |                   |
        v                   v
Matryca Trama          Matryca Brain
```

### 3.2 Compile-time and runtime dependency direction

```text
Trama -----> Plumber public contracts
Brain -----> Plumber public contracts
Plumber ---> Parser public API                 (OG only)
Plumber ---> qualified official Logseq surface (DB only)
```

The following dependencies are forbidden:

- Trama to Parser;
- Brain to Parser;
- Trama to Logseq storage or host APIs;
- Brain to Logseq storage or host APIs;
- Parser to Plumber, Trama, or Brain;
- Plumber to Trama or Brain implementation code.

An invocation starts with Trama, Brain, CLI, MCP, or the Plumber Operator
Console and enters Plumber. For an OG session, Plumber selects its Parser
adapter. For a DB session, Plumber selects its official-host adapter. The
consumer sees only Plumber's stable result and never selects or invokes Parser.
Parser identity, exception types, and internal diagnostics must not leak through
public consumer DTOs or error codes.

## 4. Repository responsibilities

### 4.1 Logseq Matryca Parser

Parser owns:

- deterministic Logseq OG Markdown parsing;
- AST, block hierarchy, page identity, references, properties, diagnostics,
  serialization, and source locations;
- bounded filesystem discovery and parsing rules;
- a stable, documented package-root Python API;
- Parser-owned conformance fixtures and semantic-version policy.

Parser does not own:

- native Logseq DB access;
- MCP, network, daemon, or product orchestration;
- Plumber configuration or maintenance policy;
- Trama or Brain intelligence;
- a long-term end-user graph interface.

LENS remains historical Parser functionality during a deprecation window. It
must not be copied into Trama. Its CLI and optional dependencies require a
separate compatibility, provenance, and semantic-version review before removal.

### 4.2 Matryca Plumber

Plumber is the sole Logseq gateway for Matryca products. It owns:

- source-session selection and graph binding;
- the OG adapter that invokes Parser through its public API;
- the DB adapter that invokes only a qualified official Logseq host surface;
- normalization from source-specific representations into Plumber contracts;
- read, topology, navigation, control, and later mutation use cases;
- CLI, MCP, daemon, safety, OCC, locks, Shadow, and receipts;
- a small Operator Console for health, configuration, jobs, and governed
  maintenance options;
- canonical public schemas, fixtures, version policy, and compatibility tests
  for Plumber contracts.

Plumber does not own:

- Trama's graph-exploration experience;
- semantic explanations or knowledge intelligence presented to users;
- Nodi;
- Brain's private reasoning, RAG, or workspace implementation;
- an alternative visualization product competing with Trama.

### 4.3 Matryca Trama

Trama owns:

- the approachable end-user knowledge application;
- graph visualization, exploration, filtering, and navigation;
- semantic analysis, intelligence, explanations, and knowledge workflows;
- Nodi and Trama presentation state;
- preview and approval experiences for intelligent gardening suggestions;
- an internal domain port implemented by a Plumber client adapter;
- future desktop composition and distribution decisions.

Trama does not own:

- Parser integration;
- Logseq OG filesystem access;
- native Logseq DB access;
- Plumber daemon, safety, Shadow, configuration, or receipts;
- public Plumber transport schemas.

### 4.4 Matryca Brain

Brain remains a separate product and repository. It may later consume released
Plumber contracts directly. It must not depend on Trama or Parser to obtain a
Logseq graph. Brain-specific authentication, consent, entitlements, caches, and
release behavior remain separate decisions.

## 5. Clean Architecture inside Plumber

Plumber separates driving adapters, application use cases, internal ports, and
source adapters:

```text
Driving adapters
  CLI | MCP | Operator Console | public local transport endpoints
                         |
                         v
Application use cases
  identify | read | topology | navigate | control | maintain
                         |
                         v
Internal source ports
  GraphSourceReadPort | HostNavigationPort | GraphMutationPort
                         |
              +----------+----------+
              |                     |
              v                     v
   OgParserSourceAdapter      LogseqDbHostAdapter
              |                     |
              v                     v
      Parser public API       official Logseq API
```

The public `GraphSessionReadPort` is a Plumber application boundary exposed to
consumers. It is not implemented by Trama. Source-specific adapters implement
smaller internal Plumber ports and remain invisible to consumers.

Trama and Brain client adapters remain in their respective repositories. They
call Plumber's public local endpoints; they are not Plumber-owned driving
adapters or modules.

The existing filesystem `GraphReadPort` and Shadow behavior must first be
characterized. They may be adapted behind the new application boundary, but
must not be widened casually to accept DB sessions or made dependent on UI or
transport types.

## 6. Clean Architecture inside Trama

Trama keeps Plumber outside its domain:

```text
Tauri or other application shell
              |
              v
Trama use cases and domain
              |
              v
KnowledgeGraphGateway                    internal Trama port
              |
              v
PlumberClientAdapter                     replaceable outer adapter
              |
              v
Plumber public contracts
```

Trama domain models may differ from Plumber DTOs. Mapping belongs in
`PlumberClientAdapter`; the domain must not import Plumber runtime modules or
source-specific Parser types.

## 7. Contract ownership and packaging

Matryca Plumber is the sole canonical owner of every `plumber.*` contract.
Canonical artifacts live in the Plumber repository and include:

- human-readable normative Markdown;
- language-neutral JSON Schema;
- positive and negative synthetic fixtures;
- stable error codes and compatibility tables;
- fixture and schema digests;
- a lightweight Python binding with no daemon, UI, model, or Logseq dependency;
- a Compatibility Test Kit that consumers can run offline.

The preferred distribution is a lightweight contract artifact produced from
the Plumber repository, provisionally named `matryca-plumber-contracts`. The
implementation plan must verify whether Plumber's present package layout can
publish this safely without importing the full runtime. If not, the first
release may expose schemas and generated bindings from the same repository,
provided generation is deterministic and every consumer pins the owner commit,
contract version, schema digest, and fixture digest.

The schema bundle is transport-neutral. CLI, MCP, local IPC, and any later
embedded transport adapt the same semantic contract; none becomes contract
authority merely because it serializes the payload.

No fourth source repository is created. Consumers must not hand-maintain a
second normative schema.

## 8. Contract families

Each family is versioned independently, but Matryca Plumber is the sole
authority for all of them. A capability in one family does not grant access to
another.

### 8.1 `plumber.graph.read/v1`

Purpose: normalized, bounded, source-independent reads for Trama, Brain, CLI,
and MCP.

Initial operations:

| Operation | Successful result |
| --- | --- |
| `session.open` | Binds one transport-authenticated client context, selects one registered source and graph under explicit policy, and returns a scoped session binding. |
| `graph.identify` | Identifies the selected graph, source mode, native authority, session binding, and supported capabilities. |
| `page.read` | Returns one requested page with ordered block content and complete provenance. |
| `block.subtree.read.complete` | Returns one root block and every descendant in declared order, explicitly marked complete. |
| `session.close` | Revokes the caller's session binding and prevents later reuse. |

Every request includes:

- exact `contract_id` and accepted major;
- operation and opaque request ID;
- operation-specific page or block reference when required;
- declared size, depth, and timeout bounds where applicable.

`session.open` includes requested capabilities and one opaque registered-source
selector. It never declares client identity, credentials, authentication
material, transport subject, transport connection, a local path, or an implicit
current graph. The selected transport derives authentication and its internal
bindings outside JSON. Its success returns:

- opaque session and graph bindings;
- non-identifying authentication-context reference, authentication policy ID,
  authentication result class, authenticated principal class, and granted
  capability scope;
- native source mode and authority;
- graph-lock or graph-switch policy;
- issue and expiry times;
- source generation or revision, or explicit `revision_unavailable`;
- producer version and build identity.

At `session.open`, Plumber stores opaque transport-derived
`authenticated_subject_binding` and `transport_connection_binding` with the
session. They are neither request fields nor result/provenance/receipt fields.
`graph.identify`, every later read, and `session.close` must present through the
same subject and authorized connection. A different subject fails
`session_subject_mismatch`; an unapproved reconnect fails
`session_connection_mismatch`; neither failure closes, rebinds, or mutates the
session. `session.resume` is not a v1 operation or capability. Any resume path
requires a separate future capability with explicit reauthentication and
session-transfer semantics.

`graph.identify` and every later read must send the returned session and graph
bindings. They may not request an implicit current graph, silently reopen a
session, extend expiry, widen capabilities, or switch graphs. A graph switch
requires closing the old session and opening a new one. Transport authentication
details, subject binding, and connection binding remain outside payloads; only
the non-identifying context reference, policy identifier, result class, and
principal class are public evidence.

Every result includes:

- exact contract version and operation;
- matching request ID plus session and graph bindings when safely established;
- `success` or one explicit failure outcome;
- Plumber producer identity and version;
- Plumber build or artifact digest when an executable profile is qualified;
- advertised and exercised capabilities;
- mode-correct provenance;
- source generation or revision when the selected host can state it safely;
- deterministic result digest for qualified fixtures;
- completeness and ordering facts where required.

Public provenance states only source mode and native authority:

| Source mode | Native authority |
| --- | --- |
| `og_markdown` | `logseq_og_markdown` |
| `db_native` | `logseq_db_native` through the selected official host surface |

Parser identity and version remain Plumber-internal operational evidence. They
may appear in Plumber diagnostics and qualification receipts, but they are not
required public fields and consumers must not branch on them.

If the selected official source cannot provide a safe generation or revision,
the result states `revision_unavailable`. Such results may be returned for a
qualified bounded read, but they must not be reused from a public-result cache.

### 8.2 `plumber.graph.topology/v1`

Purpose: graph visualization without transferring source authority to Trama.

Initial scope:

- bounded snapshot identity;
- paginated nodes and edges;
- stable opaque entity references;
- source generation and graph binding;
- explicit truncation and continuation;
- deterministic ordering for identical source generation and options.

Events, live deltas, watchers, and convergence are separate future contracts.
Trama must never reconstruct a complete graph from an explicitly incomplete
snapshot without telling the user.

### 8.3 `plumber.control/v1`

Purpose: Plumber Operator Console and external operator automation.

Permitted scope:

- read-only `control.status` for runtime and adapter health;
- selected source mode and graph identity;
- explicitly authorized daemon lifecycle commands;
- queue, job, cache, and receipt state;
- explicitly authorized technical configuration;
- deterministic gardening options and governed maintenance job commands.

Excluded scope:

- semantic interpretation of note content;
- user-facing knowledge recommendations;
- graph exploration;
- Trama intelligence or Nodi presentation behavior.

`plumber.control/v1` never carries graph mutation payloads and never grants
vault-write authority. When the Operator Console starts a gardening job, the
job must enter Plumber's separately governed maintenance and write use cases.
Existing internal OG write behavior retains its current safety contract; a
future external Trama or Brain mutation route still requires
`plumber.graph.mutate/v1`.

Every command, unlike `control.status`, requires an authenticated operator
principal, role, explicit consent or approval reference, bounded target scope,
idempotency key, receipt identifier, cancellation behavior, and disconnect
semantics. External clients receive no operator role by default.

A useful boundary test is: Plumber's console should remain useful when all note
text is hidden and only operational metadata is available.

### 8.4 `plumber.host.navigate/v1`

Purpose: let Trama request that the active Logseq host open or focus one entity
without learning source-specific host details.

The contract uses an opaque entity reference obtained from a Plumber read or
topology result. Plumber validates graph and session binding, then delegates to
a supported host capability. Unsupported navigation fails explicitly. Trama
must not guess a `logseq://` URI, filesystem path, DB identifier, or host API
fallback.

Navigation is a user-authorized command even though it does not edit graph
content. Each request binds the authenticated principal, explicit user intent,
session, graph, entity, permitted host action, target window or host scope,
receipt, cancellation, and disconnect behavior. Background analysis cannot
silently trigger navigation.

### 8.5 `plumber.graph.mutate/v1`

Status: deferred public contract.

Plumber already has governed OG mutation behavior, but no Trama or Brain
mutation permission follows from the read, topology, navigation, or control
contracts. A public mutation contract requires a separate ADR covering:

- explicit user intent and authorization;
- preview and bounded target set;
- expected source revision;
- conflict rejection and idempotency;
- atomicity, timeout reconciliation, recovery, and undo;
- mode-specific authority for OG and DB;
- audit receipt and revocation.

DB mutation remains blocked until an official host route proves required
conflict and recovery semantics. Direct mutation of Logseq's internal database
is forbidden.

## 9. Common failure semantics

Every family fails closed. Initial shared outcomes are:

- `unsupported`;
- `incompatible`;
- `invalid_request`;
- `not_found`;
- `authority_unavailable`;
- `provenance_failure`;
- `stale_session`;
- `foreign_graph`;
- `incomplete_result`;
- `limit_exceeded`;
- `timeout`;
- `cancelled`;
- `session_subject_mismatch`;
- `session_connection_mismatch`;
- `internal_failure`.

Failures include a stable namespaced code and documented retryability. They do
not contain absolute paths, credentials, unbounded vault content, raw database
queries, Parser exceptions, or private implementation details.

No consumer may convert failure into success using a cache, export, similarly
named page, different graph, Markdown mirror, source-mode fallback, or silent
session rebind.

Any derived cache key used for a public result must include at least contract
major, graph binding, source generation or revision, and provenance digest. A
cache miss or stale entry cannot change source mode or native authority.
When source revision is unavailable, public-result cache reuse is prohibited.

## 10. UI boundary

### Plumber Operator Console

The existing React/FastAPI UI remains in Plumber and evolves into a deliberately
small operator console. It may monitor and control Plumber, but it must not
become a second Trama.

### Trama Knowledge Workspace

Trama owns full graph interaction, analysis, intelligence, explanations,
insight discovery, and user-facing gardening recommendations. It may display a
summary of Plumber health by consuming `plumber.control/v1`; it must not copy
Plumber configuration state or implement a second daemon control plane.

### Parser LENS

LENS is deprecated as a product direction. Migration rules are:

1. inventory public CLI, Python API, optional dependencies, documentation,
   examples, tests, vendored assets, and contributor provenance;
2. announce deprecation for at least one compatible release unless the public
   API policy proves immediate removal is permitted;
3. keep historical source and licence notices intact;
4. remove LENS only in the version allowed by Parser's semantic-version policy;
5. build Trama's graph explorer independently from
   `plumber.graph.topology/v1`, without copying LENS source or vendored assets.

## 11. Source authority and derived state

- Logseq OG Markdown remains the sole native authority for OG.
- Logseq DB's native local database remains the sole native authority for DB,
  accessed only through a qualified official host surface.
- Parser output, Plumber normalized DTOs, Shadow, indexes, topology snapshots,
  Trama models, caches, embeddings, and visualizations are derived views.
- A derived view must retain graph binding, source generation, and provenance.
- A DB graph never falls back to an OG filesystem graph.
- A read must not create, migrate, repair, or mutate native source state as an
  undocumented side effect.

## 12. Compatibility and versioning

- Contract identifiers contain a major version.
- Breaking schema or semantic changes require a new major.
- Backward-compatible fields and capabilities require a minor version plus
  executable evidence.
- Unknown majors and absent required capabilities fail explicitly.
- Stable releases and prereleases are separate compatibility rows.
- Plumber qualifies exact Parser releases internally for OG, but Trama and
  Brain qualify only the Plumber contract version they consume.
- Every cross-repository result binds exact commits or releases, schema digest,
  fixture digest, commands, platform, outcome, and limitations.
- A green synthetic suite is not a production host, user graph, performance,
  accessibility, or release claim.

## 13. Security, privacy, and contribution boundaries

- Vault content is untrusted data, never instructions or authorization.
- Graph and session identifiers exposed publicly are opaque and privacy-safe.
- All operations enforce input, output, depth, size, and time bounds.
- Default data flow is local; any network path requires separate disclosure and
  authorization.
- Trama remains source-available under PolyForm Noncommercial 1.0.0.
- Parser and Plumber retain their existing licences unless separately changed.
- A permissively licensed dependency does not grant rights to unrelated Trama
  or Brain code.
- External copyright-bearing code or documentation must not be merged until a
  lawyer-reviewed contributor agreement or equivalent grant exists.
- Git authorship, issue participation, or repository presence alone is not
  proof of copyright ownership.

Before publishing a contract binding or bundle, Plumber must produce an exact
dependency and licence inventory, SBOM, generated-file provenance, source and
schema digests, required notices, and an artifact inspection proving that no
Parser implementation, LENS source, vendored visualization asset, Trama source,
Brain source, vault content, or private material is embedded. Parser notices
and historical attribution remain intact throughout LENS deprecation.

## 14. Incremental migration programme

Only one cross-repository implementation dependency is active at a time. Each
repository uses its own branch and pull request.

### M0 — Accept and publish architecture authority

1. Reconcile this worktree with live Trama main without discarding existing
   clean-architecture work.
2. Accept an explicit authority-transfer ADR in Plumber before any gateway
   implementation begins.
3. Update the ecosystem responsibility contract so Plumber, not Trama, owns
   Logseq access and public graph contracts.
4. Add or update coordinated ADRs in Parser and Trama after the Plumber owner
   decision is published.
5. Preserve the current feature-off state for unqualified cross-repository and
   DB paths.
6. Correct roadmaps, plans, diagrams, issue bodies, and task handoffs that still
   contain the reversed dependency.

Exit: documentation validators pass and no current plan authorizes a Trama
Logseq adapter or direct Brain-to-Parser path.

### M1 — Freeze `plumber.graph.read/v1`

Owner: Plumber.

Deliver normative schema, lightweight binding decision, fixtures, TCK,
capability negotiation, provenance, bounds, and failure semantics. No host or
consumer support claim. Publish only a clearly labelled prerelease contract
artifact after its own authorization, license and provenance gate, and
exact-head evidence. Record its version, source commit, schema and fixture
digests, SBOM, notices, and release provenance.

### M2 — Adapt the existing OG path

Owner: Plumber.

Characterize current `GraphReadPort`, Parser integration, Shadow fallback, CLI,
MCP, and daemon behavior. Implement the smallest adapter into
`plumber.graph.read/v1` without changing OG authority or Parser semantics. A
live MCP transport may advertise the feature only after it proves one trusted
authenticated subject binding and one stable authorized connection binding from
its actual runtime context. If either fact is unavailable, the feature remains
default-off and the MCP operation returns `unsupported`; service/TCK coverage
may use injected test-only transport contexts but cannot create a live support
claim.

### M3 — Convert Trama into a consumer

Owner: Trama, after M2 merges and an exact Plumber contract artifact is
published.

- retire the experimental `trama.logseq.read/v1` producer;
- remove direct Parser dependency and the Trama OG adapter;
- replace `trama_plumber_bridge` consumer admission helper with a real outer
  `PlumberClientAdapter`;
- keep Trama domain models behind `KnowledgeGraphGateway`;
- pin exact contract version, artifact digest, schema digest, fixture digest,
  and release provenance;
- run Plumber's published TCK vectors without redeclaring their semantics;
- prove that Trama has no Parser or Logseq storage import.

Initial vertical: identify one graph, read one page, and read one complete
ordered subtree through Plumber.

### M4 — Deprecate Parser LENS

Owner: Parser, independent after boundary docs are accepted.

Publish compatibility-safe deprecation, redirect product documentation toward
Trama, and remove visualization only at the correct semantic-version boundary.
Parsing, graph semantics, exports, and developer APIs remain supported.

### M5 — Add topology and navigation

Owner sequence: Plumber contract and implementation first, Trama consumer
second.

Deliver a bounded graph snapshot and one qualified open-in-Logseq action before
building Trama's full graph explorer. Unsupported OG/DB host capabilities stay
visible and must not be guessed.

### M6 — Qualify Logseq DB reads in Plumber

Owner: Plumber.

Select and qualify one official host surface. Prove graph identity, page read,
complete subtree, lifecycle, bounds, zero forbidden state change, and explicit
failure. Existing Trama DB-probe plans are superseded; Trama receives DB data
through the same Plumber contract as OG.

### M7 — Add Brain as a separate consumer

Owner: Brain, only after compatible Plumber contracts are released.

Brain consumes Plumber directly. No Brain change is required for Trama's
Community delivery and no Parser dependency is added.

Before any Brain integration claim:

1. fetch and record Brain's live head and dirty state;
2. characterize and track any legacy direct Parser, graph-path, sibling-source,
   or shared-cache coupling without silently deleting it;
3. add import and dependency tests that forbid new direct Parser or Logseq
   access;
4. pin one exact published Plumber contract profile and all required digests;
5. run accepted and rejected TCK fixtures with integration feature-off;
6. prove Brain's document RAG, Ladybug, databases, scores, and caches remain
   independent from Plumber's Logseq retrieval state;
7. enable an exact profile only through a separate Brain authorization and
   qualification gate.

### M8 — Evaluate Trama desktop distribution

Owner: Trama, separate ADR and evidence programme.

Evaluate a Python-first domain runtime, Nuitka distribution, and Tauri desktop
shell with measured cold start, idle memory, graph rendering, artifact size,
accessibility, updates, signing, and platform support. Nuitka or Tauri selection
does not by itself prove performance relative to Logseq or Electron.

## 15. Test and enforcement strategy

Repository-local boundary tests must prove:

### Parser

- no dependency on Plumber, Trama, Brain, MCP, or native Logseq DB;
- package-root API compatibility for the exact Plumber-supported range;
- LENS deprecation and removal do not change parser semantics.

### Plumber

- public contracts import no daemon, UI, model, Parser, or Logseq adapter;
- OG adapter depends only on Parser's documented package-root API;
- DB adapter cannot access internal Logseq database files;
- both source adapters satisfy identical Plumber contract vectors;
- Operator Console depends on control use cases, not domain-private state;
- Shadow and other derived stores never become native authority;
- graph switching, cancellation, disconnect, and concurrent sessions cannot
  leak a graph binding, cache result, or provenance record across sessions.
- session read and close reject a different authenticated subject and an
  unauthorized reconnect without exposing or changing either internal binding;
  resume is absent unless a later dedicated capability is qualified.
- the MCP transport starts default-off and returns `unsupported` unless a
  characterization probe against the actual runtime proves trusted subject and
  stable connection bindings; constants, object identity, and fabricated auth
  context are forbidden substitutes.

### Trama

- no import or dependency on Parser;
- no direct filesystem or native Logseq DB access;
- domain and use cases do not import Plumber transport types;
- only the outer Plumber adapter maps contract DTOs;
- graph, error, and disconnected states remain deterministic and truthful;
- integration remains feature-off until its exact Plumber profile is qualified.

### Cross-repository qualification

- exact owner and consumer versions use identical accepted fixtures;
- consumers depend on an exact published contract artifact with verified
  schema, fixture, artifact, SBOM, notice, and release-provenance records;
- negative fixtures reject version skew, missing provenance, stale sessions,
  foreign graph bindings, incomplete results, unsupported operations, and
  excess bounds;
- public CI is fork-safe and uses no private source, credentials, or user
  vaults;
- documentation and compatibility matrices match executable results.

## 16. Delivery and authorization rules

1. Reverify complete remote heads and working-tree state before each slice.
2. Change and merge the owning repository first.
3. Start each dependent branch from newly fetched `origin/main`.
4. One pull request changes one repository and one reviewable concern.
5. Run focused tests before full repository gates.
6. Record unsupported and negative outcomes; do not redefine success.
7. Treat commit, push, pull request, issue or project mutation, merge, package
   publication, and release as separate authorization gates.
8. Preserve dirty or divergent work. Never reset, stash, clean, or overwrite it
   merely to simplify migration.

## 17. Completion checklist

- [ ] Coordinated ADRs assign all Logseq access to Plumber.
- [ ] Every diagram shows OG through Parser and Plumber before Trama or Brain.
- [ ] Every diagram shows DB through Plumber before Trama or Brain.
- [ ] `plumber.graph.read/v1` has one canonical schema and fixture authority.
- [ ] Plumber's existing OG behavior passes through the new boundary unchanged.
- [ ] Trama imports neither Parser nor a Logseq adapter.
- [ ] Brain integration documentation names Plumber as its Logseq gateway.
- [ ] Brain has an exact live anchor, legacy-coupling inventory, direct-Parser
      dependency ban, feature-off TCK parity, and independent-cache evidence
      before any integration claim.
- [ ] Parser LENS has a provenance-reviewed deprecation and removal path.
- [ ] Plumber Operator Console remains operational and bounded.
- [ ] Trama owns graph exploration and intelligence without Plumber UI overlap.
- [ ] DB support remains unclaimed until official-host evidence passes.
- [ ] PolyForm commercial boundaries and contributor-agreement gate remain
      explicit.
- [ ] Exact-version compatibility tests pass in every affected repository.
- [ ] No performance, distribution, or platform claim exceeds measured evidence.
