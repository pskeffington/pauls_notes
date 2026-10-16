#!/usr/bin/env python3
"""Fail-closed tracked/staged content guard for the public teaching repository.

Heuristic defense in depth: cannot certify absence of all PII/PHI, nor scan Git history.
Never prints sensitive matched values.
"""
import argparse
import csv
import io
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
BLOCKED_DIRS = frozenset({
    "raw_data", "controlled_data", "controlled_access", "restricted_data",
    "patient_data", "participant_data", "external_data", "gdc_downloads",
    "private_data", "research_runs", "model_outputs", "datasets",
})
BLOCKED_ENDINGS = (
    ".bam", ".bai", ".cram", ".fastq", ".fastq.gz", ".fq", ".fq.gz",
    ".vcf", ".vcf.gz", ".maf", ".maf.gz", ".svs", ".dcm", ".dicom",
    ".tar", ".tar.gz", ".tgz", ".zip", ".7z", ".parquet", ".feather",
    ".h5ad", ".rds", ".rdata", ".pkl", ".pickle", ".joblib", ".pt",
    ".pth", ".safetensors", ".onnx", ".pem", ".p12", ".key",
)
DATA_ENDINGS = (".csv", ".tsv", ".json", ".jsonl", ".ndjson")
IDENTIFIER_FIELDS = frozenset({
    "full_name", "first_name", "last_name", "patient_name",
    "subject_name", "medical_record_number", "mrn", "ssn",
    "social_security_number", "date_of_birth", "dob", "street_address",
    "home_address", "address_line_1", "email", "email_address",
    "phone", "phone_number", "patient_id", "case_id",
    "case_submitter_id", "submitter_id",
})
SSN = re.compile(rb"\b\d{3}-\d{2}-\d{4}\b")
EMAIL = re.compile(rb"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
BARCODE = re.compile(rb"\bTCGA-[A-Z0-9]{2}-[A-Z0-9]{4}(?:-[A-Z0-9]{2,4})?\b", re.I)
SECRET = re.compile(
    rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|"
    rb"\b(?:ghp_|gho_|ghu_|ghs_|github_pat_)[A-Za-z0-9_]{15,}",
    re.I,
)

def norm(value):
    return re.sub(r"[^a-z0-9]+", "_", str(value).lower()).strip("_")

def json_keys_and_access(value):
    if isinstance(value, dict):
        for key, item in value.items():
            if norm(key) in IDENTIFIER_FIELDS:
                return True
            if norm(key) == "access" and isinstance(item, str) and item.lower() != "open":
                # Reject controlled/unknown metadata when a data object claims access.
                return True
            if json_keys_and_access(item):
                return True
    elif isinstance(value, list):
        return any(json_keys_and_access(item) for item in value)
    return False

def inspect(path, blob):
    """Return only error categories; no matched values or identifiers."""
    p = PurePosixPath(path)
    lower = str(p).lower()
    errors = []
    if p.is_absolute() or ".." in p.parts or set(part.lower() for part in p.parts) & BLOCKED_DIRS:
        errors.append("restricted directory/path")
    if lower.endswith(BLOCKED_ENDINGS) or (
        p.name.lower().startswith(("clinical.project-tcga-", "biospecimen.project-tcga-"))
    ):
        errors.append("raw dataset, archive, model artifact or credential format")
    if p.name.lower() in {".env", ".env.local", ".env.production", "credentials.json", "gdc-user-token.txt"} or (
        any(word in p.name.lower() for word in ("gdc-token", "dbgap-token", "patient-export"))
    ):
        errors.append("credentials or participant export filename")
    if len(blob) > 5_000_000 and lower.endswith(DATA_ENDINGS):
        errors.append("large tabular data in Git")
    if SECRET.search(blob):
        errors.append("private key or credential signature")
    if SSN.search(blob) and lower.endswith(DATA_ENDINGS):
        errors.append("direct identifier pattern in tabular data")
    if lower.endswith(DATA_ENDINGS):
        if EMAIL.search(blob):
            errors.append("email-like identifier in tabular data")
        if BARCODE.search(blob):
            errors.append("TCGA case/sample barcode in tracked tabular data")
        if lower.endswith((".csv", ".tsv")):
            text = blob.decode("utf-8-sig", errors="replace")
            try:
                header = next(csv.reader(io.StringIO(text), delimiter="\t" if lower.endswith(".tsv") else ","))
            except (csv.Error, StopIteration):
                header = []
            if any(norm(field) in IDENTIFIER_FIELDS for field in header):
                errors.append("direct or pseudonymous identifier column")
        if lower.endswith((".json", ".jsonl", ".ndjson")):
            try:
                lines = [blob] if lower.endswith(".json") else blob.splitlines()
                if any(json_keys_and_access(json.loads(line)) for line in lines if line.strip()):
                    errors.append("identifier field or non-open access metadata")
            except (UnicodeDecodeError, json.JSONDecodeError):
                errors.append("invalid structured data")
    return sorted(set(errors))

def git_output(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])

def paths_and_reader(staged):
    if staged:
        paths = git_output("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z").split(b"\0")
        def reader(path):
            return git_output("show", ":" + path)
    else:
        paths = git_output("ls-files", "-z").split(b"\0")
        def reader(path):
            location = ROOT / path
            if location.is_symlink():
                raise ValueError("symlinks forbidden in tracked repository files")
            return location.read_bytes()
    for encoded in paths:
        if encoded:
            path = encoded.decode("utf-8")
            yield path, reader(path)

def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    selection = cli.add_mutually_exclusive_group(required=True)
    selection.add_argument("--tracked", action="store_true")
    selection.add_argument("--staged", action="store_true")
    args = cli.parse_args(argv)
    failures = []
    for path, blob in paths_and_reader(args.staged):
        for reason in inspect(path, blob):
            failures.append((path, reason))
    if failures:
        for path, reason in failures:
            print(f"BLOCKED {path}: {reason}", file=sys.stderr)
        print(f"Data boundary check FAILED: {len(failures)} issue(s).", file=sys.stderr)
        return 1
    print("Public repository data boundary check passed (heuristic; does not cover Git history).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
