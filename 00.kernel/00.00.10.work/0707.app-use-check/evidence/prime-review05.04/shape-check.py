from pathlib import Path
import json,sys,importlib.util,hashlib
R=Path(r'D:\Git\lib-build');L=Path(r'D:\librarian\temp\workflow-and-harness-review-nov01');lab=R/'colab/labs/0707.app-use-check/pass04'
s=importlib.util.spec_from_file_location('shape_preflight',lab/'harness.py');h=importlib.util.module_from_spec(s);s.loader.exec_module(h)
cfg=json.loads((L/'native-harness-config.json').read_text());stub=lab/'stubs/STUB_loop.py';b=stub.read_bytes()
cfg.update(kind='stub',candidate={'path':str(stub),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)},output_root=str(L/'harness-scratch'),dependencies=None)
try:r={'result':h.preflight(cfg,'stub')}
except Exception as e:r={'uncaught':type(e).__name__,'detail':str(e)}
(L/'shape-preflight.json').write_text(json.dumps(r,indent=2));print(json.dumps(r))
