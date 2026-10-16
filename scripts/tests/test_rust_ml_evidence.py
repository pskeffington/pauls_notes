"""Challenge false upgrades, citation loss and mutable Rust source provenance."""
import copy
from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_rust_ml_evidence as checker


class RustEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = checker.read_rows()
        cls.guide = checker.GUIDE.read_text(encoding='utf-8')
        cls.bib = checker.BIBLIOGRAPHY.read_text(encoding='utf-8')

    def errors(self, rows, guide=None, bib=None):
        return checker.inspect(rows, self.guide if guide is None else guide,
                               checker.ROOT, self.bib if bib is None else bib,
                               today=date(2026, 10, 16))

    def test_valid_corpus_and_related_binding_studies(self):
        self.assertEqual(self.errors(self.rows), [])
        by_id = {row['id']: row for row in self.rows}
        self.assertEqual(by_id['RML-P02']['study_family'], by_id['RML-P03']['study_family'])
        self.assertNotEqual(by_id['RML-P02']['identifier'], by_id['RML-P03']['identifier'])

    def test_reject_software_promoted_to_publication(self):
        rows = copy.deepcopy(self.rows)
        software = next(row for row in rows if row['source_kind'] == 'software')
        software.update(source_kind='paper', publication_status='journal_article')
        self.assertTrue(any('source-kind mismatch' in e for e in self.errors(rows)))

    def test_duplicate_citations_and_incomplete_card_or_bibliography(self):
        rows = copy.deepcopy(self.rows)
        rows[1]['identifier'] = rows[0]['identifier']
        self.assertTrue(any('duplicate source identifier' in e for e in self.errors(rows)))
        self.assertTrue(self.errors(self.rows, guide=self.guide.replace('## RML-P01\n', '')))
        self.assertTrue(self.errors(self.rows, bib=self.bib.replace('RMLP01,', 'RMLP99,')))
        self.assertTrue(self.errors(self.rows, bib=self.bib.replace('10.1145/3458817.3476165', '10.1145/wrong')))

    def test_reject_mutable_or_mismatched_source(self):
        for key, value in [('artifact_revision', 'main'), ('source_sha256', 'unknown'),
                           ('review_url', 'https://raw.githubusercontent.com/rust-ml/linfa/main/README.md'),
                           ('local_application', '../outside.md')]:
            with self.subTest(key=key):
                rows = copy.deepcopy(self.rows)
                next(row for row in rows if row['source_kind'] == 'software')[key] = value
                self.assertTrue(self.errors(rows))

    def test_reject_unbacked_execution_and_clinical_upgrade(self):
        for key, value in [('local_execution', 'replicated'), ('breast_cancer_validation', 'validated')]:
            with self.subTest(key=key):
                rows = copy.deepcopy(self.rows)
                rows[0][key] = value
                self.assertTrue(any('separate validated contract' in e for e in self.errors(rows)))

    def test_reject_future_dates_and_unversioned_preprint(self):
        rows = copy.deepcopy(self.rows)
        rows[0]['checked_on'] = '2026-10-17'
        self.assertTrue(any('invalid date' in e for e in self.errors(rows)))
        rows = copy.deepcopy(self.rows)
        next(row for row in rows if row['publication_status'] == 'preprint')['identifier'] = 'arxiv:2609.25008'
        self.assertTrue(any('versioned preprint' in e for e in self.errors(rows)))


if __name__ == '__main__':
    unittest.main()
