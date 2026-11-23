# Categorical outcomes, effect measures, and ROC reporting

This chapter follows the breast-cancer research narrative from a two-by-two table through comparative effects to diagnostic discrimination. It synthesizes standard reporting practice consistent with Bernard Rosner, *Fundamentals of Biostatistics*; verify section/page references against the edition assigned in class. Worked counts below are **synthetic teaching data**, not observed patients.

For the shared structure of Methods, Results, tables, plots, precision, and report-type guidelines, see [Scientific statistical reporting standards](SCIENTIFIC_STATISTICAL_REPORTING_STANDARDS.md). The following worked example supplies the underlying 2×2 and ROC mechanics.

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

## 3A. Empirical ROC graph coding standard (Rosner-aligned)

**Source and scope.** Rosner, *Fundamentals of Biostatistics*, 8th ed., section 3.9 and Figure 3.7 (printed p. 63) establishes the threshold-coordinate geometry: x = 1 - specificity (false-positive rate) and y = sensitivity (true-positive rate). It does not prescribe R software syntax. The implementation rules below follow the official [pROC ROC documentation](https://search.r-project.org/CRAN/refmans/pROC/help/roc_.html), [plot documentation](https://cran.r-project.org/web/packages/pROC/refman/pROC.html), [axis FAQ](https://cran.r-project.org/web/packages/pROC/vignettes/FAQ.html), and [STARD 2015 diagnostic-accuracy reporting guidance](https://pmc.ncbi.nlm.nih.gov/articles/PMC5128957/). No copyrighted figure is copied.

### Coding and reporting requirements

1. **Evaluation unit and population:** one independent patient per row, or an explicitly justified clustered design. Report analyzed N, case n, control n, missing scores/outcomes, marker units, reference-standard definition and whether the data are development, internal validation, held-out, external or synthetic teaching observations.
2. **Explicit score semantics:** declare case/control levels and biomarker direction before the model or plot. With pROC, direction = "<" means *higher scores indicate cases*; direction = ">" means *lower scores indicate cases*. The default direction = "auto" should not be used for resampling or validation because it can choose the favorable orientation after seeing outcomes.
3. **Empirical ROC display:** the graph shows sensitivity versus **1 - specificity**, from 0 to 1 on each axis. Use a square plotting region, legible labels and a dashed upward 45-degree no-discrimination diagonal. Plot empirical thresholds without aesthetic smoothing unless smoothing is a separately specified statistical procedure. Preserve tied scores and both endpoints. Do not describe the curve as calibration or the AUC as classification accuracy at one cutoff.
4. **The pROC axis trap:** legacy.axes = TRUE relabels the horizontal ticks to display *1 - specificity* but DOES NOT transform the underlying x coordinates; the x position for an additional point drawn over pROC::plot.roc() is still **specificity**. In a completely custom false-positive-rate plot, the x coordinate instead must be **1 - specificity** for every curve vertex, point, diagonal and tick. Never mix these two systems.
5. **Precision and denominators:** report AUC, 95% CI and its method, case/control n and the evaluation partition. DeLong CI is a conventional option for independent case/control observations; repeated patients, clusters or complex resampling require a design-aware alternative. Do not label an arbitrary band around a curve as a 95% confidence band.
6. **Threshold origin:** a prespecified clinical cutoff and a score-derived cutoff are different procedures. For a requested target (for example 90% sensitivity), choose the closest **attainable empirical** sensitivity; use a stated tie-breaker such as highest specificity, and retain the unrounded threshold in calculations. In pROC, print.thres = TRUE defaults to the package's notion of a "best" threshold; it is NOT a target-sensitivity selector.
7. **Independent arithmetic audit:** for any marked cutoff, report the predicted-positive rule, TP, FP, FN and TN; recompute sensitivity = TP/(TP+FN) and specificity = TN/(TN+FP). Confirm these equal the ROC coordinates, not just the rounded displayed values. The highlighted point represents one operating rule and does not replace the full AUC.
8. **Prediction validity:** choose any optimized cutoff using development data; assess it on held-out/external patients when claiming predictive performance. Selecting and assessing a threshold in the same sample is an *exploratory teaching calculation*, not an independently validated clinical decision rule.
9. **Multiple markers:** paired measurements on the same patients require a paired test when formally comparing AUCs; overlap of marginal confidence intervals is not an AUC-difference test. Declare the comparison family and multiplicity policy. Use a consistent direction, palette, size and axis convention across panels; disclose any unit/score transformations.

**Relation to the existing helper:** [biostat_graph_roc()](../../06_RESOURCES/R/biostat_graphs.R) implements an original synthetic-safe ggplot with independently matched tied-rank and trapezoidal AUC and fixed 0-1 axes. Its present interface assumes *higher score = positive* and does not compute DeLong CI or show a selected cutoff. For lower-is-case biomarkers, uncertainty reporting or cutoff overlays, use the explicit pROC path below, or document any score reversal before calling that helper.

### Reproducible R implementation: original synthetic ROC and cutoff annotation

The demonstration data below are invented and unrelated to clinical observations. Selecting a cutoff on these same observations is illustrative, not independent validation.

~~~r
# ================================================================
# 01 | DECLARE THE CASE CLASS AND MARKER DIRECTION
# ================================================================
if (!requireNamespace("pROC", quietly = TRUE)) {
  stop("Install the pROC package before running this example.")
}
set.seed(712)
teaching <- data.frame(
  status = factor(c(rep("Control", 40L), rep("Case", 30L)),
                  levels = c("Control", "Case")),
  marker = c(stats::rnorm(40L, mean = 0, sd = 1),
             stats::rnorm(30L, mean = 1.2, sd = 1))
)
stopifnot(!anyNA(teaching), all(is.finite(teaching$marker)),
          all(table(teaching$status) > 0L))

roc_obj <- pROC::roc(
  response = teaching$status, predictor = teaching$marker,
  levels = c("Control", "Case"), direction = "<",
  percent = FALSE, quiet = TRUE
)
auc_value <- as.numeric(pROC::auc(roc_obj))
auc_ci <- as.numeric(pROC::ci.auc(
  roc_obj, method = "delong", conf.level = 0.95
))

# ================================================================
# 02 | CLOSEST ATTAINABLE SENSITIVITY, WITH TIE-BREAKER
# ================================================================
coordinates <- data.frame(
  threshold = as.numeric(roc_obj$thresholds),
  sensitivity = as.numeric(roc_obj$sensitivities),
  specificity = as.numeric(roc_obj$specificities)
)
coordinates <- coordinates[is.finite(coordinates$threshold), ,
                           drop = FALSE]
candidate_order <- order(abs(coordinates$sensitivity - 0.90),
                         -coordinates$specificity, -coordinates$threshold)
selected <- coordinates[candidate_order[1L], , drop = FALSE]

predicted_case <- teaching$marker >= selected$threshold
actual_case <- teaching$status == "Case"
TP <- sum(predicted_case & actual_case)
FN <- sum(!predicted_case & actual_case)
FP <- sum(predicted_case & !actual_case)
TN <- sum(!predicted_case & !actual_case)
sensitivity <- TP / (TP + FN)
specificity <- TN / (TN + FP)
stopifnot(
  isTRUE(all.equal(sensitivity, selected$sensitivity, tolerance = 1e-12)),
  isTRUE(all.equal(specificity, selected$specificity, tolerance = 1e-12))
)

# ================================================================
# 03 | PACKAGE-CORRECT AXES, CHANCE LINE AND CUTOFF POINT
# ================================================================
draw_roc <- function(roc_obj, selected, auc_value, auc_ci) {
  old_par <- graphics::par(no.readonly = TRUE)
  on.exit(graphics::par(old_par), add = TRUE)
  graphics::par(pty = "s", xaxs = "i", yaxs = "i")

  pROC::plot.roc(
    roc_obj, legacy.axes = TRUE, identity = TRUE,
    col = "#0072B2", lwd = 2,
    identity.col = "#777777", identity.lty = 2,
    xlim = c(1, 0), ylim = c(0, 1), asp = 1,
    xlab = "1 - Specificity (false-positive rate)",
    ylab = "Sensitivity (true-positive rate)",
    main = "Empirical ROC: synthetic teaching scores"
  )
  # Under pROC legacy axes, underlying x remains SPECIFICITY.
  graphics::points(selected$specificity, selected$sensitivity,
                   pch = 21, bg = "#D55E00", col = "#000000", cex = 1.3)
  graphics::legend(
    "bottomright", bty = "n", cex = 0.72,
    legend = sprintf("AUC %.3f (DeLong 95%% CI %.3f-%.3f)",
                     auc_value, auc_ci[1L], auc_ci[3L])
  )
}
draw_roc(roc_obj, selected, auc_value, auc_ci)

data.frame(
  case_n = sum(actual_case), control_n = sum(!actual_case),
  AUC = auc_value, CI_lower = auc_ci[1L], CI_upper = auc_ci[3L],
  threshold = selected$threshold, TP = TP, FN = FN, FP = FP, TN = TN,
  sensitivity = sensitivity, specificity = specificity,
  false_positive_rate = 1 - specificity
)
~~~

For a **lower-is-case** biomarker, change the pROC call to direction = ">" and calculate predicted_case using **marker <= selected threshold**; do not relabel an untransformed concentration as its negative. The highlighted pROC point still uses specificity as its internal x coordinate.

### Figure acceptance gates

- **Data:** two declared outcome classes, one evaluation unit, counts and missingness, fixed score direction and dataset partition.
- **Geometry:** visible (0,0) and (1,1), square axes from 0 to 1, correctly rising no-discrimination line; no reversed false-positive-rate labels.
- **Evidence:** the full unsmoothed empirical ROC; numerical AUC and CI method; explicit exploratory/prespecified cutoff provenance; point at the independent 2 x 2 sensitivity/specificity coordinates.
- **Presentation:** final PDF/HTML rendering inspected for clipped axes, cropped titles, overlapping legend/annotation, plot dimensions and correct symbols. A source-only check or successful knit is not visual acceptance.

**Verification status of this new example:** authored and code-reviewed from the documented pROC API; R execution, knitting and figure-image inspection have **not** been performed in this change.

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
