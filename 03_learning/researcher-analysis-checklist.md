# Principles of Statistical Analysis Selection in Biomedical Research

Authored by Paul Skeffington · Compiled with OpenAI

[Learning home](README.md) · [Data-type-first decision guide](biomedical-statistics-decision-guide.md) · [Study types and published examples](study-designs-and-published-examples.md) · [Study protocol](../templates/study-protocol.md)

Statistical analysis selection requires an explicit relationship among the scientific question, the measurement scale, the study design, and the quantity to be estimated. A procedure is justified when its assumptions and interpretation correspond to those features. Identifying a familiar test is therefore only one part of developing an analysis plan.

This chapter presents a structured framework for that reasoning. It begins with the outcome and proceeds through the study population, sampling and dependence, temporal structure, model specification, evaluation, and reporting. The framework culminates in a written analysis rationale and a concise researcher checklist. Where the available data do not support the intended question, an appropriate conclusion may be a descriptive analysis or a provisional plan pending additional information.

**Learning objectives.** After studying this chapter, the reader should be able to distinguish measurement type from study design; define an estimand and its population; explain how dependence and sampling constrain analysis; justify an analysis family; and specify the diagnostic, sensitivity, and reporting requirements of a proposed study.

**Scope.** The four worked examples are hypothetical teaching scenarios. References to published studies provide methodological context; their analyses are not reproduced here. This chapter does not modify the repository's frozen research protocols.

## 1. Outcome Definition and Measurement Scale

The outcome is the variable whose distribution, association, or response is under investigation. A concentration in ng/mL is continuous. Number of hospital visits is a discrete count. Cancer present/absent is binary. Stage is ordinal even when stored as 1, 2, 3, 4. Time to recurrence requires both elapsed time and event/censoring information. A numerical patient identifier is not a measured quantity.

The outcome must also be distinguished from the explanatory variables or predictors. Comparing mean concentration between two treatment groups has a continuous outcome and categorical predictor. Explaining disease status from concentration reverses those roles and gives a binary-outcome question. The presence of a categorical column alone does not select a chi-square test.

The data dictionary and original measurement instrument establish the meaning of each variable. In molecular research, raw counts, normalized measurements, transformed expression, and derived subtype labels represent distinct analytical inputs.

## 2. Scientific Objective and Estimand

Scientific objectives include description, group comparison, association, estimation of intervention effects, diagnostic evaluation, and prediction. These purposes may use similar data but require different evidence. A model that predicts mortality does not automatically estimate how treatment would change mortality.

An **estimand** is the precisely defined quantity that the study seeks to estimate. Examples include a mean difference, response probability, risk difference, odds ratio, incidence-rate ratio, survival probability at a specified horizon, or prediction error. Its definition includes the relevant population, comparison, outcome, and time window. A mean, median, distributional contrast, and threshold-based probability are distinct targets.

**Probability, estimation, and hypothesis testing.** “How likely are at least k responses under a specified success rate?” is a probability-model calculation. “What is the response rate and its uncertainty?” is estimation. “Is the response rate different from a prespecified benchmark?” is a hypothesis test. These questions require separate interpretations even when they use the same probability model.

## 3. Sampling, Allocation, and Study Design

Study classification begins with the basis for participant inclusion: a population sample, eligibility at a cohort index date, selection as a disease case/control, attendance at a clinic, or assignment in a trial. Exposure may be observed or assigned; when assigned, the allocation mechanism must be specified. Existing records can form a retrospective cohort; they do not automatically form a case-control study.

Sampling changes interpretation. A case-control sample generally cannot supply population disease risk from its case fraction. A complex survey needs its weights, strata, and sampling units. A randomized trial requires the assignment scheme and prespecified analysis population. A historical comparator requires an explanation of changes across time.

