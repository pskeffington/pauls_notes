#!/usr/bin/env python3
"""Read-only official GDC metadata preflight; NEVER downloads participant data."""
import argparse
import hashlib
import json
import re
import uuid
from collections import Counter
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
API = "https://api.gdc.cancer.gov/files"
PROJECT = "TCGA-BRCA"
ALLOWED_DATA_TYPES = frozenset({
    "Gene Expression Quantification",
    "Clinical Supplement",
    "Biospecimen Supplement",
})
NOTICE = ("RESEARCH/EDUCATION ONLY. NOT A CLINICAL DEVICE. No diagnosis, "
          "treatment selection, individual prognosis or re-identification. "
          "The preflight fetches metadata only, never files.")

def checked_uuid(raw):
    if not isinstance(raw, str):
        raise ValueError("GDC file identifier must be a UUID string")
    try:
        parsed = uuid.UUID(raw)
    except (ValueError, AttributeError) as exc:
        raise ValueError("Invalid GDC file identifier") from exc
    if str(parsed) != raw.lower():
        raise ValueError("Non-canonical GDC file UUID")
    return str(parsed)

def validate_metadata(hit, requested):
    """Accept only explicitly OPEN files belonging only to TCGA-BRCA."""
    requested = checked_uuid(requested)
    if not isinstance(hit, dict) or hit.get("file_id", hit.get("id")) != requested:
        raise ValueError("GDC metadata identity mismatch")
    if hit.get("access") != "open":
        raise ValueError("GDC file is not explicitly open access")
    if hit.get("data_type") not in ALLOWED_DATA_TYPES:
        raise ValueError("File type not on the reviewed open-data allowlist")
    cases = hit.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Missing case-project metadata")
    projects = {
        (item.get("project") or {}).get("project_id")
        for item in cases if isinstance(item, dict)
    }
    if projects != {PROJECT} or len(cases) != sum(isinstance(x, dict) for x in cases):
        raise ValueError("Project mismatch or missing case provenance")
    if type(hit.get("file_size")) is not int or hit["file_size"] <= 0:
        raise ValueError("Invalid GDC file size")
    if not isinstance(hit.get("md5sum"), str) or not re.fullmatch(r"[a-fA-F0-9]{32}", hit["md5sum"]):
        raise ValueError("Missing valid official GDC file checksum")
    return {"data_type": hit["data_type"], "bytes": hit["file_size"]}

def fetch_metadata(file_id):
    """Fetch only GDC file metadata over HTTPS; no credentials and no data download."""
    ident = checked_uuid(file_id)
    fields = "file_id,access,data_type,file_size,md5sum,cases.project.project_id"
    url = API + "/" + ident + "?" + urlencode({"fields": fields})
    request = Request(url, headers={"Accept": "application/json",
                                  "User-Agent": "pauls-notes-gdc-open-preflight/1.0"})
    with urlopen(request, timeout=20) as response:
        payload = response.read(500_001)
    if len(payload) > 500_000:
        raise ValueError("Oversized GDC metadata response")
    record = json.loads(payload)
    if not isinstance(record, dict) or not isinstance(record.get("data"), dict):
        raise ValueError("GDC returned malformed file metadata")
    return record["data"]

def preflight(file_ids, fetch=fetch_metadata):
    if not isinstance(file_ids, list) or not 1 <= len(file_ids) <= 100:
        raise ValueError("Provide 1-100 GDC file UUIDs")
    ids = [checked_uuid(s) for s in file_ids]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate GDC file UUID")
    accepted = [validate_metadata(fetch(fid), fid) for fid in ids]
    return {
        "status": "metadata_only_open_access_preflight_passed",
        "project": PROJECT, "file_count": len(ids),
        "types": dict(sorted(Counter(x["data_type"] for x in accepted).items())),
        "total_declared_bytes": sum(x["bytes"] for x in accepted),
        "file_id_list_sha256": hashlib.sha256(("\n".join(ids) + "\n").encode()).hexdigest(),
        "source": API, "download_performed": False, "training_performed": False,
        "patient_output_exported": False, "model_use_notice": NOTICE,
    }

def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--ids", required=True, type=Path,
                     help="Local text file with one GDC file UUID per line; never case IDs")
    cli.add_argument("--output", required=True, type=Path,
                     help="New directory outside the public repository")
    args = cli.parse_args(argv)
    dest = args.output.resolve()
    if dest.is_relative_to(ROOT) or dest.exists() or not dest.parent.is_dir():
        raise ValueError("Use a new output directory outside the public repository")
    file_ids = [line.strip() for line in args.ids.read_text().splitlines() if line.strip()]
    report = preflight(file_ids)
    dest.mkdir()
    with (dest / "preflight.json").open("x") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
    print("Verified open-access TCGA-BRCA GDC metadata; no data downloaded or trained.")

if __name__ == "__main__":
    main()
