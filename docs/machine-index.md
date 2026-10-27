# Machine-readable discovery and indexing contract

This page is for search systems, RAG pipelines, documentation harvesters and autonomous coding agents. The human entrypoint remains [README](../README.md). The lightweight machine entrypoint is [llms.txt](../llms.txt). Paths below are repository-relative; resolve them against the same commit revision whenever possible.

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
| book.labs | `oncology/examples/README.md` | executable lab navigation | synthetic inputs only |
| book.citations | `oncology/evidence/section-citations.json` | section-to-source map | structural links only |
| book.references | `oncology/evidence/source-registry.json` | linked source metadata | does not prove claim-level validity |
| book.bibliography | `oncology/evidence/SOURCES.md` | reader-facing linked references | verified routes, not scientific sign-off |
| book.evidence.policy | `oncology/evidence/README.md` | editorial standards | independent review required |
| book.manifest | `oncology/book-manifest.json` | chapter inventory | CO-01 through CO-05 have draft manuscript paths |
| book.roadmap | `oncology/ROADMAP.md` | authoring milestones | plans are not completed chapters |

Agents must consult the manifest rather than inferring that a planned chapter exists. Use the source registry and per-section mapping for citation retrieval, but check the linked original source before asserting that it supports a specific scientific claim. Chapter URLs are valid only where `chapter_path` is not null; the original research methods and examples are separate existing assets.

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
