"""Exact consumer-policy pins, not a copied owner descriptor or schema."""

PROFILE = "plumber.og.operational/v1"
SOURCE = "8c30f70e217722e719c5aedc322219ebccb87e68"
WHEEL_SHA256 = "e5bc586a3da76d8e11760b39c9d7ac45b62b1240f085a8a96a573b9902bfea12"
DESCRIPTOR_SHA256 = "bcc6ac607706e934e5df4e044802aa74c7d7455e7711220df116080f1ab0cc70"
# SHA-256 of canonical JSON derived from the authenticated descriptor bytes.
# This verifies describe's entire parsed document without vendoring that resource.
DESCRIBE_CANONICAL_SHA256 = (
    "e019be03aba8edd338bc952b01ff3253d4d53eaee39d9d0b94ec947ff00bd733"
)
VERSIONS = {"plumber": "2.1.0a3", "parser": "1.9.0", "python": "3.12.14"}
MAX_NODES = 1024
MAX_EDGES = 4096
MAX_STDOUT = 4 * 1024 * 1024
MAX_STDERR = 512
MAX_SECONDS = 180.0
READ_CONTRACT = "plumber.graph.read/v1"
TOPOLOGY_CONTRACT = "plumber.graph.topology/v1"
ERROR_EXITS = {
    "usage": 2,
    "expectation_mismatch": 3,
    "source_rejected": 4,
    "bounds_exceeded": 5,
    "source_changed": 6,
    "unsupported_platform": 7,
    "unsupported_dependency": 8,
    "audit_hook_unavailable": 9,
    "internal": 70,
}
