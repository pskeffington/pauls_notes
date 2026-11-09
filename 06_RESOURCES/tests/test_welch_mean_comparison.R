# Synthetic-only tests for dataset-neutral Welch mean comparison.
# From any working directory:
#   Rscript --vanilla 06_RESOURCES/tests/test_welch_mean_comparison.R

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (!length(file_arg)) stop("Run this test with Rscript --vanilla <path>.")
script <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
source(file.path(dirname(script), "..", "R", "welch_mean_comparison.R"))

rejects <- function(expr) inherits(try(expr, silent = TRUE), "try-error")

# All records and values are invented; no study data are embedded here.
synthetic <- data.frame(
  subject_id = sprintf("S%02d", seq_len(12)),
  group = factor(
    rep(c("Reference", "Comparison"), each = 6L),
    levels = c("Comparison", "Reference")
  ),
  measurement = c(1, 2, 4, 5, 7, 8, 3, 5, 8, 10, 12, 16)
)

result <- welch_mean_comparison(
  synthetic, outcome = "measurement", group = "group",
  subject_id = "subject_id", reference_level = "Reference",
  comparison_level = "Comparison", alpha = 0.05
)

expected <- stats::t.test(
  x = synthetic$measurement[synthetic$group == "Comparison"],
  y = synthetic$measurement[synthetic$group == "Reference"],
  alternative = "two.sided", var.equal = FALSE, conf.level = 0.95
)

stopifnot(
  inherits(result, "welch_mean_comparison"),
  identical(result$n_total, 12L),
  identical(result$n_complete, 12L),
  identical(result$n_excluded, 0L),
  result$id_uniqueness_checked,
  identical(result$group_summary$role, c("reference", "comparison")),
  identical(result$group_summary$n_observed, c(6L, 6L)),
  all(result$group_summary$n_missing == 0L),
  isTRUE(all.equal(result$mean_difference,
                   unname(expected$estimate[1] - expected$estimate[2]))),
  isTRUE(all.equal(result$t_statistic, unname(expected$statistic))),
  isTRUE(all.equal(result$degrees_freedom, unname(expected$parameter))),
  isTRUE(all.equal(result$p_value, expected$p.value)),
  isTRUE(all.equal(c(result$ci_lower, result$ci_upper),
                   as.numeric(expected$conf.int))),
  identical(result$reject_null, result$p_value < 0.05),
  is.data.frame(welch_mean_result_table(result)),
  grepl("n = 12 complete of 12", format_welch_mean_result(result), fixed = TRUE)
)

# Reversed contrast must reverse sign, t-statistic and CI endpoints.
reversed <- welch_mean_comparison(
  synthetic, "measurement", "group",
  reference_level = "Comparison", comparison_level = "Reference",
  subject_id = "subject_id"
)
stopifnot(
  isTRUE(all.equal(reversed$mean_difference, -result$mean_difference)),
  isTRUE(all.equal(reversed$t_statistic, -result$t_statistic)),
  isTRUE(all.equal(reversed$ci_lower, -result$ci_upper)),
  isTRUE(all.equal(reversed$ci_upper, -result$ci_lower)),
  isTRUE(all.equal(reversed$p_value, result$p_value))
)

# Row ordering and factor level ordering may not change the estimand.
reordered <- welch_mean_comparison(
  synthetic[rev(seq_len(nrow(synthetic))), , drop = FALSE],
  "measurement", "group", "Reference", "Comparison",
  subject_id = "subject_id"
)
stopifnot(
  isTRUE(all.equal(reordered$mean_difference, result$mean_difference)),
  isTRUE(all.equal(reordered$p_value, result$p_value))
)

