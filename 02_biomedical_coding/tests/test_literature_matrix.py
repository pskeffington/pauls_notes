#!/usr/bin/env python3
"""Offline schema, deduplication, provenance and Markdown concordance checks."""
from __future__ import annotations

import csv
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "biomedical_coding_literature_matrix.csv"
PAPER_MD = ROOT / "BIOMEDICAL_CODING_LITERATURE_MATRIX.md"
METHODS = ROOT / "official_methods_register.csv"
METHOD_MD = ROOT / "OFFICIAL_METHODS_REGISTER.md"

PAPER_FIELDS = {
    "id", "domain", "authors", "year", "title", "source_type", "doi",
    "primary_url", "software", "implementation_practice",
    "acceptance_check", "failure_mode", "priority", "reviewed"
}
METHOD_FIELDS = {
    "id", "source_ref", "category", "title", "source_type",
    "primary_url", "implementation_practice", "acceptance_check",
    "caveat",
    "version_requirement", "reviewed"
}


def load_table(path: Path, required_columns: set[str]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        assert set(reader.fieldnames or ()) == required_columns, path.name
        records = list(reader)
    assert all(set(row) == required_columns for row in records), path.name
    return records


def verify_papers() -> tuple[int, int]:
    records = load_table(PAPERS, PAPER_FIELDS)
    assert len(records) == 71, f"Expected exactly 71 sources, got {len(records)}"
    text = PAPER_MD.read_text(encoding="utf-8")
    unique_dois: set[str] = set()
    groups: set[str] = set()
    for n, row in enumerate(records, 1):
        code = f"BM-{n:03d}"
        assert row["id"] == code, code
        assert all(row[k].strip() for k in PAPER_FIELDS - {"doi"}), code
        assert re.fullmatch(r"(19|20)[0-9]{2}", row["year"]), code
        assert int(row["year"]) <= 2026, code
        assert row["primary_url"].startswith("https://"), code
        assert row["priority"] in {"core", "applied", "context"}, code
        assert row["reviewed"] == "2026-10-15", code
        assert code in text and row["primary_url"] in text, code
        if row["doi"]:
            doi = row["doi"].casefold()
            assert doi not in unique_dois, f"Duplicate DOI: {doi}"
            unique_dois.add(doi)
            assert row["primary_url"] == "https://doi.org/" + row["doi"], code
        groups.add(row["domain"])
    assert len(groups) >= 14
    return len(records), len(groups)


def verify_official_register() -> int:
    records = load_table(METHODS, METHOD_FIELDS)
    assert len(records) == 36, f"Expected 36 provider records; got {len(records)}"
    text = METHOD_MD.read_text(encoding="utf-8")
    urls: set[str] = set()
    for n, row in enumerate(records, 1):
        code = f"OFF-{n:03d}"
        assert row["id"] == code, code
        assert all(row[k].strip() for k in METHOD_FIELDS), code
        assert row["reviewed"] == "2026-10-15", code
        assert re.fullmatch(r"(BIO|QA|STD|INT|ML)-[0-9]{2}", row["source_ref"]), code
        assert row["primary_url"].startswith("https://"), code
        url_key = row["primary_url"].casefold()
        assert url_key not in urls, f"Repeated URL: {url_key}"
        urls.add(url_key)
        assert code in text and row["primary_url"] in text, code
    return len(records)


def main() -> int:
    papers, domains = verify_papers()
    providers = verify_official_register()
    index = (ROOT / "README.md").read_text(encoding="utf-8")
    for link in (
        "BIOMEDICAL_CODING_LITERATURE_MATRIX.md",
        "official_methods_register.csv",
        "OFFICIAL_METHODS_REGISTER.md",
    ):
        assert link in index, f"Missing section navigation: {link}"
    for other in (
        "IMPLEMENTATION_GATES.md",
        "PRIMARY_DOCUMENTATION.md",
    ):
        assert (ROOT / other).is_file(), other
    print(
        f"PASS: {papers} distinct publications over {domains} domains, "
        f"{providers} documented provider resources, provenance and links"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
