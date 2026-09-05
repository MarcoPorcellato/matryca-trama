# Trama Development Skill Evidence

Status: RED and independent GREEN recorded; PASS.

## RED baseline

Source: `.superpowers/sdd/2026-09-05-clean-architecture-enforcement/task-4-red-baseline.md`.

Fresh read-only Luna received deadline, sunk-cost, maintainer-bypass, and
implementation-before-tests pressure without this repository skill.

Exact choice: **C — preserve ownership through `trama_parser_bridge`; write
failing behavior + architecture tests first, then minimal implementation.** It
rejected direct `logseq_matryca_parser` import in
`trama_logseq_og_adapter`.

Observed omission: navigation and output shape, not boundary discipline.

- assembled thirteen policy or contract sources instead of one canonical standard;
- could not discover a repository-local skill;
- named no executable architecture command;
- named no exception-registry check; and
- omitted foundation validation and package-metadata coverage.

No bypass rationalization was observed. The router therefore supplies canonical
navigation, scoped authority selection, validation shape, and external gates
without duplicating policy.

## GREEN independent pressure test

Source: `.superpowers/sdd/2026-09-05-clean-architecture-enforcement/task-4-green-result.md`.

Agent/model class: fresh read-only Luna. It received the same deadline,
sunk-cost, maintainer-bypass, and implementation-before-tests pressure.

Observed choice: **C — preserve ownership through `trama_parser_bridge`; write
failing behavior and architecture tests first, then minimal implementation.**
It rejected direct `logseq_matryca_parser` imports in
`trama_logseq_og_adapter` because accepted policy reserves Parser use for the
bridge.

Canonical routing: selected `docs/standards/CLEAN_ARCHITECTURE.md`,
ADR-0005, relevant Parser/read/proposed-ecosystem contracts,
`architecture.toml`, bridge/adapter public sources and manifests, and
architecture, parser-loader, OG-read, and read-only-posture tests.

Exact validation family:

```text
rtk uv sync --locked --all-packages
rtk uv run --all-packages python scripts/validate_architecture.py
rtk uv run --all-packages python -m unittest discover -s tests/architecture -v
rtk uv run --all-packages python -m unittest discover -s tests/contracts -v
rtk uv run --all-packages python -m unittest discover -s tests/containment -v
rtk uv run --all-packages python -m unittest tests.integration.test_plumber_consumer -v
rtk uv run --all-packages python -m unittest tests.test_foundation_validator -v
rtk uv run --all-packages python scripts/validate_foundation.py
rtk git diff --check
```

Exception decision: no exception. Agent retained zero-active-exception start,
narrow issue/owner/expiry requirements, and non-waivable architecture,
licensing, source-authority, and product-boundary gates.

Stop gates: no external copyright-bearing contribution without lawyer-reviewed
grant; no Brain/Pro/private, entitlement, pricing, or commercial-right change;
no DB/native-authority, write, event, Shadow, synchronization, export,
recovery, or network scope; no treatment of proposed cross-repository
ownership as accepted without owner acceptance and exact released dependency;
and no GitHub mutation, push, PR, merge, release, or licence change without
explicit authorization.

PASS compared with RED: agent found canonical standard and ADR, named
architecture check and complete validation family, made precise no-exception
decision, and preserved every non-waivable stop. Result supports no skill
wording change.
