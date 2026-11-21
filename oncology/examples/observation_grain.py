#!/usr/bin/env python3
"""Small invented oncology cohort: keys, denominators and person-level splits.

Synthetic teaching fixture only. No patient data, model fitting or network access.
"""
from __future__ import annotations

from collections import Counter
from datetime import date
import argparse
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

# The teaching linkage rule permits at most one visit per person and date.
# P06 has a specimen but no visit row; V03 has no same-date specimen.
VISITS = [
    {"visit_id": "V01", "person_id": "P01", "date": "2025-01-10"},
    {"visit_id": "V02", "person_id": "P01", "date": "2025-03-01"},
    {"visit_id": "V03", "person_id": "P01", "date": "2025-06-01"},
    {"visit_id": "V04", "person_id": "P02", "date": "2025-01-10"},
    {"visit_id": "V05", "person_id": "P02", "date": "2025-03-15"},
    {"visit_id": "V06", "person_id": "P03", "date": "2025-01-10"},
    {"visit_id": "V07", "person_id": "P04", "date": "2025-01-10"},
    {"visit_id": "V08", "person_id": "P04", "date": "2025-04-01"},
    {"visit_id": "V09", "person_id": "P05", "date": "2025-01-10"},
]


def require_identifier(value, kind):
    """Reject missing, blank or nonstring keys before hashing or matching."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"empty or invalid {kind} identifier")


def require_canonical_date(value, kind):
    """Require YYYY-MM-DD so equal calendar days have equal join keys."""
    try:
        canonical = date.fromisoformat(value).isoformat()
    except (TypeError, ValueError):
        raise ValueError(f"{kind} date must use canonical YYYY-MM-DD") from None
    if value != canonical:
        raise ValueError(f"{kind} date must use canonical YYYY-MM-DD")


def validate_people(people):
    """Require valid, unique participant identifiers in the eligibility roster."""
    for person in people:
        require_identifier(person, "person")
    if len(people) != len(set(people)):
        raise ValueError("duplicate person identifier")


def validate(people=PERSON_IDS, samples=SAMPLES):
    """Raise on broken keys, invalid dates or duplicate specimen IDs."""
    validate_people(people)
    sample_ids = [sample["specimen_id"] for sample in samples]
    for specimen_id in sample_ids:
        require_identifier(specimen_id, "specimen")
    if len(sample_ids) != len(set(sample_ids)):
        raise ValueError("duplicate specimen identifier")
    for sample in samples:
        require_identifier(sample["person_id"], "specimen parent")
        if sample["person_id"] not in people:
            raise ValueError("unlinked specimen")
        if not isinstance(sample["baseline"], bool) or not isinstance(sample["assay_available"], bool):
            raise ValueError("invalid boolean field")
        require_canonical_date(sample["date"], "specimen")
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

def visit_index(people, visits):
    """Validate visit keys and return the declared person/date lookup.

    Same-date linkage is stipulated for this fixture; it is not a general
    inference that a clinical specimen belongs to a particular encounter.
    """
    validate_people(people)
    by_key = {}
    visit_ids = set()
    for visit in visits:
        visit_id = visit["visit_id"]
        require_identifier(visit_id, "visit")
        if visit_id in visit_ids:
            raise ValueError("duplicate visit identifier")
        require_identifier(visit["person_id"], "visit parent")
        if visit["person_id"] not in people:
            raise ValueError("unlinked visit")
        require_canonical_date(visit["date"], "visit")
        key = (visit["person_id"], visit["date"])
        if key in by_key:
            raise ValueError("ambiguous person-date visit key")
        visit_ids.add(visit_id)
        by_key[key] = visit
    return by_key


def link_specimens_to_visits(people=PERSON_IDS, samples=SAMPLES, visits=VISITS):
    """Keep one row per specimen and report unmatched records on both sides."""
    validate(people, samples)
    by_key = visit_index(people, visits)
    rows = []
    used_visits = set()
    unmatched_specimens = []
    for sample in samples:
        visit = by_key.get((sample["person_id"], sample["date"]))
        visit_id = visit["visit_id"] if visit is not None else None
        rows.append({**sample, "visit_id": visit_id})
        if visit_id is None:
            unmatched_specimens.append(sample["specimen_id"])
        else:
            used_visits.add(visit_id)
    return {
        "rows": rows,
        "unmatched_specimen_ids": sorted(unmatched_specimens),
        "unused_visit_ids": sorted(v["visit_id"] for v in visits
                                   if v["visit_id"] not in used_visits),
    }


def baseline_person_rows(people=PERSON_IDS, samples=SAMPLES):
    """Select the stipulated baseline specimen without dropping roster members.

    None means no eligible baseline specimen; False means a selected specimen
    explicitly has no available assay. Multiple eligible rows require a rule.
    """
    validate(people, samples)
    selected = {}
    for sample in samples:
        if sample["baseline"]:
            person = sample["person_id"]
            if person in selected:
                raise ValueError("multiple eligible baseline specimens")
            selected[person] = sample
    return [
        {
            "person_id": person,
            "baseline_specimen_id": (selected[person]["specimen_id"]
                                     if person in selected else None),
            "baseline_assay_available": (selected[person]["assay_available"]
                                         if person in selected else None),
        }
        for person in people
    ]


def join_exercise():
    """Compare a deliberately wrong inner join with a grain-preserving join."""
    linked = link_specimens_to_visits()
    # Deliberate counterexample: every specimen matches every visit of its owner.
    bad_rows = [
        {**sample, "visit_id": visit["visit_id"]}
        for sample in SAMPLES for visit in VISITS
        if sample["person_id"] == visit["person_id"]
    ]
    bad_counts = Counter(row["person_id"] for row in bad_rows)
    retained_people = set(bad_counts)
    retained_baseline_assays = {
        row["person_id"] for row in bad_rows
        if row["baseline"] and row["assay_available"]
    }
    participant_rows = baseline_person_rows(samples=linked["rows"])
    return {
        "source": "invented teaching records only",
        "original_summary": summarize(),
        "visit_records": len(VISITS),
        "incorrect_person_only_inner_join": {
            "rows": len(bad_rows),
            "rows_by_person": {p: bad_counts[p] for p in PERSON_IDS},
            "distinct_people": len(retained_people),
            "lost_people": sorted(set(PERSON_IDS) - retained_people),
            "people_with_baseline_assay": len(retained_baseline_assays),
        },
        "repaired_specimen_left_join": {
            "rows": len(linked["rows"]),
            "distinct_people": len({r["person_id"] for r in linked["rows"]}),
            "unmatched_specimen_ids": linked["unmatched_specimen_ids"],
            "unused_visit_ids": linked["unused_visit_ids"],
        },
        "baseline_participant_rows": participant_rows,
    }


def run_checks():
    """Replay hand-counted joins and reject ambiguous or orphaned keys."""
    def check(condition, message):
        if not condition:
            raise AssertionError(message)

    def rejects(operation, expected_message):
        try:
            operation()
        except ValueError as error:
            check(expected_message in str(error), str(error))
        else:
            raise AssertionError("invalid input was accepted: " + expected_message)

    check(summarize() == {
        "people": 6, "specimens": 9, "baseline_assay_people": 5,
        "held_out_people": 2,
        "specimens_by_person": {"P01": 2, "P02": 2, "P03": 1,
                                "P04": 2, "P05": 1, "P06": 1},
        "split_overlap": [],
    }, "original fixture summary changed")
    demo = join_exercise()
    check(demo["visit_records"] == 9, "visit denominator changed")
    check(demo["incorrect_person_only_inner_join"] == {
        "rows": 16,
        "rows_by_person": {"P01": 6, "P02": 4, "P03": 1,
                           "P04": 4, "P05": 1, "P06": 0},
        "distinct_people": 5, "lost_people": ["P06"],
        "people_with_baseline_assay": 4,
    }, "person-only join no longer matches the hand calculation")
    check(demo["repaired_specimen_left_join"] == {
        "rows": 9, "distinct_people": 6,
        "unmatched_specimen_ids": ["S06"], "unused_visit_ids": ["V03"],
    }, "specimen join lost rows or concealed unmatched records")
    expected_matches = dict(zip(
        (f"S{i:02d}" for i in range(1, 10)),
        ("V01", "V04", "V06", "V07", "V09", None, "V02", "V05", "V08"),
    ))
    check({r["specimen_id"]: r["visit_id"]
           for r in link_specimens_to_visits()["rows"]} == expected_matches,
          "specimens linked to the wrong visits")
    participant_rows = demo["baseline_participant_rows"]
    check(len(participant_rows) == 6 and
          sum(r["baseline_assay_available"] is True for r in participant_rows) == 5,
          "participant baseline denominator changed")
    check(participant_rows[4]["baseline_assay_available"] is False and
          participant_rows[5]["baseline_assay_available"] is True,
          "an unmatched visit changed an observed assay flag")
    no_visits = link_specimens_to_visits(visits=[])
    check(len(no_visits["rows"]) == 9 and
          len(no_visits["unmatched_specimen_ids"]) == 9 and
          no_visits["unused_visit_ids"] == [],
          "an empty visit table discarded the specimen roster")
    no_sixth_baseline = baseline_person_rows(
        samples=[s for s in SAMPLES if s["specimen_id"] != "S06"])
    check(len(no_sixth_baseline) == 6 and no_sixth_baseline[5] == {
        "person_id": "P06", "baseline_specimen_id": None,
        "baseline_assay_available": None,
    }, "absent baseline specimen was dropped or recoded as assay failure")
    rejects(lambda: link_specimens_to_visits(samples=SAMPLES + [SAMPLES[0]]),
            "duplicate specimen identifier")
    rejects(lambda: link_specimens_to_visits(
        samples=[{**SAMPLES[0], "person_id": "P99"}]), "unlinked specimen")
    rejects(lambda: link_specimens_to_visits(visits=VISITS + [VISITS[0]]),
            "duplicate visit identifier")
    rejects(lambda: link_specimens_to_visits(visits=VISITS + [
        {**VISITS[0], "visit_id": "V10"}]), "ambiguous person-date visit key")
    rejects(lambda: link_specimens_to_visits(visits=[
        {**VISITS[0], "person_id": "P99"}]), "unlinked visit")
    rejects(lambda: link_specimens_to_visits(visits=[
        {**VISITS[0], "visit_id": ""}]), "empty or invalid visit identifier")
    rejects(lambda: baseline_person_rows(samples=SAMPLES + [
        {**SAMPLES[0], "specimen_id": "S10"}]), "multiple eligible baseline specimens")
    for invalid_id in ("", " ", None, 7, []):
        rejects(lambda: validate(people=(invalid_id,), samples=[]),
                "empty or invalid person identifier")
        rejects(lambda: link_specimens_to_visits(samples=[
            {**SAMPLES[0], "specimen_id": invalid_id}]),
                "empty or invalid specimen identifier")
        rejects(lambda: link_specimens_to_visits(samples=[
            {**SAMPLES[0], "person_id": invalid_id}]),
                "empty or invalid specimen parent identifier")
        rejects(lambda: link_specimens_to_visits(visits=[
            {**VISITS[0], "person_id": invalid_id}]),
                "empty or invalid visit parent identifier")
        rejects(lambda: link_specimens_to_visits(visits=[
            {**VISITS[0], "visit_id": invalid_id}]),
                "empty or invalid visit identifier")
    for invalid_date in ("20250110", "2025-W02-5", None, "2025-02-30"):
        rejects(lambda: link_specimens_to_visits(samples=[
            {**SAMPLES[0], "date": invalid_date}]),
                "specimen date must use canonical YYYY-MM-DD")
        rejects(lambda: link_specimens_to_visits(visits=[
            {**VISITS[0], "date": invalid_date}]),
                "visit date must use canonical YYYY-MM-DD")
    # A compact duplicate must not bypass the one-visit-per-participant-day rule.
    rejects(lambda: link_specimens_to_visits(visits=VISITS + [
        {**VISITS[0], "visit_id": "V10", "date": "20250110"}]),
            "visit date must use canonical YYYY-MM-DD")
    print("PASS: observation-grain joins, selection, unmatched records, and invalid inputs.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--join-demo", action="store_true",
                      help="show the bad join, repaired linkage, and participant table")
    mode.add_argument("--check", action="store_true",
                      help="check counts, preserved output, and rejected invalid keys")
    args = parser.parse_args()
    if args.check:
        run_checks()
    else:
        result = join_exercise() if args.join_demo else summarize()
        print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
