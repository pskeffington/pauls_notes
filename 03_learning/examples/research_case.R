# Synthetic research computing case. All values and identifiers are invented.
# Base R only; source this file to use helpers without running the deployment.
assert <- function(ok, message) {
  if (length(ok) != 1L || is.na(ok) || !ok) stop(message, call. = FALSE)
}

require_key <- function(data, columns) {
  assert(is.data.frame(data), "Expected a data frame")
  assert(all(columns %in% names(data)), "Missing key column")
  keys <- data[columns]
  assert(!anyNA(keys), "Keys must not be missing")
  assert(all(vapply(keys, function(x) all(nzchar(as.character(x))), logical(1))),
         "Keys must not be empty")
  assert(!anyDuplicated(keys), "Duplicate key")
  invisible(data)
}

attach_registry <- function(visits, registry) {
  require_key(visits, c("person_id", "visit"))
  require_key(registry, "person_id")
  added <- setdiff(names(registry), "person_id")
  assert(!any(added %in% names(visits)), "Ambiguous overlapping columns")
  index <- match(visits$person_id, registry$person_id)
  assert(!anyNA(index), "Visit has no registry match")
  result <- cbind(visits, registry[index, added, drop = FALSE])
  rownames(result) <- NULL
  assert(nrow(result) == nrow(visits), "Join changed visit count")
  result
}

make_case <- function() {
  registry <- data.frame(
    person_id = sprintf("S%02d", seq_len(8)),
    age_years = seq(24, 59, by = 5),
    arm = factor(rep(c("Reference", "Alternate"), each = 4),
                 levels = c("Reference", "Alternate")),
    questionnaire_code = c("yes", NA, "no", "unknown", "no", "yes", "no", "yes"),
    stringsAsFactors = FALSE)
  wide <- data.frame(person_id = registry$person_id,
    baseline = c(10, 13, 12, 17, 16, 23, 20, NA_real_),
    followup = c(11, 15, NA_real_, 18, 19, 24, 21, 25))
  visits <- reshape(wide, varying = c("baseline", "followup"),
    v.names = "marker_au", timevar = "visit", times = c("baseline", "followup"),
    idvar = "person_id", direction = "long")
  visits <- visits[order(visits$person_id, visits$visit), ]
  rownames(visits) <- NULL
  visits$collected_on <- as.Date("2030-01-01") + ifelse(visits$visit == "baseline", 0, 14)
  assay <- rbind(DemoA = c(1, 3, 2, 4, 5, 7, 6, 8),
                 DemoB = c(8, 6, 7, 5, 4, 2, 3, 1),
                 DemoConstant = rep(5, 8), DemoMissing = rep(NA_real_, 8))
  colnames(assay) <- registry$person_id
  list(registry = registry, visits = visits, assay = assay)
}

read_case <- function(registry_path, visits_path, assay) {
  registry <- read.csv(registry_path, colClasses = c("character", "numeric", "character", "character"),
    na.strings = "NA", check.names = FALSE, stringsAsFactors = FALSE)
  visits <- read.csv(visits_path, colClasses = c("character", "character", "numeric", "character"),
    na.strings = "NA", check.names = FALSE, stringsAsFactors = FALSE)
  assert(identical(names(registry), c("person_id", "age_years", "arm", "questionnaire_code")),
         "Unexpected registry header")
  assert(identical(names(visits), c("person_id", "visit", "marker_au", "collected_on")),
         "Unexpected visits header")
  assert(!anyNA(registry$arm) && all(registry$arm %in% c("Reference", "Alternate")),
         "Unexpected arm category")
  registry$arm <- factor(registry$arm, levels = c("Reference", "Alternate"))
  assert(!anyNA(visits$collected_on) &&
    all(grepl("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", visits$collected_on)), "Expected ISO calendar dates")
  visits$collected_on <- as.Date(visits$collected_on, format = "%Y-%m-%d")
  assert(!anyNA(visits$collected_on), "Invalid collection date")
  list(registry = registry, visits = visits, assay = assay)
}

