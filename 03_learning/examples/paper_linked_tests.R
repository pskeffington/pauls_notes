# Paper-linked teaching implementations. See ../bio_stats/README.md for provenance.
# Source has no downloads, package installation, fitting or file-writing effects.
# Inputs are synthetic except the explicitly attributed published aggregate/toy tables.

with_paper_seed <- function(seed, expr) {
  had_seed <- exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE)
  if (had_seed) old_seed <- get(".Random.seed", envir = .GlobalEnv)
  on.exit({
    if (had_seed) assign(".Random.seed", old_seed, envir = .GlobalEnv)
    else if (exists(".Random.seed", envir = .GlobalEnv, inherits = FALSE))
      rm(".Random.seed", envir = .GlobalEnv)
  })
  set.seed(seed)
  force(expr)
}

make_paper_fixture <- function() {
  with_paper_seed(7122026L, {
    n <- 120L
    group <- factor(rep(c("reference", "comparison", "third"), each = 40L),
                    levels = c("reference", "comparison", "third"))
    age <- stats::rnorm(n, 55, 9)
    g <- as.integer(group) - 1L
    marker <- 10 + 1.2 * g + .04 * (age - 55) + stats::rnorm(n, 0, 2)
    latent_grade <- .5 * g + stats::rlogis(n)
    d <- data.frame(
      id = sprintf("invented_%03d", seq_len(n)), group = group, age = age,
      marker = marker, before = marker,
      after = marker + .6 + .25 * g + stats::rnorm(n),
      binary = stats::rbinom(n, 1L, stats::plogis(-.8 + .5 * g)),
      category = factor(sample(c("A", "B", "C"), n, replace = TRUE)),
      grade = cut(latent_grade, c(-Inf, -.5, .7, Inf),
                  labels = c("low", "middle", "high"), ordered_result = TRUE),
      person_years = stats::runif(n, .5, 2)
    )
    d$episodes <- stats::rnbinom(n, size = 1.3,
                               mu = d$person_years * exp(.5 + .3 * g))
    event_time <- stats::rexp(n, rate = .04 * exp(.25 * g))
    censor_time <- stats::runif(n, 12, 36)
    d$time <- pmin(event_time, censor_time)
    d$event <- as.integer(event_time <= censor_time)
    # Distinct competing-risk endpoint, not a reinterpretation of d$event.
    relapse <- stats::rexp(n, .035 * exp(.2 * g))
    other_death <- stats::rexp(n, .025)
    d$cr_time <- pmin(relapse, other_death, censor_time)
    d$cr_status <- ifelse(censor_time < pmin(relapse, other_death), 0L,
                          ifelse(relapse < other_death, 1L, 2L))
    # Invented sampling design: 12 PSUs, 2 strata, one row per person.
    d$psu <- rep(seq_len(12L), 10L)
    d$stratum <- factor(ifelse(d$psu <= 6L, "one", "two"))
    d$weight <- stats::runif(n, 1, 3)
    # 60 invented people, 3 ordered visits each, one clustering level.
    long <- expand.grid(visit = 0:2, id = seq_len(60L))
    long <- long[order(long$id, long$visit), ]
    long$group <- factor(ifelse(long$id <= 30L, "reference", "comparison"),
                         levels = c("reference", "comparison"))
    intercept <- stats::rnorm(60L, 0, 2)
    long$marker <- 10 + intercept[long$id] + .3 * long$visit +
      .5 * long$visit * (long$group == "comparison") + stats::rnorm(180L)
    # A wholly synthetic assay: 500 features, 12 independent samples, 6/group.
    assay_group <- factor(rep(c("reference", "comparison"), each = 6L),
                          levels = c("reference", "comparison"))
    baseline <- exp(stats::runif(500L, log(30), log(800)))
    mu <- matrix(rep(baseline, 12L), nrow = 500L)
    mu[1:40, 7:12] <- mu[1:40, 7:12] * 2
    counts <- matrix(stats::rnbinom(length(mu), mu = as.vector(mu), size = 10),
                     nrow = 500L,
                     dimnames = list(sprintf("invented_gene_%03d", 1:500),
                                     sprintf("invented_sample_%02d", 1:12)))
    metadata <- data.frame(group = assay_group, row.names = colnames(counts))
    list(people = d, visits = long, counts = counts, metadata = metadata)
  })
}

