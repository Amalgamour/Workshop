from pathlib import Path, PurePosixPath
import argparse,base64,hashlib,io,json,zipfile,sys
a=argparse.ArgumentParser();a.add_argument('--repo-root',required=True);a.add_argument('--assignment',required=True);a.add_argument('--out',required=True);a=a.parse_args()
r=Path(a.repo_root).resolve();out=Path(a.out).resolve()
def need(ok,msg):
 if not ok: raise ValueError(msg)
def safe(root,rel):
 need(isinstance(rel,str) and rel and ':' not in rel and '\\' not in rel,'unsafe path')
 p=PurePosixPath(rel);need(not p.is_absolute() and all(x not in ('','.','..') for x in rel.split('/')),'unsafe components')
 q=root
 for part in p.parts:
  q=q/part;need(not q.is_symlink() and not (hasattr(q,'is_junction') and q.is_junction()),'linked path')
 need(q.resolve().is_relative_to(root),'outside root');return q
try:
 queue=json.loads((r/'prima/assignments.json').read_text(encoding='utf-8'));jobs=[j for j in queue['assignments'] if j['id']==a.assignment];need(len(jobs)==1,'assignment not unique');j=jobs[0]
 for key in ('pack','source_manifest'):
  b=safe(r,j[key]).read_bytes();need(hashlib.sha256(b).hexdigest()==j[key+'_sha256'],key+' hash mismatch')
 bundle=json.loads(safe(r,j['source_manifest']).read_text(encoding='utf-8'));need(bundle['schema']=='prima-sprint-bundle/1','bundle schema')
 raw=base64.b64decode(bundle['archive_base64'],validate=True);need(hashlib.sha256(raw).hexdigest()==bundle['archive_sha256'],'archive hash')
 need(not out.exists() and not out.is_relative_to(r) and not r.is_relative_to(out),'output must be new and separate')
 for p in (out,*out.parents): need(not p.is_symlink() and not (hasattr(p,'is_junction') and p.is_junction()),'linked output')
 expected={x['path']:x for x in bundle['files']};need(len(expected)==len(bundle['files']),'duplicate manifest path');need(sum(x['bytes'] for x in expected.values())<30000000,'expanded size limit')
 contents=[]
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  need(len(z.namelist())==len(expected) and set(z.namelist())==set(expected),'archive members differ')
  for rel,row in expected.items():
   path=safe(out,rel);b=z.read(rel);need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'source mismatch: '+rel);contents.append((path,b))
 out.mkdir(parents=True)
 for p,b in contents:
  p.parent.mkdir(parents=True,exist_ok=True)
  with p.open('xb') as f:f.write(b)
 print(json.dumps({'schema':'prima-sprint-input-check/1','assignment_id':a.assignment,'checked_files':len(contents),'status':'matched','source_room':str(out),'authorizes_dispatch':False}))
except Exception as e:
 print(json.dumps({'status':'refused','error':str(e),'authorizes_dispatch':False}));sys.exit(2)
