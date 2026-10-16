"""Prespecified, bounded robustness and equal-fit tuning comparison on invented assay data.

No reserved-test target, measurement or prediction is used to fit or choose a model.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import itertools
import json
from pathlib import Path
import shutil
import sys
import tempfile
import time

import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss
from sklearn.model_selection import GroupKFold, GroupShuffleSplit, ParameterSampler
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import breast_cancer_comparison as comparison
import breast_cancer_feature_selection as selection

ROOT = Path(__file__).resolve().parents[2]
COHORT_SEED = 26101711
SPLIT_SEED = 26101712
ALTERNATE_SPLIT_SEED = 26101713
PERTURBATION_SEED = 26101714
SEARCH_SEED = 26101715
SCENARIOS = ('reference', 'extra_missingness', 'correlated_measurement', 'reallocated_people')
GRID = tuple((k, c) for c in (0.1, 1.0) for k in (5, 10, 20))
RANDOM_SPACE = {'select__k': (3, 5, 10, 20, 30, 40),
                'model__C': (0.03, 0.1, 0.3, 1.0, 3.0, 10.0)}
CANDIDATE_COUNT = 6
OUTER_FOLDS = 3
INNER_FOLDS = 3
FITS_PER_SEARCH = CANDIDATE_COUNT * INNER_FOLDS + 1
FITS_PER_SCENARIO = 2 * (OUTER_FOLDS + 1) * FITS_PER_SEARCH + OUTER_FOLDS + 1
PREDICTION_FIELDS = ('scenario', 'cohort_row', 'person_id', 'specimen_id', 'label',
                     'outer_fold', 'grid_probability', 'random_probability',
                     'all_feature_probability', 'prevalence_probability')


def candidate_settings(method):
    if method == 'grid':
        return GRID
    if method == 'random':
        draws = list(ParameterSampler(RANDOM_SPACE, n_iter=CANDIDATE_COUNT,
                                      random_state=SEARCH_SEED))
        result = tuple((int(d['select__k']), float(d['model__C'])) for d in draws)
        if len(set(result)) != CANDIDATE_COUNT:
            raise ValueError('Random candidate draw contains duplicates')
        return result
    raise ValueError(f'Unknown search method: {method}')


def make_pipeline(k, c):
    return Pipeline([
        ('impute', SimpleImputer(strategy='median')),
        ('select', SelectKBest(score_func=f_classif, k=k)),
        ('scale', StandardScaler()),
        ('model', LogisticRegression(C=c, max_iter=1000, random_state=selection.SEED)),
    ])


def make_scenario(name, *, cohort_seed=COHORT_SEED, split_seed=SPLIT_SEED,
                  alternate_split_seed=ALTERNATE_SPLIT_SEED,
                  perturbation_seed=PERTURBATION_SEED):
    """Change only development inputs; keep the reserved cohort boundary intact."""
    if name not in SCENARIOS:
        raise ValueError(f'Unknown scenario: {name}')
    data = selection.make_cohort(seed=cohort_seed)
    selection.validate_cohort(data)
    split_seed = alternate_split_seed if name == 'reallocated_people' else split_seed
    development, reserved = next(GroupShuffleSplit(n_splits=1, test_size=0.25,
        random_state=split_seed).split(np.zeros(len(data['person_id'])),
                                     groups=data['person_id']))
    selection.check_partition(development, reserved, data['person_id'])
    original_reserved = data['x'][reserved].copy()
    original_rate = float(np.isnan(data['x'][development]).mean())
    if name == 'extra_missingness':
        rng = np.random.default_rng(perturbation_seed)
        dropout = rng.random(data['x'][development].shape) < 0.15
        changed = data['x'][development].copy()
        changed[dropout] = np.nan
        data['x'][development] = changed
    elif name == 'correlated_measurement':
        rng = np.random.default_rng(perturbation_seed)
        changed = data['x'][development].copy()
        # Feature005 is already correlated with Feature001 in the generator.
        # Increase that relationship without editing labels or held-out people.
        preserved_missing = np.isnan(changed[:, 4])
        changed[:, 4] = 0.99 * changed[:, 0] + rng.normal(0, 0.05, len(changed))
        changed[preserved_missing, 4] = np.nan
        data['x'][development] = changed
    if not np.array_equal(data['x'][reserved], original_reserved, equal_nan=True):
        raise ValueError('Scenario modified reserved measurements')
    selection.validate_cohort(data)
    return data, development, reserved, dict(name=name, cohort_seed=cohort_seed,
        split_seed=split_seed, perturbation_seed=perturbation_seed if name in
        ('extra_missingness', 'correlated_measurement') else None,
        initial_development_missing_fraction=original_rate,
        final_development_missing_fraction=float(np.isnan(data['x'][development]).mean()),
        development_people=int(len(np.unique(data['person_id'][development]))),
        reserved_people=int(len(np.unique(data['person_id'][reserved]))))


def _deadline_guard(deadline):
    # This enforces a pre-fit budget check, not a hard interrupt during one fit.
    if time.monotonic() >= deadline:
        raise TimeoutError('Predeclared wall-clock budget exceeded before a fit')


def search_on_rows(data, rows, method, deadline, candidates=None):
    """Keep a record of every attempted inner candidate/fold fit, including failures."""
    rows = np.asarray(rows, dtype=int)
    x, y, groups = (data['x'][rows], data['y'][rows], data['person_id'][rows])
    if np.isnan(x).all(axis=0).any():
        raise ValueError('A fitting slice has a fully missing measurement')
    inner = list(GroupKFold(INNER_FOLDS).split(x, y, groups))
    inner_memberships = []
    for analysis, assessment in inner:
        selection.check_partition(rows[analysis], rows[assessment], data['person_id'], rows)
        if np.isnan(x[analysis]).all(axis=0).any():
            raise ValueError('An inner analysis slice has a fully missing measurement')
        if any(len(set(y[position])) != 2 for position in (analysis, assessment)):
            raise ValueError('Both specimen categories required in every inner fold')
        inner_memberships.append(dict(analysis=rows[analysis].tolist(),
                                      assessment=rows[assessment].tolist()))
    trial_settings = candidate_settings(method) if candidates is None else tuple(candidates)
    if not trial_settings:
        raise ValueError('At least one search candidate is required')
    history = []
    attempts = failures = 0
    began = time.monotonic()
    for k, c in trial_settings:
        outcomes = []
        for fold, (analysis, assessment) in enumerate(inner):
            _deadline_guard(deadline)
            start = time.monotonic()
            attempts += 1
            result = dict(inner_fold=fold + 1, brier=None, error=None)
            try:
                model = make_pipeline(int(k), float(c)).fit(x[analysis], y[analysis])
                prediction = selection.probabilities(model, x[assessment])
                score = float(brier_score_loss(y[assessment], prediction))
                if not np.isfinite(score):
                    raise ValueError('Nonfinite inner validation loss')
                result['brier'] = score
            except (ValueError, FloatingPointError, RuntimeError) as exc:
                failures += 1
                result['error'] = f'{type(exc).__name__}: {str(exc)[:160]}'
            result['elapsed_seconds'] = round(time.monotonic() - start, 6)
            outcomes.append(result)
        complete = all(item['error'] is None for item in outcomes)
        history.append(dict(parameters={'select__k': int(k), 'model__C': float(c)},
            inner_trials=outcomes, status='complete' if complete else 'failed',
            mean_inner_brier=float(np.mean([r['brier'] for r in outcomes])) if complete else None,
            chosen=False))
    usable = [(candidate['mean_inner_brier'], i) for i, candidate in enumerate(history)
              if candidate['status'] == 'complete']
    if not usable:
        raise ValueError('All candidate settings failed; inspect inner trial histories')
    winner = min(usable)[1]
    history[winner]['chosen'] = True
    parameters = history[winner]['parameters']
    _deadline_guard(deadline)
    attempts += 1
    start = time.monotonic()
    final = make_pipeline(parameters['select__k'], parameters['model__C']).fit(x, y)
    refit_seconds = round(time.monotonic() - start, 6)
    selected = selection.FEATURES[final.named_steps['select'].get_support()].tolist()
    return final, dict(method=method, inner=inner_memberships, candidates=history,
        chosen_parameters=parameters, selected_features=selected, attempted_fits=attempts,
        failed_fits=failures, successful_fits=attempts - failures,
        refit_seconds=refit_seconds, elapsed_seconds=round(time.monotonic() - began, 6))


def _jaccard(a, b):
    a, b = set(a), set(b)
    return float(len(a & b) / len(a | b)) if a or b else 1.0


def panel_stability(panels):
    comparisons = [_jaccard(a, b) for a, b in itertools.combinations(panels, 2)]
    return dict(outer_fits=len(panels), pairwise_jaccard=comparisons,
        mean_pairwise_jaccard=float(np.mean(comparisons)) if comparisons else None,
        selected_outer_frequency={str(feature): sum(feature in p for p in panels)
                                  for feature in selection.FEATURES})


def evaluate_scenario(name, deadline):
    data, development, reserved, config = make_scenario(name)
    groups, y = data['person_id'], data['y']
    outer = list(GroupKFold(OUTER_FOLDS).split(data['x'][development],
                                             y[development], groups[development]))
    predictions = {method: np.full(len(development), np.nan)
                   for method in ('grid', 'random', 'all_feature', 'prevalence')}
    fold_numbers = np.zeros(len(development), dtype=int)
    histories = {'grid': [], 'random': []}
    fixed_fits = 0
    began = time.monotonic()
    memberships = []
    for fold, (analysis_local, assessment_local) in enumerate(outer, start=1):
        analysis, assessment = development[analysis_local], development[assessment_local]
        selection.check_partition(analysis, assessment, groups, development)
        memberships.append(dict(analysis=analysis.tolist(), assessment=assessment.tolist()))
        fold_numbers[assessment_local] = fold
        for method in ('grid', 'random'):
            model, trial = search_on_rows(data, analysis, method, deadline)
            predictions[method][assessment_local] = selection.probabilities(model,
                                                                             data['x'][assessment])
            histories[method].append(trial)
        _deadline_guard(deadline)
        fixed = comparison.fit_all_features(data['x'][analysis], y[analysis])
        fixed_fits += 1
        predictions['all_feature'][assessment_local] = selection.probabilities(
            fixed, data['x'][assessment])
        predictions['prevalence'][assessment_local] = float(np.mean(y[analysis]))
    if not np.array_equal(np.sort(np.concatenate([np.array(m['assessment']) for m in memberships])),
                          np.sort(development)) or np.any(fold_numbers == 0):
        raise ValueError('Outer folds do not cover development people exactly once')
    for method in predictions:
        if not np.isfinite(predictions[method]).all():
            raise ValueError(f'Incomplete outer predictions for {method}')
    final_panels = {}
    for method in ('grid', 'random'):
        _, trial = search_on_rows(data, development, method, deadline)
        histories[method].append(trial)
        final_panels[method] = trial['selected_features']
    _deadline_guard(deadline)
    comparison.fit_all_features(data['x'][development], y[development])
    fixed_fits += 1
    count = sum(t['attempted_fits'] for method in histories for t in histories[method]) + fixed_fits
    failed = sum(t['failed_fits'] for method in histories for t in histories[method])
    if count != FITS_PER_SCENARIO or failed:
        # Any attempted refit still counts; this protocol fails closed on partial candidates.
        raise ValueError(f'Fit budget or candidate-failure gate: attempts={count}, failed={failed}')
    metrics = {method: selection.scores(y[development], values)
               for method, values in predictions.items()}
    contrast = {key: float(np.mean((predictions[key] - y[development]) ** 2 -
                                   (predictions['grid'] - y[development]) ** 2))
                for key in ('random', 'all_feature', 'prevalence')}
    person_rows = [np.flatnonzero(groups[development] == person)
                   for person in sorted(np.unique(groups[development]))]
    person_differences = [float(np.mean((predictions['grid'][idx] - y[development][idx]) ** 2 -
                                        (predictions['random'][idx] - y[development][idx]) ** 2))
                          for idx in person_rows]
    if not np.isclose(np.mean(person_differences), -contrast['random'], atol=1e-12):
        raise ValueError('Person-unit and specimen-unit losses disagree')
    rows = [dict(zip(PREDICTION_FIELDS, (name, int(row), int(groups[row]),
        str(data['specimen_id'][row]), int(y[row]), int(fold_numbers[i]),
        *(float(predictions[method][i]) for method in
          ('grid', 'random', 'all_feature', 'prevalence')))))
        for i, row in enumerate(development)]
    report = dict(**config, development=development.tolist(), reserved=reserved.tolist(),
        outer=memberships, fit_budget=dict(maximum=FITS_PER_SCENARIO, attempted=count,
                                           failed=failed, worker_count=1),
        development_metrics=metrics,
        comparison_vs_grid_brier=contrast,
        grid_minus_random_person_brier=person_differences,
        final_panels=final_panels, searches=histories,
        stability={m: panel_stability([trial['selected_features'] for trial in histories[m][:-1]])
                   for m in histories},
        elapsed_seconds=round(time.monotonic() - began, 3),
        interpretation='Overlapping invented people and conditional outer-fold predictions; '
                       'descriptive software experiment, not patient-level inference or gene discovery')
    return report, rows


def _sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(output, scenarios=SCENARIOS, max_fits=624, max_seconds=900):
    """Write a newly named, checksummed run directory outside the source repository."""
    scenarios = tuple(scenarios)
    if not scenarios or len(set(scenarios)) != len(scenarios) or any(s not in SCENARIOS for s in scenarios):
        raise ValueError('Scenarios must be nonempty, unique, and prespecified')
    planned = len(scenarios) * FITS_PER_SCENARIO
    if planned > max_fits or max_fits <= 0 or not np.isfinite(max_seconds) or max_seconds <= 0:
        raise ValueError(f'Preflight budget rejected {planned} planned fits')
    output = Path(output).absolute()
    output = output.parent.resolve(strict=True) / output.name
    if output.exists() or output.is_symlink() or output == ROOT or ROOT in output.parents:
        raise ValueError('Choose a new output directory outside the repository')
    stage = Path(tempfile.mkdtemp(prefix='assay-robustness-', dir=output.parent))
    begun = time.monotonic()
    deadline = begun + max_seconds
    try:
        observed, predictions = {}, []
        for name in scenarios:
            observed[name], rows = evaluate_scenario(name, deadline)
            predictions.extend(rows)
        for method in ('grid', 'random'):
            for a, b in itertools.combinations(scenarios, 2):
                observed[a].setdefault('cross_scenario_final_panel_jaccard', {}).setdefault(
                    method, {})[b] = _jaccard(observed[a]['final_panels'][method],
                                               observed[b]['final_panels'][method])
        seconds = round(time.monotonic() - begun, 3)
        if seconds > max_seconds:
            raise TimeoutError('Declared wall-clock budget exceeded')
        report = dict(protocol_id='paired-assay-robustness-v1', status='software_pass',
            purpose='Synthetic stress testing of a specimen-category classifier; not clinical validation',
            scenarios=list(scenarios), scenario_results=observed,
            budget=dict(max_fits=max_fits, planned_fits=planned,
                actual_fits=sum(v['fit_budget']['attempted'] for v in observed.values()),
                max_seconds=max_seconds, observed_seconds=seconds, worker_count=1),
            selection_contract=dict(inner_folds=INNER_FOLDS, outer_folds=OUTER_FOLDS,
                metric='Brier error', lower_is_better=True, grid_candidates=list(GRID),
                random_candidate_space=RANDOM_SPACE,
                random_candidates=list(candidate_settings('random')),
                candidates_per_search=CANDIDATE_COUNT,
                test_predictions_generated=False, test_used_for_selection=False,
                failed_candidate_policy='Record every failed inner trial; abort complete '
                                        'phase gate instead of ignoring failed search candidates'),
            source_sha256={str(path.relative_to(ROOT)): _sha256(path) for path in (
                Path(__file__), Path(selection.__file__), Path(comparison.__file__),
                ROOT / '04_machine_learning/robustness-protocol.md')})
        (stage / 'report.json').write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
        with (stage / 'development_predictions.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=PREDICTION_FIELDS)
            writer.writeheader()
            writer.writerows(sorted(predictions, key=lambda r: (r['scenario'], r['cohort_row'])))
        versions = {p: importlib.metadata.version(p) for p in
                    ('numpy', 'scipy', 'scikit-learn', 'joblib')}
        versions['python'] = sys.version
        (stage / 'versions.json').write_text(json.dumps(versions, indent=2) + '\n')
        (stage / 'README.txt').write_text(
            'INVENTED DATA ONLY. The withheld test was not evaluated in this Phase 4 run.\n'
            'All rows in development_predictions.csv are outer-held-out development specimens.\n'
            'Model selection uses disjoint-person inner folds; Brier error is lower-is-better.\n'
            'The reported fit counts include every candidate/fold fit and final refit.\n'
            'Times depend on the execution environment and do not imply speed superiority.\n'
            'Panels are descriptive, not gene findings. No clinical intervals are claimed.\n')
        manifest = {p.name: _sha256(p) for p in sorted(stage.iterdir()) if p.is_file()}
        (stage / 'sha256.json').write_text(json.dumps(manifest, indent=2) + '\n')
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
    parser.add_argument('--scenario', choices=SCENARIOS, action='append', dest='scenarios')
    parser.add_argument('--max-fits', type=int, default=624)
    parser.add_argument('--max-seconds', type=float, default=900)
    args = parser.parse_args()
    run(args.output, scenarios=args.scenarios or SCENARIOS,
        max_fits=args.max_fits, max_seconds=args.max_seconds)
