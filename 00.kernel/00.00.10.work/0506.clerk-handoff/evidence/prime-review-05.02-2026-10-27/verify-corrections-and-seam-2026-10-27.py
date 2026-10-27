from pathlib import Path
import csv,hashlib,importlib.util,json,os,shutil,subprocess,sys,tempfile
from unittest import mock
W=Path(r'D:\Git\lib-build');O=Path(tempfile.mkdtemp(prefix='prime-fixed-components-'));env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'}
def sha(b):return hashlib.sha256(b).hexdigest()
def run(name,args,cwd,timeout=280):
 r=subprocess.run(args,cwd=cwd,env=env,capture_output=True,timeout=timeout)
 (O/(name+'.stdout.txt')).write_bytes(r.stdout);(O/(name+'.stderr.txt')).write_bytes(r.stderr)
 print(name,r.returncode,r.stdout.decode('utf8','replace')[-360:],r.stderr.decode('utf8','replace')[-500:],flush=True);return r
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
print('EVIDENCE',O,flush=True)
page=W/'00.kernel/00.00.10.work/0504.app-entry';n=0
for manifest in ['custody.tsv','text-custody.tsv']:
 for row in csv.DictReader((page/'evidence/05.06'/manifest).open(encoding='utf8'),delimiter='\t'):
  b=(W/row['path']).read_bytes();assert sha(b)==row['sha256'] and len(b)==int(row['bytes']),row['path'];n+=1
print('working app custody',n,flush=True)
ws=O/'workspace';ws.mkdir();tracked=filter(None,subprocess.check_output(['git','ls-files','-z'],cwd=W,env=env).decode().split('\0'))
source_hashes={}
for rel in tracked:
 p=ws/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/rel,p)
for rel in ['app/worker_bridge.py','app/tests/test_worker_bridge.py','app/context.py','labs/worker-bridge-pass01/tests/test_pass03.py']:
 source_hashes[rel]=sha((W/rel).read_bytes())
t=load('corrected_bridge_helpers',ws/'app/tests/test_worker_bridge.py');root=t.fresh('prime-corrected-receipt');t.plant(root);t.write_job(root)
r=t.bridge(root,'bridge-test','--job','bridge/job.json');assert r.returncode==0,r.stderr
receipt=root/'bridge/store/bridge-0001/receipt.json';saved=receipt.read_bytes();bad=json.loads(saved);bad.pop('request_sha256');bad['delivery_id']='another-delivery';bad['job_id']='another-job';receipt.write_text(json.dumps(bad));before=sha(receipt.read_bytes());launch=(root/'bridge/delivery/bridge-0001/output/launches.log').read_bytes()
r=t.bridge(root,'bridge-status','--delivery','bridge-0001');assert r.returncode==2 and sha(receipt.read_bytes())==before and (root/'bridge/delivery/bridge-0001/output/launches.log').read_bytes()==launch
probe={'exit':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'receipt_unchanged':True,'launch_unchanged':True};(O/'receipt-refusal.json').write_text(json.dumps(probe,indent=2));print('corrected receipt refused',r.returncode,flush=True);receipt.write_bytes(saved)
r=run('app-integration-suite',[sys.executable,'-B','-X','utf8',str(ws/'app/tests/test_worker_bridge.py')],ws);app_exit=r.returncode
r=run('app-entry-suite',[sys.executable,'-B','-X','utf8',str(ws/'app/tests/test_entry.py')],ws);entry_exit=r.returncode
lab=W/'labs/clerk-handoff-pass02';dest=O/'clerk';dest.mkdir();count=0
for line in (lab/'evidence/SHA256SUMS.pass02.txt').read_text().splitlines():
 h,rel=line.split('  ',1);b=(lab/rel).read_bytes();assert sha(b)==h,rel;p=dest/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);count+=1
