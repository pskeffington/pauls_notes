"""Regression tests for author-neutral biomedical chapter and workbook gates."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "biostat_alignment", ROOT / "scripts/check_biostat_8e_alignment.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class WorkbookMarkupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workbook_path = ROOT / (
            "02_biomedical_coding/examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd"
        )
        cls.original = cls.workbook_path.read_text(encoding="utf-8")

    def test_real_workbook_has_17_named_chunks(self):
        labels = MODULE.validate_workbook_markup(self.original)
        self.assertEqual(len(labels), 17)
        self.assertIn("paired-and-repeated", labels)

    def test_unsafe_hyphenated_column_rejected(self):
        unsafe = self.original.replace(
            'wide[["score.Follow-up"]]', "wide$score.Follow-up", 1
        )
        with self.assertRaisesRegex(ValueError, "Unsafe hyphenated"):
            MODULE.validate_workbook_markup(unsafe)

    def test_duplicate_labels_rejected(self):
        broken = self.original.replace(
            "```{r paired-and-repeated}", "```{r validation}", 1
        )
        with self.assertRaisesRegex(ValueError, "17 unique"):
            MODULE.validate_workbook_markup(broken)

    def test_unclosed_fence_rejected(self):
        broken = self.original + "```{r unexpected}\n"
        with self.assertRaises(ValueError):
            MODULE.validate_workbook_markup(broken)

    def test_missing_exact_pair_column_rejected(self):
        broken = self.original.replace(
            'wide[["score.Baseline"]]', "baseline_vector"
        )
        with self.assertRaisesRegex(ValueError, "exact column key"):
            MODULE.validate_workbook_markup(broken)


if __name__ == "__main__":
    unittest.main()
