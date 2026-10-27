# Computational Oncology: A Clinician–Scientist's Guide

> **Independent open textbook — master roadmap, edition 0.1 (planning architecture), October 2026**
>
> Authored by Paul Skeffington · Prepared with OpenAI

## Purpose and scope

Teach oncologists, physicians, biomedical researchers, and motivated beginners the mathematics, statistics, epidemiology, coding, informatics, genomics, machine learning, artificial intelligence, and research methods required to design and critically assess reproducible computational oncology investigations. This is an independently developed educational work, not a reproduction of any university curriculum. It does not grant clinical credentials, imply regulatory clearance, or substitute for specialist training or medical judgment.

**North-star capability:** Given a clearly defined oncology question, the reader can identify the study unit and target population; select a defensible design and estimand; secure appropriate, authorized data; build a versioned analysis; examine assumptions and bias; quantify uncertainty; validate models; interpret results responsibly; and deliver reproducible scientific communication.

**Publication principle:** The book should be readable without running code, but every executable claim must have a tested reference implementation. Use purpose-built synthetic examples by default; publicly available research data are optional only after dataset-specific permission, licensing, privacy, and provenance review.

## Reader pathways

1. **Clinician without prior programming:** Follow Parts I–III before running any examples; learn R first, then Python.
2. **Researcher with basic statistics:** Complete prerequisite diagnostics and enter at Part IV, revisiting earlier modules when gaps appear.
3. **Computational scientist entering oncology:** Read cancer biology, clinical endpoint, assay, registry, and governance foundations before applying existing modeling skills.

An experienced reader may bypass a chapter only by completing its independent competency check. Reading a chapter or passing unit tests alone does not establish human mastery.

## Ten-part, 60-chapter textbook architecture

Each numbered chapter must ultimately provide: clinical framing, prerequisites, learning outcomes, conceptual account, formal notation, worked synthetic oncology case, R or Python execution where appropriate, assumptions/diagnostics, interpretation, evidence register, original exercises and answer explanations, rubric, and an independent reproducibility check.

### Part I — Clinical and computational foundations
- **01** Cancer biology for quantitative investigators: cells, tissue, tumor evolution and mechanisms.
- **02** Clinical oncology data: diagnosis, staging, grade, treatments, response, toxicity and endpoints.
- **03** Molecular foundations: DNA, RNA, proteins, pathways, mutations, expression and assay limitations.
- **04** Data literacy: observational units, persons, tumors, specimens, visits, modalities and measurement error.
- **05** Essential mathematics I: algebra, functions, logarithms, rates and dimensional analysis.
- **06** Essential mathematics II: calculus, vectors, matrices, derivatives, gradients and optimization.

### Part II — Probability, biostatistics and inference
- **07** Randomness and probability: conditional probability, Bayes' theorem and clinical interpretation.
- **08** Discrete outcomes: Bernoulli, binomial, hypergeometric, Poisson and event rates.
- **09** Continuous distributions: normal, log-normal, t, chi-square and transformations.
- **10** Sampling: estimators, variability, central limit theorem and resampling.
- **11** Statistical inference: estimands, confidence intervals, hypothesis tests and p-values.
- **12** Comparison methods: independent/paired comparisons, categorical, ordinal, exact and rank tests.
- **13** Sample size, power, multiplicity and planning sensitivity analyses.

### Part III — Research design, ethics and epidemiology
- **14** Questions, populations, exposures, outcomes and protocol development.
- **15** Descriptive oncology epidemiology: incidence, prevalence, mortality, survival and denominators.
- **16** Cohort, case-control, cross-sectional, registry and ecological studies.
- **17** Trials, randomization, allocation, intercurrent events and intention-to-treat.
- **18** Confounding, selection, information bias, effect modification and transportability.
- **19** Causal diagrams, counterfactuals, target trials and quasi-experimental methods.
- **20** Screening, diagnostic accuracy, calibration, prevalence and clinical utility.
- **21** Ethics: consent, fairness, privacy, dataset rights and responsible model use.

