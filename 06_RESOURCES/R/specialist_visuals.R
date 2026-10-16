# Original specialist scientific visualizations: descriptive, synthetic-testable.
# Source stats_plots.R and scientific_palette.R before this module.
# Requires ggplot2 at call time; loading the file performs no I/O or installs.

validate_plot_input <- function(data, columns) {
  validate_columns(data, columns)
  if (!requireNamespace("ggplot2", quietly = TRUE))
    stop("ggplot2 required; install before plotting", call. = FALSE)
  if (!exists("group_colors", mode = "function") ||
      !exists("theme_scientific", mode = "function") ||
      !exists("axis_label", mode = "function"))
    stop("Source scientific_palette.R first", call. = FALSE)
  if (!length(columns) || anyNA(columns) || anyDuplicated(columns) ||
      any(!nzchar(trimws(columns))))
    stop("Distinct nonempty column names required", call. = FALSE)
  invisible(TRUE)
}

validate_text_scalar <- function(x, label) {
  if (!is.character(x) || length(x) != 1L || is.na(x) ||
      !nzchar(trimws(x)))
    stop(label, " must be one nonempty string", call. = FALSE)
  invisible(TRUE)
}

validate_integer_scalar <- function(x, label, minimum = 1L) {
  if (!is.numeric(x) || length(x) != 1L || is.na(x) ||
      !is.finite(x) || x != as.integer(x) || x < minimum)
    stop(label, " must be an integer >= ", minimum, call. = FALSE)
  invisible(TRUE)
}

# Interval assumptions must be explicit, not inferred from a visual encoding.
validate_confidence_level <- function(conf_level) {
  if (!is.numeric(conf_level) || length(conf_level) != 1L ||
      is.na(conf_level) || !is.finite(conf_level) ||
      conf_level <= 0 || conf_level >= 1)
    stop("conf_level must be strictly between zero and one", call. = FALSE)
  invisible(TRUE)
}

validate_plot_keys <- function(data, columns) {
  for (name in columns) {
    v <- as.character(data[[name]])
    if (anyNA(v) || any(!nzchar(trimws(v))))
      stop("Missing or blank key in ", name, call. = FALSE)
  }
  invisible(TRUE)
}

# 1. Exact two-visit paired trajectories. No test statistic is inferred.
plot_paired_comparison <- function(data, id, visit, value,
                                       visit_levels, unit, paired_ci = c("none", "t"),
                                       conf_level = .95) {
  validate_plot_input(data, c(id, visit, value))
  validate_text_scalar(unit, "unit")
  paired_ci <- match.arg(paired_ci)
  if (paired_ci == "t") validate_confidence_level(conf_level)
  if (!is.character(visit_levels) || length(visit_levels) != 2L ||
      anyNA(visit_levels) || anyDuplicated(visit_levels) ||
      any(!nzchar(trimws(visit_levels))))
    stop("visit_levels must contain two distinct named visits")
  validate_numeric(data[[value]], value)
  validate_plot_keys(data, c(id, visit))
  if (anyDuplicated(data.frame(id = data[[id]], visit = data[[visit]])))
    stop("Duplicate subject x visit keys")
  if (!all(as.character(data[[visit]]) %in% visit_levels))
    stop("Unexpected visit label; restrict inputs deliberately")
  n_subjects <- length(unique(as.character(data[[id]])))
  observed <- data[!is.na(data[[value]]), , drop = FALSE]
  counts <- table(as.character(observed[[id]]))
  complete_ids <- names(counts[counts == 2L])
  if (length(complete_ids) < 2L)
    stop("At least two complete subject pairs required")
  d <- observed[as.character(observed[[id]]) %in% complete_ids, , drop = FALSE]
  d$.id <- as.character(d[[id]])
  d$.visit <- factor(as.character(d[[visit]]), levels = visit_levels)
  d$.value <- d[[value]]
  before <- d[d$.visit == visit_levels[1], c(".id", ".value")]
  after <- d[d$.visit == visit_levels[2], c(".id", ".value")]
  difference <- after$.value[match(before$.id, after$.id)] - before$.value
  change_table <- data.frame(subject_id = before$.id, difference = difference)
  estimate <- NULL
  detail <- "No inferential interval estimated."
  if (paired_ci == "t") {
    n <- length(difference)
    if (n < 3L) stop("Paired t interval requires at least three complete pairs")
    point <- mean(difference)
    half <- stats::qt((1 + conf_level) / 2, df = n - 1L) *
      stats::sd(difference) / sqrt(n)
    estimate <- data.frame(n = n, mean_change = point,
                           lower = point - half, upper = point + half)
    detail <- sprintf("Mean paired change %.3g %s; %.0f%% t CI [%.3g, %.3g].\nAssumes independent subjects and approximately normal paired differences.",
                      point, unit, conf_level * 100, point - half, point + half)
  }
  p <- ggplot2::ggplot(d, ggplot2::aes(
    x = .data$.visit, y = .data$.value, group = .data$.id)) +
    ggplot2::geom_line(alpha = .35, colour = "#0072B2") +
    ggplot2::geom_point(size = 1.8, colour = "#0072B2") +
    ggplot2::labs(
      title = paste(value, "within-participant change"),
      x = "Visit", y = axis_label(value, unit),
      caption = paste0(sprintf("Complete pairs: %d/%d subjects; %d incomplete excluded.",
                        length(complete_ids), n_subjects,
                        n_subjects - length(complete_ids)), "\n", detail)) +
    theme_scientific()
  attr(p, "design") <- list(subjects = n_subjects,
    complete_pairs = length(complete_ids),
    omitted_subjects = n_subjects - length(complete_ids))
  attr(p, "paired_change") <- list(individual = change_table,
    summary = estimate, interval = paired_ci, conf_level = if (paired_ci == "t") conf_level else NA_real_)
  p
}

