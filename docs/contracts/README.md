# Matryca Trama Public Contracts

This directory contains the public contracts and compatibility profiles for
Community integrations. The synthetic OG implementation has exact hosted
qualification evidence; no document here implies a user-graph, Logseq DB host,
application, or broader runtime claim.

## Contract set

- [Logseq Read Contract v1](LOGSEQ_READ_CONTRACT_V1.md) defines the small
  read-only boundary shared by a host-facing Trama producer and its consumers.
- [Parser Compatibility](PARSER_COMPATIBILITY.md) defines the public Parser
  profile and its provenance requirements.
- [Plumber Compatibility](PLUMBER_COMPATIBILITY.md) defines the reference
  consumer profile and future live-integration gate for Matryca Plumber.
- [Ecosystem Responsibility and Change Contract](ECOSYSTEM_RESPONSIBILITY_AND_CHANGE_CONTRACT.md)
  assigns capabilities and interface authority across Trama, Parser, Plumber,
  Brain, and Knowledge, and defines the anti-duplication delivery protocol.

The implemented contract line is `trama.logseq.read/v1`. Exact hosted evidence
at commit `862c5c89157f28c1985cde6145fc2c8af04a70b4` qualifies only owned
synthetic OG fixtures for `graph.identify`, `page.read`, and complete ordered
`block.subtree.read.complete`. Every additional source mode, host, consumer,
operation, or platform requires its own exact-version evidence.

No document in this directory authorizes a Logseq DB host claim, an export or
derived-store authority claim, events, synchronization, Shadow acceleration,
or writes.
