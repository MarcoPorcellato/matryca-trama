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

No user-facing application, real user graph, payload/title/text/property read,
native DB, write, general network isolation, performance, distribution, stable
support, or Trama release is established. The retained `trama.logseq.read/v1`
experiment and its `862c5c8` qualification are historical evidence. Plumber is
the sole Logseq gateway; Trama and Brain consume it without knowing Parser.
See the [delivery program](docs/specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md),
[claim ledger](docs/status/CLAIM_LEDGER.md), and [roadmap](docs/ROADMAP.md) for
exact evidence and independent remaining gates.

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
- `apps/` — future Trama applications and sidecar surfaces.

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
