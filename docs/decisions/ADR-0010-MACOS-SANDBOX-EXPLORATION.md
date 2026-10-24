# ADR-0010: Synthetic macOS sandbox exploration

- Status: Draft; one exploratory measurement authorized, not an admission.
- Scope: the exact admitted original alpha.3 synthetic producer tuple only.
- Dependencies: [ADR-0008](ADR-0008-EXPERIMENTAL-PROCESS-BOUNDARY.md) and [ADR-0009](ADR-0009-SYNTHETIC-PLUMBER-CLIENT.md).

## Context

The synthetic-only client does not provide OS network or write isolation.
A separate experiment asks whether a candidate custom sandbox can reject
specific operations while the exact original alpha.3 producer still returns
its authenticated synthetic topology.

Apple DTS states that custom SBPL is undocumented and unsupported for third-party
use; the related API is deprecated. A working measurement cannot establish
a supported product integration. [Apple DTS](https://developer.apple.com/forums/thread/777509).
The hosted image is also mutable; record its actual identity.
[GitHub runner documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job).

## Decision

Use one manually dispatched, non-required `macos-15` job with an exact reviewed
source input. No matrix, retry, replacement tool or automatic trigger is added.
Run attempt 1 only. Keep all existing required CI and cleanup thresholds unchanged.

Authenticate the original wheel and exact hash-locked closure using the existing
provisioner. The producer remains commit
`8c30f70e217722e719c5aedc322219ebccb87e68`, wheel SHA-256
`e5bc586a3da76d8e11760b39c9d7ac45b62b1240f085a8a96a573b9902bfea12`,
Parser 1.9.0 and CPython 3.12.14. Inspect startup hooks before the producer starts.
Create the graph only through the trusted synthetic fixture builder; never
accept a user graph, arbitrary path-plus-digest or client bypass.

The candidate profile allows ordinary execution and reads, denies network and
file-write operations, and permits only null-device output as an explicit write
exception. It is not arbitrary-read isolation or hostile-code containment.

Compile a tiny reviewed native canary using the existing hosted compiler.
It imports no producer or Python and installs no audit hook. Prove an owned
marker write and literal loopback connection succeed without confinement.
Then use the same marker, reachable listener and native helper under the profile.
An observed denial requires EPERM/EACCES for both operations, unchanged marker
evidence and no accepted connection. A forbidden success is OBSERVED_ALLOW.
Missing tools, profile rejection, unrelated errors or failed controls are
INCONCLUSIVE, not denial evidence. No DNS, remote endpoint, protected path,
tool installation or local sandbox execution is included.

Launch the actual original producer once under that same profile on the
authenticated synthetic fixture. Canonicalize the alias, then validate the
joint read/topology result against the authenticated owner schemas and golden
data. Keep this result separate from OS-canary results. Retain launcher-or-child
stderr without assuming which component wrote it; any nonempty stderr makes
the producer result inconclusive rather than relaxing its empty-stderr contract.

The existing shared bounded reader is the sole process owner. Preserve its
deadlines, output limits, reap plus deadline-bound ESRCH, reader/stream gates and
EPERM observation retention. Uncertain cleanup or integrity failure stops the
experiment, never becoming an expected sandbox refusal.

## Evidence and consequences

Retain bounded sanitized stdout/stderr, original output digests, every lifecycle
record, source/profile/helper digests, actual runtime/image identifiers and the
before/after fixture ledger. Do not publish runner paths, usernames, environment
values, credentials or wheel contents. Record only the selected non-sensitive
image identifiers, not a general environment dump.

OBSERVED_DENY and a valid producer result remain exploratory, not qualification.
Packaged proposed/static-only-unqualified/unqualified/planned labels remain
unchanged. No user graph, broader admission, payload, DB, release or stable
support claim follows. Keep source branches and all successful/failed evidence.

## Alternatives and reversal

Entitlement-based App Sandbox is a different model and is not implemented.
Virtualization, a replacement sandbox and an application containment policy
require separate design and authority. If the one attempt is inconclusive or
fails, preserve it and stop; do not rerun until a separate owner decision.
The experiment can be removed later without changing the admitted client or
immutable producer.
