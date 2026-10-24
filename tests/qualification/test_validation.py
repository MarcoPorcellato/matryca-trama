"""Consumer checks over illustrative synthetic documents, not copied owner TCKs."""

import copy
import unittest

from resources import QualificationFailure
from validation import owner_validate, snapshot_argv, validate_snapshot


class ValidationTests(unittest.TestCase):
    def test_schema_validation_is_real_and_remote_references_are_denied(self) -> None:
        owner_validate({"n": 1}, {"type": "object", "properties": {"n": {"type": "integer"}}})
        with self.assertRaises(QualificationFailure):
            owner_validate(
                {"n": "wrong"}, {"type": "object", "properties": {"n": {"type": "integer"}}}
            )
        with self.assertRaises(QualificationFailure):
            owner_validate({}, {"$ref": "https://example.invalid/must-not-fetch.json"})

    def example(self) -> tuple[dict, dict, dict]:
        common = {
            "graph_id": "graph",
            "source_revision": "revision",
            "session": {"id": "session", "state": "active"},
            "outcome": "pass",
        }
        golden = {
            "complete": True,
            "nodes": [],
            "edges": [],
            "provenance": {"source_revision": "revision"},
        }
        document = {
            "profile": "test-only",
            "descriptor_sha256": "a" * 64,
            "versions": {"plumber": "2.1.0a3", "parser": "1.9.0", "python": "3.12.14"},
            "read": {
                **copy.deepcopy(common),
                "operation": "graph.identify",
                "id": "r",
                "producer_profile_id": "rp",
                "consumer_profile_id": "rc",
                "result": {"graph_id": "graph"},
            },
            "topology": {
                **copy.deepcopy(common),
                "operation": "graph.topology.snapshot.complete",
                "id": "t",
                "producer_profile_id": "tp",
                "consumer_profile_id": "tc",
                "request": {"session_id": "session", "graph_id": "graph"},
                "result": copy.deepcopy(golden),
            },
        }
        descriptor = {
            "profile": "test-only",
            "wire": {
                "read": {"id": "r", "producer_profile_id": "rp", "consumer_profile_id": "rc"},
                "topology": {"id": "t", "producer_profile_id": "tp", "consumer_profile_id": "tc"},
            },
            "dependencies": {"parser": "1.9.0"},
            "bounds": {"max_nodes": 2, "max_edges": 2},
        }
        return document, descriptor, golden

    def check(self, document: dict, descriptor: dict, golden: dict) -> None:
        validate_snapshot(
            document,
            descriptor,
            "a" * 64,
            {"read": {"type": "object"}, "topology": {"type": "object"}},
            golden,
            {"plumber": "2.1.0a3", "parser": "1.9.0", "python": "3.12.14"},
            ["PRIVATE-CANARY"],
        )

    def test_coherent_complete_golden_is_accepted(self) -> None:
        self.check(*self.example())

    def test_incoherent_session_revision_and_graph_are_rejected(self) -> None:
        for field in ("graph_id", "source_revision", "session"):
            with self.subTest(field=field):
                document, descriptor, golden = self.example()
                document["topology"][field] = (
                    {"id": "other", "state": "active"} if field == "session" else "other"
                )
                with self.assertRaises(QualificationFailure):
                    self.check(document, descriptor, golden)

    def test_profile_version_incompleteness_and_canary_fail(self) -> None:
        for mode in ("descriptor", "python", "incomplete", "canary", "profile"):
            with self.subTest(mode=mode):
                document, descriptor, golden = self.example()
                if mode == "descriptor":
                    document["descriptor_sha256"] = "0" * 64
                elif mode == "python":
                    document["versions"]["python"] = "3.13.15"
                elif mode == "incomplete":
                    document["topology"]["result"]["complete"] = False
                elif mode == "canary":
                    document["read"]["reason"] = "PRIVATE-CANARY"
                else:
                    document["read"]["producer_profile_id"] = "other"
                with self.assertRaises(QualificationFailure):
                    self.check(document, descriptor, golden)

    def test_alias_is_canonicalized_in_actual_producer_argv(self) -> None:
        import os
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as root:
            graph = Path(root) / "graph"
            graph.mkdir()
            alias = Path(root) / "alias"
            alias.symlink_to(graph, target_is_directory=True)
            argv = snapshot_argv("/producer/bin/python", alias, "a" * 64)
            self.assertEqual(argv[argv.index("--graph-root") + 1], os.path.realpath(alias))
            self.assertNotEqual(str(alias), argv[argv.index("--graph-root") + 1])


if __name__ == "__main__":
    unittest.main()
