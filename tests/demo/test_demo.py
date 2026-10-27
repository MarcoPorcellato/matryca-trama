"""Behavior and authority boundaries for the fictional graph application."""

import copy
import hashlib
import http.client
from html.parser import HTMLParser
from http.server import HTTPServer
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

from apps.synthetic_demo.scenario import SyntheticDemoGateway
from apps.synthetic_demo.presentation import demo_view
from apps.synthetic_demo import build, preview
from scripts.validate_synthetic_demo import app_violations, validate_application

ROOT = Path(__file__).resolve().parents[2]


class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags, self.external, self.policy, self.language = [], [], "", ""

    def handle_starttag(self, tag, attrs):
        self.tags.append(tag)
        if tag == "html":
            self.language = dict(attrs).get("lang", "")
        self.external.extend(
            v for k, v in attrs if k in {"src", "href"} and v and not v.startswith("#")
        )
        if tag == "meta" and dict(attrs).get("http-equiv") == "Content-Security-Policy":
            self.policy = dict(attrs)["content"]


class DemoTests(unittest.TestCase):
    def test_gateway_is_invented_and_has_complete_valid_topology(self):
        snapshot = SyntheticDemoGateway().snapshot()
        self.assertEqual(len(snapshot.topology.nodes), 24)
        self.assertEqual(snapshot.identity.graph_id, "synthetic-demo")
        self.assertEqual(snapshot.provenance.producer_version, "synthetic-demo")
        ids = {n.id for n in snapshot.topology.nodes}
        self.assertTrue(
            all(
                e.source_id in ids and e.target_id in ids
                for e in snapshot.topology.edges
            )
        )
        self.assertTrue(all(n.parent_id is None for n in snapshot.topology.nodes))

    def test_annotations_are_fictional_presentation_not_payload(self):
        view = demo_view()
        self.assertTrue(view["synthetic"])
        self.assertEqual(len(view["nodes"]), 24)
        self.assertEqual(
            {n["category"] for n in view["nodes"]},
            {"note", "project", "journal", "tag"},
        )
        self.assertTrue(all(n["label"] and n["description"] for n in view["nodes"]))
        self.assertNotIn("producer_artifact_sha256", view)

    def test_script_like_labels_remain_data_not_markup(self):
        view = copy.deepcopy(demo_view())
        payload = '@@SCRIPTS@@ </script><img src=x onerror="alert(1)"> & \u2028'
        view["nodes"][0]["label"] = payload
        encoded = build.script_json(view)
        self.assertNotIn("<", encoded)
        self.assertEqual(json.loads(encoded)["nodes"][0]["label"], payload)
        with patch.object(build, "demo_view", return_value=view):
            parsed = Markup()
            parsed.feed(build.render_document())
        self.assertNotIn("img", parsed.tags)
        self.assertEqual(parsed.tags.count("script"), 4)

    def test_document_is_deterministic_self_contained_and_bounded(self):
        document = build.render_document()
        self.assertEqual(document, build.render_document())
        parsed = Markup()
        parsed.feed(document)
        self.assertEqual(parsed.external, [])
        self.assertIn("connect-src 'none'", parsed.policy)
        self.assertNotIn("unsafe-eval", parsed.policy)
        self.assertEqual(parsed.language, "en")
        self.assertIn("Demo data", document)
        self.assertLess(len(document.encode()), 1_048_576)

    def test_official_renderer_is_pinned(self):
        raw = (ROOT / "apps/synthetic_demo/vendor/vis-network.min.js").read_bytes()
        self.assertEqual(
            hashlib.sha256(raw).hexdigest(),
            "3729be2f3994c83229106c3d34fb8de807572cf6f282c23e2b34ecf4e84ce863",
        )

    def test_fixed_output_refuses_linked_file_and_ancestors(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            path = build._write_document(root, "synthetic")
            self.assertEqual(path, root / "build/synthetic-demo/index.html")
            self.assertEqual(path.read_text(), "synthetic")
            outside = root / "outside.html"
            outside.write_text("untouched")
            path.unlink()
            path.symlink_to(outside)
            with self.assertRaises((OSError, ValueError)):
                build._write_document(root, "must not write")
            self.assertEqual(outside.read_text(), "untouched")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            outside = root / "outside"
            outside.mkdir()
            (root / "build").symlink_to(outside, target_is_directory=True)
            with self.assertRaises((OSError, ValueError)):
                build._write_document(root, "must not write")
            self.assertEqual(list(outside.iterdir()), [])

    def test_preview_serves_only_generated_root_and_get_or_head(self):
        server = HTTPServer(("127.0.0.1", 0), preview.handler_for(b"invented"))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            for method, path, status, expected in [
                ("GET", "/", 200, b"invented"),
                ("HEAD", "/", 200, b""),
                ("GET", "/etc/passwd", 404, None),
                ("GET", "/?graph=private", 404, None),
                ("GET", "/%2e%2e/", 404, None),
                ("POST", "/", 405, None),
                ("PUT", "/", 405, None),
                ("DELETE", "/", 405, None),
            ]:
                with self.subTest(method=method, path=path):
                    connection = http.client.HTTPConnection(
                        *server.server_address, timeout=2
                    )
                    connection.request(method, path)
                    response = connection.getresponse()
                    self.assertEqual(response.status, status)
                    body = response.read()
                    if expected is not None:
                        self.assertEqual(body, expected)
                    connection.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join(2)
        self.assertFalse(thread.is_alive())

    def test_fixed_output_refuses_hard_links_before_truncating(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            output = root / "build/synthetic-demo"
            output.mkdir(parents=True)
            outside = root / "outside.html"
            outside.write_text("untouched")
            os.link(outside, output / "index.html")
            with self.assertRaises(ValueError):
                build._write_document(root, "must not write")
            self.assertEqual(outside.read_text(), "untouched")

    def test_boundary_validator_rejects_provider_process_and_dynamic_escapes(self):
        self.assertEqual(
            app_violations(
                "from trama_core.graph_values import GraphSnapshot", "scenario.py"
            ),
            [],
        )
        for source in [
            "import logseq_matryca_parser",
            "import trama_plumber_client",
            "import subprocess",
            "__import__('socket')",
            "import sys; sys.path.append('../parser')",
            "import importlib; importlib.import_module('parser')",
            "import os; os.system('x')",
            "open('not-a-graph')",
            "import os; run = os.system; run('x')",
        ]:
            with self.subTest(source=source):
                self.assertTrue(app_violations(source, "build.py"))
        self.assertEqual(validate_application(ROOT), [])

    def test_boundary_rejects_unregistered_root_app_code(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            admitted = root / "apps/synthetic_demo"
            admitted.mkdir(parents=True)
            (admitted / "__init__.py").write_text("")
            (root / "apps/__init__.py").write_text("import subprocess")
            self.assertTrue(validate_application(root))
