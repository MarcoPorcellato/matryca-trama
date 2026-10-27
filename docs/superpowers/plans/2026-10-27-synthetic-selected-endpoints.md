# Use Selected Page as Path Endpoint Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans. Direct-main:
> the primary implements; general-purpose Astra Medium reviews. Local Beads
> `matryca-trama-l5a.25` is the execution ledger, without a duplicate SDD ledger.

**Goal:** Use the currently selected fictional page as either path endpoint
without finding it again in a selector.

**Architecture:** Native buttons forward to existing `path-start`/`path-end`
actions. Existing endpoint validation, history and path-only camera behavior
remain authoritative. No reducer, algorithm or source-interface changes.

**Tech Stack:** Existing HTML/CSS/JavaScript, Python builder and renderer.

**Spec:** The short design below; the owner authorized the Astra design gate
followed by autonomous implementation on 2026-10-27.

## Short design

Place Use selected as start and Use selected as end below their respective
selectors inside Find a path. Keep selectors and Clear path. A shared literal
text hint names the currently selected page; with no selection, explain that
a page must first be selected on the map or in the list. An empty view instead
explains changing/resetting filters. Associate both native buttons with this
hint. Disable them only when there is no currently visible selected page.

A click uses the existing endpoint action with `state.selected`, changing
only its target endpoint. Repeated identical choices stay enabled and are
no-ops, preserving focus, Forward and search grouping. Changes create one
history step. Selection, filters, Focus, map center and zoom do not change.
Back/Forward restores endpoints with the full view. Labels stay English;
selected labels remain literal text. At narrow widths, endpoint groups stack.

Alternatives considered: continuing with selectors alone keeps lookup friction;
clickable route steps introduce Focus-center invalidation questions. The owner
selected the two convenience buttons. Swap and route-step navigation stay out.

## Global constraints

- Base: current live `main` at `51ddc684249d6e8c02ba991e23a972f8a0a58ba1`.
  Reuse the clean isolated worktree on `feat/synthetic-selected-endpoints`.
- Only existing invented fixtures. No MA attempt, producer/comparator, real
  graph, core/package/source/dependency/qualification-input or other repo work.
- Keep renderer, licenses, CSP, fixed inputs and existing source notices.
- Design review before product edits, fresh final Astra Medium review, ordinary
  tests/CI and draft PR only. No automatic merge, release or public hosting.

## Review focus

- A stale/hidden selection must never become an endpoint.
- A duplicate click must retain Forward, history length and keyboard focus.
- Both target bindings must be correct and leave the other endpoint unchanged.
- Focused/panned/zoomed maps must not be refitted by these convenience actions.
- Long selected labels and both buttons must fit the actual measured small
  viewport. Do not claim requested sizes or offline browser cases not exercised.

## Task 1: Native endpoint shortcuts and complete verification

**Files:** Modify `apps/synthetic_demo/web/{index.html,app.js,styles.css}`,
`README.md`, `docs/ROADMAP.md`. Existing tests remain the regression oracle;
no duplicate reducer tests, source-text assertions or DOM-mock library.

**Interfaces:** Buttons `use-selected-start`/`use-selected-end`, explanatory
`path-selected-hint`. `renderPath(current,path)` derives availability from a
selected node in `current.nodes`; handlers call `dispatch` with existing endpoint
actions and `focus=false`. Keep real controls mounted during rerender.

- [x] Obtain Astra Medium design/plan PASS before product changes.
  PASS_WITH_NOTES: neutral endpoint groups, buttons outside labels, literal
  hint text and explicit target/no-op/Focus browser coverage.
- [x] Observe browser RED: the current generated UI lacks both shortcuts.
- [x] Add the two buttons, literal selected-page hint and stacked endpoint
  groups; wire existing actions without changing state, history or camera code.
- [x] Observe browser GREEN: selection enables both, clicking start/end changes
  only that endpoint, duplicate leaves history/Forward/focus unchanged, and
  selectors/Clear still work. Exercise Back/Forward, Focus, hidden/empty views,
  keyboard and actual small-screen layout; check console errors.
- [x] Verify camera coordinates in a separate generated diagnostic copy if
  necessary; keep all observation hooks out of product code. Preserve earlier
  browser limitations rather than infer an unexecuted pass.
- [x] Update user docs. Run both existing Node suites (40 baseline), all eight
  ordinary Python groups (253 baseline), architecture/demo/foundation validators
  and whitespace checks. Expected: all pass; never run a qualification runner.
- [ ] Fresh Astra Medium final review of the complete candidate; fix blockers
  with focused RED/GREEN. Record evidence in local Beads.
- [ ] Preserve updated preview/screenshots, verify all changed paths avoid live
  qualifier filters, then commit, push, draft PR and inspect ordinary CI. Stop
  before merge. Source publication follows the existing authorized .25 delivery
  pattern; this plan grants no additional external action.

## Verification notes

The implementation reuses the endpoint actions without changing the reducer,
path algorithm, builder, renderer or dependencies. Browser RED observed both
shortcuts missing before edits. Real UI GREEN covers both target bindings,
keyboard activation/focus, exactly one changed history step, a duplicate after
Back retaining Forward, Focus/filter preservation, hidden/empty selection,
Clear and native-selector composition. Product and long-label diagnostic views
fit the measured 403-pixel viewport; desktop verification uses a separate
1280-pixel tab. A separate generated diagnostic copy visibly confirms identical
camera scale/center for both shortcuts after native Focus pan/zoom. Its only
label variation is an invented long page name; no observation hook or test
label enters product code. The earlier unexecuted tablet-size and offline
hostile-label browser cases remain unqualified.

All 253 ordinary Python tests, 40 Node tests and architecture/demo/foundation
validators passed. The final independent source gate and draft-PR CI remain
separate delivery gates. Local Beads holds execution receipts and completion.
