# Contributing

Thanks for helping. This repository holds skills, a Hermes plugin, an MCP
bridge and tests for using basal decision models. Working rules (layout,
versioning, hard rules) are in [`AGENTS.md`](AGENTS.md); this file is about
how to get a change *in*.

## What counts as a contribution

1. **Skill content** — routing tables, templates, protocols, playbook or
   map entries. The most common contribution.
2. **Code** — plugin tools (`__init__.py`), MCP bridge, desktop plugin.
3. **Evidence** — a dated row in `tested-results.md`, an evaluation result,
   a source correction. Cheapest way to raise the repo's trust.
4. **Fixes** — wrong field names, stale versions, broken links.

## Before you write

- Read the live docs the change concerns (links in `basal-serve/SKILL.md`).
  If your change contradicts current docs, the docs win.
- Check the last CHANGELOG entries so you do not re-do a merged change.
- For anything claiming a model or benchmark number: the number needs a
  link and a read date, or it does not go in.

## Getting a change in

1. Branch from `main`: `feat/<summary>`, `fix/<summary>`, `docs/<summary>`.
2. Make the change and bump versions per `AGENTS.md`:
   skill content → that skill's frontmatter version; shipped code →
   `VERSION` + `plugin.yaml` together; either way → a CHANGELOG entry
   under `[Unreleased]`.
3. Add or adjust a test when behaviour changes (`pytest` must pass; it
   enforces structure, version consistency and hygiene).
4. A new "tested" claim needs its dated row in `tested-results.md`.
5. Commit as the repo identity, push, open a PR. CI runs the suite on
   Python 3.10 and 3.12.

## Review

- One reviewer (the owner) merges; the reviewer checks the three classic
  failure modes: invented facts, machine paths or secrets, missing version
  bump.
- Content PRs are reviewed against the live docs, not against the reviewer's
  memory.
- Community-facing text (posts, announcements) is never merged into a
  release without explicit owner sign-off of the exact wording.

## Releases

The owner tags releases: align `VERSION` and `plugin.yaml`, date the
CHANGELOG section, `git tag -a vX.Y.Z`, push tags. Semver: MAJOR changes
how agents must act, MINOR adds usable capability, PATCH is wording or
bug fixes.

## Ground rules

- English in all shipped files.
- No machine paths, hostnames or credentials anywhere public.
- Do not edit frozen codebook versions; create `v2`.
- If you are unsure whether a fact belongs, open the PR as a question and
  link your source — do not guess it in.
