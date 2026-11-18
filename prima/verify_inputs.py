"""Scoped read-only Prima input check; identity verification is not authorization."""
from pathlib import Path
import hashlib, json, sys
ROOT = Path(__file__).resolve().parents[1]
M = ROOT / '00.kernel/00.00.10.work/0706.prima-loop/evidence/pack05.01/source-manifest.json'
queue = json.loads((ROOT/'prima/assignments.json').read_text(encoding='utf-8'))
job = queue['assignments'][0]
errors = []
def read_safe(rel):
    if not isinstance(rel, str) or '\\' in rel or ':' in rel:
        raise ValueError('unsafe relative path')
    parts = rel.split('/')
    if any(p in ('', '.', '..') for p in parts): raise ValueError('unsafe relative path')
    p = ROOT
    for part in parts:
        p = p / part
        if p.is_symlink() or (hasattr(p, 'is_junction') and p.is_junction()):
            raise ValueError('linked source')
    if not p.resolve().is_relative_to(ROOT): raise ValueError('outside source root')
    return p.read_bytes()
def check(rel, digest, size=None):
    try:
        data = read_safe(rel)
        if hashlib.sha256(data).hexdigest() != digest: raise ValueError('sha256 mismatch')
        if size is not None and len(data) != size: raise ValueError('byte-length mismatch')
    except (OSError, ValueError) as exc:
        errors.append({'path': rel, 'error': str(exc)})
check(job['pack'], job['pack_sha256'])
check(job['source_manifest'], job['source_manifest_sha256'])
if not errors:
    manifest = json.loads(M.read_text(encoding='utf-8'))
    for row in manifest['files']: check(row['path'], row['sha256'], row['bytes'])
else:
    manifest = {'files': []}
print(json.dumps({'schema': 'prima-input-check/1', 'assignment_id': job['id'],
    'status': 'mismatch' if errors else 'matched', 'checked_files': len(manifest['files']),
    'errors': errors, 'authorizes_execution': False}, indent=2))
sys.exit(2 if errors else 0)
