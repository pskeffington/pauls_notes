# Agent operating contract — Paul's Notes

Scope: the complete repository. Read this before editing. Repository owner: Paul Skeffington. This independent educational project covers computational oncology across cancer types; breast cancer and TCGA-BRCA are worked examples, not universal assumptions.

## Author-neutral methodology and bibliographic attribution

All internal educational material must use **method names and scientific concepts**, not a textbook author's name, as headings, file paths, R symbols, retrieval keys, CI jobs, or labels. Cite the textbook only for a source-specific methodological assertion and use the dedicated bibliography at `02_biomedical_coding/METHODOLOGY_SOURCE_REFERENCES.md`. Keep edition and section numbers for provenance when needed. Run `python3 scripts/check_methodology_attribution.py` before merging educational documentation or code. This rule does not change scientific assumptions, preserve reproducibility, or authorize erasing proper scholarly credit.

## Graph-method alignment

Use `03_learning/bio_stats/GRAPH_METHODS_ALIGNMENT.md` as the canonical figure-type and axis contract. Reuse `06_RESOURCES/R/biostat_graphs.R` and `06_RESOURCES/tests/test_biostat_graphs.R` for new teaching figures. Box quartiles must name their R quantile type; mean (+) and median line are distinct; whiskers are not confidence intervals; outliers outside 1.5×IQR and 3×IQR use distinct markers; ROC is sensitivity versus 1−specificity; survival axes must state event and time unit. Keep the palette and synthetic-data provenance. The historical type-7 descriptive helper must not be migrated silently. The textbook author belongs only in `METHODOLOGY_SOURCE_REFERENCES.md`.

## Breast cancer statistics textbook alignment
For any request to build or review the breast cancer biostatistics textbook, retrieve `oncology/BIOSTAT_BREAST_CANCER_BIOSTATS_ALIGNMENT_ROADMAP.md` and the actual `oncology/book-manifest.json` first. Use the eighth-edition biostatistics guide `02_biomedical_coding/BIOSTAT_8E_SOURCE_VERIFIED_IMPLEMENTATION.md` only within its recorded review scope, keep the sixth edition separate, implement the BR-001–BR-010 gates, and do not mark a planned chapter as drafted or validated without source, numeric, runtime and reviewer evidence.

## biostatistics verification evidence and CI acceptance
For verification or acceptance work, consult `02_biomedical_coding/BIOSTAT_8E_VERIFICATION_ACCEPTANCE_LEDGER.md`. Distinguish actual PDF/structural/numerical evidence from still-unrun R tests, full knitted output, and independent statistical review. The workbook acceptance command is `Rscript --vanilla 02_biomedical_coding/tests/test_full_study_execution.R`; CI also knits the workbook and checks a nonempty HTML artifact. A defined CI job is not a passed CI job.

## Complete eighth-edition methods method alignment and evidence controls
Before writing breast cancer statistics, consult `02_biomedical_coding/BIOSTAT_8E_COMPLETE_METHODOLOGY_CONTRACT.md` and `02_biomedical_coding/biostat_8e_complete_chapter_alignment.csv` after the oncology roadmap. Keep eighth-edition methods and 6e citations separate. Apply medical question → sampling unit → assumptions → hand/numerical check → R code → diagnostics → effect/CI → interpretation. Run `python3 scripts/check_biostat_8e_alignment.py` for structural routes and R/knit tests separately. A complete topical crosswalk is not full-book verification, code execution or scientific review.

## biostatistics source-alignment first pass
For descriptive biomedical R, inspect `02_biomedical_coding/BIOSTAT_ALIGNMENT_FIRST_PASS_AUDIT.md` and `06_RESOURCES/R/biostat_descriptive_contract.R`. eighth-edition methods uses quantile type 2 in §2.4, whereas preexisting Paul's Notes descriptive functions use type 7. Choose and report the convention explicitly, never silently migrate results, and execute `06_RESOURCES/tests/test_biostat_descriptive_contract.R` before treating the module as verified. Do not mark unrun R tests passed.

## Scientific reporting agent chain and PDF release acceptance

