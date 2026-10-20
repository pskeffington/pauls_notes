# Binomial LaTeX / R practice toolkit

[Practice sheet](worksheet.md) · [Separate answer key](answers.md) · [Reusable R solver and generator](binomial_practice.R)

Start with the worksheet, then compare your answers. There are 18 original randomized questions: exact probability, both tails, strict inequalities, and inclusive intervals.

## Run in RStudio

Open this folder as your working directory and run:

```r
source("binomial_practice.R")
result <- solve_binomial("P(X = 3; n = 10, p = 0.3)")
result$r_code
result$probability
cat(result$latex)

# Double backslashes when entering LaTeX commands in an R string.
solve_binomial("P(X \\geq 3; n = 10, p = 0.3)")

# Write a NEW worksheet and answer key outside the repository.
generate_practice(file.path(tempdir(), "binomial-set-825"), seed = 825, count = 15)
```

Base R only. Change the seed for another set; the same seed reproduces that R-generated set under the same R/RNG configuration. The shipped 18-question worksheet was generated separately using Python's random seed 20261020; the R generator does not reproduce that particular set. The R generator cycles through five single-cutoff event types; intervals appear as extension exercises in the shipped sheet.

The solver accepts one event with numeric parameters, `P(X op cutoff; n = number, p = number)`, with op `=`, `<`, `<=`, `>`, `>=`, or LaTeX equivalents. It does not parse arbitrary LaTeX, symbolic parameters, fractions, or interval syntax. Use the reference table for intervals. No input is evaluated as R code. It supports finite cutoffs and n up to 100000; n must be a nonnegative integer and p between 0 and 1. It handles noninteger cutoffs using the integer support of X.

## Verification and limits

All 18 answer-key values were compared with direct finite sums of the binomial formula using Python math and SciPy 1.17.0, tolerance 1e-12. R is unavailable in the authoring environment, so the R solver/generator has not been executed there. Run the checks below locally before relying on the toolkit:

```r
source("binomial_practice.R")
stopifnot(abs(solve_binomial("P(X = 3; n = 10, p = 0.3)")$probability - 0.266827932) < 1e-10)
for (n in c(0, 1, 10)) for (p in c(0, .3, 1)) {
  xs <- 0:n
  mass <- dbinom(xs, n, p)
  for (k in c(-1, 0, .5, n, n + 1)) for (op in c("=", "<", "<=", ">", ">=")) {
    keep <- switch(op, "="=xs==k, "<"=xs<k, "<="=xs<=k, ">"=xs>k, ">="=xs>=k)
    got <- solve_binomial(sprintf("P(X %s %s; n = %s, p = %s)", op,k,n,p))$probability
    stopifnot(abs(got - sum(mass[keep])) < 1e-12)
  }
}
```

Sources and assumptions are documented in the worksheet. This is an educational probability exercise, with invented parameters.
