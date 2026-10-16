# Synthetic binary prediction: one row per independent person.
# Sourcing defines functions only; the CLI publishes a new analysis directory.
ml_predictors <- c("marker_a", "marker_b", "age_years", "noise")

make_ml_cohort <- function(n = 160L, seed = 260416L) {
  if (length(n) != 1L || !is.numeric(n) || !is.finite(n) || n < 80 || n != floor(n))
    stop("n must be an integer of at least 80")
  set.seed(seed)
  marker_a <- rnorm(n)
  marker_b <- rnorm(n)
  age <- runif(n, 30, 75)
  probability <- plogis(-0.3 + 0.9 * marker_a - 0.5 * marker_b + 0.01 * (age - 50))
  outcome <- factor(ifelse(runif(n) < probability, "case", "control"),
                    levels = c("case", "control"))
  marker_a[sample.int(n, floor(n * 0.06))] <- NA_real_
  data.frame(person_id = sprintf("S%04d", seq_len(n)), outcome = outcome,
    marker_a = marker_a, marker_b = marker_b, age_years = age, noise = rnorm(n))
}

validate_ml_cohort <- function(data) {
  required <- c("person_id", "outcome", ml_predictors)
  if (!is.data.frame(data) || !identical(names(data), required))
    stop("Expected the documented person/outcome/predictor schema, in order")
  if (!is.character(data$person_id) || anyNA(data$person_id) ||
      any(!nzchar(trimws(data$person_id))) || anyDuplicated(data$person_id))
    stop("person_id must be unique and nonmissing; repeated records need a different design")
  if (!is.factor(data$outcome) || !identical(levels(data$outcome), c("case", "control")) ||
      anyNA(data$outcome) || any(table(data$outcome) < 8L))
    stop("Both outcome classes need at least eight people; case is the positive class")
  for (name in ml_predictors) {
    x <- data[[name]]
    if (!is.numeric(x) || any(is.infinite(x)) || all(is.na(x)))
      stop("Predictors must be numeric, not infinite or entirely missing: ", name)
  }
  invisible(TRUE)
}

make_ml_plan <- function(data, seed = 260417L, folds = 4L) {
  validate_ml_cohort(data)
  if (!is.numeric(folds) || length(folds) != 1L || !is.finite(folds) ||
      folds < 2 || folds != floor(folds)) stop("folds must be an integer of at least two")
  set.seed(seed)
  development <- sort(unlist(lapply(levels(data$outcome), function(label) {
    rows <- which(data$outcome == label)
    sample(rows, floor(0.75 * length(rows)))
  }), use.names = FALSE))
  test <- setdiff(seq_len(nrow(data)), development)
  y <- data$outcome[development]
  if (any(table(y) < folds)) stop("Too few people per class for the requested folds")
  fold_id <- integer(length(development))
  for (label in levels(y)) {
    rows <- which(y == label)
    fold_id[rows] <- sample(rep(seq_len(folds), length.out = length(rows)))
  }
  index_out <- lapply(seq_len(folds), function(i) which(fold_id == i))
  index <- lapply(index_out, function(held) setdiff(seq_along(development), held))
  names(index) <- names(index_out) <- paste0("Fold", seq_len(folds))
  plan <- list(development = development, test = test, index = index,
    index_out = index_out, seed = seed)
  validate_ml_plan(data, plan)
  plan
}

validate_ml_plan <- function(data, plan) {
  valid_rows <- function(rows, n) is.numeric(rows) && length(rows) > 0L &&
    !anyNA(rows) && all(is.finite(rows)) && all(rows == floor(rows)) &&
    all(rows >= 1L & rows <= n) && !anyDuplicated(rows)
  n <- nrow(data)
  if (!valid_rows(plan$development, n) || !valid_rows(plan$test, n) ||
      length(intersect(plan$development, plan$test)) ||
      !setequal(c(plan$development, plan$test), seq_len(n)))
    stop("Development and test rows must partition the cohort without overlap")
  for (rows in list(plan$development, plan$test))
    if (any(table(data$outcome[rows]) == 0L)) stop("Both classes required in each partition")
  size <- length(plan$development)
  if (!is.list(plan$index) || !is.list(plan$index_out) || length(plan$index) < 2L ||
      length(plan$index) != length(plan$index_out)) stop("Invalid fold lists")
  for (i in seq_along(plan$index)) {
    train <- plan$index[[i]]; assessment <- plan$index_out[[i]]
    if (!valid_rows(train, size) || !valid_rows(assessment, size) ||
        length(intersect(train, assessment)) ||
        !setequal(c(train, assessment), seq_len(size))) stop("Invalid fold partition")
    for (rows in list(train, assessment))
      if (any(table(data$outcome[plan$development[rows]]) == 0L))
        stop("Both classes required in every training and assessment fold")
  }
  held <- unlist(plan$index_out, use.names = FALSE)
  if (length(held) != size || anyDuplicated(held) || !setequal(held, seq_len(size)))
    stop("Each development person must be assessed exactly once")
  invisible(TRUE)
}

