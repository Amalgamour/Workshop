from pathlib import Path
import subprocess,os,sys,json,hashlib
R=Path(r'D:\Git\lib-build');commit='e94ca6985789c503e3d4f37019042068eef6e8f4';base='17ad02453edde4a2f65f6a0d78686004bf4e5fe1'
O=Path(r'D:\librarian\temp\cloud-core-review');O.mkdir(exist_ok=False);S=O/'source';S.mkdir();(O/'scratch').mkdir()
def git(*a):return subprocess.check_output(['git','-C',str(R),*a])
files=git('ls-tree','-r','--name-only',commit,'app/desk_core','00.kernel/00.00.10.work/0523.desk-core').decode().splitlines()
for rel in files:
    p=S/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(git('cat-file','blob',commit+':'+rel))
P=S/'00.kernel/00.00.10.work/0523.desk-core';checks={'commit':commit,'preparation':base}
pins=json.loads((P/'evidence/pack05.01/source-manifest.json').read_text(encoding='utf-8'))['sources']
for row in pins:
    b=git('cat-file','blob',commit+':'+row['path']);p=S/row['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
checks['source_pins']=len(pins)
manifest=json.loads((P/'evidence/build05.01/artifact-manifest.json').read_text(encoding='utf-8'))
checks['artifact_manifest_keys']=list(manifest)
rows=manifest.get('artifacts',manifest.get('files',[]));checks['artifacts']=[]
for row in rows:
    if not row.get('sha256'):continue
    b=(S/row['path']).read_bytes();same=len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    checks['artifacts'].append({'path':row['path'],'matches':same})
checks['changed_files']=git('diff','--name-only',base,commit).decode().splitlines()
checks['scope_ok']=all(x.startswith('app/desk_core/') or x=='00.kernel/00.00.10.work/0523.desk-core/05.01.md' or x=='00.kernel/00.00.10.work/0523.desk-core/06.01.md' or x.startswith('00.kernel/00.00.10.work/0523.desk-core/evidence/build05.01/') for x in checks['changed_files'])
env=dict(os.environ,TEMP=str(O/'scratch'),TMP=str(O/'scratch'),PYTHONDONTWRITEBYTECODE='1')
for name,args in [('tests',['-m','unittest','app.desk_core.test_loop','-v']),('demo',['-m','app.desk_core.demo','--transcript',str(O/'demo-transcript.txt')])]:
    q=subprocess.run([sys.executable,'-B',*args],cwd=S,env=env,capture_output=True)
    (O/(name+'.stdout')).write_bytes(q.stdout);(O/(name+'.stderr')).write_bytes(q.stderr)
    checks[name]={'exit':q.returncode};print(name,q.returncode,flush=True)
(O/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
print('pins',len(pins),'artifacts',len(checks['artifacts']),'scope_ok',checks['scope_ok'])
