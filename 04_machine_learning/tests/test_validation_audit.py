"""Challenge the processed-result audit without downloading or running third-party code."""
import csv
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('validation',
    Path(__file__).resolve().parents[1] / 'validation/run_validation.py')
VALIDATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATION)


class AuditTests(unittest.TestCase):
    def write(self, folder, rows):
        path = Path(folder) / 'scores.csv'
        with path.open('w', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        return path

    def row(self):
        return dict(task_id='assay', learner_id='CPH', iteration='1', tune_measure='isbs',
                    errors_cnt='0', warnings_cnt='0', harrell_c='NA', uno_c='NA',
                    isbs='0.2', isll='0.7', dcalib='0.5', alpha_calib='1.0')

    def test_uncomputed_metrics_and_failed_rows_remain_visible(self):
        failed = self.row()
        failed.update(iteration='2', errors_cnt='1', warnings_cnt='1')
        with tempfile.TemporaryDirectory() as folder:
            report = VALIDATION.audit_scores(self.write(folder, [self.row(), failed]))
        self.assertEqual(report['rows_flagged_error'], 1)
        self.assertEqual(report['rows_flagged_warning'], 1)
        self.assertEqual(report['metric_coverage']['harrell_c']['missing_or_uncomputed'], 2)
        self.assertEqual(report['metric_coverage']['isbs']['finite'], 2)

    def test_duplicate_keys_and_invalid_metrics_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, 'duplicate'):
                VALIDATION.audit_scores(self.write(folder, [self.row(), self.row()]))
            for value in ('inf', '-0.1', '1.1', 'word'):
                row = self.row()
                row['harrell_c'] = value
                with self.subTest(value=value), self.assertRaises(ValueError):
                    VALIDATION.audit_scores(self.write(folder, [row]))

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError):
                VALIDATION.run(Path(folder))
            self.assertTrue(Path(folder).is_dir())


if __name__ == '__main__':
    unittest.main()
