# Plumber Compatibility for Logseq Read Contract v1

> **Status:** planned public consumer profile. No Trama--Plumber runtime
> integration is implemented or qualified by this document.

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
| Contract line | `trama.logseq.read/v1` | planned |
| Logseq source mode | `og_markdown` | planned initial consumer profile |

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

## Future evidence gate

After ADR-0004 selects the public package and test layout, a synthetic
cross-repository suite must prove version negotiation, accepted provenance,
unknown-version rejection, missing-provenance rejection, wrong-authority
rejection, and complete-subtree preservation. It must bind every result to
exact Trama, Plumber, Parser, and fixture versions. This document does not
claim that those tests or an integration exist.
