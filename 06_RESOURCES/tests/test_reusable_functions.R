# Standalone helper validation and reproducible jitter.
source("06_RESOURCES/R/Reusable_Functions.R")
rejects <- function(expr) inherits(tryCatch({force(expr); NULL}, error=identity), "error")
stopifnot(rejects(summary_cov(matrix(1:4, 2))), rejects(summary_cov(c(1, Inf))))
if (requireNamespace("ggplot2", quietly=TRUE)) {
  data <- data.frame(group=rep(c("A", "B"), each=3), x=1:6, y=6:1)
  stopifnot(rejects(plt_hist(data, "absent")), rejects(plt_hist(data, "x", bins=0)),
            rejects(plt_scatter(data, "group", "y")))
  set.seed(47)
  before <- .Random.seed
  one <- ggplot2::ggplot_build(plt_box(data, "group", "x"))$data[[2]]$x
  two <- ggplot2::ggplot_build(plt_box(data, "group", "x"))$data[[2]]$x
  stopifnot(identical(one, two), identical(before, .Random.seed),
            inherits(plt_hist(data, "x"), "ggplot"),
            inherits(plt_scatter(data, "x", "y", fit=TRUE), "ggplot"))
}
cat("PASS: standalone plotting input validation and deterministic jitter\n")
