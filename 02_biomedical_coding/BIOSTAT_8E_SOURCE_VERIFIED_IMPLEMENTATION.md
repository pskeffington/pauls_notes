# Biomedical methods eighth edition — source-linked biomedical coding implementation companion

**Edition:** the cited textbook author, *Fundamentals of Biostatistics*, 8th ed., 2016, ISBN 978-1-305-26892-0.  
**Original digital source:** https://shahealthcare.org/wp-content/uploads/2022/04/Fundamentals-of-Biostatistics-Bernard-Biomedical methods_compressed.pdf (962 PDF pages).  
**Scope of verification:** Full-volume file/title and contents, preface, and targeted chapter discussions of bootstrap (6.11), permutation testing (9.6), FDR (12.4), clustering/GEE (13.13–13.14), and person-time/survival (14). **This is not a claim that every paragraph, exercise, or mathematical derivation in 962 pages has been individually audited.** Do not reproduce the copyrighted textbook, tables, datasets, flowchart, or exercises in this repository.

**AI retrieval key:** `pauls-notes.biostat-8e.verified-code-companion.v1`. Required alongside [Paul's Notes canonical R practices](BIOMEDICAL_R_CANONICAL_EXAMPLE.md), [full synthetic breast cancer study](examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd), [G0–G10 implementation gates](IMPLEMENTATION_GATES.md), and [8e test selector](../03_learning/bio_stats/BIOSTAT_TEST_SELECTION_MATRIX.md). The distinct [6e crosswalk](BIOSTAT_6E_CHAPTER_TO_CODE_BEST_PRACTICES.md) must **never** be used for 8e page references.

## Authorial-method style confirmed in 8e preface

Biomedical methods describes an intermediate approach between recipe-driven and purely abstract mathematical instruction: introduce a medical research problem, build a statistical concept through worked examples, and use computer output where relevant (PDF p. 14; preface). He also describes carrying **full numerical precision in intermediate calculations**, despite rounding reported results (PDF p. 15). Therefore the coding companion adopts the following **adaptation**, not a quotation or Biomedical methods-endorsed software standard:

1. Clinical/scientific question, sampling unit, protocol and population first.
2. Specify probability model, estimand, assumptions, alternate designs, and calculation before calling R.
3. Provide independently created **synthetic breast cancer example**, explicitly fictional and never imported from textbook datasets.
4. R code in small named chunks with `##` comments, exact inputs, no hidden environment state, fixed seeds when randomization occurs.
5. Keep unrounded estimates for all downstream calculations. Round only in `knitr::kable`, `sprintf`, or final figure labels.
6. Document expected failure modes, assumption diagnostics, sensitivity, coefficient/effect CI and interpretation.
7. State when source text was directly inspected versus when a method card is a topical crosswalk or editorial extrapolation.

## 8e chapter coverage and research implementation routing

| Chapter | Verified 8e topic | Breast cancer coding lane and recommended evidence |
| --- | --- | --- |
| 1 | General overview | research question; patient/specimen/unit contract; protocol before test |
| 2 | Descriptive statistics | N/missingness, location/spread, exact denominators, histogram/boxplot |
| 3 | Probability | Bayes, base-rate screening metrics, ROC and prevalence/incidence |
| 4 | Discrete probability distributions | binomial/Poisson PMF/CDF, event counts and exposure |
| 5 | Continuous probability distributions | normal parameterization, sampling/approximation diagnostics |
| 6 | Estimation, §6.11 bootstrap | mean/proportion/rate CIs; subject-unit bootstrap with seeds |
| 7 | One-sample hypothesis testing | one-/two-sided precommitment; power and benchmark justification |
| 8 | Two-sample testing | matched versus independent, Welch and pooled-variance assumptions |
| 9 | Nonparametric tests, §9.6 permutations | ties, rank distribution, permutation exchangeability |
| 10 | Categorical tests | two proportions, Fisher/chi-square/McNemar, agreement kappa |
| 11 | Regression/correlation | linear assumptions, partial correlation, fit, CI, influence |
| 12 | Multi-group ANOVA, §12.4 FDR, §12.10 mixed models | heterogeneity, factorial terms, random intercepts, familywise/FDR |
| 13 | Epidemiologic studies, §13.13 clustering, §13.14 longitudinal, §13.16 missing data | confounding, design, logistic, GEE, cluster-level uncertainty |
| 14 | Incidence/person-time and survival, §§14.9–14.14 | KM, log-rank, Cox diagnostics and parametric alternatives |

The author explicitly separates the first 12 chapters as introductory foundation from epidemiologic/person-time applications in chapters 13 and 14 (preface, PDF pp. 14–17). Use this as an instructional sequence, **not** as a claim all methods are valid for one dataset.

## Source-verified deep dives and runnable original examples

### R8-06.11 — Bootstrap confidence limits

**Source grounding:** The 8e introduction (§6.11, printed p. 199 onward; PDF pp. 221–223) constructs a bootstrap distribution by resampling original observations with replacement and describes percentile confidence limits. It emphasizes that bootstrap intervals can be asymmetric. **Our additional implementation gate:** independently sampled observational units must be resampled at their independence level; naive row resampling is invalid for longitudinal repeated measurements or clustered patients.

**Research question:** What is uncertainty in the synthetic mean marker score? **Estimand:** marginal mean of an arbitrary teaching score; not a real biomarker population parameter.

```r
## 06.11 Bootstrap across independent synthetic patients
set.seed(711)
marker <- c(8.0, 9.3, 11.1, 12.4, 14.6, 15.0, 17.2, 18.1)
stopifnot(length(marker)>2L, all(is.finite(marker)))
B <- 2000L
boot_mean <- replicate(B, mean(sample(marker, length(marker), replace=TRUE)))
boot_ci <- stats::quantile(boot_mean, c(.025,.975), type=7)
result <- data.frame(n=length(marker), estimate=mean(marker),
                     ci_lower=unname(boot_ci[1]),ci_upper=unname(boot_ci[2]))
knitr::kable(result,digits=3)
```

**Reasoning:** resampling estimates a sampling distribution from the empirical distribution; percentile intervals may underperform with small n, bias, extreme skew and dependence. Document why percentile, basic, studentized or BCa intervals suit the estimand; bootstrapping does not repair biased sampling. Test repeated seeded replay, sample size, finiteness and clustered sample handling.

### R8-09.6 — Permutation tests and exchangeability

**Source grounding:** In §9.6 (PDF pp. 381–385), the 8e permutation discussion considers reassigning group labels under an explicit null, with an exact enumeration for a small 3-versus-3 setup and Monte Carlo simulation for larger assignment spaces. The key modern design gate is **exchangeability** under the null: pairing, clustering, stratification, treatment assignment and unequal dispersion can invalidate unrestricted label shuffling for some statistics.

**Research question:** Are two synthetic subtype-labeled groups' outcome distributions distinguishable under an exchangeable null? **This demonstration uses independent randomized group labels only; it is *not* a valid causal treatment permutation for observational cancer subtypes.**

```r
## 09.6 Exact randomization distribution for 3+3 randomized teaching units
y <- c(4.1, 5.2, 5.7, 6.8, 7.5, 8.9)
assigned <- c(0L, 0L, 0L, 1L, 1L, 1L)
stopifnot(length(y)==length(assigned),sum(assigned)==3L)
observed <- mean(y[assigned==1L]) - mean(y[assigned==0L])
choices <- utils::combn(seq_along(y), sum(assigned))
all_differences <- apply(choices, 2, function(ids) {
  mean(y[ids]) - mean(y[-ids])
})
p_exact <- mean(abs(all_differences) >= abs(observed)-1e-12)
data.frame(n_assignments=ncol(choices), estimate=observed, p_exact=p_exact)
```

**Reasoning:** an enumerated two-sided absolute-value mean-difference statistic is a specified test different from the rank-sum statistic used in the textbook example. Label this implementation accurately. If comparing real observational subtypes, unrestricted permutation does not establish an intervention effect. Check that all assignments are possible under the actual design and reassign labels **at the subject/cluster level**.

### R8-12.4 — Multiple comparisons and false discovery rate

**Source grounding:** In §12.4 (PDF p. 598), the 8e FDR discussion distinguishes controlling the expected proportion of false discoveries among declared findings from Bonferroni-style familywise error control, particularly in many-gene testing.

**Research question:** Which of four fictional marker comparisons survive a prespecified four-test family? Synthetic p-values are inputs for *demonstration*, not findings.

```r
## 12.4 Declare the family before adjusting
tests <- data.frame(gene=c("ERBB2","ESR1","GENE_C","GENE_D"),
                    raw_p=c(0.001,0.018,0.049,0.63))
stopifnot(!anyNA(tests$raw_p),all(tests$raw_p>=0 & tests$raw_p<=1))
tests$bh_fdr <- stats::p.adjust(tests$raw_p, method="BH")
tests$holm_fwer <- stats::p.adjust(tests$raw_p, method="holm")
knitr::kable(tests,digits=3)
```

**Reasoning:** specify exactly which hypotheses are in the family, whether tests are independent/dependent, chosen procedure and interpretation. BH under suitable dependence assumptions controls expected false-discovery proportion, not the posterior probability that any given gene association is false. For *actual* RNA-seq count differential expression, use an assay-aware model and its established multiple-testing workflow, not four continuous t-tests on raw counts.

### R8-13.13–13.14 — Correlated outcomes and longitudinal GEE

**Source grounding:** The 8e chapter discussion (PDF pp. 751–754) explains that adjusting for within-person subunit correlation can increase standard errors relative to a naive independence model; §13.14 covers repeated measures. This motivates making a patient/center ID a first-class part of the schema.

**Research question:** Are synthetic scores associated with follow-up time when every invented patient contributes repeated measurements?

```r
## 13.14 Longitudinal clustered example; never treat visits as independent
set.seed(712)
subject_id <- sprintf("P%03d",seq_len(80L))
repeated <- expand.grid(id=subject_id,visit=0:2,KEEP.OUT.ATTRS=FALSE)
patient_intercept <- stats::rnorm(length(subject_id),0,3)
repeated$score <- 10 + .8*repeated$visit +
                  patient_intercept[match(repeated$id,subject_id)] +
                  stats::rnorm(nrow(repeated),0,2)
stopifnot(length(unique(repeated$id))==80L, nrow(repeated)==240L)
if (requireNamespace("nlme",quietly=TRUE)) {
  fit <- nlme::lme(score~visit,random=~1|id,data=repeated)
  print(summary(fit)$tTable)
} else cat("Optional nlme unavailable; clustered model not executed.\n")
```

**Reasoning:** a random-intercept model estimates conditional association and assumes a covariance structure; population-averaged GEE is an alternative with different interpretation. For GEE, use an explicit `id` and justified working correlation and robust SE, with an adequate number of independent clusters. Check informative dropout, time-dependent covariates, covariate functional form, convergence and within-person correlation.

### R8-14 — Person-time, Kaplan–Meier, Cox and parametric survival

**Source grounding:** The book’s chapter 14 and its preface distinguish incidence rates from survival functions and discuss Kaplan–Meier, log-rank, Cox PH assumptions and parametric alternatives (printed pp. 777–856). **Original implementation gate:** time origin, risk eligibility, censoring and competing-event coding precede modeling; events per person-time are not the same as the cumulative incidence probability.

```r
## 14.1 Independent event counts and exposure; units must match
events <- c(7L,11L); person_years <- c(15,22)
stopifnot(all(events>=0L),all(person_years>0))
rate_per_100py <- 100*events/person_years
rate_result <- stats::poisson.test(events,T=person_years)
data.frame(group=c("A","B"),events=events,person_years=person_years,
           rate_per_100py=rate_per_100py)
print(rate_result)
## 14.9-14.11 illustrative event-time endpoint
if (requireNamespace("survival",quietly=TRUE)) {
  synthetic <- data.frame(time=c(1,3,4,5,7,9,11,12),
                          event=c(1,0,1,1,0,1,0,1),
                          arm=factor(rep(c("A","B"),each=4)))
  s <- survival::Surv(synthetic$time,synthetic$event)
  print(survival::survfit(s~arm,data=synthetic))
  model <- survival::coxph(s~arm,data=synthetic,x=TRUE)
  print(summary(model))
  print(survival::cox.zph(model))
}
```

**Reasoning:** an incidence rate estimates observed event frequency per exposure; `poisson.test` supplies exact conditional inference under its model. KM estimates survival under noninformative censoring, Cox gives a conditional hazard ratio under PH, and parametric survival requires an explicitly chosen distribution. None automatically estimates probability of recurrence in the presence of competing mortality.

## 8e-to-Pauls-Notes coding decisions and acceptance checklist

| Evidence/process gate | Required trace | Failure mode |
| --- | --- | --- |
| G0 source | Edition, book section, PDF page, accessed URL, method cited | Misassigned sixth/eighth edition |
| G2 schema | Unique persons, specimens, visit IDs, types, units, N/missingness | Patient pseudoreplication |
| G3 design | Estimand, direction, clustering, time zero, design | Invalid sampling distribution |
| G5 inference | Null/alternative, assumptions, uncertainty and multiplicity | p-value without effect or diagnostics |
| G7 figures | Okabe–Ito colors, axes, exact N and scales | Misleading whiskers and unlabeled units |
| G8 replay | fixed seed, code and dependencies, actual run logs | Documentation mistaken for passed execution |
| G9 prediction | subject-level split, no training/test leakage, calibration | Optimistic AUC |
| G10 clinical claims | clinical purpose and external review | Synthetic finding promoted to clinical claim |

## Reader and AI workflow

- **Read the source edition first:** 8e full-text URL above. Keep the separate 6e TOC mapping intact and never merge page/section positions without checking.
- **Look up exact method:** use [8e method-selection matrix](../03_learning/bio_stats/BIOSTAT_TEST_SELECTION_MATRIX.md) and [27-route machine decision matrix](../03_learning/bio_stats/BIOMEDICAL_DECISION_MATRIX_V2.md).
- **Start with code conventions:** use [canonical R example](BIOMEDICAL_R_CANONICAL_EXAMPLE.md), [full synthetic study](examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd), and [implementation gates](IMPLEMENTATION_GATES.md).
- **Inspect a source section:** record section/page and an independently authored methodological summary. Verify modern software behavior from package documentation rather than assume 2016 R or SAS examples still match.
- **Generate outputs:** original Rmd, method rationale, assumed distribution, test/model, effect + uncertainty, figures, computed narrative, validation run. Never embed copyrighted full-text passages or original book datasets in this repository.

**Review status:** file identity, preface and chapter navigation confirmed; targeted deep-dive methods checked in source; remaining sections are routed by authoritative chapter titles and existing independent Paul’s Notes materials. R examples are provided as templates and are **not marked executed, knitted, or scientifically validated** by this document alone.
