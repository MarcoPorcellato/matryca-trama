# Application Stack Qualification Protocol

> **Status:** qualified evidence exists for the bounded synthetic OG contract
> slice only. No user graph, DB host, or broader runtime is qualified.

## Purpose

This protocol qualifies the first Python implementation slice selected by
[ADR-0004](../decisions/ADR-0004-APPLICATION-STACK.md). It separates an
accepted architecture direction from an executable claim.

## Candidate boundary

The candidate uses Python 3.12+ and a `uv` workspace with only public,
reproducible dependencies. It may implement only:

1. `graph.identify`;
2. `page.read`;
3. `block.subtree.read.complete`.

The candidate starts with synthetic OG Markdown fixtures. It must not select a
Logseq DB host surface, create a DB adapter, access a user graph, write graph
content, start a watcher, create an index, or make an application/UI claim.

## Mandatory gates

| Gate | Required evidence | Failure disposition |
| --- | --- | --- |
| Public build | exact lockfile and clean environment reproduce install and tests without private sources | block runtime admission |
| Package direction | contracts, core, and bridges import only through declared public boundaries | block runtime admission |
| Contract conformance | synthetic vectors accept valid profiles and reject unknown version, missing provenance, wrong authority, incomplete subtree, and private dependency | block contract claim |
| Filesystem containment | fixture access remains inside an explicit temporary test root; path escape and symlink cases are rejected | block adapter claim |
| Determinism | identical fixture and request produce identical normalized result and digest | record mismatch; block deterministic claim |
| Read-only posture | static and executed tests prove no graph write, DB write, watcher, export, or derived-store authority path | block all read-only claims |
| Platform evidence | record exact operating system, architecture, Python, `uv`, command, and result for every run | unsupported outside recorded evidence |

## Measurement policy

Cold start, idle memory, and artifact size are diagnostic measurements only
after a runnable candidate exists. Their fixture, command, platform, and result
must be recorded. They never replace contract, containment, or read-only gates.

## Evidence record

Each qualification record must include:

- exact Trama commit and tree;
- Python and `uv` versions, operating system, architecture, and command;
- lockfile and public dependency identities;
- Parser, Plumber, and contract versions when a bridge participates;
- synthetic fixture identifier and SHA-256 digest;
- result digest, supported operations, and explicit rejected cases;
- raw pass/fail result and any unsupported condition.

Public evidence excludes local paths, user vault content, credentials, generated
DB files, private Brain source, and machine identifiers.

## Hosted contract gate

`.github/workflows/python-contracts.yml` is the fork-safe hosted gate for the
locked contract, containment, Plumber-consumer, and Foundation suites. Its
existence and local workflow-contract tests do not constitute hosted execution
or qualification evidence.

A hosted record may be added only after the workflow is terminal on its exact
commit. The record must use the sanitized template under
`docs/spikes/evidence/python-read-contract-v1/`; a missing, failed, cancelled,
or non-terminal run leaves this protocol's completion rule unmet.

## Completion rule

The first executable slice becomes qualified only when every mandatory gate
passes on an exact commit and the resulting evidence is reviewed. A failed or
unsupported gate remains a useful recorded outcome; it must not be relabeled as
support or bypassed by a fallback authority.

## Explicit non-goals

This protocol does not qualify a Logseq DB host, application UI, Nodi,
distribution artifact, performance target, write path, events, synchronization,
Shadow acceleration, export, or recovery behavior. Each needs a separate
decision and evidence protocol.

Network behavior is also unsupported by this qualification.
