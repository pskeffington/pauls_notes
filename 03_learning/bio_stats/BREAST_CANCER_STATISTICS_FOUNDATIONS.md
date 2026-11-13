# Breast cancer biostatistics: major foundations and methods

[Distribution mathematics and power](BREAST_CANCER_DISTRIBUTIONS_AND_POWER.md) · [Rosner-aligned test matrix](ROSNER_TEST_SELECTION_MATRIX.md) | [26 method breast cancer atlas](BREAST_CANCER_WORKED_TEST_ATLAS.md) | [Reference-value validation](BREAST_CANCER_NUMERICAL_VALIDATION.md) | [Foundations R lab](../examples/breast_cancer_foundations_lab.R)

**Scope.** Original biomedical teaching notes organized around Bernard Rosner, *Fundamentals of Biostatistics*, 8th edition. All participants, outcomes, scores and clinical scenarios in this chapter are **synthetic**. Measurements are arbitrary teaching units; do not claim these are actual Ki-67 values, TCGA-BRCA results, or treatment effects.

## Core curriculum: learn in this order

| Topic | Breast cancer question | Estimand / interpretation | Gate |
| --- | --- | --- | --- |
| 1. Measurement and study design | Is ER status binary, stage ordinal, tumor diameter continuous, or recurrence time censored? | Determine outcome, patient/sample ID, unit and denominator | Pairing, repeated specimens, consent |
| 2. Descriptive statistics | How spread out are baseline marker scores? | n, mean, median, sample SD, IQR | Missingness and units |
| 3. Probability rules and Bayes | What is probability of a positive test conditional on disease? | Conditional probability; sensitivity is not PPV | Base prevalence and selection |
| 4. Bernoulli and binomial | How many pathological responses among n independent patients? | Probability of exactly k or k-or-more | Fixed n, independent common p |
| 5. Normal and z scores | How unusual is a measurement in a justified reference distribution? | Standardized distance, normal model | Known population SD where required |
| 6. Sampling, SE and CLT | Why does the cohort sample mean fluctuate? | Distribution of sample means; SE scales with 1/sqrt(n) | Independence and finite variance |
| 7. Confidence intervals | Which mean differences remain compatible? | Estimator +/- critical value times SE | Coverage assumptions |
| 8. Hypothesis, error, power | What null and minimum important difference were prespecified? | Type I/II error, power, detectable effect | Avoid post hoc power claims |
| 9. One-sample z or t | Does a marker mean differ from a reference? | One mean vs population benchmark | Unknown SD calls for t, not z |
| 10. Pooled Student t | Do two independent means differ with supported equal-variance model? | Difference in group means | Equal variances, independent samples |
| 11. Welch two-sample t | Do two independent means differ without equal-variance requirement? | Difference in means; Welch df | Independence, outliers, units |
| 12. Paired t | Does marker change within the same woman? | Mean after-before difference | Match person IDs |
| 13. Ordinary one-way ANOVA | Are three or more independent group means equal? | Omnibus F test | Residual and common-variance assumptions |
| 14. Welch ANOVA | Are group means equal when variances may differ? | Heteroscedastic omnibus | Contrasts and multiplicity |
| 15. Rank/nonparametric | Are toxicity grades or response distributions different? | Wilcoxon, signed-rank, Kruskal–Wallis | Not automatically median contrasts |
| 16. Categorical inference | Does ER status associate with response? | Chi-square/Fisher, paired McNemar | Raw counts and independence |
| 17. Correlation and linear regression | Is age associated with continuous biomarker? | Correlation r / adjusted slope | Linear form, influence, confounding |
| 18. Logistic regression | Are biomarkers associated with binary response? | Adjusted odds ratio, not risk ratio | Separation and event counts |
| 19. Poisson distribution | How likely are >=k events given lambda? | Count-tail probability | Defined event process and time |
| 20. Poisson/NB regression | Are follow-up events different per person-year? | Incidence rate ratio with offset(log(exposure)) | Dispersion, zero counts, correlated events |
| 21. Mixed/GEE/survey | Are serial specimens or cluster samples correlated? | Correlation/design-aware estimates | IDs, weights, PSUs/strata |
| 22. Survival analysis | Does recurrence-free survival differ over time? | KM, log-rank, Cox hazard ratio | Time zero, censoring, PH |
| 23. Omics and multiplicity | Which genes differ between profiles? | Expression contrast and BH FDR | Biological replicates and batch |

## Worked 1 — mean, SD and standard error

Eight independent hypothetical women have biomarker scores 8, 10, 10, 12, 12, 14, 14, 16. The mean is 12 arbitrary score units. Sample variance is 48/7 = 6.85714; sample SD is about 2.619. Standard error of the mean is 2.619/sqrt(8), about 0.926. The **SD** describes person-level variation; **SE** describes precision of a sample mean under the sampling model. Report n=8, missing n=0 and the unit.

In R: use mean(x), median(x), var(x), sd(x), and sd(x)/sqrt(length(x)). The sample SD divides squared deviations by n-1.

## Worked 2 — central limit theorem

For independent identically distributed patient measurements with finite variance, the standardized **sample mean**, not raw individual biomarker values, approaches a normal distribution as n becomes large:

$$
\frac{\bar X_n-\mu}{\sigma/\sqrt{n}} \overset{d}{\longrightarrow} N(0,1).
$$

