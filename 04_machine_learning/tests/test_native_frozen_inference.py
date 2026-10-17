"""Synthetic-only CLI controls; real G3 lineage/parity is checked separately."""
import csv
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

BINARY = os.environ.get("ASSAY_NATIVE_PREDICT_BINARY")


def known_model():
    return {
        "schema_version": 1,
        "task": "synthetic_paired_specimen_category",
        "protocol_id": "paired-assay-native-rust-v1",
        "plan_name": "final_development",
        "positive_class": 1,
        "feature_names": ["Feature001", "Feature002"],
        "medians": [3.0, 4.0],
        "means": [1.0, 2.0],
        "scales": [2.0, 2.0],
        "coefficients_class_1": [1.0, 2.0],
        "intercept_class_1": -1.0,
    }


@unittest.skipUnless(BINARY, "Set ASSAY_NATIVE_PREDICT_BINARY to the compiled Rust CLI")
class FrozenInferenceCliTests(unittest.TestCase):
    def execute(self, model=None, rows=None, header=None, output_exists=False):
        model = known_model() if model is None else model
        header = ["specimen_id", *known_model()["feature_names"]] if header is None else header
        rows = [["Specimen001", "NA", "3.0"], ["Specimen002", "3.0", "4.0"]] if rows is None else rows
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            model_file = folder / "frozen.json"
            csv_file = folder / "records.csv"
            out = folder / "output"
            model_file.write_text(json.dumps(model) + "\n")
            with csv_file.open("w", newline="") as fd:
                writer = csv.writer(fd)
                writer.writerow(header)
                writer.writerows(rows)
            if output_exists:
                out.mkdir()
                (out / "keep.txt").write_text("DO NOT OVERWRITE")
            result = subprocess.run([BINARY, str(model_file), str(csv_file), str(out)],
                                    capture_output=True, text=True)
            predictions = (out / "predictions.csv").read_bytes() if (out / "predictions.csv").exists() else None
            manifest = json.loads((out / "run.json").read_text()) if (out / "run.json").exists() else None
            untouched = (out / "keep.txt").read_text() if (out / "keep.txt").exists() else None
            return result.returncode, predictions, manifest, untouched, model_file.read_bytes(), csv_file.read_bytes()

    def test_valid_fixture_honors_order_classes_and_hashes(self):
        rc, predictions, manifest, _, model, inputs = self.execute()
        self.assertEqual(rc, 0)
        self.assertEqual(manifest["positive_class"], 1)
        self.assertFalse(manifest["training_performed"])
        self.assertEqual(manifest["model_sha256"], hashlib.sha256(model).hexdigest())
        self.assertEqual(manifest["input_sha256"], hashlib.sha256(inputs).hexdigest())
        self.assertEqual(manifest["predictions_sha256"], hashlib.sha256(predictions).hexdigest())
        values = list(csv.DictReader(predictions.decode().splitlines()))
        self.assertEqual([r["specimen_id"] for r in values], ["Specimen001", "Specimen002"])
        import math
        expected = [1 / (1 + math.exp(1)), 1 / (1 + math.exp(-2.5))]
        for r, p in zip(values, expected):
            self.assertLessEqual(abs(float(r["probability_class_1"]) - p), 1e-14)

    def test_fail_closed_on_bad_plan_class_parameters_and_unknown_keys(self):
        for field, value in (
            ("positive_class", 0),
            ("plan_name", "outer_0"),
            ("schema_version", 2),
            ("scales", [0.0, 2.0]),
            ("feature_names", ["Feature001", "Feature001"]),
            ("unexpected", "not-allowed"),
        ):
            model = copy.deepcopy(known_model())
            model[field] = value
            with self.subTest(field=field):
                rc, predictions, manifest, *_ = self.execute(model=model)
                self.assertNotEqual(rc, 0)
                self.assertIsNone(predictions)
                self.assertIsNone(manifest)

    def test_fail_closed_on_identity_schema_and_nonfinite_input(self):
        for header, rows in (
            (["specimen_id", "Feature002", "Feature001"], [["Specimen001", "1", "2"]]),
            (None, [["Specimen001", "1", "2"], ["Specimen001", "3", "4"]]),
            (None, [["Specimen001", "NaN", "4"]]),
            (None, [["Specimen001", "1"]]),
        ):
            with self.subTest(header=header, rows=rows):
                rc, predictions, manifest, *_ = self.execute(header=header, rows=rows)
                self.assertNotEqual(rc, 0)
                self.assertIsNone(predictions)
                self.assertIsNone(manifest)

    def test_output_overwrite_is_refused(self):
        rc, predictions, manifest, untouched, *_ = self.execute(output_exists=True)
        self.assertNotEqual(rc, 0)
        self.assertIsNone(predictions)
        self.assertIsNone(manifest)
        self.assertEqual(untouched, "DO NOT OVERWRITE")


if __name__ == "__main__":
    unittest.main()
