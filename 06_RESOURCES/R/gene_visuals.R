# Gene plots: source stats_plots.R first.
# Plot log2 CPM for exploration; keep raw counts for statistical models.

validate_gene_matrix <- function(expr, genes = NULL) {
  if (!is.matrix(expr) || !is.numeric(expr) || any(dim(expr) == 0L) ||
      any(!is.finite(expr)))
    stop("expr must be a finite numeric genes-by-samples matrix.")
  if (is.null(rownames(expr)) || is.null(colnames(expr)) ||
      anyNA(rownames(expr)) || anyNA(colnames(expr)) ||
      any(!nzchar(trimws(rownames(expr)))) || any(!nzchar(trimws(colnames(expr)))) ||
      anyDuplicated(rownames(expr)) || anyDuplicated(colnames(expr)))
    stop("Gene and sample names must exist and be unique.")
  if (!is.null(genes) && (!length(genes) || anyDuplicated(genes) ||
                           !all(genes %in% rownames(expr))))
    stop("genes must be unique nonempty names present in expr.")
  invisible(TRUE)
}

# Align metadata by sample ID; never assume that row order matches expression.
align_gene_metadata <- function(expr, metadata, sample_col = "Sample") {
  validate_gene_matrix(expr)
  validate_columns(metadata, sample_col)
  if (anyNA(metadata[[sample_col]]) ||
      any(!nzchar(trimws(as.character(metadata[[sample_col]])))))
    stop("Metadata sample identifiers must be nonblank and nonmissing.")
  if (anyNA(metadata[[sample_col]]) ||
      anyDuplicated(as.character(metadata[[sample_col]])))
    stop("Metadata sample identifiers must be unique and nonmissing.")
  sample_index <- match(colnames(expr), as.character(metadata[[sample_col]]))
  if (anyNA(sample_index)) stop("Metadata missing expression sample(s).")
  metadata[sample_index, , drop = FALSE]
}

# Stable top-variable feature choice for plots; uses row variance directly.
# Only use finite log-scale expression. Explicit gene lists take precedence.
top_variable_genes <- function(expr, n = 50L) {
  validate_gene_matrix(expr)
  if (length(n) != 1L || !is.finite(n) || n < 1 || n != as.integer(n))
    stop("n must be a positive integer.")
  if (ncol(expr) < 2L) stop("Variance needs at least two samples.")
  gene_variance <- if (requireNamespace("matrixStats", quietly = TRUE))
    matrixStats::rowVars(expr) else apply(expr, 1L, stats::var)
  rownames(expr)[head(order(-gene_variance, rownames(expr)), min(n, nrow(expr)))]
}


# Gene-wise percentages of observed z-scores outside +/- threshold.
# Input is already row-standardized: genes in rows, samples in columns.
# This function does NOT normalize counts or compute z-scores.
row_z_tail_percentages <- function(hm_z, threshold = 1) {
  if (!is.matrix(hm_z) || !is.numeric(hm_z) ||
      any(dim(hm_z) == 0L))
    stop("hm_z must be a nonempty numeric genes-by-samples matrix.")
  if (is.null(rownames(hm_z)) || is.null(colnames(hm_z)) ||
      anyNA(rownames(hm_z)) || anyNA(colnames(hm_z)) ||
      any(!nzchar(trimws(rownames(hm_z)))) ||
      any(!nzchar(trimws(colnames(hm_z)))) ||
      anyDuplicated(rownames(hm_z)) || anyDuplicated(colnames(hm_z)))
    stop("Gene and sample identifiers must be unique and nonblank.")
  if (any(is.nan(hm_z)) || any(is.infinite(hm_z)))
    stop("Resolve NaN/Inf row-scaling values before counting z-score tails.")
  if (!is.numeric(threshold) || length(threshold) != 1L ||
      !is.finite(threshold) || threshold <= 0)
    stop("threshold must be one positive finite number.")

  n_obs <- rowSums(!is.na(hm_z))
  if (any(n_obs == 0L))
    stop("All-missing gene rows have undefined z-score tail percentages.")

  z_pct <- cbind(
    Low = 100 * rowSums(hm_z < -threshold, na.rm = TRUE) / n_obs,
    High = 100 * rowSums(hm_z > threshold, na.rm = TRUE) / n_obs
  )
  rownames(z_pct) <- rownames(hm_z)
  z_pct
}

