# Breast cancer statistics: distributions, uncertainty and power

[Foundations](BREAST_CANCER_STATISTICS_FOUNDATIONS.md) · [Method atlas](BREAST_CANCER_WORKED_TEST_ATLAS.md) · [Synthetic R lab](../examples/breast_cancer_distribution_lab.R) · [Checks](../tests/test_breast_cancer_distribution_lab.R)

**Scope.** Original Rosner-aligned, synthetic breast cancer teaching material. No patient records, TCGA results or clinical effectiveness claims. All biomarker scores are arbitrary units.

## Method map

| Family | Main question | Reference distribution | What to report |
| --- | --- | --- | --- |
| z | Mean versus known reference, genuinely known population sigma | Standard normal | Difference, SE, z, p, interval |
| One-sample Student t | Mean versus benchmark, unknown sigma | t with n−1 df | Mean difference and CI |
| Welch t | Two independent group means; variances not assumed equal | t with Welch-Satterthwaite df | Group n, mean difference, CI |
| Paired t | Same woman's pre/post score | t on matched differences | n pairs, after-minus-before, CI |
| Pearson chi-square | Association in categorical count table | Chi-square with model df | Cells, expected counts, test, effect |
| Ordinary ANOVA | Three or more independent means | F with k−1, N−k df | Group means, F, CI for planned contrasts |
| Welch ANOVA | Three or more means, heteroscedasticity | Adjusted F | Group means, omnibus and follow-up plan |
| Binomial | Number of successes in fixed eligible trials | Binomial | k/n, reference p, exact tail and interval |
| Poisson | Counts over person-time at a constant rate | Poisson | k, rate/exposure, lambda, tail or rate CI |
| Power | Probability of rejection under a specified alternative | Test-specific | Effect, alpha, allocation, n, target power |

## One-sample z and Student t

A hypothetical assay has known population SD 4 score units and a valid reference mean 10. In n=16 independent synthetic patients, sample mean is 12. The known-sigma statistic is z=(12−10)/(4/sqrt(16))=2 and the two-sided standard-normal p≈0.04550. If SD=4 was instead calculated from the 16 patients, use a t reference with an estimated SE, not the known-sigma z test.

For invented scores (8,10,10,12,12,14,14,16), n=8, mean=12, sample variance=48/7 and SE≈0.92582. The t critical value at df=7 and 95% confidence is 2.364624. Therefore the one-sample mean confidence interval is about **[9.8108,14.1892]** arbitrary units. This interval estimates uncertainty in the **population mean**, not the variability of all individual patients.

## Welch versus pooled Student and paired t

Independent hypothetical groups A=(8,9,10,11,12,13), B=(9,11,13,15,17,19) have means 10.5 and 14; variances 3.5 and 14. Welch A−B =−3.5 with t≈−2.04939, df≈7.35294 and 95% CI approximately [−7.4994,0.4994]. This interval includes zero but cannot demonstrate equality.

Pooled Student t assumes equal underlying variances. Welch permits unequal variances, but still requires an appropriate independence and mean-estimation model. If these were the *same* women measured twice, the correct basic comparison is paired change, not two independent-group t tests.

Eight synthetic within-person changes (−1,−1,−1,−3,−1,−1,−2,−3) give mean change −1.625 and 95% CI approximately [−2.391,−0.859]. Clinical causality requires design evidence beyond this test.

## Chi-square distribution and counts

Consider an invented 2×2 table: treatment A 30 responders/20 nonresponders; B 20/30. Every expected count under independence is 25. Pearson chi-square = sum((observed−expected)^2/expected)=4, with df=1, giving p≈0.04550. In R, set correct=FALSE to disable the default continuity correction in a 2×2 chi-square test. Counts must be independent; report row proportions and an effect measure with uncertainty. A chi-square test alone does not establish causal treatment benefit.

## F distribution and ANOVA

A=(8,10,12), B=(10,12,14), C=(12,14,16), with nine different participants. Group means are 10, 12, 14; grand mean 12. Between-group sum of squares=24, within-group sum of squares=24. Mean squares are 12 and 4; F=3 on (2,6) df; upper-tail p=0.125. Omnibus ANOVA asks whether all population means are equal, **not** which group differs. Welch ANOVA relaxes common variance. Predefine pairwise contrasts and compatible multiplicity control.

## Exact binomial and Poisson tails

**Binomial:** If 36/80 eligible independent hypothetical patients respond and a justified null probability is 0.35, P(X≥36)=P(X>35)≈0.04106885. This is not P(X=36) and does not prove a treatment effect without an appropriate comparator.

**Poisson:** An invented 40 events per 100,000 person-years across 20,000 person-years gives lambda=8. P(X≥10)=P(X>9)≈0.28337574. A count process assumes exposure and event structure; recurring events, nonconstant hazards and overdispersion can invalidate the simple model. In Poisson rate regression, include log(person-time) as an offset; exponentiated group coefficients are incidence rate ratios, not cumulative risks.

## Central limit theorem and standard error

For independent identically distributed observations with finite nonzero variance, a standardized sample mean approaches a normal distribution as n grows. This does **not** make raw breast cancer biomarkers normally distributed. For synthetic right-skewed exponential individual measurements with mean and SD=10, theoretical standard error of the sample mean is 10/sqrt(n): 4.472 at n=5 and 1.414 at n=50. Seeded simulation of repeated sample means is included in the R laboratory. There is no universal n=30 guarantee; independence, tails and other sampling conditions remain necessary.

## Hypothesis testing, power and precision

The null hypothesis describes the reference data-generating model. The p-value is a tail probability calculated under that model, **not** the chance the null is true. Alpha is the planned Type I error rate. Beta is Type II error at a *specified alternative*, and power=1−beta.

For a known-sigma, two-sided normal z test at alpha=0.05 and standardized mean shift delta*sqrt(n)/sigma=2, theoretical power is approximately **0.5160**. This is a mathematical illustration, not an adequate power analysis for a breast cancer study. Sample size planning needs meaningful effect, variance, attrition, design, allocation, sidedness and multiplicity.

## Required interpretation checklist

1. State outcome scale, measurement unit, person/specimen unit, groups, missing n, and enrollment denominator.
2. Identify the estimand, null, alternative, time origin where relevant, comparison direction, and independence/paired structure.
3. Show test statistic, degrees of freedom, p-value where relevant, effect in meaningful units, confidence interval, and sensitivity analyses.
4. Distinguish statistical significance from clinically meaningful evidence; not-significant never means equivalence.
5. Review multiple outcomes, correlated samples, missingness, exposure rates, censoring and FDR/adjustment requirements.

## Replay

R functions and numerical checks live in the [synthetic lab](../examples/breast_cancer_distribution_lab.R) and [test file](../tests/test_breast_cancer_distribution_lab.R). The files are prepared for Rscript execution; an unexecuted test is not validation evidence. The broader [26-method breast cancer atlas](BREAST_CANCER_WORKED_TEST_ATLAS.md) contains rank, regression, mixed model, survival, survey and omics extensions.
