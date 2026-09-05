# Claim Ledger and Current-Head Qualification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reconcile Matryca Trama's implementation claims with durable evidence,
then qualify one exact public head without claiming support beyond the bounded
synthetic OG profile.

**Architecture:** The delivery program owns current status; the claim ledger
records each claim, exact revision, evidence, and limitation. The qualification
run is split into a reviewable source revision, terminal evidence for that exact
revision, and a durable evidence reference. This avoids a circular claim in
which a later documentation commit is described as the commit that was tested.

**Tech Stack:** Python 3.12+, `uv`, standard-library `unittest`, GitHub Actions,
Markdown, Git.

**Spec:**
[`docs/specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md`](../../specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md)

## Global Constraints

- Begin from a clean isolated worktree and reverify `origin/main`, selected
  branch, exact HEAD, tree, and dirty state.
- The existing qualified baseline is
  `862c5c89157f28c1985cde6145fc2c8af04a70b4`; it is not a current-head claim.
- The current bounded scope is synthetic OG fixtures and only
  `graph.identify`, `page.read`, and complete ordered
  `block.subtree.read.complete`.
- Public evidence never contains vault text, local paths, credentials, generated
  databases, private source, or machine identifiers.
- Do not add a DB host, write, watcher, event, Shadow, sync, export, recovery,
  UI, network, distribution, Brain, Pro, or commercial capability.
- Use only public Parser and Plumber contracts. Do not add sibling-path imports
  or copy cross-repository DTO semantics.
- Commit, push, PR, merge, hosted workflow rerun, evidence publication, and
  release are separate authorization gates.

---

### Task 1: Reverify and record V0 anchors

**Files:**

- Verify: `docs/specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md`
- Verify: `docs/status/CLAIM_LEDGER.md`
- Verify: `docs/spikes/evidence/python-read-contract-v1/`
- Create: `docs/status/receipts/<UTC-date>-v0-anchor-audit.md`

**Interfaces:**

- Consumes: selected isolated worktree and live remote state.
- Produces: a sanitized V0 receipt with repository, branch, base, HEAD, tree,
  status, baseline evidence path, and explicit unknowns.

- [ ] **Step 1: Select a clean worktree**

Run:

```bash
git fetch origin --prune
git status --short --branch
git rev-parse HEAD
git rev-parse HEAD^{tree}
git rev-parse origin/main
```

Expected: selected branch and `origin/main` are recorded; no unrelated changes
are incorporated; dirty work is preserved rather than reset or stashed.

- [ ] **Step 2: Compare the candidate to the qualified baseline**

Run:

```bash
git diff --name-only 862c5c89157f28c1985cde6145fc2c8af04a70b4..HEAD -- pyproject.toml uv.lock packages tests .github/workflows/python-contracts.yml
git rev-parse 862c5c89157f28c1985cde6145fc2c8af04a70b4^{tree}
```

Expected: report exact differences or equality. Either result remains comparison
evidence only; do not call it current-head qualification.

- [ ] **Step 3: Write the receipt**

Record only sanitized facts in the following shape:

```markdown
# V0 anchor audit

- Candidate revision: `<40-hex SHA>`; tree: `<40-hex SHA>`
- Remote main: `<40-hex SHA>`
- Baseline revision: `862c5c89157f28c1985cde6145fc2c8af04a70b4`
- Worktree state: `clean` or `dirty; preserved`
- Runtime comparison: `<exact paths and result>`
- Known qualification: `<bounded baseline scope>`
- Unknowns: `<explicit list>`
- Next gate: `V1 exact-head local qualification`
```

- [ ] **Step 4: Validate links and policy docs**

Run:

```bash
python3 scripts/validate_foundation.py
git diff --check
```

Expected: zero exit status.

- [ ] **Step 5: Commit the V0 documentation slice**

```bash
git add docs/status docs/specs docs/ROADMAP.md docs/internal README.md docs/ARCHITECTURE.md docs/contracts docs/decisions docs/superpowers
git commit -m "docs: reconcile Trama delivery claims"
```

Expected: one reviewable source revision. Stop before push unless separately
authorized.

### Task 2: Make claim-ledger presence mechanically enforceable

**Files:**

