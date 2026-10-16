#![forbid(unsafe_code)]
use assay_predict::{
    training::{fit, Input, Settings},
    Result,
};
use sha2::{Digest, Sha256};
use std::{
    fs::{self, OpenOptions},
    io::Write,
    path::Path,
};

fn run() -> Result<()> {
    let args: Vec<_> = std::env::args_os().skip(1).collect();
    if args.len() != 2 {
        return Err("Usage: assay-train DEVELOPMENT.json NEW_OUTPUT_DIRECTORY".into());
    }
    let bytes = fs::read(&args[0])?;
    let input: Input = serde_json::from_slice(&bytes)?;
    input.validate()?;
    let requested = Path::new(&args[1]);
    let name = requested
        .file_name()
        .ok_or("Output requires a new directory name")?;
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
        return Err("Choose output outside the source repository".into());
    }
    fs::create_dir(&output)?;
    let mut attempts = OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(output.join("attempts.jsonl"))?;
    for (index, plan) in input.plans.iter().enumerate() {
        writeln!(
            attempts,
            "{}",
            serde_json::json!({"plan":plan.name,"status":"started"})
        )?;
        attempts.sync_all()?;
        let fitted = match fit(&input, index, Settings::default()) {
            Ok(fitted) => fitted,
            Err(error) => {
                writeln!(
                    attempts,
                    "{}",
                    serde_json::json!({"plan":plan.name,"status":"failed","error":error.to_string()})
                )?;
                attempts.sync_all()?;
                return Err(error);
            }
        };
        fs::write(
            output.join(format!("model-{index}.json")),
            serde_json::to_vec_pretty(&fitted)?,
        )?;
        writeln!(
            attempts,
            "{}",
            serde_json::json!({"plan":plan.name,"status":"complete","model_file":format!("model-{index}.json")})
        )?;
        attempts.sync_all()?;
    }
    fs::write(
        output.join("run.json"),
        serde_json::to_vec_pretty(&serde_json::json!({
            "protocol_id":input.protocol_id,"models":input.plans.len(),"input_sha256":format!("{:x}",Sha256::digest(&bytes)),
            "build_profile":env!("ASSAY_BUILD_PROFILE"),"opt_level":env!("ASSAY_OPT_LEVEL"),"rustflags":env!("ASSAY_RUSTFLAGS"),
        "compiler":env!("ASSAY_RUSTC_VERSION"),"target":env!("ASSAY_BUILD_TARGET"),"precision":"f64",
            "linfa":"0.8.1","linfa_logistic":"0.8.1","ndarray":"0.16.1",
            "iterations_and_termination":"unavailable from fitted public API; separate gradient residual required"
        }))?,
    )?;
    println!(
        "Fitted {} development-only native models",
        input.plans.len()
    );
    Ok(())
}
fn main() {
    if let Err(error) = run() {
        eprintln!("assay-train: {error}");
        std::process::exit(1);
    }
}
