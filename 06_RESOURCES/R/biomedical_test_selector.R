# Dataset-neutral biomedical statistical-method decision helper.
# Sourcing defines functions only: no data access, analysis, installation or I/O.
# Decision support, not a substitute for a study-specific analysis plan.

biomedical_method_decision <- function(
    outcome_type,
    design = "independent",
    question = "compare",
    n_groups = NULL,
    adjusted = FALSE,
    has_exposure = FALSE,
    has_censoring = FALSE,
    multiple_outcomes = FALSE) {

  types <- c("continuous", "binary", "nominal", "ordinal",
             "count", "time_to_event", "omics_counts")
  designs <- c("independent", "paired", "repeated",
               "clustered", "complex_survey")
  questions <- c("describe", "compare", "associate", "predict")

  if (!is.character(outcome_type) || length(outcome_type) != 1L ||
      is.na(outcome_type) || !outcome_type %in% types)
    stop("outcome_type must be one of: ", paste(types, collapse = ", "),
         call. = FALSE)
  if (!is.character(design) || length(design) != 1L ||
      is.na(design) || !design %in% designs)
    stop("design must be one of: ", paste(designs, collapse = ", "),
         call. = FALSE)
  if (!is.character(question) || length(question) != 1L ||
      is.na(question) || !question %in% questions)
    stop("question must be one of: ", paste(questions, collapse = ", "),
         call. = FALSE)

  bools <- list(adjusted = adjusted, has_exposure = has_exposure,
                has_censoring = has_censoring,
                multiple_outcomes = multiple_outcomes)
  if (!all(vapply(bools, function(x)
    is.logical(x) && length(x) == 1L && !is.na(x), logical(1))))
    stop("All design flags must be one nonmissing logical value.",
         call. = FALSE)

  if (!is.null(n_groups) &&
      (!is.numeric(n_groups) || length(n_groups) != 1L ||
       !is.finite(n_groups) || n_groups < 1 ||
       n_groups != floor(n_groups)))
    stop("n_groups must be NULL or a positive whole number.",
         call. = FALSE)

  # Explicitly record the branch and release status, not a claim of
  # assumption satisfaction. Methods marked implemented have a reusable
  # function in 06_RESOURCES/R; documented methods require study implementation.
  decision <- function(id, label, status, r_entrypoint, rationale,
                       checks, evidence_ids = character()) {
    checks <- c("Confirm observation unit, outcome scale, missingness and units.",
                checks)
    if (multiple_outcomes)
      checks <- c(checks, "Declare the hypothesis family and multiplicity plan before testing.")
    result <- list(
      method_id = id,
      method = label,
      status = status,
      r_entrypoint = r_entrypoint,
      rationale = rationale,
      required_checks = unique(checks),
      reporting = c("Report observed and excluded n, with denominators.",
                    "Report estimand/effect measure and appropriate uncertainty.",
                    "State method, assumptions, contrast/reference direction and limitations."),
      evidence_ids = evidence_ids,
      decision_path = c(question, design, outcome_type,
                        if (is.null(n_groups)) "unspecified groups"
                        else paste(n_groups, "group(s)")),
      inputs = list(outcome_type = outcome_type, design = design,
                    question = question, n_groups = n_groups,
                    adjusted = adjusted, has_exposure = has_exposure,
                    has_censoring = has_censoring,
                    multiple_outcomes = multiple_outcomes)
    )
    class(result) <- "biomedical_method_decision"
    result
  }

  if (question == "describe" && design == "independent")
    return(decision(
      "descriptive", "Descriptive analysis (no hypothesis test)",
      "implemented", "describe_measurements(data, value, group = NULL)",
      "Describe denominators and distributions before selecting inference.",
      "Use appropriate summaries for variable type; do not report a test p-value."
    ))

  # Design gates outrank outcome labels: never silently infer simple-sample
  # standard errors for weighted, clustered or longitudinal data.
  if (design == "complex_survey")
    return(decision(
      "survey-design-review", "Complex-survey design-aware estimation/inference",
      "specialist-review", "survey::svydesign(); survey::svyglm()",
      "Weights alone are insufficient; strata and PSU/replicate design matter.",
      c("Verify weights, PSUs, strata and representativeness.",
        "Use design-aware variances and degrees of freedom."),
      c("BS-013", "BS-019")
    ))

  if (design %in% c("clustered", "repeated"))
    return(decision(
      "correlated-outcome-review", "Cluster/repeated-measures model review",
      "specialist-review", "lme4::lmer(); geepack::geeglm()",
      "Within-unit correlations invalidate ordinary independent-observation SEs.",
      c("Identify cluster/participant IDs and repeated occasions.",
        "Specify covariance or working-correlation structure and dropout.",
        "Select model family and diagnostics from outcome scale."),
      c("BS-002", "BS-014", "BS-015")
    ))

  if (question == "describe")
    return(decision(
      "descriptive-design-review", "Design-aware descriptive summaries",
      "specialist-review", "Specify clustered or repeated summary estimand",
      "A descriptive target for correlated observations requires a defined observation unit.",
      "Distinguish participants from repeated rows and any weighting.",
      "BS-014"
    ))

  if (outcome_type == "omics_counts")
    return(decision(
      "omics-design-review", "Assay-aware count modelling with FDR",
      "specialist-review", "DESeq2::DESeq(); edgeR::glmQLFit()",
      "Raw molecular counts require library normalization, dispersion and assay-aware designs.",
      c("Check raw counts, library sizes, batch, sample alignment and replication.",
        "Define contrasts and the gene-level multiple-testing family."),
      "BS-003"
    ))

  if (question == "predict")
    return(decision(
      "prediction-validation-review", "Prediction modelling and external validation",
      "specialist-review", "Study-specific prediction pipeline",
      "Prediction is not hypothesis testing; splits, calibration and leakage need a separate protocol.",
      c("Prespecify outcome horizon, feature timing and split unit.",
        "Report discrimination, calibration, uncertainty and subgroup performance."),
      "BS-007"
    ))

  if (adjusted)
    return(decision(
      "adjusted-model-review", "Adjusted outcome-specific regression",
      "specialist-review", "stats::lm(); stats::glm(); survival::coxph()",
      "Covariate adjustment changes the estimand and requires a design/causal specification.",
      c("Identify confounders versus mediators; check model family and diagnostics.",
        "Select an interpretable adjusted effect and confidence interval."),
      c("BS-012", "BS-013")
    ))

  if (outcome_type == "time_to_event")
    return(decision(
      if (has_censoring) "survival-analysis-review" else "time-origin-review",
      if (has_censoring) "Survival analysis with censoring"
      else "Time-to-event design: confirm origin/censoring",
      "specialist-review",
      if (has_censoring) "survival::survfit(); survival::coxph()"
      else "Define time origin and event/censoring first",
      "Event time, time zero and censoring are part of the outcome.",
      c("Verify time origin, event coding and at-risk sets.",
        "Assess competing risks and proportional hazards where relevant."),
      "BS-013"
    ))

  if (outcome_type == "count")
    return(decision(
      if (has_exposure) "count-rate-model-review" else "count-exposure-review",
      if (has_exposure) "Poisson/NB rate model review" else "Count model: exposure audit",
      "specialist-review",
      if (has_exposure) "stats::glm(..., family = poisson(), offset = log(exposure))"
      else "Verify exposure denominators before choosing an offset",
      "Count models require attention to exposure, overdispersion, zeros and dependence.",
      c("Check nonnegative integer counts and person-time/exposure.",
        "Assess mean/variance relation and zero-generating process.",
        "Consider negative binomial where Poisson dispersion is inadequate."),
      "BS-012"
    ))

  if (question == "associate")
    return(decision(
      "association-model-review", "Association/correlation model review",
      "documented", "stats::cor.test(); stats::lm(); stats::glm()",
      "Association methods depend on both variables' types, adjusted target and design.",
      c("Identify predictor scale and functional form.",
        "Distinguish descriptive correlation from adjusted association."),
      "BS-013"
    ))

  if (design == "paired") {
    if (outcome_type == "continuous" && identical(as.integer(n_groups), 2L))
      return(decision(
        "paired-t", "Paired t-test of within-subject mean change",
        "implemented", "paired_mean_change(data, id, visit, outcome, before_level, after_level)",
        "Mean difference uses within-ID alignment rather than row order.",
        c("Validate unique ID/visit keys, observed complete pairs and missingness.",
          "Inspect distribution of paired differences and influential points."),
        "BS-014"
      ))
    if (outcome_type == "binary" && identical(as.integer(n_groups), 2L))
      return(decision(
        "mcnemar", "McNemar comparison of paired binary responses",
        "documented", "stats::mcnemar.test()",
        "Discordant paired outcomes, not independent frequencies, drive the test.",
        c("Require a matched binary 2x2 table and report discordant counts.",
          "Review exact alternative for sparse discordant pairs."),
        "BS-012"
      ))
    if (outcome_type == "ordinal" && identical(as.integer(n_groups), 2L))
      return(decision(
        "signed-rank", "Paired Wilcoxon signed-rank or sign analysis",
        "implemented", "wilcox_paired(data, value, group, id)",
        "Use an ID-matched procedure rather than independent ranks.",
        c("Validate matching, zero differences and symmetry assumptions.",
          "Do not automatically interpret a rank test as a median difference."),
        "BS-001"
      ))
    return(decision(
      "paired-design-review", "Pair-aware model selection",
      "specialist-review", "Study-specific matched/pair-aware procedure",
      "The requested paired comparison does not have a simple validated route.",
      "Identify unit keys, within-pair alignment, levels and outcome family.",
      "BS-014"
    ))
  }

  # Independent-observation routes only beyond this point.
  if (is.null(n_groups) && outcome_type %in% c("continuous", "binary", "nominal", "ordinal"))
    return(decision(
      "group-count-review", "Specify comparison group structure",
      "specialist-review", "Provide n_groups and the intended group contrast",
      "Group count is required to choose a comparison method.",
      "Declare the number of observed groups and reference/category labels.",
      "BS-012"
    ))
  if (outcome_type == "continuous") {
    if (identical(as.integer(n_groups), 2L))
      return(decision(
        "welch-t", "Welch independent two-sample t-test",
        "implemented", "welch_mean_comparison(data, outcome, group, reference_level, comparison_level)",
        "Compare two independent group means without equal-variance assumption.",
        c("Inspect skewness/outliers and approximate sampling distribution of means.",
          "Specify the comparison-minus-reference direction."),
        c("BS-001", "BS-009", "BS-011")
      ))
    if (!is.null(n_groups) && n_groups >= 3)
      return(decision(
        "welch-anova", "Welch heteroscedastic one-way ANOVA",
        "implemented", "welch_oneway_comparison(data, outcome, group)",
        "Omnibus comparison of three or more independent means; no automatic post hoc claims.",
        c("Inspect within-group distributions and influential observations.",
          "Prespecify post-hoc contrasts and multiplicity separately."),
        c("BS-001", "BS-012")
      ))
    return(decision(
      "continuous-design-review", "Continuous-outcome comparison review",
      "documented", "stats::t.test()",
      "Specify groups and target estimand before applying a test.",
      "Confirm one-sample versus multi-group contrast.",
      "BS-001"
    ))
  }

  if (outcome_type == "ordinal")
    return(decision(
      if (identical(as.integer(n_groups), 2L)) "wilcox-independent" else "kruskal-wallis",
      if (identical(as.integer(n_groups), 2L)) "Wilcoxon rank-sum (distribution)"
      else "Kruskal-Wallis multi-group distribution comparison",
      if (identical(as.integer(n_groups), 2L)) "implemented" else "documented",
      if (identical(as.integer(n_groups), 2L)) "wilcox_independent(data, value, group)"
      else "stats::kruskal.test()",
      "Rank procedures compare aspects of distributions, not automatically means or medians.",
      c("Preserve ordinal coding and ties.",
        "Do not treat ordinal labels as equally spaced values."),
      "BS-001"
    ))

  if (outcome_type %in% c("binary", "nominal"))
    return(decision(
      if (identical(as.integer(n_groups), 1L)) "binomial-proportion" else "contingency-analysis",
      if (identical(as.integer(n_groups), 1L)) "Single proportion/exact binomial"
      else "Categorical contingency analysis (chi-square/Fisher)",
      "documented",
      if (identical(as.integer(n_groups), 1L)) "stats::binom.test()"
      else "stats::chisq.test(); stats::fisher.test()",
      "Categorical inference is based on counts and group denominators, not means.",
      c("Verify raw cell counts, denominators and sparse-cell assumptions.",
        "Choose exact or asymptotic method explicitly, not from an arbitrary cutoff."),
      c("BS-001", "BS-012")
    ))

  stop("No matching method route; check input specification.", call. = FALSE)
}

print.biomedical_method_decision <- function(x, ...) {
  if (!inherits(x, "biomedical_method_decision"))
    stop("Expected biomedical_method_decision object.", call. = FALSE)
  cat("Method: ", x$method, "\n",
      "ID: ", x$method_id, " | status: ", x$status, "\n",
      "R entrypoint: ", x$r_entrypoint, "\n",
      "Path: ", paste(x$decision_path, collapse = " / "), "\n",
      "Study requirements: ", paste(x$required_checks, collapse = " | "),
      "\n", sep = "")
  invisible(x)
}
