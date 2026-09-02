# Python-First Read Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the smallest qualified Python implementation of
`trama.logseq.read/v1` for synthetic Logseq OG fixtures: graph identification,
page read, and complete ordered block-subtree read.

**Architecture:** A `uv` workspace contains separate Python distributions for
contracts, deterministic core behavior, the Parser boundary, the OG adapter,
and the Plumber consumer boundary. Contracts are data-only and own version and
failure semantics; the OG adapter is the only component allowed to acquire
synthetic Markdown. Applications, DB access, caches, events, and writes remain
absent.

**Tech Stack:** Python 3.12+, `uv`, `hatchling`, standard-library `unittest`,
Logseq Matryca Parser `>=1.7.1,<2.0.0`, GitHub-hosted CI.

**Spec:**
[`../specs/2026-09-01-python-first-application-stack-design.md`](../specs/2026-09-01-python-first-application-stack-design.md),
[ADR-0004](../../decisions/ADR-0004-APPLICATION-STACK.md), and the
[application-stack qualification protocol](../../spikes/APPLICATION_STACK_QUALIFICATION.md).

## Global Constraints

- Start only after the ADR-0004 documentation delivery is merged and a fresh
  worktree is based on that exact `main` commit.
- Use Python `>=3.12`; record the exact interpreter, `uv`, lockfile, platform,
  fixture digest, and result digest for every qualification run.
- Import only documented package-root Parser symbols. Pin
  `logseq-matryca-parser>=1.7.1,<2.0.0` in the Parser bridge, never copied
  Parser internals.
- Implement only `graph.identify`, `page.read`, and
  `block.subtree.read.complete` for synthetic OG Markdown fixtures.
- Every success includes provenance. Every unsupported, incompatible, missing,
  incomplete, or untrusted input is an explicit failure result.
- Never access a user graph, native Logseq DB, cache, export, watcher, network
  service, application UI, private Brain source, or a write path.
- Use `uv run` for executable checks; do not use global package installation.
- Keep each task in its own focused pull request. Reverify exact head, hosted
  CI, reviews, and scope before every merge.

---

## File Structure

```text
pyproject.toml
uv.lock
packages/
  contracts/
    pyproject.toml
    src/trama_contracts/models.py
    src/trama_contracts/validation.py
  core/
    pyproject.toml
    src/trama_core/digests.py
    src/trama_core/normalization.py
  parser-bridge/
    pyproject.toml
    src/trama_parser_bridge/loader.py
  logseq-og-adapter/
    pyproject.toml
    src/trama_logseq_og_adapter/adapter.py
  plumber-bridge/
    pyproject.toml
    src/trama_plumber_bridge/consumer.py
tests/
  fixtures/og-minimal/pages/Example.md
  fixtures/fixture-manifest.json
  contracts/test_models.py
  contracts/test_og_read_contract.py
  containment/test_fixture_boundary.py
  integration/test_plumber_consumer.py
.github/workflows/python-contracts.yml
docs/spikes/evidence/python-read-contract-v1/README.md
```

`packages/contracts` owns public DTOs and error vocabulary. `packages/core`
owns canonical JSON normalization and SHA-256 digests. The Parser bridge loads a
selected synthetic root through `LogseqGraph.load_directory`. The OG adapter
maps stable Parser root exports into contract DTOs. The Plumber bridge accepts
only a complete, compatible public envelope; it never imports Plumber source.

## Task 1: Create Reproducible Python Workspace

**Files:**
- Create: `pyproject.toml`
- Create: `packages/contracts/pyproject.toml`
- Create: `packages/core/pyproject.toml`
- Create: `packages/parser-bridge/pyproject.toml`
- Create: `packages/logseq-og-adapter/pyproject.toml`
- Create: `packages/plumber-bridge/pyproject.toml`
  - Create: `packages/contracts/src/trama_contracts/__init__.py`
  - Create: `packages/core/src/trama_core/__init__.py`
  - Create: `packages/parser-bridge/src/trama_parser_bridge/__init__.py`
  - Create: `packages/logseq-og-adapter/src/trama_logseq_og_adapter/__init__.py`
  - Create: `packages/plumber-bridge/src/trama_plumber_bridge/__init__.py`
