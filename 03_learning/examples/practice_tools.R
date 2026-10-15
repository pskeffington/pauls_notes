# Small reusable practice functions; source without generating files.
# Inputs are teaching records, not clinical measurements or decisions.
checked_offsets <- function(values, offsets) {
  stopifnot(is.numeric(values), is.numeric(offsets),
    length(offsets) == 1L || length(offsets) == length(values))
  values + offsets
}

clean_panel <- function(x) {
  stopifnot(is.character(x), !anyNA(x))
  labels <- tolower(trimws(x))
  if (!all(labels %in% c("alpha", "beta"))) stop("Unsupported panel label")
  factor(labels, levels = c("alpha", "beta"))
}

decode_response <- function(x) {
  stopifnot(is.character(x))
  dictionary <- c(Y = "reported_yes", N = "reported_no", R = "refused", U = "uncertain")
  if (!all(is.na(x) | x %in% names(dictionary))) stop("Unsupported questionnaire response")
  factor(unname(dictionary[x]), levels = unname(dictionary))
}

checked_scatter <- function(data, x, y, x_unit, y_unit, draw = TRUE) {
  stopifnot(is.data.frame(data), length(x) == 1L, length(y) == 1L,
    x %in% names(data), y %in% names(data),
    is.numeric(data[[x]]), is.numeric(data[[y]]),
    is.character(x_unit), is.character(y_unit), length(x_unit) == 1L, length(y_unit) == 1L,
    !is.na(x_unit), !is.na(y_unit), nzchar(x_unit), nzchar(y_unit),
    is.logical(draw), length(draw) == 1L, !is.na(draw))
  keep <- is.finite(data[[x]]) & is.finite(data[[y]])
  if (!any(keep)) stop("No finite plot pairs")
  if (draw) plot(data[[x]][keep], data[[y]][keep],
    xlab = paste0(x, " (", x_unit, ")"), ylab = paste0(y, " (", y_unit, ")"))
  list(n_total = nrow(data), n_eligible = sum(keep), n_excluded = sum(!keep),
    rows = which(keep), x_unit = x_unit, y_unit = y_unit)
}

summarize_signal <- function(data, minimum) {
  stopifnot(is.data.frame(data), identical(names(data), c("record_id", "panel", "signal_au")),
    is.character(data$record_id), !anyNA(data$record_id),
    all(grepl("^[A-Za-z0-9_-]+$", data$record_id)), !anyDuplicated(data$record_id),
    is.character(data$panel), !anyNA(data$panel), all(data$panel %in% c("Alpha", "Beta")),
    is.numeric(data$signal_au), all(is.na(data$signal_au) | is.finite(data$signal_au)),
    is.numeric(minimum), length(minimum) == 1L, is.finite(minimum),
    minimum >= 1, minimum == floor(minimum))
  do.call(rbind, lapply(c("Alpha", "Beta"), function(label) {
    x <- data$signal_au[data$panel == label]
    n <- sum(is.finite(x))
    report <- n >= minimum
    data.frame(panel = label, n_total = length(x), n_measured = n,
      n_missing = sum(is.na(x)), mean_au = if (report) mean(x, na.rm = TRUE) else NA_real_,
      status = if (report) "reported" else "withheld")
  }))
}

read_signal <- function(path) {
  widths <- count.fields(path, sep = "\t", quote = "", comment.char = "", blank.lines.skip = FALSE)
  stopifnot(length(widths) > 0L, !anyNA(widths), all(widths == 3L))
  data <- read.delim(path, colClasses = "character", na.strings = character(),
    quote = "", comment.char = "", check.names = FALSE, row.names = NULL,
    stringsAsFactors = FALSE, blank.lines.skip = FALSE, fill = FALSE)
  stopifnot(identical(names(data), c("record_id", "panel", "signal_au")))
  literal <- data$signal_au
  stopifnot(!anyNA(literal), all(literal == "NA" | grepl("^[+-]?[0-9]+([.][0-9]+)?$", literal)))
  parsed <- rep(NA_real_, length(literal))
  measured <- literal != "NA"
  parsed[measured] <- as.numeric(literal[measured])
  data$signal_au <- parsed
  # Header-only input retains a declared numeric measurement column.
  summarize_signal(data, 1)
  data
}

batch_signal <- function(paths, minimum = 1) {
  stopifnot(is.character(paths), length(paths) > 0L, !anyNA(paths),
    !is.null(names(paths)), !anyNA(names(paths)), all(nzchar(names(paths))),
    !anyDuplicated(names(paths)), all(file.exists(paths)))
  physical_paths <- normalizePath(paths, mustWork = TRUE)
  if (anyDuplicated(physical_paths)) stop("Repeated input path")
  before <- tools::md5sum(paths)
  results <- lapply(paths, function(path) summarize_signal(read_signal(path), minimum))
  stopifnot(identical(before, tools::md5sum(paths)))
  list(results = results, inventory = data.frame(label = names(paths),
    file = basename(paths), md5 = unname(before),
    rows = vapply(paths, function(path) nrow(read_signal(path)), integer(1)),
    row.names = NULL))
}
