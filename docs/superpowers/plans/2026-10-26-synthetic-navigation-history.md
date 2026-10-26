# Synthetic Navigation History Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.
> Direct-main execution is selected; primary implements, Astra Medium reviews.
> Steps use checkbox syntax. Local Beads `matryca-trama-l5a.20` is the execution
> authority; no competing SDD ledger or receipt dossier is created.

**Goal:** Add application-level Back/Forward that restores fictional graph
filters and selection without a source connection.

**Architecture:** Wrap the existing pure view reducer in bounded in-memory
history. The existing UI renders the current snapshot; native controls drive
movement. Domain values, providers, builders and source admission are unchanged.

**Tech Stack:** Existing plain JavaScript/CSS/HTML, Node built-in tests, current
Python workspace and the already admitted vis-network bundle. No new dependency.

**Spec:** [Synthetic navigation history](../specs/2026-10-26-synthetic-navigation-history-design.md).

## Global Constraints

- Exact base `ec8c81aa5acc379d6fc1fed35ca413e2d44f1f9d`; reuse the clean linked
  worktree on `feat/synthetic-navigation-history`, preserve primary checkout.
- Built-in fictional data only. No MA, producer, comparator, real graph, source
  client, persistence, browser-global history or other-repository mutation.
- Maximum 100 complete view entries; coalesce consecutive changed search input.
  Reset clears all history. No viewport or scroll restoration.
- Preserve app admission, licenses, CSP, literal text, renderer bytes and
  Python/core/client/lock/qualification inputs/workflows.
- Plan gate and final gate: general-purpose Astra Medium. Source draft PR only;
  no automatic merge/public hosting. Reverify qualification path exclusion.

## Review Focus

- Search after Back must append a new branch, never rewrite the restored entry.
- Hidden selection/empty results must restore together with the right filters.
- Duplicate/invalid actions must preserve the forward path and input objects.
- Native boundary disabling must retain meaningful keyboard focus.
- Added controls must wrap without hiding source status on narrow screens.

## Task 1: Pure navigation history

**Files:** Modify `apps/synthetic_demo/web/state.js` and `tests/demo/test_state.cjs`.

**Interfaces:** Keep existing reducer exports. Add `initialHistory()`,
`historyState(history)` and `reduceHistory(view, history, action)` exactly as
in the spec; the UI consumes the current view and cursor/entry count.

- [x] Obtain Astra design/plan PASS before product code.
  PASS_WITH_NOTES: category-set equality, fresh search after collapse, overflow
  with coalescing/branching, invalid selection no-op and boundary keyboard focus.
- [x] Add failing tests: initial boundaries; full selection/filter restoration;
  empty state; coalesced search/return-to-start; changed branch after Back;
  unchanged/invalid actions preserving Forward; reset; 100-entry eviction;
  frozen input immutability. Run Node suite and observe missing-export RED.
- [x] Implement the minimal pure wrapper and visible-selection guard.
- [x] Run `node --test tests/demo/test_state.cjs`; expect all tests PASS,
  including the five existing cases. Inspect honest expected view snapshots.

## Task 2: Native history controls and complete verification

**Files:** Modify `apps/synthetic_demo/web/{app.js,index.html,styles.css}`,
`README.md`, and `docs/ROADMAP.md`. Keep ordinary workflow commands unchanged;
existing Node command already executes all added history cases.

**Interfaces:** UI owns one history object and derives the current view using
Task 1 exports. Route view actions and Back/Forward through that wrapper.

- [x] Add a browser check for labelled history controls on the current demo;
  observe RED before adding markup/handlers.
- [x] Add controls, position/status, boundary focus and responsive wrapping.
  Restore renderer selection or fit the visible view after history movement.
- [x] Build offline HTML and verify desktop 1440px, tablet 900px and mobile
  390px: multi-neighbor journey, filter hiding/restoring selection, search
  coalescing, empty result, branch, reset and native Enter/Space focus.
- [x] Check zero browser errors/external requests and preserved literal tooltip
  protection, reduced motion and both visible synthetic/source labels.
- [x] Update README/roadmap with demo-only history behavior, not compatibility.
- [x] Run ordinary Python regression family (253 baseline tests), both boundary
  validators, foundation, Node suite and whitespace checks. No qualification.
- [x] Obtain fresh independent Astra Medium final source review; fix meaningful
  findings with focused RED/GREEN and scoped re-review where required.
- [ ] Update Beads with evidence. Reverify live base/head, exact changed paths
  and qualification exclusion; commit/push/draft PR, inspect ordinary CI, stop
  before merge. Preserve the existing PR #38 screenshot archive unchanged.

## Verification commands

Use the existing local workspace/runtime; no installation is needed:

```bash
rtk proxy node --test tests/demo/test_state.cjs
rtk proxy .venv/bin/python -m unittest discover -s tests/demo -v
rtk proxy .venv/bin/python scripts/validate_synthetic_demo.py
rtk proxy .venv/bin/python -m apps.synthetic_demo
rtk git diff --check
```

Use the ordinary workflow test directories for regression, never invoke a
qualification runner or provisioner. Browser evidence remains local/ignored.

## Observed verification

Astra Medium approved the plan before product code. Eleven new history tests
first failed for missing exports, then all 16 Node tests passed. The browser
first failed for absent controls, then passed full history journeys on desktop,
900px tablet and 390px mobile, including keyboard boundary focus and offline
operation. All 253 ordinary Python tests and both boundary validators passed.

Final review identified a reselection regression: clicking the current node
after panning no longer recentered the map. A real browser check reproduced
it; the scoped fix restored the exact centered canvas without changing the
history position or Forward path. Focused tests and the complete history
browser journey passed again. Astra re-review returned PASS on tree
`f697946d42341b227d747f1e5ecadb9aa62e4ec1`, with no remaining findings.
Browser receipts report zero page errors/external requests. Beads records
source publication status; no merge, MA or real graph operation is included.
