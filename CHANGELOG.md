# Changelog — basal-skills

Format: `Keep a Changelog`, versions follow SemVer. One version for the whole
repo: `VERSION` is the single source; the Hermes plugin (`plugin.yaml`) always
mirrors it, and no artifact carries a version of its own. See `AGENTS.md` for
the workflow.

## [1.7.1] — 2026-11-05

### Fixed

- `sync-docs.yml` could push the mirror but not open its PR: run 13 died at
  `gh pr create` with `GitHub Actions is not permitted to create or approve
  pull requests`. That is a repository setting (Settings → Actions → General →
  Workflow permissions), not a code bug, so the step now names it in the error
  instead of surfacing a bare GraphQL message.
- The PR step ran only when the sync reported changes. A run that pushed the
  branch and then failed left the mirror sitting on `docs/engine-mirror`
  forever: the next day reports "up to date", the step is skipped, and nothing
  ever opens the review. It now runs every time — and when there is nothing
  new it adopts the pending branch instead of resetting it to `main`, which
  would have deleted an unreviewed mirror update.
- `sync_docs.py` failures exit 0 by design; they are now surfaced as a workflow
  warning instead of being silent.

### Tests

- `tests/test_sync_docs_step.py` gained the quiet-run cases: a pending branch
  survives and gets its PR, and a quiet run with nothing pending touches
  nothing. (They caught a dropped `git commit` in the rewritten step.)

## [1.7.0] — 2026-11-04

### Added

- Upstream's own agent guide, `skills/basal/SKILL.md`, is now mirrored as
  `references/engine/UPSTREAM-SKILL.md`. It is upstream's tutorial for calling
  the engine (state and question craft, question types, presets, coverage /
  `max_error`, calibrating, escalation) — we mirror it instead of restating
  it, so it stays one source of truth and arrives with the daily sync.
- `basal-serve`: a **Presets** section. The engine ships ready question sets
  (`triage`, `moderation`, `compliance`, `guard_input`, `guard_output`,
  `route_intent`; `basal-run --list-presets`, `b.guard()`, `b.route()`), and
  this skill said nothing about them — an agent following it wrote questions
  from scratch where a preset already fits. Their semantics and the escalation
  router live in `docs/SERVING.md`, which the mirror does not ship, so the
  section points there live.

### Changed

- `scripts/sync_docs.py` mirrors a `(upstream path -> local name)` mapping
  instead of one `docs/` directory, and rewrites every link to a page we do
  not ship into its absolute upstream URL. The mirror used to carry 9 dead
  relative links (`SERVING`, `FEATURES`, `QUANTIZATION`, `PORTS`, `SOAM`,
  `FORMATS`, `GGUF`, `NAVIGATE`, `MCP`); it now resolves or goes upstream, and
  `tests/test_skills.py` fails if a dead relative link comes back. The
  comparison against the stored copy is made on the mirrored text, so the
  rewrite does not make every run look "changed".
- `MANIFEST.json` gains `sources` (local name -> upstream path).
- Mirror refreshed to `rkinas/basal` `8e80d3eba0` (2026-11-04).

## [1.6.1] — 2026-11-04

### Fixed

- `.github/workflows/sync-docs.yml`: the daily mirror PR step failed on every
  run that had anything to publish. `git push --force-with-lease` had no
  remote-tracking value to compare against (`actions/checkout` fetches only
  `main`), so it died with "stale info", and every `gh` call exited 4 because
  the job never set `GH_TOKEN` — run 11 got past the push and then failed on
  `gh`, run 12 died at the push. The step now reads the branch's value from
  the remote before leasing it, resolves the open PR's number (the old
  `gh pr edit docs/engine-mirror` passed a branch where gh wants a number),
  and takes `GH_TOKEN` from the job.
- `tests/test_sync_docs_step.py` replays that step body against a throwaway
  remote — branch absent, branch left over by an earlier run, and an open PR —
  so CI catches the regression instead of the next cron.

### Changed

- `AGENTS.md` / `CONTRIBUTING.md`: docs- and infra-only changes take a PATCH
  bump and get a dated CHANGELOG section; `[Unreleased]` is off the table.

## [1.6.0] — 2026-11-04

### Added

