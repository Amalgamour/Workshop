import os, sys, json, hashlib, importlib.util, unittest
from pathlib import Path
root=Path(r'D:\Git\lib-build')
out=Path(r'D:\librarian\temp\loop-pass03-review-nov01')
out.mkdir(exist_ok=False)
page=root/'00.kernel/00.00.10.work/0522.review-construction'
checks=[]
for name,path in [('sources',page/'evidence/pack05.08/source-manifest.json'),('artifacts',page/'evidence/build05.08/artifact-manifest.json')]:
    rows=json.loads(path.read_text(encoding='utf-8'))['files']; bad=[]
    for row in rows:
        p=root/row['path']; data=p.read_bytes()
        if len(data)!=row['bytes'] or hashlib.sha256(data).hexdigest()!=row['sha256']: bad.append(row['path'])
    checks.append({'manifest':name,'rows':len(rows),'mismatches':bad})
(out/'integrity.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
print(json.dumps(checks),flush=True)
if any(x['mismatches'] for x in checks): sys.exit(2)
os.environ['REVIEW_LOOP_RUN']=str(out/'native-run')
os.environ['PYTHONDONTWRITEBYTECODE']='1'
spec=importlib.util.spec_from_file_location('independent_loop_tests',root/'labs/review-loop-pass03/tests/test_review_loop.py')
mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
mod.PY=Path(sys.executable);mod.EVIDENCE=out/'native-run'
with (out/'suite.log').open('w',encoding='utf-8') as stream:
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(mod))
summary={'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'success':result.wasSuccessful(),'python':sys.version}
(out/'result.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary),flush=True)
sys.exit(0 if result.wasSuccessful() else 1)
