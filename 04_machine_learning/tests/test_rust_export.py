"""Challenge portable parameter extraction and trusted-artifact boundaries."""
import copy
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

EXAMPLES = Path(__file__).resolve().parents[1] / 'examples'
sys.path.insert(0, str(EXAMPLES))
import export_rust_inference as exporter
import breast_cancer_comparison as comparison


class RustExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = comparison.selection.make_cohort(seed=comparison.COHORT_SEED)
        cls.development, cls.test = comparison.make_plan(cls.data)
        cls.models, cls.report = comparison.fit_development(cls.data, cls.development, cls.test)

    def test_exports_actual_training_parameters_and_selected_column_order(self):
        for name, fitted in self.models.items():
            document = exporter.portable_model(fitted, self.data['feature_names'], name)
            pipeline = fitted.best_estimator_ if name == 'selected' else fitted
            np.testing.assert_allclose(document['imputation_medians'], np.nanmedian(self.data['x'][self.development], axis=0))
            indices = document['selected_indices']
            self.assertEqual(indices, sorted(set(indices)))
            imputed = np.where(np.isnan(self.data['x'][self.development]), document['imputation_medians'],
                               self.data['x'][self.development])[:, indices]
            np.testing.assert_allclose(document['scaler_means'], imputed.mean(axis=0))
            np.testing.assert_allclose(document['scaler_scales'], imputed.std(axis=0))
            np.testing.assert_array_equal(document['coefficients'], pipeline.named_steps['model'].coef_[0])
            self.assertEqual(document['positive_class'], 1)
            self.assertEqual(document['training_partition'], 'development')

    def test_rejects_unsupported_transforms_and_class_direction(self):
        model = copy.deepcopy(self.models['all_features'])
        model.named_steps['scale'].with_mean = False
        with self.assertRaises(ValueError): exporter.portable_model(model, self.data['feature_names'], 'all_features')
        model = copy.deepcopy(self.models['all_features'])
        model.named_steps['model'].classes_ = np.array([1, 0])
        with self.assertRaises(ValueError): exporter.portable_model(model, self.data['feature_names'], 'all_features')
        with self.assertRaises(ValueError): exporter.portable_model(self.models['all_features'], self.data['feature_names'][::-1], 'all_features')
        with self.assertRaises(ValueError): exporter.portable_model(self.models['selected'], self.data['feature_names'], 'unknown')

    def test_untrusted_or_changed_artifacts_never_reach_joblib(self):
        with tempfile.TemporaryDirectory() as folder, patch.object(exporter.joblib, 'load') as load:
            root = Path(folder)
            with self.assertRaises(ValueError): exporter.export_bundle(root, root / 'out')
            (root / 'models.joblib').write_bytes(b'changed model')
            (root / 'sha256.json').write_text(json.dumps({'models.joblib': '0' * 64}))
            with self.assertRaises(ValueError): exporter.export_bundle(root, root / 'out', trusted_local_bundle=True)
            load.assert_not_called()
            link = root / 'dangling'
            link.symlink_to(root / 'absent')
            with self.assertRaises(ValueError): exporter.new_output(link)
            self.assertTrue(link.is_symlink())
        with self.assertRaises(ValueError): exporter.new_output(EXAMPLES.parent / 'forbidden-export')

    def test_full_export_inventories_inputs_and_preserves_reserved_predictions(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            bundle = comparison.run(root / 'training')
            output = exporter.export_bundle(bundle, root / 'portable', trusted_local_bundle=True)
            inventory = exporter.verify_inventory(output)
            self.assertTrue({'selected.json', 'all_features.json', 'specimens.csv', 'export.json'} <= set(inventory))
            with (output / 'specimens.csv').open(newline='') as stream:
                inputs = list(csv.reader(stream))
            self.assertEqual(inputs[0], ['specimen_id', *self.data['feature_names']])
            self.assertEqual(len(inputs), 126)
            self.assertTrue(all(len(row) == 49 for row in inputs))
            with (output / 'reference-probabilities.csv').open(newline='') as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(sum(r['record_kind'] == 'reserved_test_replay' for r in rows), 30)
            self.assertEqual(sum(r['record_kind'] == 'development_fitted_replay' for r in rows), 90)
            self.assertEqual(sum(r['record_kind'] == 'numerical_probe' for r in rows), 5)
            report = json.loads((bundle / 'report.json').read_text())
            for name in exporter.MODEL_NAMES:
                actual = [float(rows[i][f'{name}_probability']) for i in report['selected']['test']]
                np.testing.assert_allclose(actual, report['final_test'][name]['prediction'], rtol=0, atol=1e-12)
            with self.assertRaises(ValueError): exporter.export_bundle(bundle, output, trusted_local_bundle=True)


if __name__ == '__main__':
    unittest.main()
