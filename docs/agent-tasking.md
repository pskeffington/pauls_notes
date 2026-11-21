# Agent task queue and roadmap — 2026-10-30

[Repository overview](../README.md) · [Agent contract](../AGENTS.md) · [Textbook roadmap](../oncology/ROADMAP.md) · [Book manifest](../oncology/book-manifest.json) · [Machine-index contract](machine-index.md) · [Milestone evidence](roadmap-gates.md)

This is an **execution queue**, not a claim of implementation. It defines proposed next passes against the inspected `main` tree on 2026-10-30. Preserve recorded gate histories; recheck current code, CI and open PRs at execution time. Agent tasks are independently scoped and may proceed in parallel only where dependencies do not overlap.

## Status vocabulary
- **Ready**: definition and upstream artifacts available; execution not yet verified.
- **Planned**: requires further specification or an upstream gate.
- **Blocked**: operation prohibited until its stated prerequisite is met.
- **In progress**: a branch/PR exists, not a pass.
- **Verified**: reviewed artifact, reproducible checks and acceptance evidence recorded; never infer from prose.

## Ordered tasks

| ID | Priority | Status at queue creation | Task | Acceptance gate |
| --- | --- | --- | --- | --- |
| IDX-01 | P0 | **Verified (bounded)** — full index and orphan audit passed | Audit links, headings, duplicate section IDs, orphaned pages and indexing coverage across textbook and learning resources | Record baseline diagnostics and proposed repairs; determinism and existing machine-index tests pass |
| IDX-02 | P0 | **Verified (bounded)** — deterministic registry, graph and CI checks passed | Add machine-readable agent task registry or verified task export, aligned to this human queue | Stable IDs, dependencies, statuses, owner-less handoffs, schema tests and deterministic output |
| DOC-01 | P0 | Ready | Reconcile chapter statuses and navigation against the 60-entry book manifest and actual files | No chapter marked drafted without manuscript; README, oncology/README, llms.txt, registry and manifest cross-links agree |
| DOC-02 | P1 | Ready | Develop the applied data-science introduction as a breast-cancer research narrative, integrating existing lessons into ordered chapters | Draft original chapter bridges, keep a single declared research question and data provenance across examples, include objectives/worked examples/exercises/interpretation/limitations, and preserve separate source, runtime and clinical evidence statuses |
| CO-07 | P1 | Ready for authored draft; not delivered | Author original Ch. 07 probability and Bayes in oncology, with independent synthetic worked examples | Section citations, numerical R/Python replay where appropriate, clinical interpretation, exercises, limitations, editorial validation |
| CO-08 | P1 | Planned after CO-07 conventions | Ch. 08 discrete outcomes: binomial, hypergeometric, Poisson, denominators and rates | Distribution-selection casework, independently checked numeric examples, source references and mastery checks |
| CO-09 | P1 | Planned after CO-07 conventions | Ch. 09 continuous outcomes and transformations | Normal/log-normal and zeros, shape vs sampling distribution/CLT, worked reproducible examples |
| CO-10 | P1 | Planned after CO-07–09 | Ch. 10 sampling, standard error and resampling | Separate population-vs-sample and independent-vs-clustered sampling contracts; verified examples |
| G4-01 | P1 | Planned; protocol exists | Implement *synthetic only* survival protocol with Cox/KM, 24-month censoring-adjusted Brier computation | Freeze then replay event/censoring schema; independent numeric references; no protocol drift, no clinical claim |
| G5-01 | P2 | Planned after relevant method | Specify and reproduce a bounded published numerical result | Permitted source, target result, versioned analysis, independent reviewer replay |
| GOV-01 | P0 safety | Blocked for real data | Verify D0 public Git data-safety controls and D1 independently approved real-data admission | Review actual PR/status, secret/privacy scans and human approvals; do not promote draft to merged or metadata review to participant authorization |
| QA-01 | P1 | Ready | Establish chapter-level citation and numerical exercise regression report, without changing science gate claims | Tests discover actual sections and exercise artifacts, report missing references as missing, avoid fabricated coverage |
| REL-01 | P2 | Planned after document/index audits | Assemble publication-ready accessible ebook navigation and export reproducibility | Accessible section hierarchy, numbered chapters, navigation, source audit, independently replayed build |

