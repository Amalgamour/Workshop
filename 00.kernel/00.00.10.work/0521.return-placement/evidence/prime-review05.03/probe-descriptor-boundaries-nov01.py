from pathlib import Path
import json,importlib.util,sys,shutil
R=Path(r'D:\Git\lib-build'); O=Path(r'D:\librarian\temp\two-integration-reviews-nov01')
p=R/'labs/review-loop-pass01/test_review_loop.py';s=importlib.util.spec_from_file_location('extra_probe',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);m.PY=Path(sys.executable)
base=Path((O/'cross-lane-fixture-path.txt').read_text()); cases=[]
for label in ['target-only','target-and-custody-file','unrelated-receipt']:
 dest=O/('probe-'+label);shutil.copytree(base,dest);d=json.loads((dest/'descriptor.json').read_text())
 d['target_page']='0599.synth-lab/05.01.md'
 if label!='target-only':
  (dest/'custody-placeholder.txt').write_bytes(b'NOT VERIFIED CUSTODY\n');d['custody_path']='custody-placeholder.txt'
 if label=='unrelated-receipt':
  receipt=b'{"origin":{"book":"wrong","page":"0501.other","batch":"05.99"},"schema":"not-a-receipt"}\n'
  (dest/'unrelated-receipt.json').write_bytes(receipt);d['receipt_path']='unrelated-receipt.json';d['receipt_sha256']=m.sha(receipt)
 m.write_json(dest/'descriptor.json',d)
 r=m.run(label,m.LOOP,['prepare','--fixture-root',str(dest),'--request','request.json']);v=m.as_json(r)
 cases.append({'case':label,'qualification':'diagnostic descriptor modification only, not a valid emitted descriptor or a proposed workaround','exit':r.returncode,'result':v})
(O/'descriptor-diagnostic-probes.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'case':x['case'],'exit':x['exit'],'state':x['result'].get('pass_state'),'observation':x['result'].get('observation')} for x in cases],ensure_ascii=False))
