from pathlib import Path
import csv,hashlib,importlib.util,json,os,shutil,subprocess,sys,tempfile
from unittest import mock
W=Path(r'D:\Git\lib-build');O=Path(tempfile.mkdtemp(prefix='prime-app-clerk-'));env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'}
def sha(b):return hashlib.sha256(b).hexdigest()
def run(name,args,cwd,timeout=210):
 r=subprocess.run(args,cwd=cwd,env=env,capture_output=True,timeout=timeout)
 (O/(name+'.stdout.txt')).write_bytes(r.stdout);(O/(name+'.stderr.txt')).write_bytes(r.stderr)
 print(name,r.returncode,r.stdout.decode('utf8','replace')[-350:],r.stderr.decode('utf8','replace')[-650:],flush=True);return r
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod);return mod
print('EVIDENCE',O,flush=True)
n=0
for name in ['custody.tsv','text-custody.tsv']:
 for row in csv.DictReader((W/'00.kernel/00.00.10.work/0504.app-entry/evidence/05.05'/name).open(encoding='utf8'),delimiter='\t'):
  b=subprocess.check_output(['git','show','d9775fabe705c6a90be9bc770b17289b6b7c7188:'+row['path']],cwd=W,env=env);assert sha(b)==row['sha256'] and len(b)==int(row['bytes']),row['path'];n+=1
print('app custody',n,flush=True)
ws=O/'workspace';ws.mkdir()
for rel in filter(None,subprocess.check_output(['git','ls-files','-z'],cwd=W,env=env).decode().split('\0')):
 p=ws/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/rel,p)
# Independently inspect receipt correlation before running the broad integration suite.
t=load('prime_bridge_helpers',ws/'app/tests/test_worker_bridge.py');root=t.fresh('prime-receipt-correlation');t.plant(root);t.write_job(root)
r=t.bridge(root,'bridge-test','--job','bridge/job.json');assert r.returncode==0,r.stderr
receipt=root/'bridge/store/bridge-0001/receipt.json';saved=receipt.read_bytes();original=json.loads(saved)
bad=dict(original);bad.pop('request_sha256');bad['delivery_id']='another-delivery';bad['job_id']='another-job';receipt.write_text(json.dumps(bad),encoding='utf8')
r=t.bridge(root,'bridge-status','--delivery','bridge-0001')
probe={'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'tamper':'Removed request_sha256; changed delivery_id/job_id in an otherwise valid stored receipt','expected':'refuse inconsistent stored receipt; never report collected success'}
(O/'receipt-correlation.json').write_text(json.dumps(probe,indent=2));print('RECEIPT CORRELATION',r.returncode,r.stdout[-450:],flush=True);receipt.write_bytes(saved)
r=run('app-integration-suite',[sys.executable,'-B','-X','utf8',str(ws/'app/tests/test_worker_bridge.py')],ws)
integration_exit=r.returncode
r=run('app-entry-suite',[sys.executable,'-B','-X','utf8',str(ws/'app/tests/test_entry.py')],ws)
entry_exit=r.returncode
lab=W/'labs/clerk-handoff-pass02';dest=O/'clerk';dest.mkdir();count=0
for line in (lab/'evidence/SHA256SUMS.txt').read_text().splitlines():
 h,rel=line.split('  ',1);b=(lab/rel).read_bytes();assert sha(b)==h,rel
 p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);count+=1
print('clerk manifest',count,flush=True)
r=run('clerk-suite',[sys.executable,'-B','-X','dev',str(dest/'tests/test_clerk.py'),'-v'],dest)
clerk_exit=r.returncode
r=run('clerk-demo',[sys.executable,'-B',str(dest/'demo.py'),'--out',str(O/'clerk-demo-store')],dest);demo_exit=r.returncode
m=load('prime_clerk_helpers',dest/'tests/test_clerk.py');c=m.ClerkTests();c.setUp();assert c.queue().returncode==0;cl=c.claim();assert cl.returncode==0;token=c.token_of(cl.stdout);c.write_output()
blank=c.ret(token,evidence='');assert blank.returncode==0
terminal=c.store/'jobs/demo-0001/0003.returned.json';assert terminal.is_relative_to(c.root);terminal.unlink()
verify=c.cli(['verify','--store',str(c.store)]);inbox=c.cli(['inbox','--store',str(c.store),'--as','codex-prime']);c.write_output(m.COUNT+b'# changed\n');again=c.ret(token,delivery='d-2')
clerk_probes={'blank_evidence':{'exit':blank.returncode,'stdout':blank.stdout},'deleted_terminal_verify':{'exit':verify.returncode,'stdout':verify.stdout},'deleted_terminal_inbox':{'exit':inbox.returncode,'stdout':inbox.stdout},'different_rereturn_after_deletion':{'exit':again.returncode,'stdout':again.stdout}}
d=m.ClerkTests();d.setUp();assert d.queue().returncode==0;orig=m.clerk.os.mkdir
def collided(path,*a,**kw):
 if Path(path)==d.store/'jobs/demo-0001/outbox':
  orig(path,*a,**kw);raise FileExistsError('simulated competing outbox creation')
 return orig(path,*a,**kw)
try:
 with mock.patch.object(m.clerk.os,'mkdir',side_effect=collided):m.clerk.claim(str(d.store),'demo-0001','builder-b',str(d.base))
 clerk_probes['outbox_oserror']={'caught':False}
except OSError as ex:clerk_probes['outbox_oserror']={'caught':True,'exception':type(ex).__name__,'claim_event_written':(d.store/'jobs/demo-0001/0002.claimed.json').is_file()}
(O/'clerk-probes.json').write_text(json.dumps(clerk_probes,indent=2))
summary={'app_custody_rows':n,'app_integration_exit':integration_exit,'app_entry_exit':entry_exit,'receipt_correlation':probe,'clerk_manifest_rows':count,'clerk_suite_exit':clerk_exit,'clerk_demo_exit':demo_exit,'clerk_probes':clerk_probes,'source_writes':'isolated copies only','model_calls':0}
(O/'verification.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2),flush=True)
