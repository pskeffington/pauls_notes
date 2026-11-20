# ================================================================
# 01 | SOURCE AND REPRODUCIBLE SYNTHETIC FIXTURE
# ================================================================
# Fixed-reference checks for independent synthetic probability examples.
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (!length(file_arg)) stop("Run with Rscript --vanilla.")
here <- dirname(normalizePath(sub("^--file=", "", file_arg[1L]),
                              mustWork = TRUE))
source(file.path(here, "..", "examples", "breast_cancer_distribution_lab.R"))
set.seed(47L)
original_state <- .Random.seed
x <- breast_cancer_distribution_lab(repetitions = 500L)
stopifnot(identical(.Random.seed, original_state))
# ================================================================
# 02 | NUMERICAL COMPARISON HELPER
# ================================================================
near <- function(value, expected, tolerance = 1e-7) {
  stopifnot(length(value) == 1L, is.numeric(value), is.finite(value),
            isTRUE(all.equal(unname(value), expected,
                             tolerance = tolerance)))
}
# ================================================================
# 03 | CONTINUOUS AND HYPOTHESIS-TEST REFERENCE VALUES
# ================================================================
near(x$z["statistic"], 2)
near(x$z["p_two_sided"], 0.04550026389635857)
near(x$t$estimate, 12)
near(x$t$conf.int[1L], 9.810783339465775)
near(x$t$conf.int[2L], 14.189216660534225)
near(x$welch$estimate[1L]-x$welch$estimate[2L], -3.5)
near(x$chisq$statistic, 4)
near(x$chisq$p.value, 0.04550026389635857)
near(summary(x$anova)[[1L]][["F value"]][1L], 3)
near(stats::pf(3,2,6,lower.tail=FALSE), .125)
# ================================================================
# 04 | DISCRETE MASS, INCLUSIVE RANGE AND UPPER TAIL
# ================================================================
# Independent identities compare a cumulative interval to the sum of
# individual probability masses; bounds are inclusive on both ends.
near(x$binomial_point, stats::dbinom(36L, 80L, .35))
near(x$binomial_range, sum(stats::dbinom(30L:36L, 80L, .35)))
stopifnot(identical(unname(x$binomial_interval), c(30L, 36L)))
near(x$binomial_tail, 0.04106885425072182)
near(x$binomial$p.value, x$binomial_tail)
near(x$poisson_point, stats::dpois(10L, 8))
near(x$poisson_range, sum(stats::dpois(7L:10L, 8)))
stopifnot(identical(unname(x$poisson_interval), c(7L, 10L)))
near(x$poisson_tail, 0.28337574127298903)
# ================================================================
# 05 | SAMPLING, POWER AND RANDOM-STATE CONTRACT
# ================================================================
near(x$power_normal, 0.5160052739761748)
near(x$clt$se_5, 10/sqrt(5))
near(x$clt$se_50, 10/sqrt(50))
stopifnot(length(x$clt$means_5) == 500L,
          length(x$clt$means_50) == 500L,
          identical(x$clt$means_5,
            breast_cancer_distribution_lab(repetitions=500L)$clt$means_5))
cat("PASS: synthetic normal, t, Welch, chi-square, F, binomial and Poisson point/range/tail, CLT, power reference checks.\n")
