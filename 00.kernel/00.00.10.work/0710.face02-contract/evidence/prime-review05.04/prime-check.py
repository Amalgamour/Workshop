from pathlib import Path
import json,hashlib,subprocess,sys,importlib.util,copy
sys.dont_write_bytecode=True
R=Path('D:/Git/lib-build');P=R/'00.kernel/00.00.10.work/0710.face02-contract';E=P/'evidence/design05.04';O=Path('D:/librarian/temp/0710-pass04-prime');O.mkdir(exist_ok=False)
integrity={}
for label,m in [('artifacts',E/'ARTIFACT-MANIFEST.json'),('inputs',P/'evidence/pack05.04/source-manifest.json')]:
 rows=json.loads(m.read_text(encoding='utf-8'))['files'];bad=[];drift=[]
 for row in rows:
  raw=(R/row.get('snapshot',row['path'])).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=row['sha256'] or len(raw)!=row['bytes']:bad.append(row['path'])
  if label=='inputs' and hashlib.sha256((R/row['path']).read_bytes()).hexdigest()!=row['sha256']:drift.append(row['path'])
 integrity[label]={'count':len(rows),'bad':bad,'live_drift':drift}
(O/'integrity.json').write_text(json.dumps(integrity,indent=2),encoding='utf-8');print(json.dumps(integrity),flush=True)
p=subprocess.run([sys.executable,'-B',str(E/'lifecycle/lifecycle_sim2.py'),'--runs',str(O/'rerun35')],capture_output=True)
(O/'rerun.stdout.txt').write_bytes(p.stdout);(O/'rerun.stderr.txt').write_bytes(p.stderr);print('35 authored cases rerun exit',p.returncode,flush=True)
spec=importlib.util.spec_from_file_location('lifecycle2',E/'lifecycle/lifecycle_sim2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def prepared(name):
 b=m.Book(O/name)
 for page in m.PAGES:b.stage(page);b.sign(page);b.approve(page)
 b.seat(list(m.PAGES));return b
rows=[];page='0001.law'
def check(label,b,fn,expected_hold=True):
 before=b.tree()
 try: result={'returned':fn()}
 except m.Stop as e:result={'outcome':e.outcome,'code':e.code}
 result.update({'label':label,'tree_unchanged':b.tree()==before,'expected_hold':expected_hold});rows.append(result);print(json.dumps(result),flush=True)
b=prepared('original-completed-drift');f=b.law/page/'01.md';f.write_bytes(f.read_bytes()+b'CHANGED AFTER COMPLETION\r\n');check('original completed restart probe',b,lambda:b.restart(page))
b=prepared('original-rollback-drift');f=b.law/page/'01.md';f.write_bytes(f.read_bytes()+b'CHANGED AFTER COMPLETION\r\n');check('original rollback drift probe',b,lambda:b.rollback(page,m.decision_for(b,page)))
b=prepared('swapped-plan');r=b.r(page);r['seat']['plan']=copy.deepcopy(b.r('0002.schema')['seat']['plan']);b.save(page,r);check('page 0001 journal supplied with page 0002 plan',b,lambda:b.restart(page))
b=prepared('changed-rollback-decision')
try:b.rollback(page,m.decision_for(b,page),crash=('R1','after'))
except m.Crash:pass
r=b.r(page);r['rollback']['decision']['restore_seat_sha256']='0'*64;b.save(page,r)
check('rollback decision changes after interrupted R1',b,lambda:b.roll_restart(page))
(O/'independent-probes.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
