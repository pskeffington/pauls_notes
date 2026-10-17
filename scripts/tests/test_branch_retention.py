"""Read-only branch audit regression tests; no network, Git writes, or data."""
import sys
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit_branch_retention import (
    branch_link_counts, classify, git_branch_reachability, valid_repository, REPOSITORY_RE,
)

REPO = "pskeffington/pauls_notes"


def fixture():
    names = [
        "main", "feat/config-driven-ml-research-toolkit",
        "feat/g4-survival-execution-20261017",
        "docs/g4-frozen-synthetic-survival-protocol-20261017",
        "work/learning-check-coverage",
        "docs/merged-clean", "docs/merged-reference", "docs/unreviewed",
        "docs/closed-unmerged", "docs/protected", "docs/from-fork",
    ]
    branches = [
        {"name": n, "sha": str(i + 1).zfill(40),
         "protected": n in ("main", "docs/protected")}
        for i, n in enumerate(names)
    ]
    def pr(number, head, state, merged_at=None, body="", source=REPO):
        return {
            "number": number, "head_ref": head, "head_repository": source,
            "head_sha": next(b["sha"] for b in branches if b["name"] == head),
            "state": state, "merged_at": merged_at, "body": body,
            "merge_commit_sha": ("a" * 40) if merged_at else None,
        }
    prs = [
        pr(7, names[1], "open"),
        pr(19, names[2], "open"),
        pr(18, names[3], "closed", "2026-10-17"),
        pr(100, names[5], "closed", "2026-10-17"),
        pr(101, names[6], "closed", "2026-10-17",
           f"https://github.com/{REPO}/blob/docs/merged-reference/file.md"),
        pr(102, names[8], "closed"),
        pr(103, names[10], "open", source="someone-else/fork"),
    ]
    return {
        "repository": REPO,
        "default_branch": "main",
        "observed_utc": "2026-10-17T00:00:00+00:00",
        "branches": branches,
        "pull_requests": prs,
        "git_ancestry": {name: "contained" for name in names},
    }


