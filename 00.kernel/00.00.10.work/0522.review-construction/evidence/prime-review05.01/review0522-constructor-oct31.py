from pathlib import Path
import json,hashlib,os,sys,subprocess,importlib.util,tempfile,unittest
R=Path(r'D:\Git\lib-build');P=R/'00.kernel/00.00.10.work/0522.review-construction'
O=Path(r'D:\librarian\temp\review0522-constructor');O.mkdir(exist_ok=False);(O/'scratch').mkdir();(O/'tests').mkdir()
os.environ['TEMP']=str(O/'scratch');os.environ['TMP']=str(O/'scratch');os.environ['PYTHONDONTWRITEBYTECODE']='1';tempfile.tempdir=str(O/'scratch')
rows=json.loads((P/'evidence/build05.01/artifact-manifest.json').read_text(encoding='utf-8'))['files'];checks={'artifacts':[]}
for row in rows:
    if row['sha256'] is None:continue
    b=(R/row['path']).read_bytes();same=len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    assert same,row['path'];checks['artifacts'].append({'path':row['path'],'matches':same})
spec=importlib.util.spec_from_file_location('constructor_tests',R/'labs/review-construction-pass01/test_construct.py');T=importlib.util.module_from_spec(spec);spec.loader.exec_module(T)
# Test teardown writes evidence. Redirect it before running to preserve builder bytes.
T.EVIDENCE=O/'tests'
with open(O/'tests.log','w',encoding='utf-8') as stream:
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(T))
checks['tests']={'run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped)}
probes=[]
def command(name,world):
    world.save();q=subprocess.run([sys.executable,'-B',str(T.SCRIPT),'apply','--fixture-root',str(world.root),'--input','input.json'],capture_output=True)
    (O/(name+'.stdout')).write_bytes(q.stdout);(O/(name+'.stderr')).write_bytes(q.stderr)
    probes.append({'name':name,'exit':q.returncode,'fixture_root':str(world.root),'stdout':q.stdout.decode('utf-8','replace'),'stderr':q.stderr.decode('utf-8','replace')})
w=T.World('none');wrong=w.root/'0588.wrong-page/05.01.md';wrong.parent.mkdir();wrong.write_bytes(w.page.read_bytes());w.envelope['target']='0588.wrong-page/05.01.md';command('wrong-target',w)
w=T.World('none');w.envelope['receipt']['member']='0188.unrelated-subject'
for row in w.envelope['record']['sources']:
    if row.get('kind')=='capture':row['identity']['member']='0188.unrelated-subject'
command('wrong-return-line',w)
w=T.World('none');w.envelope['page']='00.kernel/00.00.10.work/1599.synth-lab/05.01.md';command('nonzero-prefix',w)
(O/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
(O/'probes.json').write_text(json.dumps(probes,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'tests':checks['tests'],'artifacts':len(checks['artifacts']),'probes':[{'name':p['name'],'exit':p['exit']} for p in probes]},indent=2))
