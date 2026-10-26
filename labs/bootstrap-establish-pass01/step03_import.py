"""Pack B #03: build the import manifests, check every destination together, import, verify, commit.

  python -B step03_import.py build      # manifests only (evidence/step03/*.tsv); reads git objects
  python -B step03_import.py run        # import_blobs.py per manifest, then attrs/worktree/index/commit checks

Manifests: snapshots (890 rows to imports/source-tree/), selected (81 copies into the books, each tied
to its snapshot row and checked for identical bytes), p1 (22 Director decision files from the accepted
archive commit, original relative paths under imports/director-decisions/), claude (Claude's pass 02
import manifest and collisions, from the accepted bootstrap archive).
"""
import subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import custody as C  # noqa: E402

EV = C.LAB / "evidence" / "step03"
GB = C.LB / "labs" / "bootstrap-git-bytes-pass01" / "gitbytes.py"
HEAD = ["row", "source", "git_blob", "sha256", "bytes", "destination"]
MODEL = "\n\nModel: claude-opus-5-5\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"


def blob_at(spec):
    return C.git(C.LB, "rev-parse", "--verify", spec).stdout.decode().strip()


def build():
    EV.mkdir(parents=True, exist_ok=True)
    snap = C.tsv(C.PACK / "snapshot-import-manifest.tsv")
    if len(snap) != 890:
        raise C.Refuse(f"snapshot manifest has {len(snap)} rows, pinned 890")
    s_rows = [(r["row"], r["source"], r["git_blob"], r["sha256"], r["bytes"], r["destination"]) for r in snap]
    by_row = {r["row"]: r for r in snap}
    sel = C.tsv(C.PACK / "selected-reference-manifest.tsv")
    sel_rows, register = [], []
    for r in sel:
        s = by_row.get(r["source_row"])
        if s is None or s["sha256"] != r["sha256"]:
            raise C.Refuse(f"selected row {r['source_row']} does not match its snapshot row")
        sel_rows.append((r["source_row"], s["source"], s["git_blob"], s["sha256"], s["bytes"], r["destination"]))
        register.append((r["destination"], r["source_row"], s["destination"], s["source"], r["sha256"], r["status"]))
    commit_main = C.ARCHIVES["main-worktree"][1]
    p1 = [r for r in C.tsv(C.PACK / "preservation-manifest.tsv") if r["group"] == "P1"]
    if len(p1) != 22:
        raise C.Refuse(f"{len(p1)} P1 rows, pinned 22")
    p1_rows = [(f"P1-{i + 1:02d}", f"{commit_main}:{r['destination']}", blob_at(f"{commit_main}:{r['destination']}"), r["sha256"], r["bytes"],
                f"imports/director-decisions/{r['destination']}") for i, r in enumerate(p1)]
    commit_boot = C.ARCHIVES["bootstrap"][1]
    claude = []
    for n in ("import-manifest.tsv", "collisions.tsv"):
        spec = f"{commit_boot}:sources/claude-pass02/{n}"
        data = C.git(C.LB, "cat-file", "blob", spec).stdout
        claude.append((f"C-{n}", spec, blob_at(spec), C.sha_bytes(data), len(data), f"imports/claude-pass02/{n}"))
    for name, rows in (("snapshots", s_rows), ("selected", sel_rows), ("p1", p1_rows), ("claude", claude)):
        C.write_tsv(EV / f"import-{name}.tsv", HEAD, rows)
    C.write_tsv(EV / "selection-register.tsv", ["book_path", "snapshot_row", "snapshot_path", "source", "sha256", "status"], register)
    C.check_destinations(C.LB, [r[5] for rows in (s_rows, sel_rows, p1_rows, claude) for r in rows])
    print(f"manifests: snapshots {len(s_rows)}, selected {len(sel_rows)}, p1 {len(p1_rows)}, claude {len(claude)}; "
          f"all {len(s_rows) + len(sel_rows) + len(p1_rows) + len(claude)} destinations checked together")


def gitbytes(cmd, manifest, rev=None):
    a = [sys.executable, "-B", str(GB), cmd, "--repo", str(C.LB), "--manifest", str(manifest)] + (["--rev", rev] if rev else [])
    r = subprocess.run(a, capture_output=True, text=True)
    line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()
    print(f"gitbytes {cmd} {Path(manifest).name}: exit {r.returncode}: {line}")
    if r.returncode:
        (EV / f"gitbytes-{cmd}-{Path(manifest).stem}-FAIL.txt").write_text(r.stdout + r.stderr, encoding="utf-8", newline="\n")
        raise C.Refuse(f"gitbytes {cmd} failed: {manifest}")


