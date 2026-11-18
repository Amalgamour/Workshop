from pathlib import Path
import sys,os,json,tempfile
O=Path(r'D:\librarian\temp\cloud-core-reliability-review-nov01');S=O/'source';sys.path.insert(0,str(S));os.environ['TEMP']=str(O/'scratch');os.environ['TMP']=str(O/'scratch');tempfile.tempdir=str(O/'scratch')
from app.desk_core.test_fault import FaultMatrix,_run
rows=[]
for boundary in ['after-prior-task','after-task-replacement']:
 f=FaultMatrix();f.setUp()
 try:
  f.init_captured();b=f.revise_path('B selected wording.\n','selected-B');code,rb=_run(['revise-task','--book',f.book,'--input',b]);assert code==0,rb
  c=f.revise_path('C pending wording.\n','pending-C');code,crash=_run(['revise-task','--book',f.book,'--input',c],fault=boundary);assert code==91
  shown=f.show();recovered=f.recover();history=f.source()/'05.01.history';files={p.relative_to(history).as_posix():p.read_text(encoding='utf-8') for p in history.rglob('*') if p.is_file()}
  rows.append({'boundary':boundary,'qualification':'serial second-revision probe using unmodified returned code; process exit, not power loss','crash_exit':code,'show':shown,'recover':recovered,'history':files})
 finally:f.tearDown()
(O/'second-revision-probes.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps([{'boundary':r['boundary'],'revision_state':r['show']['revision_state'],'visible_body':r['show']['body'],'recovery':r['recover']['recovery'],'history_files':list(r['history'])} for r in rows],indent=2))
