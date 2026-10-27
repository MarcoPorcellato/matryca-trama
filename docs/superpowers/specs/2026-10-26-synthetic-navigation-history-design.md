# Synthetic navigation history

Status: owner-authorized .20 scope, delegated Astra Medium design review PASS_WITH_NOTES.

## Intent and authority

Users can follow fictional page neighbors and then retrace their exploration
without reconstructing filters or selections. The owner requested this plan,
Astra review and autonomous implementation. Astra is the delegated design gate;
no additional human design-confirmation loop is required. Base main is
`ec8c81aa5acc379d6fc1fed35ca413e2d44f1f9d`, containing PR #38.

Only the existing admitted synthetic demo changes. No MA retry, producer,
comparator, real graph, source client, persistence, network request or other
repository work. Existing provenance, CSP, bundled renderer and source/admission
gates remain unchanged. The preserved PR #38 UI archive is not overwritten.

## Approach

Keep the existing pure view reducer and add a pure, bounded history wrapper
in `web/state.js`. Each entry contains query, context, categories and selected
node. The UI renders the current entry through the same existing render path.
This is the builder's choice under the owner-delegated gate.

Selection-only history would lose the context needed to restore a hidden node.
Browser-global history would add URL/session semantics and interfere with the
standalone file. Full presentation snapshots preserve the user's intended
exploration with neither new dependencies nor data/source authority.

## Exact behavior

- Start with one entry, no selection and all filters enabled. Retain at most
  100 entries including the current one; drop the oldest on overflow.
- A changed node selection, context or category records the complete view.
  Hiding the selected node clears it in that new entry; Back restores both
  the previous filters and previous valid selection. Only visible neighbors
  remain actionable. Unknown/hidden selections are ignored.
- Search still filters on every input. Consecutive state-changing search
  actions coalesce into one entry, preserving the view before typing. Any
  other changed action or successful Back/Forward ends that search group.
  Returning to the preceding entry's exact view (categories compared as a set) collapses the redundant
  coalesced entry and ends that search group. No timers or focus-dependent query rules are introduced.
- Back/Forward change only the cursor. They restore the exact query, context,
  category set and selected node, including an empty result with no selection.
  Boundary navigation, duplicate selection, invalid action and unchanged
  filters add no entry and preserve an existing forward path.
- A changed action after Back truncates the forward path and begins a new
  branch; a new search after Back never overwrites the historical current view.
- Reset demo clears history and returns to the original full view.
  Reloading starts fresh. Nothing is stored beyond the in-memory session.
- Zoom/pan, DOM focus, list scroll and dialogs are not history entries. On
  restoration, focus the selected canvas node or fit the visible graph when
  there is no selection. No promise of viewport/scroll restoration is made.

## Controls and accessibility

Add native Back/Forward buttons in a labelled history group beside the
existing toolbar and show the current position (for example 2 / 4). Disabled
states reflect boundaries. Preserve focus on an activated history button
while usable; when it becomes disabled, move focus to the enabled opposite
button, or Reset demo if neither is available. The existing live status
announces position, visible counts and selection. No browser Back interception
or keyboard shortcut overrides. Tab, Enter and Space use native controls.

Allow toolbar wrapping at intermediate widths; keep both synthetic/source
labels visible at desktop, 900px tablet and 390px mobile. Preserve node-list
focus, literal labels/tooltips and reduced-motion behavior.

## Interfaces and evidence

`initialHistory()` returns `{entries: [initialState()], index: 0, lastAction: null}`.
`historyState(history)` reads its current view.
`reduceHistory(view, history, action)` returns a new history for changed state
or movement and leaves inputs untouched. It consumes existing view actions
plus `back`/`forward`; reset returns a new initial history.

Keep existing reducer exports and tests. Node tests exercise independent
expected snapshots, coalescing, branching, no-op preservation, reset, limits
and input immutability. Browser checks exercise an actual selection/filter/
search journey, Back/Forward restoration, boundary focus, keyboard, empty
results, reset, desktop/tablet/mobile and offline operation. Ordinary Python
regression and hosted CI remain separate from qualification. Final independent
Astra Medium source review is required. Source may be delivered in a draft PR;
merge/public hosting remains separate. Beads .20 is the execution ledger.
