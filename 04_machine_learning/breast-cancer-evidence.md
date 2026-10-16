# Breast cancer machine learning: evidence and implementation

[Breast cancer book, Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data) · [Advanced training](advanced-breast-cancer-training.md) · [Structured register](evidence/breast-cancer-studies.csv) · [Broader paper mechanisms](recent-code-studies.md)

Source check: **2026-10-16**. This targeted corpus connects eight breast cancer application reports and twenty-eight methodological references to the book's people → specimens → measurements → prediction → interpretation narrative. It is a selective reading register, not a systematic review, meta-analysis, clinical recommendation, or reproduction of the studies. The two MASAI reports concern the same trial; reports are not independent cohorts. Other studies can also share public cohorts, so distinct publication identifiers do not establish independent patient evidence.

Each card separates **reported evidence**, **review extent**, and **our implementation decision**. Reading selected methods or source code does not certify the whole study. No participant datasets, external model objects, weights, figures, or third-party source trees are copied here. The book's individual gene accounts retain their existing `ABSTRACT_ONLY` status.

The [recent tuning update](recent-tuning-evidence.md) contains cards BC-M11–BC-M19 for 2021–2025 primary methods papers, alongside the existing 2023 review (BC-M10). The [selection and validation update](recent-selection-validation.md) adds BC-M20–BC-M28, including 2026 survival benchmarking. The structured register covers all three guides; methodological benchmarks remain separate from breast cancer application evidence.

## Begin with the endpoint

