"""Pack B #B-A01 and #01: verify dependencies and refresh the baseline. Read-only except --out.

  python -B step01_baseline.py --out evidence/step01

Verifies: the addendum manifest, its pinned dependencies, the original package manifest, the archive
refs on GitHub (ls-remote), the original 39-file baseline. Inventories everything in lib-build except
Git metadata: nested repositories are recorded by HEAD and remote, never walked into. Writes the
additive baseline (every regular file outside nested repositories, with a disposition) and checks that
no .git exists yet and no reparse point sits anywhere in the tree.
"""
import argparse, json, os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import custody as C  # noqa: E402

PACK_B_LABS = ("labs/bootstrap-establish-pass01/", "labs/bootstrap-git-bytes-pass01/")
SCRATCH = {  # generated scratch: excluded from staging by tracked ignore rules (addendum #B-A04)
    "labs/bootstrap-preservation-pass01/clones/": "generated clones (Pack A); remote archive refs identify them",
    "labs/bootstrap-preservation-pass01/tests-tmp/": "generated test repositories (Pack A test run)",
    "labs/bootstrap-git-bytes-pass01/scratch/": "generated fixture repositories (addendum #B-A02)",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--after-init", action="store_true", help="the root .git is expected (Pack B #02); it is never walked")
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    problems, notes = [], []

    def rows_ok(rows, root_of, label):
        for r in rows:
            p = root_of(r)
            if not p.is_file():
                problems.append(f"{label} missing: {p}")
            elif str(p.stat().st_size) != r["bytes"] or C.sha_file(p) != r["sha256"]:
                problems.append(f"{label} differs: {p}")
        return len(rows)

    n_add = rows_ok(C.tsv(C.ADD / "manifest.sha256.tsv"), lambda r: C.ADD / r["path"], "addendum package")
    n_dep = rows_ok(C.tsv(C.ADD / "dependencies.sha256.tsv"), lambda r: Path(r["source"]), "addendum dependency")
    n_pack = rows_ok(C.tsv(C.PACK / "manifest.sha256.tsv"), lambda r: C.PACK / r["path"], "original package")
    n_base = rows_ok(C.tsv(C.PACK / "workspace-baseline.tsv"), lambda r: C.LB / r["path"], "original baseline")
    remote = {}
    for line in C.git(C.LB.parent, "ls-remote", C.REMOTE).stdout.decode().splitlines():
        h, ref = line.split("\t")
        remote[ref] = h
    deps = C.tsv(C.ADD / "archive-dependencies.tsv")
    for d in deps:
        if remote.get(d["ref"]) != d["commit"]:
            problems.append(f"archive ref moved: {d['ref']} is {remote.get(d['ref'])}, pinned {d['commit']}")
    for name, want in (("refs/heads/main", C.MAIN), ("refs/heads/rebuild", C.REB),
                       ("refs/tags/archive/main-14676ca", C.MAIN), ("refs/tags/archive/rebuild-de3b8eb", C.REB)):
        if remote.get(name) != want:
            problems.append(f"remote {name} is {remote.get(name)}, expected {want}")
    if "refs/heads/workshop" in remote:
        problems.append(f"a remote workshop branch already exists: {remote['refs/heads/workshop']}")
    if (C.LB / ".git").exists() and not a.after_init:
        problems.append("lib-build already has .git")
    if a.after_init and not (C.LB / ".git").is_dir():
        problems.append("--after-init given but lib-build has no .git directory")

    original = {r["path"] for r in C.tsv(C.PACK / "workspace-baseline.tsv")}
    inventory, nested, reparse = [], [], []
    for dirpath, dirnames, filenames in os.walk(C.LB):
        d = Path(dirpath)
        rel_d = d.relative_to(C.LB).as_posix()
        if C.is_link_or_reparse(d) and d != C.LB:
            reparse.append(rel_d)
            dirnames[:] = []
            continue
        if d == C.LB and a.after_init:
            dirnames[:] = [x for x in dirnames if x != ".git"]
        elif ".git" in dirnames or ".git" in filenames:
            if d == C.LB:
                problems.append("lib-build root has .git")
                dirnames[:] = [x for x in dirnames if x != ".git"]
            else:
                head = C.git(d, "rev-parse", "HEAD", check=False).stdout.decode().strip()
                branch = C.git(d, "branch", "--show-current", check=False).stdout.decode().strip()
                url = C.git(d, "config", "--get", "remote.origin.url", check=False).stdout.decode().strip()
                nested.append((rel_d + "/", head, branch, url))
                dirnames[:] = []
                continue
        for f in sorted(filenames):
            p = d / f
            rel = p.relative_to(C.LB).as_posix()
            if C.is_link_or_reparse(p):
                reparse.append(rel)
                continue
            scratch = next((s for s in SCRATCH if rel.startswith(s)), None)
            if a.after_init and rel in (".gitignore", ".gitattributes"):
                disp = "control: tracked by the policy commit"
            elif not scratch and rel.startswith(PACK_B_LABS):
                disp = "deferred: Pack B working lab; committed at the evidence boundary with its own manifest"
            else:
                disp = ("excluded: " + SCRATCH[scratch]) if scratch else ("original baseline" if rel in original else "additive: stage")
            inventory.append((rel, C.sha_file(p), p.stat().st_size, disp))
        dirnames.sort()
    for rel, *_ in nested:
        if not any(rel.startswith(s) for s in SCRATCH):
            problems.append(f"nested repository outside declared scratch: {rel}")
    if reparse:
        problems.append(f"reparse points in lib-build: {reparse[:5]}")
    inv_paths = {r[0] for r in inventory}
    missing_orig = sorted(original - inv_paths)
    if missing_orig:
        problems.append(f"original baseline paths missing from inventory: {missing_orig[:5]}")

    C.write_tsv(out / "additive-baseline-2026-10-26.tsv", ["path", "sha256", "bytes", "disposition"], inventory)
    C.write_tsv(out / "nested-repositories.tsv", ["path", "head", "branch", "remote"], nested)
    counts = {}
    for r in inventory:
        k = r[3].split(":")[0]
        counts[k] = counts.get(k, 0) + 1
    summary = {"addendum_package_rows": n_add, "addendum_dependencies": n_dep, "original_package_rows": n_pack,
               "original_baseline_rows": n_base, "archive_refs": {d["ref"]: remote.get(d["ref"]) for d in deps},
               "inventory_files": len(inventory), "inventory_by_disposition": counts,
               "nested_repositories": len(nested), "reparse_points": reparse, "problems": problems}
    (out / "step01.json").write_text(json.dumps(summary, indent=1, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, indent=1, sort_keys=True))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
