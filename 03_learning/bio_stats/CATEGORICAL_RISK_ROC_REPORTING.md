# Categorical outcomes, effect measures, and ROC reporting

This chapter follows the breast-cancer research narrative from a two-by-two table through comparative effects to diagnostic discrimination. It synthesizes standard reporting practice consistent with Bernard Rosner, *Fundamentals of Biostatistics*; verify section/page references against the edition assigned in class. Worked counts below are **synthetic teaching data**, not observed patients.

## 1. Contingency tables

**Research question:** Is biomarker-positive status associated with pathological complete response (pCR)? Define each patient as one independent unit, the assessment window, positive biomarker threshold, and whether response is observed.

| Biomarker | pCR yes | pCR no | Total | Response risk |
| --- | ---: | ---: | ---: | ---: |
| Positive | 36 | 44 | 80 | 36/80 = 45.0% |
| Negative | 20 | 60 | 80 | 20/80 = 25.0% |
| Total | 56 | 104 | 160 | 56/160 = 35.0% |

Report counts **and row percentages** with the row denominator. State exclusions and missing outcomes separately; do not silently include them as failures. For Pearson's independence test, calculate expected counts E_ij = (row total × column total)/N, and X² = Σ(O_ij−E_ij)²/E_ij with (r−1)(c−1) degrees of freedom. Here expected counts are 28 and 52 in each row; Pearson X² = 7.03, df = 1, p ≈ 0.008. The 2×2 Pearson test here is uncorrected; R's `chisq.test()` applies Yates correction by default for 2×2 tables. Document the correction policy.

Inspect expected frequencies and sparse/zero cells before choosing asymptotic Pearson inference. Fisher's exact test is an option for sparse independent tables; it conditions on margins. For paired binary observations use McNemar's test instead. Report the actual test and any correction, not just “significant.”

**Example results:** “Among 160 patients in the synthetic cohort, pCR occurred in 36/80 (45.0%) biomarker-positive patients and 20/80 (25.0%) biomarker-negative patients. The uncorrected Pearson chi-square test indicated a difference in response distribution (χ²[1] = 7.03, p = 0.008).”

## 2. Risk ratios, odds ratios, and absolute differences

Let a = 36 (positive/responded), b = 44 (positive/did not respond), c = 20 (negative/responded), d = 60 (negative/did not respond). The exposed/reference direction must remain fixed across tables, equations and prose.

- Risk in positive group = a/(a+b) = 0.45; risk in negative group = c/(c+d) = 0.25.
- **Risk difference** = 0.45 − 0.25 = **0.20**, or 20 percentage points.
- **Risk ratio** = [a/(a+b)]/[c/(c+d)] = **1.80**.
- **Odds ratio** = (a/b)/(c/d) = ad/bc = **2.45**. Odds and risks are different quantities; OR 2.45 does not mean 2.45 times the probability.

For independent binomial samples, a conventional large-sample 95% CI for RR uses log(RR) ± 1.96√(1/a − 1/(a+b) + 1/c − 1/(c+d)), then exponentiates. For OR use log(OR) ± 1.96√(1/a+1/b+1/c+1/d). These Wald intervals require suitable cell counts; zero/sparse cells warrant a documented alternative. For the example, approximate 95% CIs are **RR 1.14–2.83** and **OR 1.26–4.78**. For RD, a simple Wald CI is approximately **0.06–0.34**; prefer a justified score/Newcombe method for publication-grade difference intervals.

**Example results:** “Response risk was 45.0% versus 25.0% (risk difference 20 percentage points); the risk ratio was 1.80 (95% CI 1.14–2.83) and the odds ratio was 2.45 (95% CI 1.26–4.78).”

**Design rule:** A cohort or randomized trial with valid denominators can estimate risks. In a case-control study sampled by outcome, sample case fractions generally cannot estimate population risks; report an odds ratio and its design-appropriate interpretation. An adjusted logistic regression coefficient exponentiates to an adjusted **odds ratio**, not an adjusted risk ratio. State covariates and reference levels for adjusted results. RR/OR for treatment arms are not interchangeable with diagnostic sensitivity/specificity.

## 3. Classification, ROC curves, and AUC

A 2×2 *classification* table has **actual outcome** as columns and **predicted positive/negative** as rows, with explicit event-positive class. Define TP, FP, FN and TN before calculating:

- Sensitivity = TP/(TP+FN); specificity = TN/(TN+FP).
- Positive predictive value = TP/(TP+FP); negative predictive value = TN/(TN+FN).
- False-positive rate = 1 − specificity.
- ROC plots sensitivity against false-positive rate across score thresholds. AUC summarizes ranking discrimination; 0.5 corresponds to chance-level ranking and 1.0 to perfect discrimination for the evaluated population.

