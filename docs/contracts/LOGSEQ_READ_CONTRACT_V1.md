# Logseq Read Contract v1

> **Status:** implemented and qualified only for the exact owned synthetic OG
> profile recorded below. No user graph, Logseq DB host, or broader runtime is
> qualified.

## Purpose

`trama.logseq.read/v1` defines a minimal read-only interchange boundary between
a host-facing Matryca Trama producer and public consumers. It preserves
native Logseq source authority and makes incompatibility or missing provenance
an explicit result rather than an inferred success.

For Logseq OG, authoritative source is the selected graph's Markdown files. For
Logseq DB, authoritative source is the native local database through a later
qualified official Logseq host surface. A cache, export, index, or derived
projection is never a substitute authority.

## Contract status and scope

The contract line is `trama.logseq.read/v1`. Every concrete profile must
publish its semantic contract version, producer version or source revision,
supported Logseq host version, and fixture set before it claims conformance.

Only these operations are in scope:

| Operation | Successful outcome |
| --- | --- |
| `graph.identify` | identifies one selected graph, its source mode, authority, and advertised capabilities |
| `page.read` | returns one requested page with provenance |
| `block.subtree.read.complete` | returns one requested root block and its complete ordered descendant subtree with provenance |

Out of scope: graph selection beyond the selected graph, events, subscriptions,
background watch, synchronization, Shadow acceleration, export, concurrent
mutation, writes, round-trip recovery, and host-authoritative automation.

## Request and result envelopes

Requests and results have separate envelopes. A request declares what a
consumer accepts; a result declares what a producer actually supplied. Every
future language binding must preserve their meaning.

| Request field | Requirement |
| --- | --- |
| `contract_id` | exactly `trama.logseq.read/v1` for this contract line |
| `accepted_contract_major` | contract major version accepted by the consumer |
| `operation` | one listed operation identifier |
| `request_id` | caller-generated opaque identifier, unique within its session |
| `graph_selector` | opaque selection context; it may name a host-selected graph but never enumerate graphs or expose a local path |
| operation reference | opaque `page_reference` or `block_reference` when the operation requires one |

| Result field | Requirement |
| --- | --- |
| `contract_id` | exactly `trama.logseq.read/v1` for this contract line |
| `contract_version` | semantic version of the concrete producer profile |
| `operation` and `request_id` | values corresponding to the request |
| `outcome` | `success`, `unsupported`, `incompatible`, `invalid_request`, `not_found`, `authority_failure`, or `provenance_failure` |
| `graph_binding` | opaque selected-graph identity when the producer can safely establish one |
| `producer` | public producer name and released version or source revision |
| `capabilities` | advertised capability identifiers for the selected profile |
| `provenance` | required for `success`; incomplete or absent evidence requires `provenance_failure` |

`graph_selector`, `graph_binding`, page references, and block references are
opaque identifiers. They must be stable enough for the concrete profile's
declared session or graph scope, but they must not expose local filesystem
paths, credentials, or user vault content outside the requested result.

## Provenance

Each successful result must include:

| Field | Requirement |
| --- | --- |
| `source_mode` | `og_markdown` or `db_native` |
| `authority` | `logseq_og_markdown` for OG or `logseq_db_native` for DB |
| `source_reference` | opaque source binding scoped to the selected graph and profile |
| `producer` | same producer identity as the shared envelope |
| `exercised_capabilities` | capabilities used for this operation |
| `evidence_digest` | digest of the synthetic fixture or declared result representation |

A producer that cannot state native authority or supply complete provenance must
return `provenance_failure`. It must not report a successful read from a cache,
export, or derived store as though it came from the native source.

## Operation semantics

### `graph.identify`

The result identifies exactly one selected graph and includes `graph_binding`,
`source_mode`, `authority`, `capabilities`, and provenance. It does not discover
or enumerate other graphs, alter graph state, or imply that every advertised
capability is currently qualified. A request does not need a pre-existing
`graph_binding`; it supplies only its `graph_selector`.

### `page.read`

The request contains one opaque `page_reference`. A success returns one page
whose identity, ordered content representation, and provenance are sufficient
for the concrete profile to distinguish it from another page in the selected
graph. A profile must define its page naming and property representation before
claiming conformance.

`not_found` means the selected graph has no matching page under that profile.
`unsupported` means the producer does not support page reads for that source
mode. Neither result may be replaced by a guessed page or a cached page from an
unknown source revision.

### `block.subtree.read.complete`

The request contains one opaque `block_reference`. A success returns the root
block and every descendant reachable from it in the source's declared order.
The result must state that its subtree is complete. A producer that cannot
establish completeness, preserve source order, or identify the root must return
`provenance_failure`, `unsupported`, or `not_found` as applicable; it must not
return a partial subtree as success.

The concrete profile must publish how it represents ordered children, block
properties, and source locations. It may not silently flatten a hierarchy when
the requested result requires a subtree.

## Failure semantics

| Outcome | Meaning | Consumer rule |
| --- | --- | --- |
| `unsupported` | operation or source mode is outside producer capability | do not retry through another authority implicitly |
| `incompatible` | contract, producer, consumer, Parser, or host version is outside declared range | stop and select an explicitly compatible profile |
| `invalid_request` | request lacks required fields or violates profile constraints | correct request; do not infer missing references |
| `not_found` | requested graph-local page or block is absent | do not substitute a similarly named object |
| `authority_failure` | native authority is unavailable or cannot be safely selected | do not fall back to cache or export authority |
| `provenance_failure` | result cannot prove required source or completeness facts | do not consume result as native graph content |

Concrete profiles may add stable, namespaced error codes, but they must map to
one outcome above and document retryability. No failure result permits writes.

## Compatibility negotiation

A consumer declares the contract-major versions and operation capabilities it
accepts. A producer declares its contract version, source mode, host binding,
and capabilities. Conformance requires matching major version, requested
operation support, complete provenance, and a profile whose declared Parser,
Plumber, and Logseq host ranges contain the participating versions.

An absent version, unselected host route, or unsupported source mode is
`incompatible` or `unsupported`; it is not a default to a nearby version.

## Privacy and public-boundary rules

- Public fixtures are synthetic, sanitized, and owned by Trama.
- Contract evidence must not contain user vaults, local paths, generated DB
  files, credentials, or private Matryca Brain source.
- Trama and consumers communicate through public versioned contracts only;
  neither imports another product's private implementation.
- Tine Direct Files context does not grant a second writer. A possibly active
  Tine session remains a strict read-only condition.

## Conformance evidence and next gate

The public Python packages and conformance suite implement this contract for
owned synthetic OG fixtures. Exact hosted evidence at commit
`862c5c89157f28c1985cde6145fc2c8af04a70b4` records accepted reads and
rejection of unknown version, missing provenance, wrong authority, incomplete
subtree, and private dependency.

That evidence does not qualify a user graph, Logseq DB host, new consumer
version, application, or platform not recorded there. Every new profile must
repeat the applicable positive and negative gates and bind exact producer,
consumer, host, Parser, fixture, and result identities.
