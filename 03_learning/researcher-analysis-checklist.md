# A researcher's narrative checklist: which analysis should I run?

Authored by Paul Skeffington · Compiled with OpenAI

[Learning home](README.md) · [Data-type-first decision guide](biomedical-statistics-decision-guide.md) · [Study types and published examples](study-designs-and-published-examples.md) · [Study protocol](../templates/study-protocol.md)

Work through this checklist **before fitting a model**. At each step, write the requested sentence. The sentences become a short analysis rationale that someone else can review. An unresolved answer can mean collecting more information, narrowing the question, or reporting descriptively; it need not produce a test name.

The worked scenarios below are invented teaching examples. Links to published studies illustrate related designs, not analyses reproduced here. This checklist does not amend any frozen research protocol.

## 1. What exactly have I measured?

- [ ] **I can name the outcome, its data type, units, and coding.**

Start with the variable whose behavior you want to explain. A concentration in ng/mL is continuous. Number of hospital visits is a discrete count. Cancer present/absent is binary. Stage is ordinal even when stored as 1, 2, 3, 4. Time to recurrence requires both elapsed time and event/censoring information. A numerical patient identifier is not a measured quantity.

Then distinguish the outcome from the predictors. Comparing mean concentration between two treatment groups has a continuous outcome and categorical predictor. Explaining disease status from concentration reverses those roles and gives a binary-outcome question. The presence of a categorical column alone does not select a chi-square test.

**Write:** “My outcome is ___, measured in ___, with type ___ and coding ___. My exposure/group/predictors are ___.”

**If unresolved:** inspect the data dictionary and original instrument. For molecular data, distinguish raw counts, normalized values, transformed expression, and derived subtype labels before selecting a model.

## 2. What do I want the answer to mean?

- [ ] **I can state a question and a target quantity in ordinary language.**

Decide whether you want to describe the sample, compare groups, estimate an association, estimate an intervention effect, evaluate a diagnostic test, or predict a future outcome. These purposes may use similar data but require different evidence. A model that predicts mortality does not automatically estimate how treatment would change mortality.

Name the quantity you want: mean difference, response probability, risk difference, odds ratio, incidence-rate ratio, survival probability at a horizon, or prediction error. Specify the population, comparator, direction, and time window. Decide whether the question is about a mean, a median, a distribution, or a clinically meaningful threshold.

**Write:** “Among ___, I want to estimate ___ for ___ compared with ___ over ___.”

**Probability or inference?** “How likely are at least k responses under a specified success rate?” is a probability-model calculation. “What is the response rate and its uncertainty?” is estimation. “Is the response rate different from a prespecified benchmark?” is a hypothesis test. Record which of these you need; do not interchange their answers.

## 3. How did these observations enter the study?

- [ ] **I can identify the sampling and assignment design.**

Ask why each participant is present: a population sample, eligibility at a cohort index date, selection as a disease case/control, attendance at a clinic, or assignment in a trial. Record whether exposure was observed or assigned and whether assignment was randomized. Existing records can form a retrospective cohort; they do not automatically form a case-control study.

Sampling changes interpretation. A case-control sample generally cannot supply population disease risk from its case fraction. A complex survey needs its weights, strata, and sampling units. A randomized trial requires the assignment scheme and prespecified analysis population. A historical comparator requires an explanation of changes across time.

**Write:** “This is a ___ study. Participants entered because ___. Exposure was ___, and the comparison group was obtained by ___.”

