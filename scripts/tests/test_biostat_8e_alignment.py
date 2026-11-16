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
        cls.gallery = (ROOT / (
            "03_learning/bio_stats/GRAPH_METHODS_SYNTHETIC_GALLERY.Rmd"
        )).read_text(encoding="utf-8")

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
        # Keep the 17 chunk labels intact; remove one closing fence only.
        head, tail = self.original.rsplit("\n```\n", 1)
        broken = head + "\n[missing fence]\n" + tail
        with self.assertRaisesRegex(ValueError, "Unbalanced"):
            MODULE.validate_workbook_markup(broken)

    def test_missing_exact_pair_column_rejected(self):
        broken = self.original.replace(
            'wide[["score.Baseline"]]', "baseline_vector"
        )
        with self.assertRaisesRegex(ValueError, "exact column key"):
            MODULE.validate_workbook_markup(broken)


    def test_original_seven_figure_gallery(self):
        labels = MODULE.validate_graph_gallery(self.gallery)
        self.assertEqual(len(labels), 7)
        self.assertIn("graph-roc", labels)

    def test_gallery_omitted_roc_fails(self):
        broken = self.gallery.replace("biostat_graph_roc(", "untracked_plot(", 1)
        with self.assertRaisesRegex(ValueError, "missing method"):
            MODULE.validate_graph_gallery(broken)

    def test_gallery_missing_fence_fails(self):
        head, tail = self.gallery.rsplit("\n```\n", 1)
        broken = head + "\n[missing closing fence]\n" + tail
        with self.assertRaisesRegex(ValueError, "unbalanced"):
            MODULE.validate_graph_gallery(broken)


if __name__ == "__main__":
    unittest.main()
