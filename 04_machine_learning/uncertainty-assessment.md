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

The implementation and numeric fixtures precede the recorded full assessment. Results, verified replay identity, limitations and the G2 completion review will be added after executing committed sources against the unchanged frozen input.
