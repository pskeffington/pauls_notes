# Check reusable summaries and the book's numerical examples against their current source.
source("06_RESOURCES/R/hse_stats_plots.R")
source("06_RESOURCES/Genomics/FIGURES/gene_companion_heatmap.R")
source("06_RESOURCES/Genomics/FIGURES/gene_companion_walkthrough.R")
rejects <- function(expr) inherits(tryCatch({force(expr); NULL}, error = identity), "error")
small <- data.frame(group = c("A", "A", "A", "A", "B"), marker = c(2, 4, 6, NA, 9))
table <- hse_describe(small, "marker", group = "group")
stopifnot(table$n[1] == 3L, table$n_missing[1] == 1L, table$pct_missing[1] == 25,
  table$median[1] == 4, table$iqr[1] == 2, is.na(table$sd[2]), is.na(table$se[2]))
report <- hse_summary_report(small, "marker", group = "group", unit = "invented au")
stopifnot(length(report$narrative) == 2L, grepl("IQR", report$narrative[1], fixed = TRUE),
  grepl("missing", report$narrative[1], fixed = TRUE),
  nrow(hse_describe(data.frame(marker = numeric()), "marker")) == 0L,
  rejects(hse_describe(data.frame(marker = "not numeric"), "marker")))
missing <- hse_summary_report(data.frame(marker = c(NA_real_, NA_real_)), "marker")
stopifnot(missing$statistics$n == 0L, grepl("no observed", missing$narrative[1], fixed = TRUE))
walk <- paired_teaching_summary()
stopifnot(isTRUE(all.equal(mean(walk$contrasts), .5)),
  isTRUE(all.equal(walk$sensitivity_range, c(.2, .8))),
  grepl("not a confidence interval", walk$interpretation, fixed = TRUE))
broken <- companion_pairs(); broken$comparator[1] <- 0
stopifnot(rejects(paired_teaching_summary(broken)))
broken <- companion_pairs(); broken$pair[2] <- broken$pair[1]
stopifnot(rejects(paired_teaching_summary(broken)))
values <- companion_matrix()
stopifnot(identical(dim(values), c(6L, 4L)), all(is.finite(values)),
  identical(range(values), c(-2, 2)), values[1, 1] == 2, 2^values[1, 1] == 4)
for (path in c("06_RESOURCES/Genomics/FIGURES/README.md",
               "06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md")) {
  lines <- readLines(path, warn = FALSE, encoding = "UTF-8")
  for (i in seq_len(nrow(values))) {
    row <- grep(paste0("^\\| ", rownames(values)[i], " \\|"), lines, value = TRUE)
    stopifnot(length(row) == 1L)
    cells <- trimws(strsplit(row, "|", fixed = TRUE)[[1]])
    cells <- cells[nzchar(cells)]
    displayed <- as.numeric(gsub("\u2212", "-", cells[-1], fixed = TRUE))
    stopifnot(identical(displayed, unname(values[i, ])))
  }
}
stopifnot(requireNamespace("ggplot2", quietly = TRUE))
heatmap <- companion_heatmap()
stopifnot(nrow(ggplot2::ggplot_build(heatmap)$data[[1]]) == 24L,
  identical(heatmap$scales$get_scales("fill")$limits, c(-2, 2)))
cat("PASS: summary quantiles and narratives, book paired arithmetic, heatmap values and rendered scale\n")
