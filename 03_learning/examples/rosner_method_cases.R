# Rosner-aligned method-selection teaching cases. Synthetic values only.
# Base R by default. Sourcing defines functions; no data reads or writes.
# Optional survival example requires the survival package.

rosner_teaching_cases <- function() {
  # Distinct independent subjects, continuous measures.
  independent <- data.frame(
    id = 1:12,
    group = rep(c("reference", "comparison"), each = 6),
    marker = c(10, 11, 12, 13, 14, 15, 12, 14, 16, 18, 20, 22)
  )
  independent$group <- factor(independent$group,
                              levels = c("reference", "comparison"))
  stopifnot(!anyDuplicated(independent$id), !anyNA(independent$marker))
  ref <- independent$marker[independent$group == "reference"]
  cmp <- independent$marker[independent$group == "comparison"]
  welch <- stats::t.test(cmp, ref, var.equal = FALSE, conf.level = .95)

  # One before/after change per patient ID: positive means after minus before.
  paired <- data.frame(
    id = 1:8,
    before = c(8, 9, 10, 11, 12, 13, 14, 15),
    after = c(9, 10, 12, 11, 14, 15, 15, 18)
  )
  stopifnot(!anyDuplicated(paired$id), complete.cases(paired))
  delta <- paired$after - paired$before
  paired_test <- stats::t.test(delta, mu = 0)
  # Raw subject IDs are keys, not samples for numerical analysis.

  # Fixed number of Bernoulli responses; one-sided, >=k includes observed k.
  k <- 36L; n <- 80L; p0 <- 0.35
  binomial <- stats::binom.test(k, n, p = p0, alternative = "greater")
  binomial_tail <- stats::pbinom(k - 1L, n, p0, lower.tail = FALSE)

  # Independent group-by-outcome counts (no invented patient-level rows).
  table_counts <- matrix(c(14, 6, 9, 11), nrow = 2L, byrow = TRUE,
                         dimnames = list(group = c("A", "B"),
                                         response = c("yes", "no")))
  chisq <- stats::chisq.test(table_counts, correct = FALSE)
  fisher <- stats::fisher.test(table_counts)

  # Uniform reference rate / person-time only for illustration.
  exposure_py <- 20000
  baseline_rate <- 40 / 100000
  lambda <- baseline_rate * exposure_py
  event_count <- 10L
  poisson_upper_tail <- stats::ppois(event_count - 1L, lambda,
                                     lower.tail = FALSE)

  list(
    independent = list(n = nrow(independent),
                       reference_n = length(ref), comparison_n = length(cmp),
                       mean_difference = unname(mean(cmp) - mean(ref)),
                       test = welch),
    paired = list(n_pairs = nrow(paired), mean_change = mean(delta),
                  test = paired_test),
    binomial = list(k = k, n = n, p0 = p0, test = binomial,
                    upper_tail = binomial_tail),
    categorical = list(counts = table_counts, chisq = chisq, fisher = fisher),
    poisson = list(events_at_least = event_count, exposure_person_years = exposure_py,
                   expected_count = lambda, upper_tail = poisson_upper_tail)
  )
}

rosner_survival_case <- function() {
  if (!requireNamespace("survival", quietly = TRUE))
    stop("Install the survival package to run this optional synthetic case.",
         call. = FALSE)
  example <- data.frame(
    id = 1:10,
    months = c(4, 7, 8, 10, 12, 4, 6, 9, 11, 13),
    event = c(1L, 0L, 1L, 1L, 0L, 1L, 1L, 0L, 1L, 0L),
    group = factor(rep(c("reference", "comparison"), each = 5L))
  )
  stopifnot(!anyDuplicated(example$id), all(example$months > 0),
            all(example$event %in% c(0L, 1L)))
  s <- survival::Surv(example$months, example$event)
  list(km = survival::survfit(s ~ group, data = example),
       log_rank = survival::survdiff(s ~ group, data = example),
       n = nrow(example))
}

# Example run (opt-in):
# source("06_RESOURCES/R/biomedical_test_selector.R")
# source("06_RESOURCES/R/rosner_method_crosswalk.R")
# decision <- biomedical_method_decision("continuous", n_groups = 2L,
#                                        include_rosner = TRUE)
# print(decision)
# cases <- rosner_teaching_cases()
# cases$independent$test
# cases$paired$test
# cases$binomial$upper_tail
# cases$categorical$counts
# cases$poisson$upper_tail
# survival_results <- rosner_survival_case()  # only if installed
