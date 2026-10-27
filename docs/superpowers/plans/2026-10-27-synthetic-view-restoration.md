# Synthetic View Restoration Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans. Direct-main is
> selected: the primary implements and an independent Astra Medium reviews.
> Local Beads is the execution ledger; these checkboxes describe the plan.

**Goal:** Back/Forward returns to the fictional exploration view with its map
centre, zoom and document/list/detail scrolling, alongside existing semantics.

**Architecture:** Keep semantic history entries and `historyState()` unchanged.
Associate a nullable presentation snapshot with each bounded entry. Pure
snapshot bookkeeping belongs in `state.js`; renderer/DOM capture and restore
belong in `app.js`. No source, transport, persistence or dependency changes.

**Tech Stack:** Existing JavaScript, Node built-in tests, Python validators and
the already bundled vis-network renderer.

**Spec:** [Research delivery proposal, Section 8.3](https://github.com/MarcoPorcellato/matryca-trama/blob/6c15e18bf6cec0e4046c6012daae93e3c04292d4/docs/research/2026-10-27-logseq-demand-and-trama-opportunities.md#83-slice-1--return-to-the-previous-exploration-view),
approved for autonomous execution by the owner on 2026-10-27.

## Global constraints

- Base: verified main `51ddc684249d6e8c02ba991e23a972f8a0a58ba1` in the existing
  isolated worktree. Preserve the local research dossier and primary checkout.
- PR #43 remains a separate unmerged draft. Do not duplicate its controls or
  merge it. This slice works against the current main without those shortcuts.
- Only the built-in fictional data. No MA attempt, producer/comparator,
  installation, real graph, source adapter, storage, browser-global history,
  source configuration write, named layout or manual node-coordinate capture.
- Preserve 100-entry history, coalescing, collapse, branching and no-op rules.
  Reset/reload clear all captures. Pan/zoom/scroll never add history steps.
- Keep renderer bytes, CSP, Python/core/client/qualification files and workflow
  triggers unchanged. Inspect changed paths before any later source PR.
- This plan and the research are separate deliverables. The owner authorized a
  dedicated GitHub PR for the research; neither PR is automatically merged.

## Approaches and chosen design

Embedding renderer state in semantic view values would couple filtering and
navigation to DOM details. A global camera would lose per-step positions.
Use an aligned `presentations` array owned by the history wrapper instead;
`historyState(history)` continues returning its existing semantic value.
This is an implementation choice within the approved session-only design.

`historyPresentation(history)` returns the current nullable capture.
`rememberPresentation(history, snapshot)` validates and copies a capture without
changing the cursor, Forward path or search-group marker. A capture contains
`camera: null | {x, y, scale}` and `scroll: {page, list, details}`, each scroll
position `{x, y}`. All coordinates must be finite; scale must be positive and
scroll coordinates nonnegative. Invalid captures retain the previous history.

Capture the departing view before a real navigation. A new semantic entry
starts without its own capture; coalescing replaces only the current capture,
while collapsing restores the predecessor's capture. Preserve alignment under
branch truncation and eviction. DOM/renderer changes can refresh the current
capture without becoming navigation actions. Invalid/no-op actions retain their
existing behavior. No automatic fit/focus may override a restored camera.

Restore scroll after rendering and keyboard-focus correction; the browser
clamps positions to the current content/viewport. Missing renderer means a null
camera, with list and history still usable. The Find a path disclosure remains
a current layout choice; it is not new semantic history state. Changed layout
can clamp scrolling, as documented, rather than inventing content/coordinates.

## Review focus

**Reviewed ruling:** Use immediate app-owned selection focus, retaining its
centering and zoom rules. Bundled vis-network can leave a transition pending
when interrupted before its first animation frame. Removing the former 250 ms
selection animation avoids that race through the public API; no vendor patch
or private renderer access is introduced. Astra Medium accepted this tradeoff.

- Search coalescing/collapse must preserve the predecessor's capture and bound.
- Rapid Back/Forward must not be overwritten by pending fitting or animation.
- Rebuilt lists, disabled-button focus and responsive reflow must not reset
  successfully restored scroll positions.
- Empty views, absent renderer and invalid captures retain usable navigation.
- Reset clears both semantic and presentation history without restoring stale
  coordinates; zoom/scroll alone preserve Forward and search grouping.

## Task 1: Pure presentation-history bookkeeping

**Files:** `apps/synthetic_demo/web/state.js`, `tests/demo/test_state.cjs`.

- [x] Obtain Astra Medium plan review before product edits.
- [x] Add focused failing tests for snapshot validation/copying, separate
  semantic values, navigation, coalescing/collapse, no-op preservation,
  truncation/eviction, frozen inputs and reset; observe RED.
- [x] Add the two exports and aligned captures, preserving reducer behavior.
- [x] Run existing and added Node history/path tests; require GREEN.

## Task 2: Browser capture and restoration

**Files:** `apps/synthetic_demo/web/app.js`, `tests/demo/test_state.cjs`,
`tests/demo/app_harness.cjs`, `README.md`, and `docs/ROADMAP.md`. The helper
supplies DOM/renderer doubles to tests registered in the existing Node suite;
the hosted workflow command and its contract remain unchanged.

- [x] Add failing app-composition checks with DOM/renderer doubles that observe
  actual capture/restore calls, scroll/focus ordering and absent renderer.
- [x] Connect current-view capture and immediate, non-animated restore.
  Retain existing focus/fit behavior for new views and explicit reselection.
- [x] Test Back/Forward with Focus, path endpoints, search grouping, empty
  views, resized layouts and cancellation of pending initial/animated fitting.
- [ ] Build the fictional HTML and verify real browser round trips at desktop
  and narrow widths; check keyboard boundaries and reduced-motion behavior.
- [x] Update user documentation with session-only restoration and clamping.
- [x] Run ordinary demo/architecture/foundation checks and focused regressions;
  do not invoke provisioners, qualification runners or producers.
- [x] Obtain independent Astra Medium source review on the exact candidate;
  correct meaningful findings and recheck affected behavior.
- [ ] Update Beads with evidence and remaining publication/merge status.

## Verification

Use the existing dependencies. No installation is required.

```bash
rtk proxy node --test tests/demo/*.cjs
rtk proxy .venv/bin/python -m unittest discover -s tests/demo -v
rtk proxy .venv/bin/python scripts/validate_architecture.py
rtk proxy .venv/bin/python scripts/validate_synthetic_demo.py
rtk proxy .venv/bin/python scripts/validate_foundation.py
rtk proxy .venv/bin/python -m apps.synthetic_demo
rtk proxy git diff --check
```

These checks prove only the selected fictional presentation. Beads records
observed results. Source publication, hosting, admission and merging remain
separate from a review verdict.

## Observed verification and limits

The seven new pure-history cases first failed for missing exports. Six initial
app-composition cases failed on absent restoration. The renderer-specific
first-frame animation race was then reproduced with a corrected boundary
double before the immediate-focus fix. All 55 Node tests passed afterward.
All 253 ordinary Python tests, architecture/demo/foundation validators and
whitespace checks passed. A restricted loopback denial was inconclusive; only
the ten affected demo tests were repeated with local-listener permission.

The actual 1280 × 720 browser restored a selected page with page scroll 266 and
list scroll 360. Three screenshot map-region comparisons showed zero differing
pixels across Back, Forward and a panned/zoomed return. Search collapse, empty
results, Focus-neighbor navigation, path endpoints and keyboard boundary focus
were exercised. The initial differing image comparison used automated scrolling
and the earlier animated candidate; it was retained as inconclusive diagnosis.

The requested 390 × 844 override did not change the browser: both existing and
new tabs reported 1280 × 720. Those keyboard checks are desktop evidence;
the narrow browser step above remains unqualified. Real detail-scroll overflow
was unavailable with the short built-in fixture; nonzero detail scrolling and
reflow clamping are covered by the app-composition tests. A local diagnostic
file was rejected by browser URL policy and was not opened through a workaround.
No diagnostic observer or elongated fixture is part of the product candidate.

These are presentation-test limits, not source/runtime admission. Beads holds
the current review and publication disposition without creating another ledger.

Independent final Astra Medium review returned **PASS_WITH_NOTES** after
verifying the seven candidate paths and exact source hashes. No important
source defect remained. The reviewer accepted the explicit evidence limits as
nonblocking for this bounded synthetic delivery; the combined browser checkbox
remains incomplete, without claiming narrow-browser qualification.
