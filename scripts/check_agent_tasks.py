#!/usr/bin/env python3
"""Validate the deterministic agent task registry and textbook chapter paths."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/agent-tasks.json"
MANIFEST = ROOT / "oncology/book-manifest.json"
ID = re.compile(r"^(?:(?:IDX|DOC|CO|GOV|QA|REL)-[0-9]{2}|G[0-9]+-[0-9]{2})$")


def validate(registry: dict, manifest: dict, root: Path) -> list[str]:
    errors: list[str] = []
    if registry.get("schema_version") != "1.0":
        errors.append("unsupported agent registry schema")
    if registry.get("source") != "docs/agent-tasking.md":
        errors.append("unexpected registry authority")
    states = {"ready", "planned", "blocked", "in_progress", "verified"}
    priorities = {"P0", "P1", "P2"}
    tasks = registry.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        return errors + ["tasks must be a nonempty list"]
    ids = [t.get("id") for t in tasks if isinstance(t, dict)]
    if len(ids) != len(tasks) or len(ids) != len(set(ids)):
        errors.append("task IDs must be unique")
    lookup = {t.get("id"): t for t in tasks if isinstance(t, dict)}
    for task in tasks:
        tid = task.get("id")
        if not isinstance(tid, str) or not ID.fullmatch(tid):
            errors.append(f"invalid task id: {tid!r}")
            continue
        if task.get("state") not in states or task.get("priority") not in priorities:
            errors.append(f"{tid}: invalid state or priority")
        if not task.get("summary") or task.get("acceptance_source") != registry.get("source"):
            errors.append(f"{tid}: missing summary or acceptance source")
        if not isinstance(task.get("evidence"), list):
            errors.append(f"{tid}: evidence must be a list")
        deps = task.get("depends_on")
        if not isinstance(deps, list) or len(deps) != len(set(deps)):
            errors.append(f"{tid}: invalid dependency list")
            continue
        for dep in deps:
            if dep == tid or dep not in lookup:
                errors.append(f"{tid}: missing or self dependency {dep!r}")
        if task.get("state") == "verified":
            if not task.get("evidence"):
                errors.append(f"{tid}: verified without recorded evidence")
            for dep in deps:
                if dep in lookup and lookup[dep].get("state") != "verified":
                    errors.append(f"{tid}: verified with unverified dependency {dep}")
    visited: set[str] = set()
    active: set[str] = set()

    def walk(tid: str) -> None:
        if tid in active:
            errors.append(f"dependency cycle at {tid}")
            return
        if tid in visited:
            return
        active.add(tid)
        for dep in lookup[tid].get("depends_on", []):
            if dep in lookup:
                walk(dep)
        active.remove(tid)
        visited.add(tid)

    for tid in lookup:
        walk(tid)
    chapters = [chapter for part in manifest.get("parts", []) for chapter in part.get("chapters", [])]
    if manifest.get("chapters_total") != len(chapters) or len(chapters) != 60:
        errors.append("book manifest chapter count inconsistent")
    chapter_ids = [c.get("id") for c in chapters]
    if len(set(chapter_ids)) != len(chapter_ids):
        errors.append("duplicate textbook chapter IDs")
    for chapter in chapters:
        chapter_id = chapter.get("id")
        path = chapter.get("chapter_path")
        if chapter.get("status") == "draft":
            if not path or not (root / path).is_file():
                errors.append(f"{chapter_id}: draft manuscript missing")
        if chapter.get("status") == "planned" and path:
            errors.append(f"{chapter_id}: planned chapter unexpectedly has manuscript path")
        for extra in chapter.get("lab_paths", []) + chapter.get("test_paths", []):
            if not (root / extra).is_file():
                errors.append(f"{chapter_id}: referenced artifact missing: {extra}")
    return errors


def main() -> int:
    try:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"FAIL: cannot load registry or manifest: {exc}", file=sys.stderr)
        return 1
    errors = validate(registry, manifest, ROOT)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(registry['tasks'])} agent tasks and 60 textbook chapter entries validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
