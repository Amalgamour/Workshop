import sys,json,traceback,importlib.util
from pathlib import Path
root=Path(r'D:\Git\lib-build');here=root/'colab/labs/0707.app-use-check/pass05'
out=Path(r'D:\librarian\temp\harness-pass05-review-nov01')
sys.path.insert(0,str(here));import harness5 as H
base=json.loads((here/'candidate.config.json').read_text())
results=[]
for label in ['nul-output-path','deep-json']:
    try:
        if label=='nul-output-path':
            cfg=dict(base);cfg['output_root']='D:\\librarian\\temp\\bad\x00path'
            H.validate_config(cfg);value=H.preflight(cfg)
        else:
            value=H.parse_config(b'['*1200+b'0'+b']'*1200)
        results.append({'probe':label,'result':value})
    except Exception as exc:
        results.append({'probe':label,'exception':type(exc).__name__,'detail':str(exc),'traceback':traceback.format_exc()})
(out/'additional-negatives.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps(results,indent=2))
