# Dataset-neutral Welch heteroscedastic omnibus one-way ANOVA.
# No automatic post-hoc contrasts or study-specific data.

welch_oneway_comparison <- function(data, outcome, group, alpha = 0.05) {
  scalar <- function(x) is.character(x) && length(x) == 1L &&
    !is.na(x) && nzchar(trimws(x))
  if (!is.data.frame(data) || nrow(data) == 0L ||
      anyNA(names(data)) || anyDuplicated(names(data)) ||
      any(!nzchar(trimws(names(data)))))
    stop("data must be a nonempty data.frame with unique columns.", call. = FALSE)
  if (!scalar(outcome) || !scalar(group) || identical(outcome, group) ||
      !all(c(outcome, group) %in% names(data)))
    stop("outcome and group must name different existing columns.", call. = FALSE)
  if (!is.numeric(data[[outcome]]) || !is.null(dim(data[[outcome]])) ||
      any(is.infinite(data[[outcome]])) || any(is.nan(data[[outcome]])))
    stop("outcome must be numeric, finite where observed.", call. = FALSE)
  if (!is.numeric(alpha) || length(alpha) != 1L || !is.finite(alpha) ||
      alpha <= 0 || alpha >= 1)
    stop("alpha must be strictly between 0 and 1.", call. = FALSE)

  group_values <- as.character(data[[group]])
  observed_groups <- sort(unique(group_values[!is.na(group_values)]),
                          method = "radix")
  if (length(observed_groups) < 3L)
    stop("Welch one-way comparison requires at least three observed groups.",
         call. = FALSE)
  if (any(!nzchar(trimws(observed_groups))))
    stop("group labels cannot be blank.", call. = FALSE)

  complete <- !is.na(group_values) & !is.na(data[[outcome]])
  analysis <- data.frame(
    value = data[[outcome]][complete],
    group = factor(group_values[complete], levels = observed_groups)
  )
  summaries <- do.call(rbind, lapply(observed_groups, function(level) {
    total <- sum(!is.na(group_values) & group_values == level)
    values <- analysis$value[analysis$group == level]
    if (length(values) < 2L || stats::sd(values) <= 0)
      stop("Each group needs >=2 observations and positive sample variance.",
           call. = FALSE)
    qs <- as.numeric(stats::quantile(values, c(.25, .75),
                                     names = FALSE, type = 7))
    data.frame(
      group = level, n_total = total, n_observed = length(values),
      n_missing = total - length(values),
      mean = mean(values), sd = stats::sd(values),
      median = stats::median(values),
      q1 = qs[1], q3 = qs[2], iqr = qs[2] - qs[1],
      stringsAsFactors = FALSE
    )
  }))
  rownames(summaries) <- NULL
  test <- stats::oneway.test(value ~ group, data = analysis, var.equal = FALSE)
  result <- list(
    method = "Welch heteroscedastic one-way ANOVA",
    outcome = outcome, group = group, alpha = alpha,
    n_total = nrow(data), n_complete = sum(complete),
    n_excluded = sum(!complete),
    n_missing_outcome = sum(is.na(data[[outcome]])),
    n_missing_group = sum(is.na(group_values)),
    group_summary = summaries,
    f_statistic = unname(test$statistic),
    df_numerator = unname(test$parameter[1]),
    df_denominator = unname(test$parameter[2]),
    p_value = test$p.value,
    reject_null = isTRUE(test$p.value < alpha),
    pairwise_posthoc_performed = FALSE,
    test = test
  )
  class(result) <- "welch_oneway_comparison"
  result
}

# Descriptive group distributions only; omnibus ANOVA provides no pairwise CIs.
plot_welch_oneway_groups <- function(result, data,
                                    outcome_label = NULL, unit = NULL) {
  if (!inherits(result, "welch_oneway_comparison"))
    stop("Expected welch_oneway_comparison result.", call. = FALSE)
  if (!is.data.frame(data) ||
      !all(c(result$outcome, result$group) %in% names(data)))
    stop("data must contain result outcome and group columns.", call. = FALSE)
  if (!requireNamespace("ggplot2", quietly = TRUE))
    stop("ggplot2 required.", call. = FALSE)
  if (!is.null(outcome_label) &&
      (!is.character(outcome_label) || length(outcome_label) != 1L ||
       is.na(outcome_label) || !nzchar(trimws(outcome_label))))
    stop("outcome_label must be nonblank.", call. = FALSE)
  if (!is.null(unit) &&
      (!is.character(unit) || length(unit) != 1L ||
       is.na(unit) || !nzchar(trimws(unit))))
    stop("unit must be a nonblank string.", call. = FALSE)

  keep <- !is.na(data[[result$outcome]]) & !is.na(data[[result$group]])
  d <- data.frame(
    group = factor(as.character(data[[result$group]][keep]),
                   levels = result$group_summary$group),
    value = data[[result$outcome]][keep]
  )
  if (nrow(d) != result$n_complete ||
      !isTRUE(all.equal(
        as.numeric(tapply(d$value, d$group, mean)),
        result$group_summary$mean,
        tolerance = 1e-10, check.attributes = FALSE)))
    stop("Plot input does not match the result's observed group means.",
         call. = FALSE)

  # Eight Okabe-Ito colors; more groups need an explicitly revised palette.
  colors <- c("#0072B2", "#D55E00", "#009E73", "#CC79A7",
              "#E69F00", "#56B4E9", "#000000", "#F0E442")
  if (nlevels(d$group) > length(colors))
    stop("More than eight groups: assign and document an expanded palette.",
         call. = FALSE)
  palette <- stats::setNames(colors[seq_len(nlevels(d$group))],
                             levels(d$group))
  label <- if (is.null(outcome_label)) result$outcome else outcome_label
  ggplot2::ggplot(d, ggplot2::aes(x = .data$group, y = .data$value,
                                 fill = .data$group)) +
    ggplot2::geom_violin(alpha = 0.23, trim = TRUE, color = NA) +
    ggplot2::geom_boxplot(width = 0.17, fill = "white",
                          color = "#252525", outlier.shape = NA) +
    ggplot2::stat_summary(fun = mean, geom = "point", shape = 23,
                          size = 2.9, fill = "#252525", color = "white") +
    ggplot2::scale_fill_manual(values = palette, guide = "none") +
    ggplot2::labs(
      title = "Group distributions for omnibus Welch ANOVA",
      subtitle = sprintf("%d valid observations; %d excluded",
                         result$n_complete, result$n_excluded),
      x = result$group,
      y = paste0(label, if (is.null(unit)) "" else paste0(" (", unit, ")")),
      caption = "Violin = density, box = median/IQR, diamond = mean. Whiskers are not CIs.\nNo pairwise tests or pairwise confidence intervals are implied."
    ) + ggplot2::theme_classic(base_size = 12) +
    ggplot2::theme(plot.caption = ggplot2::element_text(hjust = 0))
}