to_wide <- function(visits) {
  require_key(visits, c("person_id", "visit"))
  assert(setequal(unique(visits$visit), c("baseline", "followup")), "Unexpected visit labels")
  assert(nrow(visits) == 2L * length(unique(visits$person_id)), "Expected two visit rows per person")
  out <- reshape(visits[c("person_id", "visit", "marker_au")],
    idvar = "person_id", timevar = "visit", direction = "wide")
  out <- out[order(out$person_id), c("person_id", "marker_au.baseline", "marker_au.followup")]
  rownames(out) <- NULL
  out
}

scale_features <- function(assay) {
  assert(is.matrix(assay) && is.numeric(assay), "Expected numeric feature-by-specimen matrix")
  assert(!any(is.infinite(assay)), "Assay contains infinity")
  result <- matrix(NA_real_, nrow(assay), ncol(assay), dimnames = dimnames(assay))
  states <- character(nrow(assay))
  for (i in seq_len(nrow(assay))) {
    observed <- is.finite(assay[i, ])
    if (sum(observed) < 2L) {
      states[i] <- "insufficient_observations"
    } else if (sd(assay[i, observed]) == 0) {
      result[i, observed] <- 0
      states[i] <- "constant_displayed_at_zero"
    } else {
      result[i, observed] <- as.numeric(scale(assay[i, observed]))
      states[i] <- "row_z_score"
    }
  }
  list(values = result, status = states)
}

analyse_case <- function(case) {
  joined <- attach_registry(case$visits, case$registry)
  assert(is.numeric(joined$marker_au), "Measurement must be numeric")
  assert(all(is.na(joined$marker_au) | is.finite(joined$marker_au)), "Invalid measurement")
  require_key(case$registry, "person_id")
  assert(identical(colnames(case$assay), case$registry$person_id), "Assay order must match registry")
  assert(!is.null(rownames(case$assay)) && !anyDuplicated(rownames(case$assay)), "Feature IDs must be unique")
  summary <- do.call(rbind, lapply(c("baseline", "followup"), function(v) {
    x <- joined$marker_au[joined$visit == v]
    data.frame(visit = v, n_total = length(x), n_observed = sum(is.finite(x)),
      n_missing = sum(is.na(x)), mean_au = if (any(is.finite(x))) mean(x, na.rm = TRUE) else NA_real_)
  }))
  wide <- to_wide(joined)
  keep <- is.finite(wide$marker_au.baseline) & is.finite(wide$marker_au.followup)
  pairs <- wide[keep, ]
  assert(nrow(pairs) >= 2L, "Need at least two complete pairs")
  pairs$change_au <- pairs$marker_au.followup - pairs$marker_au.baseline
  baseline <- joined[joined$visit == "baseline", ]
  eligible <- is.finite(baseline$marker_au) & is.finite(baseline$age_years)
  model_data <- baseline[eligible, ]
  assert(nrow(model_data) >= 4L && length(unique(model_data$age_years)) >= 2L,
         "Model requires enough observations and variable ages")
  model <- lm(marker_au ~ age_years, data = model_data, na.action = na.fail)
  points <- data.frame(age_years = seq(min(model_data$age_years), max(model_data$age_years), length.out = 30))
  prediction <- cbind(points, predict(model, newdata = points, interval = "prediction"))
  confidence <- cbind(points, predict(model, newdata = points, interval = "confidence"))
  ledger <- data.frame(step = c("registry", "visit_rows", "observed_measurements", "complete_pairs", "baseline_model"),
    unit = c("people", "person_visits", "measurements", "people", "people"),
    n = c(nrow(case$registry), nrow(joined), sum(is.finite(joined$marker_au)), nrow(pairs), nrow(model_data)))
  list(joined = joined, summary = summary, pairs = pairs, model = model,
    model_data = model_data, confidence = confidence, prediction = prediction,
    ledger = ledger, scaled = scale_features(case$assay))
}

