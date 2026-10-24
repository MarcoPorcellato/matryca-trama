"""Exercise probe evidence/error classification using inert children only."""

import errno
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import process_boundary
import provision
import real_probe
from resources import QualificationFailure


class ProbeClassificationTests(unittest.TestCase):
    def test_client_shape_failure_retains_output_before_domain_translation(
        self,
    ) -> None:
        from trama_plumber_client._fixture import _created_fixture
        from trama_core.graph_values import GraphGatewayError

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            (root / "artifacts").mkdir()
            graph = root / "synthetic"
            graph.mkdir()
            alias = root / "alias"
            alias.symlink_to(graph, target_is_directory=True)
            fixture = _created_fixture(str(root), str(graph), str(alias))
            client = real_probe.client_module.PlumberClientAdapter(
                sys.executable,
                fixture,
                expected_resolved_python=os.path.realpath(sys.executable),
            )
            result = process_boundary.ProcessResult(
                stdout=b"[]\n",
                stderr=b"",
                returncode=0,
                child_reaped=True,
                group_probe_errno=errno.ESRCH,
                cleanup_succeeded=True,
                cleanup_exception=None,
                observations=(),
                events=(),
            )
            with (
                patch.object(
                    process_boundary, "run_process", return_value=result
                ) as launch,
                self.assertRaises(GraphGatewayError),
            ):
                real_probe.invoke_client(root, "snapshot", client, graph=graph)
            self.assertEqual(launch.call_count, 1)
            self.assertEqual(
                (root / "artifacts/snapshot.stdout.txt").read_bytes(), b"[]\n"
            )
            evidence = json.loads(
                (root / "artifacts/snapshot.lifecycle.json").read_bytes()
            )
            self.assertTrue(evidence["child_reaped"] and evidence["cleanup_succeeded"])

    def capture_attestation(self, capabilities: bytes) -> tuple[list[str], str | None]:
        class CommandCaptured(Exception):
            pass

        command: list[str] = []
        failure = None

        def capture_tool(
            root: Path,
            label: str,
            argv: list[str],
            *,
            environment: dict[str, str] | None = None,
        ) -> process_boundary.ProcessResult:
            if label == "attestation":
                command.extend(argv)
                raise CommandCaptured
            return process_boundary.ProcessResult(
                stdout=capabilities,
                stderr=b"",
                returncode=0,
                child_reaped=True,
                group_probe_errno=errno.ESRCH,
                cleanup_succeeded=True,
                cleanup_exception=None,
                observations=(),
                events=(),
            )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve() / "qualification"
            with (
                patch.object(
                    sys, "argv", ["provision", "--root", str(root), "--producer"]
                ),
                patch.dict(
                    os.environ,
                    {
                        "GITHUB_ACTIONS": "true",
                        "GITHUB_REPOSITORY": "MarcoPorcellato/matryca-trama",
                    },
                    clear=True,
                ),
                patch.object(provision.platform, "system", return_value="Linux"),
                patch.object(provision.platform, "machine", return_value="x86_64"),
                patch.object(
                    provision.platform, "python_version", return_value="3.12.14"
                ),
                patch.object(provision, "disk_admit"),
                patch.object(
                    provision, "download", return_value=root / "synthetic.whl"
                ),
                patch.object(
                    provision.shutil, "which", return_value="/qualification/gh"
                ),
                patch.object(provision, "run_tool", side_effect=capture_tool),
            ):
                try:
                    provision.main()
                except CommandCaptured:
                    pass
                except QualificationFailure as error:
                    failure = str(error)
        return command, failure

    def test_attestation_command_has_one_identity_selector_and_exact_provenance(
        self,
    ) -> None:
        argv, failure = self.capture_attestation(
            b"--signer-workflow --source-digest --source-ref "
            b"--cert-identity --deny-self-hosted-runners"
        )
        self.assertIsNone(failure)
        selectors = (
            "--cert-identity",
            "--cert-identity-regex",
            "--signer-repo",
            "--signer-workflow",
        )
        self.assertEqual(
            [flag for flag in selectors if flag in argv], ["--cert-identity"]
        )
        self.assertEqual(argv[:3], ["/qualification/gh", "attestation", "verify"])
        expected = {
            "--repo": "MarcoPorcellato/matryca-plumber",
            "--source-digest": "8c30f70e217722e719c5aedc322219ebccb87e68",
            "--source-ref": "refs/tags/v2.1.0-alpha.3",
            "--cert-identity": "https://github.com/MarcoPorcellato/matryca-plumber/"
            ".github/workflows/release.yml@refs/tags/v2.1.0-alpha.3",
            "--format": "json",
        }
        for flag, value in expected.items():
            self.assertEqual(argv.count(flag), 1)
            self.assertEqual(argv[argv.index(flag) + 1], value)
        self.assertEqual(argv.count("--deny-self-hosted-runners"), 1)

    def test_capability_check_does_not_require_unused_identity_selector(self) -> None:
        argv, failure = self.capture_attestation(
            b"--source-digest --source-ref --cert-identity --deny-self-hosted-runners"
        )
        self.assertIsNone(failure)
        self.assertIn("--cert-identity", argv)
        self.assertNotIn("--signer-workflow", argv)

    def test_managed_python_is_installed_before_both_workflow_lookups(self) -> None:
        workflow = (
            Path(__file__).resolve().parents[2]
            / ".github/workflows/plumber-og-consumer-qualification.yml"
        )
        lines = [line.strip() for line in workflow.read_text().splitlines()]
        install = "uv --no-config python install --managed-python --no-bin 3.12.14"
        lookup = 'PYTHON="$(uv python find --managed-python 3.12.14)"'
        self.assertEqual(lines.count(install), 2)
        lookups = [index for index, line in enumerate(lines) if line == lookup]
        self.assertEqual(len(lookups), 2)
        for index in lookups:
            self.assertEqual(lines[index - 1], install)

    def test_reader_exception_preserves_captured_bytes_and_cleanup(self) -> None:
        original_read = os.read
        captured_prefix = False

        def interrupted_read(fd: int, size: int) -> bytes:
            nonlocal captured_prefix
            if captured_prefix:
                raise OSError("synthetic reader interruption")
            raw = original_read(fd, size)
            if raw == b"synthetic-prefix":
                captured_prefix = True
            return raw

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "artifacts").mkdir()
            argv = [
                sys.executable,
                "-I",
                "-B",
                "-c",
                "import os,time; os.write(1,b'synthetic-prefix'); time.sleep(0.05); "
                "os.write(1,b'tail'); time.sleep(30)",
            ]
            with (
                patch.object(process_boundary.os, "read", side_effect=interrupted_read),
                self.assertRaisesRegex(OSError, "synthetic reader interruption"),
            ):
                real_probe.invoke(root, "reader", argv)
            self.assertTrue((root / "artifacts/reader.stdout.txt").is_file())
            self.assertEqual(
                (root / "artifacts/reader.stdout.txt").read_bytes(), b"synthetic-prefix"
            )
            evidence = json.loads(
                (root / "artifacts/reader.lifecycle.json").read_bytes()
            )
            self.assertTrue(evidence["child_reaped"])
            self.assertTrue(evidence["cleanup_succeeded"])
            self.assertIs(type(evidence["returncode"]), int)

    def test_provisioning_setup_interruption_retains_terminal_evidence(self) -> None:
        class Abort(BaseException):
            pass

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "artifacts").mkdir()
            with (
                patch.object(
                    process_boundary.os, "set_blocking", side_effect=Abort("setup")
                ),
                self.assertRaises(Abort),
            ):
                provision.run_tool(
                    root,
                    "setup",
                    [sys.executable, "-I", "-B", "-c", "import time; time.sleep(30)"],
                )
            self.assertTrue((root / "artifacts/setup.json").is_file())
            evidence = json.loads((root / "artifacts/setup.json").read_bytes())
            self.assertTrue(evidence["child_reaped"])
            self.assertTrue(evidence["cleanup_succeeded"])
            self.assertEqual((root / "artifacts/setup.stdout.txt").read_bytes(), b"")

    def test_expected_refusal_is_a_passing_control_with_lifecycle_evidence(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "artifacts").mkdir()
            argv = [
                sys.executable,
                "-I",
                "-B",
                "-c",
                'import os; os.write(2,b\'{"error":"source_rejected"}\\n\'); raise SystemExit(4)',
            ]
            result = real_probe.invoke(
                root,
                "negative",
                argv,
                expected_exit=4,
                expected_error="source_rejected",
            )
            self.assertEqual(result["expected_negative"], "source_rejected")
            self.assertTrue(result["child_reaped"])
            self.assertTrue(result["cleanup_succeeded"])
            self.assertEqual(
                json.loads((root / "artifacts/negative.stderr.txt").read_bytes()),
                {"error": "source_rejected"},
            )

    def test_wrong_error_is_not_accepted_merely_because_exit_matches(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "artifacts").mkdir()
            argv = [
                sys.executable,
                "-I",
                "-B",
                "-c",
                'import os; os.write(2,b\'{"error":"other"}\\n\'); raise SystemExit(4)',
            ]
            with self.assertRaises(QualificationFailure):
                real_probe.invoke(
                    root,
                    "negative",
                    argv,
                    expected_exit=4,
                    expected_error="source_rejected",
                )
            self.assertTrue((root / "artifacts/negative.lifecycle.json").is_file())

    def test_shape_failure_retains_synthetic_stdout_without_rerunning(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "artifacts").mkdir()
            argv = [sys.executable, "-I", "-B", "-c", 'import os; os.write(1,b"[]\\n")']
            with self.assertRaises(QualificationFailure):
                real_probe.invoke(root, "shape", argv)
            self.assertEqual(
                (root / "artifacts/shape.stdout.txt").read_bytes(), b"[]\n"
            )
            self.assertTrue(
                json.loads((root / "artifacts/shape.lifecycle.json").read_bytes())[
                    "cleanup_succeeded"
                ]
            )

    def test_negative_control_must_not_succeed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "artifacts").mkdir()
            with self.assertRaises(QualificationFailure):
                real_probe.invoke(
                    root,
                    "unexpected",
                    [sys.executable, "-I", "-B", "-c", "pass"],
                    expected_exit=4,
                    expected_error="source_rejected",
                )


if __name__ == "__main__":
    unittest.main()
