# Agent operating contract — Paul's Notes

Scope: the complete repository. Read this before editing. Repository owner: Paul Skeffington. This independent educational project covers computational oncology across cancer types; breast cancer and TCGA-BRCA are worked examples, not universal assumptions.

## Entry and authority order
1. `README.md` and `llms.txt`: human and machine navigation.
2. `docs/agent-tasking.md`: prioritized, bounded agent queue and acceptance contracts.
3. `oncology/book-manifest.json`, `oncology/ROADMAP.md`: chapter identity, prerequisites, publication plan.
4. `docs/roadmap-gates.md` and `docs/milestone-evidence.toml`: dated, scoped scientific/software gate evidence. Do not rewrite statuses without matching evidence and verification.
5. `docs/machine-index.md` and `docs/research-method-map.json`: retrieval/index contracts and method routing.

## Non-negotiable boundaries
- Do not copy protected course materials or imply institutional endorsement. Maintain independent original explanations and cite external science at the claim/section level.
- Use explicitly synthetic data by default. Never commit PHI, identifiable participant records, credentials, restricted controlled-access data or real TCGA specimen data without a separately documented admission and approval gate.
- Keep learning exercise correctness, executable software verification, scientific replication and clinical validation separate. No code result implies diagnosis, prognosis or clinical readiness.
- Preserve person-level grouping, preprocessing within training folds, documented estimands and reserved evaluation boundaries.
- Do not alter source or evidence registries to fabricate completed reviews; record unresolved references transparently.
- Do not mix G-series synthetic ML milestones with R-series engineering gates, D-series admission gates or CO chapter publication gates.

## Agent execution cycle
1. Inspect worktree, current branch, recent changes, issues/PRs and the task dependencies; select the highest-priority *unblocked* work item in `docs/agent-tasking.md`.
2. Verify target files, linked sources, relevant acceptance commands and evidence status before edits. If stale, reconcile the task record first.
3. Work in a focused feature branch/PR. Limit change to one gate or tightly coupled documentation slice. Never overwrite parallel work or silently merge to main.
4. For new textbook content, supply clinical framing, measurable objectives, formal notation, worked synthetic example, interpretation, assumptions, source-linked evidence, exercises, answer reasoning and reproducible checks. Update manifest only when the deliverable is actually present.
5. Run the relevant local checks and all affected existing test suites; record exact commands, pass/fail output and environmental blockers. No retroactive assertions of CI success.
6. Update navigation, source crosswalks and task statuses only after testing. Report changed paths, evidence, open limitations and next unblocked task in the PR.

## Baseline verification
```bash
python3 -m unittest discover -s scripts -p 'test_*machine_index.py' -v
python3 scripts/build_machine_index.py --output /tmp/pauls-notes-agent-index.jsonl
python3 scripts/build_machine_index.py --output /tmp/pauls-notes-agent-index.jsonl --check
python3 scripts/enrich_machine_index.py --input /tmp/pauls-notes-agent-index.jsonl --output /tmp/pauls-notes-agent-enriched.jsonl
python3 scripts/test_audit_machine_index.py
python3 scripts/audit_machine_index.py --input /tmp/pauls-notes-agent-enriched.jsonl --output /tmp/pauls-notes-agent-audit.json
python3 scripts/check_milestone_evidence.py
```
Confirm `--help` and tool availability before adding optional strict-link or external tool gates. Run chapter-specific and ML tests when their files are touched. Do not treat this command list as proof it ran.

## Agent handoff record
Every PR or checkpoint must state: task ID; scope and modified files; base/head SHA; source/data classification; executed tests and observed outcomes; evidence artifacts; limitations/blockers; whether status or indexing was updated; next task. If blocked, stop the disallowed operation and continue with the next independent task rather than inventing clearance.
