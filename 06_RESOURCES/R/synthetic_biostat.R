# Fully synthetic teaching fixture; NEVER use as clinical observations.
# Base R only; no NHANES / Dartmouth records or real-person identifiers.

pn_make_synthetic_biostat <- function(n = 120L, seed = 712L) {
  if (length(n) != 1L || !is.numeric(n) || !is.finite(n) ||
      n != floor(n) || n < 20L) stop("n must be integer >= 20.")
  if (length(seed) != 1L || !is.numeric(seed) || !is.finite(seed) ||
      seed != floor(seed) || seed < 0L || seed > .Machine$integer.max)
    stop("seed must be a nonnegative integer.")
  # Preserve caller RNG state when it exists.
  had_seed <- exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE)
  if (had_seed) old_seed <- get(".Random.seed", envir = .GlobalEnv)
  on.exit({
    if (had_seed) assign(".Random.seed", old_seed, envir = .GlobalEnv)
    else if (exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE))
      rm(".Random.seed", envir = .GlobalEnv)
  }, add = TRUE)
  set.seed(seed)
  group <- factor(rep(c("Reference", "Exposure"), length.out = n),
                  levels = c("Reference", "Exposure"))
  exposure <- as.integer(group == "Exposure")
  age <- sample(20:79, n, replace = TRUE)
  hb <- rnorm(n, mean = 13.2 - 1.1 * exposure, sd = 1.7)
  marker <- rlnorm(n, meanlog = 0.3 + 0.25 * exposure, sdlog = 0.8)
  hb[5L] <- NA_real_
  marker[9L] <- NA_real_
  marker[12L] <- 0 # log exclusion fixture; valid on raw scale
  data.frame(synthetic_id = sprintf("SYN-%04d", seq_len(n)),
             group = group, age_years = age,
             hemoglobin_g_dl = hb, marker_mg_l = marker,
             stringsAsFactors = FALSE)
}
