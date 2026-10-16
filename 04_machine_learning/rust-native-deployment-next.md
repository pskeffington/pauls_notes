# Rust G3 continuation: portable native-fit prediction

Authored by Paul Skeffington · Compiled with OpenAI

This is an **engineering-only continuation** of [G3 native training](rust-native-training.md), not a change to the frozen G3 study, not an additional independent assessment, and not a clinical model. The source contains synthetic paired-specimen category examples, never real TCGA-BRCA outcomes. The inference executable has no Linfa dependency and cannot fit any model.

## Artifact contract

The `frozen::FrozenModel` JSON schema v1 identifies `task=synthetic_paired_specimen_category`, `protocol_id=paired-assay-native-rust-v1`, `plan_name=final_development` and category 1 as the only positive class. It preserves the exact feature ordering, training-only medians/means/scales, coefficient vector and intercept from a fitted **final-development** model; reject outer-fold exports for downstream deployment. It excludes training rows and labels. The export must be constructed from a **previously audited** G3 `model-3.json` and its matching `development.json`, without any new optimizer fit or reserved people.

For an audited G3 bundle, a human or dedicated audited exporter maps `feature_names` from the development input, `preparation.medians/means/scales`, `coefficients_class_1`, and `intercept_class_1` from the final-development model. Check the G3 complete audit, plan identity, and input/model hashes before creating the JSON; an arbitrary JSON object is **not** proof of a reviewed training run.

```bash
cargo +1.90.0 fmt --manifest-path 04_machine_learning/rust/Cargo.toml -- --check
cargo +1.90.0 clippy --locked --manifest-path 04_machine_learning/rust/Cargo.toml --all-targets --all-features -- -D warnings
cargo +1.90.0 test --locked --manifest-path 04_machine_learning/rust/Cargo.toml --all-features
cargo +1.90.0 build --release --locked --manifest-path 04_machine_learning/rust/Cargo.toml --bin assay-native-predict
04_machine_learning/rust/target/release/assay-native-predict frozen.json specimens.csv /tmp/new-native-predictions
```

CSV headers must be `specimen_id` followed by the exact model feature order; empty and `NA` cells are missing, other cells require finite f64. Duplicate IDs, nonfinite values, dimension errors, invalid schema and output overwrite fail closed. Output stores `predictions.csv` and a `run.json` inventory with SHA-256 hashes. Prediction is deterministic given identical model/input bytes and compiled semantics.

## Validation and remaining gates

Unit fixtures test exact logits, median substitution, numerical saturation, malformed schema and bad inputs. Before promotion, execute an independent Python parity check against the original final-development G3 numerical probes (absolute error at most 1e-12), verify complete input/model lineage, and replay the output inventory on CI. Those parity checks are **not** claimed complete by introducing this code. The 15 reserved people remain untouched. This route is strictly for teaching and research software; no clinical use, prospective testing, prognostic claim, or TCGA-specific result follows.
