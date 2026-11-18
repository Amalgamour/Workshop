from pathlib import Path
import json, hashlib, subprocess,sys,concurrent.futures
R=Path(r'D:\Git\lib-build'); O=Path(r'D:\librarian\temp\two-integration-reviews-nov01'); O.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
checks={}
for page in ['0521.return-placement','0522.review-construction']:
 p=R/'00.kernel/00.00.10.work'/page; m=json.loads((p/'evidence/build05.03/artifact-manifest.json').read_text(encoding='utf-8')); rows=[]
 for row in m['files']:
  f=R/row['path']; b=f.read_bytes() if f.is_file() else b''; rows.append({'path':row['path'],'matches':None if row['sha256'] is None else f.is_file() and sha(b)==row['sha256'] and len(b)==row['bytes'], 'note':'declared self row; independently hash manifest via pointer' if row['sha256'] is None else ''})
 pins=json.loads((p/'evidence/pack05.03/source-manifest.json').read_text(encoding='utf-8'));checks[page]={'artifacts':rows,'pack_source_rows':len(pins.get('sources',[]))}
(O/'manifest-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
wrapper=O/'run-review-loop.py'
wrapper.write_text('''import importlib.util,unittest,sys,json\nfrom pathlib import Path\np=Path(r"D:\\Git\\lib-build\\labs\\review-loop-pass01\\test_review_loop.py")\ns=importlib.util.spec_from_file_location("review_loop_test_independent",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)\nm.PY=Path(sys.executable)\nr=unittest.TextTestRunner(verbosity=2).run(m.load_tests(None,None,None))\nPath(r"D:\\librarian\\temp\\two-integration-reviews-nov01\\independent-loop-transcript.json").write_text(json.dumps(m.LOG,ensure_ascii=False,indent=2),encoding="utf-8")\nsys.exit(not r.wasSuccessful())\n''',encoding='utf-8')
def run(name,args):
 r=subprocess.run([sys.executable,'-B','-X','utf8',*args],cwd=R,capture_output=True);(O/(name+'.stdout')).write_bytes(r.stdout);(O/(name+'.stderr')).write_bytes(r.stderr);return {'name':name,'exit':r.returncode}
jobs=[('return-lines-tests',['-m','unittest','discover','-s','labs/return-lines-pass01/tests','-v']),('review-loop-tests',[str(wrapper)])]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: results=list(pool.map(lambda x:run(*x),jobs))
(O/'test-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps({'artifacts':{k:{'count':len(v['artifacts']),'bad':[r for r in v['artifacts'] if r['matches'] is False]} for k,v in checks.items()},'tests':results}))
