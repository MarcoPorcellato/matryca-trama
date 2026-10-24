"""Narrow inward-facing port for a complete, content-free graph snapshot."""

from typing import Protocol

from .graph_values import GraphSnapshot


class KnowledgeGraphGateway(Protocol):
    def snapshot(self) -> GraphSnapshot:
        """Return one complete snapshot or raise a non-retryable domain error."""
        ...
