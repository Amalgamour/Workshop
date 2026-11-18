import sys,json,hashlib,importlib.util
from pathlib import Path
root=Path(r'D:\Git\lib-build');page=root/'00.kernel/00.00.10.work/0707.app-use-check'
out=Path(r'D:\librarian\temp\harness-pass06-review-nov01');out.mkdir(exist_ok=False)
checks=[]
for label,path in [('sources',page/'evidence/pack05.06/source-manifest.json'),('artifacts',page/'evidence/lab05.07/artifact-manifest.json')]:
    rows=json.loads(path.read_text(encoding='utf-8'))['files'];bad=[]
    for row in rows:
        b=(root/row['path']).read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:bad.append(row['path'])
    checks.append({'manifest':label,'rows':len(rows),'mismatches':bad})
(out/'integrity.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks),flush=True)
assert not any(x['mismatches'] for x in checks)
spec=importlib.util.spec_from_file_location('independent_harness6_tests',root/'colab/labs/0707.app-use-check/pass06/selftest6.py')
mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
mod.OUT=page/'evidence/lab05.08/prime-independent-selftest';mod.RUNS=mod.OUT/'runs';mod.SCRATCH=out/'scratch'
original=mod.cfg_real
def native6():
    cfg=original();cfg['interpreter']={'path':sys.executable,'version':'.'.join(map(str,sys.version_info[:3]))};return cfg
mod.cfg_real=native6
original5=mod.S5.real_cfg
def native5():
    cfg=original5();cfg['interpreter']={'path':sys.executable,'version':'.'.join(map(str,sys.version_info[:3]))};return cfg
mod.S5.real_cfg=native5
code=mod.main();summary=json.loads((mod.OUT/'summary.json').read_text())
(out/'result.json').write_text(json.dumps(summary,indent=2));(out/'suite.log').write_bytes((mod.OUT/'selftest.log').read_bytes())
print(json.dumps(summary),flush=True);sys.exit(code)
