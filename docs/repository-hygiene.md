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


## Legacy-work reconciliation and CI cleanup — 2026-10-17 follow-up

This is an additional audit against `main` at `dd479979730ab34bc9f1acc87919657a369882cd`, not a replacement for the dated 22-branch snapshot above. See [housekeeping Issue #22](https://github.com/pskeffington/pauls_notes/issues/22) for branch disposal review.

- **`work/biomedical-learning`:** GitHub comparison reported **zero commits ahead / 63 behind** with no changed files. The branch adds no changes to current `main`, but remote deletion remains a separate decision after reference checks.
- **`work/learning-check-coverage`:** GitHub reported **five commits ahead / 63 behind**, reflecting an old parallel history. Every one of its **22** differing paths was checked against `main`. **Ten** existing paths have byte-identical Git blobs, **eleven** contain later main-side edits (navigation, modernized function names, test adjustments or improved documentation-validation logic), and **one** old-named test does not exist at its former path. The obsolete historical `test_hse_stats_plots.R` (in the resource tests folder) corresponds to the retained [current `test_stats_plots.R`](../06_RESOURCES/tests/test_stats_plots.R): the latter preserves the statistical/plot checks using current non-`hse_` function names and includes extra negative cases. No missing current learning capability was identified in the file comparison. This is **content reconciliation, not a claim that the old commits were rebased or that the branch was deleted**.
- **CI triggers:** historical feature-branch **push** triggers were present in `native-rust-training.yml`, `assay-uncertainty-validation.yml` and `assay-replication-validation.yml`. The cleanup retains **main-only push**, path-filtered **pull requests**, and **manual dispatch**, without changing fitting code, scientific baselines or artifact handling. Previously archived CI evidence remains referenced by its immutable run/commit identities.
- **Tracked-build hygiene:** `scripts/check_repository_artifacts.py` and its positive/negative controls reject accidentally tracked editor files and build/runtime directories. Curated figures, book materials, pinned lockfiles, example reports and evidence artifacts are intentionally preserved. This **does not** detect participant-linked data, credentials, privacy breaches or licensing issues: D0 must still pass separately.

**Deletion disposition:** `work/biomedical-learning` is content-obsolete; `work/learning-check-coverage` is content-reconciled but has five non-ancestor commits and needs final historical/link review before remote deletion. The frozen G4 protocol remains anchored at merged PR #18 commit `d53de90837342d661e5528e8d7c15995e5bccd01`; its branch is **not** a deletion candidate until PR #18 branch-qualified links and ongoing G4 implementation references are reconciled. **No remote refs were deleted by this pass.**


## Branch retention review instrument — 2026-10-17 pass

At the latest pre-change GitHub inventory, there were **24 remote heads**: `main` (1), **19** historical heads of already merged PRs (#1–#6, #9–#18, #20–#21, #23), active drafts [D0 #7](https://github.com/pskeffington/pauls_notes/pull/7) and [G4 #19](https://github.com/pskeffington/pauls_notes/pull/19) (2), and two `work/` legacy branches. This is a dated snapshot; the new `chore/` branch used for this change adds another temporary head during review.

The descriptions of the merged PRs were inspected for branch-dependent file links. Previously identified links in PRs #6, #15 and #18 now refer to immutable merged commits; the reviewed merged-PR bodies no longer have known GitHub `blob/` or `tree/` links tied to those original heads. **This does not establish that external sites, comments, issue text, forks, other refs, or old workflow logs contain no branch links.** G4's initial protocol still retains an explicit hold even though its first merged freeze commit is recorded.

### Run the read-only branch classifier

From a **full-history checkout** exactly at the current `main` HEAD (non-shallow, with all branch objects available), with GitHub read access via a local token:

```bash
python3 -m unittest discover -s scripts/tests -p 'test_branch_retention.py' -v
GITHUB_TOKEN="$(gh auth token)" python3 scripts/audit_branch_retention.py --repository pskeffington/pauls_notes --scan-root . --output /tmp/branch-retention-review.json
```

Alternatively, open **GitHub Actions → Read-only branch retention audit → Run workflow**. The same read-only report runs automatically on a `main` push that changes the auditor, its tests or workflow file. Its report artifact is `branch-retention-review` with 14-day retention. The workflow has read-only GitHub permissions and **no delete/update-ref operation**. The resulting JSON includes branch head SHAs, associated PR numbers, immutable merged SHAs, known branch-qualified link counts and an explicit disposition; it does **not** include PR-body text or any research dataset.

| Report decision | Interpretation |
| --- | --- |
| `default_hold` / `protected_hold` | Keep integration/protected branch |
| `active_pr_hold` | Keep open PR head, including D0/G4 |
| `frozen_protocol_hold` | Keep G4 protocol branch until explicit freeze/reference review |
| `legacy_work_hold` | Keep reviewed-but-not-deletion-approved `work/` branch |
| `referenced_hold` | Known direct GitHub branch URL still present in scanned text/PR bodies |
| `merged_head_mismatch_hold` | Historical merged PR head SHA is missing or no longer matches the live branch SHA; keep branch |
| `unscanned_source_hold` | No exact-main source scan supplied; do not make a cleanup candidate |
| `incomplete_text_scan_hold` | One or more supported text files were skipped; review and rescan |
| `diverged_history_hold` / `history_unverified_hold` | Merged PR branch is not contained in `main`, or the local Git object/reachability check could not prove it; preserve pending reconciliation |
| `merged_manual_review` | One merged same-repository PR **with an identical current head SHA**, complete exact-main source scan, no known branch-qualified links, **and Git-proven ancestry into `main`**; **human review only** |
| `unresolved_hold` | Missing/ambiguous/unmerged PR association; no deletion without investigation |

Classification fails if a supplied checkout does not equal the exact current default-branch SHA, or if inventory branch names duplicate. Its reference scan checks supported tracked text up to 2 MB per file and PR **bodies**; it cannot prove that no references remain outside those boundaries. The audit does not delete anything, does not approve deletion, and never rewrites history. As additional fail-closed rules, a historical merged-PR head is **not** a manual-review candidate unless its PR-recorded SHA exactly equals the live branch SHA, the complete default-branch text scan has no skipped files, and `git merge-base --is-ancestor` proves that branch head is reachable from `main`. The GitHub Actions checkout fetches full history (`fetch-depth: 0`); missing Git objects or unverified ancestry yield an explicit hold, not a candidate. Existing external references and PR comments still require separate human review. When a candidate is explicitly cleared, verify that its remote branch head still matches the recorded SHA, confirm no essential links/evidence are lost, then use GitHub's branch-management control and record the change in [Issue #22](https://github.com/pskeffington/pauls_notes/issues/22).

### Verified run and ancestry shortlist — 2026-10-17

The first automatic read-only audit was executed on `main` at `e74257220f180d80b2b2df474c2e370320b7b9f0`: [workflow run 39073658807](https://github.com/pskeffington/pauls_notes/actions/runs/39073658807), artifact `branch-retention-review` (ID `12115858172`, SHA-256 `beb7079c517e81ab901b08455a2954fc709b3a0351ebb4f9506c41a3cdb378b2`). The report shows **26 branches**, **zero skipped text files**, 20 former `merged_manual_review` entries, and six holds: default (1), active PRs (2), frozen G4 protocol (1), and legacy `work/` (2).

**Why the new ancestry requirement matters:** the first report did not check whether a squash-merged branch's own commits remain reachable from `main`. A separate GitHub comparison established that only the five historical PR heads below are already ancestors of `main`. The revised classifier must confirm this itself in a new live run before emitting any `merged_manual_review` result. The other 15 formerly eligible merged heads remain under `diverged_history_hold` or `history_unverified_hold` until their histories are reconciled.

| PR | Former merged branch | Verified branch head SHA |
| --- | --- | --- |
| [#1](https://github.com/pskeffington/pauls_notes/pull/1) | `feat/phase4-assay-robustness-gates` | `51a10cb49a3f85bb79230a791028d0fc046d1273` |
| [#2](https://github.com/pskeffington/pauls_notes/pull/2) | `docs/roadmap-gates-and-replication-contract` | `51da68aec9738179102c615bd117e6471e4eaf71` |
| [#3](https://github.com/pskeffington/pauls_notes/pull/3) | `feat/phase4b-repeated-cohort-replication` | `cc5a208147fd59143b44c1711f07bacbbecd4517` |
| [#4](https://github.com/pskeffington/pauls_notes/pull/4) | `feat/phase4c-person-uncertainty` | `daa6650537d259d87e4c3b6f396b1fe08bfa173c` |
| [#5](https://github.com/pskeffington/pauls_notes/pull/5) | `feat/native-rust-training` | `9b468ebec1043df81d91465f0816e40c27bc48f8` |

The legacy `work/biomedical-learning` branch is also contained in `main` but remains on `legacy_work_hold`; its lack of an associated merged PR and external-reference review prevents automatic clearance. **No branch has been deleted.** GitHub issue/PR comments, archived workflows, other repositories, bookmarks, and external sites are outside the audit's URL-scan boundary; an operator must review those and recheck exact remote SHA before deleting any branch.

**Scientific and privacy boundary:** This classifier is not a D0 access/secret scan, not a D1 admission check, and does not accept G4 survival or release any participant-level information. Data and scientific gate counts are unchanged by branch housekeeping.


## Single-branch retirement after explicit approval

A separate [Guarded historical branch retirement](../.github/workflows/guarded-branch-retirement.yml) GitHub Actions workflow can delete **one historical branch per manual dispatch**. It cannot run on pull requests or ordinary pushes. It is restricted to the `pskeffington` actor on `main`, and it has a fixed reviewed allowlist of only the five branch/SHA pairs in the preceding table. Do not add the frozen G4 protocol, D0/G4 draft heads or divergent/legacy branches to this allowlist without a separately reviewed evidence record.

A maintainer must complete all of the following before dispatch:

1. Review external websites, bookmarks, related issue comments, archived run dependencies and other repositories for links that still depend on the exact historical branch. The read-only auditor checks only its documented repository and PR-body scope.
2. Record **one exact owner-authored comment** on [Issue #22](https://github.com/pskeffington/pauls_notes/issues/22) in this format (replace both placeholders with the approved branch and its full 40-character SHA):

   ```text
   APPROVE BRANCH RETIREMENT <branch> <40-character-sha>
   ```

   This is a separate authorization, not a comment the workflow creates automatically. The preflight reads Issue #22, verifies the author's GitHub username and exact branch/SHA approval text, and rejects missing or altered approvals.
3. Open **Actions → Guarded historical branch retirement → Run workflow**, select `main`, select the approved branch, and paste its full reviewed SHA. For the confirmation field, type exactly `DELETE ` followed by the chosen branch name. Check **external_refs_reviewed** only once that review is complete.
4. The workflow reruns all branch-retention tests and the complete GitHub read-only audit against the current `main`; it refuses stale inventories, missing/skipped source checks, changed branch heads, links, divergent ancestry, unexpected PR associations, and unapproved branch/SHA combinations.
5. Only after all checks pass does a single `git push --force-with-lease` request remove the selected remote ref. The lease makes deletion fail if its SHA changed. GitHub's own branch protection and repository permissions also apply. The workflow checks that the remote branch is absent afterwards and retains a success/failure receipt for 90 days. Never treat a preflight receipt alone as deletion evidence.
6. Update Issue #22 with the workflow run URL, the removed ref, prior branch SHA, retained merged-PR SHA and post-deletion verification. Re-run the **Read-only branch retention audit** on `main` and confirm the remaining branch set. Repeat for another approved branch only after independently reviewing its evidence.

The workflow uses `contents: write` **only in the manual retirement job**, with `pull-requests: read` and `issues: read` for verification. It never force-pushes `main`, rewrites history, alters models, removes tagged/merged commits, or runs unattended. The audit may not find every off-repository link, so manual approval is substantive, not a formality. Failure to establish sufficient evidence means **keep the branch**.

**No branch is deleted merely by merging this workflow.** Scientific/privacy milestones G4, D0 and D1 are not affected by branch-retention operations.
