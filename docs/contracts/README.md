# Matryca Trama Public Contracts

This directory contains public contract specifications and the documentation
for their bounded Python reference source. The documents define a reviewable
semantic boundary; they do not claim a published runtime, supported Logseq host,
or production interoperability.

## Contract set

- [Logseq Read Contract v1](LOGSEQ_READ_CONTRACT_V1.md) defines the small
  read-only boundary shared by the bounded Trama producer and its consumers.
- [Parser Compatibility](PARSER_COMPATIBILITY.md) defines the candidate public
  Parser profile and its provenance requirements.
- [Plumber Compatibility](PLUMBER_COMPATIBILITY.md) defines the candidate
  consumer profile for Matryca Plumber.

The contract line `trama.logseq.read/v1` exists in bounded source at `9905e8a`.
Qualification remains a baseline record at `862c5c8`, limited to synthetic OG
fixtures and three operations; the current head and broader Parser/Plumber
interoperability remain unqualified. See the
[delivery program](../specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md).

No document in this directory authorizes a Logseq DB host claim, an export or
derived-store authority claim, events, synchronization, Shadow acceleration,
or writes.
