# Alpha.3 Trama consumer qualification evidence

Date: 2026-10-24

Disposition: **Experimental synthetic qualification passed; consumer NOT ADMITTED.**

This durable, non-normative record preserves selected evidence from
[run 40087531263, attempt 1](https://github.com/MarcoPorcellato/matryca-trama/actions/runs/40087531263)
and [PR #30](https://github.com/MarcoPorcellato/matryca-trama/pull/30).
The [machine-readable archive](evidence/2026-10-24-og-alpha3-m1.json)
contains all 178 member identities and 56 lifecycle records from the four
authenticated report archives, both unit summaries and both producer receipts.
It is evidence, not a new contract, profile status or admission decision.
Trama [#2](https://github.com/MarcoPorcellato/matryca-trama/issues/2) remains the
owner gate; [#4](https://github.com/MarcoPorcellato/matryca-trama/issues/4)
remains separately gated. The
[factual progress comment](https://github.com/MarcoPorcellato/matryca-trama/issues/2#issuecomment-6383569142)
does not admit compatibility.

Machine-record SHA-256:
`3514abaf61d98e46e74f701dc2ab18c1514877308043c3520b19c3a581681f29`.

## Exact source and immutable public bytes

| Role | Binding |
| --- | --- |
| Producer source / tree | `8c30f70e217722e719c5aedc322219ebccb87e68` / `de80d0473aa281c52d0fed10b4561024dd12d76f` |
| Signed tag / object | `v2.1.0-alpha.3` / `c093e9e8aa735b7c37a0c1a56a601a9c31cbdf24` |
| Original publisher | `39887297548/1`, exact repository/tag/release workflow |
| Original wheel | `matryca_plumber-2.1.0a3-py3-none-any.whl`, 756,248 bytes |
| Wheel SHA-256 | `e5bc586a3da76d8e11760b39c9d7ac45b62b1240f085a8a96a573b9902bfea12` |
| Descriptor SHA-256 | `bcc6ac607706e934e5df4e044802aa74c7d7455e7711220df116080f1ab0cc70` |
| Reviewed Trama head | `be5a063cb05672d3968c116b4559f44a0974d31b` |
| Actual tested merge ref | `29563c61b906a97d3e10140167efcf6de79c7bc2` |
| Signed Trama merge/main | `bfd0e8907118905d392953bcd786b063af7e2986` |
| Shared reviewed/tested/merged tree | `b90faba8197b8f106900b181e01a916c235e357b` |

The producer remains the original public wheel. Later verifier, handoff and
evidence-record commits are not replacement producer sources. The
[Plumber handoff](https://github.com/MarcoPorcellato/matryca-plumber/blob/9907c0a0cde2793f32cf5ef7346ff5189dbdbfb4/docs/quality/OG_OPERATIONAL_V1_ALPHA3_PUBLIC_HANDOFF.md)
locates separate producer qualification; it does not substitute for these
Trama-side runs.

## Observed results

| Synthetic consumer row | Unit controls | Real producer invocations | Outcome |
| --- | ---: | --- | --- |
| Linux x86_64, CPython 3.12.14 | 32 | describe; alias-canonicalized snapshot; wrong descriptor; raw alias | PASS |
| macOS arm64, CPython 3.12.14 | 32 | describe; alias-canonicalized snapshot; wrong descriptor; raw alias | PASS |

Both rows use only the authenticated disposable synthetic fixture, exact
Parser 1.9.0 producer closure and the jointly bound `plumber.graph.read/v1`
plus `plumber.graph.topology/v1` resources. No Trama import of Plumber or Parser
is admitted. The separate six-package schema-validator closure is test-only,
not an application dependency decision.

The positive path validates owner schemas, graph/session/source-revision
coherence, complete ordered content-free topology, authenticated golden output
and fixture equality. Negative controls produce exactly
`expectation_mismatch` / exit 3 and `source_rejected` / exit 4. An expected
nonzero exit does not waive any lifecycle gate.

Every retained lifecycle record shows the direct child reaped, process-group
absence as ESRCH, no cleanup exception and successful resource finalization.
EPERM alone is not success. The reviewed boundary enforces incremental 4 MiB
stdout/512-byte stderr limits, a 180-second execution deadline and one shared
five-second finalization budget. No new execution was performed for archival.

Both canonical topology results hash to
`296e49a7bdc2b7ec8cb88d1a77786a676658a9e31fb31f90a98dcd195011bbc8`.
The serialization is defined in the machine record; this is not the packaged
raw golden-file hash. Graph/session IDs are intentionally instance-specific.

## Preservation, privacy and verification limits

The four original hosted artifacts expire on 2026-11-07. This committed record
retains their exact archive IDs, sizes and SHA-256 values; each member's
sanitized-rendering digest; all lifecycle JSON; both complete synthetic receipts;
and the original unit-result summaries. No individual test names are inferred
from summaries that did not retain them. Private authenticated originals remain
preserved for diagnosis without rerunning a producer.

The public archive excludes command arguments, environment values, local
paths, usernames, credentials, raw graph output and copied owner schemas,
fixtures or TCK implementation. Synthetic identity values and output digests
remain available to audit binding and cleanup. It is a selected projection,
not a byte-for-byte replacement for all report ZIP contents. Member digests
describe the archived sanitized rendering; lifecycle stdout/stderr digests
describe the original captured bytes and may differ after sanitization.

Hosted cryptographic verification bound the wheel to its full original source,
repository, tag and release workflow. This evidence projection is neither an
original attestation bundle nor a new local cryptographic verification.
Workflow success and selected receipts are not substitutes for those original
cryptographic inputs.

## Unchanged admission and product boundaries

The packaged catalogue/profile/descriptor/matrix labels remain
`proposed` / `static-only-unqualified` / `unqualified` / `planned`.
Accepting or rejecting external experimental evidence for consumer admission
requires a separate explicit owner decision in #2 under
[ADR-0007](../../decisions/ADR-0007-PLUMBER-CAPABILITY-ADMISSION.md) and
[ADR-0008](../../decisions/ADR-0008-EXPERIMENTAL-PROCESS-BOUNDARY.md).

This record establishes no Logseq desktop-version range, active-desktop
coexistence, user graph, OS network isolation, payload/text/properties, native
DB, Windows installation, writes, events, sync, UI or stable-support claim.
It implements no application adapter and grants no runtime dependency.
Any later #4 scope remains limited to the expressly admitted synthetic tuple
unless a separate owner decision changes that boundary. User-graph access
would additionally require explicit access and separate OS isolation evidence.

PolyForm Noncommercial and the external-contributor rights boundary remain
unchanged. The earlier M6-only frontend-alert exception does not transfer to
Trama or future adapter work. Neither issue is closed by this record.
