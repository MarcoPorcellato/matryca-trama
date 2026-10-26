"""Metadata-first boundaries for unsupported maintainer-local test tooling."""

from __future__ import annotations

import os
import platform
import re
import stat
from contextlib import ExitStack
from pathlib import Path

TEMP_PARENT = Path("/private/tmp")


class LocalFailure(RuntimeError):
    """A refused local diagnostic, never admission or implicit retry authority."""


def require_local_context() -> None:
    """Reject CI and approximate runtimes before inspecting a task root."""
    if any(
        os.environ.get(name, "").strip().lower() not in ("", "0", "false", "no")
        for name in ("CI", "GITHUB_ACTIONS", "GITHUB_RUN_ID")
    ):
        raise LocalFailure("MA is local-only")
    if (
        platform.system(),
        platform.machine(),
        platform.python_version(),
        platform.python_implementation(),
    ) != ("Darwin", "arm64", "3.12.14", "CPython"):
        raise LocalFailure("MA exact local runtime unavailable")


def admit_root(root: Path, *, fresh: bool) -> Path:
    """Admit only a canonical, private direct child of the fixed temp parent."""
    if (
        not isinstance(root, Path)
        or not root.is_absolute()
        or root.parent != TEMP_PARENT
        or re.fullmatch(r"trama-ma-[A-Za-z0-9_.-]{1,64}", root.name) is None
    ):
        raise LocalFailure("MA task root rejected")
    if Path(os.path.realpath(TEMP_PARENT)) != TEMP_PARENT:
        raise LocalFailure("MA task root parent is not canonical")
    try:
        metadata = os.lstat(root)
    except FileNotFoundError:
        if fresh:
            return root
        raise LocalFailure("MA task root absent") from None
    if (
        fresh
        or not stat.S_ISDIR(metadata.st_mode)
        or metadata.st_uid != os.getuid()
        or metadata.st_mode & 0o077
        or Path(os.path.realpath(root)) != root
    ):
        raise LocalFailure("MA task root ownership, type or freshness rejected")
    return root


def task_path(root: Path, relative: str, *, directory: bool = False) -> Path:
    """Admit fixed owned ancestors without following task-child symlinks."""
    selected = Path(relative)
    if selected.is_absolute() or not selected.parts or ".." in selected.parts:
        raise LocalFailure("MA task-relative path rejected")
    metadata = root.lstat()
    if (
        not stat.S_ISDIR(metadata.st_mode)
        or metadata.st_uid != os.getuid()
        or metadata.st_mode & 0o077
        or root.resolve(strict=True) != root
    ):
        raise LocalFailure("MA private task directory changed")
    path = root
    for index, component in enumerate(selected.parts):
        path = path / component
        metadata = path.lstat()
        expected_directory = directory or index < len(selected.parts) - 1
        if metadata.st_uid != os.getuid() or not (
            stat.S_ISDIR(metadata.st_mode) if expected_directory else stat.S_ISREG(metadata.st_mode)
        ):
            raise LocalFailure("MA task child type, owner or link rejected")
    return path


def read_task_file(root: Path, relative: str, limit: int) -> bytes:
    """Use no-follow descriptor-relative reads with pre-open type/size gates."""
    path = task_path(root, relative)
    if type(limit) is not int or not 0 < limit <= 4_194_304 or path.lstat().st_size > limit:
        raise LocalFailure("MA task file byte ceiling rejected")
    with ExitStack() as owned:
        directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        owned.callback(os.close, directory)
        for component in Path(relative).parts[:-1]:
            directory = os.open(
                component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory
            )
            owned.callback(os.close, directory)
        name = Path(relative).name
        before = os.stat(name, dir_fd=directory, follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode) or before.st_size > limit:
            raise LocalFailure("MA task leaf type or size changed")
        descriptor = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        owned.callback(os.close, descriptor)
        opened = os.fstat(descriptor)

        def identity(item: os.stat_result) -> tuple[int, int, int, int]:
            return item.st_dev, item.st_ino, item.st_size, item.st_mtime_ns

        if identity(before) != identity(opened):
            raise LocalFailure("MA task file changed before read")
        raw = bytearray()
        while chunk := os.read(descriptor, min(65_536, limit + 1 - len(raw))):
            raw.extend(chunk)
            if len(raw) > limit:
                raise LocalFailure("MA task file grew beyond its ceiling")
        if len(raw) != before.st_size or identity(before) != identity(os.fstat(descriptor)):
            raise LocalFailure("MA task file changed during read")
    return bytes(raw)