## First executable pass
Begin with **IDX-01 + DOC-01 as a documentation-only audit**. Inventory the tracked tree; compare `oncology/book-manifest.json` against `oncology/chapters/`; inspect source crosswalks, `llms.txt`, `README.md`, `docs/research-method-map.json` and index-builder diagnostics. Produce a concise evidence report with path-level discrepancies. Repair only confirmed broken routes/metadata; do not blanket-change milestone status or alter the clinical content. Then implement IDX-02 with a deterministic registry if the audit confirms its requirements.

## Dependency and ownership rules
- IDX-01 → IDX-02; DOC-01 → REL-01.
- CO-07 establishes chapter format for CO-08/CO-09; CO-07–09 → CO-10; content chapters do not require G4 research success.
- G4-01 follows its frozen synthetic survival protocol; G5-01 follows an independently selected method/result.
- GOV-01 blocks all proposed admission of real participant-linked data, **not** synthetic textbook development.
- DOC-02 uses synthetic and source-verified breast-cancer examples; chapter integration does not depend on admitting real participant data.
- No task is complete from AI-generated text alone: demand tests or checkable review evidence matching its scope.
- Keep broad cancer scope; use breast cancer as an explicit example rather than defaulting every chapter to BRCA.
- For each pass, update this queue, affected navigation and documented evidence together. Annotate the actual date, branch/PR and observed checks rather than changing historical gate snapshots without verification.

## Index and handoff output expected from an agent
At minimum: `task_id`, `state`, `depends_on`, `affected_paths`, `input_provenance`, `test_commands`, `observed_results`, `evidence_links`, `limitations`, `next_task`. For machine retrieval, preserve source path, heading identifier, content hash and exact version/commit in downstream ingestion. An indexed reference is a search aid, not a verified scientific citation.

## 2026-10-30 audit checkpoint and machine registry

- Inspected the tracked Git tree at the documentation branch: **341 files**. Compared all entries of `oncology/book-manifest.json` to tracked paths: **60 chapters, six drafts, 54 planned**; no missing draft manuscripts, no planned chapters with a manuscript path, and no missing declared lab/test paths. This closes **only the manifest path-integrity subcheck** of DOC-01; full reader navigation, citations, and runtime tests remain open.
- Added [structured task registry](agent-tasks.json) and [offline graph/manifest validator](../scripts/check_agent_tasks.py) for IDX-02. Static source review is not a successful execution or CI report; state remains **in progress**.
- Run `python3 scripts/check_agent_tasks.py` and existing machine-index tests before promotion. Resolve any discovered mismatch, and record actual command output plus commit SHA in review evidence.
- IDX-01 requires executed link/heading/coverage diagnostics and orphan report, not just this path check. Keep IDX-01 **in progress** and IDX-02 dependent on it until index coverage and orphan candidate diagnostics are reviewed.

## 2026-10-30 CI validation and retrieval-coverage pass

