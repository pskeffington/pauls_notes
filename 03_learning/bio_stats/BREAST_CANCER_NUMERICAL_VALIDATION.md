# Breast cancer biostatistics — numerical validation and interpretation

[Worked method atlas](BREAST_CANCER_WORKED_TEST_ATLAS.md) · [R example source](../examples/breast_cancer_test_atlas.R) · [R reference assertions](../tests/test_breast_cancer_reference_values.R) · [Rosner method matrix](ROSNER_TEST_SELECTION_MATRIX.md)

**Validation pass: 2026-11-13.** All values below are computed from **synthetic teaching observations**. Independent numerical reference calculations were run using Python/SciPy 1.17.0; **R execution has not been verified in this environment**. Fixed numerical targets are asserted in a companion R test so another researcher can replay the examples. Numerical agreement does **not** establish that a synthetic analysis is appropriate for real breast cancer research.

## 1. Welch's t-test: independent continuous biomarker levels

**Question.** Do independent patients in hypothetical cohorts A and B have different mean biomarker scores?

| Participant | A | B |
| --- | ---: | ---: |
| 1 | 8 | 9 |
| 2 | 9 | 11 |
| 3 | 10 | 13 |
| 4 | 11 | 15 |
| 5 | 12 | 17 |
| 6 | 13 | 19 |

These table columns represent **12 different individuals**. Row 1 in A is **not paired** with row 1 in B. Values are synthetic *arbitrary biomarker score units*, not verified Ki-67 percentages or RNA-seq read counts.

**Estimand:** \(\mu_A-\mu_B\). Sample means: \(\bar x_A=10.5\), \(\bar x_B=14.0\). Sample variances: \(s_A^2=3.5\), \(s_B^2=14.0\).

**Compute:**

\[
t=\frac{\bar x_A-\bar x_B}{\sqrt{s_A^2/n_A+s_B^2/n_B}}
 =\frac{-3.5}{\sqrt{3.5/6+14/6}}=-2.04939.
\]

Welch–Satterthwaite degrees of freedom \(\nu\approx7.35294\). Two-sided \(p\approx0.07767\); 95% CI for A minus B: **−7.4994 to 0.4994**.

```r
A <- c(8, 9, 10, 11, 12, 13)
B <- c(9, 11, 13, 15, 17, 19)
out <- stats::t.test(A, B, var.equal = FALSE)
unname(out$estimate[1] - out$estimate[2])
out$statistic
out$parameter
out$conf.int
out$p.value
```

**Results narrative (synthetic):** “In 12 independent hypothetical patients (six per cohort), the mean score was 10.5 in cohort A and 14.0 in cohort B. The estimated A-minus-B mean difference was −3.50 units (95% CI −7.50 to 0.50; Welch two-sided p=0.0777). The interval is compatible with both a lower mean in A and a small positive difference; these observations do not establish clinical equivalence.”

**Limitations:** small groups, arbitrary scores, and no basis for causal comparisons. Review influence/shape and allocation before using this procedure on a real cohort.

## 2. Paired t-test: within-person post-treatment change

**Question.** Does the biomarker change across two specimens for the *same* patients?

| Patient ID | Before | After | After − before |
| --- | ---: | ---: | ---: |
| P01 | 8 | 7 | −1 |
| P02 | 10 | 9 | −1 |
| P03 | 12 | 11 | −1 |
| P04 | 14 | 11 | −3 |
| P05 | 16 | 15 | −1 |
| P06 | 18 | 17 | −1 |
| P07 | 20 | 18 | −2 |
| P08 | 22 | 19 | −3 |

**Estimand:** mean person-level after-minus-before change. The eight changes sum to −13; mean change \(\bar d=-13/8=-1.625\). Sample SD of differences \(s_d\approx0.9161\), SE \(\approx0.3239\).

\[
t=\frac{\bar d}{s_d/\sqrt{8}}\approx-5.01699,
\qquad df=7.
\]

Two-sided p=**0.001536**, 95% CI **−2.3909 to −0.8591** synthetic score units.

```r
before <- c(8,10,12,14,16,18,20,22)
after  <- c(7,9,11,11,15,17,18,19)
delta <- after - before
stopifnot(length(delta) == 8L, !anyNA(delta))
stats::t.test(delta, mu = 0)
```

**Results narrative (synthetic):** “Among eight matched hypothetical patients with complete paired measurements, the average after-minus-before change was −1.625 score units (95% CI −2.391 to −0.859; two-sided paired t p=0.00154). These data exhibit a decrease in the invented measurement, not proof of benefit, tumor response, or treatment causality.”

**Critical issue:** this test uses the **difference distribution**, not a separate normality assumption for each timepoint. Pair IDs must be explicitly checked; row order alone is not sufficient for real studies.

## 3. Binomial test: response among eligible patients

**Question.** Given exactly \(n=80\) independent eligible hypothetical patients and \(k=36\) recorded responses, how compatible is this with a fixed baseline response probability \(p_0=0.35\), for prespecified alternative \(p>0.35\)?

