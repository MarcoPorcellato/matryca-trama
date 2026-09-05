# Plumber-Parser-Trama Contract Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Matryca Plumber the only public Logseq gateway, with a tested
`plumber.graph.read/v1` OG vertical, Trama as its consumer, Parser as the
protocol-neutral parser, and a compatible LENS deprecation path.

**Architecture:** Plumber owns transport-neutral schemas, fixtures, bindings,
TCK, session-bound application use cases, source adapters, and public local
transport. Its OG source adapter calls Parser only through Parser's documented
package-root API. Trama maps Plumber DTOs only in an outer client adapter behind
its own `KnowledgeGraphGateway`; it has no Parser or Logseq-storage dependency.

**Tech Stack:** Python 3.12+, `uv`, standard-library JSON/schema fixture
validation where possible, Pydantic in Plumber runtime boundaries, `pytest` in
Plumber and Parser, `unittest` in Trama, JSON Schema Draft 2020-12, GitHub
Actions.

**Spec:** [`2026-09-05-cross-repository-contract-roadmap.md`](../specs/2026-09-05-cross-repository-contract-roadmap.md)

## Global Constraints

- Revalidate all three complete `origin/main` heads and worktree states before
  every branch. Starting evidence: Trama `70fc14c27b11e31e8f557fd70684b6a83933e7d6`,
  Plumber `af9b1dfb1cf89e2a4160020ce565be3f617be16a`, Parser
  `65e8e64f7f0227bcae8235069fbc3da834652744`.
- Use one clean isolated worktree, short-lived branch, reviewable concern,
  commit, PR, and merge per repository slice. Never reset, stash, clean, or
  overwrite a primary checkout or another worker's changes.
- Only one cross-repository mutating slice may be active. Merge owner work and
  fetch its new `origin/main` before cutting a dependent branch.
- Logseq OG is authoritative Markdown. DB is authoritative only through one
  later qualified official Logseq host surface. No code may access internal DB
  files or make DB fall back to OG Markdown.
- Trama and Brain never import Parser or Logseq storage/host APIs. Parser never
  imports Plumber, Trama, or Brain. Plumber never imports Trama or Brain.
- `GraphReadPort` remains the existing filesystem/Shadow boundary. Do not widen
  it to hold sessions, DB selectors, DTOs, or UI concerns.
- Canonical `plumber.*` semantics, schemas, fixtures, fixture digest, and TCK
  live only in Plumber. Consumers pin an exact released profile; they do not
  copy normative schemas or recreate contract semantics.
- Keep the initial public vertical bounded to `session.open`, `graph.identify`,
  `page.read`, `block.subtree.read.complete`, and `session.close`.
- Every result and failure is session- and graph-bound, bounded, source-mode
  correct, explicit, deterministic for qualified fixtures, and privacy-safe.
  A `revision_unavailable` result is never reusable from public-result cache.
- Every v1 session is also bound internally to one authenticated transport
  subject and one authorized transport connection. Those opaque bindings never
  serialize; v1 has no reconnect or resume capability.
- Preserve existing OG, Shadow, CLI, MCP, daemon, Operator Console, Parser
  parsing, and LENS behavior unless the focused slice explicitly changes it.
- Plumber's Operator Console remains operational metadata/control only; it must
  not become a graph explorer or a second Trama.
- Repository-owned Trama material remains PolyForm Noncommercial 1.0.0. Do not
  merge external copyright-bearing code or documentation until a
  lawyer-reviewed contributor agreement or equivalent grant exists.
- No package publication, release, DB support, Brain integration, desktop
  distribution, performance, UI, user-vault, network, or host claim follows
  from a passing synthetic test. Those are separate gates.
- Current execution authority covers repository commits, pushes, PRs, and
  merges only. It does not authorize package artifact publication, package
  index upload, release creation, tag publication, or distribution.
- Public CI is GitHub-hosted and fork-safe. Do not add CCP receipt requirements
  to any public repository.

## Delivery Map

| Slice | Owner | Dependent slice may start only after | Required terminal evidence |
| --- | --- | --- | --- |
| A | Plumber | none | authority ADR/docs merge |
| B | Trama | A merged | corrected ownership/docs merge |
| C | Parser | A merged | parser boundary/docs merge |
| D | Plumber | A merged | canonical read schema, fixtures, binding decision, TCK merge |
| E | Plumber | D merged | OG adapter and local read vertical merge |
| F | Trama | E plus separately authorized public Plumber contract release and exact released profile | client adapter, TCK parity, no Parser/host imports merge |
| G | Parser | C merged | LENS deprecation release merge |
| H | Plumber | E plus separate authorization | topology/navigation contract groundwork merge |
| I | Plumber or Brain | separate evidence and authorization | DB/Brain gate record only; no capability implied |

The contract artifact is a subproject within the Plumber repository, not a
fourth source repository. Its proposed root is `contracts/python/`, with its
own `pyproject.toml`, `uv.lock`, and `uv run --project contracts/python` test
entry. Task 4 must reject that location if an isolated wheel installation
imports `src`, `frontend`, Parser, or a Logseq adapter.

## File Structure

### Plumber owner artifacts

- `docs/decisions/2026-09-05-plumber-logseq-gateway-authority.md` — accepted
  authority transfer ADR; corrects prior Trama-host direction.
- `docs/contracts/plumber-graph-read-v1.md` — normative Markdown for read
  semantics, session lifecycle, bounds, provenance, cache prohibition, and
  stable errors.
- `contracts/plumber.graph.read/v1/schema.json` — canonical JSON Schema
  Draft 2020-12 bundle.
- `contracts/plumber.graph.read/v1/fixtures/*.json` — owned positive and
  negative synthetic vectors plus immutable manifest digests.
- `contracts/python/` — independently buildable `matryca-plumber-contracts`
  binding with no import of Plumber runtime, UI, Parser, or Logseq source code;
  it has its own lockfile and is exercised by root `contracts-check`.
- `contracts/tck/runner.py` — offline fixture runner that consumes only the
  schema, fixtures, and binding.
- `src/graph/ports/session_read.py` — narrow Plumber application port; no
  `agent`, UI, Parser, or host import.
- `src/agent/plumber_graph_read_service.py` — session registry, request bounds,
  graph binding, operation dispatch, failure translation, and receipt metadata.
- `src/agent/graph_source_registry.py` — registered-source selector grammar
  resolver; opaque client selectors never contain a path or select an ambient
  current graph.
- `src/agent/graph_read_v1_config.py` — explicit default-off feature gate and
  bounded registry configuration using repository env parsing policy.
- `src/agent/og_parser_source_adapter.py` — Parser package-root integration
  and source-specific normalization behind Plumber's internal source port.
