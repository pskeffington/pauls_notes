# Scientific statistical reporting standards: methods, results, tables, and figures

**Scope.** Applied biomedical and breast-cancer research, including coursework, reproducible reports, and manuscript drafts. This is the central *reporting* companion to the [method-selection matrix](BIOMEDICAL_DECISION_MATRIX_V2.md), not a replacement for statistical design or the [R Markdown rendering acceptance guide](../../02_biomedical_coding/RMARKDOWN_PDF_PRESENTATION_ACCEPTANCE.md). Published standards describe required transparency; local rules below specify consistent presentation. **No example values are actual patient findings.** Rosner, *Fundamentals of Biostatistics*, provides the conceptual statistics sequence; verify edition-specific chapter/page references before citing pages.

## 1 | What every quantitative result must communicate

**Reporting unit:** **question → design → denominator → descriptive evidence → effect/estimate → uncertainty → test/model evidence → interpretation**.

1. **Research question and estimand:** Identify population, endpoint, observation period, contrast, analysis unit (patients, tumors, specimens, visits), reference category and whether the result is descriptive, association, causal effect or prediction performance.
2. **Analysis population:** State eligible, included and analyzed N (overall and by group), exclusions, missing values, repeated observations and follow-up/exposure. Never replace missing outcomes with nonresponses without the prespecified rule.
3. **Descriptive evidence:** For binary outcomes use n/N (%); continuous outcomes generally mean (SD) or median [Q1, Q3] with measurement units; counts require the exposure denominator when interpreted as rates.
4. **Estimate and precision:** Report a directly interpretable estimate/contrast with a 95% confidence interval where meaningful; identify interval construction, adjusted versus unadjusted analysis, and multiplicity adjustment.
5. **Test or model:** Give exact test/model name, test statistic and degrees of freedom where defined, p-value when testing, sidedness, assumptions/diagnostics and correction/estimator if these affect results. Descriptive analysis need not include a hypothesis test.
6. **Scientific reading:** Summarize direction, magnitude and precision. Avoid unsupported equivalence/causality language and repetitive generic limitations.
7. **Reproducibility:** Document preprocessing, missing-data method, statistical software/packages/versions, model specification, prespecified versus exploratory analyses and any sensitivity analysis.

**Presentation defaults:** two-sided tests unless predeclared otherwise; p = .042 (or p < .001), never p = .000 or “NS”; report effect and CI before p; use consistent rounding appropriate to precision. State sample sizes and units in table captions/footnotes. Distinguish SD (variability of observations), SE (precision of estimator), CI (uncertainty), and prediction interval (future observation). An alpha cutoff never substitutes for a clinical importance threshold. For coursework, use **R quantile type 2** for quartiles/IQR and matching custom boxplot hinges and whiskers; specify the convention in Methods. Do not silently change standard boxplots to another algorithm.

### Minimal prose structure for every method

**Methods:** “Among [population, design and N], [outcome] was compared between [groups/reference] using [method, sidedness and assumptions]. We estimated [estimand] with [95% CI method]; [handling of missingness/multiplicity] was prespecified.”

**Results:** “[Group-specific n, descriptive statistic and units]. The [contrast/effect] was [estimate] (95% CI [limits]); [statistic(df) = value, p = value when relevant]. [One sentence describing direction, magnitude and clinical context].”

**Figure caption:** “Figure X. [Question and data/units]. [What marks, lines, error bars, distributions and colors encode]. [Analyzed N, aggregation and reference]. [Any transformation or adjustment].”

## 2 | Method-specific publication-ready reporting cards

Each row identifies a *minimum results payload*, not a claim that each test requires the same diagnostic or format. The linked worked atlas supplies examples: [breast cancer test atlas](BREAST_CANCER_WORKED_TEST_ATLAS.md).

