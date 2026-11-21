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

    def mutate_matrix(
        self, mutate, registry_name="biomedical_decision_matrix.csv"
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="biostat-matrix-") as tmp:
            temp = Path(tmp)
            base = temp / "03_learning/bio_stats"
            base.mkdir(parents=True)
            for name in (
                "biomedical_decision_matrix.csv",
                "biomedical_gate_dictionary.csv",
                "biostat_method_registry.csv",
            ):
                shutil.copyfile(ROOT / "03_learning/bio_stats" / name, base / name)
            selector = temp / "06_RESOURCES/R/biomedical_test_selector.R"
            selector.parent.mkdir(parents=True)
            shutil.copyfile(ROOT / "06_RESOURCES/R/biomedical_test_selector.R",
                            selector)
            path = base / registry_name
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

    def test_nontextbook_routes_preserve_empty_chapter_attribution(self) -> None:
        with (ROOT / "03_learning/bio_stats/biostat_method_registry.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = list(csv.DictReader(handle))
        blank_routes = {
            row["method_id"]: row["coverage"]
            for row in rows if row["biostat_chapters"] == ""
        }
        self.assertEqual(blank_routes, {
            "descriptive-design-review": "extension",
            "survey-design-review": "extension",
            "omics-design-review": "extension",
            "prediction-validation-review": "extension",
            "paired-design-review": "extension",
            "group-count-review": "design_gate",
            "ordinal-one-sample-review": "extension",
        })
        self.assertEqual(validate_matrix(ROOT)["routes"], 27)

    def test_textbook_route_requires_chapters(self) -> None:
        self.mutate_matrix(
            lambda rows: rows[0].__setitem__("biostat_chapters", ""),
            "biostat_method_registry.csv",
        )

    def test_unknown_biostat_coverage(self) -> None:
        self.mutate_matrix(
            lambda rows: rows[2].__setitem__("coverage", "unverified"),
            "biostat_method_registry.csv",
        )

    def test_blank_nonchapter_fields_still_fail(self) -> None:
        for field in ("method_id", "topic", "coverage"):
            with self.subTest(field=field):
                self.mutate_matrix(
                    lambda rows: rows[2].__setitem__(field, ""),
                    "biostat_method_registry.csv",
                )

    def test_invalid_chapter_attribution(self) -> None:
        for chapters in ("0", "15", "2;2", "2;;3", "2;", "2; 3", " ", "N/A"):
            with self.subTest(chapters=chapters):
                self.mutate_matrix(
                    lambda rows: rows[0].__setitem__(
                        "biostat_chapters", chapters
                    ),
                    "biostat_method_registry.csv",
                )

    def test_extension_with_invalid_chapters_fails(self) -> None:
        self.mutate_matrix(
            lambda rows: rows[2].__setitem__("biostat_chapters", "15"),
            "biostat_method_registry.csv",
        )


if __name__ == "__main__":
    unittest.main()
