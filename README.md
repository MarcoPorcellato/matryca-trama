# Matryca Trama

Matryca Trama is a calm, local-first sidecar for understanding and safely improving Logseq graphs. It is designed for both Logseq OG and Logseq DB, with Nodi as its friendly companion layer.

This public repository contains the Community foundation and shared contracts.
Its source is available under the PolyForm Noncommercial License 1.0.0:
personal and other permitted noncommercial purposes are welcome, including the
named noncommercial organisations described by the licence. Use for commercial
purposes requires a separate commercial licence. It does not contain Pro source
code. Matryca Brain is a separate product
and repository; integrations should use documented contracts rather than private
implementation details.

## Current status

This repository remains contract-first. It now contains a bounded Python
implementation of `trama.logseq.read/v1`, qualified only for owned synthetic OG
fixtures and three read operations. No user graph, Logseq DB host, application,
Nodi UI, distribution artifact, or command-line interface is qualified by this
README. See the [roadmap](docs/ROADMAP.md) for the exact supported and deferred
scope.

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
- `packages/` — shared contracts, core behavior, bridges, and bounded adapters.
- `apps/` — future Trama applications and sidecar composition roots.

These directories may be introduced incrementally. The documentation is the current source of truth for scope and status.

## Architecture and review

The accepted [Clean Architecture standard](docs/standards/CLEAN_ARCHITECTURE.md)
is canonical for package boundaries. The repository-local
[development skill](.agents/skills/trama-development/SKILL.md) routes changes
to that policy and its checks. R1 enforcement is implemented on this local
branch; it is not hosted or main-branch qualification until the exact published
head has fork-safe CI evidence.

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
