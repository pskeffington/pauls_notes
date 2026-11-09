# Data-neutral, ID-aligned paired continuous mean comparison.
# Source to define functions; no test or file operation runs on import.

paired_mean_change <- function(data, id, visit, outcome,
                               before_level, after_level, alpha = 0.05) {
  required <- c(id, visit, outcome)
  valid_label <- function(x) is.character(x) && length(x) == 1L &&
    !is.na(x) && nzchar(trimws(x))
  if (!is.data.frame(data) || nrow(data) < 2L ||
      anyNA(names(data)) || anyDuplicated(names(data)) ||
      any(!nzchar(trimws(names(data)))))
    stop("data must have nonblank, distinct column names and rows.", call. = FALSE)
  if (!all(vapply(as.list(c(required, before_level, after_level)),
                  valid_label, logical(1))) ||
      anyDuplicated(required) ||
      identical(before_level, after_level) ||
      !all(required %in% names(data)))
    stop("Supply distinct existing columns and distinct visit levels.", call. = FALSE)
  if (!is.numeric(data[[outcome]]) || !is.null(dim(data[[outcome]])) ||
      any(is.infinite(data[[outcome]])) || any(is.nan(data[[outcome]])))
    stop("outcome must be numeric; missing values are allowed.", call. = FALSE)
  if (!is.numeric(alpha) || length(alpha) != 1L ||
      is.na(alpha) || !is.finite(alpha) || alpha <= 0 || alpha >= 1)
    stop("alpha must be strictly between 0 and 1.", call. = FALSE)

  subject <- as.character(data[[id]])
  occasion <- as.character(data[[visit]])
  if (anyNA(subject) || any(!nzchar(trimws(subject))) ||
      anyNA(occasion) || any(!nzchar(trimws(occasion))))
    stop("id and visit cannot be missing or blank.", call. = FALSE)
  if (!setequal(unique(occasion), c(before_level, after_level)))
    stop("Visit values must match exactly the named before/after levels.",
         call. = FALSE)
  if (anyDuplicated(paste(subject, occasion, sep = "\r")))
    stop("Repeated subject-by-visit key; cannot align pairs.", call. = FALSE)

  before <- occasion == before_level
  after <- occasion == after_level
  before_id <- subject[before]
  after_id <- subject[after]
  before_values <- data[[outcome]][before]
  after_values <- data[[outcome]][after]
  ids <- unique(subject)

  before_index <- match(ids, before_id)
  after_index <- match(ids, after_id)
  b <- before_values[before_index]
  a <- after_values[after_index]
  complete <- !is.na(b) & !is.na(a)
  differences <- a[complete] - b[complete]

  if (length(differences) < 2L || !is.finite(stats::sd(differences)) ||
      stats::sd(differences) <= 0)
    stop("At least two complete pairs and nonzero difference SD required.",
         call. = FALSE)

  test <- stats::t.test(differences, mu = 0,
                        alternative = "two.sided", conf.level = 1 - alpha)
  result <- list(
    method = "Paired two-sided t-test of after-minus-before change",
    id = id, visit = visit, outcome = outcome,
    before_level = before_level, after_level = after_level,
    contrast = paste(after_level, "-", before_level),
    alpha = alpha, n_rows = nrow(data),
    n_subjects_total = length(ids),
    n_complete_pairs = sum(complete),
    n_excluded_subjects = sum(!complete),
    n_missing_measurements = sum(is.na(data[[outcome]])),
    n_before_observed = sum(!is.na(before_values)),
    n_after_observed = sum(!is.na(after_values)),
    mean_change = mean(differences),
    sd_change = stats::sd(differences),
    t_statistic = unname(test$statistic),
    degrees_freedom = unname(test$parameter),
    p_value = test$p.value,
    ci_lower = unname(test$conf.int[1]),
    ci_upper = unname(test$conf.int[2]),
    reject_null = isTRUE(test$p.value < alpha),
    test = test
  )
  class(result) <- "paired_mean_change"
  result
}

# The figure uses the same computed mean and CI as the test object.
plot_paired_mean_change <- function(result, outcome_label = NULL, unit = NULL) {
  if (!inherits(result, "paired_mean_change"))
    stop("Expected paired_mean_change result.", call. = FALSE)
  if (!requireNamespace("ggplot2", quietly = TRUE))
    stop("ggplot2 is required.", call. = FALSE)
  if (!is.null(outcome_label) &&
      (!is.character(outcome_label) || length(outcome_label) != 1L ||
       is.na(outcome_label) || !nzchar(trimws(outcome_label))))
    stop("outcome_label must be a nonblank string.", call. = FALSE)
  if (!is.null(unit) &&
      (!is.character(unit) || length(unit) != 1L ||
       is.na(unit) || !nzchar(trimws(unit))))
    stop("unit must be a nonblank string.", call. = FALSE)
  label <- if (is.null(outcome_label)) result$outcome else outcome_label
  d <- data.frame(
    contrast = result$contrast,
    mean_change = result$mean_change,
    lower = result$ci_lower,
    upper = result$ci_upper
  )
  ggplot2::ggplot(d, ggplot2::aes(x = .data$mean_change, y = .data$contrast)) +
    ggplot2::geom_vline(xintercept = 0, linetype = "dashed",
                        color = "#808080") +
    ggplot2::geom_segment(
      ggplot2::aes(x = .data$lower, xend = .data$upper,
                   y = .data$contrast, yend = .data$contrast),
      color = "#0072B2", linewidth = 0.95
    ) +
    ggplot2::geom_point(size = 3, color = "#0072B2") +
    ggplot2::labs(
      title = "Paired mean change",
      subtitle = sprintf("%d complete pairs; %d subjects excluded",
                         result$n_complete_pairs, result$n_excluded_subjects),
      x = paste0("After-minus-before mean change in ", label,
                 if (is.null(unit)) "" else paste0(" (", unit, ")")),
      y = NULL,
      caption = sprintf(
        "Point = paired mean change; line = %.0f%% t CI; dashed = zero change.\nPairs are aligned by subject ID; independence across subjects must be verified.",
        100 * (1 - result$alpha)
      )
    ) + ggplot2::theme_classic(base_size = 12) +
    ggplot2::theme(plot.caption = ggplot2::element_text(hjust = 0))
}
