# G3 source clarification before assessment

Authored by Paul Skeffington · Compiled with OpenAI

[Original frozen protocol](rust-training-protocol.md) · [Unchanged numerical contract](evidence/rust-training-contract-v1.json)

Recorded **2026-10-16 before generating or fitting the declared assessment**. Only analytical and tiny numerical fixtures have run. The original protocol is preserved at `1b0d8eda2498136d495ad2a97cf24015d6d34fb1`; its seeds, objective, budgets, tolerances and failure rules remain unchanged.

The installed **linfa-logistic 0.8.1** package identifies release source commit **`4484a55c8eb3105fcab5f6d5ed0c4cc0d2c2bbb0`** in `.cargo_vcs_info.json`. Its `src/lib.rs` has SHA-256 **`a242e4224df1294997f527a5670a9624927f692c8cce702b0e4bf3d377592fca`**. This is the authoritative installed-source hash for the runner's preflight. Its [immutable release source](https://github.com/rust-ml/linfa/blob/4484a55c8eb3105fcab5f6d5ed0c4cc0d2c2bbb0/algorithms/linfa-logistic/src/lib.rs) and [hyperparameters](https://github.com/rust-ml/linfa/blob/4484a55c8eb3105fcab5f6d5ed0c4cc0d2c2bbb0/algorithms/linfa-logistic/src/hyperparams.rs) were inspected against the installed crate.

The original source pointer (`3b411a4…`, from the literature review) is a newer development revision, even though its package manifest still says 0.8.1. It adds an offset interface and fixes binary label sorting. It is **not byte-identical to the published crate**. In the published release, `label_classes` uses counts and encounter order despite comments describing sorted labels. The implementation reads the fitted `labels().pos.class`, canonicalizes coefficients and intercept to category 1, checks its probabilities against Linfa's mapped probability output and tests both encounter orders and unequal counts. The published loss and gradient still use the declared sum logistic loss, alpha/2 coefficient penalty and unpenalized intercept. No offset is used.

This addendum supersedes the original upstream pointer/hash **only for identifying the installed package** and corrects attribution of the count/order behavior to the published release. It introduces no outcome-based redesign. The runner must verify both documents against their respective pre-assessment commits, as well as Cargo.lock and all computational source hashes. The original literature register remains a historical selected-source inspection, not a claim that that newer revision was the executed crate.
