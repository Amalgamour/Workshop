import hashlib
import json
import sys
from pathlib import Path

def sha(b): return hashlib.sha256(b).hexdigest()
mode = sys.argv[1]
if mode == 'audit':
    c = json.loads(Path('../case.json').read_text())
    base = Path(c['page']).parent
    manifest = json.loads((base / 'evidence/build05.01/artifact-manifest.json').read_text())
    rows = []
    for row in manifest['artifacts']:
        p = Path(row['path'])
        b = p.read_bytes()
        rows.append({'path': row['path'], 'match': sha(b) == row['sha256'] and len(b) == row['bytes']})
    member = Path('00.kernel/00.00.10.work') / c['member']
    m = json.loads((member / 'manifest.json').read_text())
    payloads = []
    for row in m['sources']:
        b = (member / 'payload' / row['payload']).read_bytes()
        payloads.append({'logical': row['logical'], 'match': sha(b) == row['sha256'] and len(b) == row['bytes']})
    result = {'artifact_count': len(rows), 'artifacts_all_match': all(r['match'] for r in rows),
        'payload_count': len(payloads), 'payloads_all_match': all(r['match'] for r in payloads),
        'return_match': sha((member / 'return.md').read_bytes()) == m['return']['sha256'],
        'receipt': json.loads((member / 'receipt.json').read_text()), 'artifact_rows': rows, 'payload_rows': payloads}
    Path('../out/manual-audit.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['artifact_rows','payload_rows']}, indent=2))
elif mode == 'read':
    for arg in sys.argv[2:]:
        path, *part = arg.split('::')
        p = Path(path)
        lines = p.read_text(encoding='utf-8').splitlines()
        start, end = (map(int, part[0].split('-')) if part else (1, len(lines)))
        print('\nFILE', path, 'sha256', sha(p.read_bytes()), 'LINES', start, end)
        for n in range(start, min(end, len(lines))+1): print(f'{n}: {lines[n-1]}')
else:
    raise SystemExit('unknown mode')
