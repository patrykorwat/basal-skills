# Installing the basal tools — per host

Both tools (`basal_decide`, `basal_health`) talk to a local `basal-serve`
HTTP API, so every host below needs the server running (start-up commands
in the basal-serve skill; `basal_health` tells you when it is up).
`BASAL_URL` overrides the default `http://127.0.0.1:8000`. Hosts without a
native plugin run the stdlib MCP bridge
`plugins/deepseek_harness/basal_mcp.py` (JSON-RPC 2.0 over stdio, same
tool logic as the Hermes plugin; media travel as local file paths, audio
max 30 s). Tools are registered prefixed per client (DeepSeek Harness:
`mcp__basal_skills__basal_decide`).

| Tool | What it does |
|---|---|
| `basal_decide` | typed, calibrated decisions over text, images, scans, screenshots or audio (max 30 s): choice, noul, score, multi, act/tool; validates question shapes before sending and routes to the right endpoint |
| `basal_health` | is the server up, which model and mode; check before the first decide |

## Hermes Agent

The repository is a native Hermes plugin (`plugin.yaml` at the root).
Installing it gives you, in one step: both tools above plus both skills
bundled and namespaced (`skill_view("basal-skills:basal-serve")`).

```bash
hermes plugins install https://github.com/patrykorwat/basal-skills
# or: desktop app → Capabilities → Plugins → Install from Git
```

Verified with `hermes plugins doctor`: manifest, import, registration of
2 tools + 2 skills, no warnings. Updating: `hermes plugins update
basal-skills`. Without the plugin, an MCP block is equivalent — add under
`mcp_servers` in `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  basal-skills:
    command: "python3"
    args: ["/ABS/PATH/TO/basal-skills/plugins/deepseek_harness/basal_mcp.py"]
    timeout: 300
    env:
      BASAL_URL: "http://127.0.0.1:8000"
```

Restart Hermes; the tools appear in every platform toolset.

A tip that makes the tools proactive — add to your project `AGENTS.md`:

```
## Decisions (MCP: basal-skills)
- For checkable judgments (a category, a yes/no rule, a claim against a
  source), call `basal_health` once, then ask `basal_decide` with explicit
  options and criteria instead of judging in prose. A low-confidence or
  `deferred` answer goes to a human.
```

## OpenCode

Create (or merge into) `opencode.json` in the project root where you work:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "basal-skills": {
      "type": "local",
      "command": ["python3", "/ABS/PATH/TO/basal-skills/plugins/deepseek_harness/basal_mcp.py"],
      "enabled": true
    }
  }
}
```

Start OpenCode and type `/mcps` — you should see `basal-skills: connected`.

## goose

Add the extension to `~/.config/goose/config.yaml`:

```yaml
extensions:
  basal-skills:
    enabled: true
    type: stdio
    name: basal-skills
    description: "Typed, calibrated decisions from a local basal-serve.
      basal_decide for choice/noul/score/multi/act questions over text or
      media, basal_health to check the server."
    cmd: python3
    args: ["/ABS/PATH/TO/basal-skills/plugins/deepseek_harness/basal_mcp.py"]
    timeout: 300
```

goose spawns extensions without a shell and with a scrubbed environment:
use absolute paths (no `~`, no relative `./`) and pass `BASAL_URL` through
`envs:` when the server is not on the default port. After any config edit:
fully quit goose (the desktop app caches config at startup), relaunch, and
activate `basal-skills` in the session's extensions picker. One-shot
alternative (no config edit):
`goose session --with-extension "python3 /ABS/PATH/TO/basal-skills/plugins/deepseek_harness/basal_mcp.py"`.

## Codex CLI

```bash
codex mcp add basal-skills -- python3 /ABS/PATH/TO/basal-skills/plugins/deepseek_harness/basal_mcp.py
```

Verify with `codex mcp list` (or `[mcp_servers.basal-skills]` with
`command`/`args` in `~/.codex/config.toml`).

## Claude Code

```bash
claude mcp add basal-skills -- python3 /ABS/PATH/TO/basal-skills/plugins/deepseek_harness/basal_mcp.py
```

Check with `/mcp` inside a session.

## Cursor

Cursor reads MCP servers from `~/.cursor/mcp.json` (global) or
`.cursor/mcp.json` in the project:

```json
{
  "mcpServers": {
    "basal-skills": {
      "command": "python3",
      "args": ["/ABS/PATH/TO/basal-skills/plugins/deepseek_harness/basal_mcp.py"],
      "env": { "BASAL_URL": "http://127.0.0.1:8000" }
    }
  }
}
```

The server then appears under Cursor Settings → MCP & Integrations; enable
it there (and reload after editing the file while Cursor is open).

## DeepSeek Harness

First-party route: `dsh --patch /ABS/PATH/TO/basal.cordis.yml web`, or merge
the row into the profile's `cordis.patch.yml`. Tools appear as
`mcp__basal_skills__basal_decide` and `mcp__basal_skills__basal_health`.
Full walkthrough:
[plugins/deepseek_harness/README.md](../plugins/deepseek_harness/README.md).

## Skills only (no MCP)

If the agent has no MCP surface, install the skills alone
([Install in the README](../README.md#install)) and call the `basal-serve`
HTTP API directly — the skill carries the request shapes.