# 2. Held-out binary risk calibration. Equal-width bins; no confidence bands.
plot_calibration <- function(data, outcome, risk, horizon,
                                 evaluation_partition, bins = 5L,
                                 interval = c("none", "wilson"),
                                 subject_id = NULL, conf_level = .95) {
  validate_plot_input(data, c(outcome, risk))
  validate_text_scalar(horizon, "horizon")
  validate_text_scalar(evaluation_partition, "evaluation_partition")
  permitted <- c("holdout", "validation", "test", "external", "temporal", "out-of-fold")
  if (!evaluation_partition %in% permitted)
    stop("evaluation_partition must identify held-out/out-of-fold evaluation")
  validate_integer_scalar(bins, "bins", minimum = 2L)
  interval <- match.arg(interval)
  if (interval == "wilson") {
    validate_confidence_level(conf_level)
    validate_text_scalar(subject_id, "subject_id")
    validate_columns(data, subject_id)
    validate_plot_keys(data, subject_id)
    if (anyDuplicated(as.character(data[[subject_id]])))
      stop("Wilson intervals require one independent outcome per subject ID")
  }
  if (!is.numeric(data[[outcome]]) ||
      anyNA(data[[outcome]]) ||
      !all(data[[outcome]] %in% c(0, 1)) ||
      length(unique(data[[outcome]])) != 2L)
    stop("Outcome must have observed 0 and 1 with no missing values")
  validate_numeric(data[[risk]], risk)
  if (anyNA(data[[risk]]) || any(data[[risk]] < 0 | data[[risk]] > 1))
    stop("Risk predictions must be complete probabilities in [0,1]")
  if (nrow(data) < 10L) stop("At least ten evaluations required")
  bin <- cut(data[[risk]], breaks = seq(0, 1, length.out = bins + 1L),
             include.lowest = TRUE, right = TRUE)
  groups <- split(seq_len(nrow(data)), bin, drop = TRUE)
  tab <- do.call(rbind, lapply(groups, function(ix)
    data.frame(mean_risk = mean(data[[risk]][ix]),
               observed = mean(data[[outcome]][ix]),
               events = sum(data[[outcome]][ix]), n = length(ix))))
  if (nrow(tab) < 2L) stop("At least two occupied risk bins required")
  tab <- tab[order(tab$mean_risk), , drop = FALSE]
  rownames(tab) <- NULL
  tab$lower <- tab$upper <- NA_real_
  if (interval == "wilson") {
    z <- stats::qnorm((1 + conf_level) / 2)
    denominator <- 1 + z^2 / tab$n
    center <- (tab$observed + z^2 / (2 * tab$n)) / denominator
    radius <- (z / denominator) *
      sqrt(tab$observed * (1 - tab$observed) / tab$n +
             z^2 / (4 * tab$n^2))
    tab$lower <- pmax(0, center - radius)
    tab$upper <- pmin(1, center + radius)
  }
  p <- ggplot2::ggplot(tab, ggplot2::aes(x = .data$mean_risk,
                                          y = .data$observed)) +
    ggplot2::geom_abline(intercept = 0, slope = 1,
                         linetype = "dashed", colour = "#777777") +
    ggplot2::geom_line(colour = "#0072B2") +
    ggplot2::geom_point(ggplot2::aes(size = .data$n), colour = "#0072B2") +
    (if (interval == "wilson")
       ggplot2::geom_errorbar(ggplot2::aes(ymin = .data$lower,
                                          ymax = .data$upper),
                              width = .015, colour = "#0072B2")
     else NULL) +
    ggplot2::scale_x_continuous(limits = c(0, 1)) +
    ggplot2::scale_y_continuous(limits = c(0, 1)) +
    ggplot2::coord_equal() +
    ggplot2::labs(
      title = paste("Risk calibration at", horizon),
      subtitle = paste("Evaluation partition:", evaluation_partition),
      x = "Mean predicted event probability",
      y = "Observed event proportion",
      size = "Bin n",
      caption = paste0(sprintf("Evaluations n=%d; events=%d; equal-width bins: %d (%d populated).",
                        nrow(data), sum(data[[outcome]]), bins, nrow(tab)),
        "\n", if (interval == "wilson")
          sprintf("Bars: %.0f%% Wilson CIs; independent outcomes assumed.\nGrouped calibration only; no smooth curve.", 100 * conf_level)
        else "No uncertainty bars; grouped calibration is not a smooth curve.")) +
    theme_scientific()
  attr(p, "calibration") <- list(tabulation = tab,
    denominator = nrow(data), horizon = horizon,
    evaluation_partition = evaluation_partition, bins = bins,
    interval = interval, conf_level = if (interval == "wilson") conf_level else NA_real_,
    independent_id = subject_id)
  p
}

