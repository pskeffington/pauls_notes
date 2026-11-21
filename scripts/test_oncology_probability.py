"""Reproducibility, probability identities, and invalid inputs for CO-07."""
import importlib.util
import math
import unittest
from fractions import Fraction
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "oncology/examples/oncology_probability.py"
SPEC = importlib.util.spec_from_file_location("oncology_probability", PATH)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class ProbabilityTests(unittest.TestCase):
    def test_exact_rational_reference_cases(self):
        """Independent fractions establish both tables without binary rounding."""
        size, se, sp = 10000, Fraction(9, 10), Fraction(19, 20)
        for prevalence, cells, ppv, npv in [
            (Fraction(1, 100), (90, 495, 10, 9405), Fraction(2, 13), Fraction(1881, 1883)),
            (Fraction(1, 20), (450, 475, 50, 9025), Fraction(18, 37), Fraction(361, 363)),
        ]:
            with self.subTest(prevalence=prevalence):
                expected = (size * prevalence * se, size * (1 - prevalence) * (1 - sp),
                            size * prevalence * (1 - se), size * (1 - prevalence) * sp)
                self.assertEqual(expected, cells)
                self.assertEqual(expected[0] / (expected[0] + expected[1]), ppv)
                self.assertEqual(expected[3] / (expected[3] + expected[2]), npv)
                calculated = mod.expected_screening_counts(size, prevalence, se, sp)
                for result, reference in zip(calculated.values(), expected):
                    self.assertTrue(math.isclose(result, float(reference), rel_tol=1e-12))
                table = mod.probabilities_from_table(*cells)
                self.assertAlmostEqual(table["ppv"], float(ppv))
                self.assertAlmostEqual(table["npv"], float(npv))
        self.assertEqual(Fraction(8, 80) / Fraction(20, 80), Fraction(2, 5))
        self.assertEqual(Fraction(8, 80) / Fraction(16, 80), Fraction(1, 2))
        self.assertEqual(Fraction(20 + 16 - 8, 80), Fraction(7, 20))

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

    def test_valid_probability_boundaries(self):
        # Decimal input at the lower intersection bound previously failed.
        self.assertEqual(mod.union(.7, .4, .1), 1.0)
        self.assertEqual(mod.union(0, 1, 0), 1.0)
        self.assertEqual(mod.union(0, 0, 0), 0.0)
        perfect = mod.screening_probabilities(.1, 1, 1)
        self.assertEqual((perfect["ppv"], perfect["npv"]), (1, 1))
        absent = mod.screening_probabilities(0, .9, .95)
        self.assertEqual((absent["ppv"], absent["npv"]), (0, 1))
        self.assertEqual(mod.probabilities_from_table(1, 0, 0, 1),
                         {"sensitivity": 1, "specificity": 1, "ppv": 1, "npv": 1})
        self.assertEqual(mod.simulate_screening(10, 0, .9, 1),
                         {"tp": 0, "fp": 0, "fn": 0, "tn": 10})

    def test_fractional_expectations_preserve_precision(self):
        counts = mod.expected_screening_counts(1, 1e-15, .5, .5)
        # Internal decimal rounding previously converted these positive cells to zero.
        self.assertGreater(counts["expected_true_positive"], 0)
        self.assertTrue(math.isclose(counts["expected_true_positive"], 5e-16, rel_tol=1e-12))
        self.assertTrue(math.isclose(counts["expected_false_negative"], 5e-16, rel_tol=1e-12))

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
            (mod.union, (.7, .4, .099999), {}),
            (mod.screening_probabilities, (0, 1, 1), {}),
            (mod.screening_probabilities, (1, 1, 0), {}),
            (mod.expected_screening_counts, (0, .01, .9, .95), {}),
            (mod.expected_screening_counts, (2.5, .01, .9, .95), {}),
            (mod.probabilities_from_table, (0, 0, 0, 0), {}),
            (mod.probabilities_from_table, (1, -1, 2, 3), {}),
            (mod.probabilities_from_table, (1.5, 2, 3, 4), {}),
            (mod.probabilities_from_table, (True, 2, 3, 4), {}),
            (mod.probabilities_from_table, ([1, 2], 2, 3, 4), {}),
            (mod.probabilities_from_table, (math.nan, 2, 3, 4), {}),
            (mod.probabilities_from_table, (math.inf, 2, 3, 4), {}),
            (mod.simulate_screening, (10, .1, .9, .9), {"seed": True}),
        ]
        for f, a, kw in invalid:
            with self.subTest(f=f.__name__, args=a):
                with self.assertRaises(ValueError):
                    f(*a, **kw)


if __name__ == "__main__":
    unittest.main()
