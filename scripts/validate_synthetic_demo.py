"""Project the explicitly admitted synthetic app boundary into static checks."""

import ast
from pathlib import Path

FILES = {
    "__init__.py",
    "__main__.py",
    "scenario.py",
    "presentation.py",
    "build.py",
    "preview.py",
}
ALLOWED = {
    "__init__.py": set(),
    "__main__.py": {"argparse"},
    "scenario.py": {"trama_core.graph_values", "trama_core.graph_gateway"},
    "presentation.py": set(),
    "build.py": {"base64", "hashlib", "html", "json", "os", "pathlib", "stat", "re"},
    "preview.py": {"http.server"},
}
OS_CALLS = {"open", "close", "mkdir", "fdopen", "fstat", "ftruncate"}
OS_FLAGS = {
    "O_RDONLY",
    "O_DIRECTORY",
    "O_NOFOLLOW",
    "O_WRONLY",
    "O_CREAT",
    "O_NONBLOCK",
}


def app_violations(source: str, filename: str) -> list[str]:
    errors = []
    if filename not in FILES:
        return ["unadmitted application module"]
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return ["invalid Python source"]
    aliases = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                aliases[name.asname or name.name] = name.name
                if name.name not in ALLOWED[filename]:
                    errors.append("unadmitted import: " + name.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                if node.level != 1 or (node.module or "") + ".py" not in FILES:
                    errors.append("nonlocal application import")
            elif node.module not in ALLOWED[filename] or node.module == "os":
                errors.append("unadmitted import: " + str(node.module))
        elif isinstance(node, ast.Name) and node.id in {
            "__import__",
            "eval",
            "exec",
            "compile",
            "getattr",
            "setattr",
            "open",
            "globals",
            "locals",
            "vars",
            "__builtins__",
        }:
            errors.append("dynamic execution/import escape")
        elif isinstance(node, ast.Attribute):
            if (
                node.attr in {"path", "__dict__", "__subclasses__"}
                and isinstance(node.value, ast.Name)
                and node.value.id in {"sys", "builtins"}
            ):
                errors.append("path or dynamic namespace escape")
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if (
                aliases.get(node.value.id) == "os"
                and node.attr not in OS_CALLS | OS_FLAGS
            ):
                errors.append("unadmitted OS operation")
    return errors


def validate_application(root: Path) -> list[str]:
    directory = root / "apps/synthetic_demo"
    if directory.is_symlink() or not directory.is_dir():
        return ["missing admitted demo application"]
    errors = []
    for entry in (root / "apps").iterdir():
        if entry.name != "synthetic_demo" and (entry.is_dir() or entry.suffix == ".py"):
            errors.append("unadmitted application entry: " + entry.name)
    for path in directory.rglob("*.py"):
        name = path.relative_to(directory).as_posix()
        if path.is_symlink():
            errors.append(name + ": symlinked source")
            continue
        errors.extend(
            name + ": " + error for error in app_violations(path.read_text(), name)
        )
    return errors


if __name__ == "__main__":
    failures = validate_application(Path(__file__).resolve().parents[1])
    if failures:
        raise SystemExit("\n".join(failures))
    print("Synthetic demo application boundary passed.")
