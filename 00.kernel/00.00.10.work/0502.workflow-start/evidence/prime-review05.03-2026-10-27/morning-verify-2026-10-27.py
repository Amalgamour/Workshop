from pathlib import Path
import ast,hashlib,json,os,shutil,subprocess,sys,tempfile
W=Path(r'D:\Git\lib-build');O=Path(tempfile.mkdtemp(prefix='prime-morning-20261027-'));env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'}
def sha(b):return hashlib.sha256(b).hexdigest()
def run(name,args,cwd):
 r=subprocess.run(args,cwd=cwd,env=env,capture_output=True,timeout=150)
 (O/(name+'.stdout.txt')).write_bytes(r.stdout);(O/(name+'.stderr.txt')).write_bytes(r.stderr)
 print(name,r.returncode,r.stdout.decode('utf8','replace')[-350:],r.stderr.decode('utf8','replace')[-500:],flush=True);return r
print('EVIDENCE',O,flush=True)
ws=O/'workspace';ws.mkdir()
for rel in filter(None,subprocess.check_output(['git','ls-files','-z'],cwd=W,env=env).decode().split('\0')):
 p=ws/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/rel,p)
test=ws/'app/tests/test_entry.py';tree=ast.parse(test.read_text());nodes=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.ClassDef,ast.Assign,ast.AnnAssign))]
ns={'__file__':str(test),'__name__':'prime_helpers'};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(test),'exec'),ns)
root=ws/'app/scratch/prime-hardlink';digest=ns['make_fixture'](root)
victim=ws/'app/README.md';before=sha(victim.read_bytes());(root/'output').mkdir();temp=root/'output/inventory.json.tmp';os.link(victim,temp)
links=temp.stat().st_nlink
r=run('hardlink-probe',[sys.executable,'-B',str(ws/'app/librarian.py'),'test-run','--root',str(root),'--candidate',ns['CANDIDATE'],'--sha256',digest],O)
after=sha(victim.read_bytes());proof={'exit':r.returncode,'links_before':links,'victim_before':before,'victim_after':after,'reproduced':r.returncode==0 and before!=after,'isolated_workspace':str(ws)}
assert proof['reproduced'];(O/'hardlink-proof.json').write_text(json.dumps(proof,indent=2));print('HARDLINK',proof,flush=True)
lab=W/'labs/book-orientation-pass01';dest=O/'orientation';dest.mkdir();n=0
for line in (lab/'evidence/SHA256SUMS.pass02.txt').read_text().splitlines():
 h,rel=line.split('  ',1);b=(lab/rel).read_bytes();assert sha(b)==h,rel
 p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);n+=1
print('manifest rows',n,flush=True)
r=run('orientation-tests',[sys.executable,'-B','-X','dev',str(dest/'tests/test_check_book.py'),'-v'],dest);assert r.returncode==0
repro=W/'00.kernel/00.00.10.work/0502.workflow-start/evidence/repair05.03/repro.py'
r=run('orientation-regressions',[sys.executable,'-B','-W','error',str(repro),str(dest),str(O/'regressions.json')],O);assert r.returncode==0
cases=json.loads((O/'regressions.json').read_text());assert len(cases)==15 and all(c['meets_repair_contract'] for c in cases)
# Check recorded manifest files without executing the reviewed app probe bundle.
counts={}
for rel in ['00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03','00.kernel/00.00.10.work/0502.workflow-start/evidence/repair05.03']:
 folder=W/rel;count=0
 for line in (folder/'SHA256SUMS.txt').read_text().splitlines():
  h,name=line.split('  ',1);assert sha((folder/name).read_bytes())==h,name;count+=1
 counts[rel]=count
summary={'hardlink':proof,'checker_manifest_rows':n,'checker_tests':17,'checker_regressions':len(cases),'evidence_manifests':counts,'model_calls':0}
(O/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2),flush=True)
