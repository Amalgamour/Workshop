"""Pack B #07 with addendum #B-A03/#B-A05: the evidence commit, fresh-clone verification, publication.

  python -B step07_publish.py evidence            # manifest of every new file, checks, commit
  python -B step07_publish.py clone <dir> <source>  # independent clone (autocrlf=true before checkout); verify all custody
  python -B step07_publish.py push                # push workshop only, no force; verify the remote ref

The evidence manifest lists every file the evidence commit adds, except itself (its own bytes are
recorded in evidence/step07/manifest-self.tsv, which is not listed anywhere). Byte-exact paths (under
the -text roots) are checked for attributes, worktree, index and commit; root and app text is LF and is
checked at worktree, index and commit for exact bytes.
"""
import os, subprocess, sys
from pathlib import Path, PurePosixPath
sys.path.insert(0, str(Path(__file__).resolve().parent))
import custody as C  # noqa: E402

EV = C.LAB / "evidence" / "step07"
GB = C.LB / "labs" / "bootstrap-git-bytes-pass01" / "gitbytes.py"
PY = sys.executable
CUSTODY_ROOTS = ("imports/", "labs/", "notes/", "packs/", "returns/", "00.kernel/")
MODEL = "\n\nModel: claude-opus-5-5\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"


def gitbytes(cmd, manifest, repo=C.LB, rev=None):
    r = subprocess.run([PY, "-B", str(GB), cmd, "--repo", str(repo), "--manifest", str(manifest)] + (["--rev", rev] if rev else []),
                       capture_output=True, text=True)
    line = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()
    print(f"gitbytes {cmd} {Path(manifest).name} @ {Path(repo).name}: {line}")
    if r.returncode:
        (EV / f"gitbytes-{cmd}-{Path(manifest).stem}-{Path(repo).name}-FAIL.txt").write_text(r.stdout + r.stderr, encoding="utf-8", newline="\n")
        raise C.Refuse(f"gitbytes {cmd} failed")


def untracked():
    out = C.git(C.LB, "ls-files", "--others", "--exclude-standard", "-z").stdout.split(b"\0")
    return sorted(x.decode("utf-8") for x in out if x)


def evidence():
    EV.mkdir(parents=True, exist_ok=True)
    if C.git(C.LB, "status", "--porcelain", "--untracked-files=no").stdout.strip():
        raise C.Refuse("tracked files or index not clean")
    me = EV / "manifest-new-files.tsv"
    paths = [p for p in untracked() if p != me.relative_to(C.LB).as_posix()]
    if any("__pycache__" in p for p in paths):
        raise C.Refuse("a __pycache__ file would be staged")
    rows = [(p, C.sha_file(C.LB / p), (C.LB / p).stat().st_size) for p in paths]
    C.write_tsv(me, ["path", "sha256", "bytes"], rows)
    C.write_tsv(EV / "manifest-self.tsv", ["path", "sha256", "bytes"], [(me.relative_to(C.LB).as_posix(), C.sha_file(me), me.stat().st_size)])
    exact = [r for r in rows if r[0].startswith(CUSTODY_ROOTS)]
    lf = [r for r in rows if not r[0].startswith(CUSTODY_ROOTS)]
    C.write_tsv(EV / "manifest-new-exact.tsv", ["path", "sha256", "bytes"], exact)
    C.write_tsv(EV / "manifest-new-lf.tsv", ["path", "sha256", "bytes"], lf)
    for p, _, _ in lf:
        if b"\r" in (C.LB / p).read_bytes():
            raise C.Refuse(f"LF-policy file holds CR: {p}")
    print(f"new files: {len(rows)} ({len(exact)} byte-exact, {len(lf)} LF text: {[r[0] for r in lf]})")
    gitbytes("attrs", EV / "manifest-new-exact.tsv")
    for m in ("manifest-new-exact.tsv", "manifest-new-lf.tsv"):
        gitbytes("worktree", EV / m)
    stage = paths + [me.relative_to(C.LB).as_posix(), (EV / "manifest-self.tsv").relative_to(C.LB).as_posix(),
                     (EV / "manifest-new-exact.tsv").relative_to(C.LB).as_posix(), (EV / "manifest-new-lf.tsv").relative_to(C.LB).as_posix()]
    stage = sorted(set(stage))
    pf = EV / "stage-paths.nul"
    pf.write_bytes(b"\0".join(s.encode("utf-8") for s in stage) + b"\0")
    stage.append(pf.relative_to(C.LB).as_posix())
    pf.write_bytes(b"\0".join(s.encode("utf-8") for s in stage) + b"\0")
    C.git(C.LB, "--literal-pathspecs", "add", f"--pathspec-from-file={pf}", "--pathspec-file-nul")
    staged = {s for s in C.git(C.LB, "diff", "--cached", "--name-only", "-z").stdout.decode().split("\0") if s}
    if staged != set(stage):
        raise C.Refuse(f"staged set differs: extra {sorted(staged - set(stage))[:3]} missing {sorted(set(stage) - staged)[:3]}")
    for m in ("manifest-new-exact.tsv", "manifest-new-lf.tsv", "manifest-self.tsv"):
        gitbytes("index", EV / m)
    if b"160000" in C.git(C.LB, "ls-files", "--stage").stdout:
        raise C.Refuse("a gitlink is staged")
    msg = EV / "message-evidence.txt"
    msg.write_text(f"Establish the desk: drafts, work records and Pack B evidence ({len(stage)} files)\n\n"
                   "Pack B #04-#06 and addendum #B-A05. Desk furniture, book orientation candidates, the work book's "
                   "pages, law drafts (0041, 0062-0065, amendments to 0018, 0050, 0057), the runtime door and inactive "
                   "cards, README.md, AGENTS.004.md (draft), app/README.md, the derived 00.live.md, and the Pack B and "
                   "addendum labs with their tools, tests and evidence. Nothing is approved, seated or active. "
                   "Byte-exact paths verified at attributes, worktree, index and commit." + MODEL, encoding="utf-8", newline="\n")
    C.git(C.LB, "commit", "-q", "-F", str(msg))
    head = C.git(C.LB, "rev-parse", "HEAD").stdout.decode().strip()
    for m in ("manifest-new-exact.tsv", "manifest-new-lf.tsv", "manifest-self.tsv"):
        gitbytes("commit", EV / m, rev=head)
    print(f"evidence commit {head}")


