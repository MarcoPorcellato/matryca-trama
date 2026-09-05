---
name: trama-development
description: Use when implementing or reviewing Matryca Trama packages, contracts, adapters, bridges, or boundary-sensitive changes.
---

# Trama development

Use this as a router, not a second policy. Read the [Clean Architecture standard](../../../docs/standards/CLEAN_ARCHITECTURE.md) first. If its projections disagree, stop for policy review.

## Select authority

Read only the authority matching the change:

- package direction or exception: [ADR-0005](../../../docs/decisions/ADR-0005-CLEAN-ARCHITECTURE-ENFORCEMENT.md);
- Parser boundary: [Parser compatibility](../../../docs/contracts/PARSER_COMPATIBILITY.md);
- Logseq read result, provenance, or source mode: [Logseq Read Contract v1](../../../docs/contracts/LOGSEQ_READ_CONTRACT_V1.md);
- Plumber consumer boundary: [Plumber compatibility](../../../docs/contracts/PLUMBER_COMPATIBILITY.md);
- cross-repository ownership: current [Plumber gateway proposal](../../../docs/superpowers/plans/2026-09-05-plumber-parser-trama-contract-migration.md); it is proposed and grants no runtime acceptance; [ecosystem draft](../../../docs/contracts/ECOSYSTEM_RESPONSIBILITY_AND_CHANGE_CONTRACT.md) is superseded historical record only;
- Brain, Pro, commercial use, or external contributions: [ADR-0002](../../../docs/decisions/ADR-0002-TRAMA_BRAIN_PRODUCT_BOUNDARY.md) and [ADR-0003](../../../docs/decisions/ADR-0003-SOURCE_AVAILABLE-COMMERCIAL_BOUNDARY.md).

## Change flow

Before editing, classify the affected package, declared dependencies, public
contract owner, and source authority against the exact package table in the
[Clean Architecture standard](../../../docs/standards/CLEAN_ARCHITECTURE.md)
and the selected accepted contract or ADR; never decide these from memory.
Start with a focused failing behavior or boundary test, then make the smallest
change and re-run it.

Run this validation family for R1 package or boundary work:

```bash
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

## External gates

Route legal and product-boundary decisions to the [Clean Architecture standard
stop gates](../../../docs/standards/CLEAN_ARCHITECTURE.md#validation-and-stop-gates)
and [Contributor Licensing](../../../CONTRIBUTOR_LICENSING.md). Stop when either
gate matches. For any external mutation, stop unless the current instruction
provides its exact authority.
