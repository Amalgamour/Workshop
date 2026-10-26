from pathlib import Path
import csv, hashlib, io, json, os, subprocess

W=Path(r'D:\Git\lib-build')
P=W/'packs/lib-build-bootstrap-pass01-2026-10-26'
L=W/'labs/bootstrap-preservation-pass01'
R=L/'clones/verify2'
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
def git(repo,*args):
    r=subprocess.run(['git','-C',str(repo),*args],capture_output=True,env=env,timeout=60)
    if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace'))
    return r.stdout
def rows(path):return list(csv.DictReader(path.open(encoding='utf-8'),delimiter='\t'))
def check(data,r):assert len(data)==int(r['bytes']) and hashlib.sha256(data).hexdigest()==r['sha256'],r
archives={
'main-worktree':('e8b1a994da07000fa576fd771e455a94718ed431','14676ca3c01833cc1b472198e62e3451ef706ec3','archive/librarian-worktree-2026-10-26'),
'rebuild-worktree':('586cfa4ae055c29a98c1106bb70143901c57cc11','de3b8ebc3df3e1da28c4d675963699644b78afab','archive/rebuild-worktree-2026-10-26'),
'bootstrap':('fe42b017b5e8c288f70878d696cb227b09ab5a8e','14676ca3c01833cc1b472198e62e3451ef706ec3','archive/lib-build-bootstrap-2026-10-26')}
refs={ref:obj for obj,ref in (line.split('\t') for line in git(R,'ls-remote','origin').decode().splitlines())}
manifest=rows(P/'preservation-manifest.tsv')
report={}
for name,(commit,base,branch) in archives.items():
    assert refs['refs/heads/'+branch]==commit
    assert git(R,'rev-parse',commit+'~3').decode().strip()==base
    mine=[r for r in manifest if r['archive']==name]
    for r in mine:check(git(R,'cat-file','blob',commit+':'+r['destination']),r)
    evidence=list(csv.DictReader(io.StringIO(git(R,'cat-file','blob',commit+':archive-evidence/HASHES.tsv').decode()),delimiter='\t'))
    for r in evidence:check(git(R,'cat-file','blob',commit+':'+r['path']),r)
    changed=set(git(R,'diff','--name-only',base,commit).decode().splitlines())
    allowed={r['destination'] for r in mine}|{r['path'] for r in evidence}|{'archive-evidence/HASHES.tsv'}
    assert not changed-allowed
    report[name]={'commit':commit,'preserved_rows':len(mine),'evidence_rows':len(evidence),'extra_changed_paths':0}
assert refs['refs/tags/archive/main-14676ca']==archives['main-worktree'][1]
assert refs['refs/tags/archive/rebuild-de3b8eb']==archives['rebuild-worktree'][1]
assert refs['refs/heads/main']==archives['main-worktree'][1]
assert refs['refs/heads/rebuild']==archives['rebuild-worktree'][1]
for r in rows(P/'manifest.sha256.tsv'):check((P/r['path']).read_bytes(),r)
for r in manifest:check(Path(r['source']).read_bytes(),r)
for r in rows(P/'workspace-baseline.tsv'):check((W/r['path']).read_bytes(),r)
before=json.loads((L/'evidence/fingerprint-before.json').read_text())
final=json.loads((L/'evidence/fingerprint-final.json').read_text())
assert before['old']==final['old'] and not before['problems'] and not final['problems']
for name,root in [('Librarian',Path(r'D:\Git\Librarian')),('Librarian-rebuild',Path(r'D:\Git\Librarian-rebuild'))]:
    f=before['old'][name]
    assert git(root,'rev-parse','HEAD').decode().strip()==f['head']
    assert hashlib.sha256(git(root,'status','--porcelain=v1','-uall','-z')).hexdigest()==f['status_sha256']
    assert git(root,'for-each-ref','--format=%(objectname) %(refname)').decode()==f['for_each_ref']
    assert git(root,'stash','list').decode()==f['stash_list']
    assert git(root,'worktree','list','--porcelain').decode()==f['worktree_list']
    for rel,expected in f['status_file_sha256'].items():
        p=root/rel
        assert (hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None)==expected,rel
journals=[]
for p in sorted((L/'evidence/journals').glob('*.json')):
    j=json.loads(p.read_text())
    assert j['state']=='complete' and len(j['installed'])==j['rows'],str(p)
    journals.append({'name':p.name,'rows':j['rows']})
out={'reviewer':'Codex Prime','disposition':'Pack A preservation accepted; helper not approved as general production runtime','independent_checks':report,'remote_refs_checked_live':True,'source_rows':len(manifest),'workspace_baseline_rows':39,'old_checkout_fingerprints_and_status_file_hashes':'match captured before state at review','journals':journals,'test_suite':'builder evidence: 19 passed, 1 skipped; not rerun by Prime','remaining':['staged and committed blob-byte check needed before future copies are committed','tracked .gitattributes policy needed in Pack B','returns/ supersedes notes/returns/ by Director instruction','exclude generated nested clone/test repositories from workspace Git','archive helper remains pre-F1; verifier currently local evidence only'],'pack_B_started_by_prime':False}
dest=Path(r'D:\librarian\temp\pack-A-prime-verification-2026-10-26.json')
dest.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))
