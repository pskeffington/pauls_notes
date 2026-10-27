"""Reproducibility, probability identities, and invalid inputs for CO-07."""
import importlib.util
import math
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "oncology/examples/oncology_probability.py"
SPEC = importlib.util.spec_from_file_location("oncology_probability", PATH)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class ProbabilityTests(unittest.TestCase):
    def test_expected_low_prevalence(self):
        p = mod.screening_probabilities(.01, .9, .95)
        self.assertAlmostEqual(p["p_test_positive"], .0585)
        self.assertAlmostEqual(p["ppv"], 90 / 585)
        self.assertAlmostEqual(p["npv"], 9405 / 9415)
        counts = mod.expected_screening_counts(10000, .01, .9, .95)
        for k, n in {"expected_true_positive": 90, "expected_false_positive": 495,
                     "expected_false_negative": 10, "expected_true_negative": 9405}.items():
            self.assertAlmostEqual(counts[k], n)
        self.assertAlmostEqual(sum(counts.values()), 10000)

    def test_base_rate_shift_not_assay_shift(self):
        low = mod.screening_probabilities(.01, .9, .95)
        high = mod.screening_probabilities(.05, .9, .95)
        self.assertAlmostEqual(high["ppv"], 450 / 925)
        self.assertGreater(high["ppv"], low["ppv"])
        self.assertLess(high["npv"], low["npv"])

    def test_table_reconstruction(self):
        r = mod.probabilities_from_table(90, 495, 10, 9405)
        self.assertAlmostEqual(r["sensitivity"], .9)
        self.assertAlmostEqual(r["specificity"], .95)
        self.assertAlmostEqual(r["ppv"], 90 / 585)
        self.assertAlmostEqual(r["npv"], 9405 / 9415)
        self.assertAlmostEqual(mod.conditional(.1, .25), .4)
        self.assertAlmostEqual(mod.conditional(.1, .2), .5)
        self.assertAlmostEqual(mod.union(.2, .25, .1), .35)
        self.assertAlmostEqual(mod.union(.4, .3, .12), .58)

    def test_stochastic_replay_and_meaningful_variability(self):
        a = mod.simulate_screening(10000, .01, .9, .95, seed=711)
        self.assertEqual(a, mod.simulate_screening(10000, .01, .9, .95, seed=711))
        self.assertEqual(sum(a.values()), 10000)
        b = mod.simulate_screening(10000, .01, .9, .95, seed=712)
        self.assertNotEqual(a, b)
        self.assertTrue(0 < a["tp"] < 200)
        self.assertTrue(350 < a["fp"] < 700)

    def test_boundary_and_invalid_inputs(self):
        invalid = [
            (mod.probability, (True, "bad"), {}),
            (mod.probability, (math.nan, "bad"), {}),
            (mod.probability, (math.inf, "bad"), {}),
            (mod.probability, (-.1, "bad"), {}),
            (mod.probability, (1.1, "bad"), {}),
            (mod.conditional, (.2, 0), {}),
            (mod.conditional, (.6, .4), {}),
            (mod.union, (.2, .2, .3), {}),
            (mod.union, (.8, .8, .1), {}),
            (mod.screening_probabilities, (0, 1, 1), {}),
            (mod.screening_probabilities, (1, 1, 0), {}),
            (mod.expected_screening_counts, (0, .01, .9, .95), {}),
            (mod.expected_screening_counts, (2.5, .01, .9, .95), {}),
            (mod.probabilities_from_table, (0, 0, 0, 0), {}),
            (mod.probabilities_from_table, (1, -1, 2, 3), {}),
            (mod.probabilities_from_table, (1.5, 2, 3, 4), {}),
            (mod.simulate_screening, (10, .1, .9, .9), {"seed": True}),
        ]
        for f, a, kw in invalid:
            with self.subTest(f=f.__name__, args=a):
                with self.assertRaises(ValueError):
                    f(*a, **kw)


if __name__ == "__main__":
    unittest.main()
