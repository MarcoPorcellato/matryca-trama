# ADR-0008: Experimental Process-Boundary Proposal

Status: Draft — not accepted; non-admitting

Date: 2026-10-23

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

## Decision (proposed)

If a later, separately authorized implementation is considered, it should use
one explicit operator-selected virtual environment and invoke only an exact,
reviewed producer entry point in a child process. The Trama side should not
import Parser or Plumber packages, load producer code in-process, or discover
the operator environment implicitly. Invocation inputs and outputs should be
opaque bounded bytes until an owner-published contract and a separate Trama
admission decision define their meaning.

The proposed invocation shape is:

```text
/absolute/operator-venv/bin/python -I -B -m matryca_plumber.graph_gateway snapshot --graph-root <os.path.realpath(root)> --expect-descriptor-sha256 <h>
```

This command is a design datum only. It is not executable or authorized until
the producer and capability pass separate admission. This proposal and its
tests do not open or read a graph root.

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
| Producer environment | CPython `3.12` or `3.13` | Candidate only; each exact environment still needs separate qualification. |
| Producer platform | Linux x86_64; macOS arm64 | Candidate only; no platform support claim. |
| Parser | `1.9.0` | Producer environment only; no Trama dependency or direct Trama import. |
| Windows | Refusal only | No invocation or support claim. |
| Payload and native DB profiles | Excluded | No payload, database, or graph-content capability is proposed. |

Local fake-child tests and ordinary CI can exercise only consumer-side process
mechanics with synthetic bytes. They are not validation of public producer
bytes, producer/consumer compatibility, or Trama capability qualification.
Those are separate gates and remain blocked pending exact published artifacts,
contract review, and independent admission evidence.

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
the proposed isolation unsuitable. Before implementation, replace this draft
with an accepted decision that names the exact owner contracts, admitted
capability, supported process interface, operator controls, failure semantics,
and separate qualification gates. Acceptance alone would still not admit a
producer artifact or authorize a user-facing capability.
