# Run: Rscript --vanilla 06_RESOURCES/tests/test_biomedical_narrative.R
source("06_RESOURCES/R/biomedical_narrative.R")
source("06_RESOURCES/R/synthetic_biostat.R")

expect_error <- function(expr) {
  caught <- tryCatch({force(expr); FALSE}, error = function(e) TRUE)
  stopifnot(caught)
}

d <- pn_make_synthetic_biostat(120L, 712L)
stopifnot(nrow(d) == 120L, !anyDuplicated(d$synthetic_id))
stopifnot(identical(d, pn_make_synthetic_biostat(120L, 712L)))
stopifnot(identical(levels(d$group), c("Reference", "Exposure")))

stats <- pn_group_descriptives(d, "hemoglobin_g_dl", "group")
stopifnot(sum(stats$n) == 119L, sum(stats$missing_n) == 1L)
stopifnot(all(stats$iqr >= 0), all(stats$sd > 0))
stopifnot(all(stats$min <= stats$median & stats$max >= stats$median))
narrative <- pn_narrate_group(stats, "Hemoglobin", "g/dL")
stopifnot(length(narrative) == 2L, all(grepl("Descriptive", narrative)))

gm <- pn_geometric_descriptives(d, "marker_mg_l", "group")
stopifnot(sum(gm$positive_n) == 118L, sum(gm$missing_n) == 1L,
          sum(gm$nonpositive_n) == 1L)
stopifnot(all(is.finite(gm$geometric_mean) & gm$geometric_mean > 0))
stopifnot(length(pn_narrate_geometric(gm)) == 2L)
stopifnot(grepl("descriptive ratio", pn_narrate_geometric_contrast(gm, "Reference", "Exposure")))

x <- c(9, 10, 11, 12, 13)
s <- pn_sampling_mean(x, assumed_mean = 10, expected_n = 5)
stopifnot(identical(s$tail, "right"), s$one_sided_probability > 0,
          s$one_sided_probability < 0.5)
stopifnot(isTRUE(all.equal(s$estimated_se, sd(x) / sqrt(length(x)))))
stopifnot(grepl("one-sided", pn_narrate_sampling(s)))
l <- pn_sampling_mean(x, assumed_mean = 12)
stopifnot(identical(l$tail, "left"), l$one_sided_probability < 0.5)
center <- pn_sampling_mean(x, assumed_mean = mean(x))
stopifnot(center$one_sided_probability == 0.5)
stopifnot(pn_probability_label(1.3274e-49) != "0.000")
stopifnot(is.finite(pn_normality_diagnostics(x)$shapiro_p))
stopifnot(grepl("Shapiro-Wilk", pn_narrate_normality(pn_normality_diagnostics(x))))
stopifnot(is.na(pn_normality_diagnostics(c(2, 2))$shapiro_p))

expect_error(pn_group_descriptives(d, "missing", "group"))
expect_error(pn_group_descriptives(d, "group", "age_years"))
expect_error(pn_sampling_mean(x, 10, expected_n = 7))
expect_error(pn_sampling_mean(rep(10, 4), 10))
expect_error(pn_probability_label(-0.2))
expect_error(pn_probability_label(1.2))
expect_error(pn_narrate_normality(pn_normality_diagnostics(x), alpha = 1))
expect_error(pn_narrate_geometric_contrast(gm, "Reference", "NotAGroup"))
expect_error(pn_geometric_descriptives(transform(d, group = NA_character_),
                                      "marker_mg_l", "group"))

cat("PASS: synthetic cohort, descriptive/narrative, geometric, normality, tail, negatives.\n")
