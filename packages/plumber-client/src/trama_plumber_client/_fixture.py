"""Opaque qualification-fixture capability; not a public arbitrary-root API.

Only the trusted qualification builder issues this capability after exclusive
creation. It is an API scope guard, not isolation from malicious Python code in
the consumer process. Admission checks use metadata, never graph file contents.
"""

from dataclasses import dataclass
import os
import stat

from trama_core.graph_values import GraphGatewayError, GraphGatewayErrorCode as Code

_BUILDER_SEAL = object()


@dataclass(frozen=True, slots=True, init=False)
class SyntheticFixture:
    task_root: str
    canonical_root: str
    input_alias: str
    root_identity: tuple[int, int]
    task_identity: tuple[int, int]
    _seal: object

    def __init__(self) -> None:
        raise TypeError("only the qualification fixture builder can issue a handle")


def _directory_identity(path: str) -> tuple[int, int]:
    status = os.lstat(path)
    if not stat.S_ISDIR(status.st_mode) or status.st_uid != os.getuid():
        raise ValueError("fixture directory identity rejected")
    return status.st_dev, status.st_ino


def _created_fixture(
    task_root: str, canonical_root: str, input_alias: str
) -> SyntheticFixture:
    """Private builder handoff after fresh creation, never a path admission API."""
    fixture = object.__new__(SyntheticFixture)
    for key, value in (
        ("task_root", task_root),
        ("canonical_root", canonical_root),
        ("input_alias", input_alias),
        ("root_identity", _directory_identity(canonical_root)),
        ("task_identity", _directory_identity(task_root)),
        ("_seal", _BUILDER_SEAL),
    ):
        object.__setattr__(fixture, key, value)
    fixture_root(fixture)
    return fixture


def fixture_root(fixture: SyntheticFixture) -> str:
    """Reject a foreign, replaced or escaping root before content access/launch."""
    try:
        if type(fixture) is not SyntheticFixture or fixture._seal is not _BUILDER_SEAL:
            raise ValueError("invalid fixture capability")
        task, root, alias = (
            fixture.task_root,
            fixture.canonical_root,
            fixture.input_alias,
        )
        if any(
            type(value) is not str or not os.path.isabs(value)
            for value in (task, root, alias)
        ):
            raise ValueError("absolute fixture paths required")
        if (
            root == task
            or os.path.realpath(task) != task
            or os.path.realpath(root) != root
            or os.path.commonpath((task, root)) != task
            or os.path.commonpath((task, os.path.abspath(alias))) != task
            or os.path.realpath(alias) != root
            or _directory_identity(task) != fixture.task_identity
            or _directory_identity(root) != fixture.root_identity
        ):
            raise ValueError("fixture structure changed")
        return root
    except (OSError, ValueError, AttributeError, TypeError):
        raise GraphGatewayError(Code.ADMISSION_SCOPE_VIOLATION) from None
