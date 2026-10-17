#![forbid(unsafe_code)]
use assay_predict::{frozen::FrozenModel, Result};
use sha2::{Digest, Sha256};
use std::{
    collections::HashSet,
    fs::{self, OpenOptions},
    io::Write,
    path::Path,
};

fn run() -> Result<()> {
    let args: Vec<_> = std::env::args_os().skip(1).collect();
    if args.len() != 3 {
        return Err(
            "Usage: assay-native-predict FROZEN_MODEL.json SPECIMENS.csv NEW_OUTPUT_DIRECTORY"
                .into(),
        );
    }
    let model_bytes = fs::read(&args[0])?;
    let model = FrozenModel::from_json(&model_bytes)?;
    let input_bytes = fs::read(&args[1])?;
    let mut csv = csv::ReaderBuilder::new()
        .flexible(false)
        .from_reader(input_bytes.as_slice());
    let expected: Vec<&str> = std::iter::once("specimen_id")
        .chain(model.feature_names.iter().map(String::as_str))
        .collect();
    if csv.headers()?.iter().collect::<Vec<_>>() != expected {
        return Err("CSV requires exact model feature order".into());
    }
    let mut seen = HashSet::new();
    let mut predictions = Vec::new();
    for record in csv.records() {
        let record = record?;
        let id = &record[0];
        if id.is_empty()
            || id.trim() != id
            || id.chars().any(char::is_control)
            || !seen.insert(id.to_string())
        {
            return Err("Duplicate or invalid specimen ID".into());
        }
        let values: Vec<Option<f64>> = record
            .iter()
            .skip(1)
            .map(|s| {
                if s.trim().is_empty() || s.trim() == "NA" {
                    Ok(None)
                } else {
                    Ok(Some(s.trim().parse::<f64>()?))
                }
            })
            .collect::<Result<_>>()?;
        predictions.push((id.to_string(), model.predict(&values)?));
    }
    if predictions.is_empty() {
        return Err("No specimens".into());
    }
    let requested = Path::new(&args[2]);
    let name = requested
        .file_name()
        .ok_or("Expected output directory name")?;
    let parent = requested
        .parent()
        .filter(|p| !p.as_os_str().is_empty())
        .unwrap_or(Path::new("."))
        .canonicalize()?;
    let output = parent.join(name);
    let source = Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../..")
        .canonicalize()?;
    if output.starts_with(source) {
        return Err("Output must be outside repository".into());
    }
    fs::create_dir(&output)?;
    let mut writer = csv::Writer::from_writer(vec![]);
    writer.write_record(["specimen_id", "probability_class_1"])?;
    for (id, p) in &predictions {
        writer.write_record([id.as_str(), &p.to_string()])?;
    }
    let bytes = writer.into_inner()?;
    let mut file = OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(output.join("predictions.csv"))?;
    file.write_all(&bytes)?;
    file.sync_all()?;
    let record = serde_json::json!({
        "model_sha256": format!("{:x}",Sha256::digest(&model_bytes)),
        "input_sha256": format!("{:x}",Sha256::digest(&input_bytes)),
        "predictions_sha256": format!("{:x}",Sha256::digest(&bytes)),
        "rows": predictions.len(), "protocol_id": model.protocol_id,
        "positive_class": 1, "training_performed": false,
        "model_use": {
            "data_scope": "synthetic_paired_specimen_teaching_only",
            "clinical_use_authorized": false,
            "patient_level_training_authorized": false,
            "tcga_case_data_processed": false,
            "disclaimer": "RESEARCH AND EDUCATION ONLY. NOT FOR CLINICAL USE. No diagnosis, treatment selection, screening, or individual prognosis."
        }
    });
    let mut manifest = OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(output.join("run.json"))?;
    manifest.write_all(serde_json::to_string_pretty(&record)?.as_bytes())?;
    manifest.sync_all()?;
    println!(
        "Scored {} synthetic-schema specimen rows without training",
        predictions.len()
    );
    println!("RESEARCH AND EDUCATION ONLY. NOT FOR CLINICAL USE.");
    Ok(())
}
fn main() {
    if let Err(err) = run() {
        eprintln!("assay-native-predict: {err}");
        std::process::exit(1);
    }
}
