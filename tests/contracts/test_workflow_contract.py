"""Contract tests for the fork-safe hosted qualification workflow."""

from pathlib import Path
import re
import unittest


REPOSITORY = Path(__file__).resolve().parents[2]
WORKFLOW_PATH = REPOSITORY / ".github" / "workflows" / "python-contracts.yml"
CANONICAL_WORKFLOW = """name: Python contracts

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: python-contracts-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  contracts:
    name: python-contracts
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: Check out repository
        uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7
      - name: Set up uv
        uses: astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9 # v9.0.0
      - run: uv sync --locked --all-packages
      - run: uv run --all-packages python -m unittest discover -s tests/contracts -v
      - run: uv run --all-packages python -m unittest discover -s tests/containment -v
      - run: uv run --all-packages python -m unittest tests.integration.test_plumber_consumer -v
      - run: uv run --all-packages python -m unittest tests.test_foundation_validator -v
"""


class WorkflowContractTests(unittest.TestCase):
    def workflow(self) -> str:
        self.assertTrue(
            WORKFLOW_PATH.is_file(),
            f"missing hosted qualification workflow: {WORKFLOW_PATH.relative_to(REPOSITORY)}",
        )
        return WORKFLOW_PATH.read_text(encoding="utf-8")

    def test_workflow_runs_the_locked_complete_suite(self) -> None:
        workflow = self.workflow()

        for command in (
            "uv sync --locked --all-packages",
            "uv run --all-packages python -m unittest discover -s tests/contracts -v",
            "uv run --all-packages python -m unittest discover -s tests/containment -v",
            "uv run --all-packages python -m unittest tests.integration.test_plumber_consumer -v",
            "uv run --all-packages python -m unittest tests.test_foundation_validator -v",
        ):
            with self.subTest(command=command):
                self.assertIn(f"- run: {command}", workflow)

        self.assertNotIn("python -m unittest discover -s tests -v", workflow)

    def test_workflow_uses_reviewed_full_action_pins(self) -> None:
        workflow = self.workflow()

        self.assertIn(
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
            workflow,
        )
        self.assertIn(
            "astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9",
            workflow,
        )
        self.assertNotIn("astral-sh/setup-uv@20cfd1bf945f4377ade1205e4dbc17946fc9a30d", workflow)

    def test_workflow_is_minimal_and_fork_safe(self) -> None:
        workflow = self.workflow()
        self.assert_workflow_surface(workflow)

        for required in (
            "on:\n  pull_request:\n  push:\n    branches: [main]",
            "permissions:\n  contents: read",
            "concurrency:\n  group: python-contracts-${{ github.workflow }}-${{ github.ref }}\n  cancel-in-progress: true",
            "timeout-minutes: 5",
        ):
            with self.subTest(required=required):
                self.assertIn(required, workflow)

        for forbidden in (
            "pull_request_target",
            "workflow_run",
            "secrets.",
            "actions/cache",
            "upload-artifact",
            "download-artifact",
            "deploy",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, workflow.lower())

    def assert_workflow_surface(self, workflow: str) -> None:
        """Reject workflow growth outside the reviewed, read-only contract."""
        self.assertEqual(workflow, CANONICAL_WORKFLOW)
        uses = re.findall(r"^\s+uses:\s+([^\s#]+)", workflow, re.MULTILINE)
        self.assertEqual(
            uses,
            [
                "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
                "astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9",
            ],
        )
        runs = re.findall(r"^\s+- run:\s+(.+)$", workflow, re.MULTILINE)
        self.assertEqual(
            runs,
            [
                "uv sync --locked --all-packages",
                "uv run --all-packages python -m unittest discover -s tests/contracts -v",
                "uv run --all-packages python -m unittest discover -s tests/containment -v",
                "uv run --all-packages python -m unittest tests.integration.test_plumber_consumer -v",
                "uv run --all-packages python -m unittest tests.test_foundation_validator -v",
            ],
        )
        self.assertNotRegex(workflow, r"(?m)^\s{4,}permissions:")
        self.assertNotRegex(workflow, r"(?m)^\s+(?:pull_request_target|workflow_run):")
        self.assertNotRegex(
            workflow.lower(),
            r"actions/cache|upload-artifact|download-artifact|deploy|secrets\.",
        )

    def test_workflow_rejects_unauthorized_surface(self) -> None:
        workflow = self.workflow()
        for addition in (
            "\n      - uses: actions/cache@deadbeef\n",
            "\n      - run: curl https://example.invalid\n",
            "\n    permissions:\n      contents: write\n",
            "\n  workflow_run:\n",
            "\n      - uses: actions/upload-artifact@deadbeef\n",
            "\npermissions:\n  issues: write\n",
            "\n  workflow_dispatch:\n",
            "\n  schedule:\n    - cron: '0 * * * *'\n",
            "\n    branches: [main, release]\n",
            "\n  pull_request:\n    types: [opened]\n",
        ):
            with self.subTest(addition=addition):
                with self.assertRaises(AssertionError):
                    self.assert_workflow_surface(workflow + addition)


if __name__ == "__main__":
    unittest.main()
