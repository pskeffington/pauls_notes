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
  # The lower bound involves subtraction; allow only machine-scale roundoff.
  tolerance <- 8 * .Machine$double.eps
  if (i > min(a, b) || i < max(0, a + b - 1) - tolerance) {
    stop("invalid intersection for given marginals", call. = FALSE)
  }
  min(1, a + b - i)
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
  # Retain full precision; rounding belongs to presentation, not returned data.
  v <- size * p[c("p_true_positive", "p_false_positive",
                  "p_false_negative", "p_true_negative")]
  names(v) <- sub("^p_", "expected_", names(v))
  v
}

probabilities_from_table <- function(tp, fp, fn, tn) {
  # Validate each cell before c() could coerce logicals or flatten vectors.
  valid_cell <- function(value) {
    is.numeric(value) && !is.complex(value) && !is.logical(value) &&
      length(value) == 1L && !is.na(value) && is.finite(value) &&
      value >= 0 && value == floor(value)
  }
  cells <- list(tp, fp, fn, tn)
  if (!all(vapply(cells, valid_cell, logical(1)))) {
    stop("each table cell must be one finite nonnegative integer count", call. = FALSE)
  }
  # Numeric storage prevents integer overflow when valid integer cells are added.
  x <- vapply(cells, as.numeric, numeric(1))
  tp <- x[1]; fp <- x[2]; fn <- x[3]; tn <- x[4]
  denominators <- c(tp + fn, fp + tn, tp + fp, fn + tn)
  if (any(!is.finite(denominators)) || any(denominators <= 0)) {
    stop("all conditional denominators must be finite and positive", call. = FALSE)
  }
  c(sensitivity = tp/(tp + fn), specificity = tn/(fp + tn),
    ppv = tp/(tp + fp), npv = tn/(fn + tn))
}

simulate_screening <- function(n, prevalence, sensitivity, specificity, seed = 711L) {
  size <- positive_size(n)
  pi <- probability(prevalence, "prevalence")
  se <- probability(sensitivity, "sensitivity")
  sp <- probability(specificity, "specificity")
  # R requires a representable integer seed; Python accepts larger integers.
  # Matching seeds preserve replay within a language, not cross-language draws.
  if (!is.numeric(seed) || is.complex(seed) || is.logical(seed) ||
      length(seed) != 1L || !is.finite(seed) || seed != floor(seed) ||
      abs(seed) > .Machine$integer.max) {
    stop("seed must be an integer from -2147483647 to 2147483647", call. = FALSE)
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
  high_counts <- expected_screening_counts(10000, .05, .9, .95)
  table <- probabilities_from_table(90, 495, 10, 9405)
  stopifnot(isTRUE(all.equal(unname(counts), c(90, 495, 10, 9405))),
            isTRUE(all.equal(unname(high_counts), c(450, 475, 50, 9025))),
            isTRUE(all.equal(low[["ppv"]], 90/585)),
            isTRUE(all.equal(low[["npv"]], 9405/9415)),
            isTRUE(all.equal(high[["ppv"]], 450/925)),
            isTRUE(all.equal(high[["npv"]], 9025/9075)),
            high[["ppv"]] > low[["ppv"]],
            isTRUE(all.equal(table[["sensitivity"]], .9)),
            isTRUE(all.equal(table[["specificity"]], .95)),
            isTRUE(all.equal(conditional(.1, .25), .4)),
            isTRUE(all.equal(conditional(.1, .2), .5)),
            isTRUE(all.equal(union_probability(.2, .25, .1), .35)))
  # Match the independently verified rational tables and retain tiny expectations.
  tiny <- expected_screening_counts(1, 1e-15, .5, .5)
  perfect <- probabilities_from_table(1, 0, 0, 1)
  large <- probabilities_from_table(.Machine$integer.max, .Machine$integer.max,
                                    .Machine$integer.max, .Machine$integer.max)
  stopifnot(union_probability(.7, .4, .1) == 1,
            union_probability(0, 1, 0) == 1,
            union_probability(0, 0, 0) == 0,
            tiny[["expected_true_positive"]] > 0,
            abs(tiny[["expected_true_positive"]] / 5e-16 - 1) < 1e-12,
            abs(tiny[["expected_false_negative"]] / 5e-16 - 1) < 1e-12,
            all(perfect == 1), all(large == .5),
            screening_probabilities(.1, 1, 1)[["ppv"]] == 1,
            screening_probabilities(0, .9, .95)[["ppv"]] == 0,
            simulate_screening(10, 0, .9, 1)[["tn"]] == 10)
  a <- simulate_screening(10000, .01, .9, .95, seed = 711L)
  b <- simulate_screening(10000, .01, .9, .95, seed = 711L)
  stopifnot(identical(a, b), sum(a) == 10000, a[["tp"]] < 200, a[["fp"]] < 700)
  check_error(screening_probabilities(0, 1, 1))
  check_error(screening_probabilities(-.1, .9, .9))
  check_error(expected_screening_counts(0, .01, .9, .95))
  check_error(probabilities_from_table(0, 0, 0, 0))
  # Each argument must stay a scalar count; coercion must not conceal bad input.
  invalid_cells <- list(TRUE, c(1, 2), numeric(0), NA_real_, Inf, -1, 1.5, "1", 1 + 1i)
  for (cell in invalid_cells) {
    for (position in seq_len(4L)) {
      args <- list(1, 2, 3, 4)
      args[[position]] <- cell
      check_error(do.call(probabilities_from_table, args))
    }
  }
  check_error(probabilities_from_table(1e308, 1e308, 1e308, 1e308))
  check_error(conditional(.2, 0))
  check_error(union_probability(.8, .8, .1))
  check_error(union_probability(.7, .4, .099999))
  check_error(simulate_screening(10, .1, .9, .9, seed = NA_real_))
  check_error(simulate_screening(10, .1, .9, .9, seed = .Machine$integer.max + 1))
  check_error(simulate_screening(10, .1, .9, .9, seed = -.Machine$integer.max - 1))
  print(list(low_prevalence = low, higher_prevalence = high,
             expected_counts = counts, seeded_counts = a))
  cat("CO-07 R fixtures and negative-input checks passed\n")
}
