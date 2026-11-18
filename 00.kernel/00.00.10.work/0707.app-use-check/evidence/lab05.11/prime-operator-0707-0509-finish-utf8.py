from pathlib import Path
import json,hashlib,sys,subprocess,os
root=Path(r'D:\Git\lib-build');work=root/'00.kernel/00.10.work' if False else root/'00.kernel/00.00.10.work';evidence=work/'0707.app-use-check/evidence/lab05.11';book=Path(r'D:\librarian\temp\prime-operator-0707-0509')
def sha(b):return hashlib.sha256(b).hexdigest()
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
decision=json.loads((book/'decision.json').read_text(encoding='utf-8'));a=json.loads((evidence/'authored-judgment.json').read_text(encoding='utf-8'));section=a['sections'].copy()
section['tests_note']+=' '+section['tests_passed'];section['tests_passed']=None
for key in ['options','assumptions','open_questions','remaining_choices']:section[key]=[section[key]] if not section[key].startswith('Not applicable') else []
section['affected']=[{'action_id':'pilot-copy-review','dependency':section['affected']}]
section['finish_assessments']=[{'criterion_id':'preserve','assessment':'unknown'}]
for key in ['for_model','question','proposed_plan','findings_account']:section[key]=None
decision['judgment']['sections']=section;decision['supplied_record']['judgment']['sections']=section
a['sections']=section
assert decision['judgment']['finding']==a['finding'] and decision['judgment']['reasons']==a['reasons']
assert not (book/'decision.003.json').exists();dump(book/'decision.003.json',decision);dump(evidence/'authored-judgment.003.json',a)
scratch=book/'scratch/envelope.json'
if scratch.exists():(evidence/'second-refused-envelope.json').write_bytes(scratch.read_bytes())
dump(evidence/'input-correction.003.json',{'first_attempt':'03-record exit 2, bad type tests_passed; no committed cycle files','first_input_preserved':'decision.json','corrected_input':'decision.003.json','meaning_unchanged':True,'correction':'Typed sections match parse_sections: bool/null tests_passed; lists/options; affected objects; assessment objects; unused structured fields null. Original prose remains in authored-judgment.json.','production_code_changed':False})
def app(label,command):
    cmd=[sys.executable,'-B',str(root/'app/librarian.py'),'review-loop',command,'--fixture-root',str(book),'--request','request.json']
    if command=='record':cmd+=['--decision','decision.003.json']
    p=subprocess.run(cmd,cwd=str(root),capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=90)
    (evidence/(label+'.stdout')).write_bytes(p.stdout);(evidence/(label+'.stderr')).write_bytes(p.stderr);dump(evidence/(label+'.command.json'),{'argv':cmd,'exit':p.returncode})
    assert p.returncode==0,(label,p.stdout.decode(errors='replace')[:600],p.stderr.decode(errors='replace')[:600]);return json.loads(p.stdout)
recorded=app('03c-record-utf8-corrected','record');rendered=app('04-render','render');read=app('05-read-new-process','read');recover=app('06-recover-new-process','recover');again=app('07-read-after-recover','read')
assert read['supplied_next_action']['text']==a['next_action']==again['supplied_next_action']['text']
assert read['next']==read['mechanical']['text']==again['next'] and recover['render']['result']=='already-rendered' and recover['render']['apply_called'] is False
stored=json.loads((book/'cycle/05.01-r1/record.json').read_text(encoding='utf-8'));assert stored['decision']['judgment']['finding']==a['finding'] and stored['decision']['judgment']['disposition']=='held'
for b in [recorded,rendered,read,recover,again]:assert b['accepted'] is False and b['authority']=='none' and b['custody']=='not-established'
def fp(p):return {f.relative_to(p).as_posix():{'bytes':len(f.read_bytes()),'sha256':sha(f.read_bytes())} for f in p.rglob('*') if f.is_file()}
src=work/'0182.desk-app-integration-design-0501';before=json.loads((evidence/'source-fingerprints-before.json').read_text(encoding='utf-8'));after={'member':fp(src),'source_page':sha((work/'0519.desk-app/05.01.md').read_bytes())};assert before==after;dump(evidence/'source-fingerprints-after.json',after)
dump(evidence/'operator-result.json',{'first_record_refused':True,'corrected_input_preserved_separately':True,'recorded':recorded['record']['result'],'rendered':rendered['render']['result'],'restart_read_verified':read['committed_check']['verified'],'stored_actual_judgment_exact':True,'supplied_next':a['next_action'],'mechanical_next':read['next'],'recover_applied':recover['render']['apply_called'],'original_sources_unchanged':True,'book_preserved':str(book),'live_review_completed':False,'fresh_model_booted':False})
print((evidence/'operator-result.json').read_text(encoding='utf-8'))

