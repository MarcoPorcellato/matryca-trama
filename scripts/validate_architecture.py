#!/usr/bin/env python3
"""Validate repository package imports against architecture.toml."""

from __future__ import annotations

import argparse
import ast
from fnmatch import fnmatchcase
import re
import sys
import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any


REPOSITORY_ISSUE_URL = re.compile(
    r"https://github\.com/MarcoPorcellato/matryca-trama/issues/[1-9][0-9]*"
)

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
    manifest_directories: set[Path] = set()
    for manifest in sorted(root.glob("packages/*/pyproject.toml")):
        relative = manifest.relative_to(root)
        manifest_directories.add(relative.parent)
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
    source_directories = {
        source.relative_to(root).parent
        for source in root.glob("packages/*/src")
        if source.is_dir()
    }
    registered_directories = {rule.directory for rule in rules.values()}
    for directory in sorted(source_directories):
        if directory not in registered_directories:
            violations.append(Violation(directory / "src", 0, "ARCH001", f"unregistered package source tree: {directory}"))
        elif directory not in manifest_directories:
            violations.append(Violation(directory / "src", 0, "ARCH006", f"package source tree has no manifest: {directory}"))
    for distribution, rule in rules.items():
        if distribution not in declarations and rule.directory not in source_directories:
            violations.append(architecture_error(root, f"registered package has no manifest: {distribution}"))
    return declarations, violations


def validate_declared_dependencies(
    root: Path,
    declarations: dict[str, set[str]],
    rules: dict[str, PackageRule],
    external: dict[str, str],
) -> list[Violation]:
    internal_distributions = {dependency_name(rule.distribution): rule for rule in rules.values()}
    external_distributions = {dependency_name(distribution): root_name for root_name, distribution in external.items()}
    violations: list[Violation] = []
    for distribution, dependencies in declarations.items():
        rule = rules[distribution]
        manifest = rule.directory / "pyproject.toml"
        for dependency in sorted(dependencies):
            internal = internal_distributions.get(dependency)
            if internal is not None:
                if internal.import_root not in rule.allowed_internal:
                    violations.append(Violation(manifest, 0, "ARCH002", f"forbidden internal dependency: {internal.distribution}"))
                continue
            external_root = external_distributions.get(dependency)
            if external_root is None:
                violations.append(Violation(manifest, 0, "ARCH004", f"unmapped external dependency: {dependency}"))
            elif external_root not in rule.allowed_external:
                violations.append(Violation(manifest, 0, "ARCH004", f"forbidden external dependency: {external[external_root]}"))
    return violations


