# Breast cancer study design, synthetic planning only.
# Sourcing defines functions; no packages installed or data read.
validate_design_probability <- function(x, name, allow_zero = FALSE) {
  if (!is.numeric(x) || length(x) != 1L || !is.finite(x) ||
      x < (if (allow_zero) 0 else .Machine$double.eps) ||
      x >= 1) stop(name, " must be in ",
                   if (allow_zero) "[0,1)." else "(0,1).", call. = FALSE)
  invisible(x)
}

cancer_design_continuous <- function(delta = 5, sd = 12,
                                     alpha = .05, power = .8,
                                     allocation_ratio = 1,
                                     loss = .1) {
  validate_design_probability(alpha, "alpha")
  validate_design_probability(power, "power")
  validate_design_probability(loss, "loss", allow_zero = TRUE)
  if (!is.numeric(delta) || length(delta) != 1L ||
      !is.finite(delta) || delta == 0 ||
      !is.numeric(sd) || length(sd) != 1L || !is.finite(sd) || sd <= 0 ||
      !is.numeric(allocation_ratio) || length(allocation_ratio) != 1L ||
      !is.finite(allocation_ratio) || allocation_ratio <= 0)
    stop("delta must be nonzero; sd and allocation_ratio must be positive.",
         call. = FALSE)
  z <- stats::qnorm(1 - alpha/2) + stats::qnorm(power)
  r <- allocation_ratio  # n_treatment / n_control
  control_approx <- ceiling(z^2 * sd^2 * (1 + 1/r)/delta^2)
  treat_approx <- ceiling(r * control_approx)
  equal_exact <- stats::power.t.test(delta = abs(delta), sd = sd,
                                    sig.level = alpha, power = power,
                                    type = "two.sample",
                                    alternative = "two.sided")$n
  list(
    assumptions = list(delta = delta, sd = sd, alpha = alpha, power = power,
                       allocation_ratio = r, loss = loss),
    normal_approx = c(control = control_approx, treatment = treat_approx),
    exact_t_equal_arm = ceiling(equal_exact),
    enrolment_normal_approx = c(
      control = ceiling(control_approx/(1-loss)),
      treatment = ceiling(treat_approx/(1-loss))),
    note = paste("Normal approximation with equal planning variances;",
                 "power.t.test exact calculation applies only to equal arms.",
                 "Loss inflation is heuristic; verify estimand and missingness.")
  )
}

cancer_design_binary <- function(p_control = .30, p_treatment = .45,
                                 alpha = .05, power = .8, loss = .1) {
  validate_design_probability(p_control, "p_control")
  validate_design_probability(p_treatment, "p_treatment")
  validate_design_probability(alpha, "alpha")
  validate_design_probability(power, "power")
  validate_design_probability(loss, "loss", allow_zero = TRUE)
  if (p_control == p_treatment)
    stop("Planning proportions must differ for a superiority power calculation.",
         call. = FALSE)
  n <- stats::power.prop.test(p1 = p_control, p2 = p_treatment,
                             sig.level = alpha, power = power,
                             alternative = "two.sided")$n
  list(p_control = p_control, p_treatment = p_treatment,
       risk_difference = p_treatment - p_control,
       n_per_arm_analyzable = ceiling(n),
       n_per_arm_enrolment = ceiling(ceiling(n)/(1-loss)),
       alpha = alpha, power = power, loss = loss,
       note = "Approximate 1:1 two-proportion design; not an exact-test guarantee.")
}

cancer_design_events <- function(hr = .75, alpha = .05, power = .8,
                                 treatment_fraction = .5) {
  if (!is.numeric(hr) || length(hr) != 1L || !is.finite(hr) ||
      hr <= 0 || hr == 1) stop("HR must be positive and not 1.", call. = FALSE)
  validate_design_probability(alpha, "alpha")
  validate_design_probability(power, "power")
  validate_design_probability(treatment_fraction, "treatment_fraction")
  q <- treatment_fraction
  z <- stats::qnorm(1-alpha/2)+stats::qnorm(power)
  events <- z^2 / (q*(1-q)*log(hr)^2)
  list(hr = hr, required_events_approx = ceiling(events),
       unrounded_events = events, treatment_fraction = q,
       alpha = alpha, power = power,
       note = paste("Asymptotic Schoenfeld log-rank/Cox event approximation.",
                    "Events are NOT enrolled participants.",
                    "Requires hazard/accrual/follow-up modeling."))
}

cancer_cluster_design_effect <- function(m = 4, icc = .15) {
  if (!is.numeric(m) || length(m) != 1L || !is.finite(m) ||
      m < 1 || m != floor(m)) stop("m must be a positive integer.", call. = FALSE)
  if (!is.numeric(icc) || length(icc) != 1L || !is.finite(icc) ||
      icc < 0 || icc >= 1) stop("ICC must be in [0,1).", call. = FALSE)
  1 + (m-1)*icc
}

cancer_paired_plan <- function(delta = 2, sd_difference = 5,
                               alpha = .05, power = .8) {
  validate_design_probability(alpha, "alpha")
  validate_design_probability(power, "power")
  if (!is.numeric(delta) || length(delta) != 1L || !is.finite(delta) ||
      delta == 0 || !is.numeric(sd_difference) ||
      length(sd_difference) != 1L || !is.finite(sd_difference) ||
      sd_difference <= 0)
    stop("delta nonzero and SD of differences positive required.", call. = FALSE)
  n <- stats::power.t.test(delta = abs(delta), sd = sd_difference,
                          sig.level = alpha, power = power,
                          type = "paired", alternative = "two.sided")$n
  list(n_complete_pairs = ceiling(n), alpha = alpha, power = power,
       note = "Power targets complete person-level paired differences, not specimens.")
}

cancer_design_scenarios <- function() {
  list(continuous = cancer_design_continuous(),
       binary = cancer_design_binary(),
       survival = cancer_design_events(),
       cluster_de = cancer_cluster_design_effect(),
       paired = cancer_paired_plan())
}
