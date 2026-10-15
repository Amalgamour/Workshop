#!/usr/bin/env python3
"""librarian-check: drift linter for a Librarian kernel desk.

Usage:
  python3 lcheck.py DESK_DIR [--config rules.toml] [--moves moves.toml] [--all]
                    [--json out.json] [--md out.md] [--write-moves moves.toml]
                    [--fix-sentinel]
Exit code: 1 if any ERROR on reworked pages, else 0.
The default run does not write inside DESK_DIR.
--fix-sentinel writes only a missing book 00.md, from the syntax 0014 card.
"""
import argparse, collections, json, os, re, sys, tomllib
import sentinel

SEV_ORDER = {"error": 0, "warn": 1, "info": 2}
STATUS_RANK = {"draft": 0, "signed": 1, "approved": 2, "lock": 3, "locked": 3}
FACE_RE = re.compile(r'^(?P<ff>\d{2})(?:\.(?P<vvv>\d{3}))?(?:\.(?P<ret>09))?\.md$')
TASK_RE = re.compile(r'^05\.(?P<nn>\d{2})\.md$')
BOOK_RE = re.compile(r'^\d{2}\.\d{2}\.\d{2}\.[a-z][a-z\-]*$')
PAGE_RE = re.compile(r'^(?P<n>\d{4})\.(?P<t>[a-z][a-z0-9\-.]*)$')

class Finding:
    def __init__(s, rule, sev, path, msg, tier):
        s.rule, s.sev, s.path, s.msg, s.tier = rule, sev, path, msg, tier
    def d(s): return dict(rule=s.rule, severity=s.sev, path=s.path, message=s.msg, tier=s.tier)

def hdr(text, key):
    m = re.search(rf'^{key}:\s*(.+)$', text, re.M)
    return m.group(1).strip() if m else None

def body(text):
    t = re.sub(r'^(Authorization|state|last change|version):.*$', '', text, flags=re.M)
    return re.sub(r'\s+', ' ', t).strip()

def strip_history(text):
    text = re.sub(r'~~.*?~~', '', text, flags=re.S)                      # struck = history (law 0026)
    text = re.sub(r'<del>.*?</del>', '', text, flags=re.S)
    # notes / patch sections are history-ish: drop '### notes' / '## Note...' blocks to next heading
    text = re.sub(r'^#{2,3} (?:notes?|Note[^\n]*)\n.*?(?=^#{1,3} |\Z)', '', text, flags=re.S | re.M | re.I)
    return text

class Desk:
    def __init__(s, root, cfg):
        s.root, s.cfg = root, cfg
        sc = cfg['scope']
        s.law, s.syn = sc['law_book'], sc['syntax_book']
        s.books = sorted(d for d in os.listdir(root) if BOOK_RE.match(d) and os.path.isdir(os.path.join(root, d)))
        s.pages = {}        # (book, NNNN) -> title
        s.title_at = collections.defaultdict(set)   # (book,title) -> {NNNN}
        for b in s.books:
            for d in os.listdir(os.path.join(root, b)):
                m = PAGE_RE.match(d)
                if m and os.path.isdir(os.path.join(root, b, d)):
                    s.pages[(b, m['n'])] = m['t']
                    s.title_at[(b, m['t'])].add(m['n'])
                    s.title_at[(b, m['t'].split('.')[0])].add(m['n'])
        s.titles = {t for (_, t) in s.pages.values()} if False else {t for t in s.pages.values()} | {t.split('.')[0] for t in s.pages.values()}

    def tier(s, rel):
        parts = rel.split('/')
        sc = s.cfg['scope']
        if len(parts) == 1: return 'reworked'                     # desk furniture
        b = parts[0]
        if b in sc.get('history_books', []): return 'history'
        if len(parts) >= 3:
            m = PAGE_RE.match(parts[1])
            if m:
                if b == s.syn and sc.get('syntax_reworked', True): return 'reworked'
                if b == s.law and int(m['n']) > sc['reworked_max_page']: return 'pending'
        return 'reworked'

