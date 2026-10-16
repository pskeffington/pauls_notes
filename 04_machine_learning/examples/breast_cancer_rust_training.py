"""Frozen, development-only native logistic comparison with separate payload audit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import tempfile
import time
import warnings

import numpy as np
from scipy.optimize import minimize
from scipy.special import expit
from sklearn.exceptions import ConvergenceWarning
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold, GroupShuffleSplit
from sklearn.preprocessing import StandardScaler

from breast_cancer_feature_selection import make_cohort, validate_cohort, check_partition, scores

ROOT = Path(__file__).resolve().parents[2]
FREEZE = '1b0d8eda2498136d495ad2a97cf24015d6d34fb1'
PROTOCOL = ROOT/'04_machine_learning/rust-training-protocol.md'
CONTRACT = ROOT/'04_machine_learning/evidence/rust-training-contract-v1.json'
SOURCE_FREEZE = '7b512c0fbccae3a54c5d0089527032c5f0358e78'
ADDENDUM = ROOT/'04_machine_learning/rust-training-source-addendum.md'
LINFA_HASH = 'a242e4224df1294997f527a5670a9624927f692c8cce702b0e4bf3d377592fca'
ENGINES = ('linfa', 'scipy_newton', 'sklearn_lbfgs')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(), parse_constant=lambda v: (_ for _ in ()).throw(ValueError(v)))


def write_json(path, value):
    path = Path(path)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent,
            prefix=path.name, suffix='.tmp', delete=False) as stream:
        temporary = Path(stream.name)
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    temporary.replace(path)


def sources():
    paths = [PROTOCOL, CONTRACT, ADDENDUM, Path(__file__).resolve(),
        ROOT/'04_machine_learning/examples/breast_cancer_feature_selection.py',
        ROOT/'04_machine_learning/requirements-python.txt',
        ROOT/'04_machine_learning/tests/test_breast_cancer_rust_training.py',
        ROOT/'.github/workflows/native-rust-training.yml']
    paths += list((ROOT/'04_machine_learning/rust').glob('Cargo.*'))
    paths += [ROOT/'04_machine_learning/rust/rust-toolchain.toml', ROOT/'04_machine_learning/rust/build.rs']
    paths += sorted((ROOT/'04_machine_learning/rust/src').rglob('*.rs'))
    return {str(p.relative_to(ROOT)): digest(p) for p in sorted(paths)}


def freeze_check():
    for path, commit in ((PROTOCOL,FREEZE),(CONTRACT,FREEZE),(ADDENDUM,SOURCE_FREEZE)):
        original = subprocess.check_output(['git','show',f'{commit}:{path.relative_to(ROOT)}'], cwd=ROOT)
        if path.read_bytes() != original:
            raise ValueError('Frozen protocol/contract bytes changed')
    subprocess.run(['git','merge-base','--is-ancestor',SOURCE_FREEZE,'HEAD'],cwd=ROOT,check=True)
    source_hashes = sources()
    status = subprocess.check_output(['git','status','--porcelain','--',*source_hashes],cwd=ROOT,text=True)
    if status.strip():
        raise ValueError('Commit computational sources before assessment')
    if any(os.environ.get(v) != '1' for v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS')):
        raise ValueError('Set OMP_NUM_THREADS=1 and OPENBLAS_NUM_THREADS=1')
    if os.environ.get('RUSTFLAGS') or os.environ.get('CARGO_ENCODED_RUSTFLAGS'):
        raise ValueError('Use the declared default Rust compilation flags')
    expected = dict(line.strip().split('==') for line in (ROOT/'04_machine_learning/requirements-python.txt').read_text().splitlines()
                    if line.strip() and not line.startswith('#'))
    versions = {name: importlib.metadata.version(name) for name in expected}
    if versions != expected:
        raise ValueError('Pinned Python versions required')
    cargo = Path(os.environ.get('CARGO_HOME', str(Path.home()/'.cargo')))
    installed = list(cargo.glob('registry/src/*/linfa-logistic-0.8.1/src/lib.rs'))
    if len(installed) != 1 or digest(installed[0]) != LINFA_HASH:
        raise ValueError('Installed linfa-logistic source differs from reviewed bytes')
    return dict(commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
                freeze_commit=FREEZE, source_addendum_commit=SOURCE_FREEZE, source_sha256=source_hashes, versions=versions,
                linfa_source_sha256=digest(installed[0]))


def make_inputs():
    c = read_json(CONTRACT)
    data = make_cohort(people=c['people'], seed=c['cohort_seed']); validate_cohort(data)
    development, reserved = next(GroupShuffleSplit(n_splits=1,test_size=.25,
        random_state=c['split_seed']).split(data['x'],data['y'],data['person_id']))
    check_partition(development,reserved,data['person_id'])
    groups, y = data['person_id'][development], data['y'][development]
    plans = [dict(name=f'outer_{k}',train=a.tolist(),assessment=b.tolist())
        for k,(a,b) in enumerate(GroupKFold(c['outer_folds']).split(data['x'][development],y,groups))]
    plans.append(dict(name='final_development',train=list(range(len(development))),assessment=[]))
    rows=[]
    for i in development:
        rows.append(dict(cohort_row=int(i),person_id=int(data['person_id'][i]),specimen_id=str(data['specimen_id'][i]),
                         label=int(data['y'][i]),values=[None if np.isnan(v) else float(v) for v in data['x'][i]]))
    input_data=dict(protocol_id=c['protocol_id'],feature_names=data['feature_names'].tolist(),rows=rows,plans=plans)
    membership=dict(development_rows=development.tolist(),reserved_rows=reserved.tolist(),
        development_people=np.unique(groups).tolist(),reserved_people=np.unique(data['person_id'][reserved]).tolist(),
        cohort_seed=c['cohort_seed'],split_seed=c['split_seed'],reserved_predictions=0)
    if len(membership['development_people']) != c['development_people'] or len(membership['reserved_people']) != c['reserved_people']:
        raise ValueError('Wrong person denominator')
    return input_data,membership


def validate_input(data):
    if set(data) != {'protocol_id','feature_names','rows','plans'} or data['protocol_id'] != 'paired-assay-native-rust-v1':
        raise ValueError('Invalid input schema')
    rows=data['rows']; n=len(rows); p=len(data['feature_names'])
    if n<4 or not p or len(set(data['feature_names']))!=p or not data['plans']:
        raise ValueError('Missing rows/features/plans')
    for s in [*data['feature_names'],*[r['specimen_id'] for r in rows]]:
        if not isinstance(s,str) or not s or s.strip()!=s or any(ord(ch)<32 for ch in s):
            raise ValueError('Invalid identity string')
    if len({r['specimen_id'] for r in rows})!=n or len({r['cohort_row'] for r in rows})!=n:
        raise ValueError('Duplicate identity')
    for r in rows:
        if set(r) != {'cohort_row','person_id','specimen_id','label','values'} or any(type(r[k]) is not int or r[k]<0 for k in ('cohort_row','person_id','label')):
            raise ValueError('Invalid row fields')
        if r['label'] not in (0,1) or len(r['values'])!=p or any(v is not None and (type(v) not in (int,float) or not np.isfinite(v)) for v in r['values']):
            raise ValueError('Invalid label or measurement')
    groups=np.array([r['person_id'] for r in rows]);y=np.array([r['label'] for r in rows])
    for person in np.unique(groups):
        if sorted(y[groups==person]) != [0,1]:
            raise ValueError('Malformed paired person')
    if len({p['name'] for p in data['plans']}) != len(data['plans']):
        raise ValueError('Duplicate plan')
    for plan in data['plans']:
        a,b=plan['train'],plan['assessment']
        if not a or any(type(i) is not int or i<0 or i>=n for i in a+b) or len(a+b)!=n or sorted(a+b)!=list(range(n)):
            raise ValueError('Invalid plan partition')
        if b:
            check_partition(np.array(a),np.array(b),groups)
        elif plan['name']!='final_development':
            raise ValueError('Empty assessment is final-development only')
        if plan['name']=='final_development' and b:
            raise ValueError('Final development must not score assessment')
    return np.array([[np.nan if v is None else v for v in r['values']] for r in rows],dtype=np.float64),y


def prepare(raw, indices):
    train=raw[indices]
    if np.all(np.isnan(train),axis=0).any():
        raise ValueError('All-missing training column')
    imputer=SimpleImputer(strategy='median');imputed=imputer.fit_transform(train)
    scaler=StandardScaler().fit(imputed)
    # The contract assigns scale=1 only to exactly constant columns.
    scaler.scale_=np.where(scaler.var_==0,1.0,np.sqrt(scaler.var_))
    x=scaler.transform(imputed)
    if not np.isfinite(x).all():
        raise ValueError('Nonfinite standardized training data')
    return x,dict(medians=imputer.statistics_.tolist(),means=scaler.mean_.tolist(),scales=scaler.scale_.tolist())


def transform(raw, prep):
    filled=np.where(np.isnan(raw),np.asarray(prep['medians']),raw)
    with np.errstate(over='raise',invalid='raise',divide='raise'):
        x=(filled-np.asarray(prep['means']))/np.asarray(prep['scales'])
    if not np.isfinite(x).all(): raise ValueError('Nonfinite transformed data')
    return x


def objective(theta,x,y):
    w,b=theta[:-1],theta[-1];z=x@w+b
    signed=(2*y-1)*z
    return float(np.logaddexp(0,-signed).sum()+.5*(w@w))


def gradient(theta,x,y):
    residual=expit(x@theta[:-1]+theta[-1])-y
    return np.r_[x.T@residual+theta[:-1],residual.sum()]


def hessian(theta,x,y):
    probability=expit(x@theta[:-1]+theta[-1]); design=np.column_stack([x,np.ones(len(x))])
    penalty=np.eye(design.shape[1]);penalty[-1,-1]=0
    return design.T@((probability*(1-probability))[:,None]*design)+penalty


def fit_python(engine,raw,y,plan):
    start=time.perf_counter(); indices=plan['train'];x,prep=prepare(raw,indices);target=y[indices]
    if engine=='scipy_newton':
        result=minimize(objective,np.zeros(x.shape[1]+1),args=(x,target),jac=gradient,hess=hessian,
            method='trust-exact',options=dict(gtol=1e-10,maxiter=1000))
        theta=result.x;diagnostics=dict(success=bool(result.success),message=str(result.message),iterations=int(result.nit))
    elif engine=='sklearn_lbfgs':
        model=LogisticRegression(C=1,solver='lbfgs',max_iter=5000,tol=1e-10)
        with warnings.catch_warnings():
            warnings.simplefilter('error',ConvergenceWarning);model.fit(x,target)
        if model.classes_.tolist()!=[0,1]:raise ValueError('Wrong sklearn class direction')
        theta=np.r_[model.coef_[0],model.intercept_[0]]
        diagnostics=dict(success=True,iterations=int(model.n_iter_[0]),message='no ConvergenceWarning')
    else:raise ValueError('Unknown optimizer')
    g=gradient(theta,x,target);value=objective(theta,x,target)
    if not np.isfinite(theta).all() or not np.isfinite(value) or not np.isfinite(g).all() or np.max(np.abs(g))>1e-6:
        raise ValueError(f'{engine}: optimizer residual failed: {np.max(np.abs(g))}')
    prediction_rows=plan['assessment'] or indices
    prediction=expit(transform(raw[prediction_rows],prep)@theta[:-1]+theta[-1])
    return dict(plan=plan,preparation=prep,coefficients_class_1=theta[:-1].tolist(),intercept_class_1=float(theta[-1]),
        training_objective=value,training_gradient=g.tolist(),gradient_inf=float(np.max(np.abs(g))),
        prevalence=float(target.mean()),prediction_rows=prediction_rows,probabilities_class_1=prediction.tolist(),
        elapsed_seconds=time.perf_counter()-start,diagnostics=diagnostics)


def near(a,b,tolerance,label):
    a,b=np.asarray(a),np.asarray(b)
    if a.shape!=b.shape or not np.isfinite(a).all() or not np.isfinite(b).all() or np.max(np.abs(a-b),initial=0)>tolerance:
        raise ValueError(f'{label} mismatch')
    return float(np.max(np.abs(a-b),initial=0))


def audit_model(model,raw,y,plan):
    if model['plan']!=plan or model['prediction_rows']!=(plan['assessment'] or plan['train']):
        raise ValueError('Model partition/row identity mismatch')
    x,expected=prepare(raw,plan['train']);prep=model['preparation']
    preprocessing=max(near(prep[k],expected[k],1e-12,f'preprocessing {k}') for k in expected)
    theta=np.r_[model['coefficients_class_1'],model['intercept_class_1']]
    if theta.shape!=(raw.shape[1]+1,) or not np.isfinite(theta).all():raise ValueError('Invalid model parameters')
    # Recalculate with the Rust-saved preparation, including its rounding.
    x=transform(raw[plan['train']],prep);target=y[plan['train']]
    value=objective(theta,x,target);g=gradient(theta,x,target)
    near(value,model['training_objective'],1e-10,'objective recalculation')
    near(g,model['training_gradient'],1e-10,'gradient recalculation')
    near(np.max(np.abs(g)),model['gradient_inf'],1e-10,'gradient norm')
    if np.max(np.abs(g))>1e-6:raise ValueError('Residual acceptance failed')
    near(target.mean(),model['prevalence'],0,'training prevalence')
    prediction=expit(transform(raw[model['prediction_rows']],prep)@theta[:-1]+theta[-1])
    near(prediction,model['probabilities_class_1'],1e-12,'saved probability')
    if any(v<0 or v>1 for v in model['probabilities_class_1']):raise ValueError('Invalid probability')
    return preprocessing


def audit_payload(output):
    output=Path(output);data=read_json(output/'development.json');membership=read_json(output/'membership.json')
    expected,expected_membership=make_inputs()
    if data!=expected or membership!=expected_membership:raise ValueError('Frozen generated input/membership mismatch')
    raw,y=validate_input(data)
    native=read_json(output/'rust/run.json')
    if native['models']!=4 or native['input_sha256']!=digest(output/'development.json') or native['compiler']!='rustc 1.90.0 (1159e78c4 2025-09-14)':
        raise ValueError('Wrong native run provenance')
    if native['build_profile']!='release' or native['opt_level']!='3' or native['rustflags']!='':
        raise ValueError('Wrong native compilation profile')
    attempts=[json.loads(v) for v in (output/'attempts.jsonl').read_text().splitlines()]
    wanted=[(e,p['name'],s) for e in ('scipy_newton','sklearn_lbfgs') for p in data['plans'] for s in ('started','complete')]
    if [(v['engine'],v['plan'],v['status']) for v in attempts]!=wanted:raise ValueError('Python attempts do not reconcile')
    attempts=[json.loads(v) for v in (output/'rust/attempts.jsonl').read_text().splitlines()]
    if [(v['plan'],v['status']) for v in attempts]!=[(p['name'],s) for p in data['plans'] for s in ('started','complete')]:
        raise ValueError('Rust attempts do not reconcile')
    comparisons=[];oof={e:np.full(len(y),np.nan) for e in (*ENGINES,'training_prevalence')};coverage=np.zeros(len(y),int)
    prediction_records=[]
    for k,plan in enumerate(data['plans']):
        models={e:read_json(output/('rust' if e=='linfa' else e)/f'model-{k}.json') for e in ENGINES}
        prep_errors={e:audit_model(m,raw,y,plan) for e,m in models.items()}
        reference=models['scipy_newton'];cell=dict(plan=plan['name'],training_people=len(plan['train'])//2,
            assessment_people=len(plan['assessment'])//2,models={},preprocessing_error=prep_errors)
        for engine,model in models.items():
            p_error=near(model['probabilities_class_1'],reference['probabilities_class_1'],1e-5,'oracle probability')
            j_error=near(model['training_objective'],reference['training_objective'],1e-8,'oracle objective')
            if engine=='linfa' and (model['linfa_positive_class'] not in (0,1) or model['max_library_probability_difference']>1e-12 or
                model['library_iterations'] is not None or model['library_termination_reason'] is not None):
                raise ValueError('Invalid native class/diagnostic evidence')
            cell['models'][engine]=dict(max_probability_error=p_error,objective_error=j_error,gradient_inf=model['gradient_inf'],
                objective=model['training_objective'],coefficient_max_difference=float(np.max(np.abs(np.array(model['coefficients_class_1'])-reference['coefficients_class_1']))))
            if plan['assessment']:oof[engine][plan['assessment']]=model['probabilities_class_1']
        if plan['assessment']:
            coverage[plan['assessment']]+=1;oof['training_prevalence'][plan['assessment']]=models['linfa']['prevalence']
        comparisons.append(cell)
    if not np.all(coverage==1) or any(not np.isfinite(v).all() for v in oof.values()):raise ValueError('Incomplete held-out coverage')
    for i,row in enumerate(data['rows']):
        prediction_records.append(dict(cohort_row=row['cohort_row'],person_id=row['person_id'],specimen_id=row['specimen_id'],label=row['label'],
            **{f'{e}_probability':float(p[i]) for e,p in oof.items()}))
    # Exact records bind probabilities to specimen and person identities, not just row count.
    prediction_path=output/'predictions.json'
    if prediction_path.exists() and read_json(prediction_path)!=prediction_records:raise ValueError('Prediction record identity/value mismatch')
    metrics={e:scores(y,p) for e,p in oof.items()}
    groups=np.array([r['person_id'] for r in data['rows']])
    for engine,p in oof.items():
        metrics[engine]['person_mean_brier']=float(np.mean([np.mean((p[groups==g]-y[groups==g])**2) for g in np.unique(groups)]))
    summary=dict(comparisons=comparisons,metrics=metrics,optimizer_fits=12,failed_fits=0,development_people=45,
        development_predictions=90,final_development_probe_predictions_per_engine=90,reserved_predictions=0,
        max_native_probability_error=max(v['models']['linfa']['max_probability_error'] for v in comparisons),
        max_native_gradient_inf=max(v['models']['linfa']['gradient_inf'] for v in comparisons))
    return summary,prediction_records


def manifest(output):
    return {str(p.relative_to(output)):digest(p) for p in sorted(output.rglob('*')) if p.is_file() and str(p.relative_to(output))!='sha256.json'}


def audit(output):
    output=Path(output)
    saved=read_json(output/'sha256.json')
    if any(Path(p).is_absolute() or '..' in Path(p).parts for p in saved) or any(p.is_symlink() for p in output.rglob('*')) or saved!=manifest(output):
        raise ValueError('Artifact manifest mismatch')
    report=read_json(output/'report.json')
    if report['status']!='complete' or report['provenance']['source_sha256']!=sources():raise ValueError('Status/source mismatch')
    for path,commit in ((PROTOCOL,FREEZE),(CONTRACT,FREEZE),(ADDENDUM,SOURCE_FREEZE)):
        frozen=subprocess.check_output(['git','show',f'{commit}:{path.relative_to(ROOT)}'],cwd=ROOT)
        if path.read_bytes()!=frozen:raise ValueError('Frozen bytes changed')
    for path,expected_hash in report['provenance']['source_sha256'].items():
        committed=subprocess.check_output(['git','show',f"{report['provenance']['commit']}:{path}"],cwd=ROOT)
        if hashlib.sha256(committed).hexdigest()!=expected_hash:raise ValueError('Execution commit source mismatch')
    summary,_=audit_payload(output)
    if summary!=report['numerical']:raise ValueError('Report numerical summary mismatch')
    if digest(output/'binary/assay-train')!=report['binary_sha256']:raise ValueError('Saved binary hash mismatch')
    return summary


def resource_usage(who):
    usage=resource.getrusage(who)
    return dict(user_seconds=usage.ru_utime,system_seconds=usage.ru_stime,max_rss_kib=usage.ru_maxrss)


def run(output,binary):
    provenance=freeze_check();binary=Path(binary).resolve(strict=True)
    output=Path(output).absolute()
    output=output.parent.resolve(strict=True)/output.name
    if output.is_relative_to(ROOT):raise ValueError('Output must be outside repository')
    output.mkdir()  # Exclusive creation preserves existing results and symlinks.
    start=time.perf_counter()
    try:
        data,membership=make_inputs();raw,y=validate_input(data)
        write_json(output/'development.json',data);write_json(output/'membership.json',membership)
        (output/'binary').mkdir();(output/'binary/assay-train').write_bytes(binary.read_bytes())
        (output/'binary/assay-train').chmod(0o755)
        native_start=time.perf_counter()
        with (output/'rust.stdout.txt').open('w') as stdout,(output/'rust.stderr.txt').open('w') as stderr:
            result=subprocess.run([str(binary),str(output/'development.json'),str(output/'rust')],stdout=stdout,stderr=stderr,timeout=240)
        native_seconds=time.perf_counter()-native_start
        if result.returncode:raise ValueError(f'Native subprocess failed with code {result.returncode}; see retained stderr')
        with (output/'attempts.jsonl').open('x') as attempts:
            for engine in ('scipy_newton','sklearn_lbfgs'):
                (output/engine).mkdir()
                for k,plan in enumerate(data['plans']):
                    attempts.write(json.dumps(dict(engine=engine,plan=plan['name'],status='started'))+'\n');attempts.flush();os.fsync(attempts.fileno())
                    try:model=fit_python(engine,raw,y,plan)
                    except Exception as error:
                        attempts.write(json.dumps(dict(engine=engine,plan=plan['name'],status='failed',error=str(error)))+'\n');attempts.flush();raise
                    write_json(output/engine/f'model-{k}.json',model)
                    attempts.write(json.dumps(dict(engine=engine,plan=plan['name'],status='complete'))+'\n');attempts.flush();os.fsync(attempts.fileno())
                    if time.perf_counter()-start>300:raise TimeoutError('Frozen 300 second ceiling exceeded')
        summary,predictions=audit_payload(output);write_json(output/'predictions.json',predictions)
        duration=time.perf_counter()-start
        if duration>300:raise TimeoutError('Frozen 300 second ceiling exceeded')
        cpu=next((s.split(':',1)[1].strip() for s in Path('/proc/cpuinfo').read_text().splitlines() if s.startswith('model name')),'unknown')
        write_json(output/'report.json',dict(protocol_id=data['protocol_id'],status='complete',provenance=provenance,numerical=summary,
            binary_sha256=digest(binary),created_utc=datetime.now(timezone.utc).isoformat(),elapsed_seconds=duration,
            native_subprocess_seconds=native_seconds,python=platform.python_version(),os=platform.platform(),cpu=cpu,
            threads={v:os.environ.get(v) for v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS')},worker_count=1,
            self_usage=resource_usage(resource.RUSAGE_SELF),children_usage=resource_usage(resource.RUSAGE_CHILDREN),
            resource_scope='Linux process high-water RSS and cumulative CPU, including orchestration; no language speed comparison',
            build_profile='release defaults; no target-cpu=native, BLAS, GPU or fast-math requested',
            interpretation='Synthetic numerical/software agreement; no clinical validation, speed or learner-mastery claim'))
        write_json(output/'sha256.json',manifest(output));audit(output)
        return summary
    except BaseException as error:
        write_json(output/'failure.json',dict(error=type(error).__name__,message=str(error),provenance=provenance,
            elapsed_seconds=time.perf_counter()-start))
        write_json(output/'sha256.json',manifest(output));raise


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('output',type=Path)
    parser.add_argument('--binary',type=Path);parser.add_argument('--audit-only',action='store_true');args=parser.parse_args()
    if args.audit_only:result=audit(args.output)
    elif args.binary:result=run(args.output,args.binary)
    else:parser.error('--binary is required for execution')
    print(json.dumps(result,indent=2,allow_nan=False))

if __name__=='__main__':main()
