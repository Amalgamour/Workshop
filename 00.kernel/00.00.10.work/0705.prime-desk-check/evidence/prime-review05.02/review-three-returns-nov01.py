from pathlib import Path
import json,hashlib,subprocess,sys,concurrent.futures
R=Path(r'D:\Git\lib-build');O=Path(r'D:\librarian\temp\three-return-reviews-nov01');O.mkdir(exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
checks={}
for name,build in [('0524.prime-desk','build05.01'),('0522.review-construction','build05.04')]:
 p=R/'00.kernel/00.00.10.work'/name;raw=json.loads((p/'evidence'/build/'artifact-manifest.json').read_text());rows=[]
 for r in raw['files']:
  f=R/r['path'];b=f.read_bytes() if f.is_file() else b'';rows.append({'path':r['path'],'match':None if r['sha256'] is None else f.is_file() and sha(b)==r['sha256'] and len(b)==r['bytes']})
 checks[name]=rows
(O/'manifest-checks.json').write_text(json.dumps(checks,indent=2),encoding='utf-8')
w=O/'run-loop-tests.py';w.write_text('''import importlib.util,unittest,sys,json\nfrom pathlib import Path\np=Path(r"D:\\Git\\lib-build\\labs\\review-loop-pass02\\test_review_loop.py");s=importlib.util.spec_from_file_location("independent_loop04",p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.PY=Path(sys.executable)\nr=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(m.ReviewLoopTests))\nPath(r"D:\\librarian\\temp\\three-return-reviews-nov01\\loop-commands.json").write_text(json.dumps(m.LOG,ensure_ascii=False,indent=2),encoding="utf-8")\nsys.exit(not r.wasSuccessful())\n''',encoding='utf-8')
def run(name,args):
 p=subprocess.run([sys.executable,'-B','-X','utf8',*args],cwd=R,capture_output=True);(O/(name+'.stdout')).write_bytes(p.stdout);(O/(name+'.stderr')).write_bytes(p.stderr);return {'name':name,'exit':p.returncode}
lab=R/'colab/labs/0705.prime-desk-check/pass02'
jobs=[('desk-tests',['-m','unittest','discover','-s','labs/prime-desk-pass01/tests','-v']),('loop-tests',[str(w)]),('claude-tests',[str(lab/'tests/test_lab.py'),'--pack-manifest',str(R/'00.kernel/00.00.10.work/0705.prime-desk-check/evidence/pack05.02/source-manifest.json'),'--report',str(O/'claude-selftest.json')])]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:res=list(pool.map(lambda t:run(*t),jobs))
(O/'test-results.json').write_text(json.dumps(res,indent=2),encoding='utf-8');print(json.dumps({'artifacts':{k:{'rows':len(v),'bad':[r for r in v if r['match'] is False]} for k,v in checks.items()},'tests':res}))
