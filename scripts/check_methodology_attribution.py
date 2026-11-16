#!/usr/bin/env python3
"""Check that teaching, code and navigation are author-neutral.

Named methodological provenance is permitted only in the dedicated bibliography.
Run from the repository root in CI. This is text hygiene, not statistical review.
"""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = "02_biomedical_coding/METHODOLOGY_SOURCE_REFERENCES.md"
# Deliberately store the search token as bytes to avoid author-name branding
# inside the neutral project itself.
AUTHOR_TOKEN = bytes.fromhex("726f736e6572").decode("ascii")

def main():
    try:
        output = subprocess.check_output(
            ["git", "ls-files", "-z", "--cached"], cwd=ROOT
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"Cannot inspect tracked files: {exc}")
    violations = []
    paths = [p.decode("utf-8") for p in output.split(b"\0") if p]
    for relative in paths:
        if AUTHOR_TOKEN in relative.casefold():
            violations.append(f"author-named file path: {relative}")
        path = ROOT / relative
        if relative == REFERENCE or not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".markdown", ".txt", ".r", ".rmd",
                                        ".py", ".csv", ".json", ".yml", ".yaml"}:
            continue
        try:
            data = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if AUTHOR_TOKEN in data.casefold():
            for number, line in enumerate(data.splitlines(),1):
                if AUTHOR_TOKEN in line.casefold():
                    violations.append(f"unnecessary attribution: {relative}:{number}")
    if violations:
        for issue in violations:
            print("FAIL:",issue,file=sys.stderr)
        raise SystemExit(1)
    print(f"PASS: {len(paths)} tracked paths checked; attribution confined to {REFERENCE}.")

if __name__ == "__main__":
    main()
