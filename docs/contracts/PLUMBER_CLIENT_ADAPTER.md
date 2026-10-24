# Restricted synthetic Plumber client

This implementation follows [ADR-0009](../decisions/ADR-0009-SYNTHETIC-PLUMBER-CLIENT.md)
and the exact [owner admission](PLUMBER_SOURCE_ADMISSION.md#current-owner-admission--2026-10-24).
It is not a real-vault adapter, released Trama distribution or broader
compatibility claim. Integration still requires exact-source hosted evidence.

## Ownership and interface

`trama_core.graph_gateway.KnowledgeGraphGateway` exposes only
`snapshot() -> GraphSnapshot`. Its immutable values live in
`trama_core.graph_values`. No JSON, filesystem selector, Parser object or
producer DTO crosses that port. Topology is complete and content-free:
IDs, page/block kind, parentage, local sibling order and reference edges only.
Titles, block text and properties require a separately qualified payload
profile and are not inferred from topology.

`trama_plumber_client.adapter.PlumberClientAdapter` is the outer implementation.
Its package depends only on core and the standard library. It does not import
Plumber, Parser, historical bridges/adapters, Brain or Pro. The legacy
Parser-bearing workspace packages retain their historical environment and are
not used to supply this producer.

## Exact admitted profile

| Item | Required value |
| --- | --- |
| Producer | Plumber `2.1.0a3`, source `8c30f70e217722e719c5aedc322219ebccb87e68` |
| Original wheel SHA-256 | `e5bc586a3da76d8e11760b39c9d7ac45b62b1240f085a8a96a573b9902bfea12` |
| Descriptor SHA-256 | `bcc6ac607706e934e5df4e044802aa74c7d7455e7711220df116080f1ab0cc70` |
| Profile / floor | `plumber.og.operational/v1`; jointly bound read/topology v1 |
| Producer closure | Exact hash-locked closure including Parser `1.9.0` |
| Admitted consumer tuple | Linux x86_64/macOS arm64, CPython `3.12.14`, authenticated disposable synthetic fixture; new M2 run evidence remains required |
| Maximum topology | 1,024 total nodes and 4,096 edges; no partial result or pagination |
| Maximum process | 180 seconds; 4 MiB stdout, 512 bytes stderr; shared five-second finalization |

The schema ceilings of 4,096 nodes and 16,384 edges do not raise this profile's
smaller runtime limits. Limits may only be lowered by configuration. Node IDs
are not promised stable across source revisions; graph identity may depend on
the canonical root. No Logseq application/version-range claim follows.

## Invocation boundary

The trusted qualification builder creates the authenticated fixture in a new
owned directory and returns an opaque capability containing its explicit
alias. The client accepts only that handle, never a free path or a
path-plus-digest pair. It validates structure before content reads or launch.
The private builder handoff is not a supported caller bypass and is not an OS
security boundary against code already executing in the consumer.

The provisioner supplies an absolute producer venv interpreter and its expected
resolved executable. The client checks file identity separately while retaining
the original venv interpreter spelling. The only snapshot argv is:

```text
/absolute/producer-venv/bin/python -I -B -m matryca_plumber.graph_gateway snapshot --graph-root <canonical-builder-root> --expect-descriptor-sha256 <exact-alpha3-descriptor>
```

There is no shell, discovery, graph override, unknown-descriptor option or
automatic retry. All graph content access remains inside Plumber. A fresh
minimal environment excludes inherited credentials and producer-selection
variables. Startup-hook and artifact authentication are provisioning gates,
not claims inferred from a successful child exit.

## Result and error handling

The strict standard-library mapper checks closed shapes, duplicate keys,
finite JSON, exact versions/profile IDs, graph/session/revision coherence,
completeness, actual profile limits and domain topology invariants. It yields
one `GraphSnapshot` or a sanitized non-retryable domain error. No partial graph
or raw stderr is returned on failure. Schema validation remains a transient
CI check, not an application runtime dependency or copied normative artifact.

Consumer errors are `configuration_invalid`, `admission_scope_violation`,
`spawn_failed`, `process_timeout`, `process_output_limit`, `cleanup_uncertain`,
`protocol_violation`, `contract_violation` and `topology_invariant_violation`.
Known producer errors are translated only when their exact error/exit pairing
and cleanup agree: `usage`/2, `expectation_mismatch`/3, `source_rejected`/4,
`bounds_exceeded`/5, `source_changed`/6, `unsupported_platform`/7,
`unsupported_dependency`/8, `audit_hook_unavailable`/9 and `internal`/70.
Unknown, malformed, extra-field or output-bearing failures are protocol errors.
Uncertain cleanup takes precedence and requires operator intervention.

Cleanup success still requires the direct child reaped, group absence as
ESRCH before the shared deadline, and all stream/selector gates. EPERM is an
observation only; persistent observations become failure events. The original
M1 reader mechanics are moved without behavioral changes, not replaced.

## Qualification boundary

Standard hosted CI checks the domain, client, architecture and all preserved
historical suites. The dedicated workflow provisions the original authenticated
producer and a separate six-package validator environment. `describe` and the
positive alias snapshot execute through the client. Wrong-descriptor,
raw-alias and the 1,025-file refusal remain harness-only controls, not public
adapter options. Owner schemas and golden data remain transient authenticated
resources. Differential validation proves agreement only on tested cases.

Sanitized artifacts retain enough synthetic output and original digests to
diagnose shape failures without rerunning. Qualification on source does not
publish the client, admit a new producer or enable user graphs. OS sandbox
evaluation is a later, separately governed exploratory milestone and cannot
be claimed from the producer's Python audit hook.
