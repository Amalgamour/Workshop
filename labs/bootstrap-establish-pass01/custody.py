"""Shared helpers for Pack B (lib-build-bootstrap-pass01) plus addendum 001. Development tooling, not runtime.

Path-name and reparse checks are carried from labs/bootstrap-preservation-pass01/preserve_copy.py
(sha256 cbbe1993a1c502c34d86a3c3dc82539f6cec53f62d8d4da7a4fb15bc62a8c478), the helper Pack A tested.
"""
import csv, hashlib, os, re, stat, subprocess
from pathlib import Path, PurePosixPath

LB = Path(r"D:\Git\lib-build")
PACK = LB / "packs" / "lib-build-bootstrap-pass01-2026-10-26"
ADD = LB / "packs" / "lib-build-pack-B-addendum-001-2026-10-26"
LAB = LB / "labs" / "bootstrap-establish-pass01"
OLD = {"Librarian": Path(r"D:\Git\Librarian"), "Librarian-rebuild": Path(r"D:\Git\Librarian-rebuild")}
REMOTE = "https://github.com/Amalgamour/Librarian.git"
MAIN = "14676ca3c01833cc1b472198e62e3451ef706ec3"
REB = "de3b8ebc3df3e1da28c4d675963699644b78afab"
ARCHIVES = {
    "main-worktree": ("refs/heads/archive/librarian-worktree-2026-10-26", "e8b1a994da07000fa576fd771e455a94718ed431", 90),
    "rebuild-worktree": ("refs/heads/archive/rebuild-worktree-2026-10-26", "586cfa4ae055c29a98c1106bb70143901c57cc11", 28),
    "bootstrap": ("refs/heads/archive/lib-build-bootstrap-2026-10-26", "fe42b017b5e8c288f70878d696cb227b09ab5a8e", 49),
}
RESERVED = {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)}
REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


class Refuse(Exception):
    pass


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tsv(path):
    return list(csv.DictReader(open(path, encoding="utf-8", newline=""), delimiter="\t"))


def write_tsv(path, header, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def git(repo, *a, check=True, env=None, input=None):
    e = dict(os.environ, **(env or {}))
    r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, env=e, input=input)
    if check and r.returncode:
        raise Refuse(f"git {' '.join(a)}: {r.stderr.decode(errors='replace').strip()}")
    return r


def is_link_or_reparse(p):
    try:
        st = os.lstat(p)
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(st.st_mode) or bool(getattr(st, "st_file_attributes", 0) & REPARSE)


def no_reparse_chain(path, stop):
    path, stop = Path(path), Path(stop)
    cur = stop
    for part in path.relative_to(stop).parts:
        cur = cur / part
        if not os.path.lexists(cur):
            return
        if is_link_or_reparse(cur):
            raise Refuse(f"link or reparse point on the path: {cur}")


def check_dest_name(rel):
    if not rel or "\\" in rel or rel.startswith("/") or re.match(r"^[A-Za-z]:", rel):
        raise Refuse(f"destination is not a relative '/' path: {rel!r}")
    if ":" in rel:
        raise Refuse(f"destination names a stream or drive: {rel!r}")
    if any(ord(c) < 32 for c in rel) or any(c in '<>"|?*' for c in rel):
        raise Refuse(f"destination has a forbidden character: {rel!r}")
    for part in rel.split("/"):
        if part in ("", ".", ".."):
            raise Refuse(f"destination has an empty, '.' or '..' part: {rel!r}")
        if part != part.rstrip(" ."):
            raise Refuse(f"destination part ends in a dot or space: {rel!r}")
        if part.split(".")[0].upper() in RESERVED:
            raise Refuse(f"destination part is a reserved Windows name: {rel!r}")
        if part.lower() == ".git":
            raise Refuse(f"destination enters .git: {rel!r}")


def spelling_matches(root, rel):
    cur = Path(root)
    for part in rel.split("/"):
        if not cur.is_dir():
            return
        names = os.listdir(cur)
        if part in names:
            cur = cur / part
            continue
        if any(n.lower() == part.lower() for n in names):
            raise Refuse(f"destination differs only by case from an existing entry: {rel!r}")
        return


def check_destinations(root, rels):
    """Whole-set check: names, case-insensitive uniqueness (including directory prefixes), containment."""
    root = Path(root).resolve()
    seen, dirs = {}, {}
    for rel in rels:
        check_dest_name(rel)
        k = rel.lower()
        if k in seen and seen[k] != rel:
            raise Refuse(f"destinations differ only by case: {seen[k]!r} / {rel!r}")
        if k in seen:
            raise Refuse(f"duplicate destination: {rel!r}")
        seen[k] = rel
        parts = rel.split("/")
        for i in range(1, len(parts)):
            d = "/".join(parts[:i])
            if d.lower() in dirs and dirs[d.lower()] != d:
                raise Refuse(f"directory spelled two ways: {dirs[d.lower()]!r} / {d!r}")
            dirs[d.lower()] = d
        target = Path(os.path.abspath(root / PurePosixPath(rel)))
        if root not in target.parents:
            raise Refuse(f"destination escapes the root: {rel!r}")
        no_reparse_chain(target, root)
        spelling_matches(root, rel)
    for k, rel in seen.items():
        if k in dirs:
            raise Refuse(f"a path is both a file and a directory: {rel!r}")
