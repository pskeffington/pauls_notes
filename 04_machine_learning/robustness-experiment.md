# Robustness experiment: changing the data, not the clinical claim

Authored by Paul Skeffington · Compiled with OpenAI

[Protocol](robustness-protocol.md) · [Roadmap](../docs/learning-roadmap.md#phase-4-study-robustness-before-making-search-more-elaborate) · [Matched baseline](model-comparison.md) · [Model tuning](model-tuning.md) · [Breast cancer book](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data)

The book progresses from **people → specimens → measurements → prediction → assessment → interpretation**. For an invented paired breast-tissue assay, Phase 4 now has a runnable experiment that asks what happens when the development people, missing measurements or correlated assay columns change. It keeps the prior six-candidate feature-selection procedure and the all-feature classifier, then compares a fixed-budget random search against the original grid. There are no real gene expression matrices or patient records in this exercise.

## Run the versioned protocol

Install the [pinned Python requirements](requirements-python.txt) and run from the repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/tests/test_breast_cancer_robustness.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/examples/breast_cancer_robustness.py /tmp/breast-cancer-robustness
```

Use a new output directory outside the repository; the script rejects existing directories and symlinks. By default, it executes four prespecified scenarios with **624 candidate/fold/refit attempts** and one worker. To run a smaller smoke check, explicitly restrict the scenario and the matching budget:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/examples/breast_cancer_robustness.py /tmp/breast-cancer-robustness-smoke --scenario reference --max-fits 156
```

The full report keeps complete candidate histories, training/assessment row coordinates, failures, per-method Brier errors, selected panels, selection-frequency tables and measured runtime. `development_predictions.csv` contains **only outer-held-out development specimens** with IDs, target, fold and four probabilities. `versions.json` identifies the environment; `sha256.json` checks the other output files. A staged output is published only on successful completion.

## The assessment boundary

<https://scikit-learn.org/1.8/modules/generated/sklearn.model_selection.GroupKFold.html> documents group partitioning. Each person contributes one 0-labeled and one 1-labeled specimen; the two stay together in outer and inner folds. Each inner candidate learns the median imputer, F-score selection, scaling and logistic coefficients *only* from its own analysis people. An outer-assessment person cannot influence an inner candidate or its selected settings. After three outer folds, the method refits on development people for its final feature panel, but **never scores the reserved test people** in Phase 4.

A common outer split makes the grid, random, fixed all-feature and prevalence predictions directly paired **within a scenario**. The reallocated-people scenario intentionally has different development membership and cannot be treated as an independent trial or as a paired comparison against all the reference-scenario people. Reusing the same deterministic generator does not provide real-world cohort diversity.

## Read the gate evidence

1. Open `report.json` and compare `budget.planned_fits`, `budget.actual_fits` and the failed-trial counts. The original grid and randomized extension each use 76 pipeline fits per scenario; the all-feature baseline receives four.
2. Compare `development_metrics` for all four procedures. Use **Brier error** as primary, lower-is-better; ROC-AUC and average precision are descriptive, not selection metrics. A positive `comparison_vs_grid_brier.random` means the original grid did better on that synthetic development slice.
3. Trace one person's two rows in `development_predictions.csv`, then find that person's fold in `outer` and the three inner fold assignments in `searches`. Demonstrate the absence of person overlap.
4. Look at `stability.grid.selected_outer_frequency` and the pairwise Jaccard values. Name a selected-column swap and explain why correlated alternatives can exchange ranking; the anonymous columns are **not** the 60 named genes in the book.
5. Recalculate the mean squared error per specimen, then average the two errors per person. Explain why those means agree for this fixture and may differ when people contribute unequal specimen numbers.
6. Challenge the protocol: additional missingness, altered correlations and changed development people could make a procedure worse. No model is declared a winner from four overlapping stress cases, and these results cannot be used to redesign a panel and then claim its reused assessment as fresh validation.

## Implementation acceptance and remaining work

The test suite checks exact person-separated membership, complete fold coverage, six candidate histories per search, fit accounting, score replay, selected-panel sizes, output hashes, deliberate failed-candidate recording, output protection, and **reserved-value invariance** after extreme perturbation of withheld measurements and labels. GitHub CI runs the full four-scenario job separately from the existing comparison, corpus-validation and Rust-parity jobs.

This completes a bounded **Phase 4 software implementation gate**, not all of Phase 4 scientific review or personal mastery. An independent repeat on a new declared generator/data source, an appropriate cluster-aware uncertainty plan, and a separate native Rust fitting experiment remain planned. No clinical diagnostic or therapeutic interpretation is supported.
