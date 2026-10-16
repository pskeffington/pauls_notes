"""Challenge group boundaries, train-only transforms and persistence."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import joblib
import numpy as np

SPEC = importlib.util.spec_from_file_location("sklearn_methods",
    Path(__file__).resolve().parents[1] / "examples/sklearn_methods.py")
METHODS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(METHODS)


class MethodsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = METHODS.make_cohort()
        cls.train, cls.test = METHODS.make_plan(cls.data)

    def test_schema_and_family_rejections(self):
        data = copy.deepcopy(self.data)
        data["person_id"][1] = data["person_id"][0]
        with self.assertRaises(ValueError):
            METHODS.validate_cohort(data)
        data = copy.deepcopy(self.data); data["x"][:, 0] = np.nan
        with self.assertRaises(ValueError):
            METHODS.validate_cohort(data)
        # Complete row partition, but related people are deliberately separated.
        with self.assertRaises(ValueError):
            METHODS.check_partition(np.arange(0, 120, 2), np.arange(1, 120, 2), self.data["groups"])

    def test_nested_predictions_and_leakage(self):
        result, saved = METHODS.fit_supervised(self.data, self.train, self.test, "classification")
        groups = self.data["groups"][self.train]
        changed = copy.deepcopy(self.data); changed["x"][self.test] = 100000
        replay, refitted = METHODS.fit_supervised(changed, self.train, self.test, "classification")
        for name in saved:
            entry = result[name]
            np.testing.assert_allclose(entry["oof_prediction"], replay[name]["oof_prediction"])
            np.testing.assert_allclose(saved[name].best_estimator_.named_steps["impute"].statistics_,
                np.nanmedian(self.data["x"][self.train], axis=0))
            np.testing.assert_allclose(saved[name].best_estimator_.named_steps["impute"].statistics_,
                refitted[name].best_estimator_.named_steps["impute"].statistics_)
            all_assessed = []
            for outer in entry["outer_memberships"]:
                METHODS.check_partition(np.array(outer["analysis"]), np.array(outer["assessment"]), groups)
                all_assessed.extend(outer["assessment"])
                for inner in outer["inner"]:
                    METHODS.check_partition(np.array(inner["analysis"]), np.array(inner["assessment"]),
                        groups, universe=outer["analysis"])
            self.assertEqual(sorted(all_assessed), list(range(len(self.train))))
            self.assertTrue(np.isfinite(list(entry["test"].values())).all())

    def test_regression_and_unsupervised(self):
        result, models = METHODS.fit_supervised(self.data, self.train, self.test, "regression")
        for name in models:
            self.assertGreaterEqual(result[name]["test"]["rmse"], 0)
            self.assertEqual(len(result[name]["oof_prediction"]), len(self.train))
        embedding, fitted = METHODS.fit_unsupervised(self.data, self.train, self.test)
        self.assertEqual(np.shape(embedding["test_projection"]), (len(self.test), 2))
        np.testing.assert_allclose(fitted["transform"].named_steps["impute"].statistics_,
            np.nanmedian(self.data["x"][self.train], axis=0))
        # Outcome changes must not affect an unsupervised embedding.
        changed = copy.deepcopy(self.data); changed["classification"] = 1 - changed["classification"]
        second, _ = METHODS.fit_unsupervised(changed, self.train, self.test)
        np.testing.assert_allclose(embedding["test_projection"], second["test_projection"])

    def test_export_and_prediction_replay(self):
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "methods output"
            METHODS.run(output)
            with self.assertRaises(ValueError):
                METHODS.run(output)
            report = json.loads((output / "metrics.json").read_text())
            model = joblib.load(output / "models.joblib")
            for task in ("classification", "regression"):
                for name, estimator in model[task].items():
                    np.testing.assert_allclose(METHODS.predict_task(estimator, self.data["x"][self.test], task),
                        report[task][name]["test_prediction"])


if __name__ == "__main__":
    unittest.main()
