"""Pack B #02 with addendum #B-A01/#B-A03/#B-A04: Git in place, ancestry, tracked policy, baseline commit.

  python -B step02_git.py init       # repo, remote, fetch, verify pinned refs and archive rows, empty-tree commit
  python -B step02_git.py policy     # tracked .gitignore and .gitattributes, committed before any payload
  python -B step02_git.py baseline   # original 39 + additive baseline, attribute/index/commit byte checks

Each step stops on the first problem and writes its log under evidence/step02/. Old checkouts are never
touched. Nothing is staged except explicit literal paths.
"""
import json, os, subprocess, sys, time
from pathlib import Path, PurePosixPath
sys.path.insert(0, str(Path(__file__).resolve().parent))
import custody as C  # noqa: E402

EV = C.LAB / "evidence" / "step02"
GB = C.LB / "labs" / "bootstrap-git-bytes-pass01" / "gitbytes.py"
PY = sys.executable
MODEL = "\n\nModel: claude-opus-5-5\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"
GITIGNORE = (b"/labs/bootstrap-preservation-pass01/clones/\n"
             b"/labs/bootstrap-preservation-pass01/tests-tmp/\n"
             b"/labs/bootstrap-git-bytes-pass01/scratch/\n")
GITATTRIBUTES = (b"* text=auto eol=lf\n/imports/** -text\n/labs/** -text\n/notes/** -text\n/packs/** -text\n"
                 b"/returns/** -text\n/00.kernel/** -text\n")
LOG = []


def log(msg):
    line = time.strftime("%H:%M:%S ") + msg
    print(line)
    LOG.append(line)


def finish(name, code):
    EV.mkdir(parents=True, exist_ok=True)
    (EV / f"{name}.log").write_text("\n".join(LOG) + "\n", encoding="utf-8", newline="\n")
    sys.exit(code)


def g(*a, **k):
    return C.git(C.LB, *a, **k)


def commit(msg_name, text):
    EV.mkdir(parents=True, exist_ok=True)
    m = EV / f"message-{msg_name}.txt"
    m.write_text(text + MODEL, encoding="utf-8", newline="\n")
    g("commit", "-q", "-F", str(m))
    return g("rev-parse", "HEAD").stdout.decode().strip()


def gitbytes(cmd, manifest, rev=None):
    a = [PY, "-B", str(GB), cmd, "--repo", str(C.LB), "--manifest", str(manifest)] + (["--rev", rev] if rev else [])
    r = subprocess.run(a, capture_output=True, text=True)
    log(f"gitbytes {cmd} {Path(manifest).name}: exit {r.returncode}: {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()}")
    if r.returncode:
        (EV / f"gitbytes-{cmd}-{Path(manifest).stem}-FAIL.txt").write_text(r.stdout + r.stderr, encoding="utf-8", newline="\n")
        raise C.Refuse(f"gitbytes {cmd} failed for {manifest}")


def step_init():
    if (C.LB / ".git").exists():
        raise C.Refuse("lib-build already has .git; refusing to re-initialize (resume is not implemented for init)")
    g("init", "-q", "-b", "workshop")
    log("git init -b workshop in place: .git created; working files untouched")
    g("remote", "add", "origin", C.REMOTE)
    g("fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*", "+refs/tags/*:refs/tags/*")
    refs = dict(l.split(" ", 1)[::-1] for l in g("for-each-ref", "--format=%(objectname) %(refname)").stdout.decode().splitlines())
    want = {"refs/remotes/origin/main": C.MAIN, "refs/remotes/origin/rebuild": C.REB,
            "refs/tags/archive/main-14676ca": C.MAIN, "refs/tags/archive/rebuild-de3b8eb": C.REB}
    for arc, (ref, commit_id, n) in C.ARCHIVES.items():
        want[ref.replace("refs/heads/", "refs/remotes/origin/")] = commit_id
    for ref, h in want.items():
        if refs.get(ref) != h:
            raise C.Refuse(f"{ref} is {refs.get(ref)}, pinned {h}")
        log(f"verified {ref} = {h}")
    if "refs/remotes/origin/workshop" in refs:
        raise C.Refuse("origin already has a workshop branch")
    rows = C.tsv(C.PACK / "preservation-manifest.tsv")
    for arc, (ref, commit_id, n) in C.ARCHIVES.items():
        mine = [(r["destination"], r["sha256"], r["bytes"]) for r in rows if r["archive"] == arc]
        if len(mine) != n:
            raise C.Refuse(f"{arc}: {len(mine)} manifest rows, pinned {n}")
        m = EV / f"archive-{arc}.tsv"
        C.write_tsv(m, ["path", "sha256", "bytes"], mine)
        gitbytes("commit", m, commit_id)
    g("update-ref", "refs/heads/workshop", C.MAIN)
    g("read-tree", "--empty")
    staged_deletions = len([l for l in g("status", "--porcelain").stdout.decode().splitlines() if l.startswith("D ")])
    log(f"workshop at {C.MAIN}; index emptied; {staged_deletions} inherited paths now show as staged deletions (expected, no file was written)")
    c = commit("empty-tree", "workshop: start from 14676ca with an empty tree\n\nPack B #02. The inherited tree stays in history, "
               "on rebuild, and under the archive tags; the empty index records that this branch keeps none of it. "
               "No old file was checked out and no working file was deleted.")
    if g("ls-tree", "HEAD").stdout.strip():
        raise C.Refuse("empty-tree commit is not empty")
    if g("rev-parse", "HEAD^").stdout.decode().strip() != C.MAIN:
        raise C.Refuse("empty-tree commit's parent is not the main baseline")
    log(f"empty-tree commit {c}, parent {C.MAIN}")


