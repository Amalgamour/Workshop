from pathlib import Path
import json,hashlib,subprocess,sys,os
R=Path(r'D:\Git\lib-build');P=R/'00.kernel/00.00.10.work/0519.desk-app'
O=Path(r'D:\librarian\temp\review0519-design');O.mkdir(exist_ok=False);(O/'scratch').mkdir()
rows=json.loads((P/'evidence/build05.01/artifact-manifest.json').read_text(encoding='utf-8'))['artifacts']
checks={'artifacts':[]}
for row in rows:
    b=(R/row['path']).read_bytes();same=len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    checks['artifacts'].append({'path':row['path'],'matches':same});assert same,row['path']
env=dict(os.environ,TEMP=str(O/'scratch'),TMP=str(O/'scratch'),PYTHONDONTWRITEBYTECODE='1')
for name,args in [('capture-verify',[str(R/'labs/return-capture-pass01/return_capture.py'),'verify','--book',str(R/'00.kernel/00.00.10.work'),'--member','0182.desk-app-integration-design-0501']),
                  ('demo',[str(R/'labs/desk-app-integration-pass01/demo.py'),'--transcript',str(O/'independent-transcript.json'),'--keep'])]:
    p=subprocess.run([sys.executable,'-B',*args],cwd=R,env=env,capture_output=True)
    (O/(name+'.stdout')).write_bytes(p.stdout);(O/(name+'.stderr')).write_bytes(p.stderr)
    checks[name]={'exit':p.returncode}
    (O/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
    print(name,p.returncode,flush=True)
print('Artifact rows',len(rows))
