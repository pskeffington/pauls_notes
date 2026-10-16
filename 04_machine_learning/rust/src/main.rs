#![forbid(unsafe_code)]

use assay_predict::{predict_csv, Model, Result};
use sha2::{Digest, Sha256};
use std::fs::{self, OpenOptions};
use std::io::Write;
use std::path::Path;

fn run() -> Result<()> {
    let args: Vec<_> = std::env::args_os().skip(1).collect();
    if args.len() != 3 {
        return Err("Usage: assay-predict MODEL.json SPECIMENS.csv NEW_OUTPUT_DIRECTORY".into());
    }
    let model_bytes = fs::read(&args[0])?;
    let input_bytes = fs::read(&args[1])?;
    let model = Model::from_json(&model_bytes)?;
    // Validate and score the complete batch before creating any output.
    let predictions = predict_csv(input_bytes.as_slice(), &model)?;
    let output = Path::new(&args[2]);
    let filename = output
        .file_name()
        .ok_or("Output needs a new directory name")?;
    let parent = output
        .parent()
        .filter(|p| !p.as_os_str().is_empty())
        .unwrap_or(Path::new("."));
    let output = parent.canonicalize()?.join(filename);
    let source_root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
    if source_root.exists() && output.starts_with(source_root.canonicalize()?) {
        return Err("Choose an output directory outside the source repository".into());
    }
    fs::create_dir(&output)?; // Exclusive creation also rejects existing directories and symlinks.
    let file = OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(output.join("predictions.csv"))?;
    let mut writer = csv::Writer::from_writer(file);
    writer.write_record(["specimen_id", "probability_class_1"])?;
    for row in &predictions {
        writer.write_record([row.specimen_id.as_str(), &row.probability.to_string()])?;
    }
    writer.flush()?;
    let report = serde_json::json!({"schema_version": 1, "model_name": model.model_name,
        "task": model.task, "protocol_id": model.protocol_id, "specimens": predictions.len(),
        "input_features": model.feature_names.len(), "selected_features": model.selected_indices.len(),
        "positive_class": model.positive_class, "crate_version": env!("CARGO_PKG_VERSION"),
        "compiler": env!("ASSAY_RUSTC_VERSION"), "build_target": env!("ASSAY_BUILD_TARGET"),
        "os": std::env::consts::OS, "architecture": std::env::consts::ARCH,
        "model_sha256": format!("{:x}", Sha256::digest(&model_bytes)),
        "input_sha256": format!("{:x}", Sha256::digest(&input_bytes)),
        "predictions_sha256": format!("{:x}", Sha256::digest(fs::read(output.join("predictions.csv"))?)),
        "interpretation": "Frozen-model software replay on assay measurements; not clinical validation"});
    let mut file = OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(output.join("run.json"))?;
    file.write_all(serde_json::to_string_pretty(&report)?.as_bytes())?;
    println!(
        "Scored {} specimens with {}",
        predictions.len(),
        model.model_name
    );
    Ok(())
}

fn main() {
    if let Err(error) = run() {
        eprintln!("assay-predict: {error}");
        std::process::exit(1);
    }
}
