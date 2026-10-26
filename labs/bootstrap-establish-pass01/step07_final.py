"""Pack B #07 / addendum #B-A05: commit the return and the last evidence, push, and verify the return's bytes
from another read (a separate clone fetching from GitHub). Run once.

  python -B step07_final.py <separate clone dir>
"""
import subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import custody as C  # noqa: E402

EV = C.LAB / "evidence" / "step07"
GB = C.LB / "labs" / "bootstrap-git-bytes-pass01" / "gitbytes.py"
RET = "returns/pack-B-establish-return.md"
MODEL = "\n\nModel: claude-opus-5-5\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n"


def gb(cmd, m, repo=C.LB, rev=None):
    r = subprocess.run([sys.executable, "-B", str(GB), cmd, "--repo", str(repo), "--manifest", str(m)] + (["--rev", rev] if rev else []),
                       capture_output=True, text=True)
    print(f"gitbytes {cmd} {Path(m).name}: {r.stdout.strip().splitlines()[-1]}")
    if r.returncode:
        raise C.Refuse(f"gitbytes {cmd} failed")


def main(other):
    if C.git(C.LB, "status", "--porcelain", "--untracked-files=no").stdout.strip():
        raise C.Refuse("tracked files or index not clean")
    m = EV / "manifest-final.tsv"
    paths = sorted(x.decode("utf-8") for x in C.git(C.LB, "ls-files", "--others", "--exclude-standard", "-z").stdout.split(b"\0") if x)
    paths = [p for p in paths if p != m.relative_to(C.LB).as_posix()]
    if RET not in paths:
        raise C.Refuse("the return is not among the new files")
    C.write_tsv(m, ["path", "sha256", "bytes"], [(p, C.sha_file(C.LB / p), (C.LB / p).stat().st_size) for p in paths])
    print(f"final files: {len(paths)} + the manifest")
    gb("attrs", m)
    gb("worktree", m)
    stage = paths + [m.relative_to(C.LB).as_posix()]
    C.git(C.LB, "--literal-pathspecs", "add", "--", *stage)
    staged = {s for s in C.git(C.LB, "diff", "--cached", "--name-only", "-z").stdout.decode().split("\0") if s}
    if staged != set(stage):
        raise C.Refuse("staged set differs")
    gb("index", m)
    msg = C.LB / ".git" / "PACKB_FINAL_MSG"
    msg.write_text("Return for Pack B with addendum 001, and the last publication evidence\n\nPack B #07, addendum #B-A05. "
                   f"{RET} names the evidence commit 07adf6eb21ae1dc66060ebbc960eea904c9eefaf; this commit adds the return "
                   "and the push and fresh-clone records written after it." + MODEL, encoding="utf-8", newline="\n")
    C.git(C.LB, "commit", "-q", "-F", str(msg))
    head = C.git(C.LB, "rev-parse", "HEAD").stdout.decode().strip()
    gb("commit", m, rev=head)
    r = C.git(C.LB, "push", "origin", "refs/heads/workshop:refs/heads/workshop")
    print((r.stdout + r.stderr).decode(errors="replace").strip().splitlines()[-1])
    remote = dict(l.split("\t")[::-1] for l in C.git(C.LB, "ls-remote", "origin").stdout.decode().splitlines())
    if remote.get("refs/heads/workshop") != head:
        raise C.Refuse("remote workshop is not the final commit")
    C.git(Path(other), "fetch", "-q", "origin", "workshop")
    blob = C.git(Path(other), "cat-file", "blob", f"{head}:{RET}").stdout
    local = (C.LB / RET).read_bytes()
    if blob != local:
        raise C.Refuse("the return read back from GitHub differs from the local file")
    print(f"final commit {head} pushed; return read back from GitHub through {Path(other).name}: {len(blob)} bytes, sha256 {C.sha_bytes(blob)}")


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except C.Refuse as e:
        print(f"STOP: {e}")
        sys.exit(2)
