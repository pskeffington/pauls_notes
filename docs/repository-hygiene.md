# Repository hygiene and safe branch maintenance

[Home](../README.md) · [Contributing](../CONTRIBUTING.md) · [Git/GitHub from zero to push](../03_learning/git-github-from-zero-to-push.md) · [Scientific milestone gates](roadmap-gates.md)

**Audit date:** 2026-10-17. **Scope:** `pskeffington/pauls_notes` GitHub branch/PR snapshot and contributor tooling after [beginner Git guide PR #20](https://github.com/pskeffington/pauls_notes/pull/20) merged into `main` (squash merge `c40d8f3f1472d2f0266069aa5e0030930faf93dc`). This is a dated audit, not continuous monitoring.

## Current branch / PR inventory

On audit, GitHub exposed **22 remote branches**:

| Category | Count | Verified disposition |
| --- | ---: | --- |
| Main | 1 | Protected integration target; no force-push/history rewrite |
| Open PR heads | 2 | [#7 D0](https://github.com/pskeffington/pauls_notes/pull/7) (`feat/config-driven-ml-research-toolkit`) and [#19 G4](https://github.com/pskeffington/pauls_notes/pull/19) (`feat/g4-survival-execution-20261017`) stay intact for review |
| Historical heads of merged PRs | 17 | #1–#6, #9–#18 and #20 are **merged**; remote branch deletion remains a separate, reference-aware task |
| Legacy working branches | 2 | `work/biomedical-learning` has no commits ahead of `main` and is 62 behind at audit; `work/learning-check-coverage` is **5 ahead / 62 behind** and must be reviewed for unmerged work |

The historical-head set is:

`feat/phase4-assay-robustness-gates`, `docs/roadmap-gates-and-replication-contract`, `feat/phase4b-repeated-cohort-replication`, `feat/phase4c-person-uncertainty`, `feat/native-rust-training`, `feat/rust-native-frozen-deployment`, `docs/readme-reader-paths-20261016`, `docs/rust-coding-evidence-20261017`, `docs/rust-book-aligned-engineering-handbook-20261017`, `feat/rust-from-foundations-to-research-engineering`, `docs/roadmap-gate-evidence-20261017`, `docs/roadmap-r3-native-parity-accepted`, `docs/oncology-wide-research-scope-20261017`, `feat/standalone-synthetic-oncology-ml`, `docs/accept-r4-synthetic-oncology-ml-20261017`, `docs/g4-frozen-synthetic-survival-protocol-20261017`, and `docs/git-from-zero-to-push-20261017`.

**No remote branch has been deleted or force-updated by this audit.** A squash-merged PR can have a branch still showing commits “ahead” in ancestry comparisons. Use **PR merged status plus exact content/evidence review**, not simply `git branch --merged`, to identify safe deletion candidates. Preserve the G4 frozen-protocol branch until implementation links and its immutable merge/freeze reference have been reconciled. Even for merged branches, check documentation and external links before deletion. Git branch cleanup is *not* sensitive-data history erasure.

## Default maintenance policy

1. **One focused branch per change.** Start from current `main`, avoid duplicate open PRs and divergent long-lived branches, and use a descriptive `docs/`, `fix/`, `chore/` or `feat/` prefix.
2. **PR before main.** Check changed files, docs links, scripts, review requirements and exact-head CI. Squash ordinary docs changes where appropriate; preserve scientific protocol freeze/evidence refs regardless of merge strategy.
3. **Never promote research gates from housekeeping.** Keep G4 numerical acceptance separate from a green documentation build, and D0 privacy safeguards and D1 real-data admission separate from convenience workflows.
4. **Publish only reviewed sources.** Do not stage credentials, generated research runs, participant-linked inputs, model artifacts, restricted images/omics, or third-party data without explicit rights and study admission. `.gitignore` is convenience, **not** a content/access control; force-adding or already-tracked files can bypass it.
5. **Cleanup only after evidence check.** Confirm PR merge, frozen commit/hash permanence, source links, and any unmerged changes. Do not delete open PR heads or unreviewed `work/` branches. Use GitHub's branch-delete control after review, not a history rewrite.
6. **Preserve evidence.** CI run IDs, commit SHAs, failure records and frozen model/protocol bundles must retain auditable references even if a merged branch is later removed. Never equate branch deletion with deleting historic public Git objects.

## Commands for maintainers

```bash
git fetch --prune origin
git status
git branch -vv
git log --oneline --decorate -10
git diff --stat origin/main...HEAD
git ls-files
```

`git fetch --prune` updates **local remote-tracking references**; it does not delete GitHub branches. To investigate a branch, compare against `origin/main`, review its PR on GitHub and ensure the relevant files already exist in `main` or have a documented reason to remain separate. Do not delete a remote branch until its merge/freeze references and dependent links are checked.

For a new review, use the [PR template](../.github/pull_request_template.md), format according to [editor defaults](../.editorconfig), and execute the relevant [contribution checks](../CONTRIBUTING.md). An editor configuration does not replace repository tests.

## Open policy boundaries

The current `main` has only basic ignored runtime outputs. A more comprehensive cancer-wide ignore/scanning and source admission system is proposed in **draft D0 PR #7**; until its protection rules, history review, security checks and privacy approval are independently accepted, do **not** claim that these measures are enforced on `main`. **D1 real TCGA-BRCA study admission remains blocked.** G4's synthetic survival execution [draft PR #19](https://github.com/pskeffington/pauls_notes/pull/19) likewise cannot count as a passed independent numerical replay yet.
