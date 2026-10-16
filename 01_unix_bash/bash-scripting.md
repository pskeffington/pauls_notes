# Bash scripting and failure contracts

**Question:** What must a script check before it changes files or claims success?

A shell script is a program. Its **inputs**, **output locations**, **dependencies**, and **exit status** should be explicit. `#!/usr/bin/env bash` selects Bash through the environment; running `bash script.sh` also selects Bash explicitly.

## Arguments and quoting

~~~bash
#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  printf 'Usage: bash inspect.sh PATH\n' >&2
  exit 2
fi
file=$1
[[ -f "$file" ]] || { printf 'Not a regular file\n' >&2; exit 2; }
printf 'Input path: %s\n' "$file"
~~~

The example is illustrative and does not modify the file. Always quote pathname expansions and use `"$@"` (not unquoted `$*`) to preserve individual positional arguments. Bash arrays are safer than constructing command strings:

~~~bash
names=("sample one.tsv" "sample two.tsv")
for name in "${names[@]}"; do
  printf 'Selected: %s\n' "$name"
done
~~~

Bash arrays and `[[ ... ]]` are Bash-specific; do not label this code portable `/bin/sh`. This guide avoids associative arrays and newer conveniences so its examples fit Bash 3.2 syntax.

## The limits of strict mode

`set -euo pipefail` is useful but **not a proof of correctness**. Bash's `-e` behavior differs inside conditionals, AND/OR lists, functions used as conditions, and pipelines. A program may return zero after selecting the wrong records. Check the operation's meaning as well as its process status.

For an expected non-match, write an `if` or `case` that interprets the error code. Do not casually attach `|| true` to data-validation commands: it erases evidence of actual errors.

## Safe output pattern

1. Reject missing, unreadable, or unrecognized inputs.
2. Require a destination directory that exists and is writable.
3. Refuse to replace an existing output unless overwrite is an explicit contract.
4. Create a unique temporary file **in the destination directory**.
5. Populate and validate it; use nonzero exit statuses for malformed data.
6. Move the completed file into place and clean up failed temporary outputs.

The [runnable example](examples/summarize_metadata.sh) implements this pattern for a single-writer toy task. It does not promise atomic no-clobber semantics under concurrent writers; real pipelines need locking or an appropriate atomic publication primitive.

## Review checklist

- [ ] Arguments, allowed formats, and schemas are documented.
- [ ] Variables and paths are quoted; no `eval` on untrusted input.
- [ ] Numeric fields are validated before computation.
- [ ] Expected nonzero statuses are distinguished from errors.
- [ ] Inputs stay unchanged; failures do not publish partial results.
- [ ] Tests cover success, missing input, bad schema, duplicate identifiers, and existing destinations.
- [ ] The script passes `bash -n`; use ShellCheck when available.

**References:** [Bash set builtin](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html) · [Bash parameter expansion](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html) · [ShellCheck SC2086](https://www.shellcheck.net/wiki/SC2086) · [Source register](reference-register.md)

**Next:** [Reproducible workflow](reproducible-workflow.md).