Consider a deliberately right-skewed invented biomarker with exponential distribution mean=10 and SD=10. For independent sample sets, theoretical SD of the *sample mean* is 10/sqrt(n): about 4.472 for n=5 and 1.414 for n=50. The raw observations stay right-skewed. A simulation of 5,000 repeated sample means per size demonstrates the convergence visually. There is no universal n=30 rule: skew, tails, dependence and finite-variance assumptions determine adequacy.

The CLT cannot repair nonrepresentative cohorts, correlated specimens, or informative missingness.

## Worked 3 — z versus Student versus Welch versus paired t

A one-sample **z test** requires a defensible known population SD sigma for its traditional reference model. With estimated sample SD s, use a one-sample **t** reference when its assumptions are appropriate.

For independent groups A = (8,9,10,11,12,13) and B = (9,11,13,15,17,19), mean A=10.5, mean B=14; sample variances 3.5 and 14. Welch estimates A-minus-B = -3.5, with

$$
t_W=\frac{\bar x_A-\bar x_B}{\sqrt{s_A^2/n_A+s_B^2/n_B}}=-2.04939.
$$

Its Satterthwaite degrees of freedom are approximately 7.353; the two-sided p-value is approximately 0.0777 and the 95% interval about -7.50 to 0.50 score units. This CI includes zero; it does **not** demonstrate equivalence or clinical irrelevance.

- **Pooled Student t:** independent groups *and* defensible common population variance.
- **Welch t:** independent groups, without common variance assumption; frequent practical default.
- **Paired t:** same women before/after; test the mean of *within-person differences*, not an independent two-group comparison.

For eight paired hypothetical changes (-1,-1,-1,-3,-1,-1,-2,-3), the mean after-minus-before is -1.625 units (95% CI approximately -2.391 to -0.859). This synthetic decrease cannot demonstrate treatment causation.

## Worked 4 — ordinary and Welch ANOVA

Three independent groups of invented biomarker scores:

| Group A | Group B | Group C |
| --- | --- | --- |
| 8 | 10 | 12 |
| 10 | 12 | 14 |
| 12 | 14 | 16 |

Group means are 10, 12, 14; grand mean 12. Between-group sum of squares = 24, within-group sum of squares = 24. With k=3 and N=9, between df=2 and within df=6.

$$
F=\frac{SS_\text{between}/(k-1)}{SS_\text{within}/(N-k)}
=\frac{24/2}{24/6}=3.
$$

The right-tail p-value for F(2,6) >= 3 is 0.125. ANOVA tests the **joint null that all group means are equal**; it does not identify a pair or a causal effect. **Welch ANOVA** relaxes equal group variances and has different denominator degrees of freedom. If a study needs pairwise contrasts, prespecify them and control multiplicity using an approach compatible with the omnibus model. Ordinary Tukey intervals should not be attached to Welch or Kruskal-Wallis output.

## Worked 5 — binomial versus Poisson

**Binomial:** fixed 80 independent eligible people, 36 with a recorded response, prespecified baseline p0=0.35. Observed response proportion is 45%. The upper-tail probability for 36 or more under the null is approximately 0.04107. This is NOT the point probability of exactly 36 and not evidence of treatment efficacy absent a defensible comparison.

$$
P(X\ge 36)=\sum_{k=36}^{80}{80\choose k}(0.35)^k(0.65)^{80-k}.
$$

**Poisson:** invented event intensity 40 events per 100,000 person-years across 20,000 person-years means expected lambda=8. Then P(X>=10)=1-P(X<=9) approximately 0.28338. This is a *count* probability under a homogeneous Poisson model, not an individual recurrence probability. A rate model with unequal follow-up uses the log(person-time) as offset; exp(group coefficient) is an incidence rate ratio. Assess independence, stable intensity and overdispersion; consider negative binomial when justified.

## Core decision and reporting rules

1. Name the outcome and unit before looking at a p-value; an integer-coded cancer stage is ordinal, not continuous.
2. Different people: independent groups; same women before/after: paired; multiple visits/cells per patient: mixed/GEE or appropriate correlation-aware method.
3. Two independent means: Welch is a sensible default; three-plus independent means: ANOVA family; rank methods test distributional questions, not automatically means or medians.
4. Fixed number of successes: binomial. Event counts over time: Poisson with exposure, or assessed alternatives. Time-to-first-event with censoring: survival analysis.
5. Report n observed and missing, parameter/effect, direction, units, CI, diagnostics and test definition. Do not translate p>0.05 into equality or p<0.05 into clinical relevance.
6. For observational breast cancer data, statistical association does not by itself demonstrate treatment benefit or biological causality.

## R exercises and validation

The [foundation R laboratory](../examples/breast_cancer_foundations_lab.R) contains fixed synthetic cases and a seed-controlled CLT simulation. Its [test suite](../tests/test_breast_cancer_foundations_lab.R) asserts mathematical identities and expected results. Execute from the repository root:

    Rscript --vanilla 03_learning/tests/test_breast_cancer_foundations_lab.R

R execution status must be recorded separately from independent analytical checks and clinical study validity. For complete method families beyond these foundations, continue into the [26-method worked atlas](BREAST_CANCER_WORKED_TEST_ATLAS.md).