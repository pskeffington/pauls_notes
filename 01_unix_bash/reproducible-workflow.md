# Reproducible workflow: synthetic metadata summary

**Research-computing question:** Can another person derive the same group counts from a fixed file without changing its source?

This independent example uses five **invented** records. It demonstrates input contracts, explicit missingness, deterministic output, and failure checks. It is not a clinical dataset and does not make a health claim.

## Input schema

| Field | Meaning | Accepted form |
| --- | --- | --- |
| `Sample_ID` | Invented record identifier | Unique ASCII letters/digits, underscore or hyphen, beginning with an alphanumeric |
| `Group` | Category | Exactly `Control` or `Treatment` |
| `Value` | Artificial measurement | Nonnegative digits with optional decimal fraction, or literal `NA` |

The file must use **tab** separators, a single header, newline-terminated records, and one record per line. Both groups must appear. Whitespace, quotes, signed values, scientific notation, embedded tabs, and arbitrary CSV syntax are deliberately not supported. IDs remain strings, not numbers.

## Run the example

From the repository root, create a fresh workspace. Quoted paths demonstrate safe handling of spaces.

~~~bash
work=$(mktemp -d "${TMPDIR:-/tmp}/pauls-workflow.XXXXXX") || exit 1
printf 'Sample_ID\tGroup\tValue\nS01\tControl\t0.7\nS02\tTreatment\tNA\nS03\tControl\t1.2\nS04\tTreatment\t0.9\nS05\tTreatment\t1.1\n' > "$work/sample metadata.tsv"
bash 01_unix_bash/examples/summarize_metadata.sh \
  "$work/sample metadata.tsv" "$work/group summary.tsv"
cat "$work/group summary.tsv"
printf 'Practice files: %s\n' "$work"
~~~

Expected result (tab-separated):

~~~text
Group       n_total  n_measured  n_missing
Control     2        2           0
Treatment   3        2           1
~~~

The displayed spacing above is for reading; the saved file contains tabs. `n_total = n_measured + n_missing` for each group. A missing value contributes to total and missing counts but does not become zero.

## Verify, then challenge the assumptions

~~~bash
bash -n 01_unix_bash/examples/summarize_metadata.sh
bash 01_unix_bash/tests/test_summarize_metadata.sh
~~~

The tests compare exact saved bytes for the expected output; check the original input was not changed; reject an existing destination; and reject bad headers, repeated identifiers, invalid groups, invalid measurement values, one-group files, empty inputs, and missing input files.

To explore failure in your own new workspace, change `Treatment` to an unsupported value and run the example against a **new destination filename**. It must fail without creating that output. Do not remove the practice directory until you have checked its path and no longer need the files.

## Interpretation and limitations

This pipeline establishes a simple computational counting claim, **not scientific eligibility**. A correct checksum or exit status cannot establish that groups are biologically comparable or that measurements were collected correctly. It deliberately does not calculate group means, perform hypothesis tests, parse real CSV, process patient data, or generalize to unfamiliar schemas. Use a proper table parser and domain-specific validation for real studies.

**Source and review:** [Reference register](reference-register.md) · [Bash scripting](bash-scripting.md). Example and tests were written independently for Paul's Notes and do not depend on private source files.
