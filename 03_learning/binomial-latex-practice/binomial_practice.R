# Binomial LaTeX -> R -> LaTeX practice toolkit. Base R only.
# Source this file; it performs no analysis or file writes on import.
# Sources: R stats Binomial manual and OpenStax Introductory Statistics 2e 4.3.

solve_binomial <- function(input, digits = 6L) {
  if (!is.character(input) || length(input) != 1L || is.na(input))
    stop("input must be one nonmissing character string")
  if (length(digits) != 1L || !is.numeric(digits) || !is.finite(digits) ||
      digits != floor(digits) || digits < 0 || digits > 15)
    stop("digits must be an integer from 0 to 15")
  text <- input
  for (token in c("\\leq", "\\le")) text <- gsub(token, "<=", text, fixed = TRUE)
  for (token in c("\\geq", "\\ge")) text <- gsub(token, ">=", text, fixed = TRUE)
  for (token in c("\\left", "\\right", "\\(", "\\)", "\\[", "\\]",
                  "\\,", "\\;", "\\!", "\\ ", "$"))
    text <- gsub(token, "", text, fixed = TRUE)
  text <- gsub("[[:space:]]+", "", text)
  num <- "[+-]?(?:[0-9]+(?:\\.[0-9]*)?|\\.[0-9]+)(?:[eE][+-]?[0-9]+)?"
  pattern <- paste0("^P\\([Xx](<=|>=|=|<|>)(", num,
                    ");n=(", num, "),p=(", num, ")\\)$")
  a <- regmatches(text, regexec(pattern, text, perl = TRUE))[[1L]]
  if (!length(a)) stop("Expected P(X <= 3; n = 10, p = 0.3), or =, <, >, >=")
  op <- a[2L]; x <- as.numeric(a[3L]); n <- as.numeric(a[4L]); p <- as.numeric(a[5L])
  if (any(!is.finite(c(x, n, p))) || n < 0 || n != floor(n) || p < 0 || p > 1)
    stop("Require finite x, nonnegative integer n, and 0 <= p <= 1")
  # Bound n for this teaching solver, avoiding impractical support allocations.
  if (n > 100000) stop("Teaching solver supports n <= 100000")
  call_text <- switch(op,
    "=" = if (x == floor(x)) sprintf("dbinom(%s, size = %s, prob = %s)", x,n,p) else "0",
    "<=" = sprintf("pbinom(%s, size = %s, prob = %s)", floor(x),n,p),
    "<" = sprintf("pbinom(%s, size = %s, prob = %s)", ceiling(x)-1,n,p),
    ">" = sprintf("pbinom(%s, size = %s, prob = %s, lower.tail = FALSE)", floor(x),n,p),
    ">=" = sprintf("pbinom(%s, size = %s, prob = %s, lower.tail = FALSE)", ceiling(x)-1,n,p))
  # Calculate directly: never eval(parse()) user input.
  answer <- switch(op,
    "=" = if (x == floor(x)) dbinom(x,n,p) else 0,
    "<=" = pbinom(floor(x),n,p), "<" = pbinom(ceiling(x)-1,n,p),
    ">" = pbinom(floor(x),n,p,lower.tail=FALSE),
    ">=" = pbinom(ceiling(x)-1,n,p,lower.tail=FALSE))
  tex_op <- switch(op, "<="="\\leq", ">="="\\geq", op)
  latex <- sprintf("\\[P(X %s %s \\mid n=%s,\\,p=%s)\\approx %s\\]",
                   tex_op,x,n,p,formatC(answer,format="f",digits=digits))
  list(input=input, x=x, n=n, p=p, operator=op,
       r_code=call_text, probability=answer, latex=latex)
}

# Create another randomized worksheet and separate answer key.
# output_dir MUST be new; use a directory outside the repository.
generate_practice <- function(output_dir, seed = 825L, count = 15L) {
  if (length(count)!=1L || !is.numeric(count) || !is.finite(count) ||
      count < 1 || count != floor(count) || count > 1000)
    stop("count must be an integer from 1 to 1000")
  if (length(seed)!=1L || !is.numeric(seed) || !is.finite(seed) ||
      seed < 0 || seed > .Machine$integer.max || seed != floor(seed))
    stop("seed must be a nonnegative R integer")
  if (length(output_dir)!=1L || !is.character(output_dir) || is.na(output_dir) ||
      !nzchar(output_dir) || file.exists(output_dir)) stop("Choose a new output directory")
  # Preserve the caller's random-number state.
  had_seed <- exists(".Random.seed", envir=.GlobalEnv, inherits=FALSE)
  if (had_seed) old_seed <- get(".Random.seed", envir=.GlobalEnv)
  on.exit(if (had_seed) assign(".Random.seed",old_seed,envir=.GlobalEnv)
          else if (exists(".Random.seed",envir=.GlobalEnv,inherits=FALSE))
            rm(".Random.seed",envir=.GlobalEnv), add=TRUE)
  set.seed(seed)
  questions <- c("# Binomial practice: LaTeX to R and back", "",
    sprintf("Seed: %s. Assume independent trials with a common success probability.",seed),
    "For each item: identify n and p, write R code, calculate, and write a LaTeX answer.", "")
  answers <- c("# Answer key", "", paste("R version:",getRversion()), "")
  for (i in seq_len(count)) {
    n <- sample(c(8L,10L,12L,15L,20L,25L,30L),1L)
    p <- sample(c(.1,.2,.25,.3,.4,.5,.6,.7,.8),1L)
    x <- sample.int(n+1L,1L)-1L
    op <- c("=","<=","<",">=",">")[(i-1L) %% 5L+1L]
    input <- sprintf("P(X %s %s; n = %s, p = %s)",op,x,n,p)
    result <- solve_binomial(input)
    questions <- c(questions,sprintf("## Problem %s",i),"",
      sprintf("\\[X\\sim\\operatorname{Binomial}(%s,%s),\\quad P(X %s %s)\\]",
        n,p,switch(op,"<="="\\leq",">="="\\geq",op),x),
      "", "R code: __________", "", "Probability and LaTeX: __________", "")
    answers <- c(answers,sprintf("## Answer %s",i),"","```r",result$r_code,"```","",result$latex,"")
  }
  sources <- c("## Sources", "",
    "- R Core Team, The Binomial Distribution: https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Binomial.html",
    "- OpenStax, Introductory Statistics 2e, section 4.3: https://openstax.org/books/introductory-statistics-2e/pages/4-3-binomial-distribution")
  if (!dir.create(output_dir,recursive=TRUE)) stop("Could not create output directory")
  writeLines(c(questions,sources),file.path(output_dir,"worksheet.md"))
  writeLines(c(answers,sources),file.path(output_dir,"answers.md"))
  invisible(normalizePath(output_dir))
}
