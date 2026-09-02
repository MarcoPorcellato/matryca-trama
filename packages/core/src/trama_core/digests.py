"""Digest helpers for deterministic public evidence."""

from hashlib import sha256


def sha256_bytes(data: bytes) -> str:
    """Return the lowercase SHA-256 digest for immutable bytes."""

    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    return sha256(data).hexdigest()
