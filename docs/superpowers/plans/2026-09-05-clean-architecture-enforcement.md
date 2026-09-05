# Clean Architecture Enforcement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make Matryca Trama package boundaries, dependency metadata, review discipline, and repository-local agent guidance durable and fail-closed.

**Architecture:** A standard-library AST validator reads one root machine map and each package manifest, then checks real production imports and time-bounded exceptions. Human policy remains canonical; CI, tests, contributor guidance, and a concise repository skill project that policy into repeatable workflows.

**Tech Stack:** Python 3.12+, `ast`, `tomllib`, `unittest`, `uv`, GitHub Actions, Markdown, Codex repository skills.

**Spec:** `docs/superpowers/specs/2026-09-05-clean-code-clean-architecture.md`

## Global Constraints

- Preserve Logseq OG Markdown and Logseq DB native source as separate authorities.
- Do not add DB access, writes, events, Shadow, synchronization, export, recovery, network, Nodi runtime, Brain, Pro, entitlement, pricing, or commercial rights.
- Keep PolyForm Noncommercial 1.0.0; external copyright-bearing contributions remain merge-blocked pending a lawyer-reviewed contributor agreement or equivalent grant.
- Use only Python standard library for architecture validation.
- Current mechanical violations fail closed; initial exception registry is empty.
- Policy lives in docs; executable configuration and skill must not duplicate normative prose.
- Preserve fork-safe CI: read-only permissions, full-SHA actions, bounded timeout, no secrets, deployment, or artifact publication.

---

### Task 1: Accept repository architecture policy

**Files:**
- Create: `docs/decisions/ADR-0005-CLEAN-ARCHITECTURE-ENFORCEMENT.md`
- Create: `docs/standards/CLEAN_ARCHITECTURE.md`
- Modify: `docs/decisions/README.md`
- Modify: `docs/ARCHITECTURE.md`
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: accepted design in `docs/superpowers/specs/2026-09-05-clean-code-clean-architecture.md`.
- Produces: canonical layer names, dependency directions, exception policy, and review rules referenced by later tasks.

- [ ] **Step 1: Write ADR-0005**

Record the accepted standard-library checker, fail-closed structural rules,
zero-exception start, qualitative Clean Code review boundary, and deferred
personal/global skill installation.

- [ ] **Step 2: Write the canonical standard**

Include the package table from the spec, dependency declaration rule, exception
fields, TDD expectations, exact local validation commands, and stop gates.

- [ ] **Step 3: Link policy surfaces**

Update the ADR index, architecture overview, and agent guidance to point to the
canonical standard without copying it.

- [ ] **Step 4: Validate documentation**

Run:

```bash
python3 scripts/validate_foundation.py
git diff --check
```

Expected: both exit `0`.

- [ ] **Step 5: Commit**

```bash
git add AGENTS.md docs/ARCHITECTURE.md docs/decisions docs/standards docs/superpowers/specs/2026-09-05-clean-code-clean-architecture.md docs/superpowers/plans/2026-09-05-clean-architecture-enforcement.md
git commit -m "docs(architecture): accept clean architecture policy"
```

### Task 2: Build the dependency validator with TDD

**Files:**
- Create: `architecture.toml`
- Create: `scripts/validate_architecture.py`
- Create: `tests/architecture/__init__.py`
- Create: `tests/architecture/test_dependency_boundaries.py`

**Interfaces:**
- Consumes: package rules from `docs/standards/CLEAN_ARCHITECTURE.md`.
- Produces: `validate_repository(root: Path) -> list[Violation]`, `Violation(path: Path, line: int, code: str, message: str)`, and CLI exit `0` only for a clean repository.

- [ ] **Step 1: Write manifest and forbidden-edge tests**

Create temporary fixture repositories with literal `pyproject.toml`,
`architecture.toml`, and source files. Cover unregistered packages, contracts to
core, core to adapter, OG adapter to Parser, undeclared internal dependencies,
Parser internals, Brain/Pro roots, dynamic import, and `sys.path` mutation.

- [ ] **Step 2: Verify RED**

Run:

```bash
python -m unittest tests.architecture.test_dependency_boundaries -v
```

Expected: import failure for missing `scripts.validate_architecture` or missing
validator behavior, with each new case failing for its intended boundary.

- [ ] **Step 3: Implement minimal AST and manifest validator**

Use `ast.parse`, `tomllib`, `sys.stdlib_module_names`, and immutable dataclasses.
Report stable codes: `ARCH001` unregistered package, `ARCH002` forbidden internal
edge, `ARCH003` undeclared dependency, `ARCH004` forbidden external/private
import, `ARCH005` dynamic import/path mutation, and `ARCH006` invalid exception.

- [ ] **Step 4: Add allowed-edge and current-repository integration tests**

Prove same-package, standard-library, declared inward, and exact Parser-root
imports pass. Before Task 3, assert the real repository's exact known violations;
after Task 3, require zero findings.

- [ ] **Step 5: Verify GREEN**

Run:

```bash
python -m unittest tests.architecture.test_dependency_boundaries -v
```

Expected: all fixture tests pass.

- [ ] **Step 6: Commit**

```bash
git add architecture.toml scripts/validate_architecture.py tests/architecture
git commit -m "test(architecture): enforce dependency boundaries"
```

### Task 3: Repair package isolation and Parser ownership

