# patrykorwat/basal-skills

Skills for improving the **basal** community's decision-making process —
grounded in decision-systems research and the community's own experience.

| Skill | Purpose |
|---|---|
| [basal](skills/basal/SKILL.md) | Decision-process improvement for basal (Discord): decision-systems literature map, decision register, thread tracking, content discipline |

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

## Install

### Via skills.sh

```bash
npx skills add patrykorwat/basal-skills --skill basal
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

## License

MIT.
