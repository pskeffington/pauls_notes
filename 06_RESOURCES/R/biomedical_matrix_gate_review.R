# Read-only, data-neutral breast cancer test-selection matrix helpers.
# Sourcing defines functions only. Explicit root path avoids hidden I/O.
# A completed checklist means "review requested", never clinical approval.

bio_matrix_catalog <- function(root = ".") {
  if (!is.character(root) || length(root) != 1L ||
      is.na(root) || !nzchar(root))
    stop("root must be one nonempty path.", call. = FALSE)
  base <- file.path(root, "03_learning", "bio_stats")
  matrix_path <- file.path(base, "biomedical_decision_matrix.csv")
  gate_path <- file.path(base, "biomedical_gate_dictionary.csv")
  if (!file.exists(matrix_path) || !file.exists(gate_path))
    stop("Could not locate the decision matrix and gate dictionary at root.",
         call. = FALSE)
  matrix <- utils::read.csv(matrix_path, stringsAsFactors = FALSE,
                            colClasses = "character", check.names = FALSE)
  dictionary <- utils::read.csv(gate_path, stringsAsFactors = FALSE,
                                colClasses = "character", check.names = FALSE)
  matrix_fields <- c("method_id", "outcome_family", "study_design",
                     "estimand_or_target", "required_fields", "gate_keys",
                     "breast_cancer_example", "interpretation",
                     "common_pitfall", "reporting_quantity", "route_class")
  gate_fields <- c("gate_key", "review_question", "minimum_evidence")
  if (!identical(names(matrix), matrix_fields) ||
      !identical(names(dictionary), gate_fields))
    stop("Matrix/dictionary schema drift.", call. = FALSE)
  if (!nrow(matrix) || !nrow(dictionary) ||
      anyNA(matrix) || anyNA(dictionary) ||
      any(!nzchar(as.matrix(matrix))) || any(!nzchar(as.matrix(dictionary))) ||
      anyDuplicated(matrix$method_id) || anyDuplicated(dictionary$gate_key))
    stop("Matrix/dictionary must have complete unique rows.", call. = FALSE)
  if (!all(matrix$route_class %in%
           c("descriptive", "inferential", "review", "design_gate")))
    stop("Unknown route_class in matrix.", call. = FALSE)
  keys <- lapply(matrix$gate_keys, strsplit, split = ";", fixed = TRUE)
  keys <- lapply(keys, function(x) x[[1L]])
  if (any(vapply(keys, function(x) anyDuplicated(x) > 0L ||
                 !all(x %in% dictionary$gate_key), logical(1L))))
    stop("Unknown or repeated gate key in decision matrix.", call. = FALSE)
  list(matrix = matrix, gates = dictionary)
}

bio_matrix_card <- function(decision, root = ".") {
  if (!inherits(decision, "biomedical_method_decision") ||
      !is.character(decision$method_id) ||
      length(decision$method_id) != 1L ||
      is.na(decision$method_id))
    stop("Expected biomedical_method_decision from primary selector.",
         call. = FALSE)
  catalog <- bio_matrix_catalog(root)
  idx <- match(decision$method_id, catalog$matrix$method_id)
  if (is.na(idx))
    stop("No matrix entry for selector method: ", decision$method_id,
         call. = FALSE)
  entry <- as.list(catalog$matrix[idx, , drop = FALSE])
  gate_names <- strsplit(entry$gate_keys, ";", fixed = TRUE)[[1L]]
  gate_info <- catalog$gates[
    match(gate_names, catalog$gates$gate_key), , drop = FALSE]
  rownames(gate_info) <- NULL
  entry$required_fields <- strsplit(entry$required_fields, ";",
                                     fixed = TRUE)[[1L]]
  entry$gate_keys <- gate_names
  entry$gate_dictionary <- gate_info
  entry$selector_status <- decision$status
  entry$selector_method <- decision$method
  entry$evidence_ids <- decision$evidence_ids
  entry$rosner <- if (!is.null(decision$rosner)) decision$rosner else NULL
  class(entry) <- "biomedical_matrix_card"
  entry
}

bio_matrix_gate_review <- function(decision, root = ".",
                                   judgments = character()) {
  card <- bio_matrix_card(decision, root)
  gates <- card$gate_dictionary
  states <- setNames(rep("not_checked", nrow(gates)), gates$gate_key)
  if (!is.character(judgments) || anyNA(judgments))
    stop("judgments must be a named character vector.", call. = FALSE)
  if (length(judgments)) {
    keys <- names(judgments)
    if (is.null(keys) || anyNA(keys) || any(!nzchar(keys)) ||
        anyDuplicated(keys) || !all(keys %in% gates$gate_key) ||
        !all(judgments %in% c("not_checked", "documented", "concern")))
      stop("Unknown, repeated or invalid gate judgment.", call. = FALSE)
    states[keys] <- judgments
  }
  gates$status <- unname(states[gates$gate_key])
  state <- if (any(gates$status == "concern")) "blocked_by_concern"
           else if (any(gates$status == "not_checked")) "incomplete"
           else "ready_for_human_review"
  structure(list(method_id = card$method_id, method = card$selector_method,
                 review_state = state, route_class = card$route_class,
                 gate_assessments = gates, card = card,
                 clinical_validation = FALSE,
                 note = paste("Judgments record user-supplied evidence status,",
                              "not automated test eligibility or human sign-off.")),
            class = "biomedical_matrix_gate_review")
}

print.biomedical_matrix_gate_review <- function(x, ...) {
  if (!inherits(x, "biomedical_matrix_gate_review"))
    stop("Expected biomedical_matrix_gate_review object.", call. = FALSE)
  cat("Route: ", x$method_id, " | review: ", x$review_state,
      " | clinical validation: NO\n", sep = "")
  print(x$gate_assessments[, c("gate_key", "status"), drop = FALSE],
        row.names = FALSE)
  invisible(x)
}
