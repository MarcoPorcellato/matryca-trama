"""Translate validated core values to an explicitly fictional browser view."""

from .scenario import ANNOTATIONS, SyntheticDemoGateway


def demo_view() -> dict[str, object]:
    snapshot = SyntheticDemoGateway().snapshot()
    degree = {node.id: 0 for node in snapshot.topology.nodes}
    for edge in snapshot.topology.edges:
        degree[edge.source_id] += 1
        degree[edge.target_id] += 1
    nodes = []
    for node, annotation in zip(snapshot.topology.nodes, ANNOTATIONS, strict=True):
        label, category, spaces, description, x, y = annotation
        nodes.append(
            dict(
                id=node.id,
                label=label,
                category=category,
                spaces=list(spaces),
                description=description,
                degree=degree[node.id],
                x=x,
                y=y,
            )
        )
    return {
        "synthetic": True,
        "nodes": nodes,
        "edges": [
            dict(id=f"e{i}", **{"from": e.source_id, "to": e.target_id})
            for i, e in enumerate(snapshot.topology.edges)
        ],
    }
