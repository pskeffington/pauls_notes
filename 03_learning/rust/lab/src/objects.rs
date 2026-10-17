//! Rust's object-oriented idioms: private data, constructors, methods, traits,
//! enum categories, composition, and generic / dynamic polymorphism.

#[derive(Clone, Copy, Debug, Eq, PartialEq, Ord, PartialOrd)]
pub enum Tissue {
    Comparator,
    Tumor,
}

/// The IDs in this teaching crate are fictional and must never be replaced by real TCGA IDs.
#[derive(Clone, Debug)]
pub struct Specimen {
    person_id: String,
    tissue: Tissue,
    measurement: Option<f64>,
}

impl Specimen {
    pub fn new(
        person_id: impl Into<String>,
        tissue: Tissue,
        measurement: Option<f64>,
    ) -> Result<Self, &'static str> {
        let person_id = person_id.into();
        if person_id.is_empty()
            || person_id.trim() != person_id
            || person_id.chars().any(char::is_control)
        {
            return Err("Invalid fictional person identifier");
        }
        if measurement.is_some_and(|v| !v.is_finite() || v <= 0.0) {
            return Err("Invalid fictional measurement");
        }
        Ok(Self {
            person_id,
            tissue,
            measurement,
        })
    }

    pub fn person_id(&self) -> &str {
        &self.person_id
    }

    pub fn tissue(&self) -> Tissue {
        self.tissue
    }

    pub fn measurement(&self) -> Option<f64> {
        self.measurement
    }
}

/// Model a single complete pair by composition rather than class inheritance.
#[derive(Debug)]
pub struct Pair {
    comparator: Specimen,
    tumor: Specimen,
}

impl Pair {
    pub fn new(comparator: Specimen, tumor: Specimen) -> Result<Self, &'static str> {
        if comparator.tissue != Tissue::Comparator || tumor.tissue != Tissue::Tumor {
            return Err("Pair requires comparator then tumor");
        }
        if comparator.person_id != tumor.person_id {
            return Err("Two specimens must belong to the same fictional person");
        }
        Ok(Self { comparator, tumor })
    }

    pub fn log2_change(&self) -> Result<Option<f64>, &'static str> {
        match (self.tumor.measurement, self.comparator.measurement) {
            (Some(tumor), Some(comparator)) => {
                super::foundations::log2_change(tumor, comparator).map(Some)
            }
            _ => Ok(None),
        }
    }
}

/// A trait is shared *behavior*, not a base class.
pub trait Describe {
    fn summary(&self) -> String;
}

impl Describe for Specimen {
    fn summary(&self) -> String {
        // Deliberately avoid printing a person identifier or measurement.
        format!("synthetic {:?} specimen; research teaching only", self.tissue)
    }
}

/// Biological teaching annotation, NEVER a fitted feature or a measured expression row.
#[derive(Debug)]
pub struct GeneAnnotation {
    symbol: String,
    domain: String,
}

impl GeneAnnotation {
    pub fn new(symbol: &str, domain: &str) -> Result<Self, &'static str> {
        if symbol.is_empty()
            || !symbol.chars().all(|c| c.is_ascii_uppercase() || c.is_ascii_digit())
            || domain.trim().is_empty()
            || domain.trim() != domain
        {
            return Err("Invalid teaching annotation");
        }
        Ok(Self {
            symbol: symbol.to_owned(),
            domain: domain.to_owned(),
        })
    }
}

impl Describe for GeneAnnotation {
    fn summary(&self) -> String {
        format!("{}: {} (biological reference; not a trained feature)", self.symbol, self.domain)
    }
}

/// Generic (compile-time) dispatch.
pub fn describe_one<T: Describe>(item: &T) -> String {
    item.summary()
}

/// Trait object (runtime) dispatch across unlike concrete types.
pub fn describe_many(items: &[&dyn Describe]) -> Vec<String> {
    items.iter().map(|item| item.summary()).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn same_person_pair_and_missingness() {
        let a = Specimen::new("Demo1", Tissue::Comparator, Some(10.0)).unwrap();
        let b = Specimen::new("Demo1", Tissue::Tumor, Some(20.0)).unwrap();
        let pair = Pair::new(a, b).unwrap();
        assert!((pair.log2_change().unwrap().unwrap() - 1.0).abs() < 1e-12);
        let a = Specimen::new("Demo2", Tissue::Comparator, None).unwrap();
        let b = Specimen::new("Demo2", Tissue::Tumor, Some(20.0)).unwrap();
        assert_eq!(Pair::new(a, b).unwrap().log2_change().unwrap(), None);
    }

    #[test]
    fn private_field_invariants_and_pair_identity() {
        assert!(Specimen::new(" ", Tissue::Tumor, Some(3.0)).is_err());
        assert!(Specimen::new("Demo", Tissue::Tumor, Some(f64::NAN)).is_err());
        let a = Specimen::new("One", Tissue::Comparator, Some(10.0)).unwrap();
        let b = Specimen::new("Two", Tissue::Tumor, Some(20.0)).unwrap();
        assert!(Pair::new(a, b).is_err());
    }

    #[test]
    fn traits_and_polymorphism_do_not_expose_person_id() {
        let record = Specimen::new("PrivateTeachingPerson", Tissue::Tumor, None).unwrap();
        let gene = GeneAnnotation::new("ESR1", "hormone-related biology").unwrap();
        let direct = describe_one(&gene);
        assert!(direct.contains("biological reference"));
        let summaries = describe_many(&[&record, &gene]);
        assert_eq!(summaries.len(), 2);
        assert!(!summaries.join("").contains("PrivateTeachingPerson"));
        assert!(GeneAnnotation::new("esr1", "reference").is_err());
    }
}
