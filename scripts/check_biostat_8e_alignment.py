#!/usr/bin/env python3
"""Offline source-to-book alignment gate; no network, textbook files, or patient data.

Usage: python3 scripts/check_biostat_8e_alignment.py
Run from the repository root. This checks document/registry consistency, not
R execution, clinical validity, statistical correctness or full PDF review.
"""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "02_biomedical_coding/biostat_8e_complete_chapter_alignment.csv"
CONTRACT = ROOT / "02_biomedical_coding/BIOSTAT_8E_COMPLETE_METHODOLOGY_CONTRACT.md"
ROADMAP = ROOT / "oncology/BIOSTAT_BREAST_CANCER_BIOSTATS_ALIGNMENT_ROADMAP.md"
MANIFEST = ROOT / "oncology/book-manifest.json"

REQUIRED = {
    "chapter_id", "edition", "title", "printed_start_page", "pdf_start_page",
    "topic_tags", "oncology_chapters", "methodological_contract",
    "required_artifacts", "source_scope", "code_status", "statistical_review"
}

def validate():
    with REGISTRY.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or set(reader.fieldnames) != REQUIRED:
            raise ValueError("Unexpected registry field names")
        records = list(reader)
    if len(records) != 14:
        raise ValueError(f"Expected 14 Biomedical methods 8e chapters, got {len(records)}")
    if any(not all(v.strip() for v in row.values()) for row in records):
        raise ValueError("Blank or missing metadata cells")
    if [r["chapter_id"] for r in records] != [
        f"R8-CH{i:02d}" for i in range(1,15)
    ]:
        raise ValueError("Chapter IDs must be ordered R8-CH01 through R8-CH14")
    if any(r["edition"] != "8" for r in records):
        raise ValueError("Mixed Biomedical methods editions in 8e registry")
    if any(int(r["pdf_start_page"]) - int(r["printed_start_page"]) != 22
           for r in records):
        raise ValueError("PDF/printed start-page offset mismatch")
    if any(int(r["printed_start_page"]) < 1 for r in records):
        raise ValueError("Invalid printed page")
    contract = CONTRACT.read_text(encoding="utf-8")
    roadmap = ROADMAP.read_text(encoding="utf-8")
    for row in records:
        if row["chapter_id"] not in contract:
            raise ValueError("Missing contract section: " + row["chapter_id"])
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    book_ids = {
        chapter["id"]
        for part in manifest["parts"]
        for chapter in part["chapters"]
    }
    for row in records:
        for chapter in row["oncology_chapters"].split(";"):
            if chapter not in book_ids:
                raise ValueError(f"Unknown oncology chapter {chapter}")
    for target in ("BIOSTAT_8E_COMPLETE_METHODOLOGY_CONTRACT.md",
                   "biostat_8e_complete_chapter_alignment.csv"):
        if target not in roadmap:
            raise ValueError("Roadmap must point to " + target)
    if not (ROOT / "06_RESOURCES/tests/test_biostat_descriptive_contract.R").is_file():
        raise ValueError("Missing quantile fixture")
    if not (ROOT / "06_RESOURCES/R/biostat_descriptive_contract.R").is_file():
        raise ValueError("Missing quantile implementation")
    workbook = (ROOT / "02_biomedical_coding/examples/"
                "SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd").read_text(
                    encoding="utf-8")
    import re
    chunk_labels = re.findall(r"^```\\{r\\s+([^,}\\s]+)", workbook, re.M)
    closing_fences = len(re.findall(r"^```\\s*$", workbook, re.M))
    if len(chunk_labels) != 17 or len(set(chunk_labels)) != 17:
        raise ValueError("Expected 17 unique R chunk labels")
    if closing_fences != len(chunk_labels):
        raise ValueError("Unbalanced R Markdown code fences")
    if "wide$score.Follow-up" in workbook:
        raise ValueError("Unsafe hyphenated $ column reference in paired analysis")
    for expr in ('wide[["score.Baseline"]]', 'wide[["score.Follow-up"]]'):
        if expr not in workbook:
            raise ValueError("Paired analysis missing exact column key: " + expr)
    return len(records), len(book_ids)

if __name__ == "__main__":
    count, book_count = validate()
    print(f"PASS: {count} Biomedical methods 8e chapters mapped to {book_count} oncology chapter IDs.")
    print("NOTE: This is structural verification only; R/knit/scientific review pending.")
