from pathlib import Path
import json,hashlib
root=Path(r'D:\Git\lib-build');page=root/'00.kernel/00.00.10.work/0707.app-use-check';out=Path(r'D:\librarian\temp\supplement-0508-review-nov01');out.mkdir(exist_ok=False)
checks=[]
for name,p in [('sources',page/'evidence/pack05.08/source-manifest.json'),('artifacts',page/'evidence/lab05.10/artifact-manifest.json')]:
    rows=json.loads(p.read_text(encoding='utf-8'))['files'];bad=[]
    for row in rows:
        b=(root/row['path']).read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:bad.append(row['path'])
    checks.append({'manifest':name,'rows':len(rows),'mismatches':bad})
run=page/'evidence/lab05.10/runs/20261101T223407Z-ab42c3';summary=json.loads((run/'summary.json').read_text());bad=[];calls=[]
for p in run.glob('cases/*/calls/*.json'):
    r=json.loads(p.read_text());calls.append(r)
    for ext in ['stdout','stderr']:
        b=p.with_suffix('.'+ext).read_bytes()
        if len(b)!=r[ext+'_bytes'] or hashlib.sha256(b).hexdigest()!=r[ext+'_sha256']:bad.append(str(p))
facts={p.stem:json.loads(p.read_text()) for p in (run/'cases/A22b').glob('facts-*.json')}
assert facts['facts-after-decision']['target_exists'] and not facts['facts-after-target-removed']['target_exists']
assert len({v['decision_sha256'] for v in facts.values()})==1
assert all(v['committed_reviews']==[] for v in facts.values())
for case in ['A22a','A22b']:
    data=json.loads((run/'cases'/case/'checks.json').read_text());assert data['checks'] and all(x['ok'] for x in data['checks'])
old=json.loads((page/'evidence/lab05.09/candidate.config.json').read_text());new=json.loads((page/'evidence/lab05.10/candidate.config.json').read_text())
for k in ['label','output_root','release']:old.pop(k);new.pop(k)
assert old==new
r={'integrity':checks,'cases':summary['cases'],'raw_calls':len(calls),'raw_output_mismatches':bad,'decision_same_at_all_stages':True,'no_committed_reviews':True,'target_removed_at_record':True,'config_changes_only_allowed':True,'new_execution_by_prime':False}
(out/'verification.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps(r))
assert len(calls)==7 and not bad and not any(x['mismatches'] for x in checks)