| Method / design | Minimum quantitative results | Test/model evidence and caveats |
| --- | --- | --- |
| One-group continuous summary | N, missing, units, mean (SD) and/or median [Q1, Q3], range if pertinent | No p-value merely for describing a sample; explain skew/transformation |
| Categorical frequency / prevalence | n/N (%), missing denominator, definition, 95% binomial CI if estimating prevalence | State sampling design and denominator; exact/Wilson interval method |
| One-sample t test | N, mean (SD), reference value, mean difference and 95% CI | t(df), p, normality of observations or sampling justification |
| Paired t test | number of complete pairs, baseline/follow-up mean (SD), **within-person difference** mean (SD), CI | t(df), p; diagnostics for paired differences, not separate arms |
| Welch independent t test | N, mean (SD) each arm; arm A − arm B mean difference and CI | Welch t(noninteger df), p; independence and influential observations |
| Student pooled t test | same as Welch plus pooled variance assumption justification | t(df), p; clarify that equal variance was assumed |
| One-way ANOVA | N and mean (SD) for **each** group, omnibus effect size (e.g., η²) and CI when supported | F(df1, df2), p, variance/residual diagnostics; omnibus does not identify pairs |
| Welch ANOVA | same groups and estimates; report robustly estimated contrasts | Welch F(df1, df2), p; use variance-appropriate post hoc (e.g., Games–Howell), adjusted p/CI |
| Repeated-measures ANOVA | participant N, observations/time points, group/time descriptives, within-person contrasts | F, dfs and any sphericity correction; use mixed models if incomplete/irregular repeated measures warrant them |
| Post hoc contrasts | pair names, mean difference, adjusted 95% CI where available | adjustment family and method, adjusted p; label simultaneous versus individual CI |
| Wilcoxon rank-sum / Mann–Whitney | N, medians [Q1, Q3] and distributions by arm | W/U, p, ties/exactness; do **not** label the rank-based shift automatically a difference in medians |
| Wilcoxon signed-rank | complete paired N, distribution of differences, paired shift if model supports it | V/W, p, zero/tie handling; symmetry assumption for shift interpretation |
| Kruskal–Wallis | N and median [Q1,Q3] per group; distribution description | H (or chi-square statistic), df, p; pairwise comparisons need adjusted inference |
| Chi-squared contingency | full observed table, row or column %, correct denominators, optional strength e.g. Cramér V | Pearson χ²(df), p, expected-count diagnostics, continuity correction policy |
| Fisher exact 2×2 | all four cells, row risk/proportion, effect and appropriate CI | Fisher p, two-sided alternative and exact conditional OR if returned; clarify OR convention |
| McNemar matched binary | number of pairs and 2×2 paired transition table, particularly discordant b/c | McNemar χ²(1) or exact binomial result, p; never use independent Pearson χ² on pairs |
| Binomial one-sample test | events/n, observed % and 95% CI, null proportion | exact-binomial p, sidedness, count model assumption |
| Risk ratio / risk difference | a,b,c,d, risk in each group, RD in percentage points, RR and 95% CI | comparison/reference orientation, interval method; case-control sampling cannot directly yield population risks |
| Odds ratio | a,b,c,d or adjusted model, OR with 95% CI, baseline risk when estimable | OR not RR; specify reference group and adjustment; sparse data method |
| Correlation | paired N, x/y units and scatterplot, coefficient and 95% CI | Pearson r or Spearman rho, p if tested, structure/outlier/nonlinearity review |
| Linear regression | analyzed N, outcome/predictor units, slope per stated unit and 95% CI; intercept if useful | β(SE), t(df), p, R²/adjusted R², residual-vs-fit and Q–Q diagnostics; covariates |
| Logistic regression | N, event count, unadjusted/adjusted OR per predictor with 95% CI | reference, continuous-unit scaling, covariates, separation, fit and convergence; not an RR |
| Poisson count/rate | event counts, total person-time/exposure, rates by arm, IRR with CI | log link and offset, dispersion diagnostics, model assumptions, likelihood/Wald details |
| Negative-binomial count | event counts and exposure; IRR with CI | parameterization, overdispersion reason, model and fit |
| Mixed effects / GEE | number of persons/clusters/visits; arm/time effects and CI | fixed and random terms or working correlation, SE method, dependence structure |
| Survival Kaplan–Meier | N, events, censoring, time origin, median survival if estimable, survival probabilities with CI at named times | number-at-risk table, censoring policy, log-rank χ²(df), p if comparing |
| Cox proportional hazards | N, events, HR and 95% CI, adjustment set, follow-up | time origin, proportional-hazards diagnostics, ties method; HR is not risk ratio |
| Competing risks | each event type, numbers/events, cumulative incidence at fixed times with CI | cause-specific HR or subdistribution HR with clearly named estimand |
| Diagnostic threshold | full TP, FP, FN, TN table, sensitivity, specificity, PPV, NPV with CIs | event class, threshold chosen without using evaluation outcomes; test population/prevalence |
| ROC/AUC | evaluated patient N, event N, AUC with 95% CI and method | score direction, validation partition, patient-level independence, full ROC; single confusion matrix is insufficient |
| Prediction model | N/events per partition; discrimination **and calibration** estimates/plots, CI, validation strategy | feature handling, tuning, leakage prevention, performance in key subgroups, model availability; TRIPOD+AI |
| Differential expression/omics | biological replicate N, contrasts, log2 fold change and uncertainty, raw p and FDR-adjusted q | normalization, batch effects, multiplicity universe and threshold |
| Survey-weighted analysis | unweighted N, weighted estimate/percentage, design SE and CI | strata/PSU/weights, variance method and design df |
| Bayesian estimation | priors and likelihood, posterior estimate, credible interval, relevant posterior probability | convergence diagnostics, chains, sensitivity to priors; CI is **not** a credible interval |

