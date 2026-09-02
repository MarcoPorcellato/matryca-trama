"""Public read-only adapter for verified synthetic OG fixtures."""

from .adapter import OgReadAdapter, build_og_payload, og_provenance

__all__ = ["OgReadAdapter", "build_og_payload", "og_provenance"]
