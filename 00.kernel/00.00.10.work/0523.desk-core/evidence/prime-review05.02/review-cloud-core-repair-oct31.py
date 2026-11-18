from pathlib import Path
import sys,os,subprocess,json,hashlib
R=Path(r'D:\Git\lib-build');commit='eeefbeced8587991e4b4a80ce6620ea78a90c1e3';base='5e0040e1598db3b9d9b6584e4d0b19a629356ad1'
O=Path(r'D:\librarian\temp\cloud-core-repair-review');O.mkdir(exist_ok=False);S=O/'source';S.mkdir();(O/'scratch').mkdir()
def git(*a):return subprocess.check_output(['git','-C',str(R),*a])
prefix='00.kernel/00.00.10.work/0523.desk-core'
files=git('ls-tree','-r','--name-only',commit,'app/desk_core',prefix).decode().splitlines()
for rel in files:
    suffix=rel[len(prefix)+1:] if rel.startswith(prefix+'/') else ''
    if suffix.startswith('evidence/prime-review') or suffix.startswith('evidence/build05.01'):continue
    p=S/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(git('cat-file','blob',commit+':'+rel))
P=S/prefix;checks={'commit':commit,'parent_review':base}
pins=json.loads((P/'evidence/pack05.01/source-manifest.json').read_text(encoding='utf-8'))['sources']
for row in pins:
    b=git('cat-file','blob',commit+':'+row['path']);p=S/row['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
checks['source_pins']=len(pins)
repairpins=json.loads((P/'evidence/pack05.02/source-manifest.json').read_text(encoding='utf-8'))['sources']
for row in repairpins:
    b=(P/'evidence/pack05.02'/row['snapshot']).read_bytes()
    assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
checks['repair_input_snapshots']=len(repairpins)
rows=json.loads((P/'evidence/build05.02/artifact-manifest.json').read_text(encoding='utf-8'))['artifacts'];checks['artifacts']=[]
for row in rows:
    b=(S/row['path']).read_bytes();same=len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    checks['artifacts'].append({'path':row['path'],'matches':same});assert same,row['path']
changed=git('diff','--name-only',base,commit).decode().splitlines();checks['changed_files']=changed
checks['scope_ok']=all(x.startswith('app/desk_core/') or x in (prefix+'/05.02.md',prefix+'/06.03.md') or x.startswith(prefix+'/evidence/build05.02/') for x in changed)
env=dict(os.environ,TEMP=str(O/'scratch'),TMP=str(O/'scratch'),PYTHONDONTWRITEBYTECODE='1')
for name,args in [('tests',['-m','unittest','app.desk_core.test_loop','app.desk_core.test_repair','-v']),
                  ('demo',['-m','app.desk_core.demo','--transcript',str(O/'independent-demo.txt')])]:
    q=subprocess.run([sys.executable,'-B',*args],cwd=S,env=env,capture_output=True)
    (O/(name+'.stdout')).write_bytes(q.stdout);(O/(name+'.stderr')).write_bytes(q.stderr)
    checks[name]={'exit':q.returncode};print(name,q.returncode,flush=True)
(O/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8',newline='\n')
print('pins',checks['source_pins'],'repair inputs',len(repairpins),'artifacts',len(rows),'scope_ok',checks['scope_ok'])
