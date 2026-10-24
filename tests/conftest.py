"""Shared fixtures: import the plugin module and run a throwaway HTTP server."""

import importlib.util
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_plugin():
    spec = importlib.util.spec_from_file_location("basal_plugin", REPO_ROOT / "__init__.py")
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class DecisionServer(BaseHTTPRequestHandler):
    """Echo-style stand-in for basal-serve; records the last request body."""

    last = {}

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        type(self).last = {"path": self.path, "body": body}
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({"model": "basal-omni-1.0-mini", "answers": {}}).encode())

    def log_message(self, format, *args):  # noqa: A002 - silence BaseHTTPRequestHandler logging
        pass


def start_server(handler=DecisionServer):
    srv = HTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"
