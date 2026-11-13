# Rosner-aligned biomedical statistical test decision matrix

[Biomedical statistics learning guide](../biomedical-statistics-decision-guide.md) · [Design-first selector](../../06_RESOURCES/BIOMEDICAL_TEST_DECISION_TREE.md) · [Paper and executable-test atlas](README.md) · [R implementations](../../06_RESOURCES/R/README.md)

**Teaching crosswalk | 2026-11-13.** An original method-selection aid organized around Bernard Rosner, *Fundamentals of Biostatistics*, **8th ed.** (Cengage, 2016; ISBN 9781305268920). Chapter references follow the [publisher's table of contents](https://www.cengage.com/c/fundamentals-of-biostatistics-8e-rosner/9781305268920). This is **not** a reproduction of Rosner's copyrighted flowchart, worked exercises or textbook text. Rosner is the foundational textbook; the existing paper atlas supplies independently linked biomedical applications. Specific modeling choices below are editorial guidance, not claims that Rosner mandates a given software function.

## Breast-cancer worked examples and interpretation\n\n[**Independent numerical reference calculations**](BREAST_CANCER_NUMERICAL_VALIDATION.md) — 5 fully worked synthetic examples, hand formulas, R calls, reference values, uncertainty, and Results narratives.\n\n[**Full 26-method breast-cancer teaching atlas**](BREAST_CANCER_WORKED_TEST_ATLAS.md) — study questions, synthetic input structure, R commands, interpretation of effects and confidence intervals, assumption gates and modern extensions. [Executable synthetic R laboratory](../examples/breast_cancer_test_atlas.R) · [Numerical/contract checks](../tests/test_breast_cancer_test_atlas.R).\n\n## Selection contract: ask in this order

1. **Scientific target:** describe a parameter, estimate an effect, test a prespecified hypothesis, assess association, or predict outcomes? Specify the estimand, population, time zero and meaningful effect size.
2. **Outcome:** continuous; binary; nominal/ordinal; integer event count; person-time rate; censored time-to-event; or many-feature assay. Numeric coding does not establish measurement scale.
3. **Sampling unit and design:** independent subjects, paired/matched subjects, repeated measurements, clustered units, complex survey, or a stratified design. Resolve the dependence structure **before** deciding a test.
4. **Comparison:** one sample versus reference, two groups, three-plus groups, trend, or adjusted multivariable association. Define group reference and contrast direction.
5. **Eligibility:** denominators, exposure time, missingness, support/range, distributional assumptions, sparse cells, censoring, influential observations and multiplicity.
6. **Deliverable:** estimate with units, confidence interval and denominator, diagnostic evidence, prespecified p-value when relevant, sensitivity analysis, limitations and reproducible R invocation.

## Primary decision matrix

| Outcome / question | Design and comparison | Starting method / R entrypoint | Must check before inference | Rosner 8e | Existing atlas / selector |
| --- | --- | --- | --- | --- | --- |
| Continuous mean vs known reference | One independent sample | One-sample t, `stats::t.test(x, mu=...)` | Independent sampling, mean estimand, distribution/outliers, interval | Ch 7 | One-sample route: distinguish from 2-group |
| Continuous means | Two independent groups | Welch t, `stats::t.test(y ~ group)` | Individual independence, direction, influential observations, mean vs ranks | Ch 8 | `T`, `welch-t` |
| Continuous before/after | Two readings per matched unit | Paired t on differences, `stats::t.test(after,before,paired=TRUE)` | Stable IDs, paired differences, missing pairs, subtraction direction | Ch 8 | `P`, `paired-t` |
| Continuous/ordinal paired ranks | Two matched observations | Signed-rank or sign, `stats::wilcox.test(...,paired=TRUE)`; `stats::binom.test(...)` for sign counts | Symmetry for signed-rank location interpretation, ties, zero differences | Ch 9 | `P`, `signed-rank` |
| Continuous/ordinal independent ranks | Two independent groups | Wilcoxon rank-sum, `stats::wilcox.test(y ~ group)` | Independence, ties, shapes; a distribution comparison is not automatically a median difference | Ch 9 | `T`, `wilcox-independent` |
| Continuous means | Three-plus independent groups | One-way ANOVA or Welch ANOVA, `stats::aov()` / `stats::oneway.test()` | Homoscedasticity when ordinary ANOVA; prespecified post-hoc contrasts | Ch 12 | `AN`, `welch-anova` |
| Ordinal / ranks | Three-plus independent groups | Kruskal-Wallis, `stats::kruskal.test()` | Independent units, ties, meaning of distributional differences | Ch 12 | `AN`/`O`, `kruskal-wallis` |
| One binary proportion | Fixed eligible trials | Exact binomial, `stats::binom.test(k,n,p=p0)` | Fixed n, genuine success/failure, common success probability and independence | Chs 4, 7 | `BIN`, `binomial-proportion` |
| Two independent binary proportions | Two independent groups | Two-proportion inference; chi-square or Fisher exact, `stats::prop.test()` / `stats::fisher.test()` | Cell counts, denominators, independence, risk difference/risk ratio/odds ratio estimand | Ch 10 | `CH`, `contingency-analysis` |
| Paired binary transitions | Same subjects before and after | McNemar; exact discordance alternative when sparse, `stats::mcnemar.test()` | Matched 2x2 table and discordant pairs; not unpaired chi-square | Ch 10 | `MC`, `mcnemar` |
| Nominal categories | Independent R-by-C table | Pearson chi-square / exact alternative, `stats::chisq.test()` | Expected counts, table structure, sampling method, multiplicity | Ch 10 | `CH`, `contingency-analysis` |
| Categorical distribution vs hypothesized probabilities | One multinomial sample | Chi-square goodness-of-fit, `stats::chisq.test(x,p=...)` | Prespecified probabilities sum to 1; small expected cells and parameter fitting | Ch 10 | Specialist analysis; not 2-group independence |
| Continuous x and y | Independent paired x-y measurements | Pearson/Spearman correlation, `stats::cor.test()` | Linearity vs monotonicity, outliers, pairing by record | Ch 11 | `CR`, `association-model-review` |
| Continuous outcome with predictors | Independent observational units | Linear regression, `stats::lm()` | Functional form, residuals, leverage, collinearity, confounding | Ch 11 | `CR`, association review |
| Binary outcome with covariates | Independent or design-adjusted observations | Logistic regression, `stats::glm(family=binomial)` | Events, separation, model complexity, dependence and adjusted OR interpretation | Ch 13 | `CH`, specialist adjustment |
| Stratified exposure–disease table | Epidemiologic strata | Mantel–Haenszel family; `stats::mantelhaen.test()` for suitable tables | Strata defined a priori, confounding, homogeneity and outcome/design | Ch 13 | Specialist epidemiologic review |
| Repeated or clustered outcome | Multiple readings per unit/site | Mixed model or GEE, e.g. `lme4::lmer()` / `geepack::geeglm()` | Unit IDs, correlation structure, dropout, cluster count | Ch 13 | `MX`, `correlated-outcome-review` |
| Event count in equal observation windows | One count vs reference process | Poisson exact calculation, `stats::poisson.test()` | Counting process, time window, constant intensity, variance and dependence | Chs 4, 14 | `R`; one-rate review |
| Events per person-time | Unequal exposure or follow-up | Poisson rate inference or `stats::glm(family=poisson, offset=log(person_time))` | Positive exposure, count integer, dispersion, changing hazard and excess zero | Ch 14 | `R`, `count-rate-model-review` |
| Overdispersed event rates | Unequal person-time | Negative-binomial model as assessed alternative, e.g. `MASS::glm.nb()` | Exposure offset and overdispersion; distinguish excess zeros | Extension alongside Ch 14 | `R`, count review |
| Survival curve | Event time + event/censor flag | Kaplan–Meier, `survival::survfit()` | Defined time origin, event coding, censoring and follow-up | Ch 14 | `S`, survival review |
| Survival groups | Event time, censoring, independent groups | Log-rank, `survival::survdiff()` | Group assignment, time zero, survival-curve crossing and interpretation | Ch 14 | `S`, survival review |
| Adjusted time-to-event | Event time, censoring and predictors | Cox PH, `survival::coxph()` | PH assumption, time-varying effects, influential records, censoring | Ch 14 | `S`, survival review |
| Competing events | Distinct mutually exclusive first events | Cumulative incidence / cause-specific or subdistribution model as appropriate | Competing-event coding, target risk vs hazard and censoring | Modern extension, not textbook chapter claim | `S`, competing-risk atlas |
| Complex probability survey | Weights, strata and primary sampling units | `survey::svydesign()` / `survey::svyglm()` | Valid sampling design variables, degrees of freedom and population target | Modern design overlay | `MX`, `survey-design-review` |
| Gene expression features | Many tests, sample-level design | Assay-aware DESeq2/edgeR/limma pipeline and FDR | Raw vs transformed counts, batch, replication, independent sample, contrast | Modern omics extension | `H`, `omics-design-review` |

**Interpretation safeguard:** distributional tests do not become mean tests by default. A nonsignificant normality test does not prove normality; do not choose between parametric and rank methods solely by an automated Shapiro-test threshold. Observational statistical association alone does not identify causation.

## Worked teaching prompts (no imported patient data)

### Example A — vaccination response

Among 80 independent eligible participants, 36 respond; null response probability is 0.35. If the prespecified alternative is **more than 35%**, the exact one-sided tail is (P(X\ge36\mid X\sim\mathrm{Binomial}(80,0.35))), **not** the single probability (P(X=36)).

```r
stats::binom.test(36L, 80L, p = 0.35, alternative = "greater")
stats::pbinom(35L, size = 80L, prob = 0.35, lower.tail = FALSE)
```

The binomial calculation concerns response probability under the trial assumptions, not vaccine efficacy without a suitable comparative design.

### Example B — infection clearance

Nine of 29 independently observed patients cleared infection; historical null spontaneous-clearance probability 0.25. Question: is the number of clearances unexpectedly high under that **prespecified** model? Compare `P(X >= 9)` with a two-sided exact test only if the scientific alternative differs. The historical rate may not be a valid counterfactual for treated patients.

```r
stats::pbinom(8L, size = 29L, prob = 0.25, lower.tail = FALSE)
stats::binom.test(9L, 29L, p = 0.25, alternative = "greater")
```

### Example C — annual death counts

At 40 deaths per 100,000 person-years, a population of 20,000 observed **for one full year** has expected count `lambda = 40 / 100000 * 20000 = 8` under homogeneous Poisson assumptions. For `k` or more, compute `P(X >= k) = 1 - P(X <= k-1)`. If people contribute different years, use actual summed person-time; a population number alone is not exposure.

```r
lambda <- 40 / 100000 * 20000
k <- 10L
stats::ppois(k - 1L, lambda = lambda, lower.tail = FALSE)
```

### Example D — paired breast-cancer biomarkers

If ESR1 expression is recorded twice for each patient, pair on **person ID and visit/specimen definition**, then investigate paired *within-person* differences. Multiple samples per patient are not independent replicates. If biological endpoints are raw sequencing counts, use an assay-aware model rather than a t-test on unprocessed reads.

## Acceptance gates for every method card

- **G2:** source/consent boundary, unit ID, unique keys, denominators, units and missingness.
- **G3:** design structure, target population, time origin and estimand.
- **G5:** assumptions, diagnostics, effect/CI, multiplicity and sensitivity.
- **G7:** plot includes N, units, legend and accessible annotation; whiskers are not CIs.
- **G8:** stable R code, synthetic fixtures, numerical independent replay and version/seed metadata.

Do **not** mark an example validated simply because it is documented here; no new R test execution was performed as part of this documentation-only pass. Existing methods and empirical evidence remain governed by the [method intake rules](../../06_RESOURCES/STATISTICAL_METHOD_INTAKE.md) and the [paper atlas](README.md).

## Executable Rosner crosswalk

The primary R selector offers **optional textbook references**. Existing methods and routing remain unchanged if the flag is omitted.

```r
source("06_RESOURCES/R/biomedical_test_selector.R")
source("06_RESOURCES/R/rosner_method_crosswalk.R")
selected <- biomedical_method_decision(
  outcome_type = "continuous", design = "independent", n_groups = 2L,
  include_rosner = TRUE
)
print(selected)
selected$rosner$chapters   # "8"
selected$required_checks  # analytical gates, not automatic approval
```

The [CSV crosswalk](rosner_method_registry.csv) records all 27 selector IDs; `coverage = extension` explicitly means a contemporary method/design overlay, **not** a claim about Rosner's text. [Synthetic method exercises](../examples/rosner_method_cases.R) provide independent continuous, paired continuous, binomial, categorical, Poisson and optional survival examples. All data are invented; never report their estimates as clinical findings.

```bash
Rscript --vanilla 06_RESOURCES/tests/test_biomedical_test_selector.R
Rscript --vanilla 06_RESOURCES/tests/test_rosner_method_crosswalk.R
Rscript --vanilla 03_learning/tests/test_rosner_method_cases.R
```

**Execution status:** Added tests require an R installation to verify; these files have not been executed in the current environment.

## Source and scope

**Primary textbook:** Rosner B. *Fundamentals of Biostatistics*. 8th ed. Cengage Learning; 2016. ISBN 9781305268920. [Publisher catalog / chapter list](https://www.cengage.com/c/fundamentals-of-biostatistics-8e-rosner/9781305268920).

**Modern applications:** consult the [paper-based evidence atlas](README.md) and [2021–2026 biomedical R-method literature](../../06_RESOURCES/Literature/BIOSTATISTICS_R_LITERATURE_2021_2026.md). Crosswalk chapter assignments describe topical coverage, not exact section-by-section reproduction or independent verification of every formula in the book.
