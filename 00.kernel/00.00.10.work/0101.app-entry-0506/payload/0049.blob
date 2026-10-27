from pathlib import Path
import csv,hashlib,json,os,subprocess
W=Path(r'D:\Git\lib-build');O=Path(r'C:\Users\misg\AppData\Local\Temp\prime-fixed-components-v6law0wf');env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'}
def git(*a):return subprocess.check_output(['git',*a],cwd=W,env=env)
n=0
for manifest in ['custody.tsv','text-custody.tsv']:
 for row in csv.DictReader((W/'00.kernel/00.00.10.work/0504.app-entry/evidence/05.06'/manifest).open(encoding='utf8'),delimiter='\t'):
  b=git('show','fd5d3fc280516ff1ef0b719ea27695d7bcb29df7:'+row['path']);assert hashlib.sha256(b).hexdigest()==row['sha256'] and len(b)==int(row['bytes']),row['path'];n+=1
d=0
for row in csv.DictReader((W/'00.kernel/00.00.10.work/0506.clerk-handoff/evidence/pack05.03/source-manifest.tsv').open(encoding='utf8'),delimiter='\t'):
 b=git('show',row['commit']+':'+row['path']);assert hashlib.sha256(b).hexdigest()==row['sha256'] and len(b)==int(row['bytes']);d+=1
summary=json.loads((O/'verification.json').read_text());summary['app_custody_boundary']='51 actual stored blobs verified at fd5d3fc280516ff1ef0b719ea27695d7bcb29df7; Builder completed publication during review';summary['app_return_commit']='fb95fc2';summary['seam_input_blobs_verified']=d
assert n==51 and d==15
(O/'publication-followup.json').write_text(json.dumps(summary,indent=2));print(json.dumps({'stored_app_rows':n,'seam_input_blobs':d,'publication_completed':True},indent=2))
