# Synthetic breast-cancer statistical teaching laboratory.
# Sourcing this script defines functions only. No downloaded/private data.
# Model outputs are teaching artifacts, not clinical estimates.
breast_cancer_test_atlas <- function() {
  marker <- c(8,9,10,11,12,13, 9,11,13,15,17,19)
  group <- factor(rep(c("A","B"), each=6), levels=c("A","B"))
  patient_id <- sprintf("S%02d", seq_along(marker))
  age <- c(44,49,54,59,64,69,43,48,53,58,63,68)
  stopifnot(!anyDuplicated(patient_id), length(marker)==length(group))
  pre <- c(8,10,12,14,16,18,20,22)
  post <- c(7,9,11,11,15,17,18,19)
  change <- post-pre
  profile <- factor(rep(c("luminal","her2_profile","basal_profile"),each=6))
  profile_marker <- c(9,10,11,12,13,14, 12,14,16,18,20,22, 8,9,10,11,12,13)
  toxicity <- ordered(c(1,2,1,3,2,1, 2,3,3,2,4,3, 1,1,2,2,2,3),
                      levels=1:4)
  treatment <- factor(rep(c("A","B","C"), each=6))
  response <- c(1,1,1,0,1,0, 1,0,1,0,0,1,
                0,1,0,1,0,0)
  binary_table <- matrix(c(14,6,9,11),nrow=2,byrow=TRUE,
                         dimnames=list(arm=c("A","B"),response=c("yes","no")))
  transition <- matrix(c(12,3,8,17),nrow=2,byrow=TRUE,
                       dimnames=list(before=c("negative","positive"),
                                     after=c("negative","positive")))
  profile_response <- matrix(c(12,8, 9,11, 7,13),nrow=3,byrow=TRUE)
  dimnames(profile_response) <- list(profile=c("luminal","her2_profile","basal_profile"),
                                     response=c("yes","no"))
  stratified <- array(c(9,4,5,8, 7,5,6,9), dim=c(2,2,2),
                      dimnames=list(treatment=c("A","B"),
                                    response=c("yes","no"),
                                    stage=c("early","later")))
  count_data <- data.frame(
    id=1:12,
    group=factor(rep(c("A","B"),each=6)),
    visits=c(0,1,1,2,1,3, 1,2,2,4,3,5),
    years=c(.8,1.0,1.2,1.0,.7,1.1, 1.0,.9,1.2,1.1,.8,1.0)
  )
  survival_data <- data.frame(
    id=seq_len(12),
    months=c(4,6,8,10,12,14, 5,7,9,11,13,15),
    recurrence=c(1,0,1,1,0,0, 1,1,0,1,0,0),
    group=factor(rep(c("A","B"),each=6)),
    marker=marker
  )
  stopifnot(all(count_data$years>0), all(count_data$visits>=0),
            all(survival_data$recurrence %in% 0:1),
            all(survival_data$months>0))
  fit_lm <- stats::lm(marker ~ I(age/10) + group)
  fit_logit <- stats::glm(response ~ profile_marker + treatment,
                         family=stats::binomial())
  fit_count <- stats::glm(visits ~ group + offset(log(years)),
                          family=stats::poisson(),data=count_data)
  out <- list(
    one_mean=stats::t.test(marker,mu=10),
    welch=stats::t.test(marker ~ group,var.equal=FALSE),
    paired=stats::t.test(change,mu=0),
    signed_rank=stats::wilcox.test(post,pre,paired=TRUE,exact=FALSE),
    sign=stats::binom.test(sum(change>0),sum(change!=0),p=.5),
    rank_sum=stats::wilcox.test(marker ~ group,exact=FALSE),
    welch_anova=stats::oneway.test(profile_marker ~ profile,var.equal=FALSE),
    ordinary_anova=stats::aov(profile_marker ~ profile),
    kruskal=stats::kruskal.test(as.numeric(toxicity) ~ treatment),
    binomial=stats::binom.test(36L,80L,p=.35,alternative="greater"),
    two_proportions=stats::prop.test(c(14L,9L),c(20L,20L),correct=FALSE),
    paired_binary=stats::mcnemar.test(transition),
    categorical=stats::chisq.test(profile_response),
    fisher=stats::fisher.test(binary_table),
    goodness_of_fit=stats::chisq.test(c(60,45,45),p=c(.4,.35,.25)),
    pearson=stats::cor.test(age,marker,method="pearson"),
    spearman=stats::cor.test(age,marker,method="spearman",exact=FALSE),
    linear=fit_lm,
    logistic=fit_logit,
    mantel_haenszel=stats::mantelhaen.test(stratified),
    poisson_one_rate=stats::poisson.test(10,T=20000,r=40/100000),
    poisson_model=fit_count,
    poisson_tail=stats::ppois(9,lambda=8,lower.tail=FALSE),
    data=list(marker=marker,group=group,patient_id=patient_id,
              change=change,transition=transition,binary_table=binary_table,
              count=count_data,survival=survival_data)
  )
  if (requireNamespace("survival",quietly=TRUE)) {
    surv <- survival::Surv(survival_data$months,survival_data$recurrence)
    out$km <- survival::survfit(surv ~ survival_data$group)
    out$log_rank <- survival::survdiff(surv ~ survival_data$group)
    out$cox <- survival::coxph(surv ~ marker + group,data=survival_data)
  }
  if (requireNamespace("MASS",quietly=TRUE))
    out$negative_binomial <- tryCatch(
      MASS::glm.nb(visits ~ group + offset(log(years)), data=count_data),
      error=function(e) structure(list(message=conditionMessage(e)),
                                  class="optional_model_unavailable"))
  out
}

# Print a compact estimator-focused teaching report. Called explicitly only.
breast_cancer_test_report <- function(results=breast_cancer_test_atlas()) {
  stopifnot(is.list(results),is.list(results$data))
  fmt <- function(x) format(round(unname(x),4),trim=TRUE)
  cat("ALL NUMBERS ARE SYNTHETIC; NO PATIENT DATA.\n")
  cat("Welch: A-B mean difference=",fmt(diff(rev(
    tapply(results$data$marker,results$data$group,mean)))),
    "; 95% CI [",paste(fmt(results$welch$conf.int),collapse=", "),"]\n",sep="")
  cat("Paired: post-pre mean change=",fmt(mean(results$data$change)),
      "; 95% CI [",paste(fmt(results$paired$conf.int),collapse=", "),"]\n",sep="")
  cat("Binomial: observed 36/80, exact one-sided p=",fmt(results$binomial$p.value),"\n",sep="")
  cat("Poisson: expected 8, P(events >=10)=",fmt(results$poisson_tail),"\n",sep="")
  cat("Logistic: coefficients are log-odds; exponentiate for odds ratios.\n")
  cat("Count model: coefficients are log-rate ratios; exponentiate for rate ratios.\n")
  cat("Cox, if installed: coefficients are log-hazard ratios; inspect PH diagnostics.\n")
  invisible(results)
}
# From repo root:
# source("03_learning/examples/breast_cancer_test_atlas.R")
# r <- breast_cancer_test_atlas()
# breast_cancer_test_report(r)
# print(summary(r$linear))
# print(summary(r$logistic))
# print(summary(r$poisson_model))
