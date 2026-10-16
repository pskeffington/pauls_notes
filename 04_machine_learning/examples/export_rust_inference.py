"""Export trusted, repository-generated assay models for frozen Rust inference."""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
from pathlib import Path
import shutil
import tempfile

import joblib
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest

import breast_cancer_comparison as comparison

ROOT = Path(__file__).resolve().parents[2]
MODEL_NAMES = ('selected', 'all_features')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_inventory(bundle):
    bundle = Path(bundle).resolve(strict=True)
    inventory = json.loads((bundle / 'sha256.json').read_text())
    if not inventory:
        raise ValueError('Empty artifact inventory')
    for name, expected in inventory.items():
        path = bundle / name
        if (Path(name).is_absolute() or '..' in Path(name).parts or path.is_symlink()
                or bundle not in path.resolve(strict=True).parents or digest(path) != expected):
            raise ValueError(f'Artifact identity or checksum mismatch: {name}')
    return inventory


def new_output(output):
    output = Path(output).absolute()
    output = output.parent.resolve(strict=True) / output.name
    if output.exists() or output.is_symlink() or output == ROOT or ROOT in output.parents:
        raise ValueError('Choose a new output directory outside the repository')
    return output


def portable_model(model, feature_names, name):
    if name not in MODEL_NAMES:
        raise ValueError('Unsupported model name')
    if name == 'selected':
        if not isinstance(model, GridSearchCV):
            raise ValueError('Expected the selected search result')
        model = model.best_estimator_
    expected = ['impute', 'select', 'scale', 'model'] if name == 'selected' else ['impute', 'scale', 'model']
    if not isinstance(model, Pipeline) or list(model.named_steps) != expected:
        raise ValueError('Unsupported pipeline operations or order')
    steps = model.named_steps
    impute, scale, logistic = (steps[k] for k in ('impute', 'scale', 'model'))
    if (not isinstance(impute, SimpleImputer) or impute.strategy != 'median' or impute.add_indicator
            or not isinstance(scale, StandardScaler) or not scale.with_mean or not scale.with_std
            or not isinstance(logistic, LogisticRegression) or list(logistic.classes_) != [0, 1]
            or logistic.coef_.shape[0] != 1):
        raise ValueError('Only median imputation, standard scaling and binary logistic models are supported')
    names = [str(n) for n in feature_names]
    if names != [f'Feature{i:03d}' for i in range(1, len(names) + 1)]:
        raise ValueError('Unexpected feature schema')
    if name == 'selected' and not isinstance(steps['select'], SelectKBest):
        raise ValueError('Unsupported selector')
    indices = np.flatnonzero(steps['select'].get_support()) if name == 'selected' else np.arange(len(names))
    if (len(impute.statistics_) != len(names) or len(scale.mean_) != len(indices)
            or len(logistic.coef_[0]) != len(indices) or not len(indices)
            or np.any(scale.scale_ <= 0)):
        raise ValueError('Pipeline dimensions or scales disagree')
    document = dict(schema_version=1, task='synthetic_paired_specimen_category',
        protocol_id='paired-comparison-v1', training_partition='development', model_name=name,
        positive_class=1, feature_names=names, selected_indices=indices.tolist(),
        imputation_medians=impute.statistics_.tolist(), scaler_means=scale.mean_.tolist(),
        scaler_scales=scale.scale_.tolist(), coefficients=logistic.coef_[0].tolist(),
        intercept=float(logistic.intercept_[0]))
    json.dumps(document, allow_nan=False)  # Reject missing/nonfinite learned parameters.
    return document


