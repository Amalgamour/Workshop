"""Write the files an import manifest lists, from git objects, into the lib-build checkout.

Draft setup tool, lib-build pass 02 (claude-opus-5-5, 2026-10-26). Not compute. Not run yet except --check.

  python import.py --manifest import-manifest.tsv --tier minimum --repo D:\\Git\\lib-build --check
  python import.py --manifest import-manifest.tsv --tier minimum --repo D:\\Git\\lib-build

Bytes come only from `git cat-file blob <git_blob>` in --repo (after `git fetch`), never from a
working tree. A row is refused when its blob is absent, its sha256 differs from the manifest, its
destination escapes the repo, or its destination already exists (no overwrite, no renumbering).
"""
import argparse, csv, hashlib, subprocess, sys
from pathlib import Path


def blob(repo, b):
    r = subprocess.run(["git", "-C", str(repo), "cat-file", "blob", b], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--tier", required=True, choices=("minimum", "later"))
    ap.add_argument("--ids", help="comma list, e.g. M2,M3; default every id in the tier")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    repo = Path(a.repo).resolve()
    ids = set(a.ids.split(",")) if a.ids else None
    rows = [r for r in csv.DictReader(open(a.manifest, encoding="utf-8"), delimiter="\t")
            if r["tier"] == a.tier and (ids is None or r["id"] in ids)]
    seen, bad = set(), []
    for r in rows:
        d = (repo / r["destination"]).resolve()
        if repo not in d.parents:
            bad.append(f"escapes repo: {r['destination']}")
        if r["destination"] in seen:
            bad.append(f"two rows, one destination: {r['destination']}")
        seen.add(r["destination"])
        if d.exists():
            bad.append(f"destination exists: {r['destination']}")
        data = blob(repo, r["git_blob"])
        if data is None:
            bad.append(f"blob missing: {r['git_blob']} ({r['source']})")
        elif hashlib.sha256(data).hexdigest() != r["sha256"]:
            bad.append(f"sha256 differs: {r['source']}")
    if bad:
        print("\n".join(bad))
        sys.exit(f"stop: {len(bad)} problem(s); nothing written")
    print(f"ready: {len(rows)} row(s)")
    if a.check:
        return
    for r in rows:
        d = repo / r["destination"]
        d.parent.mkdir(parents=True, exist_ok=True)
        d.write_bytes(blob(repo, r["git_blob"]))
    print(f"written: {len(rows)} file(s). stage them by the manifest's destination list")


if __name__ == "__main__":
    main()
