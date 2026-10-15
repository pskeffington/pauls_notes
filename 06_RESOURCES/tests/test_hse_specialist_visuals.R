# Synthetic numerical and rendered-figure regression tests; no silent skips.
args <- commandArgs(trailingOnly = FALSE)
file <- grep("^--file=", args, value = TRUE)
if (length(file) != 1L) stop("Run with Rscript --vanilla")
here <- dirname(normalizePath(sub("^--file=", "", file)))
for (name in c("hse_stats_plots.R", "hse_plot_annotations.R",
               "hse_scientific_palette.R", "hse_specialist_visuals.R",
               "hse_plotly_visuals.R"))
  source(file.path(here, "..", "R", name))
if (!requireNamespace("ggplot2", quietly = TRUE))
  stop("ggplot2 required; this suite cannot be skipped")
options(warn = 2)

must_fail <- function(code) {
  if (!inherits(try(force(code), silent = TRUE), "try-error"))
    stop("Invalid input was not rejected")
}
audit_plot <- function(plot, title) {
  stopifnot(inherits(plot, "ggplot"), hse_plot_audit(plot)$pass,
            is.character(plot$labels$caption),
            grepl(title, plot$labels$title, fixed = TRUE))
  layers <- ggplot2::ggplot_build(plot)$data
  stopifnot(length(layers) >= 1L)
}

# Matching uses ID x visit, not row order, and excludes incomplete pairs.
paired <- data.frame(
  subject = rep(sprintf("p%02d", 1:5), each = 2),
  visit = rep(c("Baseline", "Month 6"), 5),
  creatinine = c(1, 2, 3, 4, 5, 7, 8, 10, 11, NA_real_))
p1 <- hse_plot_paired_comparison(paired, "subject", "visit",
                                  "creatinine", c("Baseline", "Month 6"), "mg/dL")
audit_plot(p1, "within-participant")
stopifnot(attr(p1, "hse_design")$complete_pairs == 4L,
          attr(p1, "hse_design")$omitted_subjects == 1L,
          nrow(p1$data) == 8L,
          identical(p1$labels$y, "creatinine (mg/dL)"),
          all(table(p1$data$.id) == 2L))
stopifnot(nrow(attr(p1, "hse_paired_change")$individual) == 4L,
          is.null(attr(p1, "hse_paired_change")$summary))
p1_ci <- hse_plot_paired_comparison(
  paired, "subject", "visit", "creatinine", c("Baseline", "Month 6"),
  "mg/dL", paired_ci = "t", conf_level = .95)
ci_pair <- attr(p1_ci, "hse_paired_change")$summary
actual_delta <- c(1, 1, 2, 2)
stopifnot(ci_pair$n == 4L,
          isTRUE(all.equal(ci_pair$mean_change, mean(actual_delta))),
          isTRUE(all.equal(ci_pair$lower,
            mean(actual_delta) - stats::qt(.975, 3L) *
              stats::sd(actual_delta) / sqrt(4))),
          grepl("t CI", p1_ci$labels$caption, fixed = TRUE))
dup <- rbind(paired, paired[1, , drop = FALSE])
must_fail(hse_plot_paired_comparison(dup, "subject", "visit",
                                     "creatinine", c("Baseline", "Month 6"), "mg/dL"))
other <- paired; other$visit[1] <- "Unscheduled"
must_fail(hse_plot_paired_comparison(other, "subject", "visit",
                                     "creatinine", c("Baseline", "Month 6"), "mg/dL"))
must_fail(hse_plot_paired_comparison(paired, "subject", "visit",
                                     "creatinine", c("Baseline", "Baseline"), "mg/dL"))

# Manual bin aggregation independently checks coordinates and denominators.
calibration <- data.frame(
  outcome = as.numeric(seq_len(200L) %% 3L == 0L),
  score = (seq_len(200L) - .5) / 200,
  subject = sprintf("s%03d", seq_len(200L)))
p2 <- hse_plot_calibration(calibration, "outcome", "score",
                            horizon = "12 months",
                            evaluation_partition = "test", bins = 5L,
                            interval = "wilson", subject_id = "subject")
