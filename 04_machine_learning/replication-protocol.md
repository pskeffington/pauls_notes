# Phase 4B protocol: repeated synthetic cohorts and panel stability

Authored by Paul Skeffington · Compiled with OpenAI

[Gate ledger](../docs/roadmap-gates.md#g1-phase-4b-repeated-cohort-robustness) · [Learning roadmap](../docs/learning-roadmap.md#phase-4-study-robustness-before-making-search-more-elaborate) · [Baseline protocol](robustness-protocol.md) · [Machine-readable contract](evidence/replication-contract-v1.json) · [Breast cancer book, Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data)

**Protocol ID:** `paired-assay-replication-v1`. Declared on **2026-10-16** for a future implementation and assessment. This pass declares the protocol and seeds; it does not implement the replication runner, generate these cohorts, or report their results. The first commit containing this document and its JSON contract establishes the freeze. The runner must record that commit, both protocol-file hashes, and its own source revision before the first recorded assessment.

The existing Phase 4 outcomes have been inspected. These new seeds are declared without generating or screening their outcomes. This is a prospective **internal synthetic replication** using the same engineered generator, not external clinical validation or a clinical preregistration. Any amendment must explain whether these new outcomes were already viewed; amendments informed by outcomes are exploratory and need a new assessment boundary.

## Question and observation unit

Follow **people → specimens → measurements → data preparation → training → validation → prediction → biological interpretation**. Across three new draws from the paired-specimen generator, how do four fixed training procedures behave under the four established sensitivity scenarios? Are selected anonymous measurement panels, settings, ranks and coefficient signs stable enough to explain their limitations to a learner?

Each cohort contains **60 invented people, 120 specimens and 48 anonymous features**. Each person contributes one comparator specimen (`label=0`) and one tumor-labeled specimen (`label=1`). The endpoint is specimen category, not a person's cancer diagnosis, recurrence, prognosis or treatment response. Features are not the book's 60 named genes. Cohort-qualified person and specimen keys are mandatory because local IDs repeat across generated cohorts.

## Frozen cohorts and procedures

| Cohort ID | Generator seed | Reference split seed | Reallocation split seed | Perturbation seed |
| --- | --- | --- | --- | --- |
| `replicate_a` | 26101801 | 26101802 | 26101803 | 26101804 |
| `replicate_b` | 26101901 | 26101902 | 26101903 | 26101904 |
| `replicate_c` | 26102001 | 26102002 | 26102003 | 26102004 |

Execute each cohort in table order, with scenarios in this order: `reference`, `extra_missingness`, `correlated_measurement`, `reallocated_people`. Use the existing generator, 25% reserved-person allocation, three grouped outer folds and three grouped inner folds. There are 45 development people and 15 reserved people per scenario. The first three scenarios share development membership; reallocation may change it. Check that reallocation actually changes membership without searching for a preferable seed.

Retain the [baseline perturbation definitions](robustness-protocol.md#frozen-comparison-and-perturbations): 15% extra development-only dropout, and development Feature005 replaced by `0.99 × Feature001 + N(0, 0.05)` while preserving its old missing mask. Feature001 missingness can propagate. The same cohort-specific perturbation seed initializes each perturbation separately. Reserved measurements remain unmodified and unscored. These probes do not simulate future patients exposed to a new assay environment.

Retain all four procedures and their original implementations:

| Procedure | Frozen selection rule | Fits per scenario |
| --- | --- | --- |
| `grid` | Six candidates in existing order: `C` in `0.1, 1.0`, then `k` in `5, 10, 20`; lowest mean inner-fold Brier, first candidate wins an exact tie | 76 |
| `random` | Six unique candidates from the existing 36-combination space, sampled without replacement with **search seed 26101715**; same Brier and tie rule | 76 |
| `all_feature` | Existing fixed `C=1.0` classifier on all 48 features; no tuning | 4 |
| `prevalence` | Outer-training specimen prevalence, computed without model fitting | 0 |

Keep the randomized candidate draw identical across cohorts and scenarios to avoid confounding new cohort draws with new search draws. Preserve the existing pipeline order, estimator defaults, training seed, `max_iter=1000`, median imputation and standardization. Every learned transformation and feature score must use its fitting slice only. Do not change the generator, search space, feature count, metric, winner rule or solver after seeing replication outcomes.

Per search, `6 candidates × 3 inner folds + 1 refit = 19` pipeline fits. Per scenario, `2 arms × 4 searches × 19 + 4 fixed fits = 156`. The full assessment has **12 cohort/scenario cells, 1,872 pipeline-fit attempts and 1,080 prediction rows**, with four probabilities per row. It includes 24 full-development selected-model refits and 12 full-development all-feature refits, which produce no reserved-person predictions. Prevalence arithmetic is not a pipeline fit.

Use one worker with `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1`, the existing [dependency pins](requirements-python.txt), and a **2,700-second** wall budget for the full run. Check the deadline before every attempted fit and after execution; a pre-fit check cannot interrupt a fit already running. Budget or convergence failure does not justify additional candidates, seed replacement or unrecorded retries.

Treat scikit-learn `ConvergenceWarning` as a recorded fit failure; a nonconverged fit cannot supply an accepted selection score or prediction. Other warnings remain visible with their fit identity. A successful full run still requires all 1,872 attempts and no failed fits.

## Predictions, losses and denominators

Every eligible development specimen receives exactly one outer-held-out prediction from each procedure. Save `cohort_id`, `scenario`, local row coordinate, person ID, specimen ID, label, outer fold and the four probabilities. Keys must be unique within `(cohort_id, scenario, specimen_id)`. Every person's two specimens must share the same outer fold and remain together in every inner split. No reserved row appears in a prediction or metric.

Primary loss is **equal-person mean Brier error**: average squared probability error over a person's two specimens, then average the 45 person losses. Compute paired **other minus grid** differences per person for random, all-feature and prevalence. Negative favors the other procedure. Also retain each person's component losses. In this balanced fixture only, specimen-mean and equal-person-mean Brier coincide. Do not average the two labels into a fictitious patient-level binary target.

Report ROC-AUC and average precision on the **90 specimen predictions**, with **45 positive specimens, 45 negative specimens and 45 people** per cell. Report their observation unit and denominators explicitly. These descriptive scores retain within-person dependence. The prevalence procedure has tied probabilities; do not remove it or treat ties as an error. Unexpected missing categories or nonfinite/out-of-range probabilities fail validation rather than receiving substitute scores.

Keep all 12 cells and all four procedures visible. A scenario summary may show the equal-weight mean, minimum and maximum of the three cohort-level losses, but not a confidence interval from three draws. Scenarios from one cohort overlap and are not independent studies. Do not pool rows across scenarios to inflate sample size or make an unconditional paired reference-versus-reallocation contrast when membership differs. Within a cell, the four procedures are paired on the same excluded people.

## Stability and candidate histories

Record all successful and failed candidate/fold fits, refits, parameters, slice IDs, elapsed time, warnings and errors. Each selected pipeline fit must record its selected anonymous features and signed standardized coefficients. Compute F-score ranks from median-imputed **fitting measurements only**, before selecting columns: descending F score with average ranks for ties. Undefined F scores/ranks remain explicitly null with a reason; never silently replace them by an apparent best or worst rank. Record all-feature signed standardized coefficients separately.

Distinguish the following denominators in machine-readable summaries:

| Summary | Denominator and scope |
| --- | --- |
| Primary selection frequency | Three chosen outer refits per method per cohort/scenario; nine per method per scenario across cohorts |
| All-fit selection frequency | Every successful selector-containing fit, identified by candidate, inner fold or refit role; nominally 76 per method/cell; descriptive and heavily overlapping |
| Outer panel overlap | All three pairwise Jaccards within a cell; all 36 pairwise Jaccards among the nine outer panels for a method/scenario, with cohort/fold IDs retained |
| Final panel overlap | Full-development refits reported separately: three between-cohort pairwise Jaccards per method/scenario; do not mix with the nine outer panels |
| Rank variability | Per-feature fitting-only F-score ranks across chosen outer fits; report contributing fit counts, median and range; ties are retained |
| Coefficient sign variability | Counts of negative, exactly zero and positive coefficients **conditional on selection**, with the selected denominator; unselected is absent, not a zero coefficient |
| Candidate selection frequency | Parameters chosen in outer refits, three per method/cell and nine per method/scenario; full-development choices in a separate table |

Jaccard is intersection size divided by union size. Retain each panel pair and its overlap so averages can be audited. Repeated candidate fits on the same training people are not independent evidence. Rank and coefficient differences describe feature dependence and fitting behavior, not causal effects or biological validation. Do not use assessment permutation importance or replication results to redesign the evaluated panels.

## Required artifacts and execution boundary

The forthcoming runner and its tests must retain the current single-cohort experiment as an independently replayable baseline. A parameterized extension must reproduce that baseline's predictions to absolute tolerance `1e-12` in the pinned Python environment before assessing the new cohorts; runtime fields need not agree. Use separate function arguments or immutable configuration rather than temporarily mutating module-global seeds.

Publish each recorded run to a newly named directory outside the source repository. The complete artifact bundle must contain:

- Versioned protocol/config snapshots, freeze commit, execution source revision, source hashes, generator-input hashes, dependency versions, Python/platform/CPU information, thread settings, commands and timestamps.
- Per-cell person/specimen allocation, full outer/inner membership and complete attempted-fit histories, including final refits and all-feature fits.
- Development-only predictions, paired person losses, per-procedure metrics and the stability/settings summaries above.
- Actual fit attempts, successes, failures, convergence warnings and time/cost by cell and procedure; arithmetic must reconcile with the fit ledger.
- A report with explicit `software_pass` or `software_fail`, plus a SHA-256 manifest covering every output except the manifest itself.

Failure records must survive an aborted search, a failed refit, a budget exception or an all-candidates-failed case. Publish a clearly labeled failed bundle with available histories and no fabricated scores. A failed cell means G1 remains open; do not drop it from a successful-looking average. Validate unused output paths and reject unsafe or existing destinations before fitting. Keep full artifacts outside Git and commit only the compact report, archive identity, retention/expiry information and digest inventory.

Separate two CI modes. A **PR smoke check** uses only the already inspected legacy cohort, runs one 156-fit reference cell plus focused failure/fixture tests, and makes no G1 completion claim. The **bounded full run**, after the freeze commit, executes exactly the declared 12 cells with 1,872 fits and preserves its complete artifacts even on failure. No smoke-test pass can substitute for this full evidence. Uploads must run on failure as well as success and document their retention; an expiring archive is not a promise of permanent availability.

## G1 acceptance and next step

G1 closes only after the frozen protocol precedes assessment, all 12 cells execute, partitions and all required predictions are audited, 1,872 attempts and complete histories reconcile, stability and unfavorable results are retained, hashes verify, regression and deliberate-failure tests pass, and the report receives scientific-scope review. No minimum AUC, smaller panel or search winner is required.

The **next executable development pass** implements the runner, regression tests and interpretation guide against this contract, proves legacy compatibility, and then records the full assessment. G1 is currently **Planned**, with this protocol sub-gate delivered for review. [G2](../docs/roadmap-gates.md#g2-phase-4c-uncertainty-and-reliability) will separately declare a paired whole-person bootstrap estimand conditional on saved predictions; no intervals are implemented or claimed here. A complete-training-procedure uncertainty experiment would require a separate protocol and fit budget. Phase 5 remains dependent on G1/G2, while native Rust training can proceed independently.
