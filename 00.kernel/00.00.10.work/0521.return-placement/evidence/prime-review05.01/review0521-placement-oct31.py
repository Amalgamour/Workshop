from pathlib import Path
import sys,subprocess,json,hashlib,os,importlib.util,tempfile
R=Path(r'D:\Git\lib-build');W=R/'00.kernel/00.00.10.work';P=W/'0521.return-placement'
O=Path(r'D:\librarian\temp\review0521-placement');O.mkdir(exist_ok=False);(O/'scratch').mkdir()
env=dict(os.environ,TEMP=str(O/'scratch'),TMP=str(O/'scratch'),PYTHONDONTWRITEBYTECODE='1')
checks={'artifacts':[]}
for row in json.loads((P/'evidence/build05.01/artifact-manifest.json').read_text(encoding='utf-8'))['files']:
    b=(R/row['path']).read_bytes();same=len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    assert same,row['path'];checks['artifacts'].append(dict(path=row['path'],matches=same))
for name,args in [('tests',[str(R/'labs/return-placement-pass01/tests/test_return_placement.py'),'-v']),
                  ('plan',[str(R/'labs/return-placement-pass01/return_placement.py'),'plan','--book',str(W),'--audit',str(W/'0417.return-placement/evidence/audit-corrected.json'),'--out',str(O/'independent-plan.json')])]:
    q=subprocess.run([sys.executable,'-B',*args],cwd=R,env=env,capture_output=True)
    (O/(name+'.stdout')).write_bytes(q.stdout);(O/(name+'.stderr')).write_bytes(q.stderr)
    checks[name]={'exit':q.returncode};print(name,q.returncode,flush=True)
spec=importlib.util.spec_from_file_location('placement',R/'labs/return-placement-pass01/return_placement.py');rp=importlib.util.module_from_spec(spec);spec.loader.exec_module(rp)
probes=[]
for page,expected in [('0504.app-entry','0104.app-entry'),('1504.app-entry','1104.app-entry'),('1702.design','1702.design')]:
    try:
        found=rp.compute_route({'book':'00.00.10.work','page':page,'batch':'05.01'})
        probes.append({'page':page,'expected':expected,'actual':found['target_page'],'matches':found['target_page']==expected})
    except rp.PlacementError as exc:probes.append({'page':page,'expected':expected,'error':str(exc),'matches':False})
plan=json.loads((O/'independent-plan.json').read_text(encoding='utf-8'))
collisions=[]
for row in plan['items']:
    route=row.get('route') or {}
    if route.get('route')!='matched-workflow-return-line':continue
    dest=route['target_page'];code=dest.split('.',1)[0]
    old=[p.name for p in W.glob(code+'.*') if p.is_dir() and p.name!=dest]
    if old:collisions.append({'target':dest,'occupied_same_number':old})
unique={x['target']:x for x in collisions}
probes.append({'probe':'occupied-line-plan','actual_number_conflicts':list(unique.values()),'reported_collisions':plan['collisions'],'filing_0121':plan['filing_0121']})
# A destination must not be complete when a source capture lacks its receipt.
root=O/'scratch/missing-receipt';root.mkdir();member=root/'0101.synthetic';member.mkdir()
reservation={'schema':'return-capture/1','kind':'reservation','submission_id':'synthetic-missing-receipt',
             'origin':{'book':'00.00.10.work','page':'0521.return-placement','batch':'05.01'},
             'destination':{'member':'0101','name':'synthetic','path':'0101.synthetic'}}
(member/'reservation.json').write_text(json.dumps(reservation),encoding='utf-8')
(member/'return.md').write_bytes(b'SYNTHETIC return without receipt or manifest\n')
out=rp.apply_run(str(root),[str(member)])
probes.append({'probe':'missing-receipt','output':out,'source_receipt_exists':False})
(O/'probes.json').write_text(json.dumps(probes,indent=2)+'\n',encoding='utf-8')
(O/'checks.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'routing_probes':probes[:3],'occupied_target_lines':len(unique),'reported_collisions':len(plan['collisions']),'missing_receipt_output':out},indent=2))
