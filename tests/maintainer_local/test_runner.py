"""Offline privacy and preflight-to-launch boundary controls."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent


class LocalRunnerTests(unittest.TestCase):
    def setUp(self):
        source = HERE / "run.py"
        self.assertTrue(source.is_file(), "MA local synthetic runner is absent")
        spec = importlib.util.spec_from_file_location("ma_runner", source)
        if spec is None or spec.loader is None:
            self.fail("MA runner source unavailable")
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    def test_report_is_fixed_shape_without_private_error_data(self):
        state = {
            "exit_class": "preflight_refused",
            "nodes": 0,
            "edges": 0,
            "cleanup_succeeded": True,
            "fixture_unchanged": False,
            "error_detail": "/synthetic-private-user/notes",
            "graph_id": "private-id",
            "source_revision": "private-digest",
        }
        report = self.module.public_report(state, 0.5)
        self.assertEqual(
            set(report),
            {
                "scope",
                "exit_class",
                "nodes",
                "edges",
                "duration_seconds",
                "cleanup_succeeded",
                "fixture_unchanged",
            },
        )
        encoded = json.dumps(report)
        for forbidden in ("synthetic-private-user", "private-id", "private-digest"):
            self.assertNotIn(forbidden, encoded)
        for field, value in (("nodes", True), ("exit_class", "private-id")):
            with self.assertRaises(RuntimeError):
                self.module.public_report({**state, field: value}, 0.5)
        with self.assertRaises(RuntimeError):
            self.module.public_report(state, float("nan"))

    def test_failed_preflight_blocks_producer_even_for_a_valid_fixture(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            graph = root / "synthetic"
            graph.mkdir()
            alias = root / "alias"
            alias.symlink_to(graph, target_is_directory=True)
            fixture = self.module.fixture_module._created_fixture(str(root), str(graph), str(alias))
            state: dict[str, object] = {}
            with (
                patch.object(
                    self.module.preflight,
                    "run_preflight",
                    side_effect=self.module.preflight.PreflightRefused("unavailable control"),
                ),
                patch.object(
                    self.module.preflight, "execute", side_effect=AssertionError("producer started")
                ),
                self.assertRaises(self.module.preflight.PreflightRefused),
            ):
                self.module.contained_snapshot(root, fixture, state, deadline=1.0)
            self.assertFalse(state.get("producer_attempted", False))


if __name__ == "__main__":
    unittest.main()
