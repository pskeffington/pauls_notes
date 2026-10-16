"""Analytical/negative fixtures only: never generate the frozen assessment here."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'examples'))
import breast_cancer_rust_training as rt


def fixture():
    return dict(protocol_id='paired-assay-native-rust-v1',feature_names=['a','b'],
        rows=[dict(cohort_row=i,person_id=i//2,specimen_id=f's{i}',label=i%2,
            values=[float(2*(i%2)-1),2.0]) for i in range(8)],
        plans=[dict(name='outer_0',train=[0,1,2,3],assessment=[4,5,6,7])])


class NumericTests(unittest.TestCase):
    def test_known_objective_gradient_and_hessian(self):
        x=np.array([[-1.],[1.]]);y=np.array([0,1]);theta=np.zeros(2)
        self.assertAlmostEqual(rt.objective(theta,x,y),2*np.log(2))
        np.testing.assert_array_equal(rt.gradient(theta,x,y),[-1,0])
        np.testing.assert_array_equal(rt.hessian(theta,x,y),[[1.5,0],[0,.5]])

    def test_finite_difference_derivatives(self):
        x=np.array([[-2.,1.],[0.,1.],[1.,3.]]);y=np.array([0,1,1]);theta=np.array([.2,-.4,.3]);eps=1e-5
        g=rt.gradient(theta,x,y);h=rt.hessian(theta,x,y)
        for j in range(3):
            step=np.eye(3)[j]*eps
            self.assertAlmostEqual(g[j],(rt.objective(theta+step,x,y)-rt.objective(theta-step,x,y))/(2*eps),places=8)
            np.testing.assert_allclose(h[:,j],(rt.gradient(theta+step,x,y)-rt.gradient(theta-step,x,y))/(2*eps),atol=1e-8,rtol=0)

    def test_extreme_logits_stay_finite(self):
        x=np.array([[-1000.],[1000.]]);y=np.array([0,1]);theta=np.array([1.,0.])
        self.assertTrue(np.isfinite(rt.objective(theta,x,y)))
        self.assertTrue(np.isfinite(rt.gradient(theta,x,y)).all())

    def test_python_optimizers_match_and_constant_intercept(self):
        data=fixture();x,y=rt.validate_input(data);plan=data['plans'][0]
        a=rt.fit_python('scipy_newton',x,y,plan);b=rt.fit_python('sklearn_lbfgs',x,y,plan)
        np.testing.assert_allclose(a['probabilities_class_1'],b['probabilities_class_1'],atol=1e-5,rtol=0)
        for row in data['rows']:row['values']=[2.,2.]
        x,y=rt.validate_input(data);m=rt.fit_python('scipy_newton',x,y,plan)
        self.assertEqual(m['coefficients_class_1'],[0.,0.]);self.assertEqual(m['intercept_class_1'],0.)
        self.assertEqual(m['probabilities_class_1'],[.5]*4)

    def test_preparation_is_training_only_and_population_scaled(self):
        data=fixture();data['rows'][0]['values'][0]=None;x,y=rt.validate_input(data);plan=data['plans'][0]
        a=rt.fit_python('scipy_newton',x,y,plan)
        self.assertEqual(a['preparation']['medians'],[1.,2.])
        self.assertEqual(a['preparation']['means'],[.5,2.])
        np.testing.assert_allclose(a['preparation']['scales'],[np.sqrt(.75),1.],atol=1e-15,rtol=0)
        x[4:]=1e5;b=rt.fit_python('scipy_newton',x,y,plan)
        self.assertEqual(a['coefficients_class_1'],b['coefficients_class_1']);self.assertEqual(a['preparation'],b['preparation'])

    def test_all_missing_and_overflow_are_rejected(self):
        data=fixture();x,y=rt.validate_input(data);x[:4,0]=np.nan
        with self.assertRaises(ValueError):rt.prepare(x,[0,1,2,3])
        with self.assertRaises((ValueError,FloatingPointError)):
            rt.transform(np.array([[1e308,1e308]]),dict(medians=[0,0],means=[-1e308,0],scales=[1,1]))

    def test_identity_and_pair_guards(self):
        for change in ('duplicate_id','duplicate_row','broken_pair'):
            data=fixture()
            if change=='duplicate_id':data['rows'][0]['specimen_id']='s1'
            elif change=='duplicate_row':data['rows'][0]['cohort_row']=1
            else:data['rows'][0]['person_id']=99
            with self.subTest(change=change),self.assertRaises(ValueError):rt.validate_input(data)

    def test_labels_values_and_partitions_fail(self):
        cases=[]
        for value in (2,True):
            data=fixture();data['rows'][0]['label']=value;cases.append(data)
        for value in (float('inf'),float('nan'),'3'):
            data=fixture();data['rows'][0]['values'][0]=value;cases.append(data)
        data=fixture();data['plans'][0].update(train=[0,2,3,4],assessment=[1,5,6,7]);cases.append(data)
        data=fixture();data['plans'][0]['train'][0]=1;cases.append(data)
        for data in cases:
            with self.assertRaises(ValueError):rt.validate_input(data)

    def test_saved_parameter_objective_probability_and_identity_corruption(self):
        data=fixture();x,y=rt.validate_input(data);plan=data['plans'][0];good=rt.fit_python('scipy_newton',x,y,plan)
        rt.audit_model(good,x,y,plan)
        for key in ('training_objective','probabilities_class_1','prediction_rows','coefficients_class_1'):
            bad=copy.deepcopy(good)
            if isinstance(bad[key],list):bad[key][0]+=.1
            else:bad[key]+=.1
            with self.subTest(key=key),self.assertRaises(ValueError):rt.audit_model(bad,x,y,plan)

    def test_nonconverged_oracle_fails_residual_gate(self):
        data=fixture();x,y=rt.validate_input(data)
        class Bad:
            x=np.zeros(3);success=False;message='budget';nit=0
        with patch.object(rt,'minimize',return_value=Bad()),self.assertRaises(ValueError):
            rt.fit_python('scipy_newton',x,y,data['plans'][0])


@unittest.skipUnless(os.environ.get('ASSAY_TRAIN_BINARY'),'Set ASSAY_TRAIN_BINARY for native CLI fixtures')
class NativeCliTests(unittest.TestCase):
    def test_fixture_replay_and_overwrite_protection(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);source=root/'input.json';rt.write_json(source,fixture());output=root/'native'
            command=[os.environ['ASSAY_TRAIN_BINARY'],str(source),str(output)]
            subprocess.run(command,check=True,capture_output=True)
            data=fixture();x,y=rt.validate_input(data);model=rt.read_json(output/'model-0.json')
            rt.audit_model(model,x,y,data['plans'][0])
            before=rt.manifest(output);result=subprocess.run(command,capture_output=True)
            self.assertNotEqual(result.returncode,0);self.assertEqual(before,rt.manifest(output))
            replay=root/'replay';subprocess.run([*command[:2],str(replay)],check=True,capture_output=True)
            self.assertEqual(model['probabilities_class_1'],rt.read_json(replay/'model-0.json')['probabilities_class_1'])

    def test_native_malformed_schema_rejected_before_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            for i,mutation in enumerate(('unknown','pair','label','overlap','null_column')):
                data=fixture()
                if mutation=='unknown':data['unexpected']=True
                elif mutation=='pair':data['rows'][0]['person_id']=99
                elif mutation=='label':data['rows'][0]['label']=2
                elif mutation=='overlap':data['plans'][0].update(train=[0,2,3,4],assessment=[1,5,6,7])
                else:
                    for row in data['rows'][:4]:row['values'][0]=None
                source=root/f'{i}.json';rt.write_json(source,data);output=root/f'out{i}'
                result=subprocess.run([os.environ['ASSAY_TRAIN_BINARY'],str(source),str(output)],capture_output=True)
                self.assertNotEqual(result.returncode,0)
                if mutation=='null_column':
                    self.assertTrue(output.exists());self.assertIn('failed',(output/'attempts.jsonl').read_text())
                else:self.assertFalse(output.exists())

if __name__=='__main__':unittest.main()
