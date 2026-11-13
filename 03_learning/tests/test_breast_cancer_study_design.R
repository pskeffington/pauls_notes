# Run with Rscript --vanilla 03_learning/tests/test_breast_cancer_study_design.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (!length(file_arg)) stop("Run using Rscript.")
here <- dirname(normalizePath(sub("^--file=", "", file_arg[1L]),
                              mustWork = TRUE))
source(file.path(here, "..", "examples", "breast_cancer_study_design.R"))
near <- function(value, expected, tolerance=1e-10)
  stopifnot(is.numeric(value), length(value)==1L, is.finite(value),
            isTRUE(all.equal(as.numeric(value), expected,
                             tolerance=tolerance)))
rejects <- function(expr) inherits(try(expr, silent=TRUE), "try-error")
normal <- cancer_design_continuous()
stopifnot(identical(unname(normal$normal_approx), c(91,91)),
          identical(unname(normal$enrolment_normal_approx), c(102,102)),
          normal$exact_t_equal_arm >= 91,
          all(normal$enrolment_normal_approx >= normal$normal_approx))
asym <- cancer_design_continuous(allocation_ratio=2, loss=0)
stopifnot(asym$normal_approx["treatment"] ==
            2*asym$normal_approx["control"],
          sum(asym$normal_approx) >= sum(normal$normal_approx))
binary <- cancer_design_binary()
stopifnot(binary$n_per_arm_analyzable > 0L,
          binary$n_per_arm_enrolment >= binary$n_per_arm_analyzable)
near(binary$risk_difference, .15)
events <- cancer_design_events()
stopifnot(events$required_events_approx == 380,
          events$required_events_approx == ceiling(events$unrounded_events))
near(events$unrounded_events,
     (stats::qnorm(.975)+stats::qnorm(.8))^2 /
       (.25*log(.75)^2))
near(cancer_cluster_design_effect(4,.15), 1.45)
near(cancer_cluster_design_effect(1,.15), 1)
paired <- cancer_paired_plan()
stopifnot(is.numeric(paired$n_complete_pairs), paired$n_complete_pairs >= 2L)
stopifnot(rejects(cancer_design_binary(p_control=.3,p_treatment=.3)),
          rejects(cancer_design_binary(p_control=NA_real_)),
          rejects(cancer_design_continuous(sd=0)),
          rejects(cancer_design_continuous(allocation_ratio=0)),
          rejects(cancer_design_continuous(loss=1)),
          rejects(cancer_design_events(hr=1)),
          rejects(cancer_design_events(hr=-.8)),
          rejects(cancer_cluster_design_effect(3.5,.1)),
          rejects(cancer_cluster_design_effect(4,1)),
          rejects(cancer_paired_plan(delta=0)))
cat("PASS: synthetic cancer study design contracts and normal/event numerical references.\n")
