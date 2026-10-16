//! Fixed all-feature fitting. See the separately frozen native-training protocol.
use crate::Result;
use linfa::prelude::*;
use linfa_logistic::LogisticRegression;
use ndarray::{Array1, Array2};
use serde::{Deserialize, Serialize};
use std::collections::HashSet;

#[derive(Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Row {
    pub cohort_row: usize,
    pub person_id: u64,
    pub specimen_id: String,
    pub label: u8,
    pub values: Vec<Option<f64>>,
}

#[derive(Clone, Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
pub struct Plan {
    pub name: String,
    pub train: Vec<usize>,
    pub assessment: Vec<usize>,
}

#[derive(Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct Input {
    pub protocol_id: String,
    pub feature_names: Vec<String>,
    pub rows: Vec<Row>,
    pub plans: Vec<Plan>,
}

fn distinct<T: std::hash::Hash + Eq>(items: impl Iterator<Item = T>, n: usize) -> bool {
    items.collect::<HashSet<_>>().len() == n
}
fn valid_name(s: &str) -> bool {
    !s.is_empty() && s.trim() == s && !s.chars().any(char::is_control)
}
impl Input {
    pub fn validate(&self) -> Result<()> {
        let n = self.rows.len();
        let p = self.feature_names.len();
        if self.protocol_id != "paired-assay-native-rust-v1"
            || p == 0
            || n < 4
            || self.plans.is_empty()
            || self.feature_names.iter().any(|s| !valid_name(s))
            || !distinct(self.feature_names.iter(), p)
            || !distinct(self.rows.iter().map(|r| &r.specimen_id), n)
            || !distinct(self.rows.iter().map(|r| r.cohort_row), n)
            || !distinct(self.plans.iter().map(|p| &p.name), self.plans.len())
        {
            return Err("Invalid native training schema or duplicate identity".into());
        }
        let people: HashSet<_> = self.rows.iter().map(|r| r.person_id).collect();
        for r in &self.rows {
            if !valid_name(&r.specimen_id)
                || r.label > 1
                || r.values.len() != p
                || r.values.iter().flatten().any(|v| !v.is_finite())
            {
                return Err("Invalid specimen, label or measurement".into());
            }
        }
        for person in people {
            let labels: Vec<_> = self
                .rows
                .iter()
                .filter(|r| r.person_id == person)
                .map(|r| r.label)
                .collect();
            if labels.len() != 2 || !labels.contains(&0) || !labels.contains(&1) {
                return Err("Each person requires exactly one specimen of each class".into());
            }
        }
        for plan in &self.plans {
            if !valid_name(&plan.name)
                || plan.train.is_empty()
                || (plan.assessment.is_empty() && plan.name != "final_development")
                || (plan.name == "final_development" && !plan.assessment.is_empty())
            {
                return Err("Invalid plan name or empty partition".into());
            }
            let indices: Vec<_> = plan.train.iter().chain(&plan.assessment).copied().collect();
            if indices.len() != n
                || indices.iter().any(|&i| i >= n)
                || !distinct(indices.into_iter(), n)
            {
                return Err("Plan must partition the development input exactly".into());
            }
            let train_people: HashSet<_> =
                plan.train.iter().map(|&i| self.rows[i].person_id).collect();
            if plan
                .assessment
                .iter()
                .any(|&i| train_people.contains(&self.rows[i].person_id))
            {
                return Err("Person overlap across training and assessment".into());
            }
        }
        Ok(())
    }
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct Preparation {
    pub medians: Vec<f64>,
    pub means: Vec<f64>,
    pub scales: Vec<f64>,
}
impl Preparation {
    pub fn fit(input: &Input, rows: &[usize]) -> Result<Self> {
        let mut result = Self {
            medians: vec![],
            means: vec![],
            scales: vec![],
        };
        for j in 0..input.feature_names.len() {
            let mut finite: Vec<f64> = rows
                .iter()
                .filter_map(|&i| input.rows[i].values[j])
                .collect();
            if finite.is_empty() {
                return Err("All-missing training column".into());
            }
            finite.sort_by(f64::total_cmp);
            let mid = finite.len() / 2;
            let median = if finite.len().is_multiple_of(2) {
                finite[mid - 1] / 2.0 + finite[mid] / 2.0
            } else {
                finite[mid]
            };
            let values: Vec<_> = rows
                .iter()
                .map(|&i| input.rows[i].values[j].unwrap_or(median))
                .collect();
            let mean = values.iter().sum::<f64>() / values.len() as f64;
            let variance =
                values.iter().map(|v| (v - mean).powi(2)).sum::<f64>() / values.len() as f64;
            let scale = if variance == 0.0 {
                1.0
            } else {
                variance.sqrt()
            };
            if !median.is_finite() || !mean.is_finite() || !scale.is_finite() || scale <= 0.0 {
                return Err("Preprocessing overflow".into());
            }
            result.medians.push(median);
            result.means.push(mean);
            result.scales.push(scale);
        }
        Ok(result)
    }
    pub fn transform(&self, input: &Input, rows: &[usize]) -> Result<Array2<f64>> {
        let p = input.feature_names.len();
        let mut x = Array2::zeros((rows.len(), p));
        for (k, &i) in rows.iter().enumerate() {
            for j in 0..p {
                x[[k, j]] = (input.rows[i].values[j].unwrap_or(self.medians[j]) - self.means[j])
                    / self.scales[j];
                if !x[[k, j]].is_finite() {
                    return Err("Transformed measurement overflow".into());
                }
            }
        }
        Ok(x)
    }
}

pub fn sigmoid(z: f64) -> f64 {
    if z >= 0.0 {
        1.0 / (1.0 + (-z).exp())
    } else {
        z.exp() / (1.0 + z.exp())
    }
}
fn softplus(z: f64) -> f64 {
    z.max(0.0) + (-z.abs()).exp().ln_1p()
}

/// Separate objective/gradient calculation in canonical category-1 coordinates.
pub fn objective_gradient(
    x: &Array2<f64>,
    y: &Array1<u8>,
    w: &[f64],
    b: f64,
) -> Result<(f64, Vec<f64>)> {
    if x.nrows() != y.len() || x.ncols() != w.len() || y.iter().any(|&y| y > 1) {
        return Err("Objective shape/label mismatch".into());
    }
    let mut loss = w.iter().map(|w| 0.5 * w * w).sum::<f64>();
    let mut gradient = w.to_vec();
    gradient.push(0.0);
    for (row, &target) in x.rows().into_iter().zip(y) {
        let z = row.iter().zip(w).map(|(v, w)| v * w).sum::<f64>() + b;
        if !z.is_finite() {
            return Err("Logit overflow".into());
        }
        loss += softplus(if target == 1 { -z } else { z });
        let residual = sigmoid(z) - f64::from(target);
        for j in 0..w.len() {
            gradient[j] += row[j] * residual;
        }
        gradient[w.len()] += residual;
    }
    if !loss.is_finite() || gradient.iter().any(|v| !v.is_finite()) {
        return Err("Objective overflow".into());
    }
    Ok((loss, gradient))
}

#[derive(Clone, Copy)]
pub struct Settings {
    pub max_iterations: u64,
    pub gradient_tolerance: f64,
}
impl Default for Settings {
    fn default() -> Self {
        Self {
            max_iterations: 5000,
            gradient_tolerance: 1e-8,
        }
    }
}

#[derive(Serialize, Deserialize)]
pub struct Fitted {
    pub plan: Plan,
    pub preparation: Preparation,
    pub coefficients_class_1: Vec<f64>,
    pub intercept_class_1: f64,
    pub linfa_positive_class: u8,
    pub training_objective: f64,
    pub training_gradient: Vec<f64>,
    pub gradient_inf: f64,
    pub prevalence: f64,
    pub prediction_rows: Vec<usize>,
    pub probabilities_class_1: Vec<f64>,
    pub max_library_probability_difference: f64,
    pub elapsed_seconds: f64,
    pub library_termination_reason: Option<String>,
    pub library_iterations: Option<u64>,
}

pub fn fit(input: &Input, plan_index: usize, settings: Settings) -> Result<Fitted> {
    input.validate()?;
    let plan = input.plans.get(plan_index).ok_or("Unknown plan")?;
    if settings.max_iterations == 0
        || !settings.gradient_tolerance.is_finite()
        || settings.gradient_tolerance <= 0.0
    {
        return Err("Invalid or exhausted optimizer budget".into());
    }
    let start = std::time::Instant::now();
    let preparation = Preparation::fit(input, &plan.train)?;
    let x = preparation.transform(input, &plan.train)?;
    let y = Array1::from_iter(plan.train.iter().map(|&i| input.rows[i].label));
    let dataset = Dataset::new(x.clone(), y.clone());
    let model = LogisticRegression::<f64>::default()
        .alpha(1.0)
        .with_intercept(true)
        .max_iterations(settings.max_iterations)
        .gradient_tolerance(settings.gradient_tolerance)
        .initial_params(Array1::zeros(x.ncols() + 1))
        .fit(&dataset)?;
    let (w, b, positive) = canonical_parameters(&model)?;
    let (objective, gradient) = objective_gradient(&x, &y, &w, b)?;
    let gradient_inf = gradient.iter().map(|v| v.abs()).fold(0.0, f64::max);
    if gradient_inf > 1e-6 {
        return Err(format!("Optimization residual failed: {gradient_inf:e}").into());
    }
    let prediction_rows = if plan.assessment.is_empty() {
        plan.train.clone()
    } else {
        plan.assessment.clone()
    };
    let predicted_x = preparation.transform(input, &prediction_rows)?;
    let library = model.predict_probabilities(&predicted_x);
    let mut probabilities = Vec::new();
    let mut max_difference: f64 = 0.0;
    for (row, &lib_p) in predicted_x.rows().into_iter().zip(&library) {
        let z = row.iter().zip(&w).map(|(v, w)| v * w).sum::<f64>() + b;
        if !z.is_finite() {
            return Err("Prediction overflow".into());
        }
        let p = sigmoid(z);
        let lib_p = if positive == 1 { lib_p } else { 1.0 - lib_p };
        if !lib_p.is_finite() || !(0.0..=1.0).contains(&lib_p) {
            return Err("Invalid library probability".into());
        }
        max_difference = max_difference.max((p - lib_p).abs());
        probabilities.push(p);
    }
    if max_difference > 1e-12 {
        return Err("Linfa probability mapping mismatch".into());
    }
    Ok(Fitted {
        plan: plan.clone(),
        preparation,
        coefficients_class_1: w,
        intercept_class_1: b,
        linfa_positive_class: positive,
        training_objective: objective,
        training_gradient: gradient,
        gradient_inf,
        prevalence: y.iter().map(|&v| f64::from(v)).sum::<f64>() / y.len() as f64,
        prediction_rows,
        probabilities_class_1: probabilities,
        max_library_probability_difference: max_difference,
        elapsed_seconds: start.elapsed().as_secs_f64(),
        library_termination_reason: None,
        library_iterations: None,
    })
}

fn canonical_parameters(
    model: &linfa_logistic::FittedLogisticRegression<f64, u8>,
) -> Result<(Vec<f64>, f64, u8)> {
    let positive = model.labels().pos.class;
    if ![0, 1].contains(&positive) || model.labels().neg.class == positive {
        return Err("Unexpected Linfa class mapping".into());
    }
    let sign = if positive == 1 { 1.0 } else { -1.0 };
    let w: Vec<_> = model.params().iter().map(|w| w * sign).collect();
    let b = model.intercept() * sign;
    Ok((w, b, positive))
}

#[cfg(test)]
mod tests {
    use super::*;
    use ndarray::array;
    fn fixture() -> Input {
        Input {
            protocol_id: "paired-assay-native-rust-v1".into(),
            feature_names: vec!["a".into(), "constant".into()],
            rows: (0..8)
                .map(|i| Row {
                    cohort_row: i,
                    person_id: (i / 2) as u64,
                    specimen_id: format!("s{i}"),
                    label: (i % 2) as u8,
                    values: vec![Some(if i % 2 == 0 { -1.0 } else { 1.0 }), Some(2.0)],
                })
                .collect(),
            plans: vec![Plan {
                name: "outer_0".into(),
                train: vec![0, 1, 2, 3],
                assessment: vec![4, 5, 6, 7],
            }],
        }
    }
    #[test]
    fn known_loss_gradient_and_extremes() {
        let (loss, g) =
            objective_gradient(&array![[-1.0], [1.0]], &array![0, 1], &[0.0], 0.0).unwrap();
        assert!((loss - 2.0 * 2.0_f64.ln()).abs() < 1e-14);
        assert_eq!(g, vec![-1.0, 0.0]);
        for z in [-1000.0, 1000.0] {
            assert!(sigmoid(z).is_finite());
            assert!(softplus(z).is_finite());
        }
        assert_eq!(sigmoid(-1000.0), 0.0);
        assert_eq!(sigmoid(1000.0), 1.0);
        assert!(objective_gradient(&array![[f64::MAX]], &array![1], &[2.0], 0.0).is_err());
    }
    #[test]
    fn finite_difference_gradient() {
        let x = array![[-2.0, 1.0], [0.0, 1.0], [1.0, 3.0]];
        let y = array![0, 1, 1];
        let theta = [0.2, -0.4, 0.3];
        let (_, g) = objective_gradient(&x, &y, &theta[..2], theta[2]).unwrap();
        for j in 0..3 {
            let mut a = theta;
            let mut b = theta;
            a[j] += 1e-5;
            b[j] -= 1e-5;
            let la = objective_gradient(&x, &y, &a[..2], a[2]).unwrap().0;
            let lb = objective_gradient(&x, &y, &b[..2], b[2]).unwrap().0;
            assert!(((la - lb) / 2e-5 - g[j]).abs() < 1e-8);
        }
    }
    #[test]
    fn training_medians_population_scales() {
        let mut data = fixture();
        data.rows[0].values[0] = None;
        let p = Preparation::fit(&data, &data.plans[0].train).unwrap();
        assert_eq!(p.medians, vec![1.0, 2.0]);
        assert_eq!(p.means, vec![0.5, 2.0]);
        assert!((p.scales[0] - 0.75_f64.sqrt()).abs() < 1e-14);
        assert_eq!(p.scales[1], 1.0);
    }
    #[test]
    fn assessment_mutation_cannot_change_training() {
        let mut data = fixture();
        let a = fit(&data, 0, Settings::default()).unwrap();
        for i in [4, 5, 6, 7] {
            data.rows[i].values = vec![Some(100.0), None];
        }
        let b = fit(&data, 0, Settings::default()).unwrap();
        assert_eq!(a.coefficients_class_1, b.coefficients_class_1);
        assert_eq!(a.preparation.means, b.preparation.means);
    }
    #[test]
    fn class_mapping_count_and_encounter_order() {
        for (x, y) in [
            (array![[-1.0], [1.0], [-2.0], [2.0]], array![0u8, 1, 0, 1]),
            (array![[1.0], [-1.0], [2.0], [-2.0]], array![1, 0, 1, 0]),
            (
                array![[-1.0], [1.0], [-2.0], [2.0], [3.0]],
                array![0, 1, 0, 1, 1],
            ),
        ] {
            let model = LogisticRegression::<f64>::default()
                .alpha(1.0)
                .gradient_tolerance(1e-8)
                .max_iterations(5000)
                .fit(&Dataset::new(x.clone(), y.clone()))
                .unwrap();
            let (w, b, _) = canonical_parameters(&model).unwrap();
            assert!(w[0] > 0.0);
            let (_, g) = objective_gradient(&x, &y, &w, b).unwrap();
            assert!(g.iter().all(|v| v.abs() < 1e-6));
        }
    }
    #[test]
    fn constant_design_has_known_intercept_and_zero_weights() {
        let mut data = fixture();
        for row in &mut data.rows {
            row.values = vec![Some(2.0), Some(2.0)];
        }
        let model = fit(&data, 0, Settings::default()).unwrap();
        assert!(model.coefficients_class_1.iter().all(|v| v.abs() < 1e-12));
        assert!(model.intercept_class_1.abs() < 1e-12);
        assert!(model.probabilities_class_1.iter().all(|&p| p == 0.5));
    }
    #[test]
    fn regularized_separation_and_collinearity_converge() {
        let mut data = fixture();
        for row in &mut data.rows {
            row.values[1] = row.values[0];
        }
        let m = fit(&data, 0, Settings::default()).unwrap();
        assert!(m.gradient_inf < 1e-6);
        assert!((m.coefficients_class_1[0] - m.coefficients_class_1[1]).abs() < 1e-12);
        assert!(m.probabilities_class_1.iter().all(|&p| p > 0.0 && p < 1.0));
    }
    #[test]
    fn malformed_identity_labels_and_partitions_fail() {
        let mut d = fixture();
        d.rows[0].specimen_id = d.rows[1].specimen_id.clone();
        assert!(d.validate().is_err());
        let mut d = fixture();
        d.rows[0].label = 2;
        assert!(d.validate().is_err());
        let mut d = fixture();
        d.plans[0].train = vec![0, 2, 3, 4];
        d.plans[0].assessment = vec![1, 5, 6, 7];
        assert!(d.validate().is_err());
        let mut d = fixture();
        d.plans[0].train[0] = 1;
        assert!(d.validate().is_err());
        let mut d = fixture();
        d.rows[0].values[0] = Some(f64::INFINITY);
        assert!(d.validate().is_err());
    }
    #[test]
    fn missing_overflow_and_budget_fail_explicitly() {
        let mut d = fixture();
        for i in [0, 1, 2, 3] {
            d.rows[i].values[0] = None;
        }
        assert!(fit(&d, 0, Settings::default()).is_err());
        let mut d = fixture();
        for i in [0, 1, 2, 3] {
            d.rows[i].values[0] = Some(f64::MAX);
        }
        assert!(fit(&d, 0, Settings::default()).is_err());
        assert!(fit(
            &fixture(),
            0,
            Settings {
                max_iterations: 0,
                ..Settings::default()
            }
        )
        .is_err());
        assert!(fit(
            &fixture(),
            0,
            Settings {
                max_iterations: 1,
                ..Settings::default()
            }
        )
        .is_err());
    }
}
