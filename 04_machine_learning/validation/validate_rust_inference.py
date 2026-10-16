"""Check frozen Rust inference against exported Python probabilities."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

EXAMPLES = Path(__file__).resolve().parents[1] / 'examples'
sys.path.insert(0, str(EXAMPLES))
import export_rust_inference as exporter

ROOT = EXAMPLES.parents[1]
TOLERANCE = 1e-12


def read_csv(path):
    with Path(path).open(newline='') as stream:
        return list(csv.DictReader(stream))


def validate(bundle, binary, output):
    bundle, binary = Path(bundle).resolve(strict=True), Path(binary).resolve(strict=True)
    output = exporter.new_output(output)
    inventory = exporter.verify_inventory(bundle)
    required = {'selected.json', 'all_features.json', 'specimens.csv',
                'reference-probabilities.csv', 'export.json'}
    if not required <= set(inventory):
        raise ValueError('Required inference artifacts are not covered by the inventory')
    reference = read_csv(bundle / 'reference-probabilities.csv')
    reference_ids = [r['specimen_id'] for r in reference]
    if len(reference_ids) != len(set(reference_ids)) or not reference_ids:
        raise ValueError('Duplicate or absent reference identities')
    stage = Path(tempfile.mkdtemp(prefix='rust-validation-', dir=output.parent))
    report = dict(started_utc=datetime.now(timezone.utc).isoformat(),
        scope='Cross-language frozen-model software replay, not training or clinical validation',
        tolerance_absolute_probability=TOLERANCE, binary_sha256=exporter.digest(binary), checks={})
    try:
        for name in exporter.MODEL_NAMES:
            destination = stage / name
            command = [str(binary), str(bundle / f'{name}.json'), str(bundle / 'specimens.csv'), str(destination)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            if result.returncode:
                raise ValueError(f'Rust inference failed: {result.stderr}')
            actual = read_csv(destination / 'predictions.csv')
            if [r['specimen_id'] for r in actual] != reference_ids:
                raise ValueError('Rust output identities/order differ from references')
            differences = [abs(float(a['probability_class_1']) - float(r[f'{name}_probability']))
                           for a, r in zip(actual, reference)]
            if not all(0 <= float(a['probability_class_1']) <= 1 for a in actual) or max(differences) > TOLERANCE:
                raise ValueError('Rust/Python probability mismatch')
            record = json.loads((destination / 'run.json').read_text())
            for key, path in [('model_sha256', bundle / f'{name}.json'), ('input_sha256', bundle / 'specimens.csv'),
                              ('predictions_sha256', destination / 'predictions.csv')]:
                if record[key] != exporter.digest(path):
                    raise ValueError('Rust run metadata checksum mismatch')
            report['checks'][name] = dict(specimens=len(actual), max_absolute_probability_difference=max(differences),
                record_kinds={kind: sum(r['record_kind'] == kind for r in reference)
                              for kind in sorted({r['record_kind'] for r in reference})},
                runtime=record)
        rejected = []
        # These challenges exercise the actual compiled CLI, including its output guards.
        def reject(label, model, inputs, destination):
            result = subprocess.run([str(binary), str(model), str(inputs), str(destination)],
                                    capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                raise ValueError(f'Rust accepted an invalid case: {label}')
            rejected.append(label)
        model = bundle / 'selected.json'
        specimens = bundle / 'specimens.csv'
        csv_rows = read_csv(specimens)
        with specimens.open(newline='') as stream:
            headers = next(csv.reader(stream))
        invalid = stage / 'invalid.csv'
        def write_csv(rows, fields=headers):
            with invalid.open('w', newline='') as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
        write_csv(csv_rows, [headers[0], headers[2], headers[1], *headers[3:]])
        reject('reordered_features', model, invalid, stage / 'bad-order')
        write_csv(csv_rows + [csv_rows[0]])
        reject('duplicate_specimen', model, invalid, stage / 'bad-duplicate')
        for value in ('NaN', 'inf'):
            changed = [dict(row) for row in csv_rows]
            changed[0][headers[1]] = value
            write_csv(changed)
            reject(f'nonfinite_{value}', model, invalid, stage / f'bad-{value}')
        bad_model = stage / 'invalid-model.json'
        document = json.loads(model.read_text())
        document['scaler_scales'][0] = 0
        bad_model.write_text(json.dumps(document))
        reject('zero_model_scale', bad_model, specimens, stage / 'bad-scale')
        # The successful result must remain intact after the rejected overwrite.
        existing = stage / 'selected/predictions.csv'
        before = exporter.digest(existing)
        reject('existing_output', model, specimens, stage / 'selected')
        if exporter.digest(existing) != before:
            raise ValueError('Rejected output overwrite changed an existing prediction file')
        link = stage / 'dangling'
        link.symlink_to(stage / 'absent')
        reject('output_symlink', model, specimens, link)
        if not link.is_symlink() or (stage / 'absent').exists():
            raise ValueError('Rejected symlink destination was changed')
        reject('repository_output', model, specimens, ROOT / '04_machine_learning/forbidden-rust-output')
        if (ROOT / '04_machine_learning/forbidden-rust-output').exists():
            raise ValueError('Rust wrote into the repository')
        for label in ('bad-order', 'bad-duplicate', 'bad-NaN', 'bad-inf', 'bad-scale'):
            if (stage / label).exists():
                raise ValueError('Malformed input produced an output directory')
        report.update(rejected_cases=rejected, status='pass')
        report['source_sha256'] = {str(p.relative_to(ROOT)): exporter.digest(p) for p in [
            Path(__file__).resolve(), EXAMPLES / 'export_rust_inference.py',
            ROOT / '04_machine_learning/rust/Cargo.toml', ROOT / '04_machine_learning/rust/Cargo.lock',
            ROOT / '04_machine_learning/rust/rust-toolchain.toml', ROOT / '04_machine_learning/rust/build.rs',
            *sorted((ROOT / '04_machine_learning/rust/src').glob('*.rs'))]}
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        (stage / 'validation.json').write_text(json.dumps(report, indent=2, allow_nan=False))
        # Invalid inputs are test artifacts; successful model outputs and report are retained.
        invalid.unlink()
        bad_model.unlink()
        link.unlink()
        if output.exists() or output.is_symlink():
            raise FileExistsError(output)
        stage.rename(output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--binary', type=Path, required=True)
    args = parser.parse_args()
    result = validate(args.bundle, args.binary, args.output)
    print(json.dumps({'status': result['status'], 'checks': {name: record['max_absolute_probability_difference']
          for name, record in result['checks'].items()}}, indent=2))
