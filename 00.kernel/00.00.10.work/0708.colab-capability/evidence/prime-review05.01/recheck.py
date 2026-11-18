from pathlib import Path
import json,subprocess,sys
R=Path(r'D:\Git\lib-build'); L=Path(r'D:\librarian\temp\prime-overhead-0708'); E=R/'00.kernel/00.00.10.work/0708.colab-capability/evidence/build05.01'; O=Path(r'C:\Users\misg\AppData\Local\Temp\0708-colab-capability\out')
cfg=json.loads((E/'fixtures/config.json').read_text());cfg['python']=sys.executable
(L/'config.json').write_text(json.dumps(cfg))
rows=[]
for name,args in [('handoff',['labs/colab-support-pass02/handoff_check.py','check','--output',str(O),'--expected-digest','058fed372869e9c47512a11addd27a88b7ffaf33433c4c1c964e88da9b9dd277','--json']),('verify',['labs/colab-support-pass02/colab_support.py','verify','--output',str(O),'--config',str(L/'config.json'),'--json'])]:
 p=subprocess.run([sys.executable,'-B',*args],cwd=R,capture_output=True)
 (L/f'{name}.stdout').write_bytes(p.stdout);(L/f'{name}.stderr').write_bytes(p.stderr)
 try:d=json.loads(p.stdout)
 except Exception:d={}
 rows.append({'name':name,'exit':p.returncode,'result':d.get('result'),'findings':d.get('findings',d.get('problems')),'stderr_bytes':len(p.stderr)})
(L/'independent-checks.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
