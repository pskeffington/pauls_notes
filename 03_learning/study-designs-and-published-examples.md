# Study types: reading the design in a real paper

Authored by Paul Skeffington · Compiled with OpenAI

[Learning home](README.md) · [Data-type-first test guide](biomedical-statistics-decision-guide.md) · [Probability and sampling](probability-and-design.md) · [Study protocol](../templates/study-protocol.md)

**Source review: 2026-10-23.** These are published-paper reading examples, with original article links and a [searchable source register](../06_RESOURCES/Literature/study_design_paper_examples.csv). Recent examples sit alongside older studies that make a design distinction clear. This is a curated teaching collection, not a systematic review or a reproduction of the authors' results. No participant data were downloaded or analyzed.

## 1. Describe the measurements, then describe how the study obtained them

Keep the [test guide's data-type-first route](biomedical-statistics-decision-guide.md#1-first-classify-the-data): identify the outcome as continuous, categorical, a count, or time plus event status. **Before choosing a test**, determine how participants entered the study and how observations are related. A binary cancer outcome can occur in a trial, case-control sample, cohort, or diagnostic evaluation; those designs support different estimates.

Write a design sentence using these separate dimensions:

| Dimension | Ask | Possible answer |
| --- | --- | --- |
| Purpose | What is being estimated? | Description, exposure association, treatment effect, diagnostic accuracy, future risk |
| Assignment | Did investigators assign the exposure? | Observational; randomized intervention; nonrandomized intervention |
| Sampling | Why is this person in the dataset? | Population survey, eligible cohort, disease case/control, selected clinic sample |
| Timing | Were measurements made at one period or over follow-up? | Cross-sectional, longitudinal; prospective collection or reconstruction from existing records |
| Unit | What was sampled, randomized, measured, and analyzed? | Person, specimen, visit, hospital, hospital-period; these can differ |
| Comparator | What supplies the comparison? | Concurrent control, historical control, self-comparison, external reference, none |

**Prospective does not mean randomized. Retrospective does not mean case-control.** A cohort can be reconstructed from historical records. A case-control analysis can use specimens collected prospectively before disease. A prediction study is an objective layered on a sampling design.

**Random sampling** concerns representation of a population. **Random allocation** concerns intervention assignment and comparability of trial groups. One does not imply the other. Blinding, allocation concealment, and probability sampling also describe different safeguards.

## 2. Recognize the main designs

| Study type | What is selected or followed? | Useful estimate or analysis family | Main interpretation trap |
| --- | --- | --- | --- |
| Case report / case series | One or several selected clinical cases; usually no designed comparison group | Clinical description, timelines, observed counts | Cannot estimate comparative efficacy or population incidence from selected cases |
| Cross-sectional | A defined sample assessed in a period | Prevalence, distributions, prevalence associations; survey-aware models if needed | Exposure/outcome order and incidence are usually unresolved |
| Case-control | Participants selected by outcome status, then exposures compared | Odds ratios; logistic models; conditional logistic methods for appropriate matched sampling | Sample case fraction is not population disease risk |
| Cohort | Eligible people observed from an index date to outcomes | Risks, rates, survival; model depends on endpoint and follow-up | Time order alone does not remove confounding |
| Individually randomized parallel trial | People allocated to intervention groups | Prespecified intention-to-treat contrasts and endpoint-specific models | Adherence-based subgroup comparisons can lose randomization's protection |
| Cluster randomized trial | Groups allocated, with outcomes measured within them | Cluster-aware analysis with allocation unit and time structure retained | Patient count is not the count of independent randomized units |
| Crossover trial | Units receive intervention sequences in different periods | Sequence/period-aware contrasts; assess carryover and washout | A cluster crossover need not expose the same patients to both regimens |
| Nonrandomized policy / service evaluation | Outcomes around a policy change, preferably with a credible comparison | Controlled before/after, interrupted time series, or justified difference-in-differences | A temporal change can reflect secular trends or concurrent interventions |
| Diagnostic accuracy study | Index test compared with a defined reference standard | Sensitivity, specificity, predictive values, ROC; account for paired readers/tests | Accuracy does not establish improved patient outcomes |
| Prognostic prediction study | Predictors at a defined decision time linked to later outcomes | Discrimination, calibration, prediction error, utility; proper validation | Predictive importance is not a causal treatment effect |
| Ecological study | Groups such as counties or countries | Group-level associations with appropriate denominators | Group association does not identify an individual's association |
| Systematic review / meta-analysis | Eligible studies; optionally their participant data | Structured synthesis; comparable effects with uncertainty and heterogeneity | Pooling cannot repair bias in the contributing studies |

These labels overlap. A systematic review need not contain a meta-analysis; a meta-analysis needs a defensible identification and selection process. Individual-participant-data (IPD) synthesis retains study structure rather than treating all participants as one newly randomized trial. The nine paper examples below cover selected rows, not every design variant.

## 3. Published-paper examples

In each example, **Paper** identifies facts reported by the article. **Reading lesson** is our methodological interpretation. Follow the named location in the original before transferring an analysis to a new study. A method family is not a complete statistical analysis plan.

### SD-01. Molecular characterization: a cross-sectional analysis layer

**Paper:** The Cancer Genome Atlas Network (2012), [doi:10.1038/nature11412](https://doi.org/10.1038/nature11412); [author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC3465532/). The study characterized primary breast cancers from **825 patients** using multiple molecular platforms and integrated subtype analyses. Read the opening results, platform descriptions, and Figure 2.

**Reading lesson:** Classify the molecular snapshot as observational characterization, rather than a randomized treatment comparison. This describes an analysis layer, not every analysis in the publication. The person, specimen, and platform are distinct units; assay-specific denominators may differ. Cross-platform concordance does not demonstrate longitudinal tumor evolution or treatment response.

**Analysis connection:** Explore continuous molecular features and categorical subtype labels with assay-aware methods. The study's full workflow is not one t-test. This connects to the [breast cancer companion](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md); the publication does not authorize new participant-data use here.

### SD-02. Case-control sampling: inherited variants and breast cancer

**Paper:** Hu et al. (2021), [CARRIERS](https://doi.org/10.1056/NEJMoa2005936); [author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC8127622/). The population-based case-control analysis included **32,247 cases and 32,544 controls**, sequencing 28 predisposition genes. Logistic regression adjusted for study, age, first-degree family history, and race or ethnic group. Read Methods: Study Population and Statistical Analysis.

**Reading lesson:** Disease status supplies the sampling contrast. The proportion of cases among sampled women is not an estimate of population breast cancer prevalence. A variant odds ratio is not itself lifetime penetrance, an absolute risk, or a risk ratio. Matching, when present in another study, must be represented in the analysis.

**Analysis connection:** Binary outcome plus selected cases/controls leads to an odds-ratio question, with covariates and sampling reviewed before fitting logistic regression.

### SD-03. Prospective cohort: exposure before disease transitions

**Paper:** Cordova et al. (2023), [EPIC multimorbidity analysis](https://doi.org/10.1016/j.lanepe.2023.100771); [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10730313/). The cohort included **266,666 participants** initially free of cancer, cardiovascular disease, and type 2 diabetes. Baseline diet preceded follow-up. Multistate Cox models estimated cause-specific hazard ratios for disease transitions. Read Methods: Study Population and Statistical Analysis.

**Reading lesson:** Recruitment was not based on already having the eventual outcome. Longitudinal follow-up permits a temporal association, while self-reported exposure, confounding, and selection remain concerns. Multiple diseases create transitions between states rather than one interchangeable binary endpoint.

**Analysis connection:** State the event, risk set, time origin, and competing transitions before using survival analysis. A hazard ratio is not an absolute probability of developing two diseases.

### SD-04. Individually randomized parallel trial: treatment and event-free survival

**Paper:** Schmid et al. (2022), [KEYNOTE-522 event-free survival](https://doi.org/10.1056/NEJMoa2112651). **1,174 patients** with stage II/III triple-negative breast cancer were randomized 2:1 to pembrolizumab or placebo with chemotherapy, followed by the assigned adjuvant treatment. The article used Kaplan–Meier estimates, a stratified log-rank comparison, and a stratified Cox model. Read Methods: Trial Design, End Points, and Statistical Analysis.

**Reading lesson:** Randomization is at the patient level. The comparison concerns the assigned treatment strategy; it does not isolate the contribution of each treatment phase. Pathological complete response is a binary endpoint, whereas event-free survival includes time and event status.

**Analysis connection:** Preserve assignment, stratification, endpoint definition, and censoring. Do not substitute a complete-case responder proportion for the survival analysis or equate a hazard ratio with a risk reduction at a fixed time.

### SD-05. Cluster randomized multiple crossover: ICU fluid policy

**Paper:** Semler et al. (2018), [SMART](https://doi.org/10.1056/NEJMoa1711584); [author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC5846085/). The trial included **15,802 adults in five ICUs**. Units alternated fluid policy by month under randomized sequences. The primary binary composite was analyzed with a generalized linear mixed-effects model. Read Methods: Randomization and Statistical Analysis, plus the supplementary model specification.

**Reading lesson:** The allocation structure is ICU and period; the outcome is patient-level. “Crossover” describes unit policy switching, not necessarily the same patient receiving both interventions. Unit, calendar period, and repeated admissions need consideration. An ordinary patient-level Fisher test would discard that structure.

**Analysis connection:** A binary endpoint does not automatically imply an independent 2×2 test. Preserve cluster/time information and distinguish conditional from marginal odds ratios.

### SD-06. Nonrandomized rollout: screening and mortality in Norway

**Paper:** Kalager et al. (2010), [Norwegian mammography evaluation](https://doi.org/10.1056/NEJMoa1000727); [abstract](https://pubmed.ncbi.nlm.nih.gov/20860502/). The investigators compared counties with and without screening availability during gradual implementation, with corresponding historical groups. Read Methods: Study Groups and Figure 1; the results report mortality rates and rate ratios.

**Reading lesson:** This is an observational rollout comparison with historical controls. “Natural experiment” is a teaching characterization of the policy setting; counties were not randomized. Contemporary and historical comparisons help address secular change but cannot guarantee that screening alone explains the difference. A simple Year 1/Year 2 count comparison lacks these comparisons.

**Analysis connection:** Review denominators, age/calendar-time comparability, and changes in treatment. Do not relabel this as an executed segmented interrupted time-series model. See the [ED policy example](biomedical-statistics-decision-guide.md#e-emergency-department-visits-before-and-after-legislation-year-1-versus-year-2).

### SD-07. Retrospective diagnostic AI evaluation: mammography readers

**Paper:** McKinney et al. (2020), [international AI screening evaluation](https://doi.org/10.1038/s41586-019-1799-6). The study assessed retrospective UK and US datasets, including an enriched US sample, and a six-radiologist reader study. It reported false-positive/false-negative comparisons and ROC performance. Read the abstract, Figures 2–3, Supplementary Methods, and [2020 addendum](https://doi.org/10.1038/s41586-020-2679-9).

**Reading lesson:** This is diagnostic performance evaluation, not a randomized trial of patient benefit. Enrichment changes case mix and predictive-value interpretation. Correlated readings require reader/case-aware comparisons. Follow-up windows and the reference definition determine what counts as a correct prediction.

**Analysis connection:** Compare paired predictions at declared thresholds, inspect sensitivity/specificity, and review transportability. A reader-study AUC does not establish mortality benefit or authorize clinical deployment. Do not imply that the complete training code or participant datasets are openly reproducible.

### SD-08. Retrospective cohort with a prognostic prediction objective

**Paper:** Clift et al. (2023), [QResearch breast cancer prognostication](https://doi.org/10.1136/bmj-2022-073800); [full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC10170264/). Linked records identified women diagnosed with invasive breast cancer during 2000–2020. The study compared Cox, competing-risk, XGBoost, and neural-network approaches for 10-year breast cancer mortality, using internal-external cross-validation and discrimination/calibration assessment. Read Methods: Outcomes, Model Development, and Model Validation.

**Reading lesson:** “Retrospective cohort” describes the record-based longitudinal design; “prediction” describes its aim. Predictors must be available at the intended prediction time. Other-cause death matters when predicting breast cancer mortality. Internal-external validation is not a trial of model-guided care.

**Analysis connection:** Assess calibration and clinical utility alongside discrimination; preserve grouping during validation and fit preprocessing within training data. A highly predictive treatment variable is not an estimated treatment benefit.

### SD-09. Individual-participant-data meta-analysis of randomized trials

**Paper:** EBCTCG (2015), [aromatase inhibitors versus tamoxifen](https://doi.org/10.1016/S0140-6736(15)61074-1); [abstract](https://pubmed.ncbi.nlm.nih.gov/26211827/). The analysis used individual data from **31,920 postmenopausal women** with ER-positive early breast cancer across randomized endocrine-treatment comparisons. Read Methods and the separate treatment schedules in the results.

**Reading lesson:** The synthesis is secondary research built from primary randomized trials. IPD allows harmonized outcomes and subgroup questions but does not erase trial boundaries, treatment schedules, missingness, or selective availability. Repeated publications from one trial must not become independent studies in a synthesis.

**Analysis connection:** Retain within-trial randomized comparisons and examine which treatment periods an estimate describes. Do not pool all rows into an unstratified comparison or average published p-values. A meta-analysis does not make results applicable to every cancer population.

## 4. How design changes an otherwise similar calculation

These formulas are generic teaching relationships, not reconstructions of the nine papers.

For a complete, independently sampled cohort observed over a common horizon without censoring, let exposed cases/noncases be a/b and unexposed cases/noncases be c/d:

\[
R_1=\frac{a}{a+b},\qquad R_0=\frac{c}{c+d},\qquad
RR=\frac{R_1}{R_0},\qquad RD=R_1-R_0.
\]

With case-control sampling, the investigator generally fixes or influences the number of cases relative to controls. The same-looking table can support a sampling-appropriate **odds ratio**,

\[
OR=\frac{ad}{bc},
\]

but its row fractions do not directly recover population incidence. Under suitable incidence-density sampling, the odds ratio estimates an incidence-rate ratio without a rare-disease requirement; do not apply that result to every control-sampling scheme. Zero cells require appropriate inference rather than blind division.

For event counts with measured follow-up, use **events/person-time**. For censored event times, use methods that represent censoring. A hazard ratio compares instantaneous hazards under the model; it is neither an odds ratio nor generally a fixed-horizon risk ratio.

For a diagnostic test,

\[
\mathrm{Sensitivity}=\frac{TP}{TP+FN},\qquad
\mathrm{Specificity}=\frac{TN}{TN+FP},\qquad
\mathrm{PPV}=\frac{TP}{TP+FP}.
\]

Check the reference standard, verification process, and sampling. Predictive values depend on prevalence; sensitivity and specificity can also change with disease spectrum and setting. Two tests applied to the same people require their paired outcomes, not independent-group uncertainty calculations.

## 5. Common variants that require another design check

- **Nested case-control:** Cases and sampled controls arise within a defined cohort. Identify the control risk set and sampling dates; a prospectively stored blood sample does not turn the sampled analysis into a full-cohort risk calculation.
- **Case-cohort:** A baseline subcohort and incident cases require methods that account for sampling and possible overlap. Ordinary unweighted Cox regression on the sampled rows is not a default substitute.
- **Matched versus paired:** Matching different people on covariates differs from measuring one person twice. Preserve matched sets or within-person links as appropriate.
- **Before/after versus interrupted time series:** Two totals cannot estimate a pre-existing trajectory, seasonal pattern, or autocorrelation. An interrupted time series needs adequate repeated observations and an explicit intervention time; a comparison series can strengthen it.
- **Ecological versus multilevel:** County averages alone support county-level inference. Individual records nested in counties permit different questions, with clustering represented. Neither design automatically proves a contextual effect.
- **Case series versus single-arm trial:** Both may lack a concurrent comparator, but a prespecified interventional protocol differs from a descriptive collection of selected cases. Response alone does not identify a treatment effect relative to natural history.

These are design extensions for recognition, not additional verified-paper case studies in this pass.

## 6. Read a paper using the same extraction questions every time

1. State the question, target population, outcome type, and estimand in one sentence.
2. Explain inclusion: disease status, exposure, clinic attendance, population sampling, or allocation?
3. Draw the timing in words: eligibility/index date, exposure/predictors, follow-up, endpoint, censoring. Check for information acquired after prediction time or immortal time introduced by exposure classification.
4. Identify the sampled unit, allocation unit, measurement unit, and independent analysis unit separately.
5. Name the comparator and explain what supports exchangeability or its limitations: randomization, measured adjustment, matching, historical trends, or none.
6. Locate the actual model in Methods and its corresponding table/figure. Record effect direction, scale, units, denominator, uncertainty, and adjustment set.
7. Inspect exclusions, missingness, multiplicity, model assumptions, sensitivity analyses, and whether analyses were prespecified.
8. Write what the design supports and one claim it cannot establish. Separate what the authors reported from your own proposed reanalysis.

For a new research plan, transfer these answers into the [protocol template](../templates/study-protocol.md) before fitting anything. Use the [data-type-first guide](biomedical-statistics-decision-guide.md) for method selection and the [ML guide](../04_machine_learning/README.md) for synthetic prediction exercises.

## 7. Practice with answer sketches

| Prompt | Answer sketch |
| --- | --- |
| A file has equal numbers of cancer cases and controls. Is cancer prevalence 50%? | Not without knowing sampling; case-control selection can create that proportion. See SD-02. |
| A study retrieves ten years of existing records. Must it be case-control? | No. Eligibility followed from an index date to outcomes can define a retrospective cohort. See SD-08. |
| Does prospective exposure measurement prove causality? | No. It establishes time order more clearly, while confounding and measurement error remain. See SD-03. |
| Does 15,802 patients mean 15,802 independent random assignments? | No. SMART allocated ICU policies through time. See SD-05. |
| Does a higher mammography AUC show fewer cancer deaths? | No. Diagnostic performance and patient benefit require different evidence. See SD-07. |
| Can a treatment coefficient from a risk model guide treatment choice? | Not by itself; prognosis under observed care differs from a causal treatment contrast. See SD-08. |
| Is every TCGA molecular comparison longitudinal because the project has clinical follow-up? | No. Classify each analysis using the observations and timing it actually uses. See SD-01. |

**Review boundary:** Original article metadata, accessible abstracts, methods excerpts/full texts, and the named figures/sections informed these summaries. Access varies by publisher; the CSV records what was checked. No source analysis was independently replayed, and no new model execution or research-admission milestone is claimed.
