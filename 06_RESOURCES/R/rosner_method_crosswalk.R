# Read-only Rosner chapter crosswalk. No dataset access or test execution.
# Mapping is an original editorial aid, not a substitute for textbook sections.
rosner_method_crosswalk <- function(method_id) {
  if (!is.character(method_id) || length(method_id) != 1L ||
      is.na(method_id) || !nzchar(method_id))
    stop("method_id must be one nonempty character value.", call. = FALSE)
  ids <- c("descriptive", "descriptive-categorical", "descriptive-design-review", "survey-design-review", "correlated-outcome-review", "omics-design-review", "prediction-validation-review", "adjusted-model-review", "survival-analysis-review", "time-origin-review", "count-rate-model-review", "count-exposure-review", "association-model-review", "paired-t", "mcnemar", "signed-rank", "paired-design-review", "group-count-review", "welch-t", "welch-anova", "continuous-design-review", "ordinal-one-sample-review", "wilcox-independent", "kruskal-wallis", "nominal-one-sample-review", "binomial-proportion", "contingency-analysis")
  chapters <- c("2", "2", "", "", "13", "", "", "11;13;14", "14", "14", "14", "14", "11;13", "8", "10", "9", "", "", "8", "12", "7;8", "", "9", "12", "10", "4;7", "10")
  coverage <- c("textbook", "textbook", "extension", "extension", "extension", "extension", "extension", "textbook", "textbook", "textbook", "textbook", "textbook", "textbook", "textbook", "textbook", "textbook", "extension", "design_gate", "textbook", "textbook", "textbook", "extension", "textbook", "textbook", "textbook", "textbook", "textbook")
  idx <- match(method_id, ids)
  if (is.na(idx)) stop("Unrecognized method_id: ", method_id, call. = FALSE)
  list(method_id = method_id,
       rosner_edition = "8th",
       chapters = if (nzchar(chapters[idx])) strsplit(chapters[idx], ";", fixed = TRUE)[[1L]]
                  else character(),
       coverage = coverage[idx],
       source = "Rosner, Fundamentals of Biostatistics, 8th ed., Cengage",
       note = "Topical chapter crosswalk only; extension/gate routes are not textbook claims.")
}

# Enrich a precomputed selector result. Never changes the method decision.
rosner_annotate_decision <- function(decision) {
  if (!inherits(decision, "biomedical_method_decision"))
    stop("Expected biomedical_method_decision object.", call. = FALSE)
  decision$rosner <- rosner_method_crosswalk(decision$method_id)
  decision
}
