# Find a Path Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans.
> Direct-main execution: primary implements, Astra Medium reviews. Checkboxes
> project status; local Beads `matryca-trama-l5a.24` is the execution authority.
> No duplicate SDD ledger or receipt dossier is created.

**Goal:** Trace a deterministic shortest link path between two fictional pages
in the current diagram, without changing active source or view authority.

**Architecture:** A pure browser path projection consumes already-visible
diagram values. Existing state/history holds two endpoint IDs; UI composes
projection, safe labelled controls and existing renderer highlighting.

**Tech Stack:** Existing JavaScript/CSS/HTML, Python builder, Node built-in tests
and admitted renderer. No new package or dependency.

**Spec:** [Find a path design](../specs/2026-10-27-synthetic-find-a-path-design.md).

## Global Constraints

- Base `203a6f4181074f14717dca1da3f1a6e0606213b4`; reuse isolated clean worktree
  on `feat/synthetic-find-a-path`; preserve primary checkout/previous archives.
- Only existing invented data. No MA, producer/comparator, real graph, source
  client/contract, core/public API, persistence, new dependency or other repo.
- Undirected minimum-link path, deterministic node-ID then edge-ID tie order.
  Current visible graph governs endpoints and every intermediate node.
- Endpoint choices join complete history; retain 100-entry/coalescing/reset
  rules. Focus is not automatically disabled or widened.
- Preserve renderer/licenses/CSP and Python provider/core/client/lock/qualifier
  inputs/workflows. Add only a fixed local script to the existing builder.
- Astra architecture/design gate before code; fresh final Astra gate; draft
  PR/ordinary CI only. No automatic merge/hosting.

## Review Focus

- Reordered inputs/parallel edges must not change an equal-length route.
- Focus/filter changes must not retain hidden endpoints or path styling.
- Cleared/unreachable/same-page results need honest distinct output.
- Selector rerender, disabled Clear path and native disclosure must retain
  keyboard focus and make active routes discoverable while collapsed.
- Long hostile labels must remain literal and not overflow mobile controls.

## Task 1: Pure path projection and executable delivery

**Files:** Create `apps/synthetic_demo/web/path.js`, `tests/demo/test_path.cjs`.
Modify `apps/synthetic_demo/build.py`, `tests/demo/test_demo.py`,
`.github/workflows/python-contracts.yml` and owning
`tests/contracts/test_workflow_contract.py`. No qualification workflow changes.

**Interfaces:** `shortestPath(view,startId,endId)` returns the exact result from
the spec; CommonJS export and `window.TramaDemoPath` browser binding. Builder
loads vendor, state, path, app in order; JSON remains a non-executable script.

- [x] Obtain Astra design/architecture PASS before product code.
  PASS_WITH_NOTES: preserve viewport for endpoint/Clear actions, explicit
  node/edge-ID adjacency ordering and Focus-center invalidation/history tests.
- [x] Add failing path cases for shortest/ties/reverse/parallel/self/no-path/
  invalid/dangling/frozen input. Observe missing-module RED.
- [x] Implement the minimal pure breadth-first helper with ordered adjacency.
- [x] Add fixed local script loading/CSP hashing; adjust known-script-count
  escape test for four executable scripts plus JSON and verify literal data.
- [x] Extend the ordinary Node command and all canonical contract expectations
  to `node --test tests/demo/test_state.cjs tests/demo/test_path.cjs`. Preserve
  all pins, guards, step order and existing negative tests.
- [x] Run both Node files, demo and owning workflow-contract tests; expect PASS.

## Task 2: Endpoint state and full-view history

**Files:** Modify `apps/synthetic_demo/web/state.js`, `tests/demo/test_state.cjs`.

**Interfaces:** Add nullable `pathStart`/`pathEnd`; actions path-start/path-end/
clear-path. UI consumes the current choices and visibleGraph; no result stored.

- [x] Update literal complete-state expectations and add failing tests for
  valid/hidden choices, clearing on filters and Focus center/scope changes,
  expanding Show all, immutable input and full history/reset/no-op/branch.
- [x] Implement only endpoint validation/normalization and equality extension.
- [x] Run both Node suites; expect all previous and new cases PASS.

## Task 3: Native controls, highlighting and complete verification

**Files:** Modify `apps/synthetic_demo/web/{app.js,index.html,styles.css}`,
`README.md`, `docs/ROADMAP.md`. Existing admitted app composition only.

**Interfaces:** Compose Task 1 helper on Task 2 visible graph/choices. Derive
all summary/list/highlight state from its result; disclosure state stays in DOM.

- [x] Observe a browser RED for missing Find a path controls.
- [x] Add native disclosure/selectors/Clear path, current-view/direction hint,
  honest result/steps, collapsed status and focus fallback. Keep English.
- [x] Highlight only returned node/edge IDs, resetting styles in all other
  states. Do not alter graph visibility or framing for path actions.
- [ ] Verify actual selectors, renderer styles, ordered steps, same/no-path/
  empty views, filters/Focus/Show all, history/reset and keyboard at desktop
  and the actual small viewport; no overflow or console errors. Record any
  unverified requested viewport size rather than infer it from the override.
- [ ] Verify standalone output and hostile-label escaping through ordinary tests;
  check browser runtime where supported. Preserve source notices and Focus bounds.
- [x] Update demo docs; run all ordinary Python directories (253 baseline),
  both validators, foundation, Node suites and whitespace checks.
- [ ] Obtain fresh Astra Medium final source review; fix meaningful findings
  through RED/GREEN and scoped re-review as required.
- [ ] Update Beads with evidence, preserve an offline artifact/screenshots;
  verify live base/head and all PR paths avoid qualifier filters, then commit,
  push, draft PR and inspect ordinary CI. Stop before merge.

## Verification

```bash
rtk proxy node --test tests/demo/test_state.cjs tests/demo/test_path.cjs
rtk proxy .venv/bin/python -m unittest discover -s tests/demo -v
rtk proxy .venv/bin/python -m unittest discover -s tests/contracts -v
rtk proxy .venv/bin/python -m apps.synthetic_demo
rtk git diff --check
```

Use current environments only. Never invoke a qualification provisioner/runner.
Browser verification uses only the generated fictional document.

### Verification notes

Astra Medium final source review returned PASS_WITH_NOTES. The only wording
correction removes an unsupported shorter-route claim when expanding one-hop
Focus. All 253 ordinary Python tests, 40 Node tests and the three validators
passed. Browser checks cover same-page/unreachable routes, Focus endpoint
choices and center invalidation, Back restoration, expanded Show all choices,
empty views, Clear focus fallback and the collapsed active-path summary.
A separate generated diagnostic document, excluded from the product, visibly
confirms unchanged scale and center for endpoint/Clear actions after Focus
pan/zoom. Product code contains no observation hooks.

The browser's requested tablet override did not change the measured viewport;
no tablet pass is claimed. The measured small viewport was 403 CSS pixels wide
and had no horizontal overflow; the separate test tab was 1280 pixels wide.
Both override objects were reset. File-protocol navigation was denied by the
browser policy, so the generated offline/hostile-label document was not
executed in the browser and no alternate browser route was attempted. Ordinary
escaping, script-count, CSP and fixed-input tests passed; they do not establish
that unexecuted browser case.
