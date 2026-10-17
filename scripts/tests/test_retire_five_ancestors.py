"""Offline checks only: never run Git remote writes in the test suite."""
import os
from unittest import TestCase
from unittest.mock import patch
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from confirm_branch_retirement import ALLOWLIST
from retire_five_ancestors import (
    HOLD_BRANCHES, assert_context, check_remote_heads, deletion_command,
    parse_remote_heads,
)


class AncestorCleanupTests(TestCase):
    def good_env(self):
        return {
            "GITHUB_REPOSITORY": "pskeffington/pauls_notes",
            "GITHUB_ACTOR": "pskeffington",
            "GITHUB_REF": "refs/heads/main",
            "GITHUB_EVENT_NAME": "push",
            "GITHUB_SHA": "a"*40,
            "GITHUB_TOKEN": "offline-test-only",
        }

    def test_only_five_original_merged_ancestors(self):
        self.assertEqual(len(ALLOWLIST), 5)
        self.assertEqual(set(v["pr"] for v in ALLOWLIST.values()), set(range(1, 6)))
        self.assertFalse(set(ALLOWLIST) & set(HOLD_BRANCHES))

    def test_owner_and_event_are_mandatory(self):
        assert_context(self.good_env())
        for field, value in (
            ("GITHUB_ACTOR", "another-user"),
            ("GITHUB_REF", "refs/heads/feature"),
            ("GITHUB_EVENT_NAME", "workflow_dispatch"),
            ("GITHUB_REPOSITORY", "another/repo"),
            ("GITHUB_SHA", ""),
            ("GITHUB_TOKEN", ""),
        ):
            env = self.good_env()
            env[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                assert_context(env)

    def test_remote_parser_and_exact_sha(self):
        remote = {name: v["head"] for name, v in ALLOWLIST.items()}
        remote.update({name: "f"*40 for name in HOLD_BRANCHES})
        text = "".join(f"{sha}\trefs/heads/{name}\n"
                       for name, sha in remote.items())
        self.assertEqual(check_remote_heads(parse_remote_heads(text)),
                         sorted(ALLOWLIST))
        with self.assertRaisesRegex(ValueError, "Remote SHA"):
            check_remote_heads({**remote, next(iter(ALLOWLIST)): "0"*40})

    def test_retirement_cannot_touch_other_refs(self):
        for forbidden in HOLD_BRANCHES + ("docs/g4-frozen-synthetic-survival-protocol-20261017",
                                          "feat/standalone-synthetic-oncology-ml"):
            with self.subTest(forbidden=forbidden), self.assertRaises(ValueError):
                deletion_command(forbidden)
        for name in ALLOWLIST:
            command = deletion_command(name)
            self.assertEqual(command[0:3], ["git", "push", "--porcelain"])
            self.assertEqual(command[3],
                             "--force-with-lease=refs/heads/" + name
                             + ":" + ALLOWLIST[name]["head"])
            self.assertEqual(command[-2:], ["origin", ":refs/heads/" + name])

    def test_remote_parser_rejects_invalid_input(self):
        for data in ("not a git ref", "abcd\trefs/tags/t",
                     "a"*40 + "\trefs/heads/x\n" +
                     "b"*40 + "\trefs/heads/x\n"):
            with self.subTest(data=data), self.assertRaises(ValueError):
                parse_remote_heads(data)


if __name__ == "__main__":
    import unittest
    unittest.main()
