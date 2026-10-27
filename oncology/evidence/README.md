# Evidence and Citation Policy — Computational Oncology

[Book home](../README.md) · [Human bibliography](SOURCES.md) · [Source registry](source-registry.json) · [Section crosswalk](section-citations.json) · [Citation validator](../../scripts/validate_oncology_citations.py)

## Purpose

This book connects foundational scientific explanations to the actual publications, official standards and methodological references that support them. A citation is a path to evidence, **not** a blanket certification of an entire paragraph, an endorsement of clinical use, or proof of numerical replication.

## Citation format and granularity

- Substantive clinical, biological, methodological and regulatory claims should be supported with **direct inline links near the relevant claim**, supported by an explicit source list at the end of each meaningful subsection.
- For the current draft, every `##` and `###` section in the introduction and CO-01 through CO-04 contains `**Section references:**` followed by direct HTTPS links. A machine-readable mapping preserves those associations independently of formatted prose.
- At least two suitable primary or authoritative sources per substantive section are preferable when the argument spans more than one domain. A single highly specific original source may be sufficient for a narrow methodological point. The validator enforces structural presence, not scientific suitability.
- Cite original research by DOI or PubMed and official terminology/data rules by the owning standards organization. Secondary summaries may help explain background but should not be presented as the original evidence.
- Mathematical identities and independently invented teaching exercises do not require a publication for the arithmetic itself; their **scientific interpretation and method assumptions** do require evidence when appropriate.
- Do not reproduce third-party full text, tables, figures or course materials without rights review. Independently authored explanations and synthetic examples are the default.

## Publication gates

1. **Link and structure:** The chapter exists, headings are stable, links are properly formed, and the source registry maps all sections. Run `python3 scripts/validate_oncology_citations.py`.
2. **Source check:** Verify each reference's identity, publication/version, accessible URL and specific relevance to the neighboring claim. Record access date and any limitations.
3. **Clinical-scientific review:** A qualified subject reviewer checks claims, terminology, appropriate context, study-design assumptions and whether any findings are overstated.
4. **Numerical/reproducibility review:** Independent replay validates calculations and code against expected results, and negative tests detect meaningful failures.
5. **Editorial review:** Confirm citations are localized to claims, figures are original or licensed, exercises are appropriately attributed and the text is accessible.
6. **Release decision:** Update the book manifest to `reviewed` or `released` only after its actual evidence is independently documented.

## Source roles

- `clinical-reference`: clinical definitions and institutional guidelines, with version/scope checks.
- `authoritative-overview`: established background and definitions, not disease-specific treatment protocols.
- `technical-specification`: file types, data lineage, processing contracts and documentation.
- `peer-reviewed-method`: a published analytical framework, not proof of its suitability in every dataset.
- `peer-reviewed-review`: conceptual synthesis and competing interpretations.
- `reporting-guideline`: transparency standards, **not** independent validation of a study.
- `regulatory-guidance`: rules that require current jurisdictional and situational interpretation.
- `editorial-standard`: manuscript practice, referencing and scholarly transparency.

## Research boundaries

The manuscript is for learning research design and computation. Public availability of a study description or portal does not imply unrestricted permission to retrieve, embed, release or model participant-level records. Protect privacy, respect data-use agreements and keep public repositories limited to independently authorized material.

The source registry currently supplies **structural** section links for an active draft; it does not represent completed claim-level scientific or editorial peer review. The final ebook must pass those additional checks.
