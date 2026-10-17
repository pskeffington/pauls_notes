//! Standalone Chapter 11 Rust exercise. All six pairs are INVENTED teaching values.
//!
//! Run (outside any G3 training experiment):
//! rustc +1.90.0 --edition=2021 --test 02_biomedical_coding/examples/book_paired_specimens.rs -o /tmp/book-paired-tests
//! /tmp/book-paired-tests
//! rustc +1.90.0 --edition=2021 02_biomedical_coding/examples/book_paired_specimens.rs -o /tmp/book-paired-demo
//! /tmp/book-paired-demo
//!
//! Not an RNA-seq count model, TCGA analysis, biomarker or clinical tool.
#![forbid(unsafe_code)]

use std::collections::{BTreeMap, BTreeSet};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Tissue {
    Comparator,
    Tumor,
}

#[derive(Clone, Copy, Debug)]
struct Measurement {
    person: &'static str,
    tissue: Tissue,
    units: f64,
}

#[derive(Clone, Copy, Debug)]
struct CompletePair {
    person: &'static str,
    comparator: f64,
    tumor: f64,
}

// The book's Chapter 11 values: six fictional people, one measurement per tissue.
const BOOK_ROWS: [Measurement; 12] = [
    Measurement {
        person: "DemoPair1",
        tissue: Tissue::Comparator,
        units: 10.0,
    },
    Measurement {
        person: "DemoPair1",
        tissue: Tissue::Tumor,
        units: 20.0,
    },
    Measurement {
        person: "DemoPair2",
        tissue: Tissue::Comparator,
        units: 10.0,
    },
    Measurement {
        person: "DemoPair2",
        tissue: Tissue::Tumor,
        units: 40.0,
    },
    Measurement {
        person: "DemoPair3",
        tissue: Tissue::Comparator,
        units: 10.0,
    },
    Measurement {
        person: "DemoPair3",
        tissue: Tissue::Tumor,
        units: 10.0,
    },
    Measurement {
        person: "DemoPair4",
        tissue: Tissue::Comparator,
        units: 10.0,
    },
    Measurement {
        person: "DemoPair4",
        tissue: Tissue::Tumor,
        units: 5.0,
    },
    Measurement {
        person: "DemoPair5",
        tissue: Tissue::Comparator,
        units: 10.0,
    },
    Measurement {
        person: "DemoPair5",
        tissue: Tissue::Tumor,
        units: 20.0,
    },
    Measurement {
        person: "DemoPair6",
        tissue: Tissue::Comparator,
        units: 10.0,
    },
    Measurement {
        person: "DemoPair6",
        tissue: Tissue::Tumor,
        units: 10.0,
    },
];

/// Fail closed on duplicate specimens, missing partners or invalid measurements.
/// One pair means ONE independent invented person, not two independent records.
fn complete_pairs(rows: &[Measurement]) -> Result<Vec<CompletePair>, &'static str> {
    if rows.is_empty() {
        return Err("No paired measurements");
    }
    let mut by_person: BTreeMap<&str, (Option<f64>, Option<f64>)> = BTreeMap::new();
    for row in rows {
        if row.person.is_empty()
            || row.person.trim() != row.person
            || row.person.chars().any(char::is_control)
        {
            return Err("Invalid local teaching pair identity");
        }
        if !row.units.is_finite() || row.units <= 0.0 {
            return Err("Measurement must be positive and finite");
        }
        let (comparator, tumor) = by_person.entry(row.person).or_default();
        let entry = match row.tissue {
            Tissue::Comparator => comparator,
            Tissue::Tumor => tumor,
        };
        if entry.replace(row.units).is_some() {
            return Err("Duplicate tissue for a person");
        }
    }
    by_person
        .into_iter()
        .map(|(person, (comparator, tumor))| {
            Ok(CompletePair {
                person,
                comparator: comparator.ok_or("Missing comparator for a person")?,
                tumor: tumor.ok_or("Missing tumor for a person")?,
            })
        })
        .collect()
}

/// Logarithms avoid overflow when forming tumor/comparator for extreme positive f64.
/// These values are fictional comparable teaching units, NOT raw RNA-seq counts.
fn log2_contrasts(pairs: &[CompletePair]) -> Result<Vec<f64>, &'static str> {
    let mut results = Vec::with_capacity(pairs.len());
    for pair in pairs {
        if !pair.tumor.is_finite()
            || !pair.comparator.is_finite()
            || pair.tumor <= 0.0
            || pair.comparator <= 0.0
        {
            return Err("Invalid pair for log2 ratio");
        }
        let contrast = pair.tumor.log2() - pair.comparator.log2();
        if !contrast.is_finite() {
            return Err("Contrast overflow");
        }
        results.push(contrast);
    }
    if results.is_empty() {
        return Err("No contrasts");
    }
    Ok(results)
}

fn mean(values: &[f64]) -> Result<f64, &'static str> {
    if values.is_empty() || values.iter().any(|v| !v.is_finite()) {
        return Err("Invalid mean input");
    }
    let result = values.iter().sum::<f64>() / values.len() as f64;
    if !result.is_finite() {
        return Err("Mean overflow");
    }
    Ok(result)
}