# Heatmap: select genes FIRST (avoids materializing a full long table).
# center_rows=TRUE highlights within-gene sample differences. Z-scores
# are not absolute gene abundance and should be labeled accordingly.
plot_gene_heatmap <- function(expr, genes, center_rows = TRUE,
                             title = "Selected gene expression heatmap", fill_scale = NULL) {
  validate_gene_matrix(expr, genes)
  require_plotting_packages()
  expression_matrix <- expr[genes, , drop = FALSE]
  if (center_rows) {
    gene_mean <- rowMeans(expression_matrix)
    sd <- if (requireNamespace("matrixStats", quietly = TRUE))
      matrixStats::rowSds(expression_matrix) else apply(expression_matrix, 1L, stats::sd)
    sd[!is.finite(sd) | sd == 0] <- 1
    expression_matrix <- sweep(sweep(expression_matrix, 1L, gene_mean), 1L, sd, "/")
  }
  plot_data <- data.frame(Gene = factor(rep(rownames(expression_matrix), times = ncol(expression_matrix)),
                                 levels = rev(rownames(expression_matrix))),
                  Sample = factor(rep(colnames(expression_matrix), each = nrow(expression_matrix)),
                                  levels = colnames(expression_matrix)),
                  Value = as.vector(expression_matrix))
  ggplot2::ggplot(plot_data, ggplot2::aes(x = .data$Sample, y = .data$Gene,
                                  fill = .data$Value)) +
    ggplot2::geom_raster() +
    (if (!is.null(fill_scale)) fill_scale else if (center_rows)
      ggplot2::scale_fill_gradient2(low = "#2166AC", mid = "#F7F7F7",
                                  high = "#B2182B", midpoint = 0,
                                  na.value = "#808080", name = "Row z-score") else
      ggplot2::scale_fill_viridis_c(na.value = "#808080", name = "log2 CPM")) +
    ggplot2::labs(title = title, x = "Sample", y = "Gene") +
    theme_publication() + ggplot2::theme(axis.text.x =
                                  ggplot2::element_text(angle = 90, hjust = 1, vjust = .5))
}

# PCA: select top-variable genes, then center gene columns across samples.
# Constant genes are discarded to avoid singular/undefined scaling.
# PCA is descriptive; biological group differences are not hypothesis tests.
plot_gene_pca <- function(expr, metadata, group, n_genes = 500L,
                         sample_col = "Sample") {
  validate_gene_matrix(expr)
  validate_columns(metadata, c(sample_col, group))
  require_plotting_packages()
  aligned_metadata <- align_gene_metadata(expr, metadata, sample_col)
  genes <- top_variable_genes(expr, n_genes)
  expression_matrix <- t(expr[genes, , drop = FALSE])
  variable_genes <- apply(expression_matrix, 2L, stats::sd) > 0
  expression_matrix <- expression_matrix[, variable_genes, drop = FALSE]
  if (nrow(expression_matrix) < 3L || ncol(expression_matrix) < 2L)
    stop("PCA requires at least three samples and two variable genes.")
  pca_fit <- stats::prcomp(expression_matrix, center = TRUE, scale. = FALSE, rank. = 2)
  plot_data <- data.frame(PC1 = pca_fit$x[, 1], PC2 = pca_fit$x[, 2],
                  Group = as.factor(aligned_metadata[[group]]))
  explained_variance_pct <- 100 * pca_fit$sdev^2 / sum(pca_fit$sdev^2)
  ggplot2::ggplot(plot_data, ggplot2::aes(x = .data$PC1, y = .data$PC2,
                                  color = .data$Group)) +
    ggplot2::geom_point(size = 2, alpha = .8) +
    ggplot2::labs(title = "Gene expression PCA",
                  x = sprintf("PC1 (%.1f%%)", explained_variance_pct[1]),
                  y = sprintf("PC2 (%.1f%%)", explained_variance_pct[2]), color = group) +
    theme_publication()
}

