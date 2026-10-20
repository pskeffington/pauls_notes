# Binomial practice: LaTeX to R and back

18 original randomized exercises. Fixed worksheet seed: 20261020 (Python random).
All parameters are invented teaching values, not observed data or source estimates.
Assume a fixed number of independent binary trials and the same success probability on each trial.

For every problem, identify n and p; translate the event into R; calculate its probability;
then write the event and numerical answer in LaTeX. Round final answers to six decimal places.
A displayed 0.000000 can be a small positive probability rounded to zero.

## Translation reference

| Event | R |
| --- | --- |
| Exactly k | `dbinom(k, size = n, prob = p)` |
| At most k | `pbinom(k, size = n, prob = p)` |
| Fewer than k | `pbinom(k - 1, size = n, prob = p)` |
| More than k | `pbinom(k, size = n, prob = p, lower.tail = FALSE)` |
| At least k | `pbinom(k - 1, size = n, prob = p, lower.tail = FALSE)` |
| From a through b, inclusive | `pbinom(b, n, p) - pbinom(a - 1, n, p)` |

The reference assumes integer cutoffs. Upper tails are strictly greater than the pbinom cutoff.
An empty sum is zero.

## Worked example

\[X\sim\operatorname{Binomial}(10,0.3),\quad P(X=3)\]

```r
dbinom(3, size = 10, prob = 0.3)
```

\[P(X=3)=\binom{10}{3}(0.3)^3(0.7)^7\approx 0.266828\]

## Problem 1

\[X\sim\operatorname{Binomial}(30,0.7),\qquad P(X = 23)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 2

\[X\sim\operatorname{Binomial}(25,0.5),\qquad P(X \leq 6)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 3

\[X\sim\operatorname{Binomial}(15,0.1),\qquad P(X < 15)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 4

\[X\sim\operatorname{Binomial}(8,0.25),\qquad P(X \geq 0)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 5

\[X\sim\operatorname{Binomial}(12,0.8),\qquad P(X > 3)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 6

\[X\sim\operatorname{Binomial}(8,0.3),\qquad P(1\leq X\leq 3)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 7

\[X\sim\operatorname{Binomial}(25,0.8),\qquad P(X = 6)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 8

\[X\sim\operatorname{Binomial}(10,0.1),\qquad P(X \leq 0)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 9

\[X\sim\operatorname{Binomial}(10,0.2),\qquad P(X < 4)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 10

\[X\sim\operatorname{Binomial}(15,0.6),\qquad P(X \geq 8)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 11

\[X\sim\operatorname{Binomial}(30,0.3),\qquad P(X > 24)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 12

\[X\sim\operatorname{Binomial}(25,0.7),\qquad P(2\leq X\leq 23)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 13

\[X\sim\operatorname{Binomial}(12,0.3),\qquad P(X = 1)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 14

\[X\sim\operatorname{Binomial}(25,0.1),\qquad P(X \leq 16)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 15

\[X\sim\operatorname{Binomial}(10,0.7),\qquad P(X < 3)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 16

\[X\sim\operatorname{Binomial}(15,0.5),\qquad P(X \geq 5)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 17

\[X\sim\operatorname{Binomial}(12,0.25),\qquad P(X > 1)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________

## Problem 18

\[X\sim\operatorname{Binomial}(8,0.5),\qquad P(1\leq X\leq 3)\]

R code: ____________________

Probability: ____________________

LaTeX answer: ____________________
## Sources and provenance

Original exercises; probability definitions and R mappings checked against:

- R Core Team. *The Binomial Distribution*. https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Binomial.html
- OpenStax. *Introductory Statistics 2e*, section 4.3, Binomial Distribution. https://openstax.org/books/introductory-statistics-2e/pages/4-3-binomial-distribution

Sources accessed October 20, 2026. No textbook exercises were copied.
