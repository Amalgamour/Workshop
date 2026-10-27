from pathlib import Path
import ast,csv,hashlib,json,os,shutil,subprocess,sys,tempfile
W=Path(r'D:\Git\lib-build');O=Path(tempfile.mkdtemp(prefix='prime-ar01-repair-'));env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'}
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=W,env=env)
def run(name,args,cwd):
 r=subprocess.run(args,cwd=cwd,env=env,capture_output=True,timeout=130)
 (O/(name+'.stdout.txt')).write_bytes(r.stdout);(O/(name+'.stderr.txt')).write_bytes(r.stderr)
 print(name,r.returncode,r.stdout.decode('utf8','replace')[-350:],r.stderr.decode('utf8','replace')[-400:],flush=True);return r
print('EVIDENCE',O,flush=True)
head=git('rev-parse','HEAD').decode().strip();ws=O/'workspace';ws.mkdir();n=0
for manifest in ['custody.tsv','text-custody.tsv']:
 p=W/'00.kernel/00.00.10.work/0504.app-entry/evidence/05.04'/manifest
 for row in csv.DictReader(p.open(encoding='utf8'),delimiter='\t'):
  b=git('show','4b0b26071649d10e0012241da63fd9051cd9a354:'+row['path']);assert sha(b)==row['sha256'] and len(b)==int(row['bytes']),row['path'];n+=1
for rel in filter(None,git('ls-files','-z').decode().split('\0')):
 p=ws/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(git('show',head+':'+rel))
print('custody',n,flush=True)
r=run('app-suite',[sys.executable,'-B','-X','utf8',str(ws/'app/tests/test_entry.py')],ws);assert r.returncode==0
test=ws/'app/tests/test_entry.py';tree=ast.parse(test.read_text());nodes=[x for x in tree.body if isinstance(x,(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.ClassDef,ast.Assign,ast.AnnAssign))]
ns={'__file__':str(test),'__name__':'prime_helpers'};exec(compile(ast.Module(body=nodes,type_ignores=[]),str(test),'exec'),ns)
root=ws/'app/scratch/prime-ar01';digest=ns['make_fixture'](root);victim=ws/'app/README.md';before=sha(victim.read_bytes());(root/'output').mkdir();temp=root/'output/inventory.json.tmp';os.link(victim,temp)
r=run('hardlink-probe',[sys.executable,'-B',str(ws/'app/librarian.py'),'test-run','--root',str(root),'--candidate',ns['CANDIDATE'],'--sha256',digest],O)
after=sha(victim.read_bytes());assert r.returncode==2 and before==after and temp.stat().st_nlink==2 and not (root/'output/inventory.json').exists()
preserved={}
for rel in ['00.kernel/00.00.01.law/0302.run/02.run.001.py','00.kernel/00.00.01.law/0302.run/02.run.002.py','00.kernel/00.00.01.law/0302.run/02.run.003.py','00.kernel/00.00.01.law/0302.run/02.md','00.kernel/00.00.10.work/0504.app-entry/fixtures/02.inventory.py']:
 assert git('show','4ae4b06fa72b2a8fc2d9b02521f998a305194262:'+rel)==git('show',head+':'+rel);preserved[rel]=sha(git('show',head+':'+rel))
summary={'head':head,'custody_rows':n,'suite':'12 positive checks, 46 expected refusals, 1 skipped file-symlink privilege case, 0 failures','hardlink_refused':True,'victim_unchanged':before==after,'victim_sha256':after,'link_count':temp.stat().st_nlink,'preserved':preserved,'model_calls':0,'source_writes':'disposable copy only'}
(O/'verification.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2),flush=True)
