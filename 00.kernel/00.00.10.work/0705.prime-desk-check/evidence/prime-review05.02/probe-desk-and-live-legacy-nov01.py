from pathlib import Path
import subprocess,sys,json,hashlib
R=Path(r'D:\Git\lib-build');O=Path(r'D:\librarian\temp\three-return-reviews-nov01')
def run(name,args):
 p=subprocess.run([sys.executable,'-B','-X','utf8',*map(str,args)],cwd=R,capture_output=True);(O/(name+'.stdout')).write_bytes(p.stdout);(O/(name+'.stderr')).write_bytes(p.stderr);return p
p=run('desk-demo',[R/'labs/prime-desk-pass01/demo.py','--out',O/'desk-demo']);print('desk demo',p.returncode)
reqfile=O/'desk-demo/request.json';req=json.loads(reqfile.read_text());root=Path(req['instance']['root']);row=next(x for x in req['references'] if x['role']=='assignment');f=root/row['path'];b=f.read_bytes().replace(b'0522.review-construction/05.04.md',b'0521.return-placement/05.03.md');f.write_bytes(b);row.update(sha256=hashlib.sha256(b).hexdigest(),bytes=len(b));new=O/'selector-divergence-request.json';new.write_text(json.dumps(req),encoding='utf-8');p=run('selector-divergence',[R/'labs/prime-desk-pass01/prime_desk.py','view','--request',new,'--json']);d=json.loads(p.stdout);(O/'selector-probe-summary.json').write_text(json.dumps({'qualification':'changed only disposable canonical assignment plus its expected hash; custom selector unchanged','exit':p.returncode,'actual_result':d},ensure_ascii=False,indent=2),encoding='utf-8');print('selector-divergence',p.returncode,'selected=',d.get('selected'), 'keys',list(d))
book=R/'00.kernel/00.00.10.work';before={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (book/'0182.desk-app-integration-design-0501').rglob('*') if f.is_file()}
p=run('actual-legacy-read',[R/'labs/review-loop-pass02/review_loop.py','describe-legacy','--book',book,'--member','0182.desk-app-integration-design-0501']);after={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (book/'0182.desk-app-integration-design-0501').rglob('*') if f.is_file()};assert before==after
print('actual legacy read',p.returncode,'bytes',len(p.stdout),'unchanged',before==after)
