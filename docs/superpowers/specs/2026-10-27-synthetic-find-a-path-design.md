# Find a path in the fictional diagram

Status: owner-authorized .24 scope, delegated Astra Medium design gate PASS_WITH_NOTES.
Base: `203a6f4181074f14717dca1da3f1a6e0606213b4` (PR #41 integrated).

## Intent and authority

Choose two fictional pages and see a shortest link path highlighted in the
current diagram, with readable ordered steps. The owner said Go to this
proposal after the plan/Astra requirement was stated. The delegated Astra gate
precedes code; implementation then proceeds directly, using local Beads .24.
No additional human design loop is required within this bounded feature.

All work stays in the admitted synthetic app and ordinary tests. No MA retry,
producer/comparator, real graph, payload, persistence, source/client/contract,
package/dependency or other-repository change. Preserve English/source notices,
CSP, renderer bytes/licenses, Python provider/core values and earlier archives.
Source delivery is a draft PR; merge and public hosting remain separate.

## Approach and architectural placement

Use a pure `web/path.js` helper on the temporary already-visible diagram. It
returns only presentation IDs for highlighting; no core/provider/source input
is acquired by it. Browser state owns two nullable endpoint choices, while the
UI composes state, diagram-path projection and existing renderer. This is a
fixture-only presentation navigation experiment, analogous to the admitted
one-hop view, not a reusable domain intelligence or source-profile contract.
Astra Medium confirmed this placement against the canonical Clean Architecture
standard before code. Do not silently add a core/public API or exception.

Alternatives: a separate path-only scope complicates current view/history;
automatically leaving Focus overrides a user's chosen view. The selected
approach highlights within the current visible view and leaves Focus intact.
No AI or semantic-relationship inference is performed.

## Path calculation

- Minimize the number of links. Treat authored links as undirected, matching
  existing neighbor navigation; explain that links can be followed either way.
- Break equal-length ties by ascending node ID using code-point string order,
  then ascending edge ID for parallel links. Input array order cannot affect
  the chosen path. Breadth-first traversal is sufficient; no new library.
- Missing/invalid endpoints give `incomplete` with empty ID arrays. Two valid
  disconnected endpoints give `unreachable`. Identical valid endpoints give
  `found`, one node and zero edges. Otherwise return ordered node/edge IDs.
- Never mutate the diagram; ignore any dangling edge outside its node set.
  This is defensive presentation behavior, not admission of malformed sources.

`shortestPath(view,startId,endId)` returns
`{status:'incomplete'|'found'|'unreachable',nodeIds:string[],edgeIds:string[]}`.
Keep it separate from state/history and renderer-specific objects.

## Endpoints, filters and history

Initial view adds `pathStart:null` and `pathEnd:null`. Native start/end page
selectors list only `visibleGraph(view,state)` nodes, including active Focus.
Actions `path-start`/`path-end` accept a visible ID or null; unknown/hidden
choices are ignored. `clear-path` clears both choices, without touching the
selected node, filters or scope. The result is derived, not stored.

After every changed view action, clear each endpoint that is no longer visible.
Search, category/context, Focus center and scope therefore cannot expose an
excluded endpoint or intermediate node. Show all may widen choices and reveal
a different route; recompute from its current graph. An active Focus view remains
a one-hop neighborhood and is still fitted together.

Both endpoint choices join history snapshots/equality. Back/Forward restores
them with the complete view. Changed endpoint/clear actions end a search group;
no-op/invalid actions preserve Forward and grouping. Keep the 100-entry bound,
branching and reset/reload rules. Reset clears both endpoints. Disclosure open
state is a DOM preference, not history or persistence.

## English UI and accessibility

Add a native collapsed Find a path disclosure near the scope controls. It
exposes labelled Start page and End page selectors, Clear path, a visible
current-view/direction hint and result summary. The collapsed summary also
indicates a found route or no path, so existing highlighting remains explicit
when the owner closes the controls. Native disclosure/selector keyboard
behavior suffices; no shortcut override or extra prerequisite button.

Calculate automatically after valid choices. Highlight the returned path nodes
and edges without removing other visible nodes; display ordered page labels
as an ordinary accessible list. Same-page, incomplete, empty and unreachable
messages must describe only the current view. In empty views, explain changing
or resetting filters. Clear path is disabled only when both choices are empty.
When clearing disables its focused button, return focus to Start page (or Reset
demo if the selector is disabled). Keep selector focus through rerender.

Render all labels/descriptions with textContent; no HTML interpolation. Distinct
path edge color/width and node-label styling must reset on incomplete/no path/
clear/filter changes. Retain source notices and no horizontal overflow at
1440px desktop, 900px tablet and 390px mobile. Endpoint and Clear path actions must not refit or recenter the diagram, even
when Focus is active and the user has panned/zoomed. Existing history
restoration and all-scope/focused framing otherwise remain unchanged.

## Verification and delivery

Node tests use hand-derived graphs/paths: shortest vs longer route, ties under
reordered arrays, reverse traversal, parallel-edge tie, self/no-path/invalid
endpoints, dangling edge and frozen inputs. State tests pin eligible endpoints,
filter/Focus clearing and expansion, history/reset/branch/no-op/search behavior.
The existing ordinary Node command must run both state and path test files.

Browser checks exercise native selectors/disclosure, actual highlighted
node/edge styles, ordered steps, same/unreachable/empty views, invalidation,
Focus/Show all/history, keyboard and mobile/offline use. Existing English,
literal hostile-label tooltip and scope guidance remain safe. Run ordinary
Python regression and both validators; no qualifier-triggering paths or runs.
Fresh Astra Medium final review and hosted ordinary CI are required.
