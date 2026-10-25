#!/usr/bin/env python3
"""Mirror rkinas/basal engine docs into docs/engine/ with a provenance manifest.

Stdlib only. Exit 0 when nothing changed, 10 when files changed (workflow
uses this to open a PR). Network or HTTP failures exit non-zero.

Usage: python3 scripts/sync_docs.py
"""
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "skills" / "basal-serve" / "references" / "engine"
REPO = "rkinas/basal"
RAW = f"https://raw.githubusercontent.com/{REPO}/main/docs/"
FILES = ["API.md", "TASKS.md", "OMNI.md", "CALIBRATION.md", "INSTALL.md", "HARDWARE.md"]
UA = {"User-Agent": "basal-skills-docs-sync/1.0"}


def get(url: str, binary: bool = False) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.status, r.read()


def main() -> int:
    # Current commit of main, for provenance. Failure here is fatal: a mirror
    # without provenance is indistinguishable from a stale copy.
    try:
        _, body = get(f"https://api.github.com/repos/{REPO}/commits/main")
        commit = json.loads(body)["sha"]
    except Exception as e:
        print(f"error: cannot resolve HEAD of {REPO}: {e}", file=sys.stderr)
        return 2

    fetched = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    OUT.mkdir(parents=True, exist_ok=True)
    changed = []
    for name in FILES:
        try:
            status, data = get(RAW + name)
        except Exception as e:
            print(f"error: {name}: {e}", file=sys.stderr)
            return 2
        if status != 200:
            print(f"error: {name}: HTTP {status}", file=sys.stderr)
            return 2
        dest = OUT / name
        if not dest.is_file() or dest.read_bytes() != data:
            dest.write_bytes(data)
            changed.append(name)

    manifest = {
        "source": f"https://github.com/{REPO}/tree/main/docs",
        "commit": commit,
        "fetched_utc": fetched,
        "files": FILES,
    }
    mpath = OUT / "MANIFEST.json"
    if not mpath.is_file() or json.loads(mpath.read_text())["commit"] != commit:
        mpath.write_text(json.dumps(manifest, indent=2) + "\n")
        changed.append("MANIFEST.json")

    if changed:
        print(f"updated {', '.join(changed)} (commit {commit[:10]}, {fetched})")
        return 10
    print(f"up to date (commit {commit[:10]})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
