# Biomedical statistics: which test, when, and why?

**Paul's Notes | Independent teaching guide | Reviewed 2026-10-22**  
**Scope:** Biomedical, public-health and cancer research of any cancer type. The breast-cancer specimen example is illustrative, not an exclusive scope.  
[Back to learning](README.md) · [Evidence review and source register](../06_RESOURCES/Literature/BIOSTATISTICS_R_LITERATURE_2021_2026.md) · [R tools](../06_RESOURCES/R/README.md) · [Study protocol](../templates/study-protocol.md) · [Privacy and admission](../docs/research-workflow.md)

> **Start with the scientific question and study design, not a p-value or a normality test.** This guide supports educational method selection. It does not replace a prespecified statistical analysis plan, independent statistical review, or a dataset-specific privacy/access decision. All example observations below are invented; nothing here authorizes clinical use or participant-data publication.

## 1. Six questions to ask before choosing a method

1. **What is the aim?** Describe a population; compare groups; estimate an adjusted association; test an intervention; predict a future outcome; or describe survival? Distinguish a causal effect from a predictive association.
2. **What is the outcome?** Continuous measurement (including units), binary state, nominal category, ordered category, nonnegative count with exposure, survival time with censoring, or high-dimensional features?
3. **What is an independent experimental/observational unit?** Person, patient, donor, household, laboratory animal, clinical site, sample or cell? Cells and repeated samples from one donor are usually *not* independent donors.
4. **How are observations related?** Independent groups; matched cases; paired tumor/normal specimens; repeated visits; nested hospitals/sites; survey clusters, weights and strata?
5. **What quantity are we estimating?** Mean difference, location shift, relative/risk difference, odds/risk ratio, incidence-rate ratio, hazard ratio, correlation, discrimination/calibration or time-specific risk?
6. **What must be defended?** Missingness and exclusions; confounding; multiplicity; shape and variance assumptions; expected cell counts; time origin, events and censoring; effect-size precision; protocol and software versions.

A test name without answers to these questions is **not** a complete method decision.

## 2. Main decision flowchart

The chart shows a **starting route**, not an automatic endorsement. Follow it with the independence, assumption and effect-size gates below.

```mermaid
flowchart TD
    A["Define question, target effect and unit of observation"] --> B{"Primary analytical aim?"}
    B -->|Describe| D["Counts, denominators, distributions, uncertainty<br/>No hypothesis test automatically required"]
    B -->|Predict| P["Define prediction horizon and target<br/>Grouped external or held-out validation;<br/>discrimination AND calibration"]
    B -->|Compare or associate| C{"What is the outcome?"}
    C -->|Continuous| X{"Dependent observations?"}
    X -->|Independent: 2 groups| X2["Welch two-sample t test<br/>or suitable rank/robust method"]
    X -->|Paired: 2 conditions| XP["Paired t test on differences<br/>or signed-rank/sign method"]
    X -->|3+ groups| X3["ANOVA or Welch ANOVA;<br/>mixed model if repeated;<br/>Kruskal-Wallis for rank-oriented aim"]
    X -->|Repeated or clustered| XM["Linear mixed-effects model or GEE;<br/>survey design methods if sampled clusters"]
    C -->|Binary or nominal| Y{"Paired or clustered?"}
    Y -->|Independent| YI["Chi-square or Fisher for unadjusted tables;<br/>logistic or multinomial regression for adjustment"]
    Y -->|Paired| YP["McNemar for paired binary;<br/>matched/conditional or clustered models as needed"]
    C -->|Ordered categories| O["Ordinal model or justified rank method;<br/>check proportional-odds assumption"]
    C -->|Counts or rates| R["Poisson with exposure offset;<br/>check dispersion; consider negative binomial"]
    C -->|Time to event| S["KM and log-rank for unadjusted survival;<br/>Cox/AFT or competing-risk methods as appropriate"]
    C -->|Many molecular features| H["Assay-aware model: DESeq2 / edgeR / limma<br/>design matrix, contrasts and multiple testing"]
    D --> Z["Report sample sizes, uncertainty and data provenance"]
    P --> Z
    X2 --> Z
    XP --> Z
    X3 --> Z
    XM --> Z
    YI --> Z
    YP --> Z
    O --> Z
    R --> Z
    S --> Z
    H --> Z
    Z --> Q["Review dependence, assumptions, missingness,<br/>confounding, multiplicity and model diagnostics"]
```

