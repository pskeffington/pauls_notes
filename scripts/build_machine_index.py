#!/usr/bin/env python3
"""Deterministic, stdlib-only Markdown section catalog for Paul's Notes."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

EXCLUDED = {".git", ".venv", "venv", "node_modules", "__pycache__", "target", "dist", "build"}
HEAD = re.compile(r"^(#{1,6})[ \t]+(.+?)\s*#*\s*$")
LINK = re.compile(r"(?<!!)\[[^\]]+\]\((<[^>]+>|[^)]+)\)")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
SCHEMA = "1.0"

def tracked(root: Path) -> list[Path]:
    try:
        raw = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z", "--cached"], stderr=subprocess.DEVNULL)
        names = [x.decode("utf-8") for x in raw.split(b"\0") if x]
    except (OSError, subprocess.CalledProcessError):
        names = [str(p.relative_to(root)) for p in root.rglob("*.md")]
    return sorted(p for s in names if (p := Path(s)).suffix.lower() in {".md", ".markdown"} and not set(p.parts) & EXCLUDED and (root / p).is_file())

def slug(text: str) -> str:
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<[^>]*>", "", text).lower()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return re.sub(r"-+", "-", re.sub(r"\s+", "-", text)).strip("-")

def sections(text: str):
    lines = text.splitlines(keepends=True)
    headings = []
    fence_char = None
    fence_length = 0
    for i, line in enumerate(lines):
        f = FENCE.match(line)
        if f:
            mark = f.group(1)
            if fence_char is None:
                fence_char, fence_length = mark[0], len(mark)
            elif mark[0] == fence_char and len(mark) >= fence_length and not line.strip()[len(mark):].strip():
                fence_char = None
            continue
        if fence_char is None and (m := HEAD.match(line)):
            headings.append((i, len(m.group(1)), m.group(2).strip()))
    seen = {}
    if not headings or headings[0][0] != 0:
        end = headings[0][0] if headings else len(lines)
        if "".join(lines[:end]).strip():
            yield ("introduction", "Introduction", 1, end, "".join(lines[:end]))
    for j, (start, level, title) in enumerate(headings):
        end = headings[j + 1][0] if j + 1 < len(headings) else len(lines)
        base = slug(title) or "section"
        count = seen.get(base, 0)
        seen[base] = count + 1
        anchor = base if count == 0 else f"{base}-{count}"
        yield anchor, title, start + 1, end, "".join(lines[start:end])

def role(path: Path) -> str:
    s = str(path).lower()
    if s.startswith("templates/"): return "template"
    if "literature" in s or "corpus" in s: return "literature"
    if "roadmap" in s or "milestone" in s: return "status"
    if "protocol" in s: return "protocol"
    if "test" in s: return "test"
    if "example" in s: return "example"
    return "instruction"

def index(root: Path):
    records = []
    problems = []
    files = tracked(root)
    known = set(files)
    for path in files:
        try:
            source = (root / path).read_text(encoding="utf-8")
        except UnicodeError:
            problems.append(f"{path}: invalid UTF-8")
            continue
        entries = list(sections(source))
        anchors = {entry[0] for entry in entries}
        for anchor, title, first, last, body in entries:
            digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
            records.append({"schema_version": SCHEMA, "repository": "pskeffington/pauls_notes",
                            "path": path.as_posix(), "section_id": f"{path.as_posix()}#{anchor}",
                            "heading": title, "start_line": first, "end_line": last,
                            "role": role(path), "content_sha256": digest, "text": body})
        for m in LINK.finditer(source):
            raw = m.group(1).strip().strip("<>").split(" ", 1)[0]
            if not raw or raw.startswith(("#", "mailto:", "tel:", "data:")): continue
            uri = urlsplit(raw)
            if uri.scheme or uri.netloc or raw.startswith("//"): continue
            dest = unquote(uri.path)
            if not dest: continue
            candidate = (root / path.parent / dest).resolve()
            try:
                rel = candidate.relative_to(root.resolve())
            except ValueError:
                problems.append(f"{path}: link escapes repository: {raw}")
                continue
            if not candidate.exists():
                problems.append(f"{path}: broken link: {raw}")
    return records, sorted(set(problems))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--check", action="store_true", help="Verify existing index matches generated records")
    parser.add_argument("--strict-links", action="store_true", help="Fail on broken Markdown paths")
    args = parser.parse_args()
    root = args.root.resolve()
    target = args.output or root / "docs" / "machine-index.jsonl"
    records, problems = index(root)
    rendered = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in records)
    if args.check:
        if not target.is_file() or target.read_text(encoding="utf-8") != rendered:
            print(f"Index stale or missing: {target}", file=sys.stderr)
            return 1
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
    for issue in problems:
        print("LINK: " + issue, file=sys.stderr)
    print(f"Indexed {len(records)} sections across {len(set(r['path'] for r in records))} documents; {len(problems)} link issues")
    return int(args.strict_links and bool(problems))

if __name__ == "__main__":
    raise SystemExit(main())
