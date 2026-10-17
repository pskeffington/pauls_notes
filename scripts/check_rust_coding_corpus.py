#!/usr/bin/env python3
"""Offline integrity check for Rust coding sources and pinned native ML baseline.

Checks evidence/register claims, not external paper results or dependency security.
"""
import csv
import re
import tomllib
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "02_biomedical_coding/rust_coding_best_practices_sources.csv"
GUIDE = ROOT / "02_biomedical_coding/RUST_CODING_BEST_PRACTICES.md"
MANIFEST = ROOT / "04_machine_learning/rust/Cargo.toml"
TOOLCHAIN = ROOT / "04_machine_learning/rust/rust-toolchain.toml"
LOCK = ROOT / "04_machine_learning/rust/Cargo.lock"
LIBRARY = ROOT / "04_machine_learning/rust/src/lib.rs"

FIELDS = (
    "id", "kind", "year", "title", "authors_or_owner", "venue_or_document",
    "identifier", "source_url", "topic", "review_scope", "source_finding",
    "limitation", "project_action", "gate_id", "checked_on",
    "local_execution", "clinical_validation",
)
KIND_TO_PREFIX = {
    "paper": "P", "preprint": "P",
    "primary_documentation": "D", "tool_documentation": "T",
}
GATES = {f"RG-{n:02d}" for n in range(1, 11)}
PAPER_SCOPES = {"abstract_metadata", "abstract_and_selected_publisher_sections"}
DOC_SCOPES = {"primary_sections"}


def read_rows(path=REGISTRY):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def inspect(rows, guide, root=ROOT, today=None):
    today = today or date.today()
    errors = []
    ids, identifiers, urls = set(), set(), set()
    cards = re.findall(r"^#### (RC-[PDT]\d{2})\s*$", guide, flags=re.M)
    counts = Counter()
    for n, row in enumerate(rows, start=2):
        if set(row) != set(FIELDS) or any(v is None for v in row.values()):
            errors.append(f"row {n}: malformed evidence fields")
            continue
        ident = row["id"].strip()
        if any(not value.strip() for value in row.values()):
            errors.append(f"{ident}: missing evidence field")
        kind = row["kind"]
        prefix = KIND_TO_PREFIX.get(kind)
        if prefix is None or not re.fullmatch(rf"RC-{prefix}\d{{2}}", ident):
            errors.append(f"{ident}: invalid kind or ID")
        counts[kind] += 1
        if ident in ids:
            errors.append(f"{ident}: duplicate ID")
        ids.add(ident)
        normalized = row["identifier"].lower()
        if normalized in identifiers:
            errors.append(f"{ident}: duplicate source identifier")
        identifiers.add(normalized)
        url = row["source_url"]
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
            errors.append(f"{ident}: invalid HTTPS source")
        if url in urls:
            errors.append(f"{ident}: duplicate source URL")
        urls.add(url)
        if row["gate_id"] not in GATES:
            errors.append(f"{ident}: unknown engineering gate")
        try:
            reviewed = date.fromisoformat(row["checked_on"])
            if reviewed > today or reviewed < date(2026, 10, 17):
                raise ValueError
        except ValueError:
            errors.append(f"{ident}: invalid review date")
        if row["local_execution"] != "not_run" or row["clinical_validation"] != "not_established":
            errors.append(f"{ident}: unbacked execution or clinical-validity claim")
        if kind in {"paper", "preprint"}:
            try:
                yr = int(row["year"])
                if not 2021 <= yr <= 2026:
                    raise ValueError
            except ValueError:
                errors.append(f"{ident}: outside recent research window")
            if row["review_scope"] not in PAPER_SCOPES:
                errors.append(f"{ident}: unsupported full-text claim")
            if kind == "paper" and not re.fullmatch(r"10\.\d{4,9}/\S+", row["identifier"], re.I):
                errors.append(f"{ident}: paper needs publisher DOI")
            if kind == "preprint":
                match = re.fullmatch(r"arxiv:(\d{4}\.\d{4,5}v\d+)", row["identifier"], re.I)
                if not match or not url.endswith("/" + (match[1] if match else "")):
                    errors.append(f"{ident}: preprint needs matching versioned URL")
        else:
            if row["year"] != "living" or row["review_scope"] not in DOC_SCOPES:
                errors.append(f"{ident}: documentation cannot be counted as dated paper")
            if not re.fullmatch(r"(?:doc|tool):[a-z0-9][a-z0-9.\-]*", row["identifier"]):
                errors.append(f"{ident}: invalid documentation identity")
        if len(row["source_finding"]) < 35 or len(row["limitation"]) < 35 or len(row["project_action"]) < 35:
            errors.append(f"{ident}: too little support/limitation/code-action detail")
        if f"#### {ident}\n" not in guide:
            errors.append(f"{ident}: missing guide appraisal")
        if url not in guide:
            errors.append(f"{ident}: primary source URL absent from guide")
    if not rows or len(rows) < 30:
        errors.append("Rust coding corpus is missing or unexpectedly small")
    if counts["paper"] < 6 or counts["preprint"] < 2 or counts["primary_documentation"] < 15 or counts["tool_documentation"] < 8:
        errors.append("Source classes cannot be silently reduced or promoted")
    if len(cards) != len(set(cards)) or set(cards) != ids:
        errors.append("Source cards must match the register exactly")
    for gate in GATES:
        if gate not in guide:
            errors.append(f"Missing engineering gate {gate}")
    if "SYNTHETIC" not in guide.upper() or "NOT" not in guide.upper() or "clinical" not in guide.lower():
        errors.append("Missing explicit scientific/nonclinical boundary")
    return errors


def inspect_rust_baseline(root=ROOT):
    """Static pin check only, not compilation or a dependency audit."""
    errors = []
    manifest = root / "04_machine_learning/rust/Cargo.toml"
    toolchain = root / "04_machine_learning/rust/rust-toolchain.toml"
    try:
        m = tomllib.loads(manifest.read_text(encoding="utf-8"))
        t = tomllib.loads(toolchain.read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError) as exc:
        return [f"Missing or invalid Rust manifest/toolchain: {type(exc).__name__}"]
    if m.get("package", {}).get("edition") != "2021" or m["package"].get("rust-version") != "1.90":
        errors.append("Frozen Rust edition or MSRV changed")
    if t.get("toolchain", {}).get("channel") != "1.90.0":
        errors.append("Frozen Rust compiler changed")
    deps = m.get("dependencies", {})
    for name, version in {"csv": "=1.4.0", "serde": "=1.0.229", "serde_json": "=1.0.154",
                           "sha2": "=0.10.9", "linfa": "=0.8.1",
                           "linfa-logistic": "=0.8.1", "ndarray": "=0.16.1"}.items():
        item = deps.get(name)
        actual = item if isinstance(item, str) else item.get("version") if isinstance(item, dict) else None
        if actual != version:
            errors.append(f"Unexpected frozen dependency: {name}")
    if not (root / "04_machine_learning/rust/Cargo.lock").is_file():
        errors.append("Missing Cargo.lock")
    lib = root / "04_machine_learning/rust/src/lib.rs"
    if not lib.is_file() or "#![forbid(unsafe_code)]" not in lib.read_text():
        errors.append("Missing first-party Rust forbid(unsafe_code)")
    return errors


def main():
    errors = inspect(read_rows(), GUIDE.read_text(encoding="utf-8")) + inspect_rust_baseline()
    if errors:
        raise SystemExit("\n".join(errors))
    print("PASS: Rust coding corpus 34 sources; classifications, reviewed claims, source cards and pinned Rust baseline")


if __name__ == "__main__":
    main()
