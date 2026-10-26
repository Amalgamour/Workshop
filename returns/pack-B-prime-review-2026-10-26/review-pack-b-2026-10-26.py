from pathlib import Path
import csv, hashlib, importlib.util, json, os, re, shutil, subprocess, sys

W=Path(r'D:\Git\lib-build')
O=Path(r'D:\librarian\temp\pack-B-prime-review-2026-10-26')
O.mkdir(exist_ok='--retry' in sys.argv)
ENV=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
def git(repo,*a,input=None):
    r=subprocess.run(['git','-C',str(repo),*a],input=input,capture_output=True,env=ENV)
    assert r.returncode==0,r.stderr.decode(errors='replace')
    return r.stdout
def sha(b):return hashlib.sha256(b).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8'),delimiter='\t'))
def blobs(specs):
    specs=list(dict.fromkeys(specs))
    raw=git(W,'cat-file','--batch',input=('\n'.join(specs)+'\n').encode())
    out={};i=0
    for spec in specs:
        j=raw.index(b'\n',i);head=raw[i:j].decode();i=j+1
        assert not head.endswith(' missing'),spec
        oid,typ,length=head.split();assert typ=='blob',spec
        n=int(length);out[spec]=(oid,raw[i:i+n]);i+=n+1
    return out
head=git(W,'rev-parse','HEAD').decode().strip()
assert head=='befac9fe0dacdae15522187a14a887dadad571bc'
assert git(W,'status','--porcelain=v1','-uall')==b''
tracked={}
for e in git(W,'ls-tree','-r','-z',head).split(b'\0'):
    if not e:continue
    meta,path=e.decode().split('\t',1);mode,typ,oid=meta.split()
    assert mode!='160000' and typ=='blob'
    tracked[path]=oid
stored=blobs(tracked.values())
for path,oid in tracked.items():assert (W/path).read_bytes()==stored[oid][1],path
index={}
for e in git(W,'ls-files','-s','-z').split(b'\0'):
    if e:
        meta,path=e.decode().split('\t',1);mode,oid,stage=meta.split();assert stage=='0' and mode!='160000';index[path]=oid
assert index==tracked
M=W/'00.kernel/00.00.10.work/0410.imports/manifests'
import_rows=[]
for name in ('step03-import-snapshots.tsv','step03-import-selected.tsv','step03-import-p1.tsv','step03-import-claude.tsv'):
    import_rows+=rows(M/name)
source=blobs(r['source'] for r in import_rows)
for r in import_rows:
    oid,data=source[r['source']]
    assert oid==r['git_blob'] and sha(data)==r['sha256'] and len(data)==int(r['bytes'])
    assert (W/r['destination']).read_bytes()==data
checked_manifests=[]
for p in [W/'packs/lib-build-bootstrap-pass01-2026-10-26/workspace-baseline.tsv',M/'step03-custody-imports.tsv',W/'labs/bootstrap-establish-pass01/evidence/step07/manifest-new-files.tsv',W/'labs/bootstrap-establish-pass01/evidence/step07/manifest-self.tsv',W/'labs/bootstrap-establish-pass01/evidence/step07/manifest-final.tsv']:
    rr=rows(p)
    for r in rr:
        data=(W/r['path']).read_bytes();assert sha(data)==r['sha256'] and len(data)==int(r['bytes']),r['path']
    checked_manifests.append({'path':p.relative_to(W).as_posix(),'rows':len(rr)})
# Compare old repositories with the capture made before Pack B. No index refresh.
before=json.loads((W/'labs/bootstrap-establish-pass01/evidence/old-fingerprint-before.json').read_text())
for name,root in [('Librarian',Path(r'D:\Git\Librarian')),('Librarian-rebuild',Path(r'D:\Git\Librarian-rebuild'))]:
    f=before['old'][name]
    assert git(root,'rev-parse','HEAD').decode().strip()==f['head']
    assert sha(git(root,'status','--porcelain=v1','-uall','-z'))==f['status_sha256']
    assert git(root,'for-each-ref','--format=%(objectname) %(refname)').decode()==f['for_each_ref']
    assert git(root,'stash','list').decode()==f['stash_list']
    assert git(root,'worktree','list','--porcelain').decode()==f['worktree_list']
    for rel,h in f['status_file_sha256'].items():
        p=root/rel;assert (sha(p.read_bytes()) if p.is_file() else None)==h,rel
# Rerun only the three bounded suites in copied labs, avoiding original evidence writes.
fixture=O/'fixture-workspace'
copies={
'bootstrap-establish-pass01':['custody.py','import_blobs.py','test_import_blobs.py','render_live.py','test_render_live.py'],
'bootstrap-git-bytes-pass01':['gitbytes.py','test_gitbytes.py']}
for lab,files in copies.items():
    dest=fixture/'labs'/lab;dest.mkdir(parents=True,exist_ok='--retry' in sys.argv)
    for name in files:shutil.copyfile(W/'labs'/lab/name,dest/name)
for rel in ('00.kernel/00.00.10.work/0401.goal/06.01.md','00.kernel/00.00.10.work/0410.imports/manifests/step03-selection-register.tsv'):
    dest=fixture/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(W/rel,dest)
tests=[]
for lab,test in [('bootstrap-git-bytes-pass01','test_gitbytes.py'),('bootstrap-establish-pass01','test_import_blobs.py'),('bootstrap-establish-pass01','test_render_live.py')]:
    r=subprocess.run([sys.executable,'-B','-X','utf8',str(fixture/'labs'/lab/test),'-v'],capture_output=True,env=ENV)
    (O/(test+('.retry.log' if '--retry' in sys.argv else '.log'))).write_bytes(r.stdout+r.stderr)
    tests.append({'suite':test,'exit':r.returncode,'output_tail':(r.stdout+r.stderr).decode(errors='replace')[-180:]})
    assert r.returncode==0,tests[-1]
r=subprocess.run([sys.executable,'-B',str(W/'labs/bootstrap-establish-pass01/render_live.py'),'check','--root',str(W)],capture_output=True,env=ENV)
assert r.returncode==0,r.stdout+r.stderr
# Test the schema boundary without writing any record or view.
spec=importlib.util.spec_from_file_location('review_renderer',W/'labs/bootstrap-establish-pass01/render_live.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
base=(W/mod.RECORD).read_bytes()
cases={'undeclared_workflow_space':base.replace(b'workflow_space: 0',b'workflow_space: 99'),
'missing_book':base.replace(b'book: 00.00.10.work',b'book: 99.99.99.missing'),
'nonexistent_work_item':base.replace(b'current_work: 00.kernel/00.00.10.work/0501.bootstrap/05.02.md',b'current_work: missing/not-a-job.md')}
boundary={}
for name,data in cases.items():
    try:mod.parse_record(data);boundary[name]='accepted by syntax parser; no cross-reference validation'
    except mod.Refuse as e:boundary[name]='refused: '+str(e)
assert git(W,'status','--porcelain=v1','-uall')==b''
result={'head':head,'tracked_files_byte_exact_vs_HEAD':len(tracked),'index_equals_HEAD':True,'gitlinks':0,'provenance_import_rows':len(import_rows),'manifest_checks':checked_manifests,'old_checkouts_unchanged_vs_pre_B':True,'rerun_suites':tests,'renderer_live_check':r.stdout.decode().strip(),'context_validation_boundary':boundary,'workspace_status_after_review_checks':'clean','remote_verified_separately':False,'scope':'independent local verification plus copied-fixture tests; no production or candidate execution'}
(O/'verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
