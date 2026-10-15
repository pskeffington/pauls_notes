# Run from the repository root. Tests use only synthetic inputs and temporary output.
source("03_learning/examples/research_case.R")
rejects <- function(expr) inherits(tryCatch({force(expr); NULL}, error = identity), "error")
case <- make_case()
r <- analyse_case(case)
stopifnot(identical(r$ledger$n, c(8L, 16L, 14L, 6L, 7L)),
  identical(r$summary$n_missing, c(1L, 1L)),
  isTRUE(all.equal(mean(r$pairs$change_au), 1.5)),
  identical(r$pairs$person_id, c("S01", "S02", "S04", "S05", "S06", "S07")),
  "S02" %in% r$model_data$person_id)
# A pivot preserves the values and keys, including two missing observations.
wide <- to_wide(case$visits)
stopifnot(identical(wide$marker_au.baseline, c(10, 13, 12, 17, 16, 23, 20, NA_real_)))
# Row order on the registry must not silently reorder visit observations.
joined <- attach_registry(case$visits, case$registry[8:1, ])
stopifnot(identical(joined$person_id, case$visits$person_id),
  joined$age_years[joined$person_id == "S01"][1] == 24)
bad <- case
bad$registry <- rbind(bad$registry, bad$registry[1, ])
stopifnot(rejects(analyse_case(bad)))
bad <- case; bad$visits$person_id[1] <- "UNKNOWN"
stopifnot(rejects(analyse_case(bad)))
bad <- case; bad$visits <- rbind(bad$visits, bad$visits[1, ])
stopifnot(rejects(analyse_case(bad)))
bad <- case; colnames(bad$assay) <- rev(colnames(bad$assay))
stopifnot(rejects(analyse_case(bad)))
bad <- case; bad$visits$marker_au[1] <- Inf
stopifnot(rejects(analyse_case(bad)))
stopifnot(all(r$scaled$values["DemoConstant", ] == 0),
  all(is.na(r$scaled$values["DemoMissing", ])),
  max(abs(rowMeans(r$scaled$values[1:2, ]))) < 1e-12,
  all((r$prediction$upr - r$prediction$lwr) > (r$confidence$upr - r$confidence$lwr)))
# Check the actual CLI, its artifact contract, and refusal to overwrite an earlier run.
workspace <- tempfile("learning-case-")
dir.create(workspace)
output <- file.path(workspace, "run with spaces")
status <- system2(file.path(R.home("bin"), "Rscript"),
  c("--vanilla", "03_learning/examples/research_case.R", shQuote(output)), stdout = FALSE)
stopifnot(status == 0L)
expected <- c("analysis_bundle.rds", "complete_pairs.csv", "diagnostics.pdf", "feature_scaling.csv",
  "individual_prediction.csv", "interpretation.txt", "mean_confidence.csv", "measurement_summary.csv",
  "model_coefficients.csv", "model_summary.txt", "observation_counts.csv", "output_checksums.csv",
  "session.txt", "synthetic_registry.csv", "synthetic_visits.csv")
stopifnot(setequal(list.files(output), expected), all(file.info(file.path(output, expected))$size > 0))
checks <- read.csv(file.path(output, "output_checksums.csv"))
stopifnot(identical(as.character(checks$md5), unname(tools::md5sum(file.path(output, checks$file)))))
before <- tools::md5sum(file.path(output, "analysis_bundle.rds"))
stopifnot(rejects(write_case(output)))
stopifnot(identical(before, tools::md5sum(file.path(output, "analysis_bundle.rds"))))
unlink(workspace, recursive = TRUE)
cat("PASS: known counts and paired change; keys, joins, missingness, scaling, intervals, CLI artifacts and overwrite rejection\n")
