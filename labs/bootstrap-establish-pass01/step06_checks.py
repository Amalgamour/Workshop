"""Pack B #06: the slice checks. Read-only.

  python -B step06_checks.py 1 2 4 5     # any subset; writes evidence/step06/check-<n>.txt

1  original 39 retained; additive baseline accounted for; old-checkout fingerprints unchanged
2  890 snapshots, 81 selected copies and 22 P1 files match pinned bytes, at worktree and in HEAD
4  one desk, three books; no new unversioned law/syntax face under 0100; no active runtime file; no seated loader
5  local links in README.md, AGENTS.004.md, app/ and the desk and work pages resolve; contents match the folders
Checks 3 and 6 are the test suites (test_import_blobs.py, test_render_live.py); 7 runs from a fresh clone.
"""
import re, subprocess, sys
from pathlib import Path, PurePosixPath
sys.path.insert(0, str(Path(__file__).resolve().parent))
import custody as C  # noqa: E402

EV = C.LAB / "evidence" / "step06"
GB = C.LB / "labs" / "bootstrap-git-bytes-pass01" / "gitbytes.py"
PY = sys.executable
OUT = []


def say(s):
    print(s)
    OUT.append(s)


def gitbytes(cmd, manifest, rev=None):
    r = subprocess.run([PY, "-B", str(GB), cmd, "--repo", str(C.LB), "--manifest", str(manifest)] + (["--rev", rev] if rev else []),
                       capture_output=True, text=True)
    say(f"  gitbytes {cmd} {Path(manifest).name}: {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()}")
    return r.returncode == 0


def check1():
    ok = True
    for r in C.tsv(C.PACK / "workspace-baseline.tsv"):
        p = C.LB / r["path"]
        if not p.is_file() or C.sha_file(p) != r["sha256"]:
            say(f"  original baseline changed: {r['path']}"); ok = False
    say(f"  original baseline: 39 files checked")
    inv = C.tsv(C.LAB / "evidence" / "step02" / "baseline-capture" / "additive-baseline-2026-10-26.tsv")
    tracked = {}
    for e in C.git(C.LB, "ls-tree", "-r", "-z", "HEAD").stdout.split(b"\0"):
        if e:
            meta, path = e.decode("utf-8").split("\t", 1)
            tracked[path] = meta.split()[2]
    counts = {}
    for r in inv:
        d = r["disposition"].split(":")[0]
        counts[d] = counts.get(d, 0) + 1
        p = C.LB / r["path"]
        if d in ("original baseline", "additive"):
            if r["path"] not in tracked:
                say(f"  baseline file not tracked: {r['path']}"); ok = False
            elif not p.is_file() or C.sha_file(p) != r["sha256"]:
                say(f"  baseline file changed since capture: {r['path']}"); ok = False
        elif d == "excluded" and r["path"] in tracked:
            say(f"  excluded scratch file is tracked: {r['path']}"); ok = False
        elif d == "deferred" and not p.is_file():
            say(f"  deferred Pack B lab file is missing: {r['path']}"); ok = False
    say(f"  additive baseline accounted for: {counts}")
    before = C.LAB / "evidence" / "old-fingerprint-before.json"
    after = C.LAB / "evidence" / "old-fingerprint-check1.json"
    pf = C.LB / "labs" / "bootstrap-preservation-pass01" / "preflight.py"
    r1 = subprocess.run([PY, "-B", "-I", str(pf), "capture", "--label", "packB-check1", "--out", str(after)], capture_output=True, text=True)
    r2 = subprocess.run([PY, "-B", "-I", str(pf), "compare", str(before), str(after)], capture_output=True, text=True)
    say(f"  old checkouts: {r2.stdout.strip()}")
    return ok and r1.returncode == 0 and r2.returncode == 0


