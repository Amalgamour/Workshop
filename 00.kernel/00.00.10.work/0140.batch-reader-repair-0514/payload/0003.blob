"""Tests for the read-only batch observation lab. Synthetic books stay outside the desk."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
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
Z_STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}Z$")


def tree_fingerprint(root: Path) -> str:
    if not root.exists():
        return "absent"
    rows = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        if path.is_dir():
            rows.append(f"dir {rel}")
        elif path.is_file():
            rows.append(f"file {rel} {hashlib.sha256(path.read_bytes()).hexdigest()} {path.stat().st_size}")
    return hashlib.sha256("\n".join(rows).encode("utf-8")).hexdigest()


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
        original_run = batch_observe.subprocess.run

        def record_git(*args, **kwargs):
            calls.append(("run_git", args))

        def record_subprocess(*args, **kwargs):
            calls.append(("subprocess", args))
            raise AssertionError("subprocess before a failed pin")

        batch_observe.run_git = record_git
        batch_observe.subprocess.run = record_subprocess
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
            self.assertNotIn("Traceback", error)
            self.assertEqual(calls, [])
        finally:
            batch_observe.run_git = original
            batch_observe.subprocess.run = original_run
            batch_observe.PARSER_PATH = old

    def test_helper_pin_mismatch_runs_no_inspect(self):
        calls = []
        original = batch_observe.launch_inspect
        original_run = batch_observe.subprocess.run

        def record_inspect(*args, **kwargs):
            calls.append(("inspect", args))

        def record_subprocess(*args, **kwargs):
            calls.append(("subprocess", args))
            raise AssertionError("subprocess before a failed pin")

        batch_observe.launch_inspect = record_inspect
        batch_observe.subprocess.run = record_subprocess
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
            self.assertNotIn("Traceback", error)
            self.assertEqual(calls, [])
        finally:
            batch_observe.launch_inspect = original
            batch_observe.subprocess.run = original_run
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
            self.assertEqual(body["source"]["commit"], commit)
            self.assertEqual(body["source"]["time_basis"], "git-blob")
            self.assertIsNone(body["source"]["live_observed_at"])
            self.assertIsNone(body["source"]["observation_started_at"])
            self.assertIsNone(body["source"]["observation_finished_at"])
            self.assertEqual(body["legacy"]["status"], "ok")
            self.assertEqual(body["legacy"]["execution"], "returned")
            self.assertTrue(body["legacy"]["revision_id"])
            (folder / "05.01.md").write_bytes(text + b"live line\n")
            code, live, error = run(["observe", "--repo", str(repo), "--live", "--path", rel, "--json"])
            self.assertEqual(code, 0, error)
            self.assertEqual(live["source"]["kind"], "live-file")
            self.assertEqual(live["source"]["label"], "worktree file, not a git blob")
            self.assertIsNone(live["source"]["commit"])
            self.assertEqual(live["source"]["time_basis"], "live-read")
            self.assertRegex(live["source"]["live_observed_at"], Z_STAMP)
            self.assertRegex(live["source"]["observation_started_at"], Z_STAMP)
            self.assertRegex(live["source"]["observation_finished_at"], Z_STAMP)
            self.assertEqual(live["source"]["live_observed_at"], live["source"]["observation_finished_at"])
            self.assertLessEqual(live["source"]["observation_started_at"], live["source"]["observation_finished_at"])
            self.assertNotEqual(live["source"]["sha256"], body["source"]["sha256"])
            supplied = repo / "supplied.md"
            supplied.write_bytes(text)
            code, other, error = run(["observe", "--supplied", str(supplied), "--path", rel, "--json"])
            self.assertEqual(code, 0, error)
            self.assertEqual(other["source"]["kind"], "supplied-text")
            self.assertEqual(other["source"]["label"], "supplied text, not a git blob")
            self.assertIsNone(other["source"]["commit"])
            self.assertIsNone(other["source"]["repository"])
            self.assertEqual(other["source"]["time_basis"], "supplied-text")
            self.assertIsNone(other["source"]["live_observed_at"])
            self.assertIsNone(other["source"]["observation_started_at"])
            self.assertIsNone(other["source"]["observation_finished_at"])
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

    def test_malformed_declarations_refuse_without_traceback(self):
        base = {
            "schema": "batch-review-declaration/1",
            "reviewed_member": "0191.declared-0513",
            "reviewed_receipt_sha256": "ab" * 32,
            "reviewed_disposition": "accepted",
            "reviewer": "Codex Prime",
        }
        bad_values = [[], {}, None, True, False, 0, 1.5]
        calls = []
        original_run = batch_observe.subprocess.run

        def record_subprocess(*args, **kwargs):
            calls.append(args)
            raise AssertionError("subprocess during declaration refusal")

        batch_observe.subprocess.run = record_subprocess
        try:
            with tempfile.TemporaryDirectory() as tmp:
                page = Path(tmp) / "page.md"
                page.write_bytes(b"# 05\nstate: draft\n\n## Return\nexecution: returned\n")
                declaration = Path(tmp) / "declaration.json"
                argv = [
                    "observe",
                    "--repo",
                    str(ROOT),
                    "--commit",
                    COMMIT,
                    "--path",
                    "00.kernel/00.00.10.work/0508.return-capture/05.10.md",
                    "--declaration",
                    str(declaration),
                    "--json",
                ]
                for field in (
                    "reviewed_member",
                    "reviewed_receipt_sha256",
                    "reviewed_disposition",
                    "reviewer",
                ):
                    for value in bad_values:
                        body = dict(base)
                        body[field] = value
                        declaration.write_text(json.dumps(body), encoding="utf-8")
                        code, payload, error = batch_observe.execute(argv)
                        self.assertEqual(code, 2, (field, value, error))
                        self.assertEqual(payload, b"")
                        self.assertNotIn("Traceback", error)
                        self.assertIn("not usable", error)
                for literal in ("NaN", "Infinity", "-Infinity"):
                    declaration.write_text(
                        "{"
                        '"schema":"batch-review-declaration/1",'
                        '"reviewed_member":"0191.declared-0513",'
                        '"reviewed_receipt_sha256":"' + ("ab" * 32) + '",'
                        '"reviewed_disposition":' + literal + ","
                        '"reviewer":"Codex Prime"'
                        "}",
                        encoding="utf-8",
                    )
                    code, payload, error = batch_observe.execute(argv)
                    self.assertEqual(code, 2, literal)
                    self.assertEqual(payload, b"")
                    self.assertNotIn("Traceback", error)
                    self.assertIn("not json", error)
                declaration.write_text(
                    '{"schema":"batch-review-declaration/1","schema":"batch-review-declaration/1",'
                    '"reviewed_member":"0191.declared-0513","reviewed_receipt_sha256":"'
                    + ("cd" * 32)
                    + '","reviewed_disposition":"held","reviewer":"Codex Prime"}',
                    encoding="utf-8",
                )
                code, payload, error = batch_observe.execute(argv)
                self.assertEqual(code, 2)
                self.assertEqual(payload, b"")
                self.assertIn("duplicate key", error)
                self.assertNotIn("Traceback", error)
                missing = dict(base)
                del missing["reviewer"]
                declaration.write_text(json.dumps(missing), encoding="utf-8")
                code, payload, error = batch_observe.execute(argv)
                self.assertEqual(code, 2)
                self.assertEqual(payload, b"")
                self.assertIn("keys are not the contract set", error)
                extra = dict(base)
                extra["accepted"] = True
                declaration.write_text(json.dumps(extra), encoding="utf-8")
                code, payload, error = batch_observe.execute(argv)
                self.assertEqual(code, 2)
                self.assertEqual(payload, b"")
                self.assertIn("keys are not the contract set", error)
                self.assertNotIn("Traceback", error)
                declaration.write_bytes(b"\xff")
                code, payload, error = batch_observe.execute(
                    ["observe", "--supplied", str(page), "--declaration", str(declaration), "--json"]
                )
                self.assertEqual(code, 2)
                self.assertEqual(payload, b"")
                self.assertIn("not utf-8", error)
                self.assertNotIn("Traceback", error)
            self.assertEqual(calls, [])
        finally:
            batch_observe.subprocess.run = original_run


class EligibleFields(unittest.TestCase):
    def observe_text(self, text: str):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "page.md"
            data = text.encode("utf-8")
            page.write_bytes(data)
            before = hashlib.sha256(page.read_bytes()).hexdigest()
            code, body, error = run(
                [
                    "observe",
                    "--supplied",
                    str(page),
                    "--path",
                    "label/00.00.10.work/0508.return-capture/05.14.md",
                    "--json",
                ]
            )
            self.assertEqual(hashlib.sha256(page.read_bytes()).hexdigest(), before)
            module = batch_observe.load_parser()
            parsed = module.parse_source(data, "page-return")
            self.assertEqual(body["legacy"]["status"], parsed["status"])
            self.assertEqual(body["legacy"]["reason"], parsed["reason"])
            self.assertEqual(body["legacy"]["execution"], parsed["execution"])
            self.assertEqual(body["legacy"]["whole"], parsed["whole"])
            if parsed["status"] != "ok":
                self.assertIsNone(body["legacy"]["revision_id"])
            return code, body, error

    def test_fences_quotes_and_other_sections_do_not_fill_fields(self):
        lines = [
            "state: draft",
            "```",
            "state: fenced-draft",
            "Executor: Fenced Person",
            "Release: fenced release",
            "Claim: fenced claim",
            "## Return pointer",
            "Member: 0196.synthetic-fenced-0512",
            "```",
            "> state: quoted-draft",
            "> Executor: Quoted Person",
            "> Release: quoted release",
            "> Claim: quoted claim",
            "  > Release: indented quote",
            "## Notes",
            "state: notes-draft",
            "Executor: Notes Person",
            "Release: notes release",
            "Claim: notes claim",
            "The prose mentions Release: and Claim: without starting the field.",
            "## Assignment",
            "Executor: Actual Executor",
            "Release and claim: recorded in the Return pointer. This draft grants no release.",
            "````",
            "```",
            "Release: inner false",
            "```",
            "Claim: still fenced",
            "````",
            "## Return pointer",
            "Release: actual release",
            "Claim: actual claim",
            "See Release: in the sentence.",
        ]
        code, body, error = self.observe_text("\n".join(lines) + "\n")
        self.assertEqual(code, 1, error)
        assert_open(self, body)
        self.assertEqual(body["document"]["header_state_raw"], "state: draft")
        self.assertEqual(body["document"]["lines"], [{"line": 1, "text": "state: draft"}])
        self.assertFalse(body["document"]["ambiguous"])
        self.assertEqual(body["assignment"]["executor_raw"], "Executor: Actual Executor")
        self.assertEqual(body["assignment"]["executor_lines"], [{"line": 22, "text": "Executor: Actual Executor"}])
        self.assertIsNone(body["assignment"]["release_raw"])
        self.assertEqual(
            body["assignment"]["release_lines"],
            [
                {
                    "line": 23,
                    "text": "Release and claim: recorded in the Return pointer. This draft grants no release.",
                },
                {"line": 31, "text": "Release: actual release"},
            ],
        )
        self.assertEqual(body["assignment"]["claim_raw"], "Claim: actual claim")
        self.assertEqual(body["assignment"]["claim_lines"], [{"line": 32, "text": "Claim: actual claim"}])
        self.assertTrue(body["assignment"]["ambiguous"])
        self.assertIn("duplicate-release", body["ambiguities"])
        self.assertNotIn("duplicate-header-state", body["ambiguities"])
        self.assertNotIn("duplicate-claim", body["ambiguities"])
        joined = json.dumps(body["document"]) + json.dumps(body["assignment"])
        for stray in (
            "fenced-draft",
            "fenced release",
            "fenced claim",
            "quoted release",
            "notes release",
            "inner false",
            "still fenced",
            "Fenced Person",
        ):
            self.assertNotIn(stray, joined)
        self.assertEqual(body["fenced_headings"][0]["title"], "Return pointer")
        self.assertEqual(body["pointers"][0]["line"], 30)
        self.assertEqual(body["pointers"][0]["members"], [])
        self.assertIsNone(body["legacy"]["revision_id"])

    def test_duplicate_lines_stay_visible(self):
        text = "\n".join(
            [
                "state: draft",
                "state: draft",
                "## Assignment",
                "Executor: Same",
                "Executor: Same",
                "## Return",
                "Release: one",
                "Release: one",
                "Claim: one",
                "Claim: one",
            ]
        )
        code, body, error = self.observe_text(text + "\n")
        self.assertEqual(code, 1, error)
        self.assertIsNone(body["document"]["header_state_raw"])
        self.assertEqual(
            body["document"]["lines"],
            [{"line": 1, "text": "state: draft"}, {"line": 2, "text": "state: draft"}],
        )
        self.assertTrue(body["document"]["ambiguous"])
        self.assertIsNone(body["assignment"]["executor_raw"])
        self.assertIsNone(body["assignment"]["release_raw"])
        self.assertIsNone(body["assignment"]["claim_raw"])
        self.assertEqual([item["line"] for item in body["assignment"]["executor_lines"]], [4, 5])
        self.assertEqual([item["line"] for item in body["assignment"]["release_lines"]], [7, 8])
        self.assertEqual([item["line"] for item in body["assignment"]["claim_lines"]], [9, 10])
        for code_name in (
            "duplicate-header-state",
            "duplicate-executor",
            "duplicate-release",
            "duplicate-claim",
        ):
            self.assertIn(code_name, body["ambiguities"])

    def test_malformed_utf8_is_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "page.md"
            page.write_bytes(b"\xff\xfe state: draft\n## Return\nexecution: returned\n")
            code, body, error = run(
                [
                    "observe",
                    "--supplied",
                    str(page),
                    "--path",
                    "label/00.00.10.work/0508.return-capture/05.14.md",
                    "--json",
                ]
            )
        self.assertEqual(code, 1, error)
        assert_open(self, body)
        self.assertIn("not-utf-8", body["ambiguities"])
        self.assertEqual(body["legacy"]["status"], "unsupported")
        self.assertEqual(body["legacy"]["reason"], "not UTF-8")
        self.assertIsNone(body["legacy"]["revision_id"])
        self.assertIsNone(body["document"]["header_state_raw"])
        self.assertEqual(body["document"]["lines"], [])
        self.assertIsNone(body["assignment"]["executor_raw"])
        self.assertIsNone(body["assignment"]["release_raw"])
        self.assertIsNone(body["assignment"]["claim_raw"])
        self.assertNotIn("Traceback", error)


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
            self.assertEqual(body["source"]["time_basis"], "git-blob")
            self.assertIsNone(body["source"]["live_observed_at"])
            self.assertIsNone(body["source"]["observation_started_at"])
            self.assertIsNone(body["source"]["observation_finished_at"])
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
                    self.assertIsNone(item["observation_started_at"])
                    self.assertIsNone(item["observation_finished_at"])
                else:
                    self.assertEqual(item["inspection"]["status"], "complete", role["member"])
                    self.assertTrue(item["receipt_bytes_match"], role["member"])
                    self.assertEqual(item["inspection"]["capture"]["retrospective"], role["retrospective"])
                    self.assertRegex(item["observation_started_at"], Z_STAMP)
                    self.assertRegex(item["observation_finished_at"], Z_STAMP)
                    self.assertLessEqual(item["observation_started_at"], item["observation_finished_at"])
                    self.assertNotIn("observation_started_at", item["inspection"])
                    self.assertNotIn("observation_finished_at", item["inspection"])
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
            self.assertRegex(item["observation_started_at"], Z_STAMP)
            self.assertRegex(item["observation_finished_at"], Z_STAMP)
            self.assertNotIn("observation_started_at", item["inspection"])
            self.assertNotIn("observation_finished_at", item["inspection"])

    def test_reservation_fixture_leaves_the_sealed_member(self):
        member = BOOK / "0138.batch-reader-0513"
        before = tree_fingerprint(member)
        head = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            capture_output=True,
            check=True,
        ).stdout
        corpus_before = hashlib.sha256(CORPUS.read_bytes()).hexdigest()
        pins = (
            ("labs/prime-support-pass01/prime_support.py", batch_observe.PARSER_SHA, batch_observe.PARSER_BYTES),
            ("labs/prime-support-pass01/clerk_adapter.py", batch_observe.ADAPTER_SHA, batch_observe.ADAPTER_BYTES),
            ("labs/return-capture-pass01/return_inspect.py", batch_observe.INSPECT_SHA, batch_observe.INSPECT_BYTES),
            ("labs/return-capture-pass01/return_capture.py", batch_observe.HELPER_SHA, batch_observe.HELPER_BYTES),
        )
        for rel, digest, size in pins:
            data = (ROOT / rel).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), digest)
            self.assertEqual(len(data), size)
        with tempfile.TemporaryDirectory() as tmp:
            book = Path(tmp) / "book"
            book.mkdir()
            reserved_text = self.helper(
                [
                    "reserve",
                    "--book",
                    str(book),
                    "--submission",
                    "obs-0514-reserved",
                    "--name",
                    "reserved-0514",
                    "--origin-book",
                    "00.00.10.work",
                    "--origin-page",
                    "0508.return-capture",
                    "--origin-batch",
                    "05.14",
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
            reserved_dir = book / reserved
            self.assertEqual(sorted(path.name for path in reserved_dir.iterdir()), ["01.md", "reservation.json"])
            page = book / "page.md"
            page.write_bytes(
                f"## Return pointer\nMember: {reserved}\nReceipt: {'9' * 64}\n".encode("utf-8")
            )
            page_hash = hashlib.sha256(page.read_bytes()).hexdigest()
            code, body, error = run(
                [
                    "observe",
                    "--supplied",
                    str(page),
                    "--path",
                    "label/00.00.10.work/0508.return-capture/05.14.md",
                    "--members-book",
                    str(book),
                    "--json",
                ]
            )
            self.assertEqual(code, 1, error)
            assert_open(self, body)
            item = body["custody"]["observations"][0]
            self.assertEqual(item["member"], reserved)
            self.assertEqual(item["role"], "reserved")
            self.assertEqual(item["inspection"]["status"], "reserved")
            self.assertEqual(item["exit"], 1)
            self.assertRegex(item["observation_started_at"], Z_STAMP)
            self.assertNotIn("observation_started_at", item["inspection"])
            self.assertEqual(hashlib.sha256(page.read_bytes()).hexdigest(), page_hash)
            self.assertEqual(sorted(path.name for path in reserved_dir.iterdir()), ["01.md", "reservation.json"])
            if (member / "receipt.json").is_file():
                copy_book = Path(tmp) / "copy"
                dest = copy_book / member.name
                shutil.copytree(member, dest)
                copied = tree_fingerprint(dest)
                receipt = hashlib.sha256((dest / "receipt.json").read_bytes()).hexdigest()
                sealed_page = copy_book / "page.md"
                sealed_page.write_bytes(
                    (
                        "## Return pointer\n"
                        f"Member: {member.name}\n"
                        f"Receipt: {receipt}\n"
                    ).encode("utf-8")
                )
                code, sealed, error = run(
                    [
                        "observe",
                        "--supplied",
                        str(sealed_page),
                        "--path",
                        "label/00.00.10.work/0508.return-capture/05.13.md",
                        "--members-book",
                        str(copy_book),
                        "--json",
                    ]
                )
                self.assertEqual(code, 1, error)
                assert_open(self, sealed)
                observed = sealed["custody"]["observations"][0]
                self.assertEqual(observed["role"], "primary-current-candidate")
                self.assertEqual(sealed["custody"]["primary"], member.name)
                self.assertEqual(observed["inspection"]["status"], "complete")
                self.assertEqual(observed["inspection"]["capture"]["receipt_sha256"], receipt)
                self.assertEqual(observed["inspection"]["capture"]["retrospective"], False)
                self.assertRegex(observed["observation_started_at"], Z_STAMP)
                self.assertNotIn("observation_started_at", observed["inspection"])
                self.assertEqual(sealed["custody"]["package_at_commit"], "not-established")
                self.assertEqual(tree_fingerprint(dest), copied)
        self.assertEqual(tree_fingerprint(member), before)
        self.assertEqual(hashlib.sha256(CORPUS.read_bytes()).hexdigest(), corpus_before)
        head_after = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"],
            capture_output=True,
            check=True,
        ).stdout
        self.assertEqual(head_after, head)
        for rel, digest, size in pins:
            data = (ROOT / rel).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), digest)
            self.assertEqual(len(data), size)


if __name__ == "__main__":
    unittest.main()
