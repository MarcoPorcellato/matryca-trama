#!/usr/bin/env python3
"""Validate the document-first public repository boundary."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote


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
FORBIDDEN_PARTS = {"matryca_core", "repomix-output.xml"}
FORBIDDEN_SUFFIXES = {".bin", ".db", ".gguf", ".lbug", ".safetensors", ".sqlite"}
LOCAL_PATH = re.compile(r"(?:/Users/|[A-Za-z]:\\\\Users\\\\)")
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
SECRET_LIKE = re.compile(
    r"(?:-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|"
    r"github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|"
    r"AKIA[0-9A-Z]{16})"
)
SELF = Path("scripts/validate_foundation.py")


def repository_files(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*") if path.is_file() and ".git" not in path.parts
    )


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    files = repository_files(root)
    present = {path.relative_to(root).as_posix() for path in files}
    for required in sorted(REQUIRED - present):
        errors.append(f"missing required file: {required}")

    license_path = root / "LICENSE"
    if license_path.is_file() and not license_path.read_text(
        encoding="utf-8"
    ).startswith("# PolyForm Noncommercial License 1.0.0"):
        errors.append("LICENSE must contain PolyForm Noncommercial License 1.0.0")

    notice_path = root / "NOTICE"
    if notice_path.is_file() and "Required Notice:" not in notice_path.read_text(
        encoding="utf-8"
    ):
        errors.append("NOTICE must contain a plain-text Required Notice: line")

    readme_path = root / "README.md"
    if readme_path.is_file():
        readme = readme_path.read_text(encoding="utf-8")
        if "source-available" not in readme:
            errors.append(
                "README must describe the Community foundation as source-available"
            )
        if "named noncommercial organisations" not in readme:
            errors.append(
                "README must preserve permissions for named noncommercial organisations"
            )

    workflow_path = root / ".github" / "workflows" / "foundation.yml"
    if workflow_path.is_file() and "fetch-depth: 2" not in workflow_path.read_text(
        encoding="utf-8"
    ):
        errors.append(
            "foundation workflow must use fetch-depth: 2 before checking HEAD^"
        )

    for path in files:
        relative = path.relative_to(root)
        relative_text = relative.as_posix()
        if FORBIDDEN_PARTS.intersection(relative.parts) or relative.name in FORBIDDEN_PARTS:
            errors.append(f"forbidden legacy path: {relative_text}")
        if relative.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f"forbidden generated database: {relative_text}")
        if relative.name.startswith(".env") and relative.name != ".env.example":
            errors.append(f"forbidden environment file: {relative_text}")

        if relative == SELF or path.suffix.lower() not in {
            ".md",
            ".txt",
            ".yml",
            ".yaml",
            ".py",
        }:
            continue
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            errors.append(f"non-UTF-8 text file: {relative_text}")
            continue
        if LOCAL_PATH.search(content):
            errors.append(f"local user path disclosed: {relative_text}")
        if "matryca-local-dashboard-" in content:
            errors.append(f"legacy credential-like literal disclosed: {relative_text}")
        if SECRET_LIKE.search(content):
            errors.append(f"secret-like value disclosed: {relative_text}")

        if path.suffix.lower() != ".md":
            continue
        for raw_target in MARKDOWN_LINK.findall(content):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>\"")
            if target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target_path = unquote(target.split("#", 1)[0])
            if target_path and not (path.parent / target_path).resolve().exists():
                errors.append(f"broken relative link in {relative_text}: {raw_target}")

    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root to validate",
    )
    return parser.parse_args()


def main() -> int:
    root = parse_args().root.resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Foundation validation passed: {len(repository_files(root))} files checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
