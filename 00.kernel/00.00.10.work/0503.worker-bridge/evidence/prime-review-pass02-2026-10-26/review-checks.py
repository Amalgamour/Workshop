from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
W=Path(r'D:\Git\lib-build');L=W/'labs/worker-bridge-pass01';P=W/'00.kernel/00.00.10.work/0503.worker-bridge'
O=Path(r'D:\librarian\temp\review-0503-pass02-2026-10-26');O.mkdir(exist_ok=False);C=O/'lab-copy';C.mkdir()
def sha(b):return hashlib.sha256(b).hexdigest()
manifest={}
for line in (L/'evidence/pass02/SHA256SUMS.pass02.txt').read_text(encoding='utf-8').splitlines():
    if not line.strip():continue
    h,rel=line.split('  ',1);data=(L/rel).read_bytes();assert sha(data)==h,rel
    manifest[rel]=h;dest=C/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
before_job=sha((P/'05.02.md').read_bytes())
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
suite=[]
for name in ('test_bridge.py','test_pass02.py'):
    r=subprocess.run([sys.executable,'-B','-X','dev',str(C/'tests'/name),'-v'],cwd=C,capture_output=True,env=env,timeout=60)
    (O/(name+'.txt')).write_bytes(r.stdout+r.stderr);assert r.returncode==0,(r.stdout+r.stderr).decode()
    suite.append({'suite':name,'exit':0})
# Same three earlier probes against a fresh copy of corrected code.
r=subprocess.run([sys.executable,'-B',str(C/'tests/probes_pass02.py'),str(C),str(O/'original-probes')],cwd=C,capture_output=True,env=env,timeout=15)
(O/'original-probes.txt').write_bytes(r.stdout+r.stderr);assert r.returncode==0,r.stderr.decode()
probes=json.loads(r.stdout)
assert probes['BR-01 elapsed_s']<1.5
assert 'refused' in probes["BR-02 status('../outside')"] and 'refused' in probes["BR-02 recover('../outside')"]
for key in ('BR-03 infinite timeout','BR-03 fractional byte cap','BR-03 bool limits'):assert probes[key].startswith('refused')
# Additional deadline boundary: direct child exits but a self-terminating grandchild holds its pipes.
grandchild=C/'fixtures/prime_inherited_pipes.py'
grandchild.write_text('''import json,sys,subprocess
request=json.loads(sys.stdin.buffer.read())
subprocess.Popen([sys.executable,'-c','import time; time.sleep(5)'],stdin=subprocess.DEVNULL,stdout=sys.stdout,stderr=sys.stderr)
''',encoding='utf-8')
driver=O/'inherited-pipes-driver.py'
driver.write_text('''import json,sys,time
from pathlib import Path
sys.path.insert(0,sys.argv[1])
from bridge.adapter import LocalProcessAdapter,CLEANUP_ALLOWANCE_S
root=Path(sys.argv[2]);root.mkdir();inp=root/'input';out=root/'output';inp.mkdir();out.mkdir()
ad=LocalProcessAdapter(root/'store',{'prime-inherited':{'kind':'protocol test worker','argv':['{python}','-B','-I','fixtures/prime_inherited_pipes.py']}},Path(sys.argv[1]))
e={'schema':'worker-bridge/request@1','delivery_id':'probe-inherited','job_id':'probe','role':'builder','work_ref':'isolated Prime review fixture','inputs':[],'input_root':str(inp),'output_root':str(out),'limits':{'timeout_s':0.2,'max_stdout_bytes':1000,'max_stderr_bytes':1000},'release':{'by':'Prime review','ref':'local fixture only'},'backend':'prime-inherited'}
t=time.monotonic();r=ad.deliver(e)
print(json.dumps({'elapsed_s':time.monotonic()-t,'timeout_s':0.2,'cleanup_allowance_s':CLEANUP_ALLOWANCE_S,'receipt':r}))
''',encoding='utf-8')
r=subprocess.run([sys.executable,'-B',str(driver),str(C),str(O/'inherited-probe')],env=env,capture_output=True,timeout=12)
(O/'inherited-pipes-probe.txt').write_bytes(r.stdout+r.stderr);assert r.returncode==0,r.stderr.decode()
inherited=json.loads(r.stdout)
for rel,h in manifest.items():assert sha((L/rel).read_bytes())==h,rel
assert sha((P/'05.02.md').read_bytes())==before_job
result={'reviewer':'Codex Prime','reviewed_batch_sha256':before_job,'manifest_files_verified':len(manifest),'independent_suites':suite,'independent_test_count':28,'original_three_probes':probes,'inherited_pipes_probe':inherited,'original_lab_and_batch_unchanged':True,'actual_model_calls':0,'shared_records_or_Git_written':False}
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