| Book question | Evidence cards | What the assessment must preserve |
| --- | --- | --- |
| Can an AI-supported workflow detect cancer during screening? | [BC-01](#bc-01), [BC-02](#bc-02), [BC-03](#bc-03) | Screening denominator, reader workflow, recall/false positives, interval follow-up and study design |
| Can baseline images predict a future diagnosis? | [BC-04](#bc-04) | Prediction origin, horizon, repeated examinations and follow-up |
| Can pathology plus clinical data estimate prognosis? | [BC-05](#bc-05) | Event definition, censoring, modality availability and external cohorts |
| Can pretreatment measurements predict response to a specified regimen? | [BC-06](#bc-06), [BC-07](#bc-07), [BC-08](#bc-08) | Pretreatment inputs, treatment context, response definition and held-out people |
| Are training, reporting and appraisal appropriate? | [BC-M01](#bc-m01), [BC-M02](#bc-m02), [BC-M03](#bc-m03) | Training-only selection, transparent reporting and a separate risk-of-bias assessment |

AUROC, a survival C-index, detection per 1,000 screens, and a workload reduction answer different questions. Do not sort these studies into a single performance leaderboard. A prognostic association is also different from demonstrating that a model-guided treatment change improves outcomes.

## BC-01

**PRAIM: observational implementation in screening — Eisemann et al., 2025.** [Primary abstract](https://pubmed.ncbi.nlm.nih.gov/39775040/) · [Article](https://doi.org/10.1038/s41591-024-03408-6)

**Reported evidence:** German prospective observational implementation across 12 sites. The paper reports detection of 6.7 versus 5.7 cancers per 1,000 screened women, a model-based relative difference of 17.6% (95% CI 5.7–30.8%). Readers chose whether to use the AI viewer; this was not randomized.

**Review extent:** Abstract plus [author code archive v1.3.0](https://doi.org/10.5281/zenodo.13952914) and [Dryad documentation](https://doi.org/10.5061/dryad.zs7h44jgn), without downloading or running the analysis package. The archive describes propensity scores and overlap weighting. The paper's overall 463,094 participants and the deposit's 461,818 analysis rows are different stated denominators; reconcile inclusion/exclusion rules before reproducing a table.

**Our implementation decision:** Retain a cohort-flow ledger and distinguish adjusted estimates from raw rates. A reader/site identifier and an AI-viewer exposure are analysis/design variables, not interchangeable with a diagnostic target. A public outcomes table is not a mammography training-image release. This workflow evaluation cannot validate our synthetic tissue classifier.

## BC-02

**MASAI: screening performance and detected-cancer characteristics — Hernström et al., 2025.** [Primary abstract](https://pubmed.ncbi.nlm.nih.gov/39904652/) · [Article](https://doi.org/10.1016/S2589-7500(24)00267-X)

**Reported evidence:** Randomized Swedish screening study; 105,934 women assigned, with 19 excluded from analysis. AI-supported screening detected 6.4 cancers per 1,000 versus 5.0 with standard double reading (ratio 1.29, 95% CI 1.09–1.51). Screen-reading workload decreased by 44.2%. The intervention combined triage and radiologist support using Transpara 1.7.0.

**Review extent:** Abstract and registration linkage, not raw trial data, full software, or a replication. These are protocol-defined secondary outcomes from [NCT04838756](https://clinicaltrials.gov/study/NCT04838756).

**Our implementation decision:** Record the intervention version, decision workflow, endpoint hierarchy and human involvement. More screen-detected cancers does not by itself establish reduced mortality. Continue to the follow-up report below rather than substituting a detection endpoint for an interval-cancer endpoint.

## BC-03

**MASAI: interval-cancer follow-up — Gommers et al., 2026.** [Author-hosted abstract](https://portal.research.lu.se/en/publications/interval-cancer-sensitivity-and-specificity-comparing-ai-supporte/) · [Article](https://doi.org/10.1016/S0140-6736(25)02464-X)

**Reported evidence:** The same randomized trial reported interval cancers at 1.55 versus 1.76 per 1,000 participants; ratio 0.88 (95% CI 0.65–1.18). This met the prespecified 20% non-inferiority margin. The confidence interval includes a ratio of one, so the numerical decrease is not evidence of demonstrated superiority for this endpoint. Sensitivity was 80.5% versus 73.8%; specificity was 98.5% in both groups.

**Review extent:** Author-hosted publication abstract and bibliographic record, not full trial reanalysis. Family identifier in the register: `MASAI-NCT04838756`, shared with BC-02.

**Our implementation decision:** Encode the estimand, margin, follow-up and uncertainty alongside the point estimate. Link reports from the same trial to avoid double-counting. Keep a screening safety or workflow claim separate from a mortality claim and from evidence about a new model trained in these notes.

## BC-04

**Mirai: multi-institutional future-risk validation — Yala et al., 2022.** [Primary abstract](https://pubmed.ncbi.nlm.nih.gov/34767469/) · [Article](https://doi.org/10.1200/JCO.21.01337)

**Reported evidence:** Evaluation included 128,793 mammograms from 62,185 patients at seven sites. The endpoint was diagnosis one to five years after the mammogram. Reported site-specific Uno concordance indices ranged from 0.75 to 0.84; the paper supplies site-specific uncertainty rather than one pooled accuracy figure.

**Review extent:** Abstract and figure-description material; model training source, weights and a reproducible environment were not audited in this pass. The paper appeared online in 2021 and in a 2022 journal issue; the register uses the issue year.

**Our implementation decision:** Count people separately from examinations. Keep all relevant examinations linked to their person, freeze the horizon and outcome source, and inspect site-specific results and calibration before considering transport. Multi-site discrimination does not establish a benefit from changing screening intervals. This is a future-risk task, unlike our paired tissue-category demonstration.

## BC-05

**Pathology plus clinical prognosis — Witowski et al., 2026.** [Article](https://doi.org/10.1038/s41467-026-73088-y) · [Primary PDF](https://www.nature.com/articles/s41467-026-73088-y.pdf)

**Reported evidence:** The study used 8,161 patients across 15 cohorts; 3,502 patients in five cohorts were reserved for external evaluation. It combines Kestrel pathology representations with clinical variables for time-to-event prediction. Reported disease-free-interval C-index: 0.71 (95% CI 0.68–0.75).

**Review extent:** Abstract, selected cohort/method sections and data/code availability statement. The full model codebase is proprietary; selected access may be considered under agreements. No released model or training procedure was executed here.

**Our implementation decision:** Retain separate pathology and clinical schemas, modality-ablation comparisons, event/censoring definitions and a pretraining-overlap audit. A numerically higher comparison score is not automatically a proven superiority claim. Prognosis under observed care does not establish differential benefit from competing treatments. Public libraries cited by a proprietary model do not make the full predictor openly reproducible.

## BC-06

**Multi-omic neoadjuvant response — Sammut et al., 2022.** [Primary abstract](https://pubmed.ncbi.nlm.nih.gov/34875674/) · [Article](https://doi.org/10.1038/s41586-021-04278-5)

**Reported evidence:** Pretreatment clinical, pathology, genomic and transcriptomic profiling covered 168 patients. The abstract reports pathological complete-response prediction with AUROC 0.87 in an external cohort of 75. The article describes a smaller complete-data modeling subset; do not treat all profiled patients as the fitting denominator. This paper appeared online in 2021 and in a 2022 issue.

**Review extent:** Abstract/indexed cohort description, [analysis README](https://github.com/cclab-brca/neoadjuvant-therapy-response-predictor/tree/405041d583baea6f8709d2e7dd43387b36cc7581), and selected [NAT-ML source](https://github.com/micrisor/NAT-ML/blob/94ce67a936b1e66410fb0be42e5516fe1d4086cf/training_code/classification_models.py). No study inputs or model files loaded.

**Our implementation decision:** Trace modality completeness and training-only selection. Separate external evaluation from internal scores after tuning. The response observed under a received regimen is not the counterfactual benefit of choosing another regimen. See the code mechanism notes below for the inspected implementation and environment limitations.

## BC-07

**Histology and clinical response prediction — Li et al., 2025.** [Article](https://doi.org/10.1038/s41698-025-01033-1) · [Primary PDF](https://www.nature.com/articles/s41698-025-01033-1.pdf)

**Reported evidence:** Retrospective modeling used 1,035 patients from four centers, comparing tissue regions and integrating a histology score with clinical predictors. Pooled validation AUROC for the integrated model was 0.780 (95% CI 0.726–0.833), compared with 0.706 (0.645–0.768) for the clinical comparator. The separate immune-information comparison, 0.831 versus 0.822, had p=0.183; that increment is not established by that comparison.

**Review extent:** Selected methods/results and availability sections, plus the linked [TS-Score README at a pinned commit](https://github.com/YongQuanYang/TS-Score/tree/21beba298c4b7d609480e59d87ee08f90cb39a51). The README describes an earlier paper and legacy segmentation/scoring components. Full coverage of the 2025 integrated model remains unverified; study data are described as available on request.

**Our implementation decision:** Track which code release implements which stage and which paper. Preserve patient-level partitions before making image patches. Verify prediction-time availability of every clinical input. Feature ranks and tissue-region explanations need evidence beyond a performance plot.

## BC-08

**Transcriptome-informed response prediction — Park et al., October 2026 preprint.** [Version 1 abstract](https://arxiv.org/abs/2610.03693v1)

**Reported evidence:** Posted 2 October 2026. The authors describe learning expression from histology, followed by response prediction from inferred expression and clinical variables. Reported downstream development: 1,080 patients in five cohorts; evaluation: 1,412 in nine cohorts; pooled AUROC 0.79 (95% CI 0.73–0.85).

**Review extent:** Versioned preprint abstract only. No peer-reviewed version was verified in this pass. Source code, cohort overlap, inferred-expression accuracy and complete modeling details were not audited. No checkpoint executed.

**Our implementation decision:** Keep measured and inferred expression distinct in the data dictionary. Before adaptation, audit representation-pretraining overlap and preserve external cohorts through both stages. Compare clinical-only, image-only and fused procedures under the same patient split. This is a recent research lead, not established treatment-selection evidence or a verification upgrade for the book's gene cards.

## BC-M01

**Selection bias control — Ambroise and McLachlan, 2002.** [Primary abstract](https://pubmed.ncbi.nlm.nih.gov/11983868/) · [Article](https://doi.org/10.1073/pnas.102102699)

The paper explains why evaluating a classifier after selecting genes using the same assessment observations can underestimate prediction error. Its worked cancer datasets concern colon cancer and leukemia, not breast cancer. This is general methodological evidence applied to our breast cancer workflow, not a breast cancer performance study. Review extent: abstract and indexed description; no reanalysis.

**Our implementation decision:** Repeat supervised ranking and subset-size tuning inside resampling. Our [paired-specimen selection case](advanced-breast-cancer-training.md) tests that boundary using synthetic data. It does not replicate this paper or establish clinical gene-panel performance.

## BC-M02

**Transparent reporting — Collins et al., TRIPOD+AI, 2024.** [Primary abstract](https://pubmed.ncbi.nlm.nih.gov/38626948/) · [Statement](https://doi.org/10.1136/bmj-2023-078378)

TRIPOD+AI addresses reporting of prediction-model development and evaluation using regression or machine learning. Review extent: publication abstract/statement description, not a completed item-by-item assessment of these studies.

**Our implementation decision:** Record intended use, data provenance, target and predictor timing, missingness, partition design, model specification, performance and uncertainty. Use the full published checklist when writing a study report. Reporting completeness does not establish low risk of bias, and adding this citation does not make our teaching examples TRIPOD+AI compliant.

## BC-M03

**Quality and bias appraisal — Moons et al., PROBAST+AI, 2025.** [Primary abstract](https://pubmed.ncbi.nlm.nih.gov/40127903/) · [Tool description](https://doi.org/10.1136/bmj-2024-082505)

PROBAST+AI separates appraisal of model development from model evaluation, addressing participants/data sources, predictors, outcome and analysis. Review extent: abstract/tool-development description; no formal ratings assigned to the studies above.

**Our implementation decision:** Appraise whether the data and assessment design fit the breast cancer use case independently of how well the paper reports them. A repository badge, large patient count, or high discrimination score is not a substitute for this appraisal. Link completed, study-specific assessments if they are performed later.

## BC-M04

**Nested tuning evidence — Varma and Simon, 2006.** [Primary article](https://doi.org/10.1186/1471-2105-7-91)

The simulation study examines using cross-validation both to optimize a classifier and to report its error. It shows optimistic error estimates from that reuse and assesses an inner-tuning/outer-evaluation procedure. Review extent: abstract and selected introductory methods; no experiments reproduced.

**Our implementation decision:** Assess the complete assay-selection and model-tuning procedure on outer-held-out people. Do not describe the winning inner score as independently validated performance. The [project tuning guide](model-tuning.md) maps this distinction to our saved candidate and prediction records.

## BC-M05

**Overfitting the selection criterion — Cawley and Talbot, 2010.** [Primary JMLR record](https://jmlr.org/papers/v11/cawley10a.html)

The paper analyzes how optimizing a noisy finite-sample selection criterion can itself overfit and bias performance assessment. Review extent: publication abstract; not a full paper audit or reanalysis.

**Our implementation decision:** Count the candidate budget and any subsequent human or model-family choices as part of development. A longer assay-model search does not add independent people or guarantee a better transported predictor. Keep the final test outside those choices.

## BC-M06

**Budgeted random search — Bergstra and Bengio, 2012.** [Primary JMLR record](https://jmlr.org/papers/v13/bergstra12a.html)

The paper compares random and grid search and studies why allocating trials across a broader space can help when only some settings strongly affect performance. Its experiments are not breast cancer clinical evidence. Review extent: publication abstract; search experiments not reproduced.

**Our implementation decision:** For a future large assay/pathology space, compare a prespecified random-search budget with an appropriate baseline using the same assessment design. Our current six-candidate grid is executed; random search remains a reference extension, not a demonstrated improvement here.

## BC-M07

**Sequential Bayesian search — Snoek, Larochelle and Adams, 2012.** [Primary proceedings abstract](https://papers.nips.cc/paper_files/paper/2012/hash/05311655a15b75fab86956663e1819cd-Abstract.html)

The work models the tuning objective with a Gaussian process and considers sequential experiment choice, including varying experiment costs. Review extent: proceedings abstract; no optimizer or benchmark executed.

**Our implementation decision:** A future expensive breast pathology/fusion workflow could use sequential search under a fixed patient split and budget. Preserve the objective and complete trial history. It cannot learn from the final test or be assumed superior to the small existing grid without a relevant comparison.

## BC-M08

**Multi-fidelity allocation — Li et al., Hyperband, 2018.** [Primary JMLR record](https://jmlr.org/papers/v18/16-558.html)

Hyperband allocates resources across configurations and uses early stopping within a bandit-based search framework. Review extent: publication abstract; no Hyperband execution or breast cancer benchmark here.

**Our implementation decision:** Define a valid training resource and stopping rule before considering adaptive allocation. Randomly removing specimens may split patients or change class composition. A low-resource winner need not be the best full-resource assay model. This is a reference mechanism; our current runner completes every grid candidate.

## BC-M09

**CV uncertainty — Bengio and Grandvalet, 2004.** [Primary JMLR record](https://www.jmlr.org/papers/v5/grandvalet04a.html)

The paper establishes that there is no universal unbiased variance estimator for k-fold cross-validation and discusses correlations induced by overlapping samples. Review extent: publication abstract; no variance study replicated.

**Our implementation decision:** Label inner fold scores and their spread as descriptive. Three outer fits, repeated splits or model-selection frequencies are not independent cohorts. A patient-level uncertainty analysis needs its own documented estimand and procedure; fold standard deviation alone is not a clinical confidence interval.

## BC-M10

**HPO practice synthesis — Bischl et al., 2023.** [Published review](https://doi.org/10.1002/widm.1484)

This methodological review covers hyperparameter optimization foundations, search algorithms, practical considerations and open challenges. Review extent: indexed publisher abstract/record; full text was not available through this pass. It is not breast cancer application evidence or an executed method comparison.

**Our implementation decision:** Maintain a project-specific tuning contract containing the search space, objective, resampling, budget, failure handling and refit rule. The [tuning guide](model-tuning.md) and candidate trace make those choices inspectable; they do not establish a globally optimal model.

The [dedicated tuning corpus](model-tuning.md) connects BC-M04–BC-M10 to this project's grids, metrics, budgets, and saved inner-fold trial scores.

## What the author code shows, and what we would adapt

These are source observations and our proposed engineering choices, not executed study reproductions.

| Artifact inspected | Observed mechanism | Adaptation for the book's workflow |
| --- | --- | --- |
| PRAIM Zenodo v1.3.0 landing documentation | Versioned analysis package; observational adjustment described; change log distinguishes author outputs and rerunning instructions | Pin the archive and data version, reconstruct denominators, then compare a defined table with the author output; no reproduction claim before execution |
| NAT-ML `classification_models.py` at `94ce67a936b1e66410fb0be42e5516fe1d4086cf` | Pipelines combine correlation filtering, scaling, top-k ranking and a classifier; randomized search tunes subsets/settings; an averaging class combines fitted probability predictions | Keep all outcome-informed filtering inside training, use explicit person/site folds, and assess the selection procedure with an outer boundary |
| Same NAT-ML file | Correlation filtering uses the outcome to choose between correlated columns; refit/plot helpers also operate on already selected settings | Treat that filter as supervised. A refit of chosen settings on CV folds is not itself a nested assessment of how settings were chosen; preserve the separate external-evaluation question |
| Same NAT-ML file | Legacy `iid=False`, `scipy.interp`, fixed `/data/` paths and unbounded parallel settings appear in the inspected source | Restore a compatible historical environment for reproduction, or document a separate tested port; use configured output paths and bounded workers in new implementations |
| TS-Score README at `21beba298c4b7d609480e59d87ee08f90cb39a51` | Segmentation and patch scoring are separate stages; README points to an earlier paper and old Python/TensorFlow requirements | Verify the exact 2025 pipeline, weights and feature aggregation before claiming the linked repository reproduces the integrated model |
| Witowski et al. code statement | Full predictor is proprietary; public framework names and conditional access are described | Record access limits explicitly; do not substitute a generic vision model and call it the published test |

The NAT-ML source observation is limited to the named file and READMEs. It is not a full implementation audit. No source is copied into our executable examples; compatibility and partition choices must be tested independently. Equal averaging of base probabilities is different from learning a stacking combiner.

## Evidence-backed practices for our next breast cancer deployment

The following are **our acceptance requirements**, informed by the cards above. They are not a completed validation checklist or clinical clearance.

| Requirement | Evidence connection | Current local position |
| --- | --- | --- |
| Define people, specimens, dates and an explicit endpoint before training | BC-01–BC-08 distinguish screening, prognosis and response | [Book Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data); synthetic identities only |
| Keep feature selection and every outcome-informed transformation inside training | BC-M01 and inspected NAT-ML pipeline mechanism | [Selection tests](tests/test_breast_cancer_feature_selection.py) inspect actual inner fitting and challenge test leakage |
| Preserve patient groups, including slide patches and paired specimens | BC-04, BC-06, BC-07 motivate the identity audit | Synthetic person-grouped nested folds execute; external-site assessment remains an extension |
| Declare a modality-completeness policy and compare with a simpler baseline | BC-05–BC-08; multimodal studies differ in available inputs | Prevalence/mean baselines execute; no pathology/transcriptomics fusion deployment is claimed |
| Report appropriate discrimination, probability error and uncertainty | Different endpoints across all application cards | Synthetic Brier/AUROC/AP and Cox concordance execute; patient-level uncertainty, horizon calibration and decision utility remain extensions |
| Keep cohort overlap, pretraining provenance and access/version records | BC-02/03 same trial; BC-05/08 representations; code access differences | Same-trial grouping and artifact status recorded; no cross-study patient-overlap clearance asserted |
| Separate transparent reporting from a formal bias/applicability appraisal | BC-M02, BC-M03 | Reporting guidance linked; formal completed study appraisals are pending |

## Use the register and keep it current

The [CSV register](evidence/breast-cancer-studies.csv) stores stable card IDs, citation identifiers, task, design, trial/cohort family, source URL, review extent, artifact status, and local application. `not_run` means no external study has been reproduced here. A shared family marks known related reports; different families do not certify non-overlap.

Run from the repository root:

```bash
python3 scripts/check_ml_evidence.py
python3 scripts/tests/test_ml_evidence.py
python3 scripts/check_documentation.py
```

The checker validates register structure, identifiers, links to local applications, card coverage, dates, and declared review/status values. It does not fetch papers, verify scientific conclusions, perform PROBAST+AI appraisal, or execute external study code. Add primary-source evidence and a concrete implementation implication with every new card. Record a new review date only for the material actually revisited.

[Return to the breast cancer research question](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data)
