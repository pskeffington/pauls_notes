#!/usr/bin/env python3
"""Small invented oncology cohort: keys, denominators and person-level splits.

Synthetic teaching fixture only. No patient data, model fitting or network access.
"""
from __future__ import annotations

from collections import Counter
from datetime import date
import json

PERSON_IDS = tuple(f"P{i:02d}" for i in range(1, 7))
SAMPLES = [
    {"specimen_id": f"S{i:02d}", "person_id": f"P{i:02d}", "date": "2025-01-10",
     "baseline": True, "assay_available": i != 5} for i in range(1, 7)
] + [
    {"specimen_id": "S07", "person_id": "P01", "date": "2025-03-01", "baseline": False, "assay_available": True},
    {"specimen_id": "S08", "person_id": "P02", "date": "2025-03-15", "baseline": False, "assay_available": True},
    {"specimen_id": "S09", "person_id": "P04", "date": "2025-04-01", "baseline": False, "assay_available": True},
]
SPLIT = {person: ("development" if i < 4 else "held_out")
         for i, person in enumerate(PERSON_IDS)}

def validate(people=PERSON_IDS, samples=SAMPLES):
    """Raise on broken keys, invalid dates or duplicate specimen IDs."""
    if len(people) != len(set(people)):
        raise ValueError("duplicate person identifier")
    sample_ids = [sample["specimen_id"] for sample in samples]
    if len(sample_ids) != len(set(sample_ids)):
        raise ValueError("duplicate specimen identifier")
    for sample in samples:
        if sample["person_id"] not in people:
            raise ValueError("unlinked specimen")
        if not isinstance(sample["baseline"], bool) or not isinstance(sample["assay_available"], bool):
            raise ValueError("invalid boolean field")
        date.fromisoformat(sample["date"])
        if sample["baseline"] and sample["date"] != "2025-01-10":
            raise ValueError("incorrect synthetic baseline date")

def split_rows(samples, assignments):
    """Return specimen assignments, enforcing one partition per person."""
    if set(assignments.values()) - {"development", "held_out"}:
        raise ValueError("unexpected partition name")
    if any(s["person_id"] not in assignments for s in samples):
        raise ValueError("person with no assigned partition")
    rows = [(s["specimen_id"], s["person_id"], assignments[s["person_id"]]) for s in samples]
    by_person = {}
    for _, person, group in rows:
        by_person.setdefault(person, set()).add(group)
    if any(len(groups) != 1 for groups in by_person.values()):
        raise ValueError("person appears in multiple partitions")
    return rows

def summarize(people=PERSON_IDS, samples=SAMPLES):
    validate(people, samples)
    with_assay = {s["person_id"] for s in samples if s["baseline"] and s["assay_available"]}
    partitions = split_rows(samples, {p: SPLIT[p] for p in people})
    return {
        "people": len(people),
        "specimens": len(samples),
        "baseline_assay_people": len(with_assay),
        "held_out_people": sum(SPLIT[p] == "held_out" for p in people),
        "specimens_by_person": dict(sorted(Counter(s["person_id"] for s in samples).items())),
        "split_overlap": sorted({p for _, p, grp in partitions if
                                  any(other_p == p and other_grp != grp
                                      for _, other_p, other_grp in partitions)}),
    }

def main():
    print(json.dumps(summarize(), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
