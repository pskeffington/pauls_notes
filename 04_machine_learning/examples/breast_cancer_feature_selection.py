"""Synthetic paired-specimen classification with training-only feature selection."""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import sys
import tempfile

import joblib
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import GridSearchCV, GroupKFold, GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SEED = 261016
FEATURES = np.array([f"Feature{i:03d}" for i in range(1, 49)])


def make_cohort(people=60, seed=SEED):
    if not isinstance(people, int) or isinstance(people, bool) or people < 36:
        raise ValueError("At least 36 synthetic people required")
    rng = np.random.default_rng(seed)
    person_id = np.repeat(np.arange(people), 2)
    y = np.tile([0, 1], people)
    x = rng.normal(size=(len(y), len(FEATURES)))
    x += rng.normal(scale=0.3, size=(people, len(FEATURES)))[person_id]
    x[:, :4] += (2 * y[:, None] - 1) * np.array([0.8, 0.6, 0.4, 0.2])
    x[:, 4] = 0.9 * x[:, 0] + rng.normal(scale=0.3, size=len(y))
    x[rng.random(x.shape) < 0.03] = np.nan
    return dict(x=x, y=y, person_id=person_id,
                specimen_id=np.array([f"Specimen{i:03d}" for i in range(len(y))]),
                feature_names=FEATURES.copy())


def validate_cohort(data):
    x = np.asarray(data["x"])
    if x.ndim != 2 or x.shape[1] != len(FEATURES) or x.dtype.kind not in "fiu":
        raise ValueError("Expected a real observations-by-48-features matrix")
    if np.isinf(x).any() or len(x) < 72:
        raise ValueError("Infinite measurements or insufficient synthetic records")
    if not np.array_equal(data["feature_names"], FEATURES):
        raise ValueError("Feature identity and order must match the documented schema")
    y, groups, ids = (np.asarray(data[k]) for k in ("y", "person_id", "specimen_id"))
    if any(v.shape != (len(x),) for v in (y, groups, ids)):
        raise ValueError("Targets and identity keys must align with measurement rows")
    if y.dtype.kind not in "iu" or set(np.unique(y)) != {0, 1}:
        raise ValueError("Binary labels required: 0 comparator, 1 tumor-labeled specimen")
    if groups.dtype.kind not in "iu" or ids.dtype.kind not in "US":
        raise ValueError("Integer person keys and string specimen keys required")
    if len(np.unique(ids)) != len(ids) or any(not str(v).strip() for v in ids):
        raise ValueError("Specimen IDs must be unique and nonblank")
    for person in np.unique(groups):
        rows = groups == person
        if np.sum(rows) != 2 or set(y[rows]) != {0, 1}:
            raise ValueError("This fixture requires one specimen of each category per person")


def check_partition(analysis, assessment, groups, universe=None):
    analysis, assessment = np.asarray(analysis), np.asarray(assessment)
    expected = np.arange(len(groups)) if universe is None else np.asarray(universe)
    if any(v.ndim != 1 or v.dtype.kind not in "iu" or not len(v)
           or len(np.unique(v)) != len(v) for v in (analysis, assessment)):
        raise ValueError("Partitions require distinct integer row positions")
    if not np.array_equal(np.sort(np.concatenate([analysis, assessment])), np.sort(expected)):
        raise ValueError("Rows must partition the specified cohort slice exactly")
    if set(groups[analysis]) & set(groups[assessment]):
        raise ValueError("Person overlap across training and assessment")


def make_plan(data):
    validate_cohort(data)
    development, test = next(GroupShuffleSplit(n_splits=1, test_size=0.25,
        random_state=SEED).split(data["x"], data["y"], data["person_id"]))
    check_partition(development, test, data["person_id"])
    return development, test


def _fit_search(x, y, groups):
    folds = list(GroupKFold(n_splits=3).split(x, y, groups))
    for analysis, assessment in folds:
        check_partition(analysis, assessment, groups)
        if np.isnan(x[analysis]).all(axis=0).any():
            raise ValueError("A training fold has a completely missing feature")
        if any(len(np.unique(y[rows])) != 2 for rows in (analysis, assessment)):
            raise ValueError("Both classes required in each inner partition")
    pipeline = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("select", SelectKBest(f_classif)),
        ("scale", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000, random_state=SEED)),
    ])
    search = GridSearchCV(pipeline, {"select__k": [5, 10, 20], "model__C": [0.1, 1.0]},
        scoring="neg_brier_score", cv=folds, refit=True, n_jobs=1, error_score="raise")
    search.fit(x, y)
    return search, folds


def summarize_search(search):
    """Record every candidate's held-out fold error, without calling it a test score."""
    result = search.cv_results_
    candidates = []
    for i, parameters in enumerate(result["params"]):
        candidates.append(dict(parameters=parameters,
            fold_brier=[float(-result[f"split{fold}_test_score"][i])
                        for fold in range(search.n_splits_)],
            mean_brier=float(-result["mean_test_score"][i]),
            rank=int(result["rank_test_score"][i]), chosen=bool(i == search.best_index_)))
    return candidates


def probabilities(model, x):
    return model.predict_proba(x)[:, list(model.classes_).index(1)]


def scores(y, probability):
    return dict(roc_auc=float(roc_auc_score(y, probability)),
                average_precision=float(average_precision_score(y, probability)),
                brier=float(brier_score_loss(y, probability)))


def selected_features(model):
    return FEATURES[model.best_estimator_.named_steps["select"].get_support()].tolist()


