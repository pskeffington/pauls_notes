#!/usr/bin/env python3
"""Offline roadmap evidence integrity, not a live GitHub status or clinical approval.

The TOML register is a dated, auditable snapshot. External PR/CI state must be
reverified through GitHub before promotion; this script enforces local contracts.
"""
from __future__ import annotations

import re
import sys
import tomllib
from datetime import date
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs/milestone-evidence.toml"
ROADMAP = ROOT / "docs/roadmap-gates.md"
EXPECTED_IDS = {*(f"G{n}" for n in range(6)), *(f"R{n}" for n in range(5)), "D0", "D1"}
REQUIRED_FIELDS = {
    "id", "track", "title", "status", "delivery", "depends_on", "primary_pr",
    "merge_commit", "reviewed_head", "ci_run_id", "ci_workflow",
    "source_path", "evidence_path", "exit_criteria", "limitations",
    "next_action", "learner_mastery", "clinical_use_authorized",
    "real_patient_training_authorized",
}
STATES = {"complete_bounded", "in_review", "planned", "blocked"}
STATE_LABEL = {
    "complete_bounded": "**Complete (bounded)**",
    "in_review": "**In review",
    "planned": "**Planned**",
    "blocked": "**Blocked**",
}
SHA = re.compile(r"[a-f0-9]{40}\Z")
OWNER = "pskeffington/pauls_notes"


def read_snapshot(path=REGISTRY):
    with path.open("rb") as handle:
        return tomllib.load(handle)


def safe_path(value):
    if not isinstance(value, str) or not value:
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and "\\" not in value


