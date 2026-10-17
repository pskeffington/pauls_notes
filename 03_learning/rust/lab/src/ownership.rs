//! Owned String, borrowed &str, mutable Vec<T>, and Option<&str>.

/// Borrow the caller's text instead of moving an owned String.
pub fn character_count(text: &str) -> usize {
    text.chars().count()
}

/// A mutable borrow allows modification without returning or cloning the whole vector.
pub fn push_unique_label(labels: &mut Vec<String>, label: &str) -> Result<(), &'static str> {
    if label.is_empty() || label.trim() != label || label.chars().any(char::is_control) {
        return Err("Invalid teaching label");
    }
    if labels.iter().any(|existing| existing == label) {
        return Err("Duplicate teaching label");
    }
    labels.push(label.to_owned());
    Ok(())
}

/// A returned string slice remains borrowed from the input collection.
pub fn first_label(labels: &[String]) -> Option<&str> {
    labels.first().map(String::as_str)
}

/// This function consumes a String; the caller has to return or clone it to retain ownership.
pub fn uppercase_owned(value: String) -> String {
    value.to_uppercase()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn mutable_borrow_and_read_only_borrow() {
        let mut labels = vec!["ESR1".to_owned()];
        push_unique_label(&mut labels, "CD8A").unwrap();
        assert_eq!(first_label(&labels), Some("ESR1"));
        assert_eq!(character_count(&labels[1]), 4);
        assert_eq!(labels.len(), 2);
    }

    #[test]
    fn ownership_move_and_invalid_label() {
        let original = String::from("example");
        let transformed = uppercase_owned(original);
        assert_eq!(transformed, "EXAMPLE");
        let mut labels = Vec::new();
        assert!(push_unique_label(&mut labels, "").is_err());
        assert!(push_unique_label(&mut labels, "bad\nlabel").is_err());
        push_unique_label(&mut labels, "ESR1").unwrap();
        assert!(push_unique_label(&mut labels, "ESR1").is_err());
    }
}
