#!/usr/bin/env python3
"""Read-only GitHub branch-retention audit; never deletes or moves refs.

Requires GitHub read permissions for --repository. A checked-out default
branch is optional; without it, repository-file link coverage is incomplete.
This is Git metadata hygiene, NOT a secret scan or D0 data-admission check.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
from urllib.request import Request, urlopen

FREEZE_HOLDS = frozenset({
    "docs/g4-frozen-synthetic-survival-protocol-20261017",
})
TEXT_SUFFIXES = frozenset({
    ".md", ".rst", ".txt", ".json", ".toml", ".yml", ".yaml",
    ".py", ".rs", ".r", ".sh",
})
REPOSITORY_RE = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")


def valid_repository(repository):
    return (isinstance(repository, str)
            and REPOSITORY_RE.fullmatch(repository) is not None
            and all(part not in (".", "..") for part in repository.split("/")))


def github_get(path, token):
    request = Request(
        "https://api.github.com" + path,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + token,
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "pauls-notes-branch-audit",
        },
    )
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def github_pages(path, token):
    found = []
    for page in range(1, 51):
        separator = "&" if "?" in path else "?"
        batch = github_get(f"{path}{separator}per_page=100&page={page}", token)
        if not isinstance(batch, list):
            raise ValueError("Unexpected paginated GitHub response")
        found.extend(batch)
        if len(batch) < 100:
            return found
    raise ValueError("GitHub pagination exceeded audit limit; fail closed")


def live_snapshot(repository, token):
    if not valid_repository(repository):
        raise ValueError("Expected repository OWNER/NAME")
    prefix = "/repos/" + repository
    info = github_get(prefix, token)
    branches = github_pages(prefix + "/branches", token)
    prs = github_pages(prefix + "/pulls?state=all", token)
    return {
        "repository": info["full_name"],
        "default_branch": info["default_branch"],
        "observed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "branches": [
            {
                "name": b["name"],
                "sha": b["commit"]["sha"],
                "protected": bool(b.get("protected", False)),
            }
            for b in branches
        ],
        "pull_requests": [
            {
                "number": p["number"],
                "head_ref": p["head"]["ref"],
                "head_sha": p["head"].get("sha"),
                "head_repository": (p["head"].get("repo") or {}).get("full_name"),
                "state": p["state"],
                "merged_at": p.get("merged_at"),
                "merge_commit_sha": p.get("merge_commit_sha"),
                "body": p.get("body") or "",
            }
            for p in prs
        ],
    }


def scan_tracked_text(root):
    """Return tracked text, checkout SHA, and count of skipped large/symlink files."""
    root = root.resolve(strict=True)
    sha = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=True, capture_output=True, text=True,
    ).stdout.strip()
    names = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=True, capture_output=True,
    ).stdout.split(b"\0")
    texts = []
    skipped = 0
    for raw in names:
        if not raw:
            continue
        name = raw.decode("utf-8", errors="surrogateescape")
        path = root / name
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 2_000_000:
            skipped += 1
            continue
        texts.append(path.read_text(encoding="utf-8", errors="replace"))
    return texts, sha, skipped



def git_branch_reachability(root, snapshot):
    """Check branch ancestry against exact default HEAD using local Git objects.

    This is distinct from a PR merged flag: squash-merged branches often
    contain commits not reachable from the integration branch. Missing Git
    objects, invalid SHAs, or unexpected Git errors fail closed.
    """
    root = root.resolve(strict=True)
    default = snapshot["default_branch"]
    branches = {b["name"]: b for b in snapshot["branches"]}
    default_sha = branches[default]["sha"]
    checkout = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    if checkout != default_sha:
        raise ValueError("Repository scan must use exact current default-branch HEAD")
    results = {}
    for branch in snapshot["branches"]:
        name, sha = branch["name"], branch["sha"]
        if name == default:
            results[name] = "contained"
            continue
        if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40,64}", sha):
            results[name] = "unverified"
            continue
        exists = subprocess.run(
            ["git", "-C", str(root), "cat-file", "-e", sha + "^{commit}"],
            capture_output=True,
        )
        if exists.returncode:
            results[name] = "unverified"
            continue
        check = subprocess.run(
            ["git", "-C", str(root), "merge-base", "--is-ancestor",
             sha, default_sha],
            capture_output=True,
        )
        if check.returncode == 0:
            results[name] = "contained"
        elif check.returncode == 1:
            results[name] = "diverged"
        else:
            results[name] = "unverified"
    return results


def branch_link_counts(texts, repository, names):
    """Count branch-qualified blob/tree/raw URLs, never bare branch-name mentions."""
    repo = re.escape(repository)
    patterns = (
        re.compile(r"https://github\.com/" + repo +
                   r"/(?:blob|tree|raw)/([^\s<>)\]]+)", re.I),
        re.compile(r"https://raw\.githubusercontent\.com/" + repo +
                   r"/([^\s<>)\]]+)", re.I),
    )
    longest_first = sorted(names, key=len, reverse=True)
    counts = Counter()
    for text in texts:
        for pattern in patterns:
            for match in pattern.finditer(text):
                tail = match.group(1).split("#", 1)[0].split("?", 1)[0]
                for branch in longest_first:
                    if tail.startswith(branch + "/"):
                        counts[branch] += 1
                        break
    return counts


def classify(snapshot, source_texts=(), checkout_sha=None, skipped=0):
    repository = snapshot["repository"]
    default = snapshot["default_branch"]
    if not valid_repository(repository):
        raise ValueError("Invalid repository in inventory")
    branches = snapshot["branches"]
    if len({b["name"] for b in branches}) != len(branches):
        raise ValueError("Duplicate branch names")
    by_name = {b["name"]: b for b in branches}
    if default not in by_name:
        raise ValueError("Default branch absent from inventory")
    if checkout_sha is not None and checkout_sha != by_name[default]["sha"]:
        raise ValueError("Repository scan must use exact current default-branch HEAD")

    names = set(by_name)
    source_links = branch_link_counts(source_texts, repository, names)
    prs = snapshot["pull_requests"]
    pr_links = branch_link_counts((p.get("body") or "" for p in prs), repository, names)
    records = []
    for b in sorted(branches, key=lambda z: z["name"]):
        name = b["name"]
        associated = [
            p for p in prs
            if p.get("head_ref") == name
            and (p.get("head_repository") or "").lower() == repository.lower()
        ]
        open_prs = [p for p in associated if p.get("state") == "open"]
        merged_prs = [p for p in associated if p.get("merged_at")]
        # A branch name may be reused or advanced after its former PR merged.
        # Never treat a PR's historical branch name as proof of head identity.
        exact_merged_head = (
            len(associated) == 1 and len(merged_prs) == 1
            and re.fullmatch(r"[0-9a-f]{40,64}",
                             merged_prs[0].get("head_sha") or "") is not None
            and merged_prs[0]["head_sha"] == b["sha"]
        )
        link_count = source_links[name] + pr_links[name]
        history = snapshot.get("git_ancestry", {}).get(name, "unverified")

        if name == default:
            decision = "default_hold"
        elif b.get("protected"):
            decision = "protected_hold"
        elif open_prs:
            decision = "active_pr_hold"
        elif name in FREEZE_HOLDS:
            decision = "frozen_protocol_hold"
        elif name.startswith("work/"):
            decision = "legacy_work_hold"
        elif link_count:
            decision = "referenced_hold"
        elif len(associated) == 1 and len(merged_prs) == 1:
            if not exact_merged_head:
                decision = "merged_head_mismatch_hold"
            elif checkout_sha is None:
                decision = "unscanned_source_hold"
            elif skipped:
                decision = "incomplete_text_scan_hold"
            elif history == "contained":
                decision = "merged_manual_review"
            elif history == "diverged":
                decision = "diverged_history_hold"
            else:
                decision = "history_unverified_hold"
        else:
            decision = "unresolved_hold"

        records.append({
            "branch": name,
            "head_sha": b["sha"],
            "decision": decision,
            "pull_requests": sorted(p["number"] for p in associated),
            "merged_prs": sorted(p["number"] for p in merged_prs),
            "matches_sole_merged_pr_head": exact_merged_head,
            "history_relative_to_default": history,
            "merged_commit_shas": sorted(p["merge_commit_sha"] for p in merged_prs
                                        if p.get("merge_commit_sha")),
            "branch_qualified_links_in_default_tree": source_links[name],
            "branch_qualified_links_in_pr_bodies": pr_links[name],
        })

    decisions = Counter(record["decision"] for record in records)
    return {
        "repository": repository,
        "default_branch": default,
        "observed_utc": snapshot.get("observed_utc", "fixture"),
        "checkout_sha": checkout_sha,
        "scanned_default_tree": checkout_sha is not None,
        "skipped_text_files": skipped,
        "disposition": "READ ONLY — NO BRANCH DELETION OR APPROVAL IMPLIED",
        "summary": dict(sorted(decisions.items())),
        "branches": records,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    choice = parser.add_mutually_exclusive_group(required=True)
    choice.add_argument("--repository", help="OWNER/NAME; read-only GitHub API")
    choice.add_argument("--snapshot", type=Path, help="Offline JSON inventory")
    parser.add_argument("--scan-root", type=Path,
                        help="Local checkout at exact default branch HEAD")
    parser.add_argument("--output", type=Path, help="Optional report JSON path")
    args = parser.parse_args()
    if args.snapshot:
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
    else:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if not token:
            parser.error("Set GITHUB_TOKEN or GH_TOKEN for read-only API access")
        snapshot = live_snapshot(args.repository, token)
    texts, sha, skipped = ([], None, 0)
    if args.scan_root:
        texts, sha, skipped = scan_tracked_text(args.scan_root)
        snapshot["git_ancestry"] = git_branch_reachability(args.scan_root, snapshot)
    report = classify(snapshot, texts, sha, skipped)
    rendered = json.dumps(report, sort_keys=True, indent=2) + "\n"
    if args.output:
        if args.output.exists():
            parser.error("Refusing to overwrite an existing audit report")
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
