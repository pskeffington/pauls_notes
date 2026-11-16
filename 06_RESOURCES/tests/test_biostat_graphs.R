# Original biomedical graph contract tests; synthetic data only.
# Run at repository root with ggplot2 installed:
# Rscript --vanilla 06_RESOURCES/tests/test_biostat_graphs.R
source("06_RESOURCES/R/biostat_graphs.R")
if (!requireNamespace("ggplot2", quietly=TRUE))
  stop("ggplot2 required for graph acceptance.")

near <- function(x,y) isTRUE(all.equal(as.numeric(x),as.numeric(y),
                                        tolerance=1e-12))
fails <- function(expr) inherits(try(expr,silent=TRUE),"try-error")
d <- data.frame(
  group=factor(c(rep("A",5),rep("B",4)),
               levels=c("A","B")),
  measure=c(1,2,5,9,NA_real_,3,4,7,11)
)
st <- biostat_graph_box_stats(d,"measure","group")
stopifnot(nrow(st)==2L,st$n_total[1]==5L,st$n_observed[1]==4L,
          st$n_missing[1]==1L,st$n_missing[2]==0L)
stopifnot(near(st$q1[1],1.5),near(st$median[1],3.5),
          near(st$q3[1],7),near(st$mean[1],4.25),
          near(st$whisker_low[1],1),near(st$whisker_high[1],9))
stopifnot(!near(st$q1[1],unname(stats::quantile(c(1,2,5,9),.25,type=7))))
## Mild and extreme outliers are distinct from ordinary points.
outlier_data <- data.frame(group=rep("C",22L),
                          measure=c(1:20,50,120))
outlier_stat <- biostat_graph_box_stats(outlier_data,"measure","group")
stopifnot(outlier_stat$n_outlying==1L,outlier_stat$n_extreme==1L)
p_outliers <- biostat_graph_box(outlier_data,"measure","group",unit="score")
stopifnot(inherits(p_outliers,"ggplot"),
          length(ggplot2::ggplot_build(p_outliers)$data)>=9L)
p_box <- biostat_graph_box(d,"measure","group",unit="synthetic units")
stopifnot(inherits(p_box,"ggplot"),nrow(attr(p_box,"figure_statistics"))==2L)
stopifnot(length(ggplot2::ggplot_build(p_box)$data)>=7L)
p_bar <- biostat_graph_bar(d,"group")
tab <- attr(p_bar,"figure_statistics")
stopifnot(inherits(p_bar,"ggplot"),sum(tab$n)==nrow(d),
          setequal(as.character(tab$category),c("A","B")))
stopifnot(nrow(ggplot2::ggplot_build(p_bar)$data[[1L]])==2L)
cat_stem <- biostat_graph_stem(c(1,2,5,9,NA_real_),"arbitrary units")
stopifnot(is.character(cat_stem),length(cat_stem)>1L,
          grepl("Observed n=4; missing=1",cat_stem[1L],fixed=TRUE))
set.seed(711)
est <- stats::rnorm(100,mean=2,sd=.3)
p_boot <- biostat_graph_bootstrap(est,2,unit="difference")
boot <- attr(p_boot,"figure_statistics")
stopifnot(inherits(p_boot,"ggplot"),boot$resamples==100L,
          boot$quantile_type==7L,
          near(boot$interval,stats::quantile(est,c(.025,.975),type=7)))
## ROC must use sensitivity on y and 1-specificity on x; rank AUC
## independently agrees with the trapezoidal empirical curve.
roc_data <- data.frame(score=c(.9,.5,.5,.2),status=c(1L,0L,1L,0L))
p_roc <- biostat_graph_roc(roc_data,"score","status",
                           positive=1L,evaluation_partition="synthetic")
roc_summary <- attr(p_roc,"figure_statistics")
stopifnot(inherits(p_roc,"ggplot"),
          near(roc_summary$auc,.875),
          near(roc_summary$roc$false_positive_rate[1],0),
          near(tail(roc_summary$roc$false_positive_rate,1),1),
          near(roc_summary$roc$sensitivity[1],0),
          near(tail(roc_summary$roc$sensitivity,1),1))
stopifnot(fails(biostat_graph_roc(roc_data,"score","status",
                                  positive=2L,evaluation_partition="synthetic")),
          fails(biostat_graph_roc(data.frame(score=1:3,status=c(1,1,1)),
                                  "score","status",
                                  evaluation_partition="synthetic")))
stopifnot(fails(biostat_graph_box(d,"measure","group",unit="")),
          fails(biostat_graph_box_stats(data.frame(group=c("A","B"),
                                                    measure=c(NA_real_,1)),
                                        "measure","group")),
          fails(biostat_graph_bar(data.frame(x=1:3),"x")),
          fails(biostat_graph_stem(c(NA_real_,1),"unit")),
          fails(biostat_graph_bootstrap(1:10,5,"units")),
          fails(biostat_graph_bootstrap(1:30,5,"units",interval=c(.9,.1))))
cat("PASS: biomedical graph distribution, mean, quartile, missingness and export-independent contracts.\n")
