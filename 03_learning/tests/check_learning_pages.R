# Execute each page's R examples in page-local order, with a fresh environment per page.
# Bash deployment examples are run by the workflow with a disposable output path.
paths <- sort(list.files("03_learning", pattern = "[.]md$", full.names = TRUE))
paths <- c(paths, "03_learning/bio_stats/README.md")
blocks <- 0L
for (path in paths) {
  text <- readLines(path, warn = FALSE)
  active <- FALSE
  chunk <- character()
  environment <- new.env(parent = globalenv())
  for (line in text) {
    if (!active && identical(line, "```r")) {
      active <- TRUE
      chunk <- character()
    } else if (active && identical(line, "```")) {
      expression <- parse(text = chunk, keep.source = TRUE)
      eval(expression, envir = environment)
      blocks <- blocks + 1L
      active <- FALSE
    } else if (active) {
      chunk <- c(chunk, line)
    }
  }
  stopifnot(!active)
}
cat(sprintf("PASS: %d runnable R documentation blocks across %d learning pages\n", blocks, length(paths)))
