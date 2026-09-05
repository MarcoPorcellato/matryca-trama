# Plumber Compatibility for Logseq Read Contract v1

> **Status:** historical Trama-side synthetic helper and candidate consumer
> profile. No live Trama--Plumber runtime, Plumber session port, or
> cross-repository production integration is qualified. The proposed Plumber
> gateway is not accepted until its ADR and canonical contract are published.

## Purpose

This profile defines the public consumer boundary between Matryca Trama and
Matryca Plumber. Bounded Trama source produces read results through
`trama.logseq.read/v1`; Plumber consumes only those declared public results and
maps them to its own consumer-side ports and retrieval behavior.

## Candidate public version range

| Component | Candidate range | Status |
| --- | --- | --- |
| Matryca Plumber | `v2.0.0` | public stable anchor; Trama compatibility unqualified |
| Logseq Matryca Parser | `>=1.7.1,<2.0.0` | Plumber-supported metadata range; Trama compatibility unqualified |
| Contract line | `trama.logseq.read/v1` | historical bounded source; not published |
| Logseq source mode | `og_markdown` | synthetic initial consumer profile |

Current Plumber source at
`d347d43dad090586b10a77a53c4e0c8fd6da8e15` reports `2.0.1rc3`; the Trama
helper accepts only `2.0.0`. The prerelease is therefore a separate,
unqualified row. Native Logseq DB host support is also not a claim: a DB
profile requires its own official-host spike and exact-version evidence.

## Consumer boundary

Plumber may request only the operations and contract-major versions it accepts.
It must inspect `outcome`, `source_mode`, `authority`, `producer`, capability
set, and provenance before mapping a result into its own domain model.

Plumber must reject `unsupported`, `incompatible`, `authority_failure`, and
`provenance_failure` as non-native input. It must not treat a cached, exported,
or partial result as a successful Trama graph read.

## Ownership and non-goals

- Trama owns host-facing acquisition, capability detection, and provenance.
- Plumber owns consumer mapping, retrieval, CLI/MCP runtime selection, and any
  separately authorized derived projection.
- Neither product imports the other's private implementation.
- This profile does not authorize Plumber writes, Safe-Sync, Shadow
  acceleration, event subscriptions, synchronization, or concurrent mutation.
- When Tine may be active, the combined posture remains strict read-only.

## Future cross-repository evidence gate

Bounded local consumer tests predate the resolved `origin/main`
`70fc14c27b11e31e8f557fd70684b6a83933e7d6`; baseline evidence at `862c5c8`
covers those historical synthetic cases only. Plumber must first publish its
ADR, canonical public contract, schemas, fixtures, and compatibility policy.
A later suite must bind exact Plumber, Trama, Parser, profile, and fixture
versions and prove version negotiation, provenance and authority rejection,
complete-subtree preservation, and unchanged Plumber OG/Shadow behavior. This
document does not claim that any such integration or qualification exists.