def clone(target, source):
    target = Path(target)
    if target.exists() and any(target.iterdir()):
        raise C.Refuse(f"clone destination is not empty: {target}")
    r = subprocess.run(["git", "clone", "-q", "--no-local", "--no-hardlinks", "--no-checkout", "--branch", "workshop", source, str(target)],
                       capture_output=True, text=True)
    if r.returncode:
        raise C.Refuse("clone failed: " + r.stderr)
    if (target / ".git" / "objects" / "info" / "alternates").exists():
        raise C.Refuse("clone borrows objects")
    C.git(target, "config", "core.autocrlf", "true")
    C.git(target, "checkout", "-q", "workshop")
    head = C.git(target, "rev-parse", "HEAD").stdout.decode().strip()
    print(f"clone {target} at {head}, core.autocrlf=true set before checkout")
    sets = {
        "original-baseline": C.LB / "00.kernel/00.00.10.work/0410.imports/manifests/pack-workspace-baseline.tsv",
        "imports": C.LB / "00.kernel/00.00.10.work/0410.imports/manifests/step03-custody-imports.tsv",
        "baseline-stage": C.LAB / "evidence/step02/baseline-stage.tsv",
        "control": C.LAB / "evidence/step02/control-files.tsv",
        "new-exact": EV / "manifest-new-exact.tsv",
        "new-lf": EV / "manifest-new-lf.tsv",
        "self": EV / "manifest-self.tsv",
    }
    for name, m in sets.items():
        if name not in ("new-lf", "control"):
            gitbytes("attrs", m, repo=target)
        gitbytes("worktree", m, repo=target)
        gitbytes("commit", m, repo=target, rev="HEAD")
    rr = subprocess.run([PY, "-B", str(target / "labs/bootstrap-establish-pass01/render_live.py"), "check", "--root", str(target)], capture_output=True, text=True)
    print(f"render check in the clone: exit {rr.returncode}: {rr.stdout.strip()}")
    if rr.returncode:
        raise C.Refuse("render check failed in the clone")
    if b"160000" in C.git(target, "ls-files", "--stage").stdout:
        raise C.Refuse("the clone tracks a gitlink")
    print("clone verification: PASS")


def push():
    remote = dict(l.split("\t")[::-1] for l in C.git(C.LB, "ls-remote", "origin").stdout.decode().splitlines())
    if "refs/heads/workshop" in remote:
        raise C.Refuse(f"origin already has workshop at {remote['refs/heads/workshop']}; not pushing over it")
    head = C.git(C.LB, "rev-parse", "HEAD").stdout.decode().strip()
    r = C.git(C.LB, "push", "origin", "refs/heads/workshop:refs/heads/workshop")
    print((r.stdout + r.stderr).decode(errors="replace").strip())
    after = dict(l.split("\t")[::-1] for l in C.git(C.LB, "ls-remote", "origin").stdout.decode().splitlines())
    if after.get("refs/heads/workshop") != head:
        raise C.Refuse("remote workshop does not equal the local head")
    for ref in ("refs/heads/main", "refs/heads/rebuild"):
        if after.get(ref) != remote.get(ref):
            raise C.Refuse(f"{ref} moved")
    print(f"pushed workshop {head}; main and rebuild unchanged")


if __name__ == "__main__":
    try:
        cmd = sys.argv[1]
        if cmd == "evidence":
            evidence()
        elif cmd == "clone":
            clone(sys.argv[2], sys.argv[3])
        elif cmd == "push":
            push()
    except C.Refuse as e:
        print(f"STOP: {e}")
        sys.exit(2)
