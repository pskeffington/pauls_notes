//! Values, functions, conditions, slices and simple calculations.
//! This is Chapter 11 arithmetic on invented comparable units, NOT RNA-seq analysis.

/// Returns log2(tumor/comparator), with explicit scientific input preconditions.
/// Log subtraction avoids overflow when the intermediate ratio would overflow.
pub fn log2_change(tumor: f64, comparator: f64) -> Result<f64, &'static str> {
    if !tumor.is_finite() || !comparator.is_finite() || tumor <= 0.0 || comparator <= 0.0 {
        return Err("Both fictional measurements must be positive and finite");
    }
    let result = tumor.log2() - comparator.log2();
    if !result.is_finite() {
        return Err("Nonfinite log2 change");
    }
    Ok(result)
}

/// An interpretation of *invented arithmetic*, not a clinical finding.
pub fn direction(change: f64) -> Result<&'static str, &'static str> {
    if !change.is_finite() {
        return Err("Invalid change");
    }
    Ok(if change > 0.0 {
        "higher in invented tumor measurement"
    } else if change < 0.0 {
        "lower in invented tumor measurement"
    } else {
        "unchanged in invented measurements"
    })
}

/// Read a slice without taking ownership of the caller's vector.
pub fn positive_count(changes: &[f64]) -> Result<usize, &'static str> {
    if changes.iter().any(|v| !v.is_finite()) {
        return Err("Nonfinite contrast");
    }
    Ok(changes.iter().filter(|&&v| v > 0.0).count())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn chapter_11_ratios_and_direction() {
        assert!((log2_change(20.0, 10.0).unwrap() - 1.0).abs() < 1e-12);
        assert!((log2_change(5.0, 10.0).unwrap() + 1.0).abs() < 1e-12);
        assert_eq!(direction(0.0).unwrap(), "unchanged in invented measurements");
        assert_eq!(positive_count(&[1.0, 2.0, 0.0, -1.0, 1.0, 0.0]).unwrap(), 3);
    }

    #[test]
    fn nonfinite_and_zero_values_fail_closed() {
        assert!(log2_change(0.0, 10.0).is_err());
        assert!(log2_change(f64::NAN, 10.0).is_err());
        assert!(log2_change(10.0, f64::INFINITY).is_err());
        assert!(direction(f64::NAN).is_err());
        assert!(positive_count(&[f64::INFINITY]).is_err());
    }
}
