from pathlib import Path
import subprocess,sys,json,hashlib,os
R=Path(r'D:\Git\lib-build');O=Path(r'D:\librarian\temp\cloud-core-reliability-review-nov01');O.mkdir(exist_ok=False);S=O/'source';S.mkdir();(O/'scratch').mkdir()
commit='dd4cd00a7c4e75b66e3a0716d564a19e5beca59f';base='42563e669457a46b73f0be8c8caf30d9d16c819d';prefix='00.kernel/00.00.10.work/0523.desk-core'
def git(*a):return subprocess.check_output(['git','-C',str(R),*a])
files=git('ls-tree','-r','--name-only',commit,'--','app/desk_core',prefix).decode().splitlines()
for rel in files:
 suffix=rel[len(prefix)+1:] if rel.startswith(prefix+'/') else ''
 if suffix.startswith('evidence/prime-review') or suffix.startswith('evidence/build05.01') or suffix.startswith('evidence/build05.02'):continue
 p=S/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(git('cat-file','blob',commit+':'+rel))
P=S/prefix;checks={'commit':commit,'base':base,'python':sys.version,'platform':sys.platform}
pins=json.loads((P/'evidence/pack05.03/source-manifest.json').read_text())['sources']
for r in pins:
 b=(P/'evidence/pack05.03'/r['snapshot']).read_bytes();assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256']
checks['pack_pins']=len(pins);rows=json.loads((P/'evidence/build05.03/artifact-manifest.json').read_text())['artifacts'];checks['artifacts']=[]
for r in rows:
 b=(S/r['path']).read_bytes();ok=len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'];checks['artifacts'].append({'path':r['path'],'matches':ok});assert ok,r['path']
changes=git('diff','--name-only',base,commit).decode().splitlines();checks['changed_files']=changes;checks['scope_ok']=all(p.startswith('app/desk_core/') or p in [prefix+'/05.03.md',prefix+'/06.05.md'] or p.startswith(prefix+'/evidence/build05.03/') for p in changes);assert checks['scope_ok']
env=dict(os.environ,TEMP=str(O/'scratch'),TMP=str(O/'scratch'),PYTHONDONTWRITEBYTECODE='1');env.pop('DESK_CORE_FAULT',None)
for name,args in [('tests',['-m','unittest','app.desk_core.test_loop','app.desk_core.test_repair','app.desk_core.test_fault','-v']),('demo',['-m','app.desk_core.demo','--transcript',str(O/'independent-demo.txt')])]:
 p=subprocess.run([sys.executable,'-B','-X','utf8',*args],cwd=S,env=env,capture_output=True);(O/(name+'.stdout')).write_bytes(p.stdout);(O/(name+'.stderr')).write_bytes(p.stderr);checks[name]={'exit':p.returncode};print(name,p.returncode,flush=True)
(O/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8',newline='\n');print('pack pins',len(pins),'artifacts',len(rows),'scope',checks['scope_ok'])
