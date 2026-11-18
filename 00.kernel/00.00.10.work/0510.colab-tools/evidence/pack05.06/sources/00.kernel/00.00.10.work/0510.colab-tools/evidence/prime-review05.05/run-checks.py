from pathlib import Path
import subprocess, sys, json, importlib.util, hashlib, tempfile
R=Path(r'D:\Git\lib-build')
L=Path(__file__).parent
rows=[]
for name,rel in [('constructor','labs/review-construction-pass03/tests/test_pass03.py'),('reserved-rules','colab/labs/0510-reserved-review/pass01/test_reserved_rules.py')]:
 p=subprocess.run([sys.executable,'-B',str(R/rel)],cwd=R,capture_output=True)
 (L/f'{name}.stdout').write_bytes(p.stdout)
 (L/f'{name}.stderr').write_bytes(p.stderr)
 rows.append({'name':name,'exit':p.returncode,'stderr_tail':p.stderr.decode('utf-8','replace').splitlines()[-5:]})
def load(name,rel):
 spec=importlib.util.spec_from_file_location(name,R/rel);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
C=load('constructor','labs/review-construction-pass03/construct.py')
Q=load('reserved','colab/labs/0510-reserved-review/pass01/reserved_rules.py')
with tempfile.TemporaryDirectory(prefix='prime-g2-inspect-') as td:
 root=Path(td); binding='ab'*32
 for newline in ['\n','\r\n']:
  p=root/('crlf.md' if newline=='\r\n' else 'lf.md')
  p.write_bytes(newline.join(['# Synthetic','## Review - Codex Prime','authority: none','task_binding: '+binding,'other body','']).encode())
  before=hashlib.sha256(p.read_bytes()).hexdigest()
  d=C.inspect_target(root,p.name,binding)
  rows.append({'name':'inspect-'+p.name,'state':d['state'],'binding':d['binding_sha256'],'unchanged':before==hashlib.sha256(p.read_bytes()).hexdigest()})
state={'schema':'supplied-review-state/1','source':'cycle decision judgment','disposition':[],'pass_terminal':'open','goal_terminal':'open','outcome':'continue'}
try:C.parse_supplied(state);answer='accepted'
except Exception as e:answer=type(e).__name__+': '+str(e)
rows.append({'name':'malformed-enum-list','observed':answer})
ex=R/'colab/labs/0510-reserved-review/pass01/examples'
raw=(ex/'05.01.return.SYNTHETIC.md').read_bytes().replace(b'\r\n',b'\n')
for n,b in [('LF',raw),('CRLF',raw.replace(b'\n',b'\r\n'))]:
 try:Q.first_findings(b);answer='accepted'
 except Exception as e:answer=type(e).__name__+': '+str(e)
 rows.append({'name':'reserved-block-'+n,'observed':answer})
(L/'checks.json').write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
