# patrykorwat/basal-skills

Skills for improving the **basal** community's decision-making process —
grounded in decision-systems research and the community's own experience.

| Skill | Purpose |
|---|---|
| [basal-strategies](skills/basal-strategies/SKILL.md) | Decision-process improvement for basal (Discord): decision methods playbook, literature map, decision register, thread tracking, content discipline |
| [basal-serve](skills/basal-serve/SKILL.md) | Using basal models on text or media (images, scans, recordings): model routing, question templates, confidence thresholds, evaluation on your own data |

## Plugins

| Plugin | Purpose |
|---|---|
| [basal-register](plugins/basal-register/README.md) | Hermes desktop pane: small personal decision tracker (propose → decide → review; markdown export) |

Install: copy `plugins/basal-register/plugin.js` to
`<hermes-home>/desktop-plugins/basal-register/plugin.js`, then run
**Reload desktop plugins** from the command palette (⌘K).

## Versioning

One version for everything: `VERSION` (SemVer), released as git tags; the
plugin manifest mirrors it, artifacts carry no versions of their own, and
`CHANGELOG.md` records every change. The workflow and the enforced rules are
in [`AGENTS.md`](AGENTS.md) — start there if you are changing this repo.

## Plug into your agent

`basal_decide` and `basal_health` talk to a local `basal-serve`; `BASAL_URL`
overrides the default `http://127.0.0.1:8000`. Every MCP host below runs the
same stdlib bridge, `plugins/deepseek_harness/basal_mcp.py` (JSON-RPC 2.0
over stdio; media as local file paths, audio max 30 s). `<path>` below is
your checkout of this repository. Per-host detail — config blocks, verify
steps, caveats: [docs/install.md](docs/install.md).

| Agent | Install |
|---|---|
| Hermes Agent | native plugin: `hermes plugins install https://github.com/patrykorwat/basal-skills` or desktop app → **Capabilities → Plugins** → Install from Git |
| OpenCode | `mcp` block in `opencode.json` |
| goose | `extensions:` block in `~/.config/goose/config.yaml` |
| Codex CLI | `codex mcp add basal-skills -- python3 <path>/basal_mcp.py` |
| Claude Code | `claude mcp add basal-skills -- python3 <path>/basal_mcp.py` |
| Cursor | `~/.cursor/mcp.json` (or `.cursor/mcp.json` in the project) |
| DeepSeek Harness | `dsh --patch <path>/basal.cordis.yml web` |
| No MCP | skills only — see [Install](#install) |

## Install

### Via skills.sh

```bash
npx skills add patrykorwat/basal-skills --skill basal-strategies
npx skills add patrykorwat/basal-skills --skill basal-serve   # media decisions
```

Select your agent when prompted. Installation is project-local by default;
add `-g` to install globally.

### Manual

Read the raw `SKILL.md` of the skill you need and paste it into your agent's
skills directory (or your prompt). Nothing here assumes a specific agent.

## Principles carried into every skill

1. Official sources only; every number links to its source.
2. Definitions frozen before results (versioned codebooks, never silently).
3. Machine-specific paths and credentials never leave the local machine —
   public skills contain knowledge, not environment.
4. Community-facing content is published only after explicit owner approval.

## Tests and CI

`pytest` runs everything with stdlib + pytest only (Python 3.10+):

- `tests/test_tools.py` — validator rules, endpoint routing, media encoding,
  offline hints, against a throwaway HTTP stand-in for basal-serve;
- `tests/test_mcp_bridge.py` — MCP handshake, tools/list, tools/call,
  malformed-frame resilience of the DeepSeek Harness bridge;
- `tests/test_skills.py` — frontmatter fields, cross-links between skills,
  referenced files exist, JSON blocks parse, README table and install
  commands, no machine paths or secrets in shipped files.

GitHub Actions (`.github/workflows/ci.yml`) runs the suite on every push and
PR, on Python 3.10 and 3.12.

## License

MIT.
