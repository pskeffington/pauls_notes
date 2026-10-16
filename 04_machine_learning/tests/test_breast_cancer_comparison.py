"""Challenge shared assessment, fixed-comparator training inputs and saved figures."""
import copy
import csv
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import joblib
import numpy as np

EXAMPLES = Path(__file__).resolve().parents[1] / 'examples'
sys.path.insert(0, str(EXAMPLES))
import breast_cancer_comparison as comparison
import plot_comparison as plots


class ComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = comparison.selection.make_cohort(seed=comparison.COHORT_SEED)
        cls.development, cls.test = comparison.make_plan(cls.data)
        cls.fixed_inputs = []
        original = comparison.fit_all_features

        def observe(x, y):
            model = original(x, y)
            cls.fixed_inputs.append((x.copy(), y.copy(), model))
            return model

        with patch.object(comparison, 'fit_all_features', observe):
            cls.models, cls.report = comparison.fit_development(cls.data, cls.development, cls.test)

    def test_fixed_comparator_uses_exact_outer_training_rows_and_all_columns(self):
        expected = [fold['analysis'] for fold in self.report['selected']['outer']] + [self.development]
        self.assertEqual(len(self.fixed_inputs), 4)
        for (x, y, model), rows in zip(self.fixed_inputs, expected):
            np.testing.assert_array_equal(x, self.data['x'][rows])
            np.testing.assert_array_equal(y, self.data['y'][rows])
            np.testing.assert_allclose(model.named_steps['impute'].statistics_, np.nanmedian(x, axis=0))
            filled = np.where(np.isnan(x), np.nanmedian(x, axis=0), x)
            np.testing.assert_allclose(model.named_steps['scale'].mean_, filled.mean(axis=0))
            self.assertEqual(model.named_steps['model'].coef_.shape, (1, 48))
            self.assertEqual(model.named_steps['model'].C, 1.0)
            self.assertNotIn('select', model.named_steps)
        self.assertEqual(self.report['pipeline_fits'], dict(selected=76, all_features=4, total=80))

    def test_reserved_values_cannot_change_either_development_procedure(self):
        changed = copy.deepcopy(self.data)
        changed['x'][self.test] = 100000
        changed['y'][self.test] = 1 - changed['y'][self.test]
        models, report = comparison.fit_development(changed, self.development, self.test)
        self.assertEqual(self.report, report)
        for key in self.models:
            expected = comparison.selection.probabilities(self.models[key], self.data['x'][self.development])
            actual = comparison.selection.probabilities(models[key], self.data['x'][self.development])
            np.testing.assert_allclose(actual, expected, rtol=0, atol=0)
        self.assertNotIn('final_test', report)
        self.assertFalse(report['final_test_used_for_selection'])

    def test_predictions_are_matched_and_primary_difference_recomputes(self):
        report = copy.deepcopy(self.report)
        report['final_test'] = comparison.assess(self.models, self.data, report)
        rows = comparison.prediction_rows(self.data, report)
        self.assertEqual({r['cohort_row'] for r in rows}, set(range(120)))
        for partition in ('development', 'test'):
            chosen = [r for r in rows if r['partition'] == partition]
            by_person = {}
            for row in chosen:
                by_person.setdefault(row['person_id'], []).append(row)
            self.assertTrue(all(len(pair) == 2 and {r['label'] for r in pair} == {0, 1}
                                for pair in by_person.values()))
            difference = np.mean([r['selected_squared_error'] - r['all_feature_squared_error'] for r in chosen])
            expected = report['development_brier_difference'] if partition == 'development' else report['final_test']['brier_difference']
            self.assertAlmostEqual(difference, expected)
        groups = self.data['person_id']
        for fold in report['selected']['outer']:
            self.assertFalse(set(groups[fold['analysis']]) & set(groups[fold['assessment']]))
        # No performance minimum or required direction of the observed difference.

    def test_export_replay_figures_and_invalid_saved_rows(self):
        snapshot = EXAMPLES.parent / 'gallery/example'
        plots.load_results(snapshot)
        for name, digest in json.loads((snapshot / 'manifest.json').read_text()).items():
            self.assertEqual(hashlib.sha256((snapshot / name).read_bytes()).hexdigest(), digest)
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'comparison run'
            comparison.run(output)
            models = joblib.load(output / 'models.joblib')
            report, rows, people = plots.load_results(output)
            self.assertEqual(len(people), 60)
            with np.load(output / 'synthetic_inputs.npz', allow_pickle=False) as data:
                for name, model in models.items():
                    p = comparison.selection.probabilities(model, data['x'][report['selected']['test']])
                    np.testing.assert_allclose(p, report['final_test'][name]['prediction'])
            for name, digest in json.loads((output / 'sha256.json').read_text()).items():
                self.assertEqual(hashlib.sha256((output / name).read_bytes()).hexdigest(), digest)
            for figure in ('brier-comparison', 'person-errors'):
                for suffix in ('svg', 'pdf', 'png'):
                    self.assertGreater((output / 'gallery' / f'{figure}.{suffix}').stat().st_size, 1000)
            with self.assertRaises(ValueError):
                comparison.run(output)
            with self.assertRaises(ValueError):
                plots.render_gallery(output, output / 'gallery')
            path = output / 'predictions.csv'
            original = path.read_bytes()
            def write(changed):
                with path.open('w', newline='') as stream:
                    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                    writer.writeheader()
                    writer.writerows(changed)
            altered = copy.deepcopy(rows)
            altered[0]['selected_probability'] = 'nan'
            write(altered)
            with self.assertRaises(ValueError): plots.load_results(output)
            write(rows + [rows[0]])
            with self.assertRaises(ValueError): plots.load_results(output)
            altered = copy.deepcopy(rows)
            altered[0]['outer_fold'] = '99'
            write(altered)
            with self.assertRaises(ValueError): plots.load_results(output)
            path.write_bytes(original)
            plots.render_gallery(output, Path(folder) / 'rerendered')

    def test_malformed_pairs_and_protected_destinations(self):
        changed = copy.deepcopy(self.data)
        changed['person_id'][1] = 1000
        with self.assertRaises(ValueError): comparison.make_plan(changed)
        with tempfile.TemporaryDirectory() as folder:
            link = Path(folder) / 'dangling'
            link.symlink_to(Path(folder) / 'absent')
            with self.assertRaises(ValueError): comparison.run(link)
            self.assertTrue(link.is_symlink())
        with self.assertRaises(ValueError): comparison.run(EXAMPLES.parent / 'forbidden-comparison')


if __name__ == '__main__':
    unittest.main()
