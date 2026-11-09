# Generic, data-independent Welch two-sample mean comparison.
# Loading this module defines functions; it does not read data or run a test.
# Required for inference: base R stats. Optional for figures: ggplot2.
# The analyst must verify independent sampling units and study design.

welch_mean_comparison <- function(data, outcome, group,
                                  reference_level, comparison_level,
                                  subject_id = NULL, alpha = 0.05) {
  scalar_label <- function(x) {
    is.character(x) && length(x) == 1L && !is.na(x) &&
      nzchar(trimws(x))
  }

  if (!is.data.frame(data) || nrow(data) == 0L ||
      anyNA(names(data)) || anyDuplicated(names(data)) ||
      any(!nzchar(trimws(names(data)))))
    stop("data must be a nonempty data.frame with unique, nonblank columns.",
         call. = FALSE)

  labels <- c(outcome, group, reference_level, comparison_level)
  if (!all(vapply(as.list(labels), scalar_label, logical(1))) ||
      identical(outcome, group) || identical(reference_level, comparison_level))
    stop("Supply distinct, nonblank outcome, group, and group-level labels.",
         call. = FALSE)

  if (!is.null(subject_id) &&
      (!scalar_label(subject_id) || subject_id %in% c(outcome, group)))
    stop("subject_id must be a distinct, nonblank column name.", call. = FALSE)

  required_columns <- c(outcome, group, subject_id)
  if (!all(required_columns %in% names(data)))
    stop("Missing columns: ",
         paste(setdiff(required_columns, names(data)), collapse = ", "),
         call. = FALSE)

  if (!is.numeric(data[[outcome]]) || !is.null(dim(data[[outcome]])) ||
      any(is.infinite(data[[outcome]])) || any(is.nan(data[[outcome]])))
    stop("outcome must be a numeric vector without Inf or NaN; NA is allowed.",
         call. = FALSE)

  if (is.list(data[[group]]) || !is.atomic(data[[group]]))
    stop("group must be an atomic vector or factor.", call. = FALSE)

  if (!is.numeric(alpha) || length(alpha) != 1L ||
      is.na(alpha) || !is.finite(alpha) || alpha <= 0 || alpha >= 1)
    stop("alpha must be a finite number strictly between 0 and 1.",
         call. = FALSE)

  # Optional identifier validation is a data-quality check, not proof that
  # participants were independently sampled or that clustering is absent.
  if (!is.null(subject_id)) {
    ids <- as.character(data[[subject_id]])
    if (anyNA(ids) || any(!nzchar(trimws(ids))) || anyDuplicated(ids))
      stop("subject_id must identify every row uniquely without missing IDs.",
           call. = FALSE)
  }

  group_values <- as.character(data[[group]])
  observed_levels <- unique(group_values[!is.na(group_values)])
  specified_levels <- c(reference_level, comparison_level)
  if (length(observed_levels) != 2L ||
      !setequal(observed_levels, specified_levels))
    stop("Exactly two observed groups must match reference_level and comparison_level.",
         call. = FALSE)

  complete <- !is.na(group_values) & !is.na(data[[outcome]])
  values_for <- function(level) {
    data[[outcome]][complete & group_values == level]
  }

  reference_values <- values_for(reference_level)
  comparison_values <- values_for(comparison_level)
  if (length(reference_values) < 2L || length(comparison_values) < 2L)
    stop("Each group needs at least two complete observations.",
         call. = FALSE)

  summarize_group <- function(level, role, values) {
    n_total <- sum(!is.na(group_values) & group_values == level)
    quartiles <- as.numeric(stats::quantile(
      values, probs = c(0.25, 0.75), names = FALSE, type = 7
    ))
    data.frame(
      role = role, level = level,
      n_total = n_total, n_observed = length(values),
      n_missing = n_total - length(values),
      pct_missing = 100 * (n_total - length(values)) / n_total,
      mean = mean(values), sd = stats::sd(values),
      median = stats::median(values),
      q1 = quartiles[1], q3 = quartiles[2],
      iqr = quartiles[2] - quartiles[1],
      min = min(values), max = max(values),
      stringsAsFactors = FALSE
    )
  }

  group_summary <- rbind(
    summarize_group(reference_level, "reference", reference_values),
    summarize_group(comparison_level, "comparison", comparison_values)
  )
  rownames(group_summary) <- NULL

  # x - y determines the sign of the estimate and its confidence interval.
  # Do not depend on alphabetical factor levels or formula dispatch order.
  test <- stats::t.test(
    x = comparison_values, y = reference_values,
    alternative = "two.sided", var.equal = FALSE,
    conf.level = 1 - alpha
  )

  output <- list(
    method = "Welch independent two-sample t-test",
    outcome = outcome, group = group, subject_id = subject_id,
    reference_level = reference_level,
    comparison_level = comparison_level,
    contrast = paste(comparison_level, "-", reference_level),
    alpha = alpha,
    n_total = nrow(data),
    n_complete = sum(complete),
    n_excluded = sum(!complete),
    n_missing_outcome = sum(is.na(data[[outcome]])),
    n_missing_group = sum(is.na(group_values)),
    n_missing_both = sum(is.na(data[[outcome]]) & is.na(group_values)),
    id_uniqueness_checked = !is.null(subject_id),
    group_summary = group_summary,
    mean_difference = unname(test$estimate[1] - test$estimate[2]),
    ci_lower = unname(test$conf.int[1]),
    ci_upper = unname(test$conf.int[2]),
    t_statistic = unname(test$statistic),
    degrees_freedom = unname(test$parameter),
    p_value = test$p.value,
    reject_null = isTRUE(test$p.value < alpha),
    test = test
  )
  class(output) <- "welch_mean_comparison"
  output
}

