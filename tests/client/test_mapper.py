"""Illustrative consumer cases; no copied owner schemas, fixtures or TCKs."""

import copy
import importlib
import importlib.util
import json
import unittest

from trama_core.graph_values import GraphGatewayError, GraphGatewayErrorCode


DESCRIPTOR = "bcc6ac607706e934e5df4e044802aa74c7d7455e7711220df116080f1ab0cc70"


def example():
    common = {
        "fixture_kind": "operation-result",
        "schema_version": 1,
        "graph_id": "graph-a",
        "source_revision": "revision-a",
        "outcome": "pass",
    }
    return {
        "profile": "plumber.og.operational/v1",
        "descriptor_sha256": DESCRIPTOR,
        "versions": {"plumber": "2.1.0a3", "parser": "1.9.0", "python": "3.12.14"},
        "read": {
            **common,
            "id": "read-1",
            "contract_id": "plumber.graph.read/v1",
            "producer_profile_id": "rp",
            "consumer_profile_id": "rc",
            "session": {"id": "session-a", "state": "active"},
            "operation": "graph.identify",
            "reason": "og-parser-identity",
            "result": {"graph_id": "graph-a"},
        },
        "topology": {
            **common,
            "id": "topology-1",
            "contract_id": "plumber.graph.topology/v1",
            "producer_profile_id": "tp",
            "consumer_profile_id": "tc",
            "session": {
                "contract_id": "plumber.graph.read/v1",
                "schema_version": 1,
                "id": "session-a",
                "state": "active",
            },
            "operation": "graph.topology.snapshot.complete",
            "reason": "og-parser-snapshot",
            "request": {"session_id": "session-a", "graph_id": "graph-a"},
            "result": {
                "topology_id": "topology-a",
                "complete": True,
                "nodes": [
                    {"id": "page", "kind": "page", "parent_id": None, "ordinal": 0},
                    {"id": "child", "kind": "block", "parent_id": "page", "ordinal": 0},
                    {
                        "id": "second",
                        "kind": "block",
                        "parent_id": "page",
                        "ordinal": 1,
                    },
                ],
                "edges": [
                    {"source_id": "child", "target_id": "second", "kind": "reference"}
                ],
                "provenance": {
                    "kind": "derived-structural",
                    "source_contract_id": "plumber.graph.read/v1",
                    "source_schema_version": 1,
                    "source_revision": "revision-a",
                },
            },
        },
    }


class MapperTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(
            importlib.util.find_spec("trama_plumber_client"),
            "The separately admitted Plumber client has not been implemented",
        )
        self.mapping = importlib.import_module("trama_plumber_client._mapping")

    def map(self, value):
        return self.mapping.snapshot_from_bytes(json.dumps(value).encode())

    def rejected(self, value, code=GraphGatewayErrorCode.CONTRACT_VIOLATION):
        with self.assertRaises(GraphGatewayError) as caught:
            self.map(value)
        self.assertEqual(caught.exception.code, code)
        self.assertFalse(caught.exception.retryable)

    def test_complete_coherent_document_maps_to_domain_values(self):
        result = self.map(example())
        self.assertEqual(result.identity.graph_id, "graph-a")
        self.assertEqual(result.identity.session_id, "session-a")
        self.assertEqual(result.identity.source_revision, "revision-a")
        self.assertEqual(
            [n.id for n in result.topology.nodes], ["page", "child", "second"]
        )
        self.assertEqual(result.topology.edges[0].target_id, "second")
        self.assertEqual(result.provenance.producer_version, "2.1.0a3")

    def test_unknown_fields_are_rejected_at_every_object_boundary(self):
        paths = [
            (),
            ("versions",),
            ("read",),
            ("read", "session"),
            ("read", "result"),
            ("topology",),
            ("topology", "session"),
            ("topology", "request"),
            ("topology", "result"),
            ("topology", "result", "provenance"),
            ("topology", "result", "nodes", 0),
            ("topology", "result", "edges", 0),
        ]
        for path in paths:
            value = example()
            target = value
            for key in path:
                target = target[key]
            target["unexpected"] = "not-permitted"
            with self.subTest(path=path):
                self.rejected(value)

    def test_missing_fields_and_boolean_schema_versions_are_rejected(self):
        for path in (
            ("read",),
            ("topology",),
            ("topology", "session"),
            ("topology", "result", "provenance"),
        ):
            value = example()
            target = value
            for key in path:
                target = target[key]
            key = (
                "source_schema_version"
                if path[-1] == "provenance"
                else "schema_version"
            )
            for replacement in (True, "1", 2):
                changed = copy.deepcopy(value)
                cursor = changed
                for part in path:
                    cursor = cursor[part]
                cursor[key] = replacement
                with self.subTest(path=path, replacement=replacement):
                    self.rejected(changed)
            del target[key]
            self.rejected(value)

    def test_foreign_profile_versions_and_operations_are_rejected(self):
        for path, replacement in (
            (("descriptor_sha256",), "0" * 64),
            (("profile",), "other"),
            (("versions", "parser"), "1.11.0"),
            (("versions", "python"), "3.13.15"),
            (("read", "producer_profile_id"), "foreign"),
            (("topology", "consumer_profile_id"), "foreign"),
            (("read", "operation"), "page.read"),
            (("topology", "result", "complete"), False),
            (("topology", "session", "state"), "closed"),
        ):
            value = example()
            cursor = value
            for key in path[:-1]:
                cursor = cursor[key]
            cursor[path[-1]] = replacement
            with self.subTest(path=path):
                self.rejected(value)

    def test_all_graph_session_and_revision_bindings_are_checked(self):
        for path in (
            ("topology", "graph_id"),
            ("read", "result", "graph_id"),
            ("topology", "request", "graph_id"),
            ("topology", "session", "id"),
            ("topology", "request", "session_id"),
            ("topology", "source_revision"),
            ("topology", "result", "provenance", "source_revision"),
        ):
            value = example()
            cursor = value
            for key in path[:-1]:
                cursor = cursor[key]
            cursor[path[-1]] = "foreign"
            with self.subTest(path=path):
                self.rejected(value)

    def test_duplicate_keys_non_finite_numbers_and_bad_utf8_are_rejected(self):
        for raw in (b'{"x":1,"x":2}', b'{"x":NaN}', b'{"x":Infinity}', b"\xff", b"[]"):
            with self.subTest(raw=raw), self.assertRaises(GraphGatewayError) as caught:
                self.mapping.snapshot_from_bytes(raw)
            self.assertEqual(
                caught.exception.code, GraphGatewayErrorCode.PROTOCOL_VIOLATION
            )

    def test_opaque_identifiers_and_untrusted_types_are_rejected(self):
        for identifier in ("", "space here", "x" * 129, "canary\nvalue", True):
            value = example()
            value["read"]["graph_id"] = identifier
            with self.subTest(identifier=identifier):
                self.rejected(value)

    def test_topology_invariants_fail_closed(self):
        value = example()
        value["topology"]["result"]["nodes"][2]["ordinal"] = 7
        self.rejected(value, GraphGatewayErrorCode.TOPOLOGY_INVARIANT_VIOLATION)

    def test_actual_profile_node_and_edge_bounds_are_not_schema_maxima(self):
        value = example()
        value["topology"]["result"]["nodes"] *= 342
        self.rejected(value)
        value = example()
        value["topology"]["result"]["edges"] *= 4097
        self.rejected(value)

    def test_each_known_producer_error_requires_its_exact_exit(self):
        for code, exitcode in (
            ("usage", 2),
            ("expectation_mismatch", 3),
            ("source_rejected", 4),
            ("bounds_exceeded", 5),
            ("source_changed", 6),
            ("unsupported_platform", 7),
            ("unsupported_dependency", 8),
            ("audit_hook_unavailable", 9),
            ("internal", 70),
        ):
            raw = json.dumps({"error": code}).encode()
            result = self.mapping.error_from_bytes(exitcode, b"", raw)
            self.assertEqual(result.code.value, code)
            self.assertFalse(result.retryable)
            with self.assertRaises(GraphGatewayError) as caught:
                self.mapping.error_from_bytes(99, b"", raw)
            self.assertEqual(
                caught.exception.code, GraphGatewayErrorCode.PROTOCOL_VIOLATION
            )

    def test_malformed_or_leaky_error_is_not_passed_to_domain(self):
        for stdout, stderr in (
            (b"partial", b'{"error":"source_rejected"}'),
            (b"", b'{"error":"private detail"}'),
            (b"", b'{"error":"source_rejected","detail":"canary"}'),
        ):
            with self.assertRaises(GraphGatewayError) as caught:
                self.mapping.error_from_bytes(4, stdout, stderr)
            self.assertEqual(str(caught.exception), "protocol_violation")


if __name__ == "__main__":
    unittest.main()
