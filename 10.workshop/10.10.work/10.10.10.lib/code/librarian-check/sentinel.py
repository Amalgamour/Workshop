#!/usr/bin/env python3
"""Build a missing book 00.md from the syntax 0014 card.

The card lives on syntax page 0014, face 02. It says write what this is,
the first page, and what this is not. Law page 0054 says 00.md proves the book.

This writes only a book 00.md that is not already there. It does not overwrite.
It does not write a desk sentinel, a 00.start, a register, or a page file.
If the card cannot be opened, or the book has no first page, it stops and
writes nothing for that book.
"""
import argparse, os, re, sys

BOOK_RE = re.compile(r'^\d{2}\.\d{2}\.\d{2}\.[a-z][a-z\-]*$')
PAGE_RE = re.compile(r'^(?P<n>\d{4})\.(?P<t>[a-z][a-z0-9\-.]*)$')
CARD_NEED = ('what this is', 'the first page', 'what this is not')

HINT = (
    "build with sentinel.py from syntax page `0014`, design, face `02`, card `00.md`. "
    "That card says: what this is, the first page, what this is not. "
    "Law page `0054`, book, section Job, says 00.md proves the book."
)


def books(root):
    return sorted(
        d for d in os.listdir(root)
        if BOOK_RE.match(d) and os.path.isdir(os.path.join(root, d))
    )


def find_face(root, page, face, prefer):
    hits = []
    for book in books(root):
        folder = None
        book_dir = os.path.join(root, book)
        for name in os.listdir(book_dir):
            if name.startswith(page + '.') and os.path.isdir(os.path.join(book_dir, name)):
                folder = name
                break
        if not folder:
            continue
        path = os.path.join(book_dir, folder, face)
        if os.path.isfile(path):
            hits.append((book, path.replace('\\', '/')))
    for book, path in hits:
        if book == prefer:
            return path
    return hits[0][1] if hits else None


def parse_card(text):
    for block in re.findall(r'```text\n(.*?)```', text, re.S):
        fields = {}
        for line in block.splitlines():
            if ':' not in line:
                continue
            key, val = line.split(':', 1)
            fields[key.strip()] = val.strip()
        if fields.get('card') == '00.md':
            return fields
    return None


def table_rows(text):
    lines = [ln.strip() for ln in text.splitlines() if ln.strip().startswith('|')]
    if len(lines) < 3:
        return []
    head = [c.strip().lower() for c in lines[0].strip('|').split('|')]
    rows = []
    for ln in lines[2:]:
        cells = [c.strip() for c in ln.strip('|').split('|')]
        if cells and set(cells[0]) <= set('-: '):
            continue
        if len(cells) < 1 or not re.fullmatch(r'\d{4}', cells[0]):
            continue
        row = {head[i]: cells[i] for i in range(min(len(head), len(cells)))}
        row.setdefault('pppp', cells[0])
        rows.append(row)
    return rows


def page_folders(book_dir):
    pages = []
    for name in os.listdir(book_dir):
        m = PAGE_RE.match(name)
        if m and os.path.isdir(os.path.join(book_dir, name)):
            pages.append((int(m.group('n')), m.group('n'), m.group('t')))
    pages.sort()
    return pages


def first_page(book_dir):
    """Return (pppp, title, source) or None. Do not invent a page.

    Law page 0056: a band door ends in 0 and is not a member. Members
    start at the next number. Work starts at 1000 and that door stays
    open. Pages before that door are reserved. When this book has a
    1000 door, the first live section is the first page at 1001 or
    after. A book with no 1000 door keeps its register row.
    """
    pages = page_folders(book_dir)
    if any(num == 1000 for num, _, _ in pages):
        members = [(n, title) for num, n, title in pages if num >= 1001]
        if not members:
            return None
        n, title = members[0]
        door = next(t for num, _, t in pages if num == 1000)
        return n, title.split('.')[0], 'band:' + door
    for name in ('00.REG.md', 'REG.md'):
        path = os.path.join(book_dir, name)
        if not os.path.isfile(path):
            continue
        text = open(path, encoding='utf-8', errors='replace').read()
        for row in table_rows(text):
            live = row.get('live', 'yes').lower()
            if live in ('no', 'false'):
                continue
            title = row.get('title') or ''
            folder = (row.get('folder') or row.get('file') or '').split('/')[0]
            if not title and PAGE_RE.match(folder):
                title = PAGE_RE.match(folder).group('t').split('.')[0]
            n = row.get('pppp') or row.get('page')
            found = _page_dir(book_dir, n, title, folder) if n and title else None
            if found:
                return n, title, name
        return None
    order = os.path.join(book_dir, '00.order.md')
    if os.path.isfile(order):
        text = open(order, encoding='utf-8', errors='replace').read()
        m = re.search(r'^- (\d{4})\.([a-z][a-z0-9.\-]*)', text, re.M)
        if m and os.path.isdir(os.path.join(book_dir, m.group(0)[2:])):
            return m.group(1), m.group(2).split('.')[0], '00.order.md'
    if not pages:
        return None
    n, title = pages[0][1], pages[0][2].split('.')[0]
    return n, title, 'page folder'


