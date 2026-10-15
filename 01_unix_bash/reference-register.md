# Reference register — Unix and Bash

**Reviewed:** 2026-10-15  
**Scope:** Public technical documentation for the independently authored Unix/Bash section of Paul's Notes.

| Source | Official or maintainer resource | Used to verify |
| --- | --- | --- |
| GNU Bash Reference Manual | https://www.gnu.org/software/bash/manual/bash.html | Shell interpretation, pipelines, exit status, expansion |
| GNU Bash — set builtin | https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html | `errexit`, `nounset`, and `pipefail` limitations |
| GNU Bash — parameter expansion | https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html | Parameters, quoting interactions, array expansions |
| GNU grep — exit status | https://www.gnu.org/software/grep/manual/html_node/Exit-Status.html | Match/no-match/error distinctions |
| GNU Coreutils — wc | https://www.gnu.org/software/coreutils/manual/html_node/wc-invocation.html | Counting newline characters rather than validated data records |
| Software Carpentry — Unix Shell | https://swcarpentry.github.io/shell-novice/ | General shell fundamentals and terminology |
| ShellCheck — SC2086 | https://www.shellcheck.net/wiki/SC2086 | Path quoting, splitting, and globbing risks |
| actions/checkout | https://github.com/actions/checkout | Checkout action used by automated tests |

## Acceptance rules

1. **Prefer primary public documentation** for command semantics, supplemented by established instructional or linting references. Link to the document; do not copy its protected text or example structure.
2. **Distinguish cited facts from tested implementation.** A correct manual link validates command semantics, not the correctness of an arbitrary script. The sample workflow has a separate executable test contract.
3. **Do not assume portability from a GNU manual.** Bash versions, BSD/macOS utilities, encoding, and locale can differ. The example avoids GNU-only switches; testing on a particular platform proves only that tested environment.
4. **Do not elevate unreviewed historical notes into a verified corpus.** This module is freshly organized and written. No private legacy files or restricted resource directories are copied into it.
5. **Require meaningful failure cases.** Verify exact outputs, unchanged inputs, schema rejection, and no partially published output before marking a runnable example ready.
6. **Retain scope and limits.** The provided TSV example is explicitly synthetic and intentionally narrow; it must not be presented as a production CSV or biomedical data parser.

## Status

- Documentation URLs: checked against authoritative or maintained public sources on the review date.
- Local example: `bash -n` and offline regression checks supplied in [the test file](tests/test_summarize_metadata.sh).
- Unverified platforms or claims: not represented as tested. External links and tools may change; recheck when updating the module.

**Author:** Paul Skeffington · Prepared with OpenAI.