audit_plot(p2, "Risk calibration")
stopifnot(grepl("\n", p2$labels$caption, fixed = TRUE))
stopifnot(isTRUE(all.equal(ggplot2::ggplot_build(p2)$layout$coord$ratio, 1)))
tab <- attr(p2, "hse_calibration")$tabulation
stopifnot(nrow(tab) == 5L, sum(tab$n) == 200L,
          isTRUE(all.equal(tab$mean_risk[1], mean(calibration$score[1:40]))),
          isTRUE(all.equal(tab$observed[1], mean(calibration$outcome[1:40]))),
          identical(p2$labels$x, "Mean predicted event probability"),
          all(tab$lower >= 0), all(tab$upper <= 1),
          all(tab$lower <= tab$observed & tab$observed <= tab$upper),
          tab$events[1] == sum(calibration$outcome[1:40]),
          length(p2$layers) == 4L)
wilson_z <- stats::qnorm(.975)
w_n <- tab$n[1]
w_p <- tab$observed[1]
w_mid <- (w_p + wilson_z^2 / (2 * w_n)) / (1 + wilson_z^2/w_n)
w_radius <- wilson_z/(1+wilson_z^2/w_n) *
  sqrt(w_p*(1-w_p)/w_n + wilson_z^2/(4*w_n^2))
stopifnot(isTRUE(all.equal(tab$lower[1], w_mid - w_radius)))
bad_cal <- calibration
bad_cal$subject[2] <- bad_cal$subject[1]
must_fail(hse_plot_calibration(bad_cal, "outcome", "score", "12 months",
  "test", interval = "wilson", subject_id = "subject"))
bad_cal <- calibration; bad_cal$score[1] <- 1.5
must_fail(hse_plot_calibration(bad_cal, "outcome", "score", "12 months", "test"))
bad_cal <- calibration; bad_cal$outcome[1] <- NA_real_
must_fail(hse_plot_calibration(bad_cal, "outcome", "score", "12 months", "test"))
must_fail(hse_plot_calibration(calibration, "outcome", "score", "12 months",
                               "training"))

# Supplied embedding only. No clustering/p-values are computed.
set.seed(711L)
embedding <- data.frame(
  cell_id = paste0("cell", 1:40),
  specimen = rep(paste0("s", 1:4), each = 10),
  batch = rep(c("run1", "run2"), each = 20),
  cell_type = rep(c("T", "B"), 20),
  UMAP1 = rnorm(40), UMAP2 = rnorm(40))
p3 <- hse_plot_cell_embedding(embedding, "cell_id", "specimen",
                               "batch", "cell_type", "UMAP1", "UMAP2",
                               method = "UMAP", seed = 2604L,
                               settings = "precomputed, n_neighbors=15")
audit_plot(p3, "embedding by batch")
stopifnot(isTRUE(all.equal(ggplot2::ggplot_build(p3)$layout$coord$ratio, 1)))
stopifnot(nrow(p3$data) == 40L, length(unique(p3$data$Sample)) == 4L,
          length(ggplot2::ggplot_build(p3)$layout$panel_params) == 2L,
          grepl("Seed=2604", p3$labels$caption, fixed = TRUE),
          grepl("independent sample IDs=4", p3$labels$caption, fixed = TRUE))
bad_embedding <- embedding
bad_embedding$cell_id[2] <- bad_embedding$cell_id[1]
must_fail(hse_plot_cell_embedding(bad_embedding, "cell_id", "specimen",
                                   "batch", "cell_type", "UMAP1", "UMAP2",
                                   seed = 1L, settings = "fixed input"))
bad_embedding <- embedding; bad_embedding$UMAP2[2] <- NA_real_
must_fail(hse_plot_cell_embedding(bad_embedding, "cell_id", "specimen",
                                   "batch", "cell_type", "UMAP1", "UMAP2",
                                   seed = 1L, settings = "fixed input"))

# Medians depend on independent specimen, not pooled cellular measurements.
micro <- data.frame(
  specimen = rep(paste0("s", 1:4), each = 6),
  field = rep(rep(c("f1", "f2"), each = 3), times = 4),
  cell = rep(paste0("c", 1:3), times = 8),
  treatment = rep(c("A", "A", "B", "B"), each = 6),
  fluorescence = rep(c(1, 2, 3), times = 8))
