# Phase 4 protocol: robustness and tuning-budget gate

Authored by Paul Skeffington · Compiled with OpenAI

[Learning roadmap](../docs/learning-roadmap.md#phase-4-study-robustness-before-making-search-more-elaborate) · [Current comparison](model-comparison.md) · [Implementation and interpretation](robustness-experiment.md) · [Breast cancer book, Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data)

**Protocol ID:** `paired-assay-robustness-v1`. This is a bounded **synthetic software experiment**, not a medical cohort study, independent external validation or preregistered clinical analysis. The procedure was drafted and locally smoke-tested during implementation on 2026-10-16; this versioned document fixes the settings for the repository execution. The local development runs have already exposed synthetic performance, so this is **not** a blinded confirmatory evaluation.

## Question, units and endpoint

Can the original six-candidate feature-selection search retain usable out-of-fold probabilities and interpretable panel stability when development-person allocation, missingness and correlation are perturbed? Does an equally sized random candidate search justify its extra range? The target remains **specimen category**, coded `0` for comparator and `1` for tumor-labeled specimen; it is not a cancer diagnosis, recurrence outcome or drug-response label.

The fixture has **60 invented people, 120 specimens and 48 anonymous measurements**. Exactly two specimens (one of each target category) belong to each person. Independent partitioning is at **person level**; specimen rows are correlated. The seed-generated values have no link to the book's named genes, real tumor assay data, or patient-level clinical endpoints.

## Frozen comparison and perturbations

| Item | Prespecified setting |
| --- | --- |
| Cohort | 60 paired people, `make_cohort(seed=26101711)` |
| Reference split | `GroupShuffleSplit(test_size=0.25, n_splits=1, random_state=26101712)`; 45 development people and 15 reserved people |
| Reallocation split | Same invented cohort, new `random_state=26101713`; produces a different 45-person development subset |
| Extra missingness | Add independent 15% dropout to *development measurements only* with seed `26101714`; retain original 3%-approximately missingness |
| Correlated measurement | Replace development Feature005 by `0.99 × Feature001 + N(0, 0.05)` with seed `26101714`, preserving the previous Feature005 missing mask; Feature001 missingness may propagate |
| Outer assessment | `GroupKFold(3)` on development people, common folds for grid, random, all-feature and prevalence procedures |
| Inner selection | `GroupKFold(3)` within each outer-training slice; imputation, univariate F-test, standardization and logistic fit *inside* each analysis fold |
| Original grid | Select `k ∈ {5,10,20}` and logistic `C ∈ {0.1,1.0}`; 6 complete candidates |
| Bounded random extension | Draw 6 unique combinations without replacement from `k ∈ {3,5,10,20,30,40}` and `C ∈ {0.03,0.1,0.3,1,3,10}`, `ParameterSampler(random_state=26101715)` |
| Shared comparators | All 48 features with independently fitted median imputation, scaling and fixed logistic `C=1.0`; fold-training prevalence |
| Objective | Mean inner-fold Brier error **minimized**; primary assessment is each procedure's person-disjoint *development* out-of-fold Brier error |
| Fit accounting | Per grid or random arm: `(3 outer + 1 development) × (6 candidates × 3 inner folds + 1 refit) = 76`; all-feature: 4; **156 per scenario, 624 for four scenarios** |
| Compute | `n_jobs=1`, single worker, pinned Python dependencies, limit 624 fit attempts and 900 seconds; pre-fit wall checks cannot interrupt a single in-flight fit |

**Four scenarios** in execution order: `reference`, `extra_missingness`, `correlated_measurement`, `reallocated_people`. The three first share the same people and outer allocation; the fourth alters development membership and therefore changes the assessment people. Each scenario retains its own final model's selected anonymous columns and the feature frequencies from three outer-training fits. No candidate selection or perturbation was tuned against the held-out output.

## Assessment and comparisons

All models produce one outer-held-out probability for each development specimen (90 rows per scenario). Save the shared fold indices, inner membership, six candidate/fold trial scores, failures, selected setting, final panel, elapsed fit time, version identifiers, and output digests. The original grid and random method each receive **the same six candidates and 76 fits**, but their search spaces differ; equal fits are not equal optimization difficulty. The all-feature comparator uses only four fits and is **not** an equal-budget search arm.

For each scenario, report Brier error, ROC-AUC and average precision for all four procedures. The contrast field `comparison_vs_grid_brier` is **other minus original grid** (positive means lower error for grid). Also compute per-person *grid minus random* Brier differences and the Jaccard overlap of selected panels across outer fits; both are descriptive. Exactly two equally weighted specimens per person make the averaged specimen Brier equal to the equal-person averaged Brier **only for this fixture**. No effect-size uncertainty intervals or p-values are supplied: overlapping development samples, correlated specimens and conditional model choice make a naive fold standard deviation invalid.

The reserved 15 people are **not scored** in this experiment. The code may validate that their synthetic ID/pair schema exists, but their measurements and labels do not enter preprocessing, feature selection, tuning, fitting, diagnostics or reported loss. In the missingness and correlation scenarios the change is intentionally applied to development data only; those scenarios are sensitivity probes, **not** transportability analyses of equally perturbed future people.

## Gate conditions and limits

A run passes the **software gate** only if all outer and inner partitions are person-disjoint, every development specimen receives exactly one probability per procedure, outcomes/IDs remain valid, all 6 × 3 inner candidate trials are recorded per search, selected settings use only inner losses, predictions and per-person losses reconcile, the complete fit budget matches 624, no candidate fit fails, the time ceiling is met, and output hashes are checked. Failures of a candidate are recorded as errors at trial level; no silent candidate omission or fallback to assessment data is permitted. A search with only failed candidates stops the run, and a failed gate is not marked complete. Regenerate outputs in an unused directory outside the repository; do not overwrite evidence.

**No performance threshold or preferred winner is a pass requirement.** A less stable panel, higher error, or a random search that does not improve performance is a valid scientific-teaching result. Selection frequency is not biological importance or adjusted significance. A positive software gate **does not** establish recurrence prognosis, biomarker discovery, clinical validity, model calibration in patients, or transportability to another site.

## Next gates that remain separate

A broader Phase 4 investigation would add prespecified repeated independent cohorts, heterogeneous per-person specimen counts, an explicit patient-level uncertainty estimand and an independent development/evaluation plan for any method changes. Native Rust model *training* remains its own numerical-objective/convergence experiment, distinct from the already implemented Rust inference parity check. Phase 5 requires a new time/event/censoring contract before a survival model can be fit.
