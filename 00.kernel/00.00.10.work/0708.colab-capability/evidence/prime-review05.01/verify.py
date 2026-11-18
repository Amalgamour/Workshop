from pathlib import Path
import json,hashlib
R=Path(r'D:\Git\lib-build'); W=R/'00.kernel/00.00.10.work/0708.colab-capability'; E=W/'evidence/build05.01'
result={}
for name,mp in [('sources',W/'evidence/pack05.01/source-manifest.json'),('artifacts',E/'artifact-manifest.json')]:
 rows=json.loads(mp.read_text(encoding='utf-8-sig'))['files']; bad=[]
 for row in rows:
  for field in ['path','snapshot'] if name=='sources' else ['path']:
   p=R/row[field]
   if not p.is_file(): bad.append([field,row[field],'missing']); continue
   b=p.read_bytes()
   if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:bad.append([field,row[field],'mismatch'])
 result[name]={'rows':len(rows),'bytes':sum(x['bytes'] for x in rows),'bad':bad}
result['compact_sha256']=hashlib.sha256(Path(r'D:\librarian\temp\prime-overhead-0708\compact-first.md').read_bytes()).hexdigest()
result['raw_exits']={p.stem:p.read_text().strip() for p in (E/'run').glob('*.exit')}
Path(r'D:\librarian\temp\prime-overhead-0708\integrity.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
for n in ['direct-review.json','out-listing.json']:
 d=json.loads((E/'fixtures'/n).read_text())
 if n=='out-listing.json': d={k:v for k,v in d.items() if k!='files'}
 print(n,json.dumps(d))
for n in ['verify','handoff-check','handoff-tamper','workflow-show','workflow-review','workflow-open-exposure','preview-trigger','preview-overlap']:
 p=E/'run'/f'{n}.stdout'
 print(n,p.read_text()[:4500] if p.exists() else 'missing')
