#!/usr/bin/env python3
"""One-time cleanup of already squash-merged, snapshot-identical branch refs.

Never remerges code or rewrites history. Before ANY deletion: verify every
original PR head, merged commit, tree snapshot, retained PR ref, reviewed SHA,
current default-tree link scan and all non-target refs. Then delete each
original branch by an exact Git SHA lease. Keep a durable partial receipt.

Not a privacy/clinical/scientific acceptance check or sensitive-data purge.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.request import Request, urlopen

REPO = "pskeffington/pauls_notes"
ACTOR = "pskeffington"
# PR number, old branch, original head SHA, immutable squash merge commit SHA.
# No D0 #7, G4 #19, G4 freeze #18, or legacy work branches.
RETIRED_PR_HEADS = (
    (6, "feat/rust-native-frozen-deployment", "75409525de2119618b4dfecea7a9aa3e56af947c", "214ee72743601da0f4b4da0add61cbaf04080e1d"),
    (9, "docs/readme-reader-paths-20261016", "bccb0049968a0b3cf4c533bff08433efa6b2be60", "c7e9efb5ce8c73151f8df5ab5e9a93568666f951"),
    (10, "docs/rust-coding-evidence-20261017", "e0eaa27d8489e5a12e3d1cf5c9bc6b3b3a262632", "86e6d919f7a5c9f2b0b2b8382e1926ab5c0dcb7e"),
    (11, "docs/rust-book-aligned-engineering-handbook-20261017", "bfabde1fe22ac3e58aaf07fcf8a6a2c8e12acc1e", "e68ab849c6bf3ba7182acbdfebabcef88b196c66"),
    (12, "feat/rust-from-foundations-to-research-engineering", "8bdd548f4588eda076acee41e22994b5fc6ae99a", "f02fe1e020e0f44c118b3c554724fe5101e643b9"),
    (13, "docs/roadmap-gate-evidence-20261017", "eed8adc41b922042e51e1d75d7350d5e70ab5923", "f98c19ecc520f1648072df2e79cbbaba55b529c1"),
    (14, "docs/roadmap-r3-native-parity-accepted", "7daf0dae9a725a341c3c49f4d1440a0ace84b17f", "cd8a07a56e87f2df69d5da2670816afce04c4879"),
    (15, "docs/oncology-wide-research-scope-20261017", "71808c9d789851257aa3cb66670c5f01f5d03f2a", "949a2f16b7d35fb97540c95dd6e91dd7c71a4f2c"),
    (16, "feat/standalone-synthetic-oncology-ml", "232a2f5ab01dd070034786b18ffc803f8e52f160", "714dbfa8d4d166b3df56451289411457afb92051"),
    (17, "docs/accept-r4-synthetic-oncology-ml-20261017", "41d6bae728847de3703b941f8d13bc86027bc429", "5d09f4de8b17d1a951de966d9ebd914f4af56563"),
    (20, "docs/git-from-zero-to-push-20261017", "be2e65e4eda4fd2b0e49e18e15d8af8f55972ed1", "c40d8f3f1472d2f0266069aa5e0030930faf93dc"),
    (21, "chore/repository-hygiene-20261017", "73b37f3c940d0cc3eff248e02e55d20003fb6c71", "dd479979730ab34bc9f1acc87919657a369882cd"),
    (23, "chore/legacy-branch-ci-hygiene-20261017", "6fe59f94d787cda3b0225dfcc1cc4211a8205068", "dc44be0af1d911b112321cf6858096f26d4d77de"),
    (24, "chore/branch-retention-audit-20261017", "6ff7bd0b15ae499258011ebcc1040ab17741b5aa", "588265a934361e4c9f11c2fb1b51bdf4b9e904e2"),
    (25, "fix/branch-retention-head-parity-20261017", "be94ac2185b1be142f92ae39e42bcfbe4c685f4a", "e74257220f180d80b2b2df474c2e370320b7b9f0"),
    (26, "fix/branch-retention-ancestry-gate-20261017", "8cddcda46def110938ebeb60970a7f78cca7eb12", "95b58d309f69fb0553d65933f552593c69246057"),
    (27, "chore/guarded-branch-retirement-20261017", "2d9ca4f5068583ba954c800f9e71a21188f17591", "a1163fadac391b87b44a54fe6e7592c3a1d55ab4"),
    (28, "chore/consolidate-merged-branches-20261017", "6e8ceb189144e493a4dc5210da21ad6e25df2f8d", "14eacfdf1f797b6ae61ea201f33e20422b543a9d"),
)
HOLD = frozenset((
    "main",
    "feat/config-driven-ml-research-toolkit",
    "feat/g4-survival-execution-20261017",
    "docs/g4-frozen-synthetic-survival-protocol-20261017",
    "work/biomedical-learning",
    "work/learning-check-coverage",
))
SHA = re.compile(r"^[0-9a-f]{40}$")


def run_git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout.strip()


def remote_refs(pattern):
    """Read remote refs; malformed input must not become deletion eligibility."""
    output = run_git("ls-remote", "origin", pattern)
    result = {}
    for line in output.splitlines():
        parts = line.split()
        if len(parts) != 2 or SHA.fullmatch(parts[0]) is None:
            raise ValueError("Malformed remote ref listing")
        sha, name = parts
        if name in result:
            raise ValueError("Duplicate remote ref: " + name)
        result[name] = sha
    return result


def github_pull(pr, token):
    url = f"https://api.github.com/repos/{REPO}/pulls/{pr}"
    req = Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + token,
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "pauls-notes-squash-history-retirement",
    })
    with urlopen(req, timeout=20) as response:
        return json.load(response)


def checked_context(env):
    expected = {
        "GITHUB_REPOSITORY": REPO,
        "GITHUB_ACTOR": ACTOR,
        "GITHUB_EVENT_NAME": "push",
        "GITHUB_REF": "refs/heads/main",
    }
    for key, want in expected.items():
        if env.get(key) != want:
            raise ValueError("Workflow must be an owner-originated main push: " + key)
    if not env.get("GITHUB_TOKEN") or SHA.fullmatch(env.get("GITHUB_SHA", "")) is None:
        raise ValueError("Missing authenticated token or current main SHA")
    if run_git("rev-parse", "HEAD") != env["GITHUB_SHA"]:
        raise ValueError("Local checkout differs from workflow main SHA")


def validate_audit(audit, now=None):
    current = now or datetime.now(timezone.utc)
    if audit.get("repository") != REPO or audit.get("default_branch") != "main":
        raise ValueError("Audit repository mismatch")
    if audit.get("scanned_default_tree") is not True or audit.get("skipped_text_files") != 0:
        raise ValueError("Incomplete tracked-source scan")
    stamp = datetime.fromisoformat(audit["observed_utc"].replace("Z", "+00:00"))
    if stamp.tzinfo is None or not 0 <= (current - stamp).total_seconds() <= 600:
        raise ValueError("Audit timestamp stale or timezone invalid")
    if audit.get("checkout_sha") != run_git("rev-parse", "HEAD"):
        raise ValueError("Audit was not run on exact checked-out main")
    rows = audit.get("branches")
    if not isinstance(rows, list) or len({z.get("branch") for z in rows}) != len(rows):
        raise ValueError("Duplicate or missing branch inventory")
    index = {r["branch"]: r for r in rows}
    if index.get("main", {}).get("head_sha") != audit["checkout_sha"]:
        raise ValueError("Audit default main identity mismatch")
    if any(branch not in index for branch in HOLD):
        raise ValueError("Required held research branch missing")
    if len(RETIRED_PR_HEADS) != 18:
        raise ValueError("Unexpected retirement allowlist size")
    for pr, branch, head, merge in RETIRED_PR_HEADS:
        if branch in HOLD or not SHA.fullmatch(head) or not SHA.fullmatch(merge):
            raise ValueError("Invalid or dangerous retirement allowlist")
        row = index.get(branch)
        if row is None:
            raise ValueError("Target absent from live audit: " + branch)
        if (row.get("head_sha") != head or row.get("pull_requests") != [pr]
                or row.get("merged_prs") != [pr]
                or row.get("merged_commit_shas") != [merge]
                or row.get("matches_sole_merged_pr_head") is not True
                or row.get("branch_qualified_links_in_default_tree") != 0
                or row.get("branch_qualified_links_in_pr_bodies") != 0
                or row.get("history_relative_to_default") not in ("diverged", "contained")
                or row.get("decision") not in ("diverged_history_hold", "merged_manual_review")):
            raise ValueError("Target branch failed review controls: " + branch)
    return index


def verify_snapshot_parity(pull, pr, branch, head, merge):
    """Prove original PR tip and squash commit have the SAME ENTIRE Git tree."""
    if (pull.get("number") != pr or not pull.get("merged_at")
            or pull.get("state") != "closed"
            or pull.get("merge_commit_sha") != merge
            or (pull.get("head") or {}).get("sha") != head
            or (pull.get("head") or {}).get("ref") != branch
            or ((pull.get("head") or {}).get("repo") or {}).get("full_name") != REPO):
        raise ValueError("Merged PR identity mismatch: #" + str(pr))
    original_tree = run_git("rev-parse", head + "^{tree}")
    squash_tree = run_git("rev-parse", merge + "^{tree}")
    if original_tree != squash_tree or SHA.fullmatch(original_tree) is None:
        raise ValueError("Git tree mismatch between original PR and merge: #" + str(pr))
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", merge, "HEAD"],
        capture_output=True,
    ).returncode != 0:
        raise ValueError("Merged snapshot commit not reachable from main: #" + str(pr))
    return original_tree


def validate_all(audit, heads, pull_refs, pulls):
    """Check all 18 and the full retained inventory BEFORE any remote mutation."""
    index = validate_audit(audit)
    target_names = {branch for _, branch, _, _ in RETIRED_PR_HEADS}
    if len(target_names) != 18 or len({pr for pr, *_ in RETIRED_PR_HEADS}) != 18:
        raise ValueError("Duplicate fixed retirement target")
    if set(index) != {ref.removeprefix("refs/heads/") for ref in heads}:
        raise ValueError("Remote branch set changed since audit")
    if any(heads.get("refs/heads/" + name) != index[name]["head_sha"] for name in index):
        raise ValueError("Remote branch moved since audit")
    if not HOLD.isdisjoint(target_names):
        raise ValueError("Retirement list overlaps protected branches")
    tree_proof = []
    for pr, branch, sha, merge in RETIRED_PR_HEADS:
        if heads.get("refs/heads/" + branch) != sha:
            raise ValueError("Reviewed remote branch SHA has changed: " + branch)
        if pull_refs.get(f"refs/pull/{pr}/head") != sha:
            raise ValueError("Original PR head ref unavailable or moved: #" + str(pr))
        tree = verify_snapshot_parity(pulls[pr], pr, branch, sha, merge)
        tree_proof.append({
            "pr": pr, "branch": branch, "head_sha": sha,
            "merge_commit_sha": merge, "identical_tree_sha": tree,
            "pr_ref": f"refs/pull/{pr}/head",
        })
    return tree_proof


def save(path, document):
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def execute(audit_file, receipt_file, env, live=False):
    receipt = {
        "result": "STARTED_NO_BRANCHES_DELETED",
        "repo": REPO,
        "utc": datetime.now(timezone.utc).isoformat(),
        "removed": [],
        "retained": sorted(HOLD),
    }
    save(receipt_file, receipt)
    try:
        if not live:
            raise ValueError("Explicit --execute is required")
        checked_context(env)
        audit = json.loads(audit_file.read_text(encoding="utf-8"))
        if audit.get("checkout_sha") != env["GITHUB_SHA"]:
            raise ValueError("Audit/workflow head SHA mismatch")
        heads = remote_refs("refs/heads/*")
        pull_refs = remote_refs("refs/pull/*/head")
        pulls = {pr: github_pull(pr, env["GITHUB_TOKEN"]) for pr, *_ in RETIRED_PR_HEADS}
        proof = validate_all(audit, heads, pull_refs, pulls)
        receipt.update({
            "result": "ALL_PREFLIGHTS_PASSED_NONE_DELETED",
            "main_sha": env["GITHUB_SHA"],
            "verified": proof,
            "retained_branch_shas": {
                name: heads["refs/heads/" + name] for name in HOLD
            },
        })
        save(receipt_file, receipt)

        for row in proof:
            branch = row["branch"]
            expected = row["head_sha"]
            ref = "refs/heads/" + branch
            # Git's exact expected-value lease rejects an updated remote ref.
            command = [
                "git", "push", "--porcelain",
                "--force-with-lease=" + ref + ":" + expected,
                "origin", ":" + ref,
            ]
            completed = subprocess.run(command, text=True, capture_output=True)
            if completed.returncode != 0:
                raise RuntimeError("SHA-leased deletion failed: " + branch
                                   + " " + completed.stderr[-300:])

            after = remote_refs("refs/heads/*")
            desired = {
                key: value for key, value in heads.items()
                if key not in {"refs/heads/" + d["branch"] for d in receipt["removed"]}
                and key != ref
            }
            if after != desired:
                raise RuntimeError("Unexpected remote ref change after " + branch)
            if remote_refs("refs/pull/" + str(row["pr"]) + "/head").get(row["pr_ref"]) != expected:
                raise RuntimeError("Original PR commit ref not preserved for #" + str(row["pr"]))

            receipt["removed"].append(row)
            receipt["result"] = "PARTIAL_DELETIONS_VERIFIED"
            save(receipt_file, receipt)

        receipt["result"] = "ALL_18_REFS_DELETED_PR_HISTORY_RETAINED"
        save(receipt_file, receipt)
    except Exception as exc:
        receipt["result"] = "FAILED_OR_PARTIAL_REVIEW_REQUIRED"
        receipt["failure"] = str(exc)
        save(receipt_file, receipt)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    if args.receipt.exists():
        parser.error("Refusing to overwrite an existing evidence receipt")
    execute(args.audit, args.receipt, os.environ, live=args.execute)
    print("PASS: 18 redundant source refs removed, all PR commit refs preserved")


if __name__ == "__main__":
    main()
