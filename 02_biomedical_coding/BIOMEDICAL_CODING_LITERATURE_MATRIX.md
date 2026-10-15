# Biomedical Coding Literature Matrix

**Paul's Notes** | Independent, source-linked methods and software literature  
**Author:** Paul Skeffington · **Prepared with OpenAI**  
**Reviewed:** October 15, 2026 · **41 sources across 10 areas**

[Machine-readable matrix](biomedical_coding_literature_matrix.csv) · [Quality gates](IMPLEMENTATION_GATES.md) · [Current manuals](PRIMARY_DOCUMENTATION.md) · [Section index](README.md)

This is a curated, non-ranked selection of influential research contributors and methodological sources in computational biology, statistics, biomedical ML, and clinical AI. It is **not a systematic review, an author citation ranking, or evidence of clinical deployment readiness**. Method papers, software articles, reporting guidelines, and risk-of-bias appraisal tools have separate roles.

Each coding practice, acceptance check, and failure mode below is an independently authored interpretation of the research's implications for code. It is **not** an extracted quotation, validation of the original authors' code, or proof of study accuracy. We link primary publications; full articles, proprietary figures and licensed datasets are not copied.

## Influential researchers and their domains

| Methods area | Representative contributors |
| --- | --- |
| Scientific computing | Greg Wilson, Jennifer Bryan, Geir Sandve, William Noble, Mark Wilkinson |
| Statistical R / Python | Hadley Wickham, Max Kuhn, Douglas Bates, Fabian Pedregosa |
| Genomic analysis | Robert Gentleman, Wolfgang Huber, Michael Love, Simon Anders, Gordon Smyth, Jeffrey Leek, Yoav Benjamini |
| Single-cell and workflow engineering | Fabian Theis, Rahul Satija, Romain Lopez, Johannes Köster, Paolo Di Tommaso, Björn Grüning |
| Prediction validity | Richard Simon, Sayash Kapoor, Judith Bernett, Ben Van Calster, Miguel Hernán |
| Clinical AI standards and safety | Gary Collins, Karel Moons, Xiaoxuan Liu, Viknesh Sounderajah, Jenna Wiens, Marzyeh Ghassemi |

The contributors are not ranked and papers with collaborative authorship are represented by abbreviated author lists.

## Literature-to-code matrix