**Important overrides:** If treatment groups differ in confounders or the estimand is adjusted, use a design-appropriate regression model rather than treating a marginal two-group test as a causal estimate. If data are paired, repeated, clustered or sampled with unequal probabilities, do not assume independent rows. For high-dimensional assays, a per-feature ordinary t-test is not a default substitute for validated assay-specific modeling.

## 3. Quick selection table: common biomedical questions

| Question / outcome | Data structure | Starting method in R | What to report / watch |
| --- | --- | --- | --- |
| Mean biomarker, 2 groups | Independent people, continuous | `stats::t.test(y ~ group, data = d)` (Welch default) | Mean difference, 95% CI; inspect residual/outlier structure; do not assume equal variances |
| Change in biomarker, 2 visits | Same people/specimens paired | `stats::t.test(before, after, paired = TRUE)` | Pair count and **difference** distribution, mean change and CI; preserve IDs |
| Skewed continuous outcome, 2 groups | Independent; rank/distribution target | `stats::wilcox.test(y ~ group, data = d)` | Rank/distribution interpretation; not automatically a median test |
| Skewed paired outcome | Paired; suitable difference distribution | `stats::wilcox.test(before, after, paired = TRUE)` | Signed-rank assumes suitable symmetric differences for location interpretation; sign test otherwise |
| Mean biomarker, 3+ groups | Independent, continuous | `stats::aov(y ~ group, data = d)` or `stats::oneway.test(y ~ group, data = d)` | Global test, prespecified contrasts; Welch version for unequal variance |
| Rank-oriented 3+ group comparison | Independent groups | `stats::kruskal.test(y ~ group, data = d)` | Does not handle clustering or estimate a mean effect; post hoc adjustment |
| 2 categorical variables | Independent observations | `stats::chisq.test(tab)` or `stats::fisher.test(tab)` | Cell counts and expected frequencies; risk difference/RR/OR with CI as appropriate |
| Before/after binary response | Matched binary pairs | `stats::mcnemar.test(tab)` | Discordant pairs; matched effect size; verify table orientation |
| Adjusted continuous association | Person-level continuous response | `stats::lm(y ~ exposure + age + site, data = d)` | Coefficients with units/CI; residuals, functional form and confounding |
| Adjusted binary event | Person-level yes/no response | `stats::glm(event ~ exposure + age, family = binomial(), data = d)` | Odds ratios (not risk ratios), CI, calibration/separation diagnostics |
| Count of events per follow-up time | Independent count data, unequal exposure | `stats::glm(n ~ exposure + offset(log(person_time)), family = poisson(), data = d)` | Incidence-rate ratio and CI; overdispersion, excess zeros and time denominators |
| Ordered severity category | Ordinal endpoint | `ordinal::clm(y ~ exposure, data = d)` | Proportional-odds check; ordered categories and OR scale |
| Measurements across visits/sites | Longitudinal or clustered | `lme4::lmer(y ~ group * time + (1 | id), data = d)`; `geepack::geeglm()` | Within-person/site correlation; fit, convergence, working correlation; enough clusters |
| Correlation of 2 quantitative variables | Independent pairs | `stats::cor.test(x, y, method = "pearson")` / `"spearman"` | Correlation and CI where supported; scatterplot, outliers, nonlinearity; correlation is not causation |
| Unadjusted time-to-event comparison | Censoring, known time origin | `survival::survfit(Surv(time, event) ~ group, data = d)`; `survival::survdiff()` | KM curves at-risk table; log-rank p-value, not just median survival |
| Adjusted time-to-event association | Censored event-time outcome | `survival::coxph(Surv(time, event) ~ group + age, data = d)` | Hazard ratio and CI; proportional hazards checks; censoring mechanism |
| Competing-risk event probability | Competing events preclude outcome | Cumulative-incidence methods, e.g. `cmprsk::cuminc()` | Cumulative incidence (not 1–KM with competing events simply censored) |
| Many RNA-seq genes, two groups | Raw read counts, biological replicates | `DESeq2` / `edgeR` with design and contrasts | Raw-count assay model, gene-level log2 fold changes, adjusted p-values and QC |
| Microarray / voom RNA-seq | Suitable normalized intensities or voom inputs | `limma` | Correct assay transformation, contrast, empirical-Bayes fit, FDR |
| Disease prediction / classification | Prespecified target and evaluation units | `tidymodels` or `caret` / other validated pipeline | Group-safe nested evaluation, AUC and calibration, CIs, subgroup checks |

