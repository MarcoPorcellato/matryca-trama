"""Offline tests for exploratory classification; never run a native sandbox."""

import importlib.util
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent


class SandboxExplorationTests(unittest.TestCase):
    def setUp(self) -> None:
        source = HERE / "macos_sandbox.py"
        self.assertTrue(source.is_file(), "M3 exploration helpers are not implemented")
        spec = importlib.util.spec_from_file_location("m3_exploration", source)
        if spec is None or spec.loader is None:
            self.fail("Exploration module specification unavailable")
        self.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.module)

    @staticmethod
    def record(
        write: object, network: object, write_errno: int = 0, network_errno: int = 0
    ) -> dict:
        return {
            "write_succeeded": write,
            "network_succeeded": network,
            "write_errno": write_errno,
            "network_errno": network_errno,
        }

    def test_permission_denials_need_successful_independent_controls(self) -> None:
        allow = self.record(True, True)
        deny = self.record(False, False, 1, 13)
        self.assertEqual(
            self.module.classify_canaries(
                allow, deny, marker_unchanged=True, accepted_connections=0
            ),
            "OBSERVED_DENY",
        )
        self.assertEqual(
            self.module.classify_canaries(
                deny, deny, marker_unchanged=True, accepted_connections=0
            ),
            "INCONCLUSIVE",
        )

    def test_forbidden_success_is_observed_allow_not_an_admission(self) -> None:
        for actual in [self.record(True, False, 0, 1), self.record(False, True, 13, 0)]:
            self.assertEqual(
                self.module.classify_canaries(
                    self.record(True, True),
                    actual,
                    marker_unchanged=False,
                    accepted_connections=1,
                ),
                "OBSERVED_ALLOW",
            )

    def test_missing_evidence_unrelated_errno_and_changed_marker_are_inconclusive(
        self,
    ) -> None:
        for actual, unchanged, accepted in [
            ({}, True, 0),
            (self.record(False, False, 22, 1), True, 0),
            (self.record(False, False, 1, 13), False, 0),
            (self.record(False, False, 1, 13), True, 1),
            (self.record(1, False, 0, 13), True, 0),
            (self.record(True, True, 1, 0), True, 0),
        ]:
            self.assertEqual(
                self.module.classify_canaries(
                    self.record(True, True),
                    actual,
                    marker_unchanged=unchanged,
                    accepted_connections=accepted,
                ),
                "INCONCLUSIVE",
            )

    def test_cleanup_uncertainty_is_fatal_even_with_permission_denial(self) -> None:
        good: dict[str, object] = dict(
            child_reaped=True,
            cleanup_succeeded=True,
            group_probe_errno=3,
            cleanup_exception=None,
            events=(),
        )
        self.module.require_cleanup(SimpleNamespace(**good))
        variants: list[dict[str, object]] = [
            dict(child_reaped=False),
            dict(cleanup_succeeded=False),
            dict(group_probe_errno=1),
            dict(cleanup_exception=RuntimeError()),
            dict(events=("cleanup",)),
        ]
        for changes in variants:
            with self.assertRaises(RuntimeError):
                self.module.require_cleanup(SimpleNamespace(**{**good, **changes}))

    def test_hosted_root_gate_precedes_arbitrary_content_reads(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            parent = Path(temporary).resolve()
            root = parent / "trama-og-m3"
            root.mkdir()
            environment = {
                "GITHUB_ACTIONS": "true",
                "GITHUB_REPOSITORY": "MarcoPorcellato/matryca-trama",
                "GITHUB_RUN_ATTEMPT": "1",
                "RUNNER_TEMP": str(parent),
            }
            with patch.dict(os.environ, environment, clear=True):
                self.module.require_hosted_root(root)
                with self.assertRaises(RuntimeError):
                    self.module.require_hosted_root(parent / "untrusted")
                with patch.dict(os.environ, {"GITHUB_RUN_ATTEMPT": "2"}):
                    with self.assertRaises(RuntimeError):
                        self.module.require_hosted_root(root)

    def test_startup_hook_is_rejected_before_producer_start(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            site = Path(temporary)
            self.module.check_startup_hooks(site)
            (site / "sitecustomize.py").write_text(
                "raise AssertionError('must never import')"
            )
            with self.assertRaises(RuntimeError):
                self.module.check_startup_hooks(site)

    def test_fixture_read_error_still_retains_final_receipt(self) -> None:
        self.assertTrue(
            hasattr(self.module, "finish_fixture"), "Final receipt retention absent"
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / "artifacts").mkdir()
            graph = root / "synthetic"
            graph.mkdir()
            state = {"complete": True}
            with patch.object(
                self.module.resources,
                "fixture_ledger",
                side_effect=OSError("synthetic ledger failure"),
            ):
                with self.assertRaises(OSError):
                    self.module.finish_fixture(root, graph, {}, state)
            import json

            saved = json.loads((root / "artifacts/m3-receipt.json").read_bytes())
            self.assertFalse(saved["complete"])
            self.assertEqual(saved["fixture_after_error"], "OSError")

    def test_fixture_mutation_is_fail_closed_with_retained_ledgers(self) -> None:
        self.assertTrue(
            hasattr(self.module, "finish_fixture"), "Final receipt retention absent"
        )
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / "artifacts").mkdir()
            graph = root / "synthetic"
            graph.mkdir()
            note = graph / "synthetic.md"
            note.write_text("- before")
            before = self.module.resources.fixture_ledger(graph)
            note.write_text("- changed")
            state = {"complete": True}
            with self.assertRaises(RuntimeError):
                self.module.finish_fixture(root, graph, before, state)
            self.assertFalse(state["complete"])
            self.assertTrue((root / "artifacts/m3-fixture-after.json").is_file())

    def test_non_hosted_execution_is_refused(self) -> None:
        with patch.dict(os.environ, {}, clear=True), self.assertRaises(RuntimeError):
            self.module.require_hosted_root(Path("/not-a-graph"))

    def test_executable_failure_suppresses_sensitive_exception_and_chain(self) -> None:
        self.assertTrue(
            hasattr(self.module, "entrypoint"), "Sanitized terminal boundary absent"
        )
        import contextlib
        import io

        error = OSError("/synthetic-sensitive-runner/private-user/file")
        error.__cause__ = RuntimeError("synthetic-sensitive-chain")
        output, errors = io.StringIO(), io.StringIO()
        with patch.object(self.module, "main", side_effect=error):
            with contextlib.redirect_stderr(errors), contextlib.redirect_stdout(output):
                status = self.module.entrypoint()
        self.assertEqual(status, 1)
        self.assertEqual(output.getvalue(), "")
        self.assertEqual(
            errors.getvalue(),
            "Exploratory measurement failed; inspect retained sanitized evidence.\n",
        )


if __name__ == "__main__":
    unittest.main()
