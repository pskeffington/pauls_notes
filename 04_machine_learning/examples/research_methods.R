# Direct survival and limma workflows; no caret dependency, synthetic inputs only.
make_survival_cohort <- function(n = 180L, seed = 260420L) {
  set.seed(seed)
  age <- runif(n, 30, 75); marker <- rnorm(n)
  event_time <- rexp(n, rate = 0.025 * exp(0.02 * (age - 50) + 0.5 * marker))
  censor_time <- runif(n, 5, 60)
  data.frame(person_id = sprintf("S%04d", seq_len(n)), age_years = age, marker = marker,
    time_months = pmin(event_time, censor_time), event = as.integer(event_time <= censor_time))
}

fit_survival_example <- function(data, train, test) {
  if (!requireNamespace("survival", quietly = TRUE)) stop("Install survival")
  required <- c("person_id", "age_years", "marker", "time_months", "event")
  if (!is.data.frame(data) || !identical(names(data), required) || anyNA(data) ||
      !is.character(data$person_id) || any(!nzchar(data$person_id)) || anyDuplicated(data$person_id))
    stop("Invalid survival schema or person identifiers")
  if (!all(vapply(data[-1], is.numeric, logical(1))) ||
      any(!is.finite(as.matrix(data[-1]))) || any(data$time_months <= 0) ||
      any(!data$event %in% c(0, 1))) stop("Invalid times, predictors or event codes")
  valid <- function(x) is.numeric(x) && length(x) > 0 && !anyNA(x) &&
    all(is.finite(x)) && all(x == floor(x)) && all(x >= 1 & x <= nrow(data)) && !anyDuplicated(x)
  if (!valid(train) || !valid(test) || length(intersect(train, test)) ||
      !setequal(c(train, test), seq_len(nrow(data)))) stop("Invalid person partitions")
  if (sum(data$event[train]) < 10 || sum(data$event[test]) < 2)
    stop("Insufficient observed events for this demonstration")
  fit <- survival::coxph(survival::Surv(time_months, event) ~ age_years + marker,
    data = data[train, ], x = TRUE, y = TRUE, model = TRUE)
  score <- as.numeric(predict(fit, newdata = data[test, ], type = "lp", reference = "sample"))
  assessment <- data[test, ]; assessment$score <- score
  concordance <- survival::concordance(survival::Surv(time_months, event) ~ score,
    data = assessment, reverse = TRUE)
  if (!is.finite(concordance$concordance) || any(!is.finite(coef(fit))))
    stop("Nonfinite survival fit or assessment")
  list(model = fit, predictions = assessment,
    concordance = concordance$concordance, proportional_hazards = survival::cox.zph(fit)$table,
    train = train, test = test)
}

make_expression_case <- function(seed = 260421L) {
  set.seed(seed)
  metadata <- data.frame(sample_id = sprintf("Sample%02d", 1:24),
    group = factor(rep(c("control", "case"), each = 12), levels = c("control", "case")),
    batch = factor(rep(c("batch_a", "batch_b"), 12)))
  expression <- matrix(rnorm(120 * 24, mean = 6, sd = 0.5), nrow = 120,
    dimnames = list(sprintf("Feature%03d", 1:120), metadata$sample_id))
  expression[1:5, metadata$group == "case"] <- expression[1:5, metadata$group == "case"] + 1
  list(expression = expression, metadata = metadata)
}

fit_expression_example <- function(expression, metadata, scale) {
  if (!requireNamespace("limma", quietly = TRUE)) stop("Install limma")
  if (!identical(scale, "log2_expression")) stop("This example requires documented log2 expression")
  if (!is.matrix(expression) || !is.numeric(expression) || any(!is.finite(expression)) ||
      nrow(expression) < 10 || ncol(expression) < 8 || is.null(rownames(expression)) ||
      is.null(colnames(expression)) || anyDuplicated(rownames(expression)) ||
      anyDuplicated(colnames(expression))) stop("Invalid feature-by-sample matrix")
  if (!is.data.frame(metadata) || !all(c("sample_id", "group", "batch") %in% names(metadata)) ||
      anyNA(metadata) || anyDuplicated(metadata$sample_id) ||
      !setequal(metadata$sample_id, colnames(expression))) stop("Sample metadata do not match the assay")
  metadata <- metadata[match(colnames(expression), metadata$sample_id), , drop = FALSE]
  if (!is.factor(metadata$group) || !identical(levels(metadata$group), c("control", "case")) ||
      any(table(metadata$group) < 3)) stop("Explicit control/case factor with replicates required")
  design <- model.matrix(~ batch + group, data = metadata)
  if (qr(design)$rank < ncol(design)) stop("Batch and group design is not identifiable")
  fit <- limma::eBayes(limma::lmFit(expression, design))
  table <- limma::topTable(fit, coef = "groupcase", number = Inf, adjust.method = "BH", sort.by = "P")
  list(model = fit, results = table, design = design, sample_ids = metadata$sample_id,
    scale = scale, interpretation = "Adjusted expression association; not a predictive classifier")
}

export_research_methods <- function(output_dir) {
  if (length(output_dir) != 1 || !nzchar(output_dir) || file.exists(output_dir) || (!is.na(Sys.readlink(output_dir)) && nzchar(Sys.readlink(output_dir))) ||
      !dir.exists(dirname(output_dir))) stop("Choose a new output directory with an existing parent")
  parent <- normalizePath(dirname(output_dir), mustWork = TRUE)
  destination <- file.path(parent, basename(output_dir)); root <- normalizePath(".")
  if (identical(destination, root) || startsWith(destination, paste0(root, .Platform$file.sep)))
    stop("Output must be outside the repository")
  stage <- tempfile("research-methods-", tmpdir = parent); dir.create(stage)
  on.exit(unlink(stage, recursive = TRUE), add = TRUE)
  cohort <- make_survival_cohort()
  set.seed(173); train <- sort(sample.int(nrow(cohort), floor(0.75 * nrow(cohort))))
  survival <- fit_survival_example(cohort, train, setdiff(seq_len(nrow(cohort)), train))
  assay <- make_expression_case()
  expression <- fit_expression_example(assay$expression, assay$metadata, "log2_expression")
  saveRDS(list(survival = survival, expression = expression), file.path(stage, "models.rds"))
  write.csv(survival$predictions, file.path(stage, "survival_test_scores.csv"), row.names = FALSE)
  write.csv(data.frame(concordance = survival$concordance), file.path(stage, "survival_metrics.csv"), row.names = FALSE)
  write.csv(survival$proportional_hazards, file.path(stage, "proportional_hazards_diagnostics.csv"))
  write.csv(expression$results, file.path(stage, "expression_associations.csv"))
  write.csv(expression$design, file.path(stage, "expression_design.csv"))
  saveRDS(list(survival = cohort, expression = assay), file.path(stage, "synthetic_inputs.rds"))
  writeLines(capture.output(sessionInfo()), file.path(stage, "session_info.txt"))
  writeLines(c("Synthetic methods only; no clinical findings.",
    "Cox score is relative log hazard, not an event probability.",
    "Concordance is descriptive; no censoring-adjusted horizon calibration is supplied.",
    "Limma estimates adjusted expression associations; it does not validate a classifier."), file.path(stage, "README.txt"))
  if (file.exists(destination) || (!is.na(Sys.readlink(destination)) && nzchar(Sys.readlink(destination))) || !file.rename(stage, destination)) stop("Could not publish output")
  invisible(destination)
}

if (sys.nframe() == 0L) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) != 1L) stop("Usage: Rscript research_methods.R NEW_OUTPUT_DIRECTORY")
  export_research_methods(args[[1L]])
}
