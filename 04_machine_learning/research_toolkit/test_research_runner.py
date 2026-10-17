"""Regression checks for configuration-only synthetic grouped ML."""
import copy
import importlib.util
import json
import tempfile
import unittest
from unittest import mock
import numpy as np
from pathlib import Path

SOURCE = Path(__file__).with_name("research_runner.py")
spec = importlib.util.spec_from_file_location("research_runner", SOURCE)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
CONFIG = json.loads(Path(__file__).with_name("synthetic_brca_config.json").read_text())

class ResearchRunnerTests(unittest.TestCase):
    def test_seed_replays_identically(self):
        first, second = runner.run(CONFIG), runner.run(CONFIG)
        self.assertEqual(first, second)
        self.assertEqual(len(first["records"]), 6)
        for row in first["records"]:
            self.assertEqual(len(row["probability_class_1"]), row["test_rows"])
            self.assertEqual(len(row["test_group_ids"]), row["test_rows"])
            self.assertEqual(len(set(row["test_group_ids"])), row["test_people"])

    def test_person_grouping_candidate_history_and_descriptive_calibration(self):
        result = runner.run(CONFIG)
        self.assertEqual(result["groups"], CONFIG["data"]["people"])
        people_by_fold = []
        for row in result["records"]:
            train = set(row["train_group_ids"])
            test = set(row["test_group_ids"])
            self.assertFalse(train & test)
            self.assertEqual(len(train), row["train_people"])
            self.assertEqual(len(test), row["test_people"])
            self.assertEqual(train | test, set(range(result["groups"])))
            self.assertEqual(len(row["labels"]), row["test_rows"])
            self.assertEqual(sum(b["observations"] for b in row["calibration_descriptive_bins"]), row["test_rows"])
            self.assertEqual(sum(b["positive_labels"] for b in row["calibration_descriptive_bins"]), sum(row["labels"]))
            for b in row["calibration_descriptive_bins"]:
                self.assertGreaterEqual(b["positive_labels"], 0)
                self.assertLessEqual(b["positive_labels"], b["observations"])
                if b["observations"] == 0:
                    self.assertIsNone(b["mean_predicted_class_1"])
                else:
                    self.assertGreaterEqual(b["mean_predicted_class_1"], b["lower_probability"])
                    self.assertLessEqual(b["mean_predicted_class_1"], b["upper_probability"])
            if row["model"] == "logistic":
                choices = row["inner_candidate_scores"]
                self.assertEqual(
                    len(choices),
                    len(CONFIG["design"]["feature_counts"]) * len(CONFIG["design"]["regularization_C"])
                )
                self.assertTrue(all(1 <= c["inner_rank"] <= len(choices) for c in choices))
                self.assertEqual(len(row["selected_feature_indices"]), row["selected_parameters"]["select__k"])
                self.assertEqual(
                    len(row["selected_coefficients_standardized_class_1"]),
                    len(row["selected_feature_indices"]),
                )
                self.assertTrue(all(0 <= k < result["features"] for k in row["selected_feature_indices"]))
                people_by_fold.append(test)
            else:
                self.assertIsNone(row["selected_parameters"])
                self.assertIsNone(row["inner_candidate_scores"])
                self.assertIsNone(row["selected_feature_indices"])
        self.assertEqual(len(people_by_fold), CONFIG["design"]["outer_folds"])
        self.assertEqual(set.union(*people_by_fold), set(range(result["groups"])))
        for i, a in enumerate(people_by_fold):
            for b in people_by_fold[i + 1:]:
                self.assertFalse(a & b)

    def test_unapproved_cancer_data_sources_are_not_admitted(self):
        for extra in (
            {"data_path": "/local/another-tumor.csv"},
            {"dataset": "TCGA-BRCA"},
            {"provider": "institutional_imaging"},
            {"clinical_use_authorized": True},
        ):
            item = copy.deepcopy(CONFIG)
            item.update(extra)
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                runner.validate(item)

    def test_generator_signal_matches_its_invented_targets(self):
        # Deliberately obvious fictional signal: the classifier must retain the
        # feature/label association emitted by make_classification, not reshuffle
        # labels independently of the generated person-level measurements.
        def known_signal(**kwargs):
            n, columns = kwargs["n_samples"], kwargs["n_features"]
            labels = np.arange(n) % 2
            matrix = np.random.default_rng(101).normal(0, .1, (n, columns))
            matrix[:, 0] += (2 * labels - 1) * 8.0
            return matrix, labels

        with mock.patch.object(runner, "make_classification", side_effect=known_signal):
            result = runner.run(CONFIG)
        assessment = [r for r in result["records"] if r["model"] == "logistic"]
        self.assertEqual(len(assessment), CONFIG["design"]["outer_folds"])
        # This bounded negative-control fixture would reliably fail if the
        # generated labels were independently randomized after generating X.
        self.assertTrue(all(r["balanced_accuracy"] >= .95 for r in assessment))

    def test_research_and_external_training_refused(self):
        for stage in ["patient-prediction", "frozen-descriptive", "research-training"]:
            item = copy.deepcopy(CONFIG)
            item["stage"] = stage
            with self.assertRaisesRegex(ValueError, "NOT admitted"):
                runner.validate(item)
        item = copy.deepcopy(CONFIG)
        item["data"]["path"] = "/private/TCGA.csv"
        with self.assertRaises(ValueError):
            runner.validate(item)

    def test_bad_configuration_rejected(self):
        for section, field, value in [("data", "missing_fraction", .8), ("data", "features", 0), ("design", "outer_folds", 1), ("design", "feature_counts", [1000]), ("design", "regularization_C", [-1.0])]:
            item = copy.deepcopy(CONFIG)
            item[section][field] = value
            with self.subTest(section=section, field=field), self.assertRaises(ValueError):
                runner.validate(item)

    def test_output_stays_outside_public_repository(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "config.json"
            source.write_text(json.dumps(CONFIG))
            forbidden = SOURCE.parent / "should-not-create-private-output"
            self.assertFalse(forbidden.exists())
            with self.assertRaisesRegex(ValueError, "outside the public source repository"):
                runner.main(["--config", str(source), "--output", str(forbidden)])
            self.assertFalse(forbidden.exists())

    def test_disclaimer_embedded_in_every_report(self):
        model_use = runner.run(CONFIG)["model_use"]
        self.assertFalse(model_use["clinical_use_authorized"])
        self.assertFalse(model_use["patient_level_training_authorized"])
        self.assertFalse(model_use["tcga_case_data_processed"])
        self.assertFalse(model_use["real_cancer_data_processed"])
        self.assertIn("any_cancer_type", model_use["research_scope"])
        self.assertEqual(model_use["current_worked_case"], "synthetic_breast_specimen_category")
        self.assertIn("NOT FOR CLINICAL USE", model_use["disclaimer"])

    def test_output_is_exclusive(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "config.json"
            config.write_text(json.dumps(CONFIG))
            output = Path(tmp) / "output"
            runner.main(["--config", str(config), "--output", str(output)])
            original = (output / "report.json").read_bytes()
            with self.assertRaisesRegex(ValueError, "already exists"):
                runner.main(["--config", str(config), "--output", str(output)])
            self.assertEqual(original, (output / "report.json").read_bytes())

if __name__ == "__main__":
    unittest.main()
