"""Render comparison figures from saved numeric results, without loading models."""
from __future__ import annotations

import argparse
from collections import defaultdict
import csv
import hashlib
import json
from pathlib import Path
import shutil
import tempfile

import numpy as np

from gallery_diagnostics import DIAGNOSTIC_NAMES, load_display_inputs, render_diagnostics

PLOT_NAMES = ('brier-comparison', 'person-errors', *DIAGNOSTIC_NAMES)

ROOT = Path(__file__).resolve().parents[2]


def load_results(bundle):
    bundle = Path(bundle)
    report = json.loads((bundle / 'report.json').read_text())
    with (bundle / 'predictions.csv').open(newline='', encoding='utf-8') as stream:
        rows = list(csv.DictReader(stream))
    if not rows:
        raise ValueError('No saved comparison predictions')
    seen, specimen_ids, people = set(), set(), defaultdict(list)
    fold_by_row = {row: str(i + 1) for i, fold in enumerate(report['selected']['outer'])
                   for row in fold['assessment']}
    for row in rows:
        try:
            index, person, y = (int(row[k]) for k in ('cohort_row', 'person_id', 'label'))
            partition = row['partition']
            if partition not in ('development', 'test'):
                raise ValueError('Unknown partition')
            probabilities = [float(row[k + '_probability'])
                             for k in ('selected', 'all_feature', 'prevalence')]
            errors = [float(row[k + '_squared_error'])
                      for k in ('selected', 'all_feature', 'prevalence')]
            membership = report['selected'][partition]
            position = membership.index(index)
            expected = ([report['selected']['outer_predictions'][position],
                         report['all_features']['outer_predictions'][position],
                         report['prevalence']['outer_predictions'][position]] if partition == 'development'
                        else [report['final_test'][k]['prediction'][position]
                              for k in ('selected', 'all_features', 'prevalence')])
        except (KeyError, ValueError, TypeError) as exc:
            raise ValueError('Invalid saved prediction identity or fields') from exc
        if index in seen or y not in (0, 1) or not row['specimen_id'] or row['specimen_id'] in specimen_ids:
            raise ValueError('Duplicate row or invalid target/partition')
        if row['outer_fold'] != fold_by_row.get(index, ''):
            raise ValueError('Saved outer fold disagrees with the report')
        if not np.isfinite(probabilities).all() or any(p < 0 or p > 1 for p in probabilities):
            raise ValueError('Invalid saved probability')
        if not np.allclose(probabilities, expected, rtol=0, atol=1e-12):
            raise ValueError('CSV probabilities disagree with the saved report')
        if not np.isfinite(errors).all() or not np.allclose(
                errors, [(p - y) ** 2 for p in probabilities], rtol=0, atol=1e-12):
            raise ValueError('Saved squared errors disagree with targets/probabilities')
        seen.add(index)
        specimen_ids.add(row['specimen_id'])
        people[person].append(row)
    expected_rows = report['selected']['development'] + report['selected']['test']
    if seen != set(expected_rows) or len(seen) != len(expected_rows):
        raise ValueError('Incomplete prediction coverage')
    for paired in people.values():
        if (len(paired) != 2 or {int(r['label']) for r in paired} != {0, 1}
                or len({r['partition'] for r in paired}) != 1
                or len({r['outer_fold'] for r in paired}) != 1):
            raise ValueError('Broken person pair in saved results')
    for partition in ('development', 'test'):
        subset = [r for r in rows if r['partition'] == partition]
        for key, name in [('selected', 'selected'), ('all_feature', 'all_features'), ('prevalence', 'prevalence')]:
            observed = float(np.mean([float(r[key + '_squared_error']) for r in subset]))
            expected = (report['selected']['nested_development']['brier'] if name == 'selected'
                        else report[name]['nested_development']['brier']) if partition == 'development' else \
                       report['final_test'][name]['metrics']['brier']
            if not np.isclose(observed, expected, rtol=0, atol=1e-12):
                raise ValueError('Saved Brier summary disagrees with prediction rows')
    return report, rows, people