# Missingness: complete-case exclusions, total and group-specific denominators.
incomplete <- synthetic
incomplete$measurement[1] <- NA_real_
incomplete$group[2] <- NA
missing_result <- welch_mean_comparison(
  incomplete, "measurement", "group", "Reference", "Comparison",
  subject_id = "subject_id"
)
stopifnot(
  missing_result$n_complete == 10L,
  missing_result$n_excluded == 2L,
  missing_result$n_missing_outcome == 1L,
  missing_result$n_missing_group == 1L,
  missing_result$n_missing_both == 0L,
  identical(missing_result$group_summary$n_total, c(5L, 6L)),
  identical(missing_result$group_summary$n_observed, c(4L, 6L)),
  identical(missing_result$group_summary$n_missing, c(1L, 0L))
)

missing_both <- synthetic
missing_both$measurement[1] <- NA_real_
missing_both$group[1] <- NA
both_result <- welch_mean_comparison(
  missing_both, "measurement", "group", "Reference", "Comparison"
)
stopifnot(both_result$n_excluded == 1L,
          both_result$n_missing_both == 1L,
          !both_result$id_uniqueness_checked)

# Invalid inputs must fail visibly (not silently impute or recode).
bad_id <- synthetic
bad_id$subject_id[2] <- bad_id$subject_id[1]
stopifnot(rejects(welch_mean_comparison(
  bad_id, "measurement", "group", "Reference", "Comparison",
  subject_id = "subject_id"
)))

bad_id <- synthetic
bad_id$subject_id[2] <- NA_character_
stopifnot(rejects(welch_mean_comparison(
  bad_id, "measurement", "group", "Reference", "Comparison",
  subject_id = "subject_id"
)))

three_groups <- synthetic
three_groups$group <- as.character(three_groups$group)
three_groups$group[1] <- "Third"
stopifnot(rejects(welch_mean_comparison(
  three_groups, "measurement", "group", "Reference", "Comparison"
)))

too_small <- synthetic[c(1, 7, 8), , drop = FALSE]
stopifnot(rejects(welch_mean_comparison(
  too_small, "measurement", "group", "Reference", "Comparison"
)))

invalid_outcome <- synthetic
invalid_outcome$measurement[1] <- Inf
stopifnot(rejects(welch_mean_comparison(
  invalid_outcome, "measurement", "group", "Reference", "Comparison"
)))
invalid_outcome$measurement[1] <- NaN
stopifnot(rejects(welch_mean_comparison(
  invalid_outcome, "measurement", "group", "Reference", "Comparison"
)))

for (bad_alpha in c(-1, 0, 1, 2, NA_real_)) {
  stopifnot(rejects(welch_mean_comparison(
    synthetic, "measurement", "group",
    "Reference", "Comparison", alpha = bad_alpha
  )))
}
stopifnot(
  rejects(welch_mean_comparison(
    synthetic, "measurement", "group",
    "Reference", "Reference"
  )),
  rejects(welch_mean_comparison(
    synthetic, "missing_column", "group",
    "Reference", "Comparison"
  )),
  rejects(welch_mean_result_table(NULL)),
  rejects(format_welch_mean_result(NULL)),
  rejects(plot_welch_mean_difference(NULL))
)

# A test that cannot estimate uncertainty must not publish a CI.
constant <- synthetic
constant$measurement <- 1
stopifnot(rejects(welch_mean_comparison(
  constant, "measurement", "group", "Reference", "Comparison"
)))

if (requireNamespace("ggplot2", quietly = TRUE)) {
  plot <- plot_welch_mean_difference(
    result, outcome_label = "Synthetic measurement", unit = "a.u."
  )
  stopifnot(
    inherits(plot, "ggplot"),
    nrow(plot$data) == 1L,
    isTRUE(all.equal(plot$data$estimate, result$mean_difference)),
    isTRUE(all.equal(plot$data$lower, result$ci_lower)),
    isTRUE(all.equal(plot$data$upper, result$ci_upper))
  )
  built <- ggplot2::ggplot_build(plot)
  stopifnot(length(built$data) == 3L)
}

cat("PASS: Welch comparison, explicit contrast, CI, missingness, invalid cases, optional ggplot2.\n")
