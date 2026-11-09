# Run: Rscript --vanilla 06_RESOURCES/tests/test_welch_oneway_comparison.R
args <- commandArgs(trailingOnly = FALSE)
fa <- grep("^--file=", args, value = TRUE)
if (!length(fa)) stop("Run using Rscript.")
here <- dirname(normalizePath(sub("^--file=", "", fa[1]), mustWork = TRUE))
source(file.path(here, "..", "R", "welch_oneway_comparison.R"))
rejects <- function(expr) inherits(try(expr, silent = TRUE), "try-error")

synthetic <- data.frame(
  subject_id = sprintf("S%02d", 1:18),
  group = rep(c("A", "B", "C"), each = 6),
  outcome = c(1, 2, 4, 5, 6, 9, 3, 4, 8, 12, 13, 17,
              4, 7, 9, 11, 15, 19)
)
r <- welch_oneway_comparison(synthetic, "outcome", "group")
expected <- stats::oneway.test(outcome ~ group, data = synthetic,
                               var.equal = FALSE)
stopifnot(inherits(r, "welch_oneway_comparison"),
          r$n_total == 18L, r$n_complete == 18L, r$n_excluded == 0L,
          all(r$group_summary$n_observed == 6L),
          isTRUE(all.equal(r$f_statistic, unname(expected$statistic))),
          isTRUE(all.equal(r$df_numerator, unname(expected$parameter[1]))),
          isTRUE(all.equal(r$df_denominator, unname(expected$parameter[2]))),
          isTRUE(all.equal(r$p_value, expected$p.value)),
          identical(r$pairwise_posthoc_performed, FALSE))

permuted <- synthetic[rev(seq_len(nrow(synthetic))), ]
r2 <- welch_oneway_comparison(permuted, "outcome", "group")
stopifnot(isTRUE(all.equal(r2$p_value, r$p_value)))
missing <- synthetic
missing$outcome[1] <- NA_real_
missing$group[7] <- NA_character_
r_missing <- welch_oneway_comparison(missing, "outcome", "group")
stopifnot(r_missing$n_excluded == 2L, r_missing$n_complete == 16L,
          r_missing$n_missing_outcome == 1L,
          r_missing$n_missing_group == 1L)

bad <- synthetic
bad$group[13:18] <- "B"
stopifnot(rejects(welch_oneway_comparison(bad, "outcome", "group")))
bad <- synthetic
bad$outcome[1] <- Inf
stopifnot(rejects(welch_oneway_comparison(bad, "outcome", "group")))
bad <- synthetic
bad$outcome[1:6] <- 1
stopifnot(rejects(welch_oneway_comparison(bad, "outcome", "group")))
stopifnot(rejects(welch_oneway_comparison(
  synthetic, "outcome", "group", alpha = 0)))

if (requireNamespace("ggplot2", quietly = TRUE)) {
  p <- plot_welch_oneway_groups(r, synthetic,
                               outcome_label = "Invented marker", unit = "a.u.")
  stopifnot(inherits(p, "ggplot"), nrow(p$data) == r$n_complete)
  ggplot2::ggplot_build(p)
  changed <- synthetic
  changed$outcome[1] <- changed$outcome[1] + 2
  stopifnot(rejects(plot_welch_oneway_groups(r, changed)))
}
cat("PASS: Welch multi-group inference, guards, missingness, ggplot2.\n")