The [published-paper examples](study-designs-and-published-examples.md#3-published-paper-examples) illustrate how inclusion criteria and allocation distinguish designs. The statistical procedure does not itself define the study design.

## 4. Units of Observation and Statistical Dependence

The number of independent experimental or sampling units must be distinguished from the number of recorded observations. Two tissue specimens from one person form a pair. Three visits form repeated measurements. Cells from one specimen and specimens from one donor form a hierarchy. In a cluster randomized trial, a hospital may be the allocation unit while patients supply outcomes.

Pairing changes the analysis: a paired continuous comparison analyzes within-person differences. For paired binary measurements, the discordant pairs drive a McNemar comparison. With several visits or nested sites, a mixed-effects model or generalized estimating equations (GEE) may be appropriate, depending on the outcome and scientific target. Cluster count and covariance assumptions matter; simply adding a person-ID predictor does not reproduce every dependence-aware method.

Participant linkage and allocation records are necessary to characterize dependence. Counting repeated observations as independent units constitutes pseudoreplication and can misrepresent statistical precision.

## 5. Temporal Structure and Denominators

A binary response measured for everyone at the same fixed endpoint differs from time to response with incomplete follow-up. A visit count over one month differs from the same count over one year. A rate needs an exposure denominator such as person-years. Survival analysis needs a time origin, event definition, censoring rules, and consideration of competing events.

For policy evaluation, the temporal resolution and duration of observations determine whether a longitudinal comparison is feasible. Two totals cannot identify baseline trend, seasonality, or autocorrelation. For prediction, each predictor must be available at the intended decision time.

## 6. Data Quality, Missingness, and Feasibility

A feasibility assessment documents the numbers of participants, complete pairs, groups, sites, events, non-events, and observed follow-up. Data review addresses duplicate identifiers, impossible values, inconsistent units, batch effects, sparse categories, and missingness by group and time. Distributional and longitudinal displays should retain the grouping structure of the study. The reported sample size is specific to the analysis and cannot be inferred from the number of imported rows alone.

The missing-data strategy requires an explicit account of plausible missingness mechanisms and the assumptions of the proposed treatment. Complete-case analysis is not automatically unbiased. Imputation must respect variable types, design, and the analysis; prediction preprocessing must be learned within training data. Few events, few clusters, separation, or a confounded design matrix can make an intended model unreliable or unidentified.

Insufficient information may require a scientifically justified reduction in model complexity, additional data collection, or restriction to descriptive estimation. A more elaborate model does not resolve inadequate identification or sampling.

## 7. Covariate Specification and Prediction Evaluation

For association or causal questions, covariate specification depends on the scientific objective, temporal ordering, and a defensible causal structure. Adjustment for all available variables is not a general safeguard: mediators and colliders can alter or bias the intended contrast. Randomized trials may prespecify baseline adjustment and stratification even though allocation was randomized.

A prediction study specifies its intended use, horizon, development and evaluation partitions, and any required separation by person, site, or time. Feature selection and preprocessing belong inside training. AUC alone does not establish calibration or clinical usefulness. Univariable statistical significance alone is an insufficient rationale for covariate selection.

## 8. Selection of an Analysis Family

The preceding sections establish the information needed to identify a suitable analysis family. Table 1 summarizes common correspondences. Each entry remains conditional on the estimand, design, and assumptions. Further procedural detail appears in the [test reference](biomedical-statistics-decision-guide.md#5-data-type-to-test-reference-common-biomedical-questions), with exercises in the [workbook](statistics-practice-workbook.md).

**Table 1. Analysis families classified by outcome, objective, and observation structure.**

| Outcome and analytical objective | Candidate analysis family | Design and assumption considerations |
| --- | --- | --- |
| Description of a continuous measurement | Distribution plots and suitable location/spread summaries; uncertainty if required | Skew, censoring of assay values, sampling design |
| One binary endpoint; specified benchmark probability | Binomial calculation, proportion estimation, or one-sample binomial test according to purpose | Nonindependence, unequal success probabilities, sampling without replacement |
| Two independent groups; target is a continuous mean difference | Welch comparison or a suitable linear model | Covariate adjustment, influential observations, dependence |
| Two continuous measurements per person; target is mean change | Paired t-test on differences | Difference distribution, incomplete pairs, more time points |
| Three or more independent groups; continuous means | ANOVA/Welch ANOVA or linear model with prespecified contrasts | Heterogeneous variance, repeated observations, multiplicity |
| Ordered outcome or a specified rank/distribution question | Appropriate ordinal model or rank procedure | Dependence; signed-rank symmetry; interpretation as a median difference needs more assumptions |
| Two categorical variables in independent people | Contingency-table inference such as chi-square or Fisher; effect estimates | Sparsity, design, adjustment, case-control sampling |
| Binary outcome and covariates | Logistic model for odds; an appropriate risk model if risk is the target and identifiable | Sampling, separation, clustering; odds ratios are not risk ratios |
| Paired binary outcome at two times | McNemar method and paired effect estimate | More visits, covariates, missing pairs |
| Event counts with exposure time | Poisson-rate model with log-exposure offset; assess negative binomial if appropriate | Overdispersion, recurrent events, clustering, serial dependence |
| Time and event status with censoring | Kaplan–Meier/log-rank for suitable survival questions; Cox or another justified survival model | Nonproportional hazards, competing risks, delayed entry, absolute-risk target |
| Index test versus reference standard | Diagnostic accuracy with thresholds and paired-test/reader structure retained | Verification bias, enrichment, incomplete reference assessments |
| Future risk prediction | Validated regression/ML pipeline; discrimination, calibration, prediction error and utility | Horizon, censoring, competing events, leakage, site/time transportability |
| Many gene-level outcomes | Assay-aware model with biological replication, contrasts and multiplicity control | Raw versus transformed data, donor/batch structure, design identifiability |
| Outcomes around a policy change | Controlled time-series or other justified quasi-experimental analysis | Adequacy of time points, trends, seasonality, comparison validity, concurrent shocks |

## 9. Assumptions, Diagnostics, and Sensitivity Analysis

Diagnostic evaluation must address the assumptions of the proposed analysis. A normality test applied indiscriminately to raw variables does not provide a general method-selection rule. For a paired t-test, the distribution of differences matters. For linear models, relevant assessments include functional form, residual behavior, influence, and variance structure. For count models, dispersion and residual patterns require evaluation. Logistic models require attention to separation and fit. Cox models require assessment of proportional hazards, time origin, and censoring assumptions. Clustered analyses require a justified correlation specification and an adequate number of independent clusters.

A nonsignificant diagnostic is not proof of an assumption. Nonparametric methods also have assumptions and may target a different quantity. Scientifically motivated sensitivity analyses should be prespecified where possible; subsequent modifications require transparent documentation.

## 10. Prespecified Comparisons and Multiplicity

Inferential testing requires a defined null or reference value, significance level, and confidence level. A one-sided alternative requires a defensible directional question specified before observing the results. The multiplicity plan identifies the relevant family of gene tests, subgroup contrasts, endpoints, or time points and the corresponding adjustment. An omnibus test and a particular pairwise difference answer different questions.

## 11. Interpretation, Reporting, and Reproducibility

Reporting includes the estimate, direction, units, denominator, uncertainty, and substantive limitations, together with any p-value. Group summaries, event counts, and missingness establish the context of the result. Prediction reports identify the evaluation population and quantify performance with uncertainty. Interpretation must preserve the estimate's scale; statistical significance does not itself establish clinical importance, causality, or useful prediction.

The [analysis record](../templates/analysis-record.md) documents protocol version, data provenance, software versions, code revision, configurations, and reproducible commands. Design variables must remain available throughout data preparation and fitting. Prespecified analyses and exploratory changes require separate identification.

## 12. Formulation of the Analysis Rationale

An analysis rationale integrates the preceding decisions into a coherent methodological statement. The following structure can be adapted to the [study protocol](../templates/study-protocol.md) before execution:

> The study will estimate [target quantity] for [comparison] among [population], using [outcome, measurement scale, units, and horizon]. The [design] comprises [independent units and dependence structure]. Eligibility and exclusions define an analysis population of [counts], with missingness addressed through [strategy and assumptions]. The primary analysis will use [method], retaining [pairing, clustering, weights, or temporal structure] and adjusting for [prespecified variables and rationale]. Model assessment will address [diagnostics], with [multiplicity plan] and [sensitivity analyses]. Reporting will include [estimate, interval, denominator, and table or figure]. Interpretation is limited by [design or data constraint].

Unresolved elements should be identified in a **provisional analysis plan**, together with the information required to resolve them. A completed rationale records the justification for the proposed analysis; validity still depends on the design, data, assumptions, and execution.

## Worked Example A. Paired Molecular Measurements

Consider an observational study in which each participant contributes one tumor specimen and one matched normal specimen. The outcome is a transformed continuous assay measurement in arbitrary units. The estimand is the mean within-person tumor-minus-normal difference in the specified study population.

For participant i, define the difference as

\[
D_i=Y_{i,\mathrm{tumor}}-Y_{i,\mathrm{normal}},\qquad
\Delta=E(D_i).
\]

When participants are independent and the distribution of differences supports the intended inference, a paired t-test provides a test of the mean difference against a prespecified value, together with an interval estimate. The assessment concerns the differences, including influential observations. The report states the number of complete pairs, the treatment of incomplete observations, and the estimated difference with its uncertainty. An independent two-sample procedure would fail to represent the pairing.

The analysis changes if the input consists of raw RNA-seq counts across thousands of genes. An assay-appropriate model then requires biological replication, participant blocking, prespecified contrasts, and a defined multiplicity strategy. Additional visits or specimens introduce further dependence. The [molecular characterization reading](study-designs-and-published-examples.md#sd-01-molecular-characterization-a-cross-sectional-analysis-layer) provides related biological context. Neither a paired molecular contrast nor its statistical significance establishes an intervention effect.

## Worked Example B. A Binomial Response Probability

Suppose that 80 independent participants are assessed for a binary response at a common endpoint. Under a specified model in which every participant has response probability 0.35, the number of responses X follows a binomial distribution. The probability of observing at least 36 responses is

\[
X\sim\operatorname{Binomial}(80,0.35),\qquad
P(X\ge36)=\sum_{x=36}^{80}\binom{80}{x}(0.35)^x(0.65)^{80-x}.
\]

The corresponding R expression is `pbinom(35, size = 80, prob = 0.35, lower.tail = FALSE)`. The argument 35 is required because the upper-tail convention calculates P(X > 35), which equals P(X ≥ 36) for an integer-valued variable. This is a documented reference expression; no numerical execution is claimed in this chapter.

This calculation answers a probability question under a stipulated model. Under a prespecified one-sided test of the simple null p = 0.35 against p > 0.35, the same upper tail supplies the p-value. Estimation of the response probability is a separate task requiring an estimate and interval. If the reference probability was estimated from another sample, its uncertainty also requires consideration. Incomplete follow-up, dependence, or unequal response probabilities can invalidate the simple binomial specification. An observed response count in a single treatment group does not by itself establish efficacy against an unobserved control.

## Worked Example C. Emergency Visits Following a Texting-While-Driving Prohibition

### Research question and outcome definition

Suppose that a jurisdiction implements a prohibition on texting while driving. A researcher seeks to determine whether implementation is associated with a change in emergency-department visits for motor-vehicle-crash injuries. The primary outcome is the number of qualifying ED encounters during a specified observation period. It is a **quantitative discrete count**. The policy indicator, coded as before or after implementation, is a **qualitative binary predictor**. Its categorical form does not make the visit count a categorical outcome.

The outcome definition should specify the injury codes, participating hospitals, inclusion of drivers and other road users, and handling of transfers or repeat encounters. All-cause ED visits answer a broader utilization question and may obscure changes in crash-related injuries. Crash-related visits also do not establish that texting caused each individual crash. The policy question concerns outcomes following a population-level intervention.

### Study design and observation unit

If the available data consist of one annual count before the law and one afterward, the design is an uncontrolled before-and-after comparison. The observations are jurisdiction-years, rather than two groups of independently randomized patients. The analysis can describe the observed change, but it cannot separate policy implementation from an existing trend or another contemporaneous change.

A more informative design uses repeated monthly counts over adequate periods before and after implementation. With one jurisdiction, this permits an interrupted time-series analysis. A comparable jurisdiction without the same policy change may provide a control series, subject to assessment of comparability, spillovers, and concurrent policies. The relevant exposure date is the effective or enforcement date specified in the protocol; an enactment date alone may not correspond to a change in driving behavior. Anticipation, delayed enforcement, and gradual adoption require explicit consideration.

### Denominator and descriptive comparison

The denominator determines the rate being estimated. Visits per resident-year describe population injury burden; visits per vehicle-mile traveled describe burden relative to driving exposure. These quantities are not interchangeable. A decline in traffic volume can reduce visit counts without a corresponding decline in injury risk per mile. The numerator and denominator must refer to compatible geography, road users, hospital coverage, and time periods.

For each period, the researcher first reports the count, exposure denominator, rate, and missingness or coverage changes. The ratio of the post-policy rate to the pre-policy rate is a descriptive rate ratio. Even if a Poisson comparison supplies a confidence interval, two annual observations provide no residual information with which to assess trend, seasonality, serial dependence, or dispersion.

### Candidate model for a monthly series

For a sufficiently informative single-jurisdiction monthly series, let Y_t denote crash-related ED encounters, E_t a positive exposure denominator, and t elapsed months. Let I_t equal one from the prespecified implementation month onward and zero beforehand; let S_t equal zero before implementation and count months since implementation, beginning at zero in the first intervention month. A candidate segmented count-model mean specification is

\[
\log(\mu_t)=\log(E_t)+\beta_0+\beta_1t+\beta_2I_t
+\beta_3S_t+f_{\mathrm{season}}(t)+\boldsymbol{\gamma}^{\mathsf T}\mathbf Z_t,
\qquad \mu_t=E(Y_t).
\]

The exposure offset represents the chosen denominator. The coefficient beta_1 describes the baseline log-rate trend, beta_2 the immediate level change, and beta_3 the change in trend following implementation. Seasonal terms and justified covariates Z_t address specified temporal features and measured alternative explanations. A Poisson variance assumption requires assessment; overdispersion may motivate a negative-binomial or another justified count model. Serial correlation requires a separate treatment: changing the count distribution alone does not account for temporal dependence.

Under this specification, the modeled rate ratio at m months after implementation, relative to continuation of the specified pre-policy trend with other terms held fixed, is exp(beta_2 + beta_3 m). This is a model-based contrast. Its interpretation depends on the trend specification and assumptions about what would have occurred without the policy. A controlled interrupted time series requires additional group and interaction terms; the single-series equation above is not a complete controlled analysis.

### Diagnostics and interpretation

The researcher examines plotted counts and rates, pre-policy trends, seasonal patterns, dispersion, residual dependence, and influential months. Relevant alternative explanations include changes in traffic volume, hospital participation, injury coding, weather, road-safety measures, and access to emergency care. Prespecified sensitivity analyses may vary the implementation window, examine a justified transition period, or assess alternative trend specifications. A decline in aggregate visits does not by itself establish individual compliance or identify the contribution of enforcement.

The resulting methods statement might read: “Monthly crash-related ED encounters will be analyzed using a segmented count-rate model with a prespecified exposure denominator. The analysis will estimate immediate and subsequent trend changes following implementation of the texting prohibition, while addressing seasonal variation, measured temporal covariates, overdispersion, and serial dependence. Results will include rate contrasts with confidence intervals, diagnostic findings, and sensitivity analyses. Policy attribution will remain conditional on the credibility of the comparison and the absence of unaccounted concurrent changes.”

### Connection to published research

Ferdinand, Aftab, and Akinlotan (2019) examined texting bans and crash-related ED visits in 16 US states during 2007–2014: [Texting-While-Driving Bans and Motor Vehicle Crash–Related Emergency Department Visits in 16 US States: 2007–2014](https://pubmed.ncbi.nlm.nih.gov/30896993/). The primary-article record provides a directly related empirical reading. The monthly segmented model above is a proposed teaching specification, not a reconstruction of that paper's analysis. No observed effect size or executed policy evaluation is asserted here. The [count/rate example](biomedical-statistics-decision-guide.md#e-emergency-department-visits-before-and-after-legislation-year-1-versus-year-2) provides complementary introductory arithmetic.

## Worked Example D. Prognostic Prediction

Consider a cohort intended to predict breast cancer mortality within a specified period after diagnosis. The outcome involves event time, incomplete follow-up, and competing death from other causes. The objective is individual prognosis using information available at diagnosis.

The protocol defines the index date, eligible population, prediction horizon, predictor availability, event definitions, and handling of censoring and competing events. Model development and validation must preserve participant separation and represent the intended site or temporal setting. Preprocessing, feature selection, and tuning remain within the development process. Evaluation includes discrimination, calibration, prediction error, and the utility of decisions at relevant thresholds.

The appropriate model depends on the probability being predicted and the treatment of competing events. A well-performing prognostic model describes risk under the conditions represented in its data; it does not, by itself, identify an individual's causal treatment benefit. The [QResearch reading](study-designs-and-published-examples.md#sd-08-retrospective-cohort-with-a-prognostic-prediction-objective) provides a published comparison of prognostic approaches. This hypothetical example does not amend the repository's frozen survival experiment.

## Researcher Checklist

The following checklist records the decisions developed in the chapter. Each completed item should correspond to a statement in the protocol or analysis rationale.

- [ ] The outcome, measurement scale, units, and coding are defined.
- [ ] The scientific objective, target population, estimand, and horizon are specified.
- [ ] Sampling, exposure assignment, comparator selection, and study design are documented.
- [ ] Observation, allocation, and independent analysis units are distinguished.
- [ ] Index date, follow-up, denominators, event definitions, and censoring rules are stated.
- [ ] Data quality, analysis-specific sample size, missingness, and feasibility are assessed.
- [ ] Covariate selection or prediction-validation strategy has a substantive justification.
- [ ] The proposed analysis family corresponds to the outcome, estimand, and design.
- [ ] Model assumptions, diagnostics, and sensitivity analyses are specified.
- [ ] Primary comparisons, inferential direction, and multiplicity handling are prespecified.
- [ ] Reporting includes effect scale, denominators, uncertainty, limitations, and reproducibility.
- [ ] A coherent analysis rationale identifies any unresolved decisions and conditions for revision.

## References and Further Study

The [source register](../06_RESOURCES/Literature/study_design_paper_examples.csv) identifies the nine published studies discussed in the companion design chapter. The [methods evidence review](../06_RESOURCES/Literature/BIOSTATISTICS_R_LITERATURE_2021_2026.md) provides further methodological context. Official R documentation describes [t-tests and pairing](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/t.test.html), [Wilcoxon hypotheses](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/wilcox.test.html), [Fisher's conditional test](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/fisher.test.html), and [binomial probabilities](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Binomial.html). Implementation details should be checked against the software version used in an analysis.

The completed rationale belongs in the study-specific protocol; execution, deviations, and verification belong in the analysis record. Participant records and restricted inputs remain outside the public notes.
