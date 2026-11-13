# Synthetic protocol-to-analysis contract and independent arithmetic checks.
args <- commandArgs(trailingOnly=FALSE)
file_arg <- grep("^--file=",args,value=TRUE)
if (!length(file_arg)) stop("Use Rscript --vanilla <test path>.")
here <- dirname(normalizePath(sub("^--file=","",file_arg[1L]),
                              mustWork=TRUE))
source(file.path(here,"..","examples","breast_cancer_protocol_replay.R"))
rejects <- function(expr) inherits(try(expr,silent=TRUE),"try-error")
set.seed(123L)
original_rng <- .Random.seed
x <- bc_protocol_replay()
stopifnot(identical(.Random.seed,original_rng),
          identical(x$data,bc_protocol_replay()$data),
          identical(x$analysis$summary,
                    bc_analyze_trial(x$data)$summary),
          nrow(x$data)==x$plan$n_total,
          all(table(x$data$arm)==x$plan$enrolled_per_arm),
          !anyDuplicated(x$data$patient_id),
          !anyNA(x$data$documented_response))
a <- x$analysis
stopifnot(sum(a$summary$randomized)==nrow(x$data),
          all(a$summary$randomized==
              a$summary$assessed+a$summary$unassessed),
          all(a$summary$documented_response<=a$summary$assessed),
          identical(a$summary$arm,c("A","B")),
          isTRUE(all.equal(a$risk_difference,
             a$summary$documented_response[2L]/a$summary$randomized[2L]-
             a$summary$documented_response[1L]/a$summary$randomized[1L])),
          length(a$risk_difference_ci)==2L,
          all(is.finite(a$risk_difference_ci)),
          a$risk_difference_ci[1L] <= a$risk_difference_ci[2L],
          a$primary_test$p.value >=0,a$primary_test$p.value<=1,
          isTRUE(all.equal(a$risk_difference,
                unname(diff(a$summary$documented_rate)))))
# Input controls: misspecified denominators or conversions cannot pass.
bad <- x$data
bad$patient_id[2L] <- bad$patient_id[1L]
stopifnot(rejects(bc_validate_trial(bad)))
bad <- x$data
bad$documented_response[1L] <- 1L - bad$documented_response[1L]
stopifnot(rejects(bc_analyze_trial(bad)))
stopifnot(rejects(bc_plan_protocol(loss=1)),
          rejects(bc_plan_protocol(p_a=.4,p_b=.4)),
          rejects(bc_plan_protocol(p_a=-.1)),
          rejects(bc_analyze_trial(x$data,conf.level=2)))
# Did not silently convert assessed-only proportions to primary composite estimand.
stopifnot(identical(a$summary$unassessed,
  as.integer(vapply(c("A","B"),function(g)
  sum(x$data$arm==g & is.na(x$data$measured_response)),integer(1)))))
cat("PASS: reproducibility, 1:1 randomization, composite endpoint, B-A arithmetic, missingness and invalid inputs.\n")
