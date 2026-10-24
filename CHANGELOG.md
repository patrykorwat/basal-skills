# Changelog — basal-skills

Format: `Keep a Changelog`, versions follow SemVer. The project version lives
in `VERSION`; the Hermes plugin (`plugin.yaml`) always mirrors it; each skill
carries its own version, bumped when its content changes. See `AGENTS.md` for
the workflow.

## [1.0.0] — 2026-10-24
First versioned release; before this date the history is:

- Versioning scheme added: `VERSION`, `CHANGELOG.md`, `AGENTS.md`,
  `tests/test_versioning.py`; plugin and desktop plugin set to 1.0.0.

- Initial skills (sejmbench, basal) and README; literature map; playbook;
  decision-register template (later removed); basal-register desktop plugin.
- `basal` renamed to `basal-strategies`; `basal-omni` skill added (routing,
  templates with JSON from engine docs 2.4.1, evaluation protocol).
- Native Hermes plugin (`plugin.yaml` + `register(ctx)`): `basal_decide`,
  `basal_health`; bundled skills.
- DeepSeek Harness adapter (MCP stdio bridge + cordis overlay).
- Query-template review applied (file-based media POST, compatibility
  matrix, codebook-as-parameter, 422 diagnosis, tested-results log).
- pytest suite + GitHub Actions CI; skill-review round applied (hard rules,
  checkable/value split, conditions per method, overclaims softened).

## Versioning rules (summary, full text in AGENTS.md)
- Every change to shipped artifacts (skill content, plugin code, tools,
  MCP bridge) bumps the affected component's version.
- Docs-only changes (README, AGENTS, CHANGELOG) need no bump but do get a
  CHANGELOG entry under "Unreleased".
- A release = `VERSION` + `plugin.yaml` aligned, CHANGELOG dated, git tag
  `vX.Y.Z` pushed.