- Create: `tests/contracts/test_workspace.py`

**Interfaces:**
- Consumes: ADR-0004 package names and Python/`uv` decision.
- Produces: importable empty distributions and a reproducible public lockfile.

- [ ] **Step 1: Write failing workspace test**

```python
import importlib
import unittest


class WorkspaceTest(unittest.TestCase):
    def test_public_packages_import(self) -> None:
        for name in (
            "trama_contracts",
            "trama_core",
            "trama_parser_bridge",
            "trama_logseq_og_adapter",
            "trama_plumber_bridge",
        ):
            self.assertIsNotNone(importlib.import_module(name))
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --all-packages python -m unittest tests.contracts.test_workspace -v`

Expected: FAIL because no workspace package exists.

- [ ] **Step 3: Add root and member metadata**

Create a root `pyproject.toml` with this workspace boundary:

```toml
[project]
name = "matryca-trama-workspace"
version = "0.0.0"
requires-python = ">=3.12"
dependencies = []

[tool.uv.workspace]
members = ["packages/*"]
```

Each member uses `hatchling`, declares its unique public distribution name,
requires Python `>=3.12`, and exposes only its own `src/` package. Add the
Parser range only to `packages/parser-bridge/pyproject.toml`.

- [ ] **Step 4: Generate lockfile and run import test**

Run: `uv lock && uv run --all-packages python -m unittest tests.contracts.test_workspace -v`

Expected: PASS. `uv.lock` contains only public resolved dependencies.

- [ ] **Step 5: Commit focused workspace slice**

```bash
git add pyproject.toml uv.lock packages tests/contracts/test_workspace.py
git commit -m "build: add Python contract workspace"
```

## Task 2: Define Versioned Contract DTOs and Rejection Rules

**Files:**
- Create: `packages/contracts/src/trama_contracts/models.py`
- Create: `packages/contracts/src/trama_contracts/validation.py`
- Modify: `packages/contracts/src/trama_contracts/__init__.py`
- Test: `tests/contracts/test_models.py`

**Interfaces:**
- Consumes: `trama.logseq.read/v1` semantics and Task 1 workspace.
- Produces: `ReadRequest`, `ReadResult`, `Provenance`, `Outcome`, and
  `validate_request(request: ReadRequest) -> Outcome | None`.

- [ ] **Step 1: Write failing contract tests**

```python
import unittest


class ReadContractTests(unittest.TestCase):
    def test_unknown_major_is_incompatible(self) -> None:
        request = ReadRequest(
            contract_id="trama.logseq.read/v2",
            accepted_contract_major=2,
            operation="graph.identify",
            request_id="request-1",
            graph_selector="fixture:og-minimal",
        )
        self.assertIs(validate_request(request), Outcome.INCOMPATIBLE)

    def test_success_requires_complete_provenance(self) -> None:
        result = ReadResult.success(request_id="request-1", payload={})
        self.assertIs(result.outcome, Outcome.PROVENANCE_FAILURE)
```

- [ ] **Step 2: Run focused test to verify it fails**

Run: `uv run --all-packages python -m unittest tests.contracts.test_models -v`

Expected: FAIL because DTOs and validation do not exist.

- [ ] **Step 3: Implement immutable public DTOs**

```python
class Outcome(StrEnum):
    SUCCESS = "success"
    UNSUPPORTED = "unsupported"
    INCOMPATIBLE = "incompatible"
    INVALID_REQUEST = "invalid_request"
    NOT_FOUND = "not_found"
    AUTHORITY_FAILURE = "authority_failure"
    PROVENANCE_FAILURE = "provenance_failure"


@dataclass(frozen=True)
class Provenance:
    source_mode: Literal["og_markdown", "db_native"]
    authority: Literal["logseq_og_markdown", "logseq_db_native"]
    source_reference: str
    evidence_digest: str
```

Use `@dataclass(frozen=True)` and JSON-compatible mappings. `ReadResult.success`
returns `PROVENANCE_FAILURE` unless every provenance field is non-empty and the
authority matches source mode. Reject any request containing an empty
`request_id`, `graph_selector`, required page/block reference, or unsupported
operation.

- [ ] **Step 4: Run contract suite**

Run: `uv run --all-packages python -m unittest tests.contracts.test_models -v`

