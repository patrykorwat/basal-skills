"""Versioning rules from AGENTS.md (enforced)."""
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


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


def test_desktop_plugin_carries_a_version():
    js = (ROOT / "plugins" / "basal-register" / "plugin.js").read_text()
    assert re.search(r"Version:\s*\d+\.\d+\.\d+", js)


def test_skill_versions_bumped_when_content_changed_since_last_tag():
    tag = _git("describe", "--tags", "--abbrev=0")
    if tag.returncode != 0:
        return  # no release tag yet (shallow CI checkout or pre-release)
    tag = tag.stdout.strip()
    for skill in sorted((ROOT / "skills").iterdir()):
        changed = _git(
            "diff", "--name-only", f"{tag}..HEAD", "--", f"skills/{skill.name}/"
        )
        if changed.returncode != 0 or not changed.stdout.strip():
            continue
        old = _git("show", f"{tag}:skills/{skill.name}/SKILL.md")
        if old.returncode != 0:
            continue  # skill added after the tag: its own version is new anyway
        old_v = re.search(r"^version:\s*(\S+)", old.stdout, re.M)
        new_v = re.search(r"^version:\s*(\S+)", (skill / "SKILL.md").read_text(), re.M)
        assert new_v and SEMVER.match(new_v.group(1)), f"{skill.name}: bad version"
        assert not old_v or old_v.group(1) != new_v.group(1), (
            f"{skill.name} content changed since {tag} but its version is "
            f"still {old_v.group(1)} — bump it (AGENTS.md)"
        )
