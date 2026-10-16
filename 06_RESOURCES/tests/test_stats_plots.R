# Run from any working directory using:
# Rscript --vanilla 06_RESOURCES/tests/test_stats_plots.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (!length(file_arg)) stop("Run via Rscript --vanilla <test path>.")
script <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
source(file.path(dirname(script), "..", "R", "stats_plots.R"))
d <- data.frame(id = rep(1:4, each = 2),
                group = rep(c("A", "B"), 4),
                value = c(1, 2, 2, 3, 3, 4, 4, 5))
summary <- describe_measurements(d, "value", "group")
stopifnot(nrow(summary) == 2L, all(summary$n == 4L))
stopifnot(inherits(wilcox_independent(d, "value", "group"), "htest"))
# Formula dispatch is independent by default; verify against vector dispatch.
independent <- wilcox_independent(d, "value", "group")
expected <- stats::wilcox.test(d$value[d$group == "A"],
                              d$value[d$group == "B"], exact = FALSE)
stopifnot(isTRUE(all.equal(independent$p.value, expected$p.value)),
          isTRUE(all.equal(unname(independent$statistic),
                           unname(expected$statistic))))
stopifnot(inherits(wilcox_paired(d, "value", "group", "id"), "htest"))
stopifnot(is.list(correlation_summary(data.frame(x=1:5, y=5:1), "x", "y")))
stopifnot(inherits(try(validate_columns(d, "unknown"), silent = TRUE), "try-error"))
expr <- matrix(1:6, nrow=2, dimnames=list(c("g1","g2"), c("s3","s1","s2")))
meta <- data.frame(Sample=c("s1","s2","s3"), Subtype=c("B","C","A"))
long <- gene_expression_long(expr, "g1", meta)
stopifnot(identical(as.character(long$Subtype), c("A","B","C")))
stopifnot(identical(long$Expression, c(1L,3L,5L)))
if (requireNamespace("ggplot2", quietly=TRUE)) {
  stopifnot(inherits(plot_histogram(d,"value"), "ggplot"))
  stopifnot(inherits(plot_boxplot(d,"value","group"), "ggplot"))
  stopifnot(inherits(plot_scatter(d,"value","id",fit=TRUE), "ggplot"))
  stopifnot(inherits(plot_gene_panel(transform(long, Subtype=as.factor(Subtype)),
                                  "Subtype"), "ggplot"))
}
if (requireNamespace("edgeR", quietly=TRUE)) {
  set.seed(711)
  counts <- matrix(sample(1:100, 60, replace=TRUE), nrow=10)
  logcpm <- normalized_cpm(counts)
  stopifnot(identical(dim(logcpm), dim(counts)), all(is.finite(logcpm)))
}
cat("PASS: base statistical, sample-alignment and available optional package smoke tests\n")
