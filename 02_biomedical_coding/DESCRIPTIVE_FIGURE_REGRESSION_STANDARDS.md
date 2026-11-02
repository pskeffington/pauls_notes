# Biomedical descriptive figure regression standards

**Scope:** Reusable engineering guidance derived from operator-observed failures in a knitted R Markdown workflow. No screenshots, participant records, figures, or clinical dataset are stored here. These observations are **bug reports**, not verification that the associated code has passed automated tests.

## G2 — data and reporting contract

- Validate an observation's unit, ID uniqueness, data types, categorical levels and laboratory measurement units against a source dictionary.
- For every variable, report total N, observed n, missing n and missing percent. Categorical percentages must identify whether their denominator is total N or valid n; do not silently remove missing categories.
- Keep sample IDs out of mean/SD summaries. Use sample SD and base R quantile type 7 unless otherwise documented.
- Separate unweighted sample summaries from survey-weighted population estimates; NHANES-like field names do not establish a valid complex survey design.

## G7 — plotting acceptance rules

1. **Manual-scale keys must exactly match factor levels.** Named palette lookup such as `c(Female = pal["vermillion"])` may produce compound names (e.g. `Female.vermillion`), and ggplot2 then warns `No shared levels found between names(values) of the manual scale and the data's fill values`. Use `unname(pal["vermillion"])` or `group_colors(..., levels=...)` and explicitly test `identical(names(fill_values), levels(data$group))` when the intended order is exact.
2. **Legends outside data panels.** Prefer `legend.position="bottom"`, allocate figure height, allow caption wrapping and check that reference marks remain visible. Numeric estimates may belong in a caption/table rather than an opaque legend over observations.
3. **Plot statistics without misleading redundancy.** Histograms may show mean, median, quartiles and mean +/- 1 SD with distinct line types; explain that SD bounds are **not** confidence intervals. In boxplots, the center is median, edges are Q1/Q3, whiskers follow 1.5 x IQR and are **not** CIs. Add a mean diamond only if useful; do not also obscure the box with redundant quartile lines.
4. **Violin plots are estimated density.** Overlay an internal box and low-opacity raw points, preserve the independent observation unit, disclose displayed n and exclusions, and specify equal-width vs count-scaled violin semantics. `geom_violin(scale="width")` gives each group equal maximum width regardless of sample size.
5. **Transformations must be labeled and consistent.** For heavily skewed nonnegative biomarkers, `log1p(x)` is a possible display transform; mark the transformed axis. If the overlaid point represents the **arithmetic mean on the original scale**, compute `log1p(mean(raw_x))` for its transformed position—not `mean(log1p(raw_x))`. The latter is a different estimator. Report original-scale estimates in the table and disclose the point definition.
6. **Avoid silent data alteration.** Record counts excluded for missing group and missing measurement separately where useful; reject negative input before `log1p`. A visual transform does not justify deleting the tail. For transformation-heavy figures consider a raw-scale companion plot.
7. **Make knitted reports self-contained.** All intended code, tables, generated graphics and captions belong in one working Rmd when requested. `print(p)` for ggplots inside loops; verify PDF/HTML output dimensions. Keep warnings visible during development, never merely suppress scale mismatches.
8. **Use Paul's Notes official palette.** Prefer `06_RESOURCES/R/scientific_palette.R`: Okabe–Ito categorical assignments and scientific theme. Avoid arbitrary lightblue/lightgreen/steelblue. Test color-level mapping, not merely hex legality.

## Failure-mode fixtures

See `scripts/test_descriptive_figure_contracts.R` for **synthetic, non-clinical** regression checks:
- exact fill-factor name matching and prevention of compound-name palette regression;
- mean-on-original-scale marker identity under `log1p`;
- missing denominator and ID uniqueness checks;
- nonnegative transform gate;
- ggplot build without manual-scale mismatch warning where ggplot2 is installed.

**Verification status:** operator screenshots demonstrated legend overlap and palette warnings in a prior workflow. The attached synthetic checks must be executed in a suitable R environment and reported separately before claiming a green test gate. The original clinical/classroom dataset was not executed or uploaded.

## Review checklist

G2: schema, missingness, units and IDs pass; G7: legibility at knit dimensions, categorical scale keys, n/exclusions, correctly positioned annotations and transformation notes pass; G8: reproducible code and a documented run environment pass. Do not call a chart manuscript-ready solely because the plotting script evaluates.
