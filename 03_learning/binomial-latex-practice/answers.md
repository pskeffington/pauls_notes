# Binomial practice: answer key

All 18 values independently checked by summing the binomial formula and comparing with SciPy CDF/PMF/SF (absolute tolerance 1e-12). R code is provided for learner execution.

## Answer 1

```r
dbinom(23, size = 30, prob = 0.7)
```

\[P(X = 23)=\binom{30}{23}(0.7)^{23}(0.3)^{7}\approx 0.121854\]

## Answer 2

```r
pbinom(6, size = 25, prob = 0.5)
```

\[P(X \leq 6)=\sum_{j=0}^{6}\binom{25}{j}(0.5)^j(0.5)^{25-j}\approx 0.007317\]

## Answer 3

```r
pbinom(14, size = 15, prob = 0.1)
```

\[P(X < 15)=\sum_{j=0}^{14}\binom{15}{j}(0.1)^j(0.9)^{15-j}\approx 1.000000\]

## Answer 4

```r
pbinom(-1, size = 8, prob = 0.25, lower.tail = FALSE)
```

\[P(X \geq 0)=\sum_{j=0}^{8}\binom{8}{j}(0.25)^j(0.75)^{8-j}\approx 1.000000\]

## Answer 5

```r
pbinom(3, size = 12, prob = 0.8, lower.tail = FALSE)
```

\[P(X > 3)=\sum_{j=4}^{12}\binom{12}{j}(0.8)^j(0.2)^{12-j}\approx 0.999938\]

## Answer 6

```r
pbinom(3, size = 8, prob = 0.3) - pbinom(0, size = 8, prob = 0.3)
```

\[P(1\leq X\leq 3)=\sum_{j=1}^{3}\binom{8}{j}(0.3)^j(0.7)^{8-j}\approx 0.748248\]

## Answer 7

```r
dbinom(6, size = 25, prob = 0.8)
```

\[P(X = 6)=\binom{25}{6}(0.8)^{6}(0.2)^{19}\approx 0.000000\]

## Answer 8

```r
pbinom(0, size = 10, prob = 0.1)
```

\[P(X \leq 0)=\sum_{j=0}^{0}\binom{10}{j}(0.1)^j(0.9)^{10-j}\approx 0.348678\]

## Answer 9

```r
pbinom(3, size = 10, prob = 0.2)
```

\[P(X < 4)=\sum_{j=0}^{3}\binom{10}{j}(0.2)^j(0.8)^{10-j}\approx 0.879126\]

## Answer 10

```r
pbinom(7, size = 15, prob = 0.6, lower.tail = FALSE)
```

\[P(X \geq 8)=\sum_{j=8}^{15}\binom{15}{j}(0.6)^j(0.4)^{15-j}\approx 0.786897\]

## Answer 11

```r
pbinom(24, size = 30, prob = 0.3, lower.tail = FALSE)
```

\[P(X > 24)=\sum_{j=25}^{30}\binom{30}{j}(0.3)^j(0.7)^{30-j}\approx 0.000000\]

## Answer 12

```r
pbinom(23, size = 25, prob = 0.7) - pbinom(1, size = 25, prob = 0.7)
```

\[P(2\leq X\leq 23)=\sum_{j=2}^{23}\binom{25}{j}(0.7)^j(0.3)^{25-j}\approx 0.998429\]

## Answer 13

```r
dbinom(1, size = 12, prob = 0.3)
```

\[P(X = 1)=\binom{12}{1}(0.3)^{1}(0.7)^{11}\approx 0.071184\]

## Answer 14

```r
pbinom(16, size = 25, prob = 0.1)
```

\[P(X \leq 16)=\sum_{j=0}^{16}\binom{25}{j}(0.1)^j(0.9)^{25-j}\approx 1.000000\]

## Answer 15

```r
pbinom(2, size = 10, prob = 0.7)
```

\[P(X < 3)=\sum_{j=0}^{2}\binom{10}{j}(0.7)^j(0.3)^{10-j}\approx 0.001590\]

## Answer 16

```r
pbinom(4, size = 15, prob = 0.5, lower.tail = FALSE)
```

\[P(X \geq 5)=\sum_{j=5}^{15}\binom{15}{j}(0.5)^j(0.5)^{15-j}\approx 0.940765\]

## Answer 17

```r
pbinom(1, size = 12, prob = 0.25, lower.tail = FALSE)
```

\[P(X > 1)=\sum_{j=2}^{12}\binom{12}{j}(0.25)^j(0.75)^{12-j}\approx 0.841618\]

## Answer 18

```r
pbinom(3, size = 8, prob = 0.5) - pbinom(0, size = 8, prob = 0.5)
```

\[P(1\leq X\leq 3)=\sum_{j=1}^{3}\binom{8}{j}(0.5)^j(0.5)^{8-j}\approx 0.359375\]
## Sources and provenance

Original exercises; probability definitions and R mappings checked against:

- R Core Team. *The Binomial Distribution*. https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Binomial.html
- OpenStax. *Introductory Statistics 2e*, section 4.3, Binomial Distribution. https://openstax.org/books/introductory-statistics-2e/pages/4-3-binomial-distribution

Sources accessed October 20, 2026. No textbook exercises were copied.
