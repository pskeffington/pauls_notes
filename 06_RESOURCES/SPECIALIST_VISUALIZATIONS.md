# Specialist biomedical visualizations: six manuscript-oriented R calls

**Author:** Paul Skeffington · **Prepared with OpenAI**  
[Resources](README.md) · [R modules](R/README.md) · [Scientific visualization gallery](SPECIALIST_VISUALIZATIONS.md) · [Literature evidence matrix](Literature/BIOSTAT_R_VISUALIZATION_EVIDENCE_MATRIX.md)

These six original functions extend existing ggplot2 and tidyverse-compatible conventions without copying published figures. They require explicit measurement units, informative captions, and preservation of independent-observation structure. Code examples below are **entirely synthetic**; none are clinical findings. Execute from the repository root with R and ggplot2 installed.

## Prepare the plotting modules

```r
source("06_RESOURCES/R/stats_plots.R")
source("06_RESOURCES/R/plot_annotations.R")
source("06_RESOURCES/R/scientific_palette.R")
source("06_RESOURCES/R/specialist_visuals.R")
```

Functions create a `ggplot` without writing files. To publish an audited PNG/PDF pair, call `save_figure(plot, "/path/outside/repo/stem")`. That helper uses the existing annotation checker and also writes sidecar manifests. For examples that write output, choose a deliberate output directory outside Git.

## 1. Paired clinical observations

Use participant ID, an explicit two-visit order, numeric measurement, and unit. Complete pairs alone contribute to the plot; the caption distinguishes complete from excluded subjects. Duplicate subject-by-visit rows or unexpected visit labels cause a hard failure.

```r
paired <- data.frame(
  Subject_ID = rep(sprintf("S%02d", 1:8), each = 2),
  Visit = rep(c("Baseline", "Month 6"), 8),
  Creatinine = c(0.9, 1.0, 1.2, 1.1, 0.8, 0.9, 1.1, 1.2,
                 1.0, 1.1, 0.9, 0.8, 1.3, 1.4, 1.0, NA_real_))
paired_plot <- plot_paired_comparison(
  paired, id = "Subject_ID", visit = "Visit",
  value = "Creatinine", visit_levels = c("Baseline", "Month 6"),
  unit = "mg/dL", paired_ci = "t", conf_level = .95
)
print(paired_plot)
attr(paired_plot, "design")  # denominator audit
attr(paired_plot, "paired_change")  # individual differences and paired t CI
```

**Interpretation:** Each segment connects two observations from the *same* participant, not two groups' unrelated means. No p-value or causal statement is created. [Weissgerber et al.](https://doi.org/10.1161/CIRCULATIONAHA.118.037777)

## 2. Prediction calibration

Plot externally computed, **out-of-sample** binary outcomes and event probabilities. Bin observed risk using fixed equal-width bins, inspect both risk and empirical event proportion, and show the identity reference. Event horizon and evaluation partition are mandatory. The function rejects the `training` partition label; the operator must still verify that the submitted predictions are genuinely out-of-sample.

```r
calibration_data <- data.frame(
  Event = as.numeric(seq_len(200) %% 3 == 0),
  PredictedRisk = (seq_len(200) - 0.5) / 200,
  Subject_ID = paste0("S", seq_len(200))
)
calibration_plot <- plot_calibration(
  calibration_data, outcome = "Event", risk = "PredictedRisk",
  horizon = "12 months", evaluation_partition = "test", bins = 5L,
  interval = "wilson", subject_id = "Subject_ID", conf_level = .95
)
print(calibration_plot)
attr(calibration_plot, "calibration")$tabulation
```

