#!/usr/bin/env python3
"""Validate one explicitly requested historical branch retirement.

This module NEVER deletes branches. A separate manual GitHub Actions job may
execute a single Git push with an exact-SHA force-with-lease after validation.
Not a privacy scan, evidence purge, or authorization to edit research gates.
"""
import argparse
import os
from urllib.request import Request, urlopen
from datetime import datetime, timezone
import json
from pathlib import Path
import re

REPOSITORY = "pskeffington/pauls_notes"
OWNER = "pskeffington"
DEFAULT_BRANCH = "main"
# Frozen list of reviewed, ancestor-of-main, nonprotected PR heads.
# A change to this allowlist requires its own code-reviewed PR.
ALLOWLIST = {
    "feat/phase4-assay-robustness-gates": {
        "pr": 1,
        "head": "51a10cb49a3f85bb79230a791028d0fc046d1273",
        "merge": "06cdc2c9de2e42de4852ce07dd8d4d52ae26216c",
    },
    "docs/roadmap-gates-and-replication-contract": {
        "pr": 2,
        "head": "51da68aec9738179102c615bd117e6471e4eaf71",
        "merge": "1bdfcf1cd105ce6daf17d749430dbd289c3081de",
    },
    "feat/phase4b-repeated-cohort-replication": {
        "pr": 3,
        "head": "cc5a208147fd59143b44c1711f07bacbbecd4517",
        "merge": "544f6ad27d339deb1ada92d05f86999f60c38b0e",
    },
    "feat/phase4c-person-uncertainty": {
        "pr": 4,
        "head": "daa6650537d259d87e4c3b6f396b1fe08bfa173c",
        "merge": "16443089342a1a8e19bc5a2a15ed3d431c6203a4",
    },
    "feat/native-rust-training": {
        "pr": 5,
        "head": "9b468ebec1043df81d91465f0816e40c27bc48f8",
        "merge": "aaec3aaaa247760539eb2b7b74133e1a0b6c00a4",
    },
}
SHA_PATTERN = re.compile(r"^[0-9a-f]{40}$")

APPROVAL_ISSUE = 22


def approval_phrase(branch, sha):
    return "APPROVE BRANCH RETIREMENT " + branch + " " + sha


def issue_approvals(token):
    """Read only Issue #22 comments; do not publish tokens or body text."""
    found = []
    for page in range(1, 21):
        endpoint = (f"https://api.github.com/repos/{REPOSITORY}/issues/"
                    f"{APPROVAL_ISSUE}/comments?per_page=100&page={page}")
        request = Request(endpoint, headers={
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json",
            "User-Agent": "pauls-notes-branch-retirement",
            "X-GitHub-Api-Version": "2022-11-28",
        })
        with urlopen(request, timeout=20) as response:
            rows = json.load(response)
        if not isinstance(rows, list):
            raise ValueError("Issue approval response was not a list")
        found.extend(rows)
        if len(rows) < 100:
            return found
    raise ValueError("Issue approval pagination incomplete; fail closed")


def find_owner_approval(comments, branch, sha):
    phrase = approval_phrase(branch, sha)
    valid = [
        comment.get("html_url")
        for comment in comments
        if (isinstance(comment, dict)
            and (comment.get("user") or {}).get("login") == OWNER
            and (comment.get("body") or "").strip() == phrase
            and comment.get("html_url", "").startswith(
                f"https://github.com/{REPOSITORY}/issues/{APPROVAL_ISSUE}#"))
    ]
    if not valid:
        raise ValueError("No exact owner-approved branch/SHA comment in Issue #22")
    return valid[-1]



