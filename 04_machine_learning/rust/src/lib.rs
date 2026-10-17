//! Frozen binary logistic inference with training-only preprocessing parameters.
#![forbid(unsafe_code)]

use serde::{Deserialize, Serialize};
use std::collections::HashSet;
use std::io::Read;

pub type Result<T> = std::result::Result<T, Box<dyn std::error::Error>>;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Model {
    pub schema_version: u32,
    pub task: String,
    pub protocol_id: String,
    pub training_partition: String,
    pub model_name: String,
    pub positive_class: u8,
    pub feature_names: Vec<String>,
    pub selected_indices: Vec<usize>,
    pub imputation_medians: Vec<f64>,
    pub scaler_means: Vec<f64>,
    pub scaler_scales: Vec<f64>,
    pub coefficients: Vec<f64>,
    pub intercept: f64,
}

impl Model {
    pub fn from_json(bytes: &[u8]) -> Result<Self> {
        let model: Self = serde_json::from_slice(bytes)?;
        model.validate()?;
        Ok(model)
    }

    pub fn validate(&self) -> Result<()> {
        let n = self.feature_names.len();
        let k = self.selected_indices.len();
        if self.schema_version != 1
            || self.task != "synthetic_paired_specimen_category"
            || self.protocol_id != "paired-comparison-v1"
            || self.training_partition != "development"
            || !["selected", "all_features"].contains(&self.model_name.as_str())
            || self.positive_class != 1
        {
            return Err("Unsupported task, model, training partition or schema".into());
        }
        if n == 0
            || k == 0
            || self.imputation_medians.len() != n
            || self.scaler_means.len() != k
            || self.scaler_scales.len() != k
            || self.coefficients.len() != k
            || self
                .feature_names
                .iter()
                .enumerate()
                .any(|(i, name)| *name != format!("Feature{:03}", i + 1))
            || self.selected_indices.iter().any(|i| *i >= n)
            || self
                .selected_indices
                .windows(2)
                .any(|pair| pair[0] >= pair[1])
            || (self.model_name == "all_features"
                && self.selected_indices != (0..n).collect::<Vec<_>>())
        {
            return Err("Invalid feature names, dimensions or selected-column order".into());
        }
        if !self.intercept.is_finite()
            || self
                .imputation_medians
                .iter()
                .chain(&self.scaler_means)
                .chain(&self.scaler_scales)
                .chain(&self.coefficients)
                .any(|v| !v.is_finite())
            || self.scaler_scales.iter().any(|v| *v <= 0.)
        {
            return Err("Model parameters must be finite and scales strictly positive".into());
        }
        Ok(())
    }

    pub fn predict(&self, values: &[Option<f64>]) -> Result<f64> {
        self.validate()?;
        if values.len() != self.feature_names.len()
            || values.iter().flatten().any(|v| !v.is_finite())
        {
            return Err("Invalid assay width or nonfinite measurement".into());
        }
        let mut logit = self.intercept;
        for (position, column) in self.selected_indices.iter().enumerate() {
            let x = values[*column].unwrap_or(self.imputation_medians[*column]);
            let standardized = (x - self.scaler_means[position]) / self.scaler_scales[position];
            logit += standardized * self.coefficients[position];
        }
        if !logit.is_finite() {
            return Err("Arithmetic overflow during prediction".into());
        }
        // Separate branches avoid exp(-logit) overflowing for large negative logits.
        Ok(if logit >= 0. {
            1. / (1. + (-logit).exp())
        } else {
            let e = logit.exp();
            e / (1. + e)
        })
    }
}

#[derive(Debug)]
pub struct Prediction {
    pub specimen_id: String,
    pub probability: f64,
}

