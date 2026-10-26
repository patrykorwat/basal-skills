# AGENTS.md — working rules for basal-skills

Guidance for humans and AI agents changing this repository. The repo is
knowledge + a small amount of code: two skills, a Hermes plugin, an MCP
bridge, and tests. Repo language is English (community-facing drafts are
the exception and stay untracked).

## Layout

```
VERSION                      project version (single source of truth)
CHANGELOG.md                 every change gets an entry
AGENTS.md / CONTRIBUTING.md  working rules / how to get a change in
plugin.yaml                  Hermes plugin manifest (version mirrors VERSION)
__init__.py                  plugin register(ctx): basal_decide, basal_health
skills/basal-strategies/     decision situations, playbook, evidence map
skills/basal-serve/           model use: live-docs-first, question craft, routing, calibration
plugins/deepseek_harness/    MCP stdio bridge + cordis overlay
plugins/basal-register/      Hermes desktop pane (JS, separate surface)
skills/basal-serve/references/engine/  mirror of rkinas/basal docs (MANIFEST.json: commit + date)
scripts/sync_docs.py         refreshes the mirror (CI cron opens a PR daily)
tests/                       pytest suite (also enforces the rules below)
.github/workflows/ci.yml     CI on every push/PR (Python 3.10 + 3.12)
```

## Versioning — one version for the whole repo

`VERSION` (SemVer) is the single source of truth for every artifact here: the
Hermes plugin (`plugin.yaml` mirrors it, test-enforced), both bundled skills
(no own `version:` field — the test rejects one), the desktop plugin (no
version header), and the MCP bridge (reports the repo version in
`serverInfo`). Releases are git tags `vX.Y.Z`. Bump `VERSION` on any change
to authored content (test enforces vs last tag); docs/infra changes and the
engine-docs mirror (tracked by its own `MANIFEST.json`) don't require a bump.

Semver: MAJOR breaks how agents must act (hard rules, endpoints, request
shapes), MINOR adds usable capability, PATCH fixes wording/bugs.

## Change workflow (checklist)

1. Make the change.
2. Bump `VERSION` (+ `plugin.yaml` mirror) if authored content changed.
   Docs-only: no bump, add a CHANGELOG entry under `[Unreleased]`.
3. Add/adjust CHANGELOG entry describing the change.
4. Run `pytest` locally — it must pass (it also checks version consistency
   and that no machine path or secret entered shipped files).
5. Commit as `patrykorwat <patrykorwat@gmail.com>` (repo-local config),
   message: `type: summary` (`feat:`, `fix:`, `docs:`, `chore:`).
6. Push; CI goes green. For a release: set VERSION+plugin.yaml, date the
   CHANGELOG section, `git tag -a vX.Y.Z -m "..."`, push tags.
7. After merge, refresh installed copies: `hermes plugins update
   basal-skills`, and sync profile skill copies (`cp -r skills/<skill>
   <profile-skills>/`).

## Hard rules (do not violate)

- Public files carry knowledge, not environment: no machine paths, no
  hostnames, no credentials (test enforces).
- Numbers in skill content need a source and a read date; benchmark
  numbers link, never copy.
- Community-facing posts are published only after explicit owner approval
  of the exact text; drafts stay gitignored (`post-*`).
- Skills stay English; JSON in templates is copied from engine docs — if
  docs change, trust the docs and re-copy.
- Claims of "tested" require a dated, reproducible run against a live
  server; if you cannot point to one, do not claim it.

## Testing

`pytest` (stdlib + pytest only). Tests import the plugin from the repo
root; the MCP bridge runs as a subprocess; HTTP is stood-in locally.
`tests/test_versioning.py` enforces the versioning rules above.

## Gotchas

- `hermes plugins update` fast-forwards; after a history rewrite, reset
  the installed clone manually (`git fetch && git reset --hard origin/main`).
- Mixed task+decision requests are legal and route to `/v1/basal`.
- A 422 from a live server is usually an engine-version mismatch, not a
  broken server: check `release_date` in `/v1/models` first.
- Profile skill copies are caches; the repo is canonical.
