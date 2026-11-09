# Probability and study design

[Computing subjects](README.md) · [Related: execution](run-and-package.md)

For cross-sectional, case-control, cohort, randomized, diagnostic, prediction and synthesis designs, read [study types with nine published-paper examples](study-designs-and-published-examples.md). It separates random sampling from random allocation and shows how design changes the estimand before a statistical test is selected.

## A reproducible simulation has a declared purpose

The deployed eight-person case uses fixed values to teach exact counts and failure checks. A probability simulation answers a different question: how a specified generator behaves across repeated draws. A seed makes a pseudorandom sequence reproducible within a recorded environment; it does not validate the generator as a biological model.

```r
set.seed(731)
normal_draw <- rnorm(2000, mean = 0, sd = 1)
count_draw <- rpois(2000, lambda = 3)
success_draw <- rbinom(2000, size = 10, prob = 0.2)
stopifnot(length(normal_draw) == 2000L)
stopifnot(all(count_draw >= 0), all(success_draw %in% 0:10))
c(normal_mean = mean(normal_draw), poisson_mean = mean(count_draw),
  binomial_mean = mean(success_draw))
```

A normal model is continuous and unbounded. A Poisson count model imposes a mean–variance relationship and integer support. A binomial model describes a specified number of Bernoulli trials under its assumptions. None should be chosen merely because a biomedical variable has a similar-looking histogram. Truncating or clipping a normal draw changes the distribution; document that change instead of describing the result as an ordinary normal sample.

## Distinguish probability functions

R's `d*` functions evaluate density or mass, `p*` functions cumulative probability, `q*` functions quantiles, and `r*` functions generate draws. A continuous density height is not the probability of one exact value. Check parameter meaning and units in the distribution's documentation.

To investigate interval coverage, generate many independent datasets under a stated model, fit the intended analysis to each, and count how often its interval contains the generator's known parameter. That is a property under the chosen simulation conditions; it does not prove coverage under an actual study's unknown data-generating process.

## Complex survey samples require design information

Sampling weights, strata and primary sampling units describe the collection design. A weighted mean is not a complete variance estimator for a complex survey. Supplying sampling weights to ordinary `lm()` does not make it a survey-design analysis.

With the optional `survey` package installed, this entirely invented balanced design illustrates the interface:

```r
if (requireNamespace("survey", quietly = TRUE)) {
  sample <- data.frame(psu = rep(1:4, each = 2),
    stratum = rep(c("A", "B"), each = 4),
    weight = rep(c(1, 2, 1, 2), each = 2),
    measurement = c(3, 5, 4, 6, 7, 9, 8, 10))
  design <- survey::svydesign(ids = ~psu, strata = ~stratum,
    weights = ~weight, data = sample)
  estimate <- survey::svymean(~measurement, design)
  stopifnot(is.finite(as.numeric(coef(estimate))))
}
```

The artificial design has two sampled clusters per stratum. Real designs may require nesting rules, finite-population corrections, replicate weights, domain estimation and special handling of single-cluster strata. Use the study's documentation rather than inventing missing design variables.

## Check repeatability and support

[Learning check LC17](mastery-checks.md#transform-compare-and-model) repeats normal, uniform and Bernoulli draws under the same seed. LC25 compares a weighted estimate with a design-aware survey calculation and checks its standard error. Explain why matching weighted means does not establish that an ordinary weighted regression uses the correct sampling variance.

## Transfer exercise

Repeat the probability experiment with the same seed, then a different seed. Separate invariant support constraints from sample means that naturally fluctuate. Describe what additional design information would be needed before applying the survey example to a real public-health dataset.

References: [R probability distributions](https://search.r-project.org/R/refmans/stats/html/Distributions.html), [random-number generation](https://search.r-project.org/R/refmans/base/html/Random.html), [survey design specification](https://r-survey.r-forge.r-project.org/survey/html/svydesign.html).
