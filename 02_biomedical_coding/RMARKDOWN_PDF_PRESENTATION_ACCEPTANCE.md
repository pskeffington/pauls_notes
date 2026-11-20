# R Markdown scientific report presentation and PDF acceptance

**Scope:** General editorial, typesetting, compilation, and visual-acceptance methods for reproducible scientific reports. This document is deliberately study-agnostic. It contains no case data, results, source-report prose, named endpoints, figures, screenshots, or study-specific inference.

**Status:** Reusable workflow distilled from iterative report-formatting work. The checks below are requirements to execute, not proof that any particular report has passed.

## 1. Separate the evidence gates

A manuscript has at least four distinct acceptance stages:

1. **Source inspection:** Review the current `.Rmd`; ensure headers, code fences, chunk labels, raw TeX, and inline R are syntactically coherent.
2. **Executable analysis:** Run the R chunks using authorized inputs; verify data assertions, model outputs, formulas, and expected objects. Structural checks alone cannot establish numeric correctness.
3. **Successful knit:** Generate the intended PDF or HTML from the current source and record the compilation command, environment, warnings, and produced artifact.
4. **Visual review:** Render the complete final PDF to page images; examine every page at reading size and re-knit after any changes. A successful knit does not prove tables, figures, and equations are legible.

Record the source revision, output file checksum, execution environment, and explicit pass/fail/not-run state for each gate. Do not represent a source-only update as a PDF acceptance.

## 2. Editing contract

- Preserve one canonical, runnable report; modify the actual source rather than editing rendered PDF text when reproducibility is required.
- Maintain named, unique R chunks and the user's code-visibility preference. If `echo=TRUE` is required, optimize code wrapping and pagination rather than hiding code.
- Keep results connected to computed R objects. Do not substitute copied statistics for live calculations.
- Separate **methods**, **assumptions**, **results**, **sensitivity tests**, **discussion**, **limitations**, **reproducibility**, and **references**; avoid repeating full comparison tables in prose.
- Apply impersonal scientific voice; remove first-person authorial language and incidental personal identifiers. Prefer semicolons for closely connected independent clauses, not as replacements for necessary commas. Avoid the prohibited closing transition used in the author's house style.
- Use APA 7 conventions where applicable; distinguish a local house-style preference from an APA requirement.
- For reporting, use correct syntax for p-values: `p = .042` or `p < .001`; avoid `p-value is = .042`. In `knitr::kable` columns, display the numeric/comparison value without an extra leading equals sign.
- Make scientific limitations explicit: statistical significance is not automatically clinical or practical significance; correlation alone does not establish causation.

