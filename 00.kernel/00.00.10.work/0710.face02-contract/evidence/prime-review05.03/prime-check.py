from pathlib import Path
import json,hashlib,subprocess,sys,importlib.util
sys.dont_write_bytecode=True
R=Path('D:/Git/lib-build');W=R/'00.kernel/00.00.10.work';C=W/'0710.face02-contract/evidence/design05.03';O=Path('D:/librarian/temp/prime-cycle4-nov02');O.mkdir(exist_ok=False)
report={}
for page,num,kind in [('0521.return-placement','05.06','build'),('0521.return-placement','05.07','build'),('0710.face02-contract','05.03','design')]:
 key=page+'/'+num;report[key]={}
 for label,mp in [('artifacts',W/page/'evidence'/(kind+num)/('ARTIFACT-MANIFEST.json' if kind=='design' else 'artifact-manifest.json')),('inputs',W/page/'evidence'/('pack'+num)/'source-manifest.json')]:
  rows=json.loads(mp.read_text(encoding='utf-8'))['files'];bad=[];drift=[]
  for row in rows:
   raw=(R/row.get('snapshot',row['path'])).read_bytes()
   if hashlib.sha256(raw).hexdigest()!=row['sha256'] or len(raw)!=row['bytes']:bad.append(row['path'])
   if label=='inputs' and hashlib.sha256((R/row['path']).read_bytes()).hexdigest()!=row['sha256']:drift.append(row['path'])
  report[key][label]={'count':len(rows),'bad':bad,'live_drift':drift}
(O/'integrity.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
commands=[]
def run(label,args):
 p=subprocess.run([sys.executable,'-B',*map(str,args)],capture_output=True,cwd=R)
 (O/(label+'.stdout.txt')).write_bytes(p.stdout);(O/(label+'.stderr.txt')).write_bytes(p.stderr)
 commands.append({'label':label,'args':list(map(str,args)),'exit':p.returncode});(O/'commands.json').write_text(json.dumps(commands,indent=2),encoding='utf-8')
 print(label,'exit',p.returncode,flush=True);return p
run('forms50',[C/'validation/validate2.py','--out',O/'forms50'])
run('lifecycle13',[C/'lifecycle/lifecycle_sim.py','--runs',O/'lifecycle13'])
run('attachment8',[C/'attach/attach_lookup.py','--book',O/'attach-book','--out',O/'attachment8.json'])
book=Path('D:/librarian/temp/0521-0507/20261102T193704Z/book')
for label,selector in [('native',['--source','0521.return-placement','--pass','05.01']),('native2',['--source','0521.return-placement','--pass','05.02']),('historical',['--source','0508.return-capture','--pass','05.08']),('occupant',['--member','0104.app-entry-0508']),('incomplete',['--member','0154.colab-support-first-0501']),('local',['--source','0701.bench-method','--pass','05.01'])]:
 run('access-'+label,[R/'app/librarian.py','return-lines','verify','--book',book,*selector])
spec=importlib.util.spec_from_file_location('life',C/'lifecycle/lifecycle_sim.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def prepared(name):
 b=m.Book(O/name)
 for p in m.PAGES:b.stage(p);b.sign(p);b.approve(p)
 b.seat(list(m.PAGES));return b
probes=[]
b=prepared('restart-probe');p='0001.law';seat=b.law/p/'01.md';seat.write_bytes(seat.read_bytes()+b'TAMPERED AFTER COMPLETE\r\n')
try:r=b.restart(p);probes.append({'probe':'completed restart after changed seated bytes','result':r})
except m.Stop as e:probes.append({'probe':'completed restart after changed seated bytes','outcome':e.outcome,'code':e.code})
b=prepared('rollback-probe');seat=b.law/p/'01.md';seat.write_bytes(seat.read_bytes()+b'TAMPERED AFTER COMPLETE\r\n')
try:r=b.rollback(p);probes.append({'probe':'rollback after changed seated bytes','result':r,'renamed_before_refusal':not seat.read_bytes().endswith(b'TAMPERED AFTER COMPLETE\r\n')})
except m.Stop as e:probes.append({'probe':'rollback after changed seated bytes','outcome':e.outcome,'code':e.code})
(O/'independent-lifecycle-probes.json').write_text(json.dumps(probes,indent=2),encoding='utf-8');print(json.dumps(probes),flush=True)
