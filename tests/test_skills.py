"""Structure and hygiene tests for the skills, README and plugin manifest.

No pyyaml: frontmatter and JSON checks use stdlib parsing only.
"""

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIRS = sorted((ROOT / "skills").iterdir())


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, "missing YAML frontmatter"
    fields = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            fields[k.strip()] = v.strip().strip('"')
    return fields


def skill_files():
    return {p.parent.name: p for p in ROOT.glob("skills/*/SKILL.md")}


def test_one_skill_per_directory_and_frontmatter_fields():
    found = skill_files()
    assert sorted(found) == [p.name for p in SKILL_DIRS if (p / "SKILL.md").exists()]
    for name, path in found.items():
        fm = frontmatter(path.read_text(encoding="utf-8"))
        assert fm["name"] == name, f"{name}: frontmatter name mismatch"
        assert fm.get("description", "").startswith("Use when "), f"{name}: description must start with a trigger"
        assert re.match(r"^\d+\.\d+\.\d+$", fm.get("version", "")), f"{name}: bad version"
        assert "author" in fm and "license" in fm


def test_referenced_files_exist():
    for name, path in skill_files().items():
        text = path.read_text(encoding="utf-8")
        for ref in set(re.findall(r"references/([\w.-]+\.md)", text)):
            assert (path.parent / "references" / ref).is_file(), f"{name}: missing references/{ref}"
        for other in set(re.findall(r"`(basal-serve|basal-strategies)`", text)):
            if other != name:
                assert (ROOT / "skills" / other / "SKILL.md").is_file(), f"{name}: dangling link to {other}"


def test_mutual_crosslink_between_skills():
    texts = {name: p.read_text(encoding="utf-8") for name, p in skill_files().items()}
    assert "basal-serve" in texts["basal-strategies"], "basal-strategies must point at basal-serve"
    assert "basal-strategies" in texts["basal-serve"], "basal-omni must point at basal-strategies"


def test_readable_json_blocks():
    """```json blocks are strict JSON; ```jsonc blocks parse after stripping // comments."""
    def strip_comments(block):
        out, in_str, esc = [], False, False
        i = 0
        while i < len(block):
            c = block[i]
            if in_str:
                out.append(c)
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            elif c == '"':
                in_str = True
                out.append(c)
            elif c == "/" and block[i:i + 2] == "//":
                while i < len(block) and block[i] != "\n":
                    i += 1
                continue
            else:
                out.append(c)
            i += 1
        return "".join(out)

    checked = 0
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for block in re.findall(r"```json\n(.*?)```", text, re.S):
            json.loads(block)
            checked += 1
        for block in re.findall(r"```jsonc\n(.*?)```", text, re.S):
            json.loads(strip_comments(block))
            checked += 1
    assert checked >= 4, f"expected several JSON examples, only checked {checked}"


def test_no_machine_paths_or_secrets_in_shipped_files():
    bad = re.compile(r"(/home/[a-z]+|/Users/|C:\\\\|/opt/data|api[_-]?key\s*[:=]\s*\S{8,}|ghp_[A-Za-z0-9]{20,})")
    for path in list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.py")) + list(ROOT.rglob("*.yml")):
        if ".git" in path.parts or path.parent == ROOT / "tests":
            continue
        m = bad.search(path.read_text(encoding="utf-8"))
        assert not m, f"{path.relative_to(ROOT)} leaks machine-specific path or secret: {m.group(0)!r}"


def test_plugin_manifest_and_registration_agree():
    manifest = (ROOT / "plugin.yaml").read_text(encoding="utf-8")
    declared = set(re.findall(r"^\s+- (basal_\w+)$", manifest, re.M))
    import conftest
    registered = set()

    class Ctx:
        def register_tool(self, name, **kw):
            registered.add(name)

        def register_skill(self, name, path):
            assert Path(path).is_file()

    conftest.load_plugin().register(Ctx())
    assert registered == declared == {"basal_decide", "basal_health"}


def test_readable_readme_table_and_install_commands():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for name in skill_files():
        assert f"skills/{name}/SKILL.md" in readme, f"README table missing {name}"
        assert f"--skill {name}" in readme, f"README install section missing {name}"
