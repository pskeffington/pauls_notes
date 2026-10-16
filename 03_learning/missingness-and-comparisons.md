# Missingness and comparisons

[Computing subjects](README.md) · [Related: models](models-and-uncertainty.md)

## Report the denominator attached to the question

The fixture contains eight people measured on two planned occasions. One baseline value and one followup value are unavailable, for different people. Each occasion therefore has seven observed measurements, while only six people have a complete pair.

A difference between the two available-case means uses partly different people. A mean of within-person differences uses complete pairs. They answer different questions even if the two numerical results happen to agree in a particular dataset.

```r
source("03_learning/examples/research_case.R")
case <- make_case()
result <- analyse_case(case)
stopifnot(identical(result$summary$n_total, c(8L, 8L)))
stopifnot(identical(result$summary$n_observed, c(7L, 7L)))
stopifnot(nrow(result$pairs) == 6L)
stopifnot(isTRUE(all.equal(mean(result$pairs$change_au), 1.5)))
```

The paired contrast is **followup minus baseline**, in invented arbitrary units. It uses people S01, S02, S04, S05, S06 and S07. Record both the eligible count and excluded IDs in an approved study workspace; public examples here use invented labels.

## Missingness belongs to variables and analyses

The registry has an unavailable questionnaire response for S02. That response is irrelevant to the baseline model's formula, so S02 remains eligible. Blanket removal of rows with any missing field would change this analysis without a formula-based reason.

`na.rm = TRUE` changes a numerical denominator. It does not document why a value was unavailable or make the observed subset representative. Distinguish missed visits, assay failure, invalid input and below-detection measurements when the source supports those categories. Unknown and negative responses must not be silently treated as equivalent.

```r
x <- c(0, 4, NA_real_)
stopifnot(sum(!is.na(x)) == 2L, mean(x, na.rm = TRUE) == 2)
```

The measured zero contributes to the denominator. Replacing the unavailable value with zero would produce a different quantity.

## Choose paired and independent comparisons deliberately

A paired comparison works on within-person differences. Independence is needed across people, not between the two values within one pair. A paired t procedure adds assumptions about the distribution of differences, especially in small samples. A Wilcoxon signed-rank procedure has its own assumptions, including symmetry for the usual location interpretation; it does not eliminate study-design concerns.

An independent rank-sum comparison assumes independent groups and concerns distributions or a model-dependent shift. It is not automatically a comparison of medians. Ties, zeros, small samples and software settings affect exact versus approximate calculations. Do not choose a test only after seeing which p-value is smallest.

The deployment reports descriptive paired arithmetic; it does not publish a p-value for the deterministic fixture. For a real study, specify the estimand, sampling process and analysis plan before estimating uncertainty.

## Transfer exercise

Set S01's followup value to missing in an in-memory copy. Predict five complete pairs and a mean change of 1.6 units, then run `analyse_case()` and inspect the output. Explain what cannot be concluded about missingness from this deliberate change.

References: [R missing-value behavior](https://search.r-project.org/R/refmans/base/html/NA.html), [paired and independent t procedures](https://search.r-project.org/R/refmans/stats/html/t.test.html), [rank-based procedures](https://search.r-project.org/R/refmans/stats/html/wilcox.test.html).
