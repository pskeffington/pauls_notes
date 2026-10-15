# Unix and Bash

**Paul's Notes · Technical foundations**

Unix-like operating systems provide files, processes, streams, and command-line utilities. Bash supplies an interactive shell and a scripting language that can combine those tools into documented, repeatable operations.

## Reading path

| Topic | Outcome |
| --- | --- |
| [Filesystem and navigation](filesystem.md) | Resolve paths, inspect files, and avoid destructive operations |
| [Streams and text tools](streams-and-text.md) | Interpret exit status, pipes, redirection, and text-record contracts |
| [Bash scripting](bash-scripting.md) | Validate arguments, quote expansions, and handle failures intentionally |
| [Reproducible workflow](reproducible-workflow.md) | Execute a deterministic, synthetic metadata summary and check its result |
| [Reference register](reference-register.md) | Trace claims to authoritative public technical documentation |

**Runnable material:** [Example script](examples/summarize_metadata.sh) · [Regression tests](tests/test_summarize_metadata.sh)

## Environment

- An interactive terminal with **Bash 3.2 or later** for the illustrated Bash syntax.
- Standard Unix command-line utilities, including `pwd`, `ls`, `cat`, `printf`, `awk`, `mktemp`, `dirname`, `mv`, and `cmp`.
- Linux or macOS. The runnable example deliberately avoids GNU-only flags.
- No R, Python packages, internet connection, external dataset, or credentials are needed for the local example.

Confirm the interpreter:

~~~bash
bash --version
command -v awk
~~~

## Verify the example

Run from the repository root:

~~~bash
bash -n 01_unix_bash/examples/summarize_metadata.sh
bash 01_unix_bash/tests/test_summarize_metadata.sh
~~~

The test uses its own temporary directory, checks exact tabular output, confirms the source is unchanged, and verifies failure cases. If `shellcheck` is installed, it also lints the scripts. Review the [input contract](reproducible-workflow.md) before adapting the example.

## Mastery check

- [ ] I can distinguish a terminal program, shell interpreter, process, current directory, and pathname.
- [ ] I can use standard streams and state why `wc -l` is not automatically a record count.
- [ ] I can explain quoting and the distinction between a successful command and a scientifically valid result.
- [ ] I can run the tests, predict a rejected input, and describe why the output is withheld.
- [ ] I can identify which parts of the toy TSV reader would be unsafe for real-world CSV or regulated data.

**Authorship:** Paul Skeffington · Prepared with OpenAI. Independently written for this repository. External technical standards are linked, not reproduced.
