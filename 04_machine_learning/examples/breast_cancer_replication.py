"""Frozen Phase 4B internal synthetic replication; never scores reserved people."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import itertools
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Any
import warnings

import numpy as np
from scipy.stats import rankdata
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_selection import f_classif
from sklearn.model_selection import GroupKFold

import breast_cancer_comparison as comparison
import breast_cancer_feature_selection as selection
import breast_cancer_robustness as legacy

ROOT = legacy.ROOT
FREEZE = '65a0b8776a876c0a845e6f9f57c067adb30f713e'
PROTOCOL = ROOT / '04_machine_learning/replication-protocol.md'
CONTRACT = ROOT / '04_machine_learning/evidence/replication-contract-v1.json'
METHODS = ('grid', 'random', 'all_feature', 'prevalence')
FEATURES = selection.FEATURES.tolist()
SOURCES = (Path(__file__), Path(legacy.__file__), Path(selection.__file__),
           Path(comparison.__file__), ROOT / '04_machine_learning/requirements-python.txt')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    temporary.replace(path)


def frozen_contract() -> dict[str, Any]:
    """Enforce the actual committed contract rather than trusting a mutable label."""
    for path in (PROTOCOL, CONTRACT):
        original = subprocess.check_output(['git', '-C', str(ROOT), 'show',
                                           f'{FREEZE}:{path.relative_to(ROOT)}'])
        if original != path.read_bytes():
            raise ValueError('Protocol/config bytes differ from the declared freeze')
    config = json.loads(CONTRACT.read_text())
    if (config['grid_order'] != [list(x) for x in legacy.GRID]
            or config['random_space'] != {k: list(v) for k, v in legacy.RANDOM_SPACE.items()}
            or config['search_seed'] != legacy.SEARCH_SEED
            or config['fits_per_cell'] != legacy.FITS_PER_SCENARIO):
        raise ValueError('Implementation no longer matches the frozen candidate contract')
    return config


def feature_details(model: Any, x: np.ndarray, y: np.ndarray) -> dict[str, Any]:
    """F ranks and coefficient signs come exclusively from this fit's analysis rows."""
    imputed = model.named_steps['impute'].transform(x)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        scores, _ = f_classif(imputed, y)
    valid = np.isfinite(scores)
    ranks = np.full(len(FEATURES), np.nan)
    ranks[valid] = rankdata(-scores[valid], method='average')
    panel = (selection.FEATURES[model.named_steps['select'].get_support()].tolist()
             if 'select' in model.named_steps else FEATURES.copy())
    coefficients = dict(zip(panel, map(float, model.named_steps['model'].coef_[0])))
    if not all(np.isfinite(list(coefficients.values()))):
        raise ValueError('Nonfinite fitted coefficients')
    return dict(selected_features=panel, coefficients=coefficients,
        ranks={f: float(r) if np.isfinite(r) else None for f, r in zip(FEATURES, ranks)},
        undefined_rank_reasons={f: 'nonfinite fitting-only F score' for f, r in
                                zip(FEATURES, ranks) if not np.isfinite(r)},
        diagnostic_warnings=[f'{w.category.__name__}: {w.message}' for w in caught])


