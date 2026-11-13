# Synthetic probability and sampling laboratory. Sourcing has no side effects.
breast_cancer_distribution_lab <- function(seed = 7122026L, repetitions = 5000L) {
  if (length(seed) != 1L || !is.numeric(seed) || !is.finite(seed) ||
      seed != floor(seed) || length(repetitions) != 1L ||
      !is.numeric(repetitions) || !is.finite(repetitions) ||
      repetitions < 100L || repetitions != floor(repetitions))
    stop("Invalid seed or repetitions.", call. = FALSE)
  had_seed <- exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE)
  if (had_seed) old_seed <- get(".Random.seed", envir = .GlobalEnv)
  on.exit({
    if (had_seed) assign(".Random.seed", old_seed, envir = .GlobalEnv)
    else if (exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE))
      rm(".Random.seed", envir = .GlobalEnv)
  }, add = TRUE)
  set.seed(as.integer(seed))
  means_5 <- replicate(as.integer(repetitions), mean(stats::rexp(5L, rate = .1)))
  means_50 <- replicate(as.integer(repetitions), mean(stats::rexp(50L, rate = .1)))
  x <- c(8,10,10,12,12,14,14,16)
  A <- c(8,9,10,11,12,13)
  B <- c(9,11,13,15,17,19)
  score <- c(8,10,12, 10,12,14, 12,14,16)
  arm <- factor(rep(c("A","B","C"), each = 3L))
  counts <- matrix(c(30L,20L,20L,30L), nrow = 2L, byrow = TRUE,
                   dimnames = list(arm = c("A","B"),
                                   response = c("yes","no")))
  null_sigma <- 4; n <- 16; sample_mean <- 12; reference_mean <- 10
  z <- (sample_mean - reference_mean)/(null_sigma/sqrt(n))
  alpha <- .05; shift <- 2
  critical <- stats::qnorm(1-alpha/2)
  list(
    z = c(statistic = z, p_two_sided = 2 * stats::pnorm(-abs(z))),
    t = stats::t.test(x),
    welch = stats::t.test(A, B, var.equal = FALSE),
    pooled = stats::t.test(A, B, var.equal = TRUE),
    chisq = stats::chisq.test(counts, correct = FALSE),
    chisq_table = counts,
    anova = stats::aov(score ~ arm),
    welch_anova = stats::oneway.test(score ~ arm, var.equal = FALSE),
    binomial = stats::binom.test(36L,80L,p=.35, alternative="greater"),
    binomial_tail = stats::pbinom(35L,80L,.35,lower.tail=FALSE),
    poisson_tail = stats::ppois(9L,8,lower.tail=FALSE),
    clt = list(means_5 = means_5, means_50 = means_50,
               se_5 = 10/sqrt(5), se_50 = 10/sqrt(50)),
    power_normal = stats::pnorm(-critical-shift) +
                   stats::pnorm(critical-shift, lower.tail=FALSE)
  )
}

# Example:
# source("03_learning/examples/breast_cancer_distribution_lab.R")
# x <- breast_cancer_distribution_lab()
# x$z; x$t; x$chisq; summary(x$anova); x$power_normal
