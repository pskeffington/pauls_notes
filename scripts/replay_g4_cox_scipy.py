#!/usr/bin/env python3
"""Independent Cox PH refit on synthetic held-out folds. SciPy reference.

For the frozen continuous-time generator observed event ties are not expected.
Reject ties rather than silently claiming Efron/Breslow equivalence.
"""
import csv
import math
import pathlib
import sys
import numpy as np
from scipy.optimize import minimize

TAU=24.0

def read(path):
    with open(path,newline="",encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

def fit_cox(train):
    x=np.array([[float(z["age_years"]),float(z["marker"])] for z in train])
    t=np.array([float(z["time_months"]) for z in train])
    e=np.array([int(z["event"]) for z in train],dtype=int)
    if not np.isfinite(x).all() or not np.isfinite(t).all() or not set(e).issubset({0,1}):
        raise ValueError("Invalid training data")
    ev=t[e==1]
    if len(set(ev))!=len(ev):
        raise ValueError("Event-time ties require a distinct verified Efron reference")
    center=x.mean(axis=0)
    xc=x-center
    order=np.argsort(-t)
    xs=xc[order]
    ts=t[order]
    es=e[order]
    event_idx=np.flatnonzero(es==1)
    def objective(beta):
        eta=xs@beta
        # Stable risk-set denominators: log-sum-exp for each event risk set.
        result=0.0
        grad=np.zeros(2)
        for i in event_idx:
            risk=eta[:i+1]
            m=risk.max()
            w=np.exp(risk-m)
            total=w.sum()
            result += m+math.log(total)-eta[i]
            grad += (w@xs[:i+1])/total-xs[i]
        return result,grad
    res=minimize(objective,np.zeros(2),jac=True,method="BFGS",
                 options={"gtol":1e-9,"maxiter":1000})
    if not np.isfinite(res.x).all() or np.linalg.norm(res.jac)>1e-6:
        raise ValueError(f"Independent Cox optimizer residual: {np.linalg.norm(res.jac)}")
    beta=res.x
    eta=xc@beta
    # No event-time ties; baseline cumulative hazard with risk weights.
    h0=0.0
    for te in sorted(ev):
        at_risk=np.exp(eta[t>=te]).sum()
        h0+=1.0/at_risk if te<=TAU else 0.0
    return beta,center,h0

def replay(folder,coefficient_tol=2e-4,survival_tol=3e-4):
    data=read(folder/"development_cohort.csv")
    pred=read(folder/"oof_predictions.csv")
    alloc=read(folder/"allocation.csv")
    coefficients=read(folder/"cox_coefficients.csv")
    declared={int(v["fold"]):v for v in coefficients}
    if set(declared)!={1,2,3} or len(coefficients)!=3:
        raise ValueError("Missing or duplicate coefficient record")
    if len(data)!=180 or len(pred)!=180 or len(alloc)!=240:
        raise ValueError("Unexpected cohort cardinality")
    rows={r["person_id"]:r for r in data}
    membership={r["person_id"]:r for r in alloc}
    if set(rows)!={p["person_id"] for p in pred}: raise ValueError("OOF mismatch")
    result=[]
    for fold in (1,2,3):
        test=[r for r in pred if int(r["fold"])==fold]
        if len(test)!=60: raise ValueError("Unexpected fold size")
        for p in test:
            if membership[p["person_id"]]["allocation"]!="development" or int(membership[p["person_id"]]["fold"])!=fold:
                raise ValueError("Reserve/fold leakage")
        held={r["person_id"] for r in test}
        training=[r for r in data if r["person_id"] not in held]
        beta,center,h0=fit_cox(training)
        expected=np.array([float(declared[fold]["age_years"]),float(declared[fold]["marker"])])
        if not np.isfinite(expected).all() or np.max(np.abs(beta-expected))>coefficient_tol:
            raise ValueError(f"Fold {fold} independently fitted coefficient mismatch")
        maxerr=0.0
        for p in test:
            raw=rows[p["person_id"]]
            features=np.array([float(raw["age_years"]),float(raw["marker"])])
            # Cox model centered baseline: exp(-H0 exp((x-mean)*beta)).
            calculated=math.exp(-h0*math.exp((features-center)@beta))
            recorded=float(p["cox_survival_24"])
            if not (0<=recorded<=1) or not math.isfinite(recorded):
                raise ValueError("Invalid recorded Cox survival")
            maxerr=max(maxerr,abs(calculated-recorded))
        if maxerr>survival_tol:
            raise ValueError(f"Fold {fold} independent survival mismatch {maxerr}")
        result.append((fold,beta.tolist(),maxerr))
    for fold,beta,error in result:
        print(f"fold={fold} independent_beta={beta} max_survival_error={error:.10g}")
    print("PASS independently fitted Cox 24-month synthetic survival reference")
    return result

if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("Usage: python scripts/replay_g4_cox_scipy.py EXTERNAL_OUTPUT_DIR")
    replay(pathlib.Path(sys.argv[1]))
