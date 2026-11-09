# CO-05: base-R arithmetic checks on invented oncology examples.
# Educational only; no patient data, treatment guidance, or external packages.

finite_scalar <- function(x, name, positive = FALSE) {
  if (!is.numeric(x) || is.logical(x) || length(x) != 1L ||
      is.na(x) || !is.finite(x) || (positive && x <= 0)) {
    stop(sprintf("%s must be a finite numeric scalar%s", name,
                 if (positive) " > 0" else ""), call. = FALSE)
  }
  as.numeric(x)
}

count_scalar <- function(x, name) {
  number <- finite_scalar(x, name)
  if (number < 0 || number != floor(number)) {
    stop(sprintf("%s must be a nonnegative integer count", name), call. = FALSE)
  }
  number
}

proportion <- function(part, whole) {
  n <- count_scalar(part, "part")
  d <- count_scalar(whole, "whole")
  if (d == 0 || n > d) stop("proportion: invalid denominator or numerator", call. = FALSE)
  n / d
}

incidence_per_100k <- function(events, population) {
  e <- count_scalar(events, "events")
  p <- count_scalar(population, "population")
  if (p == 0) stop("population denominator must be positive", call. = FALSE)
  e / p * 1e5
}

implied_events <- function(rate_per_100k, population) {
  r <- finite_scalar(rate_per_100k, "rate_per_100k")
  p <- count_scalar(population, "population")
  if (r < 0 || p == 0) stop("invalid rate or denominator", call. = FALSE)
  r * p / 1e5
}

person_time_rate_per_1000 <- function(events, person_years) {
  e <- count_scalar(events, "events")
  py <- finite_scalar(person_years, "person_years", positive = TRUE)
  e / py * 1e3
}

absolute_proportion_difference <- function(p_a, p_b) {
  a <- finite_scalar(p_a, "p_a")
  b <- finite_scalar(p_b, "p_b")
  if (any(c(a, b) < 0 | c(a, b) > 1))
    stop("proportions must be between 0 and 1", call. = FALSE)
  a - b
}

ratio_of_proportions <- function(p_a, p_b) {
  a <- finite_scalar(p_a, "p_a")
  b <- finite_scalar(p_b, "p_b", positive = TRUE)
  if (a < 0 || a > 1 || b > 1)
    stop("invalid proportion ratio", call. = FALSE)
  a / b
}

cm_to_mm <- function(value_cm) {
  value <- finite_scalar(value_cm, "value_cm")
  if (value < 0) stop("length must be nonnegative", call. = FALSE)
  value * 10
}

ng_ml_to_pg_ml <- function(value_ng_ml) {
  value <- finite_scalar(value_ng_ml, "value_ng_ml")
  if (value < 0) stop("concentration must be nonnegative", call. = FALSE)
  value * 1e3
}

log2_fold_change <- function(numerator, reference) {
  a <- finite_scalar(numerator, "numerator", positive = TRUE)
  b <- finite_scalar(reference, "reference", positive = TRUE)
  log2(a) - log2(b)
}

idealized_doubling <- function(initial, elapsed_days, doubling_days) {
  n <- finite_scalar(initial, "initial", positive = TRUE)
  t <- finite_scalar(elapsed_days, "elapsed_days")
  d <- finite_scalar(doubling_days, "doubling_days", positive = TRUE)
  if (t < 0) stop("elapsed days must be nonnegative", call. = FALSE)
  result <- n * 2^(t / d)
  if (!is.finite(result)) stop("exponential result is not finite", call. = FALSE)
  result
}

z_score <- function(value, mean, standard_deviation) {
  x <- finite_scalar(value, "value")
  mu <- finite_scalar(mean, "mean")
  sd <- finite_scalar(standard_deviation, "standard_deviation", positive = TRUE)
  (x - mu) / sd
}

fixtures <- function() {
  a <- proportion(18, 60)
  b <- proportion(12, 60)
  c(population_incidence_per_100k = incidence_per_100k(24, 80000),
    implied_incident_events = implied_events(30, 80000),
    person_time_rate_per_1000_py = person_time_rate_per_1000(12, 600),
    group_a_response_proportion = a,
    group_b_response_proportion = b,
    response_percentage_point_difference = 100 * absolute_proportion_difference(a, b),
    response_ratio = ratio_of_proportions(a, b),
    lesion_length_mm = cm_to_mm(2.5),
    analyte_pg_ml = ng_ml_to_pg_ml(0.8),
    expression_log2_fold_change = log2_fold_change(80, 20),
    abstract_doubled_quantity = idealized_doubling(100, 60, 30),
    standard_score = z_score(75, 60, 10))
}

assert_error <- function(expression) {
  caught <- tryCatch({ force(expression); FALSE }, error = function(e) TRUE)
  if (!caught) stop("expected invalid-input error", call. = FALSE)
}

if (sys.nframe() == 0L) {
  results <- fixtures()
  expected <- c(population_incidence_per_100k = 30,
                implied_incident_events = 24,
                person_time_rate_per_1000_py = 20,
                group_a_response_proportion = 0.3,
                group_b_response_proportion = 0.2,
                response_percentage_point_difference = 10,
                response_ratio = 1.5,
                lesion_length_mm = 25,
                analyte_pg_ml = 800,
                expression_log2_fold_change = 2,
                abstract_doubled_quantity = 400,
                standard_score = 1.5)
  stopifnot(identical(names(results), names(expected)),
            isTRUE(all.equal(unname(results), unname(expected), tolerance = 1e-12)))
  assert_error(proportion(2, 0))
  assert_error(proportion(4, 3))
  assert_error(incidence_per_100k(-1, 1000))
  assert_error(person_time_rate_per_1000(1, 0))
  assert_error(log2_fold_change(0, 2))
  assert_error(ratio_of_proportions(0.2, 0))
  assert_error(idealized_doubling(10, 5, 0))
  assert_error(z_score(75, 60, 0))
  print(results)
  cat("CO-05 R arithmetic and negative-input checks passed\n")
}
