# Matryca Trama

Matryca Trama is a calm, local-first sidecar for understanding and safely improving Logseq graphs. It is designed for both Logseq OG and Logseq DB, with Nodi as its friendly companion layer.

This public repository contains the Community foundation, historical synthetic
read experiments, and a restricted Python client of published Plumber contracts.
Its source is available under the PolyForm Noncommercial License 1.0.0:
personal and other permitted noncommercial purposes are welcome, including the
named noncommercial organisations described by the licence. Use for commercial
purposes requires a separate commercial licence. It does not contain Pro source
code. Matryca Brain is a separate product
and repository; integrations should use documented contracts rather than private
implementation details.

## Current status

Published `main` observed on 2026-10-25 is
`d21f2adb2101ce5fae222f6235925c1d66ece126`. It includes a content-free domain
port and restricted outer Plumber client. The [owner admission](docs/contracts/PLUMBER_SOURCE_ADMISSION.md#current-owner-admission--2026-10-24)
covers only the jointly bound read/topology profiles of the original Plumber
`2.1.0a3` producer, its hash-locked closure including Parser `1.9.0`, CPython
`3.12.14`, Linux x86_64/macOS arm64, and an authenticated disposable synthetic
fixture. Packaged qualification labels remain unchanged.

Producer-M2 implemented and synthetically qualified that client in
[PR #33](https://github.com/MarcoPorcellato/matryca-trama/pull/33), with
[qualification attempt 2](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/40112844731/attempts/2)
bound to head `a4463638baaca846fe731556417f1d2d660838f1`. The later observed
main has separate passing Foundation and Python contracts checks; they do not
rebind that specialized qualification to a different head. Producer-M3 was a
bounded exploratory run, not qualification of supported OS isolation.

No supported Logseq application, real user graph, payload/title/text/property read,
native DB, write, general network isolation, performance, distribution, stable
support, or Trama release is established. The fictional navigation demo below
is a separate presentation experiment. The retained
`trama.logseq.read/v1` source is a historical experimental read profile; its
`862c5c8` qualification is historical evidence. The
[Plumber authority decision](docs/decisions/ADR-0006-PLUMBER-GATEWAY-ADOPTION.md)
keeps Plumber the sole Logseq gateway; Trama and Brain consume it without
knowing Parser.
See the [delivery program](docs/specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md),
[claim ledger](docs/status/CLAIM_LEDGER.md), and [roadmap](docs/ROADMAP.md) for
exact evidence and independent remaining gates.

## Try the fictional graph demo

The English-language local synthetic demo renders an invented graph with search, category and
personal/work filters, node details, visible-neighbor navigation and a
keyboard-accessible node list. It reuses the vis-network renderer family used
by Parser LENS, with all assets bundled locally and no Parser import.

Select a node and use Focus connections to show it with its immediate visible
neighbors, fitted together. Show all returns to nodes matching the current
search and filters; it retains the selection. Following a neighbor moves the
focus to that node. Hiding the center clears focus and selection together.

Open Find a path and choose a start and end page to highlight a shortest route
in the current view, with readable steps. Links can be followed in either
direction. Search, filters and Focus limit every page in the route; Show all
expands the view while keeping filters. Clear path removes only the endpoint
choices and highlighting. Choosing endpoints does not move or zoom the map.
Select a page on the map or in the list, then use Use selected as start/end
below either selector to set that endpoint directly. The selected-page hint
shows which page will be used. Repeating the same choice leaves history unchanged.

Back/Forward restores the selected node together with search, categories,
personal/work perspective, graph scope and path endpoints. Consecutive search typing forms one step; a new
action after going back starts a new path. The latest 100 views stay in memory
only. Back/Forward also restores map centre, zoom and page/list/detail scrolling.
Scrolling and moving the map do not add steps. Reset demo and reloading clear
history; nothing is stored between sessions. A changed layout can clamp scroll
positions to the available content. Selection centering and restoration are
immediate, with no camera animation.

From the repository root, with the existing workspace dependencies available:

```bash
uv run --all-packages python -m apps.synthetic_demo
```

Open the generated `build/synthetic-demo/index.html` directly in a browser; it
works offline. For an optional artifact-only loopback preview, use:

```bash
uv run --all-packages python -m apps.synthetic_demo --serve
```

The builder supports POSIX developer hosts and refuses linked output paths.
The HTML contains only fictional annotations, never admitted Plumber payload.
There is no graph picker, producer invocation, MA retry or user-graph route.
This is an experimental demo, not a supported Logseq app or release. See
[the scoped design](docs/superpowers/specs/2026-10-26-synthetic-graph-demo-design.md)
and [ADR-0011](docs/decisions/ADR-0011-SYNTHETIC-GRAPH-DEMO.md).

## Principles

- For Logseq OG, Markdown files remain authoritative. For Logseq DB, the
  native local database remains authoritative; derived Markdown and indexes
  must never silently replace it.
- Local-first operation is the default; data is not sent anywhere unless an explicit integration says so.
- Vault content is data, not instructions or authority.
- Writes are explicit, bounded, reviewable, and reversible where practical.
- Community components remain useful without Pro services.

## Repository map

- `docs/` — architecture, contracts, decisions, and roadmap.
- `packages/` — Community core and restricted `plumber-client` outer adapter;
  retained contracts, Parser/Plumber bridges and synthetic OG adapter are
  historical experiments, not the source-acquisition boundary.
- `apps/` — the fixture-only synthetic demo and future Trama application surfaces.

Further directories are introduced only after their contract and evidence gate.
The [delivery program](docs/specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md) is the
current source of truth for scope and status.

## Architecture and review

The accepted [Clean Architecture standard](docs/standards/CLEAN_ARCHITECTURE.md)
is canonical for package boundaries. The repository-local
[development skill](.agents/skills/trama-development/SKILL.md) routes changes
to that policy and its checks. R1 enforcement is implemented and has recorded
hosted PR/main evidence; the observed main also passes Foundation and Python
contracts. These checks do not establish runtime support or technical merge
protection. Reverify exact candidate checks and mutable settings before integration.

## Contributing and safety

Read [CONTRIBUTING.md](CONTRIBUTING.md), [CONTRIBUTOR_LICENSING.md](CONTRIBUTOR_LICENSING.md), [AGENTS.md](AGENTS.md), and [SECURITY.md](SECURITY.md) before proposing changes. For support and design discussion, see [SUPPORT.md](SUPPORT.md) and [GOVERNANCE.md](GOVERNANCE.md).

## License

Repository-owned material is source-available under the
[PolyForm Noncommercial License 1.0.0](LICENSE). Commercial use requires a
separate agreement; no public price or self-service commercial licence is
offered yet. See [the licensing model](docs/LICENSING_MODEL.md),
[commercial licensing](COMMERCIAL_LICENSE.md), [NOTICE](NOTICE), and
[trademark policy](TRADEMARKS.md). Parser, Plumber, and other dependencies keep
their own licences; see the [third-party licence inventory](THIRD_PARTY_LICENSES.md).
