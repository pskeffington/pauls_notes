"""Independent checks of figure calculations and clustered calibration behavior."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

import numpy as np

EXAMPLES = Path(__file__).resolve().parents[1] / 'examples'
sys.path.insert(0, str(EXAMPLES))
import gallery_diagnostics as diagnostics
import plot_comparison as plots

SNAPSHOT = EXAMPLES.parent / 'gallery/example'


class DiagnosticTests(unittest.TestCase):
    def test_saved_feature_counts_and_missingness_match_snapshot(self):
        report, rows, _ = plots.load_results(SNAPSHOT)
        saved = diagnostics.load_display_inputs(SNAPSHOT, report, rows)
        derived = json.loads((SNAPSHOT / 'plot-data.json').read_text())['calculations']
        self.assertEqual(derived['missingness']['total'],
                         sum(sum(s['missing']) for s in saved['specimens']))
        self.assertEqual(derived['missingness']['cells'], 120 * 48)
        self.assertEqual(set(derived['missingness']['cohort_row_order']), set(range(120)))
        selected = report['selected']
        expected = [sum(n in fold['selected_features'] for fold in selected['outer'])
                    for n in saved['feature_names']]
        self.assertEqual(derived['outer_selection_counts'], expected)
        for _, candidates, best in diagnostics.candidate_searches(report):
            chosen = [c for c in candidates if c['chosen']]
            self.assertEqual(len(chosen), 1)
            self.assertEqual(chosen[0]['parameters'], best)
            self.assertAlmostEqual(chosen[0]['mean_brier'], min(np.mean(c['fold_brier']) for c in candidates))

    def test_rejects_corrupt_masks_identity_coefficients_and_feature_counts(self):
        report, rows, _ = plots.load_results(SNAPSHOT)
        original = json.loads((SNAPSHOT / 'display-inputs.json').read_text())
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'display-inputs.json'
            for field in ('mask', 'identity', 'duplicate', 'coefficient', 'count'):
                changed = copy.deepcopy(original)
                if field == 'mask': changed['specimens'][0]['missing'][0] = 1
                if field == 'identity': changed['specimens'][0]['person_id'] = 9999
                if field == 'duplicate': changed['specimens'][-1] = changed['specimens'][0]
                if field == 'coefficient': changed['feature_review'][0]['all_feature_standardized_coefficient'] = float('nan')
                if field == 'count': changed['feature_review'][0]['selected_outer_fits'] = 99
                path.write_text(json.dumps(changed))
                with self.subTest(field=field), self.assertRaises(ValueError):
                    diagnostics.load_display_inputs(folder, report, rows)

    def test_rejects_tampered_search_and_person_leakage(self):
        report, rows, _ = plots.load_results(SNAPSHOT)
        for field in ('score', 'winner', 'rank', 'grid', 'split'):
            changed = copy.deepcopy(report)
            fold = changed['selected']['outer'][0]
            if field == 'score': fold['search_candidates'][0]['mean_brier'] = .999
            if field == 'winner': fold['search_candidates'][0]['chosen'] = True
            if field == 'rank': fold['search_candidates'][0]['rank'] = 99
            if field == 'grid': fold['search_candidates'].pop()
            if field == 'split': fold['inner'][0]['analysis'][0] = fold['inner'][0]['assessment'][0]
            with self.subTest(field=field), self.assertRaises(ValueError):
                diagnostics.load_display_inputs(SNAPSHOT, changed, rows)

    @staticmethod
    def fixture(probabilities):
        return [dict(cohort_row=2 * i + j, person_id=i, label=j, partition='test',
                     selected_probability=p) for i, pair in enumerate(probabilities) for j, p in enumerate(pair)]

    def test_person_bootstrap_agrees_with_direct_whole_pair_resampling(self):
        rows = self.fixture([[.45, .45], [.45, .9], [.1, .45], [.9, .9]])
        summaries = diagnostics.calibration_summary(rows, 'test', 'selected',
                                                    replicates=500, seed=47, min_people=1)
        # Independent oracle: expand actual pairs rather than summing grouped counts.
        observed = []
        for draw in np.random.default_rng(47).integers(0, 4, size=(500, 4)):
            sample = [rows[2 * person + j] for person in draw for j in range(2)]
            bin_rows = [r for r in sample if .4 <= r['selected_probability'] < .6]
            if bin_rows:
                observed.append(np.mean([r['label'] for r in bin_rows]))
        result = summaries[2]
        self.assertEqual((result['specimens'], result['people'], result['positives']), (4, 3, 2))
        self.assertEqual(result['valid_replicates'], len(observed))
        np.testing.assert_allclose([result['lower'], result['upper']], np.quantile(observed, [.025, .975]))

    def test_intact_balanced_pairs_have_degenerate_not_false_precision_interval(self):
        rows = self.fixture([[.5, .5]] * 12)
        result = diagnostics.calibration_summary(rows, 'test', 'selected')[2]
        self.assertEqual(result['observed_fraction'], .5)
        self.assertEqual(result['interval_status'], 'degenerate')
        self.assertIsNone(result['lower'])
        self.assertIsNone(result['upper'])
        self.assertEqual(result['valid_replicates'], 2000)

    def test_fixed_endpoints_counts_sparse_empty_and_one_label_bins(self):
        rows = self.fixture([[p, p] for p in [0, .2, .4, .6, .8, 1]])
        bins = diagnostics.calibration_summary(rows, 'test', 'selected')
        self.assertEqual([b['specimens'] for b in bins], [2, 2, 2, 2, 4])
        self.assertEqual([b['people'] for b in bins], [1, 1, 1, 1, 2])
        self.assertTrue(all(b['interval_status'] == 'sparse' and b['lower'] is None for b in bins))
        rows = self.fixture([[.1, .9]] * 12)
        bins = diagnostics.calibration_summary(rows, 'test', 'selected')
        self.assertEqual([b['interval_status'] for b in bins], ['one_label', 'empty', 'empty', 'empty', 'one_label'])
        self.assertEqual(sum(b['specimens'] for b in bins), 24)
        self.assertEqual(sum(b['people'] for b in bins), 24)  # People can appear in multiple bins.
        self.assertTrue(all(b['lower'] is None and b['upper'] is None for b in bins))


if __name__ == '__main__':
    unittest.main()
