# Quantile and Q-Q plot reporting: evidence-linked best practices

Status: source-reviewed guidance, 2026-11-18. This is a reusable reporting contract, **not** evidence that a particular report was re-knitted or visually validated.

## Scope and distinctions

1. **Normal Q-Q plot:** sample/standardized-model-residual quantiles on Y versus theoretical normal quantiles on X. Assess approximate normality and the *shape* of departures; it does not prove normality.
2. **Two-sample Q-Q plot:** empirical quantiles of two independent distributions; labels and sample-size matching/interpolation require documentation. It is not a normality test.
3. **Quantile summary / boxplot:** median/Q1/Q3/whiskers reflect descriptive distribution. Boxplot whiskers are not confidence intervals. This is not interchangeable with a Q-Q plot.
4. **Quantile regression / quantile-residual graphics:** different estimands/diagnostics; do not call these normal Q-Q plots.

## Normal Q-Q figure acceptance contract (G2 / G5 / G7 / G8)

- Describe **unit** (independent participant, not visits), outcome and units, observed n/N, missing n, study arm/panel, and whether raw, standardized, studentized, or transformed residuals.
- X = theoretical **normal quantiles** (dimensionless); Y = ordered observed quantiles in outcome units, or standardized residual quantiles (dimensionless). Never swap these silently.
- For ggplot2 use `aes(sample = standardized_residual)`, `stat_qq(distribution = stats::qnorm)` and `stat_qq_line(distribution = stats::qnorm, line.p = c(.25,.75))`. Document the line as a *quartile-fitted reference*, not a mandatory 45-degree identity line. The default reference-line quantile calculations need not match Rosner-style type-2 descriptive quartiles; specify or implement the intended calculation explicitly when claiming type-2 alignment.
- Compare systematic curvature, central departures, short/long tails, skew, extreme observations, and stepwise behavior. **Tied/discrete/threshold-truncated observations cause steps**, especially for integer PHQ-9 scores; do not automatically label the steps as contamination or outliers.
- Show arm-specific outcome distributions **and** fitted-model residual diagnostics for ANOVA. Do not equate outcome normality tests with the model error assumption; variance diagnostics remain separate.
- For facets compare like with like: consistent quantile axes where defensible, readable panel headings, arm-specific n, adequate physical figure width, separate captions, and consistent Okabe-Ito colors and scientific theme.
- A Shapiro-Wilk p-value tests exact normality and may be sensitive to modest departures at large n. Report the actual W and p, but never make one p-value an automatic model-switch gate; assess assumptions, design, residual plots and inferential robustness.
- Optional uncertainty envelope: declare **pointwise vs simultaneous**, confidence level, distribution/simulation assumptions, resampling unit, seed, number of simulations, and whether model coefficients are refitted. A generic ribbon is **not** a valid Q-Q confidence envelope. Do not add one by default without a calibrated implementation.
- For **all coursework**, use **R `stats::quantile(type = 2)`** for descriptive Q1 and Q3, and consistently use type-2 hinges/whiskers in boxplots. This is the coursework standard, not an optional case-by-case Rosner setting. R defaults to type 7; explicitly label this distinction and never silently mix computed type-2 table quartiles with automatically determined ggplot2 boxplot hinges. Implement type-2 box hinges explicitly where consistency is required. The normal Q-Q plotting positions and its reference-line quartile algorithm are separate implementation choices; `line.p = c(.25,.75)` alone does not set quantile type to 2.
- Record plot source, random seed if any, R/ggplot2 versions, explicit complete-case criteria, and rendered figure QA at the target PDF page width. No jitter or subsampling on quantile points without an explicit defensible reason.
- Distinguish a successful R source review from **G7 page-image acceptance** and **G8 clean computational replay**.

## Recommended report interpretation

> The normal Q-Q plot of standardized ANOVA residuals showed [observed central pattern] and [observed tail behavior]. Integer-valued, bounded scores generated repeated ordered residual values. The arm-specific distributions, residual diagnostics, variance assessment, and Shapiro-Wilk result (W = [actual], p = [actual]) were considered jointly. Departure from exact normality alone does not establish that the ANOVA is invalid.

Only fill placeholders from actual executed results and visual inspection. Never invent envelope coverage, a Shapiro-Wilk result, or diagnostic interpretation.

## Minimal ggplot2 pattern

```r
stopifnot(is.numeric(d$std_residual),
          all(is.finite(d$std_residual)), nrow(d) >= 3L)
ggplot2::ggplot(d, ggplot2::aes(sample = std_residual)) +
  ggplot2::stat_qq(distribution = stats::qnorm,
                   colour = "#0072B2", alpha = 0.55, size = 0.8) +
  ggplot2::stat_qq_line(distribution = stats::qnorm,
                        line.p = c(0.25, 0.75),
                        colour = "#D55E00", linewidth = 0.7) +
  ggplot2::labs(
    title = "Standardized residual normal Q-Q",
    subtitle = sprintf("Independent observations: n = %d", nrow(d)),
    x = "Theoretical normal quantiles",
    y = "Standardized residual quantiles",
    caption = paste("Reference line fitted through first and third quartiles;",
                    "no uncertainty envelope shown.")) +
  theme_scientific()
```

Requires `06_RESOURCES/R/stats_plots.R` then `06_RESOURCES/R/scientific_palette.R` sourced from the Paul’s Notes root. For self-contained coursework Rmd, reproduce equivalent theme with provenance rather than a fragile external dependency.

## Evidence / primary documentation

- NIST/SEMATECH Engineering Statistics Handbook, *Normal Probability Plot*: https://www.itl.nist.gov/div898/handbook/eda/section3/normprpl.htm
- ggplot2, *A quantile-quantile plot*: https://ggplot2.tidyverse.org/reference/geom_qq.html
- R stats, *Quantile-Quantile Plots*: https://stat.ethz.ch/R-manual/R-devel/library/stats/html/qqnorm.html
- R stats, *Sample Quantiles*: https://stat.ethz.ch/R-manual/R-devel/library/stats/html/quantile.html
- car, *Quantile-Comparison Plot* (model-based simulation envelope): https://cran.r-project.org/web/packages/car/refman/car.html

## Coursework application

- RQ1: report W and p per arm and for standardized ANOVA residuals; annotate Q-Q quartile-line method and integer-score ties.
- RQ2: standardized baseline QOL residual normal Q-Q, with n, reference-line convention and no unwarranted identity-line claim.
- RQ4/RQ5: panel separately by change endpoint with residual type and independently complete participants; classical ANOVA QOL diagnostics are sensitivity checks, not Welch residuals.
- For every coursework descriptive table, use `quantile(..., type = 2)`; compute matching type-2 box hinges explicitly and document the plotting method. Review Q–Q reference lines separately and use type-2 sample quartiles when quartile-fitted lines are specified. Keep mathematical tests, inference and raw data unchanged; verify final knit and all plot extents before claiming G7/G8 complete.