p4 <- hse_plot_microscopy(micro, "specimen", "field", "cell",
                           "treatment", "fluorescence", "a.u.")
audit_plot(p4, "independent specimen")
stopifnot(identical(p4$theme$legend.position, "none"))
med <- attr(p4, "hse_specimens")
stopifnot(nrow(med) == 4L, all(med$Measurement == 2),
          nrow(p4$data) == 24L,
          is.null(attr(p4, "hse_specimen_uncertainty")))
micro_more <- data.frame(
  specimen = rep(paste0("spec", seq_len(8L)), each = 6L),
  field = rep(rep(c("f1", "f2"), each = 3L), times = 8L),
  cell = rep(paste0("cell", 1:3), times = 16L),
  treatment = rep(c("A", "B"), each = 24L),
  fluorescence = rep(c(1:4, 3:6), each = 6L) +
    rep(c(-.2, -.1, 0, 0, .1, .2), times = 8L))
p4_ci <- hse_plot_microscopy(micro_more, "specimen", "field", "cell",
                           "treatment", "fluorescence", "a.u.",
                           interval = "t")
micro_ci <- attr(p4_ci, "hse_specimen_uncertainty")
subtitle_lines <- strsplit(p4_ci$labels$subtitle, "\n", fixed = TRUE)[[1]]
stopifnot(length(subtitle_lines) == 2L,
          all(nchar(subtitle_lines, type = "width") <= 65L))
stopifnot(nrow(micro_ci) == 2L, nrow(p4_ci$data) == 48L,
          all(micro_ci$n == 4L),
          length(p4_ci$layers) == 4L,
          isTRUE(all.equal(micro_ci$mean[1], 2.5)),
          isTRUE(all.equal(micro_ci$lower[1],
            2.5 - stats::qt(.975, 3L) * stats::sd(1:4)/2)))
must_fail(hse_plot_microscopy(micro, "specimen", "field", "cell",
  "treatment", "fluorescence", "a.u.", interval = "t"))
bad_micro <- micro; bad_micro$cell[2] <- bad_micro$cell[1]
must_fail(hse_plot_microscopy(bad_micro, "specimen", "field", "cell",
                              "treatment", "fluorescence", "a.u."))
bad_micro <- micro; bad_micro$treatment[2] <- "B"
must_fail(hse_plot_microscopy(bad_micro, "specimen", "field", "cell",
                              "treatment", "fluorescence", "a.u."))

# Full violin distribution, deterministic points, all extremes, RNG conserved.
high <- data.frame(group = rep(c("A", "B", "C"), each = 200),
                   value = rep(seq_len(200), times = 3) +
                     rep(c(0, 250, 500), each = 200))
set.seed(987L)
before <- .Random.seed
p5 <- hse_plot_sampled_distribution(high, "value", "group", "mg/L",
                                     max_points = 60L, seed = 123L)
stopifnot(identical(before, .Random.seed))
audit_plot(p5, "distribution and observed points")
stopifnot(identical(p5$theme$legend.position, "none"))
meta <- attr(p5, "hse_sampling")
p5_again <- hse_plot_sampled_distribution(high, "value", "group", "mg/L",
                                           max_points = 60L, seed = 123L)
stopifnot(meta$original == 600L, meta$displayed == 60L,
          identical(meta$indices, attr(p5_again, "hse_sampling")$indices),
          all(meta$extrema %in% meta$indices),
          nrow(p5$data) == 600L,
          grepl("N=600", p5$labels$caption, fixed = TRUE),
          length(p5$layers) == 3L,
          nrow(attr(p5, "hse_group_descriptives")) == 3L,
          all(attr(p5, "hse_group_descriptives")$n == 200L),
          identical(p5$labels$x, "group"))
box_data <- ggplot2::ggplot_build(p5)$data[[2]]
stopifnot("middle" %in% names(box_data),
          isTRUE(all.equal(unname(box_data$middle), c(100.5, 350.5, 600.5))))