Expected: PASS, including unknown version, invalid request, authority mismatch,
missing provenance, and failure-result cases.

- [ ] **Step 5: Commit DTO slice**

```bash
git add packages/contracts tests/contracts/test_models.py
git commit -m "feat(contracts): add read contract v1 DTOs"
```

## Task 3: Add Synthetic Fixtures, Digests, and Containment Tests

**Files:**
- Create: `tests/fixtures/og-minimal/pages/Example.md`
- Create: `tests/fixtures/fixture-manifest.json`
- Create: `packages/core/src/trama_core/digests.py`
- Create: `packages/core/src/trama_core/normalization.py`
- Test: `tests/containment/test_fixture_boundary.py`

**Interfaces:**
- Consumes: Task 2 DTO vocabulary.
- Produces: `sha256_bytes(data: bytes) -> str`,
  `canonical_json(value: Mapping[str, object]) -> bytes`, and
  `resolve_fixture_path(root: Path, relative: PurePosixPath) -> Path`.

- [ ] **Step 1: Write failing containment and digest tests**

```python
class FixtureBoundaryTests(unittest.TestCase):
    def test_fixture_path_rejects_parent_escape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(ValueError, "outside fixture root"):
                resolve_fixture_path(root, PurePosixPath("../secret.md"))

    def test_canonical_json_is_stable(self) -> None:
        self.assertEqual(
            canonical_json({"b": 2, "a": 1}), b'{"a":1,"b":2}'
        )
```

- [ ] **Step 2: Run focused test to verify it fails**

Run: `uv run --all-packages python -m unittest tests.containment.test_fixture_boundary -v`

Expected: FAIL because containment and canonicalization helpers do not exist.

- [ ] **Step 3: Implement containment without following symlinks outside root**

```python
def resolve_fixture_path(root: Path, relative: PurePosixPath) -> Path:
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("fixture path outside fixture root")
    root_resolved = root.resolve(strict=True)
    candidate = (root / Path(relative)).resolve(strict=True)
    if candidate != root_resolved and root_resolved not in candidate.parents:
        raise ValueError("fixture path outside fixture root")
    return candidate
```

Test a symlink under the fixture root whose target is outside it; it must raise
the same error. Store fixture digests in the manifest and compare them before a
fixture is consumed.

- [ ] **Step 4: Run containment and contract tests**

Run: `uv run --all-packages python -m unittest tests.containment.test_fixture_boundary tests.contracts.test_models -v`

Expected: PASS. No test reads outside its temporary or fixture root.

- [ ] **Step 5: Commit fixture slice**

```bash
git add packages/core tests/fixtures tests/containment
git commit -m "test(contracts): add synthetic fixture containment"
```

## Task 4: Implement Public Parser Loader Boundary

**Files:**
- Create: `packages/parser-bridge/src/trama_parser_bridge/loader.py`
- Modify: `packages/parser-bridge/src/trama_parser_bridge/__init__.py`
- Test: `tests/contracts/test_parser_loader.py`

**Interfaces:**
- Consumes: `LogseqGraph` from the documented Parser package root and Task 3
  fixture containment.
- Produces: `load_og_fixture(fixture_root: Path, relative: PurePosixPath) -> LogseqGraph`.

- [ ] **Step 1: Write failing loader tests**

```python
import unittest


class ParserLoaderTests(unittest.TestCase):
    def test_loader_returns_graph_for_synthetic_root(self) -> None:
        graph = load_og_fixture(FIXTURES_ROOT, PurePosixPath("og-minimal"))
        self.assertEqual(graph.graph_path, (FIXTURES_ROOT / "og-minimal").resolve())
        self.assertIsNotNone(graph.get_page("Example"))

    def test_loader_rejects_path_outside_selected_root(self) -> None:
        with self.assertRaisesRegex(ValueError, "outside fixture root"):
            load_og_fixture(FIXTURES_ROOT, PurePosixPath("../outside"))
```

- [ ] **Step 2: Run focused test to verify it fails**

Run: `uv run --all-packages python -m unittest tests.contracts.test_parser_loader -v`

Expected: FAIL because the bridge is absent.

- [ ] **Step 3: Implement one read-only Parser call site**

