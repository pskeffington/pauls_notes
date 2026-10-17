"""Roadmap gate acceptance: negative controls prevent evidence inflation."""
import copy
import importlib.util
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "check_milestone_evidence.py"
spec = importlib.util.spec_from_file_location("milestone_evidence", SOURCE)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class MilestoneEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.snapshot = checker.read_snapshot()
        cls.roadmap = checker.ROADMAP.read_text(encoding="utf-8")

    def inspect(self, snapshot=None, roadmap=None):
        return checker.inspect(
            self.snapshot if snapshot is None else snapshot,
            self.roadmap if roadmap is None else roadmap,
        )

    @staticmethod
    def gate(snapshot, ident):
        return next(item for item in snapshot["gates"] if item["id"] == ident)

    def test_existing_record_is_structurally_auditable(self):
        self.assertEqual(self.inspect(), [])
        counts = {}
        for gate in self.snapshot["gates"]:
            counts[gate["status"]] = counts.get(gate["status"], 0) + 1
        self.assertEqual(counts, {"complete_bounded": 7, "in_review": 3, "planned": 2, "blocked": 1})

    def test_draft_pr_cannot_be_promoted_by_editing_status(self):
        snapshot = copy.deepcopy(self.snapshot)
        self.gate(snapshot, "R3")["status"] = "complete_bounded"
        problems = self.inspect(snapshot)
        self.assertTrue(any("delivery scope" in issue or "merge commit" in issue for issue in problems))

    def test_successful_ci_id_is_required_for_merged_scope(self):
        snapshot = copy.deepcopy(self.snapshot)
        self.gate(snapshot, "R0")["ci_run_id"] = 0
        self.assertTrue(any("traceable PR head or CI" in issue for issue in self.inspect(snapshot)))
        snapshot = copy.deepcopy(self.snapshot)
        self.gate(snapshot, "G2")["merge_commit"] = ""
        self.assertTrue(any("verified merge commit" in issue for issue in self.inspect(snapshot)))

    def test_missing_committed_evidence_and_unreviewed_data_are_rejected(self):
        snapshot = copy.deepcopy(self.snapshot)
        self.gate(snapshot, "R2")["evidence_path"] = "04_machine_learning/research_toolkit/patient_predictions.csv"
        self.assertTrue(any("recorded committed evidence_path not found" in issue for issue in self.inspect(snapshot)))
        snapshot = copy.deepcopy(self.snapshot)
        self.gate(snapshot, "D1")["real_patient_training_authorized"] = True
        self.assertTrue(any("permission is not established" in issue for issue in self.inspect(snapshot)))

    def test_human_table_cannot_disagree_with_machine_status(self):
        changed = self.roadmap.replace(
            "| R0 | Rust syntax", "| R0 | Rust syntax",
        ).replace(
            "| **Complete (bounded)** | [R0 evidence]",
            "| **Planned** | [R0 evidence]",
        )
        self.assertNotEqual(changed, self.roadmap)
        self.assertTrue(any("R0: published summary" in issue for issue in self.inspect(roadmap=changed)))

    def test_dependency_cycles_are_rejected(self):
        snapshot = copy.deepcopy(self.snapshot)
        self.gate(snapshot, "G0")["depends_on"] = ["G1"]
        self.assertTrue(any("cyclic milestone dependencies" in issue for issue in self.inspect(snapshot)))

    def test_direct_ids_and_clinical_release_cannot_be_silently_changed(self):
        snapshot = copy.deepcopy(self.snapshot)
        self.gate(snapshot, "R0")["learner_mastery"] = "passed"
        self.gate(snapshot, "G0")["clinical_use_authorized"] = True
        self.gate(snapshot, "D1")["status"] = "complete_bounded"
        issues = self.inspect(snapshot)
        self.assertTrue(any("CI result cannot certify personal mastery" in issue for issue in issues))
        self.assertTrue(any("release/clinical permission" in issue for issue in issues))
        self.assertTrue(any("D1 remains blocked" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
