# Complete eighth-edition methods methodological alignment — breast cancer biostatistics

**Retrieval key:** `pauls-notes.biostat8.complete-methodology.v1`  
**Source:** *Fundamentals of Biostatistics*, 8th edition (Cengage, 2016), ISBN 9781305268920. Full PDF supplied by the user (962 PDF pages); manuscript is copyrighted and **is not copied into this repository**.  
**Scope boundary:** The eighth-edition table of contents, preface, and opening chapter material were directly inspected across **all 14 chapters**. Focused content checks also cover descriptive quantiles, inference structure, multiple comparisons, bootstrap, permutation tests, correlated outcomes and survival (see [source notes](BIOSTAT_8E_SOURCE_VERIFIED_IMPLEMENTATION.md)). The contract below is an **original, chapter-complete implementation specification**, not an assertion that all 962 pages, numbered exercises and derivations received line-by-line review.

## Source-text teaching approach as a coding standard

The preface (PDF pp. 15–18) describes instruction built from authentic medical-research problems, thorough explanations of the concepts without treating statistics as a recipe book, and computer results where helpful. It distinguishes the introductory foundation (chapters 1–12) from advanced epidemiologic and person-time work (chapters 13–14). It also specifies carrying **full precision during calculations** and rounding only displayed results.

**Required page architecture for Paul's Notes statistical chapters:**

`clinical scenario → protocol & independent unit → probability model → estimand and notation → worked original hand calculation → reproducible R code → diagnostic & counterexample → effect/interval/test result → oncology interpretation → error modes → checks/tests → source record`.

Do not use a p-value or a test name as the entrypoint. Use the design-first selector and require G0–G10 gates.

## Chapter contracts

### R8-CH01: A study begins before a statistical test

**Biomedical methods topic:** clinical observation to study question, design and data validation (printed pp. 1–4). **Oncology:** a breast cancer biomarker measured at multiple hospitals before and after therapy. Define eligible patients, sites, specimen counts and reasons for repeated measurements. Record prospective study protocol, acquisition order, clinician vs laboratory reader, duplicate or discordant measurement, independent unit and missing specimens. Specify which contrast is observational and what causal information is not identified.

**Code practices:** one stable patient ID, a distinct specimen ID and visit/timepoint, deterministic synthetic data, `stopifnot(!anyDuplicated(...))` only for appropriately unique keys, cardinality checks for joins, range/unit validations and counts of screened/eligible/excluded/analyzed. Persist a data dictionary and codebook alongside the *synthetic* fixture.

**Counterexample:** treating two biopsies from each of 40 women as 80 independent women produces invalid standard errors. **Exit evidence:** schema fixture that fails malformed joins, duplicated keys and mistimed measurements.

### R8-CH02: Descriptive statistics are part of the scientific result

**Biomedical methods topic:** mean/median/mode, sample variance and SD, quantile rules, CV, grouped data and self-explanatory figures. **Oncology:** describe age, tumor size in centimeters, ordinal grade, synthetic continuous marker score and HER2-status categories separately. Preserve total N, available n and missing n (and percentages) for **each variable and comparison**. Use mean/SD for the right estimand, median/IQR for skewed distributions, and categorical n/% with explicit denominator.

**Coding delta:** Biomedical methods §2.4 explicitly demonstrates `stats::quantile(x, type=2)`. Paul's Notes `stats_plots.R` uses type 7; **do not silently change existing results**. Route Biomedical methods-specific instruction through `biostat_quantiles(method="biostat8")`; route legacy through `method="pauls_notes"`. State method in every quantitative table caption. Use `sd()` with sample n−1; CV only on positive meaningful ratio scales with nonzero mean. Numeric results remain unrounded until presentation.

**Counterexample:** 1,2,5,9 have type-2 Q1=1.5 and type-7 Q1=1.75. **Exit evidence:** deterministic comparison and independently checked quantiles plus graphics with N, axes, actual units and readable legends.

### R8-CH03: Screening requires conditional probability and a population

