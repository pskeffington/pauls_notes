# Synthetic-safe biomedical narratives; sourcing defines functions only.
# Data stay outside this module. No clinical, causal, or national inference.

pn_validate_groups <- function(data, value, group) {
  if (!is.data.frame(data) || !all(c(value, group) %in% names(data)))
    stop("Missing data frame or requested columns.", call. = FALSE)
  x <- data[[value]]
  if (!is.numeric(x) || any(is.infinite(x)))
    stop("Outcome must be numeric without infinite values.", call. = FALSE)
  if (anyNA(data[[group]]))
    stop("Group labels contain NA; report/exclude explicitly before analysis.", call. = FALSE)
  invisible(TRUE)
}

pn_group_descriptives <- function(data, value, group) {
  pn_validate_groups(data, value, group)
  keys <- unique(as.character(data[[group]]))
  if (!length(keys)) stop("No groups.", call. = FALSE)
  do.call(rbind, lapply(keys, function(key) {
    raw <- data[[value]][as.character(data[[group]]) == key]
    x <- raw[!is.na(raw)]
    n <- length(x)
    q <- if (n) stats::quantile(x, c(.25, .75), names = FALSE, type = 7) else c(NA_real_, NA_real_)
    data.frame(group = key, total_n = length(raw), n = n,
               missing_n = length(raw) - n,
               mean = if (n) mean(x) else NA_real_,
               sd = if (n > 1L) stats::sd(x) else NA_real_,
               median = if (n) stats::median(x) else NA_real_,
               q1 = q[1], q3 = q[2], iqr = q[2] - q[1],
               min = if (n) min(x) else NA_real_,
               max = if (n) max(x) else NA_real_))
  }))
}

pn_geometric_descriptives <- function(data, value, group) {
  pn_validate_groups(data, value, group)
  keys <- unique(as.character(data[[group]]))
  if (!length(keys)) stop("No groups.", call. = FALSE)
  do.call(rbind, lapply(keys, function(key) {
    raw <- data[[value]][as.character(data[[group]]) == key]
    observed <- raw[!is.na(raw)]
    positive <- observed[observed > 0]
    data.frame(group = key, total_n = length(raw), positive_n = length(positive),
               missing_n = sum(is.na(raw)), nonpositive_n = sum(observed <= 0),
               geometric_mean = if (length(positive)) exp(mean(log(positive))) else NA_real_)
  }))
}

pn_normality_diagnostics <- function(x, extra = FALSE) {
  if (!is.numeric(x) || any(is.infinite(x))) stop("x must be finite numeric or NA.")
  x <- x[!is.na(x)]
  n <- length(x)
  valid <- n >= 3L && n <= 5000L && length(unique(x)) >= 2L
  sh <- if (valid) stats::shapiro.test(x) else NULL
  out <- list(n = n, shapiro_w = if (valid) unname(sh$statistic) else NA_real_,
              shapiro_p = if (valid) sh$p.value else NA_real_)
  if (isTRUE(extra)) {
    if (!requireNamespace("nortest", quietly = TRUE))
      stop("Install nortest to request Anderson-Darling and Lilliefors diagnostics.")
    adequate <- n >= 8L && length(unique(x)) >= 2L
    out$ad_p <- if (adequate) nortest::ad.test(x)$p.value else NA_real_
    out$lilliefors_p <- if (adequate) nortest::lillie.test(x)$p.value else NA_real_
  }
  out
}

pn_sampling_mean <- function(x, assumed_mean, expected_n = NULL) {
  if (!is.numeric(x) || any(is.infinite(x)) || length(assumed_mean) != 1L ||
      !is.numeric(assumed_mean) || !is.finite(assumed_mean))
    stop("Invalid observations or assumed mean.", call. = FALSE)
  x <- x[!is.na(x)]
  n <- length(x)
  if (n < 2L || (!is.null(expected_n) && n != expected_n))
    stop("Sample size does not match expectation.", call. = FALSE)
  sd_x <- stats::sd(x)
  se <- sd_x / sqrt(n)
  if (!is.finite(se) || se <= 0) stop("Positive finite estimated SE required.")
  observed <- mean(x)
  z <- (observed - assumed_mean) / se
  tail <- if (z < 0) "left" else if (z > 0) "right" else "at_center"
  p <- if (z < 0) stats::pnorm(z) else if (z > 0)
    stats::pnorm(z, lower.tail = FALSE) else 0.5
  list(n = n, assumed_mean = assumed_mean, observed_mean = observed,
       sample_sd = sd_x, estimated_se = se, z = z, tail = tail,
       one_sided_probability = p, approximation = "normal with plug-in SE")
}

pn_probability_label <- function(p, digits = 3L) {
  if (!is.numeric(p) || length(p) != 1L || !is.finite(p) || p < 0 || p > 1)
    stop("Probability must be finite between 0 and 1.")
  if (p > 0 && p < 0.001) format(p, scientific = TRUE, digits = digits)
  else formatC(p, format = "f", digits = digits)
}

pn_narrate_group <- function(stats, variable, unit, digits = 2L) {
  required <- c("group", "n", "total_n", "missing_n", "mean", "sd", "median", "q1", "q3")
  if (!is.data.frame(stats) || !all(required %in% names(stats)))
    stop("Use pn_group_descriptives() output.", call. = FALSE)
  vapply(seq_len(nrow(stats)), function(i) {
    r <- stats[i, ]
    if (r$n < 2L) return(sprintf("%s: n = %d; insufficient observations for SD.", r$group, r$n))
    sprintf("%s: %s (n = %d/%d; %d missing), mean %.2f %s (SD %.2f), median %.2f [Q1 %.2f, Q3 %.2f] %s. Descriptive sample estimates only.",
            variable, r$group, r$n, r$total_n, r$missing_n,
            r$mean, unit, r$sd, r$median, r$q1, r$q3, unit)
  }, character(1))
}

pn_narrate_geometric <- function(stats, variable = "Biomarker", unit = "mg/L") {
  needed <- c("group", "positive_n", "missing_n", "nonpositive_n", "geometric_mean")
  if (!is.data.frame(stats) || !all(needed %in% names(stats)))
    stop("Use pn_geometric_descriptives() output.")
  vapply(seq_len(nrow(stats)), function(i) {
    r <- stats[i, ]
    if (!is.finite(r$geometric_mean))
      return(sprintf("%s: no positive observations; geometric mean undefined.", r$group))
    sprintf("%s: %s geometric mean %.3f %s (positive n = %d; missing = %d; nonpositive excluded = %d). Descriptive only.",
            variable, r$group, r$geometric_mean, unit, r$positive_n,
            r$missing_n, r$nonpositive_n)
  }, character(1))
}

pn_narrate_sampling <- function(result, unit = "g/dL") {
  fields <- c("n", "assumed_mean", "observed_mean", "estimated_se", "tail", "one_sided_probability")
  if (!is.list(result) || !all(fields %in% names(result)))
    stop("Use pn_sampling_mean() output.")
  sprintf("Assuming a population mean of %.2f %s and an approximately normal sampling distribution (n = %d; plug-in SE %.4f %s), the %s-tail probability for an observed mean of %.3f %s or farther in that direction is %s. This is a model-conditional one-sided tail area, not the probability that the population assumption is true.",
          result$assumed_mean, unit, result$n, result$estimated_se, unit,
          result$tail, result$observed_mean, unit,
          pn_probability_label(result$one_sided_probability))
}
