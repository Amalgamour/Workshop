from pathlib import Path
import json,hashlib,subprocess,sys,concurrent.futures
R=Path(r'D:\Git\lib-build');O=Path(r'D:\librarian\temp\two-prime-returns-review-nov01');O.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
checks={}
for page,pack,build,batch in [('0524.prime-desk','pack05.02','build05.02','05.02.md'),('0522.review-construction','pack05.05','build05.05','05.05.md')]:
 P=R/'00.kernel/00.00.10.work'/page;pin=P/'evidence'/pack;pm=json.loads((pin/'source-manifest.json').read_text());pins=[]
 for r in pm['sources']:
  b=(pin/r['snapshot']).read_bytes();pins.append({'path':r['path'],'snapshot_matches':len(b)==r['bytes'] and sha(b)==r['sha256'],'live_equal':(R/r['path']).read_bytes()==b})
 am=P/'evidence'/build/'artifact-manifest.json';a=json.loads(am.read_text());arts=[]
 for r in a.get('files',a.get('artifacts',[])):
  b=(R/r['path']).read_bytes();arts.append({'path':r['path'],'matches':r.get('sha256') is None or len(b)==r['bytes'] and sha(b)==r['sha256']})
 ptr=(P/batch).read_text(encoding='utf-8');ptrs={f.name:sha(f.read_bytes()) in ptr for f in [am,P/'evidence'/build/'submission.md']};checks[page]={'pins':pins,'artifacts':arts,'pointers':ptrs};assert all(p['snapshot_matches'] for p in pins) and all(a['matches'] for a in arts) and all(ptrs.values())
(O/'checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
w=O/'run-entry-tests.py';w.write_text('''from pathlib import Path\nimport importlib.util,unittest,sys,json\np=Path(r"D:\\Git\\lib-build\\app\\tests\\test_review_loop_entry_v2.py");s=importlib.util.spec_from_file_location("independent_review_entry05",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.PY=Path(sys.executable)\nr=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(m.ReviewLoopEntryTests))\nPath(r"D:\\librarian\\temp\\two-prime-returns-review-nov01\\entry-commands.json").write_text(json.dumps(m.LOG,ensure_ascii=False,indent=2),encoding="utf-8")\nsys.exit(not r.wasSuccessful())\n''',encoding='utf-8')
def run(name,args):
 p=subprocess.run([sys.executable,'-B','-X','utf8',*map(str,args)],cwd=R,capture_output=True);(O/(name+'.stdout')).write_bytes(p.stdout);(O/(name+'.stderr')).write_bytes(p.stderr);return {'name':name,'exit':p.returncode}
jobs=[('desk-tests',['-m','unittest','discover','-s','labs/prime-desk-pass02/tests','-v']),('entry-tests',[w]),('desk-demo',[R/'labs/prime-desk-pass02/demo.py','--out',O/'desk-demo'])]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(lambda x:run(*x),jobs))
(O/'results.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps({'sources':{k:{'pins':len(v['pins']),'artifacts':len(v['artifacts']),'live_changes':[p['path'] for p in v['pins'] if not p['live_equal']]} for k,v in checks.items()},'runs':results},indent=2))