**Do not report a test from an assumption diagnostic as the sole justification of method choice.** Show relevant residual/variance/shape plots, independence/design facts and material sensitivity evidence. Not every row warrants every statistic: if effect-size CIs are unavailable or a method only supplies a valid omnibus test, state the limitation and favor meaningful model contrasts over inventing uncertainty.

## 3 | Report-type formats and where each result belongs

| Report type | Required structure | Governing reporting framework |
| --- | --- | --- |
| Coursework R Markdown | Question/hypothesis; study design; variable dictionary; preparation; descriptive table; diagnostics; test and CI; 1–2 sentence interpretation; references; reproducible code | Rosner methods + explicit rubric + this house guide; no assumption that a journal checklist supersedes coursework rubric |
| Randomized trial | Structured abstract; registration/protocol; participant flow; assignment; arm baseline table; estimands/outcomes; effect and CI; harms; missingness; analyses | **CONSORT 2025**, plus relevant extension |
| Observational cohort, case-control, cross-sectional | Eligibility and flow; design/sampling; confounders; missingness; descriptive estimates; adjusted effects/CI; sensitivity | **STROBE**; RECORD when routinely collected data |
| Diagnostic accuracy | Intended use, target condition, reference standard, test threshold, participant flow, indeterminates, TP/FP/FN/TN; accuracy with CI | **STARD 2015** and relevant extensions |
| Prognostic tumor marker study | Marker/specimen/assay information, cutoff rules, patients and events, missingness, time origin, adjusted effect/CIs and validation | **REMARK**; TRIPOD+AI when building a patient-level prediction model |
| Predictive model / AI | Intended population and outcome horizon, development/evaluation partitions, feature and missing-data processing, model specification, discrimination, calibration, clinical utility where evaluated, subgroup performance, transparency | **TRIPOD+AI 2024** (supersedes TRIPOD 2015) |
| Systematic review/meta-analysis | Protocol/search, study selection and flow, bias assessment, pooled estimate with CI, heterogeneity and synthesis limitations | **PRISMA 2020** and relevant extensions |
| Manuscript Results section | Population/flow → Table 1 descriptives → primary effect/CIs → adjusted/secondary analysis → diagnostics or sensitivity | Use relevant study-design checklist plus **SAMPL** and journal author guidance |
| Statistical analysis plan | Objective, estimand, planned contrasts, sample size/power, missingness, assumptions/diagnostics, multiplicity, sensitivity | Protocol and relevant trial/study-type standards; no results invented in advance |
| Reproducible technical supplement | Data provenance/dictionary, exclusions, complete algorithms, package versions, code, supplementary figures/tables, seeds | Reproducibility and data-governance requirements; separate execution and visual-verification statuses |

