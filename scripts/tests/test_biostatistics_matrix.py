"""Negative fixtures for machine-readable biomedical test matrix contract."""
from __future__ import annotations

import csv
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

from check_biostatistics_matrix import MatrixValidationError, validate_matrix  # noqa: E402


class TestBiomedicalMatrix(unittest.TestCase):
    def test_baseline_registry(self) -> None:
        result = validate_matrix(ROOT)
        self.assertEqual(result["routes"], 27)
        self.assertEqual(result["gates"], 25)
        self.assertGreater(result["reviewed_gate_links"], 100)

    def mutate_matrix(self, mutate) -> None:
        with tempfile.TemporaryDirectory(prefix="biostat-matrix-") as tmp:
            temp = Path(tmp)
            base = temp / "03_learning/bio_stats"
            base.mkdir(parents=True)
            for name in (
                "biomedical_decision_matrix.csv",
                "biomedical_gate_dictionary.csv",
                "rosner_method_registry.csv",
            ):
                shutil.copyfile(ROOT / "03_learning/bio_stats" / name, base / name)
            selector = temp / "06_RESOURCES/R/biomedical_test_selector.R"
            selector.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / "06_RESOURCES/R/biomedical_test_selector.R",
                            selector)
            path = base / "biomedical_decision_matrix.csv"
            with path.open(newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                fields = list(reader.fieldnames or [])
                rows = list(reader)
            mutate(rows)
            with path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaises(MatrixValidationError):
                validate_matrix(temp)

    def test_missing_route(self) -> None:
        self.mutate_matrix(lambda rows: rows.pop())

    def test_duplicate_route(self) -> None:
        self.mutate_matrix(lambda rows: rows.append(dict(rows[0])))

    def test_unknown_gate(self) -> None:
        self.mutate_matrix(lambda rows: rows[0].__setitem__(
            "gate_keys", rows[0]["gate_keys"] + ";not_a_gate"
        ))

    def test_empty_interpretation(self) -> None:
        self.mutate_matrix(lambda rows: rows[0].__setitem__(
            "interpretation", ""
        ))

    def test_invalid_route_class(self) -> None:
        self.mutate_matrix(lambda rows: rows[0].__setitem__(
            "route_class", "clinically_approved"
        ))

    def test_repeated_gate(self) -> None:
        self.mutate_matrix(lambda rows: rows[0].__setitem__(
            "gate_keys", rows[0]["gate_keys"] + ";unit"
        ))


if __name__ == "__main__":
    unittest.main()