**Interpretation:** The identity reference is displayed with equal x/y probability scales. Black/gray dashed identity means perfect average agreement; blue points show observed event proportions within bins. Vertical bars use 95% Wilson binomial confidence intervals under independent subject outcomes; the function retains bin event counts and n. Binned calibration is not a smooth curve. For clinical model assessment include a flexible calibration curve and confidence band when feasible. This synthetic fixture is not a fitted prediction model. [Van Calster et al.](https://doi.org/10.1186/s12916-019-1466-7)

## 3. Single-cell embedding inspection

Provide already-computed coordinates, unique cell keys, biological sample keys, batch, and cell-type or subgroup labels. Color denotes categories, not a continuous scale. Faceting by batch helps identify technical structure. Explicit seed and transformation settings are *provenance labels*; the plot does not recompute the embedding.

```r
set.seed(711)
cells <- data.frame(
  Cell_ID = paste0("cell", 1:40),
  Sample_ID = rep(paste0("sample", 1:4), each = 10),
  Batch = rep(c("run1", "run2"), each = 20),
  Cell_Type = rep(c("T", "B"), 20),
  UMAP1 = rnorm(40),
  UMAP2 = rnorm(40)
)
embedding_plot <- plot_cell_embedding(
  cells, cell_id = "Cell_ID", sample_id = "Sample_ID",
  batch = "Batch", group = "Cell_Type",
  x = "UMAP1", y = "UMAP2",
  method = "UMAP", seed = 711L,
  settings = "precomputed coordinates; documented upstream model"
)
print(embedding_plot)
```

**Interpretation:** Coordinate units receive fixed geometric aspect ratio; batch facets do not re-estimate the embedding. Proximity in a two-dimensional embedding is not proof of biological distance, cluster identity, differential expression or cell independence. [Single-cell embedding study](https://doi.org/10.1038/s41467-024-45891-y)

## 4. Quantitative microscopy: cells nested within specimens

Use specimen, field and cell keys, biological group, numeric measurement and unit. Each specimen receives a single group. Plot all cell-level values as transparent context and overlay **specimen medians** as black diamonds. Reports distinguish independent specimens from cellular measurements.

```r
microscopy <- data.frame(
  Specimen_ID = rep(paste0("S", 1:4), each = 6),
  Field_ID = rep(rep(c("F1", "F2"), each = 3), 4),
  Cell_ID = rep(paste0("C", 1:3), 8),
  Treatment = rep(c("Control", "Control", "Treated", "Treated"), each = 6),
  Intensity = rep(c(10, 11, 12), 8)
)
micro_plot <- plot_microscopy(
  microscopy, specimen = "Specimen_ID", field = "Field_ID",
  cell = "Cell_ID", group = "Treatment",
  measurement = "Intensity", unit = "a.u."
)
print(micro_plot)
attr(micro_plot, "specimens")
```

**Interpretation:** Multiple cell measurements do not increase the count of independent biological replicates. This is descriptive; it does not fit a hierarchical model. [Quantitative microscopy](https://doi.org/10.1371/journal.pbio.3002167)

## 5. Large-n scientific distribution: full data + audited sampling

The violin summarizes *all* valid observations; a deterministic subset of raw observations is overlaid. Both observed extremes are always retained for each group. The function records original N, displayed n, retained extrema, and seed without mutating the caller's random-number generator state.

```r
large <- data.frame(
  Group = rep(c("A", "B", "C"), each = 200),
  Biomarker = rep(seq_len(200), 3) + rep(c(0, 250, 500), each = 200)
)
sampled_plot <- plot_sampled_distribution(
  large, value = "Biomarker", group = "Group",
  unit = "mg/L", max_points = 60L, seed = 711L
)
print(sampled_plot)
attr(sampled_plot, "sampling")$displayed
```

**Interpretation:** The density uses full observations; the points are not an independent sample drawn for inference. Extreme retention is deliberately biased, so the overlaid points must not be interpreted as representative. [Weissgerber et al.](https://doi.org/10.1371/journal.pbio.1002128)

## 6. Independent-unit estimates and uncertainty

A confidence interval is not a boxplot whisker or violin width. For descriptive group distributions, use the full-data violin, internal box and observations. For inferential uncertainty, plot the group estimator and its interval **separately**. The independent-unit ID must refer to independently sampled participants or specimens, not repeated cells from one specimen.

### Reproducible bootstrap example

```r
estimate_data <- data.frame(
  Subject_ID = paste0("S", seq_len(nrow(large))),
  Group = large$Group,
  Biomarker = large$Biomarker
)
estimate_plot <- plot_group_estimate_ci(
  estimate_data, id = "Subject_ID",
  value = "Biomarker", group = "Group", unit = "mg/L",
  estimand = "median", conf_level = .95,
  n_boot = 2000L, seed = 711L
)
print(estimate_plot)
attr(estimate_plot, "estimates")
```

The marker denotes group median and the vertical/horizontal bar is the 95% **percentile bootstrap CI** from 2,000 within-group resamples of independently sampled IDs. Specify the estimand, level, independent unit, number of draws and random seed. This is **not** an automatically valid CI when observations are clustered or longitudinal. Percentile intervals can perform poorly with small samples, strong skewness or highly discrete data; prefer sensitivity analyses and design-appropriate bootstrap or hierarchical models.

### Scientific interpretation by plot type

| Figure | Quantity that shows spread | Optional statistical uncertainty | Reviewer guardrail |
| --- | --- | --- | --- |
| Matched patient trajectories | Raw subject-specific trajectories | Paired mean-change t CI, if explicitly requested | Complete pairs, independence across subjects and approximate normality of within-pair differences |
| Risk calibration | Binned observed event proportions | Wilson binomial CI per risk bin, requiring unique subject IDs | Independent outcomes, bin counts, held-out predictions; binned points do not replace a flexible smoothed calibration curve |
| Single-cell embedding | Individual cell coordinates, batching and sample counts | None inferred from embeddings | No cluster confidence band or independent-cell inference |
| Microscopy | Cells and per-specimen medians | t CI for mean specimen medians, if 3 or more independent specimens per group | Biological specimens are the independent replicates, not image fields/cells |
| High-volume violin | KDE, internal median/IQR/whiskers and sampled observations | None on the violin; use companion group estimate plot | Raw dots are deliberately extrema-retaining and not representative |
| Group estimate plot | Independent-unit group estimate | Percentile bootstrap interval at stated confidence level | Correct resampling unit and independent-unit definition mandatory |

### Manuscript reporting checklist

A figure or its legend should provide exact independent-group sample sizes and denominators, numeric units, missingness, panel definition, data transformation, statistical estimator, uncertainty method/level, assumptions, seed, biological replicate definition, and any selection or exclusion. Avoid reporting statistical significance or clinical effects from synthetic data alone.

The internal box uses the full dataset: center = median, box = quartiles, whiskers extend to data within 1.5 × IQR. **The whiskers are not confidence intervals.** The points are a deterministic, extrema-preserving subset; both rules are documented. Original column/group case is preserved in printed labels.

Methodology: [error bars in experimental biology](https://pmc.ncbi.nlm.nih.gov/articles/PMC2064100/), [BMJ evaluation of clinical prediction models](https://www.bmj.com/content/384/bmj-2023-074820), [reproducible fluorescence microscopy methods](https://doi.org/10.1038/s41592-021-01156-w), and [estimation graphics](https://doi.org/10.1038/s41592-019-0470-3).

## Interactive Plotly companion for every figure

The **same six validated ggplot2 objects** are the source of truth for both manuscript figures (PNG and vector PDF) and interactive Plotly figures (local HTML). Plotly provides hover inspection, legend interactions where relevant, zoom/pan and browser image export. A browser rendering can differ from ggplot2's static geoms; verify critical interval geometry against the companion vector PDF. Do not interpret hover values as additional inference.

```r
source("06_RESOURCES/R/plotly_visuals.R")
interactive <- plotly_view(paired_plot)    # RStudio viewer / interactive browser
save_plotly(paired_plot, "/tmp/paired.html") # portable offline HTML + paired_files/
# Or convert and export all six plot objects after making them:
plots <- list(paired = paired_plot, calibration = calibration_plot,
              embedding = embedding_plot, microscopy = micro_plot,
              sampled = sampled_plot, estimates = estimate_plot)
for (name in names(plots)) {
  save_plotly(plots[[name]], file.path("/tmp", paste0(name, ".html")))
}
```

The installed R packages are `plotly` and `htmlwidgets` (from CRAN); the HTML export uses **local JavaScript dependencies** via `selfcontained = FALSE`, so always retain the adjacent `*_files` folder alongside each HTML. [Plotly's ggplot2 interoperability](https://plotly.com/ggplot2/getting-started/) and [htmlwidgets export contract](https://search.r-project.org/CRAN/refmans/htmlwidgets/html/saveWidget.html) provide upstream reference.

**Privacy release gate:** An interactive HTML includes underlying plot values (and may expose identifiers through hover/embedded data). The tests use synthetic demonstrations. Do not post participant-level, clinical, restricted or sensitive records without de-identification, release authorization and explicit verification of embedded HTML data. Static PDF/PNG files and Plotly HTML are separate outputs, not interchangeable evidence.

## Quality gates and release

| Gate | Requirement | How checked |
| --- | --- | --- |
| Q17 independent units | A valid specimen/group key; unique cell nesting and matched patient visits | `test_specialist_visuals.R` |
| Q18 embedding provenance | Explicit seed/settings, complete finite coordinates, unique cell identifiers | `test_specialist_visuals.R` |
| Q19 calibration admission | Held-out partition label, binary observed outcomes, finite risk in [0, 1], recorded horizon | `test_specialist_visuals.R`; operator audits prediction origin |
| Q20 sampling transparency | Fixed seed, retained extremes, N versus plotted n, preserved full distribution | `test_specialist_visuals.R` |
| Publication | All four plot labels, six raster/vector figure pairs, annotation sidecars | `save_figure()`; test suite and visual review |
| Interactive delivery | Plotly widgets with adjacent dependency folders; manual hover and zoom review | `plotly_view()`, `save_plotly()` and local export inspection |
| Privacy/security | No confidential datasets or identifiers embedded in released HTML | Manual embedded-data audit before publishing non-synthetic plots |

Run from the repository root:

```bash
Rscript --vanilla 06_RESOURCES/tests/test_specialist_visuals.R
python3 scripts/check_documentation.py
python3 scripts/check_book_learning.py
```

The **Learning case validation** workflow runs the retained R resource tests. It does not publish a figure gallery. Generate synthetic previews locally for visual review, keeping the output outside the repository:

```bash
SPECIALIST_FIGURE_DIR=/tmp/specialist-preview Rscript --vanilla 06_RESOURCES/tests/test_specialist_visuals.R
```

With the optional plotting packages installed, this test exports PNG, PDF and Plotly HTML examples. Retain each HTML dependency folder. Inspect clipping, legibility, captions, point visibility, contrast, palette meaning, and interactive behavior before sharing figures. Passing automated tests does not establish visual quality or clinical validity.

The full [literature matrix](Literature/BIOSTAT_R_VISUALIZATION_EVIDENCE_MATRIX.md) explains the methodology and limitations. Production clinical results still require separate provenance and inference authorization.