## 4 | Table and figure specifications

- **Table 1 – population:** group-specific N, categorical n (%) and continuous mean (SD) or median [Q1,Q3], missing n, clinical units. Baseline p-values are not automatically useful in randomized trials. Provide patient N separately from specimen N.
- **Table 2 – main estimates:** endpoint, arm counts/statistics, contrast/reference, estimate with 95% CI, test/statistic and p where applicable; make adjustment and CI method explicit.
- **Table 3 – model:** covariate, unit/reference level, coefficient or correctly transformed OR/HR/IRR and CI, optional p, number of events/observations, adjustment set and footnotes.
- **Table 4 – multiplicity/sensitivity:** prespecified contrasts, raw versus adjusted p, CI family, alternative models and changes in magnitude. No unexplained selective reporting.
- **Figure distributions:** histogram displays frequency/density; boxplots use type-2 quartiles in coursework; jitter/scatter distinguishes patients from specimens. Do not call SD bars confidence intervals.
- **Figure diagnostic:** label residual-versus-fitted, Q–Q and variance/outlier plots. These are evidence used in choosing/reporting a model, not results proving an assumption.
- **Figure inference:** confidence bands encode estimator uncertainty; multiplicity-adjusted intervals must be labeled. A forest plot shows estimates, reference and interval scale.
- **Figure ROC:** x = 1 − specificity; y = sensitivity; event score direction, AUC with CI and development/evaluation partition noted. If predicting risk, also show calibration.
- **Figure survival:** time units, time zero, censor marks, at-risk counts and interval/line meaning; do not confuse hazard ratios with cumulative risk.

### Worked example: two-arm mean comparison (synthetic, numbers only illustrative)

**Methods:** “Mean change in a tumor-response score was compared between independent treatment groups using a two-sided Welch t test. The effect was treatment A minus treatment B, with a 95% Welch confidence interval.”

**Results template:** “Treatment A (n = [n], mean [x], SD [s]) and treatment B (n = [n], mean [x], SD [s]) differed by [Δ] score units (95% CI [L, U]; Welch t([df]) = [t], p = [p]).”

### Worked example: categorical response and ROC

Use the [contingency/risk/ROC chapter](CATEGORICAL_RISK_ROC_REPORTING.md) for a coherent synthetic four-cell demonstration, OR/RR/RD interval construction, threshold confusion matrix and a separate ROC example. Do not extract AUC from one threshold.

## 4A | Executable reporting from the existing breast-cancer atlas

The [synthetic R laboratory](../examples/breast_cancer_test_atlas.R) now exposes `breast_cancer_reporting_examples()`. It reuses the **same computed analysis objects** to produce a compact results table, four narrative paragraphs and denominators. This avoids copying values manually between calculations, tables and prose.

```r
# ================================================================
# 01 | LOAD THE SYNTHETIC ANALYSIS
# ================================================================
source("03_learning/examples/breast_cancer_test_atlas.R")
analysis <- breast_cancer_test_atlas()

# ================================================================
# 02 | GENERATE THE RESULTS TABLE AND NARRATIVE
# ================================================================
reporting <- breast_cancer_reporting_examples(analysis)
knitr::kable(reporting$table, digits = 3,
             caption = "Synthetic statistical results")
cat(paste(reporting$narrative, collapse = "\n\n"))
reporting$denominator
reporting$methods
```

**Verified design intent, not runtime acceptance:** The function computes a Welch A−B mean difference with Welch CI and degrees of freedom, a within-person after−before paired difference, a two-by-two Pearson chi-square comparison with risk difference/RR/OR and approximate log-Wald intervals, and a Poisson count-model B-versus-A incidence rate ratio with its person-year offset. It explicitly labels all observations synthetic. The methods differ; the uniform reporting sequence does **not** mean that a Pearson omnibus statistic receives a fabricated confidence interval or that a ratio estimate receives a p-value from an unrelated test.

