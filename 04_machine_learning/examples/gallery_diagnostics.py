"""Plot saved training diagnostics; never fit, predict or load model objects."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

DIAGNOSTIC_NAMES = ('allocation-missingness', 'candidate-scores', 'selection-frequency',
                    'feature-contrasts', 'calibration')
BOOTSTRAP_SEED = 26101604
BOOTSTRAP_REPLICATES = 2000
MIN_BIN_PEOPLE = 10
BIN_EDGES = np.array([0, .2, .4, .6, .8, 1.])
BIN_LABELS = ['0–.2', '.2–.4', '.4–.6', '.6–.8', '.8–1']


def candidate_searches(report):
    selected = report['selected']
    return [(f'Outer {i + 1} training', fold['search_candidates'], fold['best_parameters'])
            for i, fold in enumerate(selected['outer'])] + [
            ('Full development', selected['final_search_candidates'], selected['best_parameters'])]


def load_display_inputs(bundle, report, rows):
    """Fail closed on inconsistent identities, masks, split traces or feature summaries."""
    saved = json.loads((Path(bundle) / 'display-inputs.json').read_text())
    names = saved['feature_names']
    if (saved['schema_version'] != 1 or len(names) != 48 or len(set(names)) != 48
            or names != [f'Feature{i:03d}' for i in range(1, 49)]):
        raise ValueError('Invalid display feature schema')
    by_row = {int(r['cohort_row']): r for r in rows}
    specimens = saved['specimens']
    if len(specimens) != len(rows) or {r['cohort_row'] for r in specimens} != set(by_row):
        raise ValueError('Incomplete or duplicate missingness records')
    for item in specimens:
        original = by_row[item['cohort_row']]
        if (item['person_id'] != int(original['person_id']) or item['specimen_id'] != original['specimen_id']
                or item['label'] != int(original['label']) or len(item['missing']) != len(names)
                or any(type(v) is not bool for v in item['missing'])):
            raise ValueError('Missingness mask or identity disagrees with predictions')
    selected = report['selected']
    development = set(selected['development'])

    def check_folds(folds, universe):
        covered = []
        for fold in folds:
            train, held = fold['analysis'], fold['assessment']
            if (not train or not held or len(set(train)) != len(train) or len(set(held)) != len(held)
                    or set(train) & set(held) or set(train) | set(held) != universe
                    or {by_row[i]['person_id'] for i in train} & {by_row[i]['person_id'] for i in held}):
                raise ValueError('Broken grouped split coordinates')
            covered.extend(held)
        if len(covered) != len(universe) or set(covered) != universe:
            raise ValueError('Incomplete grouped assessment coverage')
    check_folds(selected['outer'], development)
    for fold in selected['outer']:
        check_folds(fold['inner'], set(fold['analysis']))
    check_folds(selected['final_inner'], development)
    for _, candidates, best in candidate_searches(report):
        params = [(c['parameters']['model__C'], c['parameters']['select__k']) for c in candidates]
        if sorted(params) != [(c, k) for c in (.1, 1.) for k in (5, 10, 20)]:
            raise ValueError('Incomplete candidate grid')
        scores = [c['mean_brier'] for c in candidates]
        for candidate in candidates:
            values = candidate['fold_brier']
            rank = 1 + sum(score < candidate['mean_brier'] for score in scores)
            if (len(values) != 3 or not np.isfinite(values).all() or min(values) < 0 or max(values) > 1
                    or not np.isclose(np.mean(values), candidate['mean_brier'], rtol=0, atol=1e-12)
                    or candidate['rank'] != rank or type(candidate['chosen']) is not bool):
                raise ValueError('Invalid candidate loss, mean or rank')
        winners = [c for c in candidates if c['chosen']]
        if len(winners) != 1 or winners[0]['parameters'] != best or winners[0]['rank'] != 1:
            raise ValueError('Chosen candidate disagrees with selection rule')
    features = saved['feature_review']
    if len(features) != len(names) or {f['feature'] for f in features} != set(names):
        raise ValueError('Incomplete or duplicate feature summaries')
    for f in features:
        name = f['feature']
        expected_count = sum(name in fold['selected_features'] for fold in selected['outer'])
        expected_final = name in selected['selected_features']
        importance = selected['mean_outer_permutation_brier_increase'][names.index(name)]
        coefficient = f['standardized_coefficient']
        if (type(f['final_selected']) is not bool or f['final_selected'] != expected_final
                or f['selected_outer_fits'] != expected_count or f['outer_fits'] != len(selected['outer'])
                or not np.isfinite([f['all_feature_standardized_coefficient'],
                                    f['mean_outer_permutation_brier_increase']]).all()
                or not np.isclose(f['mean_outer_permutation_brier_increase'], importance, rtol=0, atol=1e-12)
                or (expected_final and (not isinstance(coefficient, (int, float)) or not np.isfinite(coefficient)))
                or (not expected_final and coefficient != '')):
            raise ValueError('Feature summary disagrees with saved fits')
    return saved


def calibration_summary(rows, partition, key, *, replicates=BOOTSTRAP_REPLICATES,
                        seed=BOOTSTRAP_SEED, min_people=MIN_BIN_PEOPLE):
    """Resample whole people with fixed predictions; omit sparse/degenerate ranges."""
    subset = sorted((r for r in rows if r['partition'] == partition),
                    key=lambda r: (int(r['person_id']), int(r['cohort_row'])))
    people = sorted({int(r['person_id']) for r in subset})
    if not people or replicates < 1:
        raise ValueError('Calibration needs people and positive replicate count')
    lookup = {person: i for i, person in enumerate(people)}
    p = np.array([float(r[key + '_probability']) for r in subset])
    y = np.array([int(r['label']) for r in subset])
    groups = np.array([lookup[int(r['person_id'])] for r in subset])
    if not np.isfinite(p).all() or np.any((p < 0) | (p > 1)) or not set(y) <= {0, 1}:
        raise ValueError('Invalid calibration inputs')
    bins = np.searchsorted(BIN_EDGES[1:-1], p, side='right')
    draws = np.random.default_rng(seed).integers(0, len(people), size=(replicates, len(people)))
    summaries = []
    for b in range(5):
        mask = bins == b
        counts = np.bincount(groups[mask], minlength=len(people))
        positives = np.bincount(groups[mask], weights=y[mask], minlength=len(people))
        denominator = counts[draws].sum(axis=1)
        numerator = positives[draws].sum(axis=1)
        valid = denominator > 0
        n, g = int(mask.sum()), int(np.count_nonzero(counts))
        status, lower, upper = 'estimated', None, None
        if n == 0:
            status = 'empty'
        elif g < min_people:
            status = 'sparse'
        elif len(set(y[mask])) < 2:
            status = 'one_label'
        elif valid.sum() < .95 * replicates:
            status = 'too_many_empty_replicates'
        else:
            lo, hi = np.quantile(numerator[valid] / denominator[valid], [.025, .975], method='linear')
            if hi <= lo:
                status = 'degenerate'
            else:
                lower, upper = float(lo), float(hi)
        summaries.append(dict(bin=b, left=float(BIN_EDGES[b]), right=float(BIN_EDGES[b + 1]),
            specimens=n, people=g, positives=int(y[mask].sum()),
            mean_probability=float(p[mask].mean()) if n else None,
            observed_fraction=float(y[mask].mean()) if n else None,
            valid_replicates=int(valid.sum()), lower=lower, upper=upper, interval_status=status))
    return summaries


def render_diagnostics(report, rows, saved, stage, save, plt):
    """Write five figures and their numeric derivations using an existing Agg context."""
    from matplotlib.colors import ListedColormap
    from matplotlib.patches import Patch
    blue, orange, gray = '#205493', '#bf6b0a', '#637381'
    selected = report['selected']
    by_row = {int(r['cohort_row']): r for r in rows}
    people = sorted({int(r['person_id']) for r in rows},
                    key=lambda person: (next(r['partition'] for r in rows if int(r['person_id']) == person) == 'test', person))
    person_rows = {person: [int(r['cohort_row']) for r in rows if int(r['person_id']) == person]
                   for person in people}
    outer_sets = [set(f['assessment']) for f in selected['outer']]
    inner_sets = [set(f['assessment']) for f in selected['outer'][0]['inner']]
    inner_train = set(selected['outer'][0]['analysis'])
    development = set(selected['development'])
    allocation = []
    for assessed in [set(), *outer_sets]:
        allocation.append([2 if ids[0] not in development else 1 if ids[0] in assessed else 0
                           for ids in person_rows.values()])
    for assessed in inner_sets:
        allocation.append([2 if ids[0] not in development else 3 if ids[0] not in inner_train
                           else 1 if ids[0] in assessed else 0 for ids in person_rows.values()])
    order = [i for ids in person_rows.values() for i in sorted(ids)]
    masks = {s['cohort_row']: s['missing'] for s in saved['specimens']}
    mask = np.array([masks[i] for i in order])
    fig, axes = plt.subplots(2, 1, figsize=(11, 8.4), gridspec_kw={'height_ratios': [1.15, 2.4]}, layout='constrained')
    ax = axes[0]
    ax.imshow(allocation, aspect='auto', interpolation='nearest', vmin=0, vmax=3,
              cmap=ListedColormap([blue, orange, '#d9dfe5', '#8d73a3']))
    ax.set(yticks=range(7), yticklabels=['Final fit', 'Outer 1', 'Outer 2', 'Outer 3',
        'Outer 1 / inner 1', 'Outer 1 / inner 2', 'Outer 1 / inner 3'],
        xticks=range(0, len(people), 5), xticklabels=[people[i] for i in range(0, len(people), 5)],
        xlabel='Invented person ID (development first; two specimens per column)',
        title='People stay together through the fitting boundaries')
    development_people = sum(ids[0] in development for ids in person_rows.values())
    ax.axvline(development_people - .5, color='black', lw=1)
    ax.legend(handles=[Patch(color=c, label=n) for c, n in zip([blue, orange, '#d9dfe5', '#8d73a3'],
        ['Train', 'Assess', 'Reserved test', 'Excluded outer assessment'])], ncol=4,
        loc='lower center', bbox_to_anchor=(.5, 1.12), frameon=False, fontsize=9)
    ax = axes[1]
    ax.imshow(mask, aspect='auto', interpolation='nearest', cmap=ListedColormap(['#f2f5f8', blue]), vmin=0, vmax=1)
    ax.axhline(len(development) - .5, color=orange, lw=1.5)
    ax.set(xticks=[0, 11, 23, 35, 47], xticklabels=['001', '012', '024', '036', '048'],
        yticks=[0, len(development) // 2 - 1, len(development) - 1, len(development) + 14, len(order) - 1],
        yticklabels=['Dev 1', 'Dev 45', 'Dev 90', 'Test 15', 'Test 30'],
        xlabel='Arbitrary assay feature', ylabel='Specimens in person pairs',
        title=f'Raw missingness: {int(mask.sum())} / {mask.size} cells ({mask.mean():.1%}); blue = missing')
    fig.supxlabel('Invented data | 45 development people / 90 specimens; 15 test people / 30 specimens\nRaw masks describe inputs; imputation medians are learned separately inside each training slice', fontsize=9)
    save(fig, stage, 'allocation-missingness')
    plt.close(fig)

    searches = candidate_searches(report)
    fig, axes = plt.subplots(2, 2, figsize=(11, 8.2), sharey=True, layout='constrained')
    for ax, (title, candidates, best) in zip(axes.flat, searches):
        for i, c in enumerate(candidates):
            ax.scatter(i + np.array([-.1, 0, .1]), c['fold_brier'], color=gray, s=20, alpha=.65)
            ax.scatter(i, c['mean_brier'], marker='*' if c['chosen'] else 'D',
                       color=orange if c['chosen'] else blue, s=140 if c['chosen'] else 35, zorder=3)
        labels = [f"k={c['parameters']['select__k']}\nC={c['parameters']['model__C']:g}" for c in candidates]
        ax.set(xticks=range(6), xticklabels=labels, ylabel='Inner-held-out Brier error',
            ylim=(0, max(c['fold_brier'][j] for _, cs, _ in searches for c in cs for j in range(3)) * 1.15),
            title=f"{title}: selected k={best['select__k']}, C={best['model__C']:g}")
        ax.grid(axis='y', alpha=.2)
        ax.spines[['top', 'right']].set_visible(False)
    fig.suptitle('Every candidate, with the selection rule visible')
    fig.supxlabel('Gray = 3 inner errors; blue diamond = mean; orange star = chosen minimum\nOverlapping training folds: spread is descriptive, not uncertainty; final test never selects settings', fontsize=9)
    save(fig, stage, 'candidate-scores')
    plt.close(fig)

    names = saved['feature_names']
    features = {f['feature']: f for f in saved['feature_review']}
    inclusion = [[int(n in f['selected_features']) for n in names] for f in selected['outer']]
    inclusion.append([int(n in selected['selected_features']) for n in names])
    counts = [features[n]['selected_outer_fits'] for n in names]
    fig, axes = plt.subplots(2, 1, figsize=(12, 6.7), sharex=True, layout='constrained',
                             gridspec_kw={'height_ratios': [1, 1.3]})
    axes[0].imshow(inclusion, aspect='auto', interpolation='nearest', cmap=ListedColormap(['#edf1f5', blue]), vmin=0, vmax=1)
    axes[0].set(yticks=range(4), yticklabels=['Outer 1', 'Outer 2', 'Outer 3', 'Final development'],
                title='Blue = selected by that training fit; all 48 columns shown')
    axes[1].bar(range(48), counts, color=blue)
    axes[1].set(yticks=range(4), ylim=(0, 3.4), ylabel='Outer fits selecting feature (of 3)',
                xticks=range(48), xticklabels=[n.removeprefix('Feature') for n in names],
                xlabel='Arbitrary feature identity; final development fit is excluded from the count')
    axes[1].tick_params(axis='x', labelrotation=90, labelsize=8)
    fig.suptitle('Observe selection variation across overlapping outer training slices')
    fig.supxlabel('Three outer fits do not establish repeated-sampling stability or gene significance', fontsize=10)
    save(fig, stage, 'selection-frequency')
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(12, 11), sharey=True, layout='constrained')
    positions = np.arange(48)
    fixed = [features[n]['all_feature_standardized_coefficient'] for n in names]
    axes[0].scatter(fixed, positions + .15, color=orange, s=18, label='All features, fixed C')
    included = [i for i, n in enumerate(names) if features[n]['final_selected']]
    axes[0].scatter([features[names[i]]['standardized_coefficient'] for i in included],
                    positions[included] - .15, color=blue, s=22, label='Selected + tuned C')
    axes[0].set(xlabel='Log-odds coefficient per training standard deviation',
                title='Final development coefficients', yticks=positions,
                yticklabels=[n.removeprefix('Feature') for n in names])
    axes[0].legend(frameon=False, fontsize=9)
    importance = [features[n]['mean_outer_permutation_brier_increase'] for n in names]
    axes[1].barh(positions, importance, color=blue, height=.65)
    axes[1].set(xlabel='Mean outer Brier increase after row-wise shuffling',
                title='Selected procedure: held-out permutation')
    axes[0].invert_yaxis()
    for ax in axes:
        ax.axvline(0, color=gray, lw=.8)
        ax.grid(axis='x', alpha=.15)
        ax.spines[['top', 'right']].set_visible(False)
        ax.tick_params(axis='y', labelsize=8)
    fig.suptitle('Coefficient direction and prediction sensitivity have different units')
    fig.supxlabel('Invented features | No selected dot = absent from final panel, not an estimated zero\nPermutation: 5 row shuffles per feature per outer assessment; pairing is broken; no inferential intervals', fontsize=9)
    save(fig, stage, 'feature-contrasts')
    plt.close(fig)

    calibration = {part: {key: calibration_summary(rows, part, key) for key in ('selected', 'all_feature')}
                   for part in ('development', 'test')}
    fig = plt.figure(figsize=(11, 10.4), layout='constrained')
    grid = fig.add_gridspec(4, 2, height_ratios=[3, .65, 3, .65])
    for row, part in enumerate(('development', 'test')):
        for col, (key, label, color) in enumerate([('selected', 'Selected + tuned C', blue),
                                                  ('all_feature', 'All features, fixed C', orange)]):
            ax = fig.add_subplot(grid[row * 2, col])
            bins = calibration[part][key]
            ax.plot([0, 1], [0, 1], '--', color=gray, lw=1)
            observed = [b for b in bins if b['specimens']]
            ax.plot([b['mean_probability'] for b in observed], [b['observed_fraction'] for b in observed],
                    color=color, alpha=.4, lw=1)
            for b in observed:
                x, y = b['mean_probability'], b['observed_fraction']
                ax.scatter(x, y, color=color, s=38, facecolors=color if b['lower'] is not None else 'white', zorder=3)
                if b['lower'] is not None:
                    ax.vlines(x, b['lower'], b['upper'], color=color, lw=2)
                    ax.hlines([b['lower'], b['upper']], x - .012, x + .012, color=color, lw=1)
            ax.set(xlim=(-.03, 1.03), ylim=(-.03, 1.03), xlabel='Mean saved probability in bin',
                   ylabel='Observed fraction labeled 1', title=f'{part.capitalize()} | {label}')
            ax.grid(alpha=.15)
            table_ax = fig.add_subplot(grid[row * 2 + 1, col])
            table_ax.axis('off')
            table = table_ax.table(cellText=[[b['specimens'] for b in bins], [b['people'] for b in bins]],
                rowLabels=['Specimens', 'People'], colLabels=BIN_LABELS, loc='center', cellLoc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(8)
            table.scale(.83, 1.12)
    fig.suptitle('Calibration: probability agreement, with counts and conditional ranges')
    fig.supxlabel('2,000 whole-person resamples; 95% percentile ranges conditional on fixed predictions\nHollow point = range withheld (sparse, one-label or degenerate bin); training uncertainty is omitted\nFixed bins include their left edge; final bin includes 1. People may contribute to more than one bin.', fontsize=9)
    save(fig, stage, 'calibration')
    plt.close(fig)
    calculations = dict(bootstrap=dict(seed=BOOTSTRAP_SEED, replicates=BOOTSTRAP_REPLICATES,
        minimum_bin_people=MIN_BIN_PEOPLE, interval='pointwise conditional percentiles, not full pipeline uncertainty'),
        calibration=calibration, missingness=dict(total=int(mask.sum()), cells=int(mask.size),
            cohort_row_order=order,
            by_partition={part: dict(missing=sum(sum(masks[i]) for i in by_row if by_row[i]['partition'] == part),
                cells=sum(by_row[i]['partition'] == part for i in by_row) * len(names))
                for part in ('development', 'test')}),
        feature_names=names, outer_selection_counts=counts)
    return calculations
