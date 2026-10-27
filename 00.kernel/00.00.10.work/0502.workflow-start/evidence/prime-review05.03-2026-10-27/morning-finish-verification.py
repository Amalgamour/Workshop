from pathlib import Path
import hashlib,json,re
W=Path(r'D:\Git\lib-build');O=Path(r'C:\Users\misg\AppData\Local\Temp\prime-morning-20261027-knrpbqum')
counts={}
for rel in ['00.kernel/00.00.10.work/0504.app-entry/evidence/colab05.03','00.kernel/00.00.10.work/0502.workflow-start/evidence/repair05.03']:
 folder=W/rel;n=0
 for line in (folder/'SHA256SUMS.txt').read_text().splitlines():
  m=re.fullmatch(r'([0-9a-f]{64}) (?: |\*)(.+)',line);assert m,line
  expected,name=m.groups();assert hashlib.sha256((folder/name).read_bytes()).hexdigest()==expected,name;n+=1
 counts[rel]=n
cases=json.loads((O/'regressions.json').read_text());assert len(cases)==15 and all(c['meets_repair_contract'] for c in cases)
assert 'Ran 17 tests' in (O/'orientation-tests.stderr.txt').read_text() and '\nOK' in (O/'orientation-tests.stderr.txt').read_text()
summary={'date':'2026-10-27','hardlink':json.loads((O/'hardlink-proof.json').read_text()),'checker_manifest_rows':10,'checker_tests':17,'checker_regressions':15,'evidence_manifests':counts,'model_calls':0,'verification_script_correction':'Initial verifier assumed two-space sha256 format; Colab manifest uses the valid binary *filename format. Adapted manifest parser; no test rerun needed.'}
(O/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
