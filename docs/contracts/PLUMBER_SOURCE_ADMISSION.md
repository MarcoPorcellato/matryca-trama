# Plumber Source Admission Record

> **Status:** source-pinned static evidence only. This record is not a release artifact,
> a consumer-profile admission, or runtime compatibility evidence.

## Purpose

This record pins one reviewed upstream source state so maintainers can compare a
future released Plumber artifact against known bytes. It must not create a
runtime adapter, dependency, client, package import, transport, endpoint, CLI,
MCP tool, UI, Parser, Logseq, filesystem, or DB dependency.

It does not copy Plumber schema, TCK, profile, or LENS bytes. This repository
contains only original prose, object identifiers, paths, and digests. A future
implementation must consume a released public artifact through a Trama-owned
outer adapter behind `KnowledgeGraphGateway`; it must not copy owner semantics
or import Plumber implementation modules.

## Pinned upstream observation

| Item | Value |
| --- | --- |
| Repository | `MarcoPorcellato/matryca-plumber` |
| Merge | PR #575, merged 2026-09-06 |
| Commit | `2606c096e07555b977687299eae71842cb6f021a` |
| Git tree | `a24f949e994454b224fcb0d8e7c271ea5990ccf1` |
| Catalogue path | `contracts/plumber.consumer.package/v1/manifest.json` |
| Catalogue Git blob / SHA-256 | `bcd2302a2ec547ac552fd6dddd78ab836c5523f1` / `d0ec4bf4537a642803d42238bacf6b8e0252a61467578091d65586d46eb5cc3a` |
| Catalogue schema path | `contracts/plumber.consumer.package/v1/schema.json` |
| Catalogue schema Git blob / SHA-256 | `9f7a677bd8678d0d2b12ea0ae15badd76b291e16` / `192f7b6d4719ca5d319ffdeb4e749f4b9551eef1974fd43317c0ec9ee506492c` |
| Trama profile path | `contracts/plumber.consumer.package/v1/fixtures/matryca-trama-profile-v1.json` |
| Trama profile Git blob / SHA-256 | `df2a6de4f8f6ccebb980291862239b23264c2e55` / `fc163e8f695821e4a933f6d51dda1eaf29a12bc0d5ca4c3f9adce4e421e63750` |
| Read schema SHA-256 | `250438c57580c811c3e10b2a59089ffbb23ea2f1f66c4c53acc8ace0a9ee8569` |
| Read consumer-profile SHA-256 | `00e51bb51b945c521c9cf51fc7b451920bb5fc52dddacd921e2d901696703e06` |
| Topology schema SHA-256 | `613f765376f2091b3dad2569ce19d9931f455b026f5ed495178526e87da1397a` |
| Topology consumer-profile SHA-256 | `9da9f9286f276eb18bb50c34327d75b087a891a539ef3c6424d6393f02339ea2` |

The observed Trama profile identifies itself as
`static-only-unqualified`. Its source catalogue is `proposed`; neither field
establishes a release, runtime support, capability negotiation, host support,
or compatibility qualification.

## Release hold

Git object identity makes this source observation reproducible, but not
distributable. It is insufficient for a Trama dependency pin or a runtime
adapter because it has no released artifact provenance, supported version
matrix, published schema/fixture/TCK bundle, or release-level compatibility
evidence.

Before consumer code starts, Plumber must publish immutable released artifacts
for both `plumber.graph.read/v1` and `plumber.graph.topology/v1`, including
their profile, schema, fixture, TCK, provenance, supported versions, and
fail-closed session, revision, capability, and bounds behavior. Trama then
revalidates digests against that release and opens a separately authorized
consumer-adapter slice. A mismatch, missing artifact, changed source ref, or
unreleased profile remains blocked.

## Rights and product boundary

This is repository-owned documentation under PolyForm Noncommercial 1.0.0; it
does not grant commercial use or describe Trama as open source. No external
copyright-bearing contribution may be merged until a lawyer-reviewed
contributor agreement or equivalent grant exists. Do not add third-party source,
fixtures, LENS assets, or copied Plumber artifacts to satisfy this record.

Trama remains unaware of Parser and source adapters. Future source paths stay
`OG Markdown -> Parser -> Plumber -> Trama / Brain` and
`Logseq DB official host -> Plumber -> Trama / Brain`; this record changes
neither path and creates no DB fallback.