# 3. Visualize *supplied* embeddings; never re-estimate or test clusters.
plot_cell_embedding <- function(data, cell_id, sample_id, batch, group,
                                    x, y, method = c("UMAP", "t-SNE"),
                                    seed, settings) {
  validate_plot_input(data, c(cell_id, sample_id, batch, group, x, y))
  method <- match.arg(method)
  validate_integer_scalar(seed, "seed", minimum = 0L)
  validate_text_scalar(settings, "settings")
  validate_plot_keys(data, c(cell_id, sample_id, batch, group))
  if (anyDuplicated(as.character(data[[cell_id]])))
    stop("Cell identifiers must be unique")
  for (coord in c(x, y)) {
    validate_numeric(data[[coord]], coord)
    if (anyNA(data[[coord]])) stop("Embedding coordinates must be complete")
  }
  if (nrow(data) < 3L) stop("At least three cells required")
  groups <- sort(unique(as.character(data[[group]])), method = "radix")
  colors <- group_colors(as.character(data[[group]]), levels = groups)
  d <- data.frame(X = data[[x]], Y = data[[y]],
    Group = factor(as.character(data[[group]]), levels = groups),
    Batch = factor(as.character(data[[batch]])),
    Sample = as.character(data[[sample_id]]))
  batch_counts <- table(d$Batch)
  batch_text <- paste(paste0(names(batch_counts), "=", as.integer(batch_counts)),
                      collapse = "; ")
  ggplot2::ggplot(d, ggplot2::aes(x = .data$X, y = .data$Y,
                                   colour = .data$Group)) +
    ggplot2::geom_point(alpha = .65, size = .8) +
    ggplot2::coord_equal() +
    ggplot2::facet_wrap(ggplot2::vars(.data$Batch)) +
    ggplot2::scale_colour_manual(values = colors, drop = FALSE,
                                 name = group) +
    ggplot2::labs(
      title = paste("Supplied", method, "embedding by batch"),
      x = paste(method, "1"), y = paste(method, "2"),
      caption = paste0(sprintf("Cells=%d; independent sample IDs=%d; batch cells: %s.",
                        nrow(d), length(unique(d$Sample)), batch_text),
        "\n", sprintf("Seed=%d; settings: %s. Embeddings are descriptive; no uncertainty or test inferred.",
                       seed, settings))) +
    theme_scientific()
}

