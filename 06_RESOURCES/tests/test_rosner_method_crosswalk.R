# Synthetic contract checks. Run from any working directory using Rscript.
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (!length(file_arg)) stop("Run using Rscript --vanilla <test path>.")
here <- dirname(normalizePath(sub("^--file=", "", file_arg[1L]), mustWork = TRUE))
source(file.path(here, "..", "R", "biomedical_test_selector.R"))
source(file.path(here, "..", "R", "rosner_method_crosswalk.R"))
registry <- utils::read.csv(file.path(here, "..", "..", "03_learning",
                                       "bio_stats", "rosner_method_registry.csv"),
                            stringsAsFactors = FALSE, colClasses = "character",
                            check.names = FALSE)
stopifnot(nrow(registry) == 27L,
          !anyDuplicated(registry$method_id),
          all(c("method_id", "topic", "rosner_chapters", "coverage") %in% names(registry)),
          all(registry$coverage %in% c("textbook", "extension", "design_gate")))
for (i in seq_len(nrow(registry))) {
  x <- rosner_method_crosswalk(registry$method_id[i])
  stopifnot(identical(x$method_id, registry$method_id[i]),
            identical(x$coverage, registry$coverage[i]),
            identical(paste(x$chapters, collapse = ";"), registry$rosner_chapters[i]))
}
x <- biomedical_method_decision("continuous", design = "independent", n_groups = 2L)
y <- rosner_annotate_decision(x)
stopifnot(identical(x$method_id, "welch-t"),
          identical(y$method_id, x$method_id),
          identical(y$status, x$status),
          identical(y$required_checks, x$required_checks),
          identical(y$rosner$chapters, "8"))
survey <- rosner_annotate_decision(biomedical_method_decision(
  "binary", design = "complex_survey", n_groups = 2L))
stopifnot(identical(survey$method_id, "survey-design-review"),
          identical(survey$rosner$coverage, "extension"),
          identical(length(survey$rosner$chapters), 0L))
# The primary selector must return the same decision with opt-in enrichment.
opt <- biomedical_method_decision("continuous", n_groups = 2L,
                                  include_rosner = TRUE)
base <- biomedical_method_decision("continuous", n_groups = 2L)
stopifnot(is.null(base$rosner),
          identical(opt$method_id, base$method_id),
          identical(opt$status, base$status),
          identical(opt$evidence_ids, base$evidence_ids),
          identical(opt$required_checks, base$required_checks),
          identical(opt$decision_path, base$decision_path),
          identical(opt$rosner$chapters, "8"),
          any(grepl("Rosner 8e chapters: 8",
                    capture.output(print(opt)), fixed = TRUE)))
opt_survey <- biomedical_method_decision("binary", design = "complex_survey",
                                          n_groups = 2L, include_rosner = TRUE)
stopifnot(identical(opt_survey$method_id, "survey-design-review"),
          identical(opt_survey$rosner$coverage, "extension"),
          identical(length(opt_survey$rosner$chapters), 0L))
stopifnot(identical(rosner_method_crosswalk("omics-design-review")$coverage,
                    "extension"))

failed <- function(expr) inherits(try(expr, silent = TRUE), "try-error")
stopifnot(failed(rosner_method_crosswalk("unknown-method")),
          failed(rosner_method_crosswalk(NA_character_)),
          failed(rosner_method_crosswalk(character())),
          failed(rosner_annotate_decision(list())),
          failed(biomedical_method_decision("binary", include_rosner = NA)),
          failed(biomedical_method_decision("binary", include_rosner = 1)))
# Analytic exact-tail identity: probability of >=k includes k.
k <- 36L; n <- 80L; p0 <- .35
tail <- stats::pbinom(k - 1L, n, p0, lower.tail = FALSE)
direct <- sum(stats::dbinom(k:n, n, p0))
stopifnot(isTRUE(all.equal(tail, direct, tolerance = 1e-12)))
rate <- 40 / 100000 * 20000
stopifnot(identical(rate, 8))
cat("PASS: Rosner registry, selector annotations, error handling and exact binomial tail.\n")
