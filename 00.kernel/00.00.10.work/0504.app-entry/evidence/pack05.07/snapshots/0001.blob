#!/usr/bin/env python3
"""Read-only check of a book's declared contents against its PUBLISHED Git tree at one pinned commit.

  python -B check_book.py --root <repository> --revision <commit> --book 00.kernel/00.00.10.work
                          [--contents <book-relative path>] [--json]

Batch 00.kernel/00.00.10.work/0502.workflow-start/05.02 (claude-opus-5-5, Colab). Standard library and Git only.

Scope: the commit's tree, read with `git ls-tree` and `git cat-file` at the SHA that --revision resolves to once.
The working directory, the index and untracked files are never read, so local work cannot make a published
page look present. Every Git call runs with GIT_OPTIONAL_LOCKS=0. Nothing is written.

Selection: by default the contents face is the one the book's 00.md names in its documented local sentence
form `contents in <path>.` (exactly one occurrence; <path> book-relative, under 0011.contents/, ending .md).
--contents names a candidate explicitly instead; the report then says it was chosen on the command line, not
by the sentinel. There is no fallback to 01.001 and no highest-version rule.

Covered: the Pages table rows (page folders; direct files; direct subdirectories with their recursive tracked
file counts); the "Book files:" list; the paths in the "## Other books" section (resolved relative to the book
root, lexically, inside the repository; each must be a blob at the commit). Not covered: any other prose,
link or face content. Findings are advisory. Exit: 0 clean, 1 findings, 2 invalid input, unsupported
structure or tool failure.

Other books (pass 02, batch 0502.workflow-start/05.03, OR-01): the whole section, from its heading to the next
Markdown heading or the end of the face, is accounted for. Each nonblank line is one or more items of the form
Label: `path`. joined by single spaces. The one other text allowed is the sentence `Each lists what it holds.`, once, at
the end of the section's last nonblank line. Anything else in the section refuses; it is never skipped.
"""
import argparse, hashlib, json, os, posixpath, re, subprocess, sys

ENV = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0")
PAGE_RE = re.compile(r"^(\d{4})\.[A-Za-z0-9][A-Za-z0-9._-]*$")
POINTER_RE = re.compile(r"contents in (\S+?)\.(?=\s|$)")
ROW_RE = re.compile(r"^\| `([^`]+)` \| (.+) \|$")
ENTRY_RE = re.compile(r"`([^`]+)`(?: \((\d+) files?\))?")
OTHER_HEADING = "## Other books"
OTHER_ITEM_RE = re.compile(r"([A-Z][A-Za-z]*(?: [A-Za-z]+)*): `([^`]+)`\.")
OTHER_TAIL = "Each lists what it holds."    # write_contents.py's sentence; accepted only where 06.04 C04 says
HEADING_RE = re.compile(r"^#{1,6} ")
HEADER = "| Page | Faces and files |"
SEPARATOR = "|---|---|"
COVERED = ["Pages table rows: page folders, direct files, direct subdirectories, recursive tracked-file counts",
           "Book files list", "Other books paths (relative to the book root)"]
NOT_COVERED = ["prose references and other links", "face contents", "whether a page should be published",
               "the working tree, the index and untracked files"]


class Refuse(Exception):
    pass


def git(root, *args):
    r = subprocess.run(["git", "-C", root, *args], capture_output=True, env=ENV)
    if r.returncode:
        raise Refuse(f"git {' '.join(args[:2])} failed: {r.stderr.decode(errors='replace').strip()}")
    return r.stdout


def safe_rel(p):
    if not p or p.startswith("/") or "\\" in p or re.match(r"^[A-Za-z]:", p):
        return False
    return all(part not in ("", ".", "..") for part in p.split("/"))


def resolve_commit(root, rev):
    if rev.startswith("-"):
        raise Refuse("revision may not start with '-'")
    out = git(root, "rev-parse", "--verify", "--quiet", "--end-of-options", rev + "^{commit}").decode().strip()
    if not re.fullmatch(r"[0-9a-f]{40}", out):
        raise Refuse(f"revision {rev!r} does not resolve to one commit")
    return out


