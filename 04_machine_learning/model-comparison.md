# Compare two assay-training procedures

[Breast cancer book, Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data) · [Declared protocol](comparison-protocol.md) · [Plotting gallery](gallery/README.md) · [Tuning guide](model-tuning.md)

The book asks whether molecular measurements can distinguish a recorded specimen category for previously unseen people. A smaller selected panel needs a comparator. This example assesses a tuned subset procedure against a fixed all-feature logistic model using **the same people, targets, outer folds and primary loss**.

The comparison changes both feature selection and regularization selection. It tests two complete training procedures; it does not isolate the effect of removing columns. It uses invented continuous assay values, not RNA-seq counts, the book’s named genes or participant records.

## What each procedure learns

| Procedure | Training operations | Selection | Complete pipeline fits |
| --- | --- | --- | --- |
| Selected + tuned C | Median imputation → F-score filter → scaling → logistic model | Six k/C candidates in three inner person-grouped folds; repeat inside each outer training slice and on full development | 76 |
| All features, fixed C | Median imputation → scaling → logistic model, all 48 columns | C = 1.0 declared before the run; no search | 3 outer fits + 1 development fit = 4 |
| Training prevalence | Mean target among that fold’s training people, or full development for the final test | No fitted estimator or search | Arithmetic baseline |

The comparator’s imputation and scaling are learned again from each outer training slice. It cannot reuse transformations learned from all development people. The selected procedure retains its existing candidate traces and feature diagnostics; the comparator does not run its own selector.

The two model procedures cost **80 pipeline fits** in total. This is a comparison of differently budgeted procedures, not an equal-compute optimizer benchmark. Fewer features or lower error is not a software-test requirement.

## The declared data and assessment

The [version 1 protocol](comparison-protocol.md) was written before this runner’s first execution. Cohort seed `26101602` and split seed `26101603` generate a new teaching draw from the existing engineered generator. The old case had already been inspected; the new draw does not turn that generator into independent clinical evidence.

There are 60 invented people with two specimen categories each. Reserve 15 people and their 30 specimens. The other 45 people and 90 specimens enter three shared outer folds. Both models predict each outer-assessment person exactly once. Only the selected procedure needs inner folds to choose k and C. Each procedure is then fitted on full development and assessed on the same reserved people. The runner exports both results and selects no deployment winner from them.

## Run and inspect

From the repository root with the [pinned dependencies](requirements-python.txt), including Matplotlib 3.10.8:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/examples/breast_cancer_comparison.py /tmp/breast-cancer-comparison
```

Choose a new output directory outside the repository whose parent exists. Existing outputs and symlinks are rejected. The run produces:

| Output | How to read it |
| --- | --- |
| `report.json` | Protocol/seeds, all split coordinates, six-candidate traces, matched assessment summaries, fixed settings and code/protocol hashes |
| `predictions.csv` | All 120 specimens, identity, target, development/test membership, outer fold, three probabilities and three squared errors |
| `models.joblib`, `synthetic_inputs.npz` | Both fitted procedures and invented input values for trusted prediction replay |
| `display-inputs.json` | Raw missingness masks, specimen identities, final coefficients and selection/importance summaries |
| `gallery/` | Seven figures in SVG, PDF and PNG, plus auditable plot calculations and calibration counts |
| `versions.json`, `sha256.json` | Runtime versions and file-integrity inventory |

The [plotting command](examples/plot_comparison.py) rebuilds figures from `report.json`, `predictions.csv` and `display-inputs.json`, without fitting a model or loading a model object. It rejects incomplete rows, broken pairs, incorrect fold labels, invalid probabilities, and disagreements between saved predictions and error summaries.

The [Rust deployment](rust-deployment.md) exports the two final development models into numeric JSON and applies their frozen preprocessing and coefficients in a compiled CLI. Its per-specimen parity checks verify runtime equivalence; in-sample development replay remains separate from the outer-held-out assessment above.

## Read the version 1 result

The [committed numeric example](gallery/example/report.json) and [specimen records](gallery/example/predictions.csv) produce the displayed gallery:

| Procedure | Outer-held-out development Brier | Reserved-test Brier |
| --- | --- | --- |
| Selected + tuned C | 0.144627 | 0.176303 |
| All features, fixed C | 0.175633 | 0.218904 |
| Training prevalence | 0.250000 | 0.250000 |

Brier error is the mean of `(probability - binary label)^2`; smaller is better. The saved difference is **selected minus all-feature**, so a negative difference favors the selected procedure on these invented observations. It does not establish clinical superiority, an optimized gene signature, calibration, or a feature-selection-only benefit.

Each person has exactly two specimens, so averaging the two errors per person and then averaging people gives the same mean as averaging all specimens here. With unequal specimen counts that equivalence would fail. The Brier and person-difference figures have no intervals. The calibration display separately includes conditional whole-person bootstrap ranges, with sparse bins withheld and training uncertainty omitted; these are not full-procedure or clinical confidence intervals. Overlapping outer folds are not independent patient cohorts.

## Learning checks

1. Recompute both Brier errors and their difference from `predictions.csv`; identify which people were excluded from fitting.
2. Explain why the comparator has four fits while the selected procedure has 76.
3. Find a person for whom the procedure with lower average error did worse, then explain why the average does not describe everyone.
4. Explain which further, separately assessed comparison would isolate selection from regularization tuning.
5. Describe what changes if one person contributes more specimens, or the target becomes recurrence time.

The [recorded comparison validation](evidence/comparison-validation-2026-10-16.json) passed all 19 Python tests across the four suites and replayed both saved comparison models with zero probability difference. The [expanded gallery validation](evidence/gallery-validation-2026-10-16.json) adds six diagnostic tests, for 25 tests across five suites, and retains three Python deployments. The earlier corpus run remains separately archived.

The [comparison tests](tests/test_breast_cancer_comparison.py) observe the comparator’s actual training inputs and transformations, perturb reserved values, replay both saved models, challenge malformed plot inputs and verify artifact hashes. The [corpus validation command](corpus-review.md#repeat-the-run) runs them and this deployment in CI. Tests require correct computation and boundaries, not a favorable metric.

Official implementation references: [binary Brier error, scikit-learn 1.8](https://scikit-learn.org/1.8/modules/generated/sklearn.metrics.brier_score_loss.html) and [figure export, Matplotlib 3.10.8](https://matplotlib.org/3.10.8/api/_as_gen/matplotlib.figure.Figure.savefig.html).
