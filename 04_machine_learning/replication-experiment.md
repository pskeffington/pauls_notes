# Phase 4B repeated-cohort robustness report

Authored by Paul Skeffington · Compiled with OpenAI

[Frozen protocol](replication-protocol.md) · [Contract](evidence/replication-contract-v1.json) · [Gate ledger](../docs/roadmap-gates.md#g1-phase-4b-repeated-cohort-robustness) · [Breast cancer book, Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data)

This implements the book's **people → specimens → measurements → data preparation → training → validation → prediction → biological interpretation** narrative using three new draws from the existing invented paired-specimen generator. It predicts specimen category from 48 anonymous measurements, not recurrence or the book's named genes. The [protocol](replication-protocol.md) and JSON contract remain byte-for-byte frozen at `65a0b8776a876c0a845e6f9f57c067adb30f713e`; their historical declaration says the assessment was not yet executed at that freeze. This guide and the gate ledger carry subsequent execution status.

## Run and audit

Use the [pinned dependencies](requirements-python.txt) and a fresh output directory outside the repository with an existing parent. From the repository root:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/tests/test_breast_cancer_replication.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/examples/breast_cancer_replication.py /tmp/assay-replication-smoke
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/examples/breast_cancer_replication.py /tmp/assay-replication-full --mode full
python3 04_machine_learning/examples/breast_cancer_replication.py /tmp/assay-replication-full --audit-only
```

The default smoke run and all regression fixtures use the **already inspected legacy cohort only**. Tests prove original-procedure prediction parity to absolute tolerance `1e-12`, person grouping, reserved-value invariance, rank ties/null reasons, sign denominators, failed candidate/refit retention, convergence failure, timeout handling, output protection and saved-record corruption rejection. The legacy runner remains separately executable. Its only extension accepts explicit scenario seeds, with original defaults preserved.

Full mode requires committed computational source files, unchanged frozen protocol/config bytes, pinned dependencies and the declared single-thread settings before generating new cohorts. It runs 12 cells with a ceiling of **1,872 attempted pipeline fits**, four procedures and **1,080 development-only prediction records**. The 2,700-second ceiling includes fitting and diagnostics; pre-fit deadline checks cannot interrupt an already running fit.

The [replication workflow](../.github/workflows/assay-replication-validation.yml) runs legacy-only smoke checks on ordinary PRs. A separate bounded full job runs on pushes to `main`, the declared implementation branch, or manual workflow dispatch, after smoke succeeds. Full and failed-run artifacts upload with `if: always()` and a requested **90-day** retention; smoke artifacts use 14 days. A PR smoke pass alone cannot close G1.

## Read the output

| Artifact | Contents and interpretation |
| --- | --- |
| `report.json` | Protocol freeze/source revisions, per-cell allocations, outer/inner membership, complete candidate decisions, person losses, metrics, cost and explicit pass/fail |
| `predictions.json` | Cohort/scenario-qualified development specimens, local IDs, labels, outer folds and four held-out probabilities |
| `fits.json` | Every attempted fit's role, training/assessment rows, parameters, outcome, warnings, elapsed seconds, fitting-only F ranks and signed standardized coefficients |
| `fit-events.jsonl` | Flushed start and terminal events; an interrupted process can leave a started event without a terminal event, which is not success |
| `stability.json` | Separate within-cohort and across-cohort summaries; outer versus all-fit frequency, panel Jaccards, rank ranges, conditional signs and candidate-choice counts |
| `inputs-*.npz` | Invented cohort/scenario measurements and identity metadata; reserved rows are saved for provenance, never predicted or scored |
| `environment.json`, `protocol.md`, `contract.json` | Versions, platform/CPU/thread settings, invocation and unchanged protocol snapshots |
| `sha256.json` | Every output file except the manifest itself; bundle audit verifies full coverage and hashes |

An exception preserves the available fit history, prediction records, error and manifest with `software_fail`; it never substitutes scores or marks a partial experiment complete. A hard process termination may leave an incomplete running snapshot and journal; it cannot be accepted as a completed run. Input preflight rejects invalid destinations before creating an output bundle. Do not load arbitrary pickled models: these input NPZ files are inspected with `allow_pickle=False` and no model pickle is required for the audit.

## Interpretation and review

For each cell, first confirm **45 development people, 90 specimens, 45 positive and 45 negative labels**. Average squared probability error within each person's two specimens, then over people. Paired contrasts are **other minus grid**; negative favors the other procedure. ROC-AUC and average precision operate on specimen categories with the same within-person dependence; averaging the two labels does not create a patient-level cancer endpoint.

Across cohorts, compare the nine chosen outer panels per method/scenario, while retaining their three-fits-per-cohort grouping. All-fit frequency has 228 overlapping fits per selected method/scenario and must not be interpreted as 228 independent studies. Final development panels have their own three between-cohort pairwise Jaccards. Rank summaries use fitting-only F scores; signs are conditional on a feature being selected. An absent feature is not a zero coefficient. The all-feature comparator's 12 fits per scenario across cohorts are not an equal-budget search.

Missingness and correlation perturb development measurements only. Reallocation changes assessed development people. No unconditional paired comparison across all reference/reallocation rows is justified. No minimum AUC, preferred winner, gene significance, clinical utility or confidence interval is an acceptance condition. [G2](../docs/roadmap-gates.md#g2-phase-4c-uncertainty-and-reliability) separately requires a declared whole-person conditional uncertainty estimand; none is supplied by fold spread or by three cohort draws.

## Recorded assessment

The full assessment used committed implementation `3cef4b52b1124e988eedd0c7811cc7fa9de4d3dd`, after the protocol freeze. The [compact verification record](evidence/replication-validation-2026-10-16.json) retains exact commands, versions, source/input/output digests, all 12 cells' Brier/ROC-AUC/AP values, denominators, stability summaries and the rejected-artifact history. [PR #3](https://github.com/pskeffington/pauls_notes/pull/3) delivers the implementation and review record. Ten new tests plus seven baseline tests passed; documentation/evidence suites add 17 passing tests, **34 local tests total**.

### All twelve cells

These are equal-person Brier errors, rounded for display. Each cell contains 45 people, 90 development specimens and 156 fits; the prevalence Brier is 0.25 in every cell. Negative **random minus grid** favors random search.

| Cohort | Scenario | Grid | Random | All-feature | Random minus grid |
| --- | --- | --- | --- | --- | --- |
| A | Reference | 0.121306 | 0.101734 | 0.127851 | -0.019573 |
| A | Extra missingness | 0.155682 | 0.163716 | 0.200326 | +0.008034 |
| A | Correlated measurement | 0.116885 | 0.083159 | 0.121774 | -0.033726 |
| A | Reallocated people | 0.134439 | 0.145574 | 0.179212 | +0.011134 |
| B | Reference | 0.147690 | 0.145467 | 0.160511 | -0.002223 |
| B | Extra missingness | 0.159640 | 0.171910 | 0.187583 | +0.012270 |
| B | Correlated measurement | 0.152792 | 0.168403 | 0.182342 | +0.015611 |
| B | Reallocated people | 0.184523 | 0.173751 | 0.206664 | -0.010773 |
| C | Reference | 0.094890 | 0.116606 | 0.098254 | +0.021717 |
| C | Extra missingness | 0.097637 | 0.125781 | 0.111357 | +0.028144 |
| C | Correlated measurement | 0.094110 | 0.117013 | 0.102650 | +0.022902 |
| C | Reallocated people | 0.110779 | 0.124868 | 0.179482 | +0.014090 |

Random search improves error in **four cells and worsens it in eight**. The original single-cohort experiment had favored the grid in every cell; the new draws demonstrate why that result did not establish universal optimizer superiority. Extra missingness raises all three fitted procedures' Brier error relative to reference in each of the three cohorts. This describes the declared probes, not an estimated population effect or a selection rule for a new panel.

### Panels and fitting cost

The following Jaccard means use all **36 panel pairs among nine chosen outer refits per method/scenario**. The pair identities and separate within-cohort results remain in `stability.json`. Sign-change counts identify anonymous features observed with both positive and negative coefficients among selected outer fits; selection denominators differ by feature.

| Scenario | Grid mean Jaccard | Random mean Jaccard | Grid sign-changing features | Random sign-changing features |
| --- | --- | --- | --- | --- |
| Reference | 0.510402 | 0.633333 | 2 | 2 |
| Extra missingness | 0.324309 | 0.404440 | 3 | 10 |
| Correlated measurement | 0.577652 | 0.436346 | 1 | 11 |
| Reallocated people | 0.438505 | 0.470152 | 4 | 10 |

The missingness probe has lower mean panel overlap than reference for both search methods. A more stable panel need not have lower error, and the fixed all-feature panel's Jaccard of one is true by construction. Ranks, coefficient signs and candidate frequencies are descriptive fitting behavior; they are not evidence for the book's named genes.

Each accepted full execution records **912 grid fits, 912 random fits and 48 all-feature fits**, zero failed fits and no reserved-person predictions. The accepted local replay took **12.004 seconds**, of which **10.486 seconds** were recorded fit/diagnostic time; the independent CI run took **14.314 seconds**. These are environment-specific costs, not a speed comparison. Each run stayed within the 1,872-fit and 2,700-second ceilings.

### Archive verification and rejected first output

The [full CI run](https://github.com/pskeffington/pauls_notes/actions/runs/38936820625) passed smoke, execution and a second bundle audit at the same source commit. Its downloaded artifact **12062065184**, `phase4b-full`, was independently checked against archive SHA-256 `e13edef4d52ea60439f0e5704b7add03f843050645a90777c7e47a88875c766a`, then its full manifest, coordinates, candidate histories, metrics, person losses, input identities and stability summaries were replayed locally. Its probabilities agree with the accepted local replay to a maximum absolute difference of **8.731904088676856e-14**, inside `1e-12`. The CI archive expires **2027-01-14T17:04:09Z**.

The first local execution completed 1,872 fits and initially passed its in-process audit. A subsequent audit rejected the retained `report.json`: it was in a stale `running` state and no longer matched the original manifest. The cause was not established. That bundle is **rejected**, with its retained bytes and mismatch digests preserved. No scores, seeds or modeling settings were changed. A fresh local execution of the same committed source passed both audits, and its prediction file is byte-identical to the rejected first output's prediction file. CI independently supplied the accepted complete archive above.

The downloadable **Pauls_Notes_Phase4B_Evidence_2026-10-16.zip** preserves all three bundles, the original CI ZIP, an explanatory record and a root SHA-256 inventory; its digest is `9e561dc1952b8ea737b1259be4513e1c324d37909a812dd35b515f0190c5a6a4`. It deliberately retains the invalid manifest/report pair inside the rejected sub-bundle. The three recorded full executions cost **5,616 attempted fits in total**, each limited to 1,872; they are audit/replay executions, not nine new scientific cohorts. Subsequent CI replays remain separately identified workflow runs.

G1's implementation, numeric checks, failure retention, complete assessment and scientific-scope review are complete **within the declared synthetic scope**. Learner mastery and clinical validity are not established. G2 remains open: freeze its equal-person paired loss-contrast estimand and whole-person conditional bootstrap protocol before implementing or computing intervals. Full-training-procedure uncertainty needs its own experiment and fitting budget.
