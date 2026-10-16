# Paul's Notes

**Biomedical research, scientific computing, and reproducible analysis**

Authored by Paul Skeffington · Compiled with OpenAI

A reference collection connecting biological questions with data preparation, statistical reasoning, machine learning, and research software.

## Start here

- **[Breast cancer research guide](06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md)** — Twelve chapters connecting people, specimens, molecular measurements, biological processes, and 60 gene profiles.
- **[Computing and statistics](03_learning/README.md)** — Subject guides with worked examples for R, data preparation, study design, models, and figures.
- **[Machine learning](04_machine_learning/README.md)** — A reader's introduction, basic algorithms, package guidance, and runnable R and Python workflows.

## Explore the collection

| Area | Guide | Coverage |
| --- | --- | --- |
| Unix and Bash | [Command-line computing](01_unix_bash/README.md) | Files, text processing, scripting, and automation |
| Research methods | [Biomedical coding and literature](02_biomedical_coding/README.md) | Publications, package documentation, and implementation requirements |
| Genomics | [Molecular research resources](06_RESOURCES/Genomics/README.md) | Gene function, expression interpretation, pathways, and evidence |
| Visualization | [R tools and plotting](06_RESOURCES/R/README.md) | Summaries, statistical graphics, annotations, and reusable functions |
| Scientific writing | [Manuscript and bibliography tools](06_RESOURCES/LaTeX/README.md) | Manuscript preparation and reference management |
| Resource directory | [Browse by research task](docs/resource-guide.md) | Documentation, methods, and supporting tools across the collection |

## Put the methods to work

- [Plan a research workflow](docs/research-workflow.md) — Define the question, document inputs, and organize a reproducible analysis.
- [Apply machine learning to breast cancer data](06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data) — Connect specimen identity, gene measurements, model choices, and evaluation.
- [Read the breast cancer ML evidence](04_machine_learning/breast-cancer-evidence.md) — Connect specific screening, risk, prognosis, and treatment-response studies to implementation choices.
- [Inspect the corpus review and validation run](04_machine_learning/corpus-review.md) — Review paper-level findings, unresolved access, published-output checks, and synthetic verification.
- [Understand model tuning](04_machine_learning/model-tuning.md) — Inspect this project's search grids, candidate scores, training budget, and evidence for sound assessment, with recent evidence on [tuning](04_machine_learning/recent-tuning-evidence.md) and [selection and validation](04_machine_learning/recent-selection-validation.md).
- [Train with selected assay measurements](04_machine_learning/advanced-breast-cancer-training.md) — Follow the breast cancer narrative through nested training, smaller feature sets, and careful interpretation of variable importance.
- [Run independent R and Python methods](04_machine_learning/methods-and-deployments.md) — Explore classification, regression, clustering, survival, and expression analysis.
- [Check understanding and implementation](03_learning/mastery-checks.md) — Inspect expected results, failure cases, and interpretation tasks.

The [assay comparison](04_machine_learning/model-comparison.md) adds a fixed all-feature baseline on matched people; its [plotting gallery](04_machine_learning/gallery/README.md) follows data allocation, missingness, tuning, feature summaries, probability errors and calibration through seven reproducible figures.

The [Rust deployment](04_machine_learning/rust-deployment.md) runs both frozen assay models as a compiled prediction CLI, carrying over learned preprocessing and checking probabilities against Python. The [five-year Rust ML review](04_machine_learning/rust-ml-literature.md) connects 11 publications/manuscripts and six software inspections to the breast cancer workflow. The [native Rust training baseline](04_machine_learning/rust-native-training.md) now fits a declared logistic objective with training-only preparation and matched Python numerical checks.

For a visual introduction, [follow data through machine learning](04_machine_learning/visual-data-guide.md): see the training slices, validation folds, grouped records, and protected final test.

The [Phase 4 assay robustness gate](04_machine_learning/robustness-experiment.md) adds four prespecified synthetic stress scenarios, paired development-only assessment and a bounded six-candidate randomized tuning comparison; it does not establish clinical or independent validation.

Follow the [learning roadmap](docs/learning-roadmap.md) for the next phases: data meaning, fair comparisons, visual interpretation, robustness, survival methods and a reproducible capstone.

The [milestone gate ledger](docs/roadmap-gates.md) records delivery evidence and open dependencies. The [Phase 4B replication](04_machine_learning/replication-experiment.md) assesses three prespecified synthetic cohort draws across 12 cells. The [Phase 4C uncertainty assessment](04_machine_learning/uncertainty-assessment.md) adds whole-person conditional ranges on their saved predictions, with complete draw records and verified replay. The defined synthetic Phase 4 milestone is complete. Native Rust fitting adds scoped numerical validation; a separate survival endpoint and Cox assessment protocol are next.

## TCGA-BRCA data protection and model use

The [research privacy and model-use policy](04_machine_learning/research_toolkit/MODEL_USE_POLICY.md) requires per-file GDC open-access verification for future TCGA-BRCA work, prohibits direct identifiers and controlled-access files, keeps participant records and predictions out of Git, and disclaims diagnostic, prognostic or treatment use. The [repository data guard](scripts/check_public_data_boundaries.py) runs in a dedicated pull-request workflow. The [configuration-driven ML toolkit](04_machine_learning/research_toolkit/README.md) is currently synthetic-only; official GDC metadata access checking is a separate read-only preflight.

## Research templates

- [Study protocol](templates/study-protocol.md) — Research question, study design, and analysis plan.
- [Data dictionary](templates/data-dictionary.md) — Identifiers, field definitions, units, and missing values.
- [Analysis record](templates/analysis-record.md) — Inputs, decisions, execution, and results.

---

[Gene lookup](06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#alphabetical-gene-lookup) · [All resources](06_RESOURCES/README.md) · [Contributing](CONTRIBUTING.md) · [License](LICENSE)
