# Offline regression checks for explicit quantile-method compatibility.
# Run from repository root:
# Rscript --vanilla 06_RESOURCES/tests/test_biostat_descriptive_contract.R
source("06_RESOURCES/R/biostat_descriptive_contract.R")

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
assert_close(biostat_quantiles(x, c(.25,.5,.75), "biostat8"),
             c(1.5,3.5,7))
assert_close(biostat_quantiles(x, c(.25,.5,.75), "pauls_notes"),
             c(1.75,3.5,6))

## 02 Means/SD use unrounded values; sample sd n-1
d <- biostat_descriptive_contract(c(x,NA_real_),unit="arbitrary teaching score")
stopifnot(d$total_n==5L, d$observed_n==4L, d$missing_n==1L)
assert_close(d$missing_pct,20)
assert_close(d$mean,mean(x))
assert_close(d$sample_sd,stats::sd(x))
assert_close(d$q1,1.5)
stopifnot(grepl("type 2",d$convention))

## 03 Already existing type 7 convention not silently changed
p <- biostat_descriptive_contract(x,method="pauls_notes",unit="teaching score")
assert_close(p$q1,1.75)

## 04 Missing-data handling is explicit, singleton / empty guarded
expect_error(biostat_quantiles(c(1,NA_real_)))
assert_close(biostat_quantiles(c(1,NA_real_),missing="omit"),rep(1,3L))
expect_error(biostat_quantiles(c(NA_real_,NA_real_),missing="omit"))
expect_error(biostat_quantiles(numeric()))
expect_error(biostat_quantiles(c(1,Inf)))
expect_error(biostat_quantiles(c(1,NaN)))
expect_error(biostat_quantiles(x,probs=c(-.2,.5)))
expect_error(biostat_quantiles(x,probs=c(.2,NA_real_)))
expect_error(biostat_descriptive_contract(x,unit=""))
s <- biostat_descriptive_contract(c(1,NA_real_),unit="score")
stopifnot(is.na(s$sample_sd),s$observed_n==1L)

cat("PASS: Biomedical methods 8e type-2 / Paul's Notes type-7 descriptive contract.\n")
