#!/usr/bin/env python3
"""Verify that drafted oncology textbook sections contain linked, registered sources.

Structural citation coverage is NOT a claim of scientific peer review or an
automatic judgment that every sentence is supported by its nearby sources.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCES = "oncology/evidence/source-registry.json"
COVERAGE = "oncology/evidence/section-citations.json"
MANIFEST = "oncology/book-manifest.json"
SOURCE_INDEX = "oncology/evidence/SOURCES.md"
HEAD = re.compile(r"^(#{2,3})[ \t]+(.+?)\s*$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
REF_LINE = re.compile(r"^\*\*Section references:\*\* (.+)$", re.M)
LINK = re.compile(r"\[([^\]]+)\]\((https://[^)]+)\)")

def section_chunks(markdown: str):
    """Yield H2/H3 sections, ignoring Markdown headings inside fenced code."""
    lines = markdown.splitlines(keepends=True)
    headings = []
    fence_char = None
    min_length = 0
    for i, line in enumerate(lines):
        match = FENCE.match(line)
        if match:
            token = match.group(1)
            if fence_char is None:
                fence_char, min_length = token[0], len(token)
            elif token[0] == fence_char and len(token) >= min_length:
                fence_char = None
            continue
        if fence_char is None:
            heading = HEAD.match(line)
            if heading:
                headings.append((i, heading.group(2).strip()))
    for j, (start, title) in enumerate(headings):
        end = headings[j + 1][0] if j + 1 < len(headings) else len(lines)
        yield title, "".join(lines[start:end])

def safe_file(root: Path, relative: str):
    if not isinstance(relative, str) or not relative.endswith(".md"):
        return None
    target = (root / relative).resolve()
    if not target.is_relative_to((root / "oncology").resolve()) or not target.is_file():
        return None
    return target

def validate(root=ROOT):
    root = Path(root).resolve()
    issues = []
    try:
        sources = json.loads((root / SOURCES).read_text(encoding="utf-8"))
        coverage = json.loads((root / COVERAGE).read_text(encoding="utf-8"))
        manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"manifest error: {exc}"]

    if sources.get("schema_version") != "1.0" or coverage.get("schema_version") != "1.0":
        issues.append("unsupported evidence schema")
    library = {}
    for source in sources.get("sources", []):
        if not isinstance(source, dict):
            issues.append("source record is not an object")
            continue
        identifier, url = source.get("id"), source.get("url")
        if not isinstance(identifier, str) or not re.fullmatch(r"[A-Z][A-Z0-9-]+", identifier):
            issues.append(f"invalid source ID {identifier!r}")
            continue
        if identifier in library:
            issues.append(f"duplicate source ID {identifier}")
        library[identifier] = source
        parsed = urlsplit(url if isinstance(url, str) else "")
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            issues.append(f"{identifier}: invalid HTTPS link")
        if not source.get("title") or not source.get("kind") or not source.get("supports"):
            issues.append(f"{identifier}: incomplete source metadata")

    try:
        source_index = (root / SOURCE_INDEX).read_text(encoding="utf-8")
    except OSError:
        source_index = ""
        issues.append("missing readable source bibliography")
    for identifier, source in library.items():
        if f"[{source.get('title')}]({source.get('url')})" not in source_index:
            issues.append(f"source bibliography missing link for {identifier}")

    documents = coverage.get("documents", [])
    covered_paths = set()
    for doc in documents:
        if not isinstance(doc, dict):
            issues.append("invalid citation document record")
            continue
        path, expected = doc.get("path"), doc.get("citations")
        if path in covered_paths:
            issues.append(f"duplicate citation document: {path}")
        covered_paths.add(path)
        full_path = safe_file(root, path)
        if full_path is None:
            issues.append(f"missing or unsafe citation document: {path}")
            continue
        if not isinstance(expected, dict):
            issues.append(f"{path}: citation mapping must be object")
            continue
        actual_sections = list(section_chunks(full_path.read_text(encoding="utf-8")))
        actual_names = [heading for heading, _ in actual_sections]
        if len(set(actual_names)) != len(actual_names):
            issues.append(f"{path}: repeated H2/H3 names require unique headings")
        if set(actual_names) != set(expected):
            missing = sorted(set(actual_names) - set(expected))
            stale = sorted(set(expected) - set(actual_names))
            issues.append(f"{path}: unmapped headings {missing}, stale mappings {stale}")
        for heading, section in actual_sections:
            ids = expected.get(heading)
            if not isinstance(ids, list) or not ids or len(ids) != len(set(ids)):
                issues.append(f"{path} [{heading}]: empty/duplicate source IDs")
                continue
            line_matches = REF_LINE.findall(section)
            if len(line_matches) != 1:
                issues.append(f"{path} [{heading}]: expected one section reference line")
                continue
            actual_links = LINK.findall(line_matches[0])
            if len(actual_links) != len(ids):
                issues.append(f"{path} [{heading}]: source link count mismatch")
            expected_links = []
            for identifier in ids:
                source = library.get(identifier)
                if not source:
                    issues.append(f"{path} [{heading}]: unknown source ID {identifier}")
                    continue
                expected_links.append((source["title"], source["url"]))
            if actual_links != expected_links:
                issues.append(f"{path} [{heading}]: link/title mismatch with source registry")

    required = {manifest.get("introduction_path")}
    for part in manifest.get("parts", []):
        for chapter in part.get("chapters", []):
            if chapter.get("status") != "planned":
                required.add(chapter.get("chapter_path"))
    for path in sorted(required, key=str):
        if path not in covered_paths:
            issues.append(f"draft text missing citation coverage: {path}")
    return issues

def main():
    issues = validate()
    for problem in issues:
        print("ERROR: " + problem, file=sys.stderr)
    print(f"Oncology section citation gate: {'PASS' if not issues else 'FAIL'} ({len(issues)} issues)")
    return int(bool(issues))

if __name__ == "__main__":
    raise SystemExit(main())
