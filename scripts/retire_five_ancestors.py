#!/usr/bin/env python3
"""One-time, fail-closed retirement of five fully merged ancestor branches.

Never merges code or alters history. Strictly verifies current main, the
latest read-only report, exact owner approvals, remote SHAs and protected
research heads. Deletion requires --execute and the GitHub Actions context.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys

from confirm_branch_retirement import (
    ALLOWLIST, OWNER, REPOSITORY, issue_approvals, validate,
)

HOLD_BRANCHES = (
    "main",
    "feat/config-driven-ml-research-toolkit",
    "feat/g4-survival-execution-20261017",
    "docs/g4-frozen-synthetic-survival-protocol-20261017",
    "work/biomedical-learning",
    "work/learning-check-coverage",
)


def assert_context(environ):
    if (
        environ.get("GITHUB_REPOSITORY") != REPOSITORY
        or environ.get("GITHUB_ACTOR") != OWNER
        or environ.get("GITHUB_REF") != "refs/heads/main"
        or environ.get("GITHUB_EVENT_NAME") != "push"
    ):
        raise ValueError("No retirement outside owner-authored main push")
    if not environ.get("GITHUB_TOKEN"):
        raise ValueError("GITHUB_TOKEN required")
    if not environ.get("GITHUB_SHA"):
        raise ValueError("Current integration commit identity missing")


def run_git(*argv):
    return subprocess.run(["git", *argv], check=True,
                          capture_output=True, text=True).stdout


def parse_remote_heads(data):
    found = {}
    for line in data.splitlines():
        words = line.split()
        if len(words) != 2 or not words[1].startswith("refs/heads/"):
            raise ValueError("Malformed git ls-remote branch output")
        sha, ref = words
        name = ref[len("refs/heads/"):]
        if name in found or len(sha) != 40:
            raise ValueError("Duplicate branch or unexpected SHA")
        found[name] = sha
    return found


def check_remote_heads(remote):
    """Check *every* target before issuing the first deletion."""
    if len(ALLOWLIST) != 5:
        raise ValueError("Retirement allowlist size changed")
    for name, row in ALLOWLIST.items():
        if remote.get(name) != row["head"]:
            raise ValueError("Remote SHA missing or changed for " + name)
    for name in HOLD_BRANCHES:
        if not remote.get(name):
            raise ValueError("Required retained branch missing: " + name)
    return sorted(ALLOWLIST)


def deletion_command(name):
    """Construct one reference-only, exact-SHA leased delete command."""
    if name not in ALLOWLIST:
        raise ValueError("Unreviewed branch")
    return [
        "git", "push", "--porcelain",
        "--force-with-lease=refs/heads/" + name + ":" + ALLOWLIST[name]["head"],
        "origin", ":refs/heads/" + name,
    ]


def save(path, report):
    path.write_text(json.dumps(report, sort_keys=True, indent=2) + "\n",
                    encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--audit", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--execute", action="store_true",
                   help="Allow SHA-leased remote deletes (Actions context only)")
    args = p.parse_args()
    if args.output.exists():
        p.error("Refusing to overwrite existing receipt")
    receipt = {
        "result": "STARTED_NO_REFS_DELETED",
        "repository": REPOSITORY,
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "branches": [],
        "retained": list(HOLD_BRANCHES),
    }
    save(args.output, receipt)
    try:
        if not args.execute:
            raise ValueError("Explicit --execute flag required")
        assert_context(os.environ)
        audit = json.loads(args.audit.read_text(encoding="utf-8"))
        if audit.get("checkout_sha") != os.environ["GITHUB_SHA"]:
            raise ValueError("Audit/main head SHA is not the current GitHub action head")

        # Validate all five before first remote mutation.
        comments = issue_approvals(os.environ["GITHUB_TOKEN"])
        checked = {
            name: validate(
                audit, name, row["head"], "DELETE " + name,
                "true", OWNER, REPOSITORY, comments,
            )
            for name, row in ALLOWLIST.items()
        }
        before = parse_remote_heads(run_git("ls-remote", "--heads", "origin"))
        names = check_remote_heads(before)
        receipt["result"] = "PREFLIGHT_VALIDATED_NO_REFS_DELETED"
        receipt["audit_sha"] = audit["checkout_sha"]
        receipt["approved"] = checked
        save(args.output, receipt)

        for name in names:
            cmd = deletion_command(name)
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError("Git SHA-lease rejected retirement of " + name
                                   + ": " + result.stderr[-600:])
            remote = parse_remote_heads(run_git("ls-remote", "--heads", "origin"))
            if name in remote:
                raise RuntimeError("Deletion not reflected in remote for " + name)
            for keep in HOLD_BRANCHES:
                if remote.get(keep) != before.get(keep):
                    raise RuntimeError("Protected branch was changed: " + keep)
            receipt["branches"].append({
                "branch": name, "former_head_sha": ALLOWLIST[name]["head"],
                "merge_commit": ALLOWLIST[name]["merge"],
                "result": "DELETED_AND_ABSENCE_VERIFIED",
            })
            save(args.output, receipt)

        receipt["result"] = "FIVE_DELETIONS_VERIFIED"
        save(args.output, receipt)
        print("PASS: 5 original ancestor branches deleted, retained heads unchanged")
    except Exception as exc:
        receipt["result"] = "FAILED_OR_PARTIAL_REVIEW_RECORDED"
        receipt["failure"] = str(exc)
        save(args.output, receipt)
        raise


if __name__ == "__main__":
    main()