\[
X\sim\operatorname{Binomial}(80,0.35),\quad
\hat p=36/80=0.45.
\]
\[
P(X\ge36\mid p_0)=\sum_{j=36}^{80}{80\choose j}(0.35)^j(0.65)^{80-j}
\approx0.04106885.
\]

```r
stats::binom.test(36, 80, p = .35, alternative = "greater")
stats::pbinom(35, 80, prob = .35, lower.tail = FALSE)
```

**Results narrative (synthetic):** “Response occurred in 36/80 eligible hypothetical participants (45%). Under a prespecified independent-binomial null model with response probability 35%, the one-sided probability of observing 36 or more responses was approximately 0.0411. This is not evidence of treatment *efficacy* relative to an appropriate control group.”

**Critical issue:** a one-sided test and its one-sided confidence bound must not be misreported as a conventional two-sided 95% CI. Check the historical comparator's relevance.

## 4. Poisson upper-tail: recurrence counts per person-time

**Question.** If a hypothetical baseline recurrence event **rate** is 40 per 100,000 person-years, what is the probability of at least 10 events over 20,000 person-years?

\[
\lambda=\frac{40}{100{,}000}\times20{,}000=8,\qquad
P(X\ge10)=1-\sum_{j=0}^{9}\frac{e^{-8}8^j}{j!}
\approx0.28337574.
\]

```r
rate <- 40 / 100000
person_years <- 20000
lambda <- rate * person_years
stats::ppois(9, lambda = lambda, lower.tail = FALSE)
```

**Results narrative (synthetic):** “Under a constant-rate Poisson model with expected count eight, the probability of at least ten events is approximately 28.3%. The calculation does not by itself indicate an unusual count, and cannot establish that the rate is constant or applicable to breast cancer recurrence.”

**Critical issue:** a rate denominated in person-years must not be applied to a simple population count without compatible observation time; recurrent events may be dependent.

## 5. Chi-square goodness-of-fit: invented molecular-profile mix

**Question.** Are counts across three synthetic profile categories compatible with a hypothetical prespecified distribution (40%, 35%, 25%)?

Observed \(O=(60,45,45)\), total \(N=150\). Expected counts \(E=(60,52.5,37.5)\). 

\[
\chi^2=\sum_{i=1}^{3}\frac{(O_i-E_i)^2}{E_i}
=0+\frac{56.25}{52.5}+\frac{56.25}{37.5}
\approx2.57143.
\]

With 2 degrees of freedom, \(p\approx0.27645\).

```r
counts <- c(60L, 45L, 45L)
reference <- c(.40, .35, .25)
stats::chisq.test(counts, p = reference)
```

**Results narrative (synthetic):** “The invented category counts were 60, 45 and 45. Against prespecified probabilities 0.40, 0.35 and 0.25, the Pearson chi-square statistic was 2.57 (df=2; p=0.276). This test does not identify equivalence to the reference distribution.”

**Critical issue:** if reference probabilities were *estimated from these same observations*, the naive degrees of freedom are inappropriate.

## 6. Next-stage interpretation checks for all method families

| Method family | Primary quantity | Minimum interpretation/validation work |
| --- | --- | --- |
| Rank-sum / signed-rank / Kruskal–Wallis | Relative ranks/distributions | Explicitly distinguish shift assumptions from median differences; assess ties |
| McNemar | Paired discordance | Report both off-diagonal counts; use exact alternatives for sparse pairs |
| 2×2 and R×C contingency analysis | Proportions/association | Give raw counts, denominators and prespecified effect measure |
| Linear regression | Mean outcome per predictor-unit change | Units, CI, functional form, residual/influence plots |
| Logistic regression | Adjusted odds ratio | Coding, event count, separation, coefficient CI; not automatically risk |
| Mixed/GEE | Correlation-aware mean/association | Cluster IDs, time and missingness; variance estimator |
| Poisson/NB regression | Events per exposure ratio | Explicit log-offset, positive exposure, dispersion and zero inflation |
| Kaplan–Meier/log-rank/Cox | Event-free survival, survival comparison, hazard ratio | Time origin, censoring, PH and competing risks where appropriate |
| Complex survey | Weighted population estimate | Weights, PSUs, strata and target population; do not treat rows as SRS |
| Gene-level DE | Log2 fold change and FDR | Replicates, normalization, design/contrast, batch, multiple-testing family |

### Release gates

**Numerical reference level:** Independent synthetic calculations confirmed externally for the five examples above with SciPy 1.17.0. **R replay level:** pending actual R execution of [companion checks](../tests/test_breast_cancer_reference_values.R) and the [broader lab suite](../tests/test_breast_cancer_test_atlas.R). **Biomedical validity level:** not established by synthetic calculations. Each analysis of real data requires fresh G2/G3/G5/G7/G8 evidence.
