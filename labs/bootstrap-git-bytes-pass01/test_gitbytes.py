"""Addendum 001 #B-A02 fixture gate. Every repository is new, under scratch/; only those repositories get
core.autocrlf=true. Global and system Git configuration are never changed.

  python -B test_gitbytes.py -v
"""
import csv, hashlib, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "gitbytes.py"
SCRATCH = HERE / "scratch"
ENV = dict(os.environ, GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@local", GIT_COMMITTER_NAME="fixture",
           GIT_COMMITTER_EMAIL="fixture@local")
POLICY = (b"* text=auto eol=lf\n/imports/** -text\n/labs/** -text\n/notes/** -text\n/packs/** -text\n"
          b"/returns/** -text\n/00.kernel/** -text\n")
CRLF = "Première ligne\r\nsecond line\r\n".encode("utf-8")
LF = "line one\nligne deux é\n".encode("utf-8")
BIN = bytes(range(256)) + b"\x00\x00\r\n\x00"
APP = b"def f():\n    return 1\n"
FIXTURES = {"labs/fx/crlf.md": CRLF, "00.kernel/fx/lf.md": LF, "imports/fx/data.bin": BIN, "returns/fx/r.txt": CRLF}


def git(repo, *a, check=True):
    return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, env=ENV, check=check)


def sha(b):
    return hashlib.sha256(b).hexdigest()


CALLS = HERE / "evidence" / "gate-calls"
_n = [0]


def tool(*a):
    r = subprocess.run([sys.executable, "-B", str(TOOL), *a], capture_output=True, text=True)
    CALLS.mkdir(parents=True, exist_ok=True)
    _n[0] += 1
    test = os.environ.get("GATE_TEST", "x")
    shown = [x if not x.startswith(str(SCRATCH)) else "<scratch>" + x[len(str(SCRATCH)):] for x in a]
    (CALLS / f"{test}-{_n[0]:02d}-{a[0]}.txt").write_text(
        f"$ gitbytes.py {' '.join(shown)}\nexit {r.returncode}\n{r.stdout}{r.stderr}", encoding="utf-8", newline="\n")
    return r


