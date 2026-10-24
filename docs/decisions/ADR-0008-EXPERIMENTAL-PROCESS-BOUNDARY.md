# ADR-0008: Experimental Process-Boundary Proposal

Status: Accepted for test-only synthetic qualification; non-admitting

Date: 2026-10-23

Documentary clarification and scoped owner acceptance: 2026-10-24.

Owner: Marco Porcellato

Supersedes: None

Superseded by: None

## Context

Any future evaluation of a Plumber producer through a separate process needs a
clear boundary between Trama and the operator's producer environment. A process
boundary could isolate dependencies and keep Trama from importing producer
implementation details, but it would not itself establish a supported public
contract or make a producer safe, available, or compatible.

The existing Plumber capability decisions and Trama source-admission gates
remain authoritative. This proposal does not add a profile, waive an admission
prerequisite, or turn a draft, issue, checkout, or test double into evidence of
a released capability.

The later alpha.3 [documentary evaluation](../contracts/PLUMBER_SOURCE_ADMISSION.md#released-alpha3-documentary-evaluation--2026-10-24)
now locates original public bytes and bounded external producer evidence for
both floor profiles. It does not admit the producer into Trama. The packaged
catalogue/profile/descriptor/matrix status fields remain unchanged.

## Decision

For an explicitly authorized test-only qualification experiment, use
one explicit operator-selected virtual environment and invoke only an exact,
reviewed producer entry point in a child process. The Trama side should not
import Parser or Plumber packages, load producer code in-process, or discover
the operator environment implicitly. Invocation inputs and outputs should be
opaque bounded bytes until authenticated owner-published contracts define their
meaning and an explicit Trama decision defines the permitted use. A proposed
qualification experiment is not product admission.

### Evaluation, qualification and admission are separate gates

The accepted test-only policy distinguishes three activities:

1. **Documentary evaluation:** inspect exact released artifacts, schemas,
   profiles, fixtures/TCKs and provenance without invoking a producer. This can
   establish a candidate for further consideration, never compatibility.
2. **Qualification experiment:** separate owner authorization may permit a frozen, reviewed test-only
   boundary and a finite real-producer probe using disposable synthetic roots.
   Both released read and topology floor profiles remain mandatory. This is
   evidence gathering for #2, not an application adapter or user-facing feature.
3. **Consumer admission:** after independent review of exact consumer evidence,
   the owner may make a separate scoped decision in #2. Only that decision can
   open production adapter work under #4 and ADR-0007.

The owner approved the simplified M1 milestone on 2026-10-24: a test-only
qualification implementation and real alpha.3 producer invocations in the
same-repository PR workflow, on disposable synthetic fixtures only. E0 approval
and producer TCK results did not grant that authority. Acceptance of this ADR
alone does not authorize a future experiment, user-graph access or compatibility
admission. The exact experiment scope remains a separate owner decision.

The proposed invocation shape is:

```text
/absolute/operator-venv/bin/python -I -B -m matryca_plumber.graph_gateway snapshot --graph-root <os.path.realpath(root)> --expect-descriptor-sha256 <h>
```

The separately approved M1 experiment may execute this command on the
authenticated released synthetic fixture. It does not open a production
adapter. The historical fake-only tests do not read a graph root. The M1
positive test receives an explicit alias and canonicalizes it in the consumer;
the negative alias control deliberately passes the same noncanonical path
unchanged and expects `source_rejected` / exit `4`.

The candidate producer profile specifies a 180-second execution deadline and
up to 5 seconds for finalization after the child terminates. Its output caps are
4 MiB stdout and 512 bytes stderr; a future consumer must enforce both
incrementally, before retaining bytes beyond either limit. These values are
mandatory M1 limits. One shared five-second budget covers all finalization
phases, rather than granting each phase a new budget. The historical fake
helper remains unchanged; the promoted test-local helper must prove the new
contract. Exit code `4` means `source_rejected` and is non-retryable. An
expected negative control passes only when its exact exit/error and cleanup
evidence agree; a nonzero exit alone is never evidence of success.

Cleanup is verified only when the direct child has been reaped, process-group
absence is observed as ESRCH within the existing finalization deadline, and
all stream, reader and selector gates pass. EPERM is a retained observation,
never success. Unresolved observations, exceptions or an expired deadline
must fail closed.

The candidate version matrix below is explicitly **CANDIDATE / NOT-ADMITTED**;
it does not state support or qualification:

| Dimension | Candidate value | Status and boundary |
| --- | --- | --- |
| Plumber producer | `2.1.0a3` | Candidate only; not admitted. |
| M1 probe rows | Linux x86_64 and macOS arm64, CPython `3.12.14`, original public wheel | Separately authorized synthetic experiments only; not admitted. |
| Wider producer evidence | CPython `3.12.14` and `3.13.15`, original wheel/sdist | External producer evidence only; not Trama qualification. |
| Producer platform | Linux x86_64; macOS arm64 | Candidate only; no platform support claim. |
| Parser | `1.9.0` | Producer environment only; no Trama dependency or direct Trama import. |
| Windows | Refusal only | No invocation or support claim. |
| Payload and native DB profiles | Excluded | No payload, database, or graph-content capability is proposed. |

Local fake-child tests prove only consumer-side process mechanics. The dedicated
same-repository qualification workflow may additionally exercise the exact
public producer on the synthetic fixture under the separately approved M1
scope. Passing either kind of test does not admit a producer/profile, establish
a real adapter or authorize user graphs. Both hosted rows must pass before
conditional merge; the consumer-owner admission decision remains in #2.

### M1 execution and environment boundary

The consumer runs its absolute reviewed `tests/qualification/real_probe.py`
under a separate six-dependency environment with `-I -B`. It adds only its own
resolved test directory to the import path and checks sibling module origins.
This test-local mechanism does not authorize package-level path mutation,
sibling-repository injection, or in-process Plumber/Parser imports. Before the
first consumer interpreter start, the provisioning interpreter checks the exact
top-level import-root set and rejects `.pth`, `sitecustomize`, `usercustomize`
and a top-level `tests` package. Producer dependencies remain in another venv.

The original wheel is checked for exact size and SHA-256 before resource use.
Cryptographic attestation verification must bind the full producer commit,
repository, release workflow and tag ref. Resources are read only by exact
allowlisted member names with byte ceilings and authenticated digests. No
schema, fixture, golden result or owner TCK is vendored into Trama.

The M1 experiment makes no operating-system network-isolation claim. It uses
only synthetic data in disposable hosted runners, performs no qualification-time
network retrieval, and refuses remote schema resolution. Network isolation is
required before any later real user-graph access can be considered. Fixture
before/after evidence remains mandatory; an installed-environment ledger and
privileged network namespace are not part of this experiment.

Sanitized artifacts retain bounded synthetic stdout/stderr, original digests,
and lifecycle evidence on success and failure. Redaction removes runner paths,
usernames, environment values and accidental credentials, not document shape or
the fields needed to diagnose a mismatch. Cleanup success requires reaping,
ESRCH before the shared deadline and every resource gate. EPERM observations
survive exceptions and deadline failure and become failure events if cleanup
cannot be proven. EACCES, EINTR and EINVAL remain failures.

Consumer defects may use at most three M1 repair cycles; own-check false
positives can be corrected without changing criteria. A producer defect,
applicable unresolved advisory, signing failure, provenance/hash mismatch,
uncertain cleanup or requested gate relaxation requires an owner disposition.
No failed real-producer call is silently retried. Product admission and real
adapter implementation remain excluded even after a green experiment.

### Proposed owner-contract validation route

Consume the authenticated released Draft 2020-12 schemas as transient owner
resources, not copied normative files or reconstructed wire DTOs. A generic
schema validator must not substitute for the owner-defined profile composition,
graph/session/revision coherence, bounds, completeness and failure semantics;
the frozen consumer tests must check those bindings explicitly without copying
the owner's implementation or TCK logic.

The M1 consumer uses `jsonschema==4.26.0` and its complete six-package closure
from `tests/qualification/requirements.txt`, with the Linux/macOS wheel hashes
in that test-only profile. Identity, notice/licence bytes and startup-hook
absence are checked before use. The licence inventory records their exact
test-only status. This does not admit `jsonschema` as an adapter runtime
dependency or permit imports from the producer environment. Remote schema
references, Plumber/Parser imports and substituting a producer-side TCK for a
Trama consumer test remain prohibited.

No application dependency or copied owner resource is introduced by this
decision. The historical reverse bridge remains non-authorizing;
`KnowledgeGraphGateway` remains a planned domain port, not an implemented
application path established by this proposal.

This process boundary would be only an execution mechanism. Before any
user-facing capability could be claimed, the relevant released Plumber
profiles, owner-defined schemas and fixtures/TCKs, compatibility rules, and
mode-specific qualification would still need independent admission. Graph
identity, content-free topology, and text payload retain distinct profile
requirements under [ADR-0007](ADR-0007-PLUMBER-CAPABILITY-ADMISSION.md).

## Alternatives considered

- **Import the producer or Parser in-process:** rejected for this proposal
  because it couples Trama to producer internals and defeats the intended
  dependency boundary.
- **Copy producer schemas, fixtures, or TCKs into Trama:** rejected because
  those contracts and test vectors remain owner-defined; duplication would
  create a second, potentially divergent authority.
- **Treat a fake child or process success as profile admission:** rejected
  because transport behavior cannot establish contract semantics,
  publication, compatibility, or runtime qualification.
- **Add a production adapter now:** deferred. The proposal does not establish
  the released contract, implementation scope, or the independent evidence
  required by Trama's current admission gates.

## Consequences

This decision admits no production code, application dependency, real adapter,
user graph, new profile, copied schema/fixture/TCK, host integration, capability
claim or release. The separate M1 approval is limited to test-only provisioning
and synthetic qualification of immutable alpha.3. Fake-process containment
tests alone do not exercise a producer or establish compatibility.

The existing Trama consumer gate remains unchanged. In particular, graph
identity and topology remain blocked until their existing released-profile
prerequisites are met. Text-backed behavior separately requires its released
payload profile. No admission follows from this draft or its tests.

## Reversal and next decision

Withdraw or revise this test-only decision if an owner-published process contract,
operator security review, or Trama's existing architectural boundaries make
the proposed isolation unsuitable. Each later qualification experiment needs
its own approved scope and controls. Before production adapter
implementation, require the exact admitted capabilities and the separate #4
gate. M1 is the only current real-probe scope; the Plumber M6-only security
exception does not carry over. No acceptance here alone admits a producer artifact, authorizes a
user-facing capability or change ADR-0007's composition requirements.