# 4. Specimen is the independent unit; cell-level points are contextual.
plot_microscopy <- function(data, specimen, field, cell, group,
                                measurement, unit,
                                interval = c("none", "t"), conf_level = .95) {
  validate_plot_input(data, c(specimen, field, cell, group, measurement))
  validate_text_scalar(unit, "unit")
  interval <- match.arg(interval)
  if (interval == "t") validate_confidence_level(conf_level)
  validate_plot_keys(data, c(specimen, field, cell, group))
  validate_numeric(data[[measurement]], measurement)
  if (anyNA(data[[measurement]])) stop("Measurements must be complete")
  if (anyDuplicated(data.frame(specimen = data[[specimen]],
                              field = data[[field]], cell = data[[cell]])))
    stop("Duplicate specimen x field x cell identifiers")
  by_specimen <- split(as.character(data[[group]]),
                       as.character(data[[specimen]]))
  if (any(vapply(by_specimen, function(z) length(unique(z)) != 1L,
                 logical(1))))
    stop("Each specimen must belong to exactly one group")
  if (length(by_specimen) < 2L) stop("At least two specimens required")
  levels <- sort(unique(as.character(data[[group]])), method = "radix")
  palette <- group_colors(as.character(data[[group]]), levels = levels)
  d <- data.frame(
    Specimen = as.character(data[[specimen]]),
    Group = factor(as.character(data[[group]]), levels = levels),
    Measurement = data[[measurement]])
  med <- stats::aggregate(Measurement ~ Specimen + Group, data = d,
                          FUN = stats::median)
  counts <- table(as.character(med$Group))
  estimates <- NULL
  if (interval == "t") {
    if (any(counts < 3L))
      stop("Specimen-level t intervals require at least three specimens per group")
    indexes <- split(seq_len(nrow(med)), med$Group, drop = TRUE)
    estimates <- do.call(rbind, lapply(indexes, function(ii) {
      z <- med$Measurement[ii]; n <- length(z); mu <- mean(z)
      half <- stats::qt((1 + conf_level) / 2, df = n - 1L) *
        stats::sd(z) / sqrt(n)
      data.frame(Group = med$Group[ii[1]], mean = mu,
                 lower = mu - half, upper = mu + half, n = n)
    }))
    estimates$Group <- factor(as.character(estimates$Group),
                              levels = levels)
  }
  p <- ggplot2::ggplot(d, ggplot2::aes(x = .data$Group,
                    y = .data$Measurement, colour = .data$Group)) +
    ggplot2::geom_point(position = ggplot2::position_jitter(
                          width = .15, height = 0, seed = 711L),
                          alpha = .18, size = .75) +
    ggplot2::geom_point(data = med,
                        ggplot2::aes(x = .data$Group, y = .data$Measurement),
                        colour = "black", shape = 18, size = 2.5,
                        position = ggplot2::position_jitter(
                          width = .08, height = 0, seed = 712L)) +
    (if (interval == "t")
       ggplot2::geom_errorbar(data = estimates,
          ggplot2::aes(x = .data$Group, ymin = .data$lower,
                       ymax = .data$upper),
          inherit.aes = FALSE, position = ggplot2::position_nudge(x = .22),
          width = .08, linewidth = .55, colour = "#333333")
     else NULL) +
    (if (interval == "t")
       ggplot2::geom_point(data = estimates,
          ggplot2::aes(x = .data$Group, y = .data$mean),
          inherit.aes = FALSE, position = ggplot2::position_nudge(x = .22),
          shape = 21, fill = "white", colour = "#333333", size = 2.3)
     else NULL) +
    ggplot2::scale_colour_manual(values = palette, drop = FALSE) +
    ggplot2::labs(
      title = paste(measurement, "by independent specimen"),
      subtitle = if (interval == "t")
        "Cells: points; specimen medians: diamonds\nOffset circles and bars: specimen-level mean and t CI"
      else "Colored points: cells; black diamonds: specimen medians",
      x = group, y = axis_label(measurement, unit),
      caption = paste0(sprintf("%d independent specimens; %d cell measurements; specimens/group: %s.",
                        nrow(med), nrow(d),
                        paste(paste0(names(counts), "=", as.integer(counts)), collapse = "; ")),
        "\n", if (interval == "t")
          sprintf("%.0f%% t CIs assume independent specimen medians and approximately normal variation; cells are not replicates.",
                  100 * conf_level)
        else "Cells are nested observations; no confidence interval calculated.")) +
    theme_scientific() +
    ggplot2::theme(legend.position = "none")
  attr(p, "specimens") <- med
  attr(p, "specimen_uncertainty") <- estimates
  p
}

