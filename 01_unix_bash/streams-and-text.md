# Streams, pipes, and text tools

**Question:** How do we distinguish data flowing through commands from errors and missing matches?

Commands normally read **standard input** (file descriptor 0), write results to **standard output** (1), and write diagnostics to **standard error** (2). A pipe `|` connects one command's standard output to another's standard input.

~~~bash
printf 'zeta\nalpha\nalpha\n' | LC_ALL=C sort | uniq -c
printf '%s\n' 'Example warning' >&2
~~~

In the first line, the ordering is fixed to the C locale for the example. The second line writes a message to standard error. Redirection with `>` **truncates** an existing file; `>>` appends. Never point either at raw input unless replacement is intentional.

## Exit status is part of the result

In shell programs, status `0` conventionally means command success. Nonzero values require interpretation. For `grep`, status `1` normally means **no selected line** rather than an input read error, and status `2` signals an error in GNU grep.

~~~bash
if grep -F 'Treatment' sample.tsv; then
  printf 'At least one match\n'
else
  status=$?
  if [[ $status -eq 1 ]]; then
    printf 'No matching line\n'
  else
    printf 'grep could not complete (status %s)\n' "$status" >&2
    exit "$status"
  fi
fi
~~~

The example assumes `sample.tsv` exists in your working directory; it does not create it. Use `grep -F` for a literal string, not a regular expression. The result still requires semantic review: a matching value might occur in the wrong column.

## Physical lines versus records

~~~bash
wc -l < sample.tsv
head -n 3 sample.tsv
~~~

`wc -l` counts newline characters. For a correctly newline-terminated TSV with exactly one header row and one physical line per record, records = newline count minus one. That conclusion fails for malformed files and quoted multiline formats. `head` is inspection, not schema validation.

## Text formats have contracts

The example in this guide intentionally accepts only three **tab-separated** fields, a fixed header, two exact groups, and a limited numeric representation. This makes simple `awk` splitting auditable. It is **not a general CSV parser**: quoted delimiters, embedded newlines, escapes, locale-dependent decimal marks, and arbitrary field names require a format-aware parser such as Python's `csv` module or R's documented import tools.

Pipelines can conceal upstream failures when only the last exit status is used. In Bash, `set -o pipefail` makes the pipeline return a failure when any component fails, but `set -e` still has conditional and pipeline exceptions. Handle anticipated statuses explicitly and verify the **contents** of the produced output.

**References:** [Bash pipeline behavior](https://www.gnu.org/software/bash/manual/bash.html) · [GNU grep status](https://www.gnu.org/software/grep/manual/html_node/Exit-Status.html) · [GNU wc behavior](https://www.gnu.org/software/coreutils/manual/html_node/wc-invocation.html) · [Source register](reference-register.md)

**Next:** [Bash scripting](bash-scripting.md).