must_fail(hse_plot_sampled_distribution(high, "value", "group", "mg/L",
                                         max_points = 5L))
bad_high <- high; bad_high$value[1] <- Inf
must_fail(hse_plot_sampled_distribution(bad_high, "value", "group", "mg/L",
                                         max_points = 60L))

# Independent-ID percentile bootstrap CIs are a separate visual figure.
estimate_data <- data.frame(
  subject = paste0("subject", seq_len(nrow(high))),
  group = high$group, value = high$value)
rng_before_estimate <- .Random.seed
p6 <- hse_plot_group_estimate_ci(estimate_data, "subject", "value",
                                 "group", "mg/L", n_boot = 250L, seed = 991L)
stopifnot(identical(rng_before_estimate, .Random.seed))
audit_plot(p6, "uncertainty by")
estimate_tab <- attr(p6, "hse_estimates")
stopifnot(nrow(estimate_tab) == 3L, all(estimate_tab$n == 200L),
          all(estimate_tab$Lower <= estimate_tab$Estimate),
          all(estimate_tab$Estimate <= estimate_tab$Upper),
          all(estimate_tab$Upper >= estimate_tab$Lower))
p6_again <- hse_plot_group_estimate_ci(estimate_data, "subject", "value",
                                       "group", "mg/L", n_boot = 250L, seed = 991L)
stopifnot(identical(attr(p6_again, "hse_estimates"), estimate_tab))
bad_estimate <- estimate_data
bad_estimate$subject[2] <- bad_estimate$subject[1]
must_fail(hse_plot_group_estimate_ci(bad_estimate, "subject", "value",
                                     "group", "mg/L", n_boot = 250L))
# Verify *actual* raster/vector figure export and annotation sidecars.
plots <- list(paired = p1_ci, calibration = p2, embedding = p3,
              microscopy = p4_ci, sampled = p5, estimates = p6)
output <- Sys.getenv("HSE_SPECIALIST_FIGURE_DIR", unset = "")
if (!nzchar(output)) output <- file.path(tempdir(), "hse-specialist-figures")
dir.create(output, recursive = TRUE, showWarnings = FALSE)
for (name in names(plots)) {
  files <- hse_save_figure(plots[[name]], file.path(output, name))
  stopifnot(length(files) == 2L,
            all(file.exists(files)), all(file.info(files)$size > 1000),
            all(file.exists(paste0(files, ".annotations.R"))))
}
# Manuscript figures retain their audited ggplot/PDF source; each also
# exports an offline interactive HTML widget with local JS dependencies.
if (!requireNamespace("plotly", quietly = TRUE) ||
    !requireNamespace("htmlwidgets", quietly = TRUE))
  stop("plotly and htmlwidgets required; interactive CI cannot be skipped")
must_fail(hse_plotly_view(data.frame(x = 1)))
must_fail(hse_save_plotly(plots$paired, file.path(output, "bad.pdf")))
for (name in names(plots)) {
  figure <- plots[[name]]
  labels_before <- figure$labels
  interactive <- hse_plotly_view(figure)
  stopifnot(inherits(interactive, "plotly"),
            inherits(interactive, "htmlwidget"),
            identical(labels_before, figure$labels))
  built <- plotly::plotly_build(interactive)
  stopifnot(length(built$x$data) >= 1L)
  files <- hse_save_plotly(interactive, file.path(output, paste0(name, ".html")))
  stopifnot(file.exists(files$html),
            file.info(files$html)$size > 1000,
            dir.exists(files$dependencies),
            length(list.files(files$dependencies, recursive = TRUE)) > 0L)
  body <- paste(readLines(files$html, warn = FALSE), collapse = "\n")
  stopifnot(grepl("plotly", body, fixed = TRUE),
            grepl(paste0(name, "_files"), body, fixed = TRUE))
}
cat("PASS: 6 Plotly conversions, offline HTML exports, local JS dependencies\n")

cat("PASS: 6 specialist plotting contracts, negative cases, numerical ",
    "denominators, RNG stability, 12 rendered figure files and manifests\n",
    sep = "")
