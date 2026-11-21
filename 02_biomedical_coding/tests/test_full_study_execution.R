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
  length(e$train_ids)==168L,
  length(e$test_ids)==72L,
  !anyDuplicated(e$train_ids),
  !anyDuplicated(e$test_ids),
  !any(e$train_ids %in% e$test_ids),
  !any(e$train$patient_id %in% e$test_set$patient_id),
  all(e$train$patient_id %in% e$train_ids),
  all(e$test_set$patient_id %in% e$test_ids),
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
  isTRUE(all.equal(as.numeric(e$welch$conf.int),as.numeric(reference_ci),
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
  isTRUE(all.equal(as.numeric(e$paired_t$conf.int),as.numeric(paired_ci),
                   tolerance=1e-10))
)

## Analysis-specific denominators must reflect the known synthetic NA map.
stopifnot(
  stats::nobs(e$linear_fit) == 234L,
  stats::nobs(e$logit_fit) == 238L,
  stats::nobs(e$pois_fit) == 240L,
  e$audit$baseline_N == 240L,
  e$audit$linear_model_n == 234L,
  e$audit$logistic_model_n == 238L,
  e$audit$poisson_model_n == 240L
)

## Wald intervals and exponentiated coefficients: odds != risks.
logit_coefficients <- stats::coef(e$logit_fit)
logit_se <- sqrt(diag(stats::vcov(e$logit_fit)))
logit_z <- stats::qnorm(.975)
logit_or_reference <- exp(logit_coefficients)
logit_lower <- exp(logit_coefficients - logit_z * logit_se)
logit_upper <- exp(logit_coefficients + logit_z * logit_se)
stopifnot(
  all(is.finite(logit_or_reference)), all(logit_lower > 0),
  isTRUE(all.equal(as.numeric(e$logit_or$odds_ratio),
                   as.numeric(logit_or_reference), tolerance=1e-10)),
  isTRUE(all.equal(as.numeric(e$logit_or$lower),
                   as.numeric(logit_lower), tolerance=1e-10)),
  isTRUE(all.equal(as.numeric(e$logit_or$upper),
                   as.numeric(logit_upper), tolerance=1e-10))
)

## Poisson model: the log exposure must remain an offset, not a
## freely estimated coefficient. The resulting exponentiated slopes
## are incidence rate ratios, not event probabilities.
## R records offsets in the terms object's offset attribute and omits
## them from term.labels, which lists the estimated model terms.
stopifnot(
  length(attr(stats::terms(e$pois_fit),"offset")) == 1L,
  !any(grepl("exposure_years", names(stats::coef(e$pois_fit)), fixed=TRUE)),
  all(e$study$exposure_years > 0)
)
pois_coefficients <- stats::coef(e$pois_fit)
pois_se <- sqrt(diag(stats::vcov(e$pois_fit)))
pois_rr_reference <- exp(pois_coefficients)
pois_lower <- exp(pois_coefficients - logit_z * pois_se)
pois_upper <- exp(pois_coefficients + logit_z * pois_se)
stopifnot(
  isTRUE(all.equal(as.numeric(e$pois_fit$offset),
                   log(e$study$exposure_years), tolerance=1e-10)),
  isTRUE(all.equal(as.numeric(e$pois_fit$fitted.values),
                   as.numeric(stats::predict(e$pois_fit,type="response")),
                   tolerance=1e-10)),
  isTRUE(all.equal(as.numeric(exp(e$pois_ci[,1])),
                   as.numeric(pois_lower), tolerance=1e-10)),
  isTRUE(all.equal(as.numeric(exp(e$pois_ci[,2])),
                   as.numeric(pois_upper), tolerance=1e-10)),
  isTRUE(all.equal(as.numeric(exp(stats::coef(e$pois_fit))),
                   as.numeric(pois_rr_reference), tolerance=1e-10))
)

## At fixed covariates, doubling exposure must double the expected count.
## This guards the offset's fixed coefficient of one without refitting.
double_exposure <- e$study
double_exposure$exposure_years <- 2 * double_exposure$exposure_years
stopifnot(
  isTRUE(all.equal(
    as.numeric(stats::predict(e$pois_fit,newdata=double_exposure,type="response")),
    2 * as.numeric(stats::fitted(e$pois_fit)), tolerance=1e-10))
)

## Synthetic visits are deliberately within-subject correlated.
## Test the design feature rather than claiming two independent visits.
stopifnot(
  stats::cor(e$wide[["score.Baseline"]],
             e$wide[["score.Follow-up"]]) > 0.5
)

auc <- e$auc_rank(e$probs,e$test_set$response)
stopifnot(is.finite(auc),auc>=0,auc<=1)
stopifnot(inherits(e$p_roc,"ggplot"),
          isTRUE(all.equal(
            as.numeric(attr(e$p_roc,"figure_statistics")$auc),
            as.numeric(auc),tolerance=1e-12)),
          identical(attr(e$p_roc,"figure_statistics")$partition,"held-out"))
box_summary <- attr(e$p_box,"figure_statistics")
bar_summary <- attr(e$p_bar,"figure_statistics")
stopifnot(inherits(e$p_box,"ggplot"),inherits(e$p_bar,"ggplot"),
          nrow(box_summary)==2L,
          sum(box_summary$n_observed)==236L,
          sum(box_summary$n_missing)==4L,
          sum(bar_summary$n)==240L)
for (i in seq_len(nrow(box_summary))) {
  observed <- e$study$erbb2_score[
    as.character(e$study$subtype)==box_summary$group[i] &
      !is.na(e$study$erbb2_score)]
  q <- as.numeric(stats::quantile(observed,c(.25,.50,.75),type=2))
  stopifnot(
    isTRUE(all.equal(as.numeric(unlist(box_summary[i,c("q1","median","q3")],use.names=FALSE)),
                     q,tolerance=1e-12)),
    isTRUE(all.equal(as.numeric(box_summary$mean[i]),
                     mean(observed),tolerance=1e-12))
  )
}
## Independent pairwise concordance reference, including score ties.
positive_scores <- e$probs[e$test_set$response==1L]
negative_scores <- e$probs[e$test_set$response==0L]
pair_concordance <- outer(positive_scores,negative_scores,">")
pair_ties <- outer(positive_scores,negative_scores,"==")
auc_reference <- mean(pair_concordance + 0.5*pair_ties)
stopifnot(
  length(positive_scores)>0L,length(negative_scores)>0L,
  isTRUE(all.equal(as.numeric(auc),as.numeric(auc_reference),
                   tolerance=1e-12)),
  isTRUE(all.equal(as.numeric(e$pred_metrics$brier),
                   mean((e$probs-e$test_set$response)^2),tolerance=1e-12))
)
cat("PASS: full synthetic workbook code executed, 17 chunks and analytical contracts.\n")
