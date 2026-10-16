# Corpus review and validation — 16 October 2026

[Evidence guide](breast-cancer-evidence.md) · [Paper-by-paper review](evidence/paper-review.csv) · [Executed validation record](evidence/validation-2026-10-16.json) · [Book, Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data)

The review covers **all 36 publications in the ML evidence register**: eight breast cancer reports and 28 methodological/reporting references. It does not cover the separate biomedical literature matrix or reappraise the book’s 60 individual gene accounts. **33 papers received selected full-text review; three remain abstract-limited. No external paper’s model-training results were reproduced.**

The review examined the research question, population or benchmark, outcome, partition design, selection/preprocessing, assessment, uncertainty, implementation availability and relevance to our assay narrative. It is an editorial methods appraisal, not an exhaustive supplementary-material audit, systematic review, or completed PROBAST+AI/TRIPOD+AI assessment. Reading a paper, checking its processed output and retraining its models are different activities.

## What changed after reading the methods

| Finding | Consequence for the corpus and project |
| --- | --- |
| PRAIM’s cohort flow reconciles its two denominators | Figure 1 accounts for 1,276 exclusions. The observational analysis also changed in response to reader self-selection; adjusted comparisons cannot be replaced by a raw cancer-count ratio |
| Mirai uses repeated examinations and defined follow-up eligibility | Keep examination and patient counts distinct. All-Hologic evaluation and previously analyzed cohorts constrain device and independence claims |
| Sammut’s complete-data analysis and search are more specific than its abstract | Record 147 complete molecular/pathology cases separately from 168 profiled patients. The paper describes 1,000-trial randomized fivefold tuning and repeated-seed/algorithm averaging; our small logistic example does not reproduce that ensemble |
| The Park preprint separates source-held-out development from external evaluation, but includes post hoc evaluation sweeps | Preserve inferred-expression provenance; treat the component-count sensitivity plots as exploratory, rather than a fresh confirmatory choice |
| The 2026 survival benchmark has an explicit failed-fit policy | Its published setup uses Kaplan–Meier fallback scores for failures. Retain error flags, uncomputed metrics and objective-specific denominators before interpreting rankings |
| Current source and paper-era source are different objects | Pinned SMAC3, Bommert and Burk inspections identify exactly which file was read; none establishes package execution or full end-to-end reproduction |