def _page_dir(book_dir, n, title, folder):
    if folder and os.path.isdir(os.path.join(book_dir, folder)):
        return folder
    direct = f'{n}.{title}'
    if os.path.isdir(os.path.join(book_dir, direct)):
        return direct
    for name in os.listdir(book_dir):
        if name.startswith(n + '.') and os.path.isdir(os.path.join(book_dir, name)):
            return name
    return None


def band_line(source):
    if not source.startswith('band:'):
        return ''
    door = source.split(':', 1)[1]
    return (
        f" The band door is `1000.{door}`. It stays open. It is not this page."
        " Pages before that door are reserved."
    )


def source_line(source):
    if source.startswith('band:'):
        return "Band: law page `0056`, band. A band door is not a member. Members start at the next number.\n"
    return f"Register: `{source}`.\n"


def render(book, first, register, proof):
    n, title = first
    keyword = book.split('.')[-1]
    proof = proof or 'address.proof'
    return (
        "# 00\n"
        "\n"
        "Authorization: draft — 2026-10-11\n"
        "state: draft\n"
        f"keyword: {keyword}\n"
        f"book: {book}\n"
        "why: Book sentinel. What this is, the first page, and what this is not.\n"
        "\n"
        "## Sentinel\n"
        f"This is the book sentinel of `{book}`. It proves the book.\n"
        "\n"
        f"The first page to open is `{n}`, title {title}.{band_line(register)}\n"
        "\n"
        f"This is not a page. This is not the desk walk. This is not the proof. The proof is {proof}.\n"
        "\n"
        "## Source\n"
        "Card on syntax page `0014`, design, face `02`: what this is, the first page, what this is not.\n"
        "Law page `0054`, book, section Job: `00.md` proves the book.\n"
        f"{source_line(register)}"
        "If this file is missing, the container is not real. Stop.\n"
        "\n"
        "last change: 2026-10-11 draft.\n"
    )


def build(root, dry=False):
    """Write each missing book 00.md. Return (written, stopped)."""
    root = os.path.abspath(root)
    written, stopped = [], []
    card_path = find_face(root, '0014', '02.md', '00.00.00.syntax')
    if not card_path:
        stopped.append('syntax page 0014 face 02 is not on this desk. no sentinel was written.')
        return written, stopped
    card = parse_card(open(card_path, encoding='utf-8').read())
    write = (card or {}).get('write', '')
    if not card or any(part not in write for part in CARD_NEED):
        stopped.append(f'{card_path}: card 00.md does not name the three lines. no sentinel was written.')
        return written, stopped
    if not find_face(root, '0054', '01.md', '00.00.01.law'):
        stopped.append('law page 0054 face 01 is not on this desk. no sentinel was written.')
        return written, stopped
    proof = card.get('proof', 'address.proof')
    for book in books(root):
        dest = os.path.join(root, book, '00.md')
        if os.path.exists(dest):
            continue
        got = first_page(os.path.join(root, book))
        if not got:
            stopped.append(
                f'{book}: no first page in 00.REG.md, REG.md, or 00.order.md, and no page folder. 00.md was not written.'
            )
            continue
        n, title, register = got
        text = render(book, (n, title), register, proof)
        rel = f'{book}/00.md'
        if dry:
            written.append(rel)
            continue
        with open(dest, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(text)
        written.append(rel)
    return written, stopped


def main():
    ap = argparse.ArgumentParser(description='Build a missing book 00.md from the syntax 0014 card.')
    ap.add_argument('desk')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    written, stopped = build(a.desk, dry=a.dry_run)
    for item in written:
        print(('would build ' if a.dry_run else 'built ') + item)
    for item in stopped:
        print('stop ' + item)
    if a.dry_run and written:
        # show the text of the first missing book, so the three lines can be read
        root = os.path.abspath(a.desk)
        book = written[0].split('/')[0]
        got = first_page(os.path.join(root, book))
        card_path = find_face(root, '0014', '02.md', '00.00.00.syntax')
        card = parse_card(open(card_path, encoding='utf-8').read())
        sys.stdout.write('\n' + render(book, (got[0], got[1]), got[2], card.get('proof')))
    return 1 if stopped and not written else 0


if __name__ == '__main__':
    sys.exit(main())