write_case <- function(output) {
  assert(length(output) == 1L && nzchar(output), "Expected one output directory")
  assert(!file.exists(output) && !dir.exists(output) && !(!is.na(Sys.readlink(output)) && nzchar(Sys.readlink(output))), "Output already exists; use a new path")
  parent <- dirname(output)
  assert(dir.exists(parent), "Output parent must exist")
  stage <- tempfile(pattern = ".research-case-", tmpdir = parent)
  assert(dir.create(stage), "Cannot create staging directory")
  on.exit(unlink(stage, recursive = TRUE), add = TRUE)
  case <- make_case()
  csv <- function(x, name) write.csv(x, file.path(stage, name), row.names = FALSE, na = "NA")
  csv(case$registry, "synthetic_registry.csv")
  csv(case$visits, "synthetic_visits.csv")
  case <- read_case(file.path(stage, "synthetic_registry.csv"),
    file.path(stage, "synthetic_visits.csv"), case$assay)
  result <- analyse_case(case)
  csv(result$summary, "measurement_summary.csv")
  csv(result$pairs, "complete_pairs.csv")
  csv(result$ledger, "observation_counts.csv")
  csv(result$confidence, "mean_confidence.csv")
  csv(result$prediction, "individual_prediction.csv")
  csv(data.frame(term = names(coef(result$model)), estimate = unname(coef(result$model)),
    confint(result$model), check.names = FALSE), "model_coefficients.csv")
  csv(data.frame(feature = rownames(case$assay), status = result$scaled$status), "feature_scaling.csv")
  bundle <- list(inputs = case, analysis = result,
    metadata = list(units = "invented arbitrary units", design = "deterministic teaching fixture"))
  saveRDS(bundle, file.path(stage, "analysis_bundle.rds"))
  assert(identical(readRDS(file.path(stage, "analysis_bundle.rds"))$inputs, case), "RDS round trip failed")
  capture.output(sessionInfo(), file = file.path(stage, "session.txt"))
  capture.output(summary(result$model), file = file.path(stage, "model_summary.txt"))
  writeLines(c("All values are synthetic. No population or clinical finding is claimed.",
    "Contrast: followup minus baseline; units: invented arbitrary units.",
    "Paired mean change = 1.5; complete pairs = 6; baseline model people = 7.",
    "Intervals illustrate the linear model assumptions; they do not validate the model.",
    "Constant features display at zero; all-missing features remain missing."),
    file.path(stage, "interpretation.txt"))
  grDevices::pdf(file.path(stage, "diagnostics.pdf"), width = 9, height = 7)
  tryCatch({
    par(mfrow = c(2, 2))
    matplot(t(as.matrix(result$pairs[c("marker_au.baseline", "marker_au.followup")])),
      type = "l", lty = 1, col = "#0072B2", xaxt = "n", xlab = "Visit", ylab = "Marker (invented au)", main = "Six complete synthetic pairs")
    axis(1, at = 1:2, labels = c("Baseline", "Followup"))
    plot(marker_au ~ age_years, data = result$model_data, xlab = "Age (years)",
      ylab = "Marker (invented au)", main = "Baseline model: seven people")
    abline(result$model, col = "#0072B2")
    plot(fitted(result$model), residuals(result$model), xlab = "Fitted marker (au)",
      ylab = "Residual (au)", main = "Residual pattern"); abline(h = 0, lty = 2)
    qqnorm(residuals(result$model), main = "Residual normal-quantile check")
    qqline(residuals(result$model))
    par(mfrow = c(1, 1), mar = c(5, 8, 3, 2))
    image(seq_len(ncol(case$assay)), seq_len(nrow(case$assay)), t(result$scaled$values),
      zlim = c(-2, 2), col = colorRampPalette(c("#2166AC", "white", "#B2182B"))(101),
      axes = FALSE, xlab = "Synthetic people", ylab = "", main = "Feature row z-scores; white also denotes missing")
    axis(1, at = seq_len(ncol(case$assay)), labels = colnames(case$assay))
    axis(2, at = seq_len(nrow(case$assay)), labels = rownames(case$assay), las = 2)
  }, finally = grDevices::dev.off())
  files <- sort(list.files(stage, full.names = TRUE))
  csv(data.frame(file = basename(files), md5 = unname(tools::md5sum(files))), "output_checksums.csv")
  assert(!file.exists(output) && !dir.exists(output) && !(!is.na(Sys.readlink(output)) && nzchar(Sys.readlink(output))), "Output appeared while processing")
  assert(file.rename(stage, output), "Could not publish staged outputs")
  invisible(result$ledger)
}

if (sys.nframe() == 0L) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) != 1L) stop("Usage: Rscript research_case.R NEW_OUTPUT_DIRECTORY", call. = FALSE)
  print(write_case(args[[1]]))
}
