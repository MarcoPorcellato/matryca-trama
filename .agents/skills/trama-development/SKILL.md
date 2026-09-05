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
- ownership across repositories: [ecosystem responsibility contract](../../../docs/contracts/ECOSYSTEM_RESPONSIBILITY_AND_CHANGE_CONTRACT.md), which remains proposed unless accepted;
- Brain, Pro, commercial use, or external contributions: [ADR-0002](../../../docs/decisions/ADR-0002-TRAMA_BRAIN_PRODUCT_BOUNDARY.md) and [ADR-0003](../../../docs/decisions/ADR-0003-SOURCE_AVAILABLE-COMMERCIAL_BOUNDARY.md).

## Change flow

Classify affected package, declared dependencies, public contract owner, and source authority before editing. Keep Parser use behind `trama_parser_bridge`; adapters consume its public symbols. Start with a focused failing behavior or boundary test, then make the smallest change and re-run it.

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

Stop and obtain required review or authorization when source authority could change; a contract is not released or source-bound; a proposed ownership contract is treated as accepted; work adds DB, writes, events, Shadow, synchronization, export, recovery, network behavior, UI, Nodi runtime, Brain/Pro source, entitlement, pricing, or commercial rights; an external copyright-bearing contribution lacks a lawyer-reviewed grant; or work would push, open or change GitHub objects, merge, release, change licence, or install a personal/global skill.
