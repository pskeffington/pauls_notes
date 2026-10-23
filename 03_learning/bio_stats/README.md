# bio_stats: from every decision-tree object to a paper and an R analysis

[Data-first chart](../biomedical-statistics-decision-guide.md#2-data-first-statistical-test-flowchart) · [Learning home](../README.md) · [Source and node map](decision-tree-evidence.json) · [Executable implementations](../examples/paper_linked_tests.R) · [Numerical checks](../tests/test_paper_linked_tests.R)

**Reviewed and executed: 2026-10-22.** Follow the node ID printed in the chart. Every one of its **19 objects** has a named publication, a source location, and either an executable design check or an implemented method. A decision diamond is a scientific question; it does not have its own hypothesis-test p-value.

This is a teaching atlas, with three explicitly different evidence levels:

| Evidence level | What was done here | What is not established |
| --- | --- | --- |
| **Published calculation replay** | Recomputed selected published toy vectors or aggregate counts, with their source table identified | Reproduction of an entire study or its participant-level models |
| **Independent synthetic adaptation** | Ran the paper's method family on wholly invented biomedical data, using current R interfaces | Recovery of the authors' data, code, seed, coefficients or scientific conclusions |
| **Design/interpretation gate** | Executed schema, unit, scale, denominator or diagnostic checks linked to a relevant paper | Automatic approval of assumptions from a nonsignificant diagnostic |

There are no downloaded participant records. The stem-cell transplant example remains four published aggregate counts; the code never expands them into invented individual records. The other fixtures are synthetic, including the gene matrix. This atlas is separate from the frozen G4 survival experiment and does not advance its research gates.

## Run the complete atlas

Run from the repository root. Package installation is a separate setup action; sourcing the file never installs packages, downloads data, fits a model or writes files.

```bash
# Base R: design gates, elementary tests and published calculation checks
Rscript --vanilla 03_learning/examples/paper_linked_tests.R
Rscript --vanilla 03_learning/tests/test_paper_linked_tests.R

# Every named method, including mixed/survey/survival/genomic alternatives
Rscript --vanilla 03_learning/examples/paper_linked_tests.R --full
Rscript --vanilla 03_learning/tests/test_paper_linked_tests.R --full
python3 scripts/check_biostatistics_evidence.py
```

Full mode requires `MASS`, `nnet`, `lme4`, `geepack`, `survey`, `ordinal`, `survival`, `cmprsk`, `DESeq2`, `edgeR`, and `limma`. An absent package produces a named error rather than a silent skipped method. In a normal R project, install CRAN packages with `install.packages()` and Bioconductor packages with `BiocManager::install()` using mutually compatible R/Bioconductor releases. The [CI workflow](../../.github/workflows/learning-case-validation.yml) declares its Ubuntu package setup. Record your actual versions with `sessionInfo()`; newer manuals may describe behavior absent from an older installed version.

Prepare the common inputs once for the code below:

```r
source("03_learning/examples/paper_linked_tests.R")
fixture <- make_paper_fixture()
validate_paper_fixture(fixture)
d <- fixture$people
two <- droplevels(d[d$group != "third", ])
long <- fixture$visits
base <- run_paper_base_examples(fixture)
full <- run_paper_extended_examples(fixture)
```

`d` has **120 invented people, 40 per independent group**. Before/after columns are paired by row ID. `long` has **60 other invented people, three visits per person**; it demonstrates a single clustering level, not simultaneous site and person random effects. The assay has **500 invented features × 12 independent samples**, six per group. The seed is `7122026`; constructing it preserves the caller's random-number state. Assay effects are simulated only to exercise the software; counts of significant genes are not evidence about cancer.

## Decision objects

These rows account individually for every nonterminal routing object. The code objects `base$A` through `base$N` expose their checks; they are not statistical tests of whether a study design is appropriate.

| Object | Specific paper and source location | What the paper did / why this decision exists | Demonstration and next decision |
| --- | --- | --- | --- |
| **A: identify outcome** | **BS-001**, [Chicco et al., 2025](https://doi.org/10.1186/s13040-025-00465-6), Methods / selection of statistical tests | Organizes introductory tests by variable type and comparison | `base$A`: name the measured outcome, person as unit, and mean-difference estimand before choosing a test |
| **B: data type** | **BS-001**, [Chicco et al., 2025](https://doi.org/10.1186/s13040-025-00465-6), Methods | Contrasts numeric and categorical inputs | `base$B`: inspect numeric, factor and ordered classes; time/event and many-feature routes additionally need S/H sources |
| **C: continuous or count** | **AT-004**, [Green, 2021](https://doi.org/10.1080/21642850.2021.1920416), count-regression tutorial | Fits Poisson/negative-binomial models to health-behavior counts | `base$C`: integer event count plus positive person-time routes to R; continuous marker routes to E |
| **D: nominal or ordinal** | **AT-008**, [Selman et al., 2024](https://doi.org/10.1186/s13063-024-08072-2), Background | Reviews ordered clinical endpoints and alternatives to discarding their ordering | `base$D`: `category` is unordered A/B/C; `grade` retains low/middle/high ordering |
| **E: comparison and dependence** | **BS-002**, [Muhammad, 2023](https://doi.org/10.1172/JCI171058), simulated mouse example / Table 1 | Compares analyses of repeated mouse weights with missing observations | `base$E`: distinguish independent group counts, complete person pairs and repeated-unit counts before T/P/AN/CR/MX |
| **N: categorical design** | **AT-006**, [Kim, 2017](https://doi.org/10.5395/rde.2017.42.2.152), tests of independence; **AT-007**, [Fagerland et al., 2013](https://doi.org/10.1186/1471-2288-13-91), Background | Independent contingency tables and matched before/after tables require different sampling models | `base$N`: compare the independent group × binary table with the paired before × after table; route to BIN, CH or MC |

```r
base$A
base$B[c("marker", "episodes", "binary", "grade")]
base$C
base$D
base$E
base$N
```

An R storage check cannot decide whether two specimens are from one donor. Study identifiers, metadata and protocol must establish that fact. Branches describe the question and estimand, not a sequence of automated normality pretests.

## T: independent continuous outcomes

**Papers:** **BS-009**, [West (2021), *Best practice in statistics: Use the Welch t-test when testing the difference between two groups*](https://doi.org/10.1177/0004563221992088); **BS-001**, Chicco et al. (2025), Mann–Whitney Methods and artificial-data examples. West discusses unequal-variance mean comparisons; Chicco demonstrates rank-sum calculations. Our independent invented marker comparison is an adaptation, not a reproduction of West's examples.

**Given:** continuous marker; different people in comparison and reference groups. **Mean question:** is comparison minus reference zero? **Rank question:** do the groups differ in relative distribution/location under the stated assumptions?

```r
x <- two$marker[two$group == "comparison"]
y <- two$marker[two$group == "reference"]
welch <- stats::t.test(x, y, var.equal = FALSE, conf.level = .95)
rank_sum <- stats::wilcox.test(x, y, exact = FALSE, correct = TRUE,
                              conf.int = TRUE)
c(mean_difference = mean(x) - mean(y), t = welch$statistic,
  df = welch$parameter, p = welch$p.value)
welch$conf.int
rank_sum[c("statistic", "p.value", "estimate", "conf.int")]
```

Welch's denominator is `sqrt(var(x)/length(x) + var(y)/length(y))`, with Satterthwaite degrees of freedom. The test suite independently computes both statistic and CI. Inspect group shapes, influence and meaningful units. The rank-sum output is not automatically a median difference; its location estimate/CI requires a location-shift interpretation. Exact versus approximate calculation and continuity correction are explicit, so software defaults cannot silently change this demonstration. A suitable robust method needs its own estimator and assumptions; rank-sum is the implemented alternative in this chart.

**Published-data discrepancy:** BS-001 Table 10 reports `p = .398` for `[1,1,1,1,1]` versus `[10,10,10,10,10]`. With the stated normal approximation, tie correction and continuity correction, R 4.3.3 returns **0.003976752**. This replay **does not confirm that published row**; no inference about the cause of the discrepancy is made. The vectors are toy values, not patient data. The discrepancy is tested and must not be silently overwritten.

## P: paired continuous outcomes

**Papers:** **BS-001**, [Chicco et al. (2025), Table 9](https://biodatamining.biomedcentral.com/articles/10.1186/s13040-025-00465-6/tables/9), paired artificial samples; **AT-001**, [Roberson et al. (1995), *Analysis of paired Likert data*](https://pubmed.ncbi.nlm.nih.gov/8582561/), Methods/Results. Roberson compares t, signed-rank and sign procedures on simulated ordered responses; that does not make a t-test appropriate for a single ordinal item. The code below instead uses a continuous invented marker.

**Given:** one after and one before measurement for each ID. Let Δ = after − before. The paired t-test addresses mean Δ; signed-rank uses signed ranks with symmetry needed for its location interpretation; the sign test uses only positive versus negative nonzero differences.

```r
delta <- d$after - d$before
paired_t <- stats::t.test(d$after, d$before, paired = TRUE)
signed_rank <- stats::wilcox.test(d$after, d$before, paired = TRUE,
                                 exact = FALSE, correct = TRUE, conf.int = TRUE)
nonzero <- delta[delta != 0]
sign_test <- stats::binom.test(sum(nonzero > 0), length(nonzero), p = .5)
paired_t[c("estimate", "conf.int", "statistic", "parameter", "p.value")]
signed_rank[c("statistic", "p.value", "estimate", "conf.int")]
sign_test[c("estimate", "conf.int", "p.value")]
```

Report 120 pairs, the direction of subtraction, mean change/CI for the t-test, and the zero-difference policy. The sign-test CI concerns the probability of positive change **conditional on a nonzero change**, not the mean change. Inspect the difference distribution; never sort the two vectors independently.

**Published toy replay:** Table 9's `[10,12,15,18,20] − [1,2,7,8,5]` gives mean change **10.4**, t ≈ **8.607**, df = **4**, R p = **0.001001424**. It agrees approximately with the table's reported `1.000 × 10^-3`, rather than matching all displayed digits.

## AN: three or more independent groups

**Papers:** **AT-002**, [Gurski and Dittel (2026)](https://doi.org/10.1093/immhor/vlaf072), Statistical principles / ANOVA and multiple comparisons; **AT-021**, [Welch (1951)](https://doi.org/10.1093/biomet/38.3-4.330), unequal-variance several-means method; **BS-001**, Chicco et al. (2025), Kruskal–Wallis Methods. Gurski and Dittel provide a biological multiple-comparison guide; our R implementation is not their GraphPad workflow or experimental data.

**Given:** continuous marker in three independent groups. Ordinary ANOVA compares between-group variation with within-group variation under the common-variance model; Welch ANOVA relaxes equal variances. Kruskal–Wallis compares pooled rank patterns, with a different estimand.

```r
anova_fit <- stats::aov(marker ~ group, data = d)
summary(anova_fit)
welch_anova <- stats::oneway.test(marker ~ group, data = d, var.equal = FALSE)
kw <- stats::kruskal.test(marker ~ group, data = d)
welch_anova
kw
# Prespecified all-pairs mean contrasts under the ordinary ANOVA model only:
stats::TukeyHSD(anova_fit)
```

Ordinary F = MS_between / MS_within, with numerator df = 2 and residual df = 117 here. The global p-value does not identify which groups differ. Report group summaries and planned contrasts with simultaneous CIs or justified adjustment. Do not attach Tukey's common-variance intervals to Welch or rank results. A Kruskal–Wallis rejection is not automatically a statement about medians.

## CR: two quantitative variables

**Papers:** **AT-003**, [Schober, Boer and Schwarte (2018)](https://doi.org/10.1213/ANE.0000000000002864), correlation interpretation; **AT-022**, [Aggarwal and Ranganathan (2017), *Common pitfalls in statistical analysis: Linear regression analysis*](https://doi.org/10.4103/2229-3485.203040). These are medical methods articles. Our age/marker calculations are independent synthetic demonstrations.

**Given:** age and continuous marker measured once per person. Pearson quantifies linear association; Spearman quantifies monotone rank association. Regression specifies an outcome, units and covariate adjustment.

```r
pearson <- stats::cor.test(d$age, d$marker, method = "pearson")
spearman <- stats::cor.test(d$age, d$marker, method = "spearman", exact = FALSE)
linear <- stats::lm(marker ~ age + group, data = d)
pearson[c("estimate", "conf.int", "statistic", "p.value")]
spearman[c("estimate", "statistic", "p.value")]
summary(linear)$coefficients
stats::confint(linear)
```

Report r or rho and the scatterplot; base R does not supply a Spearman CI here. The age slope is marker units per year conditional on group, with a CI. Review functional form, residuals, leverage and confounding. Neither correlation nor adjusted regression alone establishes causation.

## R: counts and rates

**Paper:** **AT-004**, [Green (2021)](https://doi.org/10.1080/21642850.2021.1920416), tutorial using overdispersed views and symptom-day counts, with Poisson/negative-binomial examples in R and other software. Our recurrent-event/person-year fixture is a **rate-model adaptation**; its exposure offset is not claimed to be the exact specification of Green's examples.

**Given:** integer episodes and unequal positive person-years. Model `log(E[count]) = log(person_years) + intercept + group effect`; the offset coefficient is fixed at one.

```r
poisson <- stats::glm(episodes ~ group + offset(log(person_years)),
                      data = d, family = stats::poisson())
nb <- MASS::glm.nb(episodes ~ group + offset(log(person_years)), data = d)
dispersion <- sum(stats::residuals(poisson, type = "pearson")^2) /
  stats::df.residual(poisson)
c(pearson_dispersion = dispersion, negative_binomial_theta = nb$theta)
exp(cbind(rate_ratio = coef(poisson), stats::confint.default(poisson)))
exp(cbind(rate_ratio = coef(nb), stats::confint.default(nb)))
```

The intercept exponentiates to a baseline rate; group coefficients exponentiate to incidence-rate ratios. NB2 variance is μ + μ²/θ. The synthetic fixture is intentionally overdispersed. Compare fit, zeros, dependence and exposure validity; a single dispersion cutoff is not sufficient model selection. The numerical tests verify the group-only Poisson rate ratio against aggregated events/person-time. A year-1/year-2 coefficient alone cannot identify a law's causal effect.

## BIN: one proportion

**Paper:** **AT-005**, [Clopper and Pearson (1934)](https://doi.org/10.1093/biomet/26.4.404), original binomial interval method. The [R `binom.test` manual](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/binom.test.html) explicitly identifies this interval. The paper is the interval source; it is not a claim that the authors analyzed our invented response data.

**Given:** successes out of a fixed number of independent eligible people, prespecified null proportion .5.

```r
binomial <- stats::binom.test(sum(d$binary), nrow(d), p = .5, conf.level = .95)
binomial[c("statistic", "parameter", "estimate", "conf.int", "p.value")]
```

Report numerator, denominator, observed proportion and Clopper–Pearson CI. Its coverage is at least the nominal level under the binomial model and can be conservative. Unknown population prevalence does not automatically justify independent Bernoulli sampling; a fixed finite population sampled without replacement can require a hypergeometric model. Do not call a repeated-event rate a binomial proportion.

## CH: independent categorical outcomes

**Papers:** **AT-006**, [Kim (2017)](https://doi.org/10.5395/rde.2017.42.2.152), independent-table tutorial and Table 1; **AT-023**, [Ranganathan, Pramesh and Aggarwal (2017), *Logistic regression*](https://doi.org/10.4103/picr.PICR_87_17); **AT-008**, [Selman et al. (2024)](https://doi.org/10.1186/s13063-024-08072-2), Background discussion of multinomial and binary alternatives. Selman's paper reviews trial analyses; our `multinom` fit is not a reanalysis of those trials.

**Given:** independent group × binary counts; binary outcome with age adjustment; or unordered A/B/C as a distinct outcome.

```r
tab <- table(two$group, two$binary)
chi <- stats::chisq.test(tab, correct = FALSE)
fisher <- stats::fisher.test(tab)
chi$expected
chi[c("statistic", "parameter", "p.value")]
fisher[c("estimate", "conf.int", "p.value")]
logistic <- stats::glm(binary ~ group + age, data = d, family = stats::binomial())
exp(cbind(odds_ratio = coef(logistic), stats::confint.default(logistic)))
multinomial <- nnet::multinom(category ~ group + age, data = d,
                              trace = FALSE, Hess = TRUE, maxit = 1000)
exp(coef(multinomial))
summary(multinomial)$standard.errors
```

Chi-square compares observed cells with expected counts under independence. Fisher conditions on margins and sums appropriate hypergeometric probabilities. Preserve table orientation when reporting ORs. Logistic coefficient exponentials are odds ratios, not risk ratios. Multinomial coefficients compare B versus A and C versus A; it does not exploit ordinal information. Use its Hessian-based SEs or a justified alternative for uncertainty, and check sparse categories, separation and convergence. Do not interpret the multinomial model as a proportional-odds fit.

**Published illustrative replay:** Kim's Table 1 Example 3, rows male/female and columns condition A/B, is `[[30,70],[70,30]]`. Expected cells are 50; the uncorrected chi-square is **32**, df = **1**, and φ = **0.4**. These are illustrative aggregate frequencies from the paper. Setting `correct = FALSE` is necessary to reproduce its Pearson statistic.

## MC: paired binary outcomes

**Paper:** **AT-007**, [Fagerland, Lydersen and Laake (2013)](https://doi.org/10.1186/1471-2288-13-91), [Table 1](https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-13-91/tables/1), equations 1–5 and Table 6. The authors compare McNemar variants, including stem-cell transplant examples. They used Matlab and StatXact/SAS for their evaluation; this is an independent R replay of one aggregate example, not their original code.

**Given:** airway hyper-responsiveness before/after transplant in 21 children. Rows are **before**; columns are **after**. Both axes use AHR first, no AHR second.

| Before / after | AHR | No AHR |
| --- | ---: | ---: |
| AHR | 1 | 1 |
| No AHR | 7 | 12 |

```r
sct <- matrix(c(1, 1, 7, 12), nrow = 2, byrow = TRUE)
asymptotic <- stats::mcnemar.test(sct, correct = FALSE)
corrected <- stats::mcnemar.test(sct, correct = TRUE)
exact <- stats::binom.test(1, 8, p = .5)
mid_p <- 2 * stats::pbinom(1, 8, .5) - stats::dbinom(1, 8, .5)
c(asymptotic = asymptotic$p.value, corrected = corrected$p.value,
  exact_conditional = exact$p.value, mid_p = mid_p)
```

There are eight discordant pairs, split 1 versus 7. The uncorrected statistic is `(7−1)^2/(7+1) = 4.5`. The replay yields **p = .03389485**, continuity-corrected **.07709987**, exact conditional **.0703125**, and mid-p **.0390625**. Method choice changes the p-value; label it explicitly. The paper critiques conservative variants; showing them is not a recommendation to choose whichever rejects. The raw marginal change is `(8−2)/21 = 0.2857143`, a descriptive **28.6 percentage-point increase**. The conditional binomial CI returned by `exact` is for the discordance direction probability, not a CI for that marginal change.

## O: ordered outcomes

**Paper:** **AT-008**, [Selman et al. (2024)](https://doi.org/10.1186/s13063-024-08072-2), Background and Results on ordinal trial endpoints, proportional-odds assumptions, rank procedures and alternatives. Our low/middle/high analysis is an adaptation. The [ordinal implementation article](https://cran.r-project.org/web/packages/ordinal/vignettes/clm_article.pdf) is package documentation, explicitly not a published JSS paper.

```r
ordinal_rank <- stats::wilcox.test(as.integer(grade) ~ group, data = two,
                                  exact = FALSE, correct = TRUE)
ordinal_fit <- ordinal::clm(grade ~ group + age, data = d, link = "logit")
ordinal_rank
summary(ordinal_fit)
exp(ordinal_fit$beta)
stats::confint.default(ordinal_fit)
ordinal::nominal_test(ordinal_fit)
```

The rank calculation uses only order, not an assumption of equal grade spacing. The cumulative logit is `logit(P(Y ≤ j)) = threshold_j − xβ`; therefore positive β increases odds of being **above** a threshold. Report exp(β) with a CI and category definitions. `nominal_test` examines relaxing parallel slopes; it cannot prove proportional odds from a large p-value. Preserve the ordered outcome, inspect category counts and convergence, and consider a prespecified partial-odds or other model when scientifically warranted.

## MX: repeated, clustered and survey designs

**Papers:** **BS-002**, [Muhammad (2023)](https://doi.org/10.1172/JCI171058), repeated mouse weights and missing observations; **AT-009**, [Bates et al. (2015)](https://doi.org/10.18637/jss.v067.i01), `lme4` model formulation; **AT-010**, [Højsgaard, Halekoh and Yan (2006)](https://doi.org/10.18637/jss.v015.i02), `geepack` marginal models; **AT-011**, [Lumley (2004)](https://doi.org/10.18637/jss.v009.i08), complex survey designs. The geepack article is conventionally cited as 2006; its publisher metadata also shows a December 2005 posting. These are distinct design choices, not interchangeable tests.

```r
# Mixed model: subject random intercept; ML fits for nested fixed-effect LRT.
mixed <- lme4::lmer(marker ~ group * visit + (1 | id), data = long, REML = FALSE)
mixed_null <- lme4::lmer(marker ~ group + visit + (1 | id), data = long, REML = FALSE)
stats::anova(mixed_null, mixed)
lme4::fixef(mixed)
stats::confint(mixed, parm = "beta_", method = "Wald")
lme4::isSingular(mixed)

# GEE: rows sorted contiguously by ID; sandwich SE is the geeglm default.
gee <- geepack::geeglm(marker ~ group * visit, id = id, waves = visit,
                       family = gaussian(), corstr = "exchangeable", data = long)
summary(gee)$coefficients

# Survey: different invented person-level fixture, 12 PSUs in 2 strata.
survey_design <- survey::svydesign(ids = ~psu, strata = ~stratum,
                                  weights = ~weight, data = d)
survey_fit <- survey::svyglm(marker ~ group + age, design = survey_design)
summary(survey_fit)$coefficients
stats::confint(survey_fit)
```

Report cluster counts, visit schedule, correlation structure, coefficient/CI, convergence and singularity. The mixed-model interaction LRT is asymptotic, not a small-sample corrected F test; ordinary `lmer` does not supply denominator-df p-values here. GEE uses 60 clusters in this fixture and population-average interpretation; few-cluster studies need additional treatment. The identity-link Gaussian example does not exhibit the conditional/marginal odds-ratio distinction of logistic mixed/GEE models.

Muhammad's published example used a different covariance structure, including AR(1), and missing observations. Our random-intercept complete-data fit **does not reproduce that specification or its results**. Survey PSUs, strata and unequal weights represent sampling design, not an arbitrary cure for repeated measurements. Real studies with sites plus patients need a fuller design than this single-level illustration.

## S: time-to-event and competing risks

**Papers:** **AT-012**, [Clark et al. (2003), Survival Analysis Part I](https://doi.org/10.1038/sj.bjc.6601118), KM/log-rank and an ovarian cancer example; **AT-013**, [Bradburn et al. (2003), Part II](https://doi.org/10.1038/sj.bjc.6601119), adjusted Cox modeling; **AT-014**, [Austin, Lee and Fine (2016)](https://doi.org/10.1161/CIRCULATIONAHA.115.017719), cumulative incidence and competing risks in a heart-failure case study. The code uses wholly synthetic follow-up and distinct invented competing-event times.

```r
Surv <- survival::Surv
km <- survival::survfit(Surv(time, event) ~ group, data = d)
log_rank <- survival::survdiff(Surv(time, event) ~ group, data = d)
cox <- survival::coxph(Surv(time, event) ~ group + age, data = d, x = TRUE)
summary(km, times = 12)  # survival, SE, CI, and numbers at risk
c(chi_square = log_rank$chisq,
  p = stats::pchisq(log_rank$chisq, df = length(log_rank$n)-1, lower.tail = FALSE))
summary(cox)$coefficients
exp(stats::confint(cox))
survival::cox.zph(cox)
# cr_status: 0=censored, 1=relapse, 2=competing death; cr_time is its own endpoint.
cif <- cmprsk::cuminc(d$cr_time, d$cr_status, group = d$group, cencode = 0)
cmprsk::timepoints(cif, times = 12)
cif$Tests  # Gray group-comparison tests for cause-specific cumulative incidence
```

KM estimates survival using event/risk-set products; log-rank compares observed and expected events over risk sets. Cox reports adjusted hazard ratios, not risk ratios or survival-time ratios. Check time zero, censoring, risk sets, proportional hazards and uncertainty. A nonsignificant `cox.zph` does not establish the assumption. `cuminc` estimates cumulative incidence while retaining competing-event information; its variance output can support justified uncertainty calculations.

**Independent numerical counterexample:** four invented people: event 1 at t=1, competing event at t=2, event 1 at t=3, censoring at t=4. Event-1 cumulative incidence at t=3 is **.5**, while `1−KM` after censoring the competing event is **.625**. The suite checks both values. These numbers illustrate a method error; they are not Austin's clinical estimates. A different justified survival model requires a separate specified example; this atlas implements the named KM/log-rank/Cox/competing-risk routes.

## H: many molecular features

**Papers:** **AT-015**, [Love, Huber and Anders (2014)](https://doi.org/10.1186/s13059-014-0550-8), DESeq2 count models; **AT-016**, [Robinson, McCarthy and Smyth (2010)](https://doi.org/10.1093/bioinformatics/btp616), edgeR; **AT-017**, [Law et al. (2014)](https://doi.org/10.1186/gb-2014-15-2-r29), voom weights; **AT-018**, [Ritchie et al. (2015)](https://doi.org/10.1093/nar/gkv007), limma linear models. Each paper develops/demonstrates a method; the matrix below is not any paper's assay data.

**Given:** 500 synthetic features × 12 independent samples, six per group. Counts must be untransformed nonnegative integers, metadata rows must exactly match count columns, and the design must identify the comparison. These samples are independent; a paired experiment would instead require a reviewed patient-blocking design.

```r
counts <- fixture$counts
metadata <- fixture$metadata
stopifnot(identical(colnames(counts), rownames(metadata)))

# DESeq2: NB dispersion estimation, fit, Wald test; explicit contrast.
dds <- DESeq2::DESeqDataSetFromMatrix(counts, metadata, design = ~group)
dds <- DESeq2::DESeq(dds, quiet = TRUE, fitType = "mean")
de <- as.data.frame(DESeq2::results(dds,
  contrast = c("group", "comparison", "reference"), alpha = .05))
head(de[, c("log2FoldChange", "lfcSE", "stat", "pvalue", "padj")])

# edgeR: expression filter, TMM normalization, dispersion, two-group exact test.
ed <- edgeR::DGEList(counts = counts, group = metadata$group)
ed <- ed[edgeR::filterByExpr(ed), , keep.lib.sizes = FALSE]
ed <- edgeR::calcNormFactors(ed)
ed <- edgeR::estimateDisp(ed)
et <- edgeR::exactTest(ed, pair = c("reference", "comparison"))
head(edgeR::topTags(et, n = Inf, adjust.method = "BH")$table)

# voom: log-count mean/variance precision weights followed by limma moderation.
design <- stats::model.matrix(~group, data = metadata)
v <- limma::voom(ed, design, plot = FALSE)
vf <- limma::eBayes(limma::lmFit(v, design))
head(limma::topTable(vf, coef = "groupcomparison", n = Inf, adjust.method = "BH"))

# Continuous-intensity limma demonstration: separate invented log2 intensity scale.
# log2(counts+1) is only an invented numeric fixture, not a microarray normalization recipe.
intensity <- log2(counts + 1)
lf <- limma::eBayes(limma::lmFit(intensity, design))
head(limma::topTable(lf, coef = "groupcomparison", n = Inf, adjust.method = "BH"))
```

Report sample/feature counts, filtering, normalization, design/contrast direction, log2 fold changes, SE/intervals where available and adjusted p-values. Inspect library size, dispersion, mean/variance and residual diagnostics. The selected DESeq2 `fitType="mean"` is explicit for the synthetic fixture and is not asserted to reproduce the paper's fitting choices. Current DESeq2 defaults and shrinkage options differ from parts of the original 2014 workflow; this example does not request separate post-fit LFC shrinkage. edgeR's two-group exact test is not an adjusted multivariable model. voom's precision weights distinguish it from simply applying t-tests to log counts. Do not transform counts then pass them to DESeq2/edgeR.

FDR families apply to retained genes/eligible tests with package-specific filtering/NA policies, not all unrelated tests in this atlas. This is not a four-method accuracy benchmark; all outputs are execution demonstrations without a model-ranking claim.

## Z: final verification

**Papers:** **BS-002**, Muhammad (2023), dependence/missing observations; **AT-019**, [Benjamini and Hochberg (1995)](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x), step-up false-discovery control; **AT-020**, [Sterne et al. (2009)](https://doi.org/10.1136/bmj.b2393), missing-data assumptions and imputation pitfalls. None endorses automatic clearance from this checklist.

```r
base$Z$missing
base$Z$linear_ci
base$Z$pearson_dispersion
base$Z$raw_p
base$Z$bh
base$Z$holm
full$mixed_singular
full$ordinal_po_check
full$cox_ph_check
utils::sessionInfo()
```

The four prespecified **invented gene p-values** `.003, .02, .07, .6` give BH-adjusted `.012, .04, .09333333, .6` and Holm-adjusted `.012, .06, .14, .6`. They are not a pooled family of unrelated branch tests. BH's original independence result is not a guarantee under arbitrary dependence. Holm familywise-error control and BH false-discovery control answer different questions.

The fixture deliberately rejects missing values rather than silently dropping them. That is an input contract, **not a recommendation for complete-case analysis**. For actual incomplete data, describe missingness, justify the missing-data model, and prespecify sensitivity analyses; this atlas does not run multiple imputation or claim that observed missingness tests determine the mechanism. Record units, pair/cluster counts, effect direction, uncertainty, model diagnostics and package versions before interpreting a result.

## Execution and reproduction ledger

| Evidence | Executed result / status | Scope |
| --- | --- | --- |
| All 19 chart objects | Paper + source locator + executable design/method mapping | Coverage validator checks exact node-set equality |
| Chicco Table 9 paired toy comparison | p = **.001001424**, approximately reported .001 | Selected toy row replay; no participant data |
| Kim Table 1 Example 3 | χ² = **32**, df = **1**, φ = **.4** | Published illustrative count-table arithmetic |
| Fagerland Table 1 SCT example | Asymptotic **.03389485**; exact **.0703125**; mid-p **.0390625** | Published aggregate calculation replay |
| Chicco Table 10 separated constant vectors | R p = **.003976752**, versus paper **.398** | **Disagreement retained**, not a successful reproduction |
| Other named chart procedures | All executed on the declared synthetic fixtures | Method-family adaptations, not published-study reproductions |
| Independent numerical checks | Welch statistic/CI, Poisson aggregate rate ratio, competing-risk .5 vs .625, BH/Holm arithmetic pass | Selected independent verification cases |
| Invalid-input checks | Reject duplicate person/pair keys, missing marker, zero exposure, invalid event code, fractional assay counts and sample-ID reordering | Prevents selected silent misuse; not a universal data validator |

Local execution used **R 4.3.3** and compatible Ubuntu 24.04 packages: MASS 7.3-60.0.1, nnet 7.3-19, lme4 1.1-35.1, geepack 1.3.10, survey 4.2-1, ordinal 2023.12-4, survival 3.5-8, cmprsk 2.2-11, DESeq2 1.42.0, edgeR 4.0.16, limma 3.58.1. Check the installed runtime rather than assuming a current online manual matches these versions. CI reruns the full suite; numerical values above are bounded teaching checks, not clinical validation.

## Source register

The [JSON register](decision-tree-evidence.json) records full paper titles, authors, years, DOI/PMID links, exact source locations, node membership and output keys. Foundational sources are intentionally outside the recent-literature window. A publisher abstract or metadata record supports a narrower claim than a full original-code audit; each source locator says what was inspected. Only the rows explicitly marked as calculation replays were reproduced numerically. No claim is made that every publication's code or full text was independently audited.
