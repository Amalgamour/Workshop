from pathlib import Path
import json,hashlib,subprocess,sys,os
R=Path(r'D:\Git\lib-build');P=R/'00.kernel/00.00.10.work/0520.desk-loop-lab'
O=Path(r'D:\librarian\temp\review0520-lab');O.mkdir(exist_ok=False);(O/'scratch').mkdir()
m=json.loads((P/'evidence/build05.01/artifact-manifest.json').read_text(encoding='utf-8'))
rows=[m['return_file']]+m['capture_artifacts']+m['local_not_in_capture_command'];checked=[]
for row in rows:
    if row['sha256'] is None:continue
    b=(R/row['path']).read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
    checked.append(row)
original=P/'evidence/build05.01/transcript.json';before=hashlib.sha256(original.read_bytes()).hexdigest()
env=dict(os.environ,TEMP=str(O/'scratch'),TMP=str(O/'scratch'),PYTHONDONTWRITEBYTECODE='1')
checks={'artifacts':checked}
for name,args in [('capture-verify',[str(R/'labs/return-capture-pass01/return_capture.py'),'verify','--book',str(R/'00.kernel/00.00.10.work'),'--member','0183.desk-loop-independent-lab-0501']),
                  ('replay',[str(R/'labs/desk-loop-replay-pass01/replay.py'),'--transcript',str(O/'independent-transcript.json')])]:
    q=subprocess.run([sys.executable,'-B',*args],env=env,capture_output=True,cwd=R)
    (O/(name+'.stdout')).write_bytes(q.stdout);(O/(name+'.stderr')).write_bytes(q.stderr)
    checks[name]={'exit':q.returncode};print(name,q.returncode,flush=True)
assert hashlib.sha256(original.read_bytes()).hexdigest()==before
checks['builder_transcript_unchanged']=True
(O/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
if checks['replay']['exit']==0:
    transcript=json.loads((O/'independent-transcript.json').read_text(encoding='utf-8'))
    assert len(transcript['checks'])==16 and all(x['ok'] for x in transcript['checks'])
    print('16 independent route checks passed; builder transcript preserved.')