- `src/agent/mcp_server.py` — additive local transport registration only;
  existing `read_graph_data` remains unchanged.

### Trama consumer artifacts

- `packages/core/src/trama_core/knowledge_graph_gateway.py` — Trama-owned
  domain port and domain values; no Plumber transport DTO import.
- `packages/plumber-client-adapter/` — outer adapter maps the exact Plumber
  contract binding into `KnowledgeGraphGateway` values.
- `architecture.toml`, root `pyproject.toml`, package manifests, and
  `tests/architecture/test_dependency_boundaries.py` — remove Parser/OG
  admission only after the consumer vertical is green; admit the new adapter.
- `packages/parser-bridge/`, `packages/logseq-og-adapter/`, and historical
  `trama.logseq.read/v1` producer tests — remove only in the same branch that
  proves replacement by the exact released Plumber profile.
- `packages/plumber-bridge/` — remove in the same profile-specific migration;
  it is replaced by `packages/plumber-client-adapter/`, not retained as a
  second admission path.

### Parser compatibility artifacts

- `docs/decisions/ADR-0004-PLUMBER-GATEWAY-BOUNDARY.md` — Parser's explicit
  product-boundary decision, numbered after current ADR-0003.
- `src/logseq_matryca_parser/lens.py` and
  `src/logseq_matryca_parser/kinetic_commands.py` — compatible deprecation
  warning and CLI notice, not removal.
- `tests/test_lens.py` and CLI tests — warning and unchanged rendering
  compatibility.

## Task 1: Plumber authority-transfer ADR and corrected programme docs

**Repository:** Matryca Plumber, fresh worktree from the newly revalidated
`origin/main`.

**Files:**
- Create: `docs/decisions/2026-09-05-plumber-logseq-gateway-authority.md`
- Create: `docs/contracts/README.md`
- Modify: `docs/decisions/index.md`
- Modify: `docs/superpowers/plans/2026-09-01-logseq-db-read-only-compatibility.md`
- Modify: `docs/roadmaps/ROADMAP_V2_PREPARATION.md`
- Modify: `CHANGELOG.md`
- Modify generated: `docs/knowledge/inventory.json`
- Modify generated: `docs/knowledge/inventory.md`
- Test: Plumber documentation inventory and link checks

**Interfaces:**
- Consumes: exact Plumber head, Parser package-root API policy, and proposed
  Trama specification.
- Produces: a Plumber-owned accepted decision declaring Plumber as sole
  Logseq gateway and `plumber.*` contract owner; no runtime change.

- [ ] **Step 1: Revalidate owner branch and record baseline**

Run:

```bash
rtk git fetch origin --prune
rtk git status --short --branch
rtk git rev-parse origin/main
rtk git worktree add ../matryca-plumber-gateway-origin origin/main -b codex/plumber-gateway-authority
```

Expected: clean new worktree at recorded `origin/main`; no primary checkout
changes.

- [ ] **Step 2: Write failing documentation assertions**

Add a focused check in the repository's existing documentation test mechanism
which reads the new ADR and asserts these literal facts:

```python
assert "Matryca Plumber is the sole Logseq gateway" in adr
assert "Trama" in adr and "does not import Parser" in adr
assert "Logseq DB official host surface" in adr
assert "direct mutation of Logseq internal database" in adr
```

The ADR must also state that `GraphReadPort` stays filesystem/Shadow-only,
`GraphSessionReadPort` is Plumber's public application boundary, Parser is
Plumber-internal for OG, and the Operator Console is bounded control UI.

- [ ] **Step 3: Run the focused assertion and observe RED**

Run:

```bash
rtk uv run pytest tests/test_docs_gateway_authority.py -q
```

Expected: FAIL because the ADR and its index entry do not exist.

- [ ] **Step 4: Apply Plumber changelog decision gate, then add the decision**

Read the repository `matryca-changelog` guidance and inspect the current
`CHANGELOG.md`. Add one `[Unreleased]` architecture entry if the maintainer's
changelog rule classifies this public ownership correction as operator-visible;
otherwise record in the ADR why no changelog entry is required. Write the ADR
with status `Accepted`, exact source authority rules, full
OG/DB/Trama/Brain topology, forbidden dependency list, contract ownership,
and feature-off limits. Replace the old DB plan's statements assigning Logseq
host acquisition, OG/DB adapters, `trama.logseq.read/v1` production, or a
Trama-side session port with the Plumber owner model. Mark historical claims
as superseded, not erased; do not claim DB execution.

- [ ] **Step 5: Run focused and documentation gates**

Run:

```bash
rtk uv run pytest tests/test_docs_gateway_authority.py -q
rtk make docs-inventory-sync
rtk make docs-inventory-md
rtk make docs-check
rtk make docs-audit
rtk git diff --check
```

Expected: all exit `0`; generated inventory is the only generated change.

- [ ] **Step 6: Commit the owner decision**

```bash
rtk git add CHANGELOG.md docs/decisions docs/contracts docs/superpowers/plans docs/roadmaps docs/knowledge tests/test_docs_gateway_authority.py
rtk git commit -m "docs(architecture): make Plumber the Logseq gateway"
```

Do not start Task 2 or Task 3 branches until this commit is merged to Plumber
`main` with required checks terminal green.

## Task 2: Trama accepts Plumber ownership and retires reversed authority docs

**Repository:** Matryca Trama, new worktree from the Trama head fetched after
Task 1 merges.

**Files:**
- Create: `docs/decisions/ADR-0006-PLUMBER-GATEWAY-ADOPTION.md`
- Modify: `docs/contracts/ECOSYSTEM_RESPONSIBILITY_AND_CHANGE_CONTRACT.md`
- Modify: `docs/contracts/LOGSEQ_READ_CONTRACT_V1.md`
- Modify: `docs/contracts/PLUMBER_COMPATIBILITY.md`
- Modify: `docs/contracts/PARSER_COMPATIBILITY.md`
- Modify: `docs/contracts/README.md`
- Modify: `docs/standards/CLEAN_ARCHITECTURE.md`
- Modify: `docs/ROADMAP.md`
- Modify: `README.md`
- Modify: `tests/contracts/test_workflow_contract.py`
- Modify: `tests/architecture/test_dependency_boundaries.py`

**Interfaces:**
- Consumes: merged Plumber authority ADR exact commit.
- Produces: no runtime feature; Trama docs and architecture policy consistently
  declare it a future Plumber consumer.

- [ ] **Step 1: Add failing policy tests**

Add assertions that the ecosystem contract rejects old ownership and the
architecture map has no admitted direct Parser or OG adapter after migration:

```python
assert "Matryca Plumber | sole Logseq gateway" in ecosystem
assert "Trama to Parser" in prohibited_dependencies
assert "Trama to Logseq storage or host APIs" in prohibited_dependencies
assert "trama-parser-bridge" not in migrated_architecture
assert "trama-logseq-og-adapter" not in migrated_architecture
```

