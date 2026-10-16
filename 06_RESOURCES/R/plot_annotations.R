# Figure annotation and export helpers; source after plotting modules.
# Statistical results are retained; annotations do not validate inference.

annotate_plot <- function(plot, title = NULL, subtitle = NULL,
                           x = NULL, y = NULL, method = NULL,
                           n = NULL, p = NULL, adjustment = NULL,
                           scale = NULL, design = NULL, source = NULL,
                           note = NULL) {
  require_plotting_packages()
  if (!inherits(plot, "ggplot")) stop("plot must be ggplot")
  if (!is.null(n) && (length(n) != 1L || !is.finite(n) || n < 0))
    stop("n must be a nonnegative scalar")
  if (!is.null(p) && (length(p) != 1L || !is.finite(p) ||
                     p < 0 || p > 1)) stop("p must lie in [0,1]")
  fmt <- function(x) if (is.null(x)) NULL else as.character(x)
  details <- c(if (!is.null(method)) paste("Method:", method),
               if (!is.null(n)) paste("n =", n),
               if (!is.null(p)) paste("p =", format.pval(p, digits = 3,
                                                        eps = .Machine$double.eps)),
               if (!is.null(adjustment)) paste("p adjustment:", adjustment))
  # Preserve existing labels when no override is supplied.
  prior <- plot$labels
  existing_subtitle <- if (!is.null(prior$subtitle)) prior$subtitle else NULL
  annotation_subtitle <- if (!is.null(subtitle)) subtitle else
    if (length(details)) paste(details, collapse = " | ") else existing_subtitle
  # Caption stores information helpful once the figure leaves its R session.
  caption <- paste(c(if (!is.null(scale)) paste("Scale:", scale),
                     if (!is.null(design)) paste("Design:", design),
                     if (!is.null(source)) paste("Source:", source),
                     if (!is.null(note)) note), collapse = " | ")
  plot <- plot + ggplot2::labs(title = if (is.null(title)) prior$title else title,
             subtitle = annotation_subtitle,
             x = if (is.null(x)) prior$x else x,
             y = if (is.null(y)) prior$y else y,
             caption = if (nzchar(caption)) caption else prior$caption)
  attr(plot, "plot_annotation") <- list(title = title, subtitle = annotation_subtitle,
       x = x, y = y, method = method, n = n, p = p,
       adjustment = adjustment, scale = scale,
       design = design, source = source, note = note)
  plot
}

# Inspect the metadata rather than manually copying labels from an image.
get_plot_annotation <- function(plot) {
  if (!inherits(plot, "ggplot")) stop("plot must be ggplot")
  attr(plot, "plot_annotation")
}

# Ensure all required labels are actually present before publication.
audit_plot_annotations <- function(plot, require_source = FALSE) {
  if (!inherits(plot, "ggplot")) stop("plot must be ggplot")
  labels <- plot$labels
  get_label <- function(key) {
    val <- labels[[key]]
    if (is.null(val) || !is.character(val) || !length(val)) "" else val[1]
  }
  required <- c("title", "x", "y", "caption")
  missing <- required[!vapply(required, function(k) nzchar(trimws(get_label(k))),
                               logical(1))]
  a <- get_plot_annotation(plot)
  if (require_source && (is.null(a$source) || !nzchar(a$source)))
    missing <- unique(c(missing, "source"))
  data.frame(field = required, valid = !(required %in% missing),
             stringsAsFactors = FALSE) -> audit
  list(pass = !length(missing), missing = missing, fields = audit)
}

# One-call export enforces annotation checks and writes a companion
# manifest so that published figures retain method and provenance.
save_annotated_plot <- function(plot, file, width = 8, height = 5,
                               dpi = 300, require_source = FALSE) {
  check <- audit_plot_annotations(plot, require_source)
  if (!check$pass)
    stop("Missing figure annotations: ", paste(check$missing, collapse = ", "))
  save_plot(plot, file, width = width, height = height, dpi = dpi)
  a <- get_plot_annotation(plot)
  # Base R dput avoids requiring JSON packages for educational users.
  manifest <- paste0(file, ".annotations.R")
  dput(list(annotation = a, labels = plot$labels,
            width_in = width, height_in = height, dpi = dpi),
       file = manifest)
  invisible(list(figure = file, manifest = manifest))
}

