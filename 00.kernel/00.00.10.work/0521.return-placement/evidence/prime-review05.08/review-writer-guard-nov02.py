from pathlib import Path
import json,hashlib,subprocess,sys,importlib.util
sys.dont_write_bytecode=True
R=Path('D:/Git/lib-build');P=R/'00.kernel/00.00.10.work/0521.return-placement';O=Path('D:/librarian/temp/0521-pass08-prime');O.mkdir(exist_ok=False)
report={}
for label,mp in [('artifacts',P/'evidence/build05.08/artifact-manifest.json'),('inputs',P/'evidence/pack05.08/source-manifest.json')]:
 rows=json.loads(mp.read_text(encoding='utf-8'))['files'];bad=[];drift=[]
 for row in rows:
  raw=(R/row.get('snapshot',row['path'])).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=row['sha256'] or len(raw)!=row['bytes']:bad.append(row['path'])
  if label=='inputs' and hashlib.sha256((R/row['path']).read_bytes()).hexdigest()!=row['sha256']:drift.append(row['path'])
 report[label]={'count':len(rows),'bad':bad,'live_drift':drift}
(O/'integrity.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
p=subprocess.run([sys.executable,'-B',str(R/'labs/return-capture-guard-pass01/tests/test_guard.py')],capture_output=True,cwd=R)
(O/'unit.stdout.txt').write_bytes(p.stdout);(O/'unit.stderr.txt').write_bytes(p.stderr);print('six author cases independent rerun exit',p.returncode,flush=True)
spec=importlib.util.spec_from_file_location('guard',R/'labs/return-capture-guard-pass01/return_capture_guard.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
lines=m.load_lines();raw=lines.dump(lines.layout_body('00.00.10.work'));rows=[]
def tree(root):return {f.relative_to(root).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in root.rglob('*') if f.is_file()}
for name,kind in [('layout-is-directory','directory'),('duplicate-layout-key','duplicate')]:
 b=O/name;b.mkdir();layout=b/'return-line-layout.json'
 if kind=='directory':layout.mkdir();(layout/'preserve.txt').write_text('keep',encoding='utf-8')
 else:layout.write_bytes(b'{"schema":"duplicate",'+raw[1:])
 before=tree(b);called=[]
 def loader():called.append(True);raise AssertionError('writer must not load')
 args=['reserve','--book',str(b),'--submission','prime-probe','--name','probe','--origin-book','00.00.10.work','--origin-page','0521.return-placement','--origin-batch','05.08','--submitter','Prime test','--reviewer','Prime','--release','synthetic caller probe, no live authority']
 code,text=m.run(args,loader=loader)
 row={'case':name,'class':'independent-reviewer','exit':code,'writer_loaded':bool(called),'tree_unchanged':tree(b)==before,'output':text};rows.append(row)
 assert code==2 and not called and row['tree_unchanged'],row
(O/'independent-cases.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps([{'case':r['case'],'exit':r['exit'],'writer_loaded':r['writer_loaded'],'tree_unchanged':r['tree_unchanged']}for r in rows]),flush=True)