- Engine docs mirror refreshed to `rkinas/basal` `160508223f` (2026-11-03), so
  the bundled references describe what a current `basal-serve` actually answers:

  - `API.md` — OpenAI's Decisions API (`POST /v1/decisions`, usable straight
    from the OpenAI Python SDK), the vLLM structured-diffusion request shape
    (`ask_if`, `depends_on`, `images`), a `code` field on every error body
    (`INVALID_REQUEST` / `OUT_OF_MEMORY` / `INTERNAL_ERROR`) plus the
    `--error-format openai` shape, and `certified` / `context` in
    `GET /v1/models`.
  - Answer sets: `coverage` (conformal `answer_set`) and `max_error`
    (`abstain`) for `choice` / `noul` / `score` questions, with the
    `basal-calibrate --conformal` fitting behind them (`CALIBRATION.md`).
  - The experimental `rank` question type, and task names no longer allowed to
    contain `::` (HTTP 422).
  - Install/hardware: LM Studio serving `/v1/systemone` itself (the `-GGUF`
    files as decision models, LM Studio 0.4.26+), MLX forward-pass trimming
    and state cache on Apple Silicon, compact rows with flex kernels on
    Blackwell.

### Changed

- Nothing in this repo's own code or skill rules changed; the bump records that
  the engine contract the skills point at moved (new endpoints, request fields
  and answer fields). Per `AGENTS.md` the mirror is tracked by its own
  `MANIFEST.json` and would not require a bump on its own.

## [1.5.0] — 2026-10-27

### Added

- Claude Code plugin: `.claude-plugin/plugin.json` (manifest with the
  bundled MCP bridge, `${CLAUDE_PLUGIN_ROOT}`-based) and
  `.claude-plugin/marketplace.json` (the repository doubles as its own
  marketplace), so `claude plugin marketplace add patrykorwat/basal-skills`
  + `claude plugin install basal-skills@basal-skills` installs the two
  tools and both skills in one step. The manifests carry no `version`
  field on purpose — `VERSION` stays the single source of truth (repo
  rule), so `claude plugin validate` warns about the missing version.
- docs/install.md: the Claude Code section now leads with the plugin
  route; `claude mcp add` is the manual fallback.

## [1.4.1] — 2026-10-27

### Changed

- README: the Hermes-plugin section became a compact per-host install table;
  the detailed per-host guide (config blocks per agent, verify steps,
  caveats) moved to `docs/install.md`. The native Hermes plugin is installed
  via `hermes plugins install` or the desktop app's **Capabilities →
  Plugins** — not Settings; the stdlib MCP bridge covers OpenCode, goose,
  Codex CLI, Claude Code, Cursor and the DeepSeek Harness bundle, with a
  skills-only fallback. Fixed the stale bundled-skill name
  (`basal-skills:basal-omni` → `basal-skills:basal-serve`) in the README
  and in the plugin manifest description.

## [1.4.0] — 2026-10-26

### Changed

- One version for the whole repo: skills and the desktop plugin no longer
  carry their own version numbers; `VERSION` is the only source of truth and
  the MCP bridge reports it in its `serverInfo` handshake. Versioning tests
  enforce the new rule: per-artifact version fields are rejected, and any
  authored-content change since the last tag must bump `VERSION` (the
  engine-docs mirror is exempt — it is tracked by its own MANIFEST.json).

## [1.3.1] — 2026-10-25

- Engine docs mirror moved into the skill: `docs/engine/` →
  `skills/basal-serve/references/engine/`, so installed skill copies carry
  the offline fallback. Script, workflow, AGENTS.md, hygiene tests and the
  SKILL.md links updated; `test_referenced_files_exist` now validates
  subdirectory references.
- Mirrored engine docs now carry a provenance footer: source link, upstream
  commit link, fetch date and "upstream data, do not edit locally". The sync
  script compares content with the footer stripped, so re-runs stay
  idempotent. Skill 0.7.2.
- `sync-docs.yml`: corrected the permissions key (`pull-requests`, not
  `pull-request`); the invalid key made the whole workflow fail to parse.
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
- Docs-only changes (README, AGENTS, CHANGELOG) get a dated CHANGELOG section
  as well, so they take a PATCH bump. Never an `[Unreleased]` section.
- A release = `VERSION` + `plugin.yaml` aligned, CHANGELOG dated, git tag
  `vX.Y.Z` pushed.
