"""Prevent incomplete paper coverage and hidden reproduction disagreements."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("evidence", ROOT / "scripts/check_biostatistics_evidence.py")
evidence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evidence)


class EvidenceCoverageTests(unittest.TestCase):
    def setUp(self):
        self.register = json.loads((evidence.ATLAS / "decision-tree-evidence.json").read_text())
        self.guide = (evidence.ATLAS / self.register["chart"]).read_text()
        self.source = (evidence.ATLAS / self.register["source"]).read_text()
        self.atlas = (evidence.ATLAS / "README.md").read_text()

    def check(self, register=None, atlas=None, source=None):
        return evidence.validate_evidence(register or self.register, self.guide,
                                         self.atlas if atlas is None else atlas,
                                         self.source if source is None else source)

    def test_current_coverage(self):
        self.assertEqual(self.check(), [])

    def test_unmapped_design_diamond_fails(self):
        register = copy.deepcopy(self.register)
        register["nodes"] = [n for n in register["nodes"] if n["node"] != "D"]
        self.assertTrue(self.check(register))

    def test_compound_node_loses_one_alternative(self):
        register = copy.deepcopy(self.register)
        next(n for n in register["nodes"] if n["node"] == "CH")["outputs"].remove("multinomial")
        self.assertTrue(self.check(register))

    def test_missing_paper_and_missing_implementation_fail(self):
        register = copy.deepcopy(self.register)
        register["nodes"][0]["paper_ids"] = ["NONEXISTENT"]
        self.assertTrue(self.check(register))
        self.assertTrue(self.check(source=self.source.replace("negative_binomial =", "removed =")))

    def test_cannot_hide_failed_reproduction(self):
        self.assertTrue(self.check(atlas=self.atlas.replace("Disagreement retained", "Confirmed")))


if __name__ == "__main__":
    unittest.main()