class FitLedger:
    """Flush attempt/terminal events before proceeding; retain partial failed runs."""

    def __init__(self, output: Path, max_fits: int, deadline: float):
        self.output, self.max_fits, self.deadline = output, max_fits, deadline
        self.records: list[dict[str, Any]] = []

    def fit(self, data: dict[str, np.ndarray], analysis: np.ndarray,
            assessment: np.ndarray, *, method: str, parameters: dict[str, Any],
            identity: dict[str, Any]) -> tuple[Any, dict[str, Any]]:
        if time.monotonic() >= self.deadline or len(self.records) >= self.max_fits:
            raise TimeoutError('Pre-fit time/attempt budget exhausted')
        if np.isnan(data['x'][analysis]).all(axis=0).any():
            raise ValueError('Completely missing analysis measurement')
        record = dict(fit_id=len(self.records) + 1, **identity, method=method,
            parameters=parameters, analysis=analysis.tolist(), assessment=assessment.tolist(),
            status='started', error=None, warnings=[], elapsed_seconds=0.0)
        self.records.append(record)
        self._event(record)
        started = time.monotonic()
        caught: list[Any] = []
        try:
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter('always')
                warnings.simplefilter('error', ConvergenceWarning)
                x, y = data['x'][analysis], data['y'][analysis]
                model = (comparison.fit_all_features(x, y) if method == 'all_feature' else
                         legacy.make_pipeline(parameters['select__k'], parameters['model__C']).fit(x, y))
                # The diagnostic never receives outer/inner assessment measurements.
                record.update(feature_details(model, x, y))
                if len(assessment):
                    probability = selection.probabilities(model, data['x'][assessment])
                    if (not np.isfinite(probability).all() or
                            np.any((probability < 0) | (probability > 1))):
                        raise ValueError('Invalid assessment probabilities')
                    record['probabilities'] = probability.tolist()
                    record['brier'] = float(np.mean((probability - data['y'][assessment]) ** 2))
                record['status'] = 'complete'
        except Exception as exc:
            record.update(status='failed', error=f'{type(exc).__name__}: {exc}')
            raise
        finally:
            record['warnings'] = [f'{w.category.__name__}: {w.message}' for w in caught]
            record['elapsed_seconds'] = time.monotonic() - started
            self._event(record)
        return model, record

    def _event(self, record: dict[str, Any]) -> None:
        with (self.output / 'fit-events.jsonl').open('a', encoding='utf-8') as handle:
            handle.write(json.dumps(record, allow_nan=False) + '\n')
            handle.flush()
            os.fsync(handle.fileno())


def search(data: dict[str, np.ndarray], rows: np.ndarray, method: str,
           ledger: FitLedger, identity: dict[str, Any], history: dict[str, Any],
           candidates: Any = None) -> tuple[Any, dict[str, Any]]:
    folds = list(GroupKFold(3).split(data['x'][rows], data['y'][rows], data['person_id'][rows]))
    history.update(method=method, inner=[], candidates=[])
    for analysis, assessment in folds:
        selection.check_partition(rows[analysis], rows[assessment], data['person_id'], rows)
        history['inner'].append(dict(analysis=rows[analysis].tolist(), assessment=rows[assessment].tolist()))
    settings = legacy.candidate_settings(method) if candidates is None else candidates
    for candidate, (k, c) in enumerate(settings):
        parameters = {'select__k': int(k), 'model__C': float(c)}
        trial = dict(parameters=parameters, fit_ids=[], mean_inner_brier=None, chosen=False)
        history['candidates'].append(trial)
        outcomes = []
        for inner_fold, (analysis, assessment) in enumerate(folds, start=1):
            before = len(ledger.records)
            try:
                _, record = ledger.fit(data, rows[analysis], rows[assessment], method=method,
                    parameters=parameters, identity=dict(**identity, role='inner_candidate',
                        candidate_index=candidate, inner_fold=inner_fold))
                outcomes.append(record['brier'])
            except (ValueError, RuntimeError, FloatingPointError, ConvergenceWarning):
                outcomes.append(None)
            finally:
                trial['fit_ids'].extend(r['fit_id'] for r in ledger.records[before:])
        trial['status'] = 'complete' if all(v is not None for v in outcomes) else 'failed'
        if trial['status'] == 'complete':
            trial['mean_inner_brier'] = float(np.mean(outcomes))
    usable = [(t['mean_inner_brier'], i) for i, t in enumerate(history['candidates'])
              if t['status'] == 'complete']
    if not usable:
        raise ValueError('All candidate settings failed; retained histories contain errors')
    chosen = history['candidates'][min(usable)[1]]
    chosen['chosen'] = True
    model, record = ledger.fit(data, rows, np.array([], dtype=int), method=method,
        parameters=chosen['parameters'], identity=dict(**identity,
            role='outer_refit' if identity['outer_fold'] else 'development_refit',
            candidate_index=None, inner_fold=None))
    history.update(chosen_parameters=chosen['parameters'], refit_id=record['fit_id'])
    return model, record


