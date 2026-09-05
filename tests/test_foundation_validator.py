from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[1]
VALIDATOR = REPOSITORY / "scripts" / "validate_foundation.py"
REQUIRED = {
    ".github/CODEOWNERS",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/workflows/dependency-review.yml",
    ".github/workflows/foundation.yml",
    "AGENTS.md",
    "CODE_OF_CONDUCT.md",
    "COMMERCIAL_LICENSE.md",
    "CONTRIBUTING.md",
    "CONTRIBUTOR_LICENSING.md",
    "GOVERNANCE.md",
    "LICENSE",
    "NOTICE",
    "README.md",
    "SECURITY.md",
    "SUPPORT.md",
    "THIRD_PARTY_LICENSES.md",
    "TRADEMARKS.md",
    "docs/ARCHITECTURE.md",
    "docs/LICENSING_MODEL.md",
    "docs/ROADMAP.md",
    "docs/decisions/ADR-0001-PUBLIC_COMMUNITY_MONOREPO.md",
    "docs/decisions/ADR-0002-TRAMA_BRAIN_PRODUCT_BOUNDARY.md",
    "docs/decisions/ADR-0003-SOURCE_AVAILABLE-COMMERCIAL_BOUNDARY.md",
    "docs/specs/MATRYCA_TRAMA_PUBLIC_MONOREPO_FOUNDATION.md",
    "docs/specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md",
    "docs/status/CLAIM_LEDGER.md",
}


def run_validator(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--root", str(root)],
        capture_output=True,
        check=False,
        text=True,
    )


def create_minimum_repository(root: Path) -> None:
    for relative in REQUIRED:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        content = "foundation\n"
        if relative == "LICENSE":
            content = "# PolyForm Noncommercial License 1.0.0\n"
        elif relative == "NOTICE":
            content = "Required Notice: Copyright 2026 Example Licensor.\n"
        elif relative == "README.md":
            content = (
                "Community source-available foundation; named noncommercial "
                "organisations retain their licence permissions.\n"
            )
        elif relative == ".github/workflows/foundation.yml":
            content = "fetch-depth: 2\n"
        path.write_text(content, encoding="utf-8")


class FoundationValidatorTests(unittest.TestCase):
    def test_canonical_authority_docs_guard_gateway_and_db_profile_boundary(self) -> None:
        delivery_program = " ".join(
            (
                REPOSITORY / "docs" / "specs" / "MATRYCA_TRAMA_DELIVERY_PROGRAM.md"
            )
            .read_text(encoding="utf-8")
            .split()
        )
        roadmap = " ".join(
            (REPOSITORY / "docs" / "ROADMAP.md").read_text(encoding="utf-8").split()
        )

        self.assertIn(
            "Matryca Plumber is the sole future Logseq gateway and canonical public-contract owner.",
            delivery_program,
        )
        self.assertIn(
            "A qualified `og_markdown` Plumber profile may support the Trama consumer independently of D1.",
            roadmap,
        )
        self.assertIn(
            "A `db_native` consumer profile requires D1 outcome `supported`.",
            roadmap,
        )
        self.assertNotIn(
            "After Plumber publishes the contract and D1 has a supported outcome",
            roadmap,
        )

    def test_repository_has_no_self_referential_false_positive(self) -> None:
        result = run_validator(REPOSITORY)

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_legacy_credential_like_literal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_minimum_repository(root)
            leaked = "matryca-" + "local-dashboard-" + "example"
            (root / "docs" / "leak.md").write_text(leaked, encoding="utf-8")

            result = run_validator(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("credential-like literal", result.stderr)

    def test_broken_relative_markdown_link_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_minimum_repository(root)
            (root / "README.md").write_text(
                "[missing](docs/missing.md)\n", encoding="utf-8"
            )

            result = run_validator(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("broken relative link", result.stderr)

    def test_apache_license_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_minimum_repository(root)
            (root / "LICENSE").write_text(
                "Apache License, Version 2.0\n", encoding="utf-8"
            )

            result = run_validator(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PolyForm Noncommercial License 1.0.0", result.stderr)

    def test_missing_codeowners_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_minimum_repository(root)
            (root / ".github" / "CODEOWNERS").unlink()

            result = run_validator(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required file: .github/CODEOWNERS", result.stderr)

    def test_missing_delivery_program_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_minimum_repository(root)
            (root / "docs" / "specs" / "MATRYCA_TRAMA_DELIVERY_PROGRAM.md").unlink()

            result = run_validator(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "missing required file: docs/specs/MATRYCA_TRAMA_DELIVERY_PROGRAM.md",
                result.stderr,
            )

    def test_missing_claim_ledger_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_minimum_repository(root)
            (root / "docs" / "status" / "CLAIM_LEDGER.md").unlink()

            result = run_validator(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "missing required file: docs/status/CLAIM_LEDGER.md",
                result.stderr,
            )

    def test_missing_required_notice_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_minimum_repository(root)
            (root / "NOTICE").write_text("Copyright only\n", encoding="utf-8")

            result = run_validator(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Required Notice:", result.stderr)

    def test_readme_must_preserve_named_noncommercial_organisations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_minimum_repository(root)
            (root / "README.md").write_text(
                "Community source-available foundation.\n", encoding="utf-8"
            )

            result = run_validator(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("named noncommercial organisations", result.stderr)

    def test_foundation_workflow_must_fetch_parent_commit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            create_minimum_repository(root)
            (root / ".github" / "workflows" / "foundation.yml").write_text(
                "fetch-depth: 1\n", encoding="utf-8"
            )

            result = run_validator(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("fetch-depth: 2", result.stderr)


if __name__ == "__main__":
    unittest.main()
