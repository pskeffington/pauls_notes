# Machine-readable discovery and indexing contract

This page is for search systems, RAG pipelines, documentation harvesters and autonomous coding agents. The human entrypoint remains [README](../README.md). The lightweight machine entrypoint is [llms.txt](../llms.txt). Paths below are repository-relative; resolve them against the same commit revision whenever possible.

## Complete Rosner 8e biomedical source-to-code contract

| Topic key | Entrypoint | Content role | Boundary |
| --- | --- | --- | --- |
| `biomedical.rosner8.complete_methods` | `02_biomedical_coding/ROSNER_8E_COMPLETE_METHODOLOGY_CONTRACT.md` | all fourteen chapter method/coding acceptance contracts | source opening/targeted content; not full-book line-by-line audit |
| `biomedical.rosner8.coverage_registry` | `02_biomedical_coding/rosner_8e_complete_chapter_alignment.csv` | source page/edition, ontology mappings and code evidence state | all R execution/statistical review pending |

Structural validator: `python3 scripts/check_rosner_8e_alignment.py`. Do not interpret a structural pass as an inferential code pass.

## First-pass biomedical coding source alignment

| Topic key | Entrypoint | Content role | Boundary |
| --- | --- | --- | --- |
| `biomedical.rosner8.first_pass_audit` | `02_biomedical_coding/ROSNER_ALIGNMENT_FIRST_PASS_AUDIT.md` | source-to-code discrepancy ledger and verification commands | R runtime and knit not yet verified |
| `biomedical.rosner8.quantiles` | `06_RESOURCES/R/rosner_descriptive_contract.R` | explicit opt-in type-2 and type-7 quantile implementations | code authored, deterministic R test execution pending |

## Breast cancer statistics book methodology route

| Topic key | Entrypoint | Content role | Boundary |
| --- | --- | --- | --- |
| `oncology.breast_cancer.rosner_roadmap` | `oncology/ROSNER_BREAST_CANCER_BIOSTATS_ALIGNMENT_ROADMAP.md` | gated chapter/biostatistics roadmap | planned tasks, not published or validated chapters |
| `biomedical.rosner8.code_companion` | `02_biomedical_coding/ROSNER_8E_SOURCE_VERIFIED_IMPLEMENTATION.md` | source-aligned independent coding examples | targeted source verification; not full-page review |
| `biomedical.rosner6.toc` | `02_biomedical_coding/ROSNER_6E_CHAPTER_TO_CODE_BEST_PRACTICES.md` | separate sixth-edition crosswalk | TOC based, chapter text unavailable |

For alignment requests, retrieve the roadmap and actual book manifest before modifying chapter or gate statuses. Source evidence must be edition specific.

## Computational Oncology routes

| Topic key | Entrypoint | Content role | Boundary |
| --- | --- | --- | --- |
| book.home | `oncology/README.md` | reader navigation | independent textbook |
| book.introduction | `oncology/INTRODUCTION.md` | scholarly purpose | draft introduction |
| book.chapter.01 | `oncology/chapters/CO-01-cancer-biology.md` | textbook chapter | draft; not independently reviewed |
| book.chapter.02 | `oncology/chapters/CO-02-clinical-oncology-data.md` | textbook chapter | draft; not independently reviewed |
| book.chapter.03 | `oncology/chapters/CO-03-molecular-foundations.md` | textbook chapter | draft; not independently reviewed |
| book.chapter.04 | `oncology/chapters/CO-04-data-literacy.md` | textbook chapter | draft; not independently reviewed |
| book.chapter.05 | `oncology/chapters/CO-05-essential-mathematics-i.md` | textbook chapter | draft; arithmetic labs added; independent review pending |
| book.chapter.06 | `oncology/chapters/CO-06-essential-mathematics-ii.md` | textbook chapter | draft; Python local validation passed, R/CI pending |
| book.validation.06 | `oncology/evidence/CO-06-VALIDATION-2026-10-27.md` | technical evidence report | precise scope and outstanding checks |
| book.labs | `oncology/examples/README.md` | executable lab navigation | synthetic inputs only |
| book.citations | `oncology/evidence/section-citations.json` | section-to-source map | structural links only |
| book.references | `oncology/evidence/source-registry.json` | linked source metadata | does not prove claim-level validity |
| book.bibliography | `oncology/evidence/SOURCES.md` | reader-facing linked references | verified routes, not scientific sign-off |
| book.evidence.policy | `oncology/evidence/README.md` | editorial standards | independent review required |
| book.manifest | `oncology/book-manifest.json` | chapter inventory | CO-01 through CO-06 have draft manuscript paths |
| book.roadmap | `oncology/ROADMAP.md` | authoring milestones | plans are not completed chapters |

