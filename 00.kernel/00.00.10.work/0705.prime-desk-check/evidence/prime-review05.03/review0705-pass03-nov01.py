from pathlib import Path
import json,hashlib,subprocess,sys,concurrent.futures
R=Path(r'D:\Git\lib-build');P=R/'00.kernel/00.00.10.work/0705.prime-desk-check';L=R/'colab/labs/0705.prime-desk-check/pass03';O=Path(r'D:\librarian\temp\review0705-pass03-nov01');O.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
pin=P/'evidence/pack05.03';m=json.loads((pin/'source-manifest.json').read_text());pins=[]
for r in m['sources']:
 b=(pin/r['snapshot']).read_bytes();pins.append({'path':r['path'],'snapshot_matches':sha(b)==r['sha256'] and len(b)==r['bytes'],'live_equal':(R/r['path']).read_bytes()==b})
am=P/'evidence/return05.03/artifact-manifest.json';a=json.loads(am.read_text());rows=[]
for r in a.get('artifacts',a.get('files',[])):
 f=R/r['path'];b=f.read_bytes();rows.append({'path':r['path'],'matches':r.get('sha256') is None or sha(b)==r['sha256'] and len(b)==r['bytes']})
ptr=(P/'05.03.pack.md').read_text(encoding='utf-8');ptrs={f.name:sha(f.read_bytes()) in ptr for f in [am,P/'05.03.return.md']}
(O/'checks.json').write_text(json.dumps({'pins':pins,'artifacts':rows,'pointers':ptrs},indent=2),encoding='utf-8');assert all(p['snapshot_matches'] for p in pins);assert all(r['matches'] for r in rows);assert all(ptrs.values())
def run(name,args):
 p=subprocess.run([sys.executable,'-I','-B',*map(str,args)],cwd=R,capture_output=True);(O/(name+'.stdout')).write_bytes(p.stdout);(O/(name+'.stderr')).write_bytes(p.stderr);return {'name':name,'exit':p.returncode}
jobs=[('adapter-tests',[L/'tests/test_adapter.py','--report',O/'adapter-selftest.json']),('baseline',[L/'run_baseline.py','--pack05-03',pin/'source-manifest.json','--pack05-02',P/'evidence/pack05.02/source-manifest.json','--out',O/'baseline'])]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:res=list(pool.map(lambda x:run(*x),jobs))
(O/'runs.json').write_text(json.dumps(res,indent=2),encoding='utf-8');print(json.dumps({'pins':len(pins),'artifacts':len(rows),'pointer_hashes':ptrs,'live_changes':[p['path'] for p in pins if not p['live_equal']],'runs':res},indent=2))