Keep the last two assertions in a migration-specific fixture until Task 6;
current live packages remain historical until their replacement is merged.

- [ ] **Step 2: Run focused tests and observe RED**

Run:

```bash
rtk uv run --all-packages python -m unittest tests.contracts.test_workflow_contract -v
rtk uv run --all-packages python -m unittest tests.architecture.test_dependency_boundaries -v
```

Expected: FAIL because accepted Plumber ownership and migration fixture do not
yet exist.

- [ ] **Step 3: Write the Trama adoption ADR and rewrite only authority text**

State that `trama.logseq.read/v1` is historical experimental producer evidence,
not a future contract authority; Plumber owns `plumber.*`, source selection,
OG Parser adapter, official DB host adapter, and public schemas. Preserve the
historical tests and facts until Task 6. Correct diagrams to show
`OG Markdown -> Parser -> Plumber -> Trama/Brain` and
`DB official host -> Plumber -> Trama/Brain`.

- [ ] **Step 4: Run Trama policy and foundation checks**

Run:

```bash
rtk uv run --all-packages python scripts/validate_architecture.py
rtk uv run --all-packages python -m unittest discover -s tests/architecture -v
rtk uv run --all-packages python -m unittest discover -s tests/contracts -v
rtk uv run --all-packages python scripts/validate_foundation.py
rtk git diff --check
```

Expected: all exit `0`; no package is removed in this documentation PR.

- [ ] **Step 5: Commit only Trama authority adoption**

```bash
rtk git add README.md docs tests/architecture/test_dependency_boundaries.py tests/contracts/test_workflow_contract.py
rtk git commit -m "docs(architecture): adopt Plumber gateway boundary"
```

## Task 3: Parser records boundary and LENS migration policy

**Repository:** Logseq Matryca Parser, fresh worktree from Parser `origin/main`
after Task 1 merges.

**Files:**
- Create: `docs/decisions/ADR-0004-PLUMBER-GATEWAY-BOUNDARY.md`
- Modify: `docs/decisions/index.md`
- Modify: `docs/ARCHITECTURE.md`
- Modify: `docs/COOKBOOK.md`
- Modify: `docs/reference/API_STABILITY.md`
- Modify: `README.md`
- Test: `tests/test_layer_boundary.py`

**Interfaces:**
- Consumes: merged Plumber authority ADR and Parser API stability policy.
- Produces: Parser's explicit library-only boundary and compatible LENS
deprecation policy; no API removal.

- [ ] **Step 1: Add a failing boundary/documentation test**

Write a test which reads the ADR and checks the parser's integration position:

```python
assert "Plumber invokes Parser through documented package-root API" in adr
assert "Trama and Brain do not import Parser" in adr
assert "LENS remains available during its deprecation window" in adr
assert "Logseq DB" in adr and "does not own" in adr
```

- [ ] **Step 2: Run focused test and observe RED**

Run:

```bash
rtk uv run pytest tests/test_plumber_gateway_boundary_docs.py -q
```

Expected: FAIL because the ADR is absent.

- [ ] **Step 3: Add the Parser boundary decision**

Document Parser's sole responsibilities: deterministic OG Markdown parsing,
package-root API, fixtures, semantic-version policy, and optional adapters.
Document exclusions: Plumber orchestration, MCP, host/DB access, Trama/Brain
UI, public consumer schema ownership. State that no LENS code, vendored asset,
or copyright-bearing visualization implementation will be copied to Trama.

- [ ] **Step 4: Verify parser boundaries**

Run:

```bash
rtk uv sync --locked --all-extras
rtk uv run pytest tests/test_plumber_gateway_boundary_docs.py tests/test_layer_boundary.py -q
rtk make all
rtk make vendor-name-check
rtk git diff --check
```

Expected: all exit `0`.

- [ ] **Step 5: Commit the Parser boundary decision**

```bash
rtk git add README.md docs tests/test_plumber_gateway_boundary_docs.py
rtk git commit -m "docs(architecture): define Parser gateway boundary"
```

## Task 4: Plumber defines canonical `plumber.graph.read/v1` material and TCK

**Repository:** Matryca Plumber, fresh worktree after Task 1 merge.

**Files:**
- Create: `docs/contracts/plumber-graph-read-v1.md`
- Create: `contracts/plumber.graph.read/v1/schema.json`
- Create: `contracts/plumber.graph.read/v1/fixtures/manifest.json`
- Create: `contracts/plumber.graph.read/v1/fixtures/positive-og-read.json`
- Create: `contracts/plumber.graph.read/v1/fixtures/negative-session-and-provenance.json`
- Create: `contracts/python/pyproject.toml`
- Create: `contracts/python/uv.lock`
- Create: `contracts/python/src/matryca_plumber_contracts/__init__.py`
- Create: `contracts/python/src/matryca_plumber_contracts/models.py`
- Create: `contracts/python/src/matryca_plumber_contracts/validation.py`
- Create: `contracts/python/tests/test_binding.py`
- Create: `contracts/tck/runner.py`
- Create: `contracts/tck/tests/test_runner.py`
- Modify: `Makefile`
- Modify: `.github/workflows/ci.yml`
- Modify: `docs/contracts/README.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: Task 1 ADR and synthetic owned fixture facts only.
- Produces: transport-neutral canonical major-1 schema, fixture manifest
digests, lightweight binding, offline TCK, and no active host claim.

- [ ] **Step 1: Add failing TCK and isolation tests**

Create an accepted OG vector and negative vectors. Test all required fields and
ensure the binding remains dependency-isolated:

```python
def test_binding_has_no_runtime_or_source_adapter_imports() -> None:
    root = Path("contracts/python/src/matryca_plumber_contracts")
    source = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(root.rglob("*.py"))
    )
    forbidden = ("src.agent", "frontend", "logseq_matryca_parser", "sqlite", "httpx")
    assert not any(token in source for token in forbidden)

def test_tck_rejects_foreign_graph_and_revision_unavailable_cache_reuse() -> None:
    assert run_vector("foreign-graph") == "foreign_graph"
    assert run_vector("revision-unavailable-cache") == "provenance_failure"
    assert run_vector("cross-principal-read") == "session_subject_mismatch"
    assert run_vector("unauthorized-reconnect") == "session_connection_mismatch"
