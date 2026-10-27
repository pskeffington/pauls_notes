# CO-07: base R screening probability and independently seeded synthetic simulation.
# Invented data only. Not suitable for clinical screening or individual diagnosis.

probability <- function(value, label = "probability") {
  if (!is.numeric(value) || is.logical(value) || length(value) != 1L ||
      is.na(value) || !is.finite(value) || value < 0 || value > 1) {
    stop(sprintf("%s must be a finite probability in [0,1]", label), call. = FALSE)
  }
  as.numeric(value)
}

positive_size <- function(n) {
  if (!is.numeric(n) || is.logical(n) || length(n) != 1L || is.na(n) ||
      !is.finite(n) || n != floor(n) || n < 1 || n > 1000000) {
    stop("n must be a whole number from 1 to 1000000", call. = FALSE)
  }
  as.integer(n)
}

conditional <- function(joint, given) {
  a <- probability(joint, "joint"); b <- probability(given, "given")
  if (b == 0 || a > b) stop("undefined conditional probability", call. = FALSE)
  a / b
}

union_probability <- function(p_a, p_b, p_joint) {
  a <- probability(p_a, "P(A)"); b <- probability(p_b, "P(B)")
  i <- probability(p_joint, "P(A and B)")
  if (i > min(a, b) || i < max(0, a + b - 1)) {
    stop("invalid intersection for given marginals", call. = FALSE)
  }
  a + b - i
}

screening_probabilities <- function(prevalence, sensitivity, specificity) {
  pi <- probability(prevalence, "prevalence")
  se <- probability(sensitivity, "sensitivity")
  sp <- probability(specificity, "specificity")
  tp <- pi * se; fn <- pi * (1 - se)
  fp <- (1 - pi) * (1 - sp); tn <- (1 - pi) * sp
  positive <- tp + fp; negative <- fn + tn
  if (positive == 0 || negative == 0) {
    stop("PPV or NPV undefined for empty test-result group", call. = FALSE)
  }
  c(p_true_positive = tp, p_false_positive = fp,
    p_false_negative = fn, p_true_negative = tn,
    p_test_positive = positive, p_test_negative = negative,
    ppv = tp / positive, npv = tn / negative)
}

expected_screening_counts <- function(n, prevalence, sensitivity, specificity) {
  size <- positive_size(n)
  p <- screening_probabilities(prevalence, sensitivity, specificity)
  v <- round(size * p[c("p_true_positive", "p_false_positive",
                        "p_false_negative", "p_true_negative")], 12)
  names(v) <- sub("^p_", "expected_", names(v))
  v
}

probabilities_from_table <- function(tp, fp, fn, tn) {
  x <- c(tp, fp, fn, tn)
  if (!is.numeric(x) || any(!is.finite(x)) || any(x < 0) || any(x != floor(x))) {
    stop("table cells must be nonnegative integer counts", call. = FALSE)
  }
  if (any(c(tp + fn, fp + tn, tp + fp, fn + tn) == 0)) {
    stop("all conditional denominators must be positive", call. = FALSE)
  }
  c(sensitivity = tp/(tp + fn), specificity = tn/(fp + tn),
    ppv = tp/(tp + fp), npv = tn/(fn + tn))
}

simulate_screening <- function(n, prevalence, sensitivity, specificity, seed = 711L) {
  size <- positive_size(n)
  pi <- probability(prevalence, "prevalence")
  se <- probability(sensitivity, "sensitivity")
  sp <- probability(specificity, "specificity")
  if (!is.numeric(seed) || is.logical(seed) || length(seed) != 1L ||
      !is.finite(seed) || seed != floor(seed)) {
    stop("seed must be a finite integer", call. = FALSE)
  }
  set.seed(as.integer(seed))
  disease <- runif(size) < pi
  result <- runif(size) < ifelse(disease, se, 1 - sp)
  c(tp = sum(disease & result), fp = sum(!disease & result),
    fn = sum(disease & !result), tn = sum(!disease & !result))
}

check_error <- function(expr) {
  did_error <- tryCatch({ force(expr); FALSE }, error = function(e) TRUE)
  if (!did_error) stop("expected invalid-input rejection", call. = FALSE)
}

if (sys.nframe() == 0L) {
  low <- screening_probabilities(.01, .9, .95)
  high <- screening_probabilities(.05, .9, .95)
  counts <- expected_screening_counts(10000, .01, .9, .95)
  table <- probabilities_from_table(90, 495, 10, 9405)
  stopifnot(isTRUE(all.equal(unname(counts), c(90, 495, 10, 9405))),
            isTRUE(all.equal(low[["ppv"]], 90/585)),
            isTRUE(all.equal(low[["npv"]], 9405/9415)),
            isTRUE(all.equal(high[["ppv"]], 450/925)),
            high[["ppv"]] > low[["ppv"]],
            isTRUE(all.equal(table[["sensitivity"]], .9)),
            isTRUE(all.equal(table[["specificity"]], .95)),
            isTRUE(all.equal(conditional(.1, .25), .4)),
            isTRUE(all.equal(conditional(.1, .2), .5)),
            isTRUE(all.equal(union_probability(.2, .25, .1), .35)))
  a <- simulate_screening(10000, .01, .9, .95, seed = 711L)
  b <- simulate_screening(10000, .01, .9, .95, seed = 711L)
  stopifnot(identical(a, b), sum(a) == 10000, a[["tp"]] < 200, a[["fp"]] < 700)
  check_error(screening_probabilities(0, 1, 1))
  check_error(screening_probabilities(-.1, .9, .9))
  check_error(expected_screening_counts(0, .01, .9, .95))
  check_error(probabilities_from_table(0, 0, 0, 0))
  check_error(conditional(.2, 0))
  check_error(union_probability(.8, .8, .1))
  check_error(simulate_screening(10, .1, .9, .9, seed = NA_real_))
  print(list(low_prevalence = low, higher_prevalence = high,
             expected_counts = counts, seeded_counts = a))
  cat("CO-07 R fixtures and negative-input checks passed\n")
}
