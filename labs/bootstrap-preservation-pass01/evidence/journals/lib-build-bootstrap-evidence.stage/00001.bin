"""Pack A #02: copy pinned files into an independent git checkout, all-or-refuse before the first write.

  python -B preserve_copy.py --manifest preservation-manifest.tsv --archive main-worktree \
      --source-root D:\\Git\\Librarian --dest <clone> --expect-head <40-hex> \
      --allow-replace-file <file of paths> --journal <journal.json> [--resume] [--stage]

Manifest columns: group, source (absolute path), destination (repo-relative, '/'), sha256, bytes, archive.

Whole-batch preflight, before any destination write:
  every source lies inside a --source-root, is a regular file (no link or reparse point on the way),
  and matches its pinned length and SHA-256;
  the destination is the top of an independent repository (.git is a directory, no alternates, no
  worktree), HEAD is the expected commit, and source and destination do not alias;
  every destination is relative, '/'-separated, unique ignoring case, inside the repository, free of
  traversal, drive letters, ':' streams, reserved or trailing-dot/space Windows names, control
  characters, links and reparse points, and an existing parent's spelling matches;
  each destination is absent, already the exact bytes, or listed in --allow-replace and tracked and
  clean in HEAD, index and worktree;
  the index and worktree hold no change except batch destinations already at their exact bytes.
Then the bytes are staged in the journal folder and re-verified, the destination conditions are
checked again, the journal is written, and each file is installed (temp file, flush, replace),
verified, and marked. Success means every row is installed and verified. An interruption leaves the
journal incomplete; only --resume with the same manifest rows and HEAD continues it. No all-files
atomicity is promised. Nothing is deleted or cleaned up.
"""
import argparse, csv, hashlib, json, os, re, shutil, stat, subprocess, sys
from pathlib import Path, PurePosixPath

RESERVED = {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"} | {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)} \
    | {f"COM{c}" for c in "¹²³"} | {f"LPT{c}" for c in "¹²³"}
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


def is_link_or_reparse(p):
    try:
        st = os.lstat(p)
    except FileNotFoundError:
        return False
    if stat.S_ISLNK(st.st_mode):
        return True
    return bool(getattr(st, "st_file_attributes", 0) & REPARSE)


def no_reparse_chain(path, stop):
    """Every existing component from stop down to path is a plain directory or file."""
    path, stop = Path(path), Path(stop)
    cur = stop
    for part in path.relative_to(stop).parts:
        cur = cur / part
        if not os.path.lexists(cur):
            return
        if is_link_or_reparse(cur):
            raise Refuse(f"link or reparse point on the path: {cur}")


def git(repo, *a, check=True):
    r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True)
    if check and r.returncode:
        raise Refuse(f"git {' '.join(a)}: {r.stderr.decode(errors='replace').strip()}")
    return r


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
    """An existing component must be spelled exactly as the destination spells it."""
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


def load_rows(manifest, archive):
    rows = [r for r in csv.DictReader(open(manifest, encoding="utf-8", newline=""), delimiter="\t") if r["archive"] == archive]
    if not rows:
        raise Refuse(f"no manifest rows for archive {archive!r}")
    return rows


def rows_id(rows):
    text = "\n".join("\t".join([r["source"], r["destination"], r["sha256"], r["bytes"]]) for r in rows)
    return sha_bytes(text.encode("utf-8"))


