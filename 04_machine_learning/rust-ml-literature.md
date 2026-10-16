# Rust machine learning: evidence and the breast cancer workflow

[ML subjects](README.md) · [Working Rust deployment](rust-deployment.md) · [Breast cancer book, Chapter 11](../06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md#applying-machine-learning-to-breast-cancer-data) · [Source register](evidence/rust-ml-sources.csv) · [BibTeX](evidence/rust-ml-references.bib) · [Search and appraisal record](evidence/rust-ml-search-2026-10-16.md)

Reviewed through **2026-10-16**, targeting the approximately five-year interval **2021-10-16 to 2026-10-16**. This focused literature review contains **11 distinct publications/manuscripts: six journal articles, four conference/workshop papers and one experience-report preprint**. It also records **six separate upstream software/documentation inspections** at immutable commits. Framework source files are not counted as academic papers. The existing [36-source breast cancer/methods corpus](breast-cancer-evidence.md) retains its own register and appraisal history.

Selected full-text methods, relevant results and limitations were read for all 11 papers; the register identifies the actual PDF/manuscript version, sections, SHA-256, publication identifier and project action. Ten publication identities/types were checked against Crossref metadata. Some reviews use author manuscripts rather than publisher PDFs. This is a targeted narrative/scoping review, with English-language sources and citation follow-up; it is not exhaustive or a systematic-review estimate of all Rust ML work. No external paper experiment was reproduced during this literature-review pass. The later [G3 native baseline](rust-native-training.md) executes the published Linfa 0.8.1 crate under its own frozen contract; its [source addendum](rust-training-source-addendum.md) distinguishes that release from the newer development source inspected here. Historical register execution states refer to this review, not the later baseline.

## What the evidence supports for this book

Rust has several distinct roles: executing a frozen model, fitting a model through a library, orchestrating a native runtime, accelerating a Python-facing scientific tool, and calculating derivatives. A result in one role does not establish performance in another. The reviewed material supports explicit interfaces, version control and measurement at these boundaries. It does **not establish patient-level breast cancer validation for our Rust deployment**, or that Rust alone improves a model's discrimination, calibration or biological interpretation.

Our current executable case asks whether 48 invented continuous measurements distinguish a recorded specimen category for people excluded from training. There are 60 people with paired specimens, 45 development people and 15 reserved people. The book's 60 named genes are a teaching catalog, not the runner's predictors. The [Rust CLI](rust-deployment.md) replays both final-development logistic procedures; its successful probability comparisons are software evidence. The gallery's outer-held-out predictions continue to assess the training procedure.

| Book question | Relevant evidence | Application and boundary |
| --- | --- | --- |
| Can a trained procedure travel between runtimes? | [Binding experiments](#rml-p03), [binding maintenance](#rml-p02), [ort source](#rml-s05) | Carry medians, feature order, scales, coefficients and class identity together; compare individual probabilities before measuring speed |
| Can Rust fit our small assay baseline? | [Linfa](#rml-s01), [SmartCore](#rml-s02) | Declare the optimization objective and grouped folds; native baseline now implemented under its [own contract](rust-native-training.md) |
| What can single-cell representations tell us about a tissue? | [SnapATAC2](#rml-p04), [independent chromatin benchmark](#rml-p05) | Preserve cell-to-specimen-to-person links; representation quality is separate from held-out-person prediction |
| How would a new training engine be checked? | [Enzyme](#rml-p01), [ad-trait](#rml-p08), [MOLPIPx](#rml-p07), [training experience](#rml-p11) | Check expected derivative paths, numerical agreement, optimizer updates and checkpoint replay on controlled fixtures |
| Would browser or small-device delivery help? | [WASM comparison](#rml-p09), [MicroFlow](#rml-p06), [Ariel-ML](#rml-p10) | Require a deployment need, supported operations, precision/conversion checks and measurements on the actual target |
| Does any of this establish a useful breast cancer test? | The separate [clinical evidence corpus](breast-cancer-evidence.md) and [validation guidance](recent-selection-validation.md) | Define the patient population, assay, endpoint and external assessment; compiler or runtime correctness does not answer clinical usefulness |

## Synthesis: preserve the question while changing the implementation

**Start with the current frozen-model route.** The binding studies motivate checking the interface between a learned model and its execution engine. Our implementation carries over every learned preprocessing quantity and tests both procedures on the same invented inputs. Matching thresholded labels or aggregate accuracy is weaker than matching the saved probabilities used by Brier error and calibration. The old binding experiments used particular host/framework releases; their timing rankings are not a forecast for today's versions or our small logistic models.

**Make native training a separately assessed comparison.** The inspected Linfa implementation is a plausible first candidate because it exposes logistic probabilities and an explicit regularized loss. Its penalty, intercept treatment, sample weighting and convergence rules need comparison with our declared Python objective; a similarly named regularization parameter is not sufficient. Give the Rust procedure training-only imputation/scaling and the same person-grouped inner/outer boundaries. Retain the fixed all-feature and prevalence comparators. Record fits, failures, stopping, workers and elapsed time. A preferred engine need not win for the experiment to be informative.

**Treat single-cell work as a new data contract.** SnapATAC2 gives a direct example of Rust inside a biomedical analysis stack. Its matrix-free representations and the independent benchmark inform preprocessing and biological structure questions. If the book adds breast tumor single-cell measurements, retain donor, specimen, batch, cell identity, QC and assay layer. For a future unseen-person predictor, learn the representation within development and define how an excluded person's cells are mapped; fitting an embedding on everyone first changes the assessment question. Descriptive atlas exploration can use a different, explicitly stated transductive design. A visually separated cluster does not establish a patient classifier or a gene mechanism.

**Verify derivatives according to the intended computation.** Enzyme, ad-trait and MOLPIPx concern different differentiation mechanisms and workloads. The current Rust CLI needs none of them because it performs frozen inference. A future neural trainer should check finite losses and derivatives, compare selected derivatives with an analytical or finite-difference oracle, and show the expected parameters update. The single-author training report is a source of failure hypotheses, with restricted full-stack availability, rather than a controlled ranking of Burn and Candle. Its proposed universal nonzero-gradient check needs qualification: zero gradients can be valid for frozen, inactive or symmetric parameters. Use a deliberately excited test fixture and an explicit expected-gradient map instead.

**Keep compiler and native-runtime boundaries visible.** Ariel-ML combines Rust with an IREE C runtime; ort wraps ONNX Runtime; these are useful hybrid architectures. Their native components, execution providers and version compatibility belong in the provenance record. Experimental compiler autodiff requires its own supported toolchain. The working stable inference toolchain should remain reproducible while those experiments are investigated separately.

**Measure delivery after equivalence.** MicroFlow's quantized MCU inference, Ariel-ML's multicore scheduling and WASM browser/WASI experiments address deployment constraints. Their hardware, operators, preprocessing and numeric precision differ from our f64 CLI. Any f32 or integer conversion needs a newly declared tolerance and probability-error/calibration assessment; the present 1e-12 replay tolerance is not automatically transferable. Measure cold startup, CSV parsing, preprocessing and prediction separately and end to end on a fixed workload. The corpus establishes no speedup, energy reduction or memory reduction for our current deployment.

## Publication appraisals

The short cards below distinguish the authors' reported mechanism, its limits and our proposed use. All external study reproductions remain `not_run`. Related manuscripts and final publications are one source family, not additional independent studies. The two ASGAARD binding papers address related questions and are not independent clinical cohorts.

## RML-P01

**Moses et al. — Reverse-mode automatic differentiation and optimization of GPU kernels via Enzyme (2021).** [conference paper](https://doi.org/10.1145/3458817.3476165) · [Reviewed text](https://c.wsmoses.com/papers/EnzymeGPU.pdf)

**Reported mechanism:** LLVM-level differentiation generates GPU gradients; Rust is among the compatible source-language frontends. The paper enables derivative generation below a source-language API. Its GPU-kernel evaluation should not be relabeled as a clinical or Rust-only model-training result.

**Appraisal limit:** GPU-kernel results do not establish a native Rust breast-cancer training benchmark.

**Breast cancer book action:** Require analytical or finite-difference gradient checks before a separately planned native-training experiment.

## RML-P02

**Li and Bezemer — Bridging the language gap: an empirical study of bindings (2024).** [journal article](https://doi.org/10.1007/s10664-024-10570-5) · [Reviewed text](https://arxiv.org/pdf/2201.07201v2)

**Reported mechanism:** Cross-ecosystem bindings often cover limited host-library releases and lag behind upstream changes. The 2022 first manuscript and 2024 revised journal work are one record here. Bindings are an additional compatibility boundary, even when the application code compiles.

**Appraisal limit:** An ecosystem inventory does not measure Rust model accuracy or deployment speed.

**Breast cancer book action:** Pin binding, host runtime and native dependencies together; test the restored environment.

## RML-P03

**Li et al. — Studying the impact of TensorFlow and PyTorch bindings on ML software quality (2024).** [journal article](https://doi.org/10.1145/3678168) · [Reviewed text](https://arxiv.org/pdf/2407.05466v1)

**Reported mechanism:** Pretrained models retained assessed accuracy across studied bindings, while training outcomes and runtimes varied. The reviewed experiments use TensorFlow 2.5.0 and PyTorch 1.9.0. The paper explicitly notes that accuracy is only one correctness measure; our probability replay is a project-specific check.

**Appraisal limit:** Historical TensorFlow 2.5.0/PyTorch 1.9.0; accuracy agreement does not establish probability or calibration parity.

**Breast cancer book action:** Preserve our per-specimen probability comparison before any Rust runtime benchmark.

## RML-P04

**Zhang et al. — A fast, scalable and versatile tool for analysis of single-cell omics data (2024).** [journal article](https://doi.org/10.1038/s41592-023-02139-9) · [Reviewed text](https://www.nature.com/articles/s41592-023-02139-9.pdf)

**Reported mechanism:** SnapATAC2 combines Rust subroutines and a Python interface for scalable single-cell representation analysis. The paper supplies an out-of-sample embedding mechanism as well as representation analysis. A donor-held-out implementation would still need an explicit fitting and mapping protocol for its own target.

**Appraisal limit:** Cell embeddings and tissue composition do not validate a patient-level breast-cancer prediction endpoint.

**Breast cancer book action:** Define cell/specimen/donor identities and an out-of-sample representation boundary before extending the book.

## RML-P05

**Luo et al. — Benchmarking computational methods for single-cell chromatin data analysis (2024).** [journal article](https://doi.org/10.1186/s13059-024-03356-x) · [Reviewed text](https://link.springer.com/content/pdf/10.1186/s13059-024-03356-x.pdf)

**Reported mechanism:** Independent evaluation compares single-cell methods across representations, graphs and clustering metrics. The authors use SnapATAC2 2.2.0 and multiple clustering seeds. Compare representation and clustering quality separately from the later assay classifier; this is not a language-isolation experiment.

**Appraisal limit:** A method-level benchmark is not a controlled Rust-versus-Python runtime experiment.

**Breast cancer book action:** Separate biological representation quality, resource use and patient-level prediction assessment.

## RML-P06

**Carnelos et al. — MicroFlow: an efficient Rust-based inference engine for TinyML (2025).** [journal article](https://doi.org/10.1016/j.iot.2025.101498) · [Reviewed text](https://arxiv.org/pdf/2409.19432v3)

**Reported mechanism:** Compile-time model processing and quantized operators support Rust inference on constrained microcontrollers. The 2024 preprint and 2025 journal article are one family. Model/operator conversion and changed numeric precision require checks before any conclusions transfer to assay probabilities.

**Appraisal limit:** Results depend on supported operators, quantization and devices; no assay-specific clinical validation.

**Breast cancer book action:** Assess conversion and a new precision contract before any embedded version of the assay model.

## RML-P07

**Drehwald et al. — MOLPIPx: differentiable polynomials in Python and Rust (2025).** [journal article](https://doi.org/10.1063/5.0250837) · [Reviewed text](https://arxiv.org/pdf/2411.17011v2)

**Reported mechanism:** Python and Rust derivative paths support molecular potential models; reviewed Rust examples are limited to linear models. The reviewed v2 manuscript explicitly limits its Rust examples to linear models, while its broader Python examples include neural and Gaussian-process models. Preserve that distinction when describing capability.

**Appraisal limit:** Molecular energies are not breast-cancer outcomes; manuscript v2 is not a full audit of the published supplement.

**Breast cancer book action:** Keep a molecular-model learning case separate from the current tissue-category and future prognosis endpoints.

## RML-P08

**Liang et al. — ad-trait: a fast and flexible automatic differentiation library in Rust (2025).** [conference paper](https://doi.org/10.1109/IROS60139.2025.11245908) · [Reviewed text](https://arxiv.org/pdf/2504.15976v1)

**Reported mechanism:** Trait-based forward/reverse differentiation is assessed on numerical functions and robotics optimization. The reviewed preprint is linked to the verified IROS 2025 publication. Its limitation discussion identifies scalar reverse-mode memory overhead and the cost of converting existing numerical code.

**Appraisal limit:** Scalar reverse-mode overhead and integration costs limit transfer to tensor-heavy neural training.

**Breast cancer book action:** Use controlled derivative checks and record objective, precision and optimization budgets for native training.

## RML-P09

**Khan et al. — Performance evaluation of ML applications using WebAssembly across languages (2025).** [conference paper](https://doi.org/10.1145/3731545.3736817) · [Reviewed text](https://arrow.tudublin.ie/cgi/viewcontent.cgi?article=1004&context=dfrhro)

**Reported mechanism:** Logistic and clustering experiments compare Rust, Python and C++ under browser and WASI runtimes. Browser and WASI differences include dependency/toolchain availability and synthetic workloads. The authors plan real-data evaluation; do not transfer their language ranking to the breast cancer case.

**Appraisal limit:** Synthetic workloads and unequal dependency support confound broad language-speed conclusions.

**Breast cancer book action:** A browser extension needs probability parity, compatible preprocessing and a declared workload before timing.

## RML-P10

**Huang et al. — Ariel-ML: embedded Rust leveraging multicore for neural networks (2026).** [conference paper](https://doi.org/10.1109/DCOSS-IoT69657.2026.00111) · [Reviewed text](https://arxiv.org/pdf/2512.09800v2)

**Reported mechanism:** Rust orchestration combines with an IREE C runtime and multicore scheduling for MCU inference. The reviewed v2 manuscript asks readers to cite ISIoT 2026. The publication DOI/type was independently confirmed; the Rust scheduler orchestrates an IREE native runtime rather than replacing every component.

**Appraisal limit:** Hybrid runtime/device results are not evidence for a wholly Rust stack or breast-cancer model accuracy.

**Breast cancer book action:** Inventory native runtimes and hardware alongside the Rust binary before a future edge deployment.

## RML-P11

**Adito — Training a language model end-to-end in Rust: an experience report (2026).** [preprint](https://arxiv.org/abs/2609.25008v1) · [Reviewed text](https://arxiv.org/pdf/2609.25008v1)

**Reported mechanism:** One author reports backend/gradient failures and advocates explicit checks before expensive training. The PDF is version-pinned and the author page corroborates the July 2026 report; arXiv landing-page metadata could not be retrieved. Treat backend defect reports as version-specific, unreplicated observations. Nonzero gradients for every parameter are not a universal correctness criterion.

**Appraisal limit:** Unreplicated single-project preprint; full training stack/logs are on request and weights are unreleased.

**Breast cancer book action:** Check expected gradient paths and numerical agreement; nonzero gradients for every parameter are not a universal validity rule.

## Pinned software inspections

These six records concern selected upstream source or documentation, not additional academic publications. They were read at the commits in the register and were **not compiled, executed or adopted as project dependencies**. A current source snapshot does not reproduce a paper-era environment.

## RML-S01

**Linfa logistic implementation.** [Immutable source](https://github.com/rust-ml/linfa/blob/3b411a4c985cdf6b83430d9c44f11e338d300c50/algorithms/linfa-logistic/src/lib.rs); inspected 2026-10-16.

**Coding mechanism:** The inspected binary logistic implementation exposes probabilities and an explicit L2-weighted objective.

**Project action:** First native-training candidate: declare the objective and person-grouped fit contract before implementation. A source inspection does not establish successful compilation, grouped assessment or penalty equivalence to scikit-learn.

## RML-S02

**SmartCore logistic implementation.** [Immutable source](https://github.com/smartcorelib/smartcore/blob/3b62cfc969236253a8c14ad170ee36dc7904efbf/src/linear/logistic_regression.rs); inspected 2026-10-16.

**Coding mechanism:** The inspected logistic predict path returns class labels rather than a saved probability table.

**Project action:** Verify a probability interface and class direction before using this learner with Brier selection. This selected file review is not an exhaustive audit of probability interfaces throughout the crate.

## RML-S03

**Burn MNIST training example.** [Immutable source](https://github.com/tracel-ai/burn/blob/ba73ce30ea34a22606c2919c67271d56b28f1050/examples/mnist/src/training.rs); inspected 2026-10-16.

**Coding mechanism:** The example has train/validation loaders, early stopping and model/config persistence.

**Project action:** Replace row-oriented example partitions with person-grouped inner training/validation slices. MNIST partitions and stopping rules do not supply donor-grouped assay validation.

## RML-S04

**Candle MNIST training example.** [Immutable source](https://github.com/huggingface/candle/blob/12bb5d1f6350f4ea9827d9086f213feec1f0af6a/candle-examples/examples/mnist-training/main.rs); inspected 2026-10-16.

**Coding mechanism:** The example makes optimization and persistence explicit and reports MNIST test accuracy each epoch.

**Project action:** Monitor an inner validation set; reserve final-test people until all stopping and model choices are frozen. Copying per-epoch test monitoring into the protected assay test would compromise its role if used for choices.

## RML-S05

**ort session implementation.** [Immutable source](https://github.com/pykeio/ort/blob/60cbb73dc911d02e42dd54bf0bda60b77d5f3602/src/session/mod.rs); inspected 2026-10-16.

**Coding mechanism:** Session runs an ONNX graph through a native ONNX Runtime interface.

**Project action:** Require end-to-end preprocessing conversion, runtime pinning and per-specimen probability parity. Our current numeric JSON is not an ONNX model; graph conversion and runtime support remain untested.

## RML-S06

**Rust unstable autodiff compiler documentation.** [Immutable source](https://github.com/rust-lang/rust/blob/bf9448e42622eaba63ebc171bb4584cea22210b4/src/doc/unstable-book/src/compiler-flags/autodiff.md); inspected 2026-10-16.

**Coding mechanism:** The documentation describes experimental compiler differentiation with an Enzyme-capable toolchain.

**Project action:** Keep compiler experiments in a separate declared environment; retain the working inference deployment. This is not enabled by the repository's pinned stable Rust inference toolchain.

## A bounded route from reading to implementation

| Priority | Proposed work | Evidence needed before calling it complete | Current status |
| --- | --- | --- | --- |
| Preserve deployment replay | Retain the two frozen procedures, ordered schema and numerical probes | Existing Rust/Python parity and artifact identities | Implemented in the [Rust deployment](rust-deployment.md); no new benchmark in this review |
| Extend training carefully | One declared native Linfa logistic baseline alongside the present Python procedures | Person-disjoint nested indices; training-only transforms; complete probability and convergence records | [Linfa baseline implemented and numerically checked](rust-native-training.md); SmartCore remains unexecuted |
| Check robustness and compute | Follow the [stability/tuning-budget phase](../docs/learning-roadmap.md#phase-4-study-robustness-before-making-search-more-elaborate) | Prespecified perturbations, budgets and unfavorable results retained | [G1/G2](../docs/roadmap-gates.md) complete within their declared synthetic scope; runtime language does not extend uncertainty coverage |
| Introduce cell-level data deliberately | A separate synthetic cell/specimen/donor fixture informed by the two single-cell papers | Aligned identity/QC contract; development-fitted representation and excluded-donor mapping | Reference design; no single-cell package deployment added |
| Add neural or edge methods only for a defined question | A bounded training or target-device experiment | Gradient/update/checkpoint checks, conversion/precision protocol and appropriate assessment | Reference; no Burn/Candle, ONNX, WASM or MCU benchmark executed |

The [reader's ML introduction](what-is-machine-learning.md), [algorithm guide](basic-algorithms.md), [tuning contract](model-tuning.md), [visual gallery](gallery/README.md) and [comparison protocol](comparison-protocol.md) remain the practical learning route. Connect a Rust package to those contracts before adding complexity. Recurrence, treatment response and molecular potential fitting each require their own endpoint and data meanings.

## Audit and repeat the integrity checks

```bash
python3 scripts/check_rust_ml_evidence.py
python3 scripts/tests/test_rust_ml_evidence.py
python3 scripts/check_ml_evidence.py
python3 scripts/check_documentation.py
```

The checks enforce source types, dates, identifiers, immutable inspected-source revisions, hashes, exact card/bibliography coverage and links to project applications. They challenge unbacked execution/clinical-validation claims and malformed records. They do not establish that a study's scientific conclusions are true, reproduce a benchmark or replace human appraisal. The [dated integrity record](evidence/rust-literature-validation-2026-10-16.json) records this pass; the [search log](evidence/rust-ml-search-2026-10-16.md) preserves selection/version decisions and remaining limits.