```python
from logseq_matryca_parser import LogseqGraph


def load_og_fixture(
    fixture_root: Path, relative: PurePosixPath
) -> LogseqGraph:
    selected_root = resolve_fixture_path(fixture_root, relative)
    return LogseqGraph.load_directory(selected_root)
```

Do not import Parser internals, writer helpers, watcher types, exporters, or
experimental APIs. Keep strict Parser options at their documented defaults
unless a later contract test proves a stricter required behavior.

- [ ] **Step 4: Run loader, containment, and contract tests**

Run: `uv run --all-packages python -m unittest tests.contracts.test_parser_loader tests.containment.test_fixture_boundary tests.contracts.test_models -v`

Expected: PASS.

- [ ] **Step 5: Commit Parser boundary slice**

```bash
git add packages/parser-bridge tests/contracts/test_parser_loader.py
git commit -m "feat(parser): add read-only fixture loader"
```

## Task 5: Implement Three OG Read Operations

**Files:**
- Create: `packages/logseq-og-adapter/src/trama_logseq_og_adapter/adapter.py`
- Modify: `packages/logseq-og-adapter/src/trama_logseq_og_adapter/__init__.py`
- Test: `tests/contracts/test_og_read_contract.py`

**Interfaces:**
- Consumes: `ReadRequest`, `ReadResult`, `Provenance`, Task 3 digests, and
  Task 4 `load_og_fixture`.
- Produces: `OgReadAdapter.identify`, `OgReadAdapter.read_page`, and
  `OgReadAdapter.read_complete_subtree`.

- [ ] **Step 1: Write failing operation tests**

```python
import unittest


class OgReadContractTests(unittest.TestCase):
    def setUp(self) -> None:
        graph = load_og_fixture(FIXTURES_ROOT, PurePosixPath("og-minimal"))
        self.adapter = OgReadAdapter(graph, fixture_manifest_digest())

    def test_page_read_has_native_og_provenance(self) -> None:
        result = self.adapter.read_page(page_request("Example"))
        self.assertIs(result.outcome, Outcome.SUCCESS)
        self.assertEqual(result.provenance.authority, "logseq_og_markdown")

    def test_incomplete_subtree_never_succeeds(self) -> None:
        result = self.adapter.read_complete_subtree(block_request("missing-block"))
        self.assertIn(result.outcome, {Outcome.NOT_FOUND, Outcome.PROVENANCE_FAILURE})
```

Include tests for exact graph identity, unknown page, wrong contract major,
missing provenance, and source-order preservation of the complete subtree.

- [ ] **Step 2: Run focused tests to verify they fail**

Run: `uv run --all-packages python -m unittest tests.contracts.test_og_read_contract -v`

Expected: FAIL because no OG adapter exists.

- [ ] **Step 3: Implement explicit operation dispatch**

```python
class OgReadAdapter:
    def __init__(self, graph: LogseqGraph, fixture_digest: str) -> None:
        self._graph = graph
        self._fixture_digest = fixture_digest

    def identify(self, request: ReadRequest) -> ReadResult:
        return self._read(request, reference=None)

    def read_page(self, request: ReadRequest) -> ReadResult:
        return self._read(request, reference=request.page_reference)

    def read_complete_subtree(self, request: ReadRequest) -> ReadResult:
        return self._read(request, reference=request.block_reference)

    def _read(self, request: ReadRequest, reference: str | None) -> ReadResult:
        validation = validate_request(request)
        if validation is not None:
            return ReadResult.failure(validation, request_id=request.request_id)
        payload = build_og_payload(self._graph, request.operation, reference)
        if payload is None:
            return ReadResult.failure(Outcome.NOT_FOUND, request_id=request.request_id)
        return ReadResult.success(
            request_id=request.request_id,
            payload=payload,
            provenance=og_provenance(self._fixture_digest, payload),
        )
```

Build `Provenance` only from the selected synthetic OG root, `LogseqGraph`,
fixture manifest digest, and normalized result digest. For every unavailable
page, block, capability, or incomplete hierarchy, return the contract outcome;
do not use cached, exported, inferred, or flattened content.

