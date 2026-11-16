# Documentation ownership and maintenance

**Scope:** Paul's Notes repository documentation, machine navigation, biomedical
methods notes and generated acceptance records. Scientific analyses and dataset
content are not modified by a documentation-formatting pass.

## One canonical source per responsibility

| Responsibility | Canonical file | Edit rule |
| --- | --- | --- |
| Reader orientation | [Root README](../README.md) | Summarize the reader journey; link to details rather than duplicating long method cards |
| Agent behavior, safety and handoffs | [AGENTS.md](../AGENTS.md) | Keep execution gates and source hierarchy; do not repeat entire book chapters |
| AI discovery | [llms.txt](../llms.txt) | Stable routes, short descriptions, usable retrieval keys |
| Machine topics and index authority | [Machine index](machine-index.md) | Repository-relative paths and explicit coverage boundaries |
| Methods and study design | [Biomedical implementation gates](../02_biomedical_coding/IMPLEMENTATION_GATES.md) | Scientific assumptions and evidence, not editorial housekeeping |
| Statistical method conventions | [Complete methodology contract](../02_biomedical_coding/BIOSTAT_8E_COMPLETE_METHODOLOGY_CONTRACT.md) | Edition-specific technical expectations without author-based branding |
| Original graph design | [Graph-method alignment](../03_learning/bio_stats/GRAPH_METHODS_ALIGNMENT.md) | Axes, sample units, quartiles, visual marks and figure QA |
| Bibliographic source identities | [Methodology sources](../02_biomedical_coding/METHODOLOGY_SOURCE_REFERENCES.md) | Full author names and bibliographic attribution only when appropriate |
| Source checks and acceptance status | [Verification ledger](../02_biomedical_coding/BIOSTAT_8E_VERIFICATION_ACCEPTANCE_LEDGER.md) | Append observed evidence; never promote unrun tests to a pass |
| Teaching and executable exercises | [Biomedical statistics notes](../03_learning/bio_stats/README.md) | Explain the intended method, link to R sources and synthetic worked examples |

## Cleanup principles

1. Preserve existing scientific statements and code results unless independently checked; a docs pass does not revalidate a model or published claim.
2. Use actual Markdown line and table-row boundaries rather than literal escaped `\n` strings copied by automation. Preserve intentional escapes inside source-code fences.
3. Prefer descriptive statistical terminology over author-based labels. Preserve necessary credit and section identifiers in the dedicated bibliography.
4. Repair obsolete links in place; do not silently create a duplicate reference document to satisfy a broken URL.
5. Keep source scope explicit: a source page checked, a Python structural assertion, an R run and a human figure inspection are distinct evidence levels.
6. Maintain historical behavior: an opt-in type-2 quartile graph does not change a type-7 legacy summary or an analysis's reported values.
7. Use existing top-level guidance and add only short cross-links from subordinate READMEs.
8. For every changed file, state the change type (formatting, path, terminology, code, source verification), then link its regression gate.

## Verification commands

From repository root:

```bash
python3 scripts/check_notes_docs_hygiene.py
python3 -m unittest discover -s scripts/tests -p 'test_notes_docs_hygiene.py' -v
python3 scripts/check_methodology_attribution.py
python3 scripts/check_biostat_8e_alignment.py
python3 scripts/check_documentation.py
```

The first two check a **bounded set of canonical entrypoints**; they are not
whole-repository link verification. `check_documentation.py` performs wider
Markdown navigation checks. R-based acceptance remains separate in
`.github/workflows/learning-case-validation.yml` and must be verified from an
actual job log and knitted artifacts.

## Cleanup record — 2026-11-16

- Replaced literal backslash-n markup with actual newlines across the learning
  index, biostatistics index, statistical method matrix, study design,
  interpretation atlas and R resource README.
- Standardized headings and removed placeholder source-identity language from
  selected biomedical documentation while retaining scientific content.
- Reconnected the root README, biomedical coding README and machine index to the
  original graph methods, synthetic workbook, R helpers, and evidence ledger.
- Corrected the method-selection matrix's source link label: the destination is
  a **bibliography**, not a live publisher catalog.
- Added a core-document regression checker and isolated Python tests, then
  configured GitHub Actions to run them on documentation changes.
- **Observed:** Eleven refetched core documents show no literal escaped
  newline tokens, residual author-name branding or named-source placeholders.
- **Not established:** Full repository link/test acceptance, actual Python CI
  success, complete R/HTML knitting or external scientific review. Do not infer
  these from clean Markdown or committed tests.

## Next review targets

Continue with machine-link integrity, repeated passages outside the canonical
sections, outdated completion claims, and source-to-result provenance. Make
small changes supported by exact file inspection, with regression coverage.