def book_tree(root, sha, book):
    """{book-relative path: (mode, type, oid)} for every entry under the book at the commit."""
    out = git(root, "ls-tree", "-r", "-z", "--full-tree", sha, "--", book + "/")
    tree = {}
    for e in out.split(b"\0"):
        if not e:
            continue
        meta, path = e.decode("utf-8").split("\t", 1)
        mode, typ, oid = meta.split()
        if not path.startswith(book + "/"):
            continue
        tree[path[len(book) + 1:]] = (mode, typ, oid)
    return tree


def blob(root, sha, path):
    try:
        return git(root, "cat-file", "blob", f"{sha}:{path}")
    except Refuse:
        return None


def is_blob(root, sha, path):
    out = git(root, "ls-tree", "-z", "--full-tree", sha, "--", path)
    for e in out.split(b"\0"):
        if e:
            meta, p = e.decode("utf-8").split("\t", 1)
            if p == path and meta.split()[1] == "blob":
                return True
    return False


def parse_contents(text):
    lines = text.split("\n")
    try:
        i = lines.index("## Pages")
    except ValueError:
        raise Refuse("unsupported structure: no '## Pages' section")
    j = i + 1
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    if j + 1 >= len(lines) or lines[j] != HEADER or lines[j + 1] != SEPARATOR:
        raise Refuse(f"unsupported structure: the Pages table header is not exactly {HEADER!r} / {SEPARATOR!r}")
    rows, k = [], j + 2
    while k < len(lines) and lines[k].strip():
        line = lines[k]
        m = ROW_RE.match(line)
        if not m:
            raise Refuse(f"unsupported structure: Pages row {k + 1} is not '| `page` | entries |': {line!r}")
        entries, rest = [], m.group(2)
        pos = 0
        for n, em in enumerate(ENTRY_RE.finditer(rest)):
            sep = rest[pos:em.start()]
            if (n == 0 and sep) or (n > 0 and sep != ", "):
                raise Refuse(f"unsupported structure: entries in row {k + 1} are not ', '-separated back-quoted names")
            name, count = em.group(1), em.group(2)
            if name.endswith("/") != (count is not None):
                raise Refuse(f"unsupported structure: row {k + 1} entry {name!r}: a directory needs '(N files)', a file must not have it")
            entries.append((name.rstrip("/"), "dir" if count is not None else "file", int(count) if count else None))
            pos = em.end()
        if pos != len(rest) or not entries:
            raise Refuse(f"unsupported structure: row {k + 1} has text that is not an entry")
        rows.append({"line": k + 1, "page": m.group(1), "entries": entries})
        k += 1
    if not rows:
        raise Refuse("unsupported structure: the Pages table has no rows")
    book_files = None
    for line in lines[k:]:
        if line.startswith("Book files:"):
            if book_files is not None:
                raise Refuse("unsupported structure: two 'Book files:' lines")
            body = line[len("Book files:"):].strip()
            if not body.endswith("."):
                raise Refuse("unsupported structure: the 'Book files:' list does not end with '.'")
            items = re.findall(r"`([^`]+)`", body)
            if not items or re.sub(r"`[^`]+`", "", body[:-1]).replace(",", "").strip():
                raise Refuse("unsupported structure: 'Book files:' is not a list of back-quoted names")
            book_files = items
    if book_files is None:
        raise Refuse("unsupported structure: no 'Book files:' line")
    return rows, book_files, parse_other_books(lines)