class Gate(unittest.TestCase):
    def setUp(self):
        os.environ["GATE_TEST"] = self._testMethodName
        _n[0] = 0
        SCRATCH.mkdir(exist_ok=True)
        self.base = Path(tempfile.mkdtemp(prefix=self._testMethodName[:22] + "-", dir=SCRATCH))
        self.repo = self.base / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q", "-b", "main")
        git(self.repo, "config", "core.autocrlf", "true")   # this test repository only

    def write(self, rel, data, root=None):
        p = (root or self.repo) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)

    def manifest(self, files, name="m.tsv"):
        m = self.base / name
        with open(m, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(["path", "sha256", "bytes"])
            for rel, data in files.items():
                w.writerow([rel, sha(data), len(data)])
        return m

    def custody_repo(self):
        self.write(".gitattributes", POLICY)
        git(self.repo, "add", "--", ".gitattributes")
        git(self.repo, "commit", "-q", "-m", "policy")
        for rel, data in FIXTURES.items():
            self.write(rel, data)
        self.write("app/code.py", APP)
        git(self.repo, "add", "--", *FIXTURES, "app/code.py")

    # 1. the original failure, caught at the index before any commit
    def test_1_normalization_caught_at_index(self):
        self.write(".gitattributes", b"* text=auto eol=lf\n")
        self.write("labs/fx/crlf.md", CRLF)
        git(self.repo, "add", "--", ".gitattributes", "labs/fx/crlf.md")
        m = self.manifest({"labs/fx/crlf.md": CRLF})
        self.assertEqual(tool("worktree", "--repo", str(self.repo), "--manifest", str(m)).returncode, 0)
        r = tool("index", "--repo", str(self.repo), "--manifest", str(m))
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("index: differs labs/fx/crlf.md", r.stdout)
        a = tool("attrs", "--repo", str(self.repo), "--manifest", str(m))
        self.assertEqual(a.returncode, 2)
        self.assertIn("text is auto", a.stdout)
        self.assertEqual(git(self.repo, "rev-parse", "--verify", "HEAD", check=False).returncode, 128)  # nothing committed

    # 2. tracked -text custody keeps CRLF, LF and binary exact; app code outside custody stays LF
    def test_2_tracked_custody_exact_everywhere(self):
        self.custody_repo()
        m = self.manifest(FIXTURES)
        for cmd in ("attrs", "worktree", "index"):
            r = tool(cmd, "--repo", str(self.repo), "--manifest", str(m))
            self.assertEqual(r.returncode, 0, cmd + ": " + r.stdout)
        git(self.repo, "commit", "-q", "-m", "fixtures")
        r = tool("commit", "--repo", str(self.repo), "--manifest", str(m), "--rev", "HEAD")
        self.assertEqual(r.returncode, 0, r.stdout)
        eff = git(self.repo, "check-attr", "text", "eol", "--", *FIXTURES, "app/code.py").stdout.decode()
        (self.base / "effective-attributes.txt").write_text(eff, encoding="utf-8", newline="\n")
        self.assertIn("app/code.py: text: auto", eff)
        self.assertEqual(git(self.repo, "cat-file", "blob", "HEAD:app/code.py").stdout, APP)

    # 3. wrong bytes staged while the worktree holds the expected bytes: the index check refuses
    def test_3_wrong_index_with_correct_worktree(self):
        self.custody_repo()
        self.write("labs/fx/crlf.md", b"wrong bytes\r\n")
        git(self.repo, "add", "--", "labs/fx/crlf.md")
        self.write("labs/fx/crlf.md", CRLF)                       # worktree is right again, index is not
        m = self.manifest(FIXTURES)
        self.assertEqual(tool("worktree", "--repo", str(self.repo), "--manifest", str(m)).returncode, 0)
        r = tool("index", "--repo", str(self.repo), "--manifest", str(m))
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("index: differs labs/fx/crlf.md", r.stdout)

    # 4. a committed blob that does not match the manifest fails the commit check
    def test_4_mismatching_commit(self):
        self.custody_repo()
        git(self.repo, "commit", "-q", "-m", "fixtures")
        wrong = dict(FIXTURES)
        wrong["imports/fx/data.bin"] = BIN + b"!"
        r = tool("commit", "--repo", str(self.repo), "--manifest", str(self.manifest(wrong, "wrong.tsv")), "--rev", "HEAD")
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("differs imports/fx/data.bin", r.stdout)
        r2 = tool("commit", "--repo", str(self.repo), "--manifest", str(self.manifest({"labs/fx/absent.md": LF}, "absent.tsv")), "--rev", "HEAD")
        self.assertEqual(r2.returncode, 2)
        self.assertIn("missing labs/fx/absent.md", r2.stdout)

    # 5. an independent clone with core.autocrlf=true set before checkout keeps every byte
    def test_5_fresh_clone_autocrlf(self):
        self.custody_repo()
        git(self.repo, "commit", "-q", "-m", "fixtures")
        clone = self.base / "clone"
        r = subprocess.run(["git", "clone", "-q", "--no-local", "--no-hardlinks", "--no-checkout", str(self.repo), str(clone)],
                           capture_output=True, env=ENV)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse((clone / ".git" / "objects" / "info" / "alternates").exists())
        git(clone, "config", "core.autocrlf", "true")
        git(clone, "checkout", "-q", "main")
        info = clone / ".git" / "info" / "attributes"
        self.assertFalse(info.exists() and info.read_text().strip(), "no local attributes workaround")
        m = self.manifest(FIXTURES)
        for cmd in ("attrs", "worktree", "index"):
            res = tool(cmd, "--repo", str(clone), "--manifest", str(m))
            self.assertEqual(res.returncode, 0, cmd + ": " + res.stdout)
        res = tool("commit", "--repo", str(clone), "--manifest", str(m), "--rev", "HEAD")
        self.assertEqual(res.returncode, 0, res.stdout)
        self.assertEqual((clone / "app" / "code.py").read_bytes(), APP)

    # an untracked local override is itself refused by the attrs check
    def test_6_local_override_refused(self):
        self.custody_repo()
        (self.repo / ".git" / "info").mkdir(exist_ok=True)
        (self.repo / ".git" / "info" / "attributes").write_text("* -text\n", encoding="utf-8")
        r = tool("attrs", "--repo", str(self.repo), "--manifest", str(self.manifest(FIXTURES)))
        self.assertEqual(r.returncode, 2)
        self.assertIn("no untracked override", r.stdout)


if __name__ == "__main__":
    unittest.main()
