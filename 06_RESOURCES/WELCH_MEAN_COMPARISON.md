# Generic Welch independent-group comparison

Use \`06_RESOURCES/R/welch_mean_comparison.R\` to compare **two independent groups' numeric means** without coupling the helper to any particular study, population, variable name or file path.

## Why this method

The default is a two-sided **Welch t-test**. It estimates the mean of a named comparison group minus the mean of a named reference group and does **not** assume equal variances. An unadjusted mean comparison does not by itself establish causality or control for confounding. Report group means/SDs and the contrast with its confidence interval; do not interpret a small p-value as an effect-size measure.

**Study gates before use:** Identify the sampled unit, independence, any matched/repeated or clustered observations, sampling weights, selection mechanism, prespecified outcome/contrast and missing-data mechanism. Unique identifiers alone do not verify independence. For complex surveys, use design-aware methods instead. For paired or repeated data, this independent test is inappropriate. Small n, heavy skewness, influential values or severe outliers may warrant a sensitivity analysis or a different estimand.

## Base R analysis — invented data

All values below are synthetic. None are patient or coursework records.

\`\`\`r
source("06_RESOURCES/R/welch_mean_comparison.R")

sample_data <- data.frame(
  subject_id = sprintf("P%02d", 1:12),
  group = rep(c("Reference", "Comparison"), each = 6L),
  outcome = c(2, 3, 5, 7, 9, 10, 4, 6, 8, 11, 12, 17)
)

result <- welch_mean_comparison(
  data = sample_data,
  outcome = "outcome",
  group = "group",
  reference_level = "Reference",
  comparison_level = "Comparison",
  subject_id = "subject_id",
  alpha = 0.05
)

# All counts and statistics are retained in full precision.
result$group_summary
welch_mean_result_table(result)
cat(format_welch_mean_result(result), "\n")
\`\`\`

Output includes total and complete-case N; missing outcome, missing group and overlap counts; group-specific totals, means, sample SDs, quantiles and ranges; explicit comparison-minus-reference difference; Welch t statistic, Satterthwaite degrees of freedom, exact numeric p value, confidence interval and alpha-level decision. Percentages in \`group_summary\` are based on the count of records *with that group label*, not the full cohort. Missing group labels are counted separately.

Do **not** sort factor levels to set direction. The \`comparison_level\` argument explicitly controls the sign of the estimate, t statistic and CI. An optional unique \`subject_id\` checks row uniqueness but not the sampling design. Missing numeric outcomes and group labels are omitted only after their counts are recorded; no imputation is performed.

## Matching ggplot2 figure

\`\`\`r
# Optional, installed separately: ggplot2
figure <- plot_welch_mean_difference(
  result,
  outcome_label = "Synthetic measurement",
  unit = "arbitrary units"
)
print(figure)
\`\`\`

The horizontal blue point and interval are **the exact result object** used in the table; dashed vertical line shows the null difference of zero. Colors follow the Okabe–Ito convention: blue \`#0072B2\`, missing-data neutral \`#808080\`. The interval is a **confidence interval for the difference in means**, not a boxplot whisker or individual-group SD. Use ggplot2 for every figure in the same report; never substitute a separately rendered Matplotlib picture.

The test is implemented using \`stats::t.test(x = comparison_values, y = reference_values, var.equal = FALSE)\`. This agrees with [R's official \`t.test\` manual](https://search.r-project.org/R/refmans/stats/html/t.test.html). The method-selection context and source evidence are documented in [biomedical statistics decision guide](../../03_learning/biomedical-statistics-decision-guide.md) and [literature matrix](../Literature/BIOSTATISTICS_R_LITERATURE_2021_2026.md).

## Testing

Run from the repository root:

\`\`\`bash
Rscript --vanilla 06_RESOURCES/tests/test_welch_mean_comparison.R
\`\`\`

The test suite uses **invented** independent groups to check identical results against direct \`stats::t.test\` calls, the reversed contrast, shuffled records/factor levels, missingness accounting, invalid inputs and (when installed) ggplot2 object construction. \`.github/workflows/learning-case-validation.yml\` automatically iterates through \`06_RESOURCES/tests/test_*.R\` on pull requests touching R resources.

**Reproducibility:** Preserve R and ggplot2 versions and the applied analysis plan with the study report; no datasets are loaded on module import. Running code tests establishes software consistency, not scientific or clinical validity.
