# Parser Compatibility for Logseq Read Contract v1

> **Status:** candidate public compatibility profile with bounded bridge source.
> This document does not qualify current-head or production interoperability.

## Purpose

This profile defines how the bounded Trama producer may use
`logseq-matryca-parser` for the OG Markdown branch of
`trama.logseq.read/v1`. Parser output helps interpret authoritative Markdown;
it does not transfer graph authority to Parser or create any DB capability.

## Candidate public version range

The first candidate profile is:

| Component | Candidate range | Status |
| --- | --- | --- |
| Logseq Matryca Parser | `>=1.7.1,<2.0.0` | candidate range; production interoperability unqualified |
| Contract line | `trama.logseq.read/v1` | implemented bounded source; not published |
| Logseq source mode | `og_markdown` | synthetic read-only profile only |

Parser `v1.8.2` is a public release anchor, but this document does not claim
that Trama has qualified it. Parser 2.x is outside the candidate range until a
new compatibility decision and evidence are published.

## Public API boundary

Only Parser's documented package-root stable API may be used. A future profile
must name every imported public symbol, its Parser range, and the exact fixture
set that exercises it. Internal Parser symbols, copied parser internals, and
undocumented behavior are not a compatibility surface.

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

## Evidence gate

Bounded bridge and synthetic fixtures exist at `9905e8a`; baseline evidence at
`862c5c8` covers only the initial synthetic OG operations and rejection cases.
Current-head and broader Parser qualification must bind exact Trama and Parser
revisions, imported public symbols, accepted graph/page/subtree reads,
source-location provenance, parse failure handling, and versions outside the
range. This document alone is not that evidence.