### Part IV — Regression and longitudinal outcomes
- **22** Linear regression: geometry, estimation, residuals and uncertainty.
- **23** Logistic regression: odds, probabilities, discrimination and calibration.
- **24** Count and rate regression: Poisson offsets, dispersion and alternatives.
- **25** Survival fundamentals: censoring, Kaplan–Meier, log-rank and risk sets.
- **26** Cox models: proportional hazards, diagnostics, time-dependent issues and validation.
- **27** Repeated measures, hierarchies, mixed effects, generalized estimating equations.
- **28** Penalization, nonlinear effects, interactions, model specification and robustness.

### Part V — Data engineering and scientific programming
- **29** R fundamentals: objects, functions, control flow and package use.
- **30** Python fundamentals: objects, control flow, NumPy, pandas and tests.
- **31** Files, shell, Git, versioning, environments and reproducible notebooks.
- **32** Relational databases and SQL: keys, schema, joins and integrity.
- **33** Clinical informatics: registries, EHR concepts, coding systems and interoperability.
- **34** Data-quality engineering: provenance, missingness, unit harmonization and safe de-identification.
- **35** Reproducible pipelines: dependency graphs, containers, CI, testing and HPC.
- **36** Visualization: exploratory graphics, uncertainty, accessibility, R graphics, Shiny and dashboards.

### Part VI — Genomics and multimodal cancer biology
- **37** Sequencing data types, assay design and biological replicates.
- **38** RNA sequencing: raw counts, QC, normalization, dispersion and differential expression.
- **39** Mutation and copy-number analysis: calling limitations, annotation and provenance.
- **40** Pathway analysis, multiple testing, biological interpretation and external evidence.
- **41** Single-cell and spatial omics: cells, donors, batches, pseudoreplication and integration.
- **42** Cancer imaging and digital pathology: preprocessing, segmentation, leakage and validation.

### Part VII — Statistical learning and predictive modeling
- **43** Prediction tasks, baselines, loss functions and experimental design.
- **44** Preprocessing and partitions: grouping, nested CV, leakage and missingness.
- **45** Classical models: regularized models, trees, ensembles and kernels.
- **46** Unsupervised learning: PCA, clustering, LDA and validation.
- **47** Feature selection, hyperparameter tuning, stability and computational budgets.
- **48** Evaluation: discrimination, calibration, uncertainty, external validation, fairness and decision utility.

### Part VIII — Deep learning and applied AI
- **49** Neural network foundations, gradients, optimization and representation learning.
- **50** Imaging models, augmentation, transfer learning and shift evaluation.
- **51** Clinical NLP, entity extraction, document corpora and evaluation.
- **52** Language models, embeddings, retrieval-augmented generation and vector indexing.
- **53** Tool use, agents, provenance, failure containment and human oversight.
- **54** Multimodal oncology AI, prospective evaluation, model monitoring and governance.

### Part IX — Scientific translation and communication
- **55** Evidence appraisal: primary literature, systematic synthesis and reproducibility.
- **56** Scientific writing, figures, reporting guidance and transparent limitations.
- **57** Clinical interpretation, stakeholder communication and implementation science.

### Part X — Independent research laboratory
- **58** Protocol lab: independent study question, data dictionary, ethics and statistical analysis plan.
- **59** Reproducibility lab: end-to-end analysis, model evaluation, independent replay and audit trail.
- **60** Final research monograph: scientific report, transparent code, defense and critical peer review.

## Integrated oncology case portfolio

Maintain **one longitudinal synthetic breast cancer case** spanning data schemas, ESR1/ERBB2 biology, molecular measurements, classification and survival, without treating distinct endpoints as interchangeable.

