args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2L)
input <- args[[1]]; workspace <- args[[2]]
source("03_learning/examples/practice_tools.R")
rejects <- function(expr) inherits(tryCatch({force(expr); NULL}, error = identity), "error")
x <- read_signal(input)
stopifnot(identical(x$record_id, sprintf("%02d", seq_len(6))))
result <- summarize_signal(x, 3)
stopifnot(identical(result$n_total, c(3L, 3L)), identical(result$n_measured, c(2L, 3L)),
  identical(result$n_missing, c(1L, 0L)), is.na(result$mean_au[1]), result$mean_au[2] == 10,
  identical(result$status, c("withheld", "reported")), summarize_signal(x, 2)$mean_au[1] == 5)
for (minimum in list(0, 2.5, Inf, NA_real_, "3")) stopifnot(rejects(summarize_signal(x, minimum)))
all_missing <- x; all_missing$signal_au <- rep(NA_real_, nrow(x))
stopifnot(all(summarize_signal(all_missing, 1)$n_measured == 0L),
  all(is.na(summarize_signal(all_missing, 1)$mean_au)))
stopifnot(all(summarize_signal(x[FALSE, ], 1)$n_total == 0L))
discovered <- sort(list.files(workspace, pattern = "^(Alpha|Beta)[.]tsv$", full.names = TRUE))
stopifnot(length(discovered) == 2L)
files <- setNames(discovered, c("alpha", "beta"))
batch <- batch_signal(files, 2)
stopifnot(identical(batch$inventory$rows, c(3L, 3L)),
  batch$results$alpha$mean_au[1] == 5, batch$results$beta$mean_au[2] == 10,
  rejects(batch_signal(setNames(c(files[1], files[1]), c("one", "two")))))
quoted <- read.csv(file.path(workspace, "quoted.csv"), colClasses = "character")
stopifnot(ncol(quoted) == 2L, quoted$label == "two, words")
cli <- normalizePath("03_learning/examples/summarize_records.R")
rscript <- file.path(R.home("bin"), "Rscript")
call <- function(arguments, quiet = TRUE) suppressWarnings(system2(rscript,
  c("--vanilla", shQuote(cli), vapply(arguments, shQuote, character(1))), stdout = FALSE, stderr = if (quiet) FALSE else ""))
output <- file.path(workspace, "checked summary.csv")
stopifnot(call(c(input, "3", output), quiet = FALSE) == 0L)
actual <- read.csv(output)
stopifnot(is.na(actual$mean_au[1]), actual$mean_au[2] == 10)
before <- tools::md5sum(c(input, output))
stopifnot(call(c(input, "3", output)) != 0L, call(c(input, "3", input)) != 0L)
stopifnot(identical(before, tools::md5sum(c(input, output))))
for (value in c("0", "1.2", "Inf", "missing")) {
  candidate <- file.path(workspace, paste0("invalid-", value, ".csv"))
  stopifnot(call(c(input, value, candidate)) != 0L, !file.exists(candidate))
}
for (name in c("duplicate", "header", "value", "category", "fields")) {
  candidate <- file.path(workspace, paste0("bridge-rejected-", name, ".csv"))
  stopifnot(call(c(file.path(workspace, paste0(name, ".tsv")), "1", candidate)) != 0L,
    !file.exists(candidate))
}
cat("PASS: parsed numeric TSV, batch identities, reporting minimum, all-missing data, quoted CSV and actual Rscript failures\n")
