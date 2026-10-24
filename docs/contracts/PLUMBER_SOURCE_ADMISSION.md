# Plumber Source Admission Record

> **Status:** source-pinned and released-package documentary evidence only.
> This record is not a release artifact, consumer-profile admission, or Trama
> runtime compatibility evidence.

## Purpose

This record pins reviewed upstream source checkpoints and later released-package
evidence so maintainers can compare artifacts against known bytes. It must not create a
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

## Released alpha.3 documentary evaluation — 2026-10-24

**Disposition: documentary evidence verified; consumer NOT ADMITTED and real
invocation NOT AUTHORIZED.** The earlier pins and release-hold discussion remain
historical source observations. This later evaluation does not erase them,
promote packaged status fields, or satisfy Trama's consumer gate by implication.

The [producer handoff](https://github.com/MarcoPorcellato/matryca-plumber/blob/9907c0a0cde2793f32cf5ef7346ff5189dbdbfb4/docs/quality/OG_OPERATIONAL_V1_ALPHA3_PUBLIC_HANDOFF.md)
and [machine-readable record](https://github.com/MarcoPorcellato/matryca-plumber/blob/9907c0a0cde2793f32cf5ef7346ff5189dbdbfb4/docs/quality/evidence/og-operational-v1-2.1.0a3-public.json)
bind the original released producer, not the newer verifier or documentary tree.

| Item | Exact released binding |
| --- | --- |
| Version / signed tag | `2.1.0a3` / `v2.1.0-alpha.3` |
| Producer commit / tree | `8c30f70e217722e719c5aedc322219ebccb87e68` / `de80d0473aa281c52d0fed10b4561024dd12d76f` |
| Signed tag object | `c093e9e8aa735b7c37a0c1a56a601a9c31cbdf24` |
| Original publisher | `39887297548/1` |
| Original wheel / SHA-256 | `matryca_plumber-2.1.0a3-py3-none-any.whl` / `e5bc586a3da76d8e11760b39c9d7ac45b62b1240f085a8a96a573b9902bfea12` |
| Original sdist / SHA-256 | `matryca_plumber-2.1.0a3.tar.gz` / `cbf6f47dece7266c0ec69820ca3ef84e6519ff5d12f5d057c851e5b9c453ed9c` |
| Operational descriptor SHA-256 | `bcc6ac607706e934e5df4e044802aa74c7d7455e7711220df116080f1ab0cc70` |
| Dependency-profile SHA-256 | `9064e339a2fa5e58ce2d49e64b896865dd3a80615b8f5dbd5391c404cde83e92` |
| External public-byte campaign | [39999081040, attempt 1](https://github.com/MarcoPorcellato/matryca-plumber/actions/runs/39999081040) |
| Separate verifier commit | `15a79076932491b588cedc43f5e6497edc87e16b`; not replacement producer source |

The retained authenticated originals were inspected as bytes without extraction,
installation, imports or execution. Twenty-three canonical JSON resources, three
static TCK scripts and sixteen operational resources/modules matched between
the wheel, corresponding sdist source paths and original producer Git objects.
The catalogue and Trama-profile hashes still equal the earlier pins above.
Both required floor bindings are present:

| Floor profile | Schema SHA-256 | Canonical consumer-profile SHA-256 |
| --- | --- | --- |
| `plumber.graph.read/v1` | `250438c57580c811c3e10b2a59089ffbb23ea2f1f66c4c53acc8ace0a9ee8569` | `00e51bb51b945c521c9cf51fc7b451920bb5fc52dddacd921e2d901696703e06` |
| `plumber.graph.topology/v1` | `613f765376f2091b3dad2569ce19d9931f455b026f5ed495178526e87da1397a` | `9da9f9286f276eb18bb50c34327d75b087a891a539ef3c6424d6393f02339ea2` |

The operational descriptor binds those same schemas and advertises only
`graph.identify` and `graph.topology.snapshot.complete`. Historical static
read fixtures mentioning page/subtree operations do not qualify text, properties
or a payload runtime. The static catalogue remains `proposed`, its Trama profile
`static-only-unqualified`, and the operational descriptor/matrix
`unqualified`/`planned`.

The external campaign records eight installed producer rows: Linux x86_64 and
macOS arm64, CPython 3.12.14/3.13.15, original wheel/sdist. Each has full installed
verification, three static TCKs, thirteen operational controls and verified
cleanup. This evaluation rechecked artifact bytes and documentation; it did not
repeat that campaign or establish any Trama consumer result. The exact Parser
1.9.0 profile belongs only in the separate producer environment. No supported
range for other Parser versions, active Logseq desktops or user graphs follows.

### Remaining consumer gates

- Explicitly accept or reject the proposed distinction in
  [draft ADR-0008](../decisions/ADR-0008-EXPERIMENTAL-PROCESS-BOUNDARY.md)
  between a separately authorized qualification experiment and later product
  admission. Until accepted, the current pre-admission invocation hold remains.
- Freeze and separately approve the test-only process boundary, exact
  owner-contract validation route, dependency/runtime profile, synthetic-root
  derivation and security applicability before implementation or execution.
  Plumber's M6-only alert exception does not apply to Trama.
- If separately authorized, start with one hosted Linux x86_64 / CPython
  3.12.14 / original-wheel synthetic probe. Preserve all lifecycle, provenance,
  bounds and failure gates. It is not a production adapter or user-graph test.
- Review the resulting evidence before any explicit #2 admission. Issue #4
  remains dependent on that admission; neither this record nor a successful
  producer TCK can open the real-adapter slice automatically.

No payload, DB, Windows installation, writes, events, sync, UI, stable support,
licensing permission or compatibility admission is added by this evaluation.

### M1 test-only qualification decision — 2026-10-24

The preceding E0 hold and one-row proposal are historical dispositions, not the
current M1 execution scope. The owner accepted ADR-0008 only for separately
authorized synthetic qualification and approved simplified M1 on PR #30.
The dedicated same-repository workflow may provision the exact original wheel
and run `describe`, one positive snapshot and two expected refusals on Linux
x86_64 and macOS arm64 with CPython 3.12.14. There is no user-graph access.

The positive run starts from an explicit alias input and canonicalizes it in
the consumer. The negative controls require `expectation_mismatch` / exit `3`
for the zero descriptor digest and `source_rejected` / exit `4` for the raw
alias. Every invocation must independently satisfy output and cleanup gates;
expected negative exits do not waive them. Fixture equality and authenticated
golden topology, version, graph/session/revision and schema bindings remain
mandatory. Wheel attestation must bind the full original source commit, tag,
repository and release workflow. All owner resource bytes stay transient.

This experiment makes no network-isolation claim and does not reuse Plumber's
M6 alert exception. Its separate test-only validator environment, exact licence
inventory and startup checks are not application-dependency admission. All
qualifying evidence must come from the exact reviewed PR candidate and both
hosted rows before conditional merge. No result is established by this decision
or by source inspection; the workflow artifacts must supply it.

Consumer admission in #2, the runtime-validator dependency decision and the
real adapter under #4 remain separate owner decisions. No payload, DB, Windows,
user graph, write, sync, release or stable compatibility claim follows.
