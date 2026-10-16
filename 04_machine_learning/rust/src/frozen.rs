//! Portable, read-only inference for a previously fitted native Rust model.
//! The model contains no training rows, labels, or optimizer state.
use crate::Result;
use serde::{Deserialize, Serialize};
use std::collections::HashSet;

#[derive(Clone, Debug, Serialize, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct FrozenModel {
    pub schema_version: u32,
    pub task: String,
    pub protocol_id: String,
    pub plan_name: String,
    pub positive_class: u8,
    pub feature_names: Vec<String>,
    pub medians: Vec<f64>,
    pub means: Vec<f64>,
    pub scales: Vec<f64>,
    pub coefficients_class_1: Vec<f64>,
    pub intercept_class_1: f64,
}

impl FrozenModel {
    pub fn from_json(bytes: &[u8]) -> Result<Self> {
        let model: Self = serde_json::from_slice(bytes)?;
        model.validate()?;
        Ok(model)
    }

    pub fn validate(&self) -> Result<()> {
        let n = self.feature_names.len();
        if self.schema_version != 1
            || self.task != "synthetic_paired_specimen_category"
            || self.protocol_id != "paired-assay-native-rust-v1"
            || self.plan_name != "final_development"
            || self.positive_class != 1
            || n == 0
            || [
                self.medians.len(),
                self.means.len(),
                self.scales.len(),
                self.coefficients_class_1.len(),
            ]
            .iter()
            .any(|&len| len != n)
            || self
                .feature_names
                .iter()
                .any(|s| s.is_empty() || s.trim() != s || s.chars().any(char::is_control))
            || self.feature_names.iter().collect::<HashSet<_>>().len() != n
            || !self.intercept_class_1.is_finite()
            || self
                .medians
                .iter()
                .chain(&self.means)
                .chain(&self.scales)
                .chain(&self.coefficients_class_1)
                .any(|v| !v.is_finite())
            || self.scales.iter().any(|&v| v <= 0.0)
        {
            return Err("Invalid native frozen model contract".into());
        }
        Ok(())
    }

    pub fn predict(&self, values: &[Option<f64>]) -> Result<f64> {
        self.validate()?;
        if values.len() != self.feature_names.len()
            || values.iter().flatten().any(|v| !v.is_finite())
        {
            return Err("Invalid feature count or nonfinite measurement".into());
        }
        let mut logit = self.intercept_class_1;
        for (j, value) in values.iter().enumerate() {
            let imputed = value.unwrap_or(self.medians[j]);
            let standardized = (imputed - self.means[j]) / self.scales[j];
            if !standardized.is_finite() {
                return Err("Preprocessing overflow".into());
            }
            logit += standardized * self.coefficients_class_1[j];
        }
        if !logit.is_finite() {
            return Err("Prediction overflow".into());
        }
        Ok(if logit >= 0.0 {
            1.0 / (1.0 + (-logit).exp())
        } else {
            let exp = logit.exp();
            exp / (1.0 + exp)
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    fn example() -> FrozenModel {
        FrozenModel {
            schema_version: 1,
            task: "synthetic_paired_specimen_category".into(),
            protocol_id: "paired-assay-native-rust-v1".into(),
            plan_name: "final_development".into(),
            positive_class: 1,
            feature_names: vec!["Feature001".into(), "Feature002".into()],
            medians: vec![3.0, 4.0],
            means: vec![1.0, 2.0],
            scales: vec![2.0, 2.0],
            coefficients_class_1: vec![1.0, 2.0],
            intercept_class_1: -1.0,
        }
    }
    #[test]
    fn known_logit_and_missingness() {
        let m = example();
        let expected = 1.0 / (1.0 + (-1.0_f64).exp());
        assert!((m.predict(&[None, Some(3.0)]).unwrap() - expected).abs() < 1e-15);
        assert_eq!(
            m.predict(&[None, None]).unwrap(),
            m.predict(&[Some(3.0), Some(4.0)]).unwrap()
        );
    }
    #[test]
    fn rejects_invalid_contract_and_inputs() {
        let mut m = example();
        m.scales[0] = 0.0;
        assert!(m.validate().is_err());
        let mut m = example();
        m.positive_class = 0;
        assert!(m.validate().is_err());
        let mut m = example();
        m.feature_names[1] = "Feature001".into();
        assert!(m.validate().is_err());
        let m = example();
        assert!(m.predict(&[Some(f64::NAN), None]).is_err());
        assert!(m.predict(&[None]).is_err());
        let mut v = serde_json::to_value(m).unwrap();
        v["other"] = serde_json::json!(true);
        assert!(FrozenModel::from_json(&serde_json::to_vec(&v).unwrap()).is_err());
    }
    #[test]
    fn saturated_probabilities_remain_finite() {
        let m = example();
        assert_eq!(m.predict(&[Some(2000.0), None]).unwrap(), 1.0);
        assert_eq!(m.predict(&[Some(-2000.0), None]).unwrap(), 0.0);
    }
}
