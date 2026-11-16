# Original instructional figures for biomedical data.
# No actions run on sourcing; this module does not modify historical plots.
# Source-linked method details: 02_biomedical_coding/METHODOLOGY_SOURCE_REFERENCES.md
# Numeric values in teaching examples are synthetic.
#
# Box: the five-number display uses explicit R quantile type 2 for Q1/Q3;
# median is an independent horizontal line and mean is a '+' marker. Whiskers
# terminate at observed values within 1.5*IQR. They are NOT confidence limits.

biostat_graph_validate_numeric <- function(x, label = "value") {
  if (!is.numeric(x) || !is.null(dim(x)) || is.complex(x) ||
      any(is.infinite(x)) || any(is.nan(x)))
    stop(label, " must be a numeric vector with finite observed values.", call. = FALSE)
  invisible(TRUE)
}

biostat_graph_require_ggplot2 <- function() {
  if (!requireNamespace("ggplot2", quietly = TRUE))
    stop("ggplot2 is required for this figure.", call. = FALSE)
  invisible(TRUE)
}

biostat_graph_box_stats <- function(data, value, group) {
  if (!is.data.frame(data) || anyDuplicated(names(data)) ||
      !all(c(value, group) %in% names(data)) || identical(value, group))
    stop("data must contain distinct, named value and group columns.", call. = FALSE)
  biostat_graph_validate_numeric(data[[value]], value)
  g <- data[[group]]
  if (!(is.factor(g) || is.character(g)))
    stop("group must be character or factor.", call. = FALSE)
  observed_groups <- if (is.factor(g)) levels(droplevels(g)) else
    sort(unique(as.character(g[!is.na(g)])), method = "radix")
  if (!length(observed_groups) || anyNA(observed_groups))
    stop("At least one nonmissing group is required.", call. = FALSE)
  results <- lapply(seq_along(observed_groups), function(i) {
    level <- observed_groups[i]
    raw <- data[[value]][!is.na(g) & as.character(g) == level]
    x <- raw[!is.na(raw)]
    if (!length(x))
      stop("Group has no observed numeric values: ", level, call. = FALSE)
    q <- unname(stats::quantile(x, c(.25, .50, .75), type = 2))
    iqr <- q[3] - q[1]
    kept <- x[x >= q[1] - 1.5*iqr & x <= q[3] + 1.5*iqr]
    if (!length(kept))
      stop("No observations within whisker limits.", call. = FALSE)
    data.frame(group = level, x = i, n_total = length(raw),
      n_observed = length(x), n_missing = sum(is.na(raw)),
      whisker_low = min(kept), q1 = q[1], median = q[2],
      q3 = q[3], whisker_high = max(kept), mean = mean(x),
      stringsAsFactors = FALSE)
  })
  result <- do.call(rbind, results)
  rownames(result) <- NULL
  result
}

biostat_graph_box <- function(data, value, group, unit,
                              title = "Distribution by group",
                              points = TRUE) {
  biostat_graph_require_ggplot2()
  if (!is.character(unit) || length(unit) != 1L ||
      is.na(unit) || !nzchar(trimws(unit)))
    stop("unit must be a documented nonempty string.", call. = FALSE)
  stats <- biostat_graph_box_stats(data, value, group)
  raw <- data.frame(
    group = factor(as.character(data[[group]]), levels = stats$group),
    value = data[[value]]
  )
  raw <- raw[!is.na(raw$group) & !is.na(raw$value), , drop = FALSE]
  xlabels <- stats::setNames(
    paste0(stats$group, "\n(n=", stats$n_observed, "; missing=", stats$n_missing, ")"),
    seq_len(nrow(stats))
  )
  p <- ggplot2::ggplot(stats) +
    ggplot2::geom_rect(
      ggplot2::aes(xmin = .data$x - .24, xmax = .data$x + .24,
                   ymin = .data$q1, ymax = .data$q3),
      fill = "#56B4E9", colour = "#222222", linewidth = .5
    ) +
    ggplot2::geom_segment(
      ggplot2::aes(x = .data$x - .24, xend = .data$x + .24,
                   y = .data$median, yend = .data$median),
      colour = "#111111", linewidth = .85
    ) +
    ggplot2::geom_segment(
      ggplot2::aes(x = .data$x, xend = .data$x,
                   y = .data$whisker_low, yend = .data$q1),
      linewidth = .5
    ) +
    ggplot2::geom_segment(
      ggplot2::aes(x = .data$x, xend = .data$x,
                   y = .data$q3, yend = .data$whisker_high),
      linewidth = .5
    ) +
    ggplot2::geom_segment(
      ggplot2::aes(x = .data$x - .10, xend = .data$x + .10,
                   y = .data$whisker_low, yend = .data$whisker_low),
      linewidth = .5
    ) +
    ggplot2::geom_segment(
      ggplot2::aes(x = .data$x - .10, xend = .data$x + .10,
                   y = .data$whisker_high, yend = .data$whisker_high),
      linewidth = .5
    )
  if (isTRUE(points))
    p <- p + ggplot2::geom_point(
      data = raw,
      ggplot2::aes(x = as.numeric(.data$group), y = .data$value),
      position = ggplot2::position_jitter(width = .055, height = 0, seed = 711),
      alpha = .28, colour = "#D55E00", size = .8,
      inherit.aes = FALSE
    )
  p <- p +
    ggplot2::geom_point(
      ggplot2::aes(x = .data$x, y = .data$mean),
      shape = 3, size = 3.8, stroke = .95, colour = "#000000"
    ) +
    ggplot2::scale_x_continuous(
      breaks = stats$x, labels = xlabels, expand = ggplot2::expansion(add = .45)
    ) +
    ggplot2::labs(title = title, x = group,
      y = paste0(value, " (", unit, ")"),
      caption = paste0(
        "Box: Q1–Q3 (quantile type 2); line: median; +: mean; ",
        "whiskers: observed values within 1.5×IQR. ",
        "Whiskers and boxes are not confidence intervals."
      )) +
    ggplot2::theme_classic(base_size = 12) +
    ggplot2::theme(plot.caption = ggplot2::element_text(hjust = 0))
  attr(p, "figure_statistics") <- stats
  p
}

