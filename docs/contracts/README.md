# Matryca Trama Public Contracts

This directory contains planned public contracts for Community integrations.
These documents define a reviewable semantic boundary; they do not claim a
published runtime, supported host, or qualified implementation.

## Contract set

- [Logseq Read Contract v1](LOGSEQ_READ_CONTRACT_V1.md) defines the small
  read-only boundary shared by a future Trama producer and its consumers.
- [Parser Compatibility](PARSER_COMPATIBILITY.md) defines the planned public
  Parser profile and its provenance requirements.
- [Plumber Compatibility](PLUMBER_COMPATIBILITY.md) defines the planned
  consumer profile for Matryca Plumber.

The contract line is planned as `trama.logseq.read/v1`. An implementation may
claim conformance only after an accepted application-stack decision, public
synthetic fixtures, executable conformance tests, and exact-version evidence.

No document in this directory authorizes a Logseq DB host claim, an export or
derived-store authority claim, events, synchronization, Shadow acceleration,
or writes.