```

- [ ] **Step 2: Run contract tests and observe RED**

Run:

```bash
rtk uv run --project contracts/python pytest contracts/python/tests/test_binding.py contracts/tck/tests/test_runner.py -q
rtk uv run --project contracts/python python contracts/tck/runner.py --fixtures contracts/plumber.graph.read/v1/fixtures
```

Expected: FAIL because schema, manifest, vectors, binding, runner, root target,
and CI integration are absent.

- [ ] **Step 3: Implement normative schema and binding**

Define exact request/result envelope values:

```python
CONTRACT_ID = "plumber.graph.read/v1"
OPERATIONS = frozenset({
    "session.open", "graph.identify", "page.read",
    "block.subtree.read.complete", "session.close",
})
ERROR_CODES = frozenset({
    "unsupported", "incompatible", "invalid_request", "not_found",
    "authority_unavailable", "provenance_failure", "stale_session",
    "foreign_graph", "incomplete_result", "limit_exceeded", "timeout",
    "cancelled", "session_subject_mismatch", "session_connection_mismatch",
    "internal_failure",
})
```

The schema requires opaque `session_binding` and `graph_binding` after open,
matching request ID, granted capabilities, source mode/authority pair,
producer/build identity, bounds, deterministic fixture digest, and explicit
success/failure. `session.open` accepts only this registered-source selector:

```json
{"kind":"registered_source","source_id":"[a-z0-9][a-z0-9_-]{0,63}"}
```

`source_id` resolves only through Plumber's configured source registry; the
payload never contains a filesystem path, DB identifier, ambient/current graph
selector, or host endpoint. The schema requires transport-supplied
`auth_policy_id`, `auth_result_class`, and `principal_class` in the result
evidence, but never a credential, raw principal identifier,
`authenticated_subject_binding`, or `transport_connection_binding`. The two
bindings are transport-derived opaque internal state, never request/result JSON
or public fixture fields. It rejects parser fields, absolute paths, raw queries,
ambient graph selection, and unbounded payloads. The manifest hashes every
fixture and schema using lowercase SHA-256. The runner validates positive and
negative vectors offline; it never opens a vault, host, network connection, or
cache.

Set `contracts/python/pyproject.toml` package version to `0.1.0`, declare only
its own test dependency group, and create its `uv.lock`. Add this exact root
target and make both `check` and `ci` depend on it:

```make
.PHONY: contracts-check
contracts-check:
	uv run --project contracts/python pytest contracts/python/tests/test_binding.py contracts/tck/tests/test_runner.py -q
	uv run --project contracts/python python contracts/tck/runner.py --fixtures contracts/plumber.graph.read/v1/fixtures
```

Add a named `Verify isolated contract project` CI step which runs
`uv sync --locked --project contracts/python` and `make contracts-check`; add
`contracts/python/uv.lock` to CI cache-dependency globs.

- [ ] **Step 4: Build the binding in isolation**

Run:

```bash
rtk uv build --project contracts/python --out-dir /private/tmp/matryca-plumber-contracts-wheel
rtk uv run --isolated --no-project --with /private/tmp/matryca-plumber-contracts-wheel/matryca_plumber_contracts-0.1.0-py3-none-any.whl python -c "import matryca_plumber_contracts; print(matryca_plumber_contracts.CONTRACT_ID)"
```

Expected: build succeeds and prints `plumber.graph.read/v1`; any import of the
full Plumber runtime, Parser, UI, or Logseq adapter is a NO-GO for this layout.

- [ ] **Step 5: Run owner tests and full repository gate**

Run:

```bash
rtk uv sync --locked --project contracts/python
rtk make contracts-check
rtk make check
rtk make ci
rtk git diff --check
```

Expected: all exit `0`; keep output/provenance local and sanitized.

- [ ] **Step 6: Commit canonical contract authority**

```bash
rtk git add .github/workflows/ci.yml Makefile docs/contracts contracts CHANGELOG.md
rtk git commit -m "feat(contracts): add Plumber graph read v1 authority"
```

Do not publish an artifact yet. Publication is a separate gate requiring exact
commit, schema digest, fixture digest, build artifact digest, SBOM, licence
inventory, notices, generated-file provenance, and inspection proving no
Parser implementation, LENS asset, Trama/Brain source, vault data, or private
material is embedded.

## Task 5: Plumber adapts OG reads behind session-bound application use cases

**Repository:** Matryca Plumber, fresh worktree after Task 4 merges.

**Files:**
- Create: `src/graph/ports/session_read.py`
- Create: `src/agent/plumber_graph_read_service.py`
- Create: `src/agent/og_parser_source_adapter.py`
- Create: `src/agent/graph_source_registry.py`
- Create: `src/agent/graph_read_v1_config.py`
- Create: `tests/test_plumber_graph_read_service.py`
- Create: `tests/test_og_parser_source_adapter.py`
- Create: `tests/test_graph_source_registry.py`
- Create: `tests/test_graph_read_v1_config.py`
- Modify: `src/agent/mcp_server.py`
- Modify: `tests/test_mcp_server.py`
- Modify: `.env.example`
- Modify: `tests/test_env_example_coverage.py`
- Modify: `docs/contracts/plumber-graph-read-v1.md`
- Modify: `CHANGELOG.md`
- Test: `tests/test_graph_repository.py`, `tests/test_graph_dispatch_read.py`,
  `tests/test_shadow_hardening_axis3_routing.py`

**Interfaces:**
- Consumes: Task 4 binding and fixtures; Parser documented root symbols
`LogseqGraph`, `LogseqPage`, `LogseqNode` only.
- Produces: `GraphSessionReadPort` (`open_session`, `read`, `close_session`),
`OgParserSourceAdapter`, registered-source resolver, default-off feature gate,
and additive local transport operation.

- [ ] **Step 1: Characterize unchanged existing read paths**

Write regression tests before new code:

```python
def test_graph_read_port_stays_path_bound() -> None:
    assert "graph_root: Path" in inspect.getsource(GraphReadPort)
    assert "session_binding" not in inspect.getsource(GraphReadPort)

def test_existing_subtree_dispatch_uses_existing_port() -> None:
    source = inspect.getsource(handle_read_subtree)
    assert "get_graph_read_port(Path(graph_path))" in source

def test_service_and_mcp_transport_match_owner_tck() -> None:
    for vector in load_tck_vectors():
        assert service_result(vector) == expected_canonical_result(vector)
        assert mcp_result_json(vector) == expected_canonical_json(vector)

def test_session_rejects_other_authenticated_subject() -> None:
    session = open_session(subject_binding="subject-a", connection_binding="connection-a")
    result = read_session(session, subject_binding="subject-b", connection_binding="connection-b")
    assert result.error_code == "session_subject_mismatch"

def test_session_rejects_unauthorized_reconnect_and_preserves_owner_session() -> None:
    session = open_session(subject_binding="subject-a", connection_binding="connection-a")
    result = close_session(session, subject_binding="subject-a", connection_binding="connection-b")
    assert result.error_code == "session_connection_mismatch"
    assert session_is_open(session)
