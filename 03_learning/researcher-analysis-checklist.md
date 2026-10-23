# Choosing a Statistical Analysis: A Clinical Research Guide

Authored by Paul Skeffington · Compiled with OpenAI

[Learning home](README.md) · [Data-type-first decision guide](biomedical-statistics-decision-guide.md) · [Study types and published examples](study-designs-and-published-examples.md) · [Study protocol](../templates/study-protocol.md)

A clinical research question usually begins with a patient problem: Did symptoms improve? Did one treatment produce more responses? Did an injury-prevention policy reduce emergency visits? Choosing an analysis begins by identifying what was measured and how the observations were collected. The test name follows from those decisions. [1](#ref-1), [2](#ref-2)

This chapter follows that sequence from a clinical question to a written analysis plan. It introduces the statistical vocabulary needed to explain a choice to a supervisor, read a methods section, or discuss a paper on rounds. The equations in the worked examples make the reasoning explicit; the clinical question and interpretation remain the starting points.

**Learning objectives.** The reader should be able to classify an outcome; distinguish independent groups from repeated observations; state the quantity being estimated; select a candidate analysis family; and identify the assumptions and reporting requirements that need further review.

**How to read the citations.** Numbered links lead to the reference list. Methods articles support analysis principles, software manuals support the named procedures, and reporting guidelines describe information that a paper should disclose. A reporting checklist does not establish that a design or model is valid. The four worked examples are hypothetical; linked empirical studies are identified separately. Sources were checked on October 23, 2026, using accessible original publications, documentation, and article records. No published analysis was independently reproduced.

## 1. Identify the Outcome: What Was Measured?

The **outcome** is the result the study seeks to describe or explain. Begin with its clinical meaning, units, and coding. Different types of outcome require different kinds of analysis. [1](#ref-1)

| Outcome type | Clinical example | Meaning for analysis |
| --- | --- | --- |
| Continuous | Systolic blood pressure in mmHg | Values lie on a measurement scale; a mean or another distribution summary may be relevant |
| Binary | Infection cleared: yes or no | Each person has one of two outcomes; proportions, risks, or odds may be relevant |
| Nominal categorical | Blood group A, B, AB, or O | Categories have no inherent ranking |
| Ordinal | Mild, moderate, or severe symptoms | Categories have an order, but the distance between grades need not be equal |
| Count | Number of crash-related ED visits in a month | Values are nonnegative integers; exposure time or population may be needed |
| Time to event | Months until cancer recurrence | Both follow-up duration and whether recurrence occurred must be recorded |

The **predictor** is the treatment, exposure, group, or characteristic being related to that outcome. In a study comparing blood pressure between treatment groups, blood pressure is continuous and treatment group is categorical. In a study predicting hypertension from age, hypertension status is binary and age is a numerical predictor. A categorical predictor does not make a continuous or count outcome categorical. [1](#ref-1), [14](#ref-14)

**Clinical checkpoint:** “What is the patient outcome, how is it measured, and which variable defines the comparison?”

## 2. State the Clinical Question and the Quantity of Interest

An **estimand** is the precise quantity the study aims to estimate. In practice, this means specifying whose outcome is being considered, what comparison is intended, and over what period. “Does treatment help?” becomes more useful when expressed as “What is the difference in 30-day recovery proportions between the assigned treatment groups?” Population, outcome, comparison, and timing should be explicit in a trial report. [3](#ref-3)

Several questions can arise from the same dataset:

| Question | Analytical purpose |
| --- | --- |
| What proportion recovered? | Estimate a response proportion and its uncertainty |
| Did recovery differ between groups? | Estimate a between-group contrast and, if planned, test a hypothesis |
| How surprising is this count under a specified recovery probability? | Calculate a probability under a stated model |
| Can baseline findings predict recovery for a new patient? | Develop and evaluate a prediction model |

A **p-value** is the probability, under the specified null model, of a test statistic at least as extreme as the one observed. It is not the probability that a treatment works or that the null hypothesis is true. Prediction is a separate objective and requires evaluation of predictions in data not used to fit or select the model. [18](#ref-18), [26](#ref-26)

**Clinical checkpoint:** “Am I describing patients, comparing groups, calculating a model probability, or predicting an outcome?”

## 3. Establish the Study Design

Study design describes how the observations were obtained. In a cohort, eligible participants are followed from a defined starting point to outcomes. In a case-control study, participants are selected because they have or do not have the outcome, and exposures are compared. A cross-sectional study assesses a sample during a defined period. Existing clinical records can support a retrospective cohort; using old records does not automatically make a study case-control. [2](#ref-2), [19](#ref-19)

In a randomized trial, investigators assign an intervention using a random allocation procedure. This differs from randomly sampling people from a population. Random assignment addresses comparability of treatment groups; it does not ensure that trial participants represent every patient seen in practice. The allocation procedure and analysis population should be reported. [3](#ref-3)

Sampling also changes what a numerical result means. In a case-control sample, the investigator influences the number of cases and controls. The sample's case fraction therefore does not directly estimate population disease risk. An odds ratio and a risk ratio are different measures and should not be used interchangeably. [2](#ref-2), [25](#ref-25)

The [published-paper chapter](study-designs-and-published-examples.md#3-published-paper-examples) provides examples of these designs. Complex surveys, cluster trials, and policy evaluations require additional design information before analysis.

**Clinical checkpoint:** “Why is each participant in this dataset, and was the exposure observed or assigned?”

## 4. Count Patients Separately from Measurements

Observations from different patients may be treated as **independent** when the design supports that assumption; repeated observations from one patient require separate consideration. Twenty patients measured before and after treatment produce forty measurements, but only twenty patient pairs. Those measurements should not be analyzed as if forty unrelated patients had been sampled. Repeated observations from the same person are usually correlated. [4](#ref-4)

For a continuous outcome measured twice in each person, a paired analysis considers the within-person differences. For a binary outcome measured twice, McNemar's method assesses the imbalance between the two kinds of change: negative to positive and positive to negative. An exact approach may be needed when discordant pairs are few; the ordinary R `mcnemar.test` uses a chi-square approximation. [5](#ref-5), [6](#ref-6)

With several visits, a **mixed-effects model** can represent variation between patients alongside within-patient measurements. The chosen approach must match the outcome and question. Specimens within a donor or patients within a hospital introduce related concerns. [4](#ref-4)

**Clinical checkpoint:** “How many different people or independent experimental units are represented, and which observations belong together?”

## 5. Define Follow-up and the Denominator

A **denominator** identifies the amount of observation behind a count or proportion. Ten infections among 100 patients differs from ten among 1,000. For a rate, the denominator may combine people and time: 100 people followed for one year contribute 100 person-years if each completes that year. A count-rate model can include an **offset**, a term that accounts for different amounts of exposure. [14](#ref-14)

**Censoring** means that the exact event time is not observed within available follow-up. A patient who remains recurrence-free through their last visit has contributed information up to that time; they have not necessarily remained recurrence-free forever. Survival methods use event and follow-up information together. [7](#ref-7)

The **time origin** is when follow-up begins, such as diagnosis or randomization. A **competing event** prevents the event of interest from occurring afterward; death from another cause competes with breast cancer death. These choices affect a prognosis analysis and must be defined before fitting the model. [23](#ref-23)

**Clinical checkpoint:** “What is the denominator, when does observation start, and what happens if follow-up ends before the outcome occurs?”

## 6. Assess Missing Data and Feasibility

Before analysis, record the numbers of eligible patients, exclusions, observed outcomes, and patients with missing measurements. Check units, identifiers, and implausible values. These details establish which patients actually contribute to each result. Observational-study reports should explain participant flow, missingness, and analysis populations. [19](#ref-19)

Missing measurements can introduce bias. For example, patients who feel worse may be less likely to attend a follow-up visit. An analysis of attendees alone may then describe a selected group. **Multiple imputation** creates several plausible completed datasets under an explicit model and combines the analyses; it does not recover the unknown values with certainty or remove the need to assess missingness assumptions. [8](#ref-8)

The number of recorded rows does not establish that a complex model is feasible. Few outcomes or very small comparison groups can yield unstable estimates. In logistic regression, **separation** occurs when predictors perfectly distinguish the outcome groups, causing difficulties for ordinary coefficient estimation. [14](#ref-14)

**Clinical checkpoint:** “Who is absent from the analysis, why might their data be missing, and are there enough informative observations for the proposed model?”

## 7. Decide Whether Adjustment or Prediction Is Required

A **confounder** is a variable that can distort an exposure–outcome comparison because of its causal relationships with both. For example, an observed association between a prescribed treatment and poor outcomes may partly reflect that sicker patients were more likely to receive it. Covariate selection should reflect the clinical question and the assumed relationships among variables. [9](#ref-9)

Adding every available variable is not a universal solution. A **mediator** lies on a pathway through which an exposure affects the outcome; adjusting for it can change the question from a total effect to a different contrast. A **collider** is influenced by two other variables; conditioning on it can introduce an association. These are reasons to justify adjustment using a causal diagram and clinical knowledge, rather than p-values alone. [9](#ref-9)

Prediction asks how well a model estimates outcomes for new patients. **Discrimination** measures how well it distinguishes patients with different outcomes; **calibration** measures agreement between predicted probabilities and observed outcomes. In a hypothetical group assigned a 20% risk, calibration would require an observed frequency compatible with that prediction. The area under the receiver operating characteristic (ROC) curve, or AUC, summarizes discrimination, not calibration. [26](#ref-26) Both development and evaluation procedures need transparent reporting. [10](#ref-10)

**Clinical checkpoint:** “Am I estimating an exposure association or predicting risk, and how does that purpose justify the variables and evaluation strategy?”

A **validation** procedure evaluates model predictions beyond the observations used for fitting. All data preparation that learns from outcomes, including selecting predictors, must be incorporated into the development and validation strategy; otherwise the reported performance may be too optimistic. [26](#ref-26)

## 8. Match the Question to an Analysis Family

Table 1 offers starting points after the outcome, design, and observation structure are clear. Each row includes a source for the named procedure or method family. The [full decision guide](biomedical-statistics-decision-guide.md#5-data-type-to-test-reference-common-biomedical-questions) and [practice workbook](statistics-practice-workbook.md) provide further explanation.

**Table 1. Common clinical questions and candidate analyses.**

| Clinical question or outcome | Candidate analysis | Main condition to check | Source |
| --- | --- | --- | --- |
| Mean measurement in two independent groups | Welch t-test; linear model if adjustment is required | Independence, measurement distribution, influential values | [5](#ref-5) |
| Mean change in the same patients at two times | Paired t-test on individual differences | Correct pairing and distribution of differences | [5](#ref-5) |
| Mean measurement across three or more independent groups | ANOVA or Welch ANOVA | Variance assumptions and planned group contrasts | [11](#ref-11) |
| Rank/distribution comparison for numerical or ordered values | Appropriate Wilcoxon or other rank procedure | Pairing, ties, and the quantity the test addresses | [12](#ref-12) |
| Two categorical variables in independent people | Chi-square or Fisher's exact test | Sampling and approximation conditions; effect estimate | [2](#ref-2), [13](#ref-13) |
| Binary outcome with explanatory variables | Logistic regression for an odds-ratio question | Sampling, adjustment, separation, clustering | [14](#ref-14), [25](#ref-25) |
| Binary status before and after in the same patients | McNemar method | Discordant pairs and suitability of approximation | [6](#ref-6) |
| Count of events with unequal exposure | Poisson-rate model; consider alternatives for overdispersion | Exposure denominator, dependence, variance | [14](#ref-14), [16](#ref-16) |
| Time to an event with incomplete follow-up | Kaplan–Meier, log-rank, or a justified survival model | Event definition, censoring, model assumptions | [7](#ref-7), [24](#ref-24) |
| Probability of a specified number of binary responses | Binomial probability calculation under stated assumptions | Fixed trial count, common probability, independence | [21](#ref-21) |
| Accuracy of a diagnostic test | Sensitivity, specificity, predictive values, ROC evaluation | Reference standard, threshold, sampling, paired tests | [20](#ref-20) |
| Future risk for individual patients | Prediction model with appropriate evaluation | Predictor timing, calibration, discrimination, validation | [10](#ref-10), [23](#ref-23) |
| Thousands of gene-level measurements | Assay-appropriate models and multiplicity control | Input scale, biological replication, design | [15](#ref-15) |
| Change after a population policy | Interrupted time series or another justified comparison design | Repeated time points, trends, seasonality, comparison | [16](#ref-16) |

For diagnostic studies, **sensitivity** is the proportion of people with the target condition who test positive; **specificity** is the proportion without it who test negative. Both depend on how the condition and reference standard are defined. [20](#ref-20)

A rank test should not automatically be described as a test of median differences: that interpretation requires additional assumptions about the distributions. Similarly, a significant ANOVA does not identify which particular groups differ; the intended contrasts require their own analysis and multiplicity plan. [12](#ref-12), [11](#ref-11), [17](#ref-17)

## 9. Examine the Assumptions

An **assumption** is a condition under which the intended model interpretation or inference is justified. The relevant condition depends on the procedure. For a paired t-test, assess the differences between paired observations. A Cox model also requires consideration of its proportional-hazards structure: the modeled hazard ratio is assumed constant over time unless a time-varying effect is specified. A **hazard** is an instantaneous event rate among people still at risk; a hazard ratio is not a fixed-time risk ratio. [5](#ref-5), [24](#ref-24)

A **residual** is a measure of discrepancy between an observed value and what the model predicts. In a count time series, **overdispersion** means greater variation than the Poisson variance assumption allows; **autocorrelation** means neighboring observations remain related over time. These are different problems and need separate assessment. [16](#ref-16)

A **sensitivity analysis** asks whether a conclusion changes under another defensible assumption or analytical choice. It is useful for issues such as missing-data assumptions and policy timing. It should address a scientific concern, rather than search for a favorable p-value. [8](#ref-8), [16](#ref-16), [18](#ref-18)

**Clinical checkpoint:** “Which conditions does this analysis rely on, and would a reasonable alternative change its interpretation?”

## 10. Prespecify the Comparison and Address Multiple Testing

The primary outcome and comparison should be stated before reviewing the study results. A **one-sided** test concerns a specified direction; a **two-sided** test allows departures in either direction. Selecting a direction after seeing the data changes the testing procedure. [3](#ref-3), [5](#ref-5)

Testing many outcomes, genes, subgroups, or time points creates opportunities for false-positive findings. The **multiplicity family** is the set of related tests for which error control is intended. A correction such as Bonferroni addresses one form of this problem, but the appropriate strategy depends on the study objective; it is not a universal correction across every analysis in a project. [17](#ref-17)

**Clinical checkpoint:** “Which result was primary, and how many related chances were there to obtain a positive finding?”

## 11. Interpret the Estimate and Report the Study Transparently

Interpret the magnitude and uncertainty, not only whether p is below a threshold. A small p-value does not measure clinical importance. A **95% confidence interval** comes from a procedure designed to include the fixed population quantity in 95% of repeated samples under its assumptions. It is an interval for an estimate, not a range containing 95% of individual patients. [27](#ref-27) It does not remove bias from the design. [19](#ref-19)

For a hypothetical example with complete follow-up, 20 events among 100 patients versus 10 among 100 give risks of 20% and 10%. The risk ratio is 2 and the risk difference is 10 percentage points. The odds ratio is (20/80)/(10/90) = 2.25. This invented arithmetic illustrates why an odds ratio is not interchangeable with a risk ratio. [25](#ref-25)

Reports should identify the analyzed population, exclusions, missingness, model, estimates, and uncertainty. Suitable reporting frameworks include CONSORT for randomized trials, STROBE for observational research, STARD for diagnostic accuracy, and TRIPOD+AI for prediction. These frameworks support transparency; they do not replace evaluation of bias or method suitability. [3](#ref-3), [19](#ref-19), [20](#ref-20), [10](#ref-10)

The [analysis record](../templates/analysis-record.md) provides a place to record code revision, data provenance, software versions, commands, and deviations from the plan.

## 12. Write the Analysis Rationale

A concise analysis rationale should connect the clinical question to the method. The following is a teaching structure to adapt in the [study protocol](../templates/study-protocol.md):

> The study will estimate [quantity] for [comparison] among [population], using [outcome, units, and follow-up period]. The design is [study type], with [independent units and repeated or clustered observations]. Eligibility and missing-data rules define [analysis population]. The primary analysis will use [method] because [reason linked to outcome, design, and question]. It will account for [pairing, clustering, exposure, or censoring] and adjust for [variables and clinical rationale]. Results will include [estimate and interval], with [diagnostics, sensitivity analyses, and multiplicity plan]. Interpretation is limited by [main design or data concern].

Missing information should remain visible in a provisional plan. Naming a test does not resolve an unknown denominator, missing linkage, or an unsuitable comparison group.

## Worked Example A. Paired Molecular Measurements

Consider a hypothetical study in which each patient contributes one tumor specimen and one matched normal specimen. A laboratory marker is measured on a continuous, transformed scale. The question is whether the mean marker value differs between the two tissues within patients. The patient supplies the pair; the two specimens are not independent people. [4](#ref-4), [5](#ref-5)

For patient i, subtract the normal-tissue value from the tumor value:

\[
D_i=Y_{i,\mathrm{tumor}}-Y_{i,\mathrm{normal}},\qquad
\Delta=E(D_i).
\]

Here D_i is one patient's difference, and Delta is the population mean difference being estimated. When patients are independent and the differences support the intended inference, a paired t-test is a candidate analysis. The report gives the number of complete pairs, the mean difference, and its confidence interval. A positive difference means a higher average value in tumor tissue on the specified scale. It does not establish a treatment benefit. [5](#ref-5)

If the input instead consists of raw RNA-seq counts for thousands of genes, the problem requires an assay-appropriate model, biological replication, and a multiple-testing strategy. A simple t-test applied to every raw count column is not the same analysis. DESeq2 provides a published example of modeling RNA-seq counts. [15](#ref-15) The [molecular characterization reading](study-designs-and-published-examples.md#sd-01-molecular-characterization-a-cross-sectional-analysis-layer) supplies related breast cancer context.

## Worked Example B. A Binomial Response Probability

Suppose that 80 independent participants are assessed for a binary response at a common endpoint. Under a specified model in which every participant has response probability 0.35, the number of responses X follows a binomial distribution. The probability of observing at least 36 responses is given by the binomial upper tail. [21](#ref-21)

\[
X\sim\operatorname{Binomial}(80,0.35),\qquad
P(X\ge36)=\sum_{x=36}^{80}\binom{80}{x}(0.35)^x(0.65)^{80-x}.
\]

The corresponding R expression is `pbinom(35, size = 80, prob = 0.35, lower.tail = FALSE)`. The argument 35 is required because the upper-tail convention calculates P(X > 35), which equals P(X ≥ 36) for an integer-valued variable. This is a documented reference expression; no numerical execution is claimed in this chapter. [21](#ref-21)

This calculation answers a probability question under a stipulated model. Under a prespecified one-sided test of the simple null p = 0.35 against p > 0.35, the same upper tail supplies the p-value. [21](#ref-21) Estimation of the response probability is a separate task requiring an estimate and interval. If the reference probability was estimated from another sample, its uncertainty also requires consideration. Incomplete follow-up, dependence, or unequal response probabilities can invalidate the simple binomial specification. An observed response count in a single treatment group does not by itself establish efficacy against an unobserved control. [2](#ref-2)

## Worked Example C. Emergency Visits Following a Texting-While-Driving Prohibition

### Research question and outcome definition

Suppose that a jurisdiction implements a prohibition on texting while driving. A researcher seeks to determine whether implementation is associated with a change in emergency-department visits for motor-vehicle-crash injuries. The primary outcome is the number of qualifying ED encounters during a specified observation period. It is a **quantitative discrete count**. The policy indicator, coded as before or after implementation, is a **qualitative binary predictor**. Its categorical form does not make the visit count a categorical outcome. [1](#ref-1), [14](#ref-14)

The outcome definition should specify the injury codes, participating hospitals, inclusion of drivers and other road users, and handling of transfers or repeat encounters. All-cause ED visits answer a broader utilization question and may obscure changes in crash-related injuries. Crash-related visits also do not establish that texting caused each individual crash. The policy question concerns outcomes following a population-level intervention. This outcome definition is part of the hypothetical protocol, not a claim about measured compliance.

### Study design and observation unit

If the available data consist of one annual count before the law and one afterward, the design is an uncontrolled before-and-after comparison. The observations are jurisdiction-years, rather than two groups of independently randomized patients. The analysis can describe the observed change, but it cannot separate policy implementation from an existing trend or another change occurring at the same time. [16](#ref-16)

A more informative design uses repeated monthly counts over adequate periods before and after implementation. With one jurisdiction, this permits an **interrupted time-series analysis**: the observed trend after a policy is compared with the trend expected from the period before it. [16](#ref-16) A comparable jurisdiction without the same policy change may provide a control series, subject to assessment of comparability, spillovers, and concurrent policies. The relevant exposure date is the effective or enforcement date specified in the protocol; an enactment date alone may not correspond to a change in driving behavior. Anticipation, delayed enforcement, and gradual adoption require explicit consideration. [16](#ref-16)

### Denominator and descriptive comparison

The denominator determines the rate being estimated. Visits per resident-year describe population injury burden; visits per vehicle-mile traveled describe burden relative to driving exposure. These quantities are not interchangeable. A decline in traffic volume can reduce visit counts without a corresponding decline in injury risk per mile. The numerator and denominator must refer to compatible geography, road users, hospital coverage, and time periods. These denominator choices define different proposed questions; a count model must represent the chosen exposure. [14](#ref-14), [16](#ref-16)

For each period, the researcher first reports the count, exposure denominator, rate, and missingness or coverage changes. The ratio of the post-policy rate to the pre-policy rate is a descriptive rate ratio. Even if a Poisson comparison supplies a confidence interval, two annual observations provide no residual information with which to assess trend, seasonality, serial dependence, or dispersion. [16](#ref-16)

### Candidate model for a monthly series: an optional mathematical extension

The clinical idea is to separate an immediate change in the visit rate from a change in its subsequent trend. The equation below formalizes that proposed comparison. It is a teaching specification informed by segmented-regression methods, not an executed fit. [16](#ref-16)

For a sufficiently informative single-jurisdiction monthly series, let Y_t denote crash-related ED encounters, E_t a positive exposure denominator, and t elapsed months. Let I_t equal one from the prespecified implementation month onward and zero beforehand; let S_t equal zero before implementation and count months since implementation, beginning at zero in the first intervention month. A candidate segmented count-model mean specification is

\[
\log(\mu_t)=\log(E_t)+\beta_0+\beta_1t+\beta_2I_t
+\beta_3S_t+f_{\mathrm{season}}(t)+\boldsymbol{\gamma}^{\mathsf T}\mathbf Z_t,
\qquad \mu_t=E(Y_t).
\]

The exposure offset represents the chosen denominator. The three main terms answer distinct questions:

| Model term | Plain-language interpretation |
| --- | --- |
| beta_1 | How was the visit rate changing before implementation? |
| beta_2 | Was there an immediate change when implementation began? |
| beta_3 | Did the subsequent trend differ from the earlier trend? |

The coefficients are expressed on the log-rate scale. Seasonal terms and justified covariates Z_t address specified temporal features and measured alternative explanations. A Poisson variance assumption requires assessment; overdispersion may motivate a negative-binomial or another justified count model. Serial correlation requires a separate treatment: changing the count distribution alone does not account for temporal dependence. [14](#ref-14), [16](#ref-16)

Under this specification, the modeled rate ratio at m months after implementation, relative to continuation of the specified pre-policy trend with other terms held fixed, is exp(beta_2 + beta_3 m). This is a model-based contrast. Its interpretation depends on the trend specification and assumptions about what would have occurred without the policy. That unobserved alternative is called the **counterfactual**. [16](#ref-16) A controlled interrupted time series requires additional group and interaction terms; the single-series equation above is not a complete controlled analysis.

### Diagnostics and interpretation

The researcher examines plotted counts and rates, pre-policy trends, seasonal patterns, dispersion, residual dependence, and influential months. Relevant alternative explanations include changes in traffic volume, hospital participation, injury coding, weather, road-safety measures, and access to emergency care. Prespecified sensitivity analyses may vary the implementation window, examine a justified transition period, or assess alternative trend specifications. A decline in aggregate visits does not by itself establish individual compliance or identify the contribution of enforcement. [16](#ref-16)

The resulting methods statement might read: “Monthly crash-related ED encounters will be analyzed using a segmented count-rate model with a prespecified exposure denominator. The analysis will estimate immediate and subsequent trend changes following implementation of the texting prohibition, while addressing seasonal variation, measured temporal covariates, overdispersion, and serial dependence. Results will include rate contrasts with confidence intervals, diagnostic findings, and sensitivity analyses. Policy attribution will remain conditional on the credibility of the comparison and the absence of unaccounted concurrent changes.”

### Connection to published research

Ferdinand, Aftab, and Akinlotan (2019) examined texting bans and crash-related ED visits in 16 US states during 2007–2014: [Texting-While-Driving Bans and Motor Vehicle Crash–Related Emergency Department Visits in 16 US States: 2007–2014](https://pubmed.ncbi.nlm.nih.gov/30896993/). The primary-article record provides a directly related empirical reading. [22](#ref-22) The monthly segmented model above is a proposed teaching specification, not a reconstruction of that paper's analysis. The clinical question is the same broad policy question, but neither an observed effect size nor execution of this hypothetical analysis is asserted here. The [count/rate example](biomedical-statistics-decision-guide.md#e-emergency-department-visits-before-and-after-legislation-year-1-versus-year-2) provides complementary introductory arithmetic.

## Worked Example D. Prognostic Prediction

Consider a cohort used to predict breast cancer death within ten years of diagnosis. This is a **prognostic** question: what is likely to happen to a patient? It differs from a **diagnostic** question about whether disease is currently present. The model may need to account for incomplete follow-up and death from another cause. The QResearch study provides a published example of comparing approaches to breast cancer prognosis. [23](#ref-23)

The protocol specifies when prediction occurs, which patients are eligible, and which measurements are available at that time. Evaluation considers whether predictions distinguish outcomes, agree with observed risks, and support useful decisions at relevant thresholds. Model selection and evaluation must be described so that the reader can assess whether performance was tested beyond the data used in development. [10](#ref-10)

A prediction such as “10-year risk under observed care” does not establish how changing a patient's treatment would change that risk. Causal treatment questions require additional design and assumptions. [9](#ref-9) This hypothetical example does not modify the repository's frozen survival experiment.

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

**Reference scope.** Foundational teaching sources are used alongside newer methods and reporting guidance. References 3, 10, 19, and 20 are reporting guidelines, not evidence that a particular analysis is valid. References to R document procedure behavior; the installed version must be checked before execution. The linked BMJ *Statistics at Square One* pages are an older edition and are used for elementary concepts, not as the sole authority for current software defaults. [5](#ref-5), [11](#ref-11) give the corresponding Welch procedures. The policy tutorial has a linked correction; the time-since-intervention variable in this chapter is explicitly defined to avoid ambiguity.

<a id="ref-1"></a>

**1.** [The BMJ. *Statistics at Square One*: Data display and summary.](https://www.bmj.com/about-bmj/resources-readers/publications/statistics-square-one/1-data-display-and-summary) Foundational teaching: measurement types and summaries.

<a id="ref-2"></a>

**2.** [The BMJ. *Statistics at Square One*: Study design and choosing a statistical test.](https://www.bmj.com/about-bmj/resources-readers/publications/statistics-square-one/13-study-design-and-choosing-statisti) Foundational teaching: design, comparisons, and analysis choice.

<a id="ref-3"></a>

**3.** [Hopewell S, et al. CONSORT 2025 statement: updated guideline for reporting randomised trials. *BMJ*. 2025;389:e081123.](https://doi.org/10.1136/bmj-2024-081123) Reporting guideline: trial objectives, outcomes, allocation, and analysis.

<a id="ref-4"></a>

**4.** [Muhammad LN. Guidelines for repeated measures statistical analysis approaches with basic science research considerations. *J Clin Invest*. 2023;133:e171058.](https://doi.org/10.1172/JCI171058) Methods viewpoint: correlated repeated measurements and mixed models.

<a id="ref-5"></a>

**5.** [R documentation. Student's t-Test: `t.test`.](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/t.test.html) Official procedure reference: independent and paired means; Welch option.

<a id="ref-6"></a>

**6.** [R documentation. McNemar's Chi-squared Test for Count Data: `mcnemar.test`.](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/mcnemar.test.html) Official procedure reference: paired categorical table and chi-square approximation.

<a id="ref-7"></a>

**7.** [Bland JM, Altman DG. Survival probabilities (the Kaplan–Meier method). *BMJ*. 1998;317:1572.](https://doi.org/10.1136/bmj.317.7172.1572) Teaching article: survival estimation with censoring.

<a id="ref-8"></a>

**8.** [Sterne JAC, et al. Multiple imputation for missing data in epidemiological and clinical research: potential and pitfalls. *BMJ*. 2009;338:b2393.](https://doi.org/10.1136/bmj.b2393) Methods article: missing-data assumptions and imputation limitations.

<a id="ref-9"></a>

**9.** [Greenland S, Pearl J, Robins JM. Causal diagrams for epidemiologic research. *Epidemiology*. 1999;10:37–48.](https://pubmed.ncbi.nlm.nih.gov/9888278/) Methods article: causal structure and adjustment.

<a id="ref-10"></a>

**10.** [Collins GS, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. *BMJ*. 2024;385:e078378.](https://doi.org/10.1136/bmj-2023-078378) Reporting guideline: prediction development, evaluation, and performance.

<a id="ref-11"></a>

**11.** [R documentation. Test for Equal Means in a One-Way Layout: `oneway.test`.](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/oneway.test.html) Official procedure reference: ordinary and Welch one-way comparisons.

<a id="ref-12"></a>

**12.** [R documentation. Wilcoxon Rank Sum and Signed Rank Tests: `wilcox.test`.](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/wilcox.test.html) Official procedure reference: rank hypotheses, pairing, and assumptions.

<a id="ref-13"></a>

**13.** [R documentation. Fisher's Exact Test for Count Data: `fisher.test`.](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/fisher.test.html) Official procedure reference: conditional contingency-table inference.

<a id="ref-14"></a>

**14.** [R documentation. Fitting Generalized Linear Models: `glm`.](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/glm.html) Official procedure reference: outcome families, offsets, and fitting considerations.

<a id="ref-15"></a>

**15.** [Love MI, Huber W, Anders S. Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biol*. 2014;15:550.](https://doi.org/10.1186/s13059-014-0550-8) Primary methods/software paper: RNA-seq count modeling and inference.

<a id="ref-16"></a>

**16.** [Lopez Bernal J, Cummins S, Gasparrini A. Interrupted time series regression for the evaluation of public health interventions: a tutorial. *Int J Epidemiol*. 2017;46:348–355.](https://doi.org/10.1093/ije/dyw098) Methods tutorial: intervention timing, segmented trends, seasonality, dispersion, and autocorrelation. See also the [2020 corrigendum](https://doi.org/10.1093/ije/dyaa118).

<a id="ref-17"></a>

**17.** [Bland JM, Altman DG. Multiple significance tests: the Bonferroni method. *BMJ*. 1995;310:170.](https://doi.org/10.1136/bmj.310.6973.170) Teaching article: multiple comparisons and error control.

<a id="ref-18"></a>

**18.** [Wasserstein RL, Lazar NA. The ASA statement on p-values: context, process, and purpose. *Am Stat*. 2016;70:129–133.](https://doi.org/10.1080/00031305.2016.1154108) Statistical statement: interpretation and limits of p-values.

<a id="ref-19"></a>

**19.** [Vandenbroucke JP, et al. Strengthening the Reporting of Observational Studies in Epidemiology (STROBE): explanation and elaboration. *PLoS Med*. 2007;4:e297.](https://doi.org/10.1371/journal.pmed.0040297) Reporting guidance: design, variables, bias, participants, missingness, and estimates.

<a id="ref-20"></a>

**20.** [Bossuyt PM, et al. STARD 2015: an updated list of essential items for reporting diagnostic accuracy studies. *BMJ*. 2015;351:h5527.](https://doi.org/10.1136/bmj.h5527) Reporting guideline: index tests, reference standards, thresholds, and accuracy.

<a id="ref-21"></a>

**21.** [R documentation. The Binomial Distribution: `Binomial`.](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Binomial.html) Official probability reference: binomial mass and upper-tail convention.

<a id="ref-22"></a>

**22.** [Ferdinand AO, Aftab A, Akinlotan MA. Texting-while-driving bans and motor vehicle crash-related emergency department visits in 16 US states: 2007–2014. *Am J Public Health*. 2019.](https://pubmed.ncbi.nlm.nih.gov/30896993/) Primary empirical reading: the related policy question, not a replay of the teaching model.

<a id="ref-23"></a>

**23.** [Clift AK, et al. Development and internal-external validation of statistical and machine learning models for breast cancer prognostication: cohort study. *BMJ*. 2023;381:e073800.](https://doi.org/10.1136/bmj-2022-073800) Primary empirical reading: prognosis and evaluation of alternative models.

<a id="ref-24"></a>

**24.** [R survival documentation. Fit Proportional Hazards Regression Model: `coxph`.](https://stat.ethz.ch/R-manual/R-devel/library/survival/html/coxph.html) Official model reference: Cox survival specification and extensions.

<a id="ref-25"></a>

**25.** [Bland JM, Altman DG. The odds ratio. *BMJ*. 2000;320:1468.](https://doi.org/10.1136/bmj.320.7247.1468) Teaching article: odds ratios and distinction from relative risk.

<a id="ref-26"></a>

**26.** [Developing clinical prediction models: a step-by-step guide. *BMJ*. 2024;386:e078276.](https://doi.org/10.1136/bmj-2023-078276) Methods guide: model development, performance assessment, validation, and clinical usefulness.

<a id="ref-27"></a>

**27.** [The BMJ. *Statistics at Square One*: Statements of probability and confidence intervals.](https://www.bmj.com/about-bmj/resources-readers/publications/statistics-square-one/4-statements-probability-and-confiden) Foundational teaching: confidence intervals versus individual reference ranges.

The [nine-paper source register](../06_RESOURCES/Literature/study_design_paper_examples.csv) provides the separate design-reading collection. The completed study rationale belongs in the protocol; execution details and deviations belong in the [analysis record](../templates/analysis-record.md). Participant records and restricted inputs remain outside the public notes.
