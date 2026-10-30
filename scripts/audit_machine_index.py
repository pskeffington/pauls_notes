#!/usr/bin/env python3
"""Audit retrieval-index path coverage and report navigation orphan candidates.

Orphan candidates may be intentionally reached via llms.txt, GitHub URLs or APIs.
They are not automatically a failure or a claim of missing scientific evidence.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINTS = frozenset({"README.md", "oncology/README.md", "docs/agent-index.md", "docs/machine-index.md"})


def expected_documents(root: Path) -> set[str]:
    """Mirror the index builder's Markdown inputs, excluding empty files."""
    from build_machine_index import tracked
    return {p.as_posix() for p in tracked(root) if (root / p).read_text(encoding="utf-8").strip()}


def audit(records: list[dict], expected_paths: set[str]) -> dict:
    errors: list[str] = []
    indexed_paths: set[str] = set()
    section_ids: set[str] = set()
    inbound: dict[str, set[str]] = defaultdict(set)
    inbound_per_path: dict[str, tuple[str, ...]] = {}

    for i, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"record {i}: expected an object")
            continue
        path = record.get("path")
        section_id = record.get("section_id")
        references = record.get("inbound_documents")
        if not isinstance(path, str) or not path.endswith((".md", ".markdown")) or PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts:
            errors.append(f"record {i}: invalid source path")
            continue
        indexed_paths.add(path)
        if not isinstance(section_id, str) or not section_id.startswith(path + "#"):
            errors.append(f"record {i}: invalid section identifier")
        elif section_id in section_ids:
            errors.append(f"duplicate section identifier: {section_id}")
        else:
            section_ids.add(section_id)
        if not isinstance(references, list) or not all(isinstance(p, str) for p in references):
            errors.append(f"{path}: inbound_documents is not a string list")
            continue
        if len(set(references)) != len(references):
            errors.append(f"{path}: duplicate incoming document")
        prior = inbound_per_path.get(path)
        current = tuple(sorted(references))
        if prior is not None and prior != current:
            errors.append(f"{path}: inconsistent incoming-link metadata across sections")
        inbound_per_path[path] = current
        inbound[path].update(references)

    missing = sorted(expected_paths - indexed_paths)
    unexpected = sorted(indexed_paths - expected_paths)
    if missing:
        errors.append(f"{len(missing)} tracked Markdown documents missing from index")
    if unexpected:
        errors.append(f"{len(unexpected)} indexed documents not in tracked Markdown input")
    for path, sources in inbound.items():
        for src in sources:
            if src not in indexed_paths:
                errors.append(f"{path}: incoming-link source is not indexed: {src}")

    orphan_candidates = sorted(path for path in indexed_paths - ENTRYPOINTS if not inbound[path])
    return {
        "schema_version": "1.0",
        "indexed_sections": len(records),
        "indexed_documents": len(indexed_paths),
        "expected_documents": len(expected_paths),
        "missing_documents": missing,
        "unexpected_documents": unexpected,
        "orphan_candidates": orphan_candidates,
        "errors": sorted(set(errors)),
        "notes": "Orphans are review candidates, not proof of broken navigation or missing citation support.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        records = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
        expected = expected_documents(args.root)
        report = audit(records, expected)
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"ERROR: cannot audit index: {exc}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Indexed {report['indexed_sections']} sections, {report['indexed_documents']} documents; "
          f"{len(report['orphan_candidates'])} orphan candidates; {len(report['errors'])} structural errors")
    for error in report["errors"]:
        print("ERROR: " + error, file=sys.stderr)
    return int(bool(report["errors"]))


if __name__ == "__main__":
    raise SystemExit(main())
