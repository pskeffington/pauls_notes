"""Independent arithmetic regression and negative-case checks for CO-05."""
import importlib.util
import math
from pathlib import Path
import unittest

SOURCE = Path(__file__).resolve().parents[1] / "oncology/examples/oncology_math.py"
SPEC = importlib.util.spec_from_file_location("oncology_math", SOURCE)
lab = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)


class OncologyMathTests(unittest.TestCase):
    def test_exact_teaching_expectations(self):
        expected = {
            "population_incidence_per_100k": 30,
            "implied_incident_events": 24,
            "person_time_rate_per_1000_py": 20,
            "group_a_response_proportion": 0.3,
            "group_b_response_proportion": 0.2,
            "response_percentage_point_difference": 10,
            "response_ratio": 1.5,
            "lesion_length_mm": 25,
            "analyte_pg_ml": 800,
            "expression_log2_fold_change": 2,
            "abstract_doubled_quantity": 400,
            "standard_score": 1.5,
        }
        self.assertEqual(set(lab.fixture_summary()), set(expected))
        for key, value in expected.items():
            with self.subTest(key=key):
                self.assertAlmostEqual(lab.fixture_summary()[key], value, places=11)

    def test_reverse_algebra(self):
        observed = lab.incidence_per_100k(24, 80_000)
        self.assertAlmostEqual(lab.implied_events(observed, 80_000), 24)
        self.assertAlmostEqual(lab.incidence_per_100k(18, 40_000), 45)

    def test_proportion_semantics(self):
        self.assertEqual(lab.proportion(0, 5), 0.0)
        self.assertEqual(lab.proportion(5, 5), 1.0)
        # A population case count may exceed people if multiple primaries are counted.
        self.assertEqual(lab.incidence_per_100k(3, 2), 150_000.0)

    def test_logarithmic_reversal_and_extreme_finite_inputs(self):
        self.assertAlmostEqual(lab.log2_fold_change(80, 20), 2)
        self.assertAlmostEqual(lab.log2_fold_change(20, 80), -2)
        self.assertAlmostEqual(lab.log2_fold_change(48, 12), 2)
        self.assertAlmostEqual(
            lab.log2_fold_change(1e300, 1e-300),
            math.log2(1e300) - math.log2(1e-300)
        )

    def test_negative_cases(self):
        invalid = [
            (lab.proportion, (1, 0)),
            (lab.proportion, (3, 2)),
            (lab.proportion, (-1, 10)),
            (lab.proportion, (2.5, 10)),
            (lab.proportion, (True, 3)),
            (lab.incidence_per_100k, (-1, 100_000)),
            (lab.incidence_per_100k, (1, 0)),
            (lab.incidence_per_100k, (1, math.nan)),
            (lab.incidence_per_100k, (1, math.inf)),
            (lab.person_time_rate_per_1000, (2, 0)),
            (lab.person_time_rate_per_1000, (2, -4)),
            (lab.implied_events, (-1, 100)),
            (lab.absolute_proportion_difference, (-0.1, 0.5)),
            (lab.ratio_of_proportions, (0.2, 0)),
            (lab.ratio_of_proportions, (0.2, 1.2)),
            (lab.cm_to_mm, (-1,)),
            (lab.ng_ml_to_pg_ml, (-0.1,)),
            (lab.log2_fold_change, (0, 20)),
            (lab.log2_fold_change, (20, -5)),
            (lab.idealized_doubling, (100, 60, 0)),
            (lab.idealized_doubling, (100, -1, 30)),
            (lab.idealized_doubling, (100, 1e6, 0.01)),
            (lab.z_score, (50, 60, 0)),
        ]
        for function, args in invalid:
            with self.subTest(function=function.__name__, args=args):
                with self.assertRaises(ValueError):
                    function(*args)


if __name__ == "__main__":
    unittest.main()
