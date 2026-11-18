from pathlib import Path
import os,sys,json,subprocess,importlib.util
root=Path(r'D:\Git\lib-build');out=Path(r'D:\librarian\temp\app-0509-review-nov02');alias=out/'checkout-alias';assert not os.path.lexists(alias)
spec=importlib.util.spec_from_file_location('reviewed_door_probe',root/'app/review_loop_tools_v3.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
p=subprocess.run(['cmd','/c','mklink','/J',str(alias),str(root)],capture_output=True)
assert p.returncode==0,p.stderr
try:
    assert alias.is_junction() and alias.resolve()==root.resolve()
    candidate=alias/'labs'
    try:r={'result':'ACCEPTED','returned':str(m.disposable_root(str(candidate)))}
    except m.Refuse as exc:r={'result':'REFUSED','reason':str(exc)}
    r.update({'probe':'static fixture-root validation only','lexical':str(candidate),'resolved':str(candidate.resolve()),'loop_launched':False,'writes_through_alias':False})
    (out/'ancestor-junction-probe.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps(r))
finally:
    assert alias.is_junction() and alias.resolve()==root.resolve()
    os.rmdir(alias)
