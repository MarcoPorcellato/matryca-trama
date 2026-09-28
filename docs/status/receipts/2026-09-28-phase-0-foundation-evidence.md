# Phase 0 foundation evidence register

- Evidence snapshot: 2026-09-28
- Live base reviewed: `d9ed04ce6e6333fc25f671fe21dbe3817b01d5cd`
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

## Foundation surfaces present on the reviewed live base

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
2026-09-28 review and is corrected in the pull request carrying this register.
Naming the DB's authoritative store grants no direct DB access and admits no
adapter or runtime compatibility.

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

## Review and mutable-state limits

On 2026-09-28, GitHub's pull-request review and conversation-comment APIs
returned no review submissions or comments for PR #1. This establishes only
that those APIs exposed no such record at query time; it does not prove that no
review occurred elsewhere. The PR description's repository-settings checks are
dated 2026-08-31. Mutable GitHub settings have not been reverified by this
register and must not be presented as current settings evidence.

The acceptance decision for the corrective pull request must use its own exact
head, required hosted checks, and current review. Historical evidence above
must not be relabelled as evidence for that head. This register does not by
itself close Phase 0 or claim any supported Logseq runtime, platform, write
path, commercial offering, Pro, or Brain implementation.