For a **separate synthetic threshold example**, TP = 30, FN = 20, FP = 15, TN = 35 gives sensitivity = 60%, specificity = 70%, PPV = 66.7%, NPV = 63.6%. These are threshold-specific metrics, **not** an ROC curve or AUC. AUC requires continuous/ordinal scores across patients and cannot be reconstructed from one confusion matrix.

Report the positive outcome definition, score direction, threshold and how it was selected, cohort/sample counts, missing scores, held-out versus training evaluation, sensitivity and specificity with uncertainty, AUC with 95% CI and CI method, and whether calibration was assessed. For patient-level data with multiple specimens, split by patient to avoid leakage. If threshold optimization occurred, perform it within development data; evaluate once on held-out data. ROC/AUC discrimination does not measure calibration or clinical benefit.

**Results template:** “On the prespecified held-out patient set (N = [N], [events] pCR events), the [model/biomarker] yielded an AUC of [estimate] (95% CI [lower–upper], [method]). At the development-selected threshold of [value], sensitivity was [x]% ([TP]/[TP+FN]) and specificity was [y]% ([TN]/[TN+FP]).”

## 4. Reproducible R example

```r
# ================================================================
# 01 | INDEPENDENT TWO-BY-TWO TABLE
# ================================================================
tab <- matrix(c(36, 44, 20, 60), nrow = 2, byrow = TRUE,
              dimnames = list(biomarker = c("Positive", "Negative"),
                              pcr = c("Yes", "No")))
addmargins(tab)
prop.table(tab, margin = 1)
stats::chisq.test(tab, correct = FALSE)
stats::fisher.test(tab)

# ================================================================
# 02 | RISKS AND EFFECT MEASURES
# ================================================================
a <- tab["Positive", "Yes"]; b <- tab["Positive", "No"]
c <- tab["Negative", "Yes"]; d <- tab["Negative", "No"]
p1 <- a / (a + b); p0 <- c / (c + d)
rr <- p1 / p0
or <- (a * d) / (b * c)
rd <- p1 - p0
rr_ci <- exp(log(rr) + c(-1, 1) * qnorm(.975) *
               sqrt(1/a - 1/(a+b) + 1/c - 1/(c+d)))
or_ci <- exp(log(or) + c(-1, 1) * qnorm(.975) *
               sqrt(1/a + 1/b + 1/c + 1/d))
data.frame(risk_positive = p1, risk_negative = p0,
           risk_difference = rd, risk_ratio = rr,
           rr_lower = rr_ci[1], rr_upper = rr_ci[2],
           odds_ratio = or, or_lower = or_ci[1], or_upper = or_ci[2])

# ================================================================
# 03 | THRESHOLD CLASSIFICATION EXAMPLE
# ================================================================
tp <- 30; fn <- 20; fp <- 15; tn <- 35
c(sensitivity = tp/(tp+fn), specificity = tn/(tn+fp),
  ppv = tp/(tp+fp), npv = tn/(tn+fn))

# ROC requires held-out patient-level scores and outcomes:
# roc_obj <- pROC::roc(response = heldout$pcr,
#                     predictor = heldout$score,
#                     levels = c("No", "Yes"), direction = "<")
# pROC::auc(roc_obj)
# pROC::ci.auc(roc_obj)
```

## 5. Reporting and verification checklist

1. Specify study design, unit of analysis, outcome definition, reference group, time window and missingness.
2. Show raw cell counts with denominators and correctly oriented percentages.
3. Match independent versus paired tests; inspect expected counts and document continuity corrections.
4. Report effect sizes and confidence intervals, not p-values alone.
5. Separate risk, odds, rate, and classification measures.
6. For ROC, document patient-level validation, threshold selection, event prevalence and AUC uncertainty.
7. Give a short clinical interpretation immediately after each table or figure; avoid redundant boilerplate.

## References and further reading

- Rosner B. *Fundamentals of Biostatistics*. Refer to the assigned edition for exact chapter and page mapping.
- Kim H-Y. Statistical notes for clinical researchers: Chi-squared test and Fisher's exact test. *Restor Dent Endod*. 2017. https://doi.org/10.5395/rde.2017.42.2.152
- Fagerland MW, Lydersen S, Laake P. The McNemar test for binary matched-pairs data. *BMC Med Res Methodol*. 2013. https://doi.org/10.1186/1471-2288-13-91
- STARD 2015 diagnostic accuracy reporting: https://www.equator-network.org/reporting-guidelines/stard/
- TRIPOD prediction-model reporting: https://www.equator-network.org/reporting-guidelines/tripod-statement/
- R statistical procedures: https://stat.ethz.ch/R-manual/R-devel/library/stats/html/chisq.test.html and https://stat.ethz.ch/R-manual/R-devel/library/stats/html/fisher.test.html
- pROC package: https://xrobin.github.io/pROC/
