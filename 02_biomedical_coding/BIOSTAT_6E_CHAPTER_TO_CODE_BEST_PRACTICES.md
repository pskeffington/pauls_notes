# Biomedical methods sixth edition — complete chapter-route biomedical coding handbook

**Paul's Notes · Original implementation guidance · Source-scope status: table-of-contents verified, chapter-body review pending**

**Source supplied:** the cited textbook author, *Fundamentals of Biostatistics*, **6th edition**, Thomson Brooks/Cole, copyright 2006, ISBN-13 978-0-495-06441-1. The user's nine-page PDF contains the title/copyright pages and the table of contents, **not chapters 1–14 or the appendix itself**. Accordingly, chapter and section *titles and printed start pages* below are verified against this supplied contents listing; explanations, R implementations, scientific guardrails and examples are independently authored, **not quotations, proofs or confirmed author-specific recommendations from the unseen chapter body**.

**Do not merge editions.** Existing [Biomedical methods test-selection matrix](../03_learning/bio_stats/BIOSTAT_TEST_SELECTION_MATRIX.md) references the **8th edition** and remains its own authority. This guide indexes the **sixth edition**. Do not infer a sixth-edition section number from an eighth-edition chapter or imply that 2006 textbook descriptions reflect today's package defaults.

**AI retrieval key:** \`pauls-notes.biostat-6e.biomedical-implementation.v1\`. For biomedical statistical programming, load this guide alongside [canonical R style](BIOMEDICAL_R_CANONICAL_EXAMPLE.md), [synthetic complete study](examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd), [implementation gates](IMPLEMENTATION_GATES.md) and the user's actual data dictionary. For a specific Biomedical methods chapter, search \`R6-CHXX\` or the listed heading; never respond as if the full textbook text was inspected.

## Universal biomedical evidence-to-code contract

1. **Preanalysis:** define the target population, observation grain (person, tumor, specimen, visit, center, cell), exposure, outcome, time origin, study design, estimand, direction of contrasts, one-/two-sided alternative, and scientifically meaningful change *before* selecting a test.
2. **Data:** validate identifiers, types, units, legal values, missingness, numerator/denominator, paired keys, biological replicates, joins, person-time, right-censoring and outliers. Record every exclusion and missing-data decision.
3. **Mathematics:** write the sampling model and assumptions; choose a method justified by scale and design. Keep exact calculations and approximations separate; use variance and effective sample size from the actual design.
4. **Implementation:** R Markdown with YAML, \`##\` R-code section dividers, independent named chunks, deterministic synthetic examples, explicit \`stats::\` calls, scoped dependencies and absence of hidden files. Keep default code visible (\`echo=TRUE\`) and use \`knitr::kable\`.
5. **Results:** estimate plus units, denominator, effect direction, 95% interval when appropriate, test statistic/df, prespecified p-value, assumption diagnostics, sensitivity and plain-language inference piped from computed values. Distinguish *statistical evidence* from *clinical relevance*.
6. **Visuals:** Okabe–Ito palette from \`06_RESOURCES/R/scientific_palette.R\`, actual N and missingness, verified scale/units, clear axes, exact reference lines, legible legends. Box whiskers are not confidence intervals.
7. **Audit:** record seed, data provenance, source version, \`sessionInfo()\`, render environment, computational replay, checks and known limitations. Do not claim clinical validation from a test passing.

## 6e chapter-to-code crosswalk

| ID | 6e chapter (printed page) | Source TOC scope | Original Paul's Notes implementation requirement |
| --- | --- | --- | --- |
| R6-CH01 | General Overview (1) | Chapter heading only | Research question and design metadata |
| R6-CH02 | Descriptive Statistics (6) | Location/spread/CV/grouping/graphics; lead and tobacco examples | Exact N, mean/SD/median/quartiles, distribution and grouped denominators |
| R6-CH03 | Probability (43) | Conditional probability; Bayes, screening, ROC, prevalence/incidence | Base rates, predictive values, thresholds and ROC caveats |
| R6-CH04 | Discrete Probability Distributions (81) | Random variables, expectation, variance, binomial and Poisson | PMF/CDF and integer outcome validation |
| R6-CH05 | Continuous Probability Distributions (122) | Normal, standardized normal, linear combinations, approximations | Verify CLT conditions and distribution approximation regime |
| R6-CH06 | Estimation (166) | Randomization, mean/variance, binomial/Poisson confidence intervals | Estimator, uncertainty, interval method, coverage assumptions |
| R6-CH07 | Hypothesis Testing: One-Sample Inference (226) | One-sided/two-sided, power, sample size, variance, binomial, Poisson | Predeclared null/alternative, alpha, CI correspondence and sensitivity |
| R6-CH08 | Hypothesis Testing: Two-Sample Inference (296) | Paired t, independent equal/unequal variance, outliers, longitudinal sample size | Distinguish subject pairing and Welch vs pooled t |
| R6-CH09 | Nonparametric Methods (359) | Sign, signed-rank, rank-sum | Ties, zero differences, symmetry and distribution estimands |
| R6-CH10 | Hypothesis Testing: Categorical Data (385) | Two proportions, Fisher, McNemar, RxC, GOF, kappa | Matched vs independent, expected cells, agreement vs association |
| R6-CH11 | Regression and Correlation Methods (464) | Least squares, intervals, fit, multiple/partial/rank correlation | Residuals, confounding, diagnostics and slope/CI |
| R6-CH12 | Multisample Inference (557) | One-/two-way ANOVA, contrasts, Kruskal–Wallis, random effects, ICC | Factorial design, variance model, nesting and multiplicity |
| R6-CH13 | Design and Analysis Techniques for Epidemiologic Studies (630) | Effect measures, standardization, MH, multiple logistic, meta-analysis, equivalence, crossover, clustering, measurement error, missing data | Explicit source population and bias/heterogeneity analysis |
| R6-CH14 | Hypothesis Testing: Person-Time Data (744) | Incidence rates, trends, strata, survival, KM, log-rank, PH | Genuine exposure, independent risk sets, censoring and PH diagnostics |

### R6-CH01 — General overview

**Method:** formulate a testable scientific question and analysis plan. **Breast cancer teaching prompt:** do fictional tumor groups differ in ERBB2 continuous score? **Code contract:** declare patients vs specimens, exposure/outcome and contrast before calling \`t.test\`. Keep hypotheses and estimands in YAML/protocol metadata. **Guardrail:** multiple specimens from one patient do not create independent patients; subtype labels derived from a marker can make the marker-group comparison tautological.

### R6-CH02 — Descriptive statistics

The contents list measures of location, arithmetic mean properties, spread, variance/SD properties, coefficient of variation (CV), grouped data, graphs and two non-oncology cases. **Original translation:** in the breast cancer workbook, summarize \`age_years\`, \`tumor_cm\`, \`erbb2_score\` with exact total N, observed n, missing n/%; sample SD (denominator n−1), median, Q1/Q3 (declare type 7), IQR, range and category frequencies. Separate specimens from patients. **CV** = SD/mean only where measurement is ratio-scaled with meaningful nonzero mean; don't apply indiscriminately to centered log expression or signed scales. **Check:** extreme values may be real; flag instead of automatically discarding.

~~~r
x <- c(9.1, 11.0, 13.5, NA_real_, 16.2)
stopifnot(is.numeric(x), !any(is.infinite(x)))
observed <- x[!is.na(x)]
c(total_n=length(x), valid_n=length(observed), missing_n=sum(is.na(x)),
  mean=mean(observed), sample_sd=stats::sd(observed),
  median=stats::median(observed),
  q1=unname(stats::quantile(observed,.25,type=7)),
  q3=unname(stats::quantile(observed,.75,type=7)))
~~~

**Figure standard:** histogram plus boxplot (or a justified distribution display), true N and units, mean/median labeled with numeric values; never identify IQR whiskers as CI.

### R6-CH03 — Probability, Bayes, screening, ROC, prevalence/incidence

The sixth-edition contents explicitly include **Bayes' rule and screening tests** (§3.7), **Bayesian inference** (§3.8), **ROC curves** (§3.9), and **prevalence/incidence** (§3.10). **Original translation:** use prevalence/base rate when deriving positive predictive value; never equate sensitivity, specificity or AUC with PPV. Declare whether probabilities refer to cancer diagnosis, risk, test positivity or population prevalence. Separate prevalence (fraction existing at a point/period) and incidence (new events per at-risk population or person-time).

~~~r
sensitivity <- .90; specificity <- .95; prevalence <- .04
ppv <- sensitivity*prevalence /
       (sensitivity*prevalence + (1-specificity)*(1-prevalence))
npv <- specificity*(1-prevalence) /
       ((1-sensitivity)*prevalence + specificity*(1-prevalence))
c(ppv=ppv,npv=npv)
~~~

These are hypothetical test properties; do **not** treat the numbers as a breast cancer screening test's true performance. For ROC, vary thresholds on held-out probabilities, document positive class, ties, AUC CI, prevalence and calibration. Bayesian **inference** (posterior distribution and prior model) is distinct from Bayes' theorem used in a 2×2 screening calculation.

### R6-CH04 — Discrete distributions and counting processes

Contents: random-variable PMF/CDF, expectation, variance, permutations/combinations, binomial and Poisson. **Original translation:** a binomial model requires a *fixed number of independent comparable Bernoulli trials* with common p; a Poisson event-count model requires a justified event mechanism and exposure/constant intensity for a homogeneous model. Do not apply either to normalized continuous gene expression. Inspect Poisson mean–variance discrepancy, repeated events, clustering and excess zeros.

~~~r
## Exactly k events vs upper-tail k or more: different questions
stats::dbinom(14L,size=40L,prob=.3)
stats::pbinom(13L,size=40L,prob=.3,lower.tail=FALSE)
## Count events per true exposure, never use counts alone as rates
stats::poisson.test(x=9L,T=6,r=.8)
~~~

### R6-CH05 — Continuous distributions and approximation conditions

Contents: normal distribution, standardization, linear combinations and binomial/Poisson normal approximations. **Original translation:** record units and parameterization \`N(mean, sd^2)\`; \`pnorm()\` takes **sd**, not variance. For binomial approximation check \`np\` and \`n(1-p)\` and use continuity correction if appropriate; do not assume the CLT repairs non-independence or heavy-tailed/infinite-variance processes. For small samples, check exact distribution methods and interval coverage.

~~~r
mu <- 10; sigma <- 2
stats::pnorm(12,mean=mu,sd=sigma)
z <- (12-mu)/sigma
stopifnot(isTRUE(all.equal(stats::pnorm(z),stats::pnorm(12,mu,sigma))))
~~~

### R6-CH06 — Estimation and randomized-study structure

Contents include the relationship between sample/population, random-number tables, randomized clinical trials, mean/variance and binomial/Poisson estimation, one-sided CIs. **Original translation:** differentiate sampling from treatment assignment; randomization is not generated by calling \`set.seed()\` after observing outcomes. State target parameter, estimator, SE, confidence level, method (Wald/exact/score/likelihood) and nominal coverage. For small binomial samples prefer intervals appropriate to design, not unguarded \`p ± 1.96 SE\`. **Check:** exact uncertainty is not the same as algorithmically exact arithmetic.

~~~r
stats::t.test(c(10.1,10.9,11.3,12.4),conf.level=.95)$conf.int
stats::binom.test(12L,40L,conf.level=.95)$conf.int
stats::poisson.test(8L,T=25,conf.level=.95)$conf.int
~~~

### R6-CH07 — One-sample testing, power and sample size

Contents cover one-/two-sided one-sample mean alternatives, power, sample size, tests vs confidence intervals, binomial/Poisson and one-sample variance inference. **Original translation:** preregister direction of alternative and alpha before inspecting data; do not infer a one-sided test after seeing a positive difference. A failed rejection is not proof of equivalence. Choose effect size and clinically meaningful difference for planning. **Sampling/design rule:** the ordinary variance chi-square test assumes a normally distributed independent sample and is fragile to non-normality.

~~~r
stats::t.test(c(1.1,1.5,1.4,1.8),mu=1.2,alternative="two.sided")
stats::binom.test(24L,50L,p=.4,alternative="greater")
stats::power.t.test(delta=2,sd=5,power=.8,sig.level=.05,
                    type="one.sample",alternative="two.sided")$n
~~~

Report unrounded planned sample size rounded **up** for enrollment and add expected attrition/cluster design effects when appropriate. Post hoc observed power from the observed p-value is not a substitute for uncertainty.

### R6-CH08 — Paired versus independent two-sample inference

Contents explicitly distinguish paired and independent equal/unequal variance t-tests, outliers and longitudinal sample size. **Original translation:** match specimens by patient ID and time definition, then use the vector of *within-patient* changes for paired t inference. For independent groups prefer Welch by default when variance equality is not established, while recording its sample sizes and Satterthwaite df. Do not choose paired tests based only on similar n. Prespecify outlier handling and inspect sensitivity, never delete values solely because they are statistically inconvenient.

~~~r
before <- c(5,7,9,6,8); after <- c(6,9,10,7,11)
stats::t.test(after,before,paired=TRUE)
stats::t.test(c(7,9,11,12),c(6,8,13,15),var.equal=FALSE)
~~~

### R6-CH09 — Sign, signed-rank and rank-sum

Contents list three nonparametric tests. **Original translation:** for pairs, sign test models number of positive *nonzero* changes; signed-rank requires attention to symmetry and zero differences; independent rank-sum compares relative distributions, not automatically median equality. Record ties, zeros, sample sizes and exact/asymptotic method used.

~~~r
delta <- c(2,-1,4,0,3,-2)
nonzero <- delta[delta!=0]
stats::binom.test(sum(nonzero>0),length(nonzero),p=.5)
stats::wilcox.test(delta,mu=0,exact=FALSE)
stats::wilcox.test(c(5,6,8,10),c(4,7,9,11),exact=FALSE)
~~~

### R6-CH10 — Categorical inference, matched data and agreement

Contents: two proportions, Fisher, McNemar, RxC, goodness of fit, kappa. **Original translation:** distinguish two independent groups from matched before/after binary outcomes. For paired binary outcomes, McNemar is based on discordant cells. For diagnostic agreement, kappa corrects for expected chance agreement but depends on prevalence/margins; include observed agreement and marginal tables too. A goodness-of-fit multinomial test uses *predeclared* expected probabilities; don't treat it as a two-group independence test.

~~~r
independent <- matrix(c(18,22,12,28),nrow=2,byrow=TRUE)
stats::fisher.test(independent)
paired <- matrix(c(32,8,3,37),nrow=2,byrow=TRUE)
stats::mcnemar.test(paired)
## Kappa is an agreement parameter, not an association test
observed_agreement <- sum(diag(paired))/sum(paired)
chance <- sum(rowSums(paired)*colSums(paired))/sum(paired)^2
kappa <- (observed_agreement-chance)/(1-chance)
kappa
~~~

### R6-CH11 — Regression, correlation and fit

Contents include least squares, coefficient inference, fitted lines, goodness of fit, multiple/partial and rank correlation. **Original translation:** report adjusted vs unadjusted estimands and predictor units, factor levels and conditional slope; inspect fitted-versus-residual, Q-Q, heteroskedasticity, influence, nonlinearity and collinearity. Correlation is scale-free association; regression slope predicts mean outcome change per predictor unit. Missingness can change analyzed N and covariate distributions.

~~~r
d <- data.frame(size_cm=c(1,2,3,4,5,6),
                score=c(9,10,12,11,15,16))
fit <- stats::lm(score~size_cm,data=d)
stats::confint(fit)
summary(fit)
~~~

### R6-CH12 — One-/two-way ANOVA, random effects and ICC

Contents list fixed-effects one-way ANOVA, specific contrasts, two-way ANOVA, Kruskal–Wallis, random-effects one-way model, and the intraclass correlation coefficient. **Original translation:** for ordinary one-way ANOVA inspect residual distribution, equal variance, independence and prespecified contrasts; for Welch ANOVA avoid automatic pooled SD assumptions. A two-way model must consider interactions and scientific interpretation of main effects conditional on interactions. A random intercept/ICC depends on a defined cluster level (hospital, patient, slide reader); do not estimate a meaningful ICC from arbitrary sequential IDs.

~~~r
d <- data.frame(group=factor(rep(c("A","B","C"),each=5)),
                y=c(7,8,9,6,8, 8,10,9,11,10, 12,11,13,12,14))
stats::oneway.test(y~group,data=d,var.equal=FALSE)
stats::kruskal.test(y~group,data=d)
## Two-way/factorial ANOVA only for a truly factorial design:
## stats::aov(y ~ treatment * site, data=validated_factorial_data)
~~~

### R6-CH13 — Epidemiologic design, confounding, stratification and bias

Contents: study design; categorical effect measures; confounding/standardization; Mantel–Haenszel; logistic regression; meta-analysis; equivalence; crossover; clustered binary data; measurement error; missing data. **Original translation:** define risk, rate, odds and hazard separately; case-control odds ratios do not directly estimate risks without additional assumptions; distinguish conditional from marginal effects. Assess exposure/covariate timing, selection bias, reverse causality, residual confounding, effect modification and clustering. Standardization needs a valid target-population distribution. Mantel–Haenszel needs explicitly constructed strata and an appropriate common effect target. Meta-analysis needs study-specific effect scale/SE and heterogeneity; a forest plot alone is not a model. Equivalence requires *two* predeclared margins/tests or an appropriate CI rule: nonsignificance is not equivalence. Crossover needs carryover/period and patient-level structure. Missing data requires describing mechanism/assumptions, complete-case changes and sensitivity; do not silently impute.

~~~r
## Two 2x2xK strata: dimension 1/2 correspond to exposure/outcome
strata <- array(c(12,18,8,22, 16,24,10,30),dim=c(2,2,2))
stats::mantelhaen.test(strata)
## Logistic regression illustrates an *odds* contrast, not risk ratio
d <- data.frame(y=c(1,0,1,1,0,0,1,0,1,0),
                exposure=c(1,1,1,0,0,0,1,0,1,0),
                age=c(51,44,60,57,48,42,62,54,55,49))
stats::glm(y~exposure+age,data=d,family=stats::binomial())
~~~

### R6-CH14 — Person-time, incidence, survival and hazards

Contents distinguish one-/two-sample and stratified incidence-rate methods, rate trends, Kaplan–Meier, log-rank, proportional hazards and power. **Original translation:** define start/end of risk period, units of person-time, event recurrence and competing risks before modeling. Event *rate* is count divided by exposure; it is not the probability of having at least one event. A log-offset Poisson model estimates rate ratios, requiring exposure positivity and review of mean-variance, cluster dependence and temporal rate homogeneity. For time-to-first-event, ensure event indicator, censoring, time zero, KM assumptions, log-rank estimand and Cox PH diagnostics. Hazard ratios are not instantaneous risk probabilities or survival differences.

~~~r
stats::poisson.test(c(6L,11L),T=c(14,19))
if (requireNamespace("survival",quietly=TRUE)) {
  demo <- data.frame(time=c(2,4,5,7,8,10),
                     event=c(1,0,1,1,0,1),
                     group=factor(c("A","A","A","B","B","B")))
  survival::survfit(survival::Surv(time,event)~group,data=demo)
}
~~~

## Appendix and advanced method routing

The 6e contents list statistical tables for exact binomial and Poisson probabilities, normal/t/chi-square/F distributions, ESD outlier statistics, Wilcoxon, Fisher z, Spearman and Kruskal–Wallis, plus a *methods-of-statistical-inference flowchart*. These are documented **as listed in the TOC only**; the table values and flowchart contents were **not supplied**. In software use version-checked R functions to obtain distribution probabilities and critical values, record tails/df/parameterization and independently verify representative hand calculations. Do not claim to reproduce the absent published flowchart.

For modern omics, complex surveys, prediction validation, competing risks, causal inference, measurement-error correction or multilevel longitudinal analysis, follow specialist protocols and the repository's existing [27-route decision matrix](../03_learning/bio_stats/BIOMEDICAL_DECISION_MATRIX_V2.md). Do not attribute newer extensions automatically to Biomedical methods 6e.

## Source-alignment and completion ledger

| Requirement | Current state |
| --- | --- |
| Supplied PDF title, edition, copyright and contents pages 1–9 read | **verified** |
| Fourteen numbered chapter titles and their listed methods mapped | **verified against 6e TOC** |
| Section-by-section exact mathematical language, proofs, examples and author cautions | **not verifiable: chapter text absent** |
| Original breast cancer examples and R implementation patterns authored | **documented, not empirically validated** |
| R example execution and knitted outputs | **not executed in this documentation pass** |
| Agreement with 8th-edition existing selector | **edition separation documented; no equivalence claim** |
| Clinical validation, real patient data or primary-source methods review | **not performed** |

## Reviewer protocol when the full textbook becomes available

For each section §§1–14, document exact source page, author-specific result/assumption, independent derivation or numeric check, modern R API and method version, synthetic fixture, counterexample, interpretation, CI and evidence artifact. Do not copy the book's prose, worked problem statements, tables or flowchart into a public repository. Mark each chapter \`toc_only\`, \`full_text_checked\`, \`computationally_tested\`, \`scientifically_reviewed\` separately; never promote a status without evidence. Preserve the current 8e material as a distinct edition.
