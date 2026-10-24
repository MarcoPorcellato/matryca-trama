"""Qualification-only compatibility import for the single package-owned reader."""

from pathlib import Path
import sys

SOURCE = Path(__file__).resolve().parents[2] / "packages/plumber-client/src"
PROJECT = Path(__file__).resolve().parents[2]
for package in ("contracts", "core", "plumber-client"):
    source = PROJECT / "packages" / package / "src"
    if source.resolve() != source:
        raise RuntimeError("qualification package source is not canonical")
    sys.path.insert(0, str(source))

import trama_contracts  # noqa: E402 - verify the inward package before core loads it.

contracts_init = PROJECT / "packages/contracts/src/trama_contracts/__init__.py"
if (
    Path(trama_contracts.__file__).resolve() != contracts_init
    or Path(trama_contracts.__spec__.origin).resolve() != contracts_init
):
    raise RuntimeError("qualification contracts origin mismatch")

import trama_core  # noqa: E402

core_init = PROJECT / "packages/core/src/trama_core/__init__.py"
if (
    Path(trama_core.__file__).resolve() != core_init
    or Path(trama_core.__spec__.origin).resolve() != core_init
):
    raise RuntimeError("qualification core origin mismatch")

import trama_plumber_client  # noqa: E402 - admit this repository's source first.

expected = SOURCE / "trama_plumber_client"
if (
    Path(trama_plumber_client.__file__).resolve() != expected / "__init__.py"
    or Path(trama_plumber_client.__spec__.origin).resolve() != expected / "__init__.py"
):
    raise RuntimeError("qualification package origin mismatch")

from trama_plumber_client import _process  # noqa: E402

if (
    Path(_process.__file__).resolve() != expected / "_process.py"
    or Path(_process.__spec__.origin).resolve() != expected / "_process.py"
):
    raise RuntimeError("qualification process origin mismatch")

ProcessResult = _process.ProcessResult
ProcessFailure = _process.ProcessFailure
run_process = _process.run_process
os = _process.os


if __name__ == "__main__":
    import unittest

    suites = [
        unittest.TestLoader().discover(str(PROJECT / "tests/client")),
        unittest.TestLoader().discover(
            str(PROJECT / "tests/core"), pattern="test_graph_gateway.py"
        ),
    ]
    result = unittest.TextTestRunner(verbosity=1).run(unittest.TestSuite(suites))
    raise SystemExit(not result.wasSuccessful())
