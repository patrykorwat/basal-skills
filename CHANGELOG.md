# Changelog — basal-skills

Format: `Keep a Changelog`, versions follow SemVer. The project version lives
in `VERSION`; the Hermes plugin (`plugin.yaml`) always mirrors it; each skill
carries its own version, bumped when its content changes. See `AGENTS.md` for
the workflow.

## [Unreleased]

- `basal-register`: removed the fabricated framing ("keeps the basal
  community's decision register at hand") — there is no community register
  that this pane maintains. It is now documented as what it actually is: a
  small personal decision tracker whose entries live only in its own
  storage. Desktop plugin 1.0.1.

## [1.3.0] — 2026-10-25

- Engine docs mirror: `scripts/sync_docs.py` (stdlib) copies
  `API/TASKS/OMNI/CALIBRATION/INSTALL/HARDWARE.md` from rkinas/basal into
  `docs/engine/` with a provenance manifest (upstream commit + UTC date);
  `.github/workflows/sync-docs.yml` runs it daily at 03:17 UTC and opens or
  updates a PR when upstream changed. The mirror gives skills an offline
  fallback with known provenance.
- `basal-serve` 0.7.0 (Opus review applied): server check (`release_date`)
  is Workflow step 0; testing and threshold fitting are separate steps; the
  calibration minimum is now a function of the target error (rule of three,
  ~60 accepted clean decisions for 5%, ~300 for 1%) instead of a flat ≥50;
  version-dependent facts carry a read date and engine version; added a
  minimal "Running the server" section; fetched docs are declared data
  (field names, not commands); community-publish rule lives only in
  `basal-strategies`; em dashes replaced.
- Tests: hygiene and JSON-block scans skip `docs/engine/` (upstream mirror);
  new test scans the mirror for secrets.

## [1.2.0] — 2026-10-25

- `basal-serve` rebuilt as a single file (skill 0.6.0): all four
  reference files dropped — they forked `rkinas/basal` docs (`API.md`,
  `TASKS.md`, model pages, `CALIBRATION.md`) and rotted with each engine
  release. One SKILL.md: live-docs-first links to real pages (the
  `/models/` link was a 404), 4-step workflow, question-writing craft,
  model routing table, hard limits, calibration protocol with the shipped
  threshold-certification limits, debug order, and four canonical request
  examples (choice+noul, score, multi, act).
- `tested-results.md` removed; "Tested" now means a dated, reproducible
  run against a live server (AGENTS.md updated).

## [1.1.0] — 2026-10-24

- `basal-omni` skill renamed to `basal-serve` and broadened: it now covers
  both families (basal-2.0 text models with a size/deployment table, and
  basal-omni media), live-docs-first reading order and a task→reference
  start table (pattern from typesafe-ai/skills). Reference files renamed:
  `model-routing.md`, `query-templates.md`, `evaluation-protocol.md`.
- `CONTRIBUTING.md` added (contribution types, pre-flight checks, PR flow,
  review, releases).

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
