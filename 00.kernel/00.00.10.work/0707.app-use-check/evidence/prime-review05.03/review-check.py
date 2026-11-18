from pathlib import Path
import json,hashlib,importlib.util,copy,subprocess,sys,shutil
R=Path(r'D:\Git\lib-build');P=R/'00.kernel/00.00.10.work/0707.app-use-check'
L=Path(r'D:\librarian\temp\claude-loop03-review-nov01');L.mkdir(exist_ok=False)
results={}
for kind,path in [('sources',P/'evidence/pack05.03/source-manifest.json'),('artifacts',P/'evidence/design05.03/artifact-manifest.json')]:
 rows=json.loads(path.read_text(encoding='utf-8-sig'))['files'];bad=[]
 for row in rows:
  for key in (['path','snapshot'] if kind=='sources' else ['path']):
   b=(R/row[key]).read_bytes()
   if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:bad.append(row[key])
 results[kind]={'rows':len(rows),'bad':bad}
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
lab=R/'colab/labs/0707.app-use-check/pass03'
runner=load('loop_probe',lab/'run_probe.py');runner.RUNS=L/'independent-runs';runner.SCRATCH=L/'scratch'
code=runner.main();results['independent_probe']={'exit':code}
rules=load('loop_rules_check',lab/'loop_rules.py')
run=next((L/'independent-runs').iterdir());I=run/'inputs'
rb=(I/'record.json').read_bytes();record=json.loads(rb)
com=json.loads((I/'COMMITTED.json').read_bytes());reg=json.loads((I/'registration.json').read_bytes());latest=json.loads((I/'A-read.stdout').read_bytes())['current']['latest_review']
env=rules.envelope_v2(json.loads((I/'envelope.json').read_bytes()),record['decision'])
changed=copy.deepcopy(env);changed['task']['task_id']='different-task-synthetic'
try:results['changed_task_precheck']=rules.verify_committed(rb,com,latest,changed,reg)
except Exception as exc:results['changed_task_precheck']={'refused':str(exc)}
results['absent_before_record_message']=rules.mechanical({'pass_state':'awaiting-review'},{'state':'absent'})
source=P/'evidence/build05.01/runs/run1/books/A.after-render'
fixture=L/'binding-fixture';shutil.copytree(source,fixture)
binds={}
for name,body in [('original',env),('changed-task',changed)]:
 (fixture/(name+'.json')).write_text(json.dumps(body),encoding='utf-8')
 proc=subprocess.run([sys.executable,'-B',str(R/'labs/review-construction-pass04/construct.py'),'bind','--fixture-root',str(fixture),'--input',name+'.json'],cwd=R,capture_output=True)
 (L/(name+'.stdout')).write_bytes(proc.stdout);(L/(name+'.stderr')).write_bytes(proc.stderr)
 binds[name]={'exit':proc.returncode,'binding':json.loads(proc.stdout).get('binding_sha256') if proc.returncode==0 else None}
results['actual_envelope_bindings']=binds
(L/'checks.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps(results,indent=2))