```

Use the repository's real fixture/monkeypatch style in the second test; do not
move `get_graph_read_port`, `MarkdownGraphRepository`, or `ShadowGraphRepository`.

- [ ] **Step 2: Run characterization tests and observe RED for new service**

Run:

```bash
rtk uv run pytest tests/test_graph_repository.py tests/test_graph_dispatch_read.py tests/test_plumber_graph_read_service.py -q
```

Expected: existing regressions pass; new-service import/test fails because it
does not exist.

- [ ] **Step 3: Implement the narrow port and OG adapter**

Use these public application signatures:

```python
class GraphSessionReadPort(Protocol):
    def open_session(self, request: SessionOpenRequest) -> SessionOpenResult:
        raise NotImplementedError
    def read(self, request: GraphReadRequest) -> GraphReadResult:
        raise NotImplementedError
    def close_session(self, request: SessionCloseRequest) -> SessionCloseResult:
        raise NotImplementedError

class OgParserSourceAdapter:
    def open(self, selector: SourceSelector, limits: ReadLimits) -> OpenedGraph:
        raise NotImplementedError
    def identify(self, graph: OpenedGraph) -> GraphIdentity:
        raise NotImplementedError
    def read_page(self, graph: OpenedGraph, page_reference: str, limits: ReadLimits) -> PagePayload:
        raise NotImplementedError
    def read_complete_subtree(self, graph: OpenedGraph, block_reference: str, limits: ReadLimits) -> SubtreePayload:
        raise NotImplementedError
```

Implement this resolver and feature-gate contract before the source adapter:

```python
@dataclass(frozen=True)
class RegisteredSourceSelector:
    source_id: str

class GraphSourceRegistry:
    def resolve(self, selector: RegisteredSourceSelector) -> RegisteredOgSource:
        raise NotImplementedError

class TransportAuthContext:
    policy_id: str
    result_class: str
    principal_class: str
    authenticated_subject_binding: str
    transport_connection_binding: str
```

`RegisteredSourceSelector` parses only the Task 4 grammar, and
`GraphSourceRegistry` maps its `source_id` to a configured bounded root. A
missing, malformed, or unregistered selector is `invalid_request`; it never
opens a default/ambient graph. `graph_read_v1_config.py` reads
`MATRYCA_PLUMBER_GRAPH_READ_V1_ENABLED` with existing `env_bool` helpers,
defaults it to `false`, documents it in `.env.example`, and returns
`unsupported` before source resolution when disabled. `TransportAuthContext` is
created by the local transport from authenticated connection state, not from
caller JSON. `authenticated_subject_binding` and `transport_connection_binding`
are opaque, non-serialized bindings derived by that transport. The service
stores both at `session.open`; public results carry only `policy_id`,
`result_class`, and `principal_class`.

`PlumberGraphReadService` owns opaque bindings, expiry, graph lock, granted
capabilities, request limit checks, source-revision/cache rule, error mapping,
and receipt metadata. It accepts an explicit `TransportAuthContext` with every
call and cannot reopen, extend, widen, or switch a session. Every `read` and
`session.close` compares both bindings with the stored values before dispatch:
a different subject returns `session_subject_mismatch`; same subject on an
unapproved replacement connection returns `session_connection_mismatch`; neither
operation changes session state. A reconnect/resume path is not in v1
operations, capabilities, schema, or feature flag. It may be proposed only as
a separate future capability with explicit reauthentication and session-transfer
semantics. `OgParserSourceAdapter` receives only a resolved bounded selected
Markdown root, calls Parser package-root API, and maps public Parser values to
Plumber DTOs. Parser exception classes, paths, and raw diagnostics never leave
the adapter. Session reuse after close/expiry returns `stale_session`; using a
different graph binding returns `foreign_graph`; oversized request/result
returns `limit_exceeded`; no cache reuse occurs when revision is unavailable.

- [ ] **Step 4: Add additive MCP/local transport adapter**

Register a new `plumber_graph_read_v1` tool in `register_mcp_tools` with this
transport signature and no default graph argument:

```python
@safe_tool()
async def plumber_graph_read_v1(
    ctx: Context[ServerSession, AppContext],
    request_json: str,
) -> str:
    auth_context = authenticated_transport_context(ctx)
    request = parse_canonical_graph_read_request(request_json)
    result = graph_read_service.handle(request, auth_context)
    return serialize_canonical_graph_read_result(result)
