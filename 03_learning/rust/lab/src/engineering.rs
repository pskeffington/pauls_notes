//! Study-aware boundaries: validate paired people, fit a training-only median,
//! and transform untouched assessment people. No prediction model is fitted.

use crate::objects::{Specimen, Tissue};
use std::collections::{BTreeMap, BTreeSet};

fn complete_people(rows: &[Specimen]) -> Result<BTreeSet<&str>, &'static str> {
    if rows.is_empty() {
        return Err("Empty partition");
    }
    let mut by_person: BTreeMap<&str, BTreeSet<Tissue>> = BTreeMap::new();
    for specimen in rows {
        let tissues = by_person.entry(specimen.person_id()).or_default();
        if !tissues.insert(specimen.tissue()) {
            return Err("Duplicate tissue for person");
        }
    }
    if by_person.values().any(|tissues| tissues.len() != 2) {
        return Err("Each fictional person must contribute both tissues");
    }
    Ok(by_person.keys().copied().collect())
}

/// Splits must preserve person groups. This example requires complete fictional pairs.
pub fn validate_person_split(
    train: &[Specimen],
    assessment: &[Specimen],
) -> Result<(), &'static str> {
    let training_people = complete_people(train)?;
    let assessment_people = complete_people(assessment)?;
    if !training_people.is_disjoint(&assessment_people) {
        return Err("Person leakage between training and assessment");
    }
    Ok(())
}

/// Encapsulate a statistic that was fitted only on development/training records.
#[derive(Clone, Copy, Debug)]
pub struct MedianPreparation {
    training_median: f64,
}

impl MedianPreparation {
    pub fn fit(training: &[Specimen]) -> Result<Self, &'static str> {
        if training.is_empty() {
            return Err("No training specimens");
        }
        let mut values = Vec::new();
        for row in training {
            if let Some(value) = row.measurement() {
                if !value.is_finite() || value <= 0.0 {
                    return Err("Invalid observed training measurement");
                }
                values.push(value);
            }
        }
        if values.is_empty() {
            return Err("All training measurements missing");
        }
        values.sort_by(f64::total_cmp);
        let middle = values.len() / 2;
        let median = if values.len().is_multiple_of(2) {
            values[middle - 1] / 2.0 + values[middle] / 2.0
        } else {
            values[middle]
        };
        if !median.is_finite() || median <= 0.0 {
            return Err("Training preprocessing overflow");
        }
        Ok(Self {
            training_median: median,
        })
    }

    pub fn median(&self) -> f64 {
        self.training_median
    }

    pub fn transform(&self, rows: &[Specimen]) -> Result<Vec<f64>, &'static str> {
        rows.iter()
            .map(|row| {
                let measurement = row.measurement().unwrap_or(self.training_median);
                if !measurement.is_finite() || measurement <= 0.0 {
                    Err("Invalid transformed measurement")
                } else {
                    Ok(measurement)
                }
            })
            .collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn specimen(person: &str, tissue: Tissue, value: Option<f64>) -> Specimen {
        Specimen::new(person, tissue, value).unwrap()
    }

    #[test]
    fn split_prevents_person_leakage() {
        let train = vec![
            specimen("Demo1", Tissue::Comparator, Some(10.0)),
            specimen("Demo1", Tissue::Tumor, Some(20.0)),
        ];
        let test = vec![
            specimen("Demo2", Tissue::Comparator, Some(30.0)),
            specimen("Demo2", Tissue::Tumor, None),
        ];
        assert!(validate_person_split(&train, &test).is_ok());
        let overlapping = vec![
            specimen("Demo1", Tissue::Comparator, Some(50.0)),
            specimen("Demo1", Tissue::Tumor, Some(100.0)),
        ];
        assert!(validate_person_split(&train, &overlapping).is_err());
        assert!(validate_person_split(&train[..1], &test).is_err());
    }

    #[test]
    fn assessment_mutation_cannot_change_fitted_median() {
        let train = vec![
            specimen("Demo1", Tissue::Comparator, Some(10.0)),
            specimen("Demo1", Tissue::Tumor, Some(20.0)),
        ];
        let original = vec![
            specimen("Demo2", Tissue::Comparator, None),
            specimen("Demo2", Tissue::Tumor, Some(100.0)),
        ];
        let changed = vec![
            specimen("Demo2", Tissue::Comparator, None),
            specimen("Demo2", Tissue::Tumor, Some(100_000.0)),
        ];
        validate_person_split(&train, &original).unwrap();
        let prepared = MedianPreparation::fit(&train).unwrap();
        assert!((prepared.median() - 15.0).abs() < 1e-12);
        assert_eq!(prepared.transform(&original).unwrap()[0], 15.0);
        assert_eq!(prepared.transform(&changed).unwrap()[0], 15.0);
        assert_eq!(
            prepared.median(),
            MedianPreparation::fit(&train).unwrap().median()
        );
    }

    #[test]
    fn missing_training_values_and_duplicate_pairs_fail() {
        let missing = vec![
            specimen("Demo1", Tissue::Comparator, None),
            specimen("Demo1", Tissue::Tumor, None),
        ];
        assert!(MedianPreparation::fit(&missing).is_err());
        let duplicate = vec![
            specimen("Demo1", Tissue::Comparator, Some(1.0)),
            specimen("Demo1", Tissue::Comparator, Some(2.0)),
        ];
        assert!(validate_person_split(&duplicate, &missing).is_err());
    }
}
