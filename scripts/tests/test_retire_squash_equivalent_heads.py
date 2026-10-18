"""No-network, no-deletion guards for the one-time squash-equivalent cleanup."""
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from retire_squash_equivalent_heads import (
    ACTOR, HOLD, REPO, RETIRED_PR_HEADS, validate_all, validate_audit,
    verify_snapshot_parity, checked_context, execute,
)

MAIN_SHA = "f" * 40
NOW = datetime(2026, 10, 18, 1, tzinfo=timezone.utc)


def fixture():
    targets = [{
        "branch": name, "head_sha": head,
        "decision": "diverged_history_hold",
        "matches_sole_merged_pr_head": True,
        "merged_prs": [n], "pull_requests": [n],
        "merged_commit_shas": [merge],
        "history_relative_to_default": "diverged",
        "branch_qualified_links_in_default_tree": 0,
        "branch_qualified_links_in_pr_bodies": 0,
    } for n, name, head, merge in RETIRED_PR_HEADS]
    holds = [{
        "branch": name, "head_sha": MAIN_SHA if name == "main" else "a" * 40,
        "decision": "default_hold" if name == "main" else "active_pr_hold",
    } for name in sorted(HOLD)]
    return {
        "repository": REPO, "default_branch": "main",
        "observed_utc": NOW.isoformat(),
        "checkout_sha": MAIN_SHA,
        "scanned_default_tree": True, "skipped_text_files": 0,
        "branches": targets + holds,
    }


def refs_from_report(report):
    return {"refs/heads/" + r["branch"]: r["head_sha"]
            for r in report["branches"]}


def pulls_from_manifest():
    return {n: {
        "number": n,
        "merged_at": "2026-10-17T16:00:00Z",
        "state": "closed",
        "merge_commit_sha": merge,
        "head": {
            "sha": head, "ref": name,
            "repo": {"full_name": REPO},
        },
    } for n, name, head, merge in RETIRED_PR_HEADS}


