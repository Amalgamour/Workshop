"""Pack B #03: write files from pinned Git objects into the workspace, all-or-refuse before the first write.

  python -B import_blobs.py --repo R --manifest M --journal J [--resume]

Manifest columns: row, source (REV:PATH), git_blob, sha256, bytes, destination. Preflight of the WHOLE
batch, before any write:
  REV resolves to a commit and REV:PATH resolves to exactly the pinned git_blob (a matching blob found
  elsewhere in history is not provenance); the blob's bytes have the pinned length and SHA-256;
  destinations pass the Pack A name rules, are unique ignoring case, contain no file/directory clash,
  stay inside the repository with no reparse point, and do not exist (a journal-marked installed file
  with exact bytes is the only exception, on --resume).
Bytes come only from `git cat-file`, never from a working tree. A journal is written before the first
install and each file is marked after it is verified. An interruption leaves it incomplete; only --resume
with the same rows continues. The journal may sit in a lab inside the repository, never in .git or on a
destination. Nothing is deleted or staged.
"""
import argparse, hashlib, json, os, subprocess, sys
from pathlib import Path, PurePosixPath
sys.path.insert(0, str(Path(__file__).resolve().parent))
import custody as C  # noqa: E402


def batch(repo, specs, mode="--batch"):
    data = C.git(repo, "cat-file", mode, input=("\n".join(specs) + "\n").encode("utf-8")).stdout
    out, i = {}, 0
    for spec in specs:
        nl = data.index(b"\n", i)
        head = data[i:nl].decode("utf-8", "replace")
        i = nl + 1
        if head.endswith(" missing") or head.endswith(" ambiguous"):
            out[spec] = None
            continue
        oid, typ, size = head.split()[:3]
        if mode == "--batch":
            out[spec] = (oid, typ, data[i:i + int(size)])
            i += int(size) + 1
        else:
            out[spec] = (oid, typ, None)
    return out


def preflight(repo, rows, done):
    revs = {}
    for r in rows:
        rev = r["source"].split(":", 1)[0]
        if rev not in revs:
            res = C.git(repo, "rev-parse", "--verify", "--quiet", rev + "^{commit}", check=False)
            if res.returncode:
                raise C.Refuse(f"source revision does not resolve to a commit: {rev}")
            revs[rev] = res.stdout.decode().strip()
    specs = [revs[r["source"].split(":", 1)[0]] + ":" + r["source"].split(":", 1)[1] for r in rows]
    found = batch(repo, specs, "--batch-check")
    for r, s in zip(rows, specs):
        f = found[s]
        if f is None:
            raise C.Refuse(f"{r['row']}: {r['source']} does not exist")
        if f[1] != "blob" or f[0] != r["git_blob"]:
            raise C.Refuse(f"{r['row']}: {r['source']} is {f[1]} {f[0]}, pinned blob {r['git_blob']} (provenance)")
    blobs = batch(repo, sorted({r["git_blob"] for r in rows}))
    for r in rows:
        b = blobs[r["git_blob"]]
        if b is None or len(b[2]) != int(r["bytes"]) or C.sha_bytes(b[2]) != r["sha256"]:
            raise C.Refuse(f"{r['row']}: pinned blob {r['git_blob']} does not have the pinned length and SHA-256")
    C.check_destinations(repo, [r["destination"] for r in rows])
    for r in rows:
        t = Path(repo) / PurePosixPath(r["destination"])
        if os.path.lexists(t):
            if r["destination"] in done and t.is_file() and C.sha_file(t) == r["sha256"]:
                continue
            raise C.Refuse(f"{r['row']}: destination already exists: {r['destination']}")
    return {r["git_blob"]: blobs[r["git_blob"]][2] for r in rows}


def write_json(p, d):
    tmp = Path(str(p) + ".tmp")
    tmp.write_text(json.dumps(d, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    os.replace(tmp, p)


def run(a):
    repo = Path(a.repo).resolve()
    rows = C.tsv(a.manifest)
    rid = C.sha_bytes("\n".join("\t".join([r["source"], r["git_blob"], r["sha256"], r["destination"]]) for r in rows).encode())
    journal = Path(a.journal).resolve()
    if (repo / ".git") in journal.parents or journal == repo / ".git":
        raise C.Refuse("the journal must not live inside .git")
    if any(journal == (repo / PurePosixPath(r["destination"])).resolve() for r in rows):
        raise C.Refuse("the journal path is one of the import destinations")
    done = {}
    if journal.exists():
        j = json.loads(journal.read_text(encoding="utf-8"))
        if not a.resume:
            raise C.Refuse(f"a journal exists ({j.get('state')}): {journal}. Use --resume with the same rows, or report it. Nothing written.")
        if j.get("rows_id") != rid or j.get("repo") != str(repo):
            raise C.Refuse("the journal belongs to other rows or another repository; refusing to resume")
        done = j.get("installed", {})
    elif a.resume:
        raise C.Refuse("--resume given but no journal exists")
    data = preflight(repo, rows, done)
    state = {"rows_id": rid, "manifest": str(Path(a.manifest).resolve()), "repo": str(repo), "rows": len(rows),
             "state": "installing", "installed": dict(done)}
    write_json(journal, state)
    fail_after = int(os.environ.get("IMPORT_TEST_FAIL_AFTER", "-1"))
    n = 0
    for r in rows:
        if r["destination"] in state["installed"]:
            continue
        if n == fail_after:
            raise C.Refuse(f"test interruption after {n} install(s); journal left incomplete")
        t = repo / PurePosixPath(r["destination"])
        t.parent.mkdir(parents=True, exist_ok=True)
        C.no_reparse_chain(t, repo)
        tmp = t.parent / (t.name + ".import-tmp")
        with open(tmp, "wb") as f:
            f.write(data[r["git_blob"]])
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, t)
        if C.sha_file(t) != r["sha256"]:
            raise C.Refuse(f"installed bytes differ: {r['destination']}")
        state["installed"][r["destination"]] = r["sha256"]
        write_json(journal, state)
        n += 1
    for r in rows:
        if C.sha_file(repo / PurePosixPath(r["destination"])) != r["sha256"]:
            raise C.Refuse(f"final check failed: {r['destination']}")
    state["state"] = "complete"
    write_json(journal, state)
    print(f"complete: {len(rows)} row(s), {n} written this run, journal {journal}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--journal", required=True)
    ap.add_argument("--resume", action="store_true")
    a = ap.parse_args()
    try:
        sys.exit(run(a))
    except C.Refuse as e:
        print(f"stop: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
