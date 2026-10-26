"""Versioning rules from AGENTS.md (enforced)."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

# One version for the whole repo. Docs/infra changes and the mechanical
# engine-docs mirror don't require a VERSION bump; authored content does.
DOCS_ONLY = {
    "VERSION", "plugin.yaml", "CHANGELOG.md", "AGENTS.md", "README.md",
    "CONTRIBUTING.md", "LICENSE", ".gitignore", "pytest.ini",
}
EXEMPT_PREFIXES = (".github/",)
MIRROR_MARKER = "/references/engine/"


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args], capture_output=True, text=True
    )


def test_version_file_is_semver():
    assert SEMVER.match((ROOT / "VERSION").read_text().strip())


def test_plugin_yaml_mirrors_project_version():
    text = (ROOT / "plugin.yaml").read_text()
    m = re.search(r"^version:\s*(\S+)", text, re.M)
    assert m, "plugin.yaml has no version"
    assert m.group(1) == (ROOT / "VERSION").read_text().strip()


def test_changelog_contains_current_version():
    v = (ROOT / "VERSION").read_text().strip()
    assert f"[{v}]" in (ROOT / "CHANGELOG.md").read_text()


def test_desktop_plugin_carries_no_own_version():
    js = (ROOT / "plugins" / "basal-register" / "plugin.js").read_text()
    assert not re.search(r"Version:\s*\d+\.\d+\.\d+", js), (
        "basal-register carries no own version — VERSION is the single source"
    )


def test_mcp_bridge_reads_repo_version():
    src = (ROOT / "plugins" / "deepseek_harness" / "basal_mcp.py").read_text()
    assert '"version": _VERSION' in src, "serverInfo must report the repo VERSION"
    assert 'ROOT / "VERSION"' in src, "bridge must read the repo VERSION file"


def test_version_bumped_when_authored_content_changed_since_last_tag():
    tag = _git("describe", "--tags", "--abbrev=0")
    if tag.returncode != 0:
        return  # no release tag yet (shallow CI checkout or pre-release)
    tag = tag.stdout.strip()
    files = _git("diff", "--name-only", f"{tag}..HEAD")
    if files.returncode != 0 or not files.stdout.strip():
        return
    changed = [f for f in files.stdout.splitlines() if f.strip()]
    authored = [
        f for f in changed
        if f not in DOCS_ONLY
        and not f.startswith(EXEMPT_PREFIXES)
        and MIRROR_MARKER not in f
    ]
    if not authored:
        return
    old = _git("show", f"{tag}:VERSION")
    if old.returncode != 0:
        return  # tag predates the VERSION file
    old_v = old.stdout.strip()
    new_v = (ROOT / "VERSION").read_text().strip()
    assert old_v != new_v, (
        f"authored content changed since {tag} but VERSION is still {new_v} "
        f"— bump it (AGENTS.md); changed: {authored[:5]}"
    )
