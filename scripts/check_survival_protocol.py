#!/usr/bin/env python3
"""Offline G4 synthetic survival protocol gate, NOT an analysis executor.

A passing check confirms a frozen *specification*, not fitted Cox models,
survival outcomes, a reproducibility replay or authorization for real data.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "04_machine_learning/evidence/survival-contract-v1.json"
PROTOCOL = ROOT / "04_machine_learning/survival-protocol.md"
DICTIONARY = ROOT / "04_machine_learning/survival-data-dictionary.md"

TOP_FIELDS = {
    "schema_version", "protocol_id", "declaration_date", "lifecycle", "scope",
    "data_source", "synthetic_only", "clinical_use_authorized",
    "real_cancer_data_admitted", "no_individual_prognosis", "scientific_question",
    "unit_of_analysis", "generator", "observation_schema", "endpoint",
    "partition", "estimators", "evaluation", "quality_gates", "reporting",
}
SCHEMA = ["person_id", "age_years", "marker", "time_months", "event"]


def load_contract(path=CONTRACT):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(contract, protocol, dictionary):
    """Return structural/scientific-boundary defects without computing outcomes."""
    issues = []

    def require(condition, name):
        if not condition:
            issues.append(name)

    if not isinstance(contract, dict):
        return ["Contract must be an object"]
    require(set(contract) == TOP_FIELDS, "Unexpected or absent top-level field")
    if not TOP_FIELDS.issubset(contract):
        return issues

    require(type(contract["schema_version"]) is int and contract["schema_version"] == 1,
            "Frozen contract schema must equal 1")
    require(contract["protocol_id"] == "oncology-synthetic-survival-g4-v1", "Protocol identity changed")
    require(contract["declaration_date"] == "2026-10-17", "Protocol declaration date changed")
    require(contract["lifecycle"] == "protocol_only_not_executed",
            "Unexecuted protocol must not claim a completed assessment")
    require(contract["data_source"] == "internally_generated_synthetic_only" and
            contract["synthetic_only"] is True and
            contract["clinical_use_authorized"] is False and
            contract["real_cancer_data_admitted"] is False and
            contract["no_individual_prognosis"] is True,
            "Only synthetic, research-only, nonclinical source is permitted")
    require("oncology" in str(contract["scope"]).lower() and
            "cancer research broadly" in str(contract["scope"]).lower(),
            "Current cancer lesson must not become a repository-wide TCGA restriction")
    require("24-month" in str(contract["scientific_question"]) and
            "Kaplan-Meier" in str(contract["scientific_question"]),
            "Frozen survival question or null comparison changed")
    require("independent invented person" in str(contract["unit_of_analysis"]),
            "Independent person unit changed")

    g = contract["generator"]
    if not isinstance(g, dict):
        return issues + ["Generator must be an object"]
    for key, expected in {
        "engine": "R base random generators",
        "rng_kind": ["Mersenne-Twister", "Inversion", "Rejection"],
        "generator_seed": 26102401, "people": 240, "baseline_hazard_per_month": .022,
        "age_center": 50, "age_log_hazard_per_year": .025, "marker_log_hazard": .50,
        "observed_time_rule": "pmin(event_time, censor_time)",
        "event_rule": "as.integer(event_time <= censor_time)",
        "ties_rule": "event_if_equal", "missingness": "none",
        "repeated_person_records": False, "competing_events": False,
        "delayed_entry": False,
    }.items():
        require(g.get(key) == expected, "Frozen generator field changed: " + key)
    require(g.get("age_years") == {"distribution": "uniform", "min": 30, "max": 75} and
            g.get("marker") == {"distribution": "normal", "mean": 0, "sd": 1},
            "Baseline feature generator changed")
    require(g.get("censor_time") == {
        "distribution": "uniform", "min_months": 12, "max_months": 60,
        "independent_of": ["event_time", "age_years", "marker"],
    }, "Independent right-censoring contract changed")
    require("U_event" in str(g.get("event_time_rule")) and
            "age_years" in str(g.get("event_time_rule")) and
            "marker" in str(g.get("event_time_rule")),
            "Event-generating equation missing")
    schema = contract["observation_schema"]
    require(isinstance(schema, list) and
            [row.get("name") if isinstance(row, dict) else None for row in schema] == SCHEMA,
            "Model input must have exactly five ordered synthetic fields")
    if isinstance(schema, list):
        for row in schema:
            if isinstance(row, dict):
                require(row.get("missing") == "prohibited" and
                        row.get("type") in {"synthetic_unique_id", "finite_numeric",
                                            "finite_positive_numeric", "integer_binary"},
                        "Unexpected missingness or model input field type")

    endpoint = contract["endpoint"]
    if not isinstance(endpoint, dict):
        return issues + ["Endpoint must be an object"]
    require(endpoint.get("horizon_months") == 24 and endpoint.get("unit") == "months" and
            endpoint.get("event_code") == 1 and endpoint.get("censored_code") == 0 and
            endpoint.get("no_competing_risk") is True and
            endpoint.get("no_left_truncation") is True and
            "month zero" in str(endpoint.get("time_origin")),
            "Fictional 24-month right-censored event endpoint changed")
    require("not verified clinical" in str(endpoint.get("fictional_event")),
            "Fictional event must not be presented as verified recurrence")
    p = contract["partition"]
    if not isinstance(p, dict):
        return issues + ["Partition must be an object"]
    require(p.get("reserve_seed") == 26102402 and p.get("fold_seed") == 26102403 and
            p.get("development_people") == 180 and p.get("reserved_people") == 60 and
            p.get("outer_folds") == 3 and p.get("outer_people_per_fold") == 60,
            "Frozen reserve/development person allocation changed")
    require("sample.int(240)" in str(p.get("split_algorithm")) and
            "sample.int(180)" in str(p.get("outer_algorithm")) and
            "never used" in str(p.get("reserved_policy")),
            "Person-disjoint split or held-out reserve protection changed")
    require(p.get("development_people", 0) + p.get("reserved_people", 0) == g.get("people"),
            "Development + reserve must equal generator person count")
    require(p.get("outer_people_per_fold", 0) * p.get("outer_folds", 0) ==
            p.get("development_people"), "Outer fold counts must cover development people exactly")

    est = contract["estimators"]
    if not isinstance(est, dict) or set(est) != {"cox", "null", "censor"}:
        return issues + ["Exactly Cox, null KM and censor KM required"]
    require(est["cox"].get("model") == "survival::coxph" and
            est["cox"].get("formula") ==
            "Surv(time_months, event) ~ age_years + marker" and
            est["cox"].get("ties") == "efron" and
            "survival::survfit" in str(est["cox"].get("prediction")) and
            "training fold only" in str(est["cox"].get("learning")),
            "Fixed Cox training-only survival probability contract changed")
    require(est["null"].get("model") == "survival::survfit" and
            est["null"].get("formula") == "Surv(time_months, event) ~ 1" and
            "training-only" in str(est["null"].get("prediction")),
            "Null KM baseline changed")
    require(est["censor"].get("model") == "survival::survfit" and
            est["censor"].get("formula") == "Surv(time_months, 1 - event) ~ 1" and
            est["censor"].get("train_only") is True and
            est["censor"].get("positivity_threshold_at_horizon") == .20 and
            est["censor"].get("no_weight_clipping") is True,
            "Training-only reverse KM censoring model changed")

    ev = contract["evaluation"]
    if not isinstance(ev, dict):
        return issues + ["Evaluation must be an object"]
    require("IPCW Brier" in str(ev.get("primary")) and
            "Cox minus null" in str(ev.get("primary")) and
            "event" in str(ev.get("event_term")) and
            "Ghat(time-)" in str(ev.get("event_term")) and
            "Ghat(24)" in str(ev.get("event_free_term")) and
            "zero weight" in str(ev.get("censored_early")) and
            "not sum of weights" in str(ev.get("weight_denominator")) and
            "training fold only" in str(ev.get("censor_weight_fit")),
            "Brier assessment must be censor-aware and out-of-fold")
    require(ev.get("secondary", "").startswith("held-out Harrell") and
            ev.get("no_hypothesis_significance_threshold") is True and
            ev.get("no_secondary_endpoint_switching") is True and
            "reject Ghat(24) < 0.20" in str(ev.get("support_fail_condition")),
            "Frozen secondary metric or horizon support rule changed")
    cal = ev.get("calibration", {})
    require(isinstance(cal, dict) and
            cal.get("bin_edges") == [0, .33, .66, 1] and
            cal.get("min_people") == 15 and cal.get("min_observed_events") == 5 and
            "unavailable" in str(cal.get("insufficient_policy")),
            "Prespecified descriptive calibration bins or availability rules changed")

    qc = contract["quality_gates"]
    if not isinstance(qc, dict):
        return issues + ["Quality-gate block missing"]
    require(qc.get("minimum_outer_train_events") == 15 and
            qc.get("minimum_outer_test_events") == 5 and
            qc.get("minimum_outer_test_events_by_horizon") == 3 and
            "fail closed" in str(qc.get("infeasible_protocol")),
            "Feasibility gates must fail closed without seed search")
    required_bad = {
        "duplicate person_id", "overlapping person folds",
        "reserved person exposed", "censoring survival unsupported at 24",
        "censored-before-horizon mislabeled as event-free",
        "Cox score confused with absolute survival probability",
    }
    require(required_bad.issubset(set(qc.get("negative_cases", []))),
            "Adversarial survival data cases missing")
    require("outside public Git" in str(qc.get("output_storage")) and
            "failure_records" in qc.get("frozen_outputs", []),
            "Versioned replay/failure containment contract changed")

    report = contract["reporting"]
    require(isinstance(report, dict) and
            "NOT FOR CLINICAL USE" in str(report.get("disclaimer")) and
            "D1" in str(report.get("admission_note")) and
            "TRIPOD+AI" in str(report.get("guidelines")),
            "Scientific reporting, nonclinical disclaimer or D1 boundary absent")

    require("**Stage:** frozen" in protocol and
            "not executed" in protocol.lower() and
            "IPCW_Brier(24)" in protocol and
            "Ghat(t_i-)" in protocol and
            "Ghat(24)" in protocol and
            "60" in protocol and
            "180" in protocol and
            "24 months" in protocol and
            "no model" not in protocol.lower(),
            "Protocol narrative absent or inconsistent with assessment contract")
    require("one independent invented person" in dictionary and
            "`time_months`" in dictionary and
            "censoring at/before 24" in dictionary and
            "S001...S240" in dictionary and
            "NOT FOR CLINICAL USE" in dictionary,
            "Participant/censoring dictionary incomplete")
    return issues


def main():
    failures = validate(load_contract(),
                        PROTOCOL.read_text(encoding="utf-8"),
                        DICTIONARY.read_text(encoding="utf-8"))
    if failures:
        for item in failures:
            print("FAILED G4 contract: " + item, file=sys.stderr)
        raise SystemExit(1)
    print("PASS: G4 frozen synthetic survival protocol, one-person unit, endpoint, "
          "train-only Cox/KM/censoring, IPCW horizon and nonclinical guard")
    print("NOTE: No survival data were generated and no model was fitted by this protocol check")


if __name__ == "__main__":
    main()
