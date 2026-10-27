#!/usr/bin/env python3
"""CO-07: synthetic oncology screening probability and seeded Monte Carlo.

No patient data. Not a diagnostic, screening, or clinical decision tool.
The expected counts are mathematical expectations, not observed persons.
"""
from __future__ import annotations

import json
import math
import random
from numbers import Real


def probability(value: Real, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{label} must be a probability in [0, 1]")
    p = float(value)
    if not math.isfinite(p) or not 0 <= p <= 1:
        raise ValueError(f"{label} must be a probability in [0, 1]")
    return p


def positive_size(value: int, label: str = "n") -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 1000000:
        raise ValueError(f"{label} must be an integer between 1 and 1000000")
    return value


def conditional(joint: float, given: float) -> float:
    a = probability(joint, "joint")
    b = probability(given, "given")
    if b == 0 or a > b:
        raise ValueError("conditional probability requires 0 < given and joint <= given")
    return a / b


def union(p_a: float, p_b: float, p_intersection: float) -> float:
    a = probability(p_a, "P(A)")
    b = probability(p_b, "P(B)")
    i = probability(p_intersection, "P(A and B)")
    if i > min(a, b) or i < max(0.0, a + b - 1.0):
        raise ValueError("intersection is incompatible with marginal probabilities")
    return a + b - i


def screening_probabilities(prevalence: float, sensitivity: float, specificity: float) -> dict[str, float]:
    """Test-characteristic identity under fixed prevalence and test properties."""
    pi = probability(prevalence, "prevalence")
    se = probability(sensitivity, "sensitivity")
    sp = probability(specificity, "specificity")
    tp = pi * se
    fn = pi * (1 - se)
    fp = (1 - pi) * (1 - sp)
    tn = (1 - pi) * sp
    positive = tp + fp
    negative = tn + fn
    # Avoid manufacturing conditional probabilities when the conditioning event is impossible.
    if positive == 0 or negative == 0:
        raise ValueError("PPV or NPV undefined when one test-result group is empty")
    return {
        "p_true_positive": tp,
        "p_false_positive": fp,
        "p_false_negative": fn,
        "p_true_negative": tn,
        "p_test_positive": positive,
        "p_test_negative": negative,
        "ppv": tp / positive,
        "npv": tn / negative,
    }


def expected_screening_counts(n: int, prevalence: float, sensitivity: float, specificity: float) -> dict[str, float]:
    """Expected, possibly fractional cell counts in a hypothetical population."""
    size = positive_size(n)
    probs = screening_probabilities(prevalence, sensitivity, specificity)
    return {key.replace("p_", "expected_", 1): round(size * probs[key], 12)
            for key in ("p_true_positive", "p_false_positive", "p_false_negative", "p_true_negative")}


def probabilities_from_table(tp: int, fp: int, fn: int, tn: int) -> dict[str, float]:
    """Descriptive sample proportions from four nonnegative integer cells."""
    cells = (tp, fp, fn, tn)
    if any(isinstance(x, bool) or not isinstance(x, int) or x < 0 for x in cells):
        raise ValueError("contingency cells must be nonnegative integers")
    if (tp + fn == 0 or fp + tn == 0 or tp + fp == 0 or fn + tn == 0):
        raise ValueError("all four conditional denominators must be positive")
    return {
        "sensitivity": tp / (tp + fn),
        "specificity": tn / (fp + tn),
        "ppv": tp / (tp + fp),
        "npv": tn / (fn + tn),
    }


def simulate_screening(n: int, prevalence: float, sensitivity: float, specificity: float, *, seed: int = 711) -> dict[str, int]:
    """Draw a hypothetical cohort; does not force observed cells to equal expectation."""
    size = positive_size(n)
    pi = probability(prevalence, "prevalence")
    se = probability(sensitivity, "sensitivity")
    sp = probability(specificity, "specificity")
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("seed must be an integer")
    rng = random.Random(seed)
    tp = fp = fn = tn = 0
    for _ in range(size):
        disease = rng.random() < pi
        test_positive = rng.random() < (se if disease else 1 - sp)
        if disease and test_positive:
            tp += 1
        elif disease:
            fn += 1
        elif test_positive:
            fp += 1
        else:
            tn += 1
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn}


def fixture() -> dict[str, object]:
    low = screening_probabilities(0.01, 0.9, 0.95)
    high = screening_probabilities(0.05, 0.9, 0.95)
    expected = expected_screening_counts(10000, 0.01, 0.9, 0.95)
    return {
        "low_prevalence": low,
        "higher_prevalence": high,
        "expected_screening_counts": expected,
        "table_check": probabilities_from_table(90, 495, 10, 9405),
        "marker_event_given_positive": 8 / 20,
        "marker_positive_given_event": 8 / 16,
        "seeded_simulated_counts": simulate_screening(10000, 0.01, 0.9, 0.95),
    }


if __name__ == "__main__":
    print(json.dumps(fixture(), indent=2, sort_keys=True))
