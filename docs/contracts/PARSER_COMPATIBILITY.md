# Parser Compatibility for Logseq Read Contract v1

> **Status:** historical experimental direct-Parser profile with bounded bridge
> source. It does not qualify current-head or production interoperability. The
> proposed Plumber-gateway design forbids future Trama-to-Parser integration.

## Purpose

This profile records how the bounded historical Trama producer used
`logseq-matryca-parser` for the OG Markdown branch of
`trama.logseq.read/v1`. Parser output helps interpret authoritative Markdown;
it does not transfer graph authority to Parser or create any DB capability.

## Candidate public version range

The first candidate profile is:

| Component | Candidate range | Status |
| --- | --- | --- |
| Logseq Matryca Parser | `>=1.7.1,<2.0.0` | historical candidate range; production interoperability unqualified |
| Contract line | `trama.logseq.read/v1` | historical bounded source; not published |
| Logseq source mode | `og_markdown` | synthetic read-only profile only |

Parser `v1.8.2` is the locked public artifact in the exact synthetic
qualification. This does not qualify every version in the declared range.
Parser 2.x is outside the range until a new compatibility decision and evidence
are published.

## Public API boundary

Only Parser's documented package-root stable API may be used. Each qualified
profile must name every imported public symbol, its Parser version, and the
exact fixture set that exercises it. Internal Parser symbols, copied parser
internals, and undocumented behavior are not a compatibility surface.

The producer must preserve enough public Parser-derived location and diagnostic
information to report source provenance and an explicit unsupported or failure
result. It must not convert parse ambiguity into guessed graph content.

## Required behavior

- The source of authority remains selected Logseq OG Markdown.
- A parser failure, unsupported representation, or missing source location
  yields a contract failure; it never yields a page or subtree success from a
  cache or inferred reconstruction.
- Successful `page.read` and `block.subtree.read.complete` results retain the
  source-mode and authority values required by the core contract.
- Parser use is read-only. It creates no write, synchronization, export, or DB
  mutation capability.

## Evidence and future gate

Bounded bridge and synthetic fixtures exist before the resolved `origin/main`
`70fc14c27b11e31e8f557fd70684b6a83933e7d6`; baseline evidence at `862c5c8`
covers only initial synthetic OG operations and rejection cases. This document
does not authorize a new Trama Parser profile. The future gateway, if accepted,
belongs to Plumber and needs its published ADR, canonical contract, and its own
exact-version evidence.
