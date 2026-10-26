"""Copy the exact files a preservation manifest lists into a git checkout, verifying every byte.

Draft setup tool, lib-build pass 02 (claude-opus-5-5, 2026-10-26). Not compute. Not run yet except --check.

  python preserve.py --manifest preservation-manifest.tsv --groups P1,P2 --workspace Librarian \
      --source D:\\Git\\Librarian --check
  python preserve.py ... --dest <archive checkout>        # copies; then stage the printed paths by name

--check reads the source only and reports any file whose sha256 no longer matches the manifest.
A copy refuses: a changed source, a path outside the source, or a destination file that already
holds different bytes than the source and was not committed in the destination's HEAD.
"""
import argparse, csv, hashlib, shutil, subprocess, sys
from pathlib import Path


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--groups", required=True, help="comma list, e.g. P1,P2")
    ap.add_argument("--workspace", required=True, help="Librarian or Librarian-rebuild")
    ap.add_argument("--source", required=True)
    ap.add_argument("--dest")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    groups = set(a.groups.split(","))
    src = Path(a.source).resolve()
    rows = [r for r in csv.DictReader(open(a.manifest, encoding="utf-8"), delimiter="\t")
            if r["group"] in groups and r["workspace"] == a.workspace]
    if not rows:
        sys.exit("stop: no manifest rows for those groups and that workspace")
    bad = 0
    for r in rows:
        p = (src / r["path"]).resolve()
        if src not in p.parents:
            sys.exit(f"stop: path escapes the source: {r['path']}")
        if not p.is_file():
            print(f"missing: {r['path']}"); bad += 1; continue
        if sha(p) != r["sha256"]:
            print(f"changed: {r['path']}"); bad += 1
    if bad:
        sys.exit(f"stop: {bad} file(s) no longer match the manifest; nothing copied")
    print(f"source matches: {len(rows)} file(s)")
    if a.check:
        return
    if not a.dest:
        sys.exit("stop: --dest or --check is required")
    dst = Path(a.dest).resolve()
    if not (dst / ".git").exists():
        sys.exit("stop: --dest is not a git checkout")
    for r in rows:
        s, d = src / r["path"], dst / r["path"]
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(s, d)
        if sha(d) != r["sha256"]:
            sys.exit(f"stop: copy differs: {r['path']}")
    print("copied and verified. stage exactly these paths:")
    for r in rows:
        print(r["path"])


if __name__ == "__main__":
    main()
