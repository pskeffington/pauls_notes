#!/usr/bin/env python3
"""CO-05: exact and checked arithmetic on entirely invented oncology examples.

Educational calculations only. No patient data, clinical decisions, or I/O beyond
printing a small synthetic example summary. No third-party packages required.
"""
from __future__ import annotations

import json
import math
from numbers import Real


def finite(name: str, value: Real, *, positive: bool = False) -> float:
    """Check scalar numeric input, rejecting bool, nan, infinity and invalid sign."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{name} must be a real numeric scalar")
    output = float(value)
    if not math.isfinite(output) or (positive and output <= 0):
        raise ValueError(f"{name} must be finite" + (" and positive" if positive else ""))
    return output


def count(name: str, value: Real) -> int:
    """Nonnegative integer count (not a floating estimate)."""
    number = finite(name, value)
    if number < 0 or not number.is_integer():
        raise ValueError(f"{name} must be a nonnegative integer")
    return int(number)


def proportion(part: Real, whole: Real) -> float:
    n = count("part", part)
    d = count("whole", whole)
    if not d or n > d:
        raise ValueError("proportion needs 0 <= part <= whole and whole > 0")
    return n / d


def incidence_per_100k(events: Real, population: Real) -> float:
    """Population-based count rate per 100,000; NOT a person-time rate."""
    e = count("events", events)
    p = count("population", population)
    if p == 0:
        raise ValueError("population must be nonzero")
    # One person may contribute more than one primary cancer, so e <= p is NOT imposed.
    return e / p * 100_000


def implied_events(rate_per_100k: Real, population: Real) -> float:
    rate = finite("rate_per_100k", rate_per_100k)
    p = count("population", population)
    if rate < 0 or p == 0:
        raise ValueError("positive population and nonnegative rate required")
    return rate * p / 100_000


def person_time_rate_per_1000(events: Real, person_years: Real) -> float:
    e = count("events", events)
    time = finite("person_years", person_years, positive=True)
    return e / time * 1_000


def absolute_proportion_difference(p_a: Real, p_b: Real) -> float:
    first = finite("p_a", p_a)
    other = finite("p_b", p_b)
    if not (0 <= first <= 1 and 0 <= other <= 1):
        raise ValueError("proportions must lie in [0,1]")
    return first - other


def ratio_of_proportions(p_a: Real, p_b: Real) -> float:
    first = finite("p_a", p_a)
    other = finite("p_b", p_b)
    if not (0 <= first <= 1 and 0 < other <= 1):
        raise ValueError("ratio requires valid proportions and positive reference")
    return first / other


def cm_to_mm(value_cm: Real) -> float:
    x = finite("value_cm", value_cm)
    if x < 0:
        raise ValueError("length must be nonnegative")
    return x * 10


def ng_ml_to_pg_ml(value_ng_ml: Real) -> float:
    x = finite("value_ng_ml", value_ng_ml)
    if x < 0:
        raise ValueError("concentration must be nonnegative")
    return x * 1000


def log2_fold_change(numerator: Real, reference: Real) -> float:
    a = finite("numerator", numerator, positive=True)
    b = finite("reference", reference, positive=True)
    # Difference of logs avoids overflow for finite but very large values.
    return math.log2(a) - math.log2(b)


def idealized_doubling(initial: Real, elapsed_days: Real, doubling_days: Real) -> float:
    start = finite("initial", initial, positive=True)
    elapsed = finite("elapsed_days", elapsed_days)
    interval = finite("doubling_days", doubling_days, positive=True)
    if elapsed < 0:
        raise ValueError("elapsed_days must be nonnegative in this teaching model")
    try:
        result = start * (2.0 ** (elapsed / interval))
    except OverflowError as exc:
        raise ValueError("exponential result exceeds numeric range") from exc
    if not math.isfinite(result):
        raise ValueError("exponential result exceeds numeric range")
    return result


def z_score(value: Real, mean: Real, standard_deviation: Real) -> float:
    x = finite("value", value)
    mu = finite("mean", mean)
    sd = finite("standard_deviation", standard_deviation, positive=True)
    return (x - mu) / sd


def fixture_summary() -> dict[str, float]:
    """Independent fictional examples; do not combine their populations or endpoints."""
    a, b = proportion(18, 60), proportion(12, 60)
    return {
        "population_incidence_per_100k": incidence_per_100k(24, 80_000),
        "implied_incident_events": implied_events(30, 80_000),
        "person_time_rate_per_1000_py": person_time_rate_per_1000(12, 600),
        "group_a_response_proportion": a,
        "group_b_response_proportion": b,
        "response_percentage_point_difference": absolute_proportion_difference(a, b) * 100,
        "response_ratio": ratio_of_proportions(a, b),
        "lesion_length_mm": cm_to_mm(2.5),
        "analyte_pg_ml": ng_ml_to_pg_ml(0.8),
        "expression_log2_fold_change": log2_fold_change(80, 20),
        "abstract_doubled_quantity": idealized_doubling(100, 60, 30),
        "standard_score": z_score(75, 60, 10),
    }


def main() -> None:
    print(json.dumps(fixture_summary(), sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