**Biomedical methods topic:** conditional probability, Bayes' theorem, screening, ROC, prevalence and incidence. **Oncology:** describe a *hypothetical* breast cancer screening test at a stated population prevalence, test sensitivity/specificity and resulting PPV/NPV. Use correct 2×2 denominators; emphasize a high AUC does not guarantee a high PPV in a low-prevalence setting.

**Gate:** distinguish sensitivity `P(test+|disease+)` and PPV `P(disease+|test+)`. Prevalence is not incidence; test threshold must be declared or selected on training data only. **Counterexample:** transfer an internally estimated PPV to a different population without correcting for prevalence. **Exit:** Bayes formula independently verified against a simulated confusion matrix.

### R8-CH04: Discrete probability is more than naming a distribution

**Biomedical methods topic:** PMF/CDF, expected value, binomial, Poisson and approximation. **Oncology:** count responses among independently assessed eligible patients (binomial) or adverse-event occurrences with observation windows (Poisson).

**Model gate:** fixed n, mutually exclusive success/failure, independence and constant p for binomial; nonnegative integer counts, defined event intensity/exposure and dependence/dispersion checks for Poisson. Distinguish `dbinom(k,n,p)` (exact mass) from `pbinom(k-1,n,p,lower.tail=FALSE)` (k or more). `dpois` vs `ppois` similarly; test tail equality to summation on small n. **Counterexample:** Poisson on continuous log-expression. **Exit:** known-value reference vectors, exact tails and invalid-count rejection.

### R8-CH05: Continuous distributions and approximation are conditional models

**Biomedical methods topic:** normal, standardized normal, linear combinations, approximate binomial and Poisson normality. **Oncology:** an independently simulated assay score with recorded transformation and arbitrary teaching units.

**Gate:** represent `N(mu,sigma^2)` but supply `sd=sigma` in `pnorm()`; indicate how sample size, skew, tails and independence affect approximations. Simulate the CLT with a documented generator and show a counterexample where cluster correlation prevents naive `sd/sqrt(number_of_rows)` from being valid. **Exit:** numerical `pnorm` tests, simulation seed and mathematical approximation range.

### R8-CH06: Estimators, confidence intervals and bootstrap

**Biomedical methods topic:** sampling vs population, randomization, mean/variance estimation, binomial/Poisson intervals and §6.11 bootstrap. **Oncology:** estimate mean marker score, fraction responding and annualized adverse-event rate, using methods appropriate to each scale.

**Gate:** state parameter, estimator, uncertainty source, confidence level, method (t/exact/score/likelihood/bootstrap), sampling unit and coverage assumptions. Bootstrap resamples independent **patients/clusters**, not serial specimen rows when people have multiple measures. Never round intermediate estimates or refit using numbers rounded for print. **Counterexample:** naive bootstrap of 500 cells originating from five patients. **Exit:** hand CI, R CI and repeated seeded bootstrap with checked interval coverage behavior on synthetic simulation.

### R8-CH07: One-sample hypothesis testing and prospective power

**Biomedical methods topic:** one-/two-sided inference, one-sample mean/variance, binomial/Poisson tests, power and sample-size planning. **Oncology:** test whether a simulated response probability differs from a *predeclared* benchmark, without labeling it an actual standard of care.

**Gate:** specify `H0`, `H1`, estimand, alpha, one/two-tail decision, multiplicity and confidence interval compatibility. Plan sample size using meaningful effect and external variability, account for attrition/cluster design. **Counterexample:** choosing `alternative="greater"` after observing the sign; treating nonrejection as equivalence. **Exit:** tail-direction fixture and simulated power vs planning formula.

### R8-CH08: Paired vs independent comparisons, Welch and outliers

**Biomedical methods topic:** paired t, independent pooled and unequal-variance t, outlier treatment, power. **Oncology:** one pair of pre-/post-treatment biomarker measurements per patient vs independent subtype cohorts. The paired estimand is the mean **within-patient difference**, not the difference of two independent marginal means.

**Gate:** enforce unique patient–time key and complete matching; inspect distribution of within-person differences. For independent mean comparison use Welch unless equal variance is adequately justified; record the sign convention and df. Outliers are inspected and subject to sensitivity, not automatically removed. **Counterexample:** join on visit only, duplicating patients. **Exit:** paired/independent numerical fixtures, direction checks and heteroskedastic example.

