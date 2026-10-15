# Run and package an analysis

[Learning sections](README.md) · [Unix and Bash](../01_unix_bash/README.md)

## Deploy a complete local workflow

Here deployment means installing the requirements and executing a documented local analysis, not publishing a network service. The runner calls R with one explicit output-directory argument. It creates synthetic CSV inputs, imports them with declared types, validates the schema and keys, performs analysis, stages outputs, and publishes the run directory after success.

Requirements: Bash, Rscript, standard R packages and a writable output parent. From the repository root:

```bash
bash 03_learning/examples/run_case.sh /tmp/biomedical-learning-run
```

Choose a fresh destination for each run. Paths containing spaces are supported when quoted. The scripts refuse an existing output directory. The case takes no external input files, has no network calls, and does not install packages while running.

## Know what was produced

| Output | Meaning |
| --- | --- |
| `synthetic_registry.csv`, `synthetic_visits.csv` | Exact invented inputs used in the run |
| `observation_counts.csv` | People, visit rows, measured values and analysis-specific counts |
| `measurement_summary.csv` | Counts, missingness and mean for each occasion |
| `complete_pairs.csv` | Complete pairs and followup-minus-baseline changes |
| `model_coefficients.csv`, `model_summary.txt` | Baseline linear model and coefficient intervals |
| `mean_confidence.csv`, `individual_prediction.csv` | Distinct interval contracts over the observed age range |
| `feature_scaling.csv` | Feature status, including constant and unavailable rows |
| `diagnostics.pdf` | Paired trajectories, model plots and a feature display |
| `analysis_bundle.rds` | Inputs, analysis objects and measurement metadata |
| `session.txt` | R version, platform and loaded package information |
| `interpretation.txt` | Comparison direction, expected teaching results and limits |
| `output_checksums.csv` | Integrity inventory of the other fourteen files |

MD5 here detects ordinary file changes; it is not a security or authenticity guarantee. The checksum inventory excludes itself. PDFs and session information can differ across environments even when analysis tables agree.

## Connect shell mechanics to scientific checks

Quoting preserves a path as one argument. `set -euo pipefail` helps surface command failures but is not a substitute for checking the input contract or handling expected statuses. The R entry point requires exactly one argument and fails if assumptions are violated. A nonzero process status stops the wrapper.

For tabular inspection, `head`, `wc`, `cut`, `sort`, `uniq` and `awk` can help when their record and delimiter assumptions are valid. A line count includes a header; quoted CSV fields can contain commas and newlines. Use a parser for general CSV. Use `grep` to search text and distinguish a no-match status from an execution error. Avoid treating an arbitrary search match as a clinical category.

The separate [metadata example](../01_unix_bash/examples/summarize_metadata.sh) validates a deliberately constrained TSV before publishing a summary. Its [tests](../01_unix_bash/tests/test_summarize_metadata.sh) cover known output and malformed inputs. The new case extends the same process-status discipline into R objects and scientific figures.

## Stage before publishing

The R case writes to a temporary sibling directory, checks the RDS round trip, creates figures and inventories its files, then renames the completed directory into the chosen destination. Its cleanup handler removes an incomplete staging directory after a failure. This reduces the chance of mistaking partial files for a successful run. Use a local filesystem with rename support and do not run concurrent processes against the same destination.

The demonstration is not a general secure artifact store or a crash-recovery service. For study deployment, also pin dependencies, define data access, capture external input checksums, and record the code version and exact invocation in the [analysis record](../templates/analysis-record.md).

## Verify before adapting

```bash
bash -n 03_learning/examples/run_case.sh
Rscript --vanilla 03_learning/tests/test_research_case.R
python3 scripts/check_documentation.py
```

The contract tests exercise known counts and arithmetic, duplicate and unmatched keys, unavailable values, matrix alignment, interval width, the R command-line entry point, output checksums and overwrite refusal. R code embedded in the learning pages is parsed and executed during continuous integration; optional package examples are labeled separately.

## Transfer exercise

Run into a path containing spaces. Attempt a second run to the same path and confirm refusal. Open the checksum inventory and verify a selected file with an appropriate checksum tool. Explain why a successful run demonstrates reproducible computation under the recorded conditions rather than a biomedical discovery.

References: [Bash reference manual](https://www.gnu.org/software/bash/manual/), [R invocation and scripting](https://cran.r-project.org/doc/manuals/r-release/R-intro.html).