def fit_development(data, development, test):
    """The test rows define the boundary; their values do not enter any fit."""
    validate_cohort(data)
    development, test = np.asarray(development), np.asarray(test)
    check_partition(development, test, data["person_id"])
    x, y, groups = data["x"][development], data["y"][development], data["person_id"][development]
    oof = np.full(len(development), np.nan)
    memberships, importance_values = [], []
    for fold, (analysis, assessment) in enumerate(GroupKFold(3).split(x, y, groups)):
        check_partition(analysis, assessment, groups)
        model, inner = _fit_search(x[analysis], y[analysis], groups[analysis])
        oof[assessment] = probabilities(model, x[assessment])
        diagnostic = permutation_importance(model, x[assessment], y[assessment],
            scoring="neg_brier_score", n_repeats=5, random_state=SEED + fold, n_jobs=1)
        importance_values.append(diagnostic.importances_mean)
        memberships.append(dict(analysis=development[analysis].tolist(),
            assessment=development[assessment].tolist(), best_parameters=model.best_params_,
            selected_features=selected_features(model), search_candidates=summarize_search(model),
            inner=[dict(analysis=development[analysis[a]].tolist(),
                        assessment=development[analysis[b]].tolist()) for a, b in inner]))
    if not np.isfinite(oof).all():
        raise ValueError("Every development specimen must receive one outer-held-out prediction")
    final, inner = _fit_search(x, y, groups)
    report = dict(development=np.asarray(development).tolist(), test=np.asarray(test).tolist(),
        coordinate_system="zero-based full-cohort row positions at every level",
        outer=memberships, final_inner=[dict(analysis=development[a].tolist(),
            assessment=development[b].tolist()) for a, b in inner],
        best_parameters=final.best_params_, selected_features=selected_features(final),
        final_search_candidates=summarize_search(final),
        outer_predictions=oof.tolist(), nested_development=scores(y, oof))
    report["mean_outer_permutation_brier_increase"] = np.mean(importance_values, axis=0).tolist()
    report["development_prevalence"] = float(np.mean(y))
    searches = len(memberships) + 1
    candidates = len(final.cv_results_["params"])
    report["tuning_contract"] = dict(selection_metric="neg_brier_score", selection_direction="maximize",
        reported_error="brier", reported_error_direction="minimize", candidates_per_search=candidates,
        inner_folds=final.n_splits_, outer_folds=len(memberships), searches=searches,
        candidate_pipeline_fits=searches * candidates * final.n_splits_,
        refit_pipeline_fits=searches, total_pipeline_fits=searches * (candidates * final.n_splits_ + 1),
        final_test_used_for_selection=False)
    return final, report


def assess(model, data, report):
    validate_cohort(data)
    development, test = np.array(report["development"]), np.array(report["test"])
    check_partition(development, test, data["person_id"])
    prediction = probabilities(model, data["x"][test])
    baseline = np.repeat(report["development_prevalence"], len(test))
    return dict(prediction=prediction.tolist(), metrics=scores(data["y"][test], prediction),
                prevalence_baseline=scores(data["y"][test], baseline))


def feature_review(model, report):
    selected = selected_features(model)
    coefficients = dict(zip(selected, model.best_estimator_.named_steps["model"].coef_[0]))
    rows = []
    for i, feature in enumerate(FEATURES):
        rows.append(dict(feature=str(feature), final_selected=feature in selected,
            standardized_coefficient=float(coefficients[feature]) if feature in selected else "",
            selected_outer_fits=sum(feature in fold["selected_features"] for fold in report["outer"]),
            outer_fits=len(report["outer"]),
            mean_outer_permutation_brier_increase=report["mean_outer_permutation_brier_increase"][i]))
    return sorted(rows, key=lambda row: (-row["mean_outer_permutation_brier_increase"], row["feature"]))


def run(output):
    output = Path(output).absolute()
    root = Path(__file__).resolve().parents[2]
    output = output.parent.resolve(strict=True) / output.name
    if output.exists() or output.is_symlink() or output == root or root in output.parents:
        raise ValueError("Choose a new output directory outside the repository")
    stage = Path(tempfile.mkdtemp(prefix="feature-selection-", dir=output.parent))
    try:
        data = make_cohort()
        development, test = make_plan(data)
        model, report = fit_development(data, development, test)
        report["final_test"] = assess(model, data, report)
        np.savez(stage / "synthetic_inputs.npz", **data)
        joblib.dump(model, stage / "pipeline.joblib")
        (stage / "report.json").write_text(json.dumps(report, indent=2, allow_nan=False))
        rows = feature_review(model, report)
        with (stage / "feature_review.csv").open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        versions = {p: importlib.metadata.version(p) for p in ("numpy", "scipy", "scikit-learn", "joblib")}
        versions["python"] = sys.version
        (stage / "versions.json").write_text(json.dumps(versions, indent=2))
        (stage / "README.txt").write_text(
            "Synthetic paired-specimen tissue-category demonstration; no clinical or named-gene claims.\n"
            "0=comparator; 1=tumor-labeled specimen. Both specimens stay with their person.\n"
            "All split indices are zero-based full-cohort row positions.\n"
            "Candidate fold scores are inner validation Brier errors, not independent test scores.\n"
            "F-scores screen variables only; their p-values are not gene-discovery evidence.\n"
            "Permutation diagnostics use row-wise shuffles on outer assessment specimens.\n"
            "They do not preserve within-person feature dependence or provide confidence intervals.\n"
            "Do not use these diagnostics or final test scores to select a panel and reuse its assessment.\n"
            "Coefficient magnitudes, selection counts and permutation scores are different quantities.\n"
            "Load model bundles only from a trusted source.\n")
        manifest = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sorted(stage.iterdir()) if p.is_file()}
        (stage / "sha256.json").write_text(json.dumps(manifest, indent=2))
        if output.exists() or output.is_symlink():
            raise FileExistsError(output)
        stage.rename(output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    run(parser.parse_args().output)
