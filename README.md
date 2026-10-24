# radoskoppl/skills

Agent skills published by [Radoskop](https://github.com/radoskoppl) —
following the [agent skills convention](https://skills.sh): one directory per
skill, each with a `SKILL.md` that any agent (Claude Code, Hermes, Codex, …)
can read and follow.

| Skill | Purpose |
|---|---|
| [sejmbench](skills/sejmbench/SKILL.md) | Work on the SejmBench benchmark: LLM evaluation on Polish parliamentary roll-call data (Sejm API recipes, metric principles, roadmap) |
| [basal](skills/basal/SKILL.md) | Engage the "basal" Polish AI community (Discord): thread tracking, content discipline for benchmark outreach |

## Install

### Via skills.sh

```bash
npx skills add radoskoppl/skills --skill sejmbench
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
