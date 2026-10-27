"""Batch 0502.workflow-start/05.02 #03: check_book.py against disposable synthetic Git repositories.

  python -B -X dev tests/test_check_book.py -v        (from the lab folder)

Every fixture repository is created under scratch/tests/ (ignored) with its own `git init` and commits, using
per-command identity variables only; no global or system Git configuration is read for identity or changed.
Expected findings are passing tests; they are not implementation failures.
"""
import hashlib, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
TOOL = LAB / "check_book.py"
SCRATCH = LAB / "scratch" / "tests"
ENV = dict(os.environ, GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@local", GIT_COMMITTER_NAME="fixture",
           GIT_COMMITTER_EMAIL="fixture@local", GIT_OPTIONAL_LOCKS="0")
BOOK = "00.kernel/00.00.10.work"

GOOD = """# 01

## Pages

| Page | Faces and files |
|---|---|
| `0010.about` | `01.001.md` |
| `0011.contents` | `01.001.md`, `01.002.md` |
| `0401.goal` | `01.md`, `06.01.md`, `evidence/` (3 files) |

Book files: `00.md`.

## Other books
Syntax: `../00.00.00.syntax/00.001.md`. Law: `../00.00.01.law/00.001.md`. Each lists what it holds.
"""


def git(repo, *a):
    return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, env=ENV, check=True).stdout.decode().strip()


