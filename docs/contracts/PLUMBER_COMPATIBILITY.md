# Plumber Compatibility for Logseq Read Contract v1

> **Status:** candidate public consumer profile with bounded local bridge tests.
> No separately qualified cross-repository production integration is claimed.

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
| Contract line | `trama.logseq.read/v1` | implemented bounded source; not published |
| Logseq source mode | `og_markdown` | synthetic initial consumer profile |

Matryca Plumber development prereleases are not a compatibility claim. Native
Logseq DB host support is also not a claim: a DB profile requires its own
official-host spike and exact-version evidence.

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

## Evidence gate

Bounded local consumer tests exist at `9905e8a`; baseline evidence at `862c5c8`
covers those local synthetic cases only. A separate cross-repository suite must
prove version negotiation, accepted provenance, unknown-version rejection,
missing-provenance rejection, wrong-authority rejection, and complete-subtree
preservation. It must bind every result to exact Trama, Plumber, Parser, and
fixture versions. This document does not claim that qualification exists.
