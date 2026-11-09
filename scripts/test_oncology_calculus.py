"""Numerical and boundary-condition checks for CO-06's synthetic calculus lab."""
import importlib.util
import math
from pathlib import Path
import unittest

PATH=Path(__file__).resolve().parents[1]/"oncology/examples/oncology_calculus.py"
SPEC=importlib.util.spec_from_file_location("oncology_calculus",PATH)
lab=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(lab)


class CalculusChecks(unittest.TestCase):
    def test_expected_hand_calculations(self):
        r=lab.fixtures()
        expected={"average_slope":2,"analytic_derivative":6,"finite_derivative":6,
                  "dot_product":32,"ols_intercept":1.1,"ols_slope":1.1,
                  "half_mean_squared_error":0.0875,
                  "logistic_zero":0.5,"logistic_derivative_zero":0.25,
                  "trapezoidal_area":5}
        for key,value in expected.items():
            with self.subTest(metric=key):
                self.assertAlmostEqual(r[key],value,places=7)
        for got,expected_value in zip(r["fitted_values"],[1.1,2.2,3.3,4.4]):
            self.assertAlmostEqual(got,expected_value,places=9)
        for got,expected_value in zip(r["starting_gradient"],[-2.75,-5.5]):
            self.assertAlmostEqual(got,expected_value,places=9)

    def test_analytic_and_numeric_gradients_match(self):
        x,y=[0,1,2,3],[1,2,4,4]
        for beta in ([0,0],[1,1],[1.1,1.1]):
            analytical=lab.mse_gradient(x,y,beta)
            numerical=lab.numeric_gradient(x,y,beta)
            for a,n in zip(analytical,numerical):
                self.assertAlmostEqual(a,n,places=6)

    def test_gradient_descent_and_closed_form_agree(self):
        x,y=[0,1,2,3],[1,2,4,4]
        expected=lab.ols_line(x,y)
        converged=lab.gradient_descent(x,y)
        for a,b in zip(expected,converged):
            self.assertAlmostEqual(a,b,places=6)
        self.assertLessEqual(
            lab.half_mean_squared_error(x,y,converged),
            lab.half_mean_squared_error(x,y,[0,0])
        )

    def test_numeric_stability_and_dimensions(self):
        self.assertAlmostEqual(lab.dot([1,2,3],[4,5,6]),32)
        self.assertEqual(lab.matrix_vector([[1,0],[1,1]],[1.1,1.1]),[1.1,2.2])
        self.assertEqual(lab.logistic(1000),1.0)
        self.assertEqual(lab.logistic(-1000),0.0)
        self.assertEqual(lab.trapezoid([0,1,2],[1,3,3]),5)

    def test_failure_cases(self):
        bad=[
            (lab.average_slope,(1,2,1,5),{}),
            (lab.average_slope,(2,2,1,5),{}),
            (lab.finite_difference_square,(3,-1e-5),{}),
            (lab.dot,([1,2],[3]),{}),
            (lab.dot,([True,2],[3,4]),{}),
            (lab.matrix_vector,([[1,2]],[1]),{}),
            (lab.matrix_vector,([[1,2],[1]],[1,2]),{}),
            (lab.ols_line,([1,1,1],[1,2,3]),{}),
            (lab.ols_line,([0,1],[1,2]),{}),
            (lab.ols_line,([0,1,2],[1,math.nan,3]),{}),
            (lab.half_mean_squared_error,([0,1],[1,2],[1,2,3]),{}),
            (lab.mse_gradient,([0,1],[1,2],[1]),{}),
            (lab.numeric_gradient,([0,1],[1,2],[0,0]),{"h":0}),
            (lab.gradient_descent,([0,1,2],[1,2,3]),{"step":0.25}),
            (lab.gradient_descent,([0,1,2],[1,2,3]),{"iterations":True}),
            (lab.logistic,(math.inf,),{}),
            (lab.trapezoid,([0,1,1],[1,3,3]),{}),
            (lab.trapezoid,([0,1],[3]),{})
        ]
        for function,args,kwargs in bad:
            with self.subTest(function=function.__name__,args=args):
                with self.assertRaises(ValueError):
                    function(*args,**kwargs)


if __name__=="__main__":
    unittest.main()
