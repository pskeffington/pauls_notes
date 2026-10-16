# Rust ML search and appraisal record — 2026-10-16

[Review and book applications](../rust-ml-literature.md) · [Structured register](rust-ml-sources.csv) · [Publication bibliography](rust-ml-references.bib)

## Question and window

Which approximately five-year primary research and software sources help us deliver or train the book's breast cancer teaching models in Rust, while retaining the correct observation unit, numerical behavior and assessment boundaries? The publication window is 2021-10-16 through 2026-10-16. Software snapshots are current primary implementation evidence, with their own source type; they are not papers from the five-year window.

This is a focused narrative/scoping review conducted by source search, selected full-text appraisal and reference follow-up. It has no preregistered systematic-review protocol, exhaustive database coverage, independent duplicate screening or pooled effect estimate. Search-engine discovery supplied candidates; author/publisher manuscripts, institutional repositories, DOI metadata and upstream source supplied the evidence. English-language review and accessibility introduce selection limits. Counts below describe included records, not a PRISMA retrieval flow.

## Searches actually used

Representative queries issued on 2026-10-16 included:

- `Rust machine learning framework Burn research paper arxiv 2023 2024 2025`
- `Rust machine learning linfa smartcore paper 2021 2022 2024`
- `Rust reinforcement learning Border library paper`
- `machine learning Rust biomedical research paper Candle 2024 2025`
- `"Rust" "deep learning" benchmark "2025" paper`
- `SnapATAC2 Rust 2024 Nature Methods`
- `"Rust" "TinyML" paper 2024 2025`
- `"Rust" "automatic differentiation" paper Enzyme 2021 2024 2025`
- `"Performance Evaluation of Machine Learning Applications Using WebAssembly" 2025 doi`
- Exact-title searches for Enzyme, MOLPIPx, ad-trait and Ariel-ML publication identities.

Two search engines were used to improve recall. Citation follow-up from the bindings and differentiation papers supplied additional candidate versions. Crossref's primary DOI records were queried at `https://api.crossref.org/works/{DOI}` for all ten included journal/conference items. The actual reviewed PDF URLs, versions and SHA-256 values are in the register. No full publication PDF, dataset, external source tree or model weight is redistributed in this repository.

## Inclusion and source classification

Include a primary study with an identifiable Rust-language implementation, a direct Rust binding/runtime experiment, a Rust-enabling numerical method, or an independent biological-method benchmark needed to appraise a reviewed Rust-backed tool. Read the selected methods, relevant results and limitations. Record the role precisely: direct native inference, hybrid runtime, software ecosystem study, compiler capability or biomedical representation. Do not convert all roles into native-Rust training evidence.

The included research set has **six journal articles, four conference/workshop papers and one preprint experience report**, all with selected full-text review. Six current upstream files were independently inspected: Linfa logistic code, SmartCore logistic code, Burn/Candle MNIST training examples, ort session code, and experimental Rust compiler autodiff documentation. These source inspections were read only. None was built, installed, trained or benchmarked in this review.

The two ASGAARD binding papers share a research program and are not independent clinical cohorts. The register uses the same family label for them. No study-level effects, participant totals or timing ratios are pooled.

## Version and duplication decisions

| Candidate versions | Decision |
| --- | --- |
| Enzyme 2020 paper and SC 2021 GPU extension | Include the eligible 2021 extension; the 2020 paper is background, not a recent included record |
| Binding ecosystem manuscript 2022 / revised journal article 2024 | One RML-P02 record, using the 2024 v2 manuscript and final DOI; do not mix the older manuscript's counts with the revision |
| MicroFlow 2024 preprint / 2025 journal | One RML-P06 record; read arXiv v3 and verify the journal identity |
| SnapATAC2 2023 preprint / 2024 journal | One RML-P04 record, using the 2024 publisher text |
| MOLPIPx 2024 preprint / 2025 journal | One RML-P07 record; selected review uses author manuscript v2, explicitly marked rather than claimed as a full published-supplement audit |
| ad-trait 2025 preprint / IROS 2025 paper | One RML-P08 record; read manuscript v1 and verify the conference DOI |
| Ariel-ML 2025 manuscript / ISIoT 2026 paper | One RML-P10 record; v2 names the workshop and the 2026 DOI/type is confirmed in Crossref |
| Adito 2026 experience report | RML-P11 is an unreplicated preprint. The retrieved PDF identifies version 1 and is dated 2026-07-27; its author page corroborates the report. The arXiv landing page was unavailable, so no independently confirmed submission-date claim is made |

A version pin identifies the material inspected. It does not prove that a source was correct or that its environment can still be rebuilt. The six framework/compiler pins are October 2026 review snapshots, not the paper-era releases and not new dependencies of the existing Rust CLI.

## Important exclusions and scope limits

| Candidate | Reason it is not counted as Rust ML implementation evidence |
| --- | --- |
| Crop “rust” disease classifiers | The word describes a plant disease, not the programming language |
| RUST single-cell representation project acronym | The name alone does not establish a Rust-language implementation |
| Cancer CANDLE/Supervisor work | Distinct software/project identity from Hugging Face Candle; do not conflate them |
| Rust repair/proof/code-generation benchmarks | ML applied to Rust code is a different question from training/executing biomedical models in Rust |
| JMLR 2026 *A Common Interface for Automatic Differentiation* | The reviewed abstract describes a Julia package; it is not direct Rust implementation evidence |
| Unverified framework ranking posts and duplicate forks | Secondary discovery sources or duplicates; primary artifacts and papers carry the recorded claims |

No included source establishes clinical validity of our assay CLI. The single-cell methods inform representation and cell composition, not a validated breast-cancer patient endpoint. MCU, robotics, molecular-energy and language-model workloads require explicit transfer arguments. The review's proposed training, gradient, single-cell and device experiments remain proposals; existing synthetic runtime-parity results retain their own separate [validation record](rust-validation-2026-10-16.json).
