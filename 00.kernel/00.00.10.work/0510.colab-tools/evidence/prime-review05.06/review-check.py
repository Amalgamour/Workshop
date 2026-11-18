from pathlib import Path
import json,hashlib,subprocess,sys,copy

ROOT=Path(r'D:\Git\lib-build')
PAGE=ROOT/'00.kernel/00.00.10.work/0510.colab-tools'
OUT=Path(r'D:\librarian\temp\claude-design06-review-nov01')
OUT.mkdir(exist_ok=False)
results={}
for kind,mp in [('sources',PAGE/'evidence/pack05.06/source-manifest.json'),('artifacts',PAGE/'evidence/design05.06/artifact-manifest.json')]:
 rows=json.loads(mp.read_text(encoding='utf-8-sig'))['files'];bad=[]
 for row in rows:
  for key in (['path','snapshot'] if kind=='sources' else ['path']):
   p=ROOT/row[key]
   if not p.is_file():bad.append([row[key],'missing']);continue
   b=p.read_bytes()
   if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:bad.append([row[key],'mismatch'])
 results[kind]={'rows':len(rows),'bad':bad}
LAB=ROOT/'colab/labs/0510-reserved-review/pass02'
p=subprocess.run([sys.executable,'-B',str(LAB/'test_rules2.py')],cwd=ROOT,capture_output=True)
(OUT/'tests.stdout').write_bytes(p.stdout);(OUT/'tests.stderr').write_bytes(p.stderr)
results['tests']={'exit':p.returncode,'stderr_tail':p.stderr.decode('utf-8','replace').splitlines()[-5:]}
sys.path.insert(0,str(LAB))
import examples as X
import reserved_rules2 as Q
s=X.build()
def stage(d,t):
 try:
  result=Q.stage(X.dump(d),s['d1_raw'],t,s['record']['transitions'],s['first_return'])
  return {'result':result['result']}
 except Exception as exc:return {'error':type(exc).__name__,'detail':str(exc)}
results['baseline']=stage(s['d2'],s['t2'])
d=copy.deepcopy(s['d2']);d['first_return']['return_bytes']+=1
results['wrong_descriptor_return_length']=stage(d,s['t2'])
t=copy.deepcopy(s['t2'])
for row in t['source_map']:
 if row['role']=='target':row['sha256']='ff'*32
results['changed_actual_target_map']=stage(s['d2'],t)
raw=b'```reserved-findings\n{"schema":"not-findings","stage":"wrong"}\n```\n'
# The public stage routine parses the block but does not yet validate the findings schema.
# Use separate synthetic data consistent with that return to avoid unrelated hash failures.
s2=X.build();d2=copy.deepcopy(s2['d2']);t2=copy.deepcopy(s2['t2']);chain=copy.deepcopy(s2['record']['transitions'])
oldhash=d2['first_return']['return_sha256'];newhash=hashlib.sha256(raw).hexdigest()
for row in t2['source_map']:
 if row['sha256']==oldhash:row['sha256']=newhash;row['bytes']=len(raw)
prev=None
for row in chain:
 if row['action']=='seal-return':row['return_sha256']=newhash;row['return_bytes']=len(raw)
 row['prev']=prev;row['sha256']=Q.sha(Q.canonical({k:v for k,v in row.items() if k!='sha256'}));prev=row['sha256']
seal=next(row for row in chain if row['action']=='seal-return')
d2['first_return'].update(return_sha256=newhash,return_bytes=len(raw),seal_transition_sha256=seal['sha256'])
try:results['invalid_findings_schema']={'result':Q.stage(X.dump(d2),s2['d1_raw'],t2,chain,raw)['result']}
except Exception as exc:results['invalid_findings_schema']={'error':type(exc).__name__,'detail':str(exc)}
(OUT/'checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