def inspect(snapshot, roadmap, root=ROOT):
    """Return validation issues; do not interpret CI green as approval."""
    errors = []
    if not isinstance(snapshot, dict) or snapshot.get("schema_version") != 1:
        return ["Missing/malformed evidence registry schema version"]
    if snapshot.get("repository") != OWNER:
        errors.append("Registry does not reference the expected public repository")
    try:
        snapshot_date = date.fromisoformat(snapshot["as_of_date"])
        if snapshot_date < date(2026, 10, 16):
            raise ValueError
    except (KeyError, TypeError, ValueError):
        errors.append("Missing or invalid snapshot date")
    if not snapshot.get("status_semantics"):
        errors.append("Status meanings must be documented")
    gates = snapshot.get("gates")
    if not isinstance(gates, list):
        return errors + ["Gate records must be a TOML table array"]
    by_id = {}
    for index, gate in enumerate(gates):
        if not isinstance(gate, dict):
            errors.append(f"Invalid gate at index {index}")
            continue
        ident = gate.get("id")
        if not isinstance(ident, str) or not re.fullmatch(r"(?:G[0-5]|R[0-4]|D[01])", ident):
            errors.append(f"Unknown gate identifier at index {index}")
            continue
        if ident in by_id:
            errors.append(f"{ident}: duplicate milestone identifier")
        by_id[ident] = gate
        if set(gate) != REQUIRED_FIELDS:
            errors.append(f"{ident}: unexpected/missing contract fields")
            continue
        for key in ("title", "track", "exit_criteria", "limitations", "next_action"):
            if not isinstance(gate[key], str) or len(gate[key].strip()) < 24:
                errors.append(f"{ident}: missing substantive {key}")
        if gate["status"] not in STATES:
            errors.append(f"{ident}: invalid delivery state")
            continue
        if gate["learner_mastery"] != "not_assessed":
            errors.append(f"{ident}: a CI result cannot certify personal mastery")
        if gate["clinical_use_authorized"] is not False or gate["real_patient_training_authorized"] is not False:
            errors.append(f"{ident}: release/clinical permission is not established")
        dependencies = gate["depends_on"]
        if not isinstance(dependencies, list) or any(not isinstance(d, str) for d in dependencies):
            errors.append(f"{ident}: malformed dependency list")
        elif len(dependencies) != len(set(dependencies)) or ident in dependencies:
            errors.append(f"{ident}: duplicate/circular direct dependency")
        if not safe_path(gate["source_path"]):
            errors.append(f"{ident}: invalid source path")
        pr = gate["primary_pr"]
        ci = gate["ci_run_id"]
        if type(pr) is not int or pr < 0 or type(ci) is not int or ci < 0:
            errors.append(f"{ident}: PR and CI references must be nonnegative integers")
            continue
        state = gate["status"]
        expected_delivery = {
            "complete_bounded": "main", "in_review": "draft_pr_only",
            "planned": "not_implemented", "blocked": "not_implemented",
        }[state]
        if gate["delivery"] != expected_delivery:
            errors.append(f"{ident}: status falsely claims the wrong delivery scope")
        if state in {"complete_bounded", "in_review"}:
            if pr == 0 or ci == 0 or not gate["ci_workflow"] or not SHA.fullmatch(gate["reviewed_head"]):
                errors.append(f"{ident}: missing traceable PR head or CI run")
            if state == "complete_bounded":
                if not SHA.fullmatch(gate["merge_commit"]):
                    errors.append(f"{ident}: a completed milestone must carry a verified merge commit")
                if not safe_path(gate["evidence_path"]):
                    errors.append(f"{ident}: completed milestone requires local evidence")
                for key in ("source_path", "evidence_path"):
                    if safe_path(gate[key]) and not (root / gate[key]).is_file():
                        errors.append(f"{ident}: recorded committed {key} not found")
            else:
                if gate["merge_commit"] != "":
                    errors.append(f"{ident}: draft PR must not assert a merged revision")
                if not safe_path(gate["evidence_path"]):
                    errors.append(f"{ident}: draft PR must identify its branch evidence")
        else:
            if pr or ci or gate["merge_commit"] or gate["reviewed_head"] or gate["evidence_path"] or gate["ci_workflow"]:
                errors.append(f"{ident}: a planned or blocked milestone has no accepted execution evidence")
            if safe_path(gate["source_path"]) and not (root / gate["source_path"]).is_file():
                errors.append(f"{ident}: planned/blocked source reference missing")
        row = next((line for line in roadmap.splitlines()
                    if line.startswith(f"| {ident} |")), None)
        if row is None or STATE_LABEL[state] not in row:
            errors.append(f"{ident}: published summary is missing or has an inconsistent status")
        if pr and f"https://github.com/{OWNER}/pull/{pr}" not in roadmap:
            errors.append(f"{ident}: recorded PR must appear in the human-readable ledger")
        if ci and f"https://github.com/{OWNER}/actions/runs/{ci}" not in roadmap:
            errors.append(f"{ident}: CI run must appear in the human-readable ledger")
    if set(by_id) != EXPECTED_IDS:
        errors.append("Gate registry must contain all thirteen scoped G/R/D milestones")
    for ident, gate in by_id.items():
        dependencies = gate.get("depends_on", [])
        if isinstance(dependencies, list):
            for dep in dependencies:
                if dep not in by_id:
                    errors.append(f"{ident}: unknown prerequisite gate")
    # Detect indirect cycles as well as direct loops, using explicit visit states.
    seen = set()
    visiting = set()

    def visit(gate_id):
        if gate_id in visiting:
            errors.append(f"{gate_id}: cyclic milestone dependencies")
            return
        if gate_id in seen:
            return
        visiting.add(gate_id)
        item = by_id.get(gate_id, {})
        for prerequisite in item.get("depends_on", []):
            if prerequisite in by_id and prerequisite not in visiting:
                visit(prerequisite)
            elif prerequisite in visiting:
                errors.append(f"{gate_id}: cyclic milestone dependencies")
        visiting.remove(gate_id)
        seen.add(gate_id)

    for gate_id in by_id:
        visit(gate_id)
    # A privacy/risk gate cannot be promoted by simply changing the label.
    if by_id.get("D1", {}).get("status") != "blocked":
        errors.append("D1 remains blocked until separate scientific/privacy-admission review changes the validator")
    if "All learner-mastery states remain unassessed" not in roadmap:
        errors.append("Human ledger must explicitly separate learner mastery from CI")
    if "not enforced on `main` yet" not in roadmap:
        errors.append("Human ledger must disclose unpublished privacy controls")
    return errors


def main():
    problems = inspect(read_snapshot(), ROADMAP.read_text(encoding="utf-8"))
    if problems:
        for message in problems:
            print("FAILED milestone evidence: " + message, file=sys.stderr)
        raise SystemExit(1)
    print("PASS: 13 roadmap gates; 7 bounded completions, 3 drafts, 2 planned, 1 blocked; source and CI provenance structurally consistent")
    print("NOTE: offline check only; verify current GitHub CI/PR state and independent permissions before changing gate labels")


if __name__ == "__main__":
    main()