```

`parse_canonical_graph_read_request` rejects duplicate/non-canonical JSON,
unknown fields, and source selectors outside Task 4 grammar. The serializer
uses canonical sorted-key UTF-8 JSON from the contract binding. The tool
delegates once to `PlumberGraphReadService`; it does not alter
`read_graph_data`, add a Parser import to `mcp_server.py`, or create a second
filesystem path.

- [ ] **Step 5: Run focused behavioral and regression gates**

Run:

```bash
rtk uv run pytest tests/test_og_parser_source_adapter.py tests/test_plumber_graph_read_service.py tests/test_mcp_server.py -q
rtk uv run pytest tests/test_graph_source_registry.py tests/test_graph_read_v1_config.py tests/test_env_example_coverage.py -q
rtk uv run pytest tests/test_graph_repository.py tests/test_graph_dispatch_read.py tests/test_shadow_hardening_axis3_routing.py -q
rtk uv run pytest tests/test_graph_layer_boundary.py -q
rtk make check
rtk make ci
rtk git diff --check
```

Expected: service and transport each execute the owner TCK accepted vectors
and reject stale, foreign, cross-principal, unauthorized-reconnect,
feature-disabled, unregistered-source, unsupported, malformed,
missing-provenance, incomplete-subtree, and excessive-limit vectors with the
canonical code; pre-existing OG/Shadow tests remain green.

- [ ] **Step 6: Commit OG vertical**

```bash
rtk git add .env.example src/graph/ports/session_read.py src/agent/plumber_graph_read_service.py src/agent/og_parser_source_adapter.py src/agent/graph_source_registry.py src/agent/graph_read_v1_config.py src/agent/mcp_server.py tests docs/contracts CHANGELOG.md
rtk git commit -m "feat(graph): serve OG reads through Plumber contracts"
```

## Task 6: Record owner evidence; block Trama migration until separately authorized release

**Repositories:** Plumber evidence-only PR first. This task does not publish a
package, tag, release, or distribution. Trama code remains blocked unless a
later explicit authorization covers public release and all profile evidence.

**Plumber evidence-only files:**
- Create: `docs/contracts/evidence/plumber-graph-read-v1-0.1.0.md`
- Create: `docs/contracts/evidence/plumber-graph-read-v1-0.1.0.sbom.json`
- Create: `docs/contracts/evidence/plumber-graph-read-v1-0.1.0.sha256`

**Trama files:**
- Create: `packages/core/src/trama_core/knowledge_graph_gateway.py`
- Create: `packages/plumber-client-adapter/pyproject.toml`
- Create: `packages/plumber-client-adapter/src/trama_plumber_client_adapter/__init__.py`
- Create: `packages/plumber-client-adapter/src/trama_plumber_client_adapter/client.py`
- Create: `tests/contracts/test_knowledge_graph_gateway.py`
- Create: `tests/integration/test_plumber_contract_profile.py`
- Modify: root `pyproject.toml`
- Modify: `architecture.toml`
- Modify: `packages/core/pyproject.toml`
- Modify: `docs/standards/CLEAN_ARCHITECTURE.md`
- Modify: `docs/contracts/LOGSEQ_READ_CONTRACT_V1.md`
- Modify: `docs/contracts/PLUMBER_COMPATIBILITY.md`
- Modify: `docs/contracts/PARSER_COMPATIBILITY.md`
- Modify: `docs/ROADMAP.md`
- Modify: `tests/architecture/test_dependency_boundaries.py`
- Delete after replacement passes: `packages/parser-bridge/`,
  `packages/logseq-og-adapter/`, `packages/plumber-bridge/`, and their
  direct-producer/consumer-helper tests.

**Interfaces:**
- Consumes: Task 5 exact commit plus locally built contract artifact evidence.
- Produces: an owner evidence record only. It produces no public profile,
  Trama code, package publication, release, or consumer compatibility claim.

- [ ] **Step 1: Create evidence without external publication**

Build and inspect the contract wheel locally, calculate all fields below, and
commit a sanitized evidence record. Its `release_provenance` value must be
`not_published`; do not upload an artifact, create a tag, or create a release:

```text
plumber_commit = full 40-character lowercase Git SHA
contract_version = 0.1.0
artifact_sha256 = 64-character lowercase SHA-256
schema_sha256 = 64-character lowercase SHA-256
fixture_sha256 = 64-character lowercase SHA-256
sbom_sha256 = 64-character lowercase SHA-256
notice_sha256 = 64-character lowercase SHA-256
release_provenance=not_published
```

If any value is absent, malformed, unverifiable, or names uninspected bundled
Parser/LENS/Trama/Brain/private material, record `BLOCKED` and do not create a
consumer claim. The evidence document is not a release profile and does not
unblock Trama.

- [ ] **Step 2: Commit evidence-only owner record**

Run:

```bash
rtk git add docs/contracts/evidence docs/contracts CHANGELOG.md
rtk git commit -m "docs(contracts): record graph read profile evidence"
```

Expected: repository evidence is reviewable and no external package/release
state changes. Stop Task 6 here under current authority.

### Future-only continuation: Trama consumer migration

This continuation is deliberately non-executable now. Start it only after a
new explicit package-publication authorization and a public immutable profile
whose `release_provenance` is a verified URL or digest. Revalidate both
Plumber and Trama heads before cutting the separate Trama branch.

- [ ] **Step 3: Stop unless public-release profile evidence is complete**

Require a signed/reviewed public-profile row before starting Trama code:

```text
plumber_commit = full 40-character lowercase Git SHA
contract_version = 0.1.0
artifact_sha256 = 64-character lowercase SHA-256
schema_sha256 = 64-character lowercase SHA-256
fixture_sha256 = 64-character lowercase SHA-256
sbom_sha256 = 64-character lowercase SHA-256
notice_sha256 = 64-character lowercase SHA-256
release_provenance = immutable public URL or immutable digest
```

If any value is absent, malformed, unverifiable, or names uninspected bundled
Parser/LENS/Trama/Brain/private material, record `BLOCKED` and do not delete
Trama packages or create a consumer claim.

- [ ] **Step 4: Write Trama's failing consumer tests**

Define Trama values independently from owner DTO types:

```python
class KnowledgeGraphGateway(Protocol):
    def identify(self) -> KnowledgeGraphIdentity:
        raise NotImplementedError
    def read_page(self, page_reference: str) -> KnowledgePage:
        raise NotImplementedError
    def read_complete_subtree(self, block_reference: str) -> KnowledgeSubtree:
        raise NotImplementedError

def test_adapter_maps_only_verified_plumber_result() -> None:
    assert adapter.read_page("Home").title == "Home"

def test_adapter_rejects_foreign_graph_without_fallback() -> None:
    with self.assertRaisesRegex(KnowledgeGraphUnavailable, "foreign_graph"):
        adapter.read_page("Home")
```

Add static tests that fail if `trama_core` imports `matryca_plumber_contracts`,
or if any Trama package imports `logseq_matryca_parser`, direct filesystem
selection, `sqlite3`, or a Logseq host SDK.

- [ ] **Step 5: Run focused tests and observe RED**

Run:

```bash
rtk uv run --all-packages python -m unittest tests.contracts.test_knowledge_graph_gateway -v
rtk uv run --all-packages python -m unittest tests.integration.test_plumber_contract_profile -v
rtk uv run --all-packages python -m unittest tests.architecture.test_dependency_boundaries -v
```

Expected: FAIL because port, adapter, exact profile pin, and architecture map
do not exist.

- [ ] **Step 6: Add the outer adapter and remove replaced Trama source path**

Place all binding imports and DTO mapping in
`trama_plumber_client_adapter.client`. Its local transport invokes only
`plumber_graph_read_v1`; it opens one session, binds graph, identifies, reads,
and closes it deterministically. It maps `unsupported`, `incompatible`,
`authority_unavailable`, `provenance_failure`, `stale_session`, `foreign_graph`,
`incomplete_result`, `limit_exceeded`, and `timeout` to truthful Trama domain
errors. It never guesses host URI/path, silently reopens a session, switches a
graph, reuses an unavailable revision, or falls back to old Trama OG code.

After TCK parity passes, remove `trama-parser-bridge`,
`trama-logseq-og-adapter`, `trama-plumber-bridge`, and `trama.logseq.read/v1`
producer source in the same commit. Remove their package entries from root
`pyproject.toml` and `architecture.toml`, and replace their architecture tests
with a no-legacy-package assertion. Retain historical documentation with an
explicit archival status and source anchor; do not claim those tests qualified
the new profile.

- [ ] **Step 7: Run exact vector, architecture, and full Trama gates**

Run:

```bash
rtk uv run --all-packages python -m unittest tests.contracts.test_knowledge_graph_gateway -v
rtk uv run --all-packages python -m unittest tests.integration.test_plumber_contract_profile -v
rtk uv run --all-packages python scripts/validate_architecture.py
rtk uv run --all-packages python -m unittest discover -s tests/architecture -v
rtk uv run --all-packages python -m unittest discover -s tests/contracts -v
rtk uv run --all-packages python -m unittest discover -s tests/containment -v
rtk uv run --all-packages python -m unittest tests.test_foundation_validator -v
rtk uv run --all-packages python scripts/validate_foundation.py
rtk git diff --check
```

Expected: exact TCK accepted and rejected vectors match Plumber; Trama has no
Parser/source-adapter dependency; integration remains feature-off except the
recorded released synthetic profile.

- [ ] **Step 8: Commit profile-specific Trama migration**

```bash
rtk git add architecture.toml pyproject.toml packages docs tests
rtk git rm -r packages/parser-bridge packages/logseq-og-adapter packages/plumber-bridge
rtk git commit -m "feat(contracts): consume Plumber graph read profile"
```

Before executing removal, inspect staged paths and confirm every removed path
is repository-owned historical Trama code. Stop if contributor provenance is
uncertain or copyrighted external material appears.

## Task 7: Parser deprecates LENS without removing it

**Repository:** Logseq Matryca Parser, fresh worktree after Task 3 merge.

**Files:**
- Modify: `src/logseq_matryca_parser/lens.py`
- Modify: `src/logseq_matryca_parser/kinetic_commands.py`
- Modify: `tests/test_lens.py`
- Modify: `tests/test_kinetic.py`
- Modify: `README.md`
- Modify: `docs/ARCHITECTURE.md`
- Modify: `docs/COOKBOOK.md`
- Modify: `docs/reference/API_STABILITY.md`
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: Task 3 boundary decision and current experimental
`GraphVisualizer` API.
- Produces: a warning and documented migration path; keeps
`GraphVisualizer`, `NetworkXVisitor`, `visualize`, `demo`, `networkx`, `pyvis`,
and vendored assets intact for this release.

- [ ] **Step 1: Write failing deprecation tests**

Add both Python and CLI coverage:

```python
def test_graph_visualizer_warns_but_still_builds_network() -> None:
    with pytest.deprecated_call(match="LENS is deprecated"):
        visualizer = GraphVisualizer(pages=[_build_fake_page()])
    visualizer.build_network()
    assert visualizer.graph.number_of_nodes() == 4