Agents must consult the manifest rather than inferring that a planned chapter exists. Use the source registry and per-section mapping for citation retrieval, but check the linked original source before asserting that it supports a specific scientific claim. Chapter URLs are valid only where `chapter_path` is not null; the original research methods and examples are separate existing assets.

## High-priority biomedical code retrieval

| Topic key | Entrypoint | Content role | Boundary |
| --- | --- | --- | --- |
| `biomedical.r.canonical_example` | `02_biomedical_coding/BIOMEDICAL_R_CANONICAL_EXAMPLE.md` | canonical runnable template and AI coding style contract | synthetic demonstration; not a study protocol |
| `biomedical.r.full_study` | `02_biomedical_coding/examples/SYNTHETIC_BREAST_CANCER_FULL_STUDY.Rmd` | full synthetic breast-cancer R Markdown study and methods walkthrough | invented data; methods are illustrative and not all jointly indicated |
| `biomedical.r.implementation_gates` | `02_biomedical_coding/IMPLEMENTATION_GATES.md` | scientific/code acceptance checks | design gates, not clinical validation |

For R/Rmd coding requests, retrieve `biomedical.r.canonical_example` first; pair it with the live study data dictionary and implementation gates. Search aliases: Paul's Notes biomedical R template, AI biostats coding, knitted R Markdown, scientific palette, reproducible analysis.

## Canonical navigation

| Topic key | Entrypoint | Content role | Data boundary |
| --- | --- | --- | --- |
| oncology.scope | `docs/cancer-research-scope.md` | research scope | general educational content |
| research.protocol | `docs/research-workflow.md` | study design and admission | verify dataset-specific permissions |
| statistics.select | `03_learning/biomedical-statistics-decision-guide.md` | test selection | teaching, not an analysis of a patient cohort |
| statistics.practice | `03_learning/statistics-practice-workbook.md` | practice | educational examples |
| ml.overview | `04_machine_learning/README.md` | method hub | inspect each example's evidence |
| ml.visual | `04_machine_learning/visual-data-guide.md` | training explanation | teaching case |
| ml.tuning | `04_machine_learning/model-tuning.md` | tuning and evaluation | do not equate test runs with validation |
| ml.survival | `04_machine_learning/survival-protocol.md` | survival protocol | consult milestone status before claims |
| genomics.book | `06_RESOURCES/Genomics/BREAST_CANCER_60_GENE_COMPANION.md` | teaching narrative | not patient-level observations |
| literature.stats | `06_RESOURCES/Literature/BIOSTATISTICS_R_LITERATURE_2021_2026.md` | evidence guide | check cited originals |
| rust.course | `03_learning/rust/README.md` | language instruction | teaching and engineering |
| rust.practices | `02_biomedical_coding/RUST_CODING_BEST_PRACTICES.md` | engineering guidance | not a clinical assurance |
| milestones | `docs/milestone-evidence.toml` | machine-readable delivery state | authoritative only within recorded scope |

## Agentic templating and scholarly literature routes

| Topic key | Entrypoint | Content role | Boundary |
| --- | --- | --- | --- |
| agentic.overview | `README.md#agentic-templating-skills-and-best-practices` | skill and templating overview | design guidance, not measured deployment |
| agentic.literature | `docs/agentic-skills-literature-matrix.md` | authored scholarly matrix | source summaries and engineering interpretations |
| agentic.registry | `docs/agentic-skills-literature-registry.json` | structured bibliography | bibliographic metadata; not claim-level verification |

Resolve `AG-LIT-01` through `AG-LIT-09` using the JSON registry's `records[].id`, then retrieve `source_url` for primary-source verification. Keep `publication_type` distinct from evidence quality and `priority_ids` distinct from empirical findings. Both files are tracked inputs to the existing heading-aware Markdown indexer; the JSON registry is a complementary structured catalog, **not** automatically joined into that JSONL. Each downstream consumer must explicitly ingest the registry if it needs publication-level metadata.

