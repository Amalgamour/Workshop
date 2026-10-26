"""Pack B #04: byte-exact copies of the packs onto 0501.bootstrap, and of the pack manifests onto 0410.imports,
from the baseline commit's Git objects (provenance), through import_blobs.py. Also copies the generated
step 03 manifests and selection register onto 0410.imports (new files; hashes recorded by step 07).
"""
import shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import custody as C  # noqa: E402

BASE = "d0bdd53a1d9d3cffda600b7102e3bcb0934359eb"   # the baseline commit (Pack B #02)
EV = C.LAB / "evidence" / "step04"
WORK = "00.kernel/00.00.10.work"


def tree(prefix):
    out = C.git(C.LB, "ls-tree", "-r", "-z", BASE, "--", prefix).stdout.split(b"\0")
    for e in out:
        if e:
            meta, path = e.decode("utf-8").split("\t", 1)
            yield path, meta.split()[2]


def main():
    EV.mkdir(parents=True, exist_ok=True)
    rows = []
    for src_dir, dest in (("packs/lib-build-bootstrap-pass01-2026-10-26/", f"{WORK}/0501.bootstrap/pack/"),
                          ("packs/lib-build-pack-B-addendum-001-2026-10-26/", f"{WORK}/0501.bootstrap/addendum-001/")):
        for path, oid in tree(src_dir):
            rows.append((path, oid, dest + path[len(src_dir):]))
    for n in ("snapshot-import-manifest.tsv", "selected-reference-manifest.tsv", "preservation-manifest.tsv", "workspace-baseline.tsv"):
        path = f"packs/lib-build-bootstrap-pass01-2026-10-26/{n}"
        oid = C.git(C.LB, "rev-parse", f"{BASE}:{path}").stdout.decode().strip()
        rows.append((path, oid, f"{WORK}/0410.imports/manifests/pack-{n}"))
    table = []
    for i, (path, oid, dest) in enumerate(rows):
        data = C.git(C.LB, "cat-file", "blob", oid).stdout
        table.append((f"K{i + 1:03d}", f"{BASE}:{path}", oid, C.sha_bytes(data), len(data), dest))
    C.write_tsv(EV / "import-copies.tsv", ["row", "source", "git_blob", "sha256", "bytes", "destination"], table)
    r = subprocess.run([sys.executable, "-B", str(C.LAB / "import_blobs.py"), "--repo", str(C.LB), "--manifest", str(EV / "import-copies.tsv"),
                        "--journal", str(EV / "journal-copies.json")], capture_output=True, text=True)
    print(f"copies: exit {r.returncode}: {r.stdout.strip()}")
    if r.returncode:
        sys.exit(2)
    gen = C.LB / WORK / "0410.imports" / "manifests"
    for n in ("import-snapshots.tsv", "import-selected.tsv", "import-p1.tsv", "import-claude.tsv", "selection-register.tsv", "custody-imports.tsv"):
        src = C.LAB / "evidence" / "step03" / n
        dst = gen / f"step03-{n}"
        if dst.exists():
            sys.exit(f"stop: exists {dst}")
        shutil.copyfile(src, dst)
        if C.sha_file(dst) != C.sha_file(src):
            sys.exit(f"stop: copy differs {n}")
    print(f"generated manifests copied: 6 into {gen}")


if __name__ == "__main__":
    main()
