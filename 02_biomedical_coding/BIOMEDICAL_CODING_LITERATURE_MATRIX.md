# Biomedical Coding Literature Matrix

**Paul's Notes** | Independent, source-linked methods and software literature  
**Author:** Paul Skeffington · **Prepared with OpenAI**  
**Reviewed:** October 15, 2026 · **71 sources across 15 areas**

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

## Reconciled additions from the private research matrix

These new entries were drawn from the earlier independently authored HSE literature registers. Their reference identities were checked against journal/publisher or primary bibliographic information; implementation practices and tests below are new summaries rather than copied passages. The [source reconciliation ledger](LEGACY_SOURCE_RECONCILIATION.md) records original file IDs and deduplication.

### Scientific visualization (19 added)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-042 | [Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods](https://doi.org/10.1080/01621459.1984.10478080) · Cleveland; McGill (1984) | Experimental methods | Prefer quantitative comparison through aligned position rather than unnecessary visual encodings | Compare slopes, points and color encodings for unambiguous units and comparable scales | Perceptual accuracy varies by encoding |
| BM-043 | [A Layered Grammar of Graphics](https://doi.org/10.1198/jcgs.2009.07098) · Wickham (2010) | Methods framework | Declare aesthetic mappings, geometry, statistical transform and scales explicitly | Generate a fixed fixture plot and verify displayed mapping against source columns | Visual consistency is not inference validity |
| BM-044 | [Welcome to the Tidyverse](https://doi.org/10.21105/joss.01686) · Wickham; Averick; Bryan et al. (2019) | Software ecosystem | Record data transformations and package versions in the plotting pipeline | Test join cardinality and output schema before creating plots | Software ecosystem does not provide analysis design |
| BM-045 | [Beyond Bar and Line Graphs: Time for a New Data Presentation Paradigm](https://doi.org/10.1371/journal.pbio.1002128) · Weissgerber; Milic; Winham; Garovic (2015) | Empirical research and perspective | Include individual observations where the number and privacy of units allow it | Verify paired/independent IDs and denominators before plotting raw values | Mean-only bar graphs can conceal distributions |
| BM-046 | [Reveal, Don't Conceal: Transforming Data Visualization to Improve Transparency](https://doi.org/10.1161/CIRCULATIONAHA.118.037777) · Weissgerber; Winham et al. (2019) | Methods review | Show raw data, paired relationships and uncertainty with study-aware graphics | Check true sample size, missingness and grouping labels on rendered figure | Apparent replication may hide nested samples |
| BM-047 | [Raincloud plots: a multi-platform tool for robust data visualization (version 2)](https://doi.org/10.12688/wellcomeopenres.15191.2) · Allen; Poggiali; Whitaker et al. (2019) | Visualization method | Combine raw values, density and distribution summary without double counting | Confirm each point and distribution summarize the same valid study units | Small-sample density may mislead |
| BM-048 | [Moving beyond P values: data analysis with estimation graphics](https://doi.org/10.1038/s41592-019-0470-3) · Ho; Tumkaya; Aryal et al. (2019) | Perspective and method | Show effect sizes alongside uncertainty, not dichotomous significance alone | Validate contrast orientation, estimator, CI method and paired structure | Confidence intervals require appropriate assumptions |
| BM-049 | [Visualizations with statistical details: The ggstatsplot approach](https://doi.org/10.21105/joss.03167) · Patil (2021) | Software paper | Link descriptive display to declared inferential test and its assumptions | Confirm plot annotations match tested model and multiplicity handling | Automatic annotations can conceal invalid test choice |
| BM-050 | [ggdist: Visualizations of Distributions and Uncertainty in the Grammar of Graphics](https://doi.org/10.1109/TVCG.2023.3327195) · Kay (2024) | Software method | Show intervals and estimated distribution rather than a single point estimate | Compare interval labels, tail probabilities and estimand to test fixture | Ambiguous intervals or uncertainty type |
| BM-051 | [colorspace: A Toolbox for Manipulating and Assessing Colors and Palettes](https://doi.org/10.18637/jss.v096.i01) · Zeileis; Fisher; Hornik et al. (2020) | Software method | Use ordered palettes for ordered values and diverging scales with meaningful midpoint | Inspect grayscale and color-vision simulations at final export size | Palette color order may imply nonexistent structure |
| BM-052 | [The misuse of colour in science communication](https://doi.org/10.1038/s41467-020-19160-7) · Crameri; Shephard; Heron (2020) | Perspective | Avoid misleading nonuniform colorscales; provide accessible print-safe legends | Check monotonic perceptual luminance and threshold semantics | Rainbow color scales can introduce artificial boundaries |
| BM-053 | [A checklist for designing and improving the visualization of scientific data](https://doi.org/10.1038/s41556-025-01684-z) · Jambor (2025) | Comment and checklist | Review legibility, visual hierarchy, axes and annotations at final output size | Render and inspect labels, padding and readable type at print dimensions | Checklist is not a substitute for review of statistical design |
| BM-054 | [What is a Good figure: Scoring of biomedical data visualization](https://doi.org/10.1371/journal.pone.0336917) · Torres; Ozturk; Fang et al. (2025) | Empirical and proposed scoring method | Treat automated figure scores as exploratory feedback alongside human review | Compare score behavior with independent visual and statistical-quality judgments | Proposed score is not a universally accepted quality metric |
| BM-055 | [Ten simple rules for designing graphical abstracts](https://doi.org/10.1371/journal.pcbi.1011789) · Jambor; Bornhäuser (2024) | Perspective and design guidance | Convey scientific question and main relationship without inserting uncited data | Check terms, causal claims, visual hierarchy and attribution | Graphical abstract is not a substitute for methods/results |
| BM-056 | [Reproducible Summary Tables with the gtsummary Package](https://doi.org/10.32614/RJ-2021-053) · Sjoberg; Whiting; Curry et al. (2021) | Software paper | Generate data- and model-derived manuscript tables without manual retyping | Validate denominators, units, confidence intervals, p-value corrections and headers | Default tables can conceal eligibility and missingness rules |
| BM-061 | [effectsize: Estimation of Effect Size Indices and Standardized Parameters](https://doi.org/10.21105/joss.02815) · Ben-Shachar; Lüdecke; Makowski (2020) | Software paper | Report effect estimates and confidence intervals on a declared scale | Match standardization, formula, estimand and CI procedure | Effect size is not itself a clinical utility estimate |
| BM-062 | [Showing the data in published biology research](https://doi.org/10.1128/mbio.00572-26) · Freeman; Haldopoulos et al. (2026) | Perspective with empirical audit | Prefer distribution-revealing plots where they suit experimental design | Check unit-of-analysis, duplicate measurements and raw-value disclosure boundaries | Mean-and-error-only plots obscure variation |
| BM-063 | [Graphic Portrayal of Studies With Paired Data: A Tutorial](https://doi.org/10.1016/j.annemergmed.2017.05.033) · Schriger (2018) | Tutorial | Visualize within-person change without breaking match links | Assert each subject-pair mapping and denominator before drawing lines | Group-only summaries can hide discordant responses |
| BM-070 | [Graphs in Statistical Analysis](https://doi.org/10.2307/2682899) · Anscombe (1973) | Methods demonstration | Inspect scatter and residual geometry before interpreting numeric summaries | Generate toy datasets with identical moments and different visible relationships | Summary-only assessment can conceal structure |

### Genomic visualization (1 added)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-057 | [Complex heatmap visualization](https://doi.org/10.1002/imt2.43) · Gu (2022) | Protocol and software review | Make heatmap design, multiomic annotations and clustering reproducible | Test dimension labels, order, colors and scaling in exported files | Row z-scores may be confused with expression magnitude |

### Clinical model evaluation (5 added)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-058 | [pROC: an open-source package for R and S+ to analyze and compare ROC curves](https://doi.org/10.1186/1471-2105-12-77) · Robin; Turck; Hainard et al. (2011) | Software paper | Construct ROC analyses with declared event direction and held-out predictions | Check positive class, CI and threshold definitions against known scores | In-sample ROC overstates external performance |
| BM-059 | [plotROC: A Tool for Plotting ROC Curves](https://doi.org/10.18637/jss.v079.c02) · Sachs (2017) | Software paper | Present threshold-oriented ROC figures with informative axes and labels | Confirm axes, event definition, thresholds and uncertainty labels | Visually polished ROC does not establish clinical usefulness |
| BM-060 | [Statistical methods for assessing agreement between two methods of clinical measurement](https://doi.org/10.1016/S0140-6736(86)90837-8) · Bland; Altman (1986) | Statistical method | Use difference-against-mean plots and prespecified agreement limits | Test paired identities, signed bias, repeatability and limits calculations | Correlation is not measurement-method agreement |
| BM-066 | [Assessing the Performance of Prediction Models: A Framework for Traditional and Novel Measures](https://doi.org/10.1097/EDE.0b013e3181c30fb2) · Steyerberg; Vickers; Cook et al. (2010) | Methods paper | Evaluate calibration, discrimination, accuracy and decision usefulness as distinct outputs | Report Brier/discrimination/calibration on held-out observations | One metric cannot summarize all clinical performance |
| BM-067 | [Decision Curve Analysis: A Novel Method for Evaluating Prediction Models](https://doi.org/10.1177/0272989X06295361) · Vickers; Elkin (2006) | Methods paper | Compute net benefit for a specified decision, event and threshold range | Check threshold bounds, event definition and treat-all/none baselines | Decision curve without defensible decision thresholds |

### Single-cell methods (1 added)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-064 | [Statistical method scDEED for detecting dubious 2D single-cell embeddings and optimizing t-SNE and UMAP hyperparameters](https://doi.org/10.1038/s41467-024-45891-y) · Xia; Lee; Li (2024) | Statistical method | Check embedding fidelity and sensitivity rather than treating UMAP distances as truth | Repeat embeddings across settings and assess neighborhood/stability metrics | 2D clusters can misrepresent original high-dimensional relations |

### Quantitative bioimaging (1 added)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-065 | [A biologist's guide to planning and performing quantitative bioimaging experiments](https://doi.org/10.1371/journal.pbio.3002167) · Senft; Diaz-Rohrer et al. (2023) | Methods essay | Preserve acquisition, image processing, sampling and segmentation provenance | Review field/cell/specimen nesting and segmentation QC | Counting cells as independent biological replicates |

### Prediction validation (1 added)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-068 | [No free lunch theorems for optimization](https://doi.org/10.1109/4235.585893) · Wolpert; Macready (1997) | Theory | Document inductive assumptions and compare baselines for target problem | Define data-generating/task assumptions before choosing algorithms | Optimization theory should not be generalized as an empirical clinical model ranking |

### Data stewardship (1 added)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-069 | [Data Organization in Spreadsheets](https://doi.org/10.1080/00031305.2017.1375989) · Broman; Woo (2018) | Methods paper | Use validated rectangular tables, dictionaries and stable typed identifiers | Check date parse, one-cell-one-value and unique row/unit meaning | Spreadsheet formatting is not data semantics |

### Reproducibility (1 added)

| ID | Publication and contributors | Evidence class | Coding practice | Verification | Failure mode |
| --- | --- | --- | --- | --- | --- |
| BM-071 | [Reproducibility and Replicability in Science](https://doi.org/10.17226/25303) · National Academies of Sciences, Engineering, and Medicine (2019) | Consensus report | Separate computational replay from independent empirical replication | Record repeated-run results and clarify which evidence has been independently collected | Reproducible code can reproduce an incorrect conclusion |

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

The CSV is canonical for IDs and bibliographic metadata. Imported-source correspondence is separately recorded in the [source reconciliation ledger](LEGACY_SOURCE_RECONCILIATION.md). Additions require real source links, explicit source category, coding purpose, verified year/author details and a scoped validation gate. Run the offline matrix consistency test before publication. Never import private study data or legacy repository history into this literature section.
