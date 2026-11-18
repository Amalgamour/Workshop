from pathlib import Path
import json,hashlib,subprocess,sys,os
R=Path(r'D:\Git\lib-build');O=Path(r'D:\librarian\temp\cloud-core-reliability-review-nov01');S=O/'source';commit='dd4cd00a7c4e75b66e3a0716d564a19e5beca59f';P=S/'00.kernel/00.00.10.work/0523.desk-core';m=json.loads((P/'evidence/pack05.01/source-manifest.json').read_text())
rows=[]
for r in m['sources']:
 b=subprocess.check_output(['git','-C',str(R),'cat-file','blob',commit+':'+r['path']]);assert hashlib.sha256(b).hexdigest()==r['sha256'] and len(b)==r['bytes'];f=S/r['path'];f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b);rows.append({'path':r['path'],'matches':True})
env=dict(os.environ,TEMP=str(O/'scratch'),TMP=str(O/'scratch'),PYTHONDONTWRITEBYTECODE='1');env.pop('DESK_CORE_FAULT',None)
p=subprocess.run([sys.executable,'-B','-X','utf8','-m','unittest','app.desk_core.test_loop.DeskCoreLoop.test_pins_and_live_book_and_undeclared','-v'],cwd=S,env=env,capture_output=True);(O/'pins-recheck.stdout').write_bytes(p.stdout);(O/'pins-recheck.stderr').write_bytes(p.stderr)
(O/'export-correction.json').write_text(json.dumps({'reason':'Prime initial review export omitted 33 original pinned reference files outside the prototype prefix; initial failed test retained, no submitted-code edit','hydrated_original_sources':rows,'affected_test_exit':p.returncode,'scope':'reran only affected dependency test; other 21 tests and native demo already passed'},indent=2),encoding='utf-8');print('Original pins',len(rows),'affected recheck exit',p.returncode)