source_hashes['labs/clerk-handoff-pass02/clerk.py']=sha((lab/'clerk.py').read_bytes())
print('clerk manifest',count,flush=True)
r=run('clerk-suite',[sys.executable,'-B','-X','dev',str(dest/'tests/test_clerk.py'),'-v'],dest);clerk_exit=r.returncode
r=run('clerk-demo',[sys.executable,'-B',str(dest/'demo.py'),'--out',str(O/'clerk-demo-store')],dest);demo_exit=r.returncode
m=load('corrected_clerk_helpers',dest/'tests/test_clerk.py');c=m.ClerkTests();c.setUp();assert c.queue().returncode==0;cl=c.claim();assert cl.returncode==0;token=c.token_of(cl.stdout);c.write_output();assert c.ret(token).returncode==0
event=c.store/'jobs/demo-0001/0003.returned.json';witness=c.store/'jobs/demo-0001/0003.witness.json';wbytes=witness.read_bytes();event.unlink();verify=c.cli(['verify','--store',str(c.store)]);inbox=c.cli(['inbox','--store',str(c.store),'--as','codex-prime']);again=c.ret(token,delivery='d-2')
assert verify.returncode!=0 and inbox.returncode!=0 and again.returncode==2 and witness.read_bytes()==wbytes and not event.exists()
d=m.ClerkTests();d.setUp();assert d.queue().returncode==0;assert d.claim().returncode==0;d.write_output();blank=d.ret(d.token_of(d.claim('--resume').stdout),evidence='');assert blank.returncode==2
e=m.ClerkTests();e.setUp();assert e.queue().returncode==0;orig=m.clerk.os.mkdir
def collide(path,*a,**kw):
 if Path(path)==e.store/'jobs/demo-0001/outbox':orig(path,*a,**kw);raise FileExistsError('controlled competing outbox creation')
 return orig(path,*a,**kw)
with mock.patch.object(m.clerk.os,'mkdir',side_effect=collide):error_result=m.clerk.claim(str(e.store),'demo-0001','builder-b',str(e.base))
assert error_result.code==2
cp={'missing_terminal_verify':{'exit':verify.returncode,'stdout':verify.stdout},'missing_terminal_inbox':{'exit':inbox.returncode,'stdout':inbox.stdout},'different_rereturn_exit':again.returncode,'witness_unchanged':True,'blank_evidence_exit':blank.returncode,'os_error_code':error_result.code,'os_error_text':error_result.text}
(O/'clerk-correction-probes.json').write_text(json.dumps(cp,indent=2))
design=W/'00.kernel/00.00.10.work/0506.clerk-handoff/evidence/design05.03';dn=0
for line in (design/'SHA256SUMS.txt').read_text().splitlines():
 h,rel=line.split('  ',1);assert sha((design/rel).read_bytes())==h,rel;dn+=1
instruction=(design/'examples/router/instructions/task.md').read_bytes();job=json.loads((design/'examples/router/clerk-job.json').read_text());bridgejob=json.loads((design/'examples/fixture/bridge/job.json').read_text());link=json.loads((design/'examples/fixture/clerk-link/bridge-0001.json').read_text())
assert job['instructions']['sha256']==sha(instruction)==bridgejob['inputs'][0]['sha256'];assert bridgejob['job_id']==job['job_id']==link['clerk_job_id'];assert bridgejob['delivery_id']==link['delivery_id'];assert sha((design/'examples/fixture/bridge/job.json').read_bytes())==link['bridge_job_sha256'];assert len([l for l in instruction.decode().splitlines() if l.strip()])==3
for rel,h in source_hashes.items():assert sha((W/rel).read_bytes())==h,('source changed during review',rel)
summary={'app_custody_rows':n,'custody_boundary':'working files; Builder evidence commit still pending at read','app_integration_exit':app_exit,'entry_exit':entry_exit,'receipt_probe':probe,'clerk_manifest_rows':count,'clerk_suite_exit':clerk_exit,'clerk_demo_exit':demo_exit,'clerk_probes':cp,'seam_design_manifest_rows':dn,'seam_example_cross_references':'pass','source_hashes':source_hashes,'model_calls':0,'SoF_touched':False}
(O/'verification.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2),flush=True)
