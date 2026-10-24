# ADR-0008: Experimental Process-Boundary Proposal

Status: Draft — not accepted; non-admitting

Date: 2026-10-23

Documentary clarification: 2026-10-24; still draft and not accepted.

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

## Decision (proposed)

If a later, separately authorized implementation is considered, it should use
one explicit operator-selected virtual environment and invoke only an exact,
reviewed producer entry point in a child process. The Trama side should not
import Parser or Plumber packages, load producer code in-process, or discover
the operator environment implicitly. Invocation inputs and outputs should be
opaque bounded bytes until authenticated owner-published contracts define their
meaning and an explicit Trama decision defines the permitted use. A proposed
qualification experiment is not product admission.

### Evaluation, qualification and admission are separate gates

The proposed policy distinguishes three activities:

1. **Documentary evaluation:** inspect exact released artifacts, schemas,
   profiles, fixtures/TCKs and provenance without invoking a producer. This can
   establish a candidate for further consideration, never compatibility.
2. **Qualification experiment:** only after this policy is explicitly accepted,
   a separate owner authorization may permit a frozen, reviewed test-only
   boundary and a finite real-producer probe using disposable synthetic roots.
   Both released read and topology floor profiles remain mandatory. This is
   evidence gathering for #2, not an application adapter or user-facing feature.
3. **Consumer admission:** after independent review of exact consumer evidence,
   the owner may make a separate scoped decision in #2. Only that decision can
   open production adapter work under #4 and ADR-0007.

This clarification is proposed, not accepted policy. Current real invocation
remains blocked. Neither E0 approval, acceptance of this ADR, a generic test
approval, nor a producer TCK result independently authorizes implementation,
execution, package acquisition/provisioning or compatibility admission.

The proposed invocation shape is:

```text
/absolute/operator-venv/bin/python -I -B -m matryca_plumber.graph_gateway snapshot --graph-root <os.path.realpath(root)> --expect-descriptor-sha256 <h>
```

This command is a design datum only. Under current accepted Trama policy, it
is not executable before separate producer/capability admission. The proposed
qualification gate above would permit a narrowly authorized evidence-gathering
exception only after explicit policy acceptance and separate implementation and
execution approval; it does not open a production adapter. This draft and its
existing tests do not open or read a graph root.

The candidate producer profile specifies a 180-second execution deadline and
up to 5 seconds for finalization after the child terminates. Its output caps are
4 MiB stdout and 512 bytes stderr; a future consumer must enforce both
incrementally, before retaining bytes beyond either limit. These values are
proposed profile limits, not claims about the current test helper: its cleanup
polling and reaping timings are prototype mechanics, not that qualified
finalization contract. Exit code `4` means `source_rejected` and is
non-retryable. The exit code carries no copied or inferred producer payload.

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
| First proposed probe | Linux x86_64, CPython `3.12.14`, original public wheel | Not authorized or admitted; one synthetic consumer-boundary row only. |
| Wider producer evidence | CPython `3.12.14` and `3.13.15`, original wheel/sdist | External producer evidence only; not Trama qualification. |
| Producer platform | Linux x86_64; macOS arm64 | Candidate only; no platform support claim. |
| Parser | `1.9.0` | Producer environment only; no Trama dependency or direct Trama import. |
| Windows | Refusal only | No invocation or support claim. |
| Payload and native DB profiles | Excluded | No payload, database, or graph-content capability is proposed. |

Local fake-child tests and ordinary CI can exercise only consumer-side process
mechanics with synthetic bytes. They are not validation of public producer
bytes, producer/consumer compatibility, or Trama capability qualification.
Those are separate gates. Original alpha.3 publication and external producer
evidence can now be inspected, but policy acceptance, the consumer boundary,
its exact dependency/security disposition and real qualification remain blocked.

### Proposed owner-contract validation route

Consume the authenticated released Draft 2020-12 schemas as transient owner
resources, not copied normative files or reconstructed wire DTOs. A generic
schema validator must not substitute for the owner-defined profile composition,
graph/session/revision coherence, bounds, completeness and failure semantics;
the frozen consumer tests must check those bindings explicitly without copying
the owner's implementation or TCK logic.

The authenticated producer requirements pin `jsonschema==4.26.0`; this is a
candidate for a later test-only validator, not an admitted Trama dependency or
an instruction to import from the producer environment. Before implementation,
freeze the exact permitted validator, full transitive hash-locked profile,
licence/provenance and offline reference-resolution policy in the consumer's
own test environment. Do not fetch remote schema references, import Plumber or
Parser into Trama, or treat a producer-side TCK as a Trama consumer test.

No validation library, package, copied resource, workflow or test is introduced
by this clarification. The historical reverse bridge remains non-authorizing;
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

This draft authorizes no production code, dependency, adapter, configuration,
profile, schema, fixture/TCK, source access, network access, graph/content
read, host integration, capability claim, or release. Test-only fake-process
containment tests demonstrate only the behavior of their local synthetic child
boundary; they do not exercise a producer or establish compatibility.

The existing Trama consumer gate remains unchanged. In particular, graph
identity and topology remain blocked until their existing released-profile
prerequisites are met. Text-backed behavior separately requires its released
payload profile. No admission follows from this draft or its tests.

## Reversal and next decision

Withdraw or revise this proposal if an owner-published process contract,
operator security review, or Trama's existing architectural boundaries make
the proposed isolation unsuitable. Before a test-only qualification boundary
is implemented, explicitly accept or reject the proposed distinction above and
separately approve its exact scope and controls. Before production adapter
implementation, require the accepted decision, exact admitted capabilities and
the separate #4 gate. A real probe still requires its own frozen execution
authorization and security disposition; the M6-only exception does not carry
over. No acceptance here would alone admit a producer artifact, authorize a
user-facing capability or change ADR-0007's composition requirements.
