# Annotated RNA-seq heatmaps: row z-scores and two-sided tails

[Genomics](README.md) · [Read scientific plots](../READING_PLOTS.md) · [R gene-visualization helpers](../R/gene_visuals.R) · [Breast cancer book, figures](BREAST_CANCER_60_GENE_COMPANION.md#chapter-9-reading-the-scientific-figures)

**Scope:** A reusable *exploratory visualization* workflow for an expression matrix of genes (rows) by specimens/samples (columns). The current worked vocabulary uses ESR1, PGR, FOXA1, GATA3, ERBB2, GRB7, MKI67, KRT5, KRT14 and EGFR, with tissue Type and recorded PAM50 Subtype. This is a **method and code pattern**, not a fitted TCGA result or validated classifier. Other cancer types need independently checked gene annotations and study design.

## First establish the input and the unit

1. Start with an explicitly defined, permitted expression matrix and documented sample identifiers. One column is **one specimen/sample**, not automatically one independent person. Resolve replicates, linked specimens, labels, missingness and any reuse of participants before inference.
2. For cross-sample visualization, use appropriately **library-size-normalized and transformed expression** (for example log2 CPM, DESeq2 VST or another specified assay-appropriate transformation). A log transform of raw counts does **not** correct library-size differences. Do not feed z-scores or log CPM to raw-count likelihoods in a differential-expression model.
3. Keep genes in rows, samples in columns, and match annotation rows to matrix columns **by a real sample identifier**, not just by row count. Check that identifiers are unique and the reordered metadata IDs exactly equal `colnames(hm_z)`. A visually plausible but misaligned annotation is an invalid result.
4. Predeclare which genes and samples were selected; describe batch, tissue mix, subtype source, exclusions and missing values. The recorded PAM50 label is external metadata, **not** recalculated from a handful of heatmap genes. “Missing” and “not applicable” should be distinguished when the source provides that distinction.

## What a row z-score means

For gene *g* and sample *s*, `z[g,s] = (x[g,s] - mean(x[g,])) / sd(x[g,])`, where the mean and sample SD are computed **across the eligible samples for that gene** on the chosen transformed-expression scale. This comparison is *within a gene*: red is relatively higher, blue is relatively lower, and white is near that gene's mean. It is **not** absolute abundance, differential expression, log-fold change, p-value or a standardized clinical score.

The color mapping below is blue `#2166AC` at −2, white `#FFFFFF` at 0, and red `#B2182B` at +2. Scores beyond ±2 receive saturated endpoint colors; the stored `hm_z` values are unchanged. Preserve an explicit missing-data color so an unavailable measurement is not confused with `z = 0`.

**Preprocessing note:** A zero-variance gene has no defined row z-score. Remove it with an explicit report or mark it unavailable; do not silently label its row `z = 0`. Likewise, exclude or document genes with insufficient observed specimens. For machine-learning evaluation, any fitted normalization, feature selection and scaling must obey train-only preprocessing rules.

## Side annotation: two-sided z-score tails

For each gene *g* at threshold 1:

| Side bar | Calculation | Meaning |
| --- | --- | --- |
| Blue, `Z < -1` | `100 * number(z[g,] < -1) / number(nonmissing z[g,])` | Percent of observed samples more than one row SD below the gene mean |
| Red, `Z > +1` | `100 * number(z[g,] > 1) / number(nonmissing z[g,])` | Percent of observed samples more than one row SD above the gene mean |

These are **two separate percentages**, not opposite ends of a 100% stacked bar: values between −1 and +1 belong to neither tail. The inequalities are strict (exactly ±1 is not counted). The denominator includes all nonmissing observations for that gene, **across every displayed tissue group**; it is not a subtype-specific rate. The helper rejects all-missing rows and nonfinite scaling artifacts rather than inventing percentages.

`row_z_tail_percentages()` is implemented and regression-tested using invented numbers in [gene_visuals.R](../R/gene_visuals.R). It accepts an **already row-standardized** matrix; it does not normalize raw sequencing counts or compute z-scores.

## ComplexHeatmap example using the current variable names

Prerequisites supplied by the calling analysis:

- `hm_z`: numeric row-z-score matrix with named genes and sample IDs; orientation **genes × samples**.
- `hm_type`: tissue-type vector in the exact order of `colnames(hm_z)`.
- `hm_meta$subtype`: external recorded PAM50 labels, aligned by sample ID; `hm_meta` has one row per column of `hm_z`.
- `type_col` and `sub_col`: **named** color vectors matching observed categories. Categories without an applicable subtype can be `NA`.

Run from the repository root. **Before using this block**, explicitly verify sample-ID alignment using the actual ID column in `hm_meta`; the dimensional assertions below do *not* substitute for that check.

~~~r
# Requires ComplexHeatmap and circlize; hm_z is already row-standardized.
source("06_RESOURCES/R/gene_visuals.R")

stopifnot(
  is.matrix(hm_z),
  ncol(hm_z) == length(hm_type),
  ncol(hm_z) == nrow(hm_meta)
)
# Required upstream: match/reorder hm_meta by sample ID, then verify equality.
# Example after identifying the true column:
# stopifnot(identical(colnames(hm_z), as.character(hm_meta[["Sample"]])))

z_pct <- row_z_tail_percentages(hm_z, threshold = 1)
stopifnot(identical(rownames(z_pct), rownames(hm_z)))

# Top: sample-level category annotations.
hm_ann <- ComplexHeatmap::HeatmapAnnotation(
  Type = hm_type,
  Subtype = hm_meta$subtype,
  col = list(
    Type = c(type_col, "Missing" = "#D9D9D9"),
    Subtype = sub_col
  ),
  na_col = "#D9D9D9"
)

# Right: two *beside* bars for each gene; not a stacked percentage.
hm_side <- ComplexHeatmap::rowAnnotation(
  "Z-score tails (%)" = ComplexHeatmap::anno_barplot(
    z_pct,
    beside = TRUE,
    gp = grid::gpar(fill = c("#2166AC", "#B2182B"), col = NA),
    border = FALSE,
    width = grid::unit(2.5, "cm"),
    axis_param = list(gp = grid::gpar(fontsize = 8))
  )
)

hm <- ComplexHeatmap::Heatmap(
  hm_z,
  name = "Row z-score",
  col = circlize::colorRamp2(
    c(-2, 0, 2),
    c("#2166AC", "#FFFFFF", "#B2182B")
  ),
  na_col = "#D9D9D9",
  top_annotation = hm_ann,
  right_annotation = hm_side,
  column_split = hm_type,
  column_title = NULL,
  cluster_column_slices = FALSE,
  cluster_columns = TRUE,
  cluster_rows = TRUE,
  clustering_distance_rows = "euclidean",
  clustering_distance_columns = "euclidean",
  clustering_method_rows = "complete",
  clustering_method_columns = "complete",
  show_column_names = FALSE,
  show_column_dend = FALSE,
  row_names_gp = grid::gpar(fontsize = 10),
  use_raster = FALSE
)

# Bar colors require their own legend: they encode *percentages*,
# whereas the heatmap's continuous legend encodes *z-score units*.
tail_legend <- ComplexHeatmap::Legend(
  title = "Z-score tails",
  at = c("Z < -1", "Z > +1"),
  legend_gp = grid::gpar(fill = c("#2166AC", "#B2182B")),
  title_gp = grid::gpar(fontsize = 10, fontface = "bold"),
  labels_gp = grid::gpar(fontsize = 9)
)

draw_gene_heatmap <- function() {
  invisible(ComplexHeatmap::draw(
    hm,
    merge_legends = TRUE,
    annotation_legend_list = list(tail_legend)
  ))
}

# Display once. The same draw function supplies *both* saved legends.
draw_gene_heatmap()

# Export outside the Git checkout; inspect both outputs at final size.
export_dir <- file.path("..", "pauls_notes_heatmap_exports")
dir.create(export_dir, recursive = TRUE, showWarnings = FALSE)

grDevices::pdf(file.path(export_dir, "gene_heatmap.pdf"),
               width = 14, height = 8)
draw_gene_heatmap()
invisible(grDevices::dev.off())

grDevices::png(file.path(export_dir, "gene_heatmap.png"),
               width = 2800, height = 1600, res = 200)
draw_gene_heatmap()
invisible(grDevices::dev.off())

stopifnot(all(file.exists(file.path(
  export_dir, c("gene_heatmap.pdf", "gene_heatmap.png")
))))
writeLines(capture.output(sessionInfo()),
           file.path(export_dir, "session_info.txt"))
~~~

**Why these choices?** `column_split = hm_type` preserves tissue-type regions; `cluster_column_slices = FALSE` avoids reordering those regions. Euclidean distance and complete linkage are *declared choices*, not biological truth; results may change with alternative distances, linkage, gene inclusion, normalization or sample composition. The tail bars summarize each gene across the full plotted cohort, while columns inside each tissue slice may be reordered by clustering.

### Visual interpretation and caption contract

> Annotated heatmap of selected RNA-expression features across eligible samples. Values are gene-wise z-scores computed on [name exact normalized/transformed expression input], with mean and SD calculated across [name eligible cohort]. Blue/white/red heatmap colors correspond to lower/near-mean/higher relative expression; colors saturate at ±2. Top tracks show recorded tissue type and externally assigned PAM50 subtype; grey indicates [missing or not applicable, as defined]. Columns are grouped by tissue type and clustered within groups; genes use Euclidean distance and complete linkage. Paired right-side bars indicate the percentages of observed samples with each gene's z-score < −1 (blue) or > +1 (red), excluding missing values from each denominator. The figure is descriptive, not a differential-expression test or classifier validation.

Do not invent the bracketed values. If the plot is of **raw-count-derived z-scores**, disclose that sequencing-depth differences may remain and treat its pattern as exploratory until an appropriate normalized sensitivity plot is reviewed. A PAM50 color does not constitute new PAM50 classifier evidence.

## Quality and reproducibility checks

- **Identity:** Confirm `identical()` sample IDs after a keyed join; assert unique gene/sample names and preserve matrix orientation.
- **Numerical:** Hand-check one gene's below/above tail counts and denominators; verify missing values, strict boundary comparisons and invalid/constant row handling. See the synthetic [R resource tests](../tests/test_gene_visuals.R).
- **Annotations:** Check that palette names cover every observed Type/Subtype level and distinguish genuine missingness from nonapplicability. Document sample counts by tissue group.
- **Clustering and palette:** State distance, linkage, splits, thresholds and score clipping. Row standardization is cohort-dependent and does not permit direct comparison of absolute gene abundance across rows.
- **Output:** Draw exactly once in the report; use the same renderer for PDF and PNG; include both the continuous color scale and the tail-bar legend. Check whether axis text or legends are clipped, and retain an execution/environment record.
- **Scientific boundary:** Do not read subtype assignment, causation, prognosis or treatment response from clusters or tail percentages. New datasets require access, privacy, provenance and validation review before public release.

### References

- [Gu, Eils & Schlesner (2016), *Complex heatmaps reveal patterns and correlations in multidimensional genomic data*](https://doi.org/10.1093/bioinformatics/btw313).
- [Gu (2022), *Complex heatmap visualization*](https://doi.org/10.1002/imt2.43).
- [ComplexHeatmap annotation reference](https://jokergoo.github.io/ComplexHeatmap-reference/book/heatmap-annotations.html) and [`anno_barplot()` API](https://jokergoo.github.io/ComplexHeatmap/reference/anno_barplot.html).
- [Breast cancer measurement guide](GENE_EXPRESSION_INTERPRETATION.md) and [biostatistical visualization evidence matrix](../Literature/BIOSTAT_R_VISUALIZATION_EVIDENCE_MATRIX.md).