**Statistical symbol reference:** [Scientific statistical reporting standards — notation](../03_learning/bio_stats/SCIENTIFIC_STATISTICAL_REPORTING_STANDARDS.md#1a--statistical-notation-and-mathematical-typography) defines estimator symbols, test-statistic grammar, italics, confidence-interval notation, and APA-oriented p-value style. Use that vocabulary consistently in source and rendered reports.

## 3. Mathematical notation and LaTeX

Write a notation key before hypothesis blocks, defining population parameters, observed statistics, indices, outcomes, time points, and contrast directions. Each inferential question should distinguish a null hypothesis, an alternative hypothesis, the estimand, two-sided versus directional testing, and the multiplicity family. Do not invent a null test for a descriptive research question.

- Put long definitions and multiple hypotheses into `\[ ... \]` display blocks instead of crowding inline prose.
- Use `\begin{aligned} ... \end{aligned}` to align operators; use line breaks and modest row spacing (for example, `\\[4pt]`) when legibility improves.
- Break broad formulas into separate lines for the estimator, standard error, test statistic, degrees of freedom, and confidence interval.
- Use `\frac{...}{...}` for important ratios and `\left(...\right)` for grouped terms where needed. Avoid unnecessarily wide, single-line expressions.
- Distinguish pooled-error and unequal-variance estimators; distinguish individual confidence intervals from simultaneous or multiplicity-adjusted intervals.
- Explicitly label reference groups and the direction of contrasts; ensure every displayed formula matches the implementation.
- Check balanced display-math delimiters and matching LaTeX environments before knitting; then inspect the actual rendered glyphs, equation width, spacing, and page breaks. A balanced delimiter count does not establish valid TeX or accurate mathematics.
- Do not insert raw Markdown bold tokens into executable R; keep math syntax outside code fences unless a code example is explicitly intended.

## 4. Figure production and float control

- Use a consistent scientific color mapping, readable axis labels with units, displayed sample size, legend/caption, and clearly documented transforms. Verify at actual page size.
- Never conflate a reversed **display axis** with transformed analysis data; preserve the original values and make the direction explicit in the caption.
- Distinguish mean markers, median/IQR boxes, whiskers, uncertainty bands, and confidence intervals.
- For paired or multipanel diagnostics, use a single plotting device if panels should appear as a unit; arrange panels explicitly and retain legible titles.
- If exact placement is required in a PDF, declare the supported LaTeX float package (for example, `\usepackage{float}`) and apply `fig.pos='H'` only to selected figure chunks. Inspect the result; forced placement can introduce whitespace and page overflow.
- A plot chunk with a caption can become a floating figure, appearing after the next heading; float settings must be reviewed on the final PDF, not inferred from the Rmd order.
- Avoid orphaned code, legends, figure captions, or section headings. Where possible, keep figure creation code and its output associated without oversized vertical gaps.
- Graphical reports should show the actual diagnostic evidence; a test statistic alone does not validate a plot.

## 5. Tables and statistical display

- Compact wide tables at the **display layer**, never by discarding scientific estimates or changing upstream results.
- Abbreviate repeated factor labels, join an estimate and its confidence bounds into one readable column, and keep headers short while preserving meaning.
- Use a consistent p-value presentation: `<0.001` for small values and three decimals for other p-values where appropriate. Do not display `0.000` as an observed p-value.
- Label whether intervals are individual or familywise/simultaneous; do not imply multiplicity adjustment when only the p-value was adjusted.
- Avoid splitting short tables across pages; split an oversized R chunk when it improves table grouping. A separate chunk does not guarantee keep-together behavior, so verify the rendered page.
- Use `\Needspace{<length>}` with `\usepackage{needspace}` for a heading or small block when justified; verify a single TeX backslash in the *actual* source. Keep raw TeX distinct from escaped strings in the language used to generate the file.
- If a native PDF table cannot fit, consider a supported long-table mechanism, landscape orientation, or concise display schema; do not rely solely on shrinking fonts.

## 6. Page layout and raw TeX

- Keep section headers with at least the first substantive paragraph, table, or code block; inspect section transitions at page boundaries.
- Use `\clearpage` cautiously to begin major sections or flush pending floats. An accidental `\\clearpage` in the underlying Rmd is not the intended single-backslash command and can print literally instead of inserting a page break.
- Forced `\clearpage` and `fig.pos='H'` solve different problems: the former separates/flushes content; the latter requests fixed figure placement. Neither should be applied mechanically to every section.
- Consider the final report as a whole: an isolated reference on its own page, a single continuation line, or a stranded discussion heading is a layout defect even when compilation passes.
- Preserve HTML compatibility when the source supports both PDF and HTML; raw TeX may be ignored outside PDF. Prefer format-specific controls if both targets matter.
- Long code lines must be wrapped into valid R expressions; leave calculations unchanged and inspect syntax after each wrap.

## 7. Source-to-PDF acceptance checklist

| Gate | Evidence required | Failure to catch |
| --- | --- | --- |
| A. Structure | All named chunks unique; complete fences; R brackets balanced; display-math pairs matched | Syntax/section corruption |
| B. Statistical fidelity | Computed outputs and formulas agree; reference groups, transforms and intervals documented | Editorial change alters inference |
| C. Render | Successful knit of the current revision; output date/checksum; warnings reviewed | Stale PDF treated as current |
| D. Pages | All pages inspected at reading scale; section boundaries and final pages assessed | Orphan headings and mostly empty pages |
| E. Figures | Axes/units, panels, legends, captions, reference marks and float placement legible | Clipped or displaced illustrations |
| F. Tables | Complete headers, readable cell widths, p-value precision, CI meaning, no damaging split | Misreported or unreadable comparisons |
| G. Grammar | Impersonal scientific prose, appropriate semicolons, citations and consistent notation | Personal voice, awkward p-value syntax |
| H. Reproducibility | Versioned source, explicit software versions, controlled input provenance, observed test state | Unverifiable artifacts |

**Acceptance rule:** The final PDF must be produced **after** the final source edit. Re-render and review all affected pages; report any unresolved defects rather than marking the document accepted. A checked code delimiter is only a structural screen.

## 8. General repair order

1. Inspect source and current rendered artifact; enumerate defects by page and component.
2. Correct scientific mislabeling or formula/code disagreement before cosmetic work.
3. Fix code overflow, p-value display, table width, equation alignment, and captions.
4. Adjust figure placement, diagnostic panel grouping, page breaks, and closing-section balance.
5. Run structural checks and source diff; execute code and knit if data/runtime are available.
6. Render the fresh PDF, inspect every page, and repeat only where the final artifact shows a defect.
7. Commit the reusable method improvements with the exact verification status; never import example-study data or findings into the methods manual.

## Related guidance

- [Canonical biomedical R Markdown conventions](BIOMEDICAL_R_CANONICAL_EXAMPLE.md)
- [Implementation and verification gates](IMPLEMENTATION_GATES.md)
- [Descriptive figure regression standards](DESCRIPTIVE_FIGURE_REGRESSION_STANDARDS.md)
