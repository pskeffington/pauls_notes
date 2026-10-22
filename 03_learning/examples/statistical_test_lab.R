# Synthetic biomedical statistical foundations lab: base R only.
# Source this file to define functions; sourcing does not execute analyses.
# These invented values are not TCGA, protected data or patient records.
# Run examples from the repository root. No clinical inference is supported.

make_statistical_test_lab <- function() {
  before <- c(9, 10, 12, 11, 8, 13, 9, 12,
              14, 15, 12, 13, 15, 14, 16, 11)
  change <- c(1, 2, 2, 1, 3, 1, 1, 2,
              2, 1, 2, 3, 1, 2, 2, 1)
  data.frame(
    person_id = sprintf("S%02d", seq_len(16)),
    group = factor(rep(c("Reference", "Comparison"), each = 8L),
                   levels = c("Reference", "Comparison")),
    marker_au = c(8, 11, 9, 10, 12, 9, 10, 11,
                  12, 14, 13, 15, 16, 12, 14, 15),
    before_au = before,
    after_au = before + change,
    age_years = c(35, 38, 41, 44, 47, 50, 53, 56,
                  36, 39, 42, 45, 48, 51, 54, 57),
    diagnosis = factor(c("No", "No", "Yes", "Yes", "No", "Yes",
                         "Yes", "No", "Yes", "No", "Yes", "Yes",
                         "No", "Yes", "No", "Yes"),
                       levels = c("No", "Yes")),
    severity = ordered(c("I", "II", "II", "III", "I", "II", "III", "I",
                         "II", "III", "III", "IV", "III", "II", "IV", "III"),
                       levels = c("I", "II", "III", "IV")),
    event_count = as.integer(c(0, 1, 1, 2, 0, 2, 1, 0,
                                1, 2, 1, 3, 0, 1, 2, 1)),
    exposure_years = c(0.5, 1, 1.5, 2, 1, 1.25, 0.75, 1.5,
                       1, 1.75, 1.5, 2, 0.75, 1.25, 2, 1),
    stringsAsFactors = FALSE
  )
}

validate_statistical_test_lab <- function(d) {
  required <- c("person_id", "group", "marker_au", "before_au", "after_au",
                "age_years", "diagnosis", "severity", "event_count", "exposure_years")
  if (!is.data.frame(d) || !all(required %in% names(d))) {
    stop("Expected a data frame with all ten named teaching columns", call. = FALSE)
  }
  if (nrow(d) < 8L || anyNA(d[required])) {
    stop("Teaching data require at least eight complete person-level rows", call. = FALSE)
  }
  if (!is.character(d$person_id) || any(!nzchar(d$person_id)) ||
      anyDuplicated(d$person_id)) {
    stop("Person identifiers must be distinct nonempty strings", call. = FALSE)
  }
  if (!is.factor(d$group) ||
      !identical(levels(d$group), c("Reference", "Comparison")) ||
      any(table(d$group) < 2L)) {
    stop("Expected two represented independent groups of two or more people", call. = FALSE)
  }
  if (!is.factor(d$diagnosis) ||
      !identical(levels(d$diagnosis), c("No", "Yes")) ||
      any(table(d$group, d$diagnosis) == 0L)) {
    stop("Diagnosis must be binary with both categories represented per group", call. = FALSE)
  }
  if (!is.ordered(d$severity) ||
      !identical(levels(d$severity), c("I", "II", "III", "IV"))) {
    stop("Severity must be an ordered I-IV factor", call. = FALSE)
  }
  measurements <- c("marker_au", "before_au", "after_au",
                    "age_years", "event_count", "exposure_years")
  if (!all(vapply(d[measurements], is.numeric, logical(1))) ||
      any(!is.finite(as.matrix(d[measurements])))) {
    stop("Measurements must be finite numeric values", call. = FALSE)
  }
  if (any(d$event_count < 0 | d$event_count != floor(d$event_count)) ||
      any(d$exposure_years <= 0)) {
    stop("Event counts must be nonnegative integers; exposure time must be positive",
         call. = FALSE)
  }
  if (length(unique(d$marker_au)) < 2L ||
      length(unique(d$after_au - d$before_au)) < 2L) {
    stop("Teaching examples require nonconstant marker and paired differences",
         call. = FALSE)
  }
  invisible(d)
}

analyse_statistical_test_lab <- function(d) {
  validate_statistical_test_lab(d)
  # These models answer different descriptive/inferential questions.
  # Every before/after pair occupies one person-level row.
  tab <- table(d$group, d$diagnosis)
  group_means <- tapply(d$marker_au, d$group, mean)
  paired_change <- d$after_au - d$before_au
  list(
    n_people = nrow(d),
    group_counts = table(d$group),
    group_means = group_means,
    # Difference direction is explicit, unlike the default t.test contrast:
    comparison_minus_reference =
      unname(group_means["Comparison"] - group_means["Reference"]),
    paired_mean_change = mean(paired_change),  # after minus before
    contingency_counts = tab,
    welch = stats::t.test(marker_au ~ group, data = d),
    paired = stats::t.test(d$after_au, d$before_au, paired = TRUE),
    fisher = stats::fisher.test(tab),
    correlation = stats::cor.test(d$age_years, d$marker_au,
                                  method = "pearson"),
    ordinal_rank = stats::wilcox.test(as.integer(severity) ~ group,
                                     data = d, exact = FALSE),
    logistic = stats::glm(I(diagnosis == "Yes") ~ group,
                          family = stats::binomial(), data = d),
    poisson_rate = stats::glm(
      event_count ~ group + offset(log(exposure_years)),
      family = stats::poisson(), data = d)
  )
}

# Explicit CLI run: produce a small readable teaching summary; no files written.
# This branch is not evaluated when this script is sourced.
if (sys.nframe() == 0L) {
  lab <- make_statistical_test_lab()
  a <- analyse_statistical_test_lab(lab)
  cat("Synthetic statistical biology lab: invented units only\n")
  cat(sprintf("Independent people: %d | mean difference (Comparison - Reference): %.4f au\n",
              a$n_people, a$comparison_minus_reference))
  cat(sprintf("Paired change (after - before): %.4f au\n", a$paired_mean_change))
  cat(sprintf("Welch p=%.5g | paired p=%.5g | Fisher p=%.5g\n",
              a$welch$p.value, a$paired$p.value, a$fisher$p.value))
  cat("Interpret study design and estimates before p-values.\n")
}
