#!/usr/bin/env python3
"""Read-only mechanical consistency checker for the Librarian kernel draft."""
import re, sys, os, collections, json
root = sys.argv[1]
findings = collections.defaultdict(list)
pages = {}  # (book, PPPP) -> folder title
files = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        if f.endswith('.md'):
            files.append(os.path.join(dp, f))
book_re = re.compile(r'(00\.00\.\d\d\.[a-z]+)')
for p in files:
    rel = os.path.relpath(p, root)
    parts = rel.split(os.sep)
    if len(parts) >= 3:
        m = re.match(r'(\d{4})\.(.+)', parts[1])
        if m: pages[(parts[0], m.group(1))] = m.group(2)
# folder-title map per number (any book)
num2titles = collections.defaultdict(set)
for (b, n), t in pages.items(): num2titles[n].add((b.split('.')[-1], t))
def hdr(text, key):
    m = re.search(rf'^{key}:\s*(.+)$', text, re.M)
    return m.group(1).strip() if m else None
for p in sorted(files):
    rel = os.path.relpath(p, root); text = open(p, encoding='utf-8').read()
    parts = rel.split(os.sep)
    auth = hdr(text, 'Authorization'); state = hdr(text, 'state'); pppp = hdr(text, 'PPPP'); kw = hdr(text, 'keyword')
    last = re.findall(r'^last change:\s*\S+\s+(\w+)', text, re.M)
    if not auth: findings['no Authorization header'].append(rel)
    authw = auth.split()[0].strip('—') if auth else None
    if authw and state and authw != state: findings['Authorization word != state field'].append(f'{rel}: auth={authw} state={state}')
    if authw and last and last[-1] in ('draft','signed','approved','lock','locked') and last[-1].rstrip('ed') != authw.rstrip('ed') and not (last[-1]=='locked' and authw=='lock'):
        findings['header vs footer state mismatch'].append(f'{rel}: header={authw} footer={last[-1]}')
    if len(parts) >= 3:
        m = re.match(r'(\d{4})\.(.+)', parts[1])
        if m:
            if pppp and pppp != m.group(1): findings['PPPP header != folder number'].append(f'{rel}: PPPP={pppp}')
            if kw and kw != m.group(2) and kw.split('.')[0] != m.group(2).split('.')[0]: findings['keyword != folder title'].append(f'{rel}: keyword={kw} folder={m.group(2)}')
    # version header vs filename suffix
    v = hdr(text, 'version'); fm = re.match(r'\d\d\.(\d{3})\.md$', parts[-1])
    if v and fm and v != fm.group(1): findings['version header != filename version'].append(f'{rel}: header={v} file={fm.group(1)}')
    # "page NNNN, titled X" / "Colab is page 0028" / "NNNN.title" references
    for m in re.finditer(r'`?(\d{4})\.([a-z][a-z\-]+)`?', text):
        n, t = m.group(1), m.group(2)
        if n in num2titles and t not in {x[1].split('.')[0] for x in num2titles[n]} and t not in {x[1] for x in num2titles[n]}:
            findings['stale address: NNNN.name points at a different concept'].append(f'{rel}: cites {n}.{t}, but {n} is now {sorted(x[1] for x in num2titles[n])}')
    for m in re.finditer(r'\b([A-Za-z]+) (?:is|on|at) (?:live law |law |syntax )?(?:page )?`?(\d{4})`?', text):
        word, n = m.group(1).lower(), m.group(2)
        if n in num2titles and word not in ('it','this','that','page','law','title','folder','book','home','one','the') and word not in {x[1].split('.')[0] for x in num2titles[n]}:
            findings['possible stale prose pointer (word near number)'].append(f'{rel}: "{m.group(0)}" -> {n} is {sorted(x[1] for x in num2titles[n])}')
# overflow/unprompted transport across colab/return/emit/report faces
for p in sorted(files):
    rel = os.path.relpath(p, root)
    if re.search(r'/(0036\.colab|0038\.return|0039\.report|0053\.emit|0106\.emit|0040\.lead|0037\.pack)/', '/'+rel):
        t = open(p, encoding='utf-8').read().lower()
        findings['overflow/unprompted carried? (colab/return/emit/report/lead/pack faces)'].append(f"{rel}: overflow={'yes' if 'overflow' in t else 'NO'} unprompted={'yes' if 'unprompted' in t else 'NO'}")
# REG vs folders (syntax)
reg = os.path.join(root, '00.00.00.syntax/00.REG.md')
if os.path.exists(reg):
    rows = re.findall(r'^\| (\d{4}) \| (\S+) \| (\S+) \|', open(reg).read(), re.M)
    for n, t, folder in rows:
        if not os.path.isdir(os.path.join(root, '00.00.00.syntax', folder)): findings['REG row with no folder (syntax)'].append(f'{n} {folder}')
order = os.path.join(root, '00.00.01.law/00.order.md')
if os.path.exists(order):
    listed = re.findall(r'^- (\d{4}\.[\w.\-]+)', open(order).read(), re.M)
    existing = {d for d in os.listdir(os.path.join(root,'00.00.01.law'))}
    for l in listed:
        if l not in existing: findings['law 00.order lists folder not in archive'].append(l)
    for d in sorted(existing):
        if re.match(r'\d{4}\.', d) and d not in listed: findings['law folder not in 00.order'].append(d)
for k, v in findings.items():
    print(f'\n## {k} ({len(v)})')
    for x in v: print('  -', x)
