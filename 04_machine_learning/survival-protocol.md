# G4 frozen protocol — synthetic oncology time-to-event learning case

Authored by Paul Skeffington · Compiled with OpenAI

[Machine learning](README.md) · [G4 milestone](../docs/roadmap-gates.md#g4-phase-5-survival-learning-case) · [Machine-readable contract](evidence/survival-contract-v1.json) · [G4 data dictionary](survival-data-dictionary.md) · [Cancer research scope](../docs/cancer-research-scope.md) · [Breast cancer book, Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data)

**Protocol ID:** `oncology-synthetic-survival-g4-v1`. **Declaration:** 2026-10-17. **Stage:** frozen *method/endpoint specification*, **not executed or empirically validated**. The first merge commit that includes this document and its contract is the declared freeze. The implementation must record that commit and the SHA-256 hashes of both files **before generating outcome records or fitting a model**. Modifications after reviewing a run's outcomes are exploratory amendments and need a new version and explicitly renewed assessment boundary.

This is **one example** in an [all-cancer methods repository](../docs/cancer-research-scope.md), narrated alongside the breast cancer book. The event, people, ages and biomarker below are wholly invented. No actual recurrence, TCGA patient records, 60 named book genes, treatment observations or clinical risk estimates enter this design. The already completed G1/G2 classification/conditional uncertainty results do **not** transfer to this endpoint.

## 1. Research question and estimand

Can a **fixed Cox proportional hazards baseline** improve person-equal **24-month event-free survival prediction** over a training-only **Kaplan–Meier null baseline** on out-of-fold records from a new fictional oncology cohort?

- **Population:** exactly **240 invented independent people**, each with **one** baseline observation. No repeated specimens or artificial pairing.
- **Time origin:** fictional baseline at month **0**. `time_months` is positive observed follow-up in months (not a clinic date).
- **Event:** first invented *recurrence-like* event, `event=1` if observed; `event=0` if right censored. **Specimen tumor/control classification is not a survival endpoint.**
- **Target:** `S(24 | age_years, marker) = Pr(fictional event time > 24 months | baseline predictors)`, predicted under the teaching generator. This is event-free **survival probability**, not the Cox linear risk score, hazard ratio or probability of cancer diagnosis.
- **Primary comparison:** `IPCW Brier[Cox, month 24] - IPCW Brier[KM null, month 24]` on **180 held-out development people**, each contributing one out-of-fold prediction. Negative favors Cox; no minimum effect or significance threshold is needed to declare the *software* run finished.
- **Clinical boundary:** There is no target population, intervention, clinical label validity, transportability, or approved patient-use case. The result cannot be applied to an individual.

## 2. Frozen synthetic generator, data dictionary and censoring

The [machine contract](evidence/survival-contract-v1.json) specifies exact parameter and seed values; the [field dictionary](survival-data-dictionary.md) specifies schema, joins and invalid cases.

| Generator setting | Frozen rule |
| --- | --- |
| Random engine | Base R `RNGkind("Mersenne-Twister", "Inversion", "Rejection")`; save R version and `survival` package version; generator seed **26102401** |
| ID | `S001` through `S240`, invented only and unique |
| Baseline predictors | `age_years ~ Uniform(30, 75)`; `marker ~ Normal(0,1)`; both fictional, complete and baseline-only |
| Event intensity | Constant per-person hazard `0.022 × exp[0.025 × (age_years - 50) + 0.50 × marker]` per month |
| Latent event time | `-log(U_event)/intensity` with `U_event ~ Uniform(0,1)` |
| Independent censoring | `C ~ Uniform(12,60)` months, independent of predictors and event time; this is a simulation assumption, **not** a property of real cancer follow-up |
| Observed record | `time_months = min(T_event, C)`; `event = 1` if `T_event <= C`, otherwise `0` |
| Schema | Exactly `person_id, age_years, marker, time_months, event` in declared order; no latent true event or censor times in fitting/evaluation input |
| Missingness and events | No missing values, competing events, delayed entry, recurrent events, or time-varying predictors; zero/negative times and event codes outside `{0,1}` are invalid |

**Risk-set interpretation:** People who are censored before 24 months have **unknown** 24-month event status. They must not be recoded as surviving event-free at the horizon. The censoring estimator and baseline survival are separately fitted **using outer-training records only**.

The generator uses an exponential PH mechanism intentionally so the Cox model has a well-defined teaching target. This design favors correct specification and therefore does **not** test model robustness to non-proportional hazards, informative censoring, competing risk, site shift or heterogeneity.

## 3. Person-level split and protected reserve

Use the exact R random engine named above, reseeding only at each declared phase:

1. From sorted `S001..S240`, `set.seed(26102402); sample.int(240)`. The **first 60** shuffled IDs form the *reserved* set; **180** remain development. Save all IDs and check disjointness. This reserve is **never used** to train, evaluate, select, check horizon support or improve the protocol in this G4 run.
2. Sort the 180 development IDs. `set.seed(26102403); sample.int(180)`. Take consecutive groups of **60** as the three outer test folds, in fold order. Each outer training fold has **120** people. Save literal IDs, record order, and prove every development person is held out exactly once.
3. Refit all preprocessing, Cox/KM and censoring models inside the relevant **outer training fold only**; do not reuse a full-development fit. No tuning, predictor selection, inner folds, label-based balancing or use of any reserved observations is authorized.

There is one row per invented person in this case, unlike paired specimens in G0–G3. For a future multi-specimen, spatial tile, repeated-visit or multicenter cancer cohort, a **different study contract** must specify grouping, time origin and site transfer.

## 4. Locked comparison models

| Procedure | Training/fitting contract | Prediction at month 24 |
| --- | --- | --- |
| Fixed Cox PH | Base R `survival::coxph(Surv(time_months, event) ~ age_years + marker, ties="efron")`; two prespecified predictors; no stepwise search | Absolute person-specific event-free `S(24)` derived through `survival::survfit(fit, newdata=outer_test)` |
| KM null | `survival::survfit(Surv(time_months, event) ~ 1)` on **outer training** | One training-only marginal event-free survival probability `S(24)` for every outer-held-out person |
| Reverse-KM censor support | `survival::survfit(Surv(time_months, 1-event) ~ 1)` on **outer training** | Censoring survival `Ghat(24)` and `Ghat(t-)` for the Brier weights; **not** an outcome predictor |

Check input types, finite features, nonempty unique IDs, exact event coding and fold identities *before* fitting. Record Cox coefficients and `survival::cox.zph` **on training records** with any warnings, without fitting an alternative model or choosing folds based on a p-value. A Cox linear predictor is a **relative log-hazard score**, not a survival probability. Preserve the original run and any failures if the fit fails.

## 5. Frozen primary assessment and failure boundaries

The sole primary time horizon is **τ = 24 months**. For held-out person `i` with observed time `t_i`, event indicator `δ_i`, and predicted event-free `S_i(24)`, define:

```text
IPCW_Brier(24) = (1 / N_test) * SUM_i [
  1(t_i <= 24 and δ_i == 1) * S_i(24)^2 / Ghat(t_i-)
  + 1(t_i > 24) * (1 - S_i(24))^2 / Ghat(24)
]
```

Here `Ghat` is the **outer-training-only reverse KM** estimate of censoring survival. The `t_i-` notation means the **left limit** just before the event. People censored at or before 24 receive *zero observed-status contribution*, not an imputed event-free label. The denominator is **all held-out people**, not the sum of nonzero weights. Pool the 180 person contributions across outer folds and divide by 180; report Cox, KM and paired Cox-minus-KM loss. Do **not** separately average fold means with unequal weights in a future amended design.

For each outer fold, **fail closed** if `Ghat(24) < 0.20`, if any required `Ghat(t-)` is zero/nonfinite, if absolute Cox/KM probabilities are outside `[0,1]`, if a prediction is missing, or if 24 exceeds supported censoring/event follow-up. Do not clip inverse weights, move the horizon or choose a favorable seed. A failed scenario is evidence and remains in the log.

**Feasibility gates (not performance goals):** at least **15** observed events in each outer train, **5** in each outer test, **3** outer test events by 24 months, and **one** held-out prediction per person. Failure stops the prespecified assessment and is not fixed by changing the generator after examining results.

### Secondary, descriptive evidence only

- **Discrimination:** held-out Harrell concordance for Cox linear risk, with `reverse=TRUE` because higher Cox scores mean higher hazard. Record tied/comparable pairs and censoring limitations; this is not IPCW-adjusted C-index.
- **Calibration:** group out-of-fold Cox event-free predictions into **fixed** probability bins `[0,.33), [.33,.66), [.66,1]`. Report bin counts, predicted mean and within-bin 24-month KM observed survival only with **≥15 people and ≥5 observed events**; otherwise label the bin *unavailable* with its denominator. These are descriptive bins, not validated calibration curves, confidence intervals or model selection.
- **Support and diagnostics:** event/censor and at-horizon counts per fold, coefficients, training `cox.zph`, censor `Ghat(24)`, NA/warnings, exact RNG, R/`survival` versions, environment, source/protocol/contract SHA-256 and mutation/failure outcomes.
- **Uncertainty:** no Cox/KM effect confidence intervals, full-procedure bootstrap, external validation or subgroup comparisons are authorized in v1. A prospective follow-up must predeclare dependence and an estimand.

Independent censoring is assumed by construction. The choice to estimate censoring survival on the **training** fold is deliberately predeclared: recent work describes tradeoffs between training- and test-based IPCW estimation. For this learning case we prioritize protected held-out outcomes and a stable training-only censor model, while explicitly limiting population inference.

## 6. Verification before numerical fitting

The [offline protocol validator](../scripts/check_survival_protocol.py) and its deliberate-failure tests are **specification checks only**; they may run now without inventing outcome results. The future executable implementation must be a **separate reviewed PR** and must pass:

- Schema abuse: duplicate/missing person IDs; extra participant keys; NaN, impossible age, missing marker, invalid time, nonbinary events, unexpected source or dataset path.
- Partition abuse: overlap among folds or with the 60 reserved people; attempts to use a reserved person's event/follow-up; a person held out twice; any use of the test records in censoring or Cox fitting.
- Survival correctness: left-limit `G(t-)` vs `G(t)` tests, event at horizon, censoring at/before horizon, support below 0.20, no event, complete censoring, Cox-risk direction and absolute-probability extraction.
- Brier oracle: hand-worked no-censoring toy case reducing to standard binary Brier, manually computed censor-weighted toy case with both observed-event and event-free terms, and an independently computed probability benchmark.
- Provenance/replay: same pinned R environment + seeds + contract produce matching synthetic cohort, splits and metric outputs; adversarial held-out-label mutation must **not** change any training-model coefficients.
- Release: outputs in a **new external directory only**, never in tracked Git or public CI artifacts; explicit **SYNTHETIC — NOT FOR CLINICAL USE** warning. Preserve failed runs.

Do **not** mark G4 complete merely because a generic `research_methods.R` file already fits `coxph`. Its older demonstration does not define this specific generator, allocation, null comparison, censor-weighted 24-month Brier or calibration checks. The G4 gate remains **Planned (frozen protocol, no assessment)** until independently replayed evidence and review.

## 7. Reporting methods and limitations

Source-informed design, **not** evidence of implementation or clinical validity:

- Collins et al. (2024), [TRIPOD+AI statement](https://doi.org/10.1136/bmj-2023-078378): report the actual data, model, internal evaluation and limitations rather than transferring claims from other cohorts.
- Graf et al. (1999), [Assessment and comparison of prognostic classification schemes for survival data](https://pubmed.ncbi.nlm.nih.gov/10474158/): time-dependent prediction assessment under censoring.
- Prince et al. (2025), [On the estimation of inverse-probability-of-censoring weights for the evaluation of survival prediction error](https://doi.org/10.1371/journal.pone.0318349): censor-estimation choices materially affect interpretation.
- [R `survival` Cox survival prediction documentation](https://search.r-project.org/CRAN/refmans/survival/help/survfit.coxph.html): predictions require a survival curve, not merely a linear risk score.

**Mandatory release text:** SYNTHETIC RESEARCH AND EDUCATIONAL USE ONLY — NOT FOR CLINICAL USE. This case cannot support cancer diagnosis, screening, treatment selection, individual prognosis, or inference about actual breast cancer patients. TCGA-BRCA is a separately proposed source with [unresolved admission gate D1](../docs/roadmap-gates.md#d0-and-d1-privacy-and-real-data-admission-remain-open); any other cancer data require their own source-specific review.
