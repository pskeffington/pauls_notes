"""Synthetic-only, configuration-driven grouped ML; not a patient training interface."""
import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path
import numpy as np
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, log_loss
from sklearn.model_selection import StratifiedGroupKFold, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

def validate(config):
    if not isinstance(config, dict) or set(config) != {"schema_version", "stage", "data", "design", "models", "seed"}:
        raise ValueError("Unexpected or missing top-level configuration field")
    if config["schema_version"] != 1 or config["stage"] != "synthetic-validation":
        raise ValueError("Research/patient training is NOT admitted; synthetic-validation only")
    data, design = config["data"], config["design"]
    if set(data) != {"people", "specimens_per_person", "features", "informative", "missing_fraction"}:
        raise ValueError("Invalid data configuration")
    if set(design) != {"outer_folds", "inner_folds", "feature_counts", "regularization_C"}:
        raise ValueError("Invalid validation design")
    if config["models"] != ["majority", "logistic"]:
        raise ValueError("Model allowlist is ['majority', 'logistic']")
    dims = (config["seed"], data["people"], data["specimens_per_person"], data["features"], data["informative"], design["outer_folds"], design["inner_folds"])
    if any(type(v) is not int for v in dims) or config["seed"] < 0:
        raise ValueError("Nonnegative integer seed and integer dimensions required")
    if not (20 <= data["people"] <= 1000 and 1 <= data["specimens_per_person"] <= 5 and 4 <= data["features"] <= 500 and 2 <= data["informative"] <= data["features"]):
        raise ValueError("Synthetic generator dimensions outside bounded scope")
    if type(data["missing_fraction"]) not in (int, float) or not (0 <= data["missing_fraction"] <= .4):
        raise ValueError("Invalid missingness")
    if not (2 <= design["outer_folds"] <= 5 and 2 <= design["inner_folds"] <= 5):
        raise ValueError("Invalid fold count")
    if type(design["feature_counts"]) is not list or not design["feature_counts"] or any(type(k) is not int or not 1 <= k <= data["features"] for k in design["feature_counts"]):
        raise ValueError("Invalid feature selection candidates")
    if type(design["regularization_C"]) is not list or not design["regularization_C"] or any(type(c) not in (int, float) or not np.isfinite(c) or not 0 < c <= 100 for c in design["regularization_C"]):
        raise ValueError("Invalid regularization candidates")
    if data["people"] // design["outer_folds"] < design["inner_folds"] * 2:
        raise ValueError("Insufficient groups for inner folds")
    if len(design["feature_counts"]) * len(design["regularization_C"]) > 30:
        raise ValueError("Search exceeds 30 candidates")
    return config

def run(config):
    validate(config)
    data, design, seed = config["data"], config["design"], config["seed"]
    people, specimens = data["people"], data["specimens_per_person"]
    rng = np.random.default_rng(seed)
    group_labels = np.arange(people) % 2
    rng.shuffle(group_labels)
    unique_x, _ = make_classification(n_samples=people, n_features=data["features"], n_informative=data["informative"], n_redundant=0, n_repeated=0, n_classes=2, random_state=seed)
    groups = np.repeat(np.arange(people), specimens)
    y = np.repeat(group_labels, specimens)
    X = np.repeat(unique_x, specimens, axis=0) + rng.normal(0, .1, size=(people * specimens, data["features"]))
    X[rng.random(X.shape) < data["missing_fraction"]] = np.nan
    records = []
    splits = StratifiedGroupKFold(n_splits=design["outer_folds"], shuffle=True, random_state=seed)
    for fold, (train, test) in enumerate(splits.split(X, y, groups)):
        if set(groups[train]).intersection(groups[test]):
            raise ValueError("Outer person leakage")
        inner = StratifiedGroupKFold(n_splits=design["inner_folds"], shuffle=True, random_state=seed + fold + 1)
        inner_splits = list(inner.split(X[train], y[train], groups[train]))
        for a, b in inner_splits:
            if set(groups[train][a]).intersection(groups[train][b]):
                raise ValueError("Inner person leakage")
            if len(set(y[train][a])) != 2 or len(set(y[train][b])) != 2:
                raise ValueError("Insufficient classes in inner partition")
        for model_name in config["models"]:
            selected = None
            if model_name == "majority":
                estimator = DummyClassifier(strategy="prior").fit(X[train], y[train])
            else:
                pipeline = Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler()), ("select", SelectKBest(score_func=f_classif)), ("classifier", LogisticRegression(max_iter=1000, solver="lbfgs", random_state=seed))])
                search = GridSearchCV(pipeline, {"select__k": design["feature_counts"], "classifier__C": design["regularization_C"]}, scoring="balanced_accuracy", cv=inner_splits, n_jobs=1, error_score="raise", refit=True)
                search.fit(X[train], y[train])
                estimator = search.best_estimator_
                selected = {k: (int(v) if isinstance(v, (np.integer, int)) else float(v)) for k, v in search.best_params_.items()}
            pred = estimator.predict_proba(X[test])
            if pred.shape != (len(test), 2) or not np.isfinite(pred).all():
                raise ValueError("Invalid probabilities")
            records.append({"fold": fold, "model": model_name, "train_people": int(len(np.unique(groups[train]))), "test_people": int(len(np.unique(groups[test]))), "test_rows": int(len(test)), "balanced_accuracy": float(balanced_accuracy_score(y[test], pred.argmax(axis=1))), "accuracy": float(accuracy_score(y[test], pred.argmax(axis=1))), "log_loss": float(log_loss(y[test], pred, labels=[0, 1])), "selected_parameters": selected, "test_group_ids": groups[test].astype(int).tolist(), "test_row_indices": test.astype(int).tolist(), "labels": y[test].astype(int).tolist(), "probability_class_1": pred[:, 1].tolist()})
    return {"status": "synthetic_validation_only", "training_data": "internally_generated",
            "clinical_claim": False, "observations": len(X), "groups": people,
            "features": X.shape[1], "records": records,
            "model_use": {
                "status": "research_education_only_not_clinically_validated",
                "clinical_use_authorized": False,
                "patient_level_training_authorized": False,
                "data_access": "internally_generated_synthetic_only",
                "tcga_case_data_processed": False,
                "reidentification_permitted": False,
                "disclaimer": "NOT FOR CLINICAL USE: not a diagnostic, prognostic, treatment-selection or medical decision tool.",
                "policy_path": "04_machine_learning/research_toolkit/MODEL_USE_POLICY.md"
            }}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args(argv)
    raw = args.config.read_bytes()
    config = json.loads(raw)
    validate(config)
    target = args.output.resolve()
    if target.is_relative_to(Path(__file__).resolve().parents[2]):
        raise ValueError("Output must be outside the public source repository")
    if target.exists():
        raise ValueError("Output already exists; never overwrite research runs")
    if not target.parent.is_dir():
        raise ValueError("Create parent directory first")
    result = run(config)
    result["config_sha256"] = hashlib.sha256(raw).hexdigest()
    result["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result["runtime"] = {"python": sys.version.split()[0], "numpy": np.__version__, "platform": platform.platform(), "threads": 1}
    target.mkdir()
    with (target / "report.json").open("x") as output:
        json.dump(result, output, indent=2, allow_nan=False)
        output.write("\n")
    print(f"Validated {len(result['records'])} synthetic fold/model assessments in {target}")
    print("SYNTHETIC RESEARCH ONLY; NOT FOR CLINICAL USE.")

if __name__ == "__main__":
    main()
