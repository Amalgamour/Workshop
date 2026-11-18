from pathlib import Path
import sys,json,hashlib,subprocess,os
R=Path(r'D:\Git\lib-build');P=R/'00.kernel/00.00.10.work/0518.colab-review'
O=Path(r'D:\librarian\temp\review0518-repair');O.mkdir(exist_ok=False);(O/'scratch').mkdir()
env=dict(os.environ,TEMP=str(O/'scratch'),TMP=str(O/'scratch'),PYTHONDONTWRITEBYTECODE='1')
rows=json.loads((P/'evidence/build05.02/artifact-manifest.json').read_text(encoding='utf-8'))['artifacts']
checks={'artifacts':[]}
for row in rows:
    b=(R/row['path']).read_bytes()
    checks['artifacts'].append({'path':row['path'],'matches':len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']})
assert all(x['matches'] for x in checks['artifacts'])
# Original pack sources are reused tool/design inputs and must still be unchanged.
pins=json.loads((P/'evidence/pack05.01/source-manifest.json').read_text(encoding='utf-8'))['sources']
checks['reused_source_pins']=[]
for row in pins:
    b=(R/row['path']).read_bytes()
    checks['reused_source_pins'].append({'path':row['path'],'matches':len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']})
assert all(x['matches'] for x in checks['reused_source_pins'])
def run(name,args):
    p=subprocess.run([sys.executable,'-B',*args],cwd=R,env=env,capture_output=True)
    (O/(name+'.stdout')).write_bytes(p.stdout);(O/(name+'.stderr')).write_bytes(p.stderr)
    checks[name]={'exit':p.returncode}
    (O/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
    print(name,p.returncode,flush=True)
for member in ['0179.colab-review-integration-0501','0181.colab-review-repair-0502']:
    run(member,[''+str(R/'labs/return-capture-pass01/return_capture.py'),'verify','--book',str(R/'00.kernel/00.00.10.work'),'--member',member])
run('tests',['-X','dev',str(R/'labs/colab-review-pass01/tests/test_colab_review.py'),'-v'])
print('Artifact rows',len(rows),'reused pins',len(pins))
