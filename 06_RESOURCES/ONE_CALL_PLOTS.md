# One-call statistical plots — R
The examples use 48 independently simulated adult participants from `make_teaching_cohort()`. Age is years; creatinine is mg/dL; albumin is g/dL. Recorded sex and site are fictional categories, and the programmed age association is not clinical evidence. Run blocks in order from the repository root. Optional file exports create or replace the named output; choose a deliberate destination.


Load these files **in order** from the repository root:

```r
source("06_RESOURCES/R/teaching_data.R")
health_data <- make_teaching_cohort()
source("06_RESOURCES/R/stats_plots.R")
source("06_RESOURCES/R/one_call_plots.R")
```

These functions run the test, build a ready-to-print `ggplot2` visualization, and put the full `htest` result in `attr(p, "statistical_test")`. No external plot-annotation package is required. The functions use **complete observations** and never infer pairing.

## Runnable synthetic examples

```r
# Linear best-fit line + confidence band + Pearson correlation p-value
p <- plot_test(health_data, "Age", "Creatinine", method="pearson", fit=TRUE)
p <- p + ggplot2::labs(x = "Age (years)", y = "Creatinine (mg/dL)")
print(p)
attr(p, "statistical_test")

# Independent groups: Wilcoxon rank-sum p-value
p <- plot_wilcox(health_data, "Creatinine", "Sex")
p <- p + ggplot2::labs(y = "Creatinine (mg/dL)")
print(p)

# Repeated measurements: subject IDs are required
# p <- plot_wilcox(long, "measurement", "time",
#                      paired=TRUE, id="Participant")

# Three or more groups: omnibus Kruskal-Wallis and BH pairwise comparisons
p <- plot_multigroup(health_data,"Creatinine","Site",p_adjust="BH")
p <- p + ggplot2::labs(y = "Creatinine (mg/dL)")
print(p)
attr(p, "posthoc")$p.value

# Gene abundance: two groups only; use independently prepared log2 CPM
# p <- plot_gene_wilcox(gene_long, "ESR1", "Subtype",
#                           value="Expression", scale="log2 CPM")
save_plot(p, "figures/group_comparison.pdf", width=7, height=5)
```

## Interpretation and safeguards

- `plot_test()`: Pearson or Spearman association p-value; its optional least-squares best-fit line and shaded **mean-response confidence band** are separate from the correlation test. The band is not a prediction interval or an edgeR confidence interval.
- `plot_wilcox()`: two-group unpaired rank-sum or paired signed-rank test. For paired data, subject IDs are matched, and only matched pairs are plotted.
- `plot_multigroup()`: Kruskal-Wallis omnibus p-value; inspect pairwise Wilcoxon adjusted p-values through `attr(p, "posthoc")`. Pairwise results are *not* automatically shown on the graph to prevent crowded or misleading marks.
- `plot_gene_wilcox()`: convenient single-gene descriptive comparison; exploratory Wilcoxon statistics cannot replace count-based edgeR inferential analysis. With many tested genes, explicitly control multiple testing.
- **P-values are not effect sizes.** Graphs must document biological group sizes, assay scale, study design, selection rules and adjustment family. These utilities are teaching helpers, not clinical decision support.

Tests: `Rscript --vanilla 06_RESOURCES/tests/test_one_call_plots.R`. Test execution depends on an R environment with ggplot2 installed.