def parse_other_books(lines):
    """Every line of the Other books section, or a refusal. None when the face has no such section."""
    heads = [n for n, line in enumerate(lines) if re.sub(r"\s", "", line).lower() == "##otherbooks"]
    if not heads:
        return None
    for n in heads:
        if lines[n] != OTHER_HEADING:
            raise Refuse(f"unsupported structure: line {n + 1} is not exactly {OTHER_HEADING!r}: {lines[n]!r}")
    if len(heads) > 1:
        raise Refuse(f"unsupported structure: {len(heads)} {OTHER_HEADING!r} headings")
    end = heads[0] + 1
    while end < len(lines) and not HEADING_RE.match(lines[end]):
        end += 1
    body = [(n, lines[n]) for n in range(heads[0] + 1, end) if lines[n].strip()]
    if not body:
        raise Refuse("unsupported structure: '## Other books' has no 'Label: `path`.' items")
    items = []
    for i, (n, line) in enumerate(body):
        last = i == len(body) - 1
        m = OTHER_ITEM_RE.match(line)
        while True:
            if not m:
                raise Refuse(f"unsupported structure: Other books line {n + 1} has text that is not a "
                             f"'Label: `path`.' item: {line!r}")
            items.append((m.group(1), m.group(2)))
            pos = m.end()
            if pos == len(line):
                break
            rest = line[pos + 1:] if line[pos] == " " else None
            if rest == OTHER_TAIL:
                if last:
                    break
                raise Refuse(f"unsupported structure: Other books line {n + 1}: {OTHER_TAIL!r} is allowed only "
                             f"at the end of the section's last line")
            m = OTHER_ITEM_RE.match(line, pos + 1) if rest is not None else None
    return items


