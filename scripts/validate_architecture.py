#!/usr/bin/env python3
"""Validate repository package imports against architecture.toml."""

from __future__ import annotations

import argparse
import ast
import re
import sys
import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


@dataclass(frozen=True, order=True)
class Violation:
    path: Path
    line: int
    code: str
    message: str


@dataclass(frozen=True)
class PackageRule:
    distribution: str
    directory: Path
    import_root: str
    allowed_internal: frozenset[str]
    allowed_external: frozenset[str]


@dataclass(frozen=True)
class Finding:
    violation: Violation
    package: str
    import_root: str | None
    package_path: Path


def architecture_error(root: Path, message: str) -> Violation:
    return Violation(Path("architecture.toml"), 0, "ARCH006", message)


def dependency_name(requirement: str) -> str:
    return re.split(r"[\s\[<>=!~;]", requirement, maxsplit=1)[0].replace("_", "-").lower()


def read_config(root: Path) -> tuple[dict[str, PackageRule], dict[str, str], set[str], list[Any], list[Violation]]:
    path = root / "architecture.toml"
    try:
        with path.open("rb") as handle:
            raw = tomllib.load(handle)
    except (FileNotFoundError, tomllib.TOMLDecodeError, OSError) as error:
        return {}, {}, set(), [], [architecture_error(root, f"invalid architecture map: {error}")]

    errors: list[Violation] = []
    raw_packages = raw.get("packages")
    raw_external = raw.get("external", {})
    raw_forbidden = raw.get("forbidden", {})
    exceptions = raw.get("exceptions", [])
    if not isinstance(raw_packages, dict):
        return {}, {}, set(), [], [architecture_error(root, "packages must be a table")]
    if not isinstance(raw_external, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in raw_external.items()
    ):
        errors.append(architecture_error(root, "external imports must map roots to distributions"))
        raw_external = {}
    roots = raw_forbidden.get("roots", []) if isinstance(raw_forbidden, dict) else []
    if not isinstance(roots, list) or not all(isinstance(root_name, str) for root_name in roots):
        errors.append(architecture_error(root, "forbidden roots must be a list"))
        roots = []
    rules: dict[str, PackageRule] = {}
    for distribution, value in raw_packages.items():
        if not isinstance(distribution, str) or not isinstance(value, dict):
            errors.append(architecture_error(root, "package rules must be named tables"))
            continue
        required = ("directory", "import_root", "allowed_internal", "allowed_external")
        if any(field not in value for field in required):
            errors.append(architecture_error(root, f"package rule {distribution} is incomplete"))
            continue
        directory = value["directory"]
        import_root = value["import_root"]
        internal = value["allowed_internal"]
        external = value["allowed_external"]
        if not (
            isinstance(directory, str)
            and isinstance(import_root, str)
            and isinstance(internal, list)
            and isinstance(external, list)
            and all(isinstance(item, str) for item in internal + external)
        ):
            errors.append(architecture_error(root, f"package rule {distribution} has invalid values"))
            continue
        rules[distribution] = PackageRule(
            distribution=distribution,
            directory=Path(directory),
            import_root=import_root,
            allowed_internal=frozenset(internal),
            allowed_external=frozenset(external),
        )
    if not isinstance(exceptions, list):
        errors.append(architecture_error(root, "exceptions must be a list"))
        exceptions = []
    return rules, dict(raw_external), set(roots), exceptions, errors


def read_manifests(root: Path, rules: dict[str, PackageRule]) -> tuple[dict[str, set[str]], list[Violation]]:
    declarations: dict[str, set[str]] = {}
    violations: list[Violation] = []
    for manifest in sorted(root.glob("packages/*/pyproject.toml")):
        relative = manifest.relative_to(root)
        try:
            with manifest.open("rb") as handle:
                project = tomllib.load(handle).get("project", {})
        except (OSError, tomllib.TOMLDecodeError) as error:
            violations.append(Violation(relative, 0, "ARCH006", f"invalid manifest: {error}"))
            continue
        distribution = project.get("name") if isinstance(project, dict) else None
        dependencies = project.get("dependencies", []) if isinstance(project, dict) else []
        if not isinstance(distribution, str) or not isinstance(dependencies, list) or not all(
            isinstance(item, str) for item in dependencies
        ):
            violations.append(Violation(relative, 0, "ARCH006", "manifest project is invalid"))
            continue
        rule = rules.get(distribution)
        if rule is None:
            violations.append(Violation(relative, 0, "ARCH001", f"unregistered package: {distribution}"))
            continue
        if rule.directory != relative.parent:
            violations.append(Violation(relative, 0, "ARCH006", f"package directory mismatch: {distribution}"))
            continue
        declarations[distribution] = {dependency_name(item) for item in dependencies}
    for distribution, rule in rules.items():
        if distribution not in declarations:
            violations.append(architecture_error(root, f"registered package has no manifest: {distribution}"))
    return declarations, violations


