source("04_machine_learning/examples/research_methods.R")
rejects <- function(expr) inherits(tryCatch({force(expr); NULL}, error = identity), "error")
cohort <- make_survival_cohort(); train <- seq_len(135); test <- 136:180
fit <- fit_survival_example(cohort, train, test)
stopifnot(is.finite(fit$concordance), fit$concordance >= 0, fit$concordance <= 1,
  rejects(fit_survival_example(cohort, train, c(135, test))))
bad <- cohort; bad$event[1] <- 2
stopifnot(rejects(fit_survival_example(bad, train, test)))
bad <- cohort; bad$time_months[1] <- 0
stopifnot(rejects(fit_survival_example(bad, train, test)))
changed <- cohort; changed$marker[test] <- 1000
replay <- fit_survival_example(changed, train, test)
stopifnot(identical(coef(fit$model), coef(replay$model)))
score <- as.numeric(predict(fit$model, cohort[test, ], type = "lp", reference = "sample"))
stopifnot(isTRUE(all.equal(score, fit$predictions$score)))

case <- make_expression_case()
association <- fit_expression_example(case$expression, case$metadata, "log2_expression")
reordered <- fit_expression_example(case$expression, case$metadata[24:1, ], "log2_expression")
stopifnot(identical(association$results, reordered$results), nrow(association$results) == 120,
  all(association$results$adj.P.Val >= 0 & association$results$adj.P.Val <= 1),
  all(association$results[sprintf("Feature%03d", 1:5), "logFC"] > 0),
  rejects(fit_expression_example(case$expression, case$metadata, "raw_counts")))
duplicate <- case$metadata; duplicate$sample_id[2] <- duplicate$sample_id[1]
stopifnot(rejects(fit_expression_example(case$expression, duplicate, "log2_expression")))
confounded <- case$metadata; confounded$batch <- factor(confounded$group)
stopifnot(rejects(fit_expression_example(case$expression, confounded, "log2_expression")))
check_export <- function() {
  out <- tempfile("research-methods-test-")
  on.exit(unlink(out, recursive = TRUE), add = TRUE)
  export_research_methods(out)
  saved <- readRDS(file.path(out, "models.rds"))
  inputs <- readRDS(file.path(out, "synthetic_inputs.rds"))
  replay <- predict(saved$survival$model, inputs$survival[saved$survival$test, ], type = "lp", reference = "sample")
  stopifnot(isTRUE(all.equal(as.numeric(replay), saved$survival$predictions$score)),
    rejects(export_research_methods(out)))
}
check_export()
cat("PASS: Cox censoring/event contracts and replay; limma sample alignment, contrasts, confounding and export\n")

# A dangling symlink is an occupied output path, not a new destination.
check_dangling_output <- function() {
  link <- tempfile("dangling-output-")
  target <- tempfile("absent-target-")
  on.exit(unlink(link), add=TRUE)
  if (.Platform$OS.type == "unix" && file.symlink(target, link)) {
    stopifnot(inherits(try(export_research_methods(link), silent=TRUE), "try-error"),
              identical(Sys.readlink(link), target), !file.exists(target))
  }
}
check_dangling_output()
