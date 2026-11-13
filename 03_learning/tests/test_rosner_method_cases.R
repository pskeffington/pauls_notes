# Synthetic-only exercise checks; run with Rscript --vanilla.
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (!length(file_arg)) stop("Run with Rscript --vanilla <test path>.")
here <- dirname(normalizePath(sub("^--file=", "", file_arg[1L]), mustWork = TRUE))
source(file.path(here, "..", "examples", "rosner_method_cases.R"))
case <- rosner_teaching_cases()
stopifnot(identical(case$independent$n, 12L),
          identical(case$independent$reference_n, 6L),
          identical(case$independent$comparison_n, 6L),
          isTRUE(all.equal(case$independent$mean_difference,
                           17 - 12.5)),
          identical(case$paired$n_pairs, 8L),
          isTRUE(all.equal(case$paired$mean_change, 1.5)),
          isTRUE(all.equal(case$binomial$upper_tail,
                           sum(stats::dbinom(36:80, 80, .35)),
                           tolerance = 1e-12)),
          isTRUE(all.equal(case$binomial$upper_tail,
                           case$binomial$test$p.value, tolerance = 1e-12)),
          identical(sum(case$categorical$counts), 40),
          identical(case$poisson$expected_count, 8),
          isTRUE(all.equal(case$poisson$upper_tail,
                           sum(stats::dpois(10:100, lambda = 8)),
                           tolerance = 1e-10)))
if (requireNamespace("survival", quietly = TRUE)) {
  surv <- rosner_survival_case()
  stopifnot(identical(surv$n, 10L),
            inherits(surv$km, "survfit"),
            inherits(surv$log_rank, "survdiff"))
}
cat("PASS: synthetic continuous, paired, binomial, categorical, Poisson and optional survival cases.\n")