# Mean-variance diagnostic: vectorized rowMeans and optional matrixStats.
# Interpret on the supplied scale (recommended: log2 CPM).
plot_gene_mean_variance <- function(expr) {
  validate_gene_matrix(expr)
  if (ncol(expr) < 2L) stop("At least two samples required.")
  require_plotting_packages()
  plot_data <- data.frame(mean = rowMeans(expr),
                  variance = if (requireNamespace("matrixStats", quietly = TRUE))
                    matrixStats::rowVars(expr) else apply(expr, 1L, stats::var))
  ggplot2::ggplot(plot_data, ggplot2::aes(x = .data$mean, y = .data$variance)) +
    ggplot2::geom_point(alpha = .2, size = .8) +
    ggplot2::labs(title = "Gene-level mean-variance diagnostic",
                  x = "Mean log2 CPM", y = "Variance of log2 CPM") + theme_publication()
}

# Volcano plot: input MUST contain model-derived logFC and adjusted p-values.
# This never fits a model and does not infer significance from CPM values.
# p=0 can arise from numeric underflow; floor only for display.
plot_gene_volcano <- function(results, logfc = "logFC", fdr = "FDR",
                             gene = NULL, fdr_cutoff = .05,
                             effect_cutoff = 1, color_scale = NULL) {
  validate_columns(results, c(logfc, fdr, gene))
  validate_numeric(results[[logfc]], logfc)
  validate_numeric(results[[fdr]], fdr)
  require_plotting_packages()
  if (!is.finite(fdr_cutoff) || fdr_cutoff <= 0 || fdr_cutoff >= 1 ||
      !is.finite(effect_cutoff) || effect_cutoff < 0)
    stop("Invalid FDR or effect-size cutoff.")
  if (any(results[[fdr]] < 0 | results[[fdr]] > 1, na.rm = TRUE))
    stop("Adjusted p-values must be between 0 and 1.")
  plot_data <- data.frame(logFC = results[[logfc]],
                  FDR = results[[fdr]])
  plot_data$score <- -log10(pmax(plot_data$FDR, .Machine$double.xmin))
  plot_data$status <- !is.na(plot_data$FDR) & !is.na(plot_data$logFC) &
    plot_data$FDR < fdr_cutoff & abs(plot_data$logFC) >= effect_cutoff
  ggplot2::ggplot(plot_data, ggplot2::aes(x = .data$logFC, y = .data$score,
                                  color = .data$status, shape = .data$status)) +
    ggplot2::geom_point(alpha = .55, size = 1.1, na.rm = TRUE) +
    ggplot2::geom_vline(xintercept = c(-effect_cutoff, effect_cutoff),
                        linetype = "dashed", color = "grey60") +
    ggplot2::geom_hline(yintercept = -log10(fdr_cutoff),
                        linetype = "dashed", color = "grey60") +
    (if (!is.null(color_scale)) color_scale else
      ggplot2::scale_color_manual(values = c("FALSE" = "grey70",
                                           "TRUE" = "#2166AC"),
                                labels = c("FALSE" = "Other", "TRUE" = "Meets cutoffs"),
                                name = "Threshold status")) +
    ggplot2::scale_shape_manual(values = c("FALSE" = 16, "TRUE" = 17),
      labels = c("FALSE" = "Other", "TRUE" = "Meets cutoffs"), name = "Threshold status") +
    ggplot2::labs(title = "Differential-expression volcano",
                  x = "Model log2 fold change", y = "-log10(adjusted p-value)") +
    theme_publication()
}
