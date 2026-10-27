# Focus connections for the fictional graph

Status: owner-authorized .22 scope, delegated Astra Medium design gate PASS_WITH_NOTES.
Base: `991d9b1fc9c55842b90e08dae409ee3f4238c01d` (English demo, PR #40).

## Intent and scope

Show a selected fictional page and its immediate visible connections together,
so the owner can explain relationships on video and users can explore a
manageable neighborhood on mobile. The owner requested a plan, Astra review
and autonomous implementation; Astra owns this design gate, with no additional
human confirmation loop. Local Beads .22 is the execution ledger.

This remains the existing admitted fixture-only application. No MA attempt,
producer/comparator, source client, real graph, payload, persistence, network
request, dependency or other-repository work. Keep English copy, source notices,
CSP, exact renderer/licenses, Python/provider values and all admission gates.

## Approach

Extend the pure view state with `scope: 'all' | 'connections'`, default `all`.
First derive the graph allowed by the existing search, category and context
filters. In connections scope, keep the selected center and its immediate
neighbors in that filtered graph, plus edges whose endpoints both remain.
This includes any links among the retained neighbors; it is a one-hop induced
view, not a new topology or source profile. Input values are not mutated.

Merely highlighting links leaves the mobile/video clutter in place. A separate
renderer or graph copy duplicates state. A derived presentation scope is the
builder's chosen smallest approach under the delegated gate. No new package,
public source contract or canonical architecture exception is needed.

## Exact behavior

- Focus connections is enabled only for a currently visible selected node.
  Entering the mode changes scope, not filters or selection; fit the entire
  retained neighborhood together. Keep the existing fit scale cap.
- Clicking a visible neighboring node moves the selected center and derives
  its neighborhood from the same filtered graph. Nodes outside the current
  focused view cannot be selected through an invalid action.
- Search/context/category filters always apply first. If they hide the center,
  clear selection and return to all scope, showing only the new filtered graph.
  If the center remains visible, keep connections scope and recompute neighbors.
  No hidden node or dangling edge may be introduced.
- An isolated center remains a useful one-node/zero-edge view. Show all stays
  usable; the inspector explains that no neighbors match the current filters.
- Show all exits to all nodes matching the existing filters and retains the
  selected node. It does not clear filters. Label the scope and provide a
  visible hint explaining that filters remain active.
- Focus connections is a native pressed-state button, enabled while a valid
  selected node exists. Repeated activation is a state no-op. Show all is
  enabled only in connections scope. Both controls stay in the DOM.
- Scope is part of every history snapshot and equality check. Back/Forward
  restores it together with selection and filters. Changed scope actions end a changed
  search group; invalid/repeated scope actions preserve it. Preserve the existing 100-entry bound, no-op Forward behavior,
  coalescing, branching and reset semantics. Reset/reload returns to all scope.
- Every change while focused fits the retained neighborhood, including neighbor
  navigation and history restoration. All-scope selection/reselection keeps
  existing recentering. Show all fits the current filtered graph. No viewport
  or list-scroll history is added.

## UI and accessibility

Keep the interface English. Add a labelled Graph scope group with Focus
connections and Show all, a current-scope description, and a visible filters
hint near the map. Preserve source status and Demo data at desktop 1440px,
tablet 900px and mobile 390px. The graph/list/inspector use the same visible
graph; counts and actionable neighbors agree. Node sizing still represents
all authored connections, as in the filtered baseline.

Preserve focus on usable stable controls. When activating Show all disables
it, move keyboard focus to the enabled Focus connections button (otherwise
Reset demo). Keep existing node-list and history-boundary focus rules. Scope
changes announce mode, visible counts and selection through the existing live
status. Native Enter/Space work; no browser shortcuts or history are intercepted.

## Evidence and delivery

Meaningful pure-state tests pin literal expected node/edge IDs, filter
intersection, moved center, isolation, invalid entry/selection, Show all,
immutable input, scope-aware history/coalescing/branching/reset. Browser tests
prove actual scoped counts/controls, neighbor travel, restoration, native focus,
full-neighborhood framing, desktop/tablet/mobile, English/offline use and
existing literal-text protections. Run ordinary regression and final fresh
Astra Medium review. All changed PR paths must avoid qualification filters.
Preserve earlier presentation packs; save an updated local artifact/screenshots.
Source delivery is a draft PR; merge and public hosting remain separate.
