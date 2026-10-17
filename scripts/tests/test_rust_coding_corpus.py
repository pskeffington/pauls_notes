"""Negative controls for Rust corpus evidence and frozen-build claims."""
import copy
from datetime import date
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_rust_coding_corpus as check


class RustCodingCorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = check.read_rows()
        cls.guide = check.GUIDE.read_text(encoding="utf-8")

    def problems(self, rows=None, guide=None, today=date(2026, 10, 17)):
        return check.inspect(
            self.rows if rows is None else rows,
            self.guide if guide is None else guide,
            today=today
        )

    def test_current_corpus_and_pinned_rust_baseline(self):
        self.assertEqual(self.problems(), [])
        self.assertEqual(check.inspect_rust_baseline(), [])
        self.assertGreaterEqual(len(self.rows), 30)

    def test_duplicate_paper_or_malformed_publication_is_rejected(self):
        rows = copy.deepcopy(self.rows)
        rows[1]["identifier"] = rows[0]["identifier"]
        self.assertTrue(any("duplicate source identifier" in s for s in self.problems(rows)))
        rows = copy.deepcopy(self.rows)
        rows[0]["identifier"] = "not-a-doi"
        self.assertTrue(any("publisher DOI" in s for s in self.problems(rows)))

    def test_reject_fake_full_text_or_clinical_claims(self):
        for field, new in (("review_scope", "full_text_systematic_review"),
                           ("local_execution", "model_validated"),
                           ("clinical_validation", "verified_on_patients")):
            rows = copy.deepcopy(self.rows)
            rows[0][field] = new
            with self.subTest(field=field):
                self.assertTrue(self.problems(rows))

    def test_reject_source_status_upgrade_and_missing_card(self):
        rows = copy.deepcopy(self.rows)
        row = next(r for r in rows if r["kind"] == "tool_documentation")
        row["kind"] = "paper"
        self.assertTrue(self.problems(rows))
        self.assertTrue(self.problems(guide=self.guide.replace("#### RC-P01\n", "")))

    def test_preprint_version_and_dates(self):
        rows = copy.deepcopy(self.rows)
        row = next(r for r in rows if r["kind"] == "preprint")
        row["identifier"] = "arxiv:2607.01504"
        self.assertTrue(any("versioned" in s for s in self.problems(rows)))
        self.assertTrue(any("review date" in s for s in self.problems(today=date(2026, 10, 16))))

    def test_pinned_manifest_changes_fail(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src = check.ROOT / "04_machine_learning/rust"
            dest = root / "04_machine_learning/rust"
            (dest / "src").mkdir(parents=True)
            for file in ("Cargo.toml", "rust-toolchain.toml", "Cargo.lock"):
                (dest / file).write_bytes((src / file).read_bytes())
            (dest / "src/lib.rs").write_bytes((src / "src/lib.rs").read_bytes())
            self.assertEqual(check.inspect_rust_baseline(root), [])
            manifest = dest / "Cargo.toml"
            manifest.write_text(manifest.read_text().replace('edition = "2021"', 'edition = "2024"'))
            self.assertTrue(any("edition" in s for s in check.inspect_rust_baseline(root)))


if __name__ == "__main__":
    unittest.main()