class SquashEquivalentRetirementTests(unittest.TestCase):
    def test_18_unique_pinned_heads_exclude_all_live_research(self):
        self.assertEqual(len(RETIRED_PR_HEADS), 18)
        self.assertEqual(len({n for n, *_ in RETIRED_PR_HEADS}), 18)
        self.assertEqual(len({name for _, name, *_ in RETIRED_PR_HEADS}), 18)
        self.assertFalse(HOLD.intersection(
            {name for _, name, *_ in RETIRED_PR_HEADS}))
        self.assertNotIn(18, {n for n, *_ in RETIRED_PR_HEADS})
        self.assertNotIn(7, {n for n, *_ in RETIRED_PR_HEADS})
        self.assertNotIn(19, {n for n, *_ in RETIRED_PR_HEADS})

    @patch("retire_squash_equivalent_heads.run_git", return_value=MAIN_SHA)
    def test_valid_full_audit_returns_branch_index(self, _):
        result = validate_audit(fixture(), now=NOW)
        self.assertEqual(len(result), 24)
        self.assertEqual(result["main"]["head_sha"], MAIN_SHA)

    @patch("retire_squash_equivalent_heads.run_git", return_value=MAIN_SHA)
    def test_incomplete_or_stale_audit_fails_closed(self, _):
        cases = [
            ("skipped_text_files", 1),
            ("scanned_default_tree", False),
            ("checkout_sha", "0" * 40),
            ("default_branch", "develop"),
            ("repository", "other/repo"),
            ("observed_utc", (NOW - timedelta(minutes=11)).isoformat()),
        ]
        for field, value in cases:
            report = fixture()
            report[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_audit(report, now=NOW)

    @patch("retire_squash_equivalent_heads.run_git", return_value=MAIN_SHA)
    def test_missing_frozen_hold_rejected(self, _):
        report = fixture()
        report["branches"] = [
            r for r in report["branches"]
            if r["branch"] != "docs/g4-frozen-synthetic-survival-protocol-20261017"
        ]
        with self.assertRaisesRegex(ValueError, "held research"):
            validate_audit(report, now=NOW)

    @patch("retire_squash_equivalent_heads.run_git", return_value=MAIN_SHA)
    def test_linked_reused_or_unmerged_candidate_rejected(self, _):
        variants = [
            ("decision", "referenced_hold"),
            ("head_sha", "0" * 40),
            ("merged_prs", []),
            ("pull_requests", [6, 19]),
            ("matches_sole_merged_pr_head", False),
            ("history_relative_to_default", "unverified"),
            ("branch_qualified_links_in_default_tree", 1),
            ("branch_qualified_links_in_pr_bodies", 1),
        ]
        for field, value in variants:
            report = fixture()
            report["branches"][0][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_audit(report, now=NOW)

    @patch("retire_squash_equivalent_heads.run_git", return_value=MAIN_SHA)
    def test_duplicate_branch_record_rejected(self, _):
        report = fixture()
        report["branches"].append(dict(report["branches"][0]))
        with self.assertRaises(ValueError):
            validate_audit(report, now=NOW)

    @patch("retire_squash_equivalent_heads.run_git", return_value=MAIN_SHA)
    @patch("retire_squash_equivalent_heads.verify_snapshot_parity", return_value="1" * 40)
    def test_all_targets_verified_with_pr_refs_and_remote_snapshot(self, _, __):
        report = fixture()
        heads = refs_from_report(report)
        pr_refs = {
            f"refs/pull/{n}/head": sha
            for n, _, sha, _ in RETIRED_PR_HEADS
        }
        # The script has separate current-time validation; use fixture timestamp now.
        with patch("retire_squash_equivalent_heads.validate_audit",
                   return_value={r["branch"]: r for r in report["branches"]}):
            result = validate_all(report, heads, pr_refs, pulls_from_manifest())
        self.assertEqual(len(result), 18)
        self.assertEqual(result[0]["pr"], 6)
        self.assertEqual(result[-1]["pr"], 28)

    @patch("retire_squash_equivalent_heads.run_git", return_value=MAIN_SHA)
    @patch("retire_squash_equivalent_heads.verify_snapshot_parity", return_value="1" * 40)
    def test_changed_remote_or_unavailable_pr_ref_fails(self, _, __):
        report = fixture()
        heads = refs_from_report(report)
        pr_refs = {f"refs/pull/{n}/head": sha
                   for n, _, sha, _ in RETIRED_PR_HEADS}
        with patch("retire_squash_equivalent_heads.validate_audit",
                   return_value={r["branch"]: r for r in report["branches"]}):
            wrong = dict(heads)
            wrong["refs/heads/" + RETIRED_PR_HEADS[0][1]] = "0" * 40
            with self.assertRaisesRegex(ValueError, "Remote branch moved"):
                validate_all(report, wrong, pr_refs, pulls_from_manifest())
            missing = dict(pr_refs)
            del missing["refs/pull/6/head"]
            with self.assertRaisesRegex(ValueError, "PR head ref unavailable"):
                validate_all(report, heads, missing, pulls_from_manifest())

    @patch("retire_squash_equivalent_heads.run_git")
    @patch("retire_squash_equivalent_heads.subprocess.run")
    def test_snapshot_parity_proves_full_git_tree(self, run, git):
        pr, name, head, merge = RETIRED_PR_HEADS[0]
        pull = pulls_from_manifest()[pr]
        git.side_effect = ["b" * 40, "b" * 40]
        run.return_value = subprocess.CompletedProcess([], 0)
        self.assertEqual(verify_snapshot_parity(pull, pr, name, head, merge), "b" * 40)
        git.side_effect = ["b" * 40, "c" * 40]
        with self.assertRaisesRegex(ValueError, "tree mismatch"):
            verify_snapshot_parity(pull, pr, name, head, merge)

    @patch("retire_squash_equivalent_heads.run_git")
    def test_guarded_actions_context_only(self, git):
        git.return_value = MAIN_SHA
        env = {
            "GITHUB_REPOSITORY": REPO, "GITHUB_ACTOR": ACTOR,
            "GITHUB_REF": "refs/heads/main", "GITHUB_EVENT_NAME": "push",
            "GITHUB_TOKEN": "test-only-not-a-real-credential",
            "GITHUB_SHA": MAIN_SHA,
        }
        checked_context(env)
        for key, value in [("GITHUB_REF", "refs/heads/feat/example"),
                           ("GITHUB_ACTOR", "other-user"),
                           ("GITHUB_REPOSITORY", "somewhere/else"),
                           ("GITHUB_EVENT_NAME", "pull_request")]:
            wrong = dict(env, **{key: value})
            with self.assertRaises(ValueError):
                checked_context(wrong)

    def test_without_execute_no_git_write_or_api_calls(self):
        with tempfile.TemporaryDirectory() as d:
            receipt = Path(d) / "receipt.json"
            audit = Path(d) / "audit.json"
            audit.write_text("{}")
            with patch("retire_squash_equivalent_heads.subprocess.run") as git:
                with self.assertRaisesRegex(ValueError, "Explicit --execute"):
                    execute(audit, receipt, {}, live=False)
                git.assert_not_called()
            record = json.loads(receipt.read_text())
            self.assertEqual(record["result"], "FAILED_OR_PARTIAL_REVIEW_REQUIRED")
            self.assertEqual(record["removed"], [])


if __name__ == "__main__":
    unittest.main()