**Files:**
- Modify: `pyproject.toml`
- Modify: `packages/parser-bridge/pyproject.toml`
- Modify: `packages/logseq-og-adapter/pyproject.toml`
- Modify: `packages/plumber-bridge/pyproject.toml`
- Modify: `packages/parser-bridge/src/trama_parser_bridge/__init__.py`
- Modify: `packages/logseq-og-adapter/src/trama_logseq_og_adapter/adapter.py`
- Modify: `tests/contracts/test_parser_loader.py`
- Modify: `tests/contracts/test_og_read_contract.py`
- Modify: `uv.lock`

**Interfaces:**
- Consumes: public Parser package-root objects in `trama-parser-bridge`.
- Produces: adapter-visible `LogseqGraph`, `LogseqNode`, and `LogseqPage` aliases through `trama_parser_bridge`; complete local dependency metadata; producer identity `trama-logseq-og-adapter 0.0.0`.

- [ ] **Step 1: Write failing ownership and producer tests**

Extend contract tests so the adapter consumes public bridge exports and its
reported producer version equals package metadata. Keep expected values literal.

- [ ] **Step 2: Verify RED**

Run:

```bash
python -m unittest tests.contracts.test_parser_loader tests.contracts.test_og_read_contract -v
python scripts/validate_architecture.py
```

Expected: direct Parser import, missing dependency declarations, and producer
version mismatch fail.

- [ ] **Step 3: Apply minimal refactor and metadata repair**

Re-export only the Parser package-root objects the adapter needs through parser
bridge. Replace adapter Parser imports with bridge imports. Declare local
dependencies and root workspace sources. Change producer identity to the real
distribution version.

- [ ] **Step 4: Refresh lock and build packages**

Run:

```bash
uv lock
uv build --all-packages
```

Expected: lock refresh and all workspace wheels build successfully.

- [ ] **Step 5: Verify GREEN**

Run:

```bash
python scripts/validate_architecture.py
python -m unittest tests.architecture.test_dependency_boundaries -v
python -m unittest discover -s tests/contracts -v
```

Expected: all pass; real repository has zero architecture findings.

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml packages tests/contracts uv.lock
git commit -m "refactor(packages): restore inward dependencies"
```

### Task 4: Create and behavior-test the repository skill

**Files:**
- Create: `.agents/skills/trama-development/SKILL.md`
- Create: `docs/quality/TRAMA_DEVELOPMENT_SKILL_EVIDENCE.md`

**Interfaces:**
- Consumes: canonical standard, relevant ADRs/contracts, validation commands, and recorded RED baseline.
- Produces: discoverable repository-local workflow that routes agents to authority and gates without restating policy.

- [ ] **Step 1: Record RED pressure scenario**

Before creating the skill, run an independent agent without it under deadline,
sunk-cost, and authority pressure. Record its exact choice, omissions, and
rationalizations in the evidence document.

- [ ] **Step 2: Write minimal skill**

Use lowercase name `trama-development`. Description begins with `Use when` and
contains only triggering conditions. Body requires authority discovery,
boundary classification, failing tests before behavior, architecture validation,
and explicit stops for legal, private-product, source-authority, write, and
publication gates.

- [ ] **Step 3: Validate skill structure**

Run bundled skill validation against `.agents/skills/trama-development` and
check entrypoint remains under 500 words.

- [ ] **Step 4: Verify GREEN with independent agent**

Repeat the same pressure scenario with only the new skill added. Require the
agent to preserve parser-bridge ownership, name exact checks, and stop at all
non-waivable boundaries. Record actual response and any remaining gap.

- [ ] **Step 5: Refactor and re-test if needed**

Change only wording supported by observed failure. Repeat until the scenario
passes without new rationalization.

- [ ] **Step 6: Commit**

```bash
git add .agents/skills/trama-development docs/quality/TRAMA_DEVELOPMENT_SKILL_EVIDENCE.md
git commit -m "docs(skill): guide Trama boundary-safe development"
```

### Task 5: Integrate review and CI evidence

**Files:**
- Modify: `.github/workflows/python-contracts.yml`
- Modify: `.github/pull_request_template.md`
- Modify: `CONTRIBUTING.md`
- Modify: `docs/ROADMAP.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: architecture CLI, standard, skill, and repaired workspace.
- Produces: fork-safe required execution path and contributor-visible evidence contract.

- [ ] **Step 1: Add architecture CI step**

Run `uv run --all-packages python scripts/validate_architecture.py` immediately
after locked workspace installation and before contract suites.

- [ ] **Step 2: Update contributor and PR evidence**

Require affected packages, boundary impact, architecture result, exception IDs
or `none`, source-authority impact, tests, limits, and contribution eligibility.

- [ ] **Step 3: Update roadmap and README navigation**

Link accepted standard and skill. Keep implementation claims bounded to local
branch until publication and hosted evidence occur.

- [ ] **Step 4: Run complete verification**

Run:

```bash
uv sync --locked --all-packages
uv run --all-packages python scripts/validate_architecture.py
uv run --all-packages python -m unittest discover -s tests/architecture -v
uv run --all-packages python -m unittest discover -s tests/contracts -v
uv run --all-packages python -m unittest discover -s tests/containment -v
uv run --all-packages python -m unittest tests.integration.test_plumber_consumer -v
uv run --all-packages python -m unittest tests.test_foundation_validator -v
uv run --all-packages python scripts/validate_foundation.py
git diff --check
```

Expected: every command exits `0`, no active exception, and no generated build
artifact enters the commit.

- [ ] **Step 5: Review scope and commit**

```bash
git status --short
git diff --stat
git diff --check
git add .github CONTRIBUTING.md README.md docs/ROADMAP.md
git commit -m "ci(architecture): require boundary evidence"
```

Stop before push, pull request, merge, GitHub mutation, release, licence change,
or personal/global skill installation.
