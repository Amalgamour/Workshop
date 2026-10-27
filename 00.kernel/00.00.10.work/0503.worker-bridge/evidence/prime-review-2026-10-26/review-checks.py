from pathlib import Path
import hashlib,importlib,json,os,shutil,subprocess,sys,time

W=Path(r'D:\Git\lib-build');L=W/'labs/worker-bridge-pass01';P=W/'00.kernel/00.00.10.work/0503.worker-bridge'
O=Path(r'D:\librarian\temp\review-0503-2026-10-26');O.mkdir(exist_ok=False)
C=O/'lab-copy';C.mkdir()
def sha(b):return hashlib.sha256(b).hexdigest()
before={}
for line in (L/'evidence/SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
    if not line.strip():continue
    h,rel=line.split('  ',1);p=L/rel;data=p.read_bytes();assert sha(data)==h,rel
    before[rel]=h;dest=C/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
jobhash=sha((P/'05.01.md').read_bytes())
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
r=subprocess.run([sys.executable,'-B','-X','dev',str(C/'tests/test_bridge.py'),'-v'],cwd=C,capture_output=True,env=env,timeout=60)
(O/'independent-tests.txt').write_bytes(r.stdout+r.stderr);assert r.returncode==0,(r.stdout+r.stderr).decode()
sys.path.insert(0,str(C))
from bridge.adapter import LocalProcessAdapter
from bridge.envelope import validate
from bridge.canon import canonical
# Control-plane identity containment: no worker launch, only scratch receipts.
scratch=O/'probes';scratch.mkdir();store=scratch/'store';store.mkdir();outside=scratch/'outside';outside.mkdir()
(outside/'receipt.json').write_bytes(b'{"sentinel":"outside the configured store"}')
adapter=LocalProcessAdapter(store,{},C)
escaped_status=adapter.status('../outside');escaped_recover=adapter.recover('../outside')
assert escaped_status.get('sentinel')=='outside the configured store'
assert escaped_recover.get('sentinel')=='outside the configured store'
# Finite timeout with a child that never reads stdin: child self-exits in 3s.
inp=scratch/'input';out=scratch/'output';inp.mkdir();out.mkdir();(inp/'i.txt').write_bytes(b'x\n')
base={'schema':'worker-bridge/request@1','delivery_id':'probe-timeout','job_id':'probe','role':'builder','work_ref':'lab-only',
'inputs':[{'name':'i','path':'i.txt','sha256':sha(b'x\n'),'bytes':2}],
'input_root':str(inp),'output_root':str(out),'limits':{'timeout_s':0.2,'max_stdout_bytes':1000,'max_stderr_bytes':1000},
'release':{'by':'Prime isolated review fixture','ref':'0503 review'},'backend':'fixture-noread'}
child=C/'fixtures/noread_prime_probe.py';child.write_text('import time\ntime.sleep(3)\n',encoding='utf-8')
driver=O/'timeout-driver.py'
driver.write_text('''import sys,json,time
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from bridge.adapter import LocalProcessAdapter
env=json.loads(Path(sys.argv[2]).read_text())
ad=LocalProcessAdapter(Path(sys.argv[3]),{'fixture-noread':{'kind':'protocol test worker','argv':['{python}','-B','-I','fixtures/noread_prime_probe.py']}},Path(sys.argv[1]))
t=time.monotonic();r=ad.deliver(env)
print(json.dumps({'elapsed_s':time.monotonic()-t,'receipt':r}))
''',encoding='utf-8')
big=dict(base,work_ref='x'*1_000_000);request=scratch/'request.json';request.write_bytes(canonical(big))
r=subprocess.run([sys.executable,'-B',str(driver),str(C),str(request),str(scratch/'timeout-store')],capture_output=True,env=env,timeout=12)
(O/'blocked-stdin-probe.txt').write_bytes(r.stdout+r.stderr);assert r.returncode==0,r.stderr.decode()
timeout=json.loads(r.stdout);assert timeout['elapsed_s']>2.5,timeout
# Malformed limit values accepted by validate before transport.
limits={}
for name,lim in [('infinite_timeout',{'timeout_s':float('inf'),'max_stdout_bytes':1000,'max_stderr_bytes':1000}),
('fractional_byte_cap',{'timeout_s':1,'max_stdout_bytes':1.5,'max_stderr_bytes':1000}),
('boolean_limits',{'timeout_s':True,'max_stdout_bytes':True,'max_stderr_bytes':True})]:
    try:validate(dict(base,limits=lim));limits[name]='accepted'
    except Exception as e:limits[name]=f'refused: {type(e).__name__}: {e}'
for rel,h in before.items():assert sha((L/rel).read_bytes())==h,rel
assert sha((P/'05.01.md').read_bytes())==jobhash
result={'reviewer':'Codex Prime','reviewed_batch_sha256':jobhash,'source_manifest_rows_verified':len(before),
'independent_suite':{'exit':0,'tests':18,'mode':'-X dev','log':'independent-tests.txt'},
'probes':{'status_path_escape':escaped_status,'recover_path_escape':escaped_recover,
'blocked_stdin':{'configured_timeout_s':0.2,'elapsed_s':timeout['elapsed_s'],'transport':timeout['receipt']['transport'],'receipt_duration_s':timeout['receipt']['duration_s']},'invalid_limits':limits},
'original_lab_and_batch_unchanged':True,'actual_model_calls':0,'shared_records_or_git_written':False,
'disposition':'request targeted corrections before accepting transport reliability for real model trial'}
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
