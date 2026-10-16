"""Compare two prespecified synthetic assay pipelines on identical held-out people."""
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
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import breast_cancer_feature_selection as selection

ROOT = Path(__file__).resolve().parents[2]
COHORT_SEED = 26101602
SPLIT_SEED = 26101603
FIXED_C = 1.0
PREDICTION_FIELDS = ['cohort_row', 'person_id', 'specimen_id', 'label', 'partition', 'outer_fold',
                     'selected_probability', 'all_feature_probability', 'prevalence_probability',
                     'selected_squared_error', 'all_feature_squared_error', 'prevalence_squared_error']


def make_plan(data):
    selection.validate_cohort(data)
    development, test = next(GroupShuffleSplit(n_splits=1, test_size=0.25,
        random_state=SPLIT_SEED).split(data['x'], data['y'], data['person_id']))
    selection.check_partition(development, test, data['person_id'])
    return development, test


def fit_all_features(x, y):
    if np.isnan(x).all(axis=0).any():
        raise ValueError('A comparator training column is completely missing')
    model = Pipeline([
        ('impute', SimpleImputer(strategy='median')),
        ('scale', StandardScaler()),
        ('model', LogisticRegression(C=FIXED_C, max_iter=1000, random_state=selection.SEED)),
    ])
    return model.fit(x, y)


def fit_development(data, development, test):
    """Learn both procedures; return development evidence only."""
    selected, selected_report = selection.fit_development(data, development, test)
    lookup = {int(row): i for i, row in enumerate(development)}
    all_probability = np.full(len(development), np.nan)
    prevalence_probability = np.full(len(development), np.nan)
    for fold in selected_report['outer']:
        analysis, assessment = np.array(fold['analysis']), np.array(fold['assessment'])
        selection.check_partition(analysis, assessment, data['person_id'], development)
        model = fit_all_features(data['x'][analysis], data['y'][analysis])
        positions = [lookup[int(row)] for row in assessment]
        all_probability[positions] = selection.probabilities(model, data['x'][assessment])
        prevalence_probability[positions] = np.mean(data['y'][analysis])
    if not np.isfinite(all_probability).all():
        raise ValueError('Missing all-feature outer predictions')
    fixed = fit_all_features(data['x'][development], data['y'][development])
    y = data['y'][development]
    selected_fits = selected_report['tuning_contract']['total_pipeline_fits']
    fixed_fits = len(selected_report['outer']) + 1
    report = dict(protocol_id='paired-comparison-v1', model_seed=selection.SEED,
        contrast='Tuned subset/C procedure versus fixed C=1 all-feature procedure; '
                 'not an isolated feature-selection effect',
        primary_loss='binary Brier error; lower is better',
        selected=selected_report,
        all_features=dict(C=FIXED_C, feature_count=len(selection.FEATURES),
            outer_predictions=all_probability.tolist(), nested_development=selection.scores(y, all_probability)),
        prevalence=dict(outer_predictions=prevalence_probability.tolist(),
            nested_development=selection.scores(y, prevalence_probability)),
        development_brier_difference=float(np.mean(
            (np.array(selected_report['outer_predictions']) - y) ** 2 - (all_probability - y) ** 2)),
        pipeline_fits=dict(selected=selected_fits, all_features=fixed_fits,
                           total=selected_fits + fixed_fits), final_test_used_for_selection=False)
    return {'selected': selected, 'all_features': fixed}, report


def assess(models, data, report):
    selected = report['selected']
    development, test = np.array(selected['development']), np.array(selected['test'])
    selection.validate_cohort(data)
    selection.check_partition(development, test, data['person_id'])
    y = data['y'][test]
    results = {}
    for name, model in models.items():
        p = selection.probabilities(model, data['x'][test])
        results[name] = dict(prediction=p.tolist(), metrics=selection.scores(y, p))
    p = np.full(len(test), selected['development_prevalence'])
    results['prevalence'] = dict(prediction=p.tolist(), metrics=selection.scores(y, p))
    results['brier_difference'] = float(np.mean(
        (np.array(results['selected']['prediction']) - y) ** 2 -
        (np.array(results['all_features']['prediction']) - y) ** 2))
    return results


def prediction_rows(data, report):
    selected = report['selected']
    fold_by_row = {row: i + 1 for i, fold in enumerate(selected['outer']) for row in fold['assessment']}
    rows = []
    for partition in ('development', 'test'):
        for position, row in enumerate(selected[partition]):
            if partition == 'development':
                ps = [selected['outer_predictions'][position],
                      report['all_features']['outer_predictions'][position],
                      report['prevalence']['outer_predictions'][position]]
            else:
                ps = [report['final_test'][name]['prediction'][position]
                      for name in ('selected', 'all_features', 'prevalence')]
            y = int(data['y'][row])
            values = [row, int(data['person_id'][row]), str(data['specimen_id'][row]), y,
                      partition, fold_by_row.get(row, ''), *ps, *[(p - y) ** 2 for p in ps]]
            rows.append(dict(zip(PREDICTION_FIELDS, values)))
    return sorted(rows, key=lambda r: r['cohort_row'])


def run(output):
    output = Path(output).absolute()
    output = output.parent.resolve(strict=True) / output.name
    if output.exists() or output.is_symlink() or output == ROOT or ROOT in output.parents:
        raise ValueError('Choose a new output directory outside the repository')
    stage = Path(tempfile.mkdtemp(prefix='assay-comparison-', dir=output.parent))
    try:
        data = selection.make_cohort(seed=COHORT_SEED)
        development, test = make_plan(data)
        models, report = fit_development(data, development, test)
        report.update(cohort_seed=COHORT_SEED, split_seed=SPLIT_SEED)
        report['final_test'] = assess(models, data, report)
        sources = [Path(__file__), Path(selection.__file__), Path(__file__).with_name('plot_comparison.py'),
                   ROOT / '04_machine_learning/comparison-protocol.md']
        report['source_sha256'] = {str(p.resolve().relative_to(ROOT)):
                                  hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
        (stage / 'report.json').write_text(json.dumps(report, indent=2, allow_nan=False))
        with (stage / 'predictions.csv').open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=PREDICTION_FIELDS)
            writer.writeheader()
            writer.writerows(prediction_rows(data, report))
        np.savez(stage / 'synthetic_inputs.npz', **data)
        joblib.dump(models, stage / 'models.joblib')
        versions = {p: importlib.metadata.version(p)
                    for p in ('numpy', 'scipy', 'scikit-learn', 'joblib', 'matplotlib')}
        versions['python'] = sys.version
        (stage / 'versions.json').write_text(json.dumps(versions, indent=2))
        from plot_comparison import render_gallery
        render_gallery(stage, stage / 'gallery')
        (stage / 'README.txt').write_text(
            'Invented paired specimens; no participant data or named-gene effects.\n'
            'Both models predict the same excluded people; neither is selected from final-test results.\n'
            'The contrast changes selection AND tuning; no isolated selection benefit is claimed.\n'
            'Report differences are descriptive; figures contain no clinical confidence intervals.\n'
            'Load only trusted, repository-generated model bundles.\n')
        manifest = {str(p.relative_to(stage)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sorted(stage.rglob('*')) if p.is_file()}
        (stage / 'sha256.json').write_text(json.dumps(manifest, indent=2))
        if output.exists() or output.is_symlink():
            raise FileExistsError(output)
        stage.rename(output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    run(parser.parse_args().output)
