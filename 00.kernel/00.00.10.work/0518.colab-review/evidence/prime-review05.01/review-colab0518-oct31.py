from pathlib import Path
import hashlib, json, subprocess, sys, os, importlib.util
R=Path(r'D:\Git\lib-build')
P=R/'00.kernel/00.00.10.work/0518.colab-review'
O=Path(r'D:\librarian\temp\review0518-results' + ('-elevated' if '--elevated' in sys.argv else ''))
O.mkdir(exist_ok=True)
T=O/'scratch'
T.mkdir(exist_ok=True)
env=dict(os.environ,TEMP=str(T),TMP=str(T),PYTHONDONTWRITEBYTECODE='1')
checks={}
for name,path,key in [('artifacts',P/'evidence/build05.01/artifact-manifest.json','artifacts'),('sources',P/'evidence/pack05.01/source-manifest.json','sources')]:
    rows=json.loads(path.read_text(encoding='utf-8'))[key]
    results=[]
    for row in rows:
        f=R/row['path']; b=f.read_bytes()
        rec={'path':row['path'],'matches':len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']}
        if 'snapshot' in row:
            rec['snapshot_matches']=(path.parent/row['snapshot']).read_bytes()==b
        results.append(rec)
    checks[name]=results
def run(name,args):
    p=subprocess.run([sys.executable,'-B',*args],capture_output=True,env=env,cwd=R)
    (O/(name+'.stdout')).write_bytes(p.stdout);(O/(name+'.stderr')).write_bytes(p.stderr)
    checks[name]={'exit':p.returncode,'stdout':name+'.stdout','stderr':name+'.stderr'}
    (O/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
    print(name,p.returncode,flush=True)
run('capture-verify',[str(R/'labs/return-capture-pass01/return_capture.py'),'verify','--book',str(R/'00.kernel/00.00.10.work'),'--member','0179.colab-review-integration-0501'])
run('tests',['-X','dev',str(R/'labs/colab-review-pass01/tests/test_colab_review.py'),'-v'])
print('Artifact matches',sum(x['matches'] for x in checks['artifacts']),'/',len(checks['artifacts']))
print('Source matches',sum(x['matches'] and x['snapshot_matches'] for x in checks['sources']),'/',len(checks['sources']))
