import csv, hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile
P=pathlib.Path
src=P(r'D:\Git\lib-build')
out=P(tempfile.mkdtemp(prefix='prime-workers-20261026-'))
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1','GIT_OPTIONAL_LOCKS':'0'}
def sha(b): return hashlib.sha256(b).hexdigest()
def run(name,args,cwd):
 r=subprocess.run(args,cwd=cwd,env=env,capture_output=True,timeout=160)
 (out/(name+'.stdout.txt')).write_bytes(r.stdout); (out/(name+'.stderr.txt')).write_bytes(r.stderr)
 print(name, 'exit',r.returncode, r.stdout.decode('utf8','replace')[-650:],r.stderr.decode('utf8','replace')[-650:],flush=True)
 return r
print('EVIDENCE',out,flush=True)
ws=out/'workspace';ws.mkdir()
files=subprocess.check_output(['git','ls-files','-z'],cwd=src,env=env).decode().split('\0')
for rel in filter(None,files):
 p=ws/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src/rel,p)
rows=0
for manifest in ['custody.tsv','text-custody.tsv']:
 p=src/'00.kernel/00.00.10.work/0504.app-entry/evidence'/manifest
 for row in csv.DictReader(p.open(encoding='utf8'),delimiter='\t'):
  b=subprocess.check_output(['git','show','70741312cb09c6413f9ea1b79902e050d884cce7:'+row['path']],cwd=src,env=env)
  assert sha(b)==row['sha256'] and len(b)==int(row['bytes']),row
  rows+=1
print('app custody verified',rows,flush=True)
run('app-suite',[sys.executable,'-B','-X','utf8',str(ws/'app/tests/test_entry.py')],ws)
# Load only helper definitions; do not repeat its test dispatcher.
import ast
test=ws/'app/tests/test_entry.py'; tree=ast.parse(test.read_text(encoding='utf8'))
nodes=[]
for node in tree.body:
 if isinstance(node,(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.ClassDef,ast.Assign,ast.AnnAssign)):
  # No top-level run calls exist in these helpers except FOREIGN setup.
  nodes.append(node)
ns={'__file__':str(test),'__name__':'prime_helpers'}
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(test),'exec'),ns)
fixture=ws/'app'; digest=ns['make_fixture'](fixture)
f=fixture/'fixture.json';data=json.loads(f.read_text());data['output']='README.md';f.write_text(json.dumps(data),encoding='utf8')
before=sha((fixture/'README.md').read_bytes())
r=run('app-source-overlap-probe',[sys.executable,'-B',str(ws/'app/librarian.py'),'test-run','--root',str(fixture),'--candidate',ns['CANDIDATE'],'--sha256',digest],out)
probe={'exit':r.returncode,'source_before':before,'source_after':sha((fixture/'README.md').read_bytes()),'isolated_copy':str(ws)}
(out/'app-probe.json').write_text(json.dumps(probe,indent=2));print('SOURCE OVERLAP',probe,flush=True)
lab=src/'labs/worker-bridge-pass01';dest=out/'bridge';dest.mkdir()
manifest=lab/'evidence/pass03/SHA256SUMS.pass03.txt'; count=0
for line in manifest.read_text().splitlines():
 h,rel=line.split('  ',1);b=(lab/rel).read_bytes();assert sha(b)==h,rel
 p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);count+=1
print('bridge manifest verified',count,flush=True)
for name in ['test_bridge.py','test_pass02.py','test_pass03.py']:
 run(name,[sys.executable,'-B','-X','dev',str(dest/'tests'/name),'-v'],dest)
(out/'summary.json').write_text(json.dumps({'custody_rows':rows,'bridge_manifest_rows':count,'app_probe':probe},indent=2))
print('DONE',out,flush=True)
