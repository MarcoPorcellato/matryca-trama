"""Validation and compatibility rules for read requests."""

from .models import CONTRACT_ID, Outcome, ReadRequest


_OPERATIONS = frozenset(
    {
        "graph.identify",
        "page.read",
        "block.subtree.read.complete",
    }
)


def validate_request(request: ReadRequest) -> Outcome | None:
    """Return a stable rejection outcome when a request is not valid."""

    if not isinstance(request, ReadRequest):
        return Outcome.INVALID_REQUEST
    if request.contract_id != CONTRACT_ID or request.accepted_contract_major != 1:
        return Outcome.INCOMPATIBLE
    if not _is_nonempty_text(request.operation) or request.operation not in _OPERATIONS:
        return Outcome.INVALID_REQUEST
    if not _is_nonempty_text(request.request_id):
        return Outcome.INVALID_REQUEST
    if not _is_nonempty_text(request.graph_selector):
        return Outcome.INVALID_REQUEST
    if request.operation == "page.read" and not _is_nonempty_text(
        request.page_reference
    ):
        return Outcome.INVALID_REQUEST
    if request.operation == "block.subtree.read.complete" and not _is_nonempty_text(
        request.block_reference
    ):
        return Outcome.INVALID_REQUEST
    return None


def _is_nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())