validate_paper_fixture <- function(fixture) {
  d <- fixture$people
  required <- c("id", "group", "age", "marker", "before", "after", "binary",
                "category", "grade", "person_years", "episodes", "time", "event",
                "cr_time", "cr_status", "psu", "stratum", "weight")
  if (!is.data.frame(d) || !all(required %in% names(d)) || nrow(d) < 6L)
    stop("Missing person-level columns or insufficient rows")
  if (anyNA(d) || anyDuplicated(d$id) || any(!nzchar(d$id)))
    stop("Person IDs must be unique and nonmissing; no silent NA omission")
  numeric_names <- setdiff(required, c("id", "group", "category", "grade", "stratum"))
  if (!all(vapply(d[numeric_names], function(x)
    is.numeric(x) && all(is.finite(x)), logical(1))))
    stop("Numeric inputs must be finite")
  if (!is.factor(d$group) || nlevels(d$group) != 3L ||
      !identical(levels(d$group), c("reference", "comparison", "third")) ||
      !is.ordered(d$grade) || !is.factor(d$category))
    stop("Preserve group reference, nominal factors and ordered grade")
  if (any(d$person_years <= 0 | d$weight <= 0 | d$time <= 0 | d$cr_time <= 0) ||
      any(d$episodes < 0 | d$episodes != floor(d$episodes)) ||
      any(!d$binary %in% 0:1) || any(!d$event %in% 0:1) ||
      any(!d$cr_status %in% 0:2)) stop("Invalid count, exposure or event coding")
  long <- fixture$visits
  if (!all(c("id", "visit", "group", "marker") %in% names(long)) ||
      anyNA(long) || anyDuplicated(long[c("id", "visit")]) ||
      is.unsorted(long$id) || !is.numeric(long$marker) ||
      any(!is.finite(long$marker))) stop("Visits require unique ordered id/visit keys")
  counts <- fixture$counts
  metadata <- fixture$metadata
  if (!is.matrix(counts) || !is.numeric(counts) || anyNA(counts) ||
      any(!is.finite(counts)) || any(counts < 0 | counts != floor(counts)) ||
      anyDuplicated(colnames(counts)) || anyDuplicated(rownames(counts)) ||
      is.null(colnames(counts)) || is.null(rownames(counts)) ||
      !identical(colnames(counts), rownames(metadata)) ||
      !is.factor(metadata$group) || nlevels(metadata$group) != 2L)
    stop("Assay must have integer counts and identical ordered sample IDs")
  invisible(TRUE)
}

run_published_examples <- function() {
  # BS-001, Table 9, 'distant groups': paper's invented sanity-check vectors.
  x <- c(1, 2, 7, 8, 5)
  y <- c(10, 12, 15, 18, 20)
  paired <- stats::t.test(y, x, paired = TRUE)
  # AT-006, Table 1, Example 3: published illustrative counts, not patient rows.
  kim <- matrix(c(30L, 70L, 70L, 30L), nrow = 2L, byrow = TRUE,
                dimnames = list(sex = c("Male", "Female"), condition = c("A", "B")))
  # AT-007, Table 1: published aggregate table; do not expand to child-level rows.
  sct <- matrix(c(1L, 1L, 7L, 12L), nrow = 2L, byrow = TRUE,
                dimnames = list(before = c("AHR", "No_AHR"),
                                after = c("AHR", "No_AHR")))
  # BS-001 Table 10 has a checkable discrepancy for these constant samples.
  # Retain the disagreement; never change inputs to force the paper's p=.398.
  rank_discrepancy <- stats::wilcox.test(rep(1, 5), rep(10, 5),
                                        exact = FALSE, correct = TRUE)
  list(paired = paired, kim_table = kim,
       chi_square = stats::chisq.test(kim, correct = FALSE),
       sct_table = sct, mcnemar = stats::mcnemar.test(sct, correct = FALSE),
       mcnemar_cc = stats::mcnemar.test(sct, correct = TRUE),
       mcnemar_exact = stats::binom.test(1L, 8L, p = .5),
       mcnemar_mid_p = 2 * stats::pbinom(1L, 8L, .5) - stats::dbinom(1L, 8L, .5),
       rank_discrepancy = rank_discrepancy)
}

