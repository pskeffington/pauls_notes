#!/usr/bin/env Rscript
# Synthetic regression contracts for biomedical descriptive figures.
# Run from pauls_notes repository root: Rscript scripts/test_descriptive_figure_contracts.R
# No user data, images or external output files.

source("06_RESOURCES/R/scientific_palette.R")

pal <- okabe_ito()
groups <- factor(c("Female", "Male", "Female"), levels = c("Female", "Male"))
fills <- c(Female = unname(pal["vermillion"]),
           Male = unname(pal["sky_blue"]))
stopifnot(identical(names(fills), levels(groups)))
stopifnot(all(unname(fills) %in% unname(pal)))
stopifnot(!anyDuplicated(names(fills)))

# Synthetic sample contracts; missing category remains explicit.
d <- data.frame(
  id = c(101L, 102L, 103L, 104L),
  sex = c("Female", "Male", NA_character_, "Female"),
  biomarker = c(0, 1, 9, NA_real_)
)
stopifnot(nrow(d) == 4L)
stopifnot(sum(is.na(d$biomarker)) == 1L)
stopifnot(sum(!is.na(d$biomarker)) == 3L)
stopifnot(length(unique(d$id)) == nrow(d))
stopifnot(identical(sum(is.na(d$sex)), 1L))
stopifnot(sum(table(replace(d$sex, is.na(d$sex), "Missing"))) == nrow(d))

# Mean of transformed observations != transformed arithmetic mean.
x <- c(0, 1, 9)
stopifnot(all(x >= 0))
raw_mean <- mean(x)
marker_y <- log1p(raw_mean)
stopifnot(isTRUE(all.equal(expm1(marker_y), raw_mean)))
stopifnot(!isTRUE(all.equal(marker_y, mean(log1p(x)))))

# Bad-domain values must be rejected before log1p.
negative <- c(0, -2, 3)
stopifnot(!all(negative >= 0))

if (requireNamespace("ggplot2", quietly = TRUE)) {
  demo <- data.frame(\n    group = factor(rep(c("Female", "Male"), each = 5), levels = c("Female", "Male")),\n    value = c(0, 1, 3, 5, 9, 0.5, 2, 4, 6, 10)\n  )
  p <- ggplot2::ggplot(demo,
          ggplot2::aes(x = group, y = value, fill = group)) +
       ggplot2::geom_violin(scale = "width", trim = TRUE) +
       ggplot2::scale_fill_manual(values = fills) +
       ggplot2::theme_classic() +
       ggplot2::theme(legend.position = "bottom")
  withCallingHandlers(
    ggplot2::ggplot_build(p),
    warning = function(w) stop("ggplot warning: ", conditionMessage(w))
  )
  stopifnot(identical(p$theme$legend.position, "bottom"))
} else {
  message("ggplot2 not installed: graphical build check SKIPPED")
}
cat("Synthetic descriptive figure contracts passed.\n")
