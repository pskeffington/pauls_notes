#!/usr/bin/env python3
"""Independently replay audited G3 final-development logits in a read-only Rust CLI.

All inputs must be from the internally generated G3 teaching run; this tool
does not download data, fit, authorize real participants or publish models.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
from scipy.special import expit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "04_machine_learning/examples"))
import breast_cancer_rust_training as training  # noqa: E402

MAX_ERROR = 1e-12
DISCLAIMER = "SYNTHETIC RESEARCH/EDUCATION ONLY; NOT FOR CLINICAL USE."


def fingerprint(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def independent_validation(source, binary, output):
    source, binary, output = Path(source).resolve(), Path(binary).resolve(), Path(output).resolve()
    if not source.is_dir() or not binary.is_file():
        raise ValueError("G3 evidence directory and compiled CLI are required")
    if output.is_relative_to(ROOT) or output.exists() or not output.parent.is_dir():
        raise ValueError("Use a new evidence output directory outside the repository")

    # Do not rely on an arbitrary frozen JSON. First audit the full G3 generated
    # cohort, frozen protocol/source, all fit attempts and accepted numeric output.
    training.audit(source)
    dataset = training.read_json(source / "development.json")
    frozen_fit = training.read_json(source / "rust/model-3.json")
    raw, labels = training.validate_input(dataset)
    plan = dataset["plans"][-1]
    if plan["name"] != "final_development" or plan["assessment"] or plan["train"] != list(range(len(dataset["rows"]))):
        raise ValueError("Native model must originate from final development, not an outer fold")
    training.audit_model(frozen_fit, raw, labels, plan)
    if frozen_fit["plan"] != plan or len(frozen_fit["coefficients_class_1"]) != len(dataset["feature_names"]):
        raise ValueError("Frozen model lineage or shape mismatch")

    prep = frozen_fit["preparation"]
    model = dict(
        schema_version=1,
        task="synthetic_paired_specimen_category",
        protocol_id="paired-assay-native-rust-v1",
        plan_name="final_development",
        positive_class=1,
        feature_names=dataset["feature_names"],
        medians=prep["medians"],
        means=prep["means"],
        scales=prep["scales"],
        coefficients_class_1=frozen_fit["coefficients_class_1"],
        intercept_class_1=frozen_fit["intercept_class_1"],
    )
    theta = np.asarray(model["coefficients_class_1"], dtype=float)
    independent = expit(training.transform(raw, prep) @ theta + model["intercept_class_1"])
    original = np.asarray(frozen_fit["probabilities_class_1"], dtype=float)
    if independent.shape != original.shape or np.max(np.abs(independent - original)) > MAX_ERROR:
        raise ValueError("Independent Python and frozen G3 training probabilities disagree")

    # This is a wholly synthetic proof fixture. Never stage the exported model,
    # row-level predictions, or development records in public Git or CI artifacts.
    output.mkdir()
    model_path = output / "frozen.json"
    model_path.write_text(json.dumps(model, indent=2, allow_nan=False) + "\n")
    sample_path = output / "specimens.csv"
    with sample_path.open("x", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["specimen_id", *dataset["feature_names"]])
        for row in dataset["rows"]:
            writer.writerow([row["specimen_id"], *["NA" if x is None else x for x in row["values"]]])

    result = subprocess.run([str(binary), str(model_path), str(sample_path),
                             str(output / "native-predictions")],
                            capture_output=True, text=True, timeout=30)
    if result.returncode:
        raise ValueError("Native frozen predictor rejected the validated synthetic fixture")
    report_path = output / "native-predictions/predictions.csv"
    with report_path.open(newline="", encoding="utf-8") as file:
        records = list(csv.DictReader(file))
    identifiers = [r["specimen_id"] for r in dataset["rows"]]
    if len(records) != len(identifiers) or [r.get("specimen_id") for r in records] != identifiers:
        raise ValueError("Native prediction identity or order mismatch")
    try:
        actual = np.asarray([float(r["probability_class_1"]) for r in records])
    except (TypeError, KeyError, ValueError) as exc:
        raise ValueError("Malformed class-1 probability CSV") from exc
    if actual.shape != independent.shape or not np.isfinite(actual).all():
        raise ValueError("Nonfinite or wrong-size prediction")
    max_error = float(np.max(np.abs(actual - independent)))
    if max_error > MAX_ERROR:
        raise ValueError("Frozen Rust/Python probability parity failed")

    manifest = training.read_json(output / "native-predictions/run.json")
    if (manifest.get("positive_class") != 1
        or manifest.get("training_performed") is not False
        or manifest.get("rows") != len(records)
        or manifest.get("model_use", {}).get("clinical_use_authorized") is not False
        or manifest.get("model_use", {}).get("tcga_case_data_processed") is not False
        or "NOT FOR CLINICAL USE" not in manifest.get("model_use", {}).get("disclaimer", "")
        or manifest.get("model_sha256") != fingerprint(model_path)
        or manifest.get("input_sha256") != fingerprint(sample_path)
        or manifest.get("predictions_sha256") != fingerprint(report_path)):
        raise ValueError("Frozen Rust evidence integrity failure")

    summary = {
        "status": "accepted_synthetic_read_only_parity",
        "protocol": "paired-assay-native-rust-v1",
        "plan": "final_development",
        "people": len({r["person_id"] for r in dataset["rows"]}),
        "development_predictions": len(records),
        "reserved_predictions": 0,
        "positive_class": 1,
        "training_performed_by_predictor": False,
        "max_probability_error": max_error,
        "prespecified_absolute_tolerance": MAX_ERROR,
        "g3_source_sha256": fingerprint(source / "development.json"),
        "g3_model_sha256": fingerprint(source / "rust/model-3.json"),
        "frozen_export_sha256": fingerprint(model_path),
        "prediction_sha256": fingerprint(report_path),
        "clinical_use_authorized": False,
        "real_tcga_data_processed": False,
        "disclaimer": DISCLAIMER,
    }
    (output / "validation.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    print("PASS: audited synthetic G3 frozen Rust/Python category-1 parity; "
          f"development rows={len(records)} max_error={max_error:.3e} "
          f"prespecified_tolerance={MAX_ERROR:.1e}; reserved people untouched.")
    print(DISCLAIMER)
    return summary


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("g3_run", type=Path)
    cli.add_argument("predict_binary", type=Path)
    cli.add_argument("new_output_directory", type=Path)
    args = cli.parse_args()
    independent_validation(args.g3_run, args.predict_binary, args.new_output_directory)


if __name__ == "__main__":
    main()