# Auto-decorate the existing one-call statistical plot functions.
# Keep the original htest attributes, and embed methods/p in the figure.
# The wrappers are installed only once by this file, after all base modules.
if (exists("plot_test", mode = "function") &&
    !exists(".original_plot_test", inherits = FALSE)) {
  .original_plot_test <- plot_test
  plot_test <- function(data, x, y,
                            method = c("pearson", "spearman"), fit = TRUE,
                            conf_level = .95) {
    method <- match.arg(method)
    p <- .original_plot_test(data,x,y,method,fit,conf_level)
    result <- attr(p,"statistical_test")
    n <- sum(stats::complete.cases(data[c(x,y)]))
    p <- annotate_plot(p, title = "Association and fitted trend",
                       x=x, y=y, method=paste(method,"correlation"), n=n,
                       p=result$p.value, design="cross-sectional",
                       note=if (fit) "Line: least squares; band: mean-response CI" else
                         "Correlation only; no fitted line")
    attr(p,"statistical_test") <- result
    p
  }
}

if (exists("plot_wilcox", mode = "function") &&
    !exists(".original_plot_wilcox", inherits = FALSE)) {
  .original_plot_wilcox <- plot_wilcox
  plot_wilcox <- function(data, value, group, paired=FALSE, id=NULL,
                              adjust="none", title=NULL) {
    p <- .original_plot_wilcox(data,value,group,paired,id,adjust,title)
    result <- attr(p,"statistical_test")
    # n corresponds to complete observations (unpaired) or matched IDs.
    if (paired) {
      d <- data[stats::complete.cases(data[c(value,group,id)]),,drop=FALSE]
      gg <- sort(unique(as.character(d[[group]])))
      a <- unique(as.character(d[[id]][as.character(d[[group]])==gg[1]]))
      b <- unique(as.character(d[[id]][as.character(d[[group]])==gg[2]]))
      n <- length(intersect(a,b))
    } else {
      n <- sum(stats::complete.cases(data[c(value,group)]))
    }
    p <- annotate_plot(p, title=title %||% "Group comparison",
      x=group,y=value,method=if(paired) "Wilcoxon signed rank" else "Wilcoxon rank sum",
      n=n,p=result$p.value,adjustment=if(adjust!="none") adjust else NULL,
      design=if(paired) "matched pairs" else "independent groups",
      note=if(paired) "n counts complete matched pairs" else
        "n counts complete independent observations")
    attr(p,"statistical_test") <- result
    p
  }
}

# Extend consistent annotations to the remaining teaching plot factories.
if (exists("plot_multigroup",mode="function") &&
    !exists(".original_plot_multigroup",inherits=FALSE)) {
  .original_plot_multigroup <- plot_multigroup
  plot_multigroup <- function(data,value,group,p_adjust="BH",pairwise=TRUE) {
    p <- .original_plot_multigroup(data,value,group,p_adjust,pairwise)
    test <- attr(p,"statistical_test"); posthoc <- attr(p,"posthoc")
    n <- sum(stats::complete.cases(data[c(value,group)]))
    p <- annotate_plot(p,title=paste(value,"by",group),x=group,y=value,
      method="Kruskal-Wallis",n=n,p=test$p.value,
      adjustment=if(pairwise) paste("pairwise Wilcoxon:",p_adjust) else NULL,
      design="independent groups",note="Global p shown; pairwise table in posthoc")
    attr(p,"statistical_test") <- test
    attr(p,"posthoc") <- posthoc
    p
  }
}

if (exists("plot_gene_wilcox",mode="function") &&
    !exists(".original_plot_gene_wilcox",inherits=FALSE)) {
  .original_plot_gene_wilcox <- plot_gene_wilcox
  plot_gene_wilcox <- function(long_data,gene,group,value="Expression",
                                   paired=FALSE,id=NULL,scale="log2 CPM") {
    p <- .original_plot_gene_wilcox(long_data,gene,group,value,paired,id,scale)
    test <- attr(p,"statistical_test")
    # The upstream wrapper may already have added annotation; replace it
    # with an explicitly named assay scale and gene identity.
    prior <- get_plot_annotation(p)
    p <- annotate_plot(p,title=paste("Expression:",gene),x=group,y=scale,
      method=if(paired) "Wilcoxon signed rank" else "Wilcoxon rank sum",
      n=if (!is.null(prior$n)) prior$n else sum(stats::complete.cases(
        long_data[as.character(long_data$Gene)==gene,c(value,group)])),
      p=test$p.value,scale=scale,
      design=if(paired) "matched gene-expression observations" else
        "independent gene-expression observations",
      note="Exploratory; not edgeR differential-expression inference")
    attr(p,"statistical_test") <- test
    p
  }
}

