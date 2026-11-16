#!/usr/bin/env python3
"""Fail on known biomedical documentation regressions, without rewriting files.

Scope is deliberately limited to entrypoint/navigation and core method pages.
Source bibliography and long-lived historical evidence are not modified.
"""
from pathlib import Path
import posixpath
import re

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "README.md",
    "AGENTS.md",
    "llms.txt",
    "docs/machine-index.md",
    "02_biomedical_coding/README.md",
    "03_learning/README.md",
    "03_learning/bio_stats/README.md",
    "03_learning/bio_stats/R_VALIDATION_STATUS.md",
    "03_learning/bio_stats/BREAST_CANCER_WORKED_TEST_ATLAS.md",
    "03_learning/bio_stats/BIOSTAT_TEST_SELECTION_MATRIX.md",
    "03_learning/bio_stats/CANCER_STUDY_DESIGN.md",
    "06_RESOURCES/R/README.md",
)
# The bibliographic entry itself is intentionally not part of this check.
PLACEHOLDERS = ("Biomedical methods", "the cited textbook author")
REQUIRED_ROUTES = {
    "README.md": (
        "03_learning/bio_stats/GRAPH_METHODS_ALIGNMENT.md",
        "02_biomedical_coding/BIOSTAT_8E_VERIFICATION_ACCEPTANCE_LEDGER.md",
    ),
    "AGENTS.md": (
        "scripts/check_methodology_attribution.py",
        "06_RESOURCES/R/biostat_graphs.R",
    ),
    "03_learning/bio_stats/README.md": (
        "03_learning/bio_stats/R_VALIDATION_STATUS.md",
        "02_biomedical_coding/BIOSTAT_8E_VERIFICATION_ACCEPTANCE_LEDGER.md",
    ),
    "docs/machine-index.md": (
        "03_learning/bio_stats/GRAPH_METHODS_SYNTHETIC_GALLERY.Rmd",
        "06_RESOURCES/tests/test_biostat_graphs.R",
    ),
}

def narrative_lines(text):
    """Ignore deliberate escape characters inside Markdown code spans/fences."""
    fenced = False
    fence_char = None
    fence_width = 0
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if not fenced:
                fenced = True
                fence_char = marker[0]
                fence_width = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_width:
                fenced = False
            continue
        if not fenced:
            yield re.sub(r"`[^`]*`", "", line)


def inspect_page(relative, text):
    """Return narrowly defined, line-oriented problems for one file."""
    failures = []
    if any("\\n" in line for line in narrative_lines(text)):
        failures.append("literal backslash-n found in narrative Markdown")
    for term in PLACEHOLDERS:
        if term.casefold() in text.casefold():
            failures.append("legacy placeholder terminology: " + term)
    # The source author's name is encoded to keep the policy checker neutral.
    attribution_token = bytes.fromhex("726f736e6572").decode("ascii")
    if attribution_token in text.casefold():
        failures.append("author attribution outside the bibliography")
    if relative == "03_learning/bio_stats/README.md":
        if "historical, bounded execution" not in text or "runtime and report-rendering gates remain pending" not in text:
            failures.append("historical atlas and later workbook must have distinct evidence scopes")
    if relative == "03_learning/bio_stats/R_VALIDATION_STATUS.md":
        if "Evidence epochs and acceptance boundaries" not in text or "17-chunk workbook" not in text:
            failures.append("validation status must distinguish the historical atlas from new workbook")
    for route in REQUIRED_ROUTES.get(relative, ()):
        relative_link = posixpath.relpath(
            route, start=posixpath.dirname(relative) or "."
        )
        if route not in text and ("(" + relative_link + ")") not in text:
            failures.append("canonical route not indexed: " + route)
        elif not (ROOT / route).is_file():
            failures.append("canonical route target missing: " + route)
    return failures

def validate():
    errors = []
    for relative in PAGES:
        file_path = ROOT / relative
        if not file_path.is_file():
            errors.append(f"{relative}: missing canonical document")
            continue
        content = file_path.read_text(encoding="utf-8")
        errors.extend(f"{relative}: {issue}"
                      for issue in inspect_page(relative, content))
    return errors

if __name__ == "__main__":
    problems = validate()
    if problems:
        for issue in problems:
            print("FAIL:", issue)
        raise SystemExit(1)
    print(f"PASS: {len(PAGES)} documentation entrypoints free of known formatting and routing regressions.")