- Modify: `scripts/validate_foundation.py`
- Modify: `tests/test_foundation_validator.py`
- Verify: `docs/specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md`
- Verify: `docs/status/CLAIM_LEDGER.md`

**Interfaces:**

- Consumes: the foundation validator's `REQUIRED` set and temporary-repository
  fixture helper.
- Produces: a deterministic failure if the canonical delivery program or claim
  ledger is removed.

- [ ] **Step 1: Add failing tests**

Add two tests using the existing temporary repository helper:

```python
def test_missing_delivery_program_is_rejected(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        create_minimum_repository(root)
        (root / "docs/specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md").unlink()
        result = run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required file: docs/specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md", result.stderr)

def test_missing_claim_ledger_is_rejected(self) -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        create_minimum_repository(root)
        (root / "docs/status/CLAIM_LEDGER.md").unlink()
        result = run_validator(root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required file: docs/status/CLAIM_LEDGER.md", result.stderr)
```

- [ ] **Step 2: Prove RED**

Run:

```bash
uv run --all-packages python -m unittest tests.test_foundation_validator -v
```

Expected: both new tests fail because the fixture helper and validator do not yet
require the two files.

- [ ] **Step 3: Add minimum fixture content and required paths**

Add these exact paths to both `REQUIRED` sets:

```python
"docs/specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md",
"docs/status/CLAIM_LEDGER.md",
```

Extend `create_minimum_repository()` so the two files are created with ordinary
UTF-8 placeholder content. Do not add a parser for status prose in this task;
the validator enforces presence and existing link validation only.

- [ ] **Step 4: Prove GREEN**

Run:

```bash
uv run --all-packages python -m unittest tests.test_foundation_validator -v
python3 scripts/validate_foundation.py
```

Expected: all validator tests and the repository validation pass.

- [ ] **Step 5: Commit the deterministic policy gate**

```bash
git add scripts/validate_foundation.py tests/test_foundation_validator.py
git commit -m "test: require Trama claim ledger"
```

Expected: a small independent commit. Stop before push unless separately
authorized.

### Task 3: Run V1 local exact-head qualification

**Files:**

- Create: `docs/status/receipts/<UTC-date>-v1-local-qualification.md`
- Verify: `uv.lock`, `tests/`, `packages/`, `.github/workflows/python-contracts.yml`

**Interfaces:**

- Consumes: the exact commit created by Tasks 1–2 and its locked workspace.
- Produces: a sanitized local receipt that is explicitly local, not a hosted or
  release qualification.

- [ ] **Step 1: Rebind exact candidate**

Run:

```bash
git status --short --branch
git rev-parse HEAD
git rev-parse HEAD^{tree}
shasum -a 256 uv.lock
```

Expected: clean candidate revision, tree, and lock digest are recorded before
tests begin.

- [ ] **Step 2: Install from lock without global cache dependence**

Run:

```bash
UV_CACHE_DIR=/private/tmp/matryca-trama-v1-uv-cache uv sync --locked --all-packages
```

Expected: a reproducible public dependency environment. Any private source,
lock mismatch, or installation failure blocks V1.

- [ ] **Step 3: Run the hosted-equivalent suite locally**

Run:

```bash
UV_CACHE_DIR=/private/tmp/matryca-trama-v1-uv-cache uv run --all-packages python -m unittest discover -s tests/contracts -v
UV_CACHE_DIR=/private/tmp/matryca-trama-v1-uv-cache uv run --all-packages python -m unittest discover -s tests/containment -v
UV_CACHE_DIR=/private/tmp/matryca-trama-v1-uv-cache uv run --all-packages python -m unittest tests.integration.test_plumber_consumer -v
UV_CACHE_DIR=/private/tmp/matryca-trama-v1-uv-cache uv run --all-packages python -m unittest tests.test_foundation_validator -v
python3 scripts/validate_foundation.py
git diff --check
```

Expected: terminal zero exit status for every command. Record individual test
counts; never collapse skipped, failed, or unrun suites into PASS.

- [ ] **Step 4: Write a local-only receipt**

Record candidate revision/tree, lock digest, Python/uv version, operating-system
family, commands, per-suite counts, outcome, limitations, and the next hosted
gate. Omit user name, local path, machine serial, vault content, and raw logs.