### Reproducibility (4)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-001 | [Good enough practices in scientific computing](https://doi.org/10.1371/journal.pcbi.1005510) · Wilson; Bryan et al. (2017) | Perspective | Separate raw inputs and derived outputs; document versioned analysis | Rebuild outputs from clean checkout and synthetic inputs | Undocumented manual processing |
| BM-002 | [Ten simple rules for reproducible computational research](https://doi.org/10.1371/journal.pcbi.1003285) · Sandve; Nekrutenko; Taylor; Hovig (2013) | Perspective | Record parameters, file identities, software and commands | Trace every output to inputs and a reproducible command | Results without provenance |
| BM-003 | [A quick guide to organizing computational biology projects](https://doi.org/10.1371/journal.pcbi.1000424) · Noble (2009) | Perspective | Separate source, data, scripts, notes, generated outputs | Confirm clean paths with no untracked local dependencies | Unreproducible ad hoc workspace |
| BM-004 | [The FAIR Guiding Principles for scientific data management and stewardship](https://doi.org/10.1038/sdata.2016.18) · Wilkinson; Dumontier et al. (2016) | Principles | Retain identifiers, dictionaries, release rights, provenance | Review license, dictionary, version, access limits | FAIR does not confer sharing permission |

### Statistical programming (4)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-005 | [Tidy data](https://doi.org/10.18637/jss.v059.i10) · Wickham (2014) | Method | Design tidy tables around observation, variable and ID semantics | Check duplicate keys, type stability and row counts after joins | Tidy structure can still encode wrong units |
| BM-006 | [Building predictive models in R using the caret package](https://doi.org/10.18637/jss.v028.i05) · Kuhn (2008) | Software paper | Define resampling, tuning, fold-safe preprocessing and seeds | Fit preprocessing within training folds and nest model selection | Overoptimistic tuning and leakage |
| BM-007 | [Fitting linear mixed-effects models using lme4](https://doi.org/10.18637/jss.v067.i01) · Bates; Mächler; Bolker; Walker (2015) | Software paper | Model clustering, repeated observations, random effects | Inspect convergence, singular fits and grouping units | Pseudoreplication |
| BM-008 | [Scikit-learn: machine learning in Python](https://www.jmlr.org/papers/v12/pedregosa11a.html) · Pedregosa; Varoquaux et al. (2011) | Software paper | Keep preprocessing and estimators in pipelines | Prove scalers and selectors never fit on held-out rows | Pipeline convenience does not prevent leakage |

### Genomic statistics (10)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-009 | [Bioconductor: open software development for computational biology and bioinformatics](https://doi.org/10.1186/gb-2004-5-10-r80) · Gentleman; Carey et al. (2004) | Software framework | Use typed genomic data objects and versioned annotations | Validate sample and gene IDs through each transform | Assay and metadata misalignment |
| BM-010 | [Orchestrating high-throughput genomic analysis with Bioconductor](https://doi.org/10.1038/nmeth.3252) · Huber; Carey; Gentleman et al. (2015) | Perspective | Build interoperable assay containers with recorded releases | Assert matching dimensions, identities and annotation provenance | Biologically wrong results from aligned-looking arrays |
| BM-011 | [Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2](https://doi.org/10.1186/s13059-014-0550-8) · Love; Huber; Anders (2014) | Methods paper | Use raw-count models with explicit design matrices and contrasts | Verify count scale, replication, rank and diagnostics | Transformed counts fed to count models |
| BM-012 | [edgeR: a Bioconductor package for differential expression analysis of digital gene expression data](https://doi.org/10.1093/bioinformatics/btp616) · Robinson; McCarthy; Smyth (2010) | Software paper | Track raw count matrix, normalization and dispersion | Inspect library sizes, offsets and dispersion assumptions | Incorrect offsets or small replication |
| BM-013 | [limma powers differential expression analyses for RNA-sequencing and microarray studies](https://doi.org/10.1093/nar/gkv007) · Ritchie; Phipson; Wu et al. (2015) | Methods paper | Fit assay-appropriate models, contrasts and weights | Audit design matrix, weights and adjusted significance | Invalid contrast or assay scale |
| BM-014 | [The sva package for removing batch effects and other unwanted variation in high-throughput experiments](https://doi.org/10.1093/bioinformatics/bts034) · Leek; Johnson; Parker; Jaffe; Storey (2012) | Software paper | Inspect batch and unwanted variation before correction | Cross-tabulate batch and outcome; isolate test-fold correction | Removing genuine biology |
| BM-015 | [Complex heatmaps reveal patterns and correlations in multidimensional genomic data](https://doi.org/10.1093/bioinformatics/btw313) · Gu; Eils; Schlesner (2016) | Software paper | Create annotated heatmaps with coherent scales and grouping | Inspect exported figure at final size and assert label order | Clipping and misleading group annotation |
| BM-016 | [Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles](https://doi.org/10.1073/pnas.0506580102) · Subramanian; Tamayo et al. (2005) | Method | Declare ranking metric, gene universe and gene set release | Retain complete ranked list and assess multiplicity | Unstated reference gene universe |
| BM-017 | [Statistical significance for genomewide studies](https://doi.org/10.1073/pnas.1530509100) · Storey; Tibshirani (2003) | Method | Use defensible multiplicity treatment over a test family | Compare p-values and corrected values on known fixtures | Excess false positives |
| BM-018 | [Controlling the false discovery rate: a practical and powerful approach to multiple testing](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x) · Benjamini; Hochberg (1995) | Method | Specify appropriate FDR adjustment and assumptions | Reproduce hand-worked adjusted-p values on small input | Assumption-free FDR claims |

### Single-cell methods (3)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-019 | [SCANPY: large-scale single-cell gene expression data analysis](https://doi.org/10.1186/s13059-017-1382-0) · Wolf; Angerer; Theis (2018) | Software paper | Record cell, feature and donor IDs across QC steps | Check shapes, filtering decisions and donor-held-out splits | Cells mistaken for independent donors |
| BM-020 | [Integrated analysis of multimodal single-cell data](https://doi.org/10.1016/j.cell.2021.04.048) · Hao; Hao et al. (2021) | Method | Record feature spaces, modality pairing and integration choices | Verify cell IDs and per-modality availability | Integration masking condition signal |
| BM-021 | [Deep generative modeling for single-cell transcriptomics](https://doi.org/10.1038/s41592-018-0229-2) · Lopez; Regier; Cole; Jordan; Yosef (2018) | Method | Represent batch effects and uncertainty in latent models | Test stability across seeds and held-out donors | Latent clusters overinterpreted |

### Workflow engineering (3)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-022 | [Snakemake: a scalable bioinformatics workflow engine](https://doi.org/10.1093/bioinformatics/bts480) · Köster; Rahmann (2012) | Software paper | Encode explicit rule inputs, outputs and dependencies | Freshly rebuild all derived outputs from inputs | Undeclared local input |
| BM-023 | [Nextflow enables reproducible computational workflows](https://doi.org/10.1038/nbt.3820) · Di Tommaso; Chatzou et al. (2017) | Software paper | Pin versions, record parameters and workflow traces | Replay fixed synthetic example with environment snapshot | Unpinned containers and database drift |
| BM-024 | [Bioconda: sustainable and comprehensive software distribution for the life sciences](https://doi.org/10.1038/s41592-018-0046-7) · Grüning; Dale et al. (2018) | Software infrastructure | Record environment resolution, channels and platform | Resolve lock/spec and compare reported binary versions | Environment depends on changing defaults |

### Prediction validation (5)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-025 | [Bias in error estimation when using cross-validation for model selection](https://doi.org/10.1186/1471-2105-7-91) · Varma; Simon (2006) | Method | Nest model selection inside unbiased outer evaluation | Verify outer fold is untouched throughout tuning | Optimistic reported error |
| BM-026 | [Leakage and the reproducibility crisis in machine-learning-based science](https://doi.org/10.1016/j.patter.2023.100804) · Kapoor; Narayanan (2023) | Critical review | Audit temporal, group, duplicate and feature leakage | Document leakage audit and negative controls | Spurious high performance |
| BM-027 | [Guiding questions to avoid data leakage in biological machine learning applications](https://doi.org/10.1038/s41592-024-02362-y) · Bernett; Blumenthal; Grimm et al. (2024) | Perspective | Prevent related subjects, donors and homologs crossing folds | Audit group exclusivity, batch structure and homology | Random row split over related samples |
| BM-028 | [The precision-recall plot is more informative than the ROC plot when evaluating binary classifiers on imbalanced datasets](https://doi.org/10.1371/journal.pone.0118432) · Saito; Rehmsmeier (2015) | Method | Evaluate precision-recall at meaningful prevalence | Check PR baseline, thresholds and confusion matrix | ROC-only interpretation on rare outcomes |
| BM-029 | [Calibration: the Achilles heel of predictive analytics](https://doi.org/10.1186/s12916-019-1466-7) · Van Calster; McLernon; van Smeden et al. (2019) | Perspective | Report discrimination and calibrated risk with uncertainty | Evaluate calibration intercept, slope and curve | High AUC but inaccurate risk probabilities |

### Clinical epidemiology (2)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-030 | [Using big data to emulate a target trial when a randomized trial is not available](https://doi.org/10.1093/aje/kwv254) · Hernán; Robins (2016) | Method | Define eligibility, time zero, treatment and estimand | Audit immortal-time bias and treatment classification | Confounding and misaligned baseline |
| BM-031 | [The REporting of studies Conducted using Observational Routinely-collected health Data (RECORD) statement](https://doi.org/10.1371/journal.pmed.1001885) · Benchimol; Smeeth et al. (2015) | Reporting guideline | Document cohort construction, code lists and linkage | Reconcile phenotype code lists and cohort attrition | Codes not equal to validated clinical phenotype |

### Clinical AI guidelines (6)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-032 | [TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods](https://doi.org/10.1136/bmj-2023-078378) · Collins; Moons; Dhiman et al. (2024) | Reporting guideline | Disclose intended use, data, model, evaluation and limitations | Complete prediction-specific checklist and reproducibility details | Reporting cannot guarantee validity |
| BM-033 | [PROBAST+AI: an updated quality, risk of bias, and applicability assessment tool for prediction models using regression or artificial intelligence methods](https://doi.org/10.1136/bmj-2024-082505) · Moons; Damen; Kaul et al. (2025) | Appraisal tool | Assess bias, quality and applicability distinct from model metrics | Record independent reviewer justification by domain | Software test falsely equated with low bias |
| BM-034 | [The STARD-AI reporting guideline for diagnostic accuracy studies using artificial intelligence](https://doi.org/10.1038/s41591-025-03953-8) · Sounderajah; Guni; Liu et al. (2025) | Reporting guideline | Document index test, comparator, reference standard and setting | Validate participant flow, exclusions and subgroup reporting | Diagnostic AUC mistaken for prospective benefit |
| BM-035 | [The TRIPOD-LLM reporting guideline for studies using large language models](https://doi.org/10.1038/s41591-024-03425-5) · Gallifant; Afshar; Ameen et al. (2025) | Reporting guideline | Record prompt, retrieval corpus, model versions and raters | Audit evidence fidelity, abstention and evaluator agreement | Hallucinations and changing model outputs |
| BM-036 | [Reporting guidelines for clinical trial reports for interventions involving artificial intelligence: the CONSORT-AI extension](https://doi.org/10.1038/s41591-020-1034-x) · Liu; Cruz Rivera; Moher et al. (2020) | Reporting guideline | Specify human-AI intervention and fault handling | Reconcile AI workflow, participant flow and trial checklist | Confusing model validation with randomized trial |
| BM-037 | [Guidelines for clinical trial protocols for interventions involving artificial intelligence: the SPIRIT-AI extension](https://doi.org/10.1038/s41591-020-1037-7) · Cruz Rivera; Liu; Chan et al. (2020) | Reporting guideline | Pre-specify intervention details, monitoring and clinician roles | Audit protocol items before enrollment | Post-hoc AI workflow definitions |

### Responsible AI (3)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-038 | [Do no harm: a roadmap for responsible machine learning for health care](https://doi.org/10.1038/s41591-019-0548-6) · Wiens; Saria; Sendak et al. (2019) | Perspective | Define clinical decisions, risks, oversight and monitoring | Set stop conditions, deployment gates and rollback plan | Retrospective metrics mistaken for safety |
| BM-039 | [The false hope of current approaches to explainable artificial intelligence in health care](https://doi.org/10.1016/S2589-7500(21)00208-9) · Ghassemi; Oakden-Rayner; Beam (2021) | Viewpoint | Check explanation faithfulness, not only attractive plots | Test attribution stability and clinical relevance | Misleading explanatory narratives |
| BM-040 | [Dissecting racial bias in an algorithm used to manage the health of populations](https://doi.org/10.1126/science.aax2342) · Obermeyer; Powers; Vogeli; Mullainathan (2019) | Empirical analysis | Evaluate proxy labels and performance across groups | Check label construction, subgroup errors and consequences | Using utilization cost as proxy for medical need |

### RAG foundations (1)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-041 | [Retrieval-augmented generation for knowledge-intensive NLP tasks](https://proceedings.neurips.cc/paper/2020/hash/6b493230205f780e1bc26945df7481e5-Abstract.html) · Lewis; Perez; Piktus et al. (2020) | Foundational NLP method | Trace retrieved evidence and citation references per answer | Measure source coverage, faithfulness and abstention | General NLP RAG is not clinical validation |

## Use and verification rules

- **Primary citation:** metadata and source URL checked against publisher, PubMed, journal, or primary proceedings records. The original research remains under its own publishing terms.
- **Code gate:** no article is promoted to approved executable practice until its assumptions, test data, current API, environment version and independent regression checks have been recorded.
- **Study design:** patient, site, donor, batch, temporal and homology dependence can invalidate naive row-level splits. Leakage assessment belongs before modeling.
- **Methods versus reporting:** TRIPOD+AI and STARD-AI guide disclosure; PROBAST+AI appraises bias and applicability; CONSORT-AI and SPIRIT-AI concern different clinical trial stages.
- **Clinical scope:** statistical significance, good plots, cross-validation or reporting compliance do not establish clinical benefit or safety.
- **RAG scope:** the foundational 2020 NeurIPS work is generic NLP research, not empirical proof of clinical correctness. Require evidence tracing and refusal/abstention validation for medical applications.
- **Reading priority:** the CSV categorizes records as core, applied or context, **not author quality or rank**.

Review the [implementation gates](IMPLEMENTATION_GATES.md) for practical acceptance criteria. Use [current package documentation](PRIMARY_DOCUMENTATION.md) to determine API behavior rather than relying on historic code examples.

## Maintenance

The CSV is canonical for IDs and bibliographic metadata. Additions require real source links, explicit source category, coding purpose, verified year/author details and a scoped validation gate. Run the offline matrix consistency test before publication. Never import private study data or legacy repository history into this literature section.
