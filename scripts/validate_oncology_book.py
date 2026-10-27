#!/usr/bin/env python3
"""Validate oncology book navigation, stable identifiers and manuscript status."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "oncology" / "book-manifest.json"
ALLOWED = {"planned", "draft", "tested", "reviewed", "released"}

def validate(root=ROOT):
    problems = []
    manifest = json.loads((root / "oncology/book-manifest.json").read_text(encoding="utf-8"))
    chapters = [c for part in manifest["parts"] for c in part["chapters"]]
    ids = [c["id"] for c in chapters]
    if len(chapters) != manifest["chapters_total"]:
        problems.append("declared chapter count differs")
    if len(set(ids)) != len(ids):
        problems.append("duplicate chapter identifiers")
    if ids != ["CO-" + str(i).zfill(2) for i in range(1, len(ids) + 1)]:
        problems.append("chapter IDs not sequential")
    for path_key in ("canonical_roadmap", "introduction_path", "navigation_path"):
        p = manifest.get(path_key)
        if not isinstance(p, str) or not (root / p).is_file():
            problems.append(f"missing {path_key}: {p}")
    for c in chapters:
        path = c.get("chapter_path")
        if c.get("status") not in ALLOWED:
            problems.append(f"invalid status {c['id']}")
        if c.get("status") != "planned" and not path:
            problems.append(f"nonplanned chapter missing manuscript: {c['id']}")
        if path:
            resolved = (root / path).resolve()
            if not resolved.is_relative_to((root / "oncology").resolve()) or not resolved.is_file():
                problems.append(f"invalid chapter_path: {c['id']}")
        if any(pr not in ids for pr in c.get("prerequisites", [])):
            problems.append(f"unknown prerequisite: {c['id']}")
        if c["id"] in c.get("prerequisites", []):
            problems.append(f"self prerequisite: {c['id']}")
    return problems

if __name__ == "__main__":
    issues = validate()
    for issue in issues:
        print("ERROR:", issue)
    print(f"Book manifest: {len(issues)} error(s)")
    raise SystemExit(bool(issues))
