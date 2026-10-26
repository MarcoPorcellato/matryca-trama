# Maintainer-local synthetic diagnostic

Status: unsupported, non-qualifying maintainer tooling. This is not a product
adapter, user-graph route, supported macOS isolation interface or expanded
consumer admission. The existing hosted qualification entry and its guards are
unchanged. See [ADR-0009](../decisions/ADR-0009-SYNTHETIC-PLUMBER-CLIENT.md) and
the historical [ADR-0010 exploration](../decisions/ADR-0010-MACOS-SANDBOX-EXPLORATION.md).

## Exact scope

The separate `tests/maintainer_local/local_provision.py` and `run.py` entries
require local Darwin arm64 and CPython 3.12.14. They reject CI before task-root
access. Their only selector is `--root`: a fresh, private, canonical direct
child of `/private/tmp` named `trama-ma-…`. There is no graph, copy, optional
preflight, caller-supplied profile or alternate producer selector.

The producer is the original `matryca-plumber` 2.1.0a3 wheel from source
`8c30f70e217722e719c5aedc322219ebccb87e68`, SHA-256
`e5bc586a3da76d8e11760b39c9d7ac45b62b1240f085a8a96a573b9902bfea12`.
The authoritative pins remain in `tests/qualification/inputs.json`. The local
provisioner independently verifies the same release attestation policy, installs
only the wheel's hash-locked producer closure with Parser 1.9.0 into a new
disposable environment, and checks startup hooks before post-install interpreter
starts. It adds no Trama runtime or workspace dependency. A separately acquired
base interpreter must have its own source, license, identity and digest evidence;
matching the version does not prove that its bytes equal a hosted interpreter.

The existing trusted qualification builder exclusively creates the authenticated
synthetic fixture. Its sealed handle, Trama-owned process owner and strict
standard-library mapper remain unchanged. No graph directory is authenticated
by reading arbitrary contents or accepting a supplied digest.

## Native preflight and refusal

The installed compiler builds the repository's small native helper. It does not
load Python, Plumber or the producer's audit hook. For each write, out-of-grant
read, TCP4, TCP6, UDP, Unix-socket and DNS control, a successful unconfined
positive must precede the confined negative. Local listeners independently
observe connection/datagram controls. File markers independently detect writes.
DNS uses a fixed public synthetic lookup without retaining returned addresses.

The fixed experimental `sandbox-exec` profile denies networking, Mach service
lookups and writes except `/dev/null`. Reads are restricted to the fixture,
producer environment, verified base runtime, native helper and declared system
paths. The Apple interface remains deprecated and unsupported for product use.
A resolver failure without an explicit permission errno is **not** proof of a
DNS denial. An unavailable positive, successful confined operation, missing
denial or malformed result refuses the producer launch.

The process owner enforces incremental output bounds, deadlines and independent
reader/stream cleanup, direct-child reap and process-group ESRCH. EPERM is only
an observation, never cleanup success. The native listener cleanup attempts all
owned finalizers independently and retains uncertainty. The actual run has a
150-second shared deadline with cleanup reserve; provisioning commands retain
their existing 180-second bounds. Disk admission retains 20 decimal GB plus
1 GiB reserve and a 1 GiB task footprint ceiling.

## Invocation and evidence

After explicit owner authorization and verified isolated runtime preparation,
invoke both entries with that base interpreter, `-I -B`, and the same fresh task
root. Provisioning creates the root; the run rechecks its fixed evidence and
creates the fixture itself. Do not substitute a different Python, reuse a failed
task root, disable a control or supply any personal graph. No cleanup command is
part of this runbook.

The producer may launch only after all native controls prove denial. Its
topology must equal the authenticated golden result and map to the same bounded
Trama values. The fixture ledger must remain unchanged. A startup, provenance,
integrity or cleanup failure is a stop, not an implicit retry.

Private `artifacts/` retain each bounded child output, lifecycle record, native
control result and before/after fixture ledger, including failures. The public
summary contains only scope, exit class, node/edge counts, duration, cleanup
status and fixture status. It contains no local paths, names, identifiers,
environment or raw error text. Preserve the private task root before reboot if
it contains evidence not yet copied to durable storage.

CI executes only the offline unit tests in this directory. It must not run the
local provisioner, native campaign or actual producer through this entry. A local
PASS is diagnostic evidence for this exact synthetic tuple, not a release,
OS-level isolation guarantee, real-graph permission or new compatibility claim.