def person_losses(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    people: dict[int, list[dict[str, Any]]] = {}
    for row in rows:
        people.setdefault(row['person_id'], []).append(row)
    results = []
    for person, pair in sorted(people.items()):
        if (len(pair) != 2 or {r['label'] for r in pair} != {0, 1} or
                len({r['specimen_id'] for r in pair}) != 2 or
                len({r['outer_fold'] for r in pair}) != 1):
            raise ValueError('Invalid paired-person prediction structure')
        losses = {m: float(np.mean([(r[f'{m}_probability'] - r['label']) ** 2 for r in pair]))
                  for m in METHODS}
        results.append(dict(person_id=person, losses=losses,
            other_minus_grid={m: losses[m] - losses['grid'] for m in METHODS[1:]}))
    return results


def evaluate_cell(cohort: dict[str, Any], scenario: str, ledger: FitLedger,
                  cell: dict[str, Any], predictions: list[dict[str, Any]]) -> None:
    seeds = {k: v for k, v in cohort.items() if k != 'cohort_id'}
    data, development, reserved, config = legacy.make_scenario(scenario, **seeds)
    selection.validate_cohort(data)
    cell.update(cohort_id=cohort['cohort_id'], scenario=scenario, config=config,
        development=development.tolist(), reserved=reserved.tolist(),
        person_id=data['person_id'].tolist(), specimen_id=data['specimen_id'].tolist(),
        labels=data['y'].tolist(), outer=[], searches=[], status='running')
    input_name = f"inputs-{cohort['cohort_id']}-{scenario}.npz"
    np.savez(ledger.output / input_name, **data)
    cell['input_file'] = input_name
    cell['input_sha256'] = digest(ledger.output / input_name)
    if scenario == 'reallocated_people':
        _, original, _, _ = legacy.make_scenario('reference', **seeds)
        if np.array_equal(development, original):
            raise ValueError('Declared reallocation seed did not change membership')
    first_fit = len(ledger.records)
    first_prediction = len(predictions)
    splits = list(GroupKFold(3).split(data['x'][development], data['y'][development],
                                    data['person_id'][development]))
    for outer_fold, (a, b) in enumerate(splits, start=1):
        analysis, assessment = development[a], development[b]
        selection.check_partition(analysis, assessment, data['person_id'], development)
        cell['outer'].append(dict(analysis=analysis.tolist(), assessment=assessment.tolist()))
        identity = dict(cohort_id=cohort['cohort_id'], scenario=scenario, outer_fold=outer_fold)
        probability = {}
        for method in ('grid', 'random'):
            history: dict[str, Any] = dict(outer_fold=outer_fold)
            cell['searches'].append(history)
            model, _ = search(data, analysis, method, ledger, identity, history)
            probability[method] = selection.probabilities(model, data['x'][assessment])
        _, fixed = ledger.fit(data, analysis, assessment, method='all_feature', parameters={'model__C': 1.0},
            identity=dict(**identity, role='fixed_outer', candidate_index=None, inner_fold=None))
        probability['all_feature'] = fixed['probabilities']
        probability['prevalence'] = np.full(len(assessment), np.mean(data['y'][analysis]))
        for i, row in enumerate(assessment):
            predictions.append(dict(cohort_id=cohort['cohort_id'], scenario=scenario,
                cohort_row=int(row), person_id=int(data['person_id'][row]),
                specimen_id=str(data['specimen_id'][row]), label=int(data['y'][row]), outer_fold=outer_fold,
                **{f'{m}_probability': float(probability[m][i]) for m in METHODS}))
    for method in ('grid', 'random'):
        history = dict(outer_fold=0)
        cell['searches'].append(history)
        search(data, development, method, ledger,
            dict(cohort_id=cohort['cohort_id'], scenario=scenario, outer_fold=0), history)
    ledger.fit(data, development, np.array([], dtype=int), method='all_feature', parameters={'model__C': 1.0},
        identity=dict(cohort_id=cohort['cohort_id'], scenario=scenario, outer_fold=0,
                      role='fixed_development', candidate_index=None, inner_fold=None))
    own = predictions[first_prediction:]
    losses = person_losses(own)
    labels = np.array([r['label'] for r in own])
    cell.update(person_losses=losses,
        metrics={m: dict(**selection.scores(labels, np.array([r[f'{m}_probability'] for r in own])),
            person_brier=float(np.mean([p['losses'][m] for p in losses])),
            people=len(losses), specimens=len(own), positive=int(sum(labels)), negative=int(sum(1-labels)))
            for m in METHODS},
        other_minus_grid={m: float(np.mean([p['other_minus_grid'][m] for p in losses])) for m in METHODS[1:]},
        attempted_fits=len(ledger.records)-first_fit)
    if cell['attempted_fits'] != 156 or any(r['status'] != 'complete' for r in ledger.records[first_fit:]):
        raise ValueError('Cell fit/failure budget did not reconcile')
    cell['status'] = 'complete'


def stability(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Keep overlapping/all-fit and chosen outer/final denominators separate."""
    output: dict[str, Any] = {}
    scenarios = list(dict.fromkeys(r['scenario'] for r in records))
    for scenario in scenarios:
        output[scenario] = {}
        for method in ('grid', 'random', 'all_feature'):
            fits = [r for r in records if r['scenario'] == scenario and r['method'] == method
                    and r['status'] == 'complete']
            outer = [r for r in fits if r['role'] in ('outer_refit', 'fixed_outer')]
            final = [r for r in fits if r['role'] in ('development_refit', 'fixed_development')]
            def overlap(selected: list[dict[str, Any]]) -> list[dict[str, Any]]:
                return [dict(left=a['fit_id'], right=b['fit_id'],
                    jaccard=legacy._jaccard(a['selected_features'], b['selected_features']))
                    for a, b in itertools.combinations(selected, 2)]
            features = {}
            for feature in FEATURES:
                ranks = [r['ranks'][feature] for r in outer if r['ranks'][feature] is not None]
                coefficients = [r['coefficients'][feature] for r in outer if feature in r['coefficients']]
                features[feature] = dict(outer_selected=len(coefficients), outer_fits=len(outer),
                    all_fit_selected=sum(feature in r['selected_features'] for r in fits), all_fits=len(fits),
                    ranks=dict(n=len(ranks), median=float(np.median(ranks)) if ranks else None,
                        minimum=min(ranks) if ranks else None, maximum=max(ranks) if ranks else None),
                    signs=dict(selected_denominator=len(coefficients), negative=sum(c < 0 for c in coefficients),
                        zero=sum(c == 0 for c in coefficients), positive=sum(c > 0 for c in coefficients)))
            def choices(selected: list[dict[str, Any]]) -> dict[str, int]:
                return dict(Counter(json.dumps(r['parameters'], sort_keys=True) for r in selected))
            output[scenario][method] = dict(features=features, outer_fit_ids=[r['fit_id'] for r in outer],
                outer_panel_pairs=overlap(outer), final_panel_pairs=overlap(final),
                outer_candidate_frequency=choices(outer), final_candidate_frequency=choices(final),
                within_cell_outer_pairs={cohort: overlap([r for r in outer if r['cohort_id'] == cohort])
                                         for cohort in sorted({r['cohort_id'] for r in outer})})
    return output


def stability_report(records: list[dict[str, Any]]) -> dict[str, Any]:
    return dict(by_scenario=stability(records), by_cohort={cohort: stability(
        [r for r in records if r['cohort_id'] == cohort])
        for cohort in sorted({r['cohort_id'] for r in records})})


def audit(report: dict[str, Any], predictions: list[dict[str, Any]],
          records: list[dict[str, Any]]) -> dict[str, Any]:
    """Recalculate saved-coordinate boundaries, scores, histories and counts."""
    if report['status'] != 'software_pass':
        raise ValueError('A failed/partial run cannot pass the audit')
    expected_cells, expected_fits, expected_rows = ((12, 1872, 1080) if report['mode'] == 'full' else (1, 156, 90))
    if (len(report['cells']), len(records), len(predictions)) != (expected_cells, expected_fits, expected_rows):
        raise ValueError('Global cell/fit/prediction budget mismatch')
    if [r['fit_id'] for r in records] != list(range(1, expected_fits+1)):
        raise ValueError('Fit identities must be complete and unique')
    contract = json.loads(CONTRACT.read_text())
    expected_keys = ([(c['cohort_id'], scenario) for c in contract['cohorts'] for scenario in contract['scenarios']]
                     if report['mode'] == 'full' else [('legacy', 'reference')])
    if [(c['cohort_id'], c['scenario']) for c in report['cells']] != expected_keys:
        raise ValueError('Missing, duplicate or undeclared cohort/scenario cells')
    if report['reserved_predictions_generated'] or report['protocol_freeze_commit'] != FREEZE:
        raise ValueError('Reserved-prediction or protocol-freeze contract violated')
    for cell in report['cells']:
        own = [p for p in predictions if (p['cohort_id'], p['scenario']) == (cell['cohort_id'], cell['scenario'])]
        groups = np.array(cell['person_id'])
        selection.check_partition(cell['development'], cell['reserved'], groups)
        if sorted(p['cohort_row'] for p in own) != sorted(cell['development']):
            raise ValueError('Development predictions missing, duplicated or reserved')
        if len({p['specimen_id'] for p in own}) != 90:
            raise ValueError('Duplicate specimen identity')
        for p in own:
            row = p['cohort_row']
            if (p['person_id'], p['specimen_id'], p['label']) != (int(groups[row]), cell['specimen_id'][row], cell['labels'][row]):
                raise ValueError('Prediction identity/label mismatch')
            for method in METHODS:
                if not np.isfinite(p[f'{method}_probability']) or not 0 <= p[f'{method}_probability'] <= 1:
                    raise ValueError('Invalid saved probability')
        seen = []
        for fold, membership in enumerate(cell['outer'], start=1):
            selection.check_partition(membership['analysis'], membership['assessment'], groups, cell['development'])
            seen.extend(membership['assessment'])
            if sorted(p['cohort_row'] for p in own if p['outer_fold'] == fold) != sorted(membership['assessment']):
                raise ValueError('Prediction outer-fold mismatch')
        if sorted(seen) != sorted(cell['development']):
            raise ValueError('Incomplete outer coverage')
        fitted = [r for r in records if (r['cohort_id'], r['scenario']) == (cell['cohort_id'], cell['scenario'])]
        if len(fitted) != 156 or any(r['status'] != 'complete' for r in fitted):
            raise ValueError('Missing or failed fit records')
        if Counter(r['method'] for r in fitted) != {'grid': 76, 'random': 76, 'all_feature': 4}:
            raise ValueError('Procedure fitting budgets mismatch')
        if len(cell['searches']) != 8 or Counter((s['method'], s['outer_fold']) for s in cell['searches']) != Counter(
                (m, f) for m in ('grid', 'random') for f in range(4)):
            raise ValueError('Missing or duplicate nested searches')
        for search_record in cell['searches']:
            parent = cell['outer'][search_record['outer_fold']-1]['analysis'] if search_record['outer_fold'] else cell['development']
            for fold in search_record['inner']:
                selection.check_partition(fold['analysis'], fold['assessment'], groups, parent)
            candidates = search_record['candidates']
            if len(candidates) != 6 or sum(t['chosen'] for t in candidates) != 1:
                raise ValueError('Incomplete candidate history')
            if [t['parameters'] for t in candidates] != [dict(select__k=k, model__C=c)
                    for k, c in legacy.candidate_settings(search_record['method'])]:
                raise ValueError('Candidate settings differ from frozen search')
            best = min((t['mean_inner_brier'], i) for i, t in enumerate(candidates))[1]
            if not candidates[best]['chosen']:
                raise ValueError('Selection did not minimize inner error')
            for candidate in candidates:
                if len(candidate['fit_ids']) != 3:
                    raise ValueError('Incomplete inner fitting history')
                scores = []
                for index, fit_id in enumerate(candidate['fit_ids']):
                    fit = records[fit_id-1]
                    boundary = search_record['inner'][index]
                    if (fit['analysis'] != boundary['analysis'] or fit['assessment'] != boundary['assessment']
                            or fit['parameters'] != candidate['parameters']):
                        raise ValueError('Candidate fitting boundary/parameters mismatch')
                    scores.append(fit['brier'])
                if not np.isclose(np.mean(scores), candidate['mean_inner_brier'], atol=1e-12, rtol=0):
                    raise ValueError('Candidate score history mismatch')
            refit = records[search_record['refit_id']-1]
            if refit['analysis'] != list(parent) or refit['parameters'] != candidates[best]['parameters']:
                raise ValueError('Chosen refit boundary mismatch')
        for fit in fitted:
            if not set(fit['analysis']) <= set(cell['development']):
                raise ValueError('Fit used reserved rows')
            if set(groups[fit['analysis']]) & set(groups[fit['assessment']]):
                raise ValueError('Person overlap in fit ledger')
            if fit['method'] == 'all_feature':
                parent = cell['outer'][fit['outer_fold']-1] if fit['outer_fold'] else None
                analysis = parent['analysis'] if parent else cell['development']
                assessment = parent['assessment'] if parent else []
                if fit['analysis'] != analysis or fit['assessment'] != assessment:
                    raise ValueError('All-feature fitting boundary mismatch')
            if set(fit['ranks']) != set(FEATURES) or set(fit['coefficients']) != set(fit['selected_features']):
                raise ValueError('Incomplete feature diagnostics')
        for fold, boundary in enumerate(cell['outer'], start=1):
            train_prevalence = float(np.mean(np.array(cell['labels'])[boundary['analysis']]))
            if any(p['prevalence_probability'] != train_prevalence for p in own if p['outer_fold'] == fold):
                raise ValueError('Prevalence comparator did not use outer training people')
        losses = person_losses(own)
        if losses != cell['person_losses']:
            raise ValueError('Saved person losses do not replay')
        y = np.array([p['label'] for p in own])
        for method in METHODS:
            if {k: cell['metrics'][method][k] for k in ('people', 'specimens', 'positive', 'negative')} != dict(people=45, specimens=90, positive=45, negative=45):
                raise ValueError('Metric denominator mismatch')
            metrics = selection.scores(y, np.array([p[f'{method}_probability'] for p in own]))
            for metric, value in metrics.items():
                if not np.isclose(value, cell['metrics'][method][metric], atol=1e-12, rtol=0):
                    raise ValueError('Saved metrics do not replay')
            if not np.isclose(np.mean([p['losses'][method] for p in losses]), cell['metrics'][method]['person_brier'], atol=1e-12, rtol=0):
                raise ValueError('Person Brier mismatch')
        for method in METHODS[1:]:
            if not np.isclose(np.mean([p['other_minus_grid'][method] for p in losses]),
                              cell['other_minus_grid'][method], atol=1e-12, rtol=0):
                raise ValueError('Paired contrast direction/value mismatch')
    return dict(status='pass', cells=expected_cells, fits=expected_fits, prediction_rows=expected_rows,
                reserved_predictions=0, person_disjoint=True)


def run(output: Path, mode: str = 'smoke', max_seconds: float | None = None) -> Path:
    config = frozen_contract()
    if mode not in ('smoke', 'full'):
        raise ValueError('Mode must be smoke or full')
    output = Path(output).absolute()
    output = output.parent.resolve(strict=True) / output.name
    if output.exists() or output.is_symlink() or output == ROOT or ROOT in output.parents:
        raise ValueError('Choose a new output directory outside the repository')
    seconds = (config['max_seconds'] if mode == 'full' else 120) if max_seconds is None else max_seconds
    if not np.isfinite(seconds) or seconds <= 0 or seconds > config['max_seconds']:
        raise ValueError('Invalid wall budget')
    source_paths = [str(p.relative_to(ROOT)) for p in SOURCES]
    dirty = subprocess.check_output(['git', '-C', str(ROOT), 'status', '--porcelain', '--', *source_paths], text=True)
    if mode == 'full' and (dirty or any(os.environ.get(k) != v for k, v in config['thread_environment'].items())):
        raise ValueError('Full assessment requires committed sources and declared single-thread settings')
    versions = {p: importlib.metadata.version(p) for p in ('numpy', 'scipy', 'scikit-learn', 'joblib')}
    if mode == 'full':
        for line in (ROOT/'04_machine_learning/requirements-python.txt').read_text().splitlines():
            package, version = line.split('==')
            if importlib.metadata.version(package) != version:
                raise ValueError('Full assessment requires the pinned dependency versions')
    output.mkdir()
    began = time.monotonic()
    ledger = FitLedger(output, config['max_fits'] if mode == 'full' else 156, began+seconds)
    report: dict[str, Any] = dict(protocol_id=config['protocol_id'], mode=mode, status='running',
        protocol_freeze_commit=FREEZE, source_revision=subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
        source_dirty=bool(dirty), started_utc=datetime.now(timezone.utc).isoformat(), cells=[], error=None,
        source_sha256={str(p.relative_to(ROOT)): digest(p) for p in (*SOURCES, PROTOCOL, CONTRACT)},
        reserved_predictions_generated=False, planned_fits=ledger.max_fits, max_seconds=seconds)
    predictions: list[dict[str, Any]] = []
    try:
        write_json(output / 'report.json', report)
        (output / 'protocol.md').write_bytes(PROTOCOL.read_bytes())
        (output / 'contract.json').write_bytes(CONTRACT.read_bytes())
        write_json(output / 'environment.json', dict(python=sys.version, platform=platform.platform(),
            machine=platform.machine(), processor=platform.processor(), cpu_count=os.cpu_count(),
            cpu_info=Path('/proc/cpuinfo').read_text() if Path('/proc/cpuinfo').exists() else None,
            versions=versions, threads={k: os.environ.get(k) for k in config['thread_environment']}, command=sys.argv))
        cohorts = config['cohorts'] if mode == 'full' else [dict(cohort_id='legacy', cohort_seed=legacy.COHORT_SEED,
            split_seed=legacy.SPLIT_SEED, alternate_split_seed=legacy.ALTERNATE_SPLIT_SEED, perturbation_seed=legacy.PERTURBATION_SEED)]
        scenarios = config['scenarios'] if mode == 'full' else ['reference']
        for cohort in cohorts:
            for scenario in scenarios:
                cell: dict[str, Any] = {}
                report['cells'].append(cell)
                evaluate_cell(cohort, scenario, ledger, cell, predictions)
                write_json(output / 'report.json', report)
                write_json(output / 'predictions.json', predictions)
        if time.monotonic()-began > seconds:
            raise TimeoutError('Post-execution wall budget exceeded')
        report['status'] = 'software_pass'
        report['audit'] = audit(report, predictions, ledger.records)
        write_json(output / 'stability.json', stability_report(ledger.records))
    except Exception as exc:
        report.update(status='software_fail', error=f'{type(exc).__name__}: {exc}')
        raise
    finally:
        report.update(finished_utc=datetime.now(timezone.utc).isoformat(), elapsed_seconds=time.monotonic()-began,
            actual_fits=len(ledger.records), failed_fits=sum(r['status'] != 'complete' for r in ledger.records),
            fitting_seconds=sum(r['elapsed_seconds'] for r in ledger.records))
        report['cost_by_procedure'] = {method: dict(attempts=sum(r['method'] == method for r in ledger.records),
            failures=sum(r['method'] == method and r['status'] != 'complete' for r in ledger.records),
            seconds=sum(r['elapsed_seconds'] for r in ledger.records if r['method'] == method))
            for method in METHODS}
        report['cost_by_cell'] = [dict(cohort_id=cohort, scenario=scenario,
            attempts=sum((r['cohort_id'], r['scenario']) == (cohort, scenario) for r in ledger.records),
            failures=sum((r['cohort_id'], r['scenario']) == (cohort, scenario) and r['status'] != 'complete' for r in ledger.records),
            seconds=sum(r['elapsed_seconds'] for r in ledger.records if (r['cohort_id'], r['scenario']) == (cohort, scenario)))
            for cohort, scenario in dict.fromkeys((r['cohort_id'], r['scenario']) for r in ledger.records)]
        write_json(output / 'fits.json', ledger.records)
        write_json(output / 'predictions.json', predictions)
        write_json(output / 'report.json', report)
        write_json(output / 'sha256.json', {p.name: digest(p) for p in sorted(output.iterdir()) if p.is_file() and p.name != 'sha256.json'})
    return output


def audit_bundle(folder: Path) -> dict[str, Any]:
    manifest = json.loads((folder / 'sha256.json').read_text())
    if set(manifest) != {p.name for p in folder.iterdir() if p.is_file() and p.name != 'sha256.json'}:
        raise ValueError('Manifest coverage mismatch')
    for name, expected in manifest.items():
        if Path(name).name != name or digest(folder / name) != expected:
            raise ValueError('Output digest mismatch')
    result = audit(json.loads((folder / 'report.json').read_text()),
        json.loads((folder / 'predictions.json').read_text()), json.loads((folder / 'fits.json').read_text()))
    saved = json.loads((folder / 'stability.json').read_text())
    if saved != stability_report(json.loads((folder / 'fits.json').read_text())):
        raise ValueError('Stability summaries do not replay')
    report = json.loads((folder/'report.json').read_text())
    for cell in report['cells']:
        if digest(folder/cell['input_file']) != cell['input_sha256']:
            raise ValueError('Cell input identity mismatch')
        with np.load(folder/cell['input_file'], allow_pickle=False) as data:
            selection.validate_cohort(data)
            if (data['person_id'].tolist() != cell['person_id'] or data['specimen_id'].tolist() != cell['specimen_id']
                    or data['y'].tolist() != cell['labels']):
                raise ValueError('Cell input/metadata mismatch')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--mode', choices=('smoke', 'full'), default='smoke')
    parser.add_argument('--audit-only', action='store_true')
    args = parser.parse_args()
    if not args.audit_only:
        run(args.output, mode=args.mode)
    print(json.dumps(audit_bundle(args.output)))
