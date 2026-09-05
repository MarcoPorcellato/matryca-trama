# Matryca Trama Public Foundation Implementation Plan

> **Historical plan:** checkboxes preserve the original planning and execution
> record. Current status is governed by the
> [delivery program](../../specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md).

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> `superpowers:subagent-driven-development` (recommended) or
> `superpowers:executing-plans` to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish and qualify the public source-available Community Matryca Trama repository
without exposing Pro, Brain, vault, credential, or legacy-history material.

**Architecture:** Documentation and policy define the authority and product
boundaries before application code. A small dependency-free validator enforces
the foundation locally and in fork-safe GitHub Actions.

**Tech Stack:** Markdown, Python 3 standard library, Git, GitHub Actions.

**Spec:** `docs/specs/MATRYCA_TRAMA_PUBLIC_MONOREPO_FOUNDATION.md`

## Global Constraints

- PolyForm Noncommercial 1.0.0 covers repository-owned Community material;
  commercial use requires a separate agreement.
- External copyright-bearing contributions are not merged until a
  lawyer-reviewed dual-path contributor grant exists.
- Pro and Matryca Brain source are excluded.
- Legacy repository history and generated artifacts are not imported.
- Logseq OG Markdown and the Logseq DB native store retain distinct authority.
- Pull-request checks receive no secrets and cannot publish.
- Every completion claim binds an exact commit and fresh evidence.

---

### Task 1: Qualify the document-first foundation

**Files:**
- Verify: all root governance and licensing files, `docs/**`, `.github/**`
- Create: `scripts/validate_foundation.py`
- Create: `.github/workflows/foundation.yml`
- Create: `.github/workflows/dependency-review.yml`

**Interfaces:**
- Consumes: the canonical specification and accepted ADRs.
- Produces: `python3 scripts/validate_foundation.py` as the stable local and CI
  foundation gate.

- [ ] Run `python3 scripts/validate_foundation.py` and record a zero exit code.
- [ ] Run `git diff --check` and record a zero exit code.
- [ ] Confirm every `uses:` reference is pinned to a verified full commit SHA.
- [ ] Commit the complete foundation as one reviewable documentation slice.
- [ ] Push the topic branch and open a pull request against current `main`.
- [ ] Confirm hosted checks are terminal and green on the exact PR head.
- [ ] Merge only after maintainer approval and reverify `origin/main`.

### Task 2: Establish GitHub planning surfaces

**Files:**
- Verify: `docs/ROADMAP.md`
- Update: `docs/specs/MATRYCA_TRAMA_PUBLIC_MONOREPO_FOUNDATION.md`

**Interfaces:**
- Consumes: merged Foundation evidence.
- Produces: one foundation milestone and issues mapped one-to-one to roadmap
  phases without implementation promises.

- [ ] Create labels for area, type, priority, and evidence status.
- [ ] Create a Foundation milestone with no invented delivery date.
- [ ] Create one issue for each next qualified decision or implementation slice.
- [ ] Link issues to their roadmap phase and acceptance evidence.
- [ ] Comment on Matryca Brain issue #430 with the public repository and ADR link.
- [ ] Record created URLs in the canonical specification.

### Task 3: Select the application stack through evidence

**Files:**
- Create: `docs/decisions/ADR-0004-APPLICATION-STACK.md`
- Create: `docs/spikes/APPLICATION_STACK_QUALIFICATION.md`
- Update: `docs/ROADMAP.md`

**Interfaces:**
- Consumes: accepted product, authority, licensing, and repository boundaries.
- Produces: an accepted stack decision with a runnable minimal sidecar spike and
  measured platform evidence.

- [ ] Define desktop, accessibility, packaging, update, filesystem, Logseq OG,
  Logseq DB, and Nodi evaluation criteria before testing candidates.
- [ ] Build each candidate spike without importing private code.
- [ ] Measure cold start, idle memory, artifact size, filesystem confinement,
  and platform support using identical fixtures.
- [ ] Record negative results and unsupported platforms.
- [ ] Accept ADR-0004 only when one candidate satisfies every mandatory gate.
- [ ] Create `apps/` and `packages/` only after ADR-0004 is accepted.

**Current direction:** the maintainer selected Python 3.12+ with `uv` as the
first Community stack. Architecture direction is accepted through ADR-0004;
runtime admission remains blocked until the qualification protocol records the
mandatory evidence. No `apps/` or `packages/` directory is created by this
documentation delivery.

### Task 4: Define Parser and Plumber contracts

**Files:**
- Create: `docs/contracts/PARSER_COMPATIBILITY.md`
- Create: `docs/contracts/PLUMBER_COMPATIBILITY.md`
- Create: contract fixtures and tests under paths selected by ADR-0004.
- Update: `docs/ROADMAP.md`

**Interfaces:**
- Consumes: released public Parser and Plumber APIs plus ADR-0004.
- Produces: version negotiation, provenance fields, typed failures, sanitized
  fixtures, and executable compatibility tests.

- [ ] Pin the minimum supported Parser and Plumber versions from released APIs.
- [ ] Write failing tests for accepted and rejected compatibility profiles.
- [ ] Implement the smallest public adapters that satisfy the tests.
- [ ] Run contract, determinism, and source-provenance tests.
- [ ] Document unsupported versions and upgrade behavior.
- [ ] Deliver through a separate exact-head pull request.

### Task 5: Qualify OG, DB, and Nodi vertical slices

**Files:**
- Create: implementation and tests in the ADR-0004 package layout.
- Create: `docs/decisions/ADR-0005-LOGSEQ-DB-AUTHORITY.md`
- Create: `docs/decisions/ADR-0006-NODI-STATE-CONTRACT.md`
- Update: `docs/ROADMAP.md`

**Interfaces:**
- Consumes: qualified core contracts and native source-authority rules.
- Produces: one read-only OG insight, one read-only DB insight, and one truthful,
  accessible Nodi state driven only by derived authorized data.

- [ ] Implement the OG slice test-first against synthetic Markdown fixtures.
- [ ] Implement the DB slice test-first with no write capability.
- [ ] Prove both slices retain native provenance and reject unsupported input.
- [ ] Implement deterministic Nodi state transitions and accessibility checks.
- [ ] Run all supported-platform, containment, and no-network default checks.
- [ ] Deliver each independently reviewable vertical slice through its own PR.

### Task 6: Rehearse the first Community release

**Files:**
- Create: release, SBOM, provenance, support-matrix, and recovery documentation.
- Create: trusted-tag release workflows after action SHA review.
- Update: `CHANGELOG.md`, `README.md`, and `docs/ROADMAP.md`.

**Interfaces:**
- Consumes: qualified application, contracts, adapters, and Nodi slices.
- Produces: reproducible Community artifacts containing no Pro or Brain material.

- [ ] Build release artifacts twice from the same clean commit and compare them.
- [ ] Generate and verify SBOM, checksums, licences, and attestations.
- [ ] Install and smoke-test every claimed platform artifact.
- [ ] Verify downgrade, uninstall, data preservation, and no-network defaults.
- [ ] Run a release rehearsal without publication.
- [ ] Publish only after a separate maintainer release authorization.
