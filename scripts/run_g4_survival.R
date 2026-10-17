#!/usr/bin/env Rscript
# G4: synthetic educational survival ONLY. No patient data.
# Usage: Rscript scripts/run_g4_survival.R /absolute/output/directory FROZEN_MERGE_SHA
suppressPackageStartupMessages(library(survival))
args <- commandArgs(trailingOnly=TRUE)
if (length(args)!=2L || !grepl("^([0-9a-f]{40})$", args[2])) stop("Usage: Rscript scripts/run_g4_survival.R /absolute/new/output 40-char-merged-freeze-SHA")
out <- args[1]; freeze <- args[2]
if (!grepl("^/", out)) stop("Output must be an absolute path outside repository")
if (!nzchar(Sys.which("git"))) stop("Git required for frozen-protocol verification")
repo <- normalizePath(getwd(), mustWork=TRUE)
parent <- normalizePath(dirname(out), mustWork=TRUE)
if (startsWith(paste0(parent, "/"), paste0(repo, "/")) || parent==repo) stop("Outputs must stay outside Git checkout")
if (file.exists(out)) stop("Exclusive output directory already exists")
if (!dir.create(out, recursive=FALSE)) stop("Cannot create output directory")
writeLines("SYNTHETIC RESEARCH AND EDUCATIONAL USE ONLY - NOT FOR CLINICAL USE", file.path(out,"DISCLAIMER.txt"))
failure <- function(reason) {
  writeLines(paste("FAILED:", reason), file.path(out,"FAILURE.txt"))
  stop(reason, call.=FALSE)
}
hash_file <- function(path) {
  if (!file.exists(path)) failure(paste("Missing protocol/source",path))
  x <- suppressWarnings(system2("sha256sum", path, stdout=TRUE, stderr=TRUE))
  if (length(x)!=1L || !grepl("^[0-9a-f]{64} ",x[1])) failure("sha256sum unavailable")
  substr(x[1], 1, 64)
}
protocol <- "04_machine_learning/survival-protocol.md"
contract <- "04_machine_learning/evidence/survival-contract-v1.json"
src <- "scripts/run_g4_survival.R"
verify_frozen <- function(path) {
  frozen <- suppressWarnings(system2("git",c("show",paste0(freeze,":",path)),stdout=TRUE,stderr=TRUE))
  status <- attr(frozen,"status")
  if (!is.null(status) && status!=0) failure(paste("Frozen file inaccessible:",path))
  tmp <- tempfile(); on.exit(unlink(tmp)); writeLines(frozen,tmp,useBytes=TRUE)
  # Git show via stdout may normalize line endings; compare actual byte streams by git blob ID.
  old <- suppressWarnings(system2("git",c("rev-parse",paste0(freeze,":",path)),stdout=TRUE,stderr=TRUE))
  current <- suppressWarnings(system2("git",c("hash-object",path),stdout=TRUE,stderr=TRUE))
  if(length(old)!=1L||length(current)!=1L||!identical(old,current)) failure(paste("Frozen contract mismatch:",path))
}
verify_frozen(protocol); verify_frozen(contract)
provenance <- list(freeze_commit=freeze, protocol_sha256=hash_file(protocol),
  contract_sha256=hash_file(contract), runner_sha256=hash_file(src),
  R_version=R.version.string, survival_version=as.character(packageVersion("survival")),
  rng_kind=c("Mersenne-Twister","Inversion","Rejection"),
  seeds=c(generator=26102401, reserve=26102402, folds=26102403))
# Write provenance before generating outcomes.
dput(provenance, file=file.path(out,"provenance.R"))
RNGkind("Mersenne-Twister","Inversion","Rejection")
set.seed(26102401)
id <- sprintf("S%03d",seq_len(240))
age <- runif(240,30,75)
marker <- rnorm(240,0,1)
rate <- 0.022*exp(0.025*(age-50)+0.50*marker)
event_time <- -log(runif(240))/rate
censor_time <- runif(240,12,60)
dat <- data.frame(person_id=id,age_years=age,marker=marker,
  time_months=pmin(event_time,censor_time),event=as.integer(event_time<=censor_time))
