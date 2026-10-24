"""Client scope, invocation and terminal error tests using inert producer doubles."""

import errno
import importlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from trama_core.graph_values import GraphGatewayError, GraphGatewayErrorCode as Code
from test_mapper import example


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(
            importlib.util.find_spec("trama_plumber_client.adapter"),
            "The structurally gated synthetic client is not implemented",
        )
        self.adapter = importlib.import_module("trama_plumber_client.adapter")
        self.fixture = importlib.import_module("trama_plumber_client._fixture")
        self.process = importlib.import_module("trama_plumber_client._process")
        self.temporary = tempfile.TemporaryDirectory(prefix="trama client test ")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.graph = self.root / "synthetic graph"
        self.graph.mkdir()
        self.alias = self.root / "input alias"
        self.alias.symlink_to(self.graph, target_is_directory=True)
        self.python = self.root / "producer python"
        self.python.symlink_to(Path(sys.executable).resolve())
        self.handle = self.fixture._created_fixture(
            str(self.root), str(self.graph), str(self.alias)
        )

    def client(self, fixture=None, **limits):
        return self.adapter.PlumberClientAdapter(
            str(self.python),
            self.handle if fixture is None else fixture,
            expected_resolved_python=os.path.realpath(self.python),
            **limits,
        )

    def result(self, stderr=b"", **changes):
        fields = dict(
            stdout=json.dumps(example()).encode(),
            stderr=stderr,
            returncode=0,
            child_reaped=True,
            group_probe_errno=errno.ESRCH,
            cleanup_succeeded=True,
            cleanup_exception=None,
            observations=(),
            events=(),
        )
        fields.update(changes)
        return self.process.ProcessResult(**fields)

    def failure(self, reason, *, exitcode=-9, stderr=b"", cleanup=True):
        return self.process.ProcessFailure(
            reason,
            stdout=b"",
            stderr=stderr,
            returncode=exitcode,
            child_reaped=True,
            signal_errno=None,
            group_probe_errno=errno.ESRCH,
            cleanup_succeeded=cleanup,
            cleanup_exception=None,
            observations=(),
            events=(),
        )

    def test_positive_alias_is_canonicalized_but_venv_python_is_not(self):
        def producer(argv, **options):
            self.assertEqual(
                argv,
                [
                    str(self.python),
                    "-I",
                    "-B",
                    "-m",
                    "matryca_plumber.graph_gateway",
                    "snapshot",
                    "--graph-root",
                    str(self.graph),
                    "--expect-descriptor-sha256",
                    "bcc6ac607706e934e5df4e044802aa74c7d7455e7711220df116080f1ab0cc70",
                ],
            )
            self.assertEqual(
                options,
                {
                    "timeout_seconds": 180.0,
                    "stdout_limit": 4194304,
                    "stderr_limit": 512,
                },
            )
            return self.result()

        with patch.object(self.adapter, "run_process", side_effect=producer):
            result = self.client().snapshot()
        self.assertEqual(result.identity.graph_id, "graph-a")

    def test_arbitrary_paths_and_forged_handles_fail_before_content_read_or_launch(
        self,
    ):
        for value in (str(self.graph), self.graph, object()):
            with (
                self.subTest(value=type(value)),
                patch("builtins.open", side_effect=AssertionError("content read")),
                patch.object(self.adapter, "run_process") as launch,
                self.assertRaises(GraphGatewayError) as caught,
            ):
                self.client(value).snapshot()
            self.assertEqual(caught.exception.code, Code.ADMISSION_SCOPE_VIOLATION)
            launch.assert_not_called()

    def test_retargeted_fixture_alias_is_rejected_without_launch(self):
        self.alias.unlink()
        self.alias.symlink_to(self.root.parent, target_is_directory=True)
        with (
            patch.object(self.adapter, "run_process") as launch,
            self.assertRaises(GraphGatewayError) as caught,
        ):
            self.client().snapshot()
        self.assertEqual(caught.exception.code, Code.ADMISSION_SCOPE_VIOLATION)
        launch.assert_not_called()

    def test_missing_executable_and_wrong_resolved_identity_fail_closed(self):
        with self.assertRaises(GraphGatewayError) as caught:
            self.adapter.PlumberClientAdapter(
                str(self.python), self.handle, expected_resolved_python="/wrong/python"
            )
        self.assertEqual(caught.exception.code, Code.CONFIGURATION_INVALID)

    def test_limits_can_only_be_lowered(self):
        for limits in (
            {"timeout_seconds": 181},
            {"timeout_seconds": float("nan")},
            {"timeout_seconds": True},
            {"stdout_limit": 4194305},
            {"stderr_limit": 513},
            {"stdout_limit": True},
            {"stderr_limit": 0},
        ):
            with (
                self.subTest(limits=limits),
                self.assertRaises(GraphGatewayError) as caught,
            ):
                self.client(**limits)
            self.assertEqual(caught.exception.code, Code.CONFIGURATION_INVALID)

    def test_success_with_stderr_or_uncertain_cleanup_is_rejected(self):
        for result, expected in (
            (self.result(stderr=b"private detail"), Code.PROTOCOL_VIOLATION),
            (self.result(cleanup_succeeded=False), Code.CLEANUP_UNCERTAIN),
            (self.result(group_probe_errno=errno.EPERM), Code.CLEANUP_UNCERTAIN),
        ):
            with (
                self.subTest(expected=expected),
                patch.object(self.adapter, "run_process", return_value=result),
                self.assertRaises(GraphGatewayError) as caught,
            ):
                self.client().snapshot()
            self.assertEqual(caught.exception.code, expected)
            self.assertNotIn("private detail", str(caught.exception))

    def test_timeout_overflow_and_spawn_errors_are_sanitized_without_retry(self):
        for failure, expected in (
            (self.failure("timeout"), Code.PROCESS_TIMEOUT),
            (self.failure("output_limit"), Code.PROCESS_OUTPUT_LIMIT),
            (OSError("private path"), Code.SPAWN_FAILED),
            (self.failure("timeout", cleanup=False), Code.CLEANUP_UNCERTAIN),
        ):
            with (
                self.subTest(expected=expected),
                patch.object(
                    self.adapter, "run_process", side_effect=failure
                ) as launch,
                self.assertRaises(GraphGatewayError) as caught,
            ):
                self.client().snapshot()
            self.assertEqual(caught.exception.code, expected)
            self.assertEqual(launch.call_count, 1)
            self.assertFalse(caught.exception.retryable)
            self.assertNotIn("private", str(caught.exception))

    def test_known_producer_refusal_is_translated_only_after_cleanup(self):
        failure = self.failure(
            "nonzero_exit", exitcode=4, stderr=b'{"error":"source_rejected"}\n'
        )
        with (
            patch.object(self.adapter, "run_process", side_effect=failure),
            self.assertRaises(GraphGatewayError) as caught,
        ):
            self.client().snapshot()
        self.assertEqual(caught.exception.code, Code.SOURCE_REJECTED)


if __name__ == "__main__":
    unittest.main()