### R8-CH09: Rank methods and permutation require the right null

**Biomedical methods topic:** sign, signed-rank, rank-sum and §9.6 permutation. **Oncology:** ordinal toxicity severity or continuous biomarker scores with outlying values. Explain sign test among nonzero differences, signed-rank symmetry condition and rank-sum's relative-distribution estimand.

**Gate:** report ties/zeros and exact vs asymptotic handling. Permutations must respect the **exchangeability** justified by the design; never indiscriminately shuffle observational labels with clusters, unequal variances or structured covariates. **Counterexample:** treating a rank-sum result as a mean difference or a median contrast without shape assumptions. **Exit:** enumerated small exact permutation and tie/zero fixtures.

### R8-CH10: Categorical tests depend on matching and the target quantity

**Biomedical methods topic:** two proportions, Fisher exact, matched-pair McNemar, RxC, GOF and kappa. **Oncology:** ER-positive counts by independent groups; paired pre/post receptor classification; agreement between two readers on the same specimen.

**Gate:** explicit 2×2 layout and reference, counts and denominators; choose Fisher/chi-square based on table structure/expected counts. McNemar uses discordant **within-person** pairs. Agreement (kappa) is not association and is affected by marginals. GOF requires prespecified reference probabilities. **Counterexample:** using ordinary chi-square for matched classification changes. **Exit:** independent, matched and sparse-cell examples with hand reference and R cross-check.

### R8-CH11: Regression is an estimand with diagnostics

**Biomedical methods topic:** linear/partial/rank correlation, least squares, inferential intervals, multiple regression and goodness of fit. **Oncology:** synthetic ERBB2 score versus tumor size, age and subtype, with a declared reference group. State coefficient units and adjusted vs unadjusted association.

**Gate:** residual-vs-fitted, Q-Q, functional form, heteroskedasticity, influential observations, cluster structure, collinearity, missing records and interactions. Distinguish rank correlation from slopes and agreement. **Counterexample:** interpreting `r=.6` as a 60% increased cancer risk. **Exit:** synthetic known linear slope recovered within simulation tolerance, bad-model counterexample and plot QA.

### R8-CH12: Multisample inference, multiple comparisons, ICC and mixed models

**Biomedical methods topic:** one- and two-way ANOVA, Kruskal–Wallis, specific contrasts, multiple comparison/FDR, random effects, ICC and §12.10 mixed models. **Oncology:** three independent synthetic cancer subtype groups; separate multireader measurements per tissue specimen.

**Gate:** conventional ANOVA's variance model vs Welch; omnibus hypothesis vs planned contrasts; balanced/unbalanced factorial effects and interactions; BH FDR family and dependence assumptions; cluster-level random effects with interpretable ICC. A small number of clusters affects robust inference. **Counterexample:** run 100 gene comparisons without multiplicity correction and call unadjusted p<.05 discoveries. **Exit:** independent one-/two-way ANOVA and group-contrast tests, fixed vs random examples, FDR and ICC sanity checks.

### R8-CH13: Epidemiology, confounding and longitudinal bias are design problems

**Biomedical methods topic:** study design, risk/odds, attributable risk, standardization, Mantel–Haenszel, logistic variants, meta-analysis, equivalence, crossover, correlated binary outcomes, longitudinal analysis, measurement error and missingness.

**Oncology:** synthetic postoperative cohort with multiple centers, age/stage confounding and repeated patient measurements. First choose target population, prospective/cohort vs case-control sampling, time ordering and comparability. Use strata/standardization or multivariable models only if assumptions permit interpretable associations; never call a conditional OR a risk ratio. An equivalence claim requires prespecified equivalence margins, not a nonsignificant superiority test.

**Gate:** common effect assumptions, effect modification, missingness and selection, repeated-subject dependence, GEE working correlation and robust SE, covariate misclassification, separation, site heterogeneity, appropriate uncertainty for meta-analysis. **Counterexample:** adjust for a mediator or an outcome-defined subtype and claim causality. **Exit:** synthetic confounded risk comparison with stratified/adjusted result and sensitive missingness/cluster diagnostic.

