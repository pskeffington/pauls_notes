#![forbid(unsafe_code)]
use breast_cancer_rust_lab::{
    engineering::{validate_person_split, MedianPreparation},
    foundations::{direction, log2_change},
    objects::{describe_many, GeneAnnotation, Pair, Specimen, Tissue},
};

#[test]
fn beginner_math_to_research_contract() {
    assert_eq!(
        direction(log2_change(20.0, 10.0).unwrap()).unwrap(),
        "higher in invented tumor measurement"
    );
    let train = vec![
        Specimen::new("Invented1", Tissue::Comparator, Some(10.0)).unwrap(),
        Specimen::new("Invented1", Tissue::Tumor, Some(20.0)).unwrap(),
    ];
    let test = vec![
        Specimen::new("Invented2", Tissue::Comparator, None).unwrap(),
        Specimen::new("Invented2", Tissue::Tumor, Some(50.0)).unwrap(),
    ];
    validate_person_split(&train, &test).unwrap();
    let prepared = MedianPreparation::fit(&train).unwrap();
    assert_eq!(prepared.transform(&test).unwrap()[0], 15.0);
    let pair = Pair::new(train[0].clone(), train[1].clone()).unwrap();
    let observed_change = pair.log2_change().unwrap().unwrap();
    assert!((observed_change - 1.0).abs() < 1e-12);

    let annotation = GeneAnnotation::new("CD8A", "immune marker context").unwrap();
    let displays = describe_many(&[&test[0], &annotation]);
    assert!(displays[1].contains("not a trained feature"));
    assert!(!displays.join("").contains("Invented2"));
}
