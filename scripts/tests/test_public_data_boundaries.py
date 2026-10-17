"""Tests for blocked commits and false-positive-resistant public examples."""
import importlib.util
import unittest
from unittest import mock
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "check_public_data_boundaries.py"
spec = importlib.util.spec_from_file_location("data_boundary", SOURCE)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

class PublicDataBoundaryTests(unittest.TestCase):
    def test_synthetic_and_corpus_fixtures_allowed(self):
        self.assertEqual(guard.inspect("04_machine_learning/rust/example/specimens.csv",
                                      b"specimen_id,Feature001\nSynthetic1,2\n"), [])
        self.assertEqual(guard.inspect("04_machine_learning/evidence/paper-review.csv",
                                      b"study,doi\nreview,10.1000/example\n"), [])

    def test_restricted_paths_and_raw_formats_denied(self):
        for path in ("raw_data/clinical.csv", "controlled_access/tumor.csv",
                     "04_machine_learning/gdc_downloads/data.txt", "data/case.vcf",
                     "model_weights.onnx", "sample.fastq.gz", "clinical.project-tcga-brca.tar.gz",
                     "local/gdc-token-2026.txt"):
            with self.subTest(path=path):
                self.assertTrue(guard.inspect(path, b"file contents"))

    def test_identifier_patterns_and_columns_denied(self):
        cases = [
            ("tables/subjects.csv", b"email_address,feature\nexample@localhost.org,2\n"),
            ("tables/subjects.csv", b"medical_record_number,x\nPRIVATE,1\n"),
            ("tables/subjects.tsv", b"date_of_birth\tx\n2000-01-01\t2\n"),
            ("metadata.json", b'{"case_id":"TEST-001"}'),
            ("prediction.csv", b"specimen_id,value\nTCGA-AB-1234,0.6\n"),
            ("patient.csv", b"feature\n123-45-6789\n"),
            ("gdc.json", b'{"access":"controlled","project":"TCGA-BRCA"}'),
            ("gdc.json", b'{"access":"unknown"}'),
            ("credential.json", b'{"key":"-----BEGIN ' + b'PRIVATE KEY-----"}'),
        ]
        for path, blob in cases:
            with self.subTest(path=path, blob=blob[:20]):
                self.assertTrue(guard.inspect(path, blob))

    def test_failure_logs_hide_identifying_filenames(self):
        secret_path = "records/" + "TCGA-" + "XX-1234.csv"
        line = guard.redacted_failure(secret_path, "unregistered structured data")
        self.assertNotIn(secret_path, line)
        self.assertIn("path_hash=", line)

    def test_new_unregistered_tabular_file_is_blocked(self):
        registered = guard.registered_assets(staged=False)
        self.assertIsNone(guard.registration_problem(
            "04_machine_learning/rust/example/specimens.csv", registered))
        self.assertIsNotNone(guard.registration_problem(
            "new/hidden_patient_data.csv", registered))
        self.assertIsNotNone(guard.registration_problem(
            "new/unreviewed_metadata.json", registered))
        self.assertIn("scripts/public_data_assets.json", registered)

    def test_git_staging_never_follows_symlinks_or_submodules(self):
        # Staging a symlink can bypass file-content inspection unless index mode
        # is read directly. No real participant filenames/data enter the fixture.
        for mode in (b"120000", b"160000"):
            def git_fake(*args):
                if args == ("ls-files", "--stage", "-z"):
                    return mode + b" " + (b"0" * 40) + b" 0\tlink.csv\0"
                if args == ("diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"):
                    return b"link.csv\0"
                raise AssertionError("A nonregular file must never be resolved")
            with self.subTest(mode=mode), mock.patch.object(guard, "git_output", side_effect=git_fake):
                entries = list(guard.paths_and_reader(staged=True))
                self.assertEqual(entries, [("link.csv", b"", mode)])
                self.assertFalse(guard.safe_git_mode(entries[0][2]))
        self.assertTrue(guard.safe_git_mode(b"100644"))
        self.assertTrue(guard.safe_git_mode(b"100755"))
        self.assertFalse(guard.safe_git_mode(None))

    def test_merged_coding_reference_is_registered(self):
        registered = guard.registered_assets(staged=False)
        self.assertEqual(
            registered["02_biomedical_coding/rust_coding_best_practices_sources.csv"],
            "literature",
        )

    def test_public_metadata_only_is_not_direct_person_data(self):
        self.assertEqual(guard.inspect("metadata.json",
            b'{"project":"TCGA-BRCA","access":"open","file_count":20}'), [])

if __name__ == "__main__":
    unittest.main()
