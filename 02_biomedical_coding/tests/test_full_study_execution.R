# End-to-end acceptance for Paul's Notes synthetic breast cancer methods workbook.
# Run from repo root:
# Rscript --vanilla 02_biomedical_coding/tests/test_full_study_execution.R
# This executes ALL chunks (via knitr::purl), checks invariants, and does not
# read patient data or install packages. The separate CI knit verifies HTML.

required <- c("knitr", "ggplot2", "survival", "nlme")
missing <- required[!vapply(required, requireNamespace, logical(1), quietly=TRUE)]
if (length(missing)) stop("Missing required packages: ",paste(missing,collapse=", "))
path <- "02_biomedical_coding/examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd"
if (!file.exists(path)) stop("Run test from the repository root")
rmd <- readLines(path,warn=FALSE,encoding="UTF-8")
labels <- sub("^```\\{r[[:space:]]+([^,}[:space:]]+).*", "\\1",
              grep("^```\\{r[[:space:]]+",rmd,value=TRUE))
if (length(labels)!=17L || anyDuplicated(labels)) stop("Chunk count or labels changed")

code_file <- tempfile(fileext=".R")
knitr::purl(path, output=code_file, quiet=TRUE, documentation=0L)
if (!file.exists(code_file)) stop("Failed to purl source")
parse(file=code_file, keep.source=FALSE)
e <- new.env(parent=globalenv())
e$params <- list(seed=711L)
plot_file <- tempfile(fileext=".pdf")
grDevices::pdf(plot_file)
tryCatch(
  sys.source(code_file,envir=e,keep.source=FALSE),
  finally=grDevices::dev.off()
)
stopifnot(
  nrow(e$study)==240L,
  !anyDuplicated(e$study$patient_id),
  sum(is.na(e$study$erbb2_score))==4L,
  sum(is.na(e$study$tumor_cm))==2L,
  nrow(e$plot_data)==236L,
  length(e$a)+length(e$b)==236L,
  e$welch$conf.int[1] <= e$welch$estimate[1]-e$welch$estimate[2],
  e$welch$conf.int[2] >= e$welch$estimate[1]-e$welch$estimate[2],
  nrow(e$repeated)==480L,
  !anyDuplicated(e$wide$patient_id),
  length(e$difference)==240L,
  all(c("score.Baseline", "score.Follow-up") %in% names(e$wide)),
  is.numeric(e$difference),
  all(is.finite(e$difference)),
  isTRUE(all.equal(e$difference,
    e$wide[["score.Follow-up"]] - e$wide[["score.Baseline"]],
    tolerance=1e-12)),
  nrow(e$test_set)>0L,
  nrow(e$train)>0L,
  nrow(e$test_set)+nrow(e$train)<=240L,
  e$tp+e$tn+e$fp+e$fn==nrow(e$test_set),
  is.finite(e$pred_metrics$brier),
  e$pred_metrics$brier>=0,e$pred_metrics$brier<=1,
  exists("km", envir=e, inherits=FALSE),
  exists("cox_fit", envir=e, inherits=FALSE),
  exists("mixed", envir=e, inherits=FALSE),
  all(is.finite(stats::coef(e$cox_fit))),
  length(e$boot_diff)==1000L,
  all(is.finite(e$boot_diff)),
  all(e$p_raw>=0 & e$p_raw<=1),
  nrow(e$audit)==1L
)
## Independent numeric reference for unequal-variance mean difference
## and paired mean change; never use display-rounded table values.
b <- e$b; a <- e$a
difference_mean <- mean(b) - mean(a)
se2 <- stats::var(b)/length(b) + stats::var(a)/length(a)
se <- sqrt(se2)
df <- se2^2 / ((stats::var(b)/length(b))^2/(length(b)-1L) +
                (stats::var(a)/length(a))^2/(length(a)-1L))
reference_t <- difference_mean/se
reference_ci <- difference_mean + c(-1, 1)*stats::qt(.975,df=df)*se
stopifnot(
  isTRUE(all.equal(unname(e$welch$statistic),unname(reference_t), tolerance=1e-10)),
  isTRUE(all.equal(unname(e$welch$parameter),unname(df), tolerance=1e-10)),
  isTRUE(all.equal(unname(e$welch$conf.int),unname(reference_ci),
                   tolerance=1e-10))
)

n_pairs <- length(e$difference)
paired_mean <- mean(e$difference)
paired_se <- stats::sd(e$difference)/sqrt(n_pairs)
paired_ci <- paired_mean +
  c(-1, 1)*stats::qt(.975, df=n_pairs-1L)*paired_se
stopifnot(
  isTRUE(all.equal(unname(e$paired_t$estimate),unname(paired_mean),
                   tolerance=1e-10)),
  isTRUE(all.equal(unname(e$paired_t$conf.int),unname(paired_ci),
                   tolerance=1e-10))
)

auc <- e$auc_rank(e$probs,e$test_set$response)
stopifnot(is.finite(auc),auc>=0,auc<=1)
cat("PASS: full synthetic workbook code executed, 17 chunks and analytical contracts.\n")