run_paper_base_examples <- function(fixture = make_paper_fixture()) {
  validate_paper_fixture(fixture)
  d <- fixture$people
  two <- droplevels(d[d$group != "third", ])
  reference <- two$marker[two$group == "reference"]
  comparison <- two$marker[two$group == "comparison"]
  delta <- d$after - d$before
  nonzero <- delta[delta != 0]
  if (!length(nonzero)) stop("Sign test requires at least one nonzero difference")
  poisson <- stats::glm(episodes ~ group + offset(log(person_years)),
                        family = stats::poisson(), data = d)
  linear <- stats::lm(marker ~ group + age, data = d)
  list(
    # Decision objects have checks and summaries, not invented p-values.
    A = list(outcome = "marker", unit = "invented person", estimand = "mean difference"),
    B = vapply(d, function(x) paste(class(x), collapse = "/"), character(1)),
    C = list(count_integer = all(d$episodes == floor(d$episodes)),
             exposure_range = range(d$person_years)),
    D = list(nominal = levels(d$category), ordinal = levels(d$grade)),
    E = list(people_per_group = table(d$group), pairs = nrow(d),
             repeated_units = length(unique(fixture$visits$id))),
    N = list(independent_table = table(two$group, two$binary),
             paired_table = run_published_examples()$sct_table),
    welch = stats::t.test(comparison, reference, var.equal = FALSE),
    rank_sum = stats::wilcox.test(comparison, reference, exact = FALSE,
                                 correct = TRUE, conf.int = TRUE),
    paired_t = stats::t.test(d$after, d$before, paired = TRUE),
    signed_rank = stats::wilcox.test(d$after, d$before, paired = TRUE,
                                    exact = FALSE, correct = TRUE, conf.int = TRUE),
    sign = stats::binom.test(sum(nonzero > 0), length(nonzero), p = .5),
    anova = stats::aov(marker ~ group, data = d),
    welch_anova = stats::oneway.test(marker ~ group, data = d, var.equal = FALSE),
    kruskal_wallis = stats::kruskal.test(marker ~ group, data = d),
    pearson = stats::cor.test(d$age, d$marker, method = "pearson"),
    spearman = stats::cor.test(d$age, d$marker, method = "spearman", exact = FALSE),
    linear = linear,
    ordinal_rank = stats::wilcox.test(as.integer(grade) ~ group, data = two,
                                     exact = FALSE, correct = TRUE),
    binomial = stats::binom.test(sum(d$binary), nrow(d), p = .5),
    chi_square = stats::chisq.test(table(two$group, two$binary), correct = FALSE),
    fisher = stats::fisher.test(table(two$group, two$binary)),
    logistic = stats::glm(binary ~ group + age, data = d, family = stats::binomial()),
    poisson = poisson,
    Z = list(missing = colSums(is.na(d)),
             linear_ci = stats::confint(linear),
             pearson_dispersion = sum(stats::residuals(poisson, type = "pearson")^2) /
               stats::df.residual(poisson),
             # Separate, explicitly prespecified family: four invented gene tests.
             raw_p = c(.003, .02, .07, .6),
             bh = stats::p.adjust(c(.003, .02, .07, .6), "BH"),
             holm = stats::p.adjust(c(.003, .02, .07, .6), "holm")),
    published = run_published_examples()
  )
}

paper_extended_packages <- function() {
  c("MASS", "nnet", "lme4", "geepack", "survey", "ordinal", "survival",
    "cmprsk", "DESeq2", "edgeR", "limma")
}

