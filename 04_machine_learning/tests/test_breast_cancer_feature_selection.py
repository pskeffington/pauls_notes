"""Challenge paired-person boundaries, selection leakage and prediction replay."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import joblib
import numpy as np

SPEC = importlib.util.spec_from_file_location("breast_cancer_selection",
    Path(__file__).resolve().parents[1] / "examples/breast_cancer_feature_selection.py")
METHODS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(METHODS)


class FeatureSelectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = METHODS.make_cohort()
        cls.development, cls.test = METHODS.make_plan(cls.data)
        cls.model, cls.report = METHODS.fit_development(cls.data, cls.development, cls.test)

    def test_schema_and_person_boundaries(self):
        self.assertEqual((len(self.development), len(self.test)), (90, 30))
        bad = copy.deepcopy(self.data)
        bad["specimen_id"][1] = bad["specimen_id"][0]
        with self.assertRaises(ValueError):
            METHODS.validate_cohort(bad)
        bad = copy.deepcopy(self.data)
        bad["feature_names"] = bad["feature_names"][::-1]
        with self.assertRaises(ValueError):
            METHODS.validate_cohort(bad)
        bad = copy.deepcopy(self.data)
        bad["x"][self.development, 0] = np.nan
        with self.assertRaises(ValueError):
            METHODS.fit_development(bad, self.development, self.test)
        bad = copy.deepcopy(self.data)
        bad["y"][0] = bad["y"][1]
        with self.assertRaises(ValueError):
            METHODS.validate_cohort(bad)
        with self.assertRaises(ValueError):
            METHODS.check_partition(np.arange(0, 120, 2), np.arange(1, 120, 2), self.data["person_id"])
        assessed = []
        for outer in self.report["outer"]:
            analysis, assessment = np.array(outer["analysis"]), np.array(outer["assessment"])
            METHODS.check_partition(analysis, assessment, self.data["person_id"], self.development)
            self.assertEqual((len(analysis), len(assessment)), (60, 30))
            assessed.extend(assessment)
            for inner in outer["inner"]:
                a, b = np.array(inner["analysis"]), np.array(inner["assessment"])
                METHODS.check_partition(a, b, self.data["person_id"], analysis)
                self.assertEqual((len(a), len(b)), (40, 20))
        self.assertEqual(sorted(assessed), sorted(self.development))
        for inner in self.report["final_inner"]:
            METHODS.check_partition(np.array(inner["analysis"]), np.array(inner["assessment"]),
                                    self.data["person_id"], self.development)

    def test_reserved_values_cannot_change_training_or_feature_review(self):
        changed = copy.deepcopy(self.data)
        changed["x"][self.test] = 100000
        changed["y"][self.test] = 1 - changed["y"][self.test]
        refit, replay = METHODS.fit_development(changed, self.development, self.test)
        self.assertEqual(self.report, replay)
        np.testing.assert_allclose(self.model.best_estimator_.named_steps["model"].coef_,
                                   refit.best_estimator_.named_steps["model"].coef_)
        self.assertEqual(METHODS.feature_review(self.model, self.report), METHODS.feature_review(refit, replay))

    def test_imputer_and_selector_fit_inside_each_inner_fold(self):
        # Observe actual GridSearchCV fits, rather than fitting a separate pipeline.
        x = self.data["x"][self.development]
        y = self.data["y"][self.development]
        groups = self.data["person_id"][self.development]
        imputer_fits, selector_fits = [], []
        original_imputer = METHODS.SimpleImputer.fit
        original_selector = METHODS.SelectKBest.fit

        def observe_imputer(instance, values, target=None):
            result = original_imputer(instance, values, target)
            imputer_fits.append((values.copy(), instance.statistics_.copy()))
            return result

        def observe_selector(instance, values, target=None):
            result = original_selector(instance, values, target)
            selector_fits.append((values.copy(), target.copy(), instance.scores_.copy()))
            return result

        with patch.object(METHODS.SimpleImputer, "fit", observe_imputer), \
             patch.object(METHODS.SelectKBest, "fit", observe_selector):
            _, folds = METHODS._fit_search(x, y, groups)
        # Six candidates across three folds, followed by one full-development refit.
        self.assertEqual(len(imputer_fits), 19)
        self.assertEqual(len(selector_fits), 19)
        possible_rows = [a for a, _ in folds] + [np.arange(len(x))]
        counts = [0] * len(possible_rows)
        for (observed, medians), (selected_input, target, ranking) in zip(imputer_fits, selector_fits):
            match = [i for i, rows in enumerate(possible_rows)
                     if np.array_equal(observed, x[rows], equal_nan=True)]
            self.assertEqual(len(match), 1)
            i = match[0]
            counts[i] += 1
            rows = possible_rows[i]
            expected_median = np.nanmedian(x[rows], axis=0)
            np.testing.assert_allclose(medians, expected_median)
            expected_input = np.where(np.isnan(x[rows]), expected_median, x[rows])
            np.testing.assert_allclose(selected_input, expected_input)
            np.testing.assert_array_equal(target, y[rows])
            expected_rank, _ = METHODS.f_classif(expected_input, y[rows])
            np.testing.assert_allclose(ranking, expected_rank)
        self.assertEqual(counts, [6, 6, 6, 1])

    def test_selected_columns_and_interpretation_fields(self):
        selected = METHODS.selected_features(self.model)
        self.assertEqual(len(selected), self.report["best_parameters"]["select__k"])
        self.assertTrue(set(selected) <= set(METHODS.FEATURES))
        review = METHODS.feature_review(self.model, self.report)
        self.assertEqual(len(review), 48)
        self.assertEqual(sum(row["final_selected"] for row in review), len(selected))
        for row in review:
            self.assertIn(row["selected_outer_fits"], range(4))
            self.assertEqual(row["outer_fits"], 3)
            self.assertTrue(np.isfinite(row["mean_outer_permutation_brier_increase"]))
            if not row["final_selected"]:
                self.assertEqual(row["standardized_coefficient"], "")
        self.assertEqual(len(self.report["outer_predictions"]), len(self.development))
        self.assertTrue(np.isfinite(list(self.report["nested_development"].values())).all())

    def test_candidate_traces_metric_direction_and_budget(self):
        traces = [fold["search_candidates"] for fold in self.report["outer"]]
        traces.append(self.report["final_search_candidates"])
        for candidates in traces:
            self.assertEqual(len(candidates), 6)
            chosen = [candidate for candidate in candidates if candidate["chosen"]]
            self.assertEqual(len(chosen), 1)
            self.assertEqual(chosen[0]["rank"], 1)
            self.assertAlmostEqual(chosen[0]["mean_brier"],
                                   min(candidate["mean_brier"] for candidate in candidates))
            for candidate in candidates:
                self.assertEqual(len(candidate["fold_brier"]), 3)
                self.assertTrue(all(0 <= value <= 1 for value in candidate["fold_brier"]))
                self.assertAlmostEqual(candidate["mean_brier"], np.mean(candidate["fold_brier"]))
        # Replay exported scores against the actual GridSearchCV result arrays.
        x, y = self.data["x"][self.development], self.data["y"][self.development]
        search, _ = METHODS._fit_search(x, y, self.data["person_id"][self.development])
        self.assertEqual(self.report["final_search_candidates"], METHODS.summarize_search(search))
        contract = self.report["tuning_contract"]
        self.assertEqual(contract["candidate_pipeline_fits"], 72)
        self.assertEqual(contract["refit_pipeline_fits"], 4)
        self.assertEqual(contract["total_pipeline_fits"], 76)
        self.assertFalse(contract["final_test_used_for_selection"])
        self.assertEqual(contract["selection_direction"], "maximize")
        self.assertEqual(contract["reported_error_direction"], "minimize")

    def test_export_integrity_replay_and_output_protection(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "paired feature run"
            METHODS.run(output)
            model = joblib.load(output / "pipeline.joblib")
            report = json.loads((output / "report.json").read_text())
            with np.load(output / "synthetic_inputs.npz", allow_pickle=False) as inputs:
                predicted = METHODS.probabilities(model, inputs["x"][report["test"]])
            np.testing.assert_allclose(predicted, report["final_test"]["prediction"])
            for name, digest in json.loads((output / "sha256.json").read_text()).items():
                self.assertEqual(hashlib.sha256((output / name).read_bytes()).hexdigest(), digest)
            with self.assertRaises(ValueError):
                METHODS.run(output)
            link = Path(folder) / "dangling"
            link.symlink_to(Path(folder) / "absent")
            with self.assertRaises(ValueError):
                METHODS.run(link)
            self.assertTrue(link.is_symlink())
            with self.assertRaises(ValueError):
                METHODS.run(Path(METHODS.__file__).resolve().parents[2] / "forbidden-selection-output")


if __name__ == "__main__":
    unittest.main()
