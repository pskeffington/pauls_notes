#!/usr/bin/env python3
"""Independent standard-library G4 audit. Synthetic development-only input.

Does not import/reuse R fitting or IPCW implementation. Strictly checks saved
out-of-fold predictions, censor estimates and metrics against raw development
rows. No reserved outcomes are read or admitted.
"""
import argparse
import csv
import math
import pathlib
import re
import sys

TAU = 24.0
def fail(msg):
    raise ValueError(msg)

def rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def num(value):
    v = float(value)
    if not math.isfinite(v):
        fail("nonfinite numeric field")
    return v

def g_before(training, at, left=False):
    # Independent reverse Kaplan-Meier: failures are censored subjects.
    # Ties use all at-risk subjects just before each time; events remove
    # risk-set membership but are not censor failures.
    observations = [(num(r["time_months"]), int(r["event"])) for r in training]
    times = sorted({t for t, event in observations if event == 0 and
                    (t < at if left else t <= at)})
    estimate = 1.0
    for t in times:
        at_risk = sum(u >= t for u, _ in observations)
        censored = sum(u == t and e == 0 for u, e in observations)
        if at_risk <= 0:
            fail("no risk set")
        estimate *= 1 - censored / at_risk
    return estimate

def run(folder):
    data = rows(folder / "development_cohort.csv")
    alloc = rows(folder / "allocation.csv")
    predictions = rows(folder / "oof_predictions.csv")
    warning = (folder / "DISCLAIMER.txt").read_text()
    if "SYNTHETIC" not in warning or "NOT FOR CLINICAL USE" not in warning:
        fail("missing disclaimer")
    if len(data) != 180 or len(alloc) != 240 or len(predictions) != 180:
        fail("wrong population counts")
    ids = [r["person_id"] for r in data]
    if len(set(ids)) != 180:
        fail("duplicate development IDs")
    expected = {f"S{i:03d}" for i in range(1, 241)}
    if {r["person_id"] for r in alloc} != expected:
        fail("wrong allocation IDs")
    dev = {r["person_id"] for r in alloc if r["allocation"] == "development"}
    reserve = {r["person_id"] for r in alloc if r["allocation"] == "reserve"}
    if len(dev) != 180 or len(reserve) != 60 or set(ids) != dev:
        fail("development/reserve mismatch")
    if {r["person_id"] for r in predictions} != dev:
        fail("invalid out-of-fold membership")
    indexed = {r["person_id"]: r for r in data}
    test_sets = {}
    for record in predictions:
        fold = int(record["fold"])
        if fold not in (1, 2, 3):
            fail("unexpected fold")
        test_sets.setdefault(fold, []).append(record)
        allocation = next(x for x in alloc if x["person_id"] == record["person_id"])
        if int(allocation["fold"]) != fold:
            fail("fold assignment mismatch")
    if {k: len(v) for k, v in test_sets.items()} != {1: 60, 2: 60, 3: 60}:
        fail("fold sizes incorrect")
    cox_total = km_total = 0.0
    for fold, test in sorted(test_sets.items()):
        testids = {r["person_id"] for r in test}
        training = [r for r in data if r["person_id"] not in testids]
        if len(training) != 120:
            fail("training membership invalid")
        g24 = g_before(training, TAU)
        if g24 < 0.2:
            fail("insufficient training censor support")
        for rec in test:
            raw = indexed[rec["person_id"]]
            t = num(raw["time_months"])
            event = int(raw["event"])
            if event not in (0, 1) or t <= 0 or t > 60:
                fail("invalid outcome")
            if abs(t - num(rec["time_months"])) > 1e-10 or event != int(rec["event"]):
                fail("held-out outcome mismatch")
            losses = []
            for field in ("cox_survival_24", "km_survival_24"):
                p = num(rec[field])
                if p < 0 or p > 1:
                    fail("prediction outside probability bounds")
                if t <= TAU and event == 1:
                    g = g_before(training, t, left=True)
                    if g <= 0:
                        fail("zero G(t-) at event")
                    loss = p * p / g
                elif t > TAU:
                    loss = (1 - p) ** 2 / g24
                else:
                    loss = 0.0
                losses.append(loss)
            if abs(losses[0] - num(rec["cox_loss"])) > 1e-9:
                fail("Cox IPCW discrepancy")
            if abs(losses[1] - num(rec["km_loss"])) > 1e-9:
                fail("KM IPCW discrepancy")
            cox_total += losses[0]
            km_total += losses[1]
    cox = cox_total / 180
    km = km_total / 180
    report = (folder / "metrics.R").read_text()
    for key, expected_value in (
        ("cox_IPCW_Brier_24", cox),
        ("km_IPCW_Brier_24", km),
        ("paired_cox_minus_km", cox - km),
    ):
        match = re.search(r"\\b" + re.escape(key) + r"\\s*=\\s*([-+0-9.eE]+)", report)
        if match is None or abs(num(match.group(1)) - expected_value) > 1e-9:
            fail(f"reported metric mismatch: {key}")
    print(f"PASS independent G4 replay: n=180, Cox={cox:.12f}, KM={km:.12f}, difference={cox-km:.12f}")
    return cox, km

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("output_directory", type=pathlib.Path)
    a = p.parse_args()
    try:
        run(a.output_directory)
    except (ValueError, OSError, KeyError) as exc:
        print(f"FAIL independent G4 replay: {exc}", file=sys.stderr)
        sys.exit(1)