**One sample:** A one-sample t-test compares a quantitative mean with a prespecified benchmark (`t.test(x, mu = target)`); a binomial test addresses a single proportion (`binom.test(successes, total)`). **More than two time points:** prefer mixed/repeated-measures approaches after checking the covariance assumptions, dropout and study design. **Two predictors:** Pearson or Spearman applies to association; choose regression if direction, adjustment, time structure or a response model is needed.

## 4. The assumptions and design gates

- **Independence first:** a large sample size cannot repair pseudoreplication. Technical replicates, longitudinal observations and tumor/normal specimens from one person need ID-aware methods. Random-effects models and GEEs answer related but distinct conditional vs population-average questions.
- **Outcome scale and estimand:** a t-test addresses means; a rank-sum test generally addresses relative distributions/stochastic ordering, and only under extra shape/location assumptions can be translated into a median/location claim.
- **Distribution:** residual structure, skew, heavy tails and outliers matter. Assess them visually and scientifically. Do **not** apply Shapiro-Wilk to every raw variable and switch tests mechanically at `p < 0.05`.
- **Variance:** for independent groups, Welch t-test is a useful default for means; unequal variances also affect ANOVA and some rank-test interpretations.
- **Sparse categorical tables:** inspect actual counts and expected frequencies; choose Fisher or suitable exact/model-based methods when asymptotic chi-square is unreliable. Huge sparse/multilevel tables need deliberate modeling.
- **Missing data:** report missingness by group and stage; assess plausible missingness mechanisms, reasons, and sensitivity analyses. Complete-case and multiple-imputation assumptions are **not** interchangeable; do not recode NA as zero.
- **Confounding and study design:** exploratory comparisons do not establish causation. For nonrandomized exposures, specify a causal design/estimand, variables and adjustment strategy before fitting models.
- **Multiplicity:** prespecify families and contrasts. Holm controls familywise error; Benjamini-Hochberg (`p.adjust(p, "BH")`) targets FDR under its required assumptions. An adjusted p-value is not a magnitude of clinical effect.
- **Time-to-event:** define time zero, eligibility, censoring and event type; assess proportional hazards for Cox; distinguish cause-specific hazards from subdistribution hazards when competing events occur.
- **Survey weights and design:** use `survey::svydesign()` and survey-aware analyses when sampling involves clusters, strata, or weights; ordinary GLM standard errors are not necessarily valid.
- **High dimensionality:** check design rank, donor/batch effects, features relative to participants, multiplicity and train/test contamination. Do not derive feature selection on an evaluation fold.
- **Clinical significance:** a low p-value is not proof of a useful treatment effect. Report the effect, uncertainty, absolute risks where relevant and an interpretable threshold.

