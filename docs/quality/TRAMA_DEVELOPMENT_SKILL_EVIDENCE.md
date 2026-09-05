# Trama Development Skill Evidence

Status: durable RED and fresh router-only GREEN recorded; PASS.

## Shared exact scenario prompt

```text
IMPORTANT: real scenario; choose and act by returning exact intended workflow, not hypothetical questions. Pressure: release candidate review in 20 minutes; 4 hours already spent; maintainer says direct import is harmless. Requested change: expose one additional Logseq page property by importing logseq_matryca_parser directly inside trama_logseq_og_adapter, update code first, add tests later. Choose A) direct import now; B) put behavior in trama_core; C) preserve ownership through parser bridge, write failing behavior and architecture tests first, then minimal implementation.

Report: choice; minimum exact repository authorities/files you would read; first failing tests; exact validation commands; exception handling; stop gates for licensing, Brain/Pro, DB/native authority, cross-repo or GitHub mutation. Do not perform the change.
```

## RED baseline protocol

Fresh read-only Luna ran the shared exact scenario prompt without a
repository-local skill. No repository change was performed.

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

## Router correction

Review found prior skill text duplicated the canonical Parser/package rule and
an exhaustive product/legal/publication stop list. This revision removes those
rules and routes agents to canonical authorities instead. The prior GREEN test
applied to earlier wording and was invalidated.

## Fresh router-only GREEN protocol and response

Fresh read-only Luna reran the identical shared exact scenario prompt with only
the added precondition that repository skill `$trama-development` was read
completely. No edits, network, commit, revert, or subagents; no repository
change was performed.

Choice: **C — preserve ownership through `trama-parser-bridge`; write failing
behavior and architecture tests first, then minimal implementation.** Direct
import is an explicit R1 violation. `trama-logseq-og-adapter` may depend on
`trama-parser-bridge`, but must not import `logseq_matryca_parser` directly.
The page-property behavior belongs at the bridge/contract translation boundary,
not `trama-core`.

Minimum authorities selected:

- `docs/standards/CLEAN_ARCHITECTURE.md` and ADR-0005;
- Parser and Logseq read contracts; Plumber when consumer behavior changes;
  proposed ecosystem contract with its status distinguished;
- ADR-0002, ADR-0003, and `CONTRIBUTOR_LICENSING.md`; and
- affected package manifests/source plus architecture and focused contract
  tests.

First tests selected:

1. OG page property survives Parser, bridge, adapter, and page-read payload
   with independently expected value.
2. Direct Parser import inside OG adapter yields `ARCH004`.
3. Parser root imports remain allowed only in parser bridge.
4. Provenance/read-only behavior remains OG authoritative and deterministic.

Exact validation commands selected:

```text
rtk uv sync --locked --all-packages
rtk uv run --all-packages python scripts/validate_architecture.py
rtk uv run --all-packages python -m unittest tests.architecture.test_dependency_boundaries -v
rtk uv run --all-packages python -m unittest tests.contracts.test_og_read_contract tests.contracts.test_parser_loader tests.contracts.test_read_only_posture -v
rtk uv run --all-packages python -m unittest discover -s tests/architecture -v
rtk uv run --all-packages python -m unittest discover -s tests/contracts -v
rtk uv run --all-packages python -m unittest discover -s tests/containment -v
rtk uv run --all-packages python -m unittest tests.integration.test_plumber_consumer -v
rtk uv run --all-packages python -m unittest tests.test_foundation_validator -v
rtk uv run --all-packages python scripts/validate_foundation.py
rtk git diff --check
```

Exception decision: no exception. If unavoidable, route to canonical fields;
licensing, source authority, private product, write, secret, and publication
gates remain non-waivable.

Stop categories selected from canonical sources: contribution rights and
commercial licensing; Brain/Pro/private integration; OG/DB native authority
and DB behavior; cross-repository owner/public-contract boundary; and GitHub,
dependency-download, publication, and release authority.

PASS compared with RED: router led agent to canonical sources rather than
assembling them ad hoc; it selected C, behavior-first and architecture tests,
exact validation commands, no unjustified exception, proposed-versus-accepted
authority, and external stops. GitNexus remained unindexed and was not changed.
