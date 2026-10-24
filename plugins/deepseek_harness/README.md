# basal-skills — DeepSeek Harness adapter

[DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (`dsh`)
is an all-plugin agent harness. This adapter is pure configuration plus a
stdlib MCP bridge: a Cordis overlay that inserts `basal_mcp.py` as an
external stdio MCP server through the first-party
`@deepseek-ai/dsh-mcp-client`. DSH starts the child, discovers the two
tools, and exposes them as `mcp__basal_skills__basal_decide` and
`mcp__basal_skills__basal_health`.

The bridge reuses the tool logic from the repo-root `__init__.py` (the same
code the Hermes plugin registers), so behaviour stays identical across
surfaces. No npm, no pip, no build — only a system `python3` (3.10+) on
PATH and a running `basal-serve` for the tools to answer (check with
`basal_health`; the basal-omni skill has the start-up commands).

## Files

| file                | use                                              |
|---------------------|--------------------------------------------------|
| `basal_mcp.py`      | MCP stdio server (JSON-RPC 2.0, stdlib only)     |
| `basal.cordis.yml`  | overlay for DSH + server on one machine          |

## Install

1. Edit `basal.cordis.yml`: replace `/ABSOLUTE/PATH/TO/basal-skills` with
   your checkout path. Optionally set `BASAL_URL` in the shell you launch
   `dsh` from (default `http://127.0.0.1:8000`).
2. One-shot: `dsh --patch /ABS/PATH/TO/basal.cordis.yml web`
3. Persist: merge the `- insert:` entry into
   `$DSH_HOME/profiles/web/cordis.patch.yml` (append, do not overwrite).

In the harness the agent sees:

- `mcp__basal_skills__basal_decide` — typed, calibrated decisions over
  text/images/audio (`/v1/systemone`; task types on `/v1/basal`). Media
  travel as local file paths; audio max 30 s.
- `mcp__basal_skills__basal_health` — is the server up, which model/mode.

## Smoke test without DSH

```bash
python3 - <<'EOF'
import json, subprocess
p = subprocess.Popen(["python3", "plugins/deepseek_harness/basal_mcp.py"],
                     stdin=subprocess.PIPE, stdout=subprocess.PIPE)
def send(m, p_):
    b = json.dumps({"jsonrpc":"2.0","id":1,"method":m,"params":p_}).encode()
    p.stdin.write(b"Content-Length: %d\r\n\r\n" % len(b) + b); p.stdin.flush()
def recv():
    n = int(p.stdout.readline().split(b":")[1]); p.stdout.readline()
    return json.loads(p.stdout.read(n))
send("initialize", {"protocolVersion": "2024-11-05", "capabilities": {}}); print(recv()["result"]["serverInfo"])
send("tools/list", {}); print([t["name"] for t in recv()["result"]["tools"]])
EOF
```

Expected: `{'name': 'basal-skills', ...}` and `['basal_decide', 'basal_health']`.
