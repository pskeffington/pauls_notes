# Phase 4C uncertainty and reliability assessment

Authored by Paul Skeffington · Compiled with OpenAI

[Frozen protocol](uncertainty-protocol.md) · [Contract](evidence/uncertainty-contract-v1.json) · [G1 report](replication-experiment.md) · [Gate ledger](../docs/roadmap-gates.md#g2-phase-4c-uncertainty-and-reliability) · [Breast cancer book, Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data)

This follows the book from **people → specimens → measurements → data preparation → training → validation → prediction → biological interpretation**, asking how paired specimen-category loss varies when the frozen development-person records are resampled. The [protocol and input](uncertainty-protocol.md) were committed at `d440b82b9af696f3717e302b6e276cb10ad39255` before resampling outcomes. G1 point estimates were already known; this is a descriptive follow-up using invented data, not a blinded clinical evaluation.

## Run and inspect

Use the [pinned Python environment](requirements-python.txt), a committed source checkout, and a fresh directory outside the repository:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/tests/test_breast_cancer_uncertainty.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/examples/breast_cancer_uncertainty.py /tmp/assay-uncertainty-fixture
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 04_machine_learning/examples/breast_cancer_uncertainty.py /tmp/assay-uncertainty-full --mode full
python3 04_machine_learning/examples/breast_cancer_uncertainty.py /tmp/assay-uncertainty-full --audit-only
```

The default is a four-person **numeric fixture**, not the G1 assessment. Full mode validates the frozen 1,080-row snapshot and reconstructs the original verified G1 prediction file's hash before resampling. The compact snapshot is committed for offline replay; the large G1 experiment remains separately archived. **No new preprocessing, feature selection, tuning or model fitting occurs.**

Thirteen regression tests use exact two-person enumeration, known Brier losses, constant/zero contrasts, deterministic shared draws and an independent SciPy paired-percentile reference. They also challenge malformed pairs, duplicate identities, conflicting folds, unknown/missing cells, invalid probabilities, invalid draw coordinates, output protection, timeout/exception artifacts and semantic corruption after rehashing.

The [CI workflow](../.github/workflows/assay-uncertainty-validation.yml) runs fixtures plus the entire inexpensive frozen-prediction calculation on PRs and pushes. It audits the completed output again in a second process and archives complete or failed artifacts with 90-day retention.

| Artifact | Audit purpose |
| --- | --- |
| `report.json` | All 36 point contrasts/ranges, denominators, seeds, person loss means, source/compute metadata and reliability description |
| `resampling.npz` | Per-cell person IDs, four person losses, three paired contrasts, every draw index and every replicate mean; read with `allow_pickle=False` |
| `input.json`, `protocol.md`, `contract.json` | Byte-identical frozen input and assessment declarations |
| `execution-start.json`, `environment.json` | Invocation, freeze/source revisions, timing and numerical environment |
| `sha256.json` | Complete output inventory and digests; no silent acceptance of changed files |

An execution exception preserves available completed cells/arrays and a `software_fail` report; input/source preflight rejection happens before resampling. Unique temporary file names, flushed writes and one final report publication help keep the report and manifest auditable. A failed or partial output cannot close G2.

## Meaning of a range

For each person, average the squared probability errors of their two specimens. Subtract that person's grid loss from each other procedure's loss, then average people. Negative **other minus grid** favors the other method. Sample people with replacement, carrying both specimens and all methods together; do not independently sample specimens or method arms. Each cell uses 45 people and 10,000 draws; 12 cells yield 36 pointwise 95% percentile ranges and zero training fits.

These are **conditional empirical-person bootstrap ranges**. They hold the observed predictions, feature panels and fitted procedures fixed. Shared outer training sets can induce dependence between losses from different people; the calculation does not capture that dependence or the variability of rerunning the entire pipeline. Its nominal central fraction is not a demonstrated 95% coverage guarantee for an unknown clinical/population target. The ranges are not simultaneous, hypothesis tests, probabilities that an optimizer is best, or authority to redesign a panel and reuse the assessment.

The [protocol's primary references](uncertainty-protocol.md#primary-method-references) document paired index sampling, linear quantiles and the limitations of ordinary cross-validation uncertainty. SciPy is an arithmetic cross-check here, not a validation of clinical coverage. A collapsed range on a constant fixture is explicitly flagged and does not prove certainty.

## Recorded results

Recorded execution used committed source `da9ecc5d8263466a3c803e31275b516899fa58b3`, after freeze `d440b82b9af696f3717e302b6e276cb10ad39255`. [PR #4](https://github.com/pskeffington/pauls_notes/pull/4) delivers the calculation and review. The [compact verification record](evidence/uncertainty-validation-2026-10-16.json) contains all **36 ranges**, exact denominators, per-cell seeds, version/source identities, reliability summaries, output hashes and replay evidence. Thirteen uncertainty tests and 17 documentation/evidence tests passed: **30 local tests**. Navigation preserves 85 Markdown pages, 12 book chapters and 60 gene profiles.

### Random minus grid: every declared cell

Each row has **45 people and 90 specimens**. Values are rounded to six decimals. The limits are the declared 2.5th and 97.5th percentiles of 10,000 paired person-resampled mean differences, conditional on the saved predictions.

| Cohort | Scenario | Point contrast | Conditional lower | Conditional upper |
| --- | --- | --- | --- | --- |
| A | Reference | -0.019573 | -0.046128 | +0.005716 |
| A | Extra missingness | +0.008034 | -0.016546 | +0.031286 |
| A | Correlated measurement | -0.033726 | -0.065420 | -0.005532 |
| A | Reallocated people | +0.011134 | -0.005826 | +0.029113 |
| B | Reference | -0.002223 | -0.017857 | +0.013180 |
| B | Extra missingness | +0.012270 | -0.006338 | +0.030404 |
| B | Correlated measurement | +0.015611 | +0.003646 | +0.028461 |
| B | Reallocated people | -0.010773 | -0.033513 | +0.010426 |
| C | Reference | +0.021717 | +0.004258 | +0.040879 |
| C | Extra missingness | +0.028144 | -0.004648 | +0.060090 |
| C | Correlated measurement | +0.022902 | +0.006706 | +0.039507 |
| C | Reallocated people | +0.014090 | -0.003884 | +0.033592 |

**Eight of twelve** random-versus-grid ranges include zero; one is entirely below zero and three entirely above. Eleven of twelve all-feature-versus-grid ranges include zero; one is entirely above. All twelve prevalence-versus-grid ranges lie above zero. These counts describe this conditional resampling output; they are neither tests of equivalence nor adjusted discoveries or evidence of universal optimizer superiority. The point estimates retain the G1 result: random search is lower in four cells and higher in eight.

The accepted local assessment completed **120,000 person-index resamples and 360,000 contrast replicate means**, with **zero new model fits**, in **2.544 seconds** against a 300-second budget. The original fitted models and panels remain fixed for every draw.

### Reliability: changes in people, measurements and choices

Missingness and correlation probes retain all 45 reference development people. Extra missingness raises each fitted procedure's mean loss in all three cohorts, while correlation changes do not move every method in the same direction. These are the declared probes' observed outcomes, with the same interpretation limits as G1.

Reallocation changes the eligible development people. The following descriptive comparisons use only people present in both scenarios; all four methods' changes remain in the machine-readable record.

| Cohort | Common people | Reference only | Reallocation only | Common-person grid loss change | Common-person random loss change |
| --- | --- | --- | --- | --- | --- |
| A | 32 | 13 | 13 | +0.011729 | +0.031419 |
| B | 34 | 11 | 11 | +0.018833 | +0.020027 |
| C | 34 | 11 | 11 | +0.007544 | -0.009268 |

For cohort C, random search's overall reallocation loss rises by approximately **0.008262**, while its mean change among the 34 common people is **-0.009268**. Changes in membership and in the fitted models/folds can therefore lead to different descriptive comparisons. Neither calculation isolates a causal allocation effect.

Candidate choice also changes under the probes: G1 selected grid `C=1, k=5` in six of nine reference outer refits and four of nine missingness outer refits. The [G1 stability report](replication-experiment.md#panels-and-fitting-cost) retains panel overlap, rank summaries and sign changes, with their overlapping-fit denominators. Those records show procedure instability; this follow-up does not separate the effects of feature correlation, missingness, training people and candidate choice. **Fitting variability at fixed inputs remains unidentified**, because no models were refitted. A full-procedure or variance-component investigation requires another prespecified experiment.

### Independent replay and acceptance

The [CI replay](https://github.com/pskeffington/pauls_notes/actions/runs/38939809441) passed numeric tests, all 36 calculations and a second-process audit at the same source revision. Artifact **12062851000**, `phase4c-uncertainty`, was downloaded and checked against SHA-256 `d89db0fe2cdd282dd56dee11273785febf5b00480461452da13e54517a40d1a5`. Its complete bundle was then audited locally: **every person/loss/draw/replicate-mean array and every endpoint and reliability summary exactly matches** the local assessment. CI runtime was **1.301 seconds**. The CI archive expires **2027-01-14T17:27:21Z**.

The saved **Pauls_Notes_Phase4C_Evidence_2026-10-16.zip** preserves local/verified-CI bundles, the original CI ZIP, and a root checksum inventory. Its SHA-256 is `5e195aeda902cdc575b90b3cd54b2c519e74807c56b35c7af3c19219933e6588`. Substantial draw arrays remain outside Git. The frozen compact prediction snapshot enables future replay without needing the expiring G1 archive.

G2's estimand, paired dependence boundary, reference fixtures, hostile-input tests, complete resampling record, independent replay and scientific-scope review pass. **G1/G2 close the defined Phase 4 synthetic scientific-software milestone.** This does not establish learner mastery, full-procedure uncertainty or clinical validity. G3 native Rust fitting still needs its own objective/numerical contract; G4 may now begin its separate breast cancer survival endpoint protocol without waiting for G3.
