import importlib
import unittest


class WorkspaceTest(unittest.TestCase):
    def test_public_packages_import(self) -> None:
        for name in (
            "trama_contracts",
            "trama_core",
            "trama_parser_bridge",
            "trama_logseq_og_adapter",
            "trama_plumber_bridge",
        ):
            self.assertIsNotNone(importlib.import_module(name))
