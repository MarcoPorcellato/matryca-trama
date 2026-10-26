# Clean Architecture Standard

Status: Canonical policy for R1

Date: 2026-09-05

Authority: [ADR-0005](../decisions/ADR-0005-CLEAN-ARCHITECTURE-ENFORCEMENT.md),
[accepted R1 design](../superpowers/specs/2026-09-05-clean-code-clean-architecture.md),
and accepted public contracts. The executable map, validator, CI, contributor
guidance, and repository-local skill project this standard; none is an
independent policy source. Stop work if a projection disagrees with policy.

## Dependency rule

Dependencies point inward. A package may import its own modules, Python
standard-library modules, and only roots explicitly allowed below. Every
imported workspace distribution must appear in the importing package's
`dependencies`; external imports need explicit distribution map. Root `uv`
workspace sources bind local distributions.

| Package | May import | Must not import |
|---|---|---|
| `trama-contracts` | Python standard library | Every other Trama package; Parser, Plumber, Brain, Pro, host SDKs |
| `trama-core` | Python standard library; `trama-contracts` when needed | adapters, bridges, apps, Nodi, Parser, Plumber, Brain, Pro, host SDKs |
| `trama-parser-bridge` | Python standard library; core; contracts; documented Parser package-root API | Parser internals; adapters; Plumber; Brain; Pro; apps; Nodi |
| `trama-logseq-og-adapter` | Python standard library; contracts; core; parser bridge | direct Parser imports after R1 migration; DB or Shadow implementations; Plumber; Brain; Pro; apps; Nodi; network clients |
| `trama-plumber-bridge` | Python standard library; contracts; core when needed | Plumber implementation imports; Parser; host adapters; Brain; Pro; apps; Nodi |
| `trama-plumber-client` | Python standard library; core | contracts, historical bridges/adapters, Plumber or Parser implementation imports; host SDKs; Brain; Pro; network clients |

