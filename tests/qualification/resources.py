"""Bounded artifact and fixture handling for the synthetic qualification lane."""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import zipfile
from importlib.machinery import all_suffixes
from pathlib import Path
from typing import NoReturn


class QualificationFailure(RuntimeError):
    """A failed evidence check, never implicit permission to retry or admit."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise QualificationFailure(message)


def strict_json(raw: bytes) -> dict:
    require(len(raw) <= 4_194_304, "JSON byte ceiling exceeded")

    def pairs(items: list[tuple[str, object]]) -> dict[str, object]:
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON member")
            result[key] = value
        return result

    def constant(value: str) -> NoReturn:
        raise QualificationFailure("nonfinite JSON value")

    try:
        result = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    except (UnicodeError, ValueError, RecursionError) as error:
        raise QualificationFailure("invalid single JSON document") from error
    require(type(result) is dict, "JSON document must be an object")
    return result


def verify_file(path: Path, digest: str, size: int) -> None:
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and before.st_size == size, "artifact type/size mismatch")
    require(size <= 64 * 1024 * 1024, "artifact byte ceiling exceeded")
    with path.open("rb") as stream:
        raw = stream.read(size + 1)
    after = path.lstat()
    require(
        (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns)
        == (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns),
        "artifact changed",
    )
    require(
        len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, "artifact digest mismatch"
    )


def read_member(wheel: Path, name: str, *, limit: int = 1_048_576) -> bytes:
    with zipfile.ZipFile(wheel) as archive:
        members = archive.infolist()
        require(len(members) <= 4096, "archive member ceiling exceeded")
        require(
            len({member.filename for member in members}) == len(members),
            "duplicate archive members",
        )
        matches = [member for member in members if member.filename == name]
        require(len(matches) == 1, "required exact archive member absent")
        member = matches[0]
        mode = member.external_attr >> 16
        require(
            not member.is_dir() and (stat.S_IFMT(mode) == 0 or stat.S_ISREG(mode)),
            "archive member is not regular",
        )
        require(
            member.file_size <= limit and not member.flag_bits & 1,
            "archive member ceiling/encryption rejected",
        )
        with archive.open(member) as stream:
            raw = stream.read(limit + 1)
        require(len(raw) == member.file_size and len(raw) <= limit, "archive member size mismatch")
        return raw


def owner_resource(wheel: Path, inputs: dict, name: str) -> bytes:
    require(name in inputs["resources"], "resource is not allowlisted")
    raw = read_member(wheel, inputs["resource_prefix"] + name)
    require(
        hashlib.sha256(raw).hexdigest() == inputs["resources"][name],
        "owner resource digest mismatch",
    )
    return raw


def check_site_packages(site: Path, expected: list[str]) -> None:
    require(site.is_dir() and not site.is_symlink(), "site-packages unavailable")
    roots = set()
    count = 0
    for parent, directories, files in os.walk(site, followlinks=False):
        for name in directories + files:
            count += 1
            require(count <= 4096, "consumer environment entry ceiling exceeded")
            path = Path(parent) / name
            require(not path.is_symlink(), "consumer environment symlink rejected")
            require(
                not name.endswith(".pth")
                and name
                not in ("sitecustomize", "usercustomize", "sitecustomize.py", "usercustomize.py"),
                "consumer startup hook rejected",
            )
            if Path(parent) == site:
                if (
                    path.is_dir()
                    and not name.endswith((".dist-info", ".egg-info"))
                    and name != "__pycache__"
                ):
                    roots.add(name)
                elif path.is_file():
                    for suffix in sorted(all_suffixes(), key=len, reverse=True):
                        if name.endswith(suffix):
                            roots.add(name[: -len(suffix)])
                            break
    require(roots == set(expected), "consumer top-level import roots mismatch")


def fixture_ledger(root: Path) -> dict:
    require(root.is_dir() and not root.is_symlink(), "fixture root rejected")
    result = {}
    total = 0
    for parent, directories, files in os.walk(root, followlinks=False):
        for name in sorted(directories + files):
            path = Path(parent) / name
            metadata = path.lstat()
            require(
                stat.S_ISDIR(metadata.st_mode) or stat.S_ISREG(metadata.st_mode),
                "fixture nonregular entry rejected",
            )
            require(len(result) < 1024, "fixture entry ceiling exceeded")
            row = {
                "mode": metadata.st_mode,
                "size": metadata.st_size,
                "mtime_ns": metadata.st_mtime_ns,
                "inode": metadata.st_ino,
            }
            if path.is_file():
                require(metadata.st_size <= 1_048_576, "fixture file ceiling exceeded")
                raw = path.read_bytes()
                total += len(raw)
                require(total <= 16_777_216, "fixture total ceiling exceeded")
                row["sha256"] = hashlib.sha256(raw).hexdigest()
            result[path.relative_to(root).as_posix()] = row
    return result


def sanitize(raw: bytes, *, replacements: dict[str, str]) -> bytes:
    text = raw.decode("utf-8", errors="backslashreplace")
    for value, replacement in sorted(
        replacements.items(), key=lambda item: len(item[0]), reverse=True
    ):
        if value:
            text = text.replace(value, replacement)
    text = re.sub(
        r"(?<![A-Za-z0-9])(?:gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+)",
        "<redacted-token>",
        text,
    )
    return text.encode("utf-8")