/// Leave-one-person-out sensitivity, NOT a confidence interval.
fn leave_one_out_range(values: &[f64]) -> Result<(f64, f64), &'static str> {
    if values.len() < 2 {
        return Err("Need at least two independent pairs");
    }
    let mut min = f64::INFINITY;
    let mut max = f64::NEG_INFINITY;
    for omitted in 0..values.len() {
        let remaining: Vec<f64> = values
            .iter()
            .enumerate()
            .filter_map(|(i, &v)| if i == omitted { None } else { Some(v) })
            .collect();
        let estimate = mean(&remaining)?;
        min = min.min(estimate);
        max = max.max(estimate);
    }
    Ok((min, max))
}

/// A split partitions ALL people exactly once: never partition two specimens apart.
/// This checks identities only; it does NOT fit a predictor or use clinical records.
fn validate_person_partition(
    pairs: &[CompletePair],
    development: &[&str],
    assessment: &[&str],
) -> Result<(), &'static str> {
    let people: BTreeSet<&str> = pairs.iter().map(|pair| pair.person).collect();
    let train: BTreeSet<&str> = development.iter().copied().collect();
    let test: BTreeSet<&str> = assessment.iter().copied().collect();
    if people.is_empty()
        || train.is_empty()
        || test.is_empty()
        || train.len() != development.len()
        || test.len() != assessment.len()
        || !train.is_disjoint(&test)
        || train.union(&test).copied().collect::<BTreeSet<_>>() != people
    {
        return Err("Invalid or overlapping person-level partition");
    }
    Ok(())
}

fn run() -> Result<(), &'static str> {
    let pairs = complete_pairs(&BOOK_ROWS)?;
    validate_person_partition(
        &pairs,
        &["DemoPair1", "DemoPair2", "DemoPair3", "DemoPair4"],
        &["DemoPair5", "DemoPair6"],
    )?;
    let values = log2_contrasts(&pairs)?;
    let estimate = mean(&values)?;
    let (min, max) = leave_one_out_range(&values)?;
    println!("SYNTHETIC Chapter 11 | pairs={} | mean_log2={estimate:.3} | leave_one_out=[{min:.3},{max:.3}]", pairs.len());
    println!("Research teaching only; no TCGA data, clinical model or inference.");
    Ok(())
}

fn main() {
    if let Err(reason) = run() {
        eprintln!("Book exercise refused: {reason}");
        std::process::exit(1);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn near(left: f64, right: f64) {
        assert!((left - right).abs() < 1e-12, "{left} != {right}");
    }

    #[test]
    fn reproduces_the_books_six_pairs_and_mean() {
        let pairs = complete_pairs(&BOOK_ROWS).expect("six complete pairs");
        let contrasts = log2_contrasts(&pairs).expect("valid ratios");
        assert_eq!(pairs.len(), 6);
        for (observed, expected) in contrasts.iter().zip([1.0, 2.0, 0.0, -1.0, 1.0, 0.0]) {
            near(*observed, expected);
        }
        near(mean(&contrasts).expect("mean"), 0.5);
        let (min, max) = leave_one_out_range(&contrasts).expect("leave one out");
        near(min, 0.2);
        near(max, 0.8);
    }

    #[test]
    fn rejects_duplicate_or_missing_tissue_and_invalid_measurements() {
        let mut duplicated = BOOK_ROWS.to_vec();
        duplicated.push(BOOK_ROWS[0]);
        assert!(complete_pairs(&duplicated).is_err());
        assert!(complete_pairs(&BOOK_ROWS[..11]).is_err());
        let mut zero = BOOK_ROWS;
        zero[0].units = 0.0;
        assert!(complete_pairs(&zero).is_err());
        let mut nonfinite = BOOK_ROWS;
        nonfinite[0].units = f64::NAN;
        assert!(complete_pairs(&nonfinite).is_err());
        let mut infinite = BOOK_ROWS;
        infinite[1].units = f64::INFINITY;
        assert!(complete_pairs(&infinite).is_err());
    }

    #[test]
    fn rejects_person_overlap_duplicates_and_incomplete_partitions() {
        let pairs = complete_pairs(&BOOK_ROWS).expect("paired");
        assert!(validate_person_partition(
            &pairs,
            &["DemoPair1", "DemoPair2", "DemoPair3", "DemoPair4"],
            &["DemoPair5", "DemoPair6"]
        )
        .is_ok());
        assert!(validate_person_partition(
            &pairs,
            &[
                "DemoPair1",
                "DemoPair2",
                "DemoPair3",
                "DemoPair4",
                "DemoPair5"
            ],
            &["DemoPair5", "DemoPair6"]
        )
        .is_err());
        assert!(validate_person_partition(
            &pairs,
            &["DemoPair1", "DemoPair2", "DemoPair3", "DemoPair4"],
            &["DemoPair6"]
        )
        .is_err());
        assert!(validate_person_partition(
            &pairs,
            &[
                "DemoPair1",
                "DemoPair1",
                "DemoPair2",
                "DemoPair3",
                "DemoPair4"
            ],
            &["DemoPair5", "DemoPair6"]
        )
        .is_err());
    }

    #[test]
    fn rejects_unsupported_statistics_and_handles_extreme_positive_values() {
        assert!(mean(&[]).is_err());
        assert!(mean(&[f64::INFINITY]).is_err());
        assert!(leave_one_out_range(&[1.0]).is_err());
        let extreme = [CompletePair {
            person: "ExtremeSynthetic",
            comparator: f64::MIN_POSITIVE,
            tumor: f64::MAX,
        }];
        let result = log2_contrasts(&extreme).expect("safe log difference");
        assert!(result[0].is_finite());
        assert!(result[0] > 2000.0);
    }
}
