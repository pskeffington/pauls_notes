"""Software-only gates for the prespecified synthetic assay robustness experiment."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest
from unittest import mock

import numpy as np

EXAMPLES = Path(__file__).resolve().parents[1] / 'examples'
sys.path.insert(0, str(EXAMPLES))
import breast_cancer_feature_selection as selection  # noqa: E402
import breast_cancer_robustness as study  # noqa: E402


class TestStudy(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.folder = tempfile.TemporaryDirectory()
        cls.out = Path(cls.folder.name) / 'bounded-study'
        study.run(cls.out, scenarios=('reference',), max_fits=study.FITS_PER_SCENARIO,
                  max_seconds=120)
        cls.report = json.loads((cls.out / 'report.json').read_text())
        with (cls.out / 'development_predictions.csv').open(newline='') as stream:
            cls.rows = list(csv.DictReader(stream))
        cls.scenario = cls.report['scenario_results']['reference']

    @classmethod
    def tearDownClass(cls):
        cls.folder.cleanup()

    def test_budget_outputs_integrity_and_no_test_predictions(self):
        self.assertEqual(self.report['protocol_id'], 'paired-assay-robustness-v1')
        self.assertEqual(self.report['status'], 'software_pass')
        self.assertEqual(self.report['budget']['actual_fits'], study.FITS_PER_SCENARIO)
        self.assertEqual(self.scenario['fit_budget']['failed'], 0)
        self.assertFalse(self.report['selection_contract']['test_predictions_generated'])
        self.assertFalse(self.report['selection_contract']['test_used_for_selection'])
        self.assertEqual(len(self.rows), 90)
        self.assertEqual({r['scenario'] for r in self.rows}, {'reference'})
        self.assertEqual(len({r['person_id'] for r in self.rows}), 45)
        self.assertEqual(len({r['specimen_id'] for r in self.rows}), 90)
        self.assertFalse(set(map(int, (r['cohort_row'] for r in self.rows))) &
                         set(self.scenario['reserved']))
        manifest = json.loads((self.out / 'sha256.json').read_text())
        for filename, expected in manifest.items():
            self.assertEqual(hashlib.sha256((self.out / filename).read_bytes()).hexdigest(),
                             expected)
        for name, digest in self.report['source_sha256'].items():
            self.assertEqual(hashlib.sha256((study.ROOT / name).read_bytes()).hexdigest(),
                             digest)

    def test_partition_integrity_and_full_candidate_histories(self):
        data, development, reserved, _ = study.make_scenario('reference')
        selection.check_partition(development, reserved, data['person_id'])
        seen = []
        for fold in self.scenario['outer']:
            selection.check_partition(fold['analysis'], fold['assessment'],
                                      data['person_id'], development)
            seen.extend(fold['assessment'])
        self.assertEqual(sorted(seen), sorted(development.tolist()))
        for method in ('grid', 'random'):
            self.assertEqual(len(self.scenario['searches'][method]), 4)
            for i, search in enumerate(self.scenario['searches'][method]):
                self.assertEqual(len(search['candidates']), 6)
                self.assertEqual(search['attempted_fits'], 19)
                self.assertEqual(search['failed_fits'], 0)
                self.assertEqual(len(search['inner']), 3)
                parent = self.scenario['outer'][i]['analysis'] if i < 3 else development
                for inner in search['inner']:
                    selection.check_partition(inner['analysis'], inner['assessment'],
                                              data['person_id'], parent)
                winning = [t for t in search['candidates'] if t['chosen']]
                self.assertEqual(len(winning), 1)
                self.assertAlmostEqual(winning[0]['mean_inner_brier'],
                    min(t['mean_inner_brier'] for t in search['candidates']))
                for candidate in search['candidates']:
                    self.assertEqual(len(candidate['inner_trials']), 3)
                    self.assertTrue(all(t['error'] is None and 0 <= t['brier'] <= 1
                                        for t in candidate['inner_trials']))
                self.assertEqual(len(search['selected_features']),
                                 search['chosen_parameters']['select__k'])
            self.assertEqual(len(self.scenario['stability'][method]['pairwise_jaccard']), 3)

    def test_predictions_match_person_level_and_specimen_level_losses(self):
        p = {m: np.array([float(r[f'{m}_probability']) for r in self.rows])
             for m in ('grid', 'random', 'all_feature', 'prevalence')}
        y = np.array([int(r['label']) for r in self.rows])
        for name, values in p.items():
            self.assertTrue(np.isfinite(values).all())
            self.assertTrue(((values >= 0) & (values <= 1)).all())
            self.assertAlmostEqual(float(np.mean((values - y) ** 2)),
                                   self.scenario['development_metrics'][name]['brier'])
        paired = []
        for person in sorted({int(r['person_id']) for r in self.rows}):
            ix = [i for i, r in enumerate(self.rows) if int(r['person_id']) == person]
            self.assertEqual(len(ix), 2)
            paired.append(float(np.mean((p['grid'][ix] - y[ix]) ** 2 -
                                        (p['random'][ix] - y[ix]) ** 2)))
        self.assertAlmostEqual(float(np.mean(paired)),
                               -self.scenario['comparison_vs_grid_brier']['random'])
        np.testing.assert_allclose(paired, self.scenario['grid_minus_random_person_brier'])

    def test_scenarios_preserve_reserved_measurements_and_pair_contracts(self):
        base = selection.make_cohort(seed=study.COHORT_SEED)
        for name in study.SCENARIOS:
            data, development, reserved, config = study.make_scenario(name)
            selection.validate_cohort(data)
            selection.check_partition(development, reserved, data['person_id'])
            np.testing.assert_allclose(data['x'][reserved], base['x'][reserved], equal_nan=True)
            self.assertEqual(config['development_people'], 45)
            self.assertEqual(config['reserved_people'], 15)
            if name == 'extra_missingness':
                self.assertGreater(config['final_development_missing_fraction'],
                                   config['initial_development_missing_fraction'] + 0.08)
            if name == 'correlated_measurement':
                before = base['x'][development, :]
                after = data['x'][development, :]
                self.assertTrue(np.array_equal(before[:, 0], after[:, 0], equal_nan=True))
                self.assertFalse(np.array_equal(before[:, 4], after[:, 4], equal_nan=True))
            if name == 'reallocated_people':
                self.assertNotEqual(set(development), set(self.scenario['development']))

    def test_reserved_value_perturbation_cannot_change_training(self):
        base_report, base_predictions = study.evaluate_scenario('reference',
                                                                 time.monotonic() + 120)
        data, development, reserved, config = study.make_scenario('reference')
        changed = {k: v.copy() for k, v in data.items()}
        changed['x'][reserved] = 100000.0
        changed['y'][reserved] = 1 - changed['y'][reserved]
        with mock.patch.object(study, 'make_scenario', return_value=(changed, development,
                                                                     reserved, config)):
            other_report, other_predictions = study.evaluate_scenario('reference',
                                                                       time.monotonic() + 120)
        self.assertEqual(base_predictions, other_predictions)
        self.assertEqual(base_report['final_panels'], other_report['final_panels'])
        self.assertEqual(base_report['development_metrics'],
                         other_report['development_metrics'])
        for method in ('grid', 'random'):
            self.assertEqual([trial['chosen_parameters'] for trial in base_report['searches'][method]],
                             [trial['chosen_parameters'] for trial in other_report['searches'][method]])

    def test_failed_candidates_are_visible_and_not_selected(self):
        data, development, _, _ = study.make_scenario('reference')
        _, trial = study.search_on_rows(data, development, 'grid',
                    deadline=time.monotonic() + 120, candidates=((-1, 1.0), (5, 0.1)))
        self.assertEqual(trial['failed_fits'], 3)
        self.assertEqual(trial['attempted_fits'], 7)
        self.assertEqual(trial['candidates'][0]['status'], 'failed')
        self.assertTrue(all(x['error'] for x in trial['candidates'][0]['inner_trials']))
        self.assertTrue(trial['candidates'][1]['chosen'])
        self.assertEqual(trial['chosen_parameters'], {'select__k': 5, 'model__C': 0.1})

    def test_output_and_budget_safeguards(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            bad_link = root / 'link'
            bad_link.symlink_to(root / 'missing')
            for bad in (self.out, bad_link, study.ROOT / 'forbidden-study-output'):
                with self.assertRaises(ValueError):
                    study.run(bad, scenarios=('reference',), max_fits=156)
            with self.assertRaises(ValueError):
                study.run(root / 'too-small', scenarios=('reference',), max_fits=155)
            with self.assertRaises(ValueError):
                study.run(root / 'duplicate', scenarios=('reference', 'reference'))


if __name__ == '__main__':
    unittest.main()
