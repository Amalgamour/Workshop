from pathlib import Path
import sys,json,contextlib,hashlib
O=Path(r'D:\librarian\temp\cloud-core-review');S=O/'source';sys.path.insert(0,str(S))
from app.desk_core import engine as e
from app.desk_core.test_loop import task
from app.desk_core.identity import Refused
# Explicit dependency substitution for serial unit probes only. This does not
# establish Windows locking support or a successful native CLI integration.
e.file_lock=lambda path:contextlib.nullcontext()
book=O/'scratch/logic-probe-book';e.init_book(str(book),'SYNTHETIC unit probe, lock substituted')
first=task(body='SYNTHETIC ORIGINAL TASK WORDING 7f31\n');r=e.record_task(str(book),first);binding=r['task_binding_sha256']
reg={'page':'0523','subject':'sample','pass':'01','synthetic':True,
     'release':{'who':'Director (SYNTHETIC)','date':'2026-10-31','text':'Synthetic release\n'},
     'claim':{'worker':'synthetic-worker','date':'2026-10-31','text':'Synthetic claim\n'}}
e.register(str(book),reg)
ret={'page':'0523','subject':'sample','pass':'01','worker':'synthetic-worker','return_text':'SYNTHETIC return for original task\n',
     'unresolved_questions':[],'artifacts':[],'synthetic':True,'task_binding_sha256':binding}
e.submit_return(str(book),ret,False,None,None)
revised=task(body='SYNTHETIC NEW TASK WORDING 9b82\n',agreement='A different synthetic agreement\n')
rr=e.revise_task(str(book),revised)
oldtext=b'SYNTHETIC ORIGINAL TASK WORDING 7f31'
retained=[f.relative_to(book).as_posix() for f in book.rglob('*') if f.is_file() and oldtext in f.read_bytes()]
judgment={'page':'0523','subject':'sample','pass':'01','reviewer':'Codex Prime (SYNTHETIC)','review_identity':'review-new-task-old-return',
          'disposition':'held','findings':[],'dissent':'','director_text':'','unresolved_questions':[],
          'assessment':'SYNTHETIC judgment after changed assignment','next_action':{'actor':'prime','action':'Inspect the task'},'synthetic':True}
try:
    review=e.review(str(book),judgment);recovered=e.recover(str(book),'0523','sample','01')
    outcome={'review_refused':False,'review_binding':review.get('review_binding_sha256'),
             'state':recovered['state'],'review_fresh':recovered['review_fresh'],'complete':recovered['complete'],
             'conflicts':recovered['conflicts'],'next_action':recovered['next_action']}
except Refused as ex:outcome={'review_refused':True,'code':ex.code,'message':ex.message}
one=e._task_input(task(page='0523'));two=e._task_input(task(page='0524'))
result={'qualification':'serial unit probes with file_lock replaced by nullcontext in memory; native Windows CLI remains failed',
        'book':str(book),'prior_task_text_retained_in_book_files':retained,'revision':rr,
        'review_changed_task_old_return':outcome,'same_text_different_origins_same_task_binding':one['task_binding_sha256']==two['task_binding_sha256']}
(O/'logic-probes.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result,indent=2))
