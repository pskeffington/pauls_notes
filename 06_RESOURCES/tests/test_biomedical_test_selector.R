# Run: Rscript --vanilla 06_RESOURCES/tests/test_biomedical_test_selector.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (!length(file_arg)) stop("Run using Rscript --vanilla <test path>.")
here <- dirname(normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE))
source(file.path(here, "..", "R", "biomedical_test_selector.R"))

rejects <- function(expr) inherits(try(expr, silent = TRUE), "try-error")
check <- function(args, id, status) {
  result <- do.call(biomedical_method_decision, args)
  stopifnot(inherits(result, "biomedical_method_decision"),
            identical(result$method_id, id),
            identical(result$status, status),
            length(result$required_checks) >= 2L,
            is.character(result$r_entrypoint))
  invisible(result)
}

check(list("continuous", "independent", n_groups = 2), "welch-t", "implemented")
check(list("continuous", "independent", n_groups = 3), "welch-anova", "implemented")
check(list("continuous", "paired", n_groups = 2), "paired-t", "implemented")
check(list("continuous", "paired", n_groups = 3), "paired-design-review", "specialist-review")
check(list("binary", "paired", n_groups = 2), "mcnemar", "documented")
check(list("ordinal", "paired", n_groups = 2), "signed-rank", "implemented")
check(list("ordinal", "independent", n_groups = 2), "wilcox-independent", "implemented")
check(list("ordinal", "independent", n_groups = 3), "kruskal-wallis", "documented")
check(list("binary", "independent", n_groups = 1), "binomial-proportion", "documented")
check(list("binary", "independent", n_groups = 2), "contingency-analysis", "documented")
check(list("nominal", "independent", n_groups = 4), "contingency-analysis", "documented")
check(list("count", has_exposure = TRUE), "count-rate-model-review", "specialist-review")
check(list("count", has_exposure = FALSE), "count-exposure-review", "specialist-review")
check(list("time_to_event", has_censoring = TRUE), "survival-analysis-review", "specialist-review")
check(list("time_to_event", has_censoring = FALSE), "time-origin-review", "specialist-review")
check(list("omics_counts"), "omics-design-review", "specialist-review")
check(list("continuous", question = "predict"), "prediction-validation-review", "specialist-review")
check(list("continuous", question = "associate"), "association-model-review", "documented")
check(list("continuous", question = "describe"), "descriptive", "implemented")

# First gate: sampling design supersedes outcome-based independent tests.
check(list("continuous", "complex_survey", n_groups = 2), "survey-design-review", "specialist-review")
check(list("binary", "clustered", n_groups = 2), "correlated-outcome-review", "specialist-review")
check(list("continuous", "repeated", n_groups = 2), "correlated-outcome-review", "specialist-review")
check(list("continuous", "independent", n_groups = 2, adjusted = TRUE),
      "adjusted-model-review", "specialist-review")

multiplicity <- biomedical_method_decision("continuous", n_groups = 2,
                                            multiple_outcomes = TRUE)
stopifnot(any(grepl("multiplicity", multiplicity$required_checks)))
no_multiplicity <- biomedical_method_decision("continuous", n_groups = 2)
stopifnot(!any(grepl("multiplicity", no_multiplicity$required_checks)))

for (invalid_type in list("invalid", "", NA_character_, character(), 1)) {
  stopifnot(rejects(biomedical_method_decision(invalid_type)))
}
stopifnot(
  rejects(biomedical_method_decision("binary", "bad_design")),
  rejects(biomedical_method_decision("binary", question = "bad_question")),
  rejects(biomedical_method_decision("continuous", n_groups = 2.3)),
  rejects(biomedical_method_decision("continuous", n_groups = 0)),
  rejects(biomedical_method_decision("continuous", adjusted = NA)),
  rejects(biomedical_method_decision("continuous", has_exposure = 1)),
  rejects(biomedical_method_decision("continuous", multiple_outcomes = c(TRUE, FALSE)))
)

# Printing does not perform an analysis or mutate the decision.
stopifnot(inherits(capture.output(print(no_multiplicity)), "character"))
cat("PASS: decision routing, design precedence, evidence/assumption output and input guards.\n")
