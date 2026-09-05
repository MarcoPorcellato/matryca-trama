# Matryca Trama Public Contracts

This directory contains historical experimental Trama contract specifications,
compatibility profiles, and bounded Python reference-source documentation. They
do not claim a published runtime, supported Logseq host, or production
interoperability. They are not future contract authority while the proposed
Plumber ADR and canonical contract remain unpublished.

## Contract set

- [Logseq Read Contract v1](LOGSEQ_READ_CONTRACT_V1.md) defines the small
  historical read-only boundary shared by a bounded Trama producer and test
  consumers.
- [Parser Compatibility](PARSER_COMPATIBILITY.md) records the historical direct
  Parser profile and provenance requirements.
- [Plumber Compatibility](PLUMBER_COMPATIBILITY.md) records the historical
  consumer helper and a future publication gate for Matryca Plumber.
- [Ecosystem Responsibility and Change Contract](ECOSYSTEM_RESPONSIBILITY_AND_CHANGE_CONTRACT.md)
  is a superseded historical coordination draft. It assigns no current
  authority. Current ownership direction is the separately proposed
  [Plumber gateway migration](../superpowers/plans/2026-09-05-plumber-parser-trama-contract-migration.md), which remains non-operative and makes no runtime or acceptance claim.

The historical line `trama.logseq.read/v1` exists in bounded source retained by
the resolved `origin/main` merge parent
`70fc14c27b11e31e8f557fd70684b6a83933e7d6`. Qualification at
`862c5c8` covers only owned synthetic OG fixtures for `graph.identify`,
`page.read`, and complete ordered `block.subtree.read.complete`; current-head
and broader Parser/Plumber interoperability remain unqualified. A new source
mode, host, consumer, operation, or platform needs its own exact-version
evidence after the Plumber contract is published.

No document in this directory authorizes a Logseq DB host claim, an export or
derived-store authority claim, events, synchronization, Shadow acceleration,
or writes.