def validate(report, branch, sha, confirmation, external_refs_reviewed,
             actor, repository, issue_comments, now=None):
    """Return a non-sensitive, reviewable intent receipt; fail closed."""
    if actor != OWNER:
        raise ValueError("Only repository owner may dispatch retirement")
    if repository != REPOSITORY or report.get("repository") != REPOSITORY:
        raise ValueError("Repository mismatch")
    if report.get("default_branch") != DEFAULT_BRANCH:
        raise ValueError("Unexpected default branch")
    required = ALLOWLIST.get(branch)
    if required is None:
        raise ValueError("Branch is not in the five-entry historical allowlist")
    if not isinstance(sha, str) or not SHA_PATTERN.fullmatch(sha):
        raise ValueError("Invalid expected commit SHA")
    if sha != required["head"]:
        raise ValueError("Commit SHA differs from reviewed historical head")
    if confirmation != "DELETE " + branch:
        raise ValueError("Exact confirmation must be DELETE followed by branch")
    if external_refs_reviewed != "true":
        raise ValueError("External link/evidence review was not acknowledged")
    approval_url = find_owner_approval(issue_comments, branch, sha)

    if report.get("scanned_default_tree") is not True:
        raise ValueError("Default-branch source scan not complete")
    if report.get("skipped_text_files") != 0:
        raise ValueError("Default-branch text scan skipped files")
    main_rows = [r for r in report.get("branches", [])
                 if r.get("branch") == DEFAULT_BRANCH]
    if len(main_rows) != 1 or report.get("checkout_sha") != main_rows[0].get("head_sha"):
        raise ValueError("Report was not scanned at the default branch HEAD")

    timestamp = report.get("observed_utc")
    if not isinstance(timestamp, str):
        raise ValueError("Audit timestamp missing")
    try:
        observed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Invalid audit timestamp") from exc
    if observed.tzinfo is None:
        raise ValueError("Audit timestamp must be timezone aware")
    current = now or datetime.now(timezone.utc)
    age = (current - observed).total_seconds()
    if not 0 <= age <= 600:
        raise ValueError("Branch inventory is stale or has a future timestamp")

    rows = [r for r in report.get("branches", [])
            if r.get("branch") == branch]
    if len(rows) != 1:
        raise ValueError("Expected exactly one reviewed branch")
    record = rows[0]
    if (record.get("decision") != "merged_manual_review"
            or record.get("head_sha") != sha
            or record.get("matches_sole_merged_pr_head") is not True
            or record.get("history_relative_to_default") != "contained"
            or record.get("pull_requests") != [required["pr"]]
            or record.get("merged_prs") != [required["pr"]]
            or record.get("merged_commit_shas") != [required["merge"]]
            or record.get("branch_qualified_links_in_default_tree") != 0
            or record.get("branch_qualified_links_in_pr_bodies") != 0):
        raise ValueError("Retention review did not certify eligibility")

    return {
        "result": "PRECHECK_PASSED_NOT_DELETED",
        "repository": REPOSITORY,
        "actor": actor,
        "branch": branch,
        "expected_head_sha": sha,
        "pr": required["pr"],
        "merged_commit_sha": required["merge"],
        "scanned_default_commit": report["checkout_sha"],
        "observed_utc": timestamp,
        "acknowledged_external_links_review": True,
        "lease_required": True,
        "issue": APPROVAL_ISSUE,
        "approval_comment_url": approval_url,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--expected-sha", required=True)
    parser.add_argument("--confirmation", required=True)
    parser.add_argument("--external-refs-reviewed", required=True)
    parser.add_argument("--actor", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    a = parser.parse_args()
    report = json.loads(a.report.read_text(encoding="utf-8"))
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        parser.error("GITHUB_TOKEN with issues:read permission is required")
    comments = issue_approvals(token)
    receipt = validate(report, a.branch, a.expected_sha, a.confirmation,
                       a.external_refs_reviewed, a.actor, a.repository, comments)
    if a.receipt.exists():
        parser.error("Refusing to overwrite an existing receipt")
    a.receipt.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                         encoding="utf-8")
    print("PASS: reviewed single-branch deletion preflight; nothing deleted")


if __name__ == "__main__":
    main()
