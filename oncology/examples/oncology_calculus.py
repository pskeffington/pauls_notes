#!/usr/bin/env python3
"""CO-06: dependency-free, invented-data calculus and linear-algebra laboratory.

Educational functions and failure checks; not a clinical model, gene-signature
validator, numerical linear-algebra package, or treatment recommendation.
"""
from __future__ import annotations
import json
import math
from numbers import Real


def scalar(value, label):
    if isinstance(value, bool) or not isinstance(value, Real):
        raise ValueError(f"{label} must be a real number")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def vector(values, label):
    if not isinstance(values, (tuple, list)) or not values:
        raise ValueError(f"{label} must be a nonempty sequence")
    return [scalar(value, f"{label}[{i}]") for i, value in enumerate(values)]


def paired(x, y, *, minimum=2):
    xx = vector(x, "x")
    yy = vector(y, "y")
    if len(xx) != len(yy) or len(xx) < minimum:
        raise ValueError(f"paired arrays must share length >= {minimum}")
    return xx, yy


def average_slope(t0, y0, t1, y1):
    a = scalar(t0, "t0")
    b = scalar(t1, "t1")
    if b <= a:
        raise ValueError("second observation time must be later")
    return (scalar(y1, "y1") - scalar(y0, "y0")) / (b - a)


def derivative_square(x):
    return 2.0 * scalar(x, "x")


def finite_difference_square(x, h=1e-5):
    xx = scalar(x, "x")
    step = scalar(h, "h")
    if step <= 0:
        raise ValueError("finite difference requires h > 0")
    return ((xx + step)**2 - (xx - step)**2) / (2 * step)


def dot(a, b):
    aa, bb = paired(a, b, minimum=1)
    return math.fsum(x*y for x, y in zip(aa, bb))


def matrix_vector(rows, coefficients):
    b = vector(coefficients, "coefficients")
    if not isinstance(rows, (list, tuple)) or not rows:
        raise ValueError("matrix needs rows")
    ans = []
    for i, row in enumerate(rows):
        vals = vector(row, f"matrix row {i}")
        if len(vals) != len(b):
            raise ValueError("matrix and coefficient dimensions disagree")
        ans.append(math.fsum(a*v for a, v in zip(vals, b)))
    return ans


def ols_line(x, y):
    xx, yy = paired(x, y, minimum=3)
    n = len(xx)
    mx, my = math.fsum(xx)/n, math.fsum(yy)/n
    delta = [xi - mx for xi in xx]
    denom = math.fsum(d*d for d in delta)
    if denom <= 1e-12*max(1.0, math.fsum(xi*xi for xi in xx)):
        raise ValueError("design is constant or insufficiently variable")
    slope = math.fsum(d*(yi-my) for d, yi in zip(delta, yy))/denom
    return (my - slope*mx, slope)


def half_mean_squared_error(x, y, beta):
    xx, yy = paired(x, y, minimum=2)
    b = vector(beta, "coefficients")
    if len(b) != 2:
        raise ValueError("this teaching model has intercept and slope")
    predictions = matrix_vector([[1.0, xi] for xi in xx], b)
    return math.fsum((pred-obs)**2 for pred,obs in zip(predictions, yy))/(2*len(yy))


def mse_gradient(x, y, beta):
    xx, yy = paired(x, y, minimum=2)
    b = vector(beta, "coefficients")
    if len(b) != 2:
        raise ValueError("gradient requires intercept and slope")
    errors = [b[0]+b[1]*xi-yi for xi,yi in zip(xx,yy)]
    n=len(yy)
    return [math.fsum(errors)/n, math.fsum(e*xi for e,xi in zip(errors,xx))/n]


def numeric_gradient(x, y, beta, h=1e-5):
    b = vector(beta, "coefficients")
    if len(b)!=2:
        raise ValueError("two coefficients needed")
    hh = scalar(h, "h")
    if hh<=0:
        raise ValueError("positive finite difference step needed")
    ans=[]
    for i in range(2):
        plus=b.copy()
        minus=b.copy()
        plus[i]+=hh
        minus[i]-=hh
        ans.append((half_mean_squared_error(x,y,plus)-half_mean_squared_error(x,y,minus))/(2*hh))
    return ans


def gradient_descent(x, y, *, step=0.1, iterations=2000):
    xx, yy=paired(x,y,minimum=3)
    rate=scalar(step, "step")
    if rate<=0 or rate>=0.2:
        raise ValueError("teaching step must satisfy 0 < step < 0.2")
    if isinstance(iterations, bool) or not isinstance(iterations, int) or not 1 <= iterations <= 10000:
        raise ValueError("iterations out of teaching bounds")
    coefficients=[0.0,0.0]
    for _ in range(iterations):
        gradient=mse_gradient(xx,yy,coefficients)
        coefficients=[b-rate*g for b,g in zip(coefficients,gradient)]
        if not all(math.isfinite(b) for b in coefficients):
            raise ValueError("numerical divergence")
    return coefficients


def logistic(z):
    x=scalar(z, "z")
    if x>=0:
        inv=math.exp(-x)
        return 1/(1+inv)
    expx=math.exp(x)
    return expx/(1+expx)


def logistic_derivative(z):
    p=logistic(z)
    return p*(1-p)


def trapezoid(time, measurement):
    tt,vv=paired(time,measurement,minimum=2)
    if any(t1<=t0 for t0,t1 in zip(tt,tt[1:])):
        raise ValueError("time must be strictly increasing")
    return math.fsum((b-a)*(y0+y1)/2 for a,b,y0,y1 in zip(tt,tt[1:],vv,vv[1:]))


def fixtures():
    x=[0,1,2,3]
    y=[1,2,4,4]
    b=ols_line(x,y)
    predicted=matrix_vector([[1,xi] for xi in x],b)
    gradient=mse_gradient(x,y,[0,0])
    gd=gradient_descent(x,y)
    return {
        "average_slope":average_slope(0,1,2,5),
        "analytic_derivative":derivative_square(3),
        "finite_derivative":finite_difference_square(3),
        "dot_product":dot([1,2,3],[4,5,6]),
        "ols_intercept":b[0],
        "ols_slope":b[1],
        "fitted_values":predicted,
        "half_mean_squared_error":half_mean_squared_error(x,y,b),
        "starting_gradient":gradient,
        "numeric_gradient":numeric_gradient(x,y,[0,0]),
        "gradient_descent":gd,
        "logistic_zero":logistic(0),
        "logistic_derivative_zero":logistic_derivative(0),
        "trapezoidal_area":trapezoid([0,1,2],[1,3,3]),
    }


if __name__=="__main__":
    print(json.dumps(fixtures(),sort_keys=True,indent=2))
