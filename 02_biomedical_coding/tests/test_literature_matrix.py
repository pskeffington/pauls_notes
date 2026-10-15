#!/usr/bin/env python3
"""Offline consistency check for biomedical literature CSV and Markdown."""
import csv
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "biomedical_coding_literature_matrix.csv"
MD = ROOT / "BIOMEDICAL_CODING_LITERATURE_MATRIX.md"
FIELDS = {"id", "domain", "authors", "year", "title", "source_type", "doi", "primary_url", "software", "implementation_practice", "acceptance_check", "failure_mode", "priority", "reviewed"}


def main() -> int:
    with CSV.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        assert set(reader.fieldnames or []) == FIELDS, "Unexpected CSV schema"
        records = list(reader)
    assert len(records) >= 40, "Insufficient source coverage"
    md = MD.read_text(encoding="utf-8")
    assert "# Biomedical Coding Literature Matrix" in md
    doi_seen = set()
    domains = set()
    for number, row in enumerate(records, start=1):
        uid = f"BM-{number:03d}"
        assert row["id"] == uid, f"Invalid stable identifier {uid}"
        assert all((row[field] or "").strip() for field in FIELDS - {"doi"}), uid
        assert re.fullmatch(r"(19|20)[0-9]{2}", row["year"]), uid
        assert 1990 <= int(row["year"]) <= 2026, uid
        assert row["primary_url"].startswith("https://"), uid
        assert row["priority"] in ("core", "applied", "context"), uid
        assert row["reviewed"] == "2026-10-15", uid
        assert uid in md and row["primary_url"] in md, uid
        if row["doi"]:
            key = row["doi"].lower()
            assert key not in doi_seen, f"Duplicate DOI {key}"
            doi_seen.add(key)
            assert row["primary_url"] == "https://doi.org/" + row["doi"], uid
        domains.add(row["domain"])
    assert len(domains) >= 9
    for filename in ("README.md", "IMPLEMENTATION_GATES.md", "PRIMARY_DOCUMENTATION.md"):
        assert (ROOT / filename).is_file(), filename
    print(f"PASS: {len(records)} unique entries and {len(domains)} methodological domains")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
