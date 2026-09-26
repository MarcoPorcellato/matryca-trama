# Plumber Source Admission Record

> **Status:** source-pinned static evidence only. This record is not a release artifact,
> a consumer-profile admission, or runtime compatibility evidence.

## Purpose

This record pins reviewed upstream source checkpoints so maintainers can compare
a future released Plumber artifact against known bytes. It must not create a
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

## Later source checkpoints

These later observations prove source implementation evidence and test-only
capability-policy evidence. This progression does not supersede the original
catalogue pin and does not establish a distributable consumer artifact.

| Evidence | Value |
| --- | --- |
| OG topology runtime merge | Plumber PR #577, merged 2026-09-06 |
| OG topology runtime commit / tree | `405ec69582b3ca240d4747ef9c89b79e0073b545` / `67ccefa91f8b4343c2d5821edae37c7c9aacd805` |
| Topology contract path | `docs/contracts/plumber-graph-topology-v1.md` |
| Topology contract Git blob / SHA-256 | `1083278b94a089f0593ac660bf230393fb9b94ad` / `1a3befbaf9d5442dc186963a374628f758714141f807192d2eee0eed5c4f27dc` |
| DB capability-policy merge | Plumber PR #578, merged 2026-09-06 |
| Current observed commit / tree | `62e1abb6c6177c3063e0dd87c43510190fd9d24a` / `5ceacf991825334ddeb3d825e72acb5c48f3710c` |
| DB capability-policy manifest path | `tests/compatibility/logseq_db_native/manifest.json` |
| DB capability-policy manifest Git blob / SHA-256 | `191995b71f03477d175be8f320c8a94419c50a7c` / `9c8f0ac2584d89dda396b9830a91094b8d83dc57ae4f23036eec05e868375627` |

The runtime checkpoint shows an internal bounded OG implementation behind
Plumber's session boundary. It adds no released transport or consumer package.
The DB checkpoint contains only synthetic rejected-candidate fixtures and an
unbound capability-discovery policy. It is not a production DB adapter and does
not establish Logseq DB support.

### Additive text-payload decision

Plumber accepted a separate `plumber.graph.payload.read/v1` semantics decision
in PR #590, merged at
`233731cde79ceb2e26da91b935ad5a4dfd02c85c`. Its exact owner document is
[`2026-09-12-plumber-graph-payload-read-v1.md`](https://github.com/MarcoPorcellato/matryca-plumber/blob/233731cde79ceb2e26da91b935ad5a4dfd02c85c/docs/decisions/2026-09-12-plumber-graph-payload-read-v1.md)
(Git blob `d149861519dd86fcc2e26e9b87cedc3e127b00e1`). The merge is present in
the live Plumber main observed at `2579702736cb3f63d3cc58aba48a29aa6aed6878`.
This is an accepted documentation decision only: it defines additive bounded
page/subtree payload semantics but publishes no schema, fixture/TCK, released
artifact, runtime route, qualified host, or Logseq DB support.

Trama records the resulting capability composition in
[ADR-0007](../decisions/ADR-0007-PLUMBER-CAPABILITY-ADMISSION.md): the planned
consumer implementation still requires both released identity/read and
topology profiles; text-backed analysis additionally requires the separately
released and qualified payload profile. These semantic prerequisites do not
admit any current artifact or authorize a reduced-profile consumer. Topology
does not supply text, and payload does not supply topology. Each source mode
and each combined profile set requires owner-defined compatibility and exact
graph, session, and source-revision binding evidence.

## Release hold

Git object identity makes these source observations reproducible, but not
distributable. It is insufficient for a Trama dependency pin or a runtime
adapter because it has no released artifact provenance, supported version
matrix, published schema/fixture/TCK bundle, or release-level compatibility
evidence.

Before the planned consumer code starts, Plumber must publish immutable
released artifacts for both `plumber.graph.read/v1` and
`plumber.graph.topology/v1`, including their profile, schema, fixture, TCK,
provenance, supported versions, and fail-closed session, revision, capability,
and bounds behavior. Any text-reading capability additionally requires the
same evidence for `plumber.graph.payload.read/v1`. Trama then revalidates
digests against the exact release and opens a separately authorized
consumer-adapter slice. Combined profiles must satisfy their owner-defined
compatibility and binding rules. A mismatch, missing artifact, changed source
ref, or unreleased profile remains blocked. OG and DB retain independent
release and compatibility gates.

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
