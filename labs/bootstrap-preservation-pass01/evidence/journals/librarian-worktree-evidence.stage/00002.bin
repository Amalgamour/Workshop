"""Pack A #02 tests for preserve_copy.py. Each test builds its own scratch repository and sources
under tests-tmp/ in this lab; no source checkout is touched.

  python -B test_preserve_copy.py -v
"""
import csv, hashlib, io, json, os, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "preserve_copy.py"
TMP = HERE / "tests-tmp"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def git(repo, *a):
    return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, check=True,
                          env=dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t"))


class Case(unittest.TestCase):
    def setUp(self):
        TMP.mkdir(exist_ok=True)
        self.base = Path(tempfile.mkdtemp(prefix=self._testMethodName[:20] + "-", dir=TMP))
        self.src = self.base / "src"
        self.dest = self.base / "dest"
        self.src.mkdir()
        self.dest.mkdir()
        git(self.dest, "init", "-q", "-b", "main")
        (self.dest / "kept.txt").write_bytes(b"base\n")
        (self.dest / "dir").mkdir()
        (self.dest / "dir" / "old.txt").write_bytes(b"old\n")
        git(self.dest, "add", "kept.txt", "dir/old.txt")
        git(self.dest, "commit", "-q", "-m", "base")
        self.head = git(self.dest, "rev-parse", "HEAD").stdout.decode().strip()
        self.journal = self.base / "journal" / "j.json"
        self.journal.parent.mkdir()
        self.allow = self.base / "allow.txt"
        self.allow.write_text("", encoding="utf-8")

    def source(self, name, data):
        p = self.src / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
        return p

    def manifest(self, rows, name="m.tsv"):
        m = self.base / name
        with open(m, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t", lineterminator="\n")
            w.writerow(["group", "source", "destination", "sha256", "bytes", "archive"])
            for src, dst, data in rows:
                w.writerow(["T", str(src), dst, sha(data), len(data), "a"])
        return m

    def run_tool(self, m, *extra, env=None, head=None):
        cmd = [sys.executable, "-B", str(TOOL), "--manifest", str(m), "--archive", "a", "--source-root", str(self.src),
               "--dest", str(self.dest), "--expect-head", head or self.head, "--allow-replace-file", str(self.allow),
               "--journal", str(self.journal), *extra]
        return subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, **(env or {})))

    def tree_bytes(self):
        out = {}
        for p in sorted(self.dest.rglob("*")):
            if ".git" in p.relative_to(self.dest).parts or not p.is_file():
                continue
            out[p.relative_to(self.dest).as_posix()] = p.read_bytes()
        return out

    def refused(self, r, words):
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn(words, r.stdout)

    # ---- success paths ----
    def test_new_file(self):
        d = b"new bytes\n"
        m = self.manifest([(self.source("a.txt", d), "x/a.txt", d)])
        r = self.run_tool(m)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual((self.dest / "x" / "a.txt").read_bytes(), d)
        self.assertEqual(json.loads(self.journal.read_text())["state"], "complete")

    def test_identical_retry(self):
        d = b"same\n"
        m = self.manifest([(self.source("a.txt", d), "a.txt", d)])
        self.assertEqual(self.run_tool(m, "--stage").returncode, 0)
        git(self.dest, "commit", "-q", "-m", "one")
        r = self.run_tool(m, head=git(self.dest, "rev-parse", "HEAD").stdout.decode().strip())
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("'present': 1", r.stdout)

    def test_allowed_clean_replacement(self):
        d = b"worktree version\n"
        self.allow.write_text("dir/old.txt\n", encoding="utf-8")
        m = self.manifest([(self.source("old.txt", d), "dir/old.txt", d)])
        r = self.run_tool(m)
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual((self.dest / "dir" / "old.txt").read_bytes(), d)

    # ---- refusals: destination state ----
    def test_tracked_not_allowed(self):
        d = b"other\n"
        m = self.manifest([(self.source("old.txt", d), "dir/old.txt", d)])
        self.refused(self.run_tool(m), "not an allowed replacement")

    def test_dirty_tracked_conflict(self):
        d = b"other\n"
        self.allow.write_text("dir/old.txt\n", encoding="utf-8")
        (self.dest / "dir" / "old.txt").write_bytes(b"locally edited\n")
        m = self.manifest([(self.source("old.txt", d), "dir/old.txt", d)])
        self.refused(self.run_tool(m), "not tracked and clean")

    def test_untracked_conflict(self):
        d = b"mine\n"
        (self.dest / "loose.txt").write_bytes(b"someone else's\n")
        self.allow.write_text("loose.txt\n", encoding="utf-8")
        m = self.manifest([(self.source("loose.txt", d), "loose.txt", d)])
        self.refused(self.run_tool(m), "not tracked and clean")

    def test_staged_conflict(self):
        d = b"n\n"
        (self.dest / "kept.txt").write_bytes(b"staged change\n")
        git(self.dest, "add", "kept.txt")
        m = self.manifest([(self.source("a.txt", d), "a.txt", d)])
        self.refused(self.run_tool(m), "unrelated or conflicting change")

    def test_unrelated_untracked(self):
        d = b"n\n"
        (self.dest / "stray.txt").write_bytes(b"stray\n")
        m = self.manifest([(self.source("a.txt", d), "a.txt", d)])
        self.refused(self.run_tool(m), "unrelated or conflicting change")

    def test_wrong_head(self):
        d = b"n\n"
        m = self.manifest([(self.source("a.txt", d), "a.txt", d)])
        self.refused(self.run_tool(m, head="0" * 40), "is not the expected")

    def test_not_independent_alternates(self):
        d = b"n\n"
        alt = self.dest / ".git" / "objects" / "info" / "alternates"
        alt.write_text(str(self.base), encoding="utf-8")
        m = self.manifest([(self.source("a.txt", d), "a.txt", d)])
        self.refused(self.run_tool(m), "alternates")

    # ---- refusals: sources and names ----
    def test_changed_source(self):
        d = b"pinned\n"
        p = self.source("a.txt", d)
        m = self.manifest([(p, "a.txt", d)])
        p.write_bytes(b"edited after pinning\n")
        self.refused(self.run_tool(m), "source changed")

    def test_duplicate_and_case_collision(self):
        d = b"n\n"
        a, b = self.source("a.txt", d), self.source("b.txt", d)
        self.refused(self.run_tool(self.manifest([(a, "Same.txt", d), (b, "same.TXT", d)])), "share a destination")
        self.refused(self.run_tool(self.manifest([(a, "Dir/new.txt", d)])), "only by case")

    def test_bad_names(self):
        d = b"n\n"
        p = self.source("a.txt", d)
        for bad, words in [("../out.txt", "'..'"), ("C:/x.txt", "relative"), ("/abs.txt", "relative"), ("a\\b.txt", "relative"),
                           ("a.txt:stream", "stream"), ("CON.txt", "reserved"), ("lpt1", "reserved"), ("trail.", "dot or space"),
                           ("sp /x.txt", "dot or space"), (".git/config", ".git"), ("q?.txt", "forbidden")]:
            with self.subTest(bad=bad):
                self.refused(self.run_tool(self.manifest([(p, bad, d)])), words)

    def test_source_outside_root(self):
        d = b"n\n"
        outside = self.base / "elsewhere.txt"
        outside.write_bytes(d)
        self.refused(self.run_tool(self.manifest([(outside, "a.txt", d)])), "outside every --source-root")

    def test_alias(self):
        d = b"n\n"
        p = self.dest / "inside.txt"
        p.write_bytes(d)
        cmd = [sys.executable, "-B", str(TOOL), "--manifest", str(self.manifest([(p, "copy.txt", d)])), "--archive", "a",
               "--source-root", str(self.dest), "--dest", str(self.dest), "--expect-head", self.head, "--journal", str(self.journal)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        self.refused(r, "alias")

    def test_junction_escape(self):
        if os.name != "nt":
            self.skipTest("junctions are Windows-only")
        d = b"n\n"
        target = self.base / "outside-dir"
        target.mkdir()
        r = subprocess.run(["cmd", "/c", "mklink", "/J", str(self.dest / "jx"), str(target)], capture_output=True, text=True)
        if r.returncode:
            self.skipTest("could not create a junction: " + r.stdout + r.stderr)
        (self.dest / ".git" / "info" / "exclude").write_text("jx\n", encoding="utf-8")
        res = self.run_tool(self.manifest([(self.source("a.txt", d), "jx/a.txt", d)]))
        self.refused(res, "reparse point")
        self.assertFalse((target / "a.txt").exists())

    def test_source_symlink(self):
        d = b"n\n"
        real = self.source("real.txt", d)
        link = self.src / "link.txt"
        try:
            os.symlink(real, link)
        except OSError as e:
            self.skipTest(f"symlink not permitted here: {e}")
        self.refused(self.run_tool(self.manifest([(link, "a.txt", d)])), "link or reparse")

    # ---- whole batch and recovery ----
    def test_late_invalid_row_writes_nothing(self):
        d = b"n\n"
        before = self.tree_bytes()
        rows = [(self.source(f"f{i}.txt", d + bytes([65 + i])), f"out/f{i}.txt", d + bytes([65 + i])) for i in range(4)]
        rows.append((self.source("bad.txt", d), "../escape.txt", d))
        self.refused(self.run_tool(self.manifest(rows)), "'..'")
        self.assertEqual(self.tree_bytes(), before)
        self.assertFalse(self.journal.exists())

    def test_interruption_and_recovery(self):
        rows = [(self.source(f"f{i}.txt", bytes([97 + i]) * 5), f"r/f{i}.txt", bytes([97 + i]) * 5) for i in range(4)]
        m = self.manifest(rows)
        r = self.run_tool(m, env={"PRESERVE_TEST_FAIL_AFTER": "2"})
        self.refused(r, "test interruption")
        self.assertNotIn("complete:", r.stdout)
        j = json.loads(self.journal.read_text())
        self.assertEqual(j["state"], "installing")
        self.assertEqual(len(j["installed"]), 2)
        self.refused(self.run_tool(m), "incomplete journal")          # no resume flag: refuse
        other = self.manifest(rows[:3], "other.tsv")
        self.refused(self.run_tool(other, "--resume"), "other rows")   # other rows: refuse
        r2 = self.run_tool(m, "--resume")
        self.assertEqual(r2.returncode, 0, r2.stdout)
        self.assertEqual(json.loads(self.journal.read_text())["state"], "complete")
        for src, dst, data in rows:
            self.assertEqual((self.dest / dst).read_bytes(), data)

    def test_stage_only_listed_paths(self):
        d = b"n\n"
        m = self.manifest([(self.source("a.txt", d), "s/a.txt", d)])
        self.assertEqual(self.run_tool(m, "--stage").returncode, 0)
        staged = git(self.dest, "diff", "--cached", "--name-only").stdout.decode().split()
        self.assertEqual(staged, ["s/a.txt"])


if __name__ == "__main__":
    unittest.main()
