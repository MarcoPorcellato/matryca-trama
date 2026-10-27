# Navigable synthetic graph demo

Status: owner-authorized scope; Astra Medium design gate PASS_WITH_NOTES.

## Intent and authority

Deliver the first visible Trama experience: open an offline graph, find a node,
inspect its neighbors and explore personal/work perspectives of one graph.
The owner requested the plan, Astra review and autonomous implementation. That
instruction delegates this design gate to Astra; no extra human design loop is
required. It authorizes neither a real graph nor another MA attempt. The wider
programme goal and source-admission gates remain blocked.

## Existing work and reuse decision

Trama base: `17d458dff090845466333700c9724663edb1030d`. Reuse its immutable
`GraphSnapshot` values and `KnowledgeGraphGateway` port. A built-in fictional
provider implements that port; it never launches a producer.

Parser reference: `edd4f5fb8675d8717093c0263a8dd9344e4d52a3`,
`src/logseq_matryca_parser/lens.py`. LENS already uses PyVis/vis-network, node
groups, degree-based sizing, filters, statistics and reset. Reuse the renderer
family and those interaction ideas. The file history includes external PR #86
in reference extraction; do not copy its Python module or GraphVisualizer.
No Parser import, NetworkX/PyVis installation or source extraction belongs here.

Use the official standalone UMD **vis-network 9.1.2** browser bundle, matching
the engine/version used by LENS, with local delivery and retained licenses.
Its SHA-256 is
`3729be2f3994c83229106c3d34fb8de807572cf6f282c23e2b34ecf4e84ce863`
(682,273 bytes). The installed PyVis copy has different bytes, so it is not the
admitted asset. Official npm archive SHA-1 is
`ddaca300a9764bbf1646a0aa03eb28fe55823ca8`; its SHA-512 integrity was verified
during research. Keep upstream MIT/Apache notices and all bundle headers;
record source/version/hash and the MIT license selection in the inventory.
New Trama code remains PolyForm Noncommercial. This is an asset-dependency
decision, not acceptance or relicensing of external Parser contributions.

Alternatives considered: copying LENS wholesale couples source extraction to
presentation; writing another renderer duplicates existing work; a desktop
shell adds packaging before the interaction is useful. The selected approach
is a Python composition plus a small browser presentation using the existing
renderer family. These are implementation choices, not prior owner approvals.

## Bounded composition

Admit only `apps/synthetic_demo` as a synthetic application composition, not a
new workspace distribution. Python may import standard-library modules, its
own modules and `trama_core.graph_values` / `graph_gateway`; no other provider.
Keep all existing package rules and dependencies unchanged. Add this admission
to the canonical architecture standard and ADR-0011 before implementation.

The provider creates 24 fictional root-page nodes with invented references.
Presentation-only annotations supply labels, descriptions, category and
personal/work membership. Categories are notes, projects, journals and tags;
they do not extend core NodeKind or adopt a Plumber page projection. Synthetic
provenance explicitly says it is not a released producer. No payload capability
or R1–R5 producer decision is implied.

Separate provider, presentation projection, builder and browser state. Labels
stay outside the content-free core. The browser renderer consumes only the
demo view, never owner wire DTOs. Python checks topology through existing core.

## Visible behavior

- English interface (owner update, 2026-10-27), always marked **Demo data** and
  **No graph connected**. One graph offers All, Work and Personal views.
  Fictional annotations, placeholders, credits and accessibility text are English.
- Search labels, toggle the four categories, show visible node/link counts,
  select nodes, inspect a description and navigate neighbor buttons.
- Zoom, fit and reset; deterministic initial layout and degree-based sizes.
- Keyboard-accessible node list supplies the same selection/neighbor actions
  as the canvas. Announce counts and empty results; preserve visible focus.
- Only visible neighbors are actionable; hiding a selected node clears it.
- Responsive desktop and 390-pixel mobile layout; reduced motion respected.

No graph picker, drag/drop, filesystem API, upload, external URL opening,
Logseq deep link, persistence, analytics, AI call or source connection.

## Delivery and safety

Build one self-contained HTML file under ignored `build/synthetic-demo/`.
Reject symlinked output ancestors/files using descriptor-based no-follow writes
on POSIX build hosts. The generated HTML itself is portable.
Bundle scripts/styles/data/licenses; no CDN, font or other outbound requests.
Use safe JSON embedding and textContent for labels/descriptions, including
tooltip DOM nodes. Hash-allow inline scripts with CSP; prohibit connections,
frames, forms and objects. Renderer styling may use inline styles.

`python -m apps.synthetic_demo` builds; `--serve` additionally previews the
generated bytes on `127.0.0.1` with an automatically chosen port. Serve only
GET/HEAD `/`; no arbitrary directory/root selector or write endpoint. This
loopback preview is ordinary demo tooling, not an isolation qualification.
An explicit demo-boundary validator covers every app Python file, prohibited
imports, dynamic-import/path escapes and controlled negative examples. It
supplements the existing package-only validator rather than claiming it scans apps.

Do not alter `architecture.toml`, core/client packages, qualification workflows
or qualification inputs. Neither demo source nor its tests match qualification
PR path filters. Ordinary CI adds only offline demo tests and Node state tests;
preserve canonical workflow equality and negative guards. No dispatch occurs.

## Success

The owner can open the artifact and search/filter/select/navigate/reset without
network access. Python and JavaScript behavior tests, ordinary regression CI,
desktop/mobile browser checks and final Astra review pass. No real content is
read. Screenshot/artifact results remain local; source can be reviewed in a
draft PR without automatic merge or public hosting.
