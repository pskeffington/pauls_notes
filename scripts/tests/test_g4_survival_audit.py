#!/usr/bin/env python3
"""G4 independent auditor tests; do not require R or data from patients."""
import csv
import importlib.util
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("audit_g4", ROOT / "scripts/audit_g4_survival.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class G4AuditorTests(unittest.TestCase):
    def test_left_limit_and_horizon(self):
        training = [
            {"time_months": "10", "event": "0"},
            {"time_months": "20", "event": "1"},
            {"time_months": "30", "event": "1"},
            {"time_months": "40", "event": "1"},
        ]
        self.assertAlmostEqual(audit.g_before(training, 10, True), 1)
        self.assertAlmostEqual(audit.g_before(training, 10), .75)
        self.assertAlmostEqual(audit.g_before(training, 24), .75)

    def test_tied_censor_failures(self):
        training = [
            {"time_months": "10", "event": "0"},
            {"time_months": "10", "event": "0"},
            {"time_months": "10", "event": "1"},
            {"time_months": "30", "event": "1"},
        ]
        self.assertAlmostEqual(audit.g_before(training, 10, True), 1)
        self.assertAlmostEqual(audit.g_before(training, 10), .5)

    def test_reject_nonfinite(self):
        for text in ("nan", "inf", "-inf"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                audit.num(text)

    def test_missing_evidence_rejected(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(OSError):
            audit.run(pathlib.Path(tmp))


if __name__ == "__main__":
    unittest.main()
