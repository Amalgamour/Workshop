"""Pack A #03: gather one branch's archive-evidence/ files and pin them in a manifest preserve_copy.py reads.

  python -B make_evidence.py <branch-name>

Writes evidence-out/<name>/archive-evidence/ (copies of the pack manifest, the tool, its tests and this
run's evidence) and evidence-out/<name>.manifest.tsv. The archive-evidence/HASHES.tsv inside lists every
other evidence file with its SHA-256 and length.
"""
import csv, hashlib, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACK = Path(r"D:\Git\lib-build\packs\lib-build-bootstrap-pass01-2026-10-26")


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(name):
    out = HERE / "evidence-out" / name
    root = out / "archive-evidence"
    if out.exists():
        sys.exit(f"stop: {out} exists; not overwriting evidence")
    files = {
        "preservation-manifest.tsv": PACK / "preservation-manifest.tsv",
        "tool/preserve_copy.py": HERE / "preserve_copy.py",
        "tool/test_preserve_copy.py": HERE / "test_preserve_copy.py",
        "tool/preflight.py": HERE / "preflight.py",
        "tool/make_evidence.py": HERE / "make_evidence.py",
        "evidence/test-output.txt": HERE / "evidence" / "test-output.txt",
        "evidence/preflight-before.txt": HERE / "evidence" / "preflight-before.txt",
        "evidence/fingerprint-before.json": HERE / "evidence" / "fingerprint-before.json",
        f"evidence/allow-replace-{name}.txt": HERE / "evidence" / f"allow-replace-{name}.txt",
        f"evidence/copy-{name}.txt": HERE / "evidence" / f"copy-{name}.txt",
        f"evidence/journal-{name}.json": HERE / "evidence" / "journals" / f"{name}.json",
        f"evidence/commit-message-{name}.txt": HERE / "evidence" / "messages" / f"{name}.txt",
    }
    rows = []
    for rel, src in files.items():
        d = root / rel
        d.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, d)
        if sha(d) != sha(src):
            sys.exit(f"stop: copy differs: {rel}")
        rows.append((rel, sha(d), d.stat().st_size))
    hashes = root / "HASHES.tsv"
    with open(hashes, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["path", "sha256", "bytes"])
        for r in rows:
            w.writerow(["archive-evidence/" + r[0], r[1], r[2]])
    rows.append(("HASHES.tsv", sha(hashes), hashes.stat().st_size))
    man = HERE / "evidence-out" / f"{name}.manifest.tsv"
    with open(man, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["group", "source", "destination", "sha256", "bytes", "archive"])
        for rel, h, n in rows:
            w.writerow(["E", str(root / rel), "archive-evidence/" + rel, h, n, "evidence"])
    print(f"{name}: {len(rows)} evidence file(s) -> {man}")


if __name__ == "__main__":
    main(sys.argv[1])