biostat_graph_bar <- function(data, category, title = "Category frequencies",
                              show_missing = TRUE) {
  biostat_graph_require_ggplot2()
  if (!is.data.frame(data) || !is.character(category) ||
      length(category) != 1L || is.na(category) || !category %in% names(data))
    stop("category must be one data.frame column name.", call. = FALSE)
  values <- data[[category]]
  if (!(is.factor(values) || is.character(values)))
    stop("Categorical bar graphs require character or factor values.", call. = FALSE)
  labels <- as.character(values)
  if (any(labels[!is.na(labels)] == "(Missing)"))
    stop("The literal '(Missing)' label is reserved.", call. = FALSE)
  if (show_missing) labels[is.na(labels)] <- "(Missing)"
  else labels <- labels[!is.na(labels)]
  if (!length(labels)) stop("No categories to display.", call. = FALSE)
  counts <- as.data.frame(table(labels), stringsAsFactors = FALSE)
  names(counts) <- c("category", "n")
  counts$pct_total <- 100 * counts$n / nrow(data)
  counts$category <- factor(counts$category, levels = counts$category)
  p <- ggplot2::ggplot(counts,
         ggplot2::aes(x = .data$category, y = .data$n)) +
    ggplot2::geom_col(width = .64, fill = "#0072B2") +
    ggplot2::geom_text(ggplot2::aes(label = .data$n),
                       vjust = -.35, size = 3.5) +
    ggplot2::scale_y_continuous(
      limits = c(0, max(counts$n) * 1.18),
      expand = ggplot2::expansion(mult = c(0, .01))
    ) +
    ggplot2::labs(title = title, x = category, y = "Number of observations",
      caption = sprintf(
        "Total N=%d; observed categories=%d; missing=%d; counts are per category.",
        nrow(data), sum(!is.na(values)), sum(is.na(values))
      )) +
    ggplot2::theme_classic(base_size = 12)
  attr(p, "figure_statistics") <- counts
  p
}

# Text-based stem-and-leaf is intentionally not disguised as a bar graph.
# R's graphics::stem retains the original values in a compact text display.
biostat_graph_stem <- function(x, unit, scale = 1) {
  biostat_graph_validate_numeric(x)
  if (!is.character(unit) || length(unit) != 1L ||
      is.na(unit) || !nzchar(trimws(unit)))
    stop("unit must be a nonempty character string.", call. = FALSE)
  y <- x[!is.na(x)]
  if (length(y) < 2L)
    stop("Stem-and-leaf needs at least two observed values.", call. = FALSE)
  if (!is.numeric(scale) || length(scale) != 1L ||
      is.na(scale) || !is.finite(scale) || scale <= 0)
    stop("scale must be a positive finite scalar.", call. = FALSE)
  c(sprintf("Observed n=%d; missing=%d; unit=%s",
            length(y), sum(is.na(x)), unit),
    capture.output(graphics::stem(y, scale = scale)))
}