Implement `build_og_payload(graph, operation, reference)` in the same module:
it returns a mapping for exactly the three operation identifiers, obtains pages
through `graph.get_page`, blocks through `graph.get_node_by_uuid`, and walks
each node's `children` depth-first in list order. It returns `None` for an
absent reference or an operation outside the three identifiers. For the subtree
operation it emits nested `children` rather than a flattened list. Implement
`og_provenance(fixture_digest, payload)` in the same module; it returns
`Provenance(source_mode="og_markdown", authority="logseq_og_markdown",
source_reference="fixture:og-minimal", evidence_digest=sha256_bytes(canonical_json(payload)))`.
`fixture_digest` remains the graph-binding value carried in the payload; the
evidence digest is the canonical result digest. Add direct tests for both
helpers, including a two-level ordered subtree.

- [ ] **Step 4: Run complete producer suite**

Run: `uv run --all-packages python -m unittest discover -s tests/contracts -v && uv run --all-packages python -m unittest discover -s tests/containment -v`

Expected: PASS. Static review finds no write, watcher, export, DB, or network
imports in `packages/logseq-og-adapter`.

- [ ] **Step 5: Commit OG adapter slice**

```bash
git add packages/logseq-og-adapter tests/contracts/test_og_read_contract.py
git commit -m "feat(logseq): add read-only OG contract adapter"
```

## Task 6: Add Plumber Consumer Compatibility Boundary

**Files:**
- Create: `packages/plumber-bridge/src/trama_plumber_bridge/consumer.py`
- Modify: `packages/plumber-bridge/src/trama_plumber_bridge/__init__.py`
- Test: `tests/integration/test_plumber_consumer.py`

**Interfaces:**
- Consumes: public `ReadResult` only; no Plumber source import.
- Produces: `accept_for_plumber(result: ReadResult, parser_version: str,
  plumber_version: str) -> Mapping[str, object]`.

- [ ] **Step 1: Write failing consumer tests**

```python
import unittest


class PlumberConsumerTests(unittest.TestCase):
    def success_result(self) -> ReadResult:
        return ReadResult.success(
            request_id="r1",
            payload={"operation": "graph.identify"},
            provenance=Provenance(
                source_mode="og_markdown",
                authority="logseq_og_markdown",
                source_reference="fixture:og-minimal",
                evidence_digest="a" * 64,
            ),
        )

    def test_consumer_rejects_missing_provenance(self) -> None:
        result = ReadResult.failure(Outcome.PROVENANCE_FAILURE, request_id="r1")
        with self.assertRaisesRegex(ValueError, "provenance_failure"):
            accept_for_plumber(result, parser_version="1.8.2", plumber_version="2.0.0")

    def test_consumer_rejects_parser_major_two(self) -> None:
        with self.assertRaisesRegex(ValueError, "incompatible"):
            accept_for_plumber(self.success_result(), parser_version="2.0.0", plumber_version="2.0.0")
```

- [ ] **Step 2: Run focused test to verify it fails**

Run: `uv run --all-packages python -m unittest tests.integration.test_plumber_consumer -v`

Expected: FAIL because the consumer boundary is absent.

- [ ] **Step 3: Implement public-envelope admission only**

```python
def accept_for_plumber(
    result: ReadResult, parser_version: str, plumber_version: str
) -> Mapping[str, object]:
    if result.outcome is not Outcome.SUCCESS:
        raise ValueError(result.outcome.value)
    require_supported_versions(parser_version, plumber_version)
    require_og_native_provenance(result.provenance)
    return result.payload
```

Accept Parser versions in `>=1.7.1,<2.0.0` and Plumber `2.0.0` only. Do not
add a Plumber dependency, retrieval call, CLI/MCP selection, write path, or
cross-repository import.

- [ ] **Step 4: Run producer and consumer suites**

Run: `uv run --all-packages python -m unittest discover -s tests -v`

Expected: PASS. The consumer rejects all non-success outcomes and non-native
authority without fallback.

- [ ] **Step 5: Commit consumer boundary slice**

```bash
git add packages/plumber-bridge tests/integration/test_plumber_consumer.py
git commit -m "feat(plumber): validate public read envelopes"
```

## Task 7: Add Hosted Contract Qualification Gate

