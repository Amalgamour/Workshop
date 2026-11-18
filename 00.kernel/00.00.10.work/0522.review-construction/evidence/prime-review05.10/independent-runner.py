from pathlib import Path
import sys,json,hashlib,importlib.util,unittest,difflib
root=Path(r'D:\Git\lib-build');page=root/'00.kernel/00.00.10.work/0522.review-construction';out=Path(r'D:\librarian\temp\app-0510-review-nov02');out.mkdir(exist_ok=False)
expected={'app/librarian.py','app/README.md'};checks=[]
for name,path in [('sources',page/'evidence/pack05.10/source-manifest.json'),('artifacts',page/'evidence/build05.10/artifact-manifest.json')]:
    rows=json.loads(path.read_text(encoding='utf-8'))['files'];changed=[];snapshot_bad=[]
    for row in rows:
        b=(root/row['path']).read_bytes()
        if len(b)!=row['bytes'] or hashlib.sha256(b).hexdigest()!=row['sha256']:changed.append(row['path'])
        if row.get('snapshot'):
            s=(root/row['snapshot']).read_bytes()
            if len(s)!=row['bytes'] or hashlib.sha256(s).hexdigest()!=row['sha256']:snapshot_bad.append(row['path'])
    checks.append({'manifest':name,'rows':len(rows),'changed_live':changed,'bad_snapshots':snapshot_bad})
assert set(checks[0]['changed_live'])==expected and not checks[0]['bad_snapshots'] and not checks[1]['changed_live']
old=(page/'evidence/build05.10/before/librarian.py').read_bytes();new=(root/'app/librarian.py').read_bytes()
assert old.replace(b'review_loop_tools_v3',b'review_loop_tools_v4')==new
for filename in ['librarian.py','README.md']:
    a=(page/'evidence/build05.10/before'/filename).read_text(encoding='utf-8').splitlines(keepends=True);b=(root/'app'/filename).read_text(encoding='utf-8').splitlines(keepends=True)
    (out/(filename+'.diff')).write_text(''.join(difflib.unified_diff(a,b,fromfile='before/'+filename,tofile='app/'+filename)),encoding='utf-8')
(out/'integrity.json').write_text(json.dumps(checks,indent=2),encoding='utf-8');print(json.dumps(checks),flush=True)
spec=importlib.util.spec_from_file_location('prime_app_tests',root/'app/tests/test_review_loop_entry_v4.py');m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m);m.PY=Path(sys.executable)
with (out/'suite.log').open('w',encoding='utf-8') as stream:r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(m.ReviewLoopEntryV4Tests))
(out/'calls.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in m.LOG),encoding='utf-8')
summary={'tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'skipped':len(r.skipped),'ok':r.wasSuccessful(),'python':sys.version};(out/'result.json').write_text(json.dumps(summary,indent=2),encoding='utf-8');print(json.dumps(summary),flush=True);sys.exit(0 if r.wasSuccessful() else 1)

