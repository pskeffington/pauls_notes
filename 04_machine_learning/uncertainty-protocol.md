# Phase 4C protocol: conditional whole-person uncertainty

Authored by Paul Skeffington · Compiled with OpenAI

[Gate ledger](../docs/roadmap-gates.md#g2-phase-4c-uncertainty-and-reliability) · [G1 report](replication-experiment.md) · [Machine-readable contract](evidence/uncertainty-contract-v1.json) · [Frozen input](evidence/uncertainty-input-v1.json) · [Breast cancer book, Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data)

**Protocol ID:** `paired-assay-conditional-uncertainty-v1`, declared **2026-10-16**. The first commit containing this protocol, its contract and its compact input snapshot establishes the freeze. G1 point estimates, selected panels and stability results have already been inspected. No G2 resampling outcomes have been computed when declaring this contract. This is a prespecified descriptive follow-up to an inspected synthetic experiment, not a blinded confirmatory clinical analysis. Any outcome-informed change requires an explicitly exploratory amendment and a new assessment boundary where relevant.

## Question, input and estimand

Follow **people → specimens → measurements → data preparation → training → validation → prediction → biological interpretation**. Holding the existing G1 predictions fixed, how does equal-person paired probability loss vary when the empirical set of development people is resampled? Separately describe the observed effects of development allocation, measurement correlation, missingness and candidate choices without attributing a variance component that the design cannot identify.

Use only the verified G1 CI archive from source `3cef4b52b1124e988eedd0c7811cc7fa9de4d3dd`, workflow run **38936820625**, artifact **12062065184**, archive SHA-256 `e13edef4d52ea60439f0e5704b7add03f843050645a90777c7e47a88875c766a`. Its prediction file SHA-256 is `efaaca18f939a96d197000e30050065d4ab918ce850fd2652b1ada6b8ae1f514`. The compact input snapshot preserves the same 1,080 prediction rows in declared field order and canonical cohort/scenario/person/label order. It is a bounded teaching fixture, not a copy of the substantial fit histories, measurement matrices or experimental outputs. Its source identities and content hash are frozen in the contract; replay does not depend on continued availability of the expiring CI archive.

Each of 12 cohort/scenario cells has **45 development people, 90 specimens, one comparator and one tumor-labeled specimen per person**. The four procedures are grid, random, all-feature and prevalence. No reserved-person record is admitted. IDs are qualified by cohort and scenario. Each paired person must have unique specimen/row identities, binary labels `{0,1}`, and one outer-fold identity. All probabilities must be finite and in `[0,1]`. Reject missing, duplicated, contradictory or extra records before resampling.

For person `i` and method `m`, define `L[i,m]` as the mean of the two squared specimen probability errors. Define `D[i,m] = L[i,m] - L[i,grid]` for **random, all-feature and prevalence**, in that order. The reported point contrast is the mean of the 45 person differences. Negative favors the other procedure. People receive equal weight; neither specimens nor folds are the resampling unit. Do not average the paired labels into a fictional patient-level cancer outcome.

The operational target is the **equal-person mean paired loss contrast represented by the frozen prediction records**, with empirical-person resampling used to describe its sensitivity to person composition. For a population interpretation this would additionally require suitable exchangeability/independence assumptions for person-level loss records. G1 outer predictions share fitted training sets; freezing predictions does not establish those assumptions or remove training-induced dependence. Therefore report **pointwise 95% conditional person-bootstrap percentile ranges**, not validated confidence intervals for the entire training procedure, a new population, or a clinical endpoint. No nominal coverage guarantee is claimed for these pooled out-of-fold records.

## Frozen resampling calculation

| Choice | Declared value |
| --- | --- |
| Cells | Cohorts `replicate_a`, `replicate_b`, `replicate_c`; within each, `reference`, `extra_missingness`, `correlated_measurement`, `reallocated_people` |
| Person order | Ascending local person ID within each cell; both specimens carried together |
| Draws | **10,000** bootstrap replicates per cell, each sampling 45 person positions with replacement |
| Pairing | The same resampled person indices are used for all three contrasts within a cell |
| RNG | NumPy `Generator(PCG64(SeedSequence([26102101, cohort_index, scenario_index])))`; indices are zero-based, in the table order |
| Sampling call | `integers(0, 45, size=(10000, 45), dtype=int64)` once per cell; save every draw index |
| Statistic | Arithmetic mean of the sampled person differences, separately for each contrast |
| Range | Quantiles **0.025 and 0.975**, NumPy `method='linear'`, independently for each contrast |
| Conditional spread | Sample standard deviation of the 10,000 replicate means, `ddof=1`; label as empirical-resampling spread |
| Analytic reference | Conditional empirical-bootstrap SD for a mean: `sqrt(mean((D-mean(D))**2)/n)`; this is not a full-procedure standard error |
| Degeneracy | If person differences are constant, retain the collapsed range and explicit flag; this does not establish absence of uncertainty |
| Budget | **120,000 person-index resamples**, **360,000 contrast replicate means**, **36 ranges**, **zero new pipeline fits**, one worker, maximum 300 seconds |

The simple percentile calculation is chosen for transparent numeric replay and teaching. Do not select BCa, a different tail probability, more draws, a new seed or a favorable subset after viewing these outcomes. Ranges are pointwise, not simultaneous across 36 contrasts, and are not hypothesis tests or a model-selection rule. A zero-excluding range cannot be used to redesign a panel or claim optimizer superiority from this assessment. No bootstrap ROC-AUC/AP/calibration interval is in scope.

## Reliability description and what remains unidentified

Prespecify these descriptive summaries from the same frozen records, with no additional intervals:

- For each cohort/scenario/method, retain person and specimen counts, equal-person Brier, point contrast and bootstrap range.
- For each cohort and perturbation, report reference/scenario development-person intersection, exclusive counts and common-person mean loss changes for each method. Missingness/correlation should retain the same people; reallocation changes membership. Common-person comparisons may also change fitted models and folds, so they do not isolate a measurement or allocation causal effect.
- Preserve G1's observed candidate-choice frequencies, panel/rank/sign variation and their source record. These show instability of the declared procedures under the probes, without isolating candidate selection from changes in training data.
- **Model fitting variability is not separately estimated**: no repeated fits at fixed training inputs or full-procedure resampling are performed. Correlation, missingness, person composition, candidate choice and fitting interactions cannot be decomposed into independent variance components here.

Full-procedure uncertainty would need a separate frozen protocol and budget repeating preprocessing, selection, tuning and fitting within the necessary resampling/evaluation boundary. It remains a distinct extension, not something supplied by this conditional calculation. Fold standard deviations are never substituted for person-level intervals.

## Software evidence and artifacts

Before assessing frozen G1 records, test paired aggregation, a known two-person numeric fixture, exact small-sample enumeration, linear quantiles, zero/constant differences, deterministic shared draws, seed separation and an independent SciPy paired-percentile calculation. Deliberately reject missing partners, mismatched labels/folds/IDs, duplicate rows, invalid probabilities, unknown/absent cells and unsafe output paths. Tests must use numeric teaching fixtures and must not compute the G1 ranges before this protocol is committed.

The full runner must validate the frozen input hash, protocol/config bytes and committed source revision before computing the recorded assessment. It saves input/protocol snapshots, per-person losses and contrasts, every index draw and replicate mean, summary ranges, reliability descriptions, versions, exact commands, source/input hashes, runtime and an output SHA-256 manifest. Write complete or clearly labeled failed bundles to new directories outside the repository; never overwrite prior evidence. Preserve unfavorable and degenerate results. Include a second-process audit and a separately executed CI replay against the same frozen input. Keep substantial generated arrays outside Git and commit a compact verification record.

Acceptance requires the estimand and limits to remain explicit; all 12 cells and 36 contrasts; person dependence and method pairing preserved; numeric fixture and malformed-structure tests; complete draw/result replay; correct denominators; output hashes; zero new fits; and scientific-scope review. No desired interval width, preferred winner or zero-exclusion threshold is required. G1 plus this G2 closes the defined Phase 4 **synthetic research-software** milestone only. Learner mastery, full-training-procedure uncertainty and clinical validity remain unestablished; Phase 5 must still introduce its own survival endpoint and protocol.

## Primary method references

- [SciPy 1.17 bootstrap documentation](https://docs.scipy.org/doc/scipy-1.17.0/reference/generated/scipy.stats.bootstrap.html): paired sampling uses common resampled indices. Used as an independent arithmetic reference, not evidence of coverage for this design.
- [NumPy 2.3 quantile documentation](https://numpy.org/doc/2.3/reference/generated/numpy.quantile.html): specifies linear interpolation for the frozen percentile endpoints.
- [Bengio and Grandvalet (2004)](https://jmlr.org/papers/v5/grandvalet04a.html), already [BC-M09](breast-cancer-evidence.md#bc-m09): overlapping training sets complicate cross-validation variance; naive independent-fold reasoning can understate it.
- [Bates, Hastie and Tibshirani, arXiv v4 (2022)](https://arxiv.org/abs/2104.00673v4): distinguishes error targets and documents deficient coverage of usual cross-validation intervals. This source informs the limitation; its proposed refitting method is not reproduced here.

These method references supplement the corpus; they do not add new clinical evidence or claim a paper reproduction.
