# Synthetic-only smoke checks. Execute with Rscript --vanilla.
args <- commandArgs(trailingOnly = FALSE)
f <- grep("^--file=", args, value = TRUE)
if (!length(f)) stop("Run with Rscript --vanilla")
dir <- dirname(normalizePath(sub("^--file=", "", f[1])))
source(file.path(dir, "..", "R", "stats_plots.R"))
source(file.path(dir, "..", "R", "gene_visuals.R"))
set.seed(711)
m <- matrix(rnorm(240), nrow = 20,
            dimnames = list(paste0("gene", 1:20), paste0("sample", 1:12)))
meta <- data.frame(Sample = rev(colnames(m)),
                   Subtype = rep(c("A", "B"), each=6))
stopifnot(length(top_variable_genes(m, 5)) == 5L)
stopifnot(identical(as.character(align_gene_metadata(m, meta)$Sample), colnames(m)))
stopifnot(inherits(try(validate_gene_matrix(m, "missing"), silent=TRUE), "try-error"))
if (requireNamespace("ggplot2", quietly = TRUE)) {
  stopifnot(inherits(plot_gene_heatmap(m, rownames(m)[1:5]), "ggplot"))
  stopifnot(inherits(plot_gene_pca(m, meta, "Subtype", n_genes=10), "ggplot"))
  stopifnot(inherits(plot_gene_mean_variance(m), "ggplot"))
  de <- data.frame(logFC = rnorm(20), FDR = seq(.001, 1, length.out=20))
  stopifnot(inherits(plot_gene_volcano(de), "ggplot"))
}
# Invented values: a strict cutoff excludes exactly -1 and +1.
z_fixture <- matrix(c(-2, -1, 0, 2,
                      NA, -2, 1, 2), nrow = 2, byrow = TRUE,
                    dimnames = list(c("ESR1", "ERBB2"), paste0("S", 1:4)))
tails <- row_z_tail_percentages(z_fixture)
stopifnot(identical(dimnames(tails), list(c("ESR1", "ERBB2"), c("Low", "High"))),
          isTRUE(all.equal(as.numeric(tails[1, ]), c(25, 25))),
          isTRUE(all.equal(as.numeric(tails[2, ]), c(100/3, 100/3))),
          isTRUE(all.equal(as.numeric(row_z_tail_percentages(z_fixture, 2)[1, ]),
                           c(0, 0))),
          all(tails >= 0 & tails <= 100))
z_bad <- z_fixture
z_bad[1, ] <- NA_real_
stopifnot(inherits(try(row_z_tail_percentages(z_bad), silent = TRUE), "try-error"))
z_bad <- z_fixture
z_bad[1, 1] <- NaN
stopifnot(inherits(try(row_z_tail_percentages(z_bad), silent = TRUE), "try-error"))
z_bad <- z_fixture
colnames(z_bad)[1] <- colnames(z_bad)[2]
stopifnot(inherits(try(row_z_tail_percentages(z_bad), silent = TRUE), "try-error"))
stopifnot(inherits(try(row_z_tail_percentages(z_fixture, threshold = 0),
                     silent = TRUE), "try-error"))

cat("PASS: synthetic genomics visualizations and validation smoke tests\n")

blank <- m
colnames(blank)[1] <- " "
stopifnot(inherits(try(validate_gene_matrix(blank), silent=TRUE), "try-error"),
          inherits(try(align_gene_metadata(blank, meta), silent=TRUE), "try-error"),
          inherits(try(validate_gene_matrix(m[FALSE, , drop=FALSE]), silent=TRUE), "try-error"))