def check(root, rev, book, contents=None):
    root = os.path.abspath(root)
    if not safe_rel(book):
        raise Refuse(f"--book is not a repository-relative path: {book!r}")
    sha = resolve_commit(root, rev)
    tree = book_tree(root, sha, book)
    if not tree:
        raise Refuse(f"book {book!r} has no tracked files at {sha}")
    sentinel = blob(root, sha, f"{book}/00.md")
    pointer_text = None
    if contents is None:
        if sentinel is None:
            raise Refuse("the book has no 00.md at this commit, so no contents pointer")
        found = POINTER_RE.findall(sentinel.decode("utf-8", "replace"))
        if len(found) != 1:
            raise Refuse(f"the book's 00.md names {len(found)} contents pointers in the form 'contents in <path>.'; exactly one is required")
        contents, source = found[0], "book 00.md pointer"
        pointer_text = f"contents in {contents}."
    else:
        source = "--contents on the command line (not selected by the sentinel)"
    if not safe_rel(contents) or not contents.startswith("0011.contents/") or not contents.endswith(".md"):
        raise Refuse(f"contents path {contents!r} is not a book-relative 0011.contents/*.md path")
    data = blob(root, sha, f"{book}/{contents}")
    if data is None:
        raise Refuse(f"contents {contents!r} does not exist at {sha}")
    rows, book_files, other = parse_contents(data.decode("utf-8"))
    findings = []

    def find(kind, msg, **kw):
        findings.append({"kind": kind, "message": msg, **kw})

    pages = {}
    for path in tree:
        if "/" in path:
            pages.setdefault(path.split("/", 1)[0], []).append(path.split("/", 1)[1])
    root_files = sorted(p for p in tree if "/" not in p)
    seen, numbers = {}, {}
    for r in rows:
        p = r["page"]
        if not PAGE_RE.match(p):
            find("bad-page-name", f"row {r['line']}: {p!r} is not a PPPP.title page folder", page=p)
        if p in seen:
            find("duplicate-row", f"row {r['line']}: {p} is listed again (first at row {seen[p]})", page=p)
            continue
        seen[p] = r["line"]
        num = p[:4]
        if num in numbers and numbers[num] != p:
            find("duplicate-page-number", f"row {r['line']}: number {num} is used by {numbers[num]} and {p}", page=p)
        numbers.setdefault(num, p)
        if p not in pages:
            find("missing-page", f"{p} is listed but is not a folder in the published tree", page=p)
            continue
        inner = pages[p]
        direct_files = {x for x in inner if "/" not in x}
        direct_dirs = {}
        for x in inner:
            if "/" in x:
                d = x.split("/", 1)[0]
                direct_dirs[d] = direct_dirs.get(d, 0) + 1
        listed_files = {n for n, t, _ in r["entries"] if t == "file"}
        listed_dirs = {n: c for n, t, c in r["entries"] if t == "dir"}
        for n in sorted(listed_files - direct_files):
            find("missing-file", f"{p}/{n} is listed but not in the published tree", page=p, item=n)
        for n in sorted(direct_files - listed_files):
            find("extra-file", f"{p}/{n} is in the published tree but not listed", page=p, item=n)
        for n, c in sorted(listed_dirs.items()):
            if n not in direct_dirs:
                find("missing-directory", f"{p}/{n}/ is listed but not in the published tree", page=p, item=n + "/")
            elif direct_dirs[n] != c:
                find("count-mismatch", f"{p}/{n}/ is listed with {c} files; the published tree has {direct_dirs[n]}",
                     page=p, item=n + "/", expected=c, actual=direct_dirs[n])
        for n in sorted(set(direct_dirs) - set(listed_dirs)):
            find("extra-directory", f"{p}/{n}/ is in the published tree but not listed", page=p, item=n + "/")
    for p in sorted(set(pages) - set(seen)):
        find("extra-page", f"{p} is a folder in the published tree but has no row", page=p)
    tree_numbers = {}
    for p in sorted(pages):
        if PAGE_RE.match(p):
            tree_numbers.setdefault(p[:4], []).append(p)
    for num, ps in sorted(tree_numbers.items()):
        if len(ps) > 1:
            find("duplicate-page-number-in-tree", f"the published tree has {len(ps)} folders numbered {num}: {', '.join(ps)}", page=num)
    for n in sorted(set(book_files) - set(root_files)):
        find("missing-book-file", f"book file {n} is listed but not at the book root in the published tree", item=n)
    for n in sorted(set(root_files) - set(book_files)):
        find("extra-book-file", f"book file {n} is at the book root in the published tree but not listed", item=n)
    other_checked = []
    for label, rel in other or []:
        target = posixpath.normpath(posixpath.join(book, rel))
        if rel.startswith("/") or re.match(r"^[A-Za-z]:", rel) or target == ".." or target.startswith("../") or target.startswith("/"):
            find("path-escape", f"Other books {label}: {rel!r} resolves outside the repository", item=rel)
            continue
        ok = is_blob(root, sha, target)
        other_checked.append({"label": label, "path": rel, "resolved": target, "present": ok})
        if not ok:
            find("missing-other-book", f"Other books {label}: {target} is not a file in the published tree", item=rel)
    return {
        "schema": "book-orientation-check@1",
        "revision_input": rev, "commit": sha, "book": book,
        "contents_path": f"{book}/{contents}", "contents_sha256": hashlib.sha256(data).hexdigest(),
        "selection_source": source, "sentinel_pointer": pointer_text,
        "scope": "published tree at the commit only; working tree, index and untracked files not read",
        "covered": COVERED, "not_covered": NOT_COVERED,
        "counts": {"rows": len(rows), "tree_pages": len(pages), "book_files_listed": len(book_files), "other_books": len(other or [])},
        "other_books": other_checked,
        "findings": findings, "result": "findings" if findings else "clean", "advisory": True,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--book", required=True)
    ap.add_argument("--contents")
    ap.add_argument("--json", action="store_true", help="print only the JSON report")
    a = ap.parse_args()
    try:
        rep = check(a.root, a.revision, a.book.rstrip("/"), a.contents)
    except Refuse as e:
        out = {"schema": "book-orientation-check@1", "result": "refused", "reason": str(e)}
        print(json.dumps(out, indent=1) if a.json else f"refused: {e}")
        sys.exit(2)
    if a.json:
        print(json.dumps(rep, indent=1))
    else:
        print(f"commit:    {rep['commit']}  (from {rep['revision_input']!r})")
        print(f"book:      {rep['book']}")
        print(f"contents:  {rep['contents_path']}  sha256 {rep['contents_sha256']}")
        print(f"selected:  {rep['selection_source']}" + (f"  [{rep['sentinel_pointer']}]" if rep["sentinel_pointer"] else ""))
        print(f"scope:     {rep['scope']}")
        print(f"result:    {rep['result']} ({len(rep['findings'])} finding(s), advisory)")
        for f in rep["findings"]:
            print(f"  - {f['kind']}: {f['message']}")
    sys.exit(1 if rep["findings"] else 0)


if __name__ == "__main__":
    main()
