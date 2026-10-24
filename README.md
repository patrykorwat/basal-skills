# patrykorwat/basal-skills

Skills for improving the **basal** community's decision-making process —
grounded in decision-systems research and the community's own experience.

| Skill | Purpose |
|---|---|
| [basal-strategies](skills/basal-strategies/SKILL.md) | Decision-process improvement for basal (Discord): decision methods playbook, literature map, decision register, thread tracking, content discipline |
| [basal-omni](skills/basal-omni/SKILL.md) | Using basal models on media (images, scans, recordings): model routing, question templates, confidence thresholds, evaluation on your own data |

The SejmBench benchmark (the measurement layer for parliamentary decisions)
lives in its own repo, with its own SKILL.md:
[radoskoppl/sejmbench](https://github.com/radoskoppl/sejmbench).

## Plugins

| Plugin | Purpose |
|---|---|
| [basal-register](plugins/basal-register/README.md) | Hermes desktop pane: live decision register for the basal community (propose → decide → review; markdown export) |

Install: copy `plugins/basal-register/plugin.js` to
`<hermes-home>/desktop-plugins/basal-register/plugin.js`, then run
**Reload desktop plugins** from the command palette (⌘K).

## Hermes plugin

This repository is also a native Hermes plugin (`plugin.yaml` at the root).
Installing it gives you, in one step:

1. the `basal_decide` tool — a stdlib-only client for a local `basal-serve`
   (`POST /v1/systemone` / `/v1/basal`): validates question shapes before
   sending, base64-encodes media from local paths, routes tasks to the right
   endpoint, and returns the calibrated answers;
2. the `basal_health` tool — checks `/health` and the served model/mode;
3. both skills bundled, namespaced: `skill_view("basal-skills:basal-omni")`.

```bash
hermes plugins install https://github.com/patrykorwat/basal-skills
# or: desktop app → Settings → Plugins → Install from Git
```

Requires a running `basal-serve` for the tools to answer (see the
basal-omni skill for start-up commands); `basal_health` tells you when it is
up. Verified with `hermes plugins doctor`: manifest, import, registration of
2 tools + 2 skills, no warnings.

## Install

### Via skills.sh

```bash
npx skills add patrykorwat/basal-skills --skill basal-strategies
npx skills add patrykorwat/basal-skills --skill basal-omni   # media decisions
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
