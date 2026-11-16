#!/usr/bin/env python3
"""Check the canonical reader/agent navigation manifest and entrypoint links.

This stdlib-only check validates navigation source and file existence, not
scientific validity, Markdown anchors throughout the repository, or CI success.
"""
from __future__ import annotations
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = "docs/navigation-routes.json"
READER_GUIDE = "docs/NAVIGATION.md"
ENTRYPOINTS = ("README.md", "03_learning/README.md",
               "02_biomedical_coding/README.md", "06_RESOURCES/README.md",
               "oncology/README.md", "llms.txt", "docs/machine-index.md")
REQUIRED_ROUTES = {"research_question", "research_protocol",
                   "biostatistics", "r_learning", "figures",
                   "biomedical_coding", "oncology_textbook",
                   "genomics", "machine_learning", "unix", "rust",
                   "acceptance", "agent"}
ALLOWED_AUDIENCES = {"reader", "agent"}
ROUTE_ID = re.compile(r"^[a-z][a-z0-9_]*$")
REQUIRED_FIELDS = {"id", "label", "audience", "entry", "next", "boundary"}


def validate_manifest(obj, root=ROOT):
    """Return stable, explicit validation failures for a parsed route manifest."""
    problems = []
    if not isinstance(obj, dict) or obj.get("schema_version") != "1.0":
        return ["Navigation manifest requires schema version 1.0"]
    routes = obj.get("routes")
    if not isinstance(routes, list) or not routes:
        return ["Navigation routes must be a nonempty list"]
    ids = []
    for i, route in enumerate(routes):
        where = f"route {i}"
        if not isinstance(route, dict) or set(route) != REQUIRED_FIELDS:
            problems.append(where + ": invalid route field set")
            continue
        route_id = route["id"]
        if not isinstance(route_id, str) or not ROUTE_ID.fullmatch(route_id):
            problems.append(where + ": invalid ID")
            continue
        ids.append(route_id)
        for key in ("label", "boundary"):
            if not isinstance(route[key], str) or not route[key].strip():
                problems.append(route_id + ": empty " + key)
        audience = route["audience"]
        if not isinstance(audience, list) or not audience or (
                len(set(str(x) for x in audience)) != len(audience)) or (
                not set(audience) <= ALLOWED_AUDIENCES):
            problems.append(route_id + ": invalid audience")
        entry = route["entry"]
        if not isinstance(entry, str) or not entry or entry.startswith("/") or (
                ".." in Path(entry).parts) or "\\" in entry:
            problems.append(route_id + ": invalid relative entry path")
        elif not (root / entry).is_file():
            problems.append(route_id + ": missing entry " + entry)
        neighbors = route["next"]
        if not isinstance(neighbors, list) or len(neighbors) != len(set(map(str, neighbors))):
            problems.append(route_id + ": invalid next edges")
        elif route_id in neighbors:
            problems.append(route_id + ": self-loop next edge")
    if len(ids) != len(set(ids)):
        problems.append("Duplicate route IDs")
    missing = REQUIRED_ROUTES - set(ids)
    if missing:
        problems.append("Missing required routes: " + ", ".join(sorted(missing)))
    known = set(ids)
    for route in routes:
        if not isinstance(route, dict) or not isinstance(route.get("next"), list):
            continue
        unknown = [n for n in route["next"] if not isinstance(n, str) or n not in known]
        if unknown:
            problems.append(str(route.get("id")) + ": unknown next route")
    return problems


def validate(root=ROOT):
    problems = []
    manifest = root / MANIFEST
    if not manifest.is_file():
        return ["Missing navigation manifest: " + MANIFEST]
    try:
        obj = json.loads(manifest.read_text(encoding="utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        return ["Cannot parse navigation manifest: " + str(exc)]
    problems.extend(validate_manifest(obj, root))
    guide = root / READER_GUIDE
    if not guide.is_file():
        problems.append("Missing reader-facing navigation guide")
    else:
        text = guide.read_text(encoding="utf-8")
        if "(navigation-routes.json)" not in text:
            problems.append("Navigation guide missing canonical manifest link")
        if "(machine-index.md)" not in text:
            problems.append("Navigation guide missing machine index link")
    for relative in ENTRYPOINTS:
        path = root / relative
        if not path.is_file():
            problems.append("Missing entrypoint: " + relative)
            continue
        text = path.read_text(encoding="utf-8")
        if relative in ("README.md", "llms.txt", "docs/machine-index.md"):
            if "NAVIGATION.md" not in text:
                problems.append(relative + ": navigation guide not discoverable")
    return sorted(set(problems))


if __name__ == "__main__":
    failures = validate()
    if failures:
        for failure in failures:
            print("FAIL: " + failure)
        raise SystemExit(1)
    print("PASS: canonical reader/agent navigation manifest and entrypoint routes")
