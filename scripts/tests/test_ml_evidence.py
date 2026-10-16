"""Reject misleading or disconnected evidence-register metadata."""
import copy
import csv
from datetime import date
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_ml_evidence as checker


class EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with checker.REGISTER.open(newline='', encoding='utf-8') as stream:
            cls.rows = list(csv.DictReader(stream))
        cls.guide = checker.read_guides()
        with checker.REVIEW.open(newline='', encoding='utf-8') as stream:
            cls.reviews = list(csv.DictReader(stream))

    def errors(self, rows, guide=None):
        return checker.inspect(rows, self.guide if guide is None else guide,
                               checker.ROOT, today=date.today())

    def test_register_and_known_trial_relationship(self):
        self.assertEqual(self.errors(self.rows), [])
        by_id = {row['id']: row for row in self.rows}
        self.assertEqual(by_id['BC-02']['study_family'], by_id['BC-03']['study_family'])
        self.assertNotEqual(by_id['BC-02']['identifier'], by_id['BC-03']['identifier'])

    def test_tuning_source_identifiers_remain_distinct(self):
        tuning = [row for row in self.rows if row['id'] in
                  {'BC-M04', 'BC-M05', 'BC-M06', 'BC-M07', 'BC-M08', 'BC-M09', 'BC-M10'}]
        self.assertEqual(len(tuning), 7)
        self.assertEqual(len({row['identifier'] for row in tuning}), 7)
        self.assertTrue(all(row['local_application'] == '04_machine_learning/model-tuning.md'
                            for row in tuning))

    def test_recent_card_coverage_and_years(self):
        recent_ids = {f'BC-M{number}' for number in range(11, 20)}
        recent = [row for row in self.rows if row['id'] in recent_ids]
        self.assertEqual({row['id'] for row in recent}, recent_ids)
        for row in recent:
            self.assertTrue(2021 <= int(row['year']) <= 2025)
            self.assertEqual(row['local_reproduction'], 'not_run')
        missing = self.guide.replace('## BC-M19\n', '## Removed\n')
        self.assertTrue(any('missing evidence card' in error
                            for error in self.errors(self.rows, missing)))

    def test_review_coverage_and_unbacked_replication(self):
        self.assertEqual(checker.inspect_review(self.rows, self.reviews), [])
        incomplete = self.reviews[:-1]
        self.assertTrue(any('exactly' in error for error in checker.inspect_review(self.rows, incomplete)))
        changed = copy.deepcopy(self.reviews)
        changed[0]['identifier'] = changed[1]['identifier']
        changed[1]['paper_reproduction'] = 'replicated'
        changed[2]['source_sha256'] = 'not-a-digest'
        errors = checker.inspect_review(self.rows, changed)
        for text in ('mismatched', 'reproduction', 'digest'):
            self.assertTrue(any(text in error for error in errors), text)

    def test_omitting_any_guide_leaves_uncovered_records(self):
        for omitted in checker.GUIDES:
            with self.subTest(guide=omitted.name):
                incomplete = '\n'.join(path.read_text(encoding='utf-8')
                                       for path in checker.GUIDES if path != omitted)
                self.assertTrue(any('missing evidence card' in error
                                    for error in self.errors(self.rows, incomplete)))

    def test_duplicate_card_across_guides(self):
        errors = self.errors(self.rows, self.guide + '\n## BC-M11\n')
        self.assertTrue(any('Duplicate evidence card' in error for error in errors))

    def test_duplicate_citation_and_unbacked_reproduction(self):
        rows = copy.deepcopy(self.rows)
        rows[1]['identifier'] = rows[0]['identifier']
        rows[0]['local_reproduction'] = 'replicated'
        errors = self.errors(rows)
        self.assertTrue(any('duplicate publication' in error for error in errors))
        self.assertTrue(any('reproduction claim' in error for error in errors))

    def test_missing_card_artifact_pin_and_local_anchor(self):
        rows = copy.deepcopy(self.rows)
        rows[0]['artifact_version'] = ''
        rows[0]['local_application'] = 'README.md#nonexistent-evidence-anchor'
        errors = self.errors(rows, self.guide.replace('## BC-01\n', '## Removed\n'))
        for text in ('inspected artifact', 'application anchor', 'missing evidence card'):
            self.assertTrue(any(text in error for error in errors), text)

    def test_future_review_and_preprint_version(self):
        rows = copy.deepcopy(self.rows)
        rows[0]['checked_on'] = '2099-01-01'
        preprint = next(row for row in rows if row['evidence_type'] == 'preprint_external_report')
        preprint['identifier'] = 'arXiv:2610.03693'
        errors = self.errors(rows)
        self.assertTrue(any('review date' in error for error in errors))
        self.assertTrue(any('publication identifier' in error for error in errors))


if __name__ == '__main__':
    unittest.main()
