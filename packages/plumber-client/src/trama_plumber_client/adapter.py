"""Synthetic-only outer adapter; Plumber remains the sole graph reader."""

from __future__ import annotations

import errno
import os
import stat

from trama_core.graph_values import (
    GraphGatewayError,
    GraphGatewayErrorCode as Code,
    GraphSnapshot,
)

from . import _mapping, _profile
from ._fixture import SyntheticFixture, fixture_root
from ._process import ProcessFailure, ProcessResult, run_process


class PlumberClientAdapter:
    """One admitted fixture, explicit producer venv and no retry or graph selector."""

    def __init__(
        self,
        python: str,
        fixture: SyntheticFixture,
        *,
        expected_resolved_python: str,
        timeout_seconds: float = _profile.MAX_SECONDS,
        stdout_limit: int = _profile.MAX_STDOUT,
        stderr_limit: int = _profile.MAX_STDERR,
    ) -> None:
        fixture_root(fixture)
        if (
            type(python) is not str
            or not os.path.isabs(python)
            or "\x00" in python
            or type(expected_resolved_python) is not str
            or not os.path.isabs(expected_resolved_python)
            or type(timeout_seconds) not in (int, float)
            or not 0 < timeout_seconds <= _profile.MAX_SECONDS
            or type(stdout_limit) is not int
            or not 0 < stdout_limit <= _profile.MAX_STDOUT
            or type(stderr_limit) is not int
            or not 0 < stderr_limit <= _profile.MAX_STDERR
            or os.name != "posix"
            or (os.uname().sysname, os.uname().machine)
            not in (("Linux", "x86_64"), ("Darwin", "arm64"))
        ):
            raise GraphGatewayError(Code.CONFIGURATION_INVALID)
        self._python = (
            python  # Preserve venv spelling; never replace argv with realpath.
        )
        self._expected_python = expected_resolved_python
        self._fixture = fixture
        self._timeout = timeout_seconds
        self._stdout_limit = stdout_limit
        self._stderr_limit = stderr_limit
        self._python_identity = self._executable_identity()

    def _executable_identity(self) -> tuple[int, int, int, int]:
        try:
            if os.path.realpath(self._python) != self._expected_python:
                raise ValueError("resolved executable mismatch")
            status = os.stat(self._python)
            if not stat.S_ISREG(status.st_mode) or not os.access(self._python, os.X_OK):
                raise ValueError("executable is unavailable")
            return status.st_dev, status.st_ino, status.st_size, status.st_mtime_ns
        except (OSError, ValueError):
            raise GraphGatewayError(Code.CONFIGURATION_INVALID) from None

    @staticmethod
    def _require_cleanup(result: ProcessResult | ProcessFailure) -> None:
        if (
            result.cleanup_succeeded is not True
            or result.child_reaped is not True
            or result.group_probe_errno != errno.ESRCH
            or result.events
            or result.cleanup_exception is not None
        ):
            raise GraphGatewayError(Code.CLEANUP_UNCERTAIN)

    def _execute(self, operation: str) -> bytes:
        root = fixture_root(self._fixture)
        if self._executable_identity() != self._python_identity:
            raise GraphGatewayError(Code.CONFIGURATION_INVALID)
        argv = [
            self._python,
            "-I",
            "-B",
            "-m",
            "matryca_plumber.graph_gateway",
            operation,
        ]
        if operation == "snapshot":
            argv += [
                "--graph-root",
                root,
                "--expect-descriptor-sha256",
                _profile.DESCRIPTOR_SHA256,
            ]
        try:
            result = run_process(
                argv,
                timeout_seconds=self._timeout,
                stdout_limit=self._stdout_limit,
                stderr_limit=self._stderr_limit,
            )
        except ProcessFailure as error:
            self._require_cleanup(error)
            if error.reason == "nonzero_exit":
                if error.returncode is None:
                    raise GraphGatewayError(Code.PROTOCOL_VIOLATION) from None
                raise _mapping.error_from_bytes(
                    error.returncode, error.stdout, error.stderr
                ) from None
            code = {
                "timeout": Code.PROCESS_TIMEOUT,
                "output_limit": Code.PROCESS_OUTPUT_LIMIT,
            }.get(error.reason, Code.PROTOCOL_VIOLATION)
            raise GraphGatewayError(code) from None
        except Exception as error:
            evidence = getattr(error, "process_evidence", None)
            if isinstance(evidence, ProcessFailure):
                self._require_cleanup(evidence)
                raise GraphGatewayError(Code.PROTOCOL_VIOLATION) from None
            raise GraphGatewayError(Code.SPAWN_FAILED) from None
        self._require_cleanup(result)
        if result.stderr or result.returncode != 0:
            raise GraphGatewayError(Code.PROTOCOL_VIOLATION)
        if len(result.stdout) > self._stdout_limit:
            raise GraphGatewayError(Code.PROCESS_OUTPUT_LIMIT)
        return result.stdout

    def describe(self) -> None:
        """Verify exact descriptor identity without returning an owner wire DTO."""
        _mapping.describe_from_bytes(self._execute("describe"))

    def snapshot(self) -> GraphSnapshot:
        """Return one complete mapped snapshot, never partial data or raw errors."""
        return _mapping.snapshot_from_bytes(self._execute("snapshot"))
