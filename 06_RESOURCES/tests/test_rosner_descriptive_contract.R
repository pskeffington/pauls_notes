# Independently authored, offline regression tests for Rosner 8e compatibility.
# Run from repository root:
# Rscript --vanilla 06_RESOURCES/tests/test_rosner_descriptive_contract.R
source("06_RESOURCES/R/rosner_descriptive_contract.R")

assert_close <- function(actual, expected, tolerance=1e-12) {
  stopifnot(isTRUE(all.equal(as.numeric(actual), as.numeric(expected),
                             tolerance=tolerance)))
}
expect_error <- function(expr) {
  got <- inherits(try(expr, silent=TRUE), "try-error")
  if (!got) stop("Expected an error.", call.=FALSE)
}

## 01 Quantiles: distinct conventions, known finite synthetic vector
x <- c(1,2,5,9)
assert_close(rosner_quantiles(x, c(.25,.5,.75), "rosner8"),
             c(1.5,3.5,7))
assert_close(rosner_quantiles(x, c(.25,.5,.75), "pauls_notes"),
             c(1.75,3.5,6))

## 02 Means/SD use unrounded values; sample sd n-1
d <- rosner_descriptive_contract(c(x,NA_real_),unit="arbitrary teaching score")
stopifnot(d$total_n==5L, d$observed_n==4L, d$missing_n==1L)
assert_close(d$missing_pct,20)
assert_close(d$mean,mean(x))
assert_close(d$sample_sd,stats::sd(x))
assert_close(d$q1,1.5)
stopifnot(grepl("type 2",d$convention))

## 03 Already existing type 7 convention not silently changed
p <- rosner_descriptive_contract(x,method="pauls_notes",unit="teaching score")
assert_close(p$q1,1.75)

## 04 Missing-data handling is explicit, singleton / empty guarded
expect_error(rosner_quantiles(c(1,NA_real_)))
assert_close(rosner_quantiles(c(1,NA_real_),missing="omit"),1)
expect_error(rosner_quantiles(c(NA_real_,NA_real_),missing="omit"))
expect_error(rosner_quantiles(numeric()))
expect_error(rosner_quantiles(c(1,Inf)))
expect_error(rosner_quantiles(c(1,NaN)))
expect_error(rosner_quantiles(x,probs=c(-.2,.5)))
expect_error(rosner_quantiles(x,probs=c(.2,NA_real_)))
expect_error(rosner_descriptive_contract(x,unit=""))
s <- rosner_descriptive_contract(c(1,NA_real_),unit="score")
stopifnot(is.na(s$sample_sd),s$observed_n==1L)

cat("PASS: Rosner 8e type-2 / Paul's Notes type-7 descriptive contract.\n")