For scientific reports, manuscripts, statistical interpretations, LaTeX, R Markdown, or final PDF presentation, first inspect the canonical skill in the dedicated `agent_skills` repository: [Scientific Reporting QA](https://github.com/pskeffington/agent_skills/blob/main/.agents/skills/scientific-reporting-qa/SKILL.md) and the [R Markdown/PDF presentation acceptance contract](02_biomedical_coding/RMARKDOWN_PDF_PRESENTATION_ACCEPTANCE.md). Route work explicitly through evidence steward → methods reviewer → scientific editor → typesetting engineer → acceptance reviewer; the same agent may fulfill several roles when findings are recorded independently.

- Protect case boundaries: **never import particular study datasets, participant counts, endpoints, conclusions, numerical estimates, or report passages into reusable methods or skills**.
- For reports, use impersonal scientific prose; avoid authorial first-person identifiers and the author's prohibited transition. Prefer valid semicolons; distinguish APA 7 conventions from local house style.
- Keep statistical R code visible if requested. Separate source lint, authorized numerical execution, successful knit, and rendered page-by-page acceptance; report each gate as passed, failed or not run.
- Maintain source/PDF revision concordance. A GitHub commit and balanced code fences do not imply a successful knit or visually accepted PDF.
- Use the existing source-provenance and biostatistics gates; do not bypass source-license, privacy, or clinical-claims controls.

## Biomedical R / biostatistics coding — mandatory example
For any biomedical R, R Markdown, biostatistics or knitted-report generation/review, retrieve `02_biomedical_coding/BIOMEDICAL_R_CANONICAL_EXAMPLE.md` before writing code. For complete study templates or broad multi-method walkthroughs also retrieve `02_biomedical_coding/examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd` (retrieval key `pauls-notes.biomedical-r.full-study.v1`). It is the canonical *layout and style example*, not a substitute for study-specific data dictionary, statistical-design decisions or `02_biomedical_coding/IMPLEMENTATION_GATES.md`. Apply named chunks, `##` R code section comments, explicit checks, computed statistical evidence in narrative, Okabe–Ito plots and real knit verification. Never put Markdown `**` into executable R code.

## Entry and authority order
1. `README.md` and `llms.txt`: human and machine navigation.
2. `docs/agent-tasking.md`: prioritized, bounded agent queue and acceptance contracts.
3. `oncology/book-manifest.json`, `oncology/ROADMAP.md`: chapter identity, prerequisites, publication plan.
4. `docs/roadmap-gates.md` and `docs/milestone-evidence.toml`: dated, scoped scientific/software gate evidence. Do not rewrite statuses without matching evidence and verification.
5. `docs/machine-index.md` and `docs/research-method-map.json`: retrieval/index contracts and method routing.

## Non-negotiable boundaries
- Do not copy protected course materials or imply institutional endorsement. Maintain independent original explanations and cite external science at the claim/section level.
- Use explicitly synthetic data by default. Never commit PHI, identifiable participant records, credentials, restricted controlled-access data or real TCGA specimen data without a separately documented admission and approval gate.
- Keep learning exercise correctness, executable software verification, scientific replication and clinical validation separate. No code result implies diagnosis, prognosis or clinical readiness.
- Preserve person-level grouping, preprocessing within training folds, documented estimands and reserved evaluation boundaries.
- Do not alter source or evidence registries to fabricate completed reviews; record unresolved references transparently.
- Do not mix G-series synthetic ML milestones with R-series engineering gates, D-series admission gates or CO chapter publication gates.

## Agent execution cycle
1. Inspect worktree, current branch, recent changes, issues/PRs and the task dependencies; select the highest-priority *unblocked* work item in `docs/agent-tasking.md`.
2. Verify target files, linked sources, relevant acceptance commands and evidence status before edits. If stale, reconcile the task record first.
3. Work in a focused feature branch/PR. Limit change to one gate or tightly coupled documentation slice. Never overwrite parallel work or silently merge to main.
4. For new textbook content, supply clinical framing, measurable objectives, formal notation, worked synthetic example, interpretation, assumptions, source-linked evidence, exercises, answer reasoning and reproducible checks. Update manifest only when the deliverable is actually present.
5. Run the relevant local checks and all affected existing test suites; record exact commands, pass/fail output and environmental blockers. No retroactive assertions of CI success.
6. Update navigation, source crosswalks and task statuses only after testing. Report changed paths, evidence, open limitations and next unblocked task in the PR.

## Baseline verification
```bash
python3 -m unittest discover -s scripts -p 'test_*machine_index.py' -v
python3 scripts/build_machine_index.py --output /tmp/pauls-notes-agent-index.jsonl
python3 scripts/build_machine_index.py --output /tmp/pauls-notes-agent-index.jsonl --check
python3 scripts/enrich_machine_index.py --input /tmp/pauls-notes-agent-index.jsonl --output /tmp/pauls-notes-agent-enriched.jsonl
python3 scripts/test_audit_machine_index.py
python3 scripts/audit_machine_index.py --input /tmp/pauls-notes-agent-enriched.jsonl --output /tmp/pauls-notes-agent-audit.json
python3 scripts/check_milestone_evidence.py
```
Confirm `--help` and tool availability before adding optional strict-link or external tool gates. Run chapter-specific and ML tests when their files are touched. Do not treat this command list as proof it ran.

## Agent handoff record
Every PR or checkpoint must state: task ID; scope and modified files; base/head SHA; source/data classification; executed tests and observed outcomes; evidence artifacts; limitations/blockers; whether status or indexing was updated; next task. If blocked, stop the disallowed operation and continue with the next independent task rather than inventing clearance.
