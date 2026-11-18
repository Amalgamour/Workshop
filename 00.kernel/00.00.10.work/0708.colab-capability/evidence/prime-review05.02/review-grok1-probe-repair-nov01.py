from pathlib import Path
import json,hashlib
R=Path(r'D:\Git\lib-build');P=R/'00.kernel/00.00.10.work/0708.colab-capability';L=Path(r'D:\librarian\temp\grok1-probe-repair-review-nov01');L.mkdir(exist_ok=False)
out={}
for kind,path in [('sources',P/'evidence/pack05.02/source-manifest.json'),('artifacts',P/'evidence/build05.02/artifact-manifest.json')]:
 rows=json.loads(path.read_text(encoding='utf-8-sig'))['files'];bad=[]
 for row in rows:
  for key in (['path','snapshot'] if kind=='sources' else ['path']):
   p=R/row[key]
   if not p.is_file():bad.append([row[key],'missing']);continue
   b=p.read_bytes()
   if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:bad.append([row[key],'mismatch'])
 out[kind]={'rows':len(rows),'bad':bad}
old=json.loads((P/'evidence/build05.02/preserved-before.json').read_text(encoding='utf-8-sig'));after=json.loads((P/'evidence/build05.02/preserved-after.json').read_text(encoding='utf-8-sig'))
bad=[];n=0
for t in old['trees']:
 for row in t['rows']:
  p=R/t['root']/row['path'];b=p.read_bytes();n+=1
  if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:bad.append(str(p))
out['prior_preservation']={'recorded_before_equals_after':old==after,'rows_rechecked':n,'bad':bad}
out['statuses']={p.parent.name:json.loads(p.read_text())['status'] for p in (P/'evidence/build05.02/slots').glob('*/status.json')}
(L/'integrity.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