Primary sources for these findings: [PRAIM](https://doi.org/10.1038/s41591-024-03408-6), [Mirai](https://doi.org/10.1200/JCO.21.01337), [Sammut](https://doi.org/10.1038/s41586-021-04278-5), [Park version 1](https://arxiv.org/html/2610.03693v1), and [Burk](https://doi.org/10.1093/bioinformatics/btag186). Exact sections and access provenance for all 36 papers are in the [review ledger](evidence/paper-review.csv); document digests identify locally retrieved sources without copying their full text into the repository. The Riley binary-outcome paper was reviewed through publisher web text and therefore has no downloaded-file digest.

## Coverage and unresolved access

| Review scope | Records | What remains unresolved |
| --- | --- | --- |
| Selected full-text methods/results, limitations and availability | BC-01, BC-04–BC-08; BC-M01–BC-M20; BC-M22–BC-M28 | Full supplementary audits, implementation fidelity and independent reproduction remain separate tasks |
| Structured/indexed abstracts and bibliographic verification | BC-02, BC-03, BC-M21 | Full methods were not obtained from the accessible routes; maintain abstract-only scope |

For MASAI, the two reports concern the same trial. The 2026 primary interval-cancer finding is noninferiority under its declared margin, not a demonstrated reduction in interval cancers. The multi-objective biomarker abstract motivates a panel-size/stability question but is insufficient to approve its reported breast cancer panel for use here. These access limits remain visible instead of being filled with inferred methods.

BC-06 and BC-08 both use TransNEO. Treat that named-cohort overlap as a reason to check individual-level provenance before counting their results as independent evidence. Repeated cohort names across other multimodal papers also require reconciliation; matching names alone do not prove matching participants.

The methodological sources support training boundaries, comparators, budget accounting and reporting. Benchmark-level optimizer rankings, speedups and generalization findings are not breast cancer efficacy estimates. None of the reviewed studies validates our invented paired-specimen classifier, and neither a prognosis model nor response under received treatment establishes counterfactual treatment benefit.

## Published-output check

We downloaded the author’s [processed survival scores at commit 37d04d1](https://github.com/slds-lmu/paper_2023_survival_benchmark/blob/37d04d15993cb1f3771dbb784ea7251e0b512b1d/results/production/scores.csv) and audited the CSV without executing external source code or loading model objects:

| Check | Observed result |
| --- | --- |
| Rows / datasets / learners | 24,750 / 34 / 21 |
| Duplicate dataset–learner–iteration–objective keys | 0 |
| Rows with error flags / warning flags | 462 / 2 |
| Finite Harrell/Uno C values, each | 15,750; 9,000 missing or uncomputed |
| Finite ISBS, ISLL, D-calibration and alpha-calibration values, each | 12,750; 12,000 missing or uncomputed |
| File SHA-256 | `e2292668b46e9ba26f2bbb0372e8274a7731101a4bf3f983d133a8fd660776e6` |

Missing or uncomputed values are not all failed fits: some metrics are evaluated only for particular tuning objectives or prediction types. Error flags and valid fallback scores can coexist. The audit preserves these distinctions and does not impute scores, pool objectives, recompute critical-difference tests, refit any learner, or confirm the paper’s inferential conclusions. The inspected README states that large raw benchmark-result objects are omitted and describes an R 4.4.3/renv/HPC setup; the processed CSV is a narrower artifact.

Aggregate arithmetic was also checked directly: PRAIM’s participant flow and the 2025 MASAI arm totals, detection rates, rate ratio and workload reduction reconcile with the published rounded values. Confidence intervals, p-values and model-based adjusted effects were not recomputed. These are consistency checks of reported numbers, not an independent clinical reanalysis.

## Executed project validation

The [validation command](validation/run_validation.py) ran both documented Python deployments and all three Python test suites: **14 tests passed**. It also checked the evidence register/review ledger, saved paired-model prediction replay, file hashes, 48 distinct feature-review rows, and three fixed synthetic cohort seeds. Perturbing every reserved-test measurement and reversing its labels left development fitting and its report unchanged for the declared perturbation check.

| Synthetic seed | Outer-held-out Brier error | Reserved-test Brier error | Selected columns |
| --- | --- | --- | --- |
| 261016 | 0.085600 | 0.090770 | Feature001, Feature002, Feature003, Feature004, Feature005 |
| 261017 | 0.101381 | 0.073662 | Feature001, Feature002, Feature003, Feature005, Feature043 |
| 261018 | 0.101039 | 0.157348 | Feature001, Feature002, Feature003, Feature005, Feature029 |

Each cohort has 45 development people and 15 reserved-test people, two specimens per person and an engineered signal. Each standard search procedure uses 76 pipeline fits. No seed was selected because of its test result. These three generated cohorts are software stress cases, not clinical cohorts, a confidence interval, a null simulation, or evidence of optimized breast cancer performance. Noise features appearing in some selected panels illustrate why selected-column identity needs its own interpretation.

This section records the earlier validation, before the comparison deployment was added. Those numeric results remain descriptive. A later [fixed all-feature comparison](model-comparison.md) now assesses two complete procedures on a newly declared synthetic draw; it still does not isolate a feature-selection-only gain. The checks verify boundaries and replay; they do not certify biological validity, external-site transportability, calibration, treatment usefulness, or every possible leakage path.

The local environment had the pinned Python dependencies and no Rscript. Therefore no local R execution is claimed in the recorded JSON. The repository’s separate R CI jobs execute caret and direct-R checks on the published commit. Their environment and results should be assessed separately from this local run. Logs and full synthetic artifacts are written to the chosen run directory; the committed JSON records versions, commands, source digests and observed results.

## Repeat the run

From the repository root, with the [pinned Python dependencies](requirements-python.txt):

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/validation/run_validation.py /tmp/pauls-notes-validation
```

Choose a new directory outside the repository whose parent exists. Without `--scores-csv`, the published-artifact audit explicitly records `not_run`. To repeat that additional check, obtain the CSV from the pinned author URL above, preserve its bytes, and supply its local path:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/validation/run_validation.py /tmp/pauls-notes-validation-with-scores --scores-csv /tmp/burk-scores.csv
```

The command checks the reviewed SHA-256 before parsing that artifact and never executes downloaded code. A checksum mismatch requires reviewing the new artifact rather than silently substituting it. The ordinary project run remains offline once Python dependencies are installed. A successful run exits zero and writes `validation.json`; command failures or integrity violations produce a failed report and a nonzero exit.

Before extending the breast cancer study, resolve the full-text access gaps, review the relevant paper-era artifact and permissions, specify the real cohort/assay/endpoint contract, and assess any new procedure independently. This review supplies a traceable starting point and an executed software check, not a blanket validation of the literature.
