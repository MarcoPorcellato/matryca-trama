# Matryca Trama

Matryca Trama is a calm, local-first sidecar for understanding and safely improving Logseq graphs. It is designed for both Logseq OG and Logseq DB, with Nodi as its friendly companion layer.

This public repository contains the Community foundation, shared contracts, and
a bounded Python reference implementation of the initial synthetic OG read
profile.
Its source is available under the PolyForm Noncommercial License 1.0.0:
personal and other permitted noncommercial purposes are welcome, including the
named noncommercial organisations described by the licence. Use for commercial
purposes requires a separate commercial licence. It does not contain Pro source
code. Matryca Brain is a separate product
and repository; integrations should use documented contracts rather than private
implementation details.

## Current status

The resolved `origin/main` merge parent is
`70fc14c27b11e31e8f557fd70684b6a83933e7d6`. It contains
bounded Python source for synthetic OG fixtures and `graph.identify`,
`page.read`, and complete ordered `block.subtree.read.complete`. The historical
qualification record remains `862c5c8`; it does not qualify this head. This
experimental `trama.logseq.read/v1` source is neither a published runtime nor
the authority for future integration. The proposed Plumber-gateway decision is
not accepted until Plumber publishes its ADR and canonical contract. No
user-graph, Logseq-host, DB, write, network, UI, performance, distribution, or
release claim follows. See the [roadmap](docs/ROADMAP.md).

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
- `packages/` — bounded Python contracts, core, Parser and Plumber bridges, and
  synthetic OG adapter; direct Parser use is historical experimental work, not a
  future integration boundary.
- `apps/` — future Trama applications and sidecar surfaces.

Further directories are introduced only after their contract and evidence gate.
The delivery program is the current source of truth for scope and status.

## Architecture and review

The accepted [Clean Architecture standard](docs/standards/CLEAN_ARCHITECTURE.md)
is canonical for package boundaries. The repository-local
[development skill](.agents/skills/trama-development/SKILL.md) routes changes
to that policy and its checks. R1 enforcement is implemented; it is not hosted
or main-branch qualification until fork-safe CI records evidence for the exact
published head.

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
