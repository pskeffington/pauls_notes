# Run: Rscript --vanilla 06_RESOURCES/tests/test_paired_mean_change.R
args <- commandArgs(trailingOnly = FALSE)
fa <- grep("^--file=", args, value = TRUE)
if (!length(fa)) stop("Run using Rscript.")
here <- dirname(normalizePath(sub("^--file=", "", fa[1]), mustWork = TRUE))
source(file.path(here, "..", "R", "paired_mean_change.R"))
rejects <- function(expr) inherits(try(expr, silent = TRUE), "try-error")

# Four invented subjects measured twice; differences = 1, 2, 4, 8.
before <- c(3, 5, 8, 12)
after <- before + c(1, 2, 4, 8)
data <- data.frame(
  subject_id = rep(sprintf("S%02d", 1:4), each = 2L),
  visit = rep(c("before", "after"), 4L),
  outcome = as.vector(rbind(before, after))
)
result <- paired_mean_change(data, "subject_id", "visit", "outcome",
                             "before", "after")
expected <- stats::t.test(after, before, paired = TRUE)
stopifnot(
  identical(result$n_subjects_total, 4L),
  identical(result$n_complete_pairs, 4L),
  identical(result$n_excluded_subjects, 0L),
  identical(result$n_missing_measurements, 0L),
  isTRUE(all.equal(result$mean_change, mean(after - before))),
  isTRUE(all.equal(result$sd_change, sd(after - before))),
  isTRUE(all.equal(result$t_statistic, unname(expected$statistic))),
  isTRUE(all.equal(result$degrees_freedom, unname(expected$parameter))),
  isTRUE(all.equal(result$p_value, expected$p.value)),
  isTRUE(all.equal(c(result$ci_lower, result$ci_upper),
                   unname(expected$conf.int)))
)

permuted <- paired_mean_change(data[c(5, 7, 2, 8, 1, 4, 6, 3), ],
                               "subject_id", "visit", "outcome", "before", "after")
stopifnot(isTRUE(all.equal(permuted$mean_change, result$mean_change)),
          isTRUE(all.equal(permuted$p_value, result$p_value)))
reversed <- paired_mean_change(data, "subject_id", "visit", "outcome",
                                "after", "before")
stopifnot(isTRUE(all.equal(reversed$mean_change, -result$mean_change)),
          isTRUE(all.equal(reversed$ci_lower, -result$ci_upper)),
          isTRUE(all.equal(reversed$ci_upper, -result$ci_lower)))

missing <- data
missing$outcome[2] <- NA_real_
m <- paired_mean_change(missing, "subject_id", "visit", "outcome",
                        "before", "after")
stopifnot(m$n_complete_pairs == 3L, m$n_excluded_subjects == 1L,
          m$n_missing_measurements == 1L)
incomplete <- data[-8, ]
mi <- paired_mean_change(incomplete, "subject_id", "visit", "outcome",
                         "before", "after")
stopifnot(mi$n_subjects_total == 4L, mi$n_complete_pairs == 3L,
          mi$n_excluded_subjects == 1L)

bad <- data
bad$subject_id[2] <- bad$subject_id[4]
stopifnot(rejects(paired_mean_change(
  bad, "subject_id", "visit", "outcome", "before", "after")))
bad <- data
bad$visit[1] <- NA_character_
stopifnot(rejects(paired_mean_change(
  bad, "subject_id", "visit", "outcome", "before", "after")))
bad <- data
bad$outcome[1] <- Inf
stopifnot(rejects(paired_mean_change(
  bad, "subject_id", "visit", "outcome", "before", "after")))
bad <- data
bad$outcome <- rep(3, nrow(bad))
stopifnot(rejects(paired_mean_change(
  bad, "subject_id", "visit", "outcome", "before", "after")))
stopifnot(rejects(paired_mean_change(
  data, "subject_id", "visit", "outcome", "before", "after", alpha = 1)))

if (requireNamespace("ggplot2", quietly = TRUE)) {
  p <- plot_paired_mean_change(result, "Synthetic measurement", "a.u.")
  stopifnot(inherits(p, "ggplot"), nrow(p$data) == 1L,
            isTRUE(all.equal(p$data$mean_change, result$mean_change)))
  ggplot2::ggplot_build(p)
}
cat("PASS: paired t inference, alignment, reversal, missingness, error guards, plotting.\n")
