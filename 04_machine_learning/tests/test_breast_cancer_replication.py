"""Legacy-only smoke, numeric fixtures and hostile inputs; never draws G1 cohorts."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest import mock
import warnings

import numpy as np
from sklearn.exceptions import ConvergenceWarning

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'examples'))
import breast_cancer_replication as study


class ReplicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temporary.name) / 'smoke'
        study.run(cls.output)
        cls.report = json.loads((cls.output / 'report.json').read_text())
        cls.predictions = json.loads((cls.output / 'predictions.json').read_text())
        cls.fits = json.loads((cls.output / 'fits.json').read_text())

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_budget_hashes_and_smoke_boundary(self):
        self.assertEqual(study.audit_bundle(self.output)['fits'], 156)
        self.assertEqual(len(self.predictions), 90)
        self.assertEqual({p['cohort_id'] for p in self.predictions}, {'legacy'})
        self.assertEqual(self.report['failed_fits'], 0)
        self.assertEqual(self.report['protocol_freeze_commit'], study.FREEZE)
        for method, expected in (('grid', 76), ('random', 76), ('all_feature', 4)):
            self.assertEqual(sum(r['method'] == method for r in self.fits), expected)

    def test_legacy_prediction_compatibility(self):
        report, original = study.legacy.evaluate_scenario('reference', time.monotonic()+120)
        actual = sorted(self.predictions, key=lambda r: r['cohort_row'])
        original = sorted(original, key=lambda r: r['cohort_row'])
        for method in study.METHODS:
            np.testing.assert_allclose([r[f'{method}_probability'] for r in actual],
                [r[f'{method}_probability'] for r in original], atol=1e-12, rtol=0)
        self.assertEqual([x['chosen_parameters'] for x in report['searches']['grid']],
            [x['chosen_parameters'] for x in self.report['cells'][0]['searches'] if x['method'] == 'grid'])

    def test_reserved_value_invariance(self):
        data, development, reserved, config = study.legacy.make_scenario('reference')
        changed = {k: v.copy() for k, v in data.items()}
        changed['x'][reserved] = 1e9
        changed['y'][reserved] = 1-changed['y'][reserved]
        with tempfile.TemporaryDirectory() as folder:
            with mock.patch.object(study.legacy, 'make_scenario', return_value=(changed, development, reserved, config)):
                output = study.run(Path(folder)/'perturbed')
            self.assertEqual(self.predictions, json.loads((output/'predictions.json').read_text()))

    def test_person_loss_numeric_fixture_and_broken_pairs(self):
        pair = [dict(person_id=1, specimen_id=str(i), label=i, outer_fold=1,
            **{f'{m}_probability': float(i) if m == 'grid' else 0.5 for m in study.METHODS}) for i in (0, 1)]
        losses = study.person_losses(pair)
        self.assertEqual(losses[0]['losses']['grid'], 0)
        self.assertEqual(losses[0]['other_minus_grid']['random'], 0.25)
        for broken in (pair[:1], pair+pair, [pair[0], dict(pair[1], outer_fold=2)],
                       [pair[0], dict(pair[1], label=0)]):
            with self.assertRaises(ValueError):
                study.person_losses(broken)

    def test_rank_ties_and_undefined_scores(self):
        data, development, _, _ = study.legacy.make_scenario('reference')
        model = study.legacy.make_pipeline(5, 0.1).fit(data['x'][development], data['y'][development])
        values = np.arange(48, dtype=float)
        values[:3] = [50, 50, np.nan]
        with mock.patch.object(study, 'f_classif', return_value=(values, values)):
            details = study.feature_details(model, data['x'][development], data['y'][development])
        self.assertEqual(details['ranks']['Feature001'], 1.5)
        self.assertEqual(details['ranks']['Feature002'], 1.5)
        self.assertIsNone(details['ranks']['Feature003'])
        self.assertIn('Feature003', details['undefined_rank_reasons'])

    def test_stability_denominators_and_signs(self):
        result = study.stability(self.fits)['reference']['grid']
        self.assertEqual(len(result['outer_panel_pairs']), 3)
        for feature, info in result['features'].items():
            self.assertEqual(info['outer_fits'], 3)
            self.assertEqual(info['all_fits'], 76)
            self.assertEqual(sum(info['signs'][s] for s in ('negative', 'zero', 'positive')),
                             info['outer_selected'])
            self.assertEqual(info['ranks']['n'], 3)
        fixture = copy.deepcopy(self.fits[18])
        fixture.update(role='outer_refit', coefficients={'Feature001': -0.1}, selected_features=['Feature001'])
        second = copy.deepcopy(fixture)
        second.update(fit_id=999, coefficients={'Feature001': 0.0})
        info = study.stability([fixture, second])['reference']['grid']['features']
        self.assertEqual(info['Feature001']['signs'], dict(selected_denominator=2, negative=1, zero=1, positive=0))
        self.assertEqual(info['Feature002']['signs']['zero'], 0)

    def test_failed_trials_remain_visible(self):
        data, development, _, _ = study.legacy.make_scenario('reference')
        with tempfile.TemporaryDirectory() as folder:
            ledger = study.FitLedger(Path(folder), 156, time.monotonic()+120)
            history = {}
            study.search(data, development, 'grid', ledger,
                dict(cohort_id='legacy', scenario='reference', outer_fold=0), history,
                candidates=((-1, 0.1), (5, 0.1)))
            self.assertEqual(len(ledger.records), 7)
            self.assertEqual(sum(r['status'] == 'failed' for r in ledger.records), 3)
            self.assertEqual(history['candidates'][0]['status'], 'failed')
            self.assertTrue(history['candidates'][1]['chosen'])
            events = [json.loads(line) for line in (Path(folder)/'fit-events.jsonl').read_text().splitlines()]
            self.assertEqual(len(events), 14)
            self.assertTrue(all(r['error'] for r in ledger.records[:3]))

    def test_all_failed_refit_convergence_and_timeout_bundles(self):
        def converge(*args, **kwargs):
            warnings.warn('fixture did not converge', ConvergenceWarning)
        for name, target, effect in (
            ('all-failed', 'make_pipeline', ValueError('deliberate trial failure')),
            ('refit-failed', 'make_pipeline', None),
            ('convergence', 'make_pipeline', converge),
        ):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as folder:
                output = Path(folder)/'failed'
                original = study.legacy.make_pipeline
                calls = 0
                def fail_refit(*args, **kwargs):
                    nonlocal calls
                    calls += 1
                    if calls == 19:
                        raise RuntimeError('deliberate refit failure')
                    return original(*args, **kwargs)
                with mock.patch.object(study.legacy, target, side_effect=fail_refit if effect is None else effect):
                    with self.assertRaises(ValueError if effect is not None else RuntimeError):
                        study.run(output)
                report = json.loads((output/'report.json').read_text())
                self.assertEqual(report['status'], 'software_fail')
                fits = json.loads((output/'fits.json').read_text())
                self.assertGreater(report['failed_fits'], 0)
                self.assertTrue(any(r['error'] for r in fits))
                self.assertTrue((output/'sha256.json').exists())
                with self.assertRaises(ValueError):
                    study.audit_bundle(output)
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)/'timeout'
            with self.assertRaises(TimeoutError):
                study.run(output, max_seconds=1e-12)
            self.assertEqual(json.loads((output/'report.json').read_text())['status'], 'software_fail')

    def test_saved_structure_corruption_is_rejected(self):
        for kind in ('duplicate', 'probability', 'identity', 'fold', 'score', 'training'):
            report, predictions, fits = copy.deepcopy((self.report, self.predictions, self.fits))
            if kind == 'duplicate': predictions[0] = predictions[1].copy()
            if kind == 'probability': predictions[0]['grid_probability'] = float('nan')
            if kind == 'identity': predictions[0]['person_id'] = 999
            if kind == 'fold': predictions[0]['outer_fold'] = 0
            if kind == 'score': fits[0]['brier'] += 0.1
            if kind == 'training': fits[0]['analysis'][0] = report['cells'][0]['reserved'][0]
            with self.subTest(kind=kind), self.assertRaises(ValueError):
                study.audit(report, predictions, fits)

    def test_output_protection_and_manifest_tamper(self):
        with self.assertRaises(ValueError):
            study.run(self.output)
        with self.assertRaises(ValueError):
            study.run(study.ROOT/'forbidden-replication')
        with tempfile.TemporaryDirectory() as folder:
            symlink = Path(folder)/'link'
            symlink.symlink_to(Path(folder)/'missing')
            with self.assertRaises(ValueError): study.run(symlink)
            with self.assertRaises(ValueError): study.run(Path(folder)/'bad-time', max_seconds=-1)
        target = self.output/'predictions.json'
        saved = target.read_bytes()
        try:
            target.write_bytes(saved+b' ')
            with self.assertRaises(ValueError): study.audit_bundle(self.output)
        finally:
            target.write_bytes(saved)


if __name__ == '__main__':
    unittest.main()
