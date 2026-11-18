from pathlib import Path
import importlib.util,json,subprocess,sys,hashlib
R=Path(r'D:\Git\lib-build');L=Path(r'D:\librarian\temp\reviews-claude-g2-nov01')
s=importlib.util.spec_from_file_location('focused_fixture',R/'labs/review-construction-pass03/tests/test_pass03.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
f=m.Fixture();f.setUp()
b=f.envelope(None,'review-construction/2',m.supplied());b['supplied_review_state']['disposition']=[]
f.write_input('invalid-enum.json',b)
before=hashlib.sha256((f.root/'0599.synth-lab/05.01.md').read_bytes()).hexdigest()
p=subprocess.run([sys.executable,'-B',str(m.PASS03),'preview','--fixture-root',str(f.root),'--input','invalid-enum.json'],cwd=R,capture_output=True)
(L/'malformed-cli.stdout').write_bytes(p.stdout);(L/'malformed-cli.stderr').write_bytes(p.stderr)
out={'exit':p.returncode,'traceback':b'Traceback' in p.stderr,'target_unchanged':before==hashlib.sha256((f.root/'0599.synth-lab/05.01.md').read_bytes()).hexdigest(),'fixture_retained':str(f.root)}
(L/'malformed-cli.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
