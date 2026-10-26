"""End-to-end tests of the MCP stdio bridge (plugins/deepseek_harness/basal_mcp.py)."""

import json
import subprocess
import sys
from pathlib import Path

BRIDGE = Path(__file__).resolve().parents[1] / "plugins" / "deepseek_harness" / "basal_mcp.py"


def start():
    return subprocess.Popen([sys.executable, str(BRIDGE)],
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def send(p, msg):
    body = json.dumps(msg).encode("utf-8")
    p.stdin.write(b"Content-Length: %d\r\n\r\n" % len(body) + body)
    p.stdin.flush()


def recv(p):
    line = p.stdout.readline()
    assert line.startswith(b"Content-Length"), f"bad frame: {line!r}"
    n = int(line.split(b":")[1])
    p.stdout.readline()  # blank
    return json.loads(p.stdout.read(n))


def rpc(method, params=None):
    return {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}


def test_initialize_and_tools_list():
    p = start()
    try:
        send(p, rpc("initialize", {"protocolVersion": "2024-11-05", "capabilities": {}}))
        res = recv(p)["result"]
        assert res["serverInfo"]["name"] == "basal-skills"
        assert res["serverInfo"]["version"] == (
            BRIDGE.parents[2] / "VERSION").read_text().strip()
        assert res["capabilities"] == {"tools": {}}
        send(p, {"jsonrpc": "2.0", "method": "notifications/initialized"})
        send(p, rpc("tools/list"))
        tools = recv(p)["result"]["tools"]
        assert {t["name"] for t in tools} == {"basal_decide", "basal_health"}
        for t in tools:
            assert t["description"] and t["inputSchema"]["type"] == "object"
    finally:
        p.terminate()


def test_tools_call_and_unknown_tool():
    p = start()
    try:
        send(p, rpc("tools/call", {"name": "basal_decide",
                                   "arguments": {"url": "http://127.0.0.1:1", "questions": {}}}))
        text = json.loads(recv(p)["result"]["content"][0]["text"])
        assert not text["ok"] and "errors" in text  # validation error, not a crash
        send(p, rpc("tools/call", {"name": "nope", "arguments": {}}))
        assert recv(p)["error"]["code"] == -32602
    finally:
        p.terminate()


def test_unknown_method_and_malformed_frame_survive():
    p = start()
    try:
        send(p, rpc("bogus/method"))
        assert recv(p)["error"]["code"] == -32601
        bad = b"{not json"
        p.stdin.write(b"Content-Length: %d\r\n\r\n" % len(bad) + bad)
        p.stdin.flush()
        send(p, rpc("ping"))
        assert recv(p)["result"] == {}  # server survived the malformed frame
    finally:
        p.terminate()
