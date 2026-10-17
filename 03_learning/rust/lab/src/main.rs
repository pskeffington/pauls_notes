//! Synthetic teaching run: no GDC data files, no network, no model training.
#![forbid(unsafe_code)]

use breast_cancer_rust_lab::{
    engineering::{validate_person_split, MedianPreparation},
    objects::{describe_many, GeneAnnotation, Pair, Specimen, Tissue},
};

fn run() -> Result<(), &'static str> {
    let comparator = Specimen::new("Demo1", Tissue::Comparator, Some(10.0))?;
    let tumor = Specimen::new("Demo1", Tissue::Tumor, Some(20.0))?;
    let pair = Pair::new(comparator.clone(), tumor.clone())?;
    let change = pair.log2_change()?.ok_or("Expected a complete pair")?;

    let training = vec![comparator, tumor];
    let assessment = vec![
        Specimen::new("Demo2", Tissue::Comparator, None)?,
        Specimen::new("Demo2", Tissue::Tumor, Some(30.0))?,
    ];
    validate_person_split(&training, &assessment)?;
    let preparation = MedianPreparation::fit(&training)?;
    let prepared_assessment = preparation.transform(&assessment)?;
    let annotation = GeneAnnotation::new("ESR1", "hormone-related gene reference")?;
    let summaries = describe_many(&[&training[1], &annotation]);
    println!("SYNTHETIC Rust lab | example log2 change = {change:.3}");
    println!(
        "Training-only median = {:.3}; missing assessment imputed = {:.3}",
        preparation.median(),
        prepared_assessment[0]
    );
    println!("Trait summaries = {}", summaries.len());
    println!("Research and education only; no participant data, trained model, or clinical claim.");
    Ok(())
}

fn main() {
    if let Err(reason) = run() {
        eprintln!("Synthetic Rust lab refused input: {reason}");
        std::process::exit(1);
    }
}
