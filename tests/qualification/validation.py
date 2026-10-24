"""Test-only consumption of authenticated owner schemas and fixture results."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import NoReturn

from jsonschema import Draft202012Validator
from referencing import Registry
from referencing.exceptions import NoSuchResource
from resources import QualificationFailure, require


def owner_validate(value: object, schema: dict) -> None:
    def deny_retrieval(uri: str) -> NoReturn:
        raise NoSuchResource(ref=uri)

    try:
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema, registry=Registry(retrieve=deny_retrieval)).validate(value)
    except Exception as error:
        raise QualificationFailure(
            "owner schema validation failed: " + type(error).__name__
        ) from error


def snapshot_argv(
    interpreter: str, root: Path, descriptor_digest: str, *, canonicalize: bool = True
) -> list[str]:
    chosen = os.path.realpath(root) if canonicalize else str(root)
    return [
        interpreter,
        "-I",
        "-B",
        "-m",
        "matryca_plumber.graph_gateway",
        "snapshot",
        "--graph-root",
        chosen,
        "--expect-descriptor-sha256",
        descriptor_digest,
    ]


def validate_snapshot(
    document: dict,
    descriptor: dict,
    descriptor_digest: str,
    schemas: dict,
    golden: dict,
    versions: dict,
    canaries: list[str],
) -> None:
    require(
        set(document) == {"profile", "descriptor_sha256", "versions", "read", "topology"},
        "snapshot outer shape mismatch",
    )
    require(
        document["profile"] == descriptor["profile"]
        and document["descriptor_sha256"] == descriptor_digest,
        "snapshot profile/descriptor mismatch",
    )
    require(
        document["versions"] == versions
        and versions["parser"] == descriptor["dependencies"]["parser"],
        "snapshot version mismatch",
    )
    read, topology = document["read"], document["topology"]
    for key, envelope in (("read", read), ("topology", topology)):
        owner_validate(envelope, schemas[key])
        require(
            envelope["outcome"] == "pass" and envelope["session"]["state"] == "active",
            "inactive or failed result",
        )
        for field, expected in descriptor["wire"][key].items():
            require(envelope[field] == expected, "wire profile binding mismatch")
    require(
        read["operation"] == "graph.identify"
        and topology["operation"] == "graph.topology.snapshot.complete",
        "operation mismatch",
    )
    for field in ("graph_id", "source_revision"):
        require(read[field] == topology[field], "graph/revision mismatch")
    require(
        read["session"]["id"] == topology["session"]["id"] == topology["request"]["session_id"],
        "session mismatch",
    )
    require(
        read["graph_id"] == read["result"]["graph_id"] == topology["request"]["graph_id"],
        "identity binding mismatch",
    )
    result = topology["result"]
    require(result["complete"] is True, "incomplete topology")
    require(
        result["provenance"]["source_revision"] == topology["source_revision"],
        "provenance revision mismatch",
    )
    require(result == golden, "authenticated golden topology mismatch")
    require(
        len(result["nodes"]) <= descriptor["bounds"]["max_nodes"]
        and len(result["edges"]) <= descriptor["bounds"]["max_edges"],
        "topology bound mismatch",
    )
    encoded = json.dumps(document, ensure_ascii=False)
    require(all(canary not in encoded for canary in canaries), "privacy canary leaked")
