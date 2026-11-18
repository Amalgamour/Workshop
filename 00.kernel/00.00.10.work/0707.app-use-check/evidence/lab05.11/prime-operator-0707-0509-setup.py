from pathlib import Path
import json,hashlib,shutil,subprocess,sys,os
root=Path(r'D:\Git\lib-build');work=root/'00.kernel/00.00.10.work';page=work/'0707.app-use-check';evidence=page/'evidence/lab05.11';book=Path(r'D:\librarian\temp\prime-operator-0707-0509')
assert not evidence.exists() and not book.exists()
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def fingerprints(p):return {f.relative_to(p).as_posix():{'bytes':len(f.read_bytes()),'sha256':sha(f.read_bytes())} for f in p.rglob('*') if f.is_file()}
rows=json.loads((page/'evidence/pack05.09/source-manifest.json').read_text(encoding='utf-8'))['files'];bad=[]
for row in rows:
    b=(root/row['path']).read_bytes()
    if len(b)!=row['bytes'] or sha(b)!=row['sha256']:bad.append(row['path'])
assert not bad,bad
evidence.mkdir();book.mkdir();dump(evidence/'source-verification.json',{'rows':len(rows),'mismatches':bad})
invocation='Run your pilot operation now.  Then tell me how it goes.  We have work to fit the 01NN section of work book.  Then I am assuming more work for the our first run of the compute.  Claude is also done it\'s work.'
(evidence/'director-invocation.txt').write_text(invocation,encoding='utf-8')
notes=page/'06.09.notes.md';assert not notes.exists();notes.write_text('''# 06.09.notes - Current Prime operator pilot
date: 2026-11-02
who: Codex Prime
state: invoked; setup then prepare, judgment authored separately before record

Director invoked the pilot in chat; exact text is evidence/lab05.11/director-invocation.txt. Scope: preserved external copy of real legacy 0182 material, no live approval or write. Method: verify frozen inputs/source hashes, copy exact member, declare pilot assignment/registration, run app describe/prepare, author actual assessment after reading payload, record/render/read in new subprocesses, verify source unchanged and retain all output. Count manual setup operations; no token-cost estimate.
''',encoding='utf-8')
src=work/'0182.desk-app-integration-design-0501';before=fingerprints(src);source_page=work/'0519.desk-app/05.01.md';dump(evidence/'source-fingerprints-before.json',{'member':before,'source_page':sha(source_page.read_bytes())})
shutil.copytree(src,book/src.name);assert fingerprints(book/src.name)==before
(evidence/'source-review-page.md').write_bytes(source_page.read_bytes())
(book/'assignment.txt').write_text('Current Codex Prime staged operator replay: assess what the copied 0182 design return and payload establish, distinguish historical proposal from current execution, and preserve actual judgment/next action through the app. Do not approve or modify the live 0519 work, infer task association from custody, or claim an autonomous workflow.\n',encoding='utf-8')
(book/'note.md').write_text('The copied return and payload retain their original bytes/identities. This is an informed historical-material operator replay. Custody labels do not authenticate Prime or establish the review task. All source originals remain untouched.\n',encoding='utf-8')
target=book/'0519.desk-app/05.01.md';target.parent.mkdir();target.write_text('# PILOT ONLY - copied-work operator review\n\nThis new review target belongs only to the external pilot book. It is not the original substantive review.\n\n## Return pointer\nPENDING.\n\n## Review - Codex Prime\nPENDING.\n\n## Notes\nPreserve this staged book and the original source.\n',encoding='utf-8')
def app(label,args):
    cmd=[sys.executable,'-B',str(root/'app/librarian.py'),'review-loop',*args];p=subprocess.run(cmd,cwd=str(root),capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=60)
    (evidence/(label+'.stdout')).write_bytes(p.stdout);(evidence/(label+'.stderr')).write_bytes(p.stderr);dump(evidence/(label+'.command.json'),{'argv':cmd,'exit':p.returncode});assert p.returncode==0,(label,p.stderr.decode(errors='replace'));return json.loads(p.stdout)
described=app('01-describe',['describe-legacy','--book',str(book),'--member',src.name]);descriptor=described['descriptor'];dump(book/'descriptor.json',descriptor)
reg=json.loads((root/'labs/prime-entry-pilot-pass01/example-registration.json').read_text(encoding='utf-8'))
reg['agreement']={'goal':'Assess copied real design evidence and operate the app without changing original work.','finish_criteria':[{'id':'preserve','text':'Original member and source page hashes unchanged; pilot judgment recovered from a new process.'}],'scope':'Only the external pilot copy; no live approval, filing or migration.','prime_discretion':'Prime authors the evidence-backed operator assessment and records it on the pilot target.','director_required':'Any live-book change or policy fork needs separate Director direction.','recorded_decisions':[{'id':'PILOT-D1','source_sha256':sha(invocation.encode()),'text':'The Director invoked this staged operator pilot; original work remains untouched.'}]}
reg['goal']={'goal_id':'prime-operator-copy-0182','statement':'Operate the app on copied real material and expose manual friction.','terminal':'open','evidence':[]};reg['work_id']='prime-operator-copy-0182';reg['task_id']='prime-operator-0707-0509'
dump(book/'registration.json',reg);dump(book/'request.json',{'schema':'review-loop-request/1','registration_path':'registration.json'})
prepared=app('02-prepare',['prepare','--fixture-root',str(book),'--request','request.json']);assert isinstance(prepared['view']['template'],dict)
dump(evidence/'prepare-template.json',prepared['view']['template'])
dump(evidence/'setup-summary.json',{'book':str(book),'descriptor_state':described.get('state'),'task_association':described.get('task_association'),'template_available':True,'target_state':prepared['target']['state'],'manual_setup_operations':['input manifest verification','source fingerprint','exact member copy','explicit pilot target','assignment/scope/evidence text','descriptor extraction through app','registration/agreement/request authored','prepare via app; inspect actual template'],'next':'Prime reads real payload and authors judgment before recording.'})
print(json.dumps({'book':str(book),'prepared':prepared['target'],'custody':described.get('task_association'),'payload':str(book/src.name/'payload'),'evidence':str(evidence)}))