if (exists("plot_panel_wilcox",mode="function") &&
    !exists(".original_panel_wilcox",inherits=FALSE)) {
  .original_panel_wilcox <- plot_panel_wilcox
  plot_panel_wilcox <- function(data,value,group,facet,p_adjust="BH",ncol=3L) {
    p <- .original_panel_wilcox(data,value,group,facet,p_adjust,ncol)
    tab <- attr(p,"statistical_tests")
    p <- annotate_plot(p,title="Facet-wise Wilcoxon comparisons",
      x=group,y=value,method="Independent Wilcoxon within each facet",
      n=sum(tab$n),adjustment=p_adjust,design=paste("faceted by",facet),
      note="Each facet title gives its n and adjusted p-value")
    attr(p,"statistical_tests") <- tab
    p
  }
}

if (exists("plot_forest",mode="function") &&
    !exists(".original_plot_forest",inherits=FALSE)) {
  .original_plot_forest <- plot_forest
  plot_forest <- function(data,label,estimate,lower,upper,
                              reference=0,x_label="Estimated effect") {
    p <- .original_plot_forest(data,label,estimate,lower,upper,
                                   reference,x_label)
    annotate_plot(p,title="Effect estimates and intervals",x=x_label,
      y="Model term",method="Supplied model estimates",
      n=nrow(data),note=paste("Reference line:",reference,
       "| Intervals supplied by caller; inference not recomputed"))
  }
}

if (exists("plot_roc",mode="function") &&
    !exists(".original_plot_roc",inherits=FALSE)) {
  .original_plot_roc <- plot_roc
  plot_roc <- function(data,outcome,score,positive) {
    p <- .original_plot_roc(data,outcome,score,positive)
    fit <- attr(p,"roc")
    p <- annotate_plot(p,title="Receiver operating characteristic",
      x="1 - specificity",y="Sensitivity",method="ROC / AUC",
      n=sum(stats::complete.cases(data[c(outcome,score)])),
      design=paste("Positive class:",positive),
      note=sprintf("AUC = %.3f; apparent performance unless held-out data provided",
                   as.numeric(pROC::auc(fit))))
    attr(p,"roc") <- fit
    p
  }
}

if (exists("plot_survival",mode="function") &&
    !exists(".original_plot_survival",inherits=FALSE)) {
  .original_plot_survival <- plot_survival
  plot_survival <- function(data,time,event,group) {
    p <- .original_plot_survival(data,time,event,group)
    fit <- attr(p,"fit")
    p <- annotate_plot(p,title="Kaplan-Meier survival estimate",x=time,
      y="Survival probability",method="Kaplan-Meier",
      n=sum(stats::complete.cases(data[c(time,event,group)])),
      design=paste("Stratified by",group),
      note="Censor marks displayed; no log-rank p or hazard ratio claimed")
    attr(p,"fit") <- fit
    p
  }
}

if (exists("plot_mean_ci",mode="function") &&
    !exists(".original_plot_mean_ci",inherits=FALSE)) {
  .original_plot_mean_ci <- plot_mean_ci
  plot_mean_ci <- function(data,time,value,group=NULL,conf_level=.95) {
    p <- .original_plot_mean_ci(data,time,value,group,conf_level)
    tab <- attr(p,"summary")
    p <- annotate_plot(p,title="Group means with pointwise intervals",
      x=time,y=paste("Mean",value),method="t confidence interval",
      n=sum(tab$n),design="descriptive time-by-group cells",
      note=sprintf("%.0f%% pointwise intervals; not a longitudinal model CI",
                   100*conf_level))
    attr(p,"summary") <- tab
    p
  }
}
