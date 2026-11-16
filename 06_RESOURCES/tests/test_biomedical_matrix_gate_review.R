# Run: Rscript --vanilla 06_RESOURCES/tests/test_biomedical_matrix_gate_review.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (!length(file_arg)) stop("Use Rscript --vanilla <test file>.")
here <- dirname(normalizePath(sub("^--file=", "", file_arg[1L]),
                              mustWork = TRUE))
root <- normalizePath(file.path(here, "..", ".."), mustWork = TRUE)
source(file.path(here, "..", "R", "biomedical_test_selector.R"))
source(file.path(here, "..", "R", "biostat_method_crosswalk.R"))
source(file.path(here, "..", "R", "biomedical_matrix_gate_review.R"))

catalog <- bio_matrix_catalog(root)
stopifnot(nrow(catalog$matrix) == 27L,
          nrow(catalog$gates) == 25L,
          !anyDuplicated(catalog$matrix$method_id),
          !anyDuplicated(catalog$gates$gate_key))
cases <- list(
  list("descriptive", list("continuous", question="describe")),
  list("descriptive-categorical", list("binary", question="describe")),
  list("descriptive-design-review", list("continuous", design="paired", question="describe")),
  list("survey-design-review", list("binary", design="complex_survey", n_groups=2L)),
  list("correlated-outcome-review", list("continuous", design="repeated", n_groups=2L)),
  list("omics-design-review", list("omics_counts")),
  list("prediction-validation-review", list("binary", question="predict")),
  list("adjusted-model-review", list("binary", n_groups=2L, adjusted=TRUE)),
  list("survival-analysis-review", list("time_to_event", has_censoring=TRUE)),
  list("time-origin-review", list("time_to_event", has_censoring=FALSE)),
  list("count-rate-model-review", list("count", has_exposure=TRUE)),
  list("count-exposure-review", list("count", has_exposure=FALSE)),
  list("association-model-review", list("continuous", question="associate")),
  list("paired-t", list("continuous", design="paired", n_groups=2L)),
  list("mcnemar", list("binary", design="paired", n_groups=2L)),
  list("signed-rank", list("ordinal", design="paired", n_groups=2L)),
  list("paired-design-review", list("nominal", design="paired", n_groups=3L)),
  list("group-count-review", list("continuous")),
  list("welch-t", list("continuous", n_groups=2L)),
  list("welch-anova", list("continuous", n_groups=3L)),
  list("continuous-design-review", list("continuous", n_groups=1L)),
  list("ordinal-one-sample-review", list("ordinal", n_groups=1L)),
  list("wilcox-independent", list("ordinal", n_groups=2L)),
  list("kruskal-wallis", list("ordinal", n_groups=3L)),
  list("nominal-one-sample-review", list("nominal", n_groups=1L)),
  list("binomial-proportion", list("binary", n_groups=1L)),
  list("contingency-analysis", list("binary", n_groups=2L))
)
covered <- character()
for (case in cases) {
  expected <- case[[1L]]
  selected <- do.call(biomedical_method_decision, case[[2L]])
  stopifnot(identical(selected$method_id, expected))
  original <- selected
  card <- bio_matrix_card(selected, root)
  stopifnot(identical(card$method_id, expected),
            length(card$gate_keys) >= 3L,
            all(card$gate_keys %in% catalog$gates$gate_key),
            nzchar(card$breast_cancer_example),
            nzchar(card$interpretation))
  review <- bio_matrix_gate_review(selected, root)
  stopifnot(identical(review$review_state, "incomplete"),
            all(review$gate_assessments$status == "not_checked"),
            identical(review$clinical_validation, FALSE))
  documented <- stats::setNames(rep("documented", length(card$gate_keys)),
                                card$gate_keys)
  completed <- bio_matrix_gate_review(selected, root, documented)
  stopifnot(identical(completed$review_state, "ready_for_human_review"),
            identical(completed$clinical_validation, FALSE))
  documented[1L] <- "concern"
  flagged <- bio_matrix_gate_review(selected, root, documented)
  stopifnot(identical(flagged$review_state, "blocked_by_concern"),
            identical(flagged$clinical_validation, FALSE),
            identical(selected, original))
  covered <- c(covered, expected)
}
stopifnot(identical(sort(unique(covered)),
                    sort(catalog$matrix$method_id)),
          length(unique(covered)) == length(covered))
fails <- function(expr) inherits(try(expr, silent=TRUE), "try-error")
example <- biomedical_method_decision("continuous", n_groups=2L)
stopifnot(fails(bio_matrix_card(list(method_id="welch-t"), root)),
          fails(bio_matrix_catalog("this_directory_does_not_exist")),
          fails(bio_matrix_gate_review(example, root, c(unit="yes"))),
          fails(bio_matrix_gate_review(example, root, c(other="documented"))),
          fails(bio_matrix_gate_review(example, root,
                                      c(unit="documented", unit="concern"))),
          is.character(capture.output(print(bio_matrix_gate_review(example, root)))))
annotated <- biomedical_method_decision("continuous", n_groups=2L,
                                       include_biostat=TRUE)
stopifnot(identical(bio_matrix_card(annotated, root)$biostat$chapters, "8"))
cat("PASS: 27 selector routes, matrix cards, 25-gate dictionary, non-automatic review and invalid inputs.\n")