def step_policy():
    for name, data in ((".gitignore", GITIGNORE), (".gitattributes", GITATTRIBUTES)):
        p = C.LB / name
        if p.exists():
            raise C.Refuse(f"{name} already exists")
        p.write_bytes(data)
    m = EV / "control-files.tsv"
    C.write_tsv(m, ["path", "sha256", "bytes"], [(n, C.sha_bytes(d), len(d)) for n, d in ((".gitignore", GITIGNORE), (".gitattributes", GITATTRIBUTES))])
    g("add", "--", ".gitignore", ".gitattributes")
    gitbytes("index", m)
    c = commit("policy", "Track the byte-custody policy and scratch exclusions before any payload\n\nAddendum 001 #B-A03/#B-A04. "
               ".gitattributes keeps /imports /labs /notes /packs /returns /00.kernel byte-exact (-text); new app "
               "and control text stays LF. .gitignore excludes only the generated scratch repositories. Inserted after "
               "the empty-tree commit and before the baseline, as the addendum requires.")
    gitbytes("commit", m, c)
    log(f"policy commit {c}")


def step_baseline():
    if g("status", "--porcelain", "--untracked-files=no").stdout.strip():
        raise C.Refuse("index or tracked files are not clean before the baseline")
    sys.argv = ["step01", "--out", str(EV / "baseline-capture")]
    r = subprocess.run([PY, "-B", str(C.LAB / "step01_baseline.py"), "--after-init", "--out", str(EV / "baseline-capture")], capture_output=True, text=True)
    if r.returncode:
        raise C.Refuse("baseline capture reported problems:\n" + r.stdout)
    inv = C.tsv(EV / "baseline-capture" / "additive-baseline-2026-10-26.tsv")
    stage = [x for x in inv if not x["disposition"].startswith(("excluded", "control", "deferred"))]
    excl = [x for x in inv if x["disposition"].startswith("excluded")]
    ignored = set(g("check-ignore", "--no-index", "--stdin", input=("\n".join(x["path"] for x in excl) + "\n").encode()).stdout.decode().split("\n")) - {""}
    if ignored != {x["path"] for x in excl}:
        raise C.Refuse(f"excluded files not all ignored: {sorted({x['path'] for x in excl} - ignored)[:5]}")
    leak = set(g("check-ignore", "--no-index", "--stdin", input=("\n".join(x["path"] for x in stage) + "\n").encode(), check=False).stdout.decode().split("\n")) - {""}
    if leak:
        raise C.Refuse(f"files meant for staging are ignored: {sorted(leak)[:5]}")
    m = EV / "baseline-stage.tsv"
    C.write_tsv(m, ["path", "sha256", "bytes"], [(x["path"], x["sha256"], x["bytes"]) for x in stage])
    gitbytes("attrs", m)
    gitbytes("worktree", m)
    pf = EV / "baseline-paths.nul"
    pf.write_bytes(b"\0".join(x["path"].encode("utf-8") for x in stage) + b"\0")
    g("--literal-pathspecs", "add", f"--pathspec-from-file={pf}", "--pathspec-file-nul")
    staged = g("diff", "--cached", "--name-only", "-z").stdout.decode().split("\0")
    staged = {s for s in staged if s}
    if staged != {x["path"] for x in stage}:
        raise C.Refuse(f"staged set differs from the declared baseline: extra {sorted(staged - {x['path'] for x in stage})[:5]}, "
                       f"missing {sorted({x['path'] for x in stage} - staged)[:5]}")
    gitbytes("index", m)
    if b"160000" in g("ls-files", "--stage").stdout:
        raise C.Refuse("a gitlink (mode 160000) is staged")
    counts = {}
    for x in stage:
        counts[x["disposition"]] = counts.get(x["disposition"], 0) + 1
    c = commit("baseline", f"Commit the lib-build baseline as found: {len(stage)} files\n\nPack B #02, addendum #B-A04. "
               f"Original 39-file baseline plus the additive baseline captured before this commit ({counts}). "
               f"{len(excl)} generated scratch files under the three ignored folders are excluded and identified in "
               "evidence/step02/baseline-capture (nested repositories by HEAD and remote). Every path was checked for "
               "-text attributes and verified at worktree, index and commit.")
    gitbytes("commit", m, c)
    log(f"baseline commit {c}: {len(stage)} files {counts}; excluded {len(excl)}")


def main():
    step = sys.argv[1]
    try:
        {"init": step_init, "policy": step_policy, "baseline": step_baseline}[step]()
    except C.Refuse as e:
        log(f"STOP: {e}")
        finish(step, 2)
    finish(step, 0)


if __name__ == "__main__":
    main()
