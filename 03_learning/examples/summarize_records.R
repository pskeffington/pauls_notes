# Standalone CLI: parse constrained TSV, count observed measurements, stage CSV output.
arguments <- commandArgs(trailingOnly = TRUE)
if (length(arguments) != 3L) stop("Expected INPUT.tsv MINIMUM NEW_OUTPUT.csv", call. = FALSE)
script_arg <- grep("^--file=", commandArgs(), value = TRUE)
script_dir <- dirname(normalizePath(sub("^--file=", "", script_arg[[1]])))
source(file.path(script_dir, "practice_tools.R"))
input <- arguments[[1]]
minimum <- suppressWarnings(as.numeric(arguments[[2]]))
output <- arguments[[3]]
if (!file.exists(input)) stop("Input is missing")
is_link <- function(path) {
  destination <- Sys.readlink(path)
  length(destination) == 1L && !is.na(destination) && nzchar(destination)
}
if (file.exists(output) || is_link(output)) stop("Output already exists")
if (!dir.exists(dirname(output))) stop("Output parent is missing")
result <- summarize_signal(read_signal(input), minimum)
stage <- tempfile(".signal-summary-", tmpdir = dirname(output))
tryCatch({
  write.csv(result, stage, row.names = FALSE, na = "NA")
  if (file.exists(output) || is_link(output)) stop("Output appeared during processing")
  if (!file.rename(stage, output)) stop("Could not publish summary")
}, finally = unlink(stage))