# 5. Full-data violin plus deterministic subset of raw points, retaining
# observed min/max within each group. Sampling never alters the violins.
plot_sampled_distribution <- function(data, value, group, unit,
                                           max_points = 1000L, seed = 711L) {
  validate_plot_input(data, c(value, group))
  validate_text_scalar(unit, "unit")
  validate_integer_scalar(max_points, "max_points", minimum = 2L)
  validate_integer_scalar(seed, "seed", minimum = 0L)
  validate_plot_keys(data, group)
  validate_numeric(data[[value]], value)
  if (anyNA(data[[value]])) stop("Measurement must be complete")
  levels <- sort(unique(as.character(data[[group]])), method = "radix")
  if (max_points < 2L * length(levels))
    stop("max_points must allow two extrema per group")
  counts <- table(as.character(data[[group]]))
  if (any(counts < 3L))
    stop("Each group needs >=3 observations for a violin density")
  colors <- group_colors(as.character(data[[group]]), levels = levels)
  d <- data.frame(Value = data[[value]],
                  Group = factor(as.character(data[[group]]), levels = levels))
  idx <- split(seq_len(nrow(d)), d$Group, drop = TRUE)
  extrema <- unique(unlist(lapply(idx, function(ii) {
    c(ii[which.min(d$Value[ii])], ii[which.max(d$Value[ii])])
  }), use.names = FALSE))
  available <- setdiff(seq_len(nrow(d)), extrema)
  budget <- min(length(available), max_points - length(extrema))
  # Restore the caller's RNG stream, including its initially unset state.
  existed <- exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE)
  if (existed) old_seed <- get(".Random.seed", envir = .GlobalEnv)
  on.exit({
    if (existed) assign(".Random.seed", old_seed, envir = .GlobalEnv)
    else if (exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE))
      rm(".Random.seed", envir = .GlobalEnv)
  }, add = TRUE)
  set.seed(as.integer(seed))
  sampled <- if (budget > 0L) sample(available, budget) else integer()
  selected <- sort(unique(c(extrema, sampled)))
  shown <- d[selected, , drop = FALSE]
  p <- ggplot2::ggplot(d, ggplot2::aes(x = .data$Group,
                                      y = .data$Value, fill = .data$Group)) +
    ggplot2::geom_violin(trim = FALSE, alpha = .38,
                          linewidth = .35, colour = "#555555") +
    ggplot2::geom_boxplot(width = .12, outlier.shape = NA,
                          fill = "white", colour = "#333333",
                          linewidth = .35) +
    ggplot2::geom_point(data = shown,
                          ggplot2::aes(x = .data$Group, y = .data$Value),
                          inherit.aes = FALSE,
                          position = ggplot2::position_jitter(
                            width = .12, height = 0, seed = as.integer(seed)),
                          alpha = .4, size = .7) +
    ggplot2::scale_fill_manual(values = colors, drop = FALSE) +
    ggplot2::scale_x_discrete(labels = function(z)
      paste0(z, " (n=", as.integer(counts[as.character(z)]), ")")) +
    ggplot2::labs(
      title = paste(value, "distribution and observed points"),
      x = group, y = axis_label(value, unit),
      caption = paste0(sprintf("Full-data KDE + box (median/IQR; 1.5×IQR whiskers); N=%d.",
                        nrow(d)),
        "\n", sprintf("Displayed points n=%d (seed=%d; each group's minima/maxima retained); plotted dots are not representative.",
                       nrow(shown), seed))) +
    theme_scientific() +
    ggplot2::theme(legend.position = "none")
  tab <- do.call(rbind, lapply(idx, function(ii)
    data.frame(Group = as.character(d$Group[ii[1]]), n = length(ii),
               median = stats::median(d$Value[ii]),
               q1 = unname(stats::quantile(d$Value[ii], .25)),
               q3 = unname(stats::quantile(d$Value[ii], .75)))))
  attr(p, "group_descriptives") <- tab
  attr(p, "sampling") <- list(original = nrow(d),
    displayed = nrow(shown), indices = selected, extrema = extrema,
    seed = seed, sampled_points = shown)
  p
}