- On commit `0c6181b81aff00a7df683994bd7c66e6ab883832`, [machine-index run 41024862009](https://github.com/pskeffington/pauls_notes/actions/runs/41024862009) **passed** its full job, including task registry tests, textbook manifest, section citations, CO-05/CO-06 R/Python exercises, index generation, deterministic enrichment and JSONL identity checks. This evidence establishes that commit's CI result, **not** all subsequent changes.
- The earlier zero-job startup failures stopped after replacing mutable setup actions with the pinned checkout pattern and base R installation. The original cause could not be established from zero-job runs; do not assert a definitive GitHub Actions policy violation.
- Eight bibliography links already registered in `oncology/evidence/source-registry.json` were added to `oncology/evidence/SOURCES.md`. This is link reconciliation, not independent scientific review.
- IDX-01 now includes [index coverage/orphan audit](../scripts/audit_machine_index.py) and [regression tests](../scripts/test_audit_machine_index.py). A new CI step checks path-level coverage and preserves a review-only orphan candidate report. Orphan candidates are **not** automatically missing or erroneous documents; inspect navigational intent and `llms.txt` before changes.
- **Remaining acceptance:** observe the updated CI run on the new head; inspect any orphan candidates, document any legitimate direct-entry pages and repair confirmed navigation gaps before changing IDX-01 to Verified. IDX-02 cannot be marked Verified until this upstream reconciliation and its own schema checks are reviewed.

## 2026-10-30 final index acceptance checkpoint (IDX-01 / IDX-02)

The above intermediate checkpoint text records its original *in-progress* state. The later, reproducible [agent-index gate evidence](agent-index-evidence-2026-10-30.md) supersedes it for these two tasks: [machine-index run 41025578262](https://github.com/pskeffington/pauls_notes/actions/runs/41025578262) passed on commit `b8a9d1cf210ba77b5860a62cf91d688a45f7326a`. It indexed **1,147 sections in 126 tracked Markdown documents** with **zero broken links, missing documents, duplicate IDs, structural errors or orphan candidates**. The only original orphan was a native Rust inference continuation, now linked in the ML overview and training guide. Structured agent task IDs, prerequisites and negative-case tests passed.

**IDX-01 and IDX-02 are Verified within their documentation/index scope only.** The updated validator also forbids marking a task Verified while any declared task dependency is unverified. The current draft PR is not a merged release, future CI is not presumed green, and none of these checks establish scientific truth, citation suitability, external model validity, or D0/D1 data admission.

**Next unblocked P0 task:** DOC-01: reconcile reader navigation, chapter-level manuscript completeness and cross-file publication readiness against the existing 60-entry manifest without writing new chapter claims. GOV-01 remains blocked for real-data admission until independent privacy and access review.

## 2026-11-21 investigator-reference development checkpoint

**Tasks:** DOC-01 / DOC-02. **State:** In progress; substantive drafts and bounded verification, not final textbook acceptance. **Review vehicle:** [existing draft PR 42](https://github.com/pskeffington/pauls_notes/pull/42), branch `docs/data-science-narrative-intro`. The current mainline source at `ea68a32` was merged into the earlier narrative branch at `cc26d1d`; its newer statistical-reporting and notation work is preserved. The PR records the exact committed head and any subsequent CI result.

### Delivered content and integration

- Expanded the existing [data-science introduction](../03_learning/INTRODUCTION_TO_DATA_SCIENCE.md) with an original opening chapter: clinical question types, estimands, participant/specimen units, an 80-person synthetic response comparison, missing-outcome bounds and six reasoned exercises.
- Extended [CO-02 clinical data](../oncology/chapters/CO-02-clinical-oncology-data.md) with breast cancer receptor/classifier distinctions; pCR, RCB, IDFS, IBCFS and EFS; patient-to-assay lineage; TCGA export/manifest/assay/CDR distinctions; WDBC suitability; and a 12-person cohort-accounting example. Added 14 source records and synchronized its 18 H2/H3 citation mappings.
- Repaired four damaged sample-size displays in the [study-design guide](../03_learning/bio_stats/CANCER_STUDY_DESIGN.md), defined their notation and independently checked the existing numerical planning values. The [protocol template](../templates/study-protocol.md) now captures time zero, ascertainment, denominators, intercurrent-event strategies, missingness, source versions and review evidence.
- Replaced the obsolete 2017 ICH draft link in the touched protocol/design material with [final FDA E9(R1) guidance (May 2021)](https://www.fda.gov/media/148473/download). Clarified the frozen synthetic protocol's documented-response endpoint and supplementary analyses. The Rmd now labels Fisher's conditional odds ratio **A relative to B** separately from the primary **B minus A** risk difference; calculation expressions and data generation are preserved.
- Added the [investigator pathway](NAVIGATION.md#breast-cancer-investigator-pathway), retained the original route IDs and registered clinical-data/reporting destinations. Corrected two stale crosswalk-test paths in existing acceptance notes. Adjusted the existing navigation regression test to verify retained routes and new canonical homes instead of assuming the old route count was permanent.
- Reconciled seven attribution findings in current reporting/quantile notes with the existing author-neutral contract; full textbook author credit remains in the canonical methodology bibliography. No statistical convention was changed.

### Sources, arithmetic and review scope

All new examples are invented teaching constructions. Clinical source material consists of primary papers, official guidance and provider documentation; no participant-level data or new clinical result was ingested. Individual source dates and claim scope are retained in the [source registry](../oncology/evidence/source-registry.json). The 2026 survival-planning methodological update is supported at **publisher-abstract level**, not a claimed full-paper replication.

Python standard-library replay reproduced the opening contrast of 0.15; the available-case contrast of 0.1842105263; missing-outcome bounds of 0.10 and 0.25; the 12-person intersection accounting; a normal-approximation requirement of 90.41909454 per arm, rounded to 91; enrollment inflation to 102; and an event requirement of 379.35172960, rounded to 380. Missing-outcome bounds are not confidence intervals, and required events are not recruited participants.

An independent AI review checked the argument, primary-source correspondence and arithmetic; its findings about relative links and the supplementary odds-ratio direction were resolved. This is **not external statistical or clinical expert review**. The 60-chapter oncology manifest remains **six drafts and 54 planned**; the separate narrative opening does not promote CO-07 or another manuscript chapter.

### Verification record

**Observed locally on 2026-11-21:**

| Gate | Exact checks | Observed scope |
| --- | --- | --- |
| Reader/documentation integrity | `check_navigation_routes.py`, `check_notes_docs_hygiene.py`, `check_documentation.py` | 16 valid routes; 12 hygiene entrypoints; 163 Markdown pages with local links and anchors resolving |
| Source and book structure | `check_methodology_attribution.py`, `check_biostat_8e_alignment.py`, `validate_oncology_book.py`, `validate_oncology_citations.py` | Attribution, 14 source chapters/60 oncology IDs, manifest and section-citation checks pass |
| Task, scope and evidence consistency | `check_agent_tasks.py`, `check_cancer_research_scope.py`, `check_milestone_evidence.py`, `validate_research_methods.py` | Existing gates retain their scientific boundaries; 13 task records valid |
| Source/repository checks | `check_repository.py`, `check_repository_artifacts.py`, `git diff --check` | 98 Python/Bash source files parse; 443 tracked paths contain no incidental editor/build debris; diff whitespace clean |
| Existing regression suites | `scripts/tests/test_navigation_routes.py`, `test_notes_docs_hygiene.py`, `test_documentation.py`; `scripts/test_oncology_citations.py`, `test_oncology_book.py`, `test_agent_tasks.py`, `test_research_method_registry.py` | 39 tests pass across these seven suites |
| Machine-index suites and replay | `python3 -m unittest discover -s scripts -p 'test_*machine_index.py' -v`; index build, deterministic replay, enrichment and coverage audit | 13 tests pass; 1,630 sections across all 163 documents indexed; zero broken links, orphan candidates or structural errors |
| Method-matrix and evidence follow-up | `check_biostatistics_matrix.py`, `check_biostatistics_evidence.py`; `scripts/tests/test_biostatistics_matrix.py`, `test_biostatistics_evidence.py` | 18 tests pass; 27 routes, 25 gates and 156 route-gate links validated; evidence registry records 19 chart objects, 26 papers and 39 method/diagnostic outputs within their stated reproduction boundaries |

Run the named checker scripts from `scripts/` unless a full path is given. The index audit initially identified the existing quantile/Q–Q guide as a navigation orphan; a contextual link from the canonical reporting standard resolves that discovery gap. The generated index and audit are disposable `/tmp` outputs; recreate them with the commands in `AGENTS.md`.

Source comparison confirmed that all eight R chunks preserve their calculation expressions; only supplementary table labels changed. The three expanded teaching chapters have paired display-math delimiters and no embedded control characters.

**Not run locally:** R execution, R Markdown knitting and rendered-page inspection. `Rscript` was unavailable, and installing base R was blocked by the environment's package-manager permissions. The existing Biomedical learning case CI includes the study-design tests, frozen protocol replay and HTML render; its actual result must be read from the final PR head. External statistical and clinical expert review remain pending. None of these uncompleted gates is recorded as passed.

**CI acceptance follow-up:** [Biomedical learning case run 44894127559](https://github.com/pskeffington/pauls_notes/actions/runs/44894127559) on `1bf317e` exposed two preexisting validation defects before the downstream report renders. The method-matrix checker required chapter numbers even for extension/design-gate routes whose source crosswalk intentionally has no textbook chapter; its correction permits that explicit distinction while rejecting missing core coverage, invalid chapter lists and empty required metadata. The full-study R acceptance test searched `term.labels` for an offset, although R stores offsets in a separate terms attribute. Its correction checks the actual offset and verifies that doubling exposure at fixed covariates doubles the expected count. The underlying registry, fitted model and study calculations are unchanged. The PR records the observed rerun outcome and exact head; neither a repaired assertion nor a queued job is recorded here as successful R execution.

### Next bounded work

1. Continue DOC-02 with an integrated data-dictionary/join exercise using the existing observation-grain and clinical-data material; keep its synthetic cohort and effect direction explicit.
2. For CO-07, inspect and reuse the existing probability R/Python labs and tests before authoring the probability/Bayes manuscript. Follow the existing biostatistics source/fixture dependencies; do not create a duplicate laboratory.
3. Obtain independent R replay and rendered acceptance for affected reports; retain specialist statistical and clinical review as publication requirements. Real-data admission remains governed by the existing D0/D1 workflow.
