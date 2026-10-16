"""Run local ML verification and optionally audit a published processed-results CSV.

Only repository-owned synthetic examples are executed. No external model is loaded.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import importlib.util
import json
import math
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[2]
BURK_COMMIT = '37d04d15993cb1f3771dbb784ea7251e0b512b1d'
BURK_SHA256 = 'e2292668b46e9ba26f2bbb0372e8274a7731101a4bf3f983d133a8fd660776e6'
BURK_URL = ('https://raw.githubusercontent.com/slds-lmu/paper_2023_survival_benchmark/'
            f'{BURK_COMMIT}/results/production/scores.csv')
SEEDS = (261016, 261017, 261018)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def published_arithmetic():
    """Check reported aggregate counts only, without refitting published statistics."""
    excluded = 214 + 610 + 451 + 1
    analyzed = 463094 - excluded
    intervention_rate = 1000 * 338 / 53043
    control_rate = 1000 * 262 / 52872
    ratio = intervention_rate / control_rate
    workload_reduction = 100 * (1 - 61248 / 109692)
    checks = [analyzed == 461818, 53043 + 52872 == 105934 - 19,
              round(intervention_rate, 1) == 6.4, round(control_rate, 1) == 5.0,
              round(ratio, 2) == 1.29, round(workload_reduction, 1) == 44.2]
    if not all(checks):
        raise ValueError('Published aggregate arithmetic does not reconcile')
    return dict(praim=dict(screened=463094, excluded=excluded, analyzed=analyzed,
        source='https://doi.org/10.1038/s41591-024-03408-6'),
        masai_2025=dict(intervention_people=53043, control_people=52872,
            detected_cancers=[338, 262], rates_per_1000=[intervention_rate, control_rate],
            detection_rate_ratio=ratio, workload_reduction_percent=workload_reduction,
            source='https://doi.org/10.1016/S2589-7500(24)00267-X'),
        interpretation='Published-count arithmetic only; confidence intervals, p-values, '
                       'causal effects and model predictions were not reproduced.')


def audit_scores(path):
    """Audit exported rows, preserving failures and uncomputed metrics as such."""
    with Path(path).open(newline='', encoding='utf-8') as stream:
        reader = csv.DictReader(stream)
        required = {'task_id', 'learner_id', 'iteration', 'tune_measure', 'errors_cnt',
                    'warnings_cnt', 'harrell_c', 'uno_c', 'isbs', 'isll', 'dcalib', 'alpha_calib'}
        if not required <= set(reader.fieldnames or []):
            raise ValueError('Missing processed-result columns')
        rows = list(reader)
    if not rows:
        raise ValueError('Empty processed-result artifact')
    seen = set()
    metric_counts = {name: Counter() for name in
                     ('harrell_c', 'uno_c', 'isbs', 'isll', 'dcalib', 'alpha_calib')}
    error_rows = warning_rows = 0
    for row in rows:
        if None in row or any(value is None for value in row.values()):
            raise ValueError('Malformed processed-result row')
        key = tuple(row[k] for k in ('task_id', 'learner_id', 'iteration', 'tune_measure'))
        if not all(key) or key in seen:
            raise ValueError('Blank or duplicate task/learner/iteration/objective key')
        seen.add(key)
        try:
            flags = [int(row[k]) for k in ('errors_cnt', 'warnings_cnt')]
        except ValueError as exc:
            raise ValueError('Invalid error/warning count') from exc
        if min(flags) < 0:
            raise ValueError('Negative error/warning count')
        error_rows += flags[0] > 0
        warning_rows += flags[1] > 0
        for name, counts in metric_counts.items():
            raw = row[name]
            if raw in {'NA', 'NaN', '', 'nan'}:
                counts['missing_or_uncomputed'] += 1
                continue
            try:
                value = float(raw)
            except ValueError as exc:
                raise ValueError(f'Non-numeric {name}') from exc
            if not math.isfinite(value) or value < 0 or (name in {'harrell_c', 'uno_c'} and value > 1):
                raise ValueError(f'Invalid {name}')
            counts['finite'] += 1
    return dict(rows=len(rows), datasets=len({r['task_id'] for r in rows}),
                learners=len({r['learner_id'] for r in rows}), duplicate_keys=0,
                rows_flagged_error=error_rows, rows_flagged_warning=warning_rows,
                metric_coverage={k: dict(v) for k, v in metric_counts.items()},
                sha256=digest(path),
                interpretation='Processed-output integrity only; NA may mean uncomputed. '
                               'No refitting, p-value replication or independent clinical validation.')


def synthetic_stress():
    # Import only the repository-owned module; never execute a downloaded source file.
    import numpy as np
    source = ROOT / '04_machine_learning/examples/breast_cancer_feature_selection.py'
    spec = importlib.util.spec_from_file_location('paired_selection_validation', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    output = []
    for seed in SEEDS:
        data = module.make_cohort(seed=seed)
        development, test = module.make_plan(data)
        model, report = module.fit_development(data, development, test)
        assessed = module.assess(model, data, report)
        groups = data['person_id']
        # Independent group-set and coverage checks against the exported coordinates.
        if set(groups[development]) & set(groups[test]):
            raise ValueError('Reserved people overlap development')
        covered = []
        for fold in report['outer']:
            analysis, assessment = fold['analysis'], fold['assessment']
            if set(groups[analysis]) & set(groups[assessment]):
                raise ValueError('Outer person overlap')
            covered.extend(assessment)
            for inner in fold['inner']:
                if set(groups[inner['analysis']]) & set(groups[inner['assessment']]):
                    raise ValueError('Inner person overlap')
        if sorted(covered) != sorted(development.tolist()):
            raise ValueError('Incomplete outer prediction coverage')
        invariant = None
        if seed == SEEDS[0]:
            changed = {k: value.copy() for k, value in data.items()}
            changed['x'][test] = 100000
            changed['y'][test] = 1 - changed['y'][test]
            refit, changed_report = module.fit_development(changed, development, test)
            invariant = (report == changed_report and np.array_equal(
                model.best_estimator_.named_steps['model'].coef_,
                refit.best_estimator_.named_steps['model'].coef_))
            if not invariant:
                raise ValueError('Reserved values changed development fitting')
        output.append(dict(seed=seed, development_people=len(set(groups[development])),
            test_people=len(set(groups[test])), nested_metrics=report['nested_development'],
            final_test_metrics=assessed['metrics'], prevalence_baseline=assessed['prevalence_baseline'],
            best_parameters=report['best_parameters'], selected_features=report['selected_features'],
            pipeline_fits=report['tuning_contract']['total_pipeline_fits'],
            reserved_value_invariance=invariant))
    return output


def run(output, scores_csv=None):
    output = Path(output).absolute()
    output = output.parent.resolve(strict=True) / output.name
    if output.exists() or output.is_symlink() or output == ROOT or ROOT in output.parents:
        raise ValueError('Choose a new output directory outside the repository')
    stage = Path(tempfile.mkdtemp(prefix='corpus-validation-', dir=output.parent))
    with (ROOT / '04_machine_learning/evidence/breast-cancer-studies.csv').open(newline='') as stream:
        registered = list(csv.DictReader(stream))
    with (ROOT / '04_machine_learning/evidence/rust-ml-sources.csv').open(newline='') as stream:
        rust_sources = list(csv.DictReader(stream))
    report = dict(started_utc=datetime.now(timezone.utc).isoformat(),
        scope='ML corpus and repository-owned synthetic workflows; not study reproduction',
        registered_publications=len(registered),
        rust_literature_sources=dict(Counter(row['source_kind'] for row in rust_sources)),
        python=sys.version, platform=platform.platform(), seeds=list(SEEDS),
        dependencies={p: importlib.metadata.version(p)
                      for p in ('numpy', 'scipy', 'scikit-learn', 'joblib', 'matplotlib')},
        rscript_available=shutil.which('Rscript') is not None, checks=[])
    env = dict(os.environ, OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
    os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
    commands = [
        ['scripts/check_ml_evidence.py'],
        ['04_machine_learning/tests/test_sklearn_methods.py'],
        ['04_machine_learning/tests/test_breast_cancer_feature_selection.py'],
        ['04_machine_learning/tests/test_validation_audit.py'],
        ['04_machine_learning/tests/test_breast_cancer_comparison.py'],
        ['04_machine_learning/tests/test_gallery_diagnostics.py'],
        ['04_machine_learning/tests/test_rust_export.py'],
        ['04_machine_learning/examples/sklearn_methods.py', str(stage / 'general')],
        ['04_machine_learning/examples/breast_cancer_feature_selection.py', str(stage / 'paired')],
        ['04_machine_learning/examples/breast_cancer_comparison.py', str(stage / 'comparison')],
    ]
    try:
        for i, command in enumerate(commands):
            start = time.monotonic()
            result = subprocess.run([sys.executable, *command], cwd=ROOT, env=env,
                                    capture_output=True, text=True, timeout=180)
            (stage / f'command-{i + 1}.log').write_text(result.stdout + result.stderr)
            report['checks'].append(dict(command=[sys.executable, *command],
                exit_code=result.returncode, elapsed_seconds=round(time.monotonic() - start, 3),
                log=f'command-{i + 1}.log'))
            if result.returncode:
                raise RuntimeError(f'Validation command failed: {command[0]}')
        import joblib
        import numpy as np
        paired = stage / 'paired'
        saved = json.loads((paired / 'report.json').read_text())
        model = joblib.load(paired / 'pipeline.joblib')
        with np.load(paired / 'synthetic_inputs.npz', allow_pickle=False) as inputs:
            predicted = model.predict_proba(inputs['x'][saved['test']])[:, list(model.classes_).index(1)]
        difference = float(np.max(np.abs(predicted - saved['final_test']['prediction'])))
        if difference > 1e-12:
            raise ValueError('Saved prediction replay mismatch')
        for name, expected in json.loads((paired / 'sha256.json').read_text()).items():
            if digest(paired / name) != expected:
                raise ValueError(f'Artifact digest mismatch: {name}')
        with (paired / 'feature_review.csv').open(newline='') as stream:
            features = list(csv.DictReader(stream))
        if len(features) != 48 or len({r['feature'] for r in features}) != 48:
            raise ValueError('Feature review has missing or repeated measurements')
        report['saved_replay'] = dict(max_absolute_probability_difference=difference,
                                      hashes_match=True, distinct_feature_rows=48)
        comparison = stage / 'comparison'
        comparison_report = json.loads((comparison / 'report.json').read_text())
        comparison_models = joblib.load(comparison / 'models.joblib')
        replay = {}
        with np.load(comparison / 'synthetic_inputs.npz', allow_pickle=False) as inputs:
            test = comparison_report['selected']['test']
            for name, fitted in comparison_models.items():
                predicted = fitted.predict_proba(inputs['x'][test])[:, list(fitted.classes_).index(1)]
                delta = float(np.max(np.abs(predicted - comparison_report['final_test'][name]['prediction'])))
                if delta > 1e-12:
                    raise ValueError(f'Comparison replay mismatch: {name}')
                replay[name] = delta
        for name, expected in json.loads((comparison / 'sha256.json').read_text()).items():
            if digest(comparison / name) != expected:
                raise ValueError(f'Comparison digest mismatch: {name}')
        report['comparison'] = dict(protocol_id=comparison_report['protocol_id'],
            cohort_seed=comparison_report['cohort_seed'], split_seed=comparison_report['split_seed'],
            pipeline_fits=comparison_report['pipeline_fits'], replay_max_absolute_difference=replay,
            development_brier_difference=comparison_report['development_brier_difference'],
            final_test=comparison_report['final_test'],
            figure_files=sorted(str(p.relative_to(comparison)) for p in (comparison / 'gallery').glob('*')))
        report['synthetic_stress'] = synthetic_stress()
        report['published_arithmetic'] = published_arithmetic()
        if scores_csv is not None:
            if digest(scores_csv) != BURK_SHA256:
                raise ValueError('Published artifact differs from the reviewed commit/hash')
            report['published_artifact'] = dict(source_url=BURK_URL, commit=BURK_COMMIT,
                                               **audit_scores(scores_csv))
        else:
            report['published_artifact'] = {'status': 'not_run', 'reason': 'No local scores CSV supplied'}
        report['status'] = 'pass'
    except Exception as exc:
        report.update(status='fail', error=f'{type(exc).__name__}: {exc}')
    report['source_sha256'] = {str(p.relative_to(ROOT)): digest(p) for p in sorted(
        set(ROOT.glob('04_machine_learning/examples/*.py')) |
        set(ROOT.glob('04_machine_learning/tests/test_*.py')) | {Path(__file__).resolve(),
        ROOT / '04_machine_learning/evidence/breast-cancer-studies.csv',
        ROOT / '04_machine_learning/evidence/paper-review.csv', ROOT / 'scripts/check_ml_evidence.py',
        ROOT / '04_machine_learning/evidence/rust-ml-sources.csv',
        ROOT / '04_machine_learning/evidence/rust-ml-references.bib',
        ROOT / '04_machine_learning/evidence/rust-ml-search-2026-10-16.md',
        ROOT / '04_machine_learning/rust-ml-literature.md',
        ROOT / 'scripts/check_rust_ml_evidence.py', ROOT / 'scripts/tests/test_rust_ml_evidence.py'})}
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (stage / 'validation.json').write_text(json.dumps(report, indent=2, allow_nan=False))
    if output.exists() or output.is_symlink():
        raise FileExistsError(output)
    stage.rename(output)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--scores-csv', type=Path, help='Optional pinned BC-M28 processed results')
    args = parser.parse_args()
    result = run(args.output, args.scores_csv)
    print(json.dumps({'status': result['status'], 'output': str(args.output)}, indent=2))
    raise SystemExit(0 if result['status'] == 'pass' else 1)
