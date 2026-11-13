# Synthetic breast-cancer protocol replay. Sourcing defines functions only.
# No external data, package installation, personal information, or file writes.

bc_with_seed <- function(seed, expr) {
  if (!is.numeric(seed) || length(seed) != 1L || !is.finite(seed) ||
      seed != floor(seed)) stop("seed must be one finite integer", call. = FALSE)
  had <- exists(".Random.seed", envir=.GlobalEnv, inherits=FALSE)
  if (had) previous <- get(".Random.seed", envir=.GlobalEnv)
  on.exit({
    if (had) assign(".Random.seed", previous, envir=.GlobalEnv)
    else if (exists(".Random.seed", envir=.GlobalEnv, inherits=FALSE))
      rm(".Random.seed", envir=.GlobalEnv)
  }, add=TRUE)
  set.seed(as.integer(seed))
  force(expr)
}

bc_plan_protocol <- function(p_a=.30, p_b=.45, loss=.10,
                             alpha=.05, power=.80) {
  p <- c(p_a,p_b,loss,alpha,power)
  if (any(!is.finite(p)) || any(p <= 0 | p >= 1) ||
      p_a == p_b) stop("Invalid binary planning parameters", call.=FALSE)
  raw <- stats::power.prop.test(p1=p_a,p2=p_b,sig.level=alpha,
                                power=power,alternative="two.sided")$n
  analyzable <- ceiling(raw)
  enrolled <- ceiling(analyzable/(1-loss))
  list(p_a=p_a,p_b=p_b,loss=loss,alpha=alpha,power=power,
       analyzable_per_arm=analyzable,
       enrolled_per_arm=enrolled,
       n_total=2L*enrolled,
       assumption="Planning proportions refer to assessable outcomes; composite documented endpoint has a different estimand.")
}

bc_simulate_trial <- function(plan=bc_plan_protocol(), seed=7122026L) {
  stopifnot(is.list(plan), length(plan$enrolled_per_arm)==1L)
  n <- as.integer(plan$enrolled_per_arm)
  if (is.na(n) || n < 2L) stop("Invalid enrollment target", call.=FALSE)
  bc_with_seed(seed, {
    arm <- factor(sample(rep(c("A","B"),each=n)),levels=c("A","B"))
    latent <- stats::rbinom(2L*n, size=1L,
                            prob=ifelse(arm=="A",plan$p_a,plan$p_b))
    available <- stats::rbinom(2L*n,size=1L,prob=1-plan$loss)
    measured <- ifelse(available==1L, latent, NA_integer_)
    documented <- as.integer(available==1L & latent==1L)
    d <- data.frame(patient_id=sprintf("SYN%04d",seq_len(2L*n)),
                    arm=arm,latent_response=latent,
                    assessment_available=available,
                    measured_response=measured,
                    documented_response=documented,
                    biomarker=round(stats::rnorm(2L*n,10,3),2))
    bc_validate_trial(d)
    d
  })
}

bc_validate_trial <- function(data) {
  required <- c("patient_id","arm","latent_response",
                "assessment_available","measured_response",
                "documented_response","biomarker")
  if (!is.data.frame(data) || !all(required %in% names(data)))
    stop("Required trial columns missing",call.=FALSE)
  if (anyNA(data$patient_id) || anyDuplicated(data$patient_id) ||
      !identical(levels(data$arm),c("A","B")) ||
      anyNA(data$arm) || any(table(data$arm)<2L) ||
      diff(as.integer(table(data$arm))) != 0L)
    stop("Invalid unique IDs or randomized 1:1 arms",call.=FALSE)
  for (name in c("latent_response","assessment_available",
                 "documented_response")) {
    x <- data[[name]]
    if (anyNA(x) || !all(x %in% c(0L,1L)))
      stop("Invalid binary column: ",name,call.=FALSE)
  }
  expected <- as.integer(data$latent_response==1L &
                         data$assessment_available==1L)
  if (!identical(as.integer(data$documented_response),expected))
    stop("Composite endpoint mismatch",call.=FALSE)
  if (!identical(is.na(data$measured_response),
                 data$assessment_available==0L))
    stop("Assessment missingness mismatch",call.=FALSE)
  observed <- which(data$assessment_available==1L)
  if (!identical(as.integer(data$measured_response[observed]),
                 as.integer(data$latent_response[observed])))
    stop("Observed-response coding mismatch",call.=FALSE)
  if (!is.numeric(data$biomarker) || any(!is.finite(data$biomarker)))
    stop("Invalid exploratory biomarker",call.=FALSE)
  invisible(TRUE)
}

bc_analyze_trial <- function(data, conf.level=.95) {
  bc_validate_trial(data)
  if (!is.numeric(conf.level) || length(conf.level)!=1L ||
      !is.finite(conf.level) || conf.level<=0 || conf.level>=1)
    stop("conf.level must be in (0,1)",call.=FALSE)
  arms <- c("A","B")
  n <- vapply(arms,function(a)sum(data$arm==a),integer(1))
  success <- vapply(arms,function(a)
    as.integer(sum(data$documented_response[data$arm==a])),integer(1))
  missing <- vapply(arms,function(a)
    as.integer(sum(data$assessment_available[data$arm==a]==0L)),integer(1))
  assessed <- n-missing
  p <- success/n
  names(p) <- arms
  difference <- unname(p["B"]-p["A"])
  se <- sqrt(sum(p*(1-p)/n))
  zcrit <- stats::qnorm(1-(1-conf.level)/2)
  ci <- difference+c(-1,1)*zcrit*se
  # Risk difference Wald CI is a teaching approximation, not universally optimal.
  primary <- suppressWarnings(stats::prop.test(x=success,n=n,correct=FALSE))
  tab <- matrix(c(success["A"],n["A"]-success["A"],
                  success["B"],n["B"]-success["B"]),
                nrow=2L,byrow=TRUE,dimnames=list(arm=arms,
                                                 documented=c("yes","no")))
  fish <- stats::fisher.test(tab)
  assessed_risk <- setNames(rep(NA_real_,2),arms)
  nonzero <- assessed>0L
  assessed_risk[nonzero] <- success[nonzero]/assessed[nonzero]
  summary <- data.frame(arm=arms,randomized=as.integer(n),
                        assessed=as.integer(assessed),
                        unassessed=as.integer(missing),
                        documented_response=as.integer(success),
                        documented_rate=as.numeric(p),
                        assessed_only_rate=as.numeric(assessed_risk))
  list(summary=summary, risk_difference=difference,
       risk_difference_ci=ci, se=se,
       primary_test=primary,fisher_test=fish,
       assessed_only_difference=if(all(nonzero))
         unname(assessed_risk["B"]-assessed_risk["A"]) else NA_real_,
       conf.level=conf.level,
       note="All values are synthetic. Endpoint is documented pCR under composite missing-assessment rule.")
}

bc_protocol_replay <- function(seed=7122026L) {
  plan <- bc_plan_protocol()
  data <- bc_simulate_trial(plan,seed)
  analysis <- bc_analyze_trial(data)
  list(plan=plan,data=data,analysis=analysis,seed=seed)
}
