"""Read-only loading of verified Trama-owned OG fixtures."""

from pathlib import Path, PurePosixPath

from logseq_matryca_parser import LogseqGraph
from trama_core import verified_fixture_directory


def load_og_fixture(fixture_root: Path, relative: PurePosixPath) -> LogseqGraph:
    """Load one verified synthetic OG fixture directory through Parser's public API."""

    verified_directory = verified_fixture_directory(fixture_root, relative)
    return LogseqGraph.load_directory(verified_directory)
