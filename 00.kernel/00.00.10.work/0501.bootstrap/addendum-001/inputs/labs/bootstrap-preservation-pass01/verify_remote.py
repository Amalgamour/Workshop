"""Pack A #04: verify the pushed archive refs from a fresh clone, by git objects, not by a checkout.

  python -B verify_remote.py <fresh clone>

For each archive branch: the remote ref equals the expected commit; its parent chain reaches the
expected base; every manifest row for that archive exists at its destination with the pinned length
and SHA-256; every archive-evidence/HASHES.tsv row matches; and the branch adds no other path to its
base. The two tags must point at the baseline commits.
"""
import csv, hashlib, io, subprocess, sys
from pathlib import Path

PACK = Path(r"D:\Git\lib-build\packs\lib-build-bootstrap-pass01-2026-10-26")
MAIN = "14676ca3c01833cc1b472198e62e3451ef706ec3"
REB = "de3b8ebc3df3e1da28c4d675963699644b78afab"
BRANCHES = {
    "archive/librarian-worktree-2026-10-26": ("main-worktree", MAIN, "e8b1a994da07000fa576fd771e455a94718ed431"),
    "archive/rebuild-worktree-2026-10-26": ("rebuild-worktree", REB, "586cfa4ae055c29a98c1106bb70143901c57cc11"),
    "archive/lib-build-bootstrap-2026-10-26": ("bootstrap", MAIN, "fe42b017b5e8c288f70878d696cb227b09ab5a8e"),
}
TAGS = {"archive/main-14676ca": MAIN, "archive/rebuild-de3b8eb": REB}


def git(repo, *a):
    r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True)
    if r.returncode:
        raise SystemExit(f"stop: git {' '.join(a)}: {r.stderr.decode(errors='replace')}")
    return r.stdout


def main(clone):
    rows = list(csv.DictReader(open(PACK / "preservation-manifest.tsv", encoding="utf-8", newline=""), delimiter="\t"))
    bad, report = [], []
    remote = dict(reversed(l.split("\t")) for l in git(clone, "ls-remote", "origin").decode().splitlines())
    for tag, want in TAGS.items():
        got = remote.get(f"refs/tags/{tag}")
        if got != want:
            bad.append(f"tag {tag}: {got} != {want}")
    for branch, (arc, base, want) in BRANCHES.items():
        got = remote.get(f"refs/heads/{branch}")
        if got != want:
            bad.append(f"{branch}: remote {got} != {want}")
            continue
        chain = git(clone, "rev-list", "--first-parent", f"{base}..{want}").decode().split()
        if len(chain) != 3 or git(clone, "rev-parse", f"{want}~3").decode().strip() != base:
            bad.append(f"{branch}: not three commits (rows, evidence, exact bytes) on {base}")
        added = set(git(clone, "diff", "--name-only", base, want).decode().splitlines())
        mine = [r for r in rows if r["archive"] == arc]
        n_bytes = 0
        for r in mine:
            data = git(clone, "cat-file", "blob", f"{want}:{r['destination']}")
            n_bytes += len(data)
            if len(data) != int(r["bytes"]) or hashlib.sha256(data).hexdigest() != r["sha256"]:
                bad.append(f"{branch}: {r['destination']} differs")
        hashes = list(csv.DictReader(io.StringIO(git(clone, "show", f"{want}:archive-evidence/HASHES.tsv").decode("utf-8")), delimiter="\t"))
        for h in hashes:
            data = git(clone, "cat-file", "blob", f"{want}:{h['path']}")
            if len(data) != int(h["bytes"]) or hashlib.sha256(data).hexdigest() != h["sha256"]:
                bad.append(f"{branch}: evidence {h['path']} differs")
        expected = {r["destination"] for r in mine} | {h["path"] for h in hashes} | {"archive-evidence/HASHES.tsv"}
        extra = added - expected
        missing_change = {r["destination"] for r in mine} - added
        if extra:
            bad.append(f"{branch}: paths beyond the manifest: {sorted(extra)[:5]}")
        report.append(f"{branch} {want}: rows {len(mine)} ({n_bytes} bytes) verified; evidence {len(hashes)} + HASHES.tsv verified; "
                      f"changed paths {len(added)}; unchanged-by-design rows {len(missing_change)}")
    print("\n".join(report))
    print("tags: " + ", ".join(f"{t} {remote.get('refs/tags/' + t)}" for t in TAGS))
    print("PASS" if not bad else "FAIL\n" + "\n".join(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
