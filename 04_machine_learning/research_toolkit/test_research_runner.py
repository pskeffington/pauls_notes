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