## Retrieval rules

1. First retrieve this discovery document or `llms.txt`; identify the best matching topic key.
2. Retrieve the linked original file and its immediate linked protocol or evidence record. Never answer solely from an index summary.
3. Record repository URL, commit SHA, relative path, heading and retrieval date for every cited claim. Build a section ID as `<relative-path>#<heading-slug>`; retain the commit SHA separately.
4. Chunk Markdown along heading boundaries (not arbitrary page lengths). Preserve parent headings, tables, code fences, captions and their nearby explanatory text. Keep citations attached to the claim they support.
5. Label chunks by evidence role: `instruction`, `protocol`, `literature`, `example`, `source_code`, `test`, `status` or `template`. A label is a retrieval classification, not a quality grade.
6. Keep status from `docs/milestone-evidence.toml` separate from narrative descriptions. If source and status appear inconsistent, disclose the conflict rather than silently promoting a planned gate to completed.
7. Exclude `.git`, caches, virtual environments, generated plots, large binaries, datasets and secrets from text embedding by default. Analyze code/test files only when the task calls for their implementation details.
8. Treat links and external papers as references requiring independent verification; do not infer that a citation alone confirms the text's interpretation.
9. Preserve source version and re-index on new commits. Do not deduplicate across distinct protocols solely because their text is similar.
10. Refuse to index personally identifiable, protected, controlled-access or credential data into a public search layer.

## Recommended search record

Each indexed section should carry:
```json
{
  "schema_version": "1.0",
  "repository": "pskeffington/pauls_notes",
  "commit_sha": "<actual indexed commit SHA>",
  "path": "03_learning/biomedical-statistics-decision-guide.md",
  "heading": "<actual source heading>",
  "section_id": "03_learning/biomedical-statistics-decision-guide.md#<heading-slug>",
  "role": "instruction",
  "content_sha256": "<SHA-256 of exact indexed section>",
  "source_url": "https://github.com/pskeffington/pauls_notes/blob/<commit-sha>/03_learning/biomedical-statistics-decision-guide.md",
  "retrieved_at": "<ISO-8601 timestamp>"
}
```
Populate placeholders from the document actually fetched; do not persist placeholders as real records.

## Recommended automation gates

- Confirm paths and anchor targets exist at the selected commit.
- Fail index builds for duplicate `(commit_sha, section_id)` identifiers or missing provenance fields.
- Report broken internal links and newly orphaned Markdown documents.
- Track added, changed and removed files between commits using content digests.
- Validate JSON output against a versioned schema before publication.
- Check public-index inputs against privacy and secret-scanning controls.
- Recheck human-readable claims against the milestone ledger after major releases.

This is a discovery and governance contract. It does not claim an automated index generator or CI validator is already installed.


## Executable index builder (October 2026)

The standard-library-only generator is [`scripts/build_machine_index.py`](../scripts/build_machine_index.py), with [unit tests](../scripts/test_machine_index.py) and [CI](../.github/workflows/machine-index.yml).

From the repository root:

```bash
python3 -m unittest discover -s scripts -p 'test_machine_index.py' -v
python3 scripts/build_machine_index.py --output /tmp/pauls-notes-index.jsonl
python3 scripts/build_machine_index.py --output /tmp/pauls-notes-index.jsonl --check
```

The emitted JSONL contains exact source text, source line spans, role, relative path, section identifier and SHA-256 digest. Output is deterministic for identical tracked Markdown content, with no generated timestamp or floating `main` URL embedded in records. Attach the actual Git commit SHA and indexing timestamp in the downstream ingestion manifest. Link problems are reported but do not fail the default build; use `--strict-links` to enforce a zero-warning gate after existing documentation issues are cleaned up. The index currently uses heading-aware chunks, not bounded token-size subchunks or embeddings.

The GitHub Actions workflow builds an ephemeral index and checks its deterministic replay, schema fields and unique section IDs. It does not publish or commit a generated index file. CI execution must be observed before treating this as a passing repository gate.