Before using in coursework or a manuscript, execute the code in R, reconcile numbers with the source objects, and review output. The log-Wald risk/odds intervals are teaching examples for nonzero independent cells, not a substitute for sparse-count methods. The Poisson model requires a dispersion/model-fit review before inferential use. All estimates remain unadjusted except the explicitly modeled count contrast. The R example intentionally produces no ROC AUC, survival estimate or individual patient conclusions.

## 5 | Review gates before calling a report scientifically ready

1. **Study identity:** source and design, authorization, eligible/included/analyzed N, patients versus repeated specimens, prespecification.
2. **Arithmetic:** denominators, factor reference, missing observations, direction of subtraction, confidence bounds and any reexpressed percentage.
3. **Method:** justified test/estimator and its assumptions, correction, adjusted covariates, multiple comparison policy and CI family.
4. **Evidence alignment:** same estimates in R objects, tables, figures, abstract, narrative and manuscript; descriptive claims not conflated with prediction performance.
5. **Reporting:** exact output label, units, precision, p-value and effect reporting, clear figure glyphs and no unsupported numerical values.
6. **Verification:** separately label source review, code execution, successful knitting and visual page inspection; never promote one stage to another.

## 6 | Literature and standard updates (reviewed November 2026)

**Statistics reporting foundations**
- Lang TA, Altman DG. *SAMPL Guidelines: Statistical Analyses and Methods in the Published Literature.* https://www.equator-network.org/wp-content/uploads/2013/07/SAMPL-Guidelines-6-27-13.pdf — emphasizes reproducible methods, denominators, effect estimates, uncertainty and model-specific reporting.
- Schreiber JB, Amin MEK. Core reporting expectations for quantitative manuscripts using independent and dependent t-tests, one-way ANOVA, OLS regression, and chi-square. *Currents in Pharmacy Teaching & Learning*. 2025;17:102462. https://doi.org/10.1016/j.cptl.2025.102462 — current test-specific reporting checklist and narrative guidance.
- *JAMA* Instructions for Authors: Statistical Methods and Data Presentation. https://jamanetwork.com/journals/jama/pages/instructions-for-authors — estimates and intervals, absolute counts, full methods and covariates.
- *JACC* Statistical Reporting Guidelines for Observational Studies. https://www.jacc.org/author-center/statistical-reporting-guidelines — correct terminology and modeling distinctions.

**Study-design guidelines**
- Hopewell S, et al. CONSORT 2025 statement: updated guideline for randomized trials. *BMJ*. 2025;389:e081123. https://equator-network.org/reporting-guidelines/consort/ — replaces older default CONSORT citation for general randomized-trial reporting.
- von Elm E, et al. STROBE statement. https://www.strobe-statement.org/ — observational design checklist.
- Cohen JF, et al. STARD 2015 diagnostic accuracy. https://www.equator-network.org/reporting-guidelines/stard/ — diagnostic study and patient-flow reporting.
- Collins GS, et al. TRIPOD+AI statement. *BMJ*. 2024;385:e078378. https://doi.org/10.1136/bmj-2023-078378 — current regression/ML prediction-model checklist; supersedes original TRIPOD 2015.
- McShane LM, et al. REMARK: Reporting Recommendations for Tumor Marker Prognostic Studies. https://pmc.ncbi.nlm.nih.gov/articles/PMC3362087/ — tumor tissue, assays, prognostic biomarkers and marker analyses.
- PRISMA 2020 statement. https://www.prisma-statement.org/prisma-2020 — systematic review and meta-analysis.
- Rosner B. *Fundamentals of Biostatistics*. Use the actual assigned edition for specific test-page references; descriptions here are a synthesis, not verbatim textbook excerpts.

- Gallifant J, et al. TRIPOD-LLM reporting guideline. *Nature Medicine*. 2025;31:60–69. https://doi.org/10.1038/s41591-024-03425-5 — LLM-focused extension for relevant biomedical studies; not a replacement for conventional prediction reporting.

**Update rule:** journal-specific instructions and current study-design reporting checklists can impose additional items. Reporting checklists are transparency frameworks, not substitutes for sound test selection or independent validation. Do not describe this synthesis as a newly published consensus standard.