class BranchRetentionAuditTests(unittest.TestCase):
    def test_statuses_never_approve_deletion(self):
        snap = fixture()
        result = classify(snap, [], snap["branches"][0]["sha"])
        found = {r["branch"]: r for r in result["branches"]}
        expected = {
            "main": "default_hold",
            "feat/config-driven-ml-research-toolkit": "active_pr_hold",
            "feat/g4-survival-execution-20261017": "active_pr_hold",
            "docs/g4-frozen-synthetic-survival-protocol-20261017":
                "frozen_protocol_hold",
            "work/learning-check-coverage": "legacy_work_hold",
            "docs/merged-clean": "merged_manual_review",
            "docs/merged-reference": "referenced_hold",
            "docs/unreviewed": "unresolved_hold",
            "docs/closed-unmerged": "unresolved_hold",
            "docs/protected": "protected_hold",
            "docs/from-fork": "unresolved_hold",
        }
        self.assertEqual({n: r["decision"] for n, r in found.items()}, expected)
        self.assertTrue(all(r["decision"] != "delete" for r in found.values()))
        self.assertNotIn("body", str(result))
        self.assertEqual(found["docs/from-fork"]["pull_requests"], [])
        self.assertEqual(found["docs/merged-reference"]
                         ["branch_qualified_links_in_pr_bodies"], 1)

    def test_local_links_hold_merged_branches(self):
        snap = fixture()
        texts = [
            f"https://github.com/{REPO}/tree/docs/merged-clean/subfolder",
            "ordinary prose containing docs/unreviewed is not a URL",
        ]
        report = classify(snap, texts, snap["branches"][0]["sha"])
        lookup = {r["branch"]: r for r in report["branches"]}
        self.assertEqual(lookup["docs/merged-clean"]["decision"], "referenced_hold")
        self.assertEqual(
            lookup["docs/merged-clean"]["branch_qualified_links_in_default_tree"], 1)
        self.assertTrue(report["scanned_default_tree"])

    def test_nested_branch_names_do_not_count_parent_twice(self):
        text = f"https://github.com/{REPO}/blob/docs/a/b/file.md"
        matches = branch_link_counts([text], REPO, {"docs/a", "docs/a/b"})
        self.assertEqual(matches["docs/a/b"], 1)
        self.assertEqual(matches["docs/a"], 0)

    def test_raw_urls_count_but_sha_links_do_not(self):
        texts = [
            f"https://raw.githubusercontent.com/{REPO}/docs/referenced/x.md",
            f"https://github.com/{REPO}/blob/" + "a" * 40 + "/x.md",
        ]
        counts = branch_link_counts(texts, REPO, {"docs/referenced"})
        self.assertEqual(counts["docs/referenced"], 1)

    def test_default_checkout_sha_must_match(self):
        with self.assertRaisesRegex(ValueError, "exact current default-branch"):
            classify(fixture(), [], "b" * 40)

    def test_duplicate_branches_fail_closed(self):
        snap = fixture()
        snap["branches"].append(dict(snap["branches"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate branch"):
            classify(snap)

    def test_source_repo_missing_does_not_create_merge_candidate(self):
        snap = fixture()
        for pr in snap["pull_requests"]:
            if pr["number"] == 100:
                pr["head_repository"] = None
        result = classify(snap)
        found = {r["branch"]: r for r in result["branches"]}
        self.assertEqual(found["docs/merged-clean"]["decision"], "unresolved_hold")

    def test_merged_branch_head_mismatch_stays_held(self):
        snap = fixture()
        snap["branches"][5]["sha"] = "b" * 40
        result = classify(snap, [], snap["branches"][0]["sha"])
        found = {r["branch"]: r for r in result["branches"]}
        row = found["docs/merged-clean"]
        self.assertEqual(row["decision"], "merged_head_mismatch_hold")
        self.assertFalse(row["matches_sole_merged_pr_head"])

    def test_missing_pr_head_sha_stays_held(self):
        snap = fixture()
        for pr in snap["pull_requests"]:
            if pr["number"] == 100:
                pr["head_sha"] = None
        result = classify(snap, [], snap["branches"][0]["sha"])
        found = {r["branch"]: r for r in result["branches"]}
        self.assertEqual(found["docs/merged-clean"]["decision"],
                         "merged_head_mismatch_hold")

    def test_no_repository_scan_is_not_a_cleanup_candidate(self):
        report = classify(fixture())
        found = {r["branch"]: r for r in report["branches"]}
        self.assertEqual(found["docs/merged-clean"]["decision"],
                         "unscanned_source_hold")
        self.assertFalse(report["scanned_default_tree"])

    def test_skipped_text_file_is_not_a_cleanup_candidate(self):
        snap = fixture()
        report = classify(snap, [], snap["branches"][0]["sha"], skipped=1)
        found = {r["branch"]: r for r in report["branches"]}
        self.assertEqual(found["docs/merged-clean"]["decision"],
                         "incomplete_text_scan_hold")
        self.assertEqual(report["skipped_text_files"], 1)

    def test_exact_head_and_complete_scan_allows_review_only(self):
        snap = fixture()
        report = classify(snap, [], snap["branches"][0]["sha"], skipped=0)
        row = next(r for r in report["branches"]
                   if r["branch"] == "docs/merged-clean")
        self.assertTrue(row["matches_sole_merged_pr_head"])
        self.assertEqual(row["decision"], "merged_manual_review")
        self.assertNotIn("approved", row["decision"])

    def test_reused_branch_with_multiple_prs_is_held(self):
        snap = fixture()
        original = next(p for p in snap["pull_requests"] if p["number"] == 100)
        additional = dict(original, number=104, merged_at=None, state="closed")
        snap["pull_requests"].append(additional)
        report = classify(snap, [], snap["branches"][0]["sha"])
        row = next(r for r in report["branches"]
                   if r["branch"] == "docs/merged-clean")
        self.assertEqual(row["decision"], "unresolved_hold")

    def test_squash_merged_diverged_branch_never_becomes_candidate(self):
        snap = fixture()
        snap["git_ancestry"]["docs/merged-clean"] = "diverged"
        result = classify(snap, [], snap["branches"][0]["sha"])
        row = next(r for r in result["branches"]
                   if r["branch"] == "docs/merged-clean")
        self.assertTrue(row["matches_sole_merged_pr_head"])
        self.assertEqual(row["history_relative_to_default"], "diverged")
        self.assertEqual(row["decision"], "diverged_history_hold")

    def test_unverified_ancestry_always_held(self):
        for setting in ("unverified", None):
            snap = fixture()
            if setting is None:
                del snap["git_ancestry"]["docs/merged-clean"]
            else:
                snap["git_ancestry"]["docs/merged-clean"] = setting
            result = classify(snap, [], snap["branches"][0]["sha"])
            row = next(r for r in result["branches"]
                       if r["branch"] == "docs/merged-clean")
            self.assertEqual(row["decision"], "history_unverified_hold")

    def test_git_reachability_discriminates_ancestor_and_diverged(self):
        snap = fixture()
        mainsha = snap["branches"][0]["sha"]
        ancestorsha = snap["branches"][5]["sha"]
        missing = snap["branches"][7]["sha"]

        def fake_git(cmd, **kwargs):
            if "rev-parse" in cmd:
                return subprocess.CompletedProcess(cmd, 0, stdout=mainsha)
            if "cat-file" in cmd:
                sha = cmd[-1].split("^", 1)[0]
                return subprocess.CompletedProcess(cmd, 1 if sha == missing else 0)
            if "merge-base" in cmd:
                sha = cmd[-2]
                return subprocess.CompletedProcess(
                    cmd, 0 if sha == ancestorsha else 1
                )
            raise AssertionError("Unknown command in fake Git")

        with patch("audit_branch_retention.subprocess.run", side_effect=fake_git):
            result = git_branch_reachability(Path("."), snap)
        self.assertEqual(result["main"], "contained")
        self.assertEqual(result["docs/merged-clean"], "contained")
        self.assertEqual(result["docs/merged-reference"], "diverged")
        self.assertEqual(result["docs/unreviewed"], "unverified")

    def test_history_refuses_stale_default_checkout(self):
        snap = fixture()
        def fake_git(cmd, **kwargs):
            return subprocess.CompletedProcess(cmd, 0, stdout="f"*40)
        with patch("audit_branch_retention.subprocess.run", side_effect=fake_git):
            with self.assertRaisesRegex(ValueError, "exact current default-branch"):
                git_branch_reachability(Path("."), snap)

    def test_repository_slug_validation(self):
        self.assertIsNotNone(REPOSITORY_RE.fullmatch(REPO))
        self.assertTrue(valid_repository(REPO))
        for bad in ("https://api.github.com/evil", "../../private",
                    "owner/one/two", "owner name/repo",
                    "../private", "owner/..", "./repo"):
            with self.subTest(bad=bad):
                self.assertFalse(valid_repository(bad))


if __name__ == "__main__":
    unittest.main()