Add independent, clearly sourced or synthetic problem cases:
- Lung cancer screening: sensitivity, specificity, overdiagnosis and longitudinal screening.
- Colorectal cancer: incidence, cohort design, comparative effectiveness and potential confounding.
- Hematologic malignancy: longitudinal laboratory profiles, hierarchical data and event times.
- Prostate cancer: competing events, risk communication and calibration.
- Pediatric oncology: sparse counts, small samples, ethics and uncertainty.
- Population oncology: geographic variation, registries and time trends.

Each scenario gets its own dataset contract, endpoint, units of analysis, evidence provenance and risk statement. Never re-label a synthetic assay model as a clinically validated predictor.

## Progressive mastery levels

| Level | Reader demonstrates | Independent evidence |
| --- | --- | --- |
| L0 Orientation | Define clinical question, population, outcome, unit and data type | Explain one case and identify invalid alternatives |
| L1 Quantitative literacy | Calculate and interpret distributions, uncertainty and common tests | Hand-solved examples plus numerical R replay |
| L2 Applied analysis | Manipulate data, visualize, fit and diagnose core regression models | Reproducible synthetic research notebook and oral/written defense |
| L3 Research design | Formulate protocol, estimand, risk-of-bias review, analysis plan | Registered-style synthetic protocol and sensitivity analysis |
| L4 Computational modeling | Use reproducible pipelines, genomics tools and leakage-safe validation | Independent split audit, benchmark and matched replay |
| L5 Advanced translation | Assess AI methods and external validity; explain limits and governance | External-assessment plan, model card, error and safety analysis |
| L6 Independent mastery | Execute and defend a complete research project within appropriate permissions | Capstone, source audit, reproducibility package and adversarial review |

These are **self-assessment milestones**, not university grades, professional certification or assurances of clinical competence.

## Delivery roadmap and publication gates

| Gate | Deliverable | Acceptance evidence | Dependency |
| --- | --- | --- | --- |
| B0 — editorial foundation | Scope, independent authorship policy, book table of contents, crosswalk, chapter contract | No restricted course materials; clear scientific/clinical boundaries | none |
| B1 — foundational manuscript | Parts I–II (chapters 01–13), reference exercises and solutions | Medical review, mathematical checks, executable probability examples | B0 |
| B2 — research reasoning | Part III (14–21), study design atlas and diagnostic examples | Original synthetic cases, bias/estimand checks, evidence citations | B1 |
| B3 — statistical modeling | Part IV (22–28) with R examples and diagnostics | Independent numerical tests, interpretability and assumptions | B1–B2 |
| B4 — computation and visualization | Part V (29–36), R/Python/SQL labs, reusable data schemas | Clean environment replay, deterministic fixtures, tests | B0–B3 |
| B5 — molecular oncology | Part VI (37–42), curated genomics and pathology cases | Assay-aware validation and biological expert review | B1–B4 |
| B6 — predictive modeling | Part VII (43–48), re-use existing synthetic ML evidence | Leakage tests, nested evaluation, reproducibility and limitations | B3–B5 |
| B7 — AI systems | Part VIII (49–54), independent retrieval and failure testing | Held-out benchmark, privacy controls, evidence links and model documentation | B4–B6 |
| B8 — publication and research lab | Parts IX–X (55–60) and completed capstone exemplars | Reproducible analysis packet, scientific review and editorial audit | B0–B7 |
| B9 — complete ebook release | Versioned multi-format publication, accessible figures, searchable crosslinks | Link checks, source/license audit, copyedit, accessibility review, reader pilot | B0–B8 |

**Gate status at inception:** B0 drafted; B1–B9 planned. Existing repository assets are reusable inputs, not evidence that corresponding chapters are publication-ready.

## Chapter writing and verification contract

Every chapter receives:
1. Stable identifier (`CO-01` through `CO-60`), title, version and prerequisite chapters.
2. A clinically meaningful question and independent, measurable learning objectives.
3. Original textbook exposition, definitions, equations and a clear distinction between association, prediction and causation.
4. At least one full calculation or reasoned derivation where meaningful.
5. At least one original synthetic worked case with explicit population, unit, endpoint and data provenance.
6. Runnable source where appropriate, versioned dependencies, expected output and negative tests.
7. Assumption checks, uncertainty, failure cases and conclusions that avoid clinical overclaim.
8. Primary references, date of verification, rights status, and independently authored interpretation.
9. Exercises in recall, computation, interpretation and design, with separately navigable model answers.
10. Editorial, scientific and accessibility review record before its status changes from draft to released.

