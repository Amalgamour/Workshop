from pathlib import Path
import json,hashlib
root=Path(r'D:\Git\lib-build');page=root/'00.kernel/00.00.10.work/0707.app-use-check';out=Path(r'D:\librarian\temp\candidate-0507-review-nov01');out.mkdir(exist_ok=False)
checks=[]
for name,p in [('sources',page/'evidence/pack05.07/source-manifest.json'),('artifacts',page/'evidence/lab05.09/artifact-manifest.json')]:
    rows=json.loads(p.read_text(encoding='utf-8'))['files'];bad=[]
    for row in rows:
        b=(root/row['path']).read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:bad.append(row['path'])
    checks.append({'manifest':name,'rows':len(rows),'mismatches':bad})
run=page/'evidence/lab05.09/runs/20261101T222554Z-8b736d';summary=json.loads((run/'summary.json').read_text())
counts={}
for row in summary['cases']:counts[row['status']]=counts.get(row['status'],0)+1
bad=[];calls=[]
for p in run.glob('cases/*/calls/*.json'):
    r=json.loads(p.read_text());calls.append(r)
    for ext in ['stdout','stderr']:
        b=p.with_suffix('.'+ext).read_bytes()
        if hashlib.sha256(b).hexdigest()!=r[ext+'_sha256'] or len(b)!=r[ext+'_bytes']:bad.append(str(p)+':'+ext)
template=json.loads((page/'evidence/pack05.07/candidate-template.json').read_text());actual=json.loads((page/'evidence/lab05.09/candidate.config.json').read_text());a=dict(actual);a['release']=template['release'];assert a==template
r={'integrity':checks,'case_counts':counts,'aggregate':summary['aggregate'],'launches':summary['launches'],'raw_call_records':len(calls),'raw_output_mismatches':bad,'timeouts':sum(bool(x['timed_out']) for x in calls),'leftover_descendants':sum(bool(x['leftover_descendants']) for x in calls),'output_incomplete':sum(x['output_status']!='complete' for x in calls),'config_changes_only_release':True}
(out/'verification.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps(r))
assert not any(x['mismatches'] for x in checks) and not bad