def lint(root, cfg, moves, show_all=False):
    D = Desk(root, cfg)
    R = cfg['rules']; sc = cfg['scope']
    out = []
    def add(rule, path, msg, tier=None, sev=None):
        sev = sev or R[rule]['severity']
        if sev == 'off': return
        out.append(Finding(rule, sev, path, msg, tier or D.tier(path)))

    files = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if not d.startswith('.') and d != '00.retire.09']  # law 0009: lookups do not enter the warehouse
        for f in fn:
            if f.endswith('.md'): files.append(os.path.relpath(os.path.join(dp, f), root).replace(os.sep, '/'))
    files.sort()
    texts = {f: open(os.path.join(root, f), encoding='utf-8', errors='replace').read() for f in files}

    # ---- sentinel / register / order
    for b in D.books:
        if not os.path.exists(os.path.join(root, b, '00.md')):
            add('sentinel', b, 'book has no 00.md sentinel. ' + sentinel.HINT)
    reg = f'{D.syn}/00.REG.md'
    if reg in texts:
        rows = re.findall(r'^\| (\d{4}) \| (\S+) \| (\S+) \| (\S+) \|', texts[reg], re.M)
        listed = set()
        for n, t, folder, live in rows:
            listed.add(folder)
            if not os.path.isdir(os.path.join(root, D.syn, folder)): add('register', reg, f'REG row {n} {folder}: no such folder')
        for (b, n), t in D.pages.items():
            if b == D.syn and f'{n}.{t}' not in listed: add('register', reg, f'folder {n}.{t} has no REG row')
    order = f'{D.law}/00.order.md'
    if order in texts:
        listed = re.findall(r'^- (\d{4}\.[\w.\-]+)', texts[order], re.M)
        for l in listed:
            if not os.path.isdir(os.path.join(root, D.law, l)):
                add('order', order, f'lists {l}, folder not in this desk', tier='pending' if int(l[:4]) > sc['reworked_max_page'] else 'reworked')
        for (b, n), t in sorted(D.pages.items()):
            if b == D.law and f'{n}.{t}' not in listed:
                add('order', order, f'folder {n}.{t} not listed', tier='pending' if int(n) > sc['reworked_max_page'] else 'reworked')

    # ---- per page / per face
    by_page = collections.defaultdict(list)
    for f in files:
        p = f.split('/')
        if len(p) == 3 and p[0] in D.books and PAGE_RE.match(p[1]): by_page[(p[0], p[1])].append(p[2])
    for (b, pdir), names in sorted(by_page.items()):
        prel = f'{b}/{pdir}'; pm = PAGE_RE.match(pdir)
        if b in sc.get('history_books', []): continue
        seats = {}; drafts = collections.defaultdict(dict)
        for nm in names:
            rel = f'{prel}/{nm}'; t = texts[rel]
            fm = FACE_RE.match(nm); tm = TASK_RE.match(nm)
            if nm == '00.md': add('face-00-on-page', rel, 'page carries face 00'); continue
            if tm and not fm:
                continue
            if re.match(r'^05\.[a-z]+\.md$', nm):
                add('work-file-name', rel, f'"{nm}" is a work file name not defined by law 0005'); continue
            if not fm:
                # law 0012 face 01: 03.10-03.19 are alphabet slices. 03.EE is the class, not a filename.
                if pdir.startswith('0012.') and re.fullmatch(r'03\.1[0-9]\.md', nm):
                    continue
                add('face-name', rel, f'filename "{nm}" is not FF / FF.VVV / FF.VVV.09 / 05.NN'); continue
            ff = fm['ff']
            if not ('01' <= ff <= '08'): add('face-name', rel, f'face {ff} outside 01-08'); continue
            if fm['vvv'] and len(fm['vvv']) == 3 and ff == '05' and not fm['ret']:
                pass
            if ff == '07' and not fm['ret']:
                # axiom 7: bare 7 means missing is a state. align #12. 1.7 is a different chain.
                cite = hdr(t, 'cite') or ''
                parts = [p.strip() for p in cite.split(',')]
                if not any(p == '7' or p.startswith('7.') for p in parts):
                    add('face-07-filled', rel, 'face 07 is filled')
            if fm['ret']: continue
            if ff in sc.get('history_faces', []) or ff in sc.get('work_faces', []):
                if fm['vvv']: drafts[ff][fm['vvv']] = rel
                else: seats[ff] = rel
                continue
            if fm['vvv']: drafts[ff][fm['vvv']] = rel
            else: seats[ff] = rel
            # stamp
            is_law_face = ff in ('01', '02', '03', '04', '08')
            auth = hdr(t, 'Authorization')
            if is_law_face:
                miss = [k for k in ('version', 'Authorization', 'Face', 'PPPP', 'book', 'why') if hdr(t, k) is None]
                if miss: add('stamp-missing', rel, 'missing stamp: ' + ', '.join(miss))
            for k, want in (('PPPP', pm['n']), ('Face', ff), ('book', b)):
                v = hdr(t, k)
                if v and v.split()[0] != want: add('stamp-mismatch', rel, f'{k}: {v} but file is {want}')
            if auth:
                aw = auth.split()[0]
                if aw not in STATUS_RANK: add('status-vocab', rel, f'Authorization "{aw}"')
                st = hdr(t, 'state'); stw = st.split()[0] if st else None
                if stw and aw in STATUS_RANK and stw in STATUS_RANK and STATUS_RANK[stw] != STATUS_RANK[aw]:
                    add('status-header-state', rel, f'Authorization {aw} but state {stw}')
                if stw and stw not in STATUS_RANK and not (stw == 'live' and aw == 'lock') and ff != '05':
                    add('status-header-state', rel, f'Authorization {aw} but state "{stw}"', sev='info')
                foot = re.findall(r'^last change:\s*\S+\s+(\w+)', t, re.M)
                if foot and foot[-1] in STATUS_RANK and aw in STATUS_RANK:
                    fr, ar = STATUS_RANK[foot[-1]], STATUS_RANK[aw]
                    if ar < fr: add('status-footer', rel, f'header {aw}, footer "last change ... {foot[-1]}"')
                    elif aw == 'lock' and fr == 2: add('status-footer-lock', rel, 'header lock, footer approved')
                if not fm['vvv'] and aw == 'draft' and ff != '05': add('seat-is-draft', rel, 'seat stamped draft')
            if fm['vvv']:
                v = hdr(t, 'version')
                if v and v != fm['vvv']: add('draft-version', rel, f'header version {v}, filename {fm["vvv"]}')
            c = hdr(t, 'cite')
            if c and not re.fullmatch(r'[1-9](?:\.[1-9])*(?:,\s*[1-9](?:\.[1-9])*)*', c):
                add('cite-format', rel, f'cite: {c}')
        if any(ff in seats for ff in ('02', '03', '04', '08')) and '01' not in seats:
            add('live-needs-01', prel, 'seated faces but no 01.md')
        for ff, dd in drafts.items():
            if ff not in seats: continue
            sv = hdr(texts[seats[ff]], 'version')
            for vvv, rel in sorted(dd.items()):
                if sv and sv.isdigit() and int(vvv) <= int(sv):
                    if int(vvv) == int(sv):
                        if body(texts[rel]) != body(texts[seats[ff]]):
                            add('same-version-differs', rel, f'draft {vvv} and seat {ff}.md (version {sv}) differ in body text')
                        else:
                            add('stale-draft', rel, f'draft {vvv} is a copy of seat {ff}.md (same version, same body): approve copied instead of renamed')
                    else:
                        add('stale-draft', rel, f'draft {vvv} < seat version {sv}; not retired (.09)')
        # carry terms
        cterms = cfg.get('carry', {}).get('terms', []); cfaces = cfg.get('carry', {}).get('faces', [])
        if '01' in seats:
            t1 = texts[seats['01']].lower()
            for term in cterms:
                if re.search(rf'^#+ .*{term}', t1, re.M) or re.search(rf'\b{term}\b', strip_history(t1)):
                    for ff in cfaces:
                        if ff in seats and term not in texts[seats[ff]].lower():
                            add('carry-terms', seats[ff], f'face 01 carries "{term}"; face {ff} does not')
        if '01' in seats and '04' in seats:
            h1 = re.findall(r'^## (.+)$', strip_history(texts[seats['01']]), re.M)
            t4 = texts[seats['04']].lower()
            for h in h1:
                hw = h.strip().lower()
                if hw in ('patch', 'face name', 'not', 'notes') : continue
                if hw not in t4: add('twin-heading', seats['04'], f'face 01 heading "{h.strip()}" not found on face 04')

    # ---- pointers
    moved = moves.get('moved', {})  # old "NNNN" -> {title, now, book}
    ptr_title = re.compile(r'(?<![\d.])`?(\d{4})\.([a-z][a-z\-]*)`?')
    ptr_bare = re.compile(r'\b(page|law|syntax|child of|parent:?)\s+`?(\d{4})`?(?!\d|\.[a-z0-9])', re.I)
    ptr_named = re.compile(r'\b([A-Z]?[a-z]+)(?: home)?(?: on live law)? is (?:(?:live )?(?:law|syntax) )?(?:page )?`?(\d{4})`?(?!\d|\.[a-z0-9])(?! through)(?!`? face)(?!,? face)')
    for f in files:
        tier = D.tier(f)
        if tier == 'history': continue
        if f.endswith('00.order.md') or f.endswith('00.REG.md') or f.endswith('/REG.md'): continue   # covered by order/register rules
        p = f.split('/'); nm = p[-1]
        if nm.endswith('.09.md'):
            continue  # law 0009: lookups ignore a retired face
        ownpage = PAGE_RE.match(p[1])['n'] if len(p) == 3 and PAGE_RE.match(p[1]) else None
        ff = nm[:2] if len(p) == 3 else None
        if ff in sc.get('history_faces', []): continue
        work = ff in sc.get('work_faces', [])
        here = p[0] if p[0] in D.books else D.law
        t = strip_history(texts[f])
        def sev_for(rule): return 'info' if work else None
        for line in t.splitlines():
            for m in ptr_title.finditer(line):
                n, ti = m.group(1), m.group(2)
                if ti in ('md',): continue
                books = [here] + [b for b in D.books if b != here]
                ok = any(D.pages.get((b, n), '').split('.')[0] == ti.split('.')[0] or D.pages.get((b, n)) == ti for b in books)
                if ok: continue
                now = sorted({(b, x) for b in D.books for x in D.title_at.get((b, ti), set())})
                cur = sorted({D.pages[(b, n)] for b in D.books if (b, n) in D.pages})
                if now:
                    add('stale-address', f, f'cites {n}.{ti}; {n} is now {cur or "absent"}, "{ti}" lives at {", ".join(x for _, x in now)}', sev=sev_for('stale-address'))
                elif cur:
                    add('stale-address', f, f'cites {n}.{ti}; {n} is now {cur}; no page titled "{ti}"', sev=sev_for('stale-address') or 'warn')
                else:
                    add('dangling-page', f, f'cites {n}.{ti}; no such page', sev=sev_for('dangling-page'))
            for m in ptr_named.finditer(line):
                word, n = m.group(1).lower(), m.group(2)
                if word not in D.titles: continue
                bk = D.syn if 'syntax' in m.group(0) else (D.law if 'law' in m.group(0) else here)
                cand = [bk] + [b for b in D.books if b != bk]
                if any(D.pages.get((b, n), '').split('.')[0] == word for b in cand): continue
                now = sorted({x for b in D.books for x in D.title_at.get((b, word), set())})
                cur = sorted({D.pages[(b, n)] for b in D.books if (b, n) in D.pages})
                conf = n in moved and moved[n]['title'] == word
                add('stale-address', f, f'"{m.group(0)}": {n} is {cur or "absent"}; "{word}" lives at {now}' + (' (moves ledger confirms)' if conf else ' (heuristic: check)'), sev=sev_for('stale-address') or (None if conf else 'info'))
            for m in ptr_bare.finditer(line):
                kind, n = m.group(1).lower(), m.group(2)
                bk = D.syn if kind == 'syntax' else (D.law if kind == 'law' else here)
                exists_bk = (bk, n) in D.pages
                exists_any = any((b, n) in D.pages for b in D.books)
                if not exists_any:
                    add('dangling-page', f, f'"{m.group(0)}": no page {n} in any book', sev=sev_for('dangling-page') or ('warn' if int(n) > sc['reworked_max_page'] else None))
                    continue
                if kind in ('law', 'syntax') and not exists_bk:
                    add('dangling-page', f, f'"{m.group(0)}": no page {n} in {bk}', sev=sev_for('dangling-page') or 'warn')
                    continue
                if n in moved and n != ownpage:
                    curt = D.pages.get((bk, n)) or ''
                    old = moved[n]['title']
                    ll = line.lower()
                    if curt.split('.')[0] not in ll:
                        sev = 'error' if old in ll else None
                        add('reassigned-number', f, f'"{m.group(0)}": {n} was "{old}" (now at {moved[n]["now"]}), is now "{curt}"', sev=sev_for('reassigned-number') or sev)
    return out, D

