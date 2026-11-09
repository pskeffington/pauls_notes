# Agent-index gate evidence — 2026-10-30

[Agent roadmap](agent-tasking.md) · [Machine-index contract](machine-index.md) · [Task registry](agent-tasks.json) · [Validation script](../scripts/check_agent_tasks.py)

## Scope and revision

This evidence covers **documentation navigation, deterministic indexed Markdown coverage and agent task-graph integrity** on the branch `docs/agent-roadmap-index-20261030` proposed in [draft PR #35](https://github.com/pskeffington/pauls_notes/pull/35). It is **not** an authorization for clinical use, external source verification, release of participant data, or agent autonomy outside `AGENTS.md`.

| Checkpoint | Exact reviewed revision | Observed evidence |
| --- | --- | --- |
| Baseline machine-index CI after runner recovery and citation repair | `0c6181b81aff00a7df683994bd7c66e6ab883832` | [Run 41024862009](https://github.com/pskeffington/pauls_notes/actions/runs/41024862009): complete job success; source registry, CO-05/CO-06 R/Python, deterministic index and task registry checks passed |
| First coverage audit | `743fc11a2f1043e3a4ea6915a1b87982b25f7820` | [Run 41025393550](https://github.com/pskeffington/pauls_notes/actions/runs/41025393550): success; 1,147 sections, 126 documents, zero coverage/structural errors and **one orphan candidate** |
| Navigation repair and audit replay | `b8a9d1cf210ba77b5860a62cf91d688a45f7326a` | [Run 41025578262](https://github.com/pskeffington/pauls_notes/actions/runs/41025578262): success; **1,147 sections, 126 documents, zero broken links, zero missing/extra indexed documents, zero orphan candidates, zero structural errors** |

## Remediation record

- Zero-job `startup_failure` runs did not provide an actionable job log. The machine-index workflow was aligned with the repository's proven pinned-checkout and direct R installation pattern, and subsequent machine-index runs launched normally. This establishes **recovery**, not a definitive root cause for earlier GitHub-side startup failure.
- Reconciled eight existing source registry entries with the readable `oncology/evidence/SOURCES.md`. The citation validator returned zero issues; this did not constitute primary-study replication or external scientific review.
- The first orphan candidate was `04_machine_learning/rust-native-deployment-next.md`, a legitimate native-fit engineering continuation. Added incoming links from `04_machine_learning/README.md` and `04_machine_learning/rust-native-training.md`. The subsequent deterministic audit reported zero candidates.
- Added a task graph validator, regression tests, machine-index coverage audit and index audit artifact. The machine-index artifact contains **path and link metadata only**, not the full indexed manuscript text.

## Acceptance and limitations

Within the recorded branch revision, **IDX-01 technical index coverage and discovery routes passed** and **IDX-02 structured agent registry and graph validation passed**. These are bounded documentation/software checks, not clinical inference, semantic retrieval-quality evaluation or a scientific peer review. Dataset admission D0/D1, survival G4 and research reproduction G5 retain their independent statuses.

This record is historical and must not be used to claim a later revision or merge passed CI. The open pull request remains draft pending required review and any additional triggered workflows.
