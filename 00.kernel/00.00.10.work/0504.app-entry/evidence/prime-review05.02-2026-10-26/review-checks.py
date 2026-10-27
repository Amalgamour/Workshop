from pathlib import Path
import ast,csv,hashlib,importlib.util,json,os,shutil,subprocess,sys,tempfile
W=Path(r'D:\Git\lib-build');O=Path(tempfile.mkdtemp(prefix='prime-workers-round2-'));env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'}
def sha(b):return hashlib.sha256(b).hexdigest()
def run(name,args,cwd):
 r=subprocess.run(args,cwd=cwd,env=env,capture_output=True,timeout=120)
 (O/(name+'.stdout.txt')).write_bytes(r.stdout);(O/(name+'.stderr.txt')).write_bytes(r.stderr)
 print(name,r.returncode,r.stdout.decode('utf8','replace')[-450:],r.stderr.decode('utf8','replace')[-450:],flush=True);return r
print('EVIDENCE',O,flush=True)
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=W,env=env,text=True).strip()
ws=O/'workspace';ws.mkdir()
for rel in filter(None,subprocess.check_output(['git','ls-files','-z'],cwd=W,env=env).decode().split('\0')):
 p=ws/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/rel,p)
n=0
for name in ['custody.tsv','text-custody.tsv']:
 for row in csv.DictReader((W/'00.kernel/00.00.10.work/0504.app-entry/evidence/05.02'/name).open(encoding='utf8'),delimiter='\t'):
  b=subprocess.check_output(['git','show','cf9ed917e4b0f1bab3f050216a1a7a2abc4118b2:'+row['path']],cwd=W,env=env)
  assert sha(b)==row['sha256'] and len(b)==int(row['bytes']);n+=1
print('app evidence custody',n,flush=True)
r=run('app-suite',[sys.executable,'-B','-X','utf8',str(ws/'app/tests/test_entry.py')],ws);assert r.returncode==0
# Reproduce Prime's original source-folder fixture against the repaired entry.
test=ws/'app/tests/test_entry.py';tree=ast.parse(test.read_text());nodes=[x for x in tree.body if isinstance(x,(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.ClassDef,ast.Assign,ast.AnnAssign))]
ns={'__file__':str(test),'__name__':'prime_helpers'};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(test),'exec'),ns)
digest=ns['make_fixture'](ws/'app');f=ws/'app/fixture.json';v=json.loads(f.read_text());v['output']='README.md';f.write_text(json.dumps(v))
before=sha((ws/'app/README.md').read_bytes())
r=run('app-original-probe',[sys.executable,'-B',str(ws/'app/librarian.py'),'test-run','--root',str(ws/'app'),'--candidate',ns['CANDIDATE'],'--sha256',digest],O)
assert r.returncode==2 and sha((ws/'app/README.md').read_bytes())==before
lab=W/'labs/book-orientation-pass01';dest=O/'orientation';dest.mkdir();count=0
for line in (lab/'evidence/SHA256SUMS.txt').read_text().splitlines():
 h,rel=line.split('  ',1);b=(lab/rel).read_bytes();assert sha(b)==h,rel
 p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);count+=1
print('orientation manifest',count,flush=True)
r=run('orientation-suite',[sys.executable,'-B','-X','dev',str(dest/'tests/test_check_book.py'),'-v'],dest);assert r.returncode==0
for tag,rev,extra in [('old-selected','a5853b7',[]),('old-candidate','a5853b7',['--contents','0011.contents/01.002.md']),('new-selected',head,[])]:
 r=run(tag,[sys.executable,'-B',str(dest/'check_book.py'),'--root',str(W),'--revision',rev,'--book','00.kernel/00.00.10.work','--json',*extra],dest);assert r.returncode==1
# Independent supported-section completeness probe in a disposable committed fixture.
spec=importlib.util.spec_from_file_location('orientation_test_helpers',dest/'tests/test_check_book.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
case=m.Book(methodName='test_correct_book_is_clean');case.setUp();files=dict(case.files)
files[m.BOOK+'/0011.contents/01.002.md']=m.GOOD.replace(' Each lists what it holds.','\nMissing: `../00.00.99.missing/00.md`.')
commit=case.commit(files);code,report=case.run_tool(commit)
(O/'orientation-extra-line.json').write_text(json.dumps({'exit':code,'report':report,'added_explicit_missing_reference':'Missing: `../00.00.99.missing/00.md`.'},indent=2))
print('OTHER BOOKS SECOND LINE',code,report['result'],flush=True)
summary={'head':head,'custody_rows':n,'orientation_manifest_rows':count,'app_original_probe_refused':True,'orientation_extra_line_exit':code,'orientation_extra_line_result':report['result'],'evidence':str(O)}
(O/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2),flush=True)
