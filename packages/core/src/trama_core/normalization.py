"""Canonical JSON and containment checks for owned synthetic fixtures."""

from collections.abc import Mapping
import hmac
import json
from math import isfinite
from pathlib import Path, PurePosixPath

from .digests import sha256_bytes


_MANIFEST_PATH = PurePosixPath("fixture-manifest.json")


def canonical_json(value: Mapping[str, object]) -> bytes:
    """Encode supported JSON data into deterministic UTF-8 bytes."""

    normalized = _normalize_json_value(value)
    return json.dumps(
        normalized,
        allow_nan=False,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def resolve_fixture_path(root: Path, relative: PurePosixPath) -> Path:
    """Resolve one existing fixture path while enforcing its selected root."""

    if not isinstance(relative, PurePosixPath):
        raise TypeError("relative must be a PurePosixPath")
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("fixture path outside fixture root")

    root_resolved = root.resolve(strict=True)
    candidate = (root_resolved / Path(relative)).resolve(strict=True)
    if candidate != root_resolved and root_resolved not in candidate.parents:
        raise ValueError("fixture path outside fixture root")
    return candidate


def verified_fixture_path(root: Path, relative: PurePosixPath) -> Path:
    """Return a contained fixture path only after manifest-digest verification."""

    candidate = resolve_fixture_path(root, relative)
    manifest_path = resolve_fixture_path(root, _MANIFEST_PATH)
    manifest = _load_manifest(manifest_path)
    path_key = relative.as_posix()
    expected_digest = manifest.get(path_key)
    if not isinstance(expected_digest, str):
        raise ValueError("fixture digest missing from manifest")
    actual_digest = sha256_bytes(candidate.read_bytes())
    if not hmac.compare_digest(expected_digest, actual_digest):
        raise ValueError("fixture digest mismatch")
    return candidate


def _load_manifest(manifest_path: Path) -> Mapping[str, str]:
    try:
        raw_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError("fixture manifest is invalid") from error
    if not isinstance(raw_manifest, dict):
        raise ValueError("fixture manifest is invalid")
    files = raw_manifest.get("files")
    if not isinstance(files, dict) or not all(
        isinstance(path, str) and isinstance(digest, str)
        for path, digest in files.items()
    ):
        raise ValueError("fixture manifest is invalid")
    return files


def _normalize_json_value(value: object) -> object:
    if isinstance(value, Mapping):
        normalized: dict[str, object] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError("JSON object keys must be strings")
            normalized[key] = _normalize_json_value(item)
        return normalized
    if isinstance(value, (list, tuple)):
        return [_normalize_json_value(item) for item in value]
    if isinstance(value, float) and not isfinite(value):
        raise ValueError("JSON numbers must be finite")
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError("value contains unsupported JSON data")