def export_bundle(bundle, output, *, trusted_local_bundle=False):
    if not trusted_local_bundle:
        raise ValueError('Explicitly identify a trusted local model bundle before loading joblib')
    output = new_output(output)
    bundle = Path(bundle).resolve(strict=True)
    inventory = verify_inventory(bundle)
    required = {'models.joblib', 'synthetic_inputs.npz', 'report.json', 'versions.json'}
    if not required <= set(inventory):
        raise ValueError('Required comparison artifacts are not covered by the inventory')
    versions = json.loads((bundle / 'versions.json').read_text())
    if any(versions[name] != importlib.metadata.version(name) for name in ('numpy', 'scikit-learn', 'joblib')):
        raise ValueError('Restore the recorded modeling versions before export')
    report = json.loads((bundle / 'report.json').read_text())
    if report['protocol_id'] != 'paired-comparison-v1' or report['final_test_used_for_selection']:
        raise ValueError('Unexpected training/assessment contract')
    with np.load(bundle / 'synthetic_inputs.npz', allow_pickle=False) as archive:
        data = {key: archive[key].copy() for key in archive.files}
    development, test = comparison.make_plan(data)
    if report['selected']['development'] != development.tolist() or report['selected']['test'] != test.tolist():
        raise ValueError('Saved partitions do not match the declared comparison plan')
    # Checksums detect changed files, not a malicious pickle. Only trusted local artifacts reach this call.
    models = joblib.load(bundle / 'models.joblib')
    if set(models) != set(MODEL_NAMES):
        raise ValueError('Expected both frozen comparison models')
    documents = {name: portable_model(models[name], data['feature_names'], name) for name in MODEL_NAMES}
    probes = np.array([np.full(48, np.nan), np.zeros(48), np.full(48, 1e6),
                       np.full(48, -1e6), np.tile([-1e6, 1e6], 24)])
    values = np.vstack([data['x'], probes])
    ids = data['specimen_id'].tolist() + ['ProbeMissing', 'ProbeZero', 'ProbePositive', 'ProbeNegative', 'ProbeAlternating']
    references = {name: comparison.selection.probabilities(models[name], values) for name in MODEL_NAMES}
    for name in MODEL_NAMES:
        if not np.allclose(references[name][test], report['final_test'][name]['prediction'], rtol=0, atol=1e-12):
            raise ValueError('Frozen model does not replay its saved test probabilities')
    stage = Path(tempfile.mkdtemp(prefix='rust-export-', dir=output.parent))
    try:
        for name, document in documents.items():
            (stage / f'{name}.json').write_text(json.dumps(document, indent=2, allow_nan=False))
        with (stage / 'specimens.csv').open('w', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(['specimen_id', *data['feature_names']])
            writer.writerows([identity, *['NA' if np.isnan(v) else format(v, '.17g') for v in row]]
                             for identity, row in zip(ids, values))
        with (stage / 'reference-probabilities.csv').open('w', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(['specimen_id', 'record_kind', 'selected_probability', 'all_features_probability'])
            for i, identity in enumerate(ids):
                kind = ('numerical_probe' if i >= len(data['y']) else
                        'reserved_test_replay' if i in test else 'development_fitted_replay')
                writer.writerow([identity, kind, *[format(references[name][i], '.17g') for name in MODEL_NAMES]])
        sources = [Path(__file__).resolve(), *sorted((ROOT / '04_machine_learning/rust/src').glob('*.rs')),
                   ROOT / '04_machine_learning/rust/Cargo.toml', ROOT / '04_machine_learning/rust/Cargo.lock',
                   ROOT / '04_machine_learning/rust/rust-toolchain.toml',
                   ROOT / '04_machine_learning/rust/build.rs']
        metadata = dict(schema_version=1, protocol_id=report['protocol_id'],
            model_names=list(MODEL_NAMES), cohort_people=60, cohort_specimens=120, numerical_probes=5,
            training_people=45, reserved_test_people=15, feature_count=48,
            source_bundle_sha256={name: inventory[name] for name in sorted(required)},
            training_source_sha256=report['source_sha256'],
            deployment_source_sha256={str(p.relative_to(ROOT)): digest(p) for p in sources},
            modeling_versions=versions,
            interpretation='Frozen final-development models; development replay is in-sample, '
                           'not the gallery outer-held-out predictions. Probes test arithmetic only.')
        (stage / 'export.json').write_text(json.dumps(metadata, indent=2, allow_nan=False))
        (stage / 'README.txt').write_text(
            'Own synthetic assay example: 120 paired specimens plus 5 numerical probes.\n'
            'Rust receives no targets or person identifiers. It does not train, tune or recalibrate.\n'
            'Reference values replay final-development models, including in-sample development rows.\n'
            'Use the source guide for schema, feature order and interpretation limits.\n')
        hashes = {p.name: digest(p) for p in sorted(stage.iterdir())}
        (stage / 'sha256.json').write_text(json.dumps(hashes, indent=2))
        if output.exists() or output.is_symlink():
            raise FileExistsError(output)
        stage.rename(output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--trusted-local-bundle', action='store_true',
                        help='Required: the joblib files were created locally from trusted repository code')
    args = parser.parse_args()
    export_bundle(args.bundle, args.output, trusted_local_bundle=args.trusted_local_bundle)
