"""Numeric/cluster fixtures only; no G1 bootstrap assessment during development."""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
from scipy.stats import bootstrap

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'examples'))
import breast_cancer_uncertainty as study


class UncertaintyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory()
        cls.output = Path(cls.temporary.name)/'fixture'
        study.run(cls.output)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_fixture_bundle_and_zero_fits(self):
        result = study.audit(self.output)
        self.assertEqual(result, dict(status='pass', cells=1, ranges=3,
            person_index_resamples=128, model_fits=0, conditional_only=True))
        report = json.loads((self.output/'report.json').read_text())
        self.assertFalse(report['full_procedure_uncertainty_estimated'])
        self.assertEqual(report['cells'][0]['people'], 4)
        self.assertEqual(report['cells'][0]['specimens'], 8)

    def test_known_person_losses(self):
        people, losses = study.person_losses(study.fixture_rows())
        np.testing.assert_array_equal(people, [0, 1, 2, 3])
        np.testing.assert_allclose(losses[:, 0], [0.01, 0.0169, 0.0256, 0.0361], atol=1e-15, rtol=0)
        np.testing.assert_allclose(losses[:, 1], 0.04, atol=1e-15, rtol=0)
        np.testing.assert_allclose(losses[:, 2], 0.26, atol=1e-15, rtol=0)
        np.testing.assert_allclose(losses[:, 3], 0.25, atol=1e-15, rtol=0)

    def test_exact_enumerated_draws_and_linear_endpoints(self):
        differences = np.array([[-0.2, -0.4, 0.0], [0.2, 0.4, 0.0]])
        indices = np.array(list(itertools.product(range(2), repeat=2)), dtype=np.int64)
        means = study.bootstrap_means(differences, indices)
        np.testing.assert_allclose(means[:, 0], [-0.2, 0.0, 0.0, 0.2], atol=1e-15, rtol=0)
        result = study.summarize(differences, means)
        self.assertAlmostEqual(result[0]['point'], 0)
        self.assertAlmostEqual(result[0]['lower'], -0.185)
        self.assertAlmostEqual(result[0]['upper'], 0.185)
        self.assertAlmostEqual(result[1]['upper'], 0.37)
        self.assertAlmostEqual(result[0]['analytic_empirical_bootstrap_sd'], np.sqrt(0.02))
        self.assertTrue(result[2]['constant_person_differences'])

    def test_scipy_paired_percentile_reference(self):
        losses = np.array([[0.02, 0.1, 0.1, 0.25], [0.2, 0.04, 0.3, 0.25],
            [0.05, 0.11, 0.08, 0.25], [0.1, 0.06, 0.15, 0.25], [0.08, 0.12, 0.05, 0.25]])
        differences = losses[:, 1:]-losses[:, [0]]
        indices = study.person_draws(5, 10000, [77, 0, 0])
        means = study.bootstrap_means(differences, indices)
        def statistic(grid, random, all_feature, prevalence, axis=-1):
            return np.array([np.mean(other-grid, axis=axis) for other in (random, all_feature, prevalence)])
        result = bootstrap(tuple(losses[:, i] for i in range(4)), statistic, paired=True,
            vectorized=True, n_resamples=10000, batch=10000, method='percentile',
            rng=np.random.Generator(np.random.PCG64(np.random.SeedSequence([77, 0, 0]))))
        np.testing.assert_allclose(means.T, result.bootstrap_distribution, atol=1e-15, rtol=0)
        summary = study.summarize(differences, means)
        np.testing.assert_allclose([x['lower'] for x in summary], result.confidence_interval.low, atol=1e-15, rtol=0)
        np.testing.assert_allclose([x['upper'] for x in summary], result.confidence_interval.high, atol=1e-15, rtol=0)

    def test_shared_person_draws_and_seed_replay(self):
        indices = study.person_draws(4, 128, [5, 0, 0])
        np.testing.assert_array_equal(indices, study.person_draws(4, 128, [5, 0, 0]))
        self.assertFalse(np.array_equal(indices, study.person_draws(4, 128, [5, 0, 1])))
        d = np.array([[-0.2, -0.4, 0], [-0.1, -0.2, 0], [0.1, 0.2, 0], [0.2, 0.4, 0]])
        means = study.bootstrap_means(d, indices)
        np.testing.assert_array_equal(means[:, 1], 2*means[:, 0])
        np.testing.assert_array_equal(means[:, 2], 0)

    def test_constant_contrasts_remain_explicit(self):
        differences = np.tile([0.125, -0.25, 0.0], (4, 1))
        result = study.summarize(differences, study.bootstrap_means(differences, study.person_draws(4, 128, [8])))
        for i, value in enumerate([0.125, -0.25, 0]):
            self.assertEqual(result[i]['lower'], value)
            self.assertEqual(result[i]['upper'], value)
            self.assertEqual(result[i]['empirical_resampling_sd'], 0)
            self.assertTrue(result[i]['constant_person_differences'])

    def test_malformed_pairs_and_denominators(self):
        variants = []
        rows = study.fixture_rows()
        variants.extend([rows[:-1], rows+rows[:1], [rows[1]]+rows[1:]])
        for field, value in (('label', 0), ('outer_fold', 2), ('person_id', 55),
                             ('specimen_id', rows[0]['specimen_id']), ('cohort_row', rows[0]['cohort_row'])):
            bad = copy.deepcopy(rows)
            bad[1][field] = value
            variants.append(bad)
        for bad in variants:
            with self.subTest(bad=bad[0]), self.assertRaises(ValueError):
                study.validate_cells(bad, ['fixture'], ['reference'], 4)

    def test_invalid_values_unknown_cells_and_missing_fields(self):
        for field, value in (('random_probability', float('nan')), ('random_probability', float('inf')),
            ('random_probability', -0.1), ('random_probability', 1.1), ('random_probability', '0.5'),
            ('random_probability', True), ('label', 1.0), ('person_id', True), ('specimen_id', ''),
            ('scenario', 'unknown'), ('cohort_id', 'unknown'), ('outer_fold', 0)):
            rows = study.fixture_rows()
            rows[0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                study.validate_cells(rows, ['fixture'], ['reference'], 4)
        rows = study.fixture_rows()
        del rows[0]['grid_probability']
        with self.assertRaises(ValueError): study.validate_cells(rows, ['fixture'], ['reference'], 4)
        with self.assertRaises(ValueError): study.validate_cells(study.fixture_rows(), ['fixture'], ['reference', 'missing'], 4)

    def test_order_invariance_and_cross_scenario_identity(self):
        rows = study.fixture_rows()
        ordered = study.validate_cells(rows, ['fixture'], ['reference'], 4)
        reverse = study.validate_cells(list(reversed(rows)), ['fixture'], ['reference'], 4)
        np.testing.assert_array_equal(study.person_losses(ordered['fixture', 'reference'])[1],
                                     study.person_losses(reverse['fixture', 'reference'])[1])
        other = [dict(r, scenario='stress') for r in rows]
        other[0]['specimen_id'] = 'changed'
        with self.assertRaises(ValueError): study.validate_cells(rows+other, ['fixture'], ['reference', 'stress'], 4)

    def test_invalid_bootstrap_coordinates(self):
        d = np.zeros((4, 3))
        for indices in (np.zeros((2, 3), dtype=int), np.zeros((2, 4)),
                        np.full((2, 4), 4), np.full((2, 4), -1), np.zeros((1, 4), dtype=int)):
            with self.assertRaises(ValueError): study.bootstrap_means(d, indices)
        for bad in (np.zeros((1, 3)), np.zeros((4, 2)), np.full((4, 3), np.nan), np.full((4, 3), 1.1)):
            with self.assertRaises(ValueError): study.bootstrap_means(bad, np.zeros((2, 4), dtype=int))
        with self.assertRaises(ValueError): study.person_draws(True, 128, [4])

    def test_failed_execution_and_timeout_are_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            for label, kwargs in (('failed', {}), ('timeout', {'max_seconds': 1e-12})):
                output = Path(folder)/label
                if label == 'failed':
                    with mock.patch.object(study, 'bootstrap_means', side_effect=ValueError('deliberate fixture failure')):
                        with self.assertRaises(ValueError): study.run(output)
                else:
                    with self.assertRaises(TimeoutError): study.run(output, **kwargs)
                self.assertEqual(json.loads((output/'report.json').read_text())['status'], 'software_fail')
                self.assertTrue((output/'sha256.json').exists())
                with self.assertRaises(ValueError): study.audit(output)

    def test_output_and_manifest_guards(self):
        for output in (self.output, study.ROOT/'forbidden-uncertainty'):
            with self.assertRaises(ValueError): study.output_path(output)
        with tempfile.TemporaryDirectory() as folder:
            link = Path(folder)/'link'
            link.symlink_to(Path(folder)/'missing')
            with self.assertRaises(ValueError): study.output_path(link)
        p = self.output/'report.json'
        raw = p.read_bytes()
        try:
            p.write_bytes(raw+b' ')
            with self.assertRaises(ValueError): study.audit(self.output)
        finally:
            p.write_bytes(raw)

    def test_semantic_audit_after_rehash_rejects_corruption(self):
        p = self.output/'report.json'
        original = p.read_bytes()
        manifest_path = self.output/'sha256.json'
        original_manifest = manifest_path.read_bytes()
        try:
            for field, value in (('model_fits', 1), ('completed_ranges', 4), ('conditional_only', False), ('mode', 'other')):
                report = json.loads(original)
                report[field] = value
                p.write_text(json.dumps(report))
                manifest = json.loads(original_manifest)
                manifest['report.json'] = hashlib.sha256(p.read_bytes()).hexdigest()
                manifest_path.write_text(json.dumps(manifest))
                with self.subTest(field=field), self.assertRaises(ValueError): study.audit(self.output)
            report = json.loads(original)
            report['cells'][0]['seed_parts'][0] += 1
            p.write_text(json.dumps(report))
            manifest['report.json'] = hashlib.sha256(p.read_bytes()).hexdigest()
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaises(ValueError): study.audit(self.output)
        finally:
            p.write_bytes(original)
            manifest_path.write_bytes(original_manifest)


if __name__ == '__main__':
    unittest.main()
