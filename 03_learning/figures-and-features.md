# Figures and feature matrices

[Learning sections](README.md) · [Next: study design](probability-and-design.md)

## Start with the comparison and observation unit

A paired line connects two measurements from one person. A scatterplot shows the relationship between two measured variables. A histogram shows counts within bins; a density curve is a smoothed estimate whose appearance depends on bandwidth. An empirical cumulative curve shows the observed fraction at or below a value.

Boxplots summarize quantiles under a stated convention. Violin shapes depend on density estimation and may look convincing with little data. For small samples, retain individual observations when permitted, and distinguish the number of measurements from the number of independent people. Plot choice must expose the structure relevant to the question.

```r
source("03_learning/examples/research_case.R")
result <- analyse_case(make_case())
x <- result$model_data$marker_au
stopifnot(length(x) == 7L)
summary(x)
stats::ecdf(x)(median(x))
```

The deployed figure shows six complete paired trajectories, seven baseline observations, and model diagnostics. Axis labels state invented arbitrary units; none of the points is a real participant measurement.

## Preserve matrix orientation

```r
case <- make_case()
stopifnot(identical(dim(case$assay), c(4L, 8L)))
stopifnot(identical(colnames(case$assay), case$registry$person_id))
scaled <- scale_features(case$assay)
stopifnot(all(scaled$values["DemoConstant", ] == 0))
stopifnot(all(is.na(scaled$values["DemoMissing", ])))
```

Rows are four invented features; columns are eight synthetic people. Before attaching metadata, check IDs and order, not only dimensions. A transposed matrix may still produce a colored image while answering a different question.

For each variable feature, the case subtracts its observed row mean and divides by its observed sample standard deviation. The resulting row z-score is unitless and describes relative position within that feature. It is not a fold change, standardized clinical score or differential-expression result.

## Constant and unavailable features need policies

A constant feature has zero observed standard deviation. The fixture displays its observed entries at zero and records `constant_displayed_at_zero` in `feature_scaling.csv`. That is a display convention, not a mathematically defined z-score. A feature with fewer than two observed values remains missing and receives a separate status.

The heatmap uses a fixed scale from −2 to +2. White also represents missing cells in this small base-R display; read the feature status table to distinguish missing data from near-zero values. A production figure should use a visually distinct missing-data treatment where the graphics library supports it and state any clipping of values outside the scale.

## Captions should carry the interpretation contract

State what a point or line represents, counts of independent units, units, transformation, comparison direction, and what any interval means. A plot annotation must name its test and multiplicity family if inferential labels are present. The deployment supplies descriptive figures rather than automatic significance labels.

Inspect [specialist visualization guidance](../06_RESOURCES/SPECIALIST_VISUALIZATIONS.md) for paired, calibration, cell-level and uncertainty displays. Read the [breast cancer figure explanations](../06_RESOURCES/Genomics/FIGURES/README.md) for molecular context.

## Test figure functions and numerical summaries

The [extended checks](tests/test_mastery.R) export a PDF containing Anscombe's four datasets, then labeled histogram, density, ECDF, box and violin displays. The nearly equal slopes in Anscombe's examples conceal different point patterns; inspect the graphs alongside the summaries.

The [checked plotting helper](examples/practice_tools.R) returns total, eligible and excluded row counts and rejects nonnumeric inputs or missing unit labels. Use it to explain why a distribution panel and a two-variable association panel can have different denominators.

## Transfer exercise

Create a feature with one observed value and seven missing values. Predict its scaling status before running `scale_features()`. Explain why forcing a colored row would communicate more information than the data support.

References: [R graphics](https://cran.r-project.org/doc/manuals/r-release/R-intro.html), [empirical cumulative distribution](https://search.r-project.org/R/refmans/stats/html/ecdf.html), [density estimation](https://search.r-project.org/R/refmans/stats/html/density.html).