- [ ] **Step 5: Commit local evidence without overstating it**

```bash
git add docs/status/receipts
git commit -m "docs: record local Trama qualification"
```

Expected: receipt refers to the preceding tested revision as
`qualified_revision` and to its own commit as `evidence_revision`.

### Task 4: Obtain exact-head hosted evidence

**Files:**

- Create only after terminal hosted checks: an immutable evidence reference or
  sanitized record under `docs/spikes/evidence/python-read-contract-v1/`.
- Verify: `.github/workflows/python-contracts.yml`, Foundation CI, dependency review.

**Interfaces:**

- Consumes: an explicitly authorized pushed PR head.
- Produces: terminal hosted evidence for the exact PR head, not merely for a
  local ancestor or merge base.

- [x] **Step 1: Request explicit push and PR authorization**

Do not push, create a PR, or rerun a workflow without the maintainer's separate
authorization. Reverify `origin/main`, PR base, selected head, checks, and
review requirements immediately before the mutation.

- [x] **Step 2: Push the selected source revision and open one PR**

Expected: the PR targets current `main`, has a narrow V0/V1 description, and
does not claim a release, DB, user-graph, or production integration.

- [x] **Step 3: Wait for terminal checks on the exact PR head**

Required named checks:

```text
foundation
dependency-review
python-contracts
```

Expected: every check is terminal and successful on the exact `headRefOid`.
Cancelled, skipped, or ancestor results block V1.

- [x] **Step 4: Preserve durable public evidence**

Use a maintainer-approved append-only evidence branch or immutable attestation
keyed by the qualified `headRefOid`. Record check URLs, workflow names, run IDs,
revision/tree, lock digest, fixture digest, platform/runtime, counts, and
limitations. Never put raw logs, local paths, vault data, credentials, or
machine identifiers in public evidence.

- [x] **Step 5: Stop at the merge gate**

After evidence verification, report the exact qualified revision, evidence
reference, checks, residual unsupported scope, and merge decision. Do not merge
without a separate explicit authorization.

### Task 5: Post-merge current-main reconciliation

**Files:**

- Modify only with a new authorization: `docs/status/CLAIM_LEDGER.md`
- Create only with a new authorization: `docs/status/receipts/<UTC-date>-v1-main-reconciliation.md`

**Interfaces:**

- Consumes: an explicitly authorized and verified merge to `main`.
- Produces: a claim only for the exact merged main revision and its terminal
push workflow, preserving the PR-head evidence separately.

- [x] **Step 1: Fetch and bind merged `origin/main`**

Run:

```bash
git fetch origin --prune
git rev-parse origin/main
git show --no-patch --format=fuller origin/main
```

Expected: recorded main revision is the selected merge result, not an assumed
local branch tip.

- [x] **Step 2: Verify push-workflow evidence for that exact revision**

Expected: terminal Foundation and Python-contract push checks are attached to
the exact merged main revision. Dependency Review stays PR-scoped and remains
bound to the exact PR base/head; an identical PR-head/main tree corroborates
provenance only. If push evidence is absent, leave `V1-CURRENT-001` blocked.

- [x] **Step 3: Add a new ledger entry; do not rewrite history**

Use this shape:

```markdown
| `V1-CURRENT-<sequence>` | Qualified current head | Synthetic OG scope only. | `<merged SHA>` | `<immutable hosted evidence URL>` | `<all unsupported profiles>` |
```

- [x] **Step 4: Stop before V2 execution**

V2 needs a separate approved implementation plan. Do not broaden Parser,
Plumber, OG, DB, Nodi, agent, distribution, or release claims as a side effect
of V1.

## Plan self-review

- [ ] V0 records anchors and contradictions without changing runtime scope.
- [ ] Task 2 has explicit RED/GREEN coverage for the new policy paths.
- [x] V1 binds local and hosted evidence to the exact tested revision.
- [x] Evidence commits and tested revisions remain distinct when necessary.
- [x] Push, PR, evidence publication, and merge remain explicit external gates.
- [x] No task introduces a DB, write, user-graph, network, UI, commercial, or
  private-source claim.