def render_gallery(bundle, output):
    report, rows, people = load_results(bundle)
    display = load_display_inputs(bundle, report, rows)
    output = Path(output).absolute()
    output = output.parent.resolve(strict=True) / output.name
    if output.exists() or output.is_symlink() or output == ROOT or ROOT in output.parents:
        raise ValueError('Choose a new figure directory outside the repository')
    stage = Path(tempfile.mkdtemp(prefix='comparison-plots-', dir=output.parent))
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    palette = ['#205493', '#bf6b0a', '#637381']
    names = ['Selected + tuned C', 'All features, fixed C', 'Training prevalence']
    try:
        with plt.rc_context({'font.size': 10, 'svg.fonttype': 'none', 'svg.hashsalt': 'paired-comparison-v1'}):
            fig, ax = plt.subplots(figsize=(8.8, 5.5), layout='constrained')
            x = np.arange(2)
            maximum = 0.0
            for i, key in enumerate(('selected', 'all_feature', 'prevalence')):
                values = [np.mean([float(r[key + '_squared_error']) for r in rows if r['partition'] == part])
                          for part in ('development', 'test')]
                bars = ax.bar(x + (i - 1) * 0.24, values, width=0.22, color=palette[i], label=names[i])
                ax.bar_label(bars, fmt='%.3f', padding=4)
                maximum = max(maximum, *values)
            labels = []
            for part, label in [('development', 'Outer-held-out development'), ('test', 'Reserved final test')]:
                n_people = sum(pair[0]['partition'] == part for pair in people.values())
                n_specimens = sum(row['partition'] == part for row in rows)
                labels.append(f'{label}\n{n_people} people / {n_specimens} specimens')
            ax.set(xticks=x, xticklabels=labels,
                   ylim=(0, max(0.35, maximum * 1.4)), ylabel='Mean squared probability error (Brier)',
                   title='Two assay procedures on the same excluded people')
            ax.legend(loc='upper right', frameon=False)
            ax.spines[['top', 'right']].set_visible(False)
            ax.grid(axis='y', alpha=0.2)
            ax.set_axisbelow(True)
            fig.supxlabel('Invented paired specimens | Lower error is better | No uncertainty interval')
            save(fig, stage, 'brier-comparison')
            plt.close(fig)
            fig, axes = plt.subplots(2, 1, figsize=(9, 6.7), layout='constrained')
            for ax, part, title in zip(axes, ('development', 'test'),
                    ('Outer-held-out development people', 'Reserved final-test people')):
                selected = sorted((person, pair) for person, pair in people.items() if pair[0]['partition'] == part)
                differences = [np.mean([float(r['selected_squared_error']) -
                                        float(r['all_feature_squared_error']) for r in pair]) for _, pair in selected]
                ids = [person for person, _ in selected]
                ax.scatter(ids, differences, c=[palette[0] if d < 0 else palette[1] for d in differences], s=32)
                ax.axhline(0, color='#30343b', linestyle='--', linewidth=1)
                ax.set(title=f'{title} (n={len(ids)})', ylabel='Selected minus all-feature error',
                       xlabel='Invented person ID', ylim=(-1, 1))
                ax.spines[['top', 'right']].set_visible(False)
                ax.grid(axis='y', alpha=0.2)
            fig.suptitle('Average the two specimen errors within each person')
            fig.supxlabel('Below zero favors selected + tuned C; above zero favors fixed all-feature\nDescriptive paired differences, not independent fold estimates or confidence intervals')
            save(fig, stage, 'person-errors')
            plt.close(fig)
            calculations = render_diagnostics(report, rows, display, stage, save, plt)
        (stage / 'plot-data.json').write_text(json.dumps(dict(protocol_id=report['protocol_id'],
            cohort_seed=report['cohort_seed'], source_files=['report.json', 'predictions.csv', 'display-inputs.json'],
            source_sha256={name: hashlib.sha256((Path(bundle) / name).read_bytes()).hexdigest()
                for name in ('report.json', 'predictions.csv', 'display-inputs.json')},
            calculations=calculations,
            development_people=sum(pair[0]['partition'] == 'development' for pair in people.values()),
            test_people=sum(pair[0]['partition'] == 'test' for pair in people.values())), indent=2, allow_nan=False))
        if output.exists() or output.is_symlink():
            raise FileExistsError(output)
        stage.rename(output)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return output


def save(fig, output, name):
    for suffix in ('svg', 'pdf', 'png'):
        metadata = {'Date': None} if suffix == 'svg' else \
                   {'CreationDate': None, 'ModDate': None} if suffix == 'pdf' else None
        fig.savefig(output / f'{name}.{suffix}', dpi=150, metadata=metadata)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bundle', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    render_gallery(args.bundle, args.output)