class ImportVisitor(ast.NodeVisitor):
    def __init__(
        self,
        root: Path,
        path: Path,
        rule: PackageRule,
        declarations: set[str],
        internal_roots: dict[str, PackageRule],
        external: dict[str, str],
        forbidden: set[str],
    ) -> None:
        self.root = root
        self.path = path
        self.rule = rule
        self.declarations = declarations
        self.internal_roots = internal_roots
        self.external = external
        self.forbidden = forbidden
        self.findings: list[Finding] = []
        self.importlib_names = {"importlib"}
        self.dynamic_names = {"__import__"}
        self.sys_names = {"sys"}
        self.sys_path_names: set[str] = set()

    def add(self, node: ast.AST, code: str, message: str, import_root: str | None) -> None:
        relative = self.path.relative_to(self.root)
        self.findings.append(
            Finding(Violation(relative, node.lineno, code, message), self.rule.distribution, import_root, self.path.relative_to(self.root / self.rule.directory))
        )

    def check_import(self, node: ast.AST, module: str) -> None:
        root_name = module.split(".", 1)[0]
        if root_name in sys.stdlib_module_names or root_name == self.rule.import_root:
            return
        internal = self.internal_roots.get(root_name)
        if internal is not None:
            if root_name not in self.rule.allowed_internal:
                self.add(node, "ARCH002", f"forbidden internal import: {root_name}", root_name)
            elif dependency_name(internal.distribution) not in self.declarations:
                self.add(node, "ARCH003", f"undeclared dependency: {internal.distribution}", root_name)
            return
        if root_name in self.forbidden:
            self.add(node, "ARCH004", f"forbidden private import: {root_name}", root_name)
            return
        distribution = self.external.get(root_name)
        if distribution is None:
            self.add(node, "ARCH004", f"unmapped external import: {root_name}", root_name)
        elif root_name not in self.rule.allowed_external or module != root_name:
            self.add(node, "ARCH004", f"forbidden external import: {module}", root_name)
        elif dependency_name(distribution) not in self.declarations:
            self.add(node, "ARCH003", f"undeclared dependency: {distribution}", root_name)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            root_name = alias.name.split(".", 1)[0]
            if root_name == "importlib":
                self.importlib_names.add(alias.asname or root_name)
            if root_name == "sys":
                self.sys_names.add(alias.asname or root_name)
            self.check_import(node, alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.level or node.module is None:
            return
        if node.module == "importlib":
            for alias in node.names:
                if alias.name == "import_module":
                    self.dynamic_names.add(alias.asname or alias.name)
        if node.module == "builtins":
            for alias in node.names:
                if alias.name == "__import__":
                    self.dynamic_names.add(alias.asname or alias.name)
        if node.module == "sys":
            for alias in node.names:
                if alias.name == "path":
                    self.sys_path_names.add(alias.asname or alias.name)
        self.check_import(node, node.module)
        self.generic_visit(node)

    def is_sys_path(self, node: ast.AST) -> bool:
        if isinstance(node, ast.Name):
            return node.id in self.sys_path_names
        if isinstance(node, ast.Attribute):
            return isinstance(node.value, ast.Name) and node.value.id in self.sys_names and node.attr == "path"
        return isinstance(node, ast.Subscript) and self.is_sys_path(node.value)

    def visit_Call(self, node: ast.Call) -> None:
        function = node.func
        if isinstance(function, ast.Name) and function.id in self.dynamic_names:
            self.add(node, "ARCH005", "dynamic import is forbidden", None)
        elif (
            isinstance(function, ast.Attribute)
            and isinstance(function.value, ast.Name)
            and function.value.id in self.importlib_names
            and function.attr == "import_module"
        ):
            self.add(node, "ARCH005", "dynamic import is forbidden", None)
        if isinstance(function, ast.Attribute) and self.is_sys_path(function.value):
            self.add(node, "ARCH005", "sys.path mutation is forbidden", None)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        if any(self.is_sys_path(target) for target in node.targets):
            self.add(node, "ARCH005", "sys.path mutation is forbidden", None)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        if self.is_sys_path(node.target):
            self.add(node, "ARCH005", "sys.path mutation is forbidden", None)
        self.generic_visit(node)


def is_narrow_path_glob(path_glob: object, package_directory: Path) -> bool:
    if not isinstance(path_glob, str) or not path_glob or path_glob.startswith(("/", "\\")):
        return False
    if re.match(r"^[A-Za-z]:[\\/]", path_glob):
        return False
    parts = path_glob.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return False
    if any(token in path_glob for token in "*?[]"):
        return False
    return path_glob.startswith(f"{package_directory.as_posix()}/") and path_glob.endswith(".py")


def validate_exceptions(
    root: Path,
    exceptions: list[Any],
    rules: dict[str, PackageRule],
    forbidden: set[str],
    findings: list[Finding],
) -> tuple[list[Finding], list[Violation]]:
    errors: list[Violation] = []
    suppressed: set[int] = set()
    seen: set[str] = set()
    required = {"id", "package", "import_root", "path_glob", "issue", "owner", "reason", "created", "expires", "removal_condition"}
    for entry in exceptions:
        if not isinstance(entry, dict) or not required.issubset(entry):
            errors.append(architecture_error(root, "exception is incomplete"))
            continue
        identifier = entry["id"]
        package = entry["package"]
        import_root = entry["import_root"]
        path_glob = entry["path_glob"]
        if not isinstance(identifier, str) or identifier in seen:
            errors.append(architecture_error(root, "exception identifier is invalid or duplicate"))
            continue
        seen.add(identifier)
        if not isinstance(package, str) or not isinstance(import_root, str) or any(
            character in package + import_root for character in "*?[]"
        ) or package not in rules or import_root in forbidden:
            errors.append(architecture_error(root, f"exception {identifier} is over-broad or forbidden"))
            continue
        if not is_narrow_path_glob(path_glob, rules[package].directory):
            errors.append(architecture_error(root, f"exception {identifier} has invalid path_glob"))
            continue
        if not all(isinstance(entry[field], str) and entry[field] for field in required - {"created", "expires"}):
            errors.append(architecture_error(root, f"exception {identifier} is incomplete"))
            continue
        try:
            expires = date.fromisoformat(str(entry["expires"]))
            date.fromisoformat(str(entry["created"]))
        except ValueError:
            errors.append(architecture_error(root, f"exception {identifier} has invalid dates"))
            continue
        if expires < date.today():
            errors.append(architecture_error(root, f"exception {identifier} is expired"))
            continue
        matches = [
            index
            for index, finding in enumerate(findings)
            if finding.package == package
            and finding.import_root == import_root
            and finding.violation.code in {"ARCH002", "ARCH003", "ARCH004"}
            and finding.violation.path.as_posix() == path_glob
        ]
        if not matches:
            errors.append(architecture_error(root, f"exception {identifier} matches no live violation"))
            continue
        suppressed.update(matches)
    return [finding for index, finding in enumerate(findings) if index not in suppressed], errors


def validate_repository(root: Path) -> list[Violation]:
    root = root.resolve()
    rules, external, forbidden, exceptions, violations = read_config(root)
    if not rules:
        return sorted(violations)
    declarations, manifest_violations = read_manifests(root, rules)
    violations.extend(manifest_violations)
    internal_roots = {rule.import_root: rule for rule in rules.values()}
    findings: list[Finding] = []
    for distribution, rule in rules.items():
        if distribution not in declarations:
            continue
        source_root = root / rule.directory / "src"
        for path in sorted(source_root.rglob("*.py")):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except (OSError, SyntaxError, UnicodeDecodeError) as error:
                violations.append(Violation(path.relative_to(root), 0, "ARCH006", f"invalid source: {error}"))
                continue
            visitor = ImportVisitor(root, path, rule, declarations[distribution], internal_roots, external, forbidden)
            visitor.visit(tree)
            findings.extend(visitor.findings)
    findings, exception_violations = validate_exceptions(root, exceptions, rules, forbidden, findings)
    violations.extend(exception_violations)
    violations.extend(finding.violation for finding in findings)
    return sorted(violations)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    return parser.parse_args()


def main() -> int:
    violations = validate_repository(parse_args().root)
    if violations:
        for violation in violations:
            print(f"{violation.path}:{violation.line}: {violation.code}: {violation.message}", file=sys.stderr)
        return 1
    print("Architecture validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
