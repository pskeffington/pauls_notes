# Contract checks and deliberate leakage challenges; no clinical AUC target.
source("04_machine_learning/examples/caret_case.R")
rejects <- function(expr) inherits(tryCatch({force(expr); NULL}, error = identity), "error")
data <- make_ml_cohort()
stopifnot(identical(data, make_ml_cohort()), validate_ml_cohort(data))
plan <- make_ml_plan(data)
stopifnot(identical(plan, make_ml_plan(data)),
  !length(intersect(plan$development, plan$test)),
  length(unlist(plan$index_out)) == length(plan$development))
duplicate <- data; duplicate$person_id[2] <- duplicate$person_id[1]
stopifnot(rejects(validate_ml_cohort(duplicate)))
bad <- data; bad$marker_b[1] <- Inf
stopifnot(rejects(validate_ml_cohort(bad)))
bad <- data; bad$noise <- NA_real_
stopifnot(rejects(validate_ml_cohort(bad)))
bad <- data; bad$outcome <- factor(rep("case", nrow(bad)), levels = c("case", "control"))
stopifnot(rejects(validate_ml_cohort(bad)), rejects(make_ml_plan(data, folds = 1000L)))
overlap <- plan; overlap$test[1] <- overlap$development[1]
stopifnot(rejects(validate_ml_plan(data, overlap)))
overlap <- plan; overlap$index_out[[1]][1] <- overlap$index[[1]][1]
stopifnot(rejects(validate_ml_plan(data, overlap)))

truth <- factor(c("case", "control", "case", "control"), levels = c("case", "control"))
perfect <- binary_ml_metrics(truth, c(1, 0, 1, 0))
constant <- binary_ml_metrics(truth, rep(0.5, 4))
reversed <- binary_ml_metrics(truth, c(0, 1, 0, 1))
stopifnot(perfect$roc_auc == 1, perfect$average_precision == 1, perfect$brier == 0,
  constant$roc_auc == 0.5, constant$average_precision == 0.5, constant$brier == 0.25,
  reversed$roc_auc == 0, rejects(binary_ml_metrics(truth, c(2, 0, 1, 0))))

output <- tempfile("caret-test-output-")
check_export <- function() {
  on.exit(unlink(output, recursive = TRUE), add = TRUE)
  export_ml_case(output)
  fitted <- readRDS(file.path(output, "model_bundle.rds"))
  plan <- fitted$plan
  stopifnot(identical(sort(fitted$training_ids), sort(data$person_id[plan$development])),
    identical(fitted$predictors, ml_predictors), !"person_id" %in% fitted$predictors,
    !"outcome" %in% fitted$predictors, rejects(export_ml_case(output)))
  assessment <- assess_ml_models(fitted, data[plan$test, , drop = FALSE])
  stopifnot(nrow(assessment$metrics) == 3L,
    all(is.finite(assessment$metrics$roc_auc)),
    all(assessment$metrics$n == length(plan$test)),
    all(assessment$metrics$brier >= 0 & assessment$metrics$brier <= 1),
    rejects(assess_ml_models(fitted, data[plan$development, , drop = FALSE])))
  for (name in names(fitted$models)) {
    model <- fitted$models[[name]]
    stopifnot(identical(sort(model$pred$rowIndex), seq_along(plan$development)),
      identical(model$control$index, plan$index),
      isTRUE(all.equal(unname(model$preProcess$mean[ml_predictors]),
        unname(colMeans(data[plan$development, ml_predictors], na.rm = TRUE)))))
  }
  # Altering held-out predictors cannot change fitted preprocessing or tuning results.
  changed <- data
  changed[plan$test, ml_predictors] <- 100000
  replay <- fit_ml_development(changed, plan)
  for (name in names(fitted$models)) {
    stopifnot(identical(fitted$models[[name]]$bestTune, replay$models[[name]]$bestTune),
      isTRUE(all.equal(fitted$models[[name]]$results, replay$models[[name]]$results)),
      isTRUE(all.equal(fitted$models[[name]]$preProcess$mean, replay$models[[name]]$preProcess$mean)))
    probability <- predict(replay$models[[name]], data[plan$test, ml_predictors], type = "prob")$case
    stopifnot(isTRUE(all.equal(probability, assessment$predictions[[name]], tolerance = 1e-10)))
  }
  inventory <- read.csv(file.path(output, "file_inventory.csv"), stringsAsFactors = FALSE)
  stopifnot(all(file.exists(file.path(output, inventory$file))),
    identical(unname(tools::md5sum(file.path(output, inventory$file))), inventory$md5))
  stopifnot(file.info(file.path(output, "test_calibration.csv"))$size > 0)
}
check_export()
cat("PASS: patient partitions, fold integrity, leakage challenge, two caret engines, probability metrics and replayed exports\n")