def derive_moves(findings):
    """Build a moves ledger from stale NNNN.title pointers: old number -> title -> current home."""
    led = {}
    for x in findings:
        if x.rule != 'stale-address': continue
        m = re.search(r'cites (\d{4})\.([a-z\-]+); \1 is now .*?"\2" lives at (\S+)', x.msg)
        if m: led.setdefault(m.group(1), {'title': m.group(2), 'now': m.group(3).rstrip(','), 'seen_in': x.path})
    return led

def report(findings, show_all):
    lines = []
    tiers = collections.Counter((x.tier, x.sev) for x in findings)
    lines.append('# librarian-check report\n')
    lines.append('| tier | error | warn | info |\n|---|---|---|---|')
    for tr in ('reworked', 'pending'):
        lines.append(f'| {tr} | {tiers[(tr,"error")]} | {tiers[(tr,"warn")]} | {tiers[(tr,"info")]} |')
    for tr in ('reworked', 'pending'):
        sub = [x for x in findings if x.tier == tr]
        lines.append(f'\n## {tr.upper()} pages')
        byrule = collections.Counter((x.sev, x.rule) for x in sub)
        lines.append('rule counts: ' + ', '.join(f'{r} {s}={c}' for (s, r), c in sorted(byrule.items(), key=lambda k: (SEV_ORDER[k[0][0]], k[0][1]))))
        if tr == 'pending' and not show_all:
            lines.append('(pending pages: counts only; use --all to list)')
            continue
        for sev in ('error', 'warn', 'info'):
            items = sorted([x for x in sub if x.sev == sev], key=lambda x: (x.rule, x.path))
            if not items or (sev == 'info' and not show_all):
                if items: lines.append(f'\n### {sev}: {len(items)} (use --all to list)')
                continue
            lines.append(f'\n### {sev} ({len(items)})')
            for x in items: lines.append(f'- [{x.rule}] `{x.path}`: {x.msg}')
    return '\n'.join(lines) + '\n'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('desk'); here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument('--config', default=os.path.join(here, 'rules.toml'))
    ap.add_argument('--moves', default=os.path.join(here, 'moves.toml'))
    ap.add_argument('--all', action='store_true'); ap.add_argument('--brief', action='store_true', help='short model-facing card: reworked errors only'); ap.add_argument('--json'); ap.add_argument('--md')
    ap.add_argument('--write-moves', help='derive a moves ledger from stale NNNN.title pointers and write it')
    ap.add_argument('--fix-sentinel', action='store_true', help='write a missing book 00.md from the syntax 0014 card, then lint')
    a = ap.parse_args()
    cfg = tomllib.load(open(a.config, 'rb'))
    moves = tomllib.load(open(a.moves, 'rb')) if os.path.exists(a.moves) else {}
    if a.fix_sentinel:
        written, stopped = sentinel.build(a.desk)
        for item in written:
            print(f'built {item}')
        for item in stopped:
            print(f'stop {item}')
    findings, D = lint(a.desk, cfg, moves, a.all)
    if a.write_moves:
        led = derive_moves(findings)
        with open(a.write_moves, 'w') as fh:
            fh.write('# moves ledger: a number that once held a title, and where that title lives now.\n# Derived from stale NNNN.title pointers; review and edit by hand (axiom 6 Lineage).\n')
            for n, v in sorted(led.items()):
                fh.write(f'\n[moved."{n}"]\ntitle = "{v["title"]}"\nnow = "{v["now"]}"\nseen_in = "{v["seen_in"]}"\n')
        print(f'wrote {len(led)} moves to {a.write_moves}')
    rep = report(findings, a.all)
    if a.brief:
        errs = [x for x in findings if x.tier == 'reworked' and x.sev == 'error']
        rep = '```text\ncard: librarian-check\nscope: reworked pages, errors only. pending pages not listed\n' + f'errors: {len(errs)}\n' + ''.join(f'{x.path}: {x.rule}: {x.msg}\n' for x in sorted(errs, key=lambda x: x.path)) + 'not: a write. not permission. the director releases fixes\n```\n'
    if a.md: open(a.md, 'w').write(rep)
    if a.json: json.dump([x.d() for x in findings], open(a.json, 'w'), indent=1)
    print(rep)
    sys.exit(1 if any(x.sev == 'error' and x.tier == 'reworked' for x in findings) else 0)

if __name__ == '__main__':
    main()
