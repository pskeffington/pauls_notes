# Foundational statistical mastery — Notes-to-synthetic-demonstration crosswalk

**Scope:** Foundational statistical competencies. This is a source-level coverage audit and build specification, not evidence of fresh R execution, figure rendering, or proficiency certification. A separate presentation project may draw on these general-purpose methods.

## Required teaching and demonstration sequence
For every outcome follow **concept → sampling unit and assumptions → mathematical model → manual calculation → reproducible R analysis with deterministic synthetic data → numerical/visual diagnostics → example Methods/Results table, figure, and ≤2-sentence visual interpretation → test assertions → slide source link**. A finished explanation alone cannot pass its example or execution gate. Label synthetic outcomes explicitly.

## Coverage audit against current canonical sources

| LO | Existing canonical Notes | Verified by source inspection | Gap to close | Evidence status |
| --- | --- | --- | --- | --- |
| LO1 discrete distributions and probability | `03_learning/bio_stats/BREAST_CANCER_STATISTICS_FOUNDATIONS.md`; `BREAST_CANCER_DISTRIBUTIONS_AND_POWER.md`; `BREAST_CANCER_NUMERICAL_VALIDATION.md`; `../examples/breast_cancer_distribution_lab.R` | Binomial and Poisson distribution examples, parameters, exact versus upper-tail probability, implementation references | Ensure both exact-point and interval calculations appear together with assumptions, hand arithmetic and deterministic executable R checks | SOURCE COVERED / SYNTHETIC REPLAY PENDING |
| LO2 normal vs log-normal and CLT | `BREAST_CANCER_STATISTICS_FOUNDATIONS.md`; `BREAST_CANCER_DISTRIBUTIONS_AND_POWER.md`; `../examples/breast_cancer_distribution_lab.R` | Normal reference, sampling mean/SE, right-skew exponential CLT simulation described | **Explicit normal-vs-log-normal identification with raw/log histogram, raw/log Q–Q, model/scale comparison and interpretation is not present in reviewed key chapters.** Develop an integrated synthetic example with CLT inference and CI | PARTIAL / PRIORITY GAP |
| LO3 independent unmatched categorical and continuous bivariate tests | `BIOSTAT_TEST_SELECTION_MATRIX.md`; `BREAST_CANCER_WORKED_TEST_ATLAS.md`; `CATEGORICAL_RISK_ROC_REPORTING.md` | Chi-square/Fisher, Welch, rank-sum, ordinary/Welch ANOVA and Kruskal-Wallis with sample-unit decision gates | Create a single synthetic vignette documenting test choice, alternatives, numeric expected counts, heteroscedasticity and robust alternatives; distinguish independent from matched units | SOURCE COVERED / SYNTHETIC REPLAY PENDING |
| LO4 one-way ANOVA sources of variation | `BREAST_CANCER_DISTRIBUTIONS_AND_POWER.md`; `BREAST_CANCER_STATISTICS_FOUNDATIONS.md`; `BREAST_CANCER_WORKED_TEST_ATLAS.md` | Synthetic 3-arm result: SSB=24, SSW=24, MSB=12, MSW=4, F(2,6)=3, upper-tail p=0.125 | Add side-by-side decomposition SST=48, df and ANOVA table with **actual residual-vs-fitted and Q–Q graphics**; show choice of Welch vs pooled, avoid instructor-deck errors | SOURCE COVERED / FIGURE REPLAY PENDING |
| LO5 ROC/AUC classification | `CATEGORICAL_RISK_ROC_REPORTING.md`; `GRAPH_METHODS_SYNTHETIC_GALLERY.Rmd`; `SCIENTIFIC_STATISTICAL_REPORTING_STANDARDS.md` | Correct TP/FP/FN/TN definitions, threshold metrics, ROC axes, synthetic curve code and distinction between threshold metrics and AUC | Reproduce full score-level synthetic ROC and AUC, held-out split/threshold rule, numerical AUC assertion, CI method and proper interpretation; never infer AUC from one 2×2 table | SOURCE COVERED / EXECUTION PENDING |
| LO6 tables, figures and scientific prose | `SCIENTIFIC_STATISTICAL_REPORTING_STANDARDS.md`; `GRAPH_METHODS_SYNTHETIC_GALLERY.Rmd`; `06_RESOURCES/QUANTILE_QQ_REPORTING_BEST_PRACTICES.md` | Comprehensive reporting contract, templates, statistical typography, six-figure synthetic gallery, explicit type-2 descriptive quartiles | Apply reporting review to **every** worked LO exhibit; verify rendered plots and legibility, not merely source code | SOURCE COVERED / CROSS-CUTTING QA PENDING |

## Example-specific acceptance requirements
- **LO1:** define X and population/event unit, justify independence and parameters, show P(X=k) and P(a≤X≤b) with `dbinom/pbinom` or `dpois/ppois` and exact checked numbers; interval inclusion explicit.
- **LO2:** compare meaningful transformations rather than assuming a log transform proves log-normality; diagnostic figure on raw and log scales, summary and sampling-mean CLT experiment; display formula SE = sigma/sqrt(n), sample-size dependence and confidence interval distinction.
- **LO3:** comparison has a valid independent sampling unit; categorical cells/expected counts and effect; continuous data show distribution and variance assessment, chosen method with justified alternative, inference with precision and result narrative.
- **LO4:** `SST = SSB + SSW`, corresponding degrees of freedom, `F=MSB/MSW`, upper-tail p-value, effect size (eta squared), residual Q–Q and spread, observed assumptions; no automatic rejection merely because F>1.
- **LO5:** true labels plus variable scores, positive class and direction, selected decision threshold, sensitivity/specificity, ROC/AUC and held-out uncertainty; no test-set threshold selection.
- **LO6:** per-figure caption with synthetic provenance, analysis unit, N, axes/units, visual distinction between distribution and uncertainty; concise Results prose with estimate and precision. Type-2 quartiles for applied exercises descriptive graphics, correct legend/palette, and run/render checks.

## Implementation plan
1. Preserve existing Notes chapters; add concise missing explanations and cross-links in canonical files, not duplicate chapters.
2. Create or extend an **independently executable synthetic R laboratory** for each outcome and a small numeric assertion set. Prefer existing `03_learning/examples/` and `03_learning/tests/` patterns and reusable 06_RESOURCES helpers.
3. Execute R scripts/tests, knit galleries, inspect rendered plots and record exact command, runtime, seed, output and commit. Mark source reviewed, numerically checked, executed and visually inspected separately.
4. Accept each outcome only when its Notes coverage AND synthetic demonstration AND communication slide each pass their separate evidence gates.

## Active pass
**LO1:** inspect existing binomial/Poisson lab and tests; combine point and inclusive range calculations with a results table and interpretive text if absent. Do not move to LO2 before LO1's acceptance gate or a recorded reason to advance.
