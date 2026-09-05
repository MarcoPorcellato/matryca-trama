# Architecture Validator Evidence

Status: durable provenance record for R1

Date: 2026-09-05

## Scope and boundary

This record concerns only repository-owned standard-library architecture
validator and controlled fixtures. It does not qualify runtime, host, user
graph, DB source, write, event, Shadow, synchronization, export, recovery,
network, Nodi, Brain, Pro, entitlement, pricing, commercial right, release, or
hosted/main result. Active registry remains zero exceptions.

## Bootstrap provenance deviation

Only known initial validator RED is aggregate missing-module result:

```text
$ rtk run 'python3 -m unittest tests.architecture.test_dependency_boundaries -v'
ModuleNotFoundError: No module named 'scripts.validate_architecture'
Ran 1 test in 0.000s
FAILED (errors=1)
```

Initial fixture tests and validator implementation entered together. No
historical record proves each original negative fixture was independently
observed RED before corresponding behavior. Controller accepted this as one-time
bootstrap provenance deviation, not strict-TDD evidence. It does not waive
focused RED-before-GREEN requirement for future validator changes.

## Review-driven fixes

Two subsequent review-driven fixture rounds observed focused RED then GREEN:

```text
$ rtk run 'python3 -m unittest tests.architecture.test_dependency_boundaries -v'
Ran 16 tests in 0.163s
FAILED (failures=9)

$ rtk run 'python3 -m unittest tests.architecture.test_dependency_boundaries -v'
Ran 16 tests in 0.165s
OK

$ rtk run 'python3 -m unittest tests.architecture.test_dependency_boundaries -v'
Ran 16 tests in 0.186s
FAILED (failures=5)

$ rtk run 'python3 -m unittest tests.architecture.test_dependency_boundaries -v'
Ran 16 tests in 0.195s
OK
```

First round covered import/path bypasses and exception scope. Second covered
exact exception paths. These records do not repair absent historical
per-fixture bootstrap evidence.

## Final R1 review fix wave

Before production checker changes, seven controlled fixtures produced expected
RED for manifest-only forbidden local and external dependencies, manifestless
package source tree, direct `builtins.__import__`, late `importlib` alias,
`del sys.path[0]`, and invalid issue URL:

```text
$ rtk uv run --all-packages python -m unittest tests.architecture.test_dependency_boundaries -v
Ran 23 tests in 0.183s
FAILED (failures=7)
```

After minimal standard-library checker change, same focused command was GREEN:

```text
$ rtk uv run --all-packages python -m unittest tests.architecture.test_dependency_boundaries -v
Ran 23 tests in 0.201s
OK
```

First focused `uv` attempt was blocked before test execution by sandbox access
to default user cache; same offline command was repeated with approved access
to existing cache. That access limitation is not test result.
