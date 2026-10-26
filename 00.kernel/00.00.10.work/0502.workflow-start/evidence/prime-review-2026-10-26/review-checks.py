from pathlib import Path
import csv,hashlib,json,os,re,subprocess,sys

W=Path(r'D:\Git\lib-build');P=W/'00.kernel/00.00.10.work/0502.workflow-start';O=Path(r'D:\librarian\temp\review-0502-2026-10-26');O.mkdir(exist_ok=False)
E='1bb8b47de9f7fff26250f48e1f5313a23ab74d12';B='befac9fe0dacdae15522187a14a887dadad571bc'
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
def git(*a,input=None):
    r=subprocess.run(['git','-C',str(W),*a],capture_output=True,input=input,env=env);assert r.returncode==0,r.stderr.decode(errors='replace');return r.stdout
def sha(b):return hashlib.sha256(b).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8'),delimiter='\t'))
def batch(specs):
    specs=list(dict.fromkeys(specs));raw=git('cat-file','--batch',input=('\n'.join(specs)+'\n').encode());out={};i=0
    for s in specs:
        j=raw.index(b'\n',i);h=raw[i:j].decode();i=j+1;assert not h.endswith(' missing'),s
        oid,typ,n=h.split();assert typ=='blob';n=int(n);out[s]=raw[i:i+n];i+=n+1
    return out
head=git('rev-parse','HEAD').decode().strip()
assert head.startswith('a5853b7')
changed=git('diff','--name-only',B,head).decode().splitlines()
allowed={
'00.kernel/00.00.10.work/0011.contents/01.002.md','00.kernel/00.00.10.work/0401.goal/01.md',
'00.kernel/00.00.10.work/0401.goal/06.01.md','00.kernel/00.00.10.work/0408.seats/01.md',
'00.kernel/00.00.10.work/0409.decisions/01.md','00.kernel/00.00.10.work/0500.band.packs/01.md',
'00.kernel/00.00.10.work/0611.findings/01.md','00.kernel/00.live.md','README.md',
'returns/pack-B-prime-report-2026-10-26.md'}
for path in changed:
    assert path in allowed or path.startswith('00.kernel/00.00.10.work/0502.workflow-start/') or path.startswith('returns/pack-B-prime-review-2026-10-26/'),path
assert not git('diff','--name-only','HEAD').strip()
assert not git('diff','--cached','--name-only').strip()
stored=batch([head+':'+p for p in changed])
for path in changed:assert (W/path).read_bytes()==stored[head+':'+path],path
cust=rows(P/'evidence/custody.tsv')+rows(P/'evidence/readme-custody.tsv')
original=batch([E+':'+r['path'] for r in cust])
for r in cust:
    data=original[E+':'+r['path']];assert sha(data)==r['sha256'] and len(data)==int(r['bytes']),r['path']
baseline=rows(W/'packs/lib-build-bootstrap-pass01-2026-10-26/workspace-baseline.tsv')
for r in baseline:
    data=(W/r['path']).read_bytes();assert sha(data)==r['sha256'] and len(data)==int(r['bytes'])
assert git('show',B+':00.kernel/00.00.10.work/0011.contents/01.001.md')==(W/'00.kernel/00.00.10.work/0011.contents/01.001.md').read_bytes()
for name in ('01.md','05.01.md','06.01.md','source-manifest.tsv'):
    stage=Path(r'D:\librarian\temp\workbook-first-use-2026-10-26')/name
    assert stage.read_bytes()==(P/'evidence/packed'/name).read_bytes(),name
packed=(P/'evidence/packed/05.01.md').read_text(encoding='utf-8');current=(P/'05.01.md').read_text(encoding='utf-8')
for n in range(1,5):
    marker=f'## #{n:02d} — '
    a=packed.split(marker)[1].split('result: PENDING')[0]
    b=current.split(marker)[1].split('result: pass.')[0]
    assert a==b,marker
seed=(P/'evidence/packed/06.01.md').read_text(encoding='utf-8')
assert (P/'06.01.md').read_text(encoding='utf-8').startswith(seed)
record=(W/'00.kernel/00.00.10.work/0401.goal/06.01.md').read_text(encoding='utf-8')
assert 'assignment_state: returned' in record and '0502.workflow-start/05.01.md' in record
r=subprocess.run([sys.executable,'-B',str(W/'labs/bootstrap-establish-pass01/render_live.py'),'check','--root',str(W)],env=env,capture_output=True)
assert r.returncode==0,r.stdout+r.stderr
refs={ref:oid for oid,ref in (l.split('\t') for l in git('ls-remote','origin','refs/heads/workshop','refs/heads/main','refs/heads/rebuild').decode().splitlines())}
assert refs['refs/heads/workshop']==head
assert refs['refs/heads/main']=='14676ca3c01833cc1b472198e62e3451ef706ec3' and refs['refs/heads/rebuild']=='de3b8ebc3df3e1da28c4d675963699644b78afab'
result={'reviewer':'Codex Prime','reviewed_commit':head,'reviewed_batch_sha256':sha((P/'05.01.md').read_bytes()),'changed_paths_in_scope':len(changed),'changed_worktree_bytes_match_HEAD':True,'custody_rows_verified_at_evidence_commit':len(cust),'original_baseline_unchanged':len(baseline),'packed_files_match_prime_sources':4,'numbered_task_instructions_preserved':4,'seed_notes_preserved':True,'renderer_check':r.stdout.decode().strip(),'remote_refs':refs,'other_worker_files_excluded_from_commits':True,'known_followups':['book entry still points to old contents; protected by batch scope','return incorrectly says contents candidate omits 0503; actual candidate lists it','metadata has packed/claimed historical fields alongside returned execution result; needs structured mutable state later'],'scope':'read-only independent review; no runtime tests or candidate execution'}
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
