"""Place the law.draft sample beside the kernel seats as FF.VVV drafts.

--kernel writes only new draft files under 00.00.00.kernel.draft/00.00.01.law.
It does not overwrite a seat, does not write the check kernel, and does not approve.
--dry-run prints the map and writes nothing.
--sample installs a rebuilt payload into law.draft and refuses to overwrite.
"""

from pathlib import Path
import json
import os
import re
import sys

repo = Path(__file__).resolve().parents[4]
sample = repo / 'law.draft'
law = repo / '00.00.00.kernel.draft' / '00.00.01.law'
check = repo / '00.00.00.kernel'
payload = Path(os.environ['TEMP']) / 'librarian-law-build' / 'payload' / 'manifest.json'

PAGES = (
    '0000.invariant', '0001.law', '0002.schema', '0003.operate',
    '0004.user', '0005.ticket', '0006.note', '0007.reserved',
    '0008.map', '0009.retire', '0010.about', '0011.contents',
)

BLURB = {
    '0000': 'The locked seat is the invariant template. This draft adds how to read the book. The seat face 08 stays.',
    '0001': 'The seat bars commands, addresses, and section charts on face 01. This draft allows a source pointer and puts an owner on each section. A local page 0001 may hold subject law. It does not replace the kernel face contract.',
    '0002': 'A compact form is for a section that needs one. This sample still writes a card for every teaching section so the match can be checked.',
    '0003': 'The menu names the faces a section supplies. The sample says a clerk or a model selects them. The seated king says clerk is not a law title.',
    '0004': 'Face 04 keeps the why and enough body to recover the conditions. A rebuild stays a draft until the lawful review.',
    '0005': 'Face 05 teaches the work ranges. This draft does not open a live task.',
    '0006': 'Face 06 is page memory. A note does not change the law. The seated notes are copied below so the walk can see them.',
    '0007': 'Face 07 stays absent. This page teaches that absence. No face 07 is written.',
    '0008': 'The seat has no face 08. This draft adds one for relationship rows. The rows are examples. They do not install a parent chain. The override home shared with page 0001 is unresolved.',
    '0009': '09 stays the retirement tail. This draft performs no retirement. Axiom 9 and the seated retire wording do not agree. The retired file beside the seat stays.',
    '0010': 'The sample calls itself law.draft and says it has no desk. This page is the about page of book 00.00.01.law, which has a desk. The sample wording is kept for the walk to correct.',
    '0011': 'The sample contents list the twelve teaching pages. The seat lists this law book. This draft is the sample list, not a new register.',
}


def version_of(text):
    m = re.search(r'^version:\s*(\d{3})\b', text, re.M)
    return m.group(1) if m else None


def next_version(page_dir, ff):
    seat = page_dir / f'{ff}.md'
    if not seat.exists():
        archived = sorted(p.name for p in page_dir.glob(f'{ff}.*.md'))
        if archived:
            raise SystemExit(f'refuse a first cut; archive already exists: {page_dir.name} {archived}')
        return '001'
    sv = version_of(seat.read_text(encoding='utf-8-sig'))
    if not sv:
        raise SystemExit(f'no version on seat {seat}')
    n = int(sv) + 1
    while (page_dir / f'{ff}.{n:03d}.md').exists() or (page_dir / f'{ff}.{n:03d}.09.md').exists():
        n += 1
    return f'{n:03d}'


def rewrite(text, folder, versions):
    text = re.sub(r'^version:\s*\d{3}\b.*$', 'version: {vvv}', text, count=1, flags=re.M)
    # version placeholder filled by caller after this function knows vvv... handled below
    text = re.sub(r'^book:\s*.+$', 'book: 00.00.01.law', text, count=1, flags=re.M)

    def repl(m):
        prefix, ff = m.group(1), m.group(2)
        dest = folder
        if prefix:
            dest = prefix.strip('/').split('/')[-1]
        key = (dest, ff)
        if key not in versions:
            raise SystemExit(f'no draft version for {key} from link {m.group(0)}')
        return f'{prefix}{ff}.{versions[key]}.md'

    text = re.sub(
        r'((?:\.\./[0-9]{4}\.[A-Za-z0-9.\-]*/)?)([0-9]{2})\.001\.md',
        repl,
        text,
    )
    return text