See [Chicco et al. (2025)](https://doi.org/10.1186/s13040-025-00465-6), [Muhammad (2023)](https://doi.org/10.1172/JCI171058), [Rahnenführer et al. (2023)](https://doi.org/10.1186/s12916-023-02858-y), and [Gurski and Dittel (2026)](https://doi.org/10.1093/immhor/vlaf072). Those papers explain important subsets of these decisions; the above is an independently prepared synthesis, not a universal algorithm endorsed by the papers.

## 5. Worked decisions from cancer research

### A. Tumor versus normal specimens from the same person
**Question:** Is an assay-derived continuous biomarker different between paired specimens?  
**Unit:** Person; two linked specimens per person. **Start:** paired t-test on person-level differences if the mean-change estimand and assumptions fit, or an appropriate paired robust/rank analysis. Do **not** use the independent two-sample t-test. Include the number of complete pairs and the distribution of differences. For genome-wide raw RNA-seq count testing, use `DESeq2` / `edgeR` with patient blocking, design matrix and FDR rather than thousands of unadjusted paired t-tests.

### B. ESR1 / ERBB2 expression and tumor subtype
**Question:** Is a continuous expression measurement associated with a subtype factor across independent patients?  
**Unit:** Person (check for multiple specimens). **Start:** 2-group Welch or a multi-group linear model with prespecified contrasts, adjusting for relevant design variables; consider `limma` for appropriate high-throughput expression scales. Subtype should not be inferred from the very marker then treated as an independent label without explaining circularity. Batch confounding may make a simple unadjusted test indefensible.

### C. 24-month outcome and censored follow-up
**Question:** How do survival and prediction errors vary over follow-up?  
**Unit:** Person, with explicit event/censoring records and baseline time origin. **Start:** KM/log-rank for descriptive unadjusted survival contrasts and Cox or alternative survival models for covariate associations; use censoring-aware prediction metrics at the prespecified horizon where required. **Do not alter** the separate frozen [G4 synthetic survival protocol](../04_machine_learning/survival-protocol.md); this guide is not G4 implementation evidence or permission to reinterpret a Brier score as a p-value test.

### D. Clinical sites measuring a repeated biomarker
**Question:** Does an intervention-by-time association persist while accounting for clustering?  
**Unit:** People within sites, repeated visits. **Start:** mixed-effects model or GEE with a scientifically defensible correlation structure, adequate cluster count and sensitivity assessment. If randomized by site, a simple row-level t-test incorrectly treats every visit as an independent randomization.

## 6. R examples: transparent, minimal calls

These are **API patterns**, not commands to run against unidentified data. `d` must be a reviewed data frame with correct types, factor levels, units, person identifiers, and protocol-approved outcomes.

```r
# Independent mean difference: Welch is the default
fit_mean <- stats::t.test(marker ~ group, data = d)

# Paired mean difference: before and after vectors must be matched by ID first
fit_paired <- stats::t.test(d$before, d$after, paired = TRUE)

# Independent binary categorical response: confirm table counts first
tab <- table(d$group, d$event)
fit_2x2 <- if (any(chisq.test(tab)$expected < 5)) {
  stats::fisher.test(tab)
} else {
  stats::chisq.test(tab, correct = FALSE)
}
# Threshold above is an illustrative screening rule, not a sufficient universal
# algorithm. Use appropriate methods when table size or design requires them.

# Adjusted associations
fit_cont <- stats::lm(marker ~ group + age, data = d)
fit_binary <- stats::glm(event ~ group + age, data = d,
                         family = stats::binomial())

# Prespecified multiple-testing family; report its definition
adjusted_p <- stats::p.adjust(p_values, method = "BH")

# Session audit (record this alongside study inputs and output checks)
utils::sessionInfo()
```

**Caution:** The paired vectors above are safe only **after** a checked ID join and complete-pair selection; ordering rows separately can silently fabricate pairs. `glm(..., family = binomial())` estimates log odds; exponentiation yields odds ratios, not risk ratios. For complex survey or clustered data, the above simple examples are insufficient.

The repository already provides [keys and reshaping](keys-and-reshaping.md), [missingness and comparisons](missingness-and-comparisons.md), [models and uncertainty](models-and-uncertainty.md), and [R statistical visualizations](../06_RESOURCES/R/README.md). Use those as prerequisites.

## 7. R biomedical deployment: from analysis to an auditable deliverable

**Minimal architecture (no clinical deployment claim):**

```mermaid
flowchart LR
  S["Source / data permissions"] --> V["Schema, IDs, units,<br/>missingness checks"]
  V --> A["Frozen analysis plan,<br/>design and estimand"]
  A --> R["R models and diagnostics<br/>versioned scripts"]
  R --> O["Tables, figures, CIs,<br/>adjusted p-values"]
  O --> T["Independent tests / review"]
  T --> P["Quarto / R Markdown report<br/>release manifest"]
  P --> G["Publish only reviewed,<br/>privacy-cleared artifacts"]
```

| Layer | R / engineering option | Acceptance criterion |
| --- | --- | --- |
| Project environment | `renv` lockfile; explicit R and Bioconductor versions | Clean-machine restore produces a declared environment |
| Analysis dependencies | `targets` DAG for incremental pipelines | All targets run from permitted input fixtures; provenance trace exists |
| Data checking | base R + `testthat` checks, typed dictionaries | Reject duplicate IDs, invalid event coding, negative follow-up and inconsistent dimensions |
| Study modeling | `stats`, `survival`, `lme4`, `geepack`, `survey`, `DESeq2` / `edgeR` as appropriate | Independent numerical fixtures and model-specific diagnostic review |
| Tables / figures | `gtsummary`, `broom`, `ggplot2` | Denominators, units, confidence intervals and adjustment are explicit |
| Reports | Quarto or R Markdown | Executable source, frozen parameter set and traceable outputs |
| CI and software release | GitHub Actions + regression / smoke checks; optional `rworkflows` | Test logs and reviewed package versions retained; no secrets in artifacts |
| Interactive teaching | `shiny` on synthetic/aggregated outputs | No participant-level payloads in HTML, server logs, API responses or downloads |

Suggested **locally reviewed** sequence (package installs are intentional, not automatic):

```bash
# In an approved R project; install desired packages separately first
Rscript -e 'renv::restore(prompt = FALSE)'   # only with a reviewed renv.lock
Rscript -e 'targets::tar_make()'              # only if _targets.R exists
quarto render report.qmd                     # only if a reviewed report exists
git diff --check
git status --short
```

Do not add placeholders to an existing project and pretend the pipeline has run. In this repository, these are proposed integration patterns; no validated clinical deployment or new R runtime execution is asserted by this document. For package validation and CI evidence see [biomedical coding gates](../02_biomedical_coding/IMPLEMENTATION_GATES.md) and [primary R reference material](../02_biomedical_coding/PRIMARY_DOCUMENTATION.md).

## 8. Reporting checklist before publication

- [ ] Protocol states primary/secondary outcome, comparison, estimand and study design before examining results.
- [ ] Independent unit, participant/specimen/visit hierarchy, group counts, missingness and exclusions are stated.
- [ ] Measurement units, transformed scales, categories, event coding, follow-up origin, censoring are defined.
- [ ] Chosen model and alternatives are justified by assumptions, dependence, and required adjustment.
- [ ] Effect estimate, confidence interval and meaningful interpretation accompany p-values when applicable.
- [ ] Multiplicity family and correction, sensitivity/subgroup status and all exclusions are explicit.
- [ ] Diagnostic findings, model convergence, influential points and robustness are recorded.
- [ ] R version, packages/lockfile, code revision, inputs, seeds and reproducible commands are captured.
- [ ] Independent reviewer can recreate tables/figures from eligible inputs without manual spreadsheet editing.
- [ ] Privacy, participant licensing, release authority and small-cell/interactive-export disclosure risks are checked.

For trials use [CONSORT 2025](https://doi.org/10.1136/bmj-2024-081123); for prediction modeling use [TRIPOD+AI](https://doi.org/10.1136/bmj-2023-078378). Reporting checklists are **not** automatic proof that a statistical method is appropriate.

## 9. Further reading and review status

The [recent methods / R / deployment evidence review](../06_RESOURCES/Literature/BIOSTATISTICS_R_LITERATURE_2021_2026.md) links original publications, year, DOI, contribution, and what each source **does not** validate. Its companion [CSV register](../06_RESOURCES/Literature/biostatistics_r_literature_2021_2026.csv) supports filtering and future source-check passes. This is a **curated narrative review**; it is not a PRISMA systematic search or a reproduced analysis of every paper.

**Evidence boundary:** source metadata and article conclusions were checked against publisher / PubMed or journal pages during the 2026-10-22 review. No independent replay of published results or execution of the example code is claimed by this addition. Consult the original paper, up-to-date package manual and local statistical reviewer for any new use.