fit_ml_development <- function(data, plan, seed = 260418L) {
  validate_ml_cohort(data); validate_ml_plan(data, plan)
  packages <- c("caret", "glmnet", "ranger", "pROC")
  missing <- packages[!vapply(packages, requireNamespace, logical(1), quietly = TRUE)]
  if (length(missing)) stop("Install required packages: ", paste(missing, collapse = ", "))
  train <- data[plan$development, , drop = FALSE]
  # Reject fold-specific degenerate predictors instead of silently learning from assessment rows.
  for (rows in c(plan$index, list(seq_len(nrow(train))))) {
    for (name in ml_predictors)
      if (length(unique(na.omit(train[[name]][rows]))) < 2L)
        stop("Predictor has insufficient training-fold variation: ", name)
  }
  grids <- list(
    elastic_net = expand.grid(alpha = c(0, 0.5, 1), lambda = c(0.01, 0.1)),
    random_forest = expand.grid(mtry = c(2L, 3L), splitrule = "gini", min.node.size = c(5L, 10L)))
  models <- list(); timing <- list()
  for (name in names(grids)) {
    set.seed(seed)
    seeds <- lapply(plan$index, function(x) sample.int(1000000L, nrow(grids[[name]])))
    seeds[[length(seeds) + 1L]] <- seed
    control <- caret::trainControl(method = "cv", number = length(plan$index),
      index = plan$index, indexOut = plan$index_out, classProbs = TRUE,
      summaryFunction = caret::twoClassSummary, savePredictions = "final",
      returnResamp = "final", allowParallel = FALSE, seeds = seeds)
    arguments <- list(x = train[ml_predictors], y = train$outcome,
      method = if (name == "elastic_net") "glmnet" else "ranger",
      trControl = control, tuneGrid = grids[[name]], metric = "ROC",
      preProcess = c("medianImpute", "center", "scale"))
    if (name == "elastic_net") arguments$standardize <- FALSE
    else {
      arguments$num.trees <- 100L
      arguments$num.threads <- 1L
      arguments$importance <- "none"
    }
    set.seed(seed)
    elapsed <- system.time(models[[name]] <- do.call(caret::train, arguments))
    if (any(!is.finite(models[[name]]$results$ROC))) stop("Nonfinite tuning ROC")
    timing[[name]] <- data.frame(model = name, elapsed_seconds = unname(elapsed["elapsed"]),
      grid_candidates = nrow(grids[[name]]))
  }
  list(models = models, prevalence = mean(train$outcome == "case"),
    training_ids = train$person_id, plan = plan, predictors = ml_predictors,
    timing = do.call(rbind, timing), seed = seed)
}

binary_ml_metrics <- function(truth, probability, threshold = 0.5) {
  if (!is.factor(truth) || !identical(levels(truth), c("case", "control")) ||
      anyNA(truth) || any(table(truth) == 0L)) stop("Both outcome classes required")
  if (!is.numeric(probability) || length(probability) != length(truth) ||
      any(!is.finite(probability)) || any(probability < 0 | probability > 1))
    stop("Probabilities must be finite, aligned and between zero and one")
  if (!is.numeric(threshold) || length(threshold) != 1L || !is.finite(threshold) ||
      threshold < 0 || threshold > 1) stop("Invalid decision threshold")
  positive <- truth == "case"; predicted <- probability >= threshold
  roc <- pROC::roc(truth, probability, levels = c("control", "case"), direction = "<", quiet = TRUE)
  # Non-interpolated average precision, grouping tied predictions at the same threshold.
  order <- order(probability, decreasing = TRUE)
  ends <- c(which(diff(probability[order]) != 0), length(probability))
  true_positive <- cumsum(positive[order])[ends]
  recall <- true_positive / sum(positive)
  precision <- true_positive / ends
  data.frame(n = length(truth), prevalence = mean(positive),
    roc_auc = as.numeric(pROC::auc(roc)),
    average_precision = sum(diff(c(0, recall)) * precision),
    brier = mean((probability - as.numeric(positive))^2),
    sensitivity = mean(predicted[positive]), specificity = mean(!predicted[!positive]),
    threshold = threshold)
}