def independent_repo(dest, expect_head):
    top = git(dest, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if Path(top).resolve() != dest:
        raise Refuse(f"destination is not the top of a repository: {dest}")
    dotgit = dest / ".git"
    if not dotgit.is_dir() or is_link_or_reparse(dotgit):
        raise Refuse("destination .git is not a plain directory (a worktree or a link)")
    alt = dotgit / "objects" / "info" / "alternates"
    if alt.exists() and alt.read_text(errors="replace").strip():
        raise Refuse("destination borrows objects through alternates (a shared clone)")
    if (dotgit / "commondir").exists():
        raise Refuse("destination is a linked worktree")
    head = git(dest, "rev-parse", "HEAD").stdout.decode().strip()
    if head != expect_head:
        raise Refuse(f"destination HEAD {head} is not the expected {expect_head}")


def status_paths(dest):
    out = git(dest, "status", "--porcelain=v1", "-uall", "-z", "--ignored=no").stdout
    paths, entries, i = {}, [e for e in out.split(b"\0") if e], 0
    while i < len(entries):
        e = entries[i].decode("utf-8")
        code, path = e[:2], e[3:]
        if code[0] in "RC":
            i += 1
        paths[path] = code
        i += 1
    return paths


def tracked_clean(dest, rel):
    if git(dest, "ls-tree", "HEAD", "--", rel).stdout.strip() == b"":
        return False
    if git(dest, "diff", "--quiet", "HEAD", "--", rel, check=False).returncode:
        return False
    if git(dest, "diff", "--quiet", "--cached", "--", rel, check=False).returncode:
        return False
    return True


def preflight(rows, roots, dest, expect_head, allowed, journal_done, resume=False):
    """Raises Refuse on the first problem; returns the per-row plan. Writes nothing."""
    independent_repo(dest, expect_head)
    for root in roots:
        if root == dest or root in dest.parents or dest in root.parents:
            raise Refuse(f"source root and destination alias: {root} / {dest}")
    seen = {}
    plan = []
    for r in rows:
        rel = r["destination"]
        check_dest_name(rel)
        key = rel.lower()
        if key in seen:
            raise Refuse(f"two rows share a destination (ignoring case): {seen[key]!r} and {rel!r}")
        seen[key] = rel
        src = Path(r["source"])
        if not src.is_absolute():
            raise Refuse(f"source is not absolute: {src}")
        root = next((x for x in roots if x in Path(os.path.abspath(src)).parents), None)
        if root is None:
            raise Refuse(f"source is outside every --source-root: {src}")
        no_reparse_chain(Path(os.path.abspath(src)), root)
        rsrc = src.resolve()
        if root not in rsrc.parents:
            raise Refuse(f"source resolves outside its root: {src}")
        if not rsrc.is_file():
            raise Refuse(f"source is not a regular file: {src}")
        if rsrc.stat().st_size != int(r["bytes"]) or sha_file(rsrc) != r["sha256"]:
            raise Refuse(f"source changed since the manifest was pinned: {src}")
        target = dest / PurePosixPath(rel)
        if any(x in Path(os.path.abspath(target)).parents or x == Path(os.path.abspath(target)) for x in roots):
            raise Refuse(f"destination lies inside a source root: {target}")
        no_reparse_chain(target, dest)
        if dest not in Path(os.path.abspath(target)).parents:
            raise Refuse(f"destination escapes the repository: {rel}")
        spelling_matches(dest, rel)
        if target.exists():
            if not target.is_file():
                raise Refuse(f"destination exists and is not a file: {rel}")
            if sha_file(target) == r["sha256"]:
                plan.append((r, src, target, "present"))
                continue
            if rel in journal_done:
                raise Refuse(f"journal marks {rel} installed but its bytes differ")
            if rel not in allowed:
                raise Refuse(f"destination exists with other bytes and is not an allowed replacement: {rel}")
            if not tracked_clean(dest, rel):
                raise Refuse(f"allowed replacement is not tracked and clean in HEAD, index and worktree: {rel}")
            plan.append((r, src, target, "replace"))
        else:
            plan.append((r, src, target, "new"))
    by_rel = {r["destination"]: r for r in rows}
    for path, code in status_paths(dest).items():
        if resume and path.endswith(".preserve-tmp") and path[: -len(".preserve-tmp")] in by_rel                 and path[: -len(".preserve-tmp")] not in journal_done:
            continue  # this tool's own partial write from the interrupted run; the install overwrites it
        r = by_rel.get(path)
        tgt = dest / PurePosixPath(path)
        if r is None or not tgt.is_file() or sha_file(tgt) != r["sha256"]:
            raise Refuse(f"the index or worktree holds an unrelated or conflicting change: {code} {path}")
    return plan


def write_json(p, data):
    tmp = Path(str(p) + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=1, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, p)


def run(a):
    dest = Path(a.dest).resolve()
    roots = [Path(x).resolve() for x in a.source_root]
    rows = load_rows(a.manifest, a.archive)
    rid = rows_id(rows)
    allowed = set()
    if a.allow_replace_file:
        allowed = {l.strip() for l in Path(a.allow_replace_file).read_text(encoding="utf-8").splitlines() if l.strip()}
    journal = Path(a.journal).resolve()
    if dest in journal.parents:
        raise Refuse("the journal must live outside the destination repository")
    done = {}
    if journal.exists():
        j = json.loads(journal.read_text(encoding="utf-8"))
        if j.get("state") == "complete" and not a.resume:
            pass  # a finished journal: a retry is checked row by row as 'present'
        elif not a.resume:
            raise Refuse(f"an incomplete journal exists: {journal}. Re-run with --resume and the same manifest rows "
                         f"and --expect-head, or move the journal aside after reporting it. Nothing was written.")
        if a.resume:
            if j.get("rows_id") != rid or j.get("expect_head") != a.expect_head or j.get("dest") != str(dest):
                raise Refuse("the journal belongs to other rows, another HEAD or another destination; refusing to resume")
        done = {k: v for k, v in j.get("installed", {}).items()}
    elif a.resume:
        raise Refuse("--resume given but no journal exists")
    plan = preflight(rows, roots, dest, a.expect_head, allowed, done, a.resume)
    stage_dir = journal.parent / (journal.stem + ".stage")
    stage_dir.mkdir(parents=True, exist_ok=True)
    staged = []
    for i, (r, src, target, mode) in enumerate(plan):
        if mode == "present":
            continue
        data = Path(src).read_bytes()
        if len(data) != int(r["bytes"]) or sha_bytes(data) != r["sha256"]:
            raise Refuse(f"source changed while staging: {src}")
        sp = stage_dir / f"{i:05d}.bin"
        sp.write_bytes(data)
        if sha_file(sp) != r["sha256"]:
            raise Refuse(f"staged copy differs: {src}")
        staged.append((r, sp, target, mode))
    plan2 = preflight(rows, roots, dest, a.expect_head, allowed, done, a.resume)  # destination conditions again
    if [(p[0]["destination"], p[3]) for p in plan2] != [(p[0]["destination"], p[3]) for p in plan]:
        raise Refuse("destination conditions changed between preflight and install")
    state = {"rows_id": rid, "manifest": str(Path(a.manifest).resolve()), "archive": a.archive, "dest": str(dest),
             "expect_head": a.expect_head, "state": "installing", "rows": len(rows),
             "installed": {**done, **{p[0]["destination"]: p[0]["sha256"] for p in plan if p[3] == "present"}}}
    write_json(journal, state)
    fail_after = int(os.environ.get("PRESERVE_TEST_FAIL_AFTER", "-1"))
    for n, (r, sp, target, mode) in enumerate(staged):
        if n == fail_after:
            raise Refuse(f"test interruption after {n} install(s); journal left incomplete")
        target.parent.mkdir(parents=True, exist_ok=True)
        no_reparse_chain(target, dest)
        tmp = target.parent / (target.name + ".preserve-tmp")
        with open(tmp, "wb") as f:
            f.write(sp.read_bytes())
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, target)
        if sha_file(target) != r["sha256"]:
            raise Refuse(f"installed bytes differ: {r['destination']}")
        state["installed"][r["destination"]] = r["sha256"]
        write_json(journal, state)
    for r in rows:
        t = dest / PurePosixPath(r["destination"])
        if not t.is_file() or sha_file(t) != r["sha256"]:
            raise Refuse(f"final check failed: {r['destination']}")
    state["state"] = "complete"
    write_json(journal, state)
    if a.stage:
        paths = [r["destination"] for r in rows]
        git(dest, "--literal-pathspecs", "add", "--", *paths)
    counts = {}
    for p in plan:
        counts[p[3]] = counts.get(p[3], 0) + 1
    print(f"complete: {len(rows)} row(s) {counts}, journal {journal}")
    for r in rows:
        print(r["destination"])
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--archive", required=True)
    ap.add_argument("--source-root", action="append", required=True)
    ap.add_argument("--dest", required=True)
    ap.add_argument("--expect-head", required=True)
    ap.add_argument("--allow-replace-file")
    ap.add_argument("--journal", required=True)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--stage", action="store_true", help="git add exactly the manifest destinations")
    a = ap.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", a.expect_head):
        print("stop: --expect-head must be a full 40-hex commit")
        sys.exit(2)
    try:
        sys.exit(run(a))
    except Refuse as e:
        print(f"stop: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