def run():
    if C.git(C.LB, "status", "--porcelain", "--untracked-files=no").stdout.strip():
        raise C.Refuse("tracked files or index not clean before import")
    names = ("snapshots", "selected", "p1", "claude")
    for n in names:
        r = subprocess.run([sys.executable, "-B", str(C.LAB / "import_blobs.py"), "--repo", str(C.LB), "--manifest", str(EV / f"import-{n}.tsv"),
                            "--journal", str(EV / f"journal-{n}.json")], capture_output=True, text=True)
        print(f"import {n}: exit {r.returncode}: {r.stdout.strip()}")
        if r.returncode:
            raise C.Refuse(f"import {n} stopped")
    custody = EV / "custody-imports.tsv"
    rows = {}
    for n in names:
        for r in C.tsv(EV / f"import-{n}.tsv"):
            if r["destination"] in rows:
                raise C.Refuse(f"two manifests write {r['destination']}")
            rows[r["destination"]] = (r["destination"], r["sha256"], r["bytes"])
    C.write_tsv(custody, ["path", "sha256", "bytes"], list(rows.values()))
    gitbytes("attrs", custody)
    gitbytes("worktree", custody)
    pf = EV / "import-paths.nul"
    pf.write_bytes(b"\0".join(p.encode("utf-8") for p in rows) + b"\0")
    C.git(C.LB, "--literal-pathspecs", "add", f"--pathspec-from-file={pf}", "--pathspec-file-nul")
    staged = {s for s in C.git(C.LB, "diff", "--cached", "--name-only", "-z").stdout.decode().split("\0") if s}
    if staged != set(rows):
        raise C.Refuse(f"staged set differs: extra {sorted(staged - set(rows))[:3]} missing {sorted(set(rows) - staged)[:3]}")
    gitbytes("index", custody)
    msg = EV / "message-imports.txt"
    msg.write_text("Import snapshots, selected book copies, P1 decisions and Claude's manifests from pinned Git objects\n\n"
                   f"Pack B #03. {len(rows)} files: 890 snapshots under imports/source-tree/ (reference only), 81 selected "
                   "copies into the books (73 imported reference faces, 8 inactive runtime candidates), 22 Director "
                   "decision files from archive e8b1a99 under imports/director-decisions/, and Claude's pass 02 manifest "
                   "and collisions from archive fe42b01. Every row was checked against its pinned rev:path blob, length "
                   "and SHA-256 before any write, and at worktree, index and commit. No old stamp confers local approval."
                   + MODEL, encoding="utf-8", newline="\n")
    C.git(C.LB, "commit", "-q", "-F", str(msg))
    head = C.git(C.LB, "rev-parse", "HEAD").stdout.decode().strip()
    gitbytes("commit", custody, head)
    print(f"import commit {head}: {len(rows)} files")


def resume_index():
    """Continue run() after its staging step: re-check the staged set and journals, then index, commit, commit check."""
    rows = {r["path"]: r for r in C.tsv(EV / "custody-imports.tsv")}
    staged = {x for x in C.git(C.LB, "diff", "--cached", "--name-only", "-z").stdout.decode().split("\0") if x}
    if staged != set(rows):
        raise C.Refuse("staged set differs from custody-imports.tsv")
    for n in ("snapshots", "selected", "p1", "claude"):
        if '"state": "complete"' not in (EV / f"journal-{n}.json").read_text(encoding="utf-8"):
            raise C.Refuse(f"journal {n} is not complete")
    gitbytes("index", EV / "custody-imports.tsv")
    msg = EV / "message-imports.txt"
    msg.write_text("Import snapshots, selected book copies, P1 decisions and Claude's manifests from pinned Git objects\n\n"
                   f"Pack B #03. {len(rows)} files: 890 snapshots under imports/source-tree/ (reference only), 81 selected "
                   "copies into the books (73 imported reference faces, 8 inactive runtime candidates), 22 Director "
                   "decision files from archive e8b1a99 under imports/director-decisions/, and Claude's pass 02 manifest "
                   "and collisions from archive fe42b01. Every row was checked against its pinned rev:path blob, length "
                   "and SHA-256 before any write, and at worktree, index and commit. No old stamp confers local approval."
                   + MODEL, encoding="utf-8", newline="\n")
    C.git(C.LB, "commit", "-q", "-F", str(msg))
    head = C.git(C.LB, "rev-parse", "HEAD").stdout.decode().strip()
    gitbytes("commit", EV / "custody-imports.tsv", head)
    print(f"import commit {head}: {len(rows)} files")


if __name__ == "__main__":
    try:
        {"build": build, "run": run, "resume-index": resume_index}[sys.argv[1]]()
    except C.Refuse as e:
        print(f"STOP: {e}")
        sys.exit(2)
