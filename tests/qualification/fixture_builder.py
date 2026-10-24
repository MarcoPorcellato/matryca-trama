"""Trusted builder for fresh, authenticated qualification fixtures only."""

import hashlib
import json
import os
import stat
import tempfile
from pathlib import Path, PurePosixPath

from trama_plumber_client._fixture import SyntheticFixture, _created_fixture
import resources


def build_fixture(
    root: Path, wheel: Path, inputs: dict, manifest: dict
) -> SyntheticFixture:
    """Create a new owned graph; never authenticate an existing arbitrary root."""
    parent = root / "synthetic"
    parent.mkdir(exist_ok=False)
    graph = Path(tempfile.mkdtemp(prefix="graph-", dir=parent)).resolve()
    files = manifest["files"]
    resources.require(0 < len(files) <= 1024, "fixture manifest file bound rejected")
    total = 0
    for logical, expected in files.items():
        path = PurePosixPath(logical)
        resources.require(
            not path.is_absolute()
            and len(path.parts) >= 2
            and all(part not in ("", ".", "..") for part in path.parts)
            and "\\" not in logical
            and path.parts[0] in ("pages", "journals")
            and path.suffix == ".md",
            "fixture path rejected",
        )
        raw = resources.read_member(
            wheel, inputs["resource_prefix"] + "fixtures/" + logical
        )
        total += len(raw)
        resources.require(
            len(raw) <= 1048576
            and total <= 16777216
            and hashlib.sha256(raw).hexdigest() == expected["sha256"],
            "fixture digest or byte bound mismatch",
        )
        destination = graph.joinpath(*path.parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as stream:
            stream.write(raw)
    alias = root / "input-alias"
    alias.symlink_to(graph, target_is_directory=True)
    return _created_fixture(str(root), str(graph), str(alias))


def build_file_bound_control(root: Path) -> Path:
    """Harness-only 1025-file refusal control; never issue a client capability."""
    graph = root / "file-bound-control"
    graph.mkdir(exist_ok=False)
    pages = graph / "pages"
    pages.mkdir(exist_ok=False)
    for ordinal in range(1025):
        with (pages / f"synthetic-{ordinal:04d}.md").open("xb") as stream:
            stream.write(b"- synthetic bound control\n")
    return graph


def file_bound_ledger(graph: Path) -> dict:
    """Fixed-shape fingerprint for only the separately built 1025-file control."""
    pages = graph / "pages"
    expected = {f"synthetic-{ordinal:04d}.md" for ordinal in range(1025)}
    names = set()
    with os.scandir(pages) as entries:
        for entry in entries:
            resources.require(
                len(names) < 1025 and entry.name in expected,
                "file-bound control entry mismatch",
            )
            names.add(entry.name)
    resources.require(names == expected, "file-bound control is incomplete")
    rows = []
    for name in sorted(expected):
        path = pages / name
        metadata = path.lstat()
        resources.require(
            stat.S_ISREG(metadata.st_mode) and metadata.st_size == 26,
            "file-bound control file rejected",
        )
        raw = path.read_bytes()
        resources.require(
            raw == b"- synthetic bound control\n", "file-bound control changed"
        )
        rows.append(
            (
                name,
                metadata.st_mode,
                metadata.st_size,
                metadata.st_ino,
                metadata.st_mtime_ns,
                hashlib.sha256(raw).hexdigest(),
            )
        )
    return {
        "files": 1025,
        "sha256": hashlib.sha256(
            json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
    }
