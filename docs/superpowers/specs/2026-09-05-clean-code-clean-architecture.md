# Clean Code and Clean Architecture Enforcement

Status: Accepted for repository-local R1 implementation

Date: 2026-09-05

Live planning anchor: `9905e8a36acb83a17a33b702a5fa620d6bfed185`

Related issue: [#9](https://github.com/MarcoPorcellato/matryca-trama/issues/9)

## Purpose

Matryca Trama must remain understandable and safely changeable as the Community
application grows. Architecture rules therefore need three aligned forms:

1. human-readable policy that explains intent;
2. deterministic checks that reject mechanical boundary violations; and
3. a repository-local agent skill that routes work through the policy and
   checks without copying either.

This decision applies to the current Python workspace and defines how future
packages enter it. It does not authorize new product capabilities.

## Decision

Use a repository-owned Python standard-library validator, configured by a
machine-readable dependency map, to enforce package boundaries and packaging
metadata. Add focused `unittest` fixtures that prove forbidden edges fail and
allowed edges pass. Run the validator in fork-safe CI before behavioral contract
tests.

No third-party architecture linter is required for R1. A later ADR may add one
when it provides a demonstrated benefit that the repository-owned checks cannot
provide.

Clean Architecture rules that can be decided mechanically fail closed. Clean
Code guidance that requires judgment remains in review documentation and the
repository skill. R1 does not invent numeric complexity, file-length, coverage,
or style thresholds without evidence that they protect a real maintenance risk.

## Sources of authority

Authority is ordered as follows:

1. accepted ADRs and public contracts;
2. this accepted design and the architecture standard it creates;
3. executable configuration and checks as projections of that policy;
4. contributor and pull-request guidance;
5. the repository-local skill as workflow routing.

The skill and checker never become independent policy sources. If prose and an
executable projection disagree, work stops until the policy and projection are
reviewed together.

The proposed cross-repository responsibility contract informs coordination but
does not become accepted merely because R1 references it. Until that proposal is
accepted, R1 enforces only rules already supported by accepted Trama decisions,
public contracts, and current package ownership.

## Layer and dependency rules

Dependencies point inward. A package may import its own modules, Python standard
library modules, and only the internal or external roots listed below.

| Package | May import | Must not import |
|---|---|---|
| `trama-contracts` | Python standard library | Every other Trama package; Parser, Plumber, Brain, Pro, or host SDKs |
| `trama-core` | Python standard library; `trama-contracts` when needed | adapters, bridges, apps, Nodi, Parser, Plumber, Brain, Pro, or host SDKs |
| `trama-parser-bridge` | Python standard library; core; contracts; documented Parser package-root API | Parser internals; adapters; Plumber; Brain; Pro; apps; Nodi |
| `trama-logseq-og-adapter` | Python standard library; contracts; core; parser bridge | direct Parser imports after R1 migration; DB or Shadow implementations; Plumber; Brain; Pro; apps; Nodi; network clients |
| `trama-plumber-bridge` | Python standard library; contracts; core when needed | Plumber implementation imports; Parser; host adapters; Brain; Pro; apps; Nodi |

Future packages are not required until they exist. When admitted:

- a DB adapter may depend on contracts, core, and its separately selected
  official-host port; it never opens Logseq internal SQLite directly and never
  falls back to OG Markdown;
- Nodi may depend on contracts, core, and use-case ports, never concrete
  adapters, bridges, host SDKs, network clients, Brain, or Pro;
- apps compose public providers and use cases; business and domain logic do not
  live in apps.

## Cross-repository rules

Parser owns parsing, its public intermediate representation, source locations,
diagnostics, and documented package-root API. Trama owns the
`trama.logseq.read/v1` envelope, Logseq adapters, provenance, Nodi, and
application composition. Plumber owns its downstream mapping, orchestration,
and consumer evidence.

Cross-repository use requires a released public dependency or an exact
source-bound contract profile. The following fail closed:

- sibling-repository path injection;
- imports from private or internal modules;
- copied wire DTOs or copied owner semantics;
- generated bindings without their canonical schema identity;
- undeclared local or external dependencies;
- dynamic imports used to bypass dependency checks.

## Source authority and product boundaries

Logseq OG Markdown remains authoritative for OG workflows. The native Logseq DB
store remains authoritative for DB workflows. Derived data, exports, caches, or
Shadow state never silently replace either source.

R1 adds no DB access, writes, events, Shadow, synchronization, export, recovery,
network behavior, UI, Nodi runtime, Brain connection, Pro source, entitlement,
pricing, or commercial right.

Repository-owned Community material remains under PolyForm Noncommercial 1.0.0.
Commercial use requires a separate written agreement. External
copyright-bearing contributions remain merge-blocked until a lawyer-reviewed
contributor agreement or equivalent grant exists.

## Executable architecture projection

Root `architecture.toml` records:

- package directory, distribution name, and import root;
- allowed internal import roots;
- allowed exact external imports and their distribution names;
- forbidden private or product import roots;
- approved exceptions, if any.

`scripts/validate_architecture.py` parses package `pyproject.toml` files and
Python ASTs under `packages/*/src`. It reports source path and line for every
violation and exits nonzero when it finds:

- an unregistered package;
- a manifestless `packages/*/src` package tree;
- a declared local or external dependency that is not allowed by the package
  map, before source ASTs are scanned;
- a forbidden dependency direction;
- an undeclared internal or external dependency;
- a private or product-boundary import;
- a non-package-root Parser import;
- direct Parser use outside the parser bridge;
- direct or aliased `builtins.__import__`, `importlib.import_module`, or
  `sys.path` mutation, including deletion, in production packages; aliases are
  collected independently of source order;
- malformed, expired, or over-broad architecture exceptions.

The validator does not infer architectural intent from directory names alone.
Its configuration must match each present package and each package manifest.

## Package metadata

Every imported workspace distribution must be declared in the importing
package's `dependencies`. External imports need an explicit distribution map.
The root `uv` workspace binds local distributions through workspace sources.

R1 repairs current hidden defects:

- parser bridge declares `trama-core`;
- OG adapter declares contracts, core, and parser bridge;
- Plumber bridge declares contracts;
- OG adapter consumes Parser types through parser bridge;
- producer identity matches package distribution version.

Workspace-wide installation is not evidence that packages are independently
well-described. Build checks and manifest validation remain separate evidence.

## Exception policy

Initial R1 state has zero exceptions. An exception is permitted only when a
maintainer accepts a concrete, temporary incompatibility that cannot be removed
in the same change.

Each exception must include:

- unique identifier;
- exact importing package and imported root;
- narrow path glob when the whole package is not affected;
- public issue URL;
- owner;
- reason;
- creation date;
- expiry date;
- removal condition.

The validator rejects missing fields, duplicate identifiers, expired entries,
wildcard package/import roots, and entries that match no live violation. The
issue URL must be an exact public
`https://github.com/MarcoPorcellato/matryca-trama/issues/<positive-number>` URL;
this deterministic offline rule does not fetch GitHub.
Licensing, external-contribution rights, private Brain or Pro source, native
source authority, write permission, secrets, and publication gates can never be
waived through this registry.

## Clean Code review contract

Deterministic tools enforce formatting already selected by the repository,
dependency declarations, import boundaries, contract behavior, and reproducible
tests. Reviewers and agents additionally check that:

- names express domain intent;
- each module has one coherent responsibility;
- public behavior is represented by focused tests;
- expected test values are independently derived;
- adapters translate at boundaries instead of leaking host types inward;
- errors preserve explicit unsupported outcomes instead of guessing;
- comments explain constraints or decisions, not obvious syntax;
- refactoring does not widen product, data, write, or licensing scope.

These are review questions, not pretend objective metrics.

## Test strategy

Architecture behavior follows RED-GREEN-REFACTOR:

1. controlled fixture repositories introduce one forbidden edge;
2. the new test is observed failing for that edge;
3. the smallest validator behavior makes it pass;
4. an allowed-edge fixture guards against over-rejection;
5. current packages are scanned as an integration test.

Future validator changes must retain this focused RED requirement. Historical
bootstrap provenance is narrower: an aggregate missing-module RED was observed,
but the original per-fixture RED sequence was not recorded because the initial
tests and validator entered together. A one-time controller ruling accepts that
deviation without retroactively claiming strict TDD; review-driven and final
fix waves have focused RED/GREEN evidence in
[`docs/quality/ARCHITECTURE_VALIDATOR_EVIDENCE.md`](../../quality/ARCHITECTURE_VALIDATOR_EVIDENCE.md).

Required negative cases cover contracts importing core, core importing an
adapter, OG adapter importing Parser directly, undeclared workspace dependency,
Parser internal import, dynamic import, sibling-path mutation, private
Brain/Pro import, malformed exception, expired exception, and unused exception.

Behavioral contract and containment suites remain independent. Architecture
success does not qualify a runtime, host, user graph, cross-repository version,
or release.

## Repository-local skill

`.agents/skills/trama-development/SKILL.md` is the single versioned agent
entrypoint for implementation and review in this repository. It stays concise
and routes agents to this design, `docs/standards/CLEAN_ARCHITECTURE.md`, relevant
contracts and ADRs, and exact validation commands.

The skill must be behavior-tested without and with the skill. Tests use pressure
scenarios involving deadlines, sunk cost, and maintainer pressure to bypass
Parser/adapter ownership, TDD, or licensing gates. The skill is accepted only
when an independent agent preserves the boundary and identifies the correct
checks and stop conditions.

A personal/global discovery skill may only point to this repository-local
authority. It must not copy policy text. Creating or modifying a skill outside
this repository requires separate filesystem and publication authorization and
is not part of the repository-local R1 commit.

## CI and review

The fork-safe `python-contracts` workflow runs architecture validation before
contract suites. It keeps read-only permissions, full-SHA actions, bounded
timeout, no secrets, no deployment, and no artifact publication.

Pull requests record:

- affected packages and boundaries;
- architecture validator result;
- behavioral and contract tests;
- accepted exception identifiers or `none`;
- authority/source-mode impact;
- known limitations;
- contribution-rights eligibility.

## Adoption gates

R1 completes only when all are true:

1. design, ADR, standard, and executable map agree;
2. every future required negative fixture is observed failing before its
   corresponding validator behavior; the one-time bootstrap deviation is
   limited to the evidence record and does not waive later focused RED;
3. all architecture tests and existing suites pass;
4. current package manifests match real imports;
5. OG adapter no longer imports Parser directly;
6. skill baseline failure and post-skill compliance are recorded;
7. CI and contributor guidance require the new evidence;
8. the exact diff passes whitespace and foundation validation;
9. no exception is active unless explicitly reviewed;
10. no unsupported capability or commercial-right claim is introduced.

Push, pull request, merge, GitHub issue mutation, release, licence change, and
personal/global skill installation remain separate actions.
