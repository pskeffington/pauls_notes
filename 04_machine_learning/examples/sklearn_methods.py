"""Independent scikit-learn workflows; synthetic data, no caret dependency."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
from pathlib import Path
import shutil
import tempfile
import time

import joblib
import numpy as np
from sklearn.base import clone
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier, RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import (average_precision_score, brier_score_loss, mean_absolute_error,
    mean_squared_error, r2_score, roc_auc_score, silhouette_score)
from sklearn.model_selection import GridSearchCV, GroupKFold, GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def make_cohort(seed=260419, families=60):
    if not isinstance(families, int) or families < 30:
        raise ValueError("At least 30 synthetic families required")
    rng = np.random.default_rng(seed)
    groups = np.repeat(np.arange(families), 2)
    x = rng.normal(size=(len(groups), 5))
    family_effect = rng.normal(scale=0.3, size=families)[groups]
    risk = 1 / (1 + np.exp(-(x[:, 0] - 0.6 * x[:, 1] + family_effect)))
    classification = (rng.random(len(groups)) < risk).astype(int)
    regression = 2 * x[:, 0] - x[:, 1] + family_effect + rng.normal(scale=0.7, size=len(groups))
    x[rng.random(x.shape) < 0.04] = np.nan
    return dict(x=x, classification=classification, regression=regression,
                groups=groups, person_id=np.arange(len(groups)))


def validate_cohort(data):
    x = np.asarray(data["x"])
    if x.ndim != 2 or x.shape[1] != 5 or len(x) < 60 or not np.issubdtype(x.dtype, np.number):
        raise ValueError("Expected at least 60 people and five numeric predictors")
    if np.isinf(x).any() or np.isnan(x).all(axis=0).any():
        raise ValueError("Infinite or entirely unavailable predictor")
    for key in ("classification", "regression", "groups", "person_id"):
        values = np.asarray(data[key])
        if values.shape != (len(x),) or not np.isfinite(values).all():
            raise ValueError(f"Invalid aligned field: {key}")
    if len(np.unique(data["person_id"])) != len(x):
        raise ValueError("Person identifiers must be unique")
    if set(np.unique(data["classification"])) != {0, 1}:
        raise ValueError("Both binary classes required; 1 is the positive event")


def check_partition(train, test, groups, universe=None):
    train, test = np.asarray(train), np.asarray(test)
    expected = np.arange(len(groups)) if universe is None else np.asarray(universe)
    if (train.ndim != 1 or test.ndim != 1 or not len(train) or not len(test)
        or not np.issubdtype(train.dtype, np.integer) or not np.issubdtype(test.dtype, np.integer)
        or len(np.unique(train)) != len(train) or len(np.unique(test)) != len(test)
        or not np.array_equal(np.sort(np.concatenate([train, test])), np.sort(expected))):
        raise ValueError("Rows must partition the specified universe exactly")
    if set(groups[train]) & set(groups[test]):
        raise ValueError("Family leakage across partitions")


def make_plan(data):
    validate_cohort(data)
    train, test = next(GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=173).split(
        data["x"], data["classification"], data["groups"]))
    check_partition(train, test, data["groups"])
    for rows in (train, test):
        if len(np.unique(data["classification"][rows])) != 2:
            raise ValueError("Both classes required in each partition")
    return train, test


def model_specs(task):
    if task == "classification":
        return {
            "logistic": (LogisticRegression(max_iter=1000, random_state=173), {"model__C": [0.1, 1.0]}),
            "forest": (RandomForestClassifier(n_estimators=50, random_state=173, n_jobs=1),
                       {"model__min_samples_leaf": [3, 8]}),
            "boosting": (HistGradientBoostingClassifier(max_iter=50, early_stopping=False, random_state=173),
                         {"model__max_leaf_nodes": [3, 7]}),
        }
    if task == "regression":
        return {
            "ridge": (Ridge(), {"model__alpha": [0.1, 1.0, 10.0]}),
            "forest": (RandomForestRegressor(n_estimators=50, random_state=173, n_jobs=1),
                       {"model__min_samples_leaf": [3, 8]}),
        }
    raise ValueError("Unknown task")


def pipeline(model):
    return Pipeline([("impute", SimpleImputer(strategy="median")),
                     ("scale", StandardScaler()), ("model", model)])


def fit_search(x, y, groups, task, spec):
    estimator, grid = spec
    folds = list(GroupKFold(n_splits=3).split(x, y, groups))
    for train, test in folds:
        check_partition(train, test, groups)
        if task == "classification" and any(len(np.unique(y[rows])) != 2 for rows in (train, test)):
            raise ValueError("Both classes required within grouped folds")
        if np.isnan(x[train]).all(axis=0).any():
            raise ValueError("A training fold has an entirely missing predictor")
    search = GridSearchCV(pipeline(clone(estimator)), grid, cv=folds, n_jobs=1,
        scoring="neg_brier_score" if task == "classification" else "neg_mean_squared_error",
        error_score="raise", refit=True)
    search.fit(x, y)
    return search, folds


def predict_task(model, x, task):
    return model.predict_proba(x)[:, list(model.classes_).index(1)] if task == "classification" else model.predict(x)


def metrics(y, prediction, task):
    if task == "classification":
        return dict(roc_auc=float(roc_auc_score(y, prediction)),
            average_precision=float(average_precision_score(y, prediction)),
            brier=float(brier_score_loss(y, prediction)))
    return dict(rmse=float(np.sqrt(mean_squared_error(y, prediction))),
        mae=float(mean_absolute_error(y, prediction)), r2=float(r2_score(y, prediction)))


def fit_supervised(data, train, test, task):
    validate_cohort(data); check_partition(train, test, data["groups"])
    x, y, groups = data["x"][train], data[task][train], data["groups"][train]
    outer = list(GroupKFold(n_splits=3).split(x, y, groups))
    results, saved = {}, {}
    for name, spec in model_specs(task).items():
        started = time.perf_counter()
        oof = np.full(len(train), np.nan)
        memberships = []
        for fold, (analysis, assessment) in enumerate(outer):
            check_partition(analysis, assessment, groups)
            search, inner = fit_search(x[analysis], y[analysis], groups[analysis], task, spec)
            oof[assessment] = predict_task(search, x[assessment], task)
            memberships.append(dict(outer=fold, analysis=analysis.tolist(), assessment=assessment.tolist(),
                inner=[dict(analysis=analysis[a].tolist(), assessment=analysis[b].tolist()) for a, b in inner]))
        if not np.isfinite(oof).all():
            raise ValueError("Every development person needs an outer-held-out prediction")
        final, inner = fit_search(x, y, groups, task, spec)
        prediction = predict_task(final, data["x"][test], task)
        results[name] = dict(nested_development=metrics(y, oof, task),
            test=metrics(data[task][test], prediction, task),
            best_parameters=final.best_params_, elapsed_seconds=time.perf_counter()-started,
            outer_memberships=memberships, final_inner=[dict(analysis=a.tolist(), assessment=b.tolist()) for a, b in inner],
            oof_prediction=oof.tolist(), test_prediction=prediction.tolist())
        saved[name] = final
    baseline = (np.repeat(np.mean(y), len(test)))
    results["development_mean_baseline"] = dict(test=metrics(data[task][test], baseline, task))
    return results, saved


def fit_unsupervised(data, train, test):
    validate_cohort(data); check_partition(train, test, data["groups"])
    transform = Pipeline([("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()), ("pca", PCA(n_components=2, svd_solver="full"))])
    development = transform.fit_transform(data["x"][train])
    assessment = transform.transform(data["x"][test])
    model = KMeans(n_clusters=3, n_init=10, random_state=173).fit(development)
    labels = model.predict(assessment)
    distinct = len(np.unique(labels))
    silhouette = float(silhouette_score(assessment, labels)) if 1 < distinct < len(labels) else None
    return dict(explained_variance_ratio=transform.named_steps["pca"].explained_variance_ratio_.tolist(),
        test_projection=assessment.tolist(), test_cluster=labels.tolist(),
        test_silhouette=silhouette, n_clusters_prespecified=3), dict(transform=transform, model=model)


def run(output):
    output = Path(output).absolute()
    root = Path.cwd().resolve()
    parent = output.parent.resolve(strict=True)
    output = parent / output.name
    if output.exists() or output == root or root in output.parents:
        raise ValueError("Choose a new output directory outside the repository")
    stage = Path(tempfile.mkdtemp(prefix="methods-stage-", dir=parent))
    try:
        data = make_cohort(); train, test = make_plan(data)
        report, models = {}, {}
        for task in ("classification", "regression"):
            report[task], models[task] = fit_supervised(data, train, test, task)
        report["unsupervised"], models["unsupervised"] = fit_unsupervised(data, train, test)
        np.savez(stage / "synthetic_cohort.npz", **data)
        joblib.dump(models, stage / "models.joblib")
        (stage / "metrics.json").write_text(json.dumps(report, indent=2, allow_nan=False))
        (stage / "splits.json").write_text(json.dumps(dict(development=train.tolist(), test=test.tolist(),
            person_id=data["person_id"].tolist(), family_id=data["groups"].tolist()), indent=2))
        (stage / "versions.json").write_text(json.dumps({p: importlib.metadata.version(p)
            for p in ("numpy", "scipy", "scikit-learn", "joblib")}, indent=2))
        (stage / "README.txt").write_text("Synthetic methods checks only. Family-disjoint nested CV; no clinical claims.\n"
            "Do not choose the winning model from the final test scores.\n"
            "Clustering and silhouette are exploratory, not phenotype validation.\n")
        if output.exists():
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