# Full-precision results; round for display in knitr::kable, not computation.
welch_mean_result_table <- function(result) {
  if (!inherits(result, "welch_mean_comparison"))
    stop("result must be returned by welch_mean_comparison().", call. = FALSE)
  data.frame(
    contrast = result$contrast,
    n_complete = result$n_complete,
    mean_difference = result$mean_difference,
    t_statistic = result$t_statistic,
    degrees_freedom = result$degrees_freedom,
    p_value = result$p_value,
    ci_lower = result$ci_lower,
    ci_upper = result$ci_upper,
    alpha = result$alpha,
    decision = if (result$reject_null) "Reject H0" else "Fail to reject H0",
    stringsAsFactors = FALSE
  )
}

format_welch_mean_result <- function(result, digits = 3L) {
  if (!inherits(result, "welch_mean_comparison"))
    stop("result must be returned by welch_mean_comparison().", call. = FALSE)
  if (length(digits) != 1L || is.na(digits) ||
      !is.numeric(digits) || digits < 0 || digits != floor(digits))
    stop("digits must be a nonnegative integer.", call. = FALSE)
  template <- paste0(
    "Welch comparison (", result$contrast, "): mean difference %.",
    digits, "f; t(%.2f) = %.", digits,
    "f; p = %s; %.0f%% CI [%.", digits, "f, %.",
    digits, "f]. n = %d complete of %d; %d excluded. %s."
  )
  sprintf(
    template, result$mean_difference, result$degrees_freedom,
    result$t_statistic,
    format.pval(result$p_value, digits = 3L, eps = .Machine$double.eps),
    100 * (1 - result$alpha), result$ci_lower, result$ci_upper,
    result$n_complete, result$n_total, result$n_excluded,
    if (result$reject_null) "Reject H0" else "Fail to reject H0"
  )
}

plot_welch_mean_difference <- function(result, outcome_label = NULL,
                                       unit = NULL) {
  if (!inherits(result, "welch_mean_comparison"))
    stop("result must be returned by welch_mean_comparison().", call. = FALSE)
  if (!requireNamespace("ggplot2", quietly = TRUE))
    stop("ggplot2 is required for plotting.", call. = FALSE)
  if (!is.null(outcome_label) &&
      (!is.character(outcome_label) || length(outcome_label) != 1L ||
       is.na(outcome_label) || !nzchar(trimws(outcome_label))))
    stop("outcome_label must be a nonblank string.", call. = FALSE)
  if (!is.null(unit) &&
      (!is.character(unit) || length(unit) != 1L ||
       is.na(unit) || !nzchar(trimws(unit))))
    stop("unit must be a nonblank string when supplied.", call. = FALSE)

  quantity <- if (is.null(outcome_label)) result$outcome else outcome_label
  axis_title <- paste0(
    "Mean difference in ", quantity,
    if (is.null(unit)) "" else paste0(" (", unit, ")")
  )
  plot_data <- data.frame(
    contrast = result$contrast,
    estimate = result$mean_difference,
    lower = result$ci_lower, upper = result$ci_upper
  )

  ggplot2::ggplot(
    plot_data,
    ggplot2::aes(x = .data$estimate, y = .data$contrast)
  ) +
    ggplot2::geom_vline(
      xintercept = 0, linetype = "dashed", color = "#808080"
    ) +
    ggplot2::geom_segment(
      ggplot2::aes(
        x = .data$lower, xend = .data$upper,
        y = .data$contrast, yend = .data$contrast
      ),
      linewidth = 0.95, color = "#0072B2"
    ) +
    ggplot2::geom_point(
      size = 3.1, shape = 21, fill = "#0072B2", color = "white"
    ) +
    ggplot2::labs(
      title = "Independent-group mean difference",
      subtitle = sprintf(
        "%d complete observations; %d excluded",
        result$n_complete, result$n_excluded
      ),
      x = axis_title, y = NULL,
      caption = sprintf(
        "Point = comparison minus reference; line = %.0f%% Welch CI; dashed = null (0).\nIndependent sampling and study design require separate verification.",
        100 * (1 - result$alpha)
      )
    ) +
    ggplot2::theme_classic(base_size = 12) +
    ggplot2::theme(
      plot.title = ggplot2::element_text(face = "bold"),
      plot.caption = ggplot2::element_text(
        color = "#555555", hjust = 0
      )
    )
}
