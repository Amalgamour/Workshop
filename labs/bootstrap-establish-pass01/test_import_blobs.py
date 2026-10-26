"""Pack B #06 check 3: import_blobs.py refuses before any write, and restarts only from its journal.

  python -B test_import_blobs.py -v
"""
import csv, hashlib, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "import_blobs.py"
SCRATCH = HERE.parent / "bootstrap-git-bytes-pass01" / "scratch" / "import-tests"
ENV = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")


def git(repo, *a):
    return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, env=ENV, check=True).stdout.decode().strip()


class Imports(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.base = Path(tempfile.mkdtemp(prefix=self._testMethodName[:20] + "-", dir=SCRATCH))
        self.src = self.base / "src"
        self.src.mkdir()
        git(self.src, "init", "-q", "-b", "main")
        self.files = {"a/one.md": b"one\r\n", "a/two.md": b"two\n", "b/three.bin": b"\x00\x01three", "b/four.md": b"four\n"}
        for k, v in self.files.items():
            p = self.src / k
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(v)
        (self.src / ".gitattributes").write_bytes(b"* -text\n")
        git(self.src, "add", "-A")
        git(self.src, "commit", "-q", "-m", "src")
        self.rev = git(self.src, "rev-parse", "HEAD")
        (self.src / "a" / "one.md").write_bytes(b"later version\n")
        git(self.src, "commit", "-q", "-am", "later")
        self.dest = self.src  # import into the same repository's worktree, as Pack B does
        self.journal = self.base / "j.json"

    def blob(self, path, rev=None):
        return git(self.src, "rev-parse", f"{rev or self.rev}:{path}")

    def manifest(self, rows, name="m.tsv"):
        m = self.base / name
        with open(m, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(["row", "source", "git_blob", "sha256", "bytes", "destination"])
            for i, (path, dest) in enumerate(rows):
                data = self.files[path]
                w.writerow([f"R{i}", f"{self.rev[:7]}:{path}", self.blob(path), hashlib.sha256(data).hexdigest(), len(data), dest])
        return m

    def run_tool(self, m, *extra, env=None):
        return subprocess.run([sys.executable, "-B", str(TOOL), "--repo", str(self.dest), "--manifest", str(m),
                               "--journal", str(self.journal), *extra], capture_output=True, text=True, env=dict(os.environ, **(env or {})))

    def listing(self):
        return sorted(p.relative_to(self.dest).as_posix() for p in self.dest.rglob("*") if ".git" not in p.parts and p.is_file())

    def refused(self, r, words):
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn(words, r.stdout)

    def test_imports_exact_bytes_from_the_pinned_revision(self):
        r = self.run_tool(self.manifest([(k, "imp/" + k) for k in self.files]))
        self.assertEqual(r.returncode, 0, r.stdout)
        for k, v in self.files.items():
            self.assertEqual((self.dest / "imp" / k).read_bytes(), v)
        self.assertEqual((self.dest / "imp" / "a" / "one.md").read_bytes(), b"one\r\n")   # not the later or worktree version

    def test_case_duplicate_refused_before_writes(self):
        before = self.listing()
        self.refused(self.run_tool(self.manifest([("a/one.md", "imp/X.md"), ("a/two.md", "imp/x.MD")])), "differ only by case")
        self.refused(self.run_tool(self.manifest([("a/one.md", "Imp/a.md"), ("a/two.md", "imp/b.md")], "m2.tsv")), "spelled two ways")
        self.assertEqual(self.listing(), before)

    def test_escape_refused(self):
        for bad, words in [("../out.md", "'..'"), ("C:/x.md", "relative"), ("CON.md", "reserved"), (".git/x", ".git")]:
            with self.subTest(bad=bad):
                self.refused(self.run_tool(self.manifest([("a/two.md", bad)], "e.tsv")), words)

    def test_existing_destination_refused(self):
        (self.dest / "imp").mkdir()
        (self.dest / "imp" / "two.md").write_bytes(b"two\n")   # even identical bytes: not this tool's install
        self.refused(self.run_tool(self.manifest([("a/one.md", "imp/one.md"), ("a/two.md", "imp/two.md")])), "already exists")
        self.assertFalse((self.dest / "imp" / "one.md").exists())

    def test_bad_blob_and_hash_refused_before_writes(self):
        m = self.manifest([("a/one.md", "imp/one.md"), ("a/two.md", "imp/two.md")])
        rows = list(csv.reader(open(m, encoding="utf-8"), delimiter="\t"))
        later = self.blob("a/one.md", "HEAD")   # a real blob, elsewhere in history: not provenance
        bad = self.base / "bad-blob.tsv"
        with open(bad, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(rows[0]); w.writerow(rows[1]); w.writerow(rows[2][:2] + [later] + rows[2][3:])
        self.refused(self.run_tool(bad), "provenance")
        badh = self.base / "bad-hash.tsv"
        with open(badh, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(rows[0]); w.writerow(rows[1]); w.writerow(rows[2][:3] + ["0" * 64] + rows[2][4:])
        self.refused(self.run_tool(badh), "pinned length and SHA-256")
        self.assertFalse((self.dest / "imp").exists())
        self.assertFalse(self.journal.exists())

    def test_restart_with_journal(self):
        m = self.manifest([(k, "imp/" + k) for k in self.files])
        r = self.run_tool(m, env={"IMPORT_TEST_FAIL_AFTER": "2"})
        self.refused(r, "test interruption")
        j = json.loads(self.journal.read_text())
        self.assertEqual((j["state"], len(j["installed"])), ("installing", 2))
        self.refused(self.run_tool(m), "a journal exists")
        self.refused(self.run_tool(self.manifest([("a/one.md", "imp/a/one.md")], "other.tsv"), "--resume"), "other rows")
        r2 = self.run_tool(m, "--resume")
        self.assertEqual(r2.returncode, 0, r2.stdout)
        self.assertEqual(json.loads(self.journal.read_text())["state"], "complete")
        for k, v in self.files.items():
            self.assertEqual((self.dest / "imp" / k).read_bytes(), v)


if __name__ == "__main__":
    unittest.main()
