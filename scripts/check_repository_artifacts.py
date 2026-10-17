#!/usr/bin/env python3
"""Reject tracked editor/build debris without altering scientific artifact policy.

This is a narrow source-tree housekeeping check, NOT a secret/PHI scanner,
a permission check, or a substitute for the separately gated D0 controls.
"""
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BLOCKED_DIRECTORY_NAMES = frozenset({
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".tox", ".venv", "venv", "node_modules", ".idea", "target",
})
BLOCKED_FILE_NAMES = frozenset({
    ".ds_store", "thumbs.db", ".rhistory", ".rdata", "rplots.pdf",
    ".coverage", "coverage.xml",
})
BLOCKED_FILE_SUFFIXES = (".pyc", ".pyo", ".swp", ".swo")


def find_tracked_debris(paths):
    """Return sorted tracked runtime/editor paths; preserve research outputs."""
    hits = []
    for original in paths:
        # Backslash is a literal filename character on Unix but a path
        # separator on Windows. Treat it as a separator for safety.
        normalized = original.replace("\\", "/").strip("/")
        parts = normalized.split("/")
        if not normalized or "." in parts or ".." in parts:
            hits.append(original)
            continue
        parents = {p.lower() for p in parts[:-1]}
        leaf = parts[-1].lower()
        if (parents & BLOCKED_DIRECTORY_NAMES
                or leaf in BLOCKED_FILE_NAMES
                or leaf.endswith(BLOCKED_FILE_SUFFIXES)
                or leaf.endswith("~")
                or leaf.startswith(".#")):
            hits.append(original)
    return sorted(set(hits))


def tracked_paths(root=ROOT):
    completed = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=True, capture_output=True,
    )
    return [
        p.decode("utf-8", errors="surrogateescape")
        for p in completed.stdout.split(b"\0") if p
    ]


def main():
    paths = tracked_paths()
    bad = find_tracked_debris(paths)
    if bad:
        raise SystemExit(
            "Tracked editor/runtime artifacts (remove from Git index, "
            "preserve working copies as appropriate):\n"
            + "\n".join(f"  - {path}" for path in bad)
        )
    print(f"PASS: {len(paths)} tracked paths have no incidental editor/runtime debris")
    print("Scope: does not check secrets, participant data or data admission (D0/D1).")


if __name__ == "__main__":
    main()