class Book(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.repo = Path(tempfile.mkdtemp(prefix=self._testMethodName[:24] + "-", dir=SCRATCH))
        git(self.repo, "init", "-q", "-b", "main")
        self.files = {
            f"{BOOK}/00.md": "00.00.10.work: the work book. Provisional; contents in 0011.contents/01.002.md.\n",
            f"{BOOK}/0010.about/01.001.md": "about\n",
            f"{BOOK}/0011.contents/01.001.md": "old candidate\n",
            f"{BOOK}/0011.contents/01.002.md": GOOD,
            f"{BOOK}/0401.goal/01.md": "goal\n",
            f"{BOOK}/0401.goal/06.01.md": "record\n",
            f"{BOOK}/0401.goal/evidence/a.txt": "a\n",
            f"{BOOK}/0401.goal/evidence/b.txt": "b\n",
            f"{BOOK}/0401.goal/evidence/deep/c.txt": "c\n",
            "00.kernel/00.00.00.syntax/00.001.md": "syntax\n",
            "00.kernel/00.00.01.law/00.001.md": "law\n",
        }

    def commit(self, files=None, msg="fixture"):
        for rel, text in (files or self.files).items():
            p = self.repo / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(text.encode("utf-8"))
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", msg)
        return git(self.repo, "rev-parse", "HEAD")

    def run_tool(self, rev, *extra):
        r = subprocess.run([sys.executable, "-B", str(TOOL), "--root", str(self.repo), "--revision", rev, "--book", BOOK, "--json", *extra],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.stderr, "", "the tool wrote to stderr (a warning would hide here)")
        return r.returncode, json.loads(r.stdout)

    def kinds(self, rep):
        return sorted(f["kind"] for f in rep["findings"])

    def snapshot(self):
        idx = self.repo / ".git" / "index"
        return (git(self.repo, "status", "--porcelain=v1", "-uall"), git(self.repo, "rev-parse", "HEAD"),
                hashlib.sha256(idx.read_bytes()).hexdigest() if idx.exists() else None)

    # ---- clean ----
    def test_correct_book_is_clean(self):
        sha = self.commit()
        code, rep = self.run_tool(sha)
        self.assertEqual((code, rep["result"]), (0, "clean"), rep)
        self.assertEqual(rep["selection_source"], "book 00.md pointer")
        self.assertEqual(rep["contents_path"], f"{BOOK}/0011.contents/01.002.md")
        self.assertEqual([o["present"] for o in rep["other_books"]], [True, True])

    # ---- published versus local ----
    def test_untracked_local_folder_does_not_satisfy_a_missing_published_page(self):
        f = dict(self.files)
        f[f"{BOOK}/0011.contents/01.002.md"] = GOOD.replace("| `0401.goal` |", "| `0402.local` | `01.md` |\n| `0401.goal` |")
        sha = self.commit(f)
        local = self.repo / BOOK / "0402.local"
        local.mkdir()
        (local / "01.md").write_text("local only\n", encoding="utf-8")
        code, rep = self.run_tool(sha)
        self.assertEqual(code, 1)
        self.assertEqual(self.kinds(rep), ["missing-page"])

    def test_working_tree_and_index_changes_do_not_alter_a_pinned_result(self):
        sha = self.commit()
        before = self.run_tool(sha)
        (self.repo / BOOK / "0010.about" / "01.001.md").write_text("edited locally\n", encoding="utf-8")
        (self.repo / BOOK / "0099.untracked").mkdir()
        (self.repo / BOOK / "0099.untracked" / "01.md").write_text("x\n", encoding="utf-8")
        (self.repo / BOOK / "0011.contents" / "01.002.md").write_text("broken\n", encoding="utf-8")
        git(self.repo, "add", f"{BOOK}/0011.contents/01.002.md")          # a staged change, too
        self.assertEqual(self.run_tool(sha), before)

    def test_checker_is_read_only_on_the_inspected_checkout(self):
        sha = self.commit()
        (self.repo / "loose.txt").write_text("untracked\n", encoding="utf-8")
        (self.repo / BOOK / "0010.about" / "01.001.md").write_text("modified\n", encoding="utf-8")
        before = self.snapshot()
        for extra in ((), ("--contents", "0011.contents/01.001.md")):
            self.run_tool(sha, *extra)
        self.assertEqual(self.snapshot(), before)

    # ---- tree mismatches ----
    def test_files_and_count_mismatch(self):
        f = dict(self.files)
        f[f"{BOOK}/0011.contents/01.002.md"] = GOOD.replace("`evidence/` (3 files)", "`evidence/` (2 files), `gone.md`")
        f[f"{BOOK}/0401.goal/extra.md"] = "extra\n"
        sha = self.commit(f)
        code, rep = self.run_tool(sha)
        self.assertEqual(code, 1)
        self.assertEqual(self.kinds(rep), ["count-mismatch", "extra-file", "missing-file"])
        cm = [x for x in rep["findings"] if x["kind"] == "count-mismatch"][0]
        self.assertEqual((cm["expected"], cm["actual"]), (2, 3))

    def test_duplicate_page_identity(self):
        f = dict(self.files)
        f[f"{BOOK}/0011.contents/01.002.md"] = GOOD.replace(
            "| `0401.goal` |", "| `0010.about` | `01.001.md` |\n| `0401.other` | `01.md` |\n| `0401.goal` |")
        sha = self.commit(f)
        code, rep = self.run_tool(sha)
        self.assertEqual(code, 1)
        self.assertEqual(self.kinds(rep), ["duplicate-page-number", "duplicate-row", "missing-page"])

    def test_missing_book_file_and_other_book(self):
        f = dict(self.files)
        f[f"{BOOK}/0011.contents/01.002.md"] = GOOD.replace("Book files: `00.md`.", "Book files: `00.md`, `README.md`.").replace(
            "../00.00.01.law/00.001.md", "../00.00.01.law/00.002.md")
        sha = self.commit(f)
        code, rep = self.run_tool(sha)
        self.assertEqual(code, 1)
        self.assertEqual(self.kinds(rep), ["missing-book-file", "missing-other-book"])

    # ---- selection ----
    def test_pointer_to_older_candidate_is_honoured_not_the_newest(self):
        f = dict(self.files)
        f[f"{BOOK}/00.md"] = "Provisional; contents in 0011.contents/01.001.md.\n"
        f[f"{BOOK}/0011.contents/01.001.md"] = GOOD
        f[f"{BOOK}/0011.contents/01.003.md"] = "newer candidate, deliberately not a valid contents face\n"
        f[f"{BOOK}/0011.contents/01.002.md"] = "also not selected\n"
        sha = self.commit(f)
        code, rep = self.run_tool(sha)
        self.assertEqual(rep["contents_path"], f"{BOOK}/0011.contents/01.001.md")
        self.assertEqual(rep["selection_source"], "book 00.md pointer")
        self.assertIn("extra-file", self.kinds(rep), "01.003 is reported as unlisted, never chosen")

    def test_explicit_contents_is_labelled_as_not_selected_by_the_sentinel(self):
        f = dict(self.files)
        f[f"{BOOK}/00.md"] = "Provisional; contents in 0011.contents/01.001.md.\n"
        sha = self.commit(f)
        code, rep = self.run_tool(sha, "--contents", "0011.contents/01.002.md")
        self.assertEqual(rep["contents_path"], f"{BOOK}/0011.contents/01.002.md")
        self.assertIn("not selected by the sentinel", rep["selection_source"])
        self.assertIsNone(rep["sentinel_pointer"])

    def test_missing_ambiguous_and_dangling_pointer_refuse(self):
        cases = {"none": "Provisional; no pointer here.\n",
                 "two": "contents in 0011.contents/01.001.md. Also contents in 0011.contents/01.002.md.\n",
                 "dangling": "contents in 0011.contents/01.009.md.\n",
                 "outside": "contents in ../elsewhere/01.md.\n"}
        for name, text in cases.items():
            with self.subTest(case=name):
                f = dict(self.files)
                f[f"{BOOK}/00.md"] = text
                sha = self.commit(f, msg=name)
                code, rep = self.run_tool(sha)
                self.assertEqual((code, rep["result"]), (2, "refused"), rep)

    def test_no_sentinel_refuses(self):
        f = {k: v for k, v in self.files.items() if not k.endswith("work/00.md")}
        sha = self.commit(f)
        code, rep = self.run_tool(sha)
        self.assertEqual(code, 2)
        self.assertIn("no 00.md", rep["reason"])

    # ---- escape and bad input ----
    def test_path_escape(self):
        f = dict(self.files)
        f[f"{BOOK}/0011.contents/01.002.md"] = GOOD.replace("../00.00.01.law/00.001.md", "../../../../outside.md")
        sha = self.commit(f)
        code, rep = self.run_tool(sha)
        self.assertEqual(code, 1)
        self.assertEqual(self.kinds(rep), ["path-escape"])
        for bad in (("--contents", "../0011.contents/01.002.md"), ("--contents", "C:/x/01.md"), ("--contents", "0401.goal/01.md")):
            with self.subTest(arg=bad):
                self.assertEqual(self.run_tool(sha, *bad)[0], 2)
        r = subprocess.run([sys.executable, "-B", str(TOOL), "--root", str(self.repo), "--revision", sha, "--book", "../outside", "--json"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)

    def test_unsupported_table_syntax_refuses(self):
        variants = {"extra column": GOOD.replace("| `0010.about` | `01.001.md` |", "| `0010.about` | `01.001.md` | note |"),
                    "bare entry": GOOD.replace("| `0010.about` | `01.001.md` |", "| `0010.about` | 01.001.md |"),
                    "dir without count": GOOD.replace("`evidence/` (3 files)", "`evidence/`"),
                    "header": GOOD.replace("| Page | Faces and files |", "| Page | Files |"),
                    "no pages": GOOD.replace("## Pages", "## Index"),
                    "no book files": GOOD.replace("Book files: `00.md`.", "")}
        for name, text in variants.items():
            with self.subTest(variant=name):
                f = dict(self.files)
                f[f"{BOOK}/0011.contents/01.002.md"] = text
                sha = self.commit(f, msg=name)
                code, rep = self.run_tool(sha)
                self.assertEqual((code, rep["result"]), (2, "refused"), rep)
                self.assertIn("unsupported structure", rep["reason"])

    def test_bad_revision_refuses(self):
        self.commit()
        for rev in ("0" * 40, "no-such-branch"):
            with self.subTest(rev=rev):
                self.assertEqual(self.run_tool(rev)[0], 2)
        # an option-looking revision passed as a value reaches the checker's own refusal, not git
        r = subprocess.run([sys.executable, "-B", str(TOOL), "--root", str(self.repo), "--revision=--output=x", "--book", BOOK, "--json"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("may not start with '-'", json.loads(r.stdout)["reason"])
        self.assertFalse((self.repo / "x").exists())

    # ---- Other books, the whole section (0502.workflow-start/05.03, OR-01) ----
    def contents(self, text, msg):
        f = dict(self.files)
        f[f"{BOOK}/0011.contents/01.002.md"] = text
        return self.run_tool(self.commit(f, msg=msg))

    def test_or01_second_line_missing_book_is_a_finding_not_clean(self):
        # Prime's fixture from the 05.02 review, byte for byte
        code, rep = self.contents(GOOD.replace(" Each lists what it holds.", "\nMissing: `../00.00.99.missing/00.md`."), "or01")
        self.assertEqual(code, 1, rep)
        self.assertEqual(self.kinds(rep), ["missing-other-book"])
        self.assertEqual([o["path"] for o in rep["other_books"]],
                         ["../00.00.00.syntax/00.001.md", "../00.00.01.law/00.001.md", "../00.00.99.missing/00.md"])

    def test_other_books_multiline_form_and_section_boundary(self):
        head = GOOD.split("## Other books")[0] + "## Other books\n"
        cases = {"two lines and a blank line": (head + "Syntax: `../00.00.00.syntax/00.001.md`.\n\nLaw: `../00.00.01.law/00.001.md`. Each lists what it holds.\n", 0),
                 "missing book on a later line": (head + "Syntax: `../00.00.00.syntax/00.001.md`.\nGone: `../00.00.99.missing/00.md`. Each lists what it holds.\n", 1),
                 "a later heading ends the section": (GOOD + "\n## Notes\nFree text `../00.00.99.missing/00.md` here.\n", 0)}
        for name, (text, want) in cases.items():
            with self.subTest(case=name):
                code, rep = self.contents(text, name)
                self.assertEqual(code, want, rep)

    def test_other_books_unconsumed_text_refuses(self):
        syn, law, tail = "Syntax: `../00.00.00.syntax/00.001.md`.", "Law: `../00.00.01.law/00.001.md`.", "Each lists what it holds."
        head = GOOD.split("## Other books")[0]
        variants = {"same-line unlabelled path": f"## Other books\n{syn} see `../00.00.99.missing/00.md`. {law} {tail}\n",
                    "comma separator": f"## Other books\nSyntax: `../00.00.00.syntax/00.001.md`, {law} {tail}\n",
                    "item after the sentence": f"## Other books\n{syn} {law} {tail} Missing: `../00.00.99.missing/00.md`.\n",
                    "prose line": f"## Other books\n{syn} {law} {tail}\nSee also the old index.\n",
                    "bare path line": f"## Other books\n{syn} {law} {tail}\n`../00.00.99.missing/00.md`.\n",
                    "sentence on an earlier line": f"## Other books\n{syn} {tail}\n{law}\n",
                    "sentence alone": f"## Other books\n{syn} {law}\n{tail}\n",
                    "item without period": f"## Other books\n{syn} Law: `../00.00.01.law/00.001.md` {tail}\n",
                    "trailing whitespace": f"## Other books\n{syn} {law} {tail}  \n",
                    "duplicate heading": f"## Other books\n{syn} {law} {tail}\n\n## Other books\nMissing: `../00.00.99.missing/00.md`.\n",
                    "near-miss heading": "## Other Books\nMissing: `../00.00.99.missing/00.md`.\n",
                    "empty section": "## Other books\n\n"}
        for name, section in variants.items():
            with self.subTest(variant=name):
                code, rep = self.contents(head + section, name)
                self.assertEqual((code, rep["result"]), (2, "refused"), rep)
                self.assertIn("unsupported structure", rep["reason"])


if __name__ == "__main__":
    unittest.main()
