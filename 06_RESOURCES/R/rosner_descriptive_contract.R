# Rosner 8e method-aligned descriptive estimators.
# This is a separate opt-in module: never silently change stats_plots.R.
# Source in R or invoke functions after loading; no execution at import.
#
# Source: Rosner (2016), Fundamentals of Biostatistics, 8e,
# section 2.4, printed pp. 17-19 (quantile type 2 illustrations).
# R base stats::quantile type 7 is Paul's Notes existing convention.
#
# The author discusses the type=2 quantile algorithm; the additional
# validation, safety and reporting contracts below are editorial conventions.

rosner_quantiles <- function(x, probs = c(.25, .5, .75),
                             method = c("rosner8", "pauls_notes"),
                             missing = c("error", "omit")) {
  method <- match.arg(method)
  missing <- match.arg(missing)
  if (!is.numeric(x) || !is.null(dim(x)) || is.complex(x)) {
    stop("x must be a numeric vector.", call. = FALSE)
  }
  if (!is.numeric(probs) || !length(probs) || anyNA(probs) ||
      any(!is.finite(probs)) || any(probs < 0 | probs > 1)) {
    stop("probs must be finite probabilities in [0,1].", call. = FALSE)
  }
  if (any(is.infinite(x)) || any(is.nan(x))) {
    stop("x contains infinite or NaN values.", call. = FALSE)
  }
  if (identical(missing, "error") && anyNA(x)) {
    stop("Missing values require missing='omit'.", call. = FALSE)
  }
  observed <- x[!is.na(x)]
  if (!length(observed)) {
    stop("No observed values; quantiles undefined.", call. = FALSE)
  }
  type <- if (identical(method, "rosner8")) 2L else 7L
  stats::quantile(observed, probs = probs, type = type, names = TRUE)
}

rosner_descriptive_contract <- function(x, method = c("rosner8","pauls_notes"),
                                        unit = "unspecified") {
  method <- match.arg(method)
  if (!is.character(unit) || length(unit) != 1L ||
      is.na(unit) || !nzchar(trimws(unit))) {
    stop("unit must be a nonempty documented string.", call. = FALSE)
  }
  if (!is.numeric(x) || !is.null(dim(x)) || is.complex(x) ||
      any(is.infinite(x)) || any(is.nan(x))) {
    stop("x must contain numeric finite or NA values.", call. = FALSE)
  }
  n_total <- length(x)
  y <- x[!is.na(x)]
  n <- length(y)
  q <- if (n) unname(rosner_quantiles(
    y, probs = c(.25, .5, .75), method=method
  )) else rep(NA_real_,3L)
  data.frame(
    convention=if(method=="rosner8") "Rosner 8e (type 2)" else "Paul's Notes (type 7)",
    unit=unit,
    total_n=n_total, observed_n=n, missing_n=n_total-n,
    missing_pct=if(n_total) 100*(n_total-n)/n_total else NA_real_,
    mean=if(n)mean(y)else NA_real_,
    sample_sd=if(n>1L)stats::sd(y)else NA_real_,
    median=q[2], q1=q[1], q3=q[3],
    iqr=q[3]-q[1], stringsAsFactors=FALSE
  )
}
