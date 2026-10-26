"""Addendum 001 #B-A02/#B-A03: verify byte custody at each Git boundary. Development tooling, not runtime.

  python -B gitbytes.py attrs    --repo R --manifest M
  python -B gitbytes.py worktree --repo R --manifest M
  python -B gitbytes.py index    --repo R --manifest M
  python -B gitbytes.py commit   --repo R --manifest M --rev REV

Manifest: TSV with columns path, sha256, bytes (repo-relative '/' paths). Every check reads Git's own
objects: `index` reads the stage-0 blob each path has in the index, `commit` reads REV:path. A correct
worktree file never satisfies an index or commit check. `attrs` requires, for every path, text unset and
no filter, ident or working-tree-encoding, and reports local or configured attribute files. Exit 0 when
every row passes, 2 on the first class of failure (all failing rows are listed).
"""
import argparse, csv, hashlib, os, subprocess, sys
from pathlib import Path, PurePosixPath


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(repo, *a, input=None, check=True):
    r = subprocess.run(["git", "-C", str(repo), "--literal-pathspecs", *a], capture_output=True, input=input)
    if check and r.returncode:
        sys.exit(f"stop: git {' '.join(a)}: {r.stderr.decode(errors='replace').strip()}")
    return r.stdout


def rows(manifest):
    out = list(csv.DictReader(open(manifest, encoding="utf-8", newline=""), delimiter="\t"))
    seen = {}
    for r in out:
        if r["path"] in seen and (seen[r["path"]]["sha256"], seen[r["path"]]["bytes"]) != (r["sha256"], r["bytes"]):
            sys.exit(f"stop: conflicting manifest rows for {r['path']}")
        seen[r["path"]] = r
    return list(seen.values())


def batch_blobs(repo, specs):
    """Read objects through `git cat-file --batch`; returns {spec: bytes or None}."""
    data = git(repo, "cat-file", "--batch", input=("\n".join(specs) + "\n").encode("utf-8"))
    res, i = {}, 0
    for spec in specs:
        nl = data.index(b"\n", i)
        head = data[i:nl].decode("utf-8", "replace")
        i = nl + 1
        if head.endswith(" missing") or head.endswith(" ambiguous"):
            res[spec] = None
            continue
        size = int(head.split()[2])
        res[spec] = data[i:i + size]
        i += size + 1
    return res


def check_bytes(rs, got, label):
    bad = []
    for r in rs:
        b = got.get(r["path"])
        if b is None:
            bad.append(f"{label}: missing {r['path']}")
        elif len(b) != int(r["bytes"]) or sha(b) != r["sha256"]:
            bad.append(f"{label}: differs {r['path']} ({len(b)} bytes, {sha(b)[:12]})")
    return bad


def cmd_worktree(repo, rs):
    got = {}
    for r in rs:
        p = Path(repo) / PurePosixPath(r["path"])
        got[r["path"]] = p.read_bytes() if p.is_file() else None
    return check_bytes(rs, got, "worktree")


def cmd_index(repo, rs):
    want = {r["path"] for r in rs}
    out = git(repo, "ls-files", "-s", "-z")   # the whole index, filtered here: no path list on the command line
    entries, bad = {}, []
    for e in out.split(b"\0"):
        if not e:
            continue
        meta, path = e.decode("utf-8").split("\t", 1)
        if path not in want:
            continue
        mode, oid, stage = meta.split()
        if stage != "0":
            bad.append(f"index: unmerged {path}")
        if mode == "160000":
            bad.append(f"index: gitlink {path}")
        entries[path] = oid
    blobs = batch_blobs(repo, sorted(set(entries.values())))
    got = {p: blobs.get(o) for p, o in entries.items()}
    return bad + check_bytes(rs, got, "index")


def cmd_commit(repo, rs, rev):
    specs = [f"{rev}:{r['path']}" for r in rs]
    blobs = batch_blobs(repo, specs)
    return check_bytes(rs, {r["path"]: blobs[f"{rev}:{r['path']}"] for r in rs}, f"commit {rev[:12]}")


def cmd_attrs(repo, rs):
    names = ["text", "eol", "filter", "ident", "working-tree-encoding", "crlf"]
    out = git(repo, "check-attr", "-z", "--stdin", *names, input=("\0".join(r["path"] for r in rs) + "\0").encode("utf-8"))
    parts = out.split(b"\0")
    eff = {}
    for i in range(0, len(parts) - 2, 3):
        eff.setdefault(parts[i].decode("utf-8"), {})[parts[i + 1].decode()] = parts[i + 2].decode()
    bad = []
    for r in rs:
        a = eff.get(r["path"], {})
        if a.get("text") != "unset":
            bad.append(f"attrs: text is {a.get('text')} for {r['path']}")
        for k in ("filter", "ident", "working-tree-encoding"):
            if a.get(k) not in ("unspecified", "unset"):
                bad.append(f"attrs: {k} is {a.get(k)} for {r['path']}")
        if a.get("crlf") not in ("unspecified", "unset"):
            bad.append(f"attrs: crlf is {a.get('crlf')} for {r['path']}")
    gitdir = Path(git(repo, "rev-parse", "--absolute-git-dir").decode().strip())
    info = gitdir / "info" / "attributes"
    notes = []
    if info.exists() and info.read_text(errors="replace").strip():
        bad.append(f"attrs: local {info} is not empty (no untracked override is allowed)")
    cfg = subprocess.run(["git", "-C", str(repo), "config", "--get", "core.attributesFile"], capture_output=True).stdout.decode().strip()
    if cfg:
        notes.append(f"core.attributesFile = {cfg}")
    for n in notes:
        print("note: " + n)
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=("attrs", "worktree", "index", "commit"))
    ap.add_argument("--repo", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--rev")
    a = ap.parse_args()
    rs = rows(a.manifest)
    if a.cmd == "commit":
        if not a.rev:
            sys.exit("stop: commit needs --rev")
        rev = git(a.repo, "rev-parse", "--verify", a.rev + "^{commit}").decode().strip()
        bad = cmd_commit(a.repo, rs, rev)
    else:
        bad = {"attrs": cmd_attrs, "worktree": cmd_worktree, "index": cmd_index}[a.cmd](a.repo, rs)
    if bad:
        print("\n".join(bad))
        print(f"FAIL {a.cmd}: {len(bad)} of {len(rs)} row(s)")
        sys.exit(2)
    print(f"pass {a.cmd}: {len(rs)} row(s)")


if __name__ == "__main__":
    main()