def validate_workspace(root: Path, rules: dict[str, PackageRule]) -> list[Violation]:
    path = root / "pyproject.toml"
    try:
        with path.open("rb") as handle:
            raw = tomllib.load(handle)
    except (FileNotFoundError, tomllib.TOMLDecodeError, OSError) as error:
        return [Violation(Path("pyproject.toml"), 0, "ARCH006", f"invalid workspace manifest: {error}")]

    tool = raw.get("tool", {})
    uv = tool.get("uv", {}) if isinstance(tool, dict) else {}
    workspace = uv.get("workspace", {}) if isinstance(uv, dict) else {}
    sources = uv.get("sources", {}) if isinstance(uv, dict) else {}
    members = workspace.get("members", []) if isinstance(workspace, dict) else []
    if not isinstance(members, list) or not all(isinstance(member, str) for member in members):
        return [Violation(Path("pyproject.toml"), 0, "ARCH006", "workspace members must be a string list")]
    if not isinstance(sources, dict):
        return [Violation(Path("pyproject.toml"), 0, "ARCH006", "workspace sources must be a table")]

    violations: list[Violation] = []
    for distribution, rule in rules.items():
        directory = rule.directory.as_posix()
        if not any(fnmatchcase(directory, member) for member in members):
            violations.append(Violation(Path("pyproject.toml"), 0, "ARCH006", f"workspace member missing: {directory}"))
        if sources.get(distribution) != {"workspace": True}:
            violations.append(Violation(Path("pyproject.toml"), 0, "ARCH006", f"workspace source binding invalid: {distribution}"))
    return violations


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
        self.builtins_names = {"builtins"}
        self.sys_names = {"sys"}
        self.sys_path_names: set[str] = set()

    def collect_aliases(self, tree: ast.AST) -> None:
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root_name = alias.name.split(".", 1)[0]
                    if root_name == "importlib":
                        self.importlib_names.add(alias.asname or root_name)
                    elif root_name == "builtins":
                        self.builtins_names.add(alias.asname or root_name)
                    elif root_name == "sys":
                        self.sys_names.add(alias.asname or root_name)
            elif isinstance(node, ast.ImportFrom) and not node.level:
                if node.module == "importlib":
                    for alias in node.names:
                        if alias.name == "import_module":
                            self.dynamic_names.add(alias.asname or alias.name)
                elif node.module == "builtins":
                    for alias in node.names:
                        if alias.name == "__import__":
                            self.dynamic_names.add(alias.asname or alias.name)
                elif node.module == "sys":
                    for alias in node.names:
                        if alias.name == "path":
                            self.sys_path_names.add(alias.asname or alias.name)

        assignments: list[tuple[set[str], ast.AST]] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                assignments.append((
                    {target.id for target in node.targets if isinstance(target, ast.Name)},
                    node.value,
                ))
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
                assignments.append(({node.target.id}, node.value))
            elif isinstance(node, ast.NamedExpr) and isinstance(node.target, ast.Name):
                assignments.append(({node.target.id}, node.value))
        changed = True
        while changed:
            changed = False
            for names, value in assignments:
                if self.is_dynamic_import_callable(value):
                    before = len(self.dynamic_names)
                    self.dynamic_names.update(names)
                    changed = changed or len(self.dynamic_names) != before
                elif self.is_sys_path(value):
                    before = len(self.sys_path_names)
                    self.sys_path_names.update(names)
                    changed = changed or len(self.sys_path_names) != before

    def is_dynamic_import_callable(self, node: ast.AST) -> bool:
        if isinstance(node, ast.NamedExpr):
            return self.is_dynamic_import_callable(node.value)
        if isinstance(node, ast.Name):
            return node.id in self.dynamic_names
        return (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and (
                (node.value.id in self.importlib_names and node.attr == "import_module")
                or (node.value.id in self.builtins_names and node.attr == "__import__")
            )
        )

    def is_dangerous_primitive_reference(self, node: ast.AST) -> bool:
        """Recognize the primitives before aliases or containers can obscure them."""
        return isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and (
            (node.value.id in self.importlib_names and node.attr == "import_module")
            or (node.value.id in self.builtins_names and node.attr == "__import__")
            or (node.value.id in self.sys_names and node.attr == "path")
        )

    def is_dangerous_primitive_alias_reference(self, node: ast.AST) -> bool:
        return isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and (
            node.id in self.dynamic_names or node.id in self.sys_path_names
        )

    def contains_dangerous_primitive_reference(self, node: ast.AST) -> bool:
        return any(
            self.is_dangerous_primitive_reference(candidate)
            or self.is_dangerous_primitive_alias_reference(candidate)
            for candidate in ast.walk(node)
        )

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
            self.check_import(node, alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.level or node.module is None:
            return
        self.check_import(node, node.module)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if self.is_dangerous_primitive_reference(node):
            message = "sys.path reference is forbidden" if node.attr == "path" else "dynamic import primitive reference is forbidden"
            self.add(node, "ARCH005", message, None)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if self.is_dangerous_primitive_alias_reference(node):
            message = "sys.path reference is forbidden" if node.id in self.sys_path_names else "dynamic import primitive reference is forbidden"
            self.add(node, "ARCH005", message, None)
        self.generic_visit(node)

    def is_sys_path(self, node: ast.AST) -> bool:
        if isinstance(node, ast.NamedExpr):
            return self.is_sys_path(node.value)
        if isinstance(node, ast.Name):
            return node.id in self.sys_path_names
        if isinstance(node, ast.Attribute):
            return isinstance(node.value, ast.Name) and node.value.id in self.sys_names and node.attr == "path"
        return isinstance(node, ast.Subscript) and self.is_sys_path(node.value)

    def visit_Call(self, node: ast.Call) -> None:
        function = node.func
        if self.is_dynamic_import_callable(function) and not self.contains_dangerous_primitive_reference(function):
            self.add(node, "ARCH005", "dynamic import is forbidden", None)
        if (
            isinstance(function, ast.Attribute)
            and self.is_sys_path(function.value)
            and not self.contains_dangerous_primitive_reference(function.value)
        ):
            self.add(node, "ARCH005", "sys.path mutation is forbidden", None)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> None:
        if any(
            self.is_sys_path(target) and not self.contains_dangerous_primitive_reference(target)
            for target in node.targets
        ) and not self.is_sys_path(node.value):
            self.add(node, "ARCH005", "sys.path mutation is forbidden", None)
        self.generic_visit(node)

    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        if self.is_sys_path(node.target) and not self.contains_dangerous_primitive_reference(node.target):
            self.add(node, "ARCH005", "sys.path mutation is forbidden", None)
        self.generic_visit(node)

    def visit_Delete(self, node: ast.Delete) -> None:
        if any(
            self.is_sys_path(target) and not self.contains_dangerous_primitive_reference(target)
            for target in node.targets
        ):
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
        if not REPOSITORY_ISSUE_URL.fullmatch(entry["issue"]):
            errors.append(architecture_error(root, f"exception {identifier} has invalid issue URL"))
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
    violations.extend(validate_workspace(root, rules))
    declarations, manifest_violations = read_manifests(root, rules)
    violations.extend(manifest_violations)
    violations.extend(validate_declared_dependencies(root, declarations, rules, external))
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
            visitor.collect_aliases(tree)
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