def kernel(dry):
    if not sample.is_dir() or not law.is_dir():
        raise SystemExit('sample or law book is missing')
    versions = {}
    bodies = {}
    for folder in PAGES:
        src = sample / folder
        dest_dir = law / folder
        if not src.is_dir() or not dest_dir.is_dir():
            raise SystemExit(f'missing page folder {folder}')
        for path in sorted(src.glob('??.001.md')):
            ff = path.name[:2]
            if not ('01' <= ff <= '08') or ff == '07':
                raise SystemExit(f'refuse face {path}')
            vvv = next_version(dest_dir, ff)
            versions[(folder, ff)] = vvv
            bodies[(folder, ff)] = path.read_text(encoding='utf-8-sig')
        seat06 = dest_dir / '06.md'
        if seat06.exists():
            if version_of(seat06.read_text(encoding='utf-8-sig')):
                versions[(folder, '06')] = next_version(dest_dir, '06')
            else:
                versions[(folder, '06')] = None
        else:
            versions[(folder, '06')] = next_version(dest_dir, '06')

    plan = []
    for folder in PAGES:
        pppp = folder[:4]
        note_vvv = versions[(folder, '06')]
        faces = sorted(ff for (fol, ff) in bodies if fol == folder)
        if note_vvv:
            faces.append('06')
        for ff in faces:
            vvv = note_vvv if ff == '06' else versions[(folder, ff)]
            name = f'{ff}.{vvv}.md'
            target = (law / folder / name).resolve()
            if not target.is_relative_to(law.resolve()):
                raise SystemExit(f'path escaped the law book: {target}')
            if target.is_relative_to(check.resolve()):
                raise SystemExit(f'refuse check kernel: {target}')
            if target.exists():
                raise SystemExit(f'refuse overwrite: {target}')
            if ff == '06':
                text = note_text(folder, pppp, vvv, inline=False)
            else:
                text = rewrite(bodies[(folder, ff)], folder, versions)
                text = text.replace('version: {vvv}', f'version: {vvv}', 1)
                if 'version: {vvv}' in text:
                    raise SystemExit(f'version stamp survived in {folder} {ff}')
                if not text.startswith(f'# {ff}\n'):
                    raise SystemExit(f'bad header {folder} {ff}')
                if note_vvv:
                    carry = (
                        f'Seated 05 and 06 for this page are carried on `06.{note_vvv}.md`.\n'
                        'The seat stays. This draft does not approve.\n'
                    )
                elif ff == '01':
                    carry = note_text(folder, pppp, None, inline=True)
                else:
                    carry = (
                        'The seated note face has no version line, so it was not given a draft number.\n'
                        'The seated 05 and 06 are carried in the notes on face 01 of this draft.\n'
                        'The seat stays. This draft does not approve.\n'
                    )
                text = text.rstrip() + (
                    '\n\n### notes\n\n'
                    'born: 2026-10-10\n'
                    'source: law.draft sample\n'
                    + carry
                    + '\nlast change: 2026-10-10 draft. Restamped from the law.draft sample.\n'
                )
            plan.append((target, text))

    for target, _ in plan:
        print(f'{target.relative_to(repo).as_posix()}')
    print(f'files: {len(plan)}')
    if dry:
        print('dry-run: nothing written')
        return
    for target, text in plan:
        target.write_bytes(text.encode('utf-8'))
    for target, text in plan:
        if target.read_bytes() != text.encode('utf-8'):
            raise SystemExit(f'verify failed: {target}')
    print(f'wrote and verified {len(plan)} draft files')


def note_text(folder, pppp, vvv, inline):
    title = folder.split('.', 1)[1]
    lines = []
    if not inline:
        lines.extend([
            '# 06',
            '',
            f'version: {vvv}',
            'Authorization: draft — 2026-10-10',
            'state: draft',
            'Face: 06',
            f'PPPP: {pppp}',
            'book: 00.00.01.law',
            f'keyword: {title}',
            'why: Seated notes carried onto this draft. A note does not govern.',
            'cite: 6.8',
            '',
        ])
    lines.extend([
        'Carry' if inline else '## Carry',
        '',
        BLURB[pppp],
        '',
        'Sentences in the sample that say this book has no desk describe law.draft. They are not a claim about book 00.00.01.law.',
        '',
    ])
    page = law / folder
    sources = sorted(page.glob('05*.md')) + ([page / '06.md'] if (page / '06.md').exists() else [])
    if not sources:
        lines.append('No seated 05 or 06 was on this page.')
        lines.append('')
    for src in sources:
        lines.append(f'From {src.name}' if inline else f'## From {src.name}')
        lines.append('')
        body = src.read_text(encoding='utf-8-sig').rstrip()
        if inline:
            body = '\n'.join(('    ' + line) if line else '' for line in body.splitlines())
        lines.append(body)
        lines.append('')
    if not inline:
        lines.append('last change: 2026-10-10 draft. Seated notes carried beside the new faces.')
        lines.append('')
    return '\n'.join(lines)


def sample_install():
    if not payload.is_file():
        raise SystemExit(f'no payload at {payload}. Run build.py first.')
    files = json.loads(payload.read_text(encoding='utf-8'))
    targets = []
    for name, body in files.items():
        if name.startswith('../') or not name.startswith('law.draft/'):
            continue
        target = (repo / name).resolve()
        if not target.is_relative_to((repo / 'law.draft').resolve()):
            raise SystemExit(f'path escaped law.draft: {target}')
        if target.exists():
            raise SystemExit(f'Existing file would be overwritten: {target}')
        targets.append((target, body))
    for target, body in targets:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body.encode('utf-8'))
    for target, body in targets:
        if target.read_bytes() != body.encode('utf-8'):
            raise SystemExit(f'verify failed: {target}')
    print(f'Created and verified {len(targets)} sample files; no existing files overwritten.')


def main():
    args = set(sys.argv[1:])
    if args <= {'--kernel', '--dry-run'} and '--kernel' in args:
        kernel(dry='--dry-run' in args)
        return
    if args == {'--sample'}:
        sample_install()
        return
    print('usage: install.py --kernel [--dry-run] | install.py --sample')
    sys.exit(2)


if __name__ == '__main__':
    main()
