# ================================================================
# 01 | SYNTHETIC DISTRIBUTIONS AND SAMPLING
# ================================================================
# All values are invented teaching examples. Sourcing this file defines
# a function; it does not draw random samples or write output files.
breast_cancer_distribution_lab <- function(seed = 7122026L, repetitions = 5000L) {

  # ================================================================
  # 02 | INPUT VALIDATION AND RANDOM-STATE PRESERVATION
  # ================================================================
  # Replication counts and random seeds must be finite whole numbers.
  if (length(seed) != 1L || !is.numeric(seed) || !is.finite(seed) ||
      seed != floor(seed) || seed < 0 ||
      seed > .Machine$integer.max ||
      length(repetitions) != 1L ||
      !is.numeric(repetitions) || !is.finite(repetitions) ||
      repetitions < 100L ||
      repetitions > .Machine$integer.max ||
      repetitions != floor(repetitions)) {
    stop("Invalid seed or repetitions.", call. = FALSE)
  }
  had_seed <- exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE)
  if (had_seed) old_seed <- get(".Random.seed", envir = .GlobalEnv)
  on.exit({
    if (had_seed) assign(".Random.seed", old_seed, envir = .GlobalEnv)
    else if (exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE))
      rm(".Random.seed", envir = .GlobalEnv)
  }, add = TRUE)
  set.seed(as.integer(seed))

  # ================================================================
  # 03 | SAMPLING DISTRIBUTIONS AND FIXED TEACHING OBSERVATIONS
  # ================================================================
  # Exponential individual values have mean and SD of 10. Repeated
  # sample means illustrate the standard error as sample size grows.
  means_5 <- replicate(as.integer(repetitions), mean(stats::rexp(5L, rate = .1)))
  means_50 <- replicate(as.integer(repetitions), mean(stats::rexp(50L, rate = .1)))

  x <- c(8, 10, 10, 12, 12, 14, 14, 16)
  A <- c(8, 9, 10, 11, 12, 13)
  B <- c(9, 11, 13, 15, 17, 19)
  score <- c(8, 10, 12, 10, 12, 14, 12, 14, 16)
  arm <- factor(rep(c("A", "B", "C"), each = 3L),
                levels = c("A", "B", "C"))
  counts <- matrix(c(30L, 20L, 20L, 30L), nrow = 2L, byrow = TRUE,
                   dimnames = list(arm = c("A", "B"),
                                   response = c("yes", "no")))

  # ================================================================
  # 04 | DISCRETE PROBABILITY: BINOMIAL AND POISSON
  # ================================================================
  # X counts responses across 80 independent, equally likely trials.
  # The null probability of a response is 0.35; the observed count is
  # 36. Exact P(X=36), inclusive P(30<=X<=36), and P(X>=36)
  # answer different probability questions under the same model.
  binomial_n <- 80L
  binomial_p <- .35
  binomial_observed <- 36L
  binomial_interval <- c(lower = 30L, upper = 36L)
  binomial_point <- stats::dbinom(binomial_observed, binomial_n, binomial_p)
  binomial_range <- stats::pbinom(binomial_interval[["upper"]],
                                  binomial_n, binomial_p) -
                    stats::pbinom(binomial_interval[["lower"]] - 1L,
                                  binomial_n, binomial_p)
  binomial_tail <- stats::pbinom(binomial_observed - 1L,
                                 binomial_n, binomial_p, lower.tail = FALSE)

  # Y counts events in a fixed exposure period at a constant mean
  # count of 8. Exact P(Y=10), inclusive P(7<=Y<=10), and P(Y>=10)
  # illustrate the Poisson mass function and cumulative probabilities.
  poisson_lambda <- 8
  poisson_observed <- 10L
  poisson_interval <- c(lower = 7L, upper = 10L)
  poisson_point <- stats::dpois(poisson_observed, poisson_lambda)
  poisson_range <- stats::ppois(poisson_interval[["upper"]],
                               poisson_lambda) -
                   stats::ppois(poisson_interval[["lower"]] - 1L,
                                poisson_lambda)
  poisson_tail <- stats::ppois(poisson_observed - 1L, poisson_lambda,
                               lower.tail = FALSE)

  # ================================================================
  # 05 | CONTINUOUS INFERENCE AND COMPARATIVE TESTS
  # ================================================================
  null_sigma <- 4
  n <- 16L
  sample_mean <- 12
  reference_mean <- 10
  z <- (sample_mean - reference_mean) / (null_sigma / sqrt(n))
  alpha <- .05
  shift <- 2
  critical <- stats::qnorm(1 - alpha / 2)

  # ================================================================
  # 06 | RETURN REPRODUCIBLE RESULTS
  # ================================================================
  # Retain legacy result names so existing consumers remain compatible.
  # Separate point, bounded range, and upper-tail probabilities clearly.
  list(
    z = c(statistic = z, p_two_sided = 2 * stats::pnorm(-abs(z))),
    t = stats::t.test(x),
    welch = stats::t.test(A, B, var.equal = FALSE),
    pooled = stats::t.test(A, B, var.equal = TRUE),
    chisq = stats::chisq.test(counts, correct = FALSE),
    chisq_table = counts,
    anova = stats::aov(score ~ arm),
    welch_anova = stats::oneway.test(score ~ arm, var.equal = FALSE),
    binomial = stats::binom.test(binomial_observed, binomial_n,
                                 p = binomial_p, alternative = "greater"),
    binomial_point = binomial_point,
    binomial_range = binomial_range,
    binomial_interval = binomial_interval,
    binomial_tail = binomial_tail,
    poisson_point = poisson_point,
    poisson_range = poisson_range,
    poisson_interval = poisson_interval,
    poisson_tail = poisson_tail,
    clt = list(means_5 = means_5, means_50 = means_50,
               se_5 = 10 / sqrt(5), se_50 = 10 / sqrt(50)),
    power_normal = stats::pnorm(-critical - shift) +
                   stats::pnorm(critical - shift, lower.tail = FALSE)
  )
}

# ================================================================
# 07 | INTERACTIVE EXAMPLE (RUN AFTER SOURCING)
# ================================================================
# source("03_learning/examples/breast_cancer_distribution_lab.R")
# result <- breast_cancer_distribution_lab()
# result$binomial_point; result$binomial_range; result$binomial_tail
# result$poisson_point; result$poisson_range; result$poisson_tail
# summary(result$anova); result$clt$se_50
