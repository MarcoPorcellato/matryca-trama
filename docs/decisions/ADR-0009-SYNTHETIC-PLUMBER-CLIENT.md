# ADR-0009: Restricted synthetic Plumber client

Status: Accepted design for the separately approved M2 implementation;
exact-source hosted qualification is required before integration.

Date: 2026-10-24

Owner: Marco Porcellato

Supersedes: None. ADR-0007 capability composition and ADR-0008 historical M1
qualification evidence remain unchanged.

## Context

The owner adopted the exact original alpha.3 joint read/topology tuple in
[#2, comment 6383824647](https://github.com/MarcoPorcellato/matryca-trama/issues/2#issuecomment-6383824647).
The [admission record](../contracts/PLUMBER_SOURCE_ADMISSION.md#current-owner-admission--2026-10-24)
binds its immutable evidence, wheel, source, closure, runtime and synthetic
fixture. Admission alone did not authorize an application adapter. The later
M2 approval separately permits this synthetic-only implementation and hosted
qualification; it does not permit arbitrary roots or broader admission.

## Decision

Place the narrow `KnowledgeGraphGateway.snapshot()` domain port and immutable
content-free graph values in `trama-core`. The port has no filesystem selector
or producer DTO. A complete `GraphSnapshot` contains identity, topology and
provenance, or a sanitized non-retryable `GraphGatewayError` is raised.
The domain enforces unique IDs, parent-before-child canonical preorder,
contiguous ordinals within each root/sibling group, and non-dangling unique
references. It does not interpret Markdown or depend on a producer package.

Admit one outer workspace package, `trama-plumber-client`, import root
`trama_plumber_client`, with only `trama-core` as an internal dependency and no
third-party runtime dependency. Its `PlumberClientAdapter` invokes the exact
original Plumber `2.1.0a3` producer in a separate explicitly provisioned venv.
Preserve the venv interpreter spelling in argv and separately verify its
resolved file identity. Do not replace it with the base interpreter realpath.
The exact admitted closure remains producer-owned, including Parser `1.9.0`;
Trama never imports either implementation. The historical workspace Parser
`1.8.2` environment and reverse bridges are unchanged and non-authorizing.

### Structural synthetic-only scope

The supported client interface accepts an opaque fixture capability, not a
path plus digest. Only the trusted qualification builder issues that capability
after exclusively creating a task-owned directory, writing authenticated owner
fixture bytes and creating its explicit input alias. The private capability
issuer is not a supported arbitrary-path admission API or bypass option.
Before each producer launch, the client checks the capability, directory
ownership and identity, canonical containment and alias binding using metadata
only. It neither reads arbitrary graph files to decide whether a root is
allowed nor parses graph contents. The positive real run starts with that
alias and canonicalizes it in the consumer.

This is a supported-interface scope restriction, not an OS sandbox or a claim
of protection against malicious Python code already running in the consumer.
There is no public runtime fixture builder, user-root selector, UI or general
operator client command. A real-vault route requires a later decision and
qualification; passing a fixture digest is insufficient to open it.

### Validation and lifecycle

The runtime mapper uses only the standard library. It rejects duplicate keys,
non-finite numbers, unknown or missing fields, unsupported versions, foreign
profile bindings, incoherent graph/session/revision identities, incomplete or
oversized topology and invalid domain invariants. Owner schemas remain
authoritative and are authenticated transiently in CI. The differential test
shows agreement on its tested structural cases, not schema equivalence or
general acceptance of every schema-valid document. No owner schema, fixture,
TCK implementation or wire DTO is vendored.

`describe` checks both the advertised original descriptor digest and the
canonical digest of its entire parsed body. The latter is a derived consumer
pin, not a replacement descriptor. Runtime conversion attaches the admitted
profile's provenance; it does not independently authenticate a wheel on every
call. Qualification must first verify the original artifact, attestation,
dependency closure and consumer startup environment before issuing the fixture handle
or constructing the client.

Move the existing M1 process helper and its tests into the package without
changing process mechanics. Retain a qualification-only origin-checked import
at the old test path. The reader remains the single lifecycle owner: stdin is
closed, environment is fresh, a new session is created, output is incrementally
bounded to at most 4 MiB stdout / 512 bytes stderr, and execution is at most
180 seconds. Callers may lower, never raise, those limits. All finalization
phases share five seconds. Cleanup requires reaping plus ESRCH within that
deadline and every stream/selector gate. EPERM is only an observation; unknown
cleanup always fails. No automatic retry is offered.

The read-only posture guard admits the reviewed POSIX process/metadata imports
only inside the new client source root. Writes, `open`, network, SQLite and
dynamic imports remain forbidden; every other package keeps its previous
guard. The canonical dependency policy and machine-readable map change
together, with negative tests protecting the inward-only edge.

## Qualification and evidence

Hosted Linux x86_64 and macOS arm64 rows use CPython `3.12.14`, the original
alpha.3 wheel and exact producer closure. The test-only six-dependency schema
validator environment remains separate; `jsonschema` is not a runtime client
dependency. It loads only exact reviewed same-repository client/core sources,
with startup-hook and module-origin checks. This qualifies the Trama source
candidate, not a published Trama distribution.

`describe` and the positive snapshot run through the client. Existing
wrong-descriptor and raw-alias controls remain harness-only; the extra
1,025-file control must fail with `bounds_exceeded` / exit `5` without changing
the original fixture or providing a client bypass. Every invocation retains
bounded sanitized output, digests and lifecycle evidence before translation
can fail. The capture layer delegates once to the unchanged reader and does
not own another process lifecycle. The exact authenticated golden topology,
mapped values, profile bindings and unchanged fixtures must agree.

No new compatibility result is established by this ADR. Conditional integration
requires accepted frozen-candidate review and all exact-head hosted gates.
Actual run identities and outcomes must be recorded separately.

## Alternatives considered

- Import Plumber or Parser in-process: rejected; it crosses the ownership and
  dependency boundary.
- Copy owner schemas or use `jsonschema` at runtime: rejected; retain owner
  authority and avoid a new application dependency.
- Accept any path after computing a digest: rejected; that reads an arbitrary
  directory before establishing permission.
- Add a second process reader or relax cleanup for convenience: rejected;
  reuse the existing qualified mechanism and its negative controls.
- Treat the client as a real-vault adapter: rejected; the only current tuple
  is synthetic and exact-version-bound.

## Consequences and reversal

This adds restricted source and qualification machinery, not a release,
general Logseq/platform range, OS network-isolation result, user graph,
payload, native DB, write, event, sync or stable-support claim. All packaged
`proposed` / `static-only-unqualified` / `unqualified` / `planned` labels stay
unchanged. Issue #2 remains open. A future #4 slice cannot widen data or
version boundaries through implementation alone.

Withdraw or revise the client if exact provenance, cleanup or owner-contract
coherence fails. New artifacts, runtimes, roots, capacities, payloads and
security claims require their separate owner gates. The future real-vault
profile is tracked in [Plumber #654](https://github.com/MarcoPorcellato/matryca-plumber/issues/654).
Repository material stays PolyForm Noncommercial 1.0.0; no commercial right or
external contribution-rights waiver follows.