## Retrieval enrichment and incremental changes (Pass 3)

Run the basic builder first, then enrich its records:

```bash
python3 scripts/build_machine_index.py --output /tmp/pauls-notes-base.jsonl
python3 scripts/enrich_machine_index.py --input /tmp/pauls-notes-base.jsonl --output /tmp/pauls-notes-enriched.jsonl
python3 -m unittest discover -s scripts -p 'test_*machine_index.py' -v
```

Enriched records retain all base fields and add `topics`, `retrieval_terms`, `outbound_documents`, and `inbound_documents`. These are deterministic, heuristic navigation aids; they do **not** constitute formal biomedical ontology coding or independently validated citations. Cross-document edges are computed from existing local Markdown links, not inferred semantic relationships.

To compare the current base index with a previous base index:

```bash
python3 scripts/enrich_machine_index.py --input /tmp/pauls-notes-base.jsonl --output /tmp/pauls-notes-enriched.jsonl --previous /tmp/previous-base.jsonl --delta-output /tmp/section-delta.json
```

The delta lists added, removed, changed and unchanged sections based on section IDs and content hashes. It reports change candidates for downstream indexing; it does not yet implement selective vector re-embedding. The CI workflow tests deterministic enrichment, but does not publish indexes or claim ontology validation. Broken links remain non-fatal unless strict link checking is requested.

## Pass 4: Curated research methods

The [method registry](research-method-map.json) gives stable keys to selected teaching methods and links them to the statistics guide and literature identifiers. The [validator](../scripts/validate_research_methods.py) checks method ID uniqueness, source paths, and whether referenced BS literature identifiers appear in the current curated reading list. An empty evidence list means no publication-level relationship has been curated; it does not imply the method lacks evidence.

Run `python3 scripts/validate_research_methods.py` and `python3 -m unittest discover -s scripts -p 'test_research_method_registry.py' -v`. CI runs both on changes to the registry or validator. A registry record is a navigation pointer, not proof that a particular publication supports every implementation choice. Direct links to specific assumptions, code implementations, and verified study-level evidence remain future enrichment work.


## Evidence-aware section indexing — October 2026

The [textbook section citation register](../oncology/evidence/section-citations.json) can be joined into the enriched JSONL catalog with a source-ID field rather than by inferring scientific support from keywords.

```bash
python3 scripts/build_machine_index.py --output /tmp/pauls-notes-base.jsonl
python3 scripts/enrich_machine_index.py \
  --input /tmp/pauls-notes-base.jsonl \
  --output /tmp/pauls-notes-enriched.jsonl \
  --section-citations oncology/evidence/section-citations.json
```

Each enriched section includes `citation_ids` (empty where no curated section mapping exists). Resolve IDs against [the source registry](../oncology/evidence/source-registry.json) and use the exact link associated with the selected section. Do not assign evidence from another heading merely because its keywords resemble the question. The [citation validator](../scripts/validate_oncology_citations.py) separately checks that manuscript section references are present and match the register.

The join is deterministic but **not** scientific claim validation. Human scholarly review, assessment of each linked publication and independent replay remain required. The enrichment process does not download external articles or publish participant records.

## Coverage and orphan-candidate audit (agent pass, 2026-10-30)

The index pipeline now has a [coverage auditor](../scripts/audit_machine_index.py) and [unit tests](../scripts/test_audit_machine_index.py). Run the builder and enrichment as shown above, then:

```bash
python3 scripts/test_audit_machine_index.py
python3 scripts/audit_machine_index.py --input /tmp/pauls-notes-enriched.jsonl --output /tmp/pauls-notes-audit.json
```

The audit compares indexed paths to all nonempty tracked Markdown inputs, rejects duplicate section identifiers and inconsistent incoming-link metadata, and reports documents without Markdown incoming links as **orphan candidates**. Such candidates can legitimately be reached through `llms.txt`, external stable URLs or direct entrypoints and are **not automatically release failures**. Review each candidate, then update navigation only when a concrete reader or agent retrieval gap is confirmed.

The workflow stores the deterministic audit JSON as a short-retention artifact. It does not publish the full index, crawl remote citations, build embeddings, claim clinical verification, or automatically fix links. See [agent tasking](agent-tasking.md) for the current gate status.