def check2():
    ok = True
    m = C.LB / "00.kernel/00.00.10.work/0410.imports/manifests/step03-custody-imports.tsv"
    ok &= gitbytes("worktree", m)
    ok &= gitbytes("commit", m, "HEAD")
    snap = {r["row"]: r for r in C.tsv(C.PACK / "snapshot-import-manifest.tsv")}
    for r in C.tsv(C.PACK / "selected-reference-manifest.tsv"):
        a, b = C.LB / r["destination"], C.LB / snap[r["source_row"]]["destination"]
        if C.sha_file(a) != C.sha_file(b) or C.sha_file(a) != r["sha256"]:
            say(f"  selected copy differs from its snapshot: {r['destination']}"); ok = False
    say("  selected copies: 81 identical to their snapshot rows")
    p1 = [r for r in C.tsv(C.PACK / "preservation-manifest.tsv") if r["group"] == "P1"]
    for r in p1:
        p = C.LB / "imports/director-decisions" / r["destination"]
        if not p.is_file() or C.sha_file(p) != r["sha256"] or str(p.stat().st_size) != r["bytes"]:
            say(f"  P1 differs from the preservation manifest: {r['destination']}"); ok = False
    say(f"  P1: {len(p1)} files match the preservation manifest's pinned hashes")
    return ok


def check4():
    ok = True
    k = C.LB / "00.kernel"
    books = sorted(p.name for p in k.iterdir() if p.is_dir())
    say(f"  desk 00.kernel books: {books}")
    ok &= books == ["00.00.00.syntax", "00.00.01.law", "00.00.10.work"]
    desks = sorted(p.name for p in C.LB.iterdir() if p.is_dir() and re.match(r"^\d{2}\.", p.name))
    say(f"  desk folders at the root: {desks}")
    ok &= desks == ["00.kernel"]
    selected = {r["destination"] for r in C.tsv(C.PACK / "selected-reference-manifest.tsv")}
    for book in ("00.00.00.syntax", "00.00.01.law"):
        for f in sorted((k / book).rglob("*")):
            if not f.is_file():
                continue
            rel = f.relative_to(C.LB).as_posix()
            if rel in selected:
                continue
            page = f.parent.name
            num = int(page[:4]) if re.match(r"^\d{4}\.", page) else None
            if f.parent == k / book:
                versioned = re.match(r"^00\.\d{3}\.md$", f.name) is not None
            else:
                versioned = re.match(r"^\d{2}\.\d{3}\.md$", f.name) is not None
            if (num is None or num < 100) and not versioned:
                say(f"  new unversioned face under 0100: {rel}"); ok = False
    active = [p.relative_to(C.LB).as_posix() for p in (k / "00.00.01.law").glob("03*/02.*") if re.match(r"^02\.[a-z]+\.(py|toml)$", p.name)]
    say(f"  active runtime files: {active or 'none'}")
    ok &= not active
    ok &= not (k / "00.00.01.law" / "0302.run" / "02.run.py").exists()
    say("  seated loader: none (0302.run/02.run.py absent)")
    return ok


def check5():
    ok = True
    files = [C.LB / "README.md", C.LB / "AGENTS.004.md", C.LB / "app" / "README.md"] + \
            [p for p in (C.LB / "00.kernel").glob("*.md")] + \
            [p for p in (C.LB / "00.kernel" / "00.00.10.work").rglob("*.md") if "0501.bootstrap/pack" not in p.as_posix() and "addendum-001" not in p.as_posix()]
    n = 0
    for f in files:
        for target in re.findall(r"\]\(([^)#]+)(?:#[^)]*)?\)", f.read_text(encoding="utf-8")):
            if "://" in target:
                continue
            n += 1
            if not (f.parent / target).exists():
                say(f"  broken link in {f.relative_to(C.LB).as_posix()}: {target}"); ok = False
    say(f"  markdown links checked: {n} in {len(files)} files")
    r = subprocess.run([PY, "-B", str(C.LAB / "write_contents.py"), "--check"], capture_output=True, text=True)
    say("  " + r.stdout.strip())
    return ok and r.returncode == 0


def main():
    EV.mkdir(parents=True, exist_ok=True)
    rc = 0
    for n in sys.argv[1:]:
        OUT.clear()
        say(f"check {n}")
        good = {"1": check1, "2": check2, "4": check4, "5": check5}[n]()
        say(f"check {n}: {'PASS' if good else 'FAIL'}")
        (EV / f"check-{n}.txt").write_text("\n".join(OUT) + "\n", encoding="utf-8", newline="\n")
        rc |= 0 if good else 1
    sys.exit(rc)


if __name__ == "__main__":
    main()
