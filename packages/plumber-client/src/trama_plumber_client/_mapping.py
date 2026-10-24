"""Strict stdlib translation into Trama values; owner schemas stay authoritative."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Any, NoReturn, cast

from trama_core.graph_values import (
    GraphGatewayError,
    GraphGatewayErrorCode as Code,
    GraphIdentity,
    GraphSnapshot,
    GraphTopology,
    NodeKind,
    ReferenceEdge,
    SnapshotProvenance,
    TopologyNode,
)

from . import _profile as profile


def _fail(code: Code = Code.CONTRACT_VIOLATION) -> NoReturn:
    raise GraphGatewayError(code)


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate key")
        result[key] = value
    return result


def _nonfinite(value: str) -> NoReturn:
    raise ValueError("non-finite number")


def strict_document(raw: bytes, *, limit: int = profile.MAX_STDOUT) -> dict[str, Any]:
    try:
        if type(raw) is not bytes or not 0 < len(raw) <= limit:
            raise ValueError("invalid byte envelope")
        value = json.loads(
            raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_nonfinite
        )
        if type(value) is not dict:
            raise ValueError("object required")
        return cast(dict[str, Any], value)
    except (ValueError, RecursionError):
        raise GraphGatewayError(Code.PROTOCOL_VIOLATION) from None


def _object(value: Any, keys: str) -> dict[str, Any]:
    if type(value) is not dict or set(value) != set(keys.split()):
        _fail()
    return cast(dict[str, Any], value)


def _equal(value: Any, expected: Any) -> None:
    if type(value) is not type(expected) or value != expected:
        _fail()


def _opaque(value: Any) -> str:
    if type(value) is not str or not 1 <= len(value) <= 128:
        _fail()
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:-]*", value) is None:
        _fail()
    return value


def describe_from_bytes(raw: bytes) -> None:
    document = _object(strict_document(raw), "descriptor descriptor_sha256")
    _equal(document["descriptor_sha256"], profile.DESCRIPTOR_SHA256)
    try:
        canonical = json.dumps(
            document["descriptor"],
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    except (ValueError, UnicodeError, RecursionError):
        raise GraphGatewayError(Code.PROTOCOL_VIOLATION) from None
    _equal(hashlib.sha256(canonical).hexdigest(), profile.DESCRIBE_CANONICAL_SHA256)


def _envelope(value: Any, *, topology: bool) -> dict[str, Any]:
    keys = (
        "fixture_kind id contract_id schema_version producer_profile_id "
        "consumer_profile_id graph_id session source_revision operation outcome reason result"
    )
    value = _object(value, keys + (" request" if topology else ""))
    expected = {
        "fixture_kind": "operation-result",
        "schema_version": 1,
        "outcome": "pass",
        "id": "topology-1" if topology else "read-1",
        "contract_id": profile.TOPOLOGY_CONTRACT if topology else profile.READ_CONTRACT,
        "producer_profile_id": "tp" if topology else "rp",
        "consumer_profile_id": "tc" if topology else "rc",
        "operation": "graph.topology.snapshot.complete"
        if topology
        else "graph.identify",
        "reason": "og-parser-snapshot" if topology else "og-parser-identity",
    }
    for key, literal in expected.items():
        _equal(value[key], literal)
    for key in ("graph_id", "source_revision"):
        _opaque(value[key])
    session = _object(
        value["session"],
        "id state" + (" contract_id schema_version" if topology else ""),
    )
    _opaque(session["id"])
    _equal(session["state"], "active")
    if topology:
        _equal(session["contract_id"], profile.READ_CONTRACT)
        _equal(session["schema_version"], 1)
    return cast(dict[str, Any], value)


def snapshot_from_bytes(raw: bytes) -> GraphSnapshot:
    document = _object(
        strict_document(raw), "profile descriptor_sha256 versions read topology"
    )
    _equal(document["profile"], profile.PROFILE)
    _equal(document["descriptor_sha256"], profile.DESCRIPTOR_SHA256)
    versions = _object(document["versions"], "plumber parser python")
    for key, expected in profile.VERSIONS.items():
        _equal(versions[key], expected)
    read = _envelope(document["read"], topology=False)
    topology = _envelope(document["topology"], topology=True)
    identity = _object(read["result"], "graph_id")
    request = _object(topology["request"], "graph_id session_id")
    for value in (identity["graph_id"], request["graph_id"], topology["graph_id"]):
        _equal(value, read["graph_id"])
    for value in (topology["session"]["id"], request["session_id"]):
        _equal(value, read["session"]["id"])
    _equal(topology["source_revision"], read["source_revision"])
    result = _object(topology["result"], "topology_id complete nodes edges provenance")
    _equal(result["complete"], True)
    topology_id = _opaque(result["topology_id"])
    provenance = _object(
        result["provenance"],
        "kind source_contract_id source_schema_version source_revision",
    )
    _equal(provenance["kind"], "derived-structural")
    _equal(provenance["source_contract_id"], profile.READ_CONTRACT)
    _equal(provenance["source_schema_version"], 1)
    _equal(provenance["source_revision"], read["source_revision"])
    if type(result["nodes"]) is not list or len(result["nodes"]) > profile.MAX_NODES:
        _fail()
    if type(result["edges"]) is not list or len(result["edges"]) > profile.MAX_EDGES:
        _fail()
    nodes: list[TopologyNode] = []
    for value in result["nodes"]:
        node = _object(value, "id kind parent_id ordinal")
        identifier = _opaque(node["id"])
        parent = _opaque(node["parent_id"]) if node["parent_id"] is not None else None
        if type(node["kind"]) is not str or node["kind"] not in ("page", "block"):
            _fail()
        if type(node["ordinal"]) is not int or node["ordinal"] < 0:
            _fail()
        nodes.append(
            TopologyNode(identifier, NodeKind(node["kind"]), parent, node["ordinal"])
        )
    edges: list[ReferenceEdge] = []
    for value in result["edges"]:
        edge = _object(value, "source_id target_id kind")
        _equal(edge["kind"], "reference")
        edges.append(
            ReferenceEdge(_opaque(edge["source_id"]), _opaque(edge["target_id"]))
        )
    try:
        graph_topology = GraphTopology(topology_id, tuple(nodes), tuple(edges))
    except ValueError:
        raise GraphGatewayError(Code.TOPOLOGY_INVARIANT_VIOLATION) from None
    return GraphSnapshot(
        GraphIdentity(read["graph_id"], read["session"]["id"], read["source_revision"]),
        graph_topology,
        SnapshotProvenance(
            profile.VERSIONS["plumber"],
            profile.SOURCE,
            profile.WHEEL_SHA256,
            profile.DESCRIPTOR_SHA256,
            profile.VERSIONS["python"],
        ),
    )


def error_from_bytes(exitcode: int, stdout: bytes, stderr: bytes) -> GraphGatewayError:
    if type(exitcode) is not int or stdout:
        _fail(Code.PROTOCOL_VIOLATION)
    document = strict_document(stderr, limit=profile.MAX_STDERR)
    if set(document) != {"error"} or type(document["error"]) is not str:
        _fail(Code.PROTOCOL_VIOLATION)
    name = document["error"]
    if name not in profile.ERROR_EXITS or exitcode != profile.ERROR_EXITS[name]:
        _fail(Code.PROTOCOL_VIOLATION)
    return GraphGatewayError(Code(name))
