# G4 execution and replay (synthetic only)

This code is **not an accepted G4 result**. It is an executable candidate under review in PR #19. The approved endpoint is the protocol in PR #18, which must first merge, with the first merged protocol commit recorded as `FROZEN_MERGE_SHA`. Never substitute the implementation branch commit for that freeze.

## Controlled local execution

Requirements: R with the `survival` package, Git, sha256sum (Linux coreutils), Python 3, and an output directory **outside** the Git checkout. No TCGA data, identifiers, external datasets, credentials, network downloads, or participant records are inputs.

```sh
python3 -m unittest scripts/tests/test_g4_survival_audit.py
Rscript scripts/tests/g4_survival_oracles.R
Rscript scripts/run_g4_survival.R /tmp/g4-survival-unique-run FROZEN_MERGE_SHA
python3 scripts/audit_g4_survival.py /tmp/g4-survival-unique-run
```

The runner refuses an existing output directory; its input is internally generated only. A failure is retained in `FAILURE.txt`. The second-process auditor recomputes censor KM and scores from development outcomes, rather than reading the first process's fitted censor weights. Reserved outcomes are not exported.

## Required evidence before any G4 promotion

1. Verify PR #18 merged and the freeze commit is anchored in `main`; preserve protocol and JSON SHA-256, R/survival versions, script commit, RNG version and seeds.
2. Confirm all numerical fixtures and negative tests pass, including absent/duplicate identities, corrupted losses, horizon-event and censor left-limit behavior, unsupported censor weights, reserved leakage, and mutation of held-out outcomes.
3. Execute once without seed hunting or horizon changes; preserve the complete first attempt, any failure, fold diagnostics and external-only evidence archive.
4. Independently replay on a second environment with the **same pinned runtime**; compare row identities, allocations, data hashes, predictions and metrics, and retain signed/hashed manifests.
5. Review any statistical failure and exception before merge. Even a numerical pass establishes only bounded synthetic software correctness, not full-procedure statistical uncertainty or clinical validity.

**Current limitations:** The runner and audit have not been executed in the available environment; their R API behavior, oracle consistency and model fitting must be verified. The auditor checks prediction/loss arithmetic but does **not yet independently reproduce Cox coefficients or absolute survival probabilities**. A second fitter or independent reference predictions must close that gap. Do not mark G4 Complete or change D0/D1 in this branch.

SYNTHETIC RESEARCH AND EDUCATIONAL USE ONLY — NOT FOR CLINICAL USE.