**Files:**
- Create: `.github/workflows/python-contracts.yml`
- Modify: `docs/spikes/APPLICATION_STACK_QUALIFICATION.md`
- Create: `docs/spikes/evidence/python-read-contract-v1/README.md`
- Create: `tests/contracts/test_workflow_contract.py`

**Interfaces:**
- Consumes: Tasks 1–6 and the public qualification protocol.
- Produces: hosted Python evidence and a sanitized exact-commit qualification
  record.

- [ ] **Step 1: Write a failing workflow-contract test**

```python
import unittest


class WorkflowContractTests(unittest.TestCase):
    def test_python_contract_workflow_runs_locked_suite(self) -> None:
        workflow = Path(".github/workflows/python-contracts.yml").read_text()
        self.assertIn("uv sync --locked --all-packages", workflow)
        self.assertIn("python -m unittest discover -s tests -v", workflow)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run --all-packages python -m unittest tests.contracts.test_workflow_contract -v`

Expected: FAIL because the workflow does not exist.

- [ ] **Step 3: Implement smallest fork-safe workflow**

```yaml
name: Python contracts
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  contracts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
      - uses: astral-sh/setup-uv@20cfd1bf945f4377ade1205e4dbc17946fc9a30d # v10.0.1
      - run: uv sync --locked --all-packages
      - run: uv run --all-packages python -m unittest discover -s tests -v
```

Pin every action to a reviewed full SHA. Do not add secrets, cache uploads,
artifact publication, deployment, or privileged pull-request triggers.

- [ ] **Step 4: Run local workflow-contract and full test suite**

Run: `uv run --all-packages python -m unittest discover -s tests -v`

Expected: PASS. Then inspect hosted CI on the exact pull-request head.

- [ ] **Step 5: Record sanitized qualification evidence and commit**

`README.md` defines evidence-file names as the exact 40-hex commit followed by
`.md`. Each evidence record names commit/tree, lockfile digest, fixture digests,
commands, platform, Python/`uv` versions, pass/fail outcomes, and explicitly
unsupported behavior. It contains no local path, vault content, credentials,
machine identity, container ID, or raw environment value.

```bash
git add .github/workflows/python-contracts.yml docs/spikes tests
git commit -m "ci: qualify Python read contract gate"
```

## Task 8: Review Qualification and Publish Narrow Claims

**Files:**
- Modify: `docs/ROADMAP.md`
- Modify: `docs/internal/PERSISTENT_GOAL.md`
- Modify: `docs/spikes/APPLICATION_STACK_QUALIFICATION.md`

**Interfaces:**
- Consumes: terminal hosted CI and exact qualification evidence from Task 7.
- Produces: only evidence-backed status vocabulary and next blocked decision.

- [ ] **Step 1: Verify every mandatory gate against exact evidence**

Review build, package-direction, contract, containment, determinism, read-only,
and platform rows. Any absent or failing row remains unqualified.

- [ ] **Step 2: Record qualified scope or explicit NO-GO**

If every row passes, state only: Python-first synthetic OG read-contract slice
is qualified on the exact recorded commit/platform. Do not claim user-graph,
DB, UI, distribution, performance, or write support. If any row fails, record
the failure and leave runtime admission blocked.

- [ ] **Step 3: Commit qualification disposition**

```bash
git add docs/ROADMAP.md docs/internal/PERSISTENT_GOAL.md docs/spikes
git commit -m "docs(quality): record Python contract qualification"
```

## Plan Self-Review

- **Spec coverage:** Tasks 1–6 cover Python/`uv`, public package boundaries,
  synthetic fixtures, deterministic results, containment, Parser and Plumber
  public boundaries, and all three read operations. Tasks 7–8 cover hosted CI
  and exact evidence. DB, UI, writes, events, Shadow, sync, export, recovery,
  and distribution remain excluded.
- **Dependency direction:** contracts are consumed by core and bridges; the OG
  adapter is sole fixture acquisition path; the Plumber bridge consumes the
  public envelope only. No package depends on an application layer or private
  product.
- **Risk controls:** every task starts with a failing focused test, preserves
  synthetic-only inputs, and ends with a narrow verification command and
  separate commit. Qualification cannot promote an absent or failing gate.
- **Scope boundary:** the plan contains no DB adapter, host selection, Tine
  write coordination, Nodi UI, release, or production graph activity.
