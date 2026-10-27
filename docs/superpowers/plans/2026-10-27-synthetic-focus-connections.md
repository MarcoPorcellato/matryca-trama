# Focus Connections Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.
> Direct-main: primary implements; Astra Medium reviews. Steps use checkboxes.
> Local Beads `matryca-trama-l5a.22` is the execution authority; no duplicate
> SDD ledger or receipt dossier is created.

**Goal:** Explore a fictional node and its immediate connections with a clear
Show all exit, preserving filters and navigation history.

**Architecture:** A pure filtered-graph projection feeds a one-hop presentation
scope. The existing reducer/history stores that scope and the existing UI
renders its current graph. No provider or domain package changes.

**Tech Stack:** Existing plain JavaScript/CSS/HTML, Node built-in tests, Python
workspace and admitted renderer. No new dependency or installation.

**Spec:** [Focus connections design](../specs/2026-10-27-synthetic-focus-connections-design.md).

## Global Constraints

- Base `991d9b1fc9c55842b90e08dae409ee3f4238c01d`; reuse clean linked worktree
  on `feat/synthetic-focus-connections`; preserve primary and prior archives.
- Fictional fixture only. No MA, producer/comparator, real graph, source client,
  payload, persistence, new dependency or other-repository work.
- Keep English/source notices, literal text/CSP, renderer/licenses, Python/core/
  client/lock/qualification inputs/workflows unchanged.
- Scope joins complete view snapshots; retain 100-entry history and all current
  search/branch/no-op/reset rules. Show all keeps filters and selection.
- Astra plan gate before code; fresh Astra final gate after tests. Draft source
  PR only, no automatic merge/hosting. Reverify qualifier path exclusion.

## Review Focus

- Filters hiding a center must clear focus without revealing excluded nodes.
- Neighbor selection must derive a fresh one-hop view, not shrink the old one.
- Scope-only changes must be meaningful history entries and survive restoration.
- Isolated/empty views need a useful exit and valid native keyboard focus.
- All retained connections must fit together; controls must wrap on mobile.

## Task 1: Pure filtered and focused view state

**Files:** Modify `apps/synthetic_demo/web/state.js` and `tests/demo/test_state.cjs`.

**Interfaces:** Add `filteredGraph(view,state)` for existing filters; retain
`visibleGraph(view,state)` as the final graph. Initial state adds `scope:'all'`.
`reduceState` consumes `{type:'scope',value:'all'|'connections'}`. Existing
`reduceHistory` includes scope in equality; signatures otherwise unchanged.

- [x] Obtain Astra design/plan PASS before product code.
  PASS_WITH_NOTES pins neighborhood expansion, center-clearing, no-op scope
  search-group preservation and actual renderer bounds for all retained nodes.
- [x] Update existing literal expected snapshots with default scope and add
  failing behavior tests for scoped node/edge IDs (including neighbor links),
  all filter intersections, moving center, isolated center, invalid/no-op
  actions, Show all, frozen inputs and scope-aware history/reset. Observe RED.
- [x] Implement the smallest filtered projection, neighborhood projection,
  reducer normalization and history equality extension. No renderer behavior.
- [x] Run `node --test tests/demo/test_state.cjs`; expect old and new tests PASS,
  including coalescing, branch, overflow and input immutability.

## Task 2: Controls, framing and end-to-end verification

**Files:** Modify `apps/synthetic_demo/web/{app.js,index.html,styles.css}`,
`README.md`, `docs/ROADMAP.md`; no workflow changes. Existing CI runs the Node file.

**Interfaces:** Consume Task 1 state/projections. Stable Focus connections and
Show all controls dispatch scope actions; the current graph drives renderer,
counts, list and inspector. In connections scope, fit instead of recentering.

- [x] Add a browser control/journey check and observe RED before markup.
- [x] Implement labelled controls, pressed/disabled states, mode/hint/live
  status, Show all boundary focus and whole-neighborhood fitting.
- [x] Verify actual selection/focus/neighbor/Show all/filter/history/reset
  journeys, isolated and empty views, Enter/Space and focus on 1440px desktop,
  900px tablet and 390px mobile; zero overflow/errors/external requests.
- [x] Preserve offline operation, English copy, literal hostile-label tooltip,
  source notices, previous all-scope behavior and reduced motion.
- [x] Update README/roadmap to describe demo-only scope and Show all semantics.
- [x] Run all ordinary Python regression directories (253 baseline tests),
  architecture/app validators, foundation, Node and whitespace checks.
- [x] Obtain fresh Astra Medium final source review; repair meaningful findings
  with RED/GREEN and focused re-review as required.
- [ ] Record evidence in Beads, preserve updated local demo/screenshots, verify
  live base/head and changed paths against qualifier filters; commit/push/draft
  PR and inspect ordinary CI. Stop before merge.

## Verification

```bash
rtk proxy node --test tests/demo/test_state.cjs
rtk proxy .venv/bin/python -m unittest discover -s tests/demo -v
rtk proxy .venv/bin/python scripts/validate_synthetic_demo.py
rtk proxy .venv/bin/python -m apps.synthetic_demo
rtk git diff --check
```

Use ordinary workflow test directories for regression. Never invoke a
qualification provisioner/runner; browser evidence remains local and ignored.

## Observed verification

Astra Medium approved the design before implementation. New state expectations
and eight Focus behaviors failed before the feature; all 24 Node tests passed
after implementation. The browser failed for the missing control before markup,
then passed selection, moved-center, filters, Show all, scope history, isolation,
empty results and keyboard journeys at desktop, tablet and mobile widths.
Fifteen actual renderer bounding-box checks confirmed every retained node/label
stayed within the canvas, including isolated nodes on mobile.

All 253 ordinary Python tests, both architecture validators, foundation and
whitespace checks passed. Existing English/history/offline/security browser
regressions also passed, including literal tooltip and scope-description text.
All browser receipts recorded zero page errors/external requests. Fresh Astra
Medium final review returned PASS on tree
`c03e75b239b02667697112ce028eeedd6d46444a`, with no findings. Beads records
actual source-publication status; no MA, real graph or producer was executed.