if (!identical(names(dat),c("person_id","age_years","marker","time_months","event")) ||
    anyDuplicated(dat$person_id) || anyNA(dat) || any(!is.finite(as.matrix(dat[-1]))) ||
    any(dat$time_months<=0|dat$time_months>60) ||
    any(!dat$event %in% 0:1)) failure("Synthetic schema invalid")
set.seed(26102402)
shuffled <- sample.int(240)
reserved <- sort(id[shuffled[seq_len(60)]])
development <- sort(setdiff(id,reserved))
set.seed(26102403)
fold_order <- sample.int(180)
folds <- lapply(seq_len(3),function(j) development[fold_order[((j-1)*60+1):(j*60)]])
if (length(unique(unlist(folds)))!=180L || length(intersect(unlist(folds),reserved))!=0L) failure("Partition overlap")
alloc <- data.frame(person_id=id,allocation=ifelse(id %in% reserved,"reserve","development"),
  fold=ifelse(id %in% reserved,NA_integer_,vapply(id,function(k) {
    z <- which(vapply(folds,function(f) k %in% f,logical(1)))
    if(length(z)==0L) NA_integer_ else z
  },integer(1))))
write.csv(alloc,file.path(out,"allocation.csv"),row.names=FALSE,na="")
write.csv(dat,file.path(out,"synthetic_cohort.csv"),row.names=FALSE)
# Reserved observations are not exported: audit only development records and ID allocation.
# The frozen reserve is protected from evaluation and prediction, including generated output.
write.csv(dat[dat$person_id %in% development,,drop=FALSE],file.path(out,"development_cohort.csv"),row.names=FALSE)
unlink(file.path(out,"synthetic_cohort.csv"))
# KM right-continuous at tau, left-continuous before an observed event.
km_at <- function(fit,t,left=FALSE) {
  idx <- which(if(left) fit$time<t else fit$time<=t)
  if (length(idx)==0L) 1 else fit$surv[max(idx)]
}
ipcw_loss <- function(t,d,p,gfit,tau=24) {
  if (length(t)!=length(d)||length(d)!=length(p)) stop("IPCW length mismatch")
  if (any(!is.finite(t))||any(!d %in% 0:1)) stop("Invalid held-out outcomes")
  if (any(!is.finite(p)|p<0|p>1)) stop("Invalid survival probability")
  g24 <- km_at(gfit,tau)
  if (!is.finite(g24)||g24<0.20) stop("Censor support < 0.20 at 24")
  v <- numeric(length(t))
  for(i in seq_along(t)) {
    if (t[i]<=tau && d[i]==1L) {
      g <- km_at(gfit,t[i],left=TRUE)
      if (!is.finite(g)||g<=0) stop("Zero/nonfinite left-limit censor support")
      v[i] <- p[i]^2/g
    } else if(t[i]>tau) v[i] <- (1-p[i])^2/g24
    # censored at/before horizon contributes zero, but remains in denominator
  }
  v
}
# R survival::survfit.coxph produces one column per newdata row.
cox_at <- function(fit,newdata,tau=24) {
  sf <- survfit(fit,newdata=newdata)
  ss <- sf$surv
  if (is.null(dim(ss))) {
    if(nrow(newdata)!=1L) stop("Ambiguous Cox prediction shape")
    ss <- matrix(ss,ncol=1)
  }
  idx <- which(sf$time<=tau)
  if(length(idx)==0L) return(rep(1,nrow(newdata)))
  value <- as.numeric(ss[max(idx),,drop=TRUE])
  if(length(value)!=nrow(newdata)) stop("Cox prediction cardinality mismatch")
  value
}
pred <- list(); diagnostics <- list()
tryCatch({
  for(j in seq_len(3)) {
    te <- dat[match(folds[[j]],dat$person_id),,drop=FALSE]
    tr <- dat[dat$person_id %in% setdiff(development,folds[[j]]),,drop=FALSE]
    if(nrow(tr)!=120L||nrow(te)!=60L||any(tr$person_id%in%te$person_id)||
        any(tr$person_id%in%reserved)||any(te$person_id%in%reserved)) stop("Fit leakage")
    if(sum(tr$event)<15L||sum(te$event)<5L||sum(te$event==1L&te$time_months<=24)<3L) stop("Insufficient fold events")
    fit <- coxph(Surv(time_months,event)~age_years+marker,data=tr,ties="efron",
                 x=TRUE, model=TRUE)
    if(any(!is.finite(coef(fit)))) stop("Cox coefficients nonfinite")
    km <- survfit(Surv(time_months,event)~1,data=tr)
    censor <- survfit(Surv(time_months,1-event)~1,data=tr)
    if(max(tr$time_months)<24||max(km$time)<24||max(censor$time)<24) stop("Horizon beyond training support")
    cp <- cox_at(fit,te)
    kp <- rep(km_at(km,24),nrow(te))
    lc <- ipcw_loss(te$time_months,te$event,cp,censor)
    lk <- ipcw_loss(te$time_months,te$event,kp,censor)
    ph <- cox.zph(fit)
    pred[[j]] <- data.frame(person_id=te$person_id,fold=j,time_months=te$time_months,
      event=te$event,cox_survival_24=cp,km_survival_24=kp,
      cox_loss=lc,km_loss=lk,cox_log_hazard=as.numeric(predict(fit,newdata=te,type="lp")))
    diagnostics[[j]] <- list(fold=j,train_ids=tr$person_id,test_ids=te$person_id,
      train_events=sum(tr$event),test_events=sum(te$event),
      test_events_by_24=sum(te$event==1L&te$time_months<=24),
      censor_G24=km_at(censor,24),coefficients=coef(fit),cox_zph=ph$table)
  }
  all <- do.call(rbind,pred)
  if (nrow(all)!=180L||anyDuplicated(all$person_id)||!setequal(all$person_id,development)) stop("OOF membership invalid")
  write.csv(all,file.path(out,"oof_predictions.csv"),row.names=FALSE)
  dput(diagnostics,file=file.path(out,"fold_diagnostics.R"))
  cut_bins <- cut(all$cox_survival_24,breaks=c(0,.33,.66,1),
                  include.lowest=TRUE,right=FALSE)
  cut_bins[all$cox_survival_24==1] <- levels(cut_bins)[3]
  calibration <- lapply(seq_len(3),function(b) {
    z <- all[!is.na(cut_bins)&as.integer(cut_bins)==b,,drop=FALSE]
    available <- nrow(z)>=15L && sum(z$event)>=5L
    list(bin=b,n=nrow(z),observed_events=sum(z$event),
      mean_predicted=if(nrow(z)) mean(z$cox_survival_24) else NA_real_,
      observed_km_24=if(available) km_at(survfit(Surv(time_months,event)~1,data=z),24) else NA_real_,
      status=if(available) "descriptive" else "unavailable")
  })
  # Concordance across OOF predictions is descriptive; compare pair count.
  con <- concordance(Surv(time_months,event)~cox_log_hazard,data=all,reverse=TRUE)
  metrics <- list(n=180L,cox_IPCW_Brier_24=mean(all$cox_loss),
    km_IPCW_Brier_24=mean(all$km_loss),
    paired_cox_minus_km=mean(all$cox_loss-all$km_loss),
    harrell_c=unname(con$concordance),concordance_counts=con$count,
    calibration=calibration)
  dput(metrics,file=file.path(out,"metrics.R"))
  writeLines("PASS - synthetic numeric execution (independent replay not yet certified)",
             file.path(out,"RUN_STATUS.txt"))
},error=function(e) failure(conditionMessage(e)))
