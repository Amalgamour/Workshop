from pathlib import Path
import importlib.util,sys,json,subprocess,hashlib
R=Path(r'D:\Git\lib-build'); O=Path(r'D:\librarian\temp\two-integration-reviews-nov01')
def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
m=load('probe_fixture',R/'labs/review-loop-pass01/test_review_loop.py');m.PY=Path(sys.executable)
c=load('probe_cycle',R/'labs/prime-cycle-pass02/prime_cycle.py')
sys.path.insert(0,str(R/'labs/return-lines-pass01'));import return_lines as rl
fix=m.Fixture(); root=fix.root
try:
 initial=c.observe_descriptor(root,c.load_registration(root,'registration.json')) if hasattr(c,'load_registration') else None
except Exception as e:initial={'probe_error':str(e)}
# Use registration parser via CLI's existing fixture path in the generated fixture.
(root/'source-return.md').write_bytes(b'SYNTHETIC REAL CAPTURE\n'); (root/'note.md').write_bytes(b'NOTE\n')
rl.init_run(str(root),'00.00.10.work')
rl.reserve_run(str(root),fix.page_id,'05.01','synthetic-0522',['note.md'],'grok-1','codex-prime','prepared',None)
r=rl.capture_run(str(root),fix.page_id,'05.01','synthetic-0522',str(root/'source-return.md'),[('note.md',str(root/'note.md'))]);assert r['exit']==0
m.write_json(root/'descriptor.json',r['descriptor'])
p,v=fix.call('cross-lane-real-descriptor','prepare')
res={'real_capture':r,'consumer_exit':p.returncode,'consumer_view':v,'stderr':p.stderr.decode(errors='replace'),'initial':initial}
(O/'cross-lane-probe.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'capture_state':r['state'],'descriptor':r['descriptor'],'consumer_exit':p.returncode,'consumer_view':v},ensure_ascii=False)[:5500])
# Retain this disposable fixture as probe evidence.
(O/'cross-lane-fixture-path.txt').write_text(str(root),encoding='utf-8')
