"""Immutable, content-free graph values owned by Trama, not producer DTOs."""

from dataclasses import dataclass
from enum import StrEnum


class GraphGatewayErrorCode(StrEnum):
    CONFIGURATION_INVALID = "configuration_invalid"
    ADMISSION_SCOPE_VIOLATION = "admission_scope_violation"
    SPAWN_FAILED = "spawn_failed"
    PROCESS_TIMEOUT = "process_timeout"
    PROCESS_OUTPUT_LIMIT = "process_output_limit"
    CLEANUP_UNCERTAIN = "cleanup_uncertain"
    PROTOCOL_VIOLATION = "protocol_violation"
    CONTRACT_VIOLATION = "contract_violation"
    TOPOLOGY_INVARIANT_VIOLATION = "topology_invariant_violation"
    USAGE = "usage"
    EXPECTATION_MISMATCH = "expectation_mismatch"
    SOURCE_REJECTED = "source_rejected"
    BOUNDS_EXCEEDED = "bounds_exceeded"
    SOURCE_CHANGED = "source_changed"
    UNSUPPORTED_DEPENDENCY = "unsupported_dependency"
    UNSUPPORTED_PLATFORM = "unsupported_platform"
    AUDIT_HOOK_UNAVAILABLE = "audit_hook_unavailable"
    INTERNAL = "internal"


class GraphGatewayError(RuntimeError):
    """A sanitized terminal failure, never a recommendation to retry."""

    retryable = False

    def __init__(self, code: GraphGatewayErrorCode) -> None:
        if not isinstance(code, GraphGatewayErrorCode):
            raise ValueError("invalid gateway error code")
        self.code = code
        super().__init__(code.value)


class NodeKind(StrEnum):
    PAGE = "page"
    BLOCK = "block"


def _identifier(value: str) -> None:
    if type(value) is not str or not value:
        raise ValueError("a nonempty identifier is required")


@dataclass(frozen=True, slots=True)
class GraphIdentity:
    graph_id: str
    session_id: str
    source_revision: str

    def __post_init__(self) -> None:
        for value in (self.graph_id, self.session_id, self.source_revision):
            _identifier(value)


@dataclass(frozen=True, slots=True)
class TopologyNode:
    id: str
    kind: NodeKind
    parent_id: str | None
    ordinal: int

    def __post_init__(self) -> None:
        _identifier(self.id)
        if self.parent_id is not None:
            _identifier(self.parent_id)
        if not isinstance(self.kind, NodeKind):
            raise ValueError("invalid node kind")
        if type(self.ordinal) is not int or self.ordinal < 0:
            raise ValueError("invalid sibling ordinal")


@dataclass(frozen=True, slots=True)
class ReferenceEdge:
    source_id: str
    target_id: str

    def __post_init__(self) -> None:
        _identifier(self.source_id)
        _identifier(self.target_id)


@dataclass(frozen=True, slots=True)
class GraphTopology:
    id: str
    nodes: tuple[TopologyNode, ...]
    edges: tuple[ReferenceEdge, ...]

    def __post_init__(self) -> None:
        _identifier(self.id)
        if type(self.nodes) is not tuple or type(self.edges) is not tuple:
            raise ValueError("immutable topology collections are required")
        seen: set[str] = set()
        ancestors: list[str] = []
        ordinals: dict[str | None, int] = {}
        for node in self.nodes:
            if not isinstance(node, TopologyNode) or node.id in seen:
                raise ValueError("duplicate or invalid node")
            if (node.parent_id is None) != (node.kind == NodeKind.PAGE):
                raise ValueError("pages are roots and blocks require a parent")
            if node.parent_id is None:
                ancestors.clear()
            else:
                while ancestors and ancestors[-1] != node.parent_id:
                    ancestors.pop()
                if not ancestors:
                    raise ValueError("parent is absent or its subtree has ended")
            expected = ordinals.get(node.parent_id, 0)
            if node.ordinal != expected:
                raise ValueError("sibling ordinals must be contiguous")
            ordinals[node.parent_id] = expected + 1
            seen.add(node.id)
            ancestors.append(node.id)
        references: set[tuple[str, str]] = set()
        for edge in self.edges:
            if not isinstance(edge, ReferenceEdge):
                raise ValueError("invalid reference")
            pair = (edge.source_id, edge.target_id)
            if (
                edge.source_id not in seen
                or edge.target_id not in seen
                or pair in references
            ):
                raise ValueError("dangling or duplicate reference")
            references.add(pair)


@dataclass(frozen=True, slots=True)
class SnapshotProvenance:
    producer_version: str
    producer_source: str
    producer_artifact_sha256: str
    descriptor_sha256: str
    python_version: str

    def __post_init__(self) -> None:
        for value in (
            self.producer_version,
            self.producer_source,
            self.producer_artifact_sha256,
            self.descriptor_sha256,
            self.python_version,
        ):
            _identifier(value)


@dataclass(frozen=True, slots=True)
class GraphSnapshot:
    identity: GraphIdentity
    topology: GraphTopology
    provenance: SnapshotProvenance

    def __post_init__(self) -> None:
        if not (
            isinstance(self.identity, GraphIdentity)
            and isinstance(self.topology, GraphTopology)
            and isinstance(self.provenance, SnapshotProvenance)
        ):
            raise ValueError("validated immutable snapshot values are required")
