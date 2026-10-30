#!/usr/bin/env python3
"""Regression tests for agent registry identifiers and dependency graph."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from check_agent_tasks import ROOT, validate


class AgentTaskRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads((ROOT / "docs/agent-tasks.json").read_text())
        cls.manifest = json.loads((ROOT / "oncology/book-manifest.json").read_text())

    def test_actual_registry_and_chapter_paths(self):
        self.assertEqual([], validate(self.registry, self.manifest, ROOT))

    def test_scoped_g4_and_g5_task_ids(self):
        ids = {task["id"] for task in self.registry["tasks"]}
        self.assertIn("G4-01", ids)
        self.assertIn("G5-01", ids)

    def test_cycle_rejected(self):
        registry = copy.deepcopy(self.registry)
        for task in registry["tasks"]:
            if task["id"] == "IDX-01":
                task["depends_on"] = ["IDX-02"]
        self.assertTrue(any("cycle" in error for error in validate(registry, self.manifest, ROOT)))

    def test_verified_requires_evidence(self):
        registry = copy.deepcopy(self.registry)
        registry["tasks"][0]["state"] = "verified"
        self.assertTrue(any("verified without recorded evidence" in error for error in validate(registry, self.manifest, ROOT)))


if __name__ == "__main__":
    unittest.main()
