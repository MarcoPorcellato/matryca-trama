# Plumber Compatibility for Logseq Read Contract v1

> **Status:** Trama contains a synthetic reference admission helper for the
> declared stable anchor. No live Trama--Plumber runtime, Plumber session port,
> or current-prerelease compatibility is qualified.

## Purpose

This profile defines the future public consumer boundary between Matryca Trama
and Matryca Plumber. Trama produces host-facing read results through
`trama.logseq.read/v1`; Plumber consumes only those declared public results and
maps them to its own consumer-side ports and retrieval behavior.

## Candidate public version range

| Component | Candidate range | Status |
| --- | --- | --- |
| Matryca Plumber | `v2.0.0` | public stable anchor; Trama compatibility unqualified |
| Logseq Matryca Parser | `>=1.7.1,<2.0.0` | Plumber-supported metadata range; Trama compatibility unqualified |
| Contract line | `trama.logseq.read/v1` | implemented synthetic reference profile |
| Logseq source mode | `og_markdown` | qualified only through Trama-owned synthetic fixtures |

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

Plumber must first publish its consumer evidence profile while referencing,
not copying, this Trama contract. A later cross-repository suite must prove
version negotiation, accepted provenance, unknown-version rejection,
missing-provenance rejection, wrong-authority rejection, complete-subtree
preservation, and unchanged OG/Shadow behavior. It must bind every result to
exact Trama, Plumber, Parser, profile, and fixture versions. This document does
not claim that a live integration exists.
