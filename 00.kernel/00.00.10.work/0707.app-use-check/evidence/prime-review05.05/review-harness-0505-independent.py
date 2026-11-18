import os,sys,json,hashlib,importlib.util,unittest,io
from pathlib import Path
root=Path(r'D:\Git\lib-build');page=root/'00.kernel/00.00.10.work/0707.app-use-check'
out=Path(r'D:\librarian\temp\harness-pass05-review-nov01');out.mkdir(exist_ok=False)
results=[]
for label,path in [('sources',page/'evidence/pack05.05/source-manifest.json'),('artifacts',page/'evidence/lab05.05/artifact-manifest.json')]:
    rows=json.loads(path.read_text(encoding='utf-8'))['files'];bad=[]
    for row in rows:
        b=(root/row['path']).read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:bad.append(row['path'])
    results.append({'manifest':label,'rows':len(rows),'mismatches':bad})
(out/'integrity.json').write_text(json.dumps(results,indent=2));print(json.dumps(results),flush=True)
assert not any(x['mismatches'] for x in results)
spec=importlib.util.spec_from_file_location('independent_harness_tests',root/'colab/labs/0707.app-use-check/pass05/selftest5.py')
mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
mod.OUT=page/'evidence/lab05.06/prime-independent-selftest';mod.RUNS=mod.OUT/'runs';mod.SCRATCH=out/'scratch'
orig=mod.real_cfg
def native_cfg():
    cfg=orig();cfg['interpreter']={'path':sys.executable,'version':'.'.join(map(str,sys.version_info[:3]))};return cfg
mod.real_cfg=native_cfg
code=mod.main()
summary=json.loads((mod.OUT/'summary.json').read_text());(out/'result.json').write_text(json.dumps(summary,indent=2));(out/'suite.log').write_bytes((mod.OUT/'selftest.log').read_bytes())
print(json.dumps(summary),flush=True)
sys.exit(code)