# Companion estimate figure; CIs are deliberately separate from violin
# quartiles/whiskers. One row per independently sampled subject/specimen.
# Resampling the individual IDs (not rows nested within specimens) is required.
plot_group_estimate_ci <- function(data, id, value, group, unit,
                                       estimand = c("median", "mean"),
                                       conf_level = .95, n_boot = 1000L,
                                       seed = 711L) {
  validate_plot_input(data, c(id, value, group))
  validate_text_scalar(unit, "unit")
  validate_confidence_level(conf_level)
  validate_integer_scalar(n_boot, "n_boot", minimum = 200L)
  validate_integer_scalar(seed, "seed", minimum = 0L)
  estimand <- match.arg(estimand)
  validate_plot_keys(data, c(id, group))
  if (anyDuplicated(as.character(data[[id]])))
    stop("One measurement per independently sampled subject/specimen ID required")
  validate_numeric(data[[value]], value)
  if (anyNA(data[[value]]))
    stop("Remove or explicitly disclose missing measurements before estimation")
  groups <- sort(unique(as.character(data[[group]])), method = "radix")
  if (length(groups) > 8L) stop("Use facets for more than eight groups")
  index <- split(seq_len(nrow(data)), as.character(data[[group]]))
  if (any(lengths(index) < 5L))
    stop("Each independent group needs at least five observations")
  existed <- exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE)
  if (existed) old_seed <- get(".Random.seed", envir = .GlobalEnv)
  on.exit({
    if (existed) assign(".Random.seed", old_seed, envir = .GlobalEnv)
    else if (exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE))
      rm(".Random.seed", envir = .GlobalEnv)
  }, add = TRUE)
  set.seed(as.integer(seed))
  estimator <- if (estimand == "median") stats::median else base::mean
  tab <- do.call(rbind, lapply(groups, function(g) {
    z <- data[[value]][index[[g]]]
    draws <- replicate(n_boot, estimator(sample(z, length(z),
                                                replace = TRUE)))
    bounds <- stats::quantile(draws, probs = c((1-conf_level)/2,
                                               (1+conf_level)/2),
                              names = FALSE)
    data.frame(Group = g, n = length(z), Estimate = estimator(z),
               Lower = bounds[1], Upper = bounds[2])
  }))
  tab$Group <- factor(tab$Group, levels = groups)
  color_values <- group_colors(as.character(tab$Group), groups)
  p <- ggplot2::ggplot(tab, ggplot2::aes(x = .data$Group,
      y = .data$Estimate, ymin = .data$Lower, ymax = .data$Upper,
      colour = .data$Group)) +
    ggplot2::geom_pointrange(linewidth = .6) +
    ggplot2::scale_colour_manual(values = color_values, drop = FALSE) +
    ggplot2::scale_x_discrete(labels = function(z)
      paste0(z, " (n=", tab$n[match(z, as.character(tab$Group))], ")")) +
    ggplot2::coord_flip() +
    ggplot2::labs(title = paste(value, estimand, "and uncertainty by", group),
                  x = group, y = axis_label(value, unit),
                  caption = sprintf("Point: group %s; bar: %.0f%% percentile-bootstrap CI.\nDraws=%d; seed=%d. Independent %s assumed; no contrast test.",
                                    estimand, 100*conf_level, n_boot, seed, id)) +
    theme_scientific() + ggplot2::theme(legend.position = "none")
  attr(p, "estimates") <- tab
  attr(p, "bootstrap_design") <- list(unit_id = id, estimator = estimand,
    conf_level = conf_level, draws = n_boot, seed = seed)
  p
}