pub fn predict_csv(reader: impl Read, model: &Model) -> Result<Vec<Prediction>> {
    model.validate()?;
    let mut csv = csv::ReaderBuilder::new()
        .flexible(false)
        .from_reader(reader);
    let expected: Vec<&str> = std::iter::once("specimen_id")
        .chain(model.feature_names.iter().map(String::as_str))
        .collect();
    if csv.headers()?.iter().collect::<Vec<_>>() != expected {
        return Err(
            "CSV header must be specimen_id followed by the exact model feature order".into(),
        );
    }
    let mut ids = HashSet::new();
    let mut predictions = Vec::new();
    for record in csv.records() {
        let record = record?;
        let id = &record[0];
        if id.is_empty()
            || id.trim() != id
            || id.contains(['\n', '\r'])
            || !ids.insert(id.to_string())
        {
            return Err("Blank, padded, multiline or duplicate specimen identity".into());
        }
        let values: Vec<Option<f64>> = record
            .iter()
            .skip(1)
            .map(|raw| {
                let raw = raw.trim();
                if raw.is_empty() || raw == "NA" {
                    Ok(None)
                } else {
                    raw.parse::<f64>().map(Some)
                }
            })
            .collect::<std::result::Result<_, _>>()?;
        predictions.push(Prediction {
            specimen_id: id.to_string(),
            probability: model.predict(&values)?,
        });
    }
    if predictions.is_empty() {
        return Err("No specimens supplied".into());
    }
    Ok(predictions)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn model() -> Model {
        Model {
            schema_version: 1,
            task: "synthetic_paired_specimen_category".into(),
            protocol_id: "paired-comparison-v1".into(),
            training_partition: "development".into(),
            model_name: "selected".into(),
            positive_class: 1,
            feature_names: vec!["Feature001".into(), "Feature002".into()],
            selected_indices: vec![1],
            imputation_medians: vec![10., 4.],
            scaler_means: vec![2.],
            scaler_scales: vec![2.],
            coefficients: vec![3.],
            intercept: -1.,
        }
    }

    #[test]
    fn known_logit_checks_imputation_selection_scaling_and_direction() {
        let m = model();
        // Missing selected feature: ((4 - 2) / 2) * 3 - 1 = 2.
        let p = m.predict(&[Some(-999.), None]).unwrap();
        assert!((p - 0.880_797_077_977_882_3).abs() < 1e-15);
        assert_eq!(p, m.predict(&[Some(999.), Some(4.)]).unwrap());
        assert_eq!(
            m.predict(&[None, Some(2.)]).unwrap(),
            1. / (1. + 1_f64.exp())
        );
    }

    #[test]
    fn sigmoid_is_stable_and_invalid_arithmetic_is_rejected() {
        let mut m = model();
        m.coefficients[0] = 1.;
        m.scaler_means[0] = 0.;
        m.scaler_scales[0] = 1.;
        m.intercept = 0.;
        assert_eq!(m.predict(&[None, Some(1000.)]).unwrap(), 1.);
        assert_eq!(m.predict(&[None, Some(-1000.)]).unwrap(), 0.);
        m.coefficients[0] = 10.;
        assert!(m.predict(&[None, Some(f64::MAX)]).is_err());
        assert!(m.predict(&[Some(f64::NAN), Some(1.)]).is_err());
        assert!(m.predict(&[None]).is_err());
    }

    #[test]
    fn rejects_bad_schema_duplicate_indices_and_nonpositive_scales() {
        let mut m = model();
        m.schema_version = 2;
        assert!(m.validate().is_err());
        let mut m = model();
        m.selected_indices = vec![1, 1];
        assert!(m.validate().is_err());
        let mut m = model();
        m.selected_indices = vec![2];
        assert!(m.validate().is_err());
        let mut m = model();
        m.scaler_scales[0] = 0.;
        assert!(m.validate().is_err());
        let mut m = model();
        m.feature_names[1] = "Feature001".into();
        assert!(m.validate().is_err());
        let mut m = model();
        m.coefficients[0] = f64::INFINITY;
        assert!(m.validate().is_err());
        let mut m = model();
        m.positive_class = 0;
        assert!(m.validate().is_err());
        let mut m = model();
        m.model_name = "all_features".into();
        assert!(m.validate().is_err());
    }

    #[test]
    fn rejects_unknown_json_fields_and_wrong_parameter_types() {
        let mut value = serde_json::to_value(model()).unwrap();
        value["extra"] = serde_json::json!(true);
        assert!(Model::from_json(&serde_json::to_vec(&value).unwrap()).is_err());
        value.as_object_mut().unwrap().remove("extra");
        value["scaler_means"] = serde_json::json!([null]);
        assert!(Model::from_json(&serde_json::to_vec(&value).unwrap()).is_err());
    }

    #[test]
    fn csv_supports_quoted_ids_missing_cells_and_multiple_rows() {
        let input = "specimen_id,Feature001,Feature002\n\"Specimen,1\",NA,4\nSpecimen2,0,\n";
        let p = predict_csv(input.as_bytes(), &model()).unwrap();
        assert_eq!(p.len(), 2);
        assert_eq!(p[0].specimen_id, "Specimen,1");
        assert_eq!(p[0].probability, p[1].probability);
    }

    #[test]
    fn csv_rejects_wrong_headers_duplicates_nonfinite_and_ragged_records() {
        for input in [
            "specimen_id,Feature002,Feature001\nS,1,2\n",
            "specimen_id,Feature001,Feature002\nS,1,2\nS,3,4\n",
            "specimen_id,Feature001,Feature002\nS,1,inf\n",
            "specimen_id,Feature001,Feature002\nS,NaN,1\n",
            "specimen_id,Feature001,Feature002\nS,1\n",
            "specimen_id,Feature001,Feature002\n,1,2\n",
            "specimen_id,Feature001,Feature002\n",
        ] {
            assert!(predict_csv(input.as_bytes(), &model()).is_err(), "{input}");
        }
    }
}

#[cfg(feature = "native-training")]
pub mod training;

/// Strict read-only replay of previously fitted native Rust models.
pub mod frozen;