### R8-CH14: Person-time and survival use a defined risk process

**Biomedical methods topic:** person-time rates, stratified and trend tests, sample-size planning, Kaplan–Meier, log-rank, Cox PH and parametric survival. **Oncology:** invented time to recurrence with a defined postoperative time zero, censoring and a separate death-before-recurrence code if needed.

**Gate:** event vs first-event, recurrence vs mortality and competing risk; exposed years; risk-set entry/exit; noninformative censoring for KM; PH diagnostics for Cox; changing rates, delayed entry, immortal time and informative follow-up. Poisson offset log(person-time) must use >0 exposure, and recurrent counts require appropriate independence/correlation assumptions. **Counterexample:** interpret hazard ratio 0.7 as 30% lower cumulative incidence at year five. **Exit:** rate ratio, KM at defined time, log-rank/Cox diagnostics, competing risk caution and hand calculation.

## Controlling source-versus-modern-extension distinctions

The above 14 chapters cover Biomedical methods's **historical foundational method families**, not all current breast-cancer science. Today an actual RNA-seq DE experiment needs verified raw-count assumptions, biological replicates, batch modeling and established differential-expression software. Modern prediction adds nested tuning, subgroup and external validation, calibration, trial-design and clinical governance. Causal inference, complex surveys and competing risks have their own methodological requirements. Label these as `modern_extension` in citations, even when basic ideas share textbook foundations.

## Reconciliation of current repository discrepancies

| Audit ID | Current state | Required permanent action |
| --- | --- | --- |
| R8-A01 | `stats_plots.R` uses type 7 quantiles | Preserve compatibility; cite type and opt into `biostat_quantiles(...,method="biostat8")` for 8e replication |
| R8-A02 | `describe_measurements()` rounds returned numeric summaries | Treat its output as **presentation-only**; always calculate inferential estimates from raw/unrounded inputs or a separately unrounded summary |
| R8-A03 | Some older files contain escaped literal `\n\n` in narrative | Repair Markdown formatting only as a safe scoped edit, not statistical code rewrites |
| R8-A04 | 26-method breast cancer atlas and 27-route selector overlap | Reuse current IDs as authority; do not fork competing selector logic |
| R8-A05 | Some Rmd analyses are synthetic broad demonstrations | Include only methods selected by actual study question in a real cohort |
| R8-A06 | 6e TOC and 8e full textbook coexist | Version paths, source/page fields and edition tags explicitly; no ambiguous Biomedical methods reference |
| R8-A07 | Existing R test and knit status is not established in this session | Run actual R in CI or working machine; do not mark as passing without logs |

## Machine and human completion contract

- Source coverage record: `biostat_8e_complete_chapter_alignment.csv` maps **all 14 eighth-edition chapters** to print/PDF start page, oncology chapter IDs, source scope, and acceptance deliverables. This is *coverage of chapter topics*, not completed end-to-end technical execution.
- Entry route: `AGENTS.md` → `llms.txt` → `oncology/BIOSTAT_BREAST_CANCER_BIOSTATS_ALIGNMENT_ROADMAP.md` → this methodology contract → `03_learning/bio_stats/BIOSTAT_TEST_SELECTION_MATRIX.md` → actual study protocol, Rmd and tests.
- For **every** eventual code-to-book chapter, evidence must include source edition/section/page, original explanation and synthetic case, tested R chunk, numerical reference, missing-data and independence gates, diagnostic plots, complete knit, and an independent statistical/clinical review when clinical interpretability is claimed.
- Code implementation is not a copyright-derived reproduction of the textbook; do not store the uploaded PDF or its tables/flowcharts in the public repository.
- Status labels: `source_opening_checked`, `section_source_checked`, `numeric_replayed`, `r_test_passed`, `knit_reviewed`, `scientifically_reviewed`, `publication_ready`. Never infer higher statuses from earlier ones.

**Current checkpoint:** All 14 chapter topics mapped and each opening inspected, original methods contract authored; targeted sections read; R execution/knit and complete line-level section coverage **not yet proven**. For any future claim of *complete verification*, close those gates with actual evidence. 