Use the [published-paper examples](study-designs-and-published-examples.md#3-published-paper-examples) to check this classification. Do not choose a design label simply because a particular statistical test is familiar.

## 4. What is independent, and what belongs together?

- [ ] **I can distinguish participants from specimens, visits, cells, and allocation units.**

Count the independent people or experimental units, then describe the rows. Two tissue specimens from one person form a pair. Three visits form repeated measurements. Cells from one specimen and specimens from one donor form a hierarchy. In a cluster randomized trial, a hospital may be the allocation unit while patients supply outcomes.

Pairing changes the analysis: a paired continuous comparison analyzes within-person differences. For paired binary measurements, the discordant pairs drive a McNemar comparison. With several visits or nested sites, consider a mixed model or GEE suitable for the outcome and scientific target. Cluster count and covariance assumptions matter; simply adding a person-ID predictor does not reproduce every dependence-aware method.

**Write:** “The independent unit is ___. Each unit contributes ___ rows, linked by ___. Assignment occurred at the ___ level.”

**If unresolved:** recover the linkage or allocation information. Do not treat repeated observations as independent to make a larger apparent sample.

## 5. What time, denominator, and comparison are available?

- [ ] **I can define the index date, follow-up, exposure denominator, and event window.**

A binary response measured for everyone at the same fixed endpoint differs from time to response with incomplete follow-up. A visit count over one month differs from the same count over one year. A rate needs an exposure denominator such as person-years. Survival analysis needs a time origin, event definition, censoring rules, and consideration of competing events.

For a policy evaluation, determine whether you have only two annual totals or a sufficiently long series before and after the change. Two totals cannot identify baseline trend, seasonality, or autocorrelation. For prediction, verify that every predictor is available when the prediction would actually be made.

**Write:** “Follow-up begins at ___ and ends at ___. The denominator is ___. Events are ___; censoring/competing events are ___.”

## 6. Are the data sufficient for the proposed question?

- [ ] **I have checked counts, missingness, measurement quality, and analysis feasibility.**

Summarize people, complete pairs, groups, sites, events, non-events, and follow-up. Check duplicate IDs, impossible values, units, batch effects, sparse categories, and missingness by group and time. Plot distributions and trajectories in a way that preserves the study structure. Document the analysis-specific denominator rather than reporting the imported row count as n.

Ask why values are missing and what the planned handling assumes. Complete-case analysis is not automatically unbiased. Imputation must respect variable types, design, and the analysis; prediction preprocessing must be learned within training data. Few events, few clusters, separation, or a confounded design matrix can make an intended model unreliable or unidentified.

**Write:** “The analysis includes ___ independent units and ___ events/pairs/clusters. Missingness and exclusions are ___. The main feasibility concern is ___.”

**If insufficient:** simplify a justified model, seek additional data, or retain descriptive estimates with clear limitations. Do not increase model complexity to compensate for a weak design.

## 7. Do I need an unadjusted contrast, an adjusted model, or prediction validation?

- [ ] **I can justify the covariates and evaluation strategy before inspecting significance.**

For association or causal questions, choose adjustment variables using the scientific question, timing, and a defensible causal structure. Avoid mechanically adjusting for every available column; mediators and colliders can change or bias the target contrast. Randomized trials may prespecify baseline adjustment and stratification even though allocation was randomized.

For prediction, define the intended use, horizon, training/tuning/evaluation partitions, and separation by person, site, or time as appropriate. Feature selection and preprocessing belong inside training. AUC alone does not establish calibration or clinical usefulness. Do not select covariates solely because their univariable p-values are small.

**Write:** “My primary contrast is ___; I will adjust for ___ because ___. For prediction, I will evaluate on ___ using ___.”

## 8. Which analysis family matches those answers?

- [ ] **I can explain both the proposed method and why a tempting alternative would answer the wrong question.**

The table is a starting point after Steps 1–7, not an automatic selector. Use the [full test reference](biomedical-statistics-decision-guide.md#5-data-type-to-test-reference-common-biomedical-questions) for details and the [workbook](statistics-practice-workbook.md) to practice.

| Answers so far | Initial analysis family | What could change the choice? |
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

**Write:** “I propose ___ because the outcome is ___, the target is ___, and the design is ___. I would not use ___ because ___.”

## 9. What must be checked for that analysis to be credible?

- [ ] **I have a diagnostic and sensitivity plan tied to the model.**

Check what the model assumes, rather than applying one normality test to every raw column. For a paired t-test, the distribution of differences matters. For linear models, inspect functional form, residual behavior, influence, and variance structure. For counts, assess dispersion and residual patterns. For logistic models, inspect separation and fit. For Cox models, evaluate proportional hazards and whether time origin and censoring are defensible. For clustered analyses, examine the correlation specification and adequacy of independent clusters.

A nonsignificant diagnostic is not proof of an assumption. Nonparametric methods also have assumptions and may target a different quantity. Specify scientifically motivated sensitivity analyses before results when possible; explain changes after fitting instead of hiding them.

**Write:** “I will assess ___ using ___. If it fails materially, the planned response is ___; the resulting estimand would ___.”

## 10. What comparison did I promise to make?

- [ ] **I have declared the primary endpoint, contrasts, tail, and multiplicity family.**

Define the null/reference value and confidence level if inferential testing is needed. Choose a one-sided alternative only with a defensible prespecified directional question, never after seeing the result. Specify which gene tests, subgroup contrasts, endpoints, or time points form a multiplicity family and the appropriate adjustment. An omnibus test and a particular pairwise difference answer different questions.

**Write:** “The primary comparison is ___. The null/reference is ___. The test is ___ sided. The multiplicity family and handling are ___. Other analyses are exploratory because ___.”

## 11. What will I report, and can another researcher repeat it?

- [ ] **I can state the planned table, figure, interpretation, and reproducibility record.**

Report the estimate, direction, units, denominator, uncertainty, and meaningful limitations alongside any p-value. Show group summaries or event counts and missingness. For prediction, report evaluation performance with uncertainty and the population on which it was assessed. Interpret the estimate on its actual scale; statistical significance does not itself establish clinical importance, causality, or useful prediction.

Record protocol version, data provenance, software versions, code revision, configurations, and reproducible commands in the [analysis record](../templates/analysis-record.md). Preserve design variables through cleaning and fitting. Separate prespecified work from exploratory changes.

**Write:** “My main output will be ___, reporting ___ with uncertainty ___. It supports ___ but cannot establish ___. Reproduction requires ___.”

## 12. Write the analysis decision paragraph

Complete this paragraph before execution and review it against your [study protocol](../templates/study-protocol.md):

> Among [population], I will analyze [outcome, type, units, horizon] to estimate [target quantity] for [comparison]. This is a [design] with [independent unit and dependence structure]. The eligible analysis set contains [counts and exclusions], with missingness handled by [strategy and assumptions]. I will use [method], preserving [pairing/clustering/weights/time structure] and adjusting for [prespecified variables and rationale]. I will assess [diagnostics], apply [multiplicity plan], and conduct [sensitivity analyses]. Results will report [estimate, interval, denominator and figure/table]. The main limitation is [design or data constraint].

If key fields remain unresolved, label the result **provisional analysis plan** and state the missing information. Completing the paragraph documents reasoning; it does not prove that the study is valid.

## Worked narrative A: two linked breast tissue specimens per person

“My outcome is a transformed continuous assay measurement in arbitrary units. I want the mean tumor-minus-normal difference among the sampled people. Each person contributes one linked tumor/normal pair; this is an observational paired comparison. After validating IDs and documenting complete pairs, I would analyze within-person differences with a paired t-test if its assumptions suit the target. I would examine those differences and influential observations, report the paired mean difference and confidence interval, and describe missing pairs. An independent two-sample test would discard pairing. This does not estimate a treatment effect.”

**What changes the plan?** Raw RNA-seq counts across thousands of genes call for an assay-aware model with person blocking and a defined multiple-testing family. Several specimens or visits per person require a richer dependence structure. See [molecular characterization](study-designs-and-published-examples.md#sd-01-molecular-characterization-a-cross-sectional-analysis-layer).

## Worked narrative B: is a response count surprising under a benchmark?

“My outcome is response yes/no by a fixed endpoint for each of 80 independent people. For this invented exercise, the question is the probability of at least 36 responses if every person's response probability is 0.35. Under the binomial assumptions, I would calculate the upper tail, rather than compare two sample means.”

\[
X\sim\operatorname{Binomial}(80,0.35),\qquad
P(X\ge36)=\sum_{x=36}^{80}\binom{80}{x}(0.35)^x(0.65)^{80-x}.
\]

The corresponding R expression is `pbinom(35, size = 80, prob = 0.35, lower.tail = FALSE)`. This is a reference calculation, not an executed analysis in this chapter. If the actual question were a prespecified one-sided hypothesis test against 0.35, the same tail supplies its p-value under the simple binomial null. If 0.35 was estimated from another small sample, its uncertainty needs consideration. Loss to follow-up, unequal probabilities, or dependent responses can invalidate this simple model. A single-arm response count cannot by itself establish efficacy relative to an unobserved control.

## Worked narrative C: emergency visits before and after a law

“The outcome is a count and the predictor is the pre/post period. I first need the covered population or person-time, hospital coverage, and timing of the observations. If I have only two annual totals, I can report counts and defensible rates, but cannot estimate a baseline trend or attribute a change to the law. With sufficient repeated observations and a credible comparison series, I would plan a controlled time-series analysis, considering exposure offsets, trend, seasonality, autocorrelation, and dispersion. I would report the modeled change with uncertainty and explain concurrent policy or service changes.”

**What changes the plan?** Repeated patient counts require patient-level dependence handling; varying hospital coverage can undermine the denominator. Compare the [ED worked example](biomedical-statistics-decision-guide.md#e-emergency-department-visits-before-and-after-legislation-year-1-versus-year-2) and the [Norwegian rollout reading](study-designs-and-published-examples.md#sd-06-nonrandomized-rollout-screening-and-mortality-in-norway).

## Worked narrative D: breast cancer prognosis at diagnosis

“My outcome is breast cancer death within a defined horizon, with incomplete follow-up and other-cause death considered. I want individual risk predictions using information available at diagnosis. I would specify a cohort index date, predictor availability, event/censoring definitions, and a validation design that separates people and reflects intended site/time use. I would compare justified survival or competing-risk prediction approaches and assess calibration, discrimination, prediction error, and decision utility. Predictor selection and tuning would stay inside training. This estimates prognosis under observed care; it does not establish which treatment would benefit an individual.”

For a published design comparison, read [QResearch prognostication](study-designs-and-published-examples.md#sd-08-retrospective-cohort-with-a-prognostic-prediction-objective). This narrative proposes a new teaching plan; it does not change the repository's frozen survival experiment.

## References and next use

Use the [nine-paper source register](../06_RESOURCES/Literature/study_design_paper_examples.csv) for the linked study readings and the [methods evidence review](../06_RESOURCES/Literature/BIOSTATISTICS_R_LITERATURE_2021_2026.md) for broader methodological context. Official R references document [t-tests and pairing](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/t.test.html), [Wilcoxon hypotheses](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/wilcox.test.html), [Fisher's conditional test](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/fisher.test.html), and [binomial probabilities](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Binomial.html). Check the documentation for the R version actually used.

Save a study-specific completed paragraph in the protocol, then use the analysis record for execution and deviations. Keep participant records and restricted inputs out of the public notes.
