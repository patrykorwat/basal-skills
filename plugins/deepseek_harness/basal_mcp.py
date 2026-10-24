#!/usr/bin/env python3
"""MCP stdio bridge for basal-skills: exposes basal_decide and basal_health
to any MCP client — DeepSeek Harness (via @deepseek-ai/dsh-mcp-client),
Claude Code, goose, or anything speaking JSON-RPC 2.0 over stdio.

Stdlib only. The tool logic lives in the repo-root __init__.py (the Hermes
plugin); this file is transport glue.
"""

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("basal_plugin", ROOT / "__init__.py")
assert _spec is not None and _spec.loader is not None
plugin = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(plugin)

TOOLS = {"basal_decide": plugin.basal_decide, "basal_health": plugin.basal_health}
SCHEMAS = {"basal_decide": plugin.DECIDE_SCHEMA, "basal_health": plugin.HEALTH_SCHEMA}


def _send(msg: dict) -> None:
    body = json.dumps(msg).encode("utf-8")
    sys.stdout.buffer.write(b"Content-Length: %d\r\n\r\n" % len(body) + body)
    sys.stdout.buffer.flush()


def _read():
    headers = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        if b":" in line:
            key, _, value = line.partition(b":")
            headers[key.strip().lower()] = value.strip()
    length = int(headers.get(b"content-length", b"0"))
    if not length:
        return None
    data = sys.stdin.buffer.read(length)
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return {}  # malformed frame: ignore, keep the pipe alive


def main() -> None:
    while True:
        msg = _read()
        if msg is None:
            break
        method = msg.get("method")
        mid = msg.get("id")
        if method == "initialize":
            wanted = msg.get("params", {}).get("protocolVersion", "2024-11-05")
            _send({"jsonrpc": "2.0", "id": mid, "result": {
                "protocolVersion": wanted,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "basal-skills", "version": "0.1.0"}}})
        elif method == "tools/list":
            _send({"jsonrpc": "2.0", "id": mid, "result": {"tools": [
                {"name": name,
                 "description": SCHEMAS[name]["description"],
                 "inputSchema": SCHEMAS[name]["parameters"]}
                for name in TOOLS]}})
        elif method == "tools/call":
            params = msg.get("params", {})
            name = params.get("name")
            handler = TOOLS.get(name)
            if handler is None:
                _send({"jsonrpc": "2.0", "id": mid,
                       "error": {"code": -32602, "message": f"unknown tool: {name}"}})
            else:
                try:
                    out = handler(params.get("arguments") or {})
                except Exception as exc:  # noqa: BLE001 - report, never crash the pipe
                    out = json.dumps({"ok": False,
                                      "error": f"{type(exc).__name__}: {exc}"})
                _send({"jsonrpc": "2.0", "id": mid, "result": {
                    "content": [{"type": "text", "text": out}]}})
        elif method == "ping":
            _send({"jsonrpc": "2.0", "id": mid, "result": {}})
        elif mid is not None:
            _send({"jsonrpc": "2.0", "id": mid,
                   "error": {"code": -32601, "message": f"method not found: {method}"}})
        # notifications (no id): initialized, cancelled, ... — nothing to do


if __name__ == "__main__":
    main()
