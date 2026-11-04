#!/usr/bin/env python3
"""Replay the sync-docs "Open or update PR" step against a throwaway remote.

The daily mirror PR broke twice in production (`git push --force-with-lease`
refusing with "stale info", and every `gh` call exiting 4 for want of
GH_TOKEN), so the step body is exercised here rather than trusted to the next
cron. Stdlib only; no network, `gh` stubbed on PATH.
"""
import os
import re
import subprocess
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "sync-docs.yml"
BRANCH = "docs/engine-mirror"
GH_STUB = """#!/usr/bin/env bash
echo "gh $*" >> "$GH_LOG"
case "$1" in
  pr) case "$2" in
        list) if [ -n "${FAKE_OPEN_PR:-}" ]; then echo "$FAKE_OPEN_PR"; fi ;;
      esac ;;
esac
exit 0
"""


def sh(cmd: str, cwd: Path) -> str:
    r = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    assert r.returncode == 0, f"$ {cmd}\n{r.stdout}{r.stderr}"
    return r.stdout.strip()


def step_body() -> str:
    """The exact shell of the step that fails, read from the workflow file."""
    m = re.search(r"- name: Open or update PR\n(?:.*\n)*?\s+run: \|\n((?: {10}.*\n?)+)",
                  WORKFLOW.read_text())
    assert m, "the 'Open or update PR' step is missing from sync-docs.yml"
    return textwrap.dedent(m.group(1))


@pytest.fixture()
def sandbox(tmp_path: Path) -> Path:
    gh = tmp_path / "bin"
    gh.mkdir()
    stub = gh / "gh"
    stub.write_text(GH_STUB)
    stub.chmod(0o755)
    sh("git init -q --bare origin.git", tmp_path)
    src = tmp_path / "src"
    (src / "scripts").mkdir(parents=True)
    eng = src / "skills" / "basal-serve" / "references" / "engine"
    eng.mkdir(parents=True)
    sh("git init -q -b main . && git config user.name t && git config user.email t@t", src)
    (src / "README.md").write_text("sandbox\n")
    (src / "scripts" / "sync_docs.py").write_text("# stub\n")
    (eng / "API.md").write_text("old docs\n")
    (eng / "MANIFEST.json").write_text('{"commit": "' + "a" * 40 + '"}\n')
    sh("git add -A && git commit -qm init", src)
    sh("git remote add origin ../origin.git && git push -q origin main", src)
    return tmp_path


def clone(sandbox: Path, *, stale_branch: bool) -> Path:
    """A checkout like actions/checkout@v4: single branch, depth 1, no other refs."""
    work = sandbox / "work"
    sh("git clone -q --depth 1 --single-branch --branch main origin.git work", sandbox)
    sh("git config user.name t && git config user.email t@t", work)
    if stale_branch:  # an earlier run (or a merged PR) left the branch on the remote
        sh("git checkout -q -b {b} && echo older > skills/basal-serve/references/engine/API.md"
           " && git add -A && git commit -qm older && git push -q origin {b}".format(b=BRANCH),
           sandbox / "src")
    return work


def run_step(sandbox: Path, work: Path, open_pr=None) -> subprocess.CompletedProcess:
    env = {**os.environ, "PATH": f"{sandbox / 'bin'}:{os.environ['PATH']}",
           "GITHUB_REPOSITORY": "patrykorwat/basal-skills",
           "GITHUB_OUTPUT": str(sandbox / "out.txt"),
           "GH_LOG": str(sandbox / "gh.log"),
           "GIT_AUTHOR_NAME": "bot", "GIT_AUTHOR_EMAIL": "bot@bot",
           "GIT_COMMITTER_NAME": "bot", "GIT_COMMITTER_EMAIL": "bot@bot"}
    if open_pr:
        env["FAKE_OPEN_PR"] = str(open_pr)
    (sandbox / "gh.log").write_text("")
    eng = work / "skills" / "basal-serve" / "references" / "engine"
    eng.joinpath("API.md").write_text("NEW docs from upstream\n")
    eng.joinpath("MANIFEST.json").write_text('{"commit": "' + "b" * 40 + '"}\n')
    return subprocess.run(["bash", "-c", step_body()], cwd=work, env=env,
                          capture_output=True, text=True)


def remote_sha(work: Path) -> str | None:
    for line in sh(f"git ls-remote --refs origin refs/heads/{BRANCH}", work).splitlines():
        sha, ref = line.split("\t")
        if ref == f"refs/heads/{BRANCH}":
            return sha
    return None


def gh_calls(sandbox: Path) -> str:
    return (sandbox / "gh.log").read_text()


def test_first_run_pushes_the_branch_and_opens_a_pr(sandbox):
    work = clone(sandbox, stale_branch=False)
    r = run_step(sandbox, work)
    assert r.returncode == 0, r.stdout + r.stderr
    assert remote_sha(work) == sh("git rev-parse HEAD", work)
    calls = gh_calls(sandbox)
    assert "pr create" in calls and "pr edit" not in calls


def test_existing_remote_branch_is_not_refused(sandbox):
    """The production bug: with no remote-tracking ref, --force-with-lease could
    not guess the branch's value and died on "stale info" before gh ran."""
    work = clone(sandbox, stale_branch=True)
    before = remote_sha(work)
    assert before, "precondition: the branch should already be on the remote"
    r = run_step(sandbox, work)
    assert r.returncode == 0, r.stdout + r.stderr
    after = remote_sha(work)
    assert after not in (None, before) and after == sh("git rev-parse HEAD", work)


def test_open_pr_is_updated_not_duplicated(sandbox):
    work = clone(sandbox, stale_branch=True)
    r = run_step(sandbox, work, open_pr=7)
    assert r.returncode == 0, r.stdout + r.stderr
    calls = gh_calls(sandbox)
    assert "pr edit 7" in calls and "pr create" not in calls


def test_gh_is_given_a_token():
    """Without GH_TOKEN every gh call exits 4 — that is what killed run 11."""
    assert "GH_TOKEN" in WORKFLOW.read_text()
