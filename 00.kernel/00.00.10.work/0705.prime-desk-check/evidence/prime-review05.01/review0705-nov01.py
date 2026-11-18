from pathlib import Path
import json,hashlib,subprocess,sys
R=Path(r'D:\Git\lib-build');C=R/'00.kernel/00.00.10.work/0705.prime-desk-check';O=Path(r'D:\librarian\temp\review0705-nov01');O.mkdir(exist_ok=True);L=R/'colab/labs/0705.prime-desk-check/pass01'
m=json.loads((C/'evidence/pack05.01/source-manifest.json').read_text());pins=[]
for r in m['sources']:
 b=(C/'evidence/pack05.01'/r['snapshot']).read_bytes();pins.append({'path':r['path'],'snapshot_ok':len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'live_equal':(R/r['path']).read_bytes()==b})
pointer=(C/'05.01.pack.md').read_text(encoding='utf-8');outputs=[]
for f in [C/'05.01.return.md',C/'06.01.notes.md',*(C/'evidence/return05.01').iterdir(),*L.iterdir()]:
 if f.is_file():
  b=f.read_bytes();h=hashlib.sha256(b).hexdigest();outputs.append({'path':f.relative_to(R).as_posix(),'bytes':len(b),'sha256':h,'pointer_matches':h in pointer})
fixture=json.loads((L/'cases.json').read_text());mut=json.loads(json.dumps(fixture));mut['cases'][0]['sources'][0]['sha256']='0'*64;mut['cases']=[c for c in mut['cases'] if c['id']!='C14'];(O/'mutated-cases.json').write_text(json.dumps(mut),encoding='utf-8')
runs=[]
for label,file,expected in [('original',L/'cases.json',0),('mutation',O/'mutated-cases.json',1)]:
 args=[sys.executable,'-I','-B',str(L/'check_fixtures.py'),'--cases',str(file),'--manifest',str(C/'evidence/pack05.01/source-manifest.json')];p=subprocess.run(args,capture_output=True);(O/(label+'.stdout')).write_bytes(p.stdout);(O/(label+'.stderr')).write_bytes(p.stderr);runs.append({'label':label,'command':args,'exit':p.returncode,'expected':expected})
# Independently spot-check the expectations; a regex accepts zero-prefix line names too.
checks={'legacy_regex_matches_zero_prefix_matching_line':__import__('re').fullmatch(r'01\d\d\.[a-z0-9][a-z0-9.-]*','0124.prime-desk') is not None,'goal_mojibake_sequence_count':(R/'00.kernel/00.00.10.work/0401.goal/01.md').read_bytes().count(bytes.fromhex('c3a2e282ac')),'director_double_space_quote_present':b'I like it.  I can\'t think of anything' in (R/'00.kernel/00.00.10.work/0420.prime-desk/06.01.md').read_bytes()}
result={'pins':pins,'outputs':outputs,'runs':runs,'independent_checks':checks};(O/'checks.json').write_text(json.dumps(result,indent=2),encoding='utf-8');assert all(p['snapshot_ok'] for p in pins);assert all(o['pointer_matches'] for o in outputs);assert all(r['exit']==r['expected'] for r in runs)
print(json.dumps({'pins':len(pins),'outputs':len(outputs),'live_changes':[p['path'] for p in pins if not p['live_equal']],'runs':runs,'independent_checks':checks},indent=2))
