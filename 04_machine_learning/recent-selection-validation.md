# Recent evidence: selecting assays and validating predictions

[Breast cancer book, Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data) · [Tuning corpus](recent-tuning-evidence.md) · [Advanced training](advanced-breast-cancer-training.md) · [Evidence register](evidence/breast-cancer-studies.csv)

Reviewed **2026-10-16**. This pass adds **nine publications from 2021–2026**, a roughly five-year reading window, on feature selection, validation precision, leakage and model comparison. Read them alongside the ten recent sources in the [tuning corpus](recent-tuning-evidence.md), giving **nineteen sources across these two reading sets**. Other recent reporting guidance and clinical applications remain in the [main evidence guide](breast-cancer-evidence.md). Counts describe publications, not independent cohorts or replications.

The thread remains the book’s people → specimens → measurements → prediction → interpretation narrative. Start by asking what outcome is being predicted. Our executed synthetic example predicts specimen category for previously unseen people. Moving to recurrence or survival changes the task, outcome representation, assessment and sample-size question. New methods must be evaluated within that design.

## Follow the question, then choose the evidence

| Question in the breast cancer project | Read | Evidence boundary |
| --- | --- | --- |
| Which assay columns belong in a smaller panel? | [Survival filters](#bc-m20), [Multi-objective panels](#bc-m21) | Panel stability and predictive performance are separate; survival is different from tissue classification |
| Is an external assessment precise enough? | [Binary outcomes](#bc-m22), [Time-to-event outcomes](#bc-m23) | Plan for the population, endpoint and dependence structure; specimen count is not patient count |
| Does a model comparison answer a useful question? | [Medical imaging](#bc-m24), [Leakage audit](#bc-m25) | Audit upstream information and intended use as well as the splitter |
| Which model families deserve comparison? | [Trees and networks](#bc-m26), [TabPFN](#bc-m27) | General benchmark findings motivate comparators; they do not validate an assay predictor |
| How should prognosis models be tuned? | [2026 survival benchmark](#bc-m28) | Risk ranking, probability prediction and calibration require distinct assessment |

Each card distinguishes reported findings from our proposed application. Abstract-only review remains explicitly marked; selected methods do not imply a full source-code audit. All nine register entries retain `local_reproduction=not_run` and `artifact_status=not_reviewed`. No packages, weights or patient datasets were added by this literature pass.

## BC-M20

**Select genes for the endpoint actually being predicted — Bommert et al., 2022.** [Primary source](https://academic.oup.com/bib/article/23/1/bbab354/6366322) · [DOI](https://doi.org/10.1093/bib/bbab354)

**Reported evidence:** The benchmark compares 14 feature filters on 11 gene-expression survival datasets, including BRCA. It evaluates prediction, runtime, panel size and selection stability. Simple variance filtering performed strongly in this particular comparison.

**Review extent:** Abstract and selected experiment descriptions: nested resampling, package roles and the BRCA dataset. Journal issue year is 2022; online publication was September 2021. The linked R source was not inspected.

**Breast cancer application:** For a future breast cancer prognosis task, compare a simple filter with supervised or embedded selection inside the training procedure. Do not replace our binary tissue-category F-score selector solely because variance filtering ranked well on censored survival data. Check panel stability separately from predictive error; neither establishes a causal gene mechanism. Our current selection frequencies describe three overlapping outer training sets, not independent biological replications.

**Artifact pointer:** [Author-linked research artifact](https://github.com/bommert/survival-filter-benchmark); not source-reviewed or executed.

## BC-M21

**Treat panel size, accuracy and stability as separate goals — Cattelani et al., 2024.** [Primary source](https://pubmed.ncbi.nlm.nih.gov/39401114/) · [DOI](https://doi.org/10.1109/TCBB.2024.3480150)

**Reported evidence:** The authors compare seven feature-subset algorithms using cancer transcriptome datasets with training and external-validation sets. Their evaluation includes predictive performance, selected-set size, diversity and gene stability, with a reported breast cancer example.

**Review extent:** Indexed primary abstract and author-institution publication metadata only; full methods, cohort independence and code availability were not established.

**Breast cancer application:** When asking whether a smaller breast cancer panel is useful, declare both the prediction objective and how panel burden is measured. Select the final tradeoff within development; do not pick a panel from external-test results. Compare gene identities and prediction stability across resamples because correlated measurements can substitute for one another. The reported panel is not a validated replacement for the book’s 60-gene catalog, and a low column count alone does not establish assay feasibility.

## BC-M22

**Plan external-validation precision before collecting the cohort — Riley et al., 2021.** [Primary source](https://onlinelibrary.wiley.com/doi/10.1002/sim.9025) · [DOI](https://doi.org/10.1002/sim.9025)

**Reported evidence:** This methodological paper sizes binary-outcome validation studies for precision in calibration, discrimination and net benefit. Required inputs include anticipated event frequency, model predictions and calibration, desired uncertainty, and any decision thresholds.

**Review extent:** Publisher abstract only; formulas, supplied software and worked-example calculations were not reproduced.

**Breast cancer application:** A future patient-level breast cancer endpoint needs a validation cohort justified for that endpoint and population. Our 15 synthetic final-test people were chosen for a software example, not by a clinical precision calculation. Two specimens per person cannot simply be counted as two independent patients. A protocol with clustered specimens needs methods addressing that dependence; these participant-level calculations do not automatically cover our paired-specimen assessment. Keep recruitment requirements separate from tuning budgets.

## BC-M23

**Preserve censoring and prediction horizon in validation planning — Riley et al., 2022.** [Primary source](https://pubmed.ncbi.nlm.nih.gov/34915593/) · [DOI](https://doi.org/10.1002/sim.9275)

**Reported evidence:** The paper extends external-validation sample-size planning to time-to-event prediction, using simulation with assumptions about the model’s linear predictor and event/censoring distributions.

**Review extent:** Indexed primary abstract only. Journal issue year is 2022; the article appeared online in December 2021. No simulation code was run.

**Breast cancer application:** For a recurrence or disease-free follow-up question, specify time zero, event definition, prediction horizon and censoring before estimating validation needs. People without an observed event by last contact cannot all be coded as event-free at a later horizon. Our current binary tissue classifier has neither survival predictions nor follow-up and therefore supplies no evidence about recurrence. The binary and survival sizing papers are related methodological work, not independent clinical confirmations.

## BC-M24

**Ask whether the comparison solves a clinical research problem — Varoquaux and Cheplygina, 2022.** [Primary source](https://researcher.itu.dk/en/publications/machine-learning-for-medical-imaging-methodological-failures-and-/) · [DOI](https://doi.org/10.1038/s41746-022-00592-y)

**Reported evidence:** The authors review obstacles in medical-imaging research, linking data limitations, assessment choices and research incentives to the gap between benchmark progress and clinical usefulness.

**Review extent:** Author-institution abstract and indexed published abstract only; the associated analysis repository was not reviewed.

**Breast cancer application:** If extending the book to pathology or mammography, define the decision and eligible population before choosing an available dataset. A tissue-category model, screening detector and treatment-response model need different denominators and outcomes. Compare errors by relevant acquisition context and held-out site, and retain uncertainty alongside score differences. Site-based validation is a future study requirement, not something demonstrated by our synthetic person-grouped folds.

**Artifact pointer:** [Author-linked research artifact](https://github.com/GaelVaroquaux/ml_med_imaging_failures); not source-reviewed or executed.

## BC-M25

**Audit information flow across the whole scientific claim — Kapoor and Narayanan, 2023.** [Primary source](https://doi.org/10.1016/j.patter.2023.100804) · [DOI](https://doi.org/10.1016/j.patter.2023.100804)

**Reported evidence:** The paper surveys leakage in ML-based science, proposes a taxonomy of failure modes and model information sheets, and uses a civil-war prediction case study to investigate misleading model comparisons.

**Review extent:** Published/indexed abstract and author citation metadata only; no independent reanalysis of the case study.

**Breast cancer application:** For breast cancer assays, document when each predictor became available and where each transformation was fitted. Audit cohort construction, duplicate people, outcome-derived feature lists, batch correction and analyst choices as well as the final train/test split. A group-aware splitter does not by itself prove an entire upstream dataset is leakage-free. The civil-war example informs an audit approach; it does not measure leakage prevalence in breast cancer research.

## BC-M26

**Keep tree-based comparators when testing newer tabular models — Grinsztajn et al., 2022.** [Primary source](https://proceedings.neurips.cc/paper_files/paper/2022/hash/0378c7692da36807bdec87ab043cdadc-Abstract-Datasets_and_Benchmarks.html) · [DOI](https://doi.org/10.52202/068431-0037)

**Reported evidence:** This benchmark compares tree methods and neural networks while accounting for hyperparameter search. Its results on medium-sized tabular datasets motivate attention to irrelevant features, data representation and the functions each learner can capture.

**Review extent:** Primary NeurIPS abstract only; no benchmark code or individual dataset was audited.

**Breast cancer application:** Before adding a neural assay predictor, compare it against a fixed logistic model and appropriately tuned forest or boosting procedures on the same excluded people. Include preprocessing and search costs in the comparison. The benchmark’s roughly ten-thousand-row scale is different from our 45 development people, and its aggregate ranking is not a reason to promise a tree model will win on molecular measurements. Family selection must remain part of the assessed development procedure.

## BC-M27

**Evaluate foundation models without relaxing patient separation — Hollmann et al., 2025.** [Primary source](https://pubmed.ncbi.nlm.nih.gov/39780007/) · [DOI](https://doi.org/10.1038/s41586-024-08328-6)

**Reported evidence:** TabPFN uses a pretrained tabular model for classification and regression and reports strong benchmark results on small-to-medium datasets, including comparisons against tuned conventional methods.

**Review extent:** Indexed primary abstract and publication metadata only; paper-era weights, package API, license and current releases were not inspected.

**Breast cancer application:** A pretrained learner could become a research comparator, but every held-out person must remain outside the labeled context supplied to it. Keep preprocessing training-only, record the exact checkpoint and inference configuration, and investigate any overlap between evaluation cohorts and model-development data. In-context prediction is a different fitting mechanism, not permission to expose test labels. No TabPFN package or weights are deployed here; benchmark speed or accuracy does not establish a breast cancer benefit.

## BC-M28

**Tune survival models to the kind of prediction being assessed — Burk et al., 2026.** [Primary source](https://academic.oup.com/bioinformatics/article/42/5/btag186/8656833) · [DOI](https://doi.org/10.1093/bioinformatics/btag186)

**Reported evidence:** The 2026 benchmark compares 21 models on 34 low-dimensional, right-censored datasets. It tunes discrimination and survival probability error separately. No learner significantly outperformed Cox across the stated comparisons; this is not an equivalence finding.

**Review extent:** Abstract and selected study-design, preprocessing and resampling descriptions: mlr3 pipelines, training-only transformations and three-inner/three-outer nested resampling. The published archive is a pointer, not a reviewed or executed artifact.

**Breast cancer application:** Retain Cox as a declared baseline for a future breast cancer prognosis comparison and ask whether the model supplies risk rankings or survival probabilities. A C-index objective cannot substitute for probability calibration at a specified horizon. Carry the pipeline boundary into our design, while adding person/site/time separation as appropriate. Low-dimensional benchmark findings do not settle a high-dimensional gene-panel question; connect this reading to the survival filter study rather than treating them as interchangeable evidence.

**Artifact pointer:** [Author-linked research artifact](https://doi.org/10.5281/zenodo.19075310); not source-reviewed or executed.

## From paper mechanisms to a project plan

This map describes the next research design, not additional executed deployments:

| Mechanism observed in the reading | Candidate implementation route | What our protocol must add |
| --- | --- | --- |
| Filter selection and survival pipelines in BC-M20 | R `mlr3`, `mlr3filters`, `mlr3proba`, `mlr3pipelines`; `survival`/`glmnet` for relevant learners | Endpoint-specific task, nested training-only selection, person/site/time boundaries, a declared stability measure |
| Multi-objective panel selection in BC-M21 | Reference design; optimizer and assay-cost model still need selection | A development-only tradeoff rule, comparable budgets and a separate final assessment |
| Validation sizing in BC-M22–M23 | Evaluate the paper’s formulas/software after full-method review | Plausible event/censoring assumptions, uncertainty targets and explicit treatment of repeated specimens |
| Leakage audit in BC-M25 | [Study protocol](../templates/study-protocol.md) and [analysis record](../templates/analysis-record.md) | Predictor timing, upstream selection history, cohort identities and every data-driven revision |
| Model-family comparison in BC-M26–M27 | Existing [Python methods](methods-and-deployments.md) provide conventional starting points; TabPFN remains reference-only | Equivalent outcome/split definitions, versioned artifacts, prediction interface and complete search costs |
| Separate survival objectives in BC-M28 | Review the published archive before designing an mlr3 survival extension | Distinguish rank from distribution output, prespecify horizons and test assumptions about censoring |

For learners, inspect the existing [candidate traces](model-tuning.md#read-every-candidate-not-just-the-winner) and `feature_review.csv` from the [paired-specimen runner](examples/breast_cancer_feature_selection.py). Explain why a feature can appear frequently without proving a biological mechanism. Then write how the same training boundary would change if the outcome became recurrence time. That is a change in the research question, not a substitution of scoring functions in the current tissue classifier.

## Search and interpretation notes

The targeted search covered 2021–2026 work on cancer transcriptome selection, biomarker stability, external-validation sample size, clinical imaging evaluation, leakage, tabular foundation models and survival benchmarking. Primary journal/proceedings pages, indexed primary abstracts and author-institution records were checked on 2026-10-16. This was a selective update, not a systematic search or formal risk-of-bias assessment. Some full pages were blocked or returned incomplete text; those cards stay at abstract review rather than implying full-text access.

Journal issue years are used in the register. BC-M20 and BC-M23 first appeared online in 2021 but belong to 2022 journal issues. Related papers, public cancer datasets and benchmark ecosystems can overlap; the two Riley papers share a methodological programme, and the tabular papers connect to authors/benchmarks already represented in the tuning corpus. Do not pool their scores or count them as separate patient validations. Exact cohort independence and paper-era software compatibility require further review before adoption.

[Return to the breast cancer evidence guide](breast-cancer-evidence.md)
