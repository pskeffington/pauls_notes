# Run: Rscript --vanilla 03_learning/tests/test_breast_cancer_test_atlas.R
args <- commandArgs(trailingOnly=FALSE)
which_file <- grep("^--file=",args,value=TRUE)
if (!length(which_file)) stop("Run using Rscript.")
here <- dirname(normalizePath(sub("^--file=","",which_file[1]),mustWork=TRUE))
source(file.path(here,"..","examples","breast_cancer_test_atlas.R"))
x <- breast_cancer_test_atlas()
stopifnot(length(x$data$patient_id)==12L,
          !anyDuplicated(x$data$patient_id),
          identical(sum(x$data$binary_table),40),
          isTRUE(all.equal(x$binomial$p.value,
                           stats::pbinom(35,80,.35,lower.tail=FALSE),
                           tolerance=1e-12)),
          isTRUE(all.equal(x$poisson_tail,
                           stats::ppois(9,8,lower.tail=FALSE))),
          isTRUE(all.equal(unname(x$welch$estimate[1]-x$welch$estimate[2]),
                           mean(x$data$marker[1:6])-mean(x$data$marker[7:12]))),
          isTRUE(all.equal(unname(x$paired$estimate),mean(x$data$change))),
          inherits(x$logistic,"glm"),inherits(x$linear,"lm"),
          inherits(x$poisson_model,"glm"))
if (requireNamespace("survival",quietly=TRUE))
 stopifnot(inherits(x$km,"survfit"),inherits(x$log_rank,"survdiff"),
           inherits(x$cox,"coxph"))
stopifnot(is.character(capture.output(breast_cancer_test_report(x))))
cat("PASS: synthetic breast-cancer test atlas identities and result types.\n")
