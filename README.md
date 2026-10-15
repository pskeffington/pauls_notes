# Paul's Notes

**Independent notes on computing and reproducible research**

**Author:** Paul Skeffington · **Prepared with OpenAI**

This repository is organized by subject and technical dependency, not by class, calendar week, assignment, or institution. Each published topic should have a usable explanation, authoritative references, a reproducible example where appropriate, and an explicit account of its limitations.

## Begin here

**[01 — Unix and Bash](01_unix_bash/README.md)**

Navigate files safely, reason about pipes and program status, write small Bash programs, and verify a synthetic research metadata workflow.

The next sections will be added only after their contents and references have been reviewed. Empty topic directories and placeholder lessons are intentionally omitted.

## Editorial and publication rules

- **Provenance first.** Use independent explanations and examples. Link to primary manuals and reputable teaching references; do not mirror their prose, examples, or lesson ordering.
- **Known-good gate.** A document must identify its assumptions, platform requirements, authoritative references, and failure modes. Executable examples require syntax checks and testable output contracts.
- **Scoped publication.** No private repository material, third-party teaching material, restricted study data, student submissions, or identifiable participant records are imported by default.
- **One canonical page per topic.** Prefer short, directly linked Markdown files to duplicate renderings or numbered week copies.
- **Clean changes.** Keep each commit focused; run the relevant checks before publishing, and use descriptive commit messages.

This is an independent reference notebook, not an official curriculum or a source of verified research findings. Examples use invented data; commands should be run only in workspaces you control.

## Validation

From the repository root:

~~~bash
bash -n 01_unix_bash/examples/summarize_metadata.sh
bash 01_unix_bash/tests/test_summarize_metadata.sh
~~~

The [Unix/Bash source register](01_unix_bash/reference-register.md) records documentation used for this first module. See the [MIT license](LICENSE) for this repository's license; linked external references retain their own terms.
