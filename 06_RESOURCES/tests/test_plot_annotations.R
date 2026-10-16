# Annotation smoke tests; synthetic data only.
args <- commandArgs(FALSE); f <- grep("^--file=",args,value=TRUE)
if (!length(f)) stop("Run with Rscript --vanilla")
here <- dirname(normalizePath(sub("^--file=","",f[1])))
for (nm in c("stats_plots.R","one_call_plots.R",
             "biostat_panels.R","plot_annotations.R"))
  source(file.path(here,"..","R",nm))
if (!requireNamespace("ggplot2",quietly=TRUE)) {
  cat("SKIP: ggplot2 unavailable\n")
} else {
  set.seed(711)
  d <- data.frame(x=seq_len(40),y=rnorm(40)+seq_len(40)/10,
                  group=rep(c("A","B"),each=20),
                  facet=rep(rep(c("first","second"),each=10),2))
  p <- plot_test(d,"x","y")
  stopifnot(audit_plot_annotations(p)$pass, inherits(attr(p,"statistical_test"),"htest"),
            is.numeric(get_plot_annotation(p)$p))
  w <- plot_wilcox(d,"y","group")
  stopifnot(audit_plot_annotations(w)$pass, inherits(attr(w,"statistical_test"),"htest"))
  q <- plot_multigroup(d,"y","group")
  stopifnot(audit_plot_annotations(q)$pass,
            inherits(attr(q,"posthoc"),"pairwise.htest"))
  pw <- plot_panel_wilcox(d,"y","group","facet")
  stopifnot(audit_plot_annotations(pw)$pass, nrow(attr(pw,"statistical_tests"))==2L)
  fw <- plot_forest(data.frame(term=c("G1","G2"),est=c(.1,.2),
    lo=c(0,.1),hi=c(.3,.4)), "term","est","lo","hi")
  stopifnot(audit_plot_annotations(fw)$pass)
  gene <- transform(d, Gene="ESR1", Expression=y, Subtype=group)
  gw <- plot_gene_wilcox(gene,"ESR1","Subtype")
  stopifnot(audit_plot_annotations(gw)$pass)
  bad <- ggplot2::ggplot(data.frame(x=1,y=1),ggplot2::aes(x=x,y=y))+
         ggplot2::geom_point()
  stopifnot(!audit_plot_annotations(bad)$pass)
  annotated <- annotate_plot(bad,title="Demo",x="X units",y="Y units",
                              source="synthetic fixture",note="No inference")
  stopifnot(audit_plot_annotations(annotated, require_source=TRUE)$pass)
  outfile <- tempfile(fileext=".pdf")
  saved <- save_annotated_plot(annotated,outfile,require_source=TRUE)
  stopifnot(file.exists(saved$figure),file.exists(saved$manifest))
  unlink(c(saved$figure,saved$manifest))
  cat("PASS: annotation, metadata retention, audit and export smoke tests\n")
}
