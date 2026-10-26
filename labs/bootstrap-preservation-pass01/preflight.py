"""Pack A #01 and #04: read-only preflight and fingerprint capture.

  python -B preflight.py capture --label before --out evidence/fingerprint-before.json
  python -B preflight.py compare evidence/fingerprint-before.json evidence/fingerprint-after.json

capture verifies the pack's own hashes, every preservation source row (length and SHA-256), and the
lib-build workspace baseline, then fingerprints both old checkouts: HEAD, status --porcelain=v1 -uall,
for-each-ref, stash list, worktree list, and the SHA-256 of every file the status names. Reads of the
old repositories run with GIT_OPTIONAL_LOCKS=0, so git does not refresh their index. Nothing is written
outside --out.
"""
import argparse, csv, hashlib, json, os, subprocess, sys
from pathlib import Path

PACK = Path(r"D:\Git\lib-build\packs\lib-build-bootstrap-pass01-2026-10-26")
LB = Path(r"D:\Git\lib-build")
OLD = {"Librarian": Path(r"D:\Git\Librarian"), "Librarian-rebuild": Path(r"D:\Git\Librarian-rebuild")}
ENV = dict(os.environ, GIT_OPTIONAL_LOCKS="0")


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def git(repo, *a):
    r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, env=ENV)
    if r.returncode:
        raise SystemExit(f"stop: git {' '.join(a)} failed in {repo}: {r.stderr.decode(errors='replace')}")
    return r.stdout


def tsv(path):
    return list(csv.DictReader(open(path, encoding="utf-8", newline=""), delimiter="\t"))


def check_rows(rows, root_of, label):
    bad = []
    for r in rows:
        p = root_of(r)
        if not p.is_file():
            bad.append(f"{label} missing: {p}")
            continue
        size = p.stat().st_size
        if str(size) != r["bytes"]:
            bad.append(f"{label} length {size} != {r['bytes']}: {p}")
        elif sha(p) != r["sha256"]:
            bad.append(f"{label} sha256 differs: {p}")
    return bad


def fingerprint(repo):
    status = git(repo, "status", "--porcelain=v1", "-uall", "-z")
    files = {}
    entries = [e for e in status.split(b"\0") if e]
    i = 0
    while i < len(entries):
        e = entries[i].decode("utf-8")
        code, path = e[:2], e[3:]
        if code[0] in "RC":
            i += 1  # the source path of a rename follows
        p = repo / path
        files[path] = sha(p) if p.is_file() else None
        i += 1
    return {
        "head": git(repo, "rev-parse", "HEAD").decode().strip(),
        "status_sha256": hashlib.sha256(status).hexdigest(),
        "status_entries": len(entries),
        "for_each_ref": git(repo, "for-each-ref", "--format=%(objectname) %(refname)").decode(),
        "stash_list": git(repo, "stash", "list").decode(),
        "worktree_list": git(repo, "worktree", "list", "--porcelain").decode(),
        "status_file_sha256": files,
    }


def capture(label, out):
    bad = []
    bad += check_rows(tsv(PACK / "manifest.sha256.tsv"), lambda r: PACK / r["path"], "package")
    bad += check_rows(tsv(PACK / "preservation-manifest.tsv"), lambda r: Path(r["source"]), "source")
    bad += check_rows(tsv(PACK / "workspace-baseline.tsv"), lambda r: LB / r["path"], "baseline")
    result = {
        "label": label,
        "package_rows": len(tsv(PACK / "manifest.sha256.tsv")),
        "preservation_rows": len(tsv(PACK / "preservation-manifest.tsv")),
        "baseline_rows": len(tsv(PACK / "workspace-baseline.tsv")),
        "problems": bad,
        "old": {name: fingerprint(repo) for name, repo in OLD.items()},
    }
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(result, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"{label}: package {result['package_rows']}, sources {result['preservation_rows']}, baseline {result['baseline_rows']}, problems {len(bad)}")
    for name, f in result["old"].items():
        print(f"  {name}: HEAD {f['head'][:12]} status {f['status_sha256'][:16]} entries {f['status_entries']} hashed files {sum(1 for v in f['status_file_sha256'].values() if v)}")
    for b in bad:
        print("  " + b)
    return 1 if bad else 0


def compare(a, b):
    x, y = json.loads(Path(a).read_text(encoding="utf-8")), json.loads(Path(b).read_text(encoding="utf-8"))
    diffs = []
    for name in OLD:
        for key in ("head", "status_sha256", "for_each_ref", "stash_list", "worktree_list"):
            if x["old"][name][key] != y["old"][name][key]:
                diffs.append(f"{name}: {key} changed")
        fa, fb = x["old"][name]["status_file_sha256"], y["old"][name]["status_file_sha256"]
        for path in sorted(set(fa) | set(fb)):
            if fa.get(path) != fb.get(path):
                diffs.append(f"{name}: file changed: {path}")
    if y["problems"]:
        diffs += [f"after: {p}" for p in y["problems"]]
    print("unchanged" if not diffs else "\n".join(diffs))
    return 1 if diffs else 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("capture"); c.add_argument("--label", required=True); c.add_argument("--out", required=True)
    m = sub.add_parser("compare"); m.add_argument("a"); m.add_argument("b")
    a = ap.parse_args()
    sys.exit(capture(a.label, a.out) if a.cmd == "capture" else compare(a.a, a.b))


if __name__ == "__main__":
    main()
