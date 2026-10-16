"""Paired whole-person resampling of frozen OOF losses; no model fitting."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
FREEZE = 'd440b82b9af696f3717e302b6e276cb10ad39255'
G1_BASE = '544f6ad27d339deb1ada92d05f86999f60c38b0e'
PROTOCOL = ROOT/'04_machine_learning/uncertainty-protocol.md'
CONTRACT = ROOT/'04_machine_learning/evidence/uncertainty-contract-v1.json'
INPUT = ROOT/'04_machine_learning/evidence/uncertainty-input-v1.json'
G1_RECORD = ROOT/'04_machine_learning/evidence/replication-validation-2026-10-16.json'
METHODS = ('grid', 'random', 'all_feature', 'prevalence')
FIELDS = ('cohort_id', 'scenario', 'cohort_row', 'person_id', 'specimen_id', 'label',
          'outer_fold', *(f'{m}_probability' for m in METHODS))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    """Use a unique temporary name and flush bytes before atomic publication."""
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
                prefix=path.name+'-', suffix='.tmp', delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(value, handle, indent=2, allow_nan=False)
            handle.write('\n')
            handle.flush()
            os.fsync(handle.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def frozen_contract() -> dict[str, Any]:
    for path in (PROTOCOL, CONTRACT, INPUT):
        committed = subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{FREEZE}:{path.relative_to(ROOT)}'])
        if committed != path.read_bytes():
            raise ValueError('Frozen protocol, contract or input was modified')
    contract = json.loads(CONTRACT.read_text())
    if digest(INPUT) != contract['input_sha256']:
        raise ValueError('Frozen prediction snapshot hash mismatch')
    return contract


def validate_cells(rows: list[dict[str, Any]], cohorts: list[str], scenarios: list[str],
                   people_per_cell: int) -> dict[tuple[str, str], list[dict[str, Any]]]:
    """Reject broken person/specimen identities before constructing any loss."""
    if not rows or len(set(cohorts)) != len(cohorts) or len(set(scenarios)) != len(scenarios):
        raise ValueError('Nonempty unique cohort/scenario structure required')
    cells: dict[tuple[str, str], list[dict[str, Any]]] = {(c, s): [] for c in cohorts for s in scenarios}
    identity_by_specimen: dict[tuple[str, str], tuple[int, int, int]] = {}
    identity_by_row: dict[tuple[str, int], str] = {}
    for row in rows:
        if set(row) != set(FIELDS) or (row['cohort_id'], row['scenario']) not in cells:
            raise ValueError('Undeclared cell or prediction field schema')
        if any(type(row[k]) is not int for k in ('cohort_row', 'person_id', 'label', 'outer_fold')):
            raise ValueError('Integer row/person/label/fold identities required')
        if not (0 <= row['cohort_row'] < 120 and 0 <= row['person_id'] < 60
                and row['label'] in (0, 1) and row['outer_fold'] in (1, 2, 3)):
            raise ValueError('Invalid row/person/label/fold value')
        if not isinstance(row['specimen_id'], str) or not row['specimen_id'].strip():
            raise ValueError('Nonblank specimen identity required')
        for method in METHODS:
            p = row[f'{method}_probability']
            if type(p) not in (int, float) or not np.isfinite(p) or not 0 <= p <= 1:
                raise ValueError('Probabilities must be finite real numbers in [0,1]')
        specimen_key = row['cohort_id'], row['specimen_id']
        identity = row['cohort_row'], row['person_id'], row['label']
        if identity_by_specimen.setdefault(specimen_key, identity) != identity:
            raise ValueError('Specimen identity/label changes across scenarios')
        row_key = row['cohort_id'], row['cohort_row']
        if identity_by_row.setdefault(row_key, row['specimen_id']) != row['specimen_id']:
            raise ValueError('Row identity changes across scenarios')
        cells[row['cohort_id'], row['scenario']].append(row)
    for cell in cells.values():
        if len(cell) != people_per_cell*2:
            raise ValueError('Missing, duplicated or extra prediction records')
        if (len({r['specimen_id'] for r in cell}) != len(cell)
                or len({r['cohort_row'] for r in cell}) != len(cell)):
            raise ValueError('Duplicate specimen or row identity')
        groups = {r['person_id'] for r in cell}
        if len(groups) != people_per_cell:
            raise ValueError('Person denominator mismatch')
        for person in groups:
            pair = [r for r in cell if r['person_id'] == person]
            if (len(pair) != 2 or {r['label'] for r in pair} != {0, 1}
                    or len({r['outer_fold'] for r in pair}) != 1):
                raise ValueError('Broken paired-person label/fold structure')
        cell.sort(key=lambda r: (r['person_id'], r['label']))
    return cells


def read_input(contract: dict[str, Any]) -> dict[tuple[str, str], list[dict[str, Any]]]:
    packed = json.loads(INPUT.read_text())
    if packed['schema'] != 'paired-oof-input-v1' or packed['fields'] != list(FIELDS):
        raise ValueError('Frozen input schema mismatch')
    if any(not isinstance(row, list) or len(row) != len(FIELDS) for row in packed['rows']):
        raise ValueError('Malformed compact prediction row')
    rows = [dict(zip(FIELDS, row)) for row in packed['rows']]
    cells = validate_cells(rows, contract['cohorts'], contract['scenarios'], contract['people_per_cell'])
    # Reconstruct the original G1 prediction file, not just a claimed source label.
    original = sorted(rows, key=lambda r: (contract['cohorts'].index(r['cohort_id']),
        contract['scenarios'].index(r['scenario']), r['outer_fold'], r['cohort_row']))
    raw = (json.dumps(original, indent=2, allow_nan=False)+'\n').encode()
    if (hashlib.sha256(raw).hexdigest() != contract['g1_prediction_sha256']
            or packed['source']['predictions_sha256'] != contract['g1_prediction_sha256']
            or packed['source']['archive_sha256'] != contract['g1_archive_sha256']
            or packed['source']['g1_execution_commit'] != contract['g1_execution_commit']):
        raise ValueError('Snapshot does not reconstruct the verified G1 predictions')
    return cells


def person_losses(rows: list[dict[str, Any]]) -> tuple[np.ndarray, np.ndarray]:
    people = np.array(sorted({r['person_id'] for r in rows}), dtype=np.int64)
    losses = []
    for person in people:
        pair = sorted((r for r in rows if r['person_id'] == person), key=lambda r: r['label'])
        if len(pair) != 2 or [r['label'] for r in pair] != [0, 1] or len({r['outer_fold'] for r in pair}) != 1:
            raise ValueError('Whole-person losses require a valid specimen pair')
        losses.append([np.mean([(r[f'{method}_probability']-r['label'])**2 for r in pair]) for method in METHODS])
    return people, np.array(losses, dtype=np.float64)


def person_draws(n: int, repetitions: int, seed_parts: list[int]) -> np.ndarray:
    if any(type(v) is not int or v < 2 for v in (n, repetitions)):
        raise ValueError('At least two people and two bootstrap draws required')
    rng = np.random.Generator(np.random.PCG64(np.random.SeedSequence(seed_parts)))
    return rng.integers(0, n, size=(repetitions, n), dtype=np.int64)


def bootstrap_means(differences: np.ndarray, indices: np.ndarray) -> np.ndarray:
    if (differences.ndim != 2 or differences.shape[0] < 2 or differences.shape[1] != 3
            or not np.isfinite(differences).all() or np.any(np.abs(differences) > 1)):
        raise ValueError('Expected finite person-by-three Brier contrasts in [-1,1]')
    if (indices.ndim != 2 or indices.shape[1] != len(differences) or len(indices) < 2
            or indices.dtype.kind not in 'iu' or np.any(indices < 0) or np.any(indices >= len(differences))):
        raise ValueError('Invalid whole-person resampling indices')
    return np.mean(differences[indices], axis=1)


def summarize(differences: np.ndarray, means: np.ndarray) -> list[dict[str, Any]]:
    endpoints = np.quantile(means, [0.025, 0.975], axis=0, method='linear')
    point = differences.mean(axis=0)
    reference = np.sqrt(np.mean((differences-point)**2, axis=0)/len(differences))
    return [dict(method=method, point=float(point[i]), lower=float(endpoints[0, i]),
        upper=float(endpoints[1, i]), empirical_resampling_sd=float(np.std(means[:, i], ddof=1)),
        analytic_empirical_bootstrap_sd=float(reference[i]),
        constant_person_differences=bool(np.all(differences[:, i] == differences[0, i])),
        interpretation='pointwise conditional person-bootstrap range; no full-procedure coverage claim')
        for i, method in enumerate(METHODS[1:])]


def reliability(cells: dict[tuple[str, str], list[dict[str, Any]]]) -> list[dict[str, Any]]:
    results = []
    for (cohort, scenario), rows in cells.items():
        if scenario == 'reference':
            continue
        people, loss = person_losses(rows)
        reference_people, reference_loss = person_losses(cells[cohort, 'reference'])
        common = sorted(set(people) & set(reference_people))
        left = {int(p): v for p, v in zip(reference_people, reference_loss)}
        right = {int(p): v for p, v in zip(people, loss)}
        results.append(dict(cohort_id=cohort, scenario=scenario, reference_people=len(reference_people),
            scenario_people=len(people), common_people=len(common),
            reference_only=len(set(reference_people)-set(people)), scenario_only=len(set(people)-set(reference_people)),
            common_person_mean_loss_change={m: float(np.mean([right[p][i]-left[p][i] for p in common]))
                                           if common else None for i, m in enumerate(METHODS)},
            limitation='Common people may have different training models and folds; not an isolated causal or variance component'))
    return results


def fixture_rows() -> list[dict[str, Any]]:
    return [dict(cohort_id='fixture', scenario='reference', cohort_row=2*person+label,
        person_id=person, specimen_id=f'fixture-{person}-{label}', label=label, outer_fold=1,
        grid_probability=(0.1+0.03*person if not label else 0.9-0.03*person),
        random_probability=(0.2 if not label else 0.8), all_feature_probability=0.4,
        prevalence_probability=0.5) for person in range(4) for label in (0, 1)]


def output_path(path: Path) -> Path:
    path = Path(path).absolute()
    path = path.parent.resolve(strict=True)/path.name
    if path.exists() or path.is_symlink() or path == ROOT or ROOT in path.parents:
        raise ValueError('Choose a new output directory outside the repository')
    return path


def run(output: Path, mode: str = 'fixture', max_seconds: float = 300) -> Path:
    contract = frozen_contract()
    if mode not in ('fixture', 'full') or not np.isfinite(max_seconds) or not 0 < max_seconds <= contract['max_seconds']:
        raise ValueError('Invalid mode or time budget')
    output = output_path(output)
    sources = (Path(__file__), ROOT/'04_machine_learning/requirements-python.txt', G1_RECORD)
    dirty = subprocess.check_output(['git', '-C', str(ROOT), 'status', '--porcelain', '--',
                                    *(str(p.relative_to(ROOT)) for p in sources)], text=True)
    if mode == 'full' and dirty:
        raise ValueError('Full assessment requires committed computational sources')
    if mode == 'full':
        for line in (ROOT/'04_machine_learning/requirements-python.txt').read_text().splitlines():
            package, version = line.split('==')
            if importlib.metadata.version(package) != version:
                raise ValueError('Full assessment requires pinned dependency versions')
        original = subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{G1_BASE}:{G1_RECORD.relative_to(ROOT)}'])
        if original != G1_RECORD.read_bytes():
            raise ValueError('G1 diagnostic source record changed')
    cells = read_input(contract) if mode == 'full' else validate_cells(fixture_rows(), ['fixture'], ['reference'], 4)
    repetitions = contract['resamples_per_cell'] if mode == 'full' else 128
    output.mkdir()
    began = time.monotonic()
    arrays: dict[str, np.ndarray] = {}
    report: dict[str, Any] = dict(protocol_id=contract['protocol_id'], mode=mode, status='running', error=None,
        source_revision=subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
        source_dirty=bool(dirty), protocol_freeze_commit=FREEZE, started_utc=datetime.now(timezone.utc).isoformat(),
        input_sha256=digest(INPUT), source_sha256={str(p.relative_to(ROOT)): digest(p) for p in sources},
        protocol_sha256=digest(PROTOCOL), contract_sha256=digest(CONTRACT), cells=[], model_fits=0,
        conditional_only=True, full_procedure_uncertainty_estimated=False, resamples_per_cell=repetitions,
        max_seconds=max_seconds)
    try:
        (output/'protocol.md').write_bytes(PROTOCOL.read_bytes())
        (output/'contract.json').write_bytes(CONTRACT.read_bytes())
        (output/'input.json').write_bytes(INPUT.read_bytes())
        write_json(output/'execution-start.json', dict(source_revision=report['source_revision'],
            protocol_freeze_commit=FREEZE, started_utc=report['started_utc'], command=sys.argv))
        write_json(output/'environment.json', dict(python=sys.version, platform=platform.platform(),
            numpy=importlib.metadata.version('numpy'), scipy=importlib.metadata.version('scipy'),
            thread_environment={k: os.environ.get(k) for k in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS')}))
        for index, ((cohort, scenario), rows) in enumerate(cells.items()):
            if time.monotonic()-began >= max_seconds:
                raise TimeoutError('Prespecified wall budget exceeded before a cell')
            people, losses = person_losses(rows)
            differences = losses[:, 1:]-losses[:, [0]]
            seed_parts = [contract['root_seed'], contract['cohorts'].index(cohort) if mode == 'full' else 0,
                          contract['scenarios'].index(scenario)]
            indices = person_draws(len(people), repetitions, seed_parts)
            means = bootstrap_means(differences, indices)
            prefix = f'cell{index:02d}'
            arrays.update({prefix+'_people': people, prefix+'_losses': losses,
                prefix+'_contrasts': differences, prefix+'_indices': indices, prefix+'_means': means})
            report['cells'].append(dict(cohort_id=cohort, scenario=scenario, people=len(people), specimens=len(rows),
                positive=sum(r['label'] for r in rows), negative=sum(1-r['label'] for r in rows),
                array_prefix=prefix, seed_parts=seed_parts, person_ids=people.tolist(),
                person_brier={m: float(np.mean(losses[:, i])) for i, m in enumerate(METHODS)},
                ranges=summarize(differences, means)))
        report['reliability'] = reliability(cells)
        if mode == 'full':
            report['g1_stability_and_candidate_reference'] = json.loads(original)['stability_summary']
        report['fitting_variability'] = 'Not separately identified: predictions and fits are fixed; no refitting performed'
        np.savez_compressed(output/'resampling.npz', **arrays)
        if time.monotonic()-began > max_seconds:
            raise TimeoutError('Prespecified post-execution wall budget exceeded')
        report['status'] = 'software_pass'
    except Exception as exc:
        report.update(status='software_fail', error=f'{type(exc).__name__}: {exc}')
        if arrays and not (output/'resampling.npz').exists():
            np.savez_compressed(output/'partial-resampling.npz', **arrays)
        raise
    finally:
        report.update(finished_utc=datetime.now(timezone.utc).isoformat(), elapsed_seconds=time.monotonic()-began,
            completed_cells=len(report['cells']), completed_ranges=sum(len(c['ranges']) for c in report['cells']),
            person_index_resamples=len(report['cells'])*repetitions,
            contrast_replicate_means=len(report['cells'])*repetitions*3)
        write_json(output/'report.json', report)
        write_json(output/'sha256.json', {p.name: digest(p) for p in sorted(output.iterdir()) if p.is_file() and p.name != 'sha256.json'})
    return output


def audit(folder: Path) -> dict[str, Any]:
    manifest = json.loads((folder/'sha256.json').read_text())
    if set(manifest) != {p.name for p in folder.iterdir() if p.is_file() and p.name != 'sha256.json'}:
        raise ValueError('Manifest coverage mismatch')
    for name, expected in manifest.items():
        if Path(name).name != name or digest(folder/name) != expected:
            raise ValueError('Output hash mismatch')
    report = json.loads((folder/'report.json').read_text())
    contract = frozen_contract()
    if (report['status'] != 'software_pass' or report['model_fits'] != 0
            or report['protocol_freeze_commit'] != FREEZE or not report['conditional_only']
            or report['full_procedure_uncertainty_estimated'] or report['mode'] not in ('fixture', 'full')):
        raise ValueError('Incomplete or incorrectly scoped uncertainty run')
    if (report['input_sha256'] != digest(INPUT) or report['protocol_sha256'] != digest(PROTOCOL)
            or report['contract_sha256'] != digest(CONTRACT)
            or not 0 <= report['elapsed_seconds'] <= report['max_seconds'] <= contract['max_seconds']):
        raise ValueError('Source identity or wall-budget mismatch')
    for saved, original in (('protocol.md', PROTOCOL), ('contract.json', CONTRACT), ('input.json', INPUT)):
        if (folder/saved).read_bytes() != original.read_bytes():
            raise ValueError('Frozen snapshot identity mismatch')
    full = report['mode'] == 'full'
    cells = read_input(contract) if full else validate_cells(fixture_rows(), ['fixture'], ['reference'], 4)
    if len(report['cells']) != len(cells) or report['resamples_per_cell'] != (10000 if full else 128):
        raise ValueError('Cell or resampling denominator mismatch')
    with np.load(folder/'resampling.npz', allow_pickle=False) as arrays:
        expected_arrays = {f'cell{i:02d}_{suffix}' for i in range(len(cells))
                           for suffix in ('people', 'losses', 'contrasts', 'indices', 'means')}
        if set(arrays.files) != expected_arrays:
            raise ValueError('Resampling array coverage mismatch')
        for index, ((cohort, scenario), rows) in enumerate(cells.items()):
            cell = report['cells'][index]
            if (cell['cohort_id'], cell['scenario']) != (cohort, scenario):
                raise ValueError('Cell identity mismatch')
            people, losses = person_losses(rows)
            prefix = f'cell{index:02d}'
            differences = losses[:, 1:]-losses[:, [0]]
            seed_parts = [contract['root_seed'], contract['cohorts'].index(cohort) if full else 0,
                          contract['scenarios'].index(scenario)]
            if cell['seed_parts'] != seed_parts or cell['person_ids'] != people.tolist() or cell['array_prefix'] != prefix:
                raise ValueError('Person order, array identity or frozen seed mismatch')
            indices = person_draws(len(people), report['resamples_per_cell'], seed_parts)
            means = np.mean(differences[indices], axis=1)
            for suffix, expected in (('people', people), ('losses', losses), ('contrasts', differences),
                                     ('indices', indices), ('means', means)):
                if arrays[prefix+'_'+suffix].dtype != expected.dtype or not np.array_equal(arrays[prefix+'_'+suffix], expected):
                    raise ValueError('Saved person/draw/statistic arrays do not replay')
            if cell['ranges'] != summarize(differences, means):
                raise ValueError('Saved endpoints or spread do not replay')
            if (cell['people'], cell['specimens'], cell['positive'], cell['negative']) != (len(people), 2*len(people), len(people), len(people)):
                raise ValueError('Person/specimen denominator mismatch')
            if cell['person_brier'] != {m: float(np.mean(losses[:, i])) for i, m in enumerate(METHODS)}:
                raise ValueError('Saved Brier losses do not replay')
    if report['reliability'] != reliability(cells):
        raise ValueError('Reliability summaries do not replay')
    if full and (report['source_dirty'] or report['g1_stability_and_candidate_reference'] != json.loads(G1_RECORD.read_text())['stability_summary']):
        raise ValueError('Full source status or G1 diagnostic reference mismatch')
    if (report['completed_cells'], report['completed_ranges'], report['person_index_resamples'],
            report['contrast_replicate_means']) != (len(cells), len(cells)*3,
                len(cells)*report['resamples_per_cell'], len(cells)*report['resamples_per_cell']*3):
        raise ValueError('Global resampling/range budget mismatch')
    return dict(status='pass', cells=len(cells), ranges=len(cells)*3,
        person_index_resamples=len(cells)*report['resamples_per_cell'], model_fits=0, conditional_only=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--mode', choices=('fixture', 'full'), default='fixture')
    parser.add_argument('--audit-only', action='store_true')
    args = parser.parse_args()
    if not args.audit_only:
        run(args.output, mode=args.mode)
    print(json.dumps(audit(args.output)))