run_paper_extended_examples <- function(fixture = make_paper_fixture()) {
  validate_paper_fixture(fixture)
  packages <- paper_extended_packages()
  missing <- packages[!vapply(packages, requireNamespace, logical(1), quietly = TRUE)]
  if (length(missing)) stop("Install declared packages before full replay: ",
                            paste(missing, collapse = ", "))
  d <- fixture$people
  long <- fixture$visits
  counts <- fixture$counts
  metadata <- fixture$metadata
  # R resolves Surv() within the formula; bind it locally without attaching packages.
  Surv <- survival::Surv
  mixed_full <- lme4::lmer(marker ~ group * visit + (1 | id), data = long, REML = FALSE)
  mixed_null <- lme4::lmer(marker ~ group + visit + (1 | id), data = long, REML = FALSE)
  gee <- geepack::geeglm(marker ~ group * visit, id = id, waves = visit,
                         family = gaussian(), corstr = "exchangeable", data = long)
  design <- survey::svydesign(ids = ~psu, strata = ~stratum, weights = ~weight, data = d)
  ordinal <- ordinal::clm(grade ~ group + age, data = d, link = "logit")
  multinomial <- nnet::multinom(category ~ group + age, data = d,
                                trace = FALSE, Hess = TRUE, maxit = 1000)
  cox <- survival::coxph(Surv(time, event) ~ group + age, data = d, x = TRUE)
  dds <- DESeq2::DESeqDataSetFromMatrix(countData = counts, colData = metadata,
                                       design = ~group)
  dds <- DESeq2::DESeq(dds, quiet = TRUE, fitType = "mean")
  # filterByExpr is explicit; no outcome-driven filtering or sample reordering.
  ed <- edgeR::DGEList(counts = counts, group = metadata$group)
  ed <- ed[edgeR::filterByExpr(ed), , keep.lib.sizes = FALSE]
  ed <- edgeR::calcNormFactors(ed)
  ed <- edgeR::estimateDisp(ed)
  edge_result <- edgeR::exactTest(ed, pair = c("reference", "comparison"))
  assay_design <- stats::model.matrix(~group, data = metadata)
  voom <- limma::voom(ed, design = assay_design, plot = FALSE)
  voom_fit <- limma::eBayes(limma::lmFit(voom, assay_design))
  # Invented continuous log2 intensities, a distinct assay from the raw counts.
  intensities <- log2(counts + 1)
  intensity_fit <- limma::eBayes(limma::lmFit(intensities, assay_design))
  list(
    negative_binomial = MASS::glm.nb(episodes ~ group + offset(log(person_years)), data = d),
    multinomial = multinomial, ordinal = ordinal,
    ordinal_po_check = ordinal::nominal_test(ordinal),
    mixed = mixed_full, mixed_lrt = stats::anova(mixed_null, mixed_full),
    mixed_singular = lme4::isSingular(mixed_full),
    gee = gee,
    survey = survey::svyglm(marker ~ group + age, design = design),
    kaplan_meier = survival::survfit(Surv(time, event) ~ group, data = d),
    log_rank = survival::survdiff(Surv(time, event) ~ group, data = d),
    cox = cox, cox_ph_check = survival::cox.zph(cox),
    cumulative_incidence = cmprsk::cuminc(d$cr_time, d$cr_status, group = d$group, cencode = 0),
    deseq2 = as.data.frame(DESeq2::results(dds,
      contrast = c("group", "comparison", "reference"), alpha = .05)),
    edger = edgeR::topTags(edge_result, n = Inf, adjust.method = "BH")$table,
    voom_limma = limma::topTable(voom_fit, coef = "groupcomparison", n = Inf,
                               adjust.method = "BH"),
    intensity_limma = limma::topTable(intensity_fit, coef = "groupcomparison", n = Inf,
                                    adjust.method = "BH")
  )
}

if (sys.nframe() == 0L) {
  args <- commandArgs(trailingOnly = TRUE)
  if (length(args) > 1L || (length(args) == 1L && args != "--full"))
    stop("Usage: Rscript --vanilla 03_learning/examples/paper_linked_tests.R [--full]")
  base <- run_paper_base_examples()
  cat("Published paired t p:", base$published$paired$p.value, "\n")
  cat("Published chi-square:", unname(base$published$chi_square$statistic), "\n")
  cat("Published McNemar asymptotic p:", base$published$mcnemar$p.value, "\n")
  cat("Published McNemar exact p:", base$published$mcnemar_exact$p.value, "\n")
  cat("Published rank-sum discrepancy; R p:", base$published$rank_discrepancy$p.value, "\n")
  if (length(args)) {
    extended <- run_paper_extended_examples()
    cat("Executed extended methods:", paste(names(extended), collapse = ", "), "\n")
  }
  print(utils::sessionInfo())
}
