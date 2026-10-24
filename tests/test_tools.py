"""Behavioural tests for the basal_decide / basal_health tools (stdlib only)."""

import base64
import json

from conftest import DecisionServer, load_plugin, start_server

mod = load_plugin()


def ok(r):
    return json.loads(r)


def test_unknown_type_rejected_locally():
    r = ok(mod.basal_decide({"questions": {"x": {"type": "nope"}}}))
    assert not r["ok"] and "unknown type" in r["errors"][0]
    assert DecisionServer.last == {}  # nothing was sent


def test_act_needs_costs():
    r = ok(mod.basal_decide({"questions": {"a": {"type": "act", "criteria": {"true": "t", "false": "f"}}}}))
    assert not r["ok"] and "needs costs" in r["errors"][0]


def test_max_error_range():
    r = ok(mod.basal_decide({"questions": {"a": {"type": "act", "criteria": {"true": "t", "false": "f"},
                                                "costs": {"human": {"true": 1, "false": 1}},
                                                "max_error": 0.5}}}))
    assert not r["ok"] and "max_error" in r["errors"][0]


def test_verify_extract_classify_shape_checks():
    for q, msg in [({"type": "verify"}, "claims"), ({"type": "extract"}, "schema"), ({"type": "classify"}, "labels")]:
        r = ok(mod.basal_decide({"questions": {"a": q}}))
        assert not r["ok"] and msg in r["errors"][0], (q, r)


def test_text_decision_routes_to_systemone():
    srv, url = start_server()
    r = ok(mod.basal_decide({"url": url, "state": "x",
                             "questions": {"q": {"type": "noul", "instructions": "?"}}}))
    assert r["ok"] and r["endpoint"] == "/v1/systemone"
    assert DecisionServer.last["path"] == "/v1/systemone"
    srv.shutdown()


def test_task_and_mixed_requests_route_to_basal():
    srv, url = start_server()
    r = ok(mod.basal_decide({"url": url, "questions": {"v": {"type": "verify", "claims": {"c": "x"}}}}))
    assert r["ok"] and r["endpoint"] == "/v1/basal"
    r = ok(mod.basal_decide({"url": url, "questions": {
        "v": {"type": "verify", "claims": {"c": "x"}},
        "c": {"type": "choice", "criteria": {"k": "d"}}}}))  # mixing is legal per docs/TASKS.md
    assert r["ok"] and r["endpoint"] == "/v1/basal"
    srv.shutdown()


def test_media_encoded_from_path(tmp_path):
    srv, url = start_server()
    img = tmp_path / "scan.png"
    img.write_bytes(b"IMGDATA")
    r = ok(mod.basal_decide({"url": url, "state": "",
                             "media": [{"type": "image", "path": str(img)}],
                             "questions": {"q": {"type": "noul", "instructions": "?"}}}))
    assert r["ok"]
    assert DecisionServer.last["body"]["media"][0]["data"] == base64.b64encode(b"IMGDATA").decode()
    srv.shutdown()


def test_media_missing_file_and_size_limit(tmp_path):
    r = ok(mod.basal_decide({"questions": {"q": {"type": "noul", "instructions": "?"}},
                             "media": [{"type": "image", "path": str(tmp_path / "nope.png")}]}))
    assert not r["ok"] and "not a readable file" in r["errors"][0]
    big = tmp_path / "big.bin"
    big.write_bytes(b"x" * (21 * 1024 * 1024))
    r = ok(mod.basal_decide({"questions": {"q": {"type": "noul", "instructions": "?"}},
                             "media": [{"type": "image", "path": str(big)}]}))
    assert not r["ok"] and "limit" in r["errors"][0]


def test_health_offline_hint():
    r = ok(mod.basal_health({"url": "http://127.0.0.1:1"}))  # port 1: refused
    assert not r["ok"] and "basal-serve" in r["hint"]


def test_health_empty_body_tolerated():
    class EmptyHealth(DecisionServer):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"" if self.path == "/health" else b'{"models": []}')

    srv, url = start_server(EmptyHealth)
    r = ok(mod.basal_health({"url": url}))
    assert r["ok"] and r["models"] == []
    srv.shutdown()
