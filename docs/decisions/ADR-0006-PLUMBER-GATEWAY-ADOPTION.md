# ADR-0006: Plumber Gateway Adoption

Status: Accepted

Date: 2026-09-05

Owner: Marco Porcellato

Supersedes: the source-adapter and public-wire-contract responsibility assigned
to Trama by ADR-0002 and historical Trama plans; it does not supersede Trama and
Brain product separation.

Superseded by: None

## Context

The historical Trama synthetic read implementation contains a Parser bridge, an
OG adapter, a Plumber helper, and `trama.logseq.read/v1`. Those bounded sources
and their fixtures are useful audit evidence, but their former ownership model
would make Trama both a product and a competing Logseq gateway.

Matryca Plumber accepted its gateway authority decision in
[PR #563](https://github.com/MarcoPorcellato/matryca-plumber/pull/563), merged
at `0646f349572d9a5dfaf37e936f5162b6212dc194`. This ADR adopts that ownership
decision in Trama without claiming a released contract, a consumer profile, or
a runtime integration.

## Decision

Matryca Plumber is the sole Logseq gateway for future Matryca product work.
Plumber owns the future `plumber.*` contract families, source selection, the OG
Parser adapter, any qualified official Logseq DB-host adapter, and the public
schemas that consumers use.

The only future source-to-product flows are:

```text
OG Markdown -> Parser -> Plumber -> Trama / Brain
Logseq DB official host -> Plumber -> Trama / Brain
```

Trama owns graph UI, exploration, intelligence, analysis, Nodi, and its own
domain mapping. A future Trama outer client adapter may implement an internal
`KnowledgeGraphGateway` port over a published Plumber contract. It must not
import Parser, select a source, read Logseq OG Markdown, or access a Logseq DB
or host API.

`trama.logseq.read/v1`, the Parser bridge, the OG adapter, and the Plumber
bridge are historical experimental producer evidence. They are not future
contract authority and remain retained until their separately authorized,
profile-specific replacement and removal gate.

An `og_markdown` consumer profile may qualify independently of Decision D1. A
`db_native` consumer profile requires D1 outcome `supported`; no DB graph falls
back to Markdown.

## Consequences

This is a documentation-only ownership decision: it introduces no runtime
feature, package, schema, public consumer profile, release, host access, DB
support, or performance claim. A canonical Plumber contract artifact, its
fixtures, and an immutable public profile remain separate gates before Trama
consumer code can start.

Historical documents keep their original facts but carry a prominent
non-authorizing redirect to this ADR and the Plumber authority decision. The
current legacy package admissions remain unchanged until the later replacement
gate; this ADR neither removes nor extends them.

Repository-owned Community material remains under PolyForm Noncommercial 1.0.0.
External copyright-bearing contributions remain merge-blocked until a
lawyer-reviewed contributor agreement or equivalent grant exists.

## Reversal

A change to the sole-gateway boundary requires a new ADR in the owning
repository, versioned public contracts, compatibility evidence, and a separate
Trama adoption decision. It must preserve product separation, native source
authority, the PolyForm Noncommercial boundary, and contributor-rights gates.