def test_visualize_command_warns_and_preserves_html_output() -> None:
    result = runner.invoke(app, ["visualize", str(graph_root), str(output_html)])
    assert result.exit_code == 0
    assert "deprecated" in result.output.lower()
    assert output_html.is_file()
```

- [ ] **Step 2: Run focused tests and observe RED**

Run:

```bash
rtk uv run pytest tests/test_lens.py tests/test_kinetic.py -q
```

Expected: warning assertions fail while existing visualization behavior still
passes.

- [ ] **Step 3: Add compatible warning and documentation**

At `GraphVisualizer` construction issue a `DeprecationWarning` with
`stacklevel=2`, naming LENS as deprecated and stating that no removal occurs in
the current release. `visualize` and `demo` print a concise deprecation notice
before retaining their existing behavior. Documentation directs product users
to future Trama exploration through Plumber topology, but does not claim that
Trama topology exists. Keep source notices, optional extras, assets, and API
exports unchanged.

- [ ] **Step 4: Run focused and full Parser gates**

Run:

```bash
rtk uv sync --locked --all-extras
rtk uv run pytest tests/test_lens.py tests/test_kinetic.py tests/test_layer_boundary.py -q
rtk make all
rtk make vendor-name-check
rtk git diff --check
```

Expected: visualization output and parser semantics unchanged; warning and
docs pass; no LENS removal occurs.

- [ ] **Step 5: Commit compatible LENS deprecation**

```bash
rtk git add src/logseq_matryca_parser/lens.py src/logseq_matryca_parser/kinetic_commands.py tests README.md docs CHANGELOG.md
rtk git commit -m "deprecate: mark LENS product path for migration"
```

## Task 8: Plumber topology and navigation contract groundwork

**Repository:** Matryca Plumber, fresh worktree after Task 5 merges and a
separate maintainer authorization.

**Files:**
- Create: `docs/contracts/plumber-graph-topology-v1.md`
- Create: `docs/contracts/plumber-host-navigate-v1.md`
- Create: `contracts/plumber.graph.topology/v1/schema.json`
- Create: `contracts/plumber.graph.topology/v1/fixtures/manifest.json`
- Create: `contracts/plumber.graph.topology/v1/fixtures/negative-incomplete-snapshot.json`
- Create: `contracts/plumber.host.navigate/v1/schema.json`
- Create: `contracts/plumber.host.navigate/v1/fixtures/manifest.json`
- Create: `contracts/plumber.host.navigate/v1/fixtures/negative-unsupported-and-cancelled.json`
- Create: `contracts/tck/tests/test_topology_navigation_runner.py`
- Modify: `contracts/tck/runner.py`
- Modify: `docs/contracts/README.md`

**Interfaces:**
- Consumes: merged `plumber.graph.read/v1` binding/session/graph identifiers.
- Produces: schema and negative vectors only; no graph explorer, navigation
endpoint, host invocation, DB support, or Trama UI.

- [ ] **Step 1: Write failing contract-vector tests**

```python
def test_topology_rejects_incomplete_snapshot_as_complete_graph() -> None:
    assert run_vector("negative-incomplete-snapshot") == "incomplete_result"

def test_navigation_requires_user_intent_and_supported_host() -> None:
    assert run_vector("unsupported-host") == "unsupported"
    assert run_vector("cancelled-request") == "cancelled"
```

- [ ] **Step 2: Run TCK and observe RED**

Run:

```bash
rtk uv run --project contracts/python pytest contracts/tck/tests/test_topology_navigation_runner.py -q
```

Expected: FAIL because the two contract families and vectors are absent.

- [ ] **Step 3: Define bounded, non-runtime schemas**

Topology schema requires session/graph bindings, source generation/revision,
opaque node and edge references, deterministic ordering, pagination cursor,
explicit truncation, continuation, and capability. Navigation schema accepts
only an opaque entity reference emitted by a read/topology result plus
authenticated principal class, explicit user-intent/approval reference, target
host scope, idempotency key, receipt identifier, cancellation, and disconnect
semantics. Reject guessed `logseq://` URIs, paths, DB IDs, and background
navigation. Define `cancelled` as a terminal, distinct outcome: the receipt
records cancellation initiator, observed host-action state (`not_started`,
`started_unknown`, or `completed_before_cancel`), and retry rule. Only
`not_started` may be retried with the same idempotency key; the other states
require receipt inspection and a new explicit user intent. `timeout` remains a
separate bounded-duration outcome and never substitutes for cancellation.

- [ ] **Step 4: Run owner contract gates**

Run:

```bash
rtk uv run --project contracts/python pytest contracts/tck/tests/test_topology_navigation_runner.py -q
rtk uv run --project contracts/python python contracts/tck/runner.py --fixtures contracts/plumber.graph.topology/v1/fixtures
rtk uv run --project contracts/python python contracts/tck/runner.py --fixtures contracts/plumber.host.navigate/v1/fixtures
rtk make check
rtk git diff --check
```

Expected: only schema/vector groundwork passes. Do not add a UI or source
adapter in this task.

- [ ] **Step 5: Commit contract groundwork**

```bash
rtk git add docs/contracts contracts
rtk git commit -m "docs(contracts): define topology and navigation groundwork"
```

## Task 9: DB and Brain remain explicit evidence gates

**Repository:** Plumber for DB gate record; Brain repository only if a later
separate authorization explicitly includes it. No Trama/Parser runtime work.

**Files:**
- Create when evidence exists: `docs/contracts/evidence/logseq-db-host-evidence.md`
- Modify when evidence exists: `docs/contracts/plumber-graph-read-v1.md`
- Modify when evidence exists: `docs/roadmaps/ROADMAP_V2_PREPARATION.md`

**Interfaces:**
- Consumes: exact official host artifact/version, sanctioned transport,
synthetic disposable graph, and measured evidence.
- Produces: only `supported`, `capability_no_go`, or `upstream_blocked` record;
never direct DB access or automatic implementation.

- [ ] **Step 1: Enforce preconditions before any host execution**

Record all fields below in a proposed evidence file before running a probe:

```text
official_host_name = exact official product surface name
artifact_version = immutable version string
artifact_sha256 = 64-character lowercase SHA-256
transport = one of CLI, official SDK, or separately approved local transport
synthetic_graph_digest = 64-character lowercase SHA-256
requested_operations=graph.identify,page.read,block.subtree.read.complete
forbidden_actions=internal-db-access,mutation,export,cache-authority-fallback
```

- [ ] **Step 2: Stop on missing evidence**

Do not create `LogseqDbHostAdapter`, change `GraphReadPort`, add a DB source
to Shadow, or enable Trama/Brain. Mark `BLOCKED` if graph identity, complete
ordered subtree, lifecycle/process side effects, bounds, zero forbidden state
change, or explicit failures cannot be proven.

- [ ] **Step 3: Require separate Brain re-entry**

Before a Brain integration claim, fetch Brain's live head and dirty state,
inventory legacy direct Parser/path/sibling/cache coupling, add its own direct
Parser/Logseq import bans, pin the released Plumber profile, run accepted and
rejected TCK vectors feature-off, and prove its RAG/Ladybug/databases/scores/
caches remain independent. This plan grants none of those changes.

## Review, PR, and Rollback Protocol

### Exact PR order

1. Task 1 Plumber ADR/docs.
2. Task 2 Trama authority adoption.
3. Task 3 Parser boundary policy.
4. Task 4 Plumber canonical read contract/TCK.
5. Task 5 Plumber OG vertical.
6. Task 6 Plumber evidence-only record. Stop: Trama consumer remains `BLOCKED`
   until a separately authorized public package release creates an exact profile.
7. Task 7 Parser LENS deprecation.
8. Task 8 Plumber topology/navigation contract groundwork.
9. Task 9 only after independent DB/Brain authorization and evidence.

For every PR: fetch, bind base/head SHA, run focused tests, run full repository
gate, inspect `rtk git diff --check`, run code-impact inspection before source
symbol edits where repository policy requires it, request fresh review, push,
wait for terminal required GitHub checks, reread unresolved reviews, reverify
base/head, then merge. A follow-up branch starts only from newly fetched merged
`origin/main`.

### Commit boundaries

| Commit | Allowed content | Must not include |
| --- | --- | --- |
| Task 1 | Plumber authority ADR/docs/inventory | contract code or DB adapter |
| Task 2 | Trama authority docs/tests | package removal or direct consumer |
| Task 3 | Parser boundary docs/tests | LENS warning/removal |
| Task 4 | Plumber schema/fixtures/binding/TCK | source adapter or publication |
| Task 5 | Plumber OG vertical | DB host or Trama code |
| Task 6 | one Plumber evidence-only commit | package publication, Trama consumer commit, Brain code |
| Task 7 | Parser LENS deprecation | visualization removal/assets rewrite |
| Task 8 | topology/navigation schemas/vectors | runtime host/UI/navigation endpoint |
| Task 9 | evidence-only gate record | capability implementation without proof |

### Rollback rules

- Before merge: close/reject the PR or create a corrective commit; never reset
  or rewrite another worker's branch.
- After a documentation or schema merge: add a new superseding ADR/schema
  major; do not mutate published historical evidence or fixture digests.
- After Task 5: disable the new additive local tool behind its explicit feature
  gate and retain existing MCP/read paths. Do not roll back by changing source
  authority or Shadow behavior.
- After Task 6: retain `BLOCKED` because no public profile exists. After the
  separately authorized future consumer migration, disable its exact profile
  and show a truthful unavailable state; never resurrect Trama Parser/OG source
  as a hidden fallback.
- After Task 7: retain LENS through its documented deprecation window; any
  future removal is a separate Parser major-version plan with licence/provenance
  review.
- DB and Brain failures remain `BLOCKED`, `capability_no_go`, or
  `upstream_blocked`; they are not retried through internal DB access or an OG
  mirror.

## Plan Self-Review

### Spec coverage

| Specification requirement | Implementing task |
| --- | --- |
| Plumber sole gateway and corrected OG/DB/Brain diagrams | 1, 2, 3 |
| canonical transport-neutral contract, binding, fixtures, digests, TCK | 4 |
| Trama only as Plumber consumer, no Parser/storage imports | 6 |
| compatible LENS deprecation; no copied assets | 3, 7 |
| bounded topology/navigation contracts, no premature UI | 8 |
| DB official-host and Brain evidence gates | 9 |
| PolyForm and contributor-agreement guard | Global Constraints; every task |
| owner-first PRs, exact anchors, review, rollback | Delivery Map; Review protocol |

### Placeholder scan

Checked for forbidden placeholder patterns and undefined adjacent interfaces.
None remain. The only deferred work is explicitly bounded Task 9, which grants
no implementation authority.

### Type consistency

`GraphSessionReadPort` is Plumber's public application port; source adapters
remain internal. `KnowledgeGraphGateway` is Trama's internal domain port;
`PlumberClientAdapter` is its outer adapter. `GraphReadPort` remains the
existing path-bound filesystem/Shadow port. No task assigns the same role to
two names.

## Execution Handoff

Plan saved to
`docs/superpowers/plans/2026-09-05-plumber-parser-trama-contract-migration.md`.

Execution uses Subagent-Driven development: one owner implementer at a time,
fresh reviewer gates after each task, and no dependent task before its owner PR
is merged and revalidated.
