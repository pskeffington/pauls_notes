"""Offline regression tests for SHA-guarded historical-branch preflight."""
from copy import deepcopy
from datetime import datetime, timezone, timedelta
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from confirm_branch_retirement import ALLOWLIST, validate

BRANCH = "feat/phase4-assay-robustness-gates"
SHA = ALLOWLIST[BRANCH]["head"]
WHEN = datetime(2026, 10, 17, 22, 30, tzinfo=timezone.utc)


def report():
    return {
        "repository": "pskeffington/pauls_notes",
        "default_branch": "main",
        "checkout_sha": "f" * 40,
        "scanned_default_tree": True,
        "skipped_text_files": 0,
        "observed_utc": WHEN.isoformat(),
        "branches": [
            {"branch": "main", "head_sha": "f" * 40,
             "decision": "default_hold"},
            {
                "branch": BRANCH, "head_sha": SHA,
                "decision": "merged_manual_review",
                "matches_sole_merged_pr_head": True,
                "history_relative_to_default": "contained",
                "pull_requests": [1], "merged_prs": [1],
                "merged_commit_shas": [ALLOWLIST[BRANCH]["merge"]],
                "branch_qualified_links_in_default_tree": 0,
                "branch_qualified_links_in_pr_bodies": 0,
            },
        ],
    }


def check(value=None, **kwargs):
    opts = dict(branch=BRANCH, sha=SHA, confirmation="DELETE " + BRANCH,
                external_refs_reviewed="true", actor="pskeffington",
                repository="pskeffington/pauls_notes", now=WHEN)
    opts.update(kwargs)
    return validate(report() if value is None else value, **opts)


class RetirementPreflightTests(unittest.TestCase):
    def test_happy_path_is_only_a_preflight_receipt(self):
        r = check()
        self.assertEqual(r["result"], "PRECHECK_PASSED_NOT_DELETED")
        self.assertEqual(r["expected_head_sha"], SHA)
        self.assertEqual(r["pr"], 1)
        self.assertTrue(r["lease_required"])

    def test_all_allowlisted_heads_are_fixed_hashes(self):
        self.assertEqual(len(ALLOWLIST), 5)
        self.assertEqual(len({v["pr"] for v in ALLOWLIST.values()}), 5)
        for key, v in ALLOWLIST.items():
            self.assertEqual(len(v["head"]), 40)
            self.assertEqual(len(v["merge"]), 40)
            self.assertNotIn(key, ("main", "work/learning-check-coverage",
                                   "feat/g4-survival-execution-20261017",
                                   "feat/config-driven-ml-research-toolkit",
                                   "docs/g4-frozen-synthetic-survival-protocol-20261017"))

    def test_never_allow_frozen_or_active_research_heads(self):
        for branch in ("main", "feat/config-driven-ml-research-toolkit",
                       "feat/g4-survival-execution-20261017",
                       "docs/g4-frozen-synthetic-survival-protocol-20261017",
                       "work/biomedical-learning"):
            with self.subTest(branch=branch), self.assertRaisesRegex(ValueError, "allowlist"):
                check(branch=branch, confirmation="DELETE " + branch)

    def test_reject_changed_or_invalid_sha(self):
        for sha in ("0" * 40, "abc", "A" * 40, "", SHA + "0"):
            with self.subTest(sha=sha), self.assertRaises(ValueError):
                check(sha=sha)

    def test_reject_different_actor_or_repository(self):
        for override in ({"actor": "another-user"},
                         {"repository": "other/repo"}):
            with self.subTest(override=override), self.assertRaises(ValueError):
                check(**override)

    def test_reject_missing_confirmation_and_external_review(self):
        for override in ({"confirmation": "DELETE"},
                         {"confirmation": "DELETE main"},
                         {"external_refs_reviewed": "false"},
                         {"external_refs_reviewed": "TRUE"}):
            with self.subTest(override=override), self.assertRaises(ValueError):
                check(**override)

    def test_reject_incomplete_audit(self):
        mutations = (
            ("scanned_default_tree", False),
            ("skipped_text_files", 1),
            ("checkout_sha", "0" * 40),
            ("default_branch", "develop"),
            ("repository", "someone/repo"),
        )
        for field, change in mutations:
            r = report()
            r[field] = change
            with self.subTest(field=field), self.assertRaises(ValueError):
                check(r)

    def test_reject_stale_or_future_audit(self):
        for moment in (WHEN - timedelta(minutes=11),
                       WHEN + timedelta(seconds=1)):
            r = report()
            r["observed_utc"] = moment.isoformat()
            with self.subTest(time=moment), self.assertRaises(ValueError):
                check(r)

    def test_reject_any_candidate_control_mutation(self):
        mutations = (
            ("decision", "diverged_history_hold"),
            ("head_sha", "0" * 40),
            ("matches_sole_merged_pr_head", False),
            ("history_relative_to_default", "diverged"),
            ("pull_requests", [1, 99]),
            ("merged_prs", []),
            ("merged_commit_shas", ["a" * 40]),
            ("branch_qualified_links_in_default_tree", 1),
            ("branch_qualified_links_in_pr_bodies", 1),
        )
        for field, change in mutations:
            r = report()
            r["branches"][1][field] = change
            with self.subTest(field=field), self.assertRaises(ValueError):
                check(r)

    def test_reject_missing_or_duplicate_branch_row(self):
        for delete in (True, False):
            r = report()
            if delete:
                r["branches"].pop()
            else:
                r["branches"].append(deepcopy(r["branches"][1]))
            with self.subTest(delete=delete), self.assertRaises(ValueError):
                check(r)


if __name__ == "__main__":
    unittest.main()
