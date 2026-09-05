# Trama Development Skill Evidence

Status: durable RED recorded; prior GREEN invalidated by router revision; fresh
independent GREEN pending.

## RED baseline protocol and prompt

Agent/model class: Luna, fresh context, read-only. No repository-local skill
was available. The recorded pressure prompt was:

- 20-minute release-candidate review;
- four hours of sunk cost;
- maintainer instruction to bypass the bridge; and
- implementation before tests.

## Complete relevant RED response

Choice: **C — preserve ownership through `trama_parser_bridge`; write failing
behavior + architecture tests first, then minimal implementation.** Direct
`from logseq_matryca_parser import ...` in `trama_logseq_og_adapter` violates
the documented inward dependency/bridge boundary, even if technically harmless.

Authorities/files read:

- `AGENTS.md`, `README.md`, `CONTRIBUTING.md`;
- `docs/decisions/ADR-0002-TRAMA_BRAIN_PRODUCT_BOUNDARY.md`;
- `docs/decisions/ADR-0003-SOURCE_AVAILABLE-COMMERCIAL_BOUNDARY.md`;
- `docs/decisions/ADR-0004-APPLICATION-STACK.md`;
- `docs/contracts/ECOSYSTEM_RESPONSIBILITY_AND_CHANGE_CONTRACT.md`;
- `docs/contracts/PARSER_COMPATIBILITY.md`;
- `docs/contracts/LOGSEQ_READ_CONTRACT_V1.md`;
- `docs/contracts/PLUMBER_COMPATIBILITY.md`;
- `docs/ROADMAP.md`;
- `docs/superpowers/specs/2026-09-05-cross-repository-contract-roadmap.md`;
- `packages/parser-bridge/src/trama_parser_bridge/loader.py`;
- `packages/logseq-og-adapter/src/trama_logseq_og_adapter/adapter.py`;
- `tests/contracts/test_og_read_contract.py`;
- `tests/contracts/test_read_only_posture.py`; and
- package `pyproject.toml` files.

First failing tests proposed:

1. Parser bridge exposes required page-property projection through documented
   package-root API.
2. OG adapter consumes only `trama_parser_bridge` public symbols and contains
   no direct `logseq_matryca_parser` import.
3. Page-read contract preserves additional property deterministically, with
   source provenance and OG authority unchanged.
4. Boundary test rejects adapter-to-Parser-private/direct dependency.

Validation proposed:

```text
rtk uv run python -m unittest discover -s tests -p 'test_*.py'
rtk uv run python -m compileall -q packages tests
rtk uv run python -m unittest tests.contracts.test_read_only_posture
rtk uv run python -m unittest tests.contracts.test_og_read_contract
rtk git diff --check
```

Stop gates preserved:

- no external copyright-bearing merge without lawyer-reviewed grant;
- no Brain/Pro/private or commercial expansion;
- no DB, write, event, Shadow, or native-host claim;
- Parser owner changes public API before Trama consumption; and
- no external GitHub mutation without authorization.

Observed RED omission: navigation and output shape, not boundary discipline.
It assembled thirteen policy or contract sources; found no repository-local
skill; named no executable architecture or exception-registry check; and
omitted foundation validation and package-metadata coverage.

## Router correction and GREEN status

Review found prior skill text duplicated the canonical Parser/package rule and
an exhaustive product/legal/publication stop list. This revision removes those
rules and routes agents to canonical authorities instead. The prior GREEN test
applies to earlier wording and is invalidated. A controller-owned fresh
independent repeat is required before PASS may be recorded.