### Release-status vocabulary

`planned` = outline only; `draft` = substantive writing exists; `tested` = code/numerical evidence exists; `reviewed` = editorial/scientific review passed; `released` = all gates satisfied. Avoid conflating an implemented script with a scientifically reviewed chapter.

## Independent academic content policy

Use the publicly listed disciplinary subjects of biomedical data science as an **external completeness check only**. Do not copy university slide decks, handouts, recorded lectures, assessments, answer keys, LMS content or proprietary instructional diagrams. Do not mirror university course assignments or publish course-derived materials. Instead develop original chapter sequencing, explanations, synthetic datasets, illustrations, questions and software from independent sources.

Use original figures or carefully licensed figures with attribution and permissions. Cite original methodological papers and authoritative technical documentation; store metadata and analysis rather than full third-party copyrighted articles. Do not claim affiliation, endorsement, or instructional approval from any academic institution.

## Existing Paul's Notes material to reuse by reference

- [Cancer-wide scope](../docs/cancer-research-scope.md)
- [Computing subjects](../03_learning/README.md)
- [Statistics decision guide](../03_learning/biomedical-statistics-decision-guide.md)
- [Statistics practice workbook](../03_learning/statistics-practice-workbook.md)
- [ML methods](../04_machine_learning/README.md)
- [60-gene breast cancer companion](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md)
- [Biomedical coding and literature](../02_biomedical_coding/README.md)
- [Machine indexing contract](../docs/machine-index.md)

Existing material is linked rather than duplicated. This file is the canonical roadmap; it is **not** a claim that all 60 chapters are already written.

## Disciplinary coverage checklist

For coverage verification only, check that the finished manuscript teaches mathematics/calculus/linear algebra, R, probability and biostatistics, ethics, wrangling, visualization, regression, survival/longitudinal modeling, research design, systems thinking, Python/Bash/HPC, statistical learning, genomics, machine learning/deep learning/NLP, LLM/RAG/agent systems and full research project communication. These are general fields, not a reproduction of a program's unique curriculum.


## Immediate authoring queue

1. Finalize the introductory learning diagnostics and oncology vocabulary for chapters 01–06.
2. Write Part II as a coherent mathematical/statistical text using independent oncology cases.
3. Build the original study-design atlas with observational and interventional contrasts.
4. Translate existing R/ML tools into chapter labs, preserving source version and audit evidence.
5. Add a machine-readable chapter registry and independent editorial checks before publishing ebook builds.

## Draft publication and citation coverage snapshot — 2026-10-27

The introduction and CO-01 through CO-05 are drafted and carry direct section-level evidence links; chapters CO-06 through CO-60 remain planned. This is **B1 authoring in progress**, not a completed or peer-reviewed book.

- [Reader navigation](README.md) lists the actual authored chapters rather than placeholder links.
- [Source register](evidence/source-registry.json) records curated primary and authoritative evidence URLs; the [readable bibliography](evidence/SOURCES.md) groups those links by scientific role.
- [Section citation crosswalk](evidence/section-citations.json) maps every H2/H3 heading in the five drafted manuscript documents to external evidence sources.
- [Evidence and editorial policy](evidence/README.md) distinguishes structural citation coverage from claim-level scholarly review.
- [Automated citation validation](../scripts/validate_oncology_citations.py) fails when new manuscript sections lack a mapped, direct linked reference or cite an unknown source.

**Editorial requirement:** Source links must be placed near the claims they support and verified in context before any chapter advances beyond draft status. A cited reporting guideline is not evidence of a successful clinical study or verified model.
