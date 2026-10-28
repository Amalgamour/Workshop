"""Tests for the read-only batch observation lab. Synthetic books stay outside the desk."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(LAB))

import batch_observe

COMMIT = "4cca1d2e9ac845e82a2d44df432f8f7f6584f1e5"
CORPUS = ROOT / "00.kernel/00.00.10.work/0508.return-capture/evidence/corpus05.12/corpus.json"
CORPUS_SHA = "591721b62f2bedafc2255e1638c64fa6642585b822defaf5c65253ea376e0b53"
BOOK = ROOT / "00.kernel/00.00.10.work"
HELPER = ROOT / "labs/return-capture-pass01/return_capture.py"
PY = sys.executable
FORBIDDEN = {"lifecycle", "accepted", "closed", "ready", "completed"}
ROLE = {
    "primary current submission": "primary-current-candidate",
    "retrospective custody of this same page": "same-page-retrospective",
    "secondary historical capture": "secondary-historical",
    "named in the assignment, not in the return heading text": "assignment-mention",
}


def run(argv: list[str]):
    code, payload, error = batch_observe.execute(argv)
    body = json.loads(payload.decode("utf-8")) if payload else None
    return code, body, error


def assert_open(test: unittest.TestCase, body: dict) -> None:
    test.assertEqual(body["schema"], "batch-observation/1")
    test.assertEqual(body["authority"], "none")
    test.assertEqual(body["review"]["binding"], "unbound")
    test.assertFalse(body["channels"]["revision_repaired"])
    test.assertEqual(body["custody"]["package_at_commit"], "not-established")
    for key in FORBIDDEN:
        test.assertNotIn(key, body)


class PinsAndRefusals(unittest.TestCase):
    def test_git_write_commands_are_refused(self):
        for args in (["commit", "-m", "no"], ["add", "x"], ["push"], ["fetch"], ["status"]):
            with self.assertRaises(batch_observe.ObserveError):
                batch_observe.run_git(str(ROOT), args)

    def test_parser_pin_mismatch_runs_no_git(self):
        calls = []
        original = batch_observe.run_git
        batch_observe.run_git = lambda *args, **kwargs: calls.append(args)
        old = batch_observe.PARSER_PATH
        try:
            with tempfile.TemporaryDirectory() as tmp:
                bad = Path(tmp) / "prime_support.py"
                bad.write_bytes(b"raise SystemExit('imported')\n")
                batch_observe.PARSER_PATH = bad
                code, payload, error = batch_observe.execute(
                    ["observe", "--repo", str(ROOT), "--commit", COMMIT, "--path", "README.md", "--json"]
                )
            self.assertEqual(code, 2)
            self.assertEqual(payload, b"")
            self.assertIn("pin mismatch", error)
            self.assertEqual(calls, [])
        finally:
            batch_observe.run_git = original
            batch_observe.PARSER_PATH = old

    def test_helper_pin_mismatch_runs_no_inspect(self):
        calls = []
        original = batch_observe.launch_inspect
        batch_observe.launch_inspect = lambda *args, **kwargs: calls.append(args)
        old = batch_observe.HELPER_PATH
        try:
            with tempfile.TemporaryDirectory() as tmp:
                bad = Path(tmp) / "return_capture.py"
                bad.write_bytes(b"not the helper\n")
                batch_observe.HELPER_PATH = bad
                code, payload, error = batch_observe.execute(
                    [
                        "observe",
                        "--supplied",
                        str(CORPUS),
                        "--path",
                        "00.kernel/00.00.10.work/0508.return-capture/05.10.md",
                        "--members-book",
                        str(BOOK),
                        "--json",
                    ]
                )
            self.assertEqual(code, 2)
            self.assertEqual(payload, b"")
            self.assertIn("pin mismatch", error)
            self.assertEqual(calls, [])
        finally:
            batch_observe.launch_inspect = original
            batch_observe.HELPER_PATH = old

    def test_malformed_inputs_and_unknown_schema(self):
        cases = [
            ["observe", "--repo", str(ROOT), "--commit", "abcd", "--path", "a.md", "--json"],
            ["observe", "--repo", str(ROOT), "--commit", COMMIT.upper(), "--path", "a.md", "--json"],
            ["observe", "--repo", str(ROOT), "--commit", COMMIT, "--path", "../a.md", "--json"],
            ["observe", "--repo", str(ROOT), "--commit", COMMIT, "--path", "C:/a.md", "--json"],
            ["observe", "--repo", str(ROOT), "--live", "--commit", COMMIT, "--path", "a.md", "--json"],
            ["observe", "--json"],
            ["observe", "--repo", str(ROOT), "--commit", COMMIT, "--path", "a.md"],
        ]
        for argv in cases:
            code, payload, error = batch_observe.execute(argv)
            self.assertEqual(code, 2, argv)
            self.assertEqual(payload, b"")
            self.assertTrue(error)
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "decl.json"
            bad.write_bytes(b'{"schema":"batch-observation/9"}\n')
            calls = []
            original = batch_observe.run_git
            batch_observe.run_git = lambda *args, **kwargs: calls.append(args)
            try:
                code, payload, error = batch_observe.execute(
                    [
                        "observe",
                        "--repo",
                        str(ROOT),
                        "--commit",
                        COMMIT,
                        "--path",
                        "a.md",
                        "--declaration",
                        str(bad),
                        "--json",
                    ]
                )
            finally:
                batch_observe.run_git = original
            self.assertEqual(code, 2)
            self.assertEqual(payload, b"")
            self.assertIn("unknown declaration schema", error)
            self.assertEqual(calls, [])
            broken = Path(tmp) / "broken.json"
            broken.write_bytes(b"{")
            code, payload, _error = batch_observe.execute(
                ["observe", "--supplied", str(CORPUS), "--declaration", str(broken), "--json"]
            )
            self.assertEqual(code, 2)
            self.assertEqual(payload, b"")


class GitAndSupplied(unittest.TestCase):
    def test_live_file_is_not_a_blob_and_git_stays_unmoved(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            repo.mkdir()
            subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "observe@example.com"], cwd=repo, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.name", "observe"], cwd=repo, check=True, capture_output=True)
            folder = repo / "label" / "00.00.10.work" / "0508.return-capture"
            folder.mkdir(parents=True)
            rel = "label/00.00.10.work/0508.return-capture/05.01.md"
            text = b"# 05\nstate: draft\n\n## Return\nexecution: returned\n"
            (folder / "05.01.md").write_bytes(text)
            subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True)
            subprocess.run(["git", "commit", "-m", "fixture"], cwd=repo, check=True, capture_output=True)
            commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True).stdout.decode().strip()
            code, body, error = run(["observe", "--repo", str(repo), "--commit", commit, "--path", rel, "--json"])
            self.assertEqual(code, 0, error)
            assert_open(self, body)
            self.assertEqual(body["source"]["kind"], "git-blob")
            self.assertEqual(body["source"]["label"], "git blob at the named commit")
            self.assertEqual(body["source"]["sha256"], hashlib.sha256(text).hexdigest())
            self.assertEqual(body["legacy"]["status"], "ok")
            self.assertEqual(body["legacy"]["execution"], "returned")
            self.assertTrue(body["legacy"]["revision_id"])
            (folder / "05.01.md").write_bytes(text + b"live line\n")
            code, live, error = run(["observe", "--repo", str(repo), "--live", "--path", rel, "--json"])
            self.assertEqual(code, 0, error)
            self.assertEqual(live["source"]["kind"], "live-file")
            self.assertEqual(live["source"]["label"], "worktree file, not a git blob")
            self.assertIsNone(live["source"]["commit"])
            self.assertNotEqual(live["source"]["sha256"], body["source"]["sha256"])
            supplied = repo / "supplied.md"
            supplied.write_bytes(text)
            code, other, error = run(["observe", "--supplied", str(supplied), "--path", rel, "--json"])
            self.assertEqual(code, 0, error)
            self.assertEqual(other["source"]["kind"], "supplied-text")
            self.assertEqual(other["source"]["label"], "supplied text, not a git blob")
            self.assertIsNone(other["source"]["commit"])
            self.assertIsNone(other["source"]["repository"])
            self.assertEqual(other["source"]["sha256"], hashlib.sha256(text).hexdigest())
            head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, check=True, capture_output=True).stdout.decode().strip()
            self.assertEqual(head, commit)
            self.assertEqual(subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=repo, check=True, capture_output=True).stdout.strip(), b"1")

    def test_typed_declaration_is_not_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "page.md"
            page.write_bytes(b"# 05\nstate: draft\n\n## Return\nexecution: returned\n")
            declaration = Path(tmp) / "declaration.json"
            declaration.write_text(
                json.dumps(
                    {
                        "schema": "batch-review-declaration/1",
                        "reviewed_member": "0191.declared-0513",
                        "reviewed_receipt_sha256": "ab" * 32,
                        "reviewed_disposition": "accepted",
                        "reviewer": "Codex Prime",
                    }
                ),
                encoding="utf-8",
            )
            code, body, error = run(
                ["observe", "--supplied", str(page), "--path", "label/00.00.10.work/0508.return-capture/05.01.md", "--declaration", str(declaration), "--json"]
            )
            self.assertEqual(code, 1, error)
            assert_open(self, body)
            self.assertEqual(body["review"]["typed_declaration"]["authority"], "not authenticated")
            self.assertEqual(body["review"]["typed_declaration"]["reviewed_disposition"], "accepted")
            self.assertIn("declaration-not-authenticated", body["attention"])
            self.assertIsNone(body["custody"]["primary"])


class RealCorpus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = CORPUS.read_bytes()
        if hashlib.sha256(data).hexdigest() != CORPUS_SHA:
            raise AssertionError("corpus pin drifted")
        cls.corpus = json.loads(data.decode("utf-8"))

    def observe_page(self, rel: str, book: str | None = None):
        argv = ["observe", "--repo", str(ROOT), "--commit", COMMIT, "--path", rel, "--json"]
        if book:
            argv[1:1] = ["--members-book", book]
            # insert before --json is awkward because of the slice. Rebuild.
            argv = [
                "observe",
                "--repo",
                str(ROOT),
                "--commit",
                COMMIT,
                "--path",
                rel,
                "--members-book",
                book,
                "--json",
            ]
        return run(argv)

    def test_sixteen_real_shapes(self):
        self.assertEqual(len(self.corpus["cases"]), 16)
        for case in self.corpus["cases"]:
            rel = case["source"]["path"]
            code, body, error = self.observe_page(rel, str(BOOK))
            self.assertIn(code, (0, 1), error)
            self.assertEqual(code, 1, case["id"])
            assert_open(self, body)
            self.assertEqual(body["source"]["kind"], "git-blob")
            self.assertEqual(body["source"]["commit"], COMMIT)
            self.assertEqual(body["source"]["sha256"], case["source"]["sha256"])
            self.assertEqual(body["source"]["bytes"], case["source"]["bytes"])
            self.assertEqual(body["source"]["label"], "git blob at the named commit")
            legacy = body["legacy"]
            observed = case["observation"]
            self.assertEqual(legacy["status"], observed["status"], case["id"])
            self.assertEqual(legacy["reason"], observed["reason"], case["id"])
            self.assertEqual(legacy["execution"], observed["execution"], case["id"])
            self.assertEqual(legacy["whole"], observed["whole"], case["id"])
            if observed["status"] != "ok":
                self.assertIsNone(legacy["revision_id"], case["id"])
                self.assertIsNone(legacy["review"], case["id"])
            else:
                self.assertEqual(legacy["revision_id"], observed["revision_id"], case["id"])
            self.assertEqual(body["fenced_headings"], [])
            primaries = [
                item["member"]
                for item in case["capture_roles"]
                if item["role"] == "primary current submission"
            ]
            expected_primary = primaries[0] if len(primaries) == 1 else None
            self.assertEqual(body["custody"]["primary"], expected_primary, case["id"])
            by_member = {item["member"]: item for item in body["custody"]["observations"]}
            for role in case["capture_roles"]:
                item = by_member[role["member"]]
                self.assertEqual(item["role"], ROLE[role["role"]], case["id"] + " " + role["member"])
                if role["role"] == "named in the assignment, not in the return heading text":
                    self.assertIsNone(item["inspection"])
                    self.assertIsNone(item["commit_receipt_present"])
                else:
                    self.assertEqual(item["inspection"]["status"], "complete", role["member"])
                    self.assertTrue(item["receipt_bytes_match"], role["member"])
                    self.assertEqual(item["inspection"]["capture"]["retrospective"], role["retrospective"])
            if case["id"] in {"C13", "C14"}:
                self.assertIn("return-pointers", [item["form"] for item in body["pointers"]])
            if case["id"] == "C14":
                self.assertEqual(body["pointers"][0]["members"][0]["name"], "0128.pack-assembly-0501")
                self.assertEqual(body["custody"]["primary"], "0129.assembly-capture-0510")
            if case["id"] == "C15":
                self.assertEqual(body["pointers"][0]["form"], "return-pointer")
                self.assertEqual(len(body["pointers"][0]["members"]), 2)
            if case["id"] in {"C01", "C08"}:
                self.assertIn("return-archive-pointer", [item["form"] for item in body["pointers"]])
                self.assertIn("return-em", [item["form"] for item in body["pointers"]])
            if case["id"] == "C07":
                digest = "8ac327e236f10315b27646a4328d9322d39f463720f37bc3c53cbbba055f269b"
                hashes = [item["hash"] for item in body["review"]["legacy_hashes"]]
                self.assertIn(digest, hashes)
                self.assertIn("legacy-hash-not-current", body["attention"])
                self.assertEqual(body["custody"]["observations"], [])
            if case["id"] == "C16":
                stray = "2cf4fd147bc4bcacb77585d11311ae6c57a4e031b40ede4d0f19a353af1e3816"
                hashes = [item["hash"] for item in body["review"]["legacy_hashes"]]
                self.assertNotIn(stray, hashes)
            if case["id"] == "C11":
                self.assertEqual(
                    [item["member"] for item in body["assignment_mentions"]],
                    ["0118.workflow-start-0501", "0119.app-entry-0503"],
                )

    def test_corpus_controls_and_real_missing(self):
        by_id = {item["id"]: item for item in self.corpus["synthetic_controls"]}
        for label in ("S1", "S2", "S3", "S4", "S6"):
            control = by_id[label]
            folder = None
            with tempfile.TemporaryDirectory() as tmp:
                page = Path(tmp) / "page.md"
                page.write_bytes(control["source"]["text"].encode("utf-8"))
                book = str(BOOK) if label == "S4" else None
                argv = ["observe", "--supplied", str(page), "--path", "label/00.00.10.work/0508.return-capture/05.12.md", "--json"]
                if book:
                    argv = [
                        "observe",
                        "--supplied",
                        str(page),
                        "--path",
                        "label/00.00.10.work/0508.return-capture/05.12.md",
                        "--members-book",
                        book,
                        "--json",
                    ]
                code, body, error = run(argv)
            self.assertEqual(code, 1, error)
            assert_open(self, body)
            self.assertEqual(body["source"]["kind"], "supplied-text")
            self.assertEqual(body["legacy"]["status"], control["observation"]["status"], label)
            self.assertEqual(body["legacy"]["reason"], control["observation"]["reason"], label)
            self.assertEqual(body["legacy"]["execution"], control["observation"]["execution"], label)
            if control["observation"]["status"] != "ok":
                self.assertIsNone(body["legacy"]["revision_id"], label)
            if label == "S1":
                self.assertEqual(body["fenced_headings"][0]["title"], "Return")
                self.assertEqual(body["pointers"][0]["form"], "return-pointer")
                self.assertEqual(body["pointers"][0]["members"][0]["name"], "0196.synthetic-fenced-0512")
                self.assertIn("fenced-heading-ignored", body["ambiguities"])
            if label == "S2":
                self.assertEqual(len(body["pointers"]), 2)
                self.assertIsNone(body["legacy"]["revision_id"])
                self.assertEqual(
                    [item["members"][0]["name"] for item in body["pointers"]],
                    ["0197.synthetic-one-0512", "0197.synthetic-two-0512"],
                )
            if label == "S3":
                self.assertEqual(len(body["pointers"][0]["members"]), 2)
                self.assertEqual(body["legacy"]["execution"], "unknown")
            if label == "S4":
                item = body["custody"]["observations"][0]
                self.assertEqual(item["role"], "missing")
                self.assertEqual(item["inspection"]["status"], "missing")
                self.assertEqual(item["exit"], 1)
                self.assertIsNone(item["inspection"]["capture"])
            if label == "S6":
                self.assertIn("unpaired-receipt", body["attention"])
                self.assertEqual(body["custody"]["observations"], [])
                self.assertEqual(body["legacy"]["review"]["disposition"], "recorded sentence only.")
                self.assertIn("legacy-hash-not-current", body["attention"])
                digest = body["review"]["legacy_hashes"][0]
                self.assertFalse(digest["equals_whole"])
                self.assertFalse(digest["equals_revision"])
                self.assertNotEqual(body["legacy"]["revision_id"], "8" * 64)
                self.assertNotEqual(body["legacy"]["whole"], "7" * 64)


class CustodyFixtures(unittest.TestCase):
    def helper(self, args: list[str], cwd: Path) -> str:
        proc = subprocess.run([PY, "-B", str(HELPER), *args], cwd=cwd, capture_output=True)
        text = proc.stdout.decode("utf-8", "replace")
        if proc.returncode != 0:
            raise AssertionError(text + proc.stderr.decode("utf-8", "replace"))
        return text

    def capture(self, book: Path, submission: str, name: str, origin: tuple[str, str, str], retrospective: bool) -> str:
        source = book / "src"
        source.mkdir(exist_ok=True)
        (source / "note.txt").write_bytes(b"fixture\n")
        return_file = source / f"{submission}.md"
        return_file.write_bytes(b"Did.\nBlocked.\nNeed.\nFixture.\n")
        reserved = self.helper(
            [
                "reserve",
                "--book",
                str(book),
                "--submission",
                submission,
                "--name",
                name,
                "--origin-book",
                origin[0],
                "--origin-page",
                origin[1],
                "--origin-batch",
                origin[2],
                "--expected-output",
                "note.txt",
                "--submitter",
                "Grok Builder 2",
                "--reviewer",
                "Codex Prime",
                "--release",
                "fixture only",
            ],
            book,
        )
        member = next(line.split()[1] for line in reserved.splitlines() if line.startswith("member "))
        command = [
            "capture",
            "--book",
            str(book),
            "--submission",
            submission,
            "--return-file",
            str(return_file),
            "--source-root",
            str(source),
            "--artifact",
            "note.txt|note.txt",
        ]
        if retrospective:
            command.extend(["--retrospective", "--source-commit", COMMIT])
        self.helper(command, book)
        self.assertTrue(str(book).startswith(tempfile.gettempdir()))
        self.assertFalse(str(book).startswith(str(ROOT)))
        return member

    def test_ambiguous_primary_cross_book_partial_and_foreign_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            book = Path(tmp) / "book"
            book.mkdir()
            same_a = self.capture(book, "obs-0513-same-a", "same-a-0513", ("00.00.10.work", "0508.return-capture", "05.99"), False)
            same_b = self.capture(book, "obs-0513-same-b", "same-b-0513", ("00.00.10.work", "0508.return-capture", "05.99"), False)
            foreign = self.capture(book, "obs-0513-foreign", "foreign-0513", ("00.00.10.work", "0509.pack-assembly", "05.01"), True)
            current = self.capture(book, "obs-0513-current", "current-0513", ("00.00.10.work", "0508.return-capture", "05.98"), False)
            other = self.capture(book, "obs-0513-other", "other-book-0513", ("other.book", "0508.return-capture", "05.97"), False)
            partial = book / "0199.synthetic-partial-0513"
            partial.mkdir()
            (partial / "return.md").write_bytes(b"Did.\nBlocked.\nNeed.\npartial\n")
            reserved_text = self.helper(
                [
                    "reserve",
                    "--book",
                    str(book),
                    "--submission",
                    "obs-0513-reserved",
                    "--name",
                    "reserved-0513",
                    "--origin-book",
                    "00.00.10.work",
                    "--origin-page",
                    "0508.return-capture",
                    "--origin-batch",
                    "05.96",
                    "--expected-output",
                    "note.txt",
                    "--submitter",
                    "Grok Builder 2",
                    "--reviewer",
                    "Codex Prime",
                    "--release",
                    "fixture only",
                ],
                book,
            )
            reserved = next(line.split()[1] for line in reserved_text.splitlines() if line.startswith("member "))

            def page(text: str, rel: str):
                file = book / "page.md"
                file.write_bytes(text.encode("utf-8"))
                return run(
                    [
                        "observe",
                        "--supplied",
                        str(file),
                        "--path",
                        rel,
                        "--members-book",
                        str(book),
                        "--json",
                    ]
                )

            code, body, error = page(
                f"## Return pointers\nMember: {same_a}\nReceipt: {'a' * 64}\n\nMember: {same_b}\nReceipt: {'b' * 64}\n",
                "label/00.00.10.work/0508.return-capture/05.99.md",
            )
            self.assertEqual(code, 1, error)
            assert_open(self, body)
            self.assertIsNone(body["custody"]["primary"])
            self.assertEqual(
                {item["role"] for item in body["custody"]["observations"]},
                {"ambiguous-primary-candidate"},
            )
            self.assertIn("multiple-primary-candidates", body["attention"])
            self.assertEqual(body["pointers"][0]["members"][0]["name"], same_a)
            self.assertIn("stated-receipt-differs", body["attention"])

            code, body, error = page(
                f"## Return pointers\nMember: {foreign}\nReceipt: {'c' * 64}\n\nMember: {current}\nReceipt: {'d' * 64}\n",
                "label/00.00.10.work/0508.return-capture/05.98.md",
            )
            self.assertEqual(code, 1, error)
            roles = {item["member"]: item["role"] for item in body["custody"]["observations"]}
            self.assertEqual(roles[foreign], "secondary-historical")
            self.assertEqual(roles[current], "primary-current-candidate")
            self.assertEqual(body["custody"]["primary"], current)
            self.assertEqual(body["pointers"][0]["members"][0]["name"], foreign)

            code, body, error = page(
                f"## Return pointer\nMember: {other}\nReceipt: {'e' * 64}\n",
                "label/00.00.10.work/0508.return-capture/05.97.md",
            )
            self.assertEqual(body["custody"]["observations"][0]["role"], "cross-book-origin")
            self.assertIsNone(body["custody"]["primary"])
            self.assertIn("cross-book-origin", body["attention"])

            code, body, error = page(
                "## Return pointer\nMember: 0199.synthetic-partial-0513\nReceipt: " + "f" * 64 + "\n",
                "label/00.00.10.work/0508.return-capture/05.95.md",
            )
            item = body["custody"]["observations"][0]
            self.assertEqual(item["role"], "incomplete")
            self.assertEqual(item["inspection"]["status"], "incomplete")
            self.assertEqual(item["exit"], 2)
            self.assertIsNone(body["custody"]["primary"])

            code, body, error = page(
                f"## Return pointer\nMember: {reserved}\nReceipt: {'9' * 64}\n",
                "label/00.00.10.work/0508.return-capture/05.96.md",
            )
            item = body["custody"]["observations"][0]
            self.assertEqual(item["role"], "reserved")
            self.assertEqual(item["inspection"]["status"], "reserved")
            self.assertEqual(item["exit"], 1)

    def test_reserved_member_on_the_desk_is_untouched(self):
        member = BOOK / "0138.batch-reader-0513"
        names = sorted(path.name for path in member.iterdir())
        self.assertEqual(names, ["01.md", "reservation.json"])
        digest = hashlib.sha256((member / "reservation.json").read_bytes()).hexdigest()
        self.assertEqual(digest, "b2484b6235ba6674c65732f53dfaaaa2bcd7a6f0adf4fc6aa736671e8a5798d5")
        for rel in (
            "labs/prime-support-pass01/prime_support.py",
            "labs/prime-support-pass01/clerk_adapter.py",
            "labs/return-capture-pass01/return_inspect.py",
            "labs/return-capture-pass01/return_capture.py",
        ):
            data = (ROOT / rel).read_bytes()
            if rel.endswith("prime_support.py"):
                self.assertEqual(hashlib.sha256(data).hexdigest(), batch_observe.PARSER_SHA)
                self.assertEqual(len(data), batch_observe.PARSER_BYTES)


if __name__ == "__main__":
    unittest.main()
