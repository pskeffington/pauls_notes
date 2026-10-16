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

Implementation and legacy-only tests are ready; the first full assessment follows the committed implementation. Its numerical results, complete-run archive identity and review are recorded here and in the ledger after execution. G1 remains open until those artifacts and all acceptance checks are reviewed.
