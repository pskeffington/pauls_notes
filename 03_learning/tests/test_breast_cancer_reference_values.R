# Fixed reference values computed independently using SciPy 1.17.0.
# Run from repository root or any directory: Rscript --vanilla <this file>
# These are numeric replay targets, not breast cancer clinical evidence.
args <- commandArgs(trailingOnly = FALSE)
match <- grep("^--file=", args, value = TRUE)
if (!length(match)) stop("Run with Rscript --vanilla.")
here <- dirname(normalizePath(sub("^--file=", "", match[1L]), mustWork = TRUE))
source(file.path(here, "..", "examples", "breast_cancer_test_atlas.R"))
r <- breast_cancer_test_atlas()
near <- function(observed, expected, tol=1e-6) {
  stopifnot(is.numeric(observed),length(observed)==1L,is.finite(observed),
            isTRUE(all.equal(unname(observed), expected,tolerance=tol)))
}
near(unname(r$welch$estimate[1L] - r$welch$estimate[2L]), -3.5)
near(unname(r$welch$statistic), -2.04939015319192)
near(unname(r$welch$parameter), 7.352941176470588)
near(r$welch$p.value, .0776714813536115)
near(r$welch$conf.int[1L], -7.499399820271666)
near(r$welch$conf.int[2L], .4993998202716661)
near(unname(r$paired$estimate), -1.625)
near(unname(r$paired$statistic), -5.016992402421739)
near(r$paired$p.value, .0015356346304149261)
near(r$paired$conf.int[1L], -2.3908999856135846)
near(r$paired$conf.int[2L], -.8591000143864151)
near(r$binomial$p.value, .04106885425072182)
near(r$poisson_tail, .28337574127298903)
near(unname(r$goodness_of_fit$statistic), 2.571428571428571)
near(r$goodness_of_fit$p.value, .2764530466295643)
stopifnot(identical(unname(r$goodness_of_fit$parameter), 2))
cat("PASS: 16 independent breast-cancer numerical reference assertions.\n")
