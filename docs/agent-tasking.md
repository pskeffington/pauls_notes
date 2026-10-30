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
| IDX-01 | P0 | Ready | Audit links, headings, duplicate section IDs, orphaned pages and indexing coverage across textbook and learning resources | Record baseline diagnostics and proposed repairs; determinism and existing machine-index tests pass |
| IDX-02 | P0 | Planned (after IDX-01) | Add machine-readable agent task registry or verified task export, aligned to this human queue | Stable IDs, dependencies, statuses, owner-less handoffs, schema tests and deterministic output |
| DOC-01 | P0 | Ready | Reconcile chapter statuses and navigation against the 60-entry book manifest and actual files | No chapter marked drafted without manuscript; README, oncology/README, llms.txt, registry and manifest cross-links agree |
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
- No task is complete from AI-generated text alone: demand tests or checkable review evidence matching its scope.
- Keep broad cancer scope; use breast cancer as an explicit example rather than defaulting every chapter to BRCA.
- For each pass, update this queue, affected navigation and documented evidence together. Annotate the actual date, branch/PR and observed checks rather than changing historical gate snapshots without verification.

## Index and handoff output expected from an agent
At minimum: `task_id`, `state`, `depends_on`, `affected_paths`, `input_provenance`, `test_commands`, `observed_results`, `evidence_links`, `limitations`, `next_task`. For machine retrieval, preserve source path, heading identifier, content hash and exact version/commit in downstream ingestion. An indexed reference is a search aid, not a verified scientific citation.