The separately approved M2 package `trama-plumber-client` is restricted to the
exact synthetic-only alpha.3 tuple in the [admission record](../contracts/PLUMBER_SOURCE_ADMISSION.md#current-owner-admission--2026-10-24).
It implements the Trama-owned `KnowledgeGraphGateway` port and maps bounded
owner wire results into immutable core values. It has no third-party runtime
dependency. Owner schemas remain authoritative and transient in qualification;
the strict standard-library runtime mapper is not a replacement schema.
The qualification builder alone issues the structural fixture handle before
content reads or producer launch. No arbitrary-root or bypass option is part
of the client interface. This API scope guard is not an OS sandbox or protection
against malicious code already executing inside the consumer process.

The read-only posture scanner permits the package's reviewed POSIX process and
metadata imports only beneath `packages/plumber-client/src/trama_plumber_client`.
That path-specific rule does not allow filesystem writes, `open`, network,
SQLite, dynamic imports or the same process authority in any other package.
The moved process helper retains its existing ownership, incremental output,
shared five-second finalization and reap-plus-ESRCH gates.

The current Parser bridge, OG adapter, and Plumber bridge are historical
experimental packages retained for their bounded synthetic evidence. Their
admissions do not authorize future extension. Future packages require separate
admission before they exist. A future Trama consumer may use an internal domain
port and a published Plumber public contract, but it must not add a Logseq DB or
OG source adapter, open internal SQLite, or fall back to OG Markdown. Nodi may
use contracts, core, and use-case ports, never concrete adapters, bridges, host
SDKs, network clients, Brain, or Pro. Apps compose public providers and use
cases; business and domain logic stay below apps.

Cross-repository use needs released public dependency or exact source-bound
contract profile. Reject sibling-repository path injection, private or internal
module imports, copied wire DTOs or owner semantics, schema-less generated
bindings, undeclared dependencies, and dynamic-import bypasses. Parser owns its
documented package-root API. Plumber owns the future `plumber.*` contract
families, source selection, the OG Parser adapter, any qualified official
DB-host adapter, and provenance normalization. Trama owns product mapping,
graph UI, intelligence, Nodi, and application composition over published
Plumber contracts. Historical `trama.logseq.read/v1` material is not future
authority.

## Source and product boundaries

### Admitted synthetic demo application

The owner-authorized `apps/synthetic_demo` composition is admitted by
[ADR-0011](../decisions/ADR-0011-SYNTHETIC-GRAPH-DEMO.md). It is not a workspace
distribution. Its fixture provider and presentation may use only standard
library, own modules and existing core graph values/port. It imports neither
Parser, Plumber nor a source client. Invented labels/categories are separate
presentation annotations, not payload or topology-profile admission.

Only `build.py` may read its fixed bundled assets and write the fixed generated
HTML below `build/synthetic-demo`, using no-follow descriptor access. Only
`preview.py` may expose a loopback HTTP listener serving generated bytes at
GET/HEAD `/`; it has no directory mapping, source selector or outbound client.
The browser uses only the exact admitted local renderer asset and fictional
data. `scripts/validate_synthetic_demo.py` supplements the package validator
with explicit app import/dynamic-import/path-escape checks and negative tests.
These narrow composition exceptions grant no package, real graph, producer,
OS-isolation, payload, DB, release or general network authority.

Logseq OG Markdown is authoritative for OG workflows. Native Logseq DB storage
is authoritative for DB workflows. Derived data, exports, caches, and Shadow
state never silently replace either source.

R1 adds no DB access, writes, events, Shadow, synchronization, export,
recovery, network behavior, UI, Nodi runtime, Brain connection, Pro source,
entitlement, pricing, or commercial right. Community material remains under
PolyForm Noncommercial 1.0.0. Commercial use needs separate written agreement.
External copyright-bearing contributions remain merge-blocked until
lawyer-reviewed contributor agreement or equivalent grant exists.

## Exceptions

Initial R1 state: zero active exceptions. A maintainer may accept only a
concrete, temporary incompatibility that cannot be removed in the same change.
Each exception must contain:

- unique identifier;
- exact importing package and imported root;
- narrow path glob when whole package is not affected;
- public issue URL;
- owner;
- reason;
- creation date;
- expiry date; and
- removal condition.

Reject missing fields, duplicate identifiers, expired entries, wildcard
package/import roots, over-broad entries, and entries matching no live
violation. Never waive licensing, external-contribution rights, private Brain
or Pro source, native source authority, write permission, secrets, or
publication gates.

## Clean Code review and tests

Use RED-GREEN-REFACTOR for architecture behavior: observe a focused forbidden
edge fail, add the smallest validator behavior, protect an allowed edge, then
scan current packages. Required negative cases cover contracts importing core,
core importing an adapter, direct Parser import in the OG adapter, an
undeclared workspace dependency, Parser internal import, dynamic import,
sibling-path mutation, private Brain/Pro import, malformed exception, expired
exception, and unused exception.

Reviewers and agents check domain-intent names, coherent module responsibility,
focused public-behavior tests, independently derived expected values, boundary
translation instead of host-type leakage, explicit unsupported outcomes,
decision-focused comments, and no widening of product, data, write, or
licensing scope. These are review questions, not invented numeric metrics.

## Validation and stop gates

For this policy-document change, run exactly:

```bash
python3 scripts/validate_foundation.py
git diff --check
```

Both must exit `0`. Later R1 executable-projection work must also run its
repository-owned standard-library architecture validator before behavioral
contract suites in fork-safe CI. That validator must reject unregistered
packages, forbidden directions, undeclared dependencies, private/product
imports, non-package-root Parser imports, direct Parser use outside parser
bridge, dynamic imports, `sys.path` mutation, and invalid exceptions.

Stop rather than guess when policy and projection disagree; a package or
dependency has no accepted admission; a required exception is absent or invalid;
a cross-repository contract is not released or source-bound; source authority
could change; or a proposed responsibility contract is presented as accepted.
Architecture success does not qualify a runtime, host, user graph,
cross-repository version, or release.
