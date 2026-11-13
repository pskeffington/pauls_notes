# All values are synthetic; source defines functions only.
breast_cancer_foundations_lab <- function(simulations=5000L, seed=7122026L) {
  stopifnot(length(simulations)==1L, is.numeric(simulations),
            is.finite(simulations), simulations>=100L,
            simulations==floor(simulations),
            length(seed)==1L, is.numeric(seed),
            is.finite(seed), seed==floor(seed))
  # Preserve global random state; no downloads, file writes or installations.
  had_seed <- exists(".Random.seed", envir=.GlobalEnv, inherits=FALSE)
  if (had_seed) saved <- get(".Random.seed", envir=.GlobalEnv)
  on.exit(if (had_seed) assign(".Random.seed", saved, envir=.GlobalEnv)
          else if (exists(".Random.seed", envir=.GlobalEnv, inherits=FALSE))
            rm(".Random.seed", envir=.GlobalEnv), add=TRUE)
  set.seed(as.integer(seed))
  sample_means <- function(n) replicate(as.integer(simulations),
                                         mean(stats::rexp(n, rate=.1)))
  clt5 <- sample_means(5L); clt50 <- sample_means(50L)
  x <- c(8,10,10,12,12,14,14,16)
  A <- c(8,9,10,11,12,13)
  B <- c(9,11,13,15,17,19)
  before <- c(8,10,12,14,16,18,20,22)
  after <- c(7,9,11,11,15,17,18,19)
  score <- c(8,10,12,10,12,14,12,14,16)
  arm <- factor(rep(c("A","B","C"),each=3L))
  anova <- stats::aov(score~arm)
  list(
    descriptive=c(n=length(x),mean=mean(x),variance=var(x),
                  sd=sd(x),se=sd(x)/sqrt(length(x))),
    clt=list(means_n5=clt5,means_n50=clt50,
             theoretical_se_n5=10/sqrt(5),
             theoretical_se_n50=10/sqrt(50)),
    welch=stats::t.test(A,B,var.equal=FALSE),
    pooled_student=stats::t.test(A,B,var.equal=TRUE),
    paired=stats::t.test(after-before,mu=0),
    one_sample=stats::t.test(x,mu=10),
    anova=anova,
    welch_anova=stats::oneway.test(score~arm,var.equal=FALSE),
    binomial=stats::binom.test(36L,80L,p=.35,alternative="greater"),
    binomial_tail=stats::pbinom(35L,80L,.35,lower.tail=FALSE),
    poisson_tail=stats::ppois(9L,8,lower.tail=FALSE),
    anova_components=list(score=score,arm=arm,
                          between=24,within=24,F_value=3)
  )
}

# Optional, in-document base R visual explanations. No external files.
plot_breast_cancer_clt <- function(result=breast_cancer_foundations_lab()) {
  old <- graphics::par(mfrow=c(1,2))
  on.exit(graphics::par(old))
  graphics::hist(result$clt$means_n5,main="Synthetic mean, n=5",
                 xlab="Mean biomarker score (arbitrary units)",
                 col="#0072B2",border="white")
  graphics::abline(v=10,col="#D55E00",lty=2,lwd=2)
  graphics::hist(result$clt$means_n50,main="Synthetic mean, n=50",
                 xlab="Mean biomarker score (arbitrary units)",
                 col="#0072B2",border="white")
  graphics::abline(v=10,col="#D55E00",lty=2,lwd=2)
  invisible(result)
}

# Run from repo root:
# source("03_learning/examples/breast_cancer_foundations_lab.R")
# result <- breast_cancer_foundations_lab()
# result$welch
# summary(result$anova)
# result$binomial_tail
# result$poisson_tail
# plot_breast_cancer_clt(result)
