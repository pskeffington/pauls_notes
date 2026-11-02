# Triple-block analytical reporting contract

Applies to all numerical analysis, simulations, statistical examples, model evaluation, tables, and reporting code in Paul's Notes, including R, Python, Rust, R Markdown, Quarto, and Markdown teaching materials.

## Required sequence: code / result / interpretation

For each reported analytical claim, supply three contiguous, explicitly identifiable blocks.

1. **BLOCK 1 — METHOD AND EXECUTABLE CODE.** State the research question and observation unit; specify inputs, sampling/exposure denominator, assumptions, estimator/model, seed, and execution code. For R Markdown use a named, closed `\`\`\`{r chunk_name}` chunk, with `echo=TRUE` when the reader needs to see code.
2. **BLOCK 2 — COMPUTED NUMERICAL RESULT.** Show the actual output from the immediately preceding code: N, analyzed n, missing counts, units, event denominators, proportions/rates, estimates and uncertainty, and table/figure labels. Use `knitr::kable()` and executable inline R where appropriate. Never type plausible-looking numerical results into the report before running the analysis. Identify synthetic data.
3. **BLOCK 3 — SCIENTIFIC INTERPRETATION.** Explain exactly what the output supports, study-design limitations, uncertainty, diagnostics/assumptions, and whether an association is causal or not. If not executed, say explicitly `Not executed; no numerical result verified`.

Each block should be a clearly marked heading or section; a line of three backticks is a **code fence**, not a separator for prose. Use Markdown headings or horizontal rules to separate prose blocks, not empty code fences. Do not insert triple-backtick markers into standalone `.R` or `.py` source files. For command-line programs, document the three blocks in adjacent Markdown, or in a generated report.

## Standard R Markdown example

The following outer fence is for displaying the example in Markdown; use the inner R chunks in a real `.Rmd`:

~~~~markdown
### Block 1 — Method and executable code

Question: Among 80 independent observations, how many meet the endpoint?
The code below uses **synthetic** binary observations solely to demonstrate reporting.

```{r endpoint-summary, echo=TRUE}
response <- c(rep(TRUE, 36L), rep(FALSE, 44L))
n_total <- length(response)
n_observed <- sum(!is.na(response))
n_missing <- n_total - n_observed
n_responders <- sum(response, na.rm = TRUE)
proportion <- n_responders / n_observed
```

### Block 2 — Computed numerical result

```{r endpoint-table, echo=TRUE}
knitr::kable(data.frame(
  total_N = n_total,
  observed_n = n_observed,
  missing_n = n_missing,
  responders = n_responders,
  responder_proportion = proportion
))
```

### Block 3 — Scientific interpretation

The synthetic sample has `r n_responders` responses among
`r n_observed` evaluable observations (`r sprintf("%.1f%%", 100 * proportion)`).
The sample proportion is descriptive and is not evidence of treatment efficacy.
~~~~

## Audit gates

- Check every code fence is balanced and correctly labeled; nested examples should use longer outer fences.
- Ensure each analytical step has corresponding numerical result and interpretation; no orphan tables, figures, or p-values.
- Verify each reported value against the generating code (and the data where available).
- Report denominators and missingness explicitly; never equate `N`, analyzed `n`, events, and person-time.
- Confirm confidence intervals, p-values and model diagnostics were actually produced by executable code.
- Avoid output duplication and hard-coded results that can become stale.
- Keep code unchanged unless there is a demonstrable defect; preserve all author-written prose **verbatim**, including spelling and typos, unless the author authorizes edits.
- Treat analysis using real patient-level records separately; never push restricted data or identifiers.
- R Markdown/Quarto: knit/render and inspect the result. Plain `.R` scripts: run tests and produce a report or documented sample output.
- Record **PASS / FAIL / NOT RUN** for each verification. A formatting audit alone is not scientific verification.

## Migration priorities

1. Numerical R Markdown/Quarto coursework and reports (including existing local work not present in this repository).
2. `03_learning` statistical examples and worked problems.
3. `04_machine_learning` evaluation and validation outputs.
4. `02_biomedical_coding` and cancer research protocols and computational illustrations.
5. All other scripts and documents producing numerical claims.

This contract is format-only until run results are independently validated. Do not bulk-reformat source files where triple-backtick fences would cause syntax errors.
