"""Trama-owned topology invariants, independent of a producer wire format."""

from dataclasses import FrozenInstanceError
import importlib
import importlib.util
import unittest


class GraphValueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.assertIsNotNone(
            importlib.util.find_spec("trama_core.graph_values"),
            "Trama domain graph values have not been implemented",
        )
        self.values = importlib.import_module("trama_core.graph_values")

    def node(self, identifier, kind="block", parent="page", ordinal=0):
        return self.values.TopologyNode(
            identifier, self.values.NodeKind(kind), parent, ordinal
        )

    def topology(self, nodes, edges=()):
        return self.values.GraphTopology("topology", tuple(nodes), tuple(edges))

    def test_canonical_preorder_and_local_sibling_ordinals_are_accepted(self):
        nodes = (
            self.node("page", "page", None),
            self.node("a"),
            self.node("nested", parent="a"),
            self.node("b", ordinal=1),
            self.node("page2", "page", None, 1),
            self.node("c", parent="page2"),
        )
        edge = self.values.ReferenceEdge("nested", "page2")
        topology = self.topology(nodes, [edge])
        self.assertEqual(topology.nodes, nodes)
        self.assertEqual(topology.edges, (edge,))
        with self.assertRaises(FrozenInstanceError):
            topology.nodes = ()

    def test_empty_complete_topology_is_valid(self):
        self.assertEqual(self.topology(()).nodes, ())

    def test_duplicate_ids_and_orphan_parent_are_rejected(self):
        page = self.node("page", "page", None)
        for nodes in ((page, page), (page, self.node("child", parent="absent"))):
            with self.subTest(nodes=nodes), self.assertRaises(ValueError):
                self.topology(nodes)

    def test_reentering_a_finished_parent_subtree_is_rejected(self):
        with self.assertRaises(ValueError):
            self.topology(
                (
                    self.node("page", "page", None),
                    self.node("a"),
                    self.node("b", ordinal=1),
                    self.node("late", parent="a"),
                )
            )

    def test_gapped_root_or_sibling_ordinals_are_rejected(self):
        page = self.node("page", "page", None)
        for nodes in (
            (self.node("x", "page", None, 1),),
            (page, self.node("a", ordinal=1)),
        ):
            with self.subTest(nodes=nodes), self.assertRaises(ValueError):
                self.topology(nodes)

    def test_roots_are_pages_and_only_blocks_have_parents(self):
        for nodes in (
            (self.node("root", "block", None),),
            (self.node("page", "page", None), self.node("nested-page", "page")),
        ):
            with self.subTest(nodes=nodes), self.assertRaises(ValueError):
                self.topology(nodes)

    def test_dangling_and_duplicate_references_are_rejected(self):
        nodes = (self.node("page", "page", None), self.node("child"))
        edge = self.values.ReferenceEdge("child", "page")
        for edges in ((edge, edge), (self.values.ReferenceEdge("absent", "page"),)):
            with self.subTest(edges=edges), self.assertRaises(ValueError):
                self.topology(nodes, edges)

    def test_boolean_and_negative_ordinals_are_rejected(self):
        for ordinal in (True, -1, 1.0):
            with self.subTest(ordinal=ordinal), self.assertRaises(ValueError):
                self.node("child", ordinal=ordinal)

    def test_gateway_errors_are_sanitized_and_non_retryable(self):
        error = self.values.GraphGatewayError(
            self.values.GraphGatewayErrorCode.CONTRACT_VIOLATION
        )
        self.assertEqual(str(error), "contract_violation")
        self.assertFalse(error.retryable)

    def test_domain_port_is_a_narrow_snapshot_protocol(self):
        gateway = importlib.import_module("trama_core.graph_gateway")
        self.assertTrue(getattr(gateway.KnowledgeGraphGateway, "_is_protocol", False))
        self.assertTrue(callable(gateway.KnowledgeGraphGateway.snapshot))


if __name__ == "__main__":
    unittest.main()
