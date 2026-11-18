from pathlib import Path
import json,hashlib,subprocess,sys,os
root=Path(r'D:\Git\lib-build');page=root/'00.kernel/00.00.10.work/0511.workflow-colab'
out=Path(r'D:\librarian\temp\workflow-pass04-review-nov01');out.mkdir(exist_ok=False)
checks=[]
for name,p in [('sources',page/'evidence/pack05.05/source-manifest.json'),('artifacts',page/'evidence/build05.05/artifact-manifest.json')]:
    rows=json.loads(p.read_text())['files'];bad=[]
    for row in rows:
        b=(root/row['path']).read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:bad.append(row['path'])
    checks.append({'manifest':name,'rows':len(rows),'mismatches':bad})
(out/'integrity.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks),flush=True)
assert not any(x['mismatches'] for x in checks)
results=[]
for name in ['test_pass04.py','test_real_two_pass.py']:
    script=root/'labs/colab-workflow-pass04/tests'/name
    p=subprocess.run([sys.executable,'-B',str(script)],cwd=str(root),capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=180)
    (out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr)
    row={'test':name,'exit':p.returncode,'stdout':p.stdout.decode(errors='replace'),'stderr':p.stderr.decode(errors='replace')};results.append(row);print(json.dumps(row),flush=True)
(out/'result.json').write_text(json.dumps(results,indent=2));sys.exit(0 if all(x['exit']==0 for x in results) else 1)
