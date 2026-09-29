# Phase 0 foundation evidence register

- Evidence snapshot: 2026-09-29
- PR #27 base reviewed: `d9ed04ce6e6333fc25f671fe21dbe3817b01d5cd`
- Post-merge main reviewed: `ce3dbd2e5ad4b39cfb84ec38d0d5f93557a8c4b2`
- Purpose: reconcile the public foundation evidence without claiming runtime, host, or consumer compatibility.

## Original foundation pull request

PR [#1](https://github.com/MarcoPorcellato/matryca-trama/pull/1) introduced the document-first public foundation. Its exact PR head was `5555a128b833bf1fa45777db6bb7859198e3b9e3`; it merged as `cd9ec408ed9d4ece39d3eeaef506f4b172ab77d5`.

| Evidence | Exact PR-head result |
|---|---|
| [Foundation CI run 33344974666](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/33344974666) | Success |
| [Dependency Review run 33344974627](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/33344974627) | Success |

The PR description also records local validator, unit-test, syntax, YAML,
whitespace, licence-text, and sensitive-artifact checks. Those are PR-submitted
claims, not independently replayed by this register.

## Foundation surfaces present on the reviewed main

- `LICENSE` and `NOTICE` carry the repository's PolyForm Noncommercial
  boundary; commercial use requires separate written permission.
- `CONTRIBUTING.md`, `CONTRIBUTOR_LICENSING.md`, and `GOVERNANCE.md` preserve
  the hold on external copyright-bearing contributions until a lawyer-reviewed
  contributor agreement or equivalent grant exists.
- `.github/CODEOWNERS` defines ownership review routing.
- `.github/workflows/foundation.yml`,
  `.github/workflows/dependency-review.yml`, and
  `.github/workflows/python-contracts.yml` are the repository's policy and
  contract checks. Their fork-safe permissions and exact-head results must be
  assessed from the workflow source and each pull request's own runs; a check
  on one PR head is not evidence for another head or its merge commit.
- `docs/standards/CLEAN_ARCHITECTURE.md` and ADR-0005 document the
  repository-owned architecture policy. `scripts/validate_architecture.py`
  and `tests/architecture/` enforce its dependency boundaries;
  `scripts/validate_foundation.py` validates the public foundation separately.
- `README.md`, the foundation specification, ADR-0003, and ADR-0007 distinguish
  source authority and commercial boundaries. Logseq OG Markdown and the
  Logseq DB native store remain authoritative for their respective graphs;
  Trama access remains through Plumber.

The source-authority sentence in `SECURITY.md` was found overbroad during the
2026-09-28 review and was corrected by [PR #27](https://github.com/MarcoPorcellato/matryca-trama/pull/27),
which introduced this register. Naming the DB's authoritative store grants no
direct DB access and admits no adapter or runtime compatibility.

## Later exact-head evidence; not a substitute for original runs

PR [#26](https://github.com/MarcoPorcellato/matryca-trama/pull/26) had exact
head `58eb5830a5be51069b893f1952e4e05e9978f877`. Its Foundation CI run
[36284110036](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/36284110036),
Dependency Review run
[36284110037](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/36284110037),
and Python contracts run
[36284110045](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/36284110045)
all succeeded on that PR head. They are not runs on merge commit
`d9ed04ce6e6333fc25f671fe21dbe3817b01d5cd`; the workflow-run query for that
merge commit returned no PR-triggered runs.

## PR #27 merge and main-push evidence

PR [#27](https://github.com/MarcoPorcellato/matryca-trama/pull/27) had exact
head `030d1d7fe7720c14c6f88534a1bc4fc48de5582e`. Its Foundation CI,
Dependency Review, and Python contracts checks all succeeded on that PR head.
It merged as `ce3dbd2e5ad4b39cfb84ec38d0d5f93557a8c4b2`.

The push-triggered checks on that exact merge commit also succeeded:

| Evidence | Exact merge-commit result |
|---|---|
| [Foundation CI run 36433008503](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/36433008503) | Success |
| [Python contracts run 36433008516](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/36433008516) | Success |

Dependency Review passed on the exact PR head; no Dependency Review run is
claimed for the merge commit. Issue [#8](https://github.com/MarcoPorcellato/matryca-trama/issues/8)
was closed on 2026-09-29 for its foundation planning-and-evidence criteria
after these exact-head and post-merge results were verified.

This reconciliation does not claim any supported Logseq runtime, host,
consumer profile, platform, write path, commercial offering, Pro, or Brain
implementation. It does not close the broader, ongoing Phase 0 governance and
coordination work.

## Review and mutable-state limits

On 2026-09-28, GitHub's pull-request review and conversation-comment APIs
returned no review submissions or comments for PR #1. This establishes only
that those APIs exposed no such record at query time; it does not prove that no
review occurred elsewhere. The PR description's repository-settings checks are
dated 2026-08-31. Mutable GitHub settings have not been reverified by this
register and must not be presented as current settings evidence.