assess_ml_models <- function(fitted, test) {
  if (!is.data.frame(test) || anyDuplicated(test$person_id) ||
      any(test$person_id %in% fitted$training_ids)) stop("Test people must be distinct and unseen")
  scores <- lapply(fitted$models, function(model)
    as.numeric(predict(model, newdata = test[fitted$predictors], type = "prob")[["case"]]))
  scores$prevalence_baseline <- rep(fitted$prevalence, nrow(test))
  metrics <- lapply(names(scores), function(name)
    cbind(model = name, binary_ml_metrics(test$outcome, scores[[name]])))
  predictions <- data.frame(person_id = test$person_id, outcome = test$outcome,
    as.data.frame(scores), check.names = FALSE)
  calibration <- lapply(names(scores), function(name) {
    risk <- scores[[name]]
    bins <- cut(risk, breaks = seq(0, 1, by = 0.2), include.lowest = TRUE)
    do.call(rbind, lapply(levels(bins), function(bin) {
      selected <- bins == bin
      if (!any(selected)) return(NULL)
      data.frame(model = name, probability_bin = bin, n = sum(selected),
        mean_prediction = mean(risk[selected]), observed_fraction = mean(test$outcome[selected] == "case"))
    }))
  })
  list(metrics = do.call(rbind, metrics), predictions = predictions,
    calibration = do.call(rbind, calibration))
}

export_ml_case <- function(output_dir) {
  if (length(output_dir) != 1L || !nzchar(output_dir) || file.exists(output_dir) ||
      !dir.exists(dirname(output_dir))) stop("Choose a new output directory with an existing parent")
  parent <- normalizePath(dirname(output_dir), mustWork = TRUE)
  destination <- file.path(parent, basename(output_dir))
  root <- normalizePath(".", mustWork = TRUE)
  if (identical(destination, root) || startsWith(destination, paste0(root, .Platform$file.sep)))
    stop("Output must be outside the repository")
  stage <- tempfile("caret-stage-", tmpdir = parent)
  dir.create(stage)
  on.exit(unlink(stage, recursive = TRUE), add = TRUE)
  data <- make_ml_cohort(); plan <- make_ml_plan(data)
  fitted <- fit_ml_development(data, plan)
  assessment <- assess_ml_models(fitted, data[plan$test, , drop = FALSE])
  saveRDS(fitted, file.path(stage, "model_bundle.rds"))
  saveRDS(plan, file.path(stage, "split_plan.rds"))
  write.csv(data, file.path(stage, "synthetic_cohort.csv"), row.names = FALSE)
  write.csv(assessment$metrics, file.path(stage, "test_metrics.csv"), row.names = FALSE)
  write.csv(assessment$predictions, file.path(stage, "test_predictions.csv"), row.names = FALSE)
  write.csv(assessment$calibration, file.path(stage, "test_calibration.csv"), row.names = FALSE)
  write.csv(fitted$timing, file.path(stage, "training_timing.csv"), row.names = FALSE)
  membership <- data.frame(person_id = data$person_id, partition = "test", fold = NA_integer_)
  membership$partition[plan$development] <- "development"
  for (i in seq_along(plan$index_out)) membership$fold[plan$development[plan$index_out[[i]]]] <- i
  write.csv(membership, file.path(stage, "split_membership.csv"), row.names = FALSE)
  tuning <- do.call(rbind, lapply(names(fitted$models), function(name) {
    model <- fitted$models[[name]]
    data.frame(model = name, mean_cv_roc = mean(model$resample$ROC),
      best_parameters = paste(names(model$bestTune), unlist(model$bestTune), collapse = "; "))
  }))
  write.csv(tuning, file.path(stage, "development_selection.csv"), row.names = FALSE)
  for (name in names(fitted$models)) {
    model <- fitted$models[[name]]
    write.csv(model$results, file.path(stage, paste0(name, "_tuning.csv")), row.names = FALSE)
    write.csv(model$pred, file.path(stage, paste0(name, "_oof_predictions.csv")), row.names = FALSE)
  }
  packages <- c("caret", "glmnet", "ranger", "pROC")
  write.csv(data.frame(package = packages, version = vapply(packages,
    function(p) as.character(utils::packageVersion(p)), character(1))),
    file.path(stage, "package_versions.csv"), row.names = FALSE)
  writeLines(capture.output(sessionInfo()), file.path(stage, "session_info.txt"))
  writeLines(c("Synthetic workflow verification only; no patient data or clinical performance claim.",
    "Case is the positive class. Threshold 0.5 was fixed before assessment.",
    "Choose model families using development evidence; do not select from test_metrics.csv.",
    "Four-fold tuning summaries are selection scores, not unbiased performance estimates.",
    "The independent test is a synthetic random holdout, not external validation.",
    "Package versions record this run; a fully restorable dependency lock is separate."),
    file.path(stage, "README.txt"))
  files <- list.files(stage, full.names = TRUE)
  write.csv(data.frame(file = basename(files), md5 = unname(tools::md5sum(files))),
    file.path(stage, "file_inventory.csv"), row.names = FALSE)
  if (file.exists(destination) || !file.rename(stage, destination)) stop("Could not publish output")
  invisible(destination)
}

if (sys.nframe() == 0L) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) != 1L) stop("Usage: Rscript caret_case.R NEW_OUTPUT_DIRECTORY")
  export_ml_case(args[[1L]])
}
