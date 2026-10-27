#!/usr/bin/env python3
"""Validate curated method routes against tracked source documents and literature IDs."""
import argparse
import json
import re
import sys
from pathlib import Path

def validate(root):
    registry = json.loads((root / "docs/research-method-map.json").read_text(encoding="utf-8"))
    problems = []
    if registry.get("schema_version") != "1.0": problems.append("invalid schema_version")
    methods = registry.get("methods")
    if not isinstance(methods, list) or not methods: return ["methods must be a nonempty list"]
    ids = set()
    evidence_path = root / "06_RESOURCES/Literature/BIOSTATISTICS_R_LITERATURE_2021_2026.md"
    evidence = evidence_path.read_text(encoding="utf-8") if evidence_path.is_file() else ""
    supported = set(re.findall(r"\bBS-\d{3}\b", evidence))
    for n, method in enumerate(methods):
        if not isinstance(method, dict):
            problems.append(f"method {n} must be an object")
            continue
        key = method.get("id")
        if not isinstance(key, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", key):
            problems.append(f"method {n}: invalid id")
        elif key in ids:
            problems.append(f"duplicate method id: {key}")
        ids.add(key)
        guide = method.get("guide")
        if not isinstance(guide, str) or not guide.endswith(".md"):
            problems.append(f"{key}: invalid guide")
        else:
            candidate = (root / guide).resolve()
            if not candidate.is_relative_to(root.resolve()) or not candidate.is_file():
                problems.append(f"{key}: missing or unsafe guide path: {guide}")
        evidence_ids = method.get("evidence_ids")
        if not isinstance(evidence_ids, list) or any(not isinstance(x, str) for x in evidence_ids):
            problems.append(f"{key}: evidence_ids must be strings")
        else:
            for evidence_id in evidence_ids:
                if evidence_id not in supported:
                    problems.append(f"{key}: unknown evidence id {evidence_id}")
    return problems

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = p.parse_args()
    problems = validate(args.root.resolve())
    for issue in problems: print(issue, file=sys.stderr)
    print("Method registry: valid" if not problems else f"Method registry: {len(problems)} errors")
    return int(bool(problems))

if __name__ == "__main__":
    raise SystemExit(main())
