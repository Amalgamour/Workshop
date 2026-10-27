"""Read-only inspection tests. Disposable copies and members only."""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
HELPER = LAB / "return_capture.py"
INSPECT = LAB / "return_inspect.py"
CAPTURE_TESTS = LAB / "tests" / "test_return_capture.py"
PIN = "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac"
CAPTURE_TEST_PIN = "842547f798288af6b82baeedd2adf48d59c0723e3756dfecef8c4fcafc5bc2ba"
PY = sys.executable
DECISIONS = {"approved", "accepted", "published", "seated"}


def outside_git(path: Path) -> bool:
    current = path.resolve()
    while True:
        if (current / ".git").exists():
            return False
        if current.parent == current:
            return True
        current = current.parent


def git_env() -> dict[str, str]:
    env = os.environ.copy()
    for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_NAMESPACE", "GIT_PREFIX"):
        env.pop(key, None)
    env["GIT_AUTHOR_NAME"] = "Return Capture"
    env["GIT_AUTHOR_EMAIL"] = "return-capture@example.invalid"
    env["GIT_COMMITTER_NAME"] = "Return Capture"
    env["GIT_COMMITTER_EMAIL"] = "return-capture@example.invalid"
    env["GIT_AUTHOR_DATE"] = "2026-10-27T12:00:00+00:00"
    env["GIT_COMMITTER_DATE"] = "2026-10-27T12:00:00+00:00"
    return env


def run_git(repo: Path, args: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        ["git", *args],
        cwd=repo,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise AssertionError(f"git {' '.join(args)}\n{proc.stderr}\n{proc.stdout}")
    return proc


def git_metadata_dir(repo: Path) -> Path:
    marker = repo / ".git"
    if marker.is_file():
        text = marker.read_text(encoding="utf-8")
        gitdir = Path(text.split(":", 1)[1].strip())
        if not gitdir.is_absolute():
            gitdir = (repo / gitdir).resolve()
        return gitdir
    return marker


def snapshot_git_control(gitdir: Path) -> dict[str, bytes]:
    found: dict[str, bytes] = {}
    for name in ("HEAD", "index", "config"):
        path = gitdir / name
        if path.is_file() and not path.is_symlink():
            found[name] = path.read_bytes()
    refs = gitdir / "refs"
    if refs.is_dir():
        for dirpath, _dirnames, filenames in os.walk(refs):
            for filename in filenames:
                path = Path(dirpath) / filename
                if path.is_symlink():
                    continue
                found[path.relative_to(gitdir).as_posix()] = path.read_bytes()
    packed = gitdir / "packed-refs"
    if packed.is_file() and not packed.is_symlink():
        found["packed-refs"] = packed.read_bytes()
    return found


def snap_bytes(root: Path) -> dict[str, bytes]:
    found = {}
    if not root.exists():
        return found
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            path = Path(dirpath) / name
            if path.is_symlink():
                continue
            found[path.relative_to(root).as_posix()] = path.read_bytes()
    return found


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def keys_of(value):
    if isinstance(value, dict):
        for key, item in value.items():
            yield key
            yield from keys_of(item)
    elif isinstance(value, list):
        for item in value:
            yield from keys_of(item)


class InspectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.helper_bytes = HELPER.read_bytes()
        cls.capture_test_bytes = CAPTURE_TESTS.read_bytes()
        if hashlib.sha256(cls.helper_bytes).hexdigest() != PIN:
            raise AssertionError("helper pin drifted before the inspection suite")
        if hashlib.sha256(cls.capture_test_bytes).hexdigest() != CAPTURE_TEST_PIN:
            raise AssertionError("capture tests drifted before the inspection suite")

    @classmethod
    def tearDownClass(cls) -> None:
        if HELPER.read_bytes() != cls.helper_bytes:
            raise AssertionError("inspection suite changed return_capture.py")
        if CAPTURE_TESTS.read_bytes() != cls.capture_test_bytes:
            raise AssertionError("inspection suite changed test_return_capture.py")

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="rc-inspect-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.assertTrue(outside_git(self.tmp), self.tmp)
        self.lab = self.tmp / "lab"
        self.lab.mkdir()
        shutil.copyfile(HELPER, self.lab / "return_capture.py")
        shutil.copyfile(INSPECT, self.lab / "return_inspect.py")
        self.helper = load_module(self.lab / "return_capture.py", f"helper_{id(self)}")
        self.book = self.tmp / "book"
        self.book.mkdir()
        self.source = self.tmp / "source"
        self.source.mkdir()
        (self.source / "note.txt").write_bytes(b"note\n")
        self.return_file = self.tmp / "return.md"
        self.return_file.write_bytes(b"Did.\n")

    def reserve(self, **over):
        fields = {
            "book": str(self.book),
            "submission": "sub-1",
            "name": "alpha",
            "origin_book": "0508.return-capture",
            "origin_page": "05.04.md",
            "origin_batch": "05.04",
            "expected_outputs": ["note.txt"],
            "submitter": "Grok Builder 2",
            "reviewer": "Codex Prime",
            "release": "Director 2026-10-27",
        }
        fields.update(over)
        return self.helper.reserve(**fields)

    def capture(self, **over):
        fields = {
            "book": str(self.book),
            "submission": "sub-1",
            "return_file": str(self.return_file),
            "source_root": str(self.source),
            "artifacts": ["note.txt|note.txt"],
        }
        fields.update(over)
        return self.helper.capture(**fields)

    def seal(self) -> Path:
        reserved = self.reserve()
        self.assertEqual(reserved.code, 0, reserved.text)
        captured = self.capture()
        self.assertEqual(captured.code, 0, captured.text)
        return self.book / "0101.alpha"

    def run_inspect(self, member: str, book: Path | None = None) -> subprocess.CompletedProcess[bytes]:
        return subprocess.run(
            [
                PY,
                "-B",
                str(self.lab / "return_inspect.py"),
                "inspect",
                "--book",
                str(book or self.book),
                "--member",
                member,
                "--json",
            ],
            capture_output=True,
        )

    def observation(self, member: str, book: Path | None = None) -> tuple[dict, subprocess.CompletedProcess[bytes]]:
        proc = self.run_inspect(member, book)
        self.assertEqual(proc.stderr, b"", proc.stderr)
        self.assertNotIn(b"Traceback", proc.stdout)
        observed = json.loads(proc.stdout.decode("utf-8"))
        self.assertTrue(proc.stdout.endswith(b"\n"))
        self.assertEqual(proc.stdout, self.helper.canonical(observed))
        self.assertTrue(DECISIONS.isdisjoint(set(keys_of(observed))))
        return observed, proc

    def test_pin_gate_and_inspector_imports(self) -> None:
        tree = ast.parse(INSPECT.read_text(encoding="utf-8"))
        banned = {"subprocess", "shutil", "sqlite3"}
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name.split(".")[0])
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertTrue(banned.isdisjoint(imported))
        source = INSPECT.read_text(encoding="utf-8")
        self.assertNotIn("os.remove", source)
        self.assertNotIn("result complete", source)
        self.assertIn(PIN, source)
        self.assertEqual(hashlib.sha256(HELPER.read_bytes()).hexdigest(), PIN)

    def test_complete_agrees_with_public_verify_and_changes_nothing(self) -> None:
        member = self.seal()
        before = snap_bytes(self.book)
        source_before = self.return_file.read_bytes()
        note_before = (self.source / "note.txt").read_bytes()
        helper_before = (self.lab / "return_capture.py").read_bytes()
        observed, proc = self.observation("0101.alpha")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(observed["status"], "complete")
        self.assertEqual(observed["problems"], [])
        self.assertEqual(observed["member"], "0101.alpha")
        self.assertEqual(observed["book"], str(Path(os.path.abspath(self.book))))
        info = self.helper.verify_member(member)
        verified = self.helper.verify(str(self.book), "0101.alpha")
        self.assertEqual(verified.code, 0)
        capture = observed["capture"]
        self.assertEqual(capture["receipt_sha256"], info["receipt_sha256"])
        self.assertEqual(capture["manifest_sha256"], info["manifest_sha256"])
        self.assertEqual(capture["reservation_sha256"], info["reservation_sha256"])
        self.assertEqual(capture["return"]["sha256"], info["manifest"]["return"]["sha256"])
        self.assertEqual(capture["return"]["bytes"], 5)
        self.assertIs(capture["return"]["includes_prime_review"], False)
        self.assertEqual(capture["payloads"][0]["sha256"], info["payloads"][0][1])
        self.assertEqual(capture["payloads"][0]["bytes"], 5)
        self.assertEqual(observed["reservation"]["submission_id"], "sub-1")
        self.assertEqual(observed["reservation"]["reservation_sha256"], info["reservation_sha256"])
        self.assertEqual(snap_bytes(self.book), before)
        self.assertEqual(self.return_file.read_bytes(), source_before)
        self.assertEqual((self.source / "note.txt").read_bytes(), note_before)
        self.assertEqual((self.lab / "return_capture.py").read_bytes(), helper_before)
        again, second = self.observation("0101.alpha")
        self.assertEqual(second.returncode, 0)
        self.assertEqual(again, observed)
        self.assertEqual(snap_bytes(self.book), before)

    def test_reserved_missing_and_empty_are_not_complete(self) -> None:
        reserved = self.reserve()
        self.assertEqual(reserved.code, 0, reserved.text)
        before = snap_bytes(self.book)
        observed, proc = self.observation("0101.alpha")
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(observed["status"], "reserved")
        self.assertEqual(observed["problems"], ["reservation only"])
        self.assertIsNone(observed["capture"])
        self.assertEqual(observed["reservation"]["submission_id"], "sub-1")
        self.assertEqual(observed["reservation"]["origin"]["batch"], "05.04")
        self.assertEqual(self.helper.verify(str(self.book), "0101.alpha").code, 2)
        self.assertEqual(snap_bytes(self.book), before)
        missing, missing_proc = self.observation("0102.absent")
        self.assertEqual(missing_proc.returncode, 1)
        self.assertEqual(missing["status"], "missing")
        self.assertEqual(missing["problems"], ["member is absent"])
        self.assertIsNone(missing["reservation"])
        self.assertIsNone(missing["capture"])
        self.assertEqual(self.helper.verify(str(self.book), "0102.absent").code, 2)
        (self.book / "0103.empty").mkdir()
        empty, empty_proc = self.observation("0103.empty")
        self.assertEqual(empty_proc.returncode, 1)
        self.assertEqual(empty["status"], "missing")
        self.assertEqual(empty["problems"], ["empty member"])
        self.assertIsNone(empty["capture"])
        kept = {key: value for key, value in before.items() if key.startswith("0101.alpha/")}
        self.assertEqual(snap_bytes(self.book / "0101.alpha"), {key.split("/", 1)[1]: value for key, value in kept.items()})
        self.assertFalse((self.book / "0102.absent").exists())

    def test_partial_before_receipt(self) -> None:
        self.reserve()
        stopped = self.capture(interrupt="before-receipt")
        self.assertEqual(stopped.code, 2, stopped.text)
        member = self.book / "0101.alpha"
        before = snap_bytes(member)
        observed, proc = self.observation("0101.alpha")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(observed["status"], "incomplete")
        self.assertIn("missing receipt.json", observed["problems"])
        self.assertIsNone(observed["capture"])
        self.assertEqual(observed["reservation"]["submission_id"], "sub-1")
        self.assertEqual(self.helper.verify(str(self.book), "0101.alpha").code, 2)
        self.assertEqual(snap_bytes(member), before)
        self.assertFalse((member / "receipt.json").exists())

    def test_mutations_keep_capture_null(self) -> None:
        cases = (
            ("return.md", b"Did.\nX", "hash mismatch return"),
            ("payload/0001.blob", b"note\nX", "hash mismatch payload/0001.blob"),
            ("receipt.json", b"{", "invalid JSON"),
        )
        for rel, data, text in cases:
            with self.subTest(rel=rel):
                member = self.seal()
                target = member / rel
                target.write_bytes(data)
                before = snap_bytes(member)
                observed, proc = self.observation("0101.alpha")
                self.assertEqual(proc.returncode, 2)
                self.assertEqual(observed["status"], "incomplete")
                self.assertTrue(any(text in item for item in observed["problems"]), observed["problems"])
                self.assertIsNone(observed["capture"])
                self.assertEqual(self.helper.verify(str(self.book), "0101.alpha").code, 2)
                self.assertEqual(snap_bytes(member), before)
                shutil.rmtree(member)
        member = self.seal()
        manifest = json.loads((member / "manifest.json").read_text(encoding="utf-8"))
        manifest["return"]["sha256"] = "0" * 64
        (member / "manifest.json").write_bytes(self.helper.canonical(manifest))
        observed, proc = self.observation("0101.alpha")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(observed["status"], "incomplete")
        self.assertIn("hash mismatch return", observed["problems"])
        self.assertIsNone(observed["capture"])
        shutil.rmtree(member)
        member = self.seal()
        (member / "reservation.json").write_bytes(b'{"schema":"return-capture/1","schema":"other"}\n')
        observed, proc = self.observation("0101.alpha")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(observed["status"], "incomplete")
        self.assertIn("duplicate JSON key", observed["problems"])
        self.assertIsNone(observed["reservation"])
        self.assertIsNone(observed["capture"])
        self.assertEqual(self.helper.verify(str(self.book), "0101.alpha").code, 2)

    def test_wrong_helper_hash_does_not_execute(self) -> None:
        marker = self.tmp / "executed.txt"
        bomb = (
            "from pathlib import Path\n"
            f"Path({str(marker)!r}).write_text('executed', encoding='utf-8')\n"
        )
        (self.lab / "return_capture.py").write_text(bomb, encoding="utf-8")
        observed, proc = self.observation("0101.alpha")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(observed["status"], "refused")
        self.assertTrue(observed["problems"][0].startswith("helper hash mismatch:"))
        self.assertIn(PIN, observed["problems"][0])
        self.assertIsNone(observed["capture"])
        self.assertFalse(marker.exists())

    def test_path_escape_and_unreadable_member(self) -> None:
        canary = self.tmp / "secret.txt"
        canary.write_bytes(b"secret")
        before = canary.read_bytes()
        for name in ("../secret.txt", "..\\secret.txt", str(canary), "0101.alpha/../0102.other"):
            with self.subTest(name=name):
                observed, proc = self.observation(name)
                self.assertEqual(proc.returncode, 2)
                self.assertEqual(observed["status"], "refused")
                self.assertEqual(observed["problems"], ["member path is not a return member"])
                self.assertIsNone(observed["capture"])
                self.assertEqual(canary.read_bytes(), before)
                self.assertFalse((self.tmp / "secret.txt.md").exists())
        relative = subprocess.run(
            [
                PY,
                "-B",
                str(self.lab / "return_inspect.py"),
                "inspect",
                "--book",
                "book",
                "--member",
                "0101.alpha",
                "--json",
            ],
            capture_output=True,
        )
        self.assertEqual(relative.returncode, 2)
        self.assertEqual(relative.stderr, b"")
        body = json.loads(relative.stdout.decode("utf-8"))
        self.assertEqual(body["status"], "refused")
        self.assertIn("absolute", body["problems"][0])

    def test_symlink_member_is_refused_or_skipped(self) -> None:
        linked_target = self.book / "0101.alpha"
        linked_target.mkdir()
        link = self.book / "0102.link"
        try:
            os.symlink(linked_target, link, target_is_directory=True)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                self.skipTest(f"symlink privilege: {exc}")
            raise
        before = snap_bytes(self.book)
        observed, proc = self.observation("0102.link")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(observed["status"], "refused")
        self.assertEqual(observed["problems"], ["member is link"])
        self.assertIsNone(observed["capture"])
        self.assertEqual(snap_bytes(self.book), before)

    def test_hard_linked_payload_is_incomplete(self) -> None:
        member = self.seal()
        payload = member / "payload" / "0001.blob"
        outside = self.tmp / "hard.txt"
        os.link(payload, outside)
        self.assertGreater(payload.stat().st_nlink, 1)
        before = snap_bytes(member)
        observed, proc = self.observation("0101.alpha")
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(observed["status"], "incomplete")
        self.assertTrue(any("payload/0001.blob" in item for item in observed["problems"]))
        self.assertIsNone(observed["capture"])
        self.assertEqual(self.helper.verify(str(self.book), "0101.alpha").code, 2)
        self.assertEqual(snap_bytes(member), before)
        self.assertEqual(outside.read_bytes(), b"note\n")
        self.assertGreater(payload.stat().st_nlink, 1)

    def test_git_backed_book_is_unchanged(self) -> None:
        env = git_env()
        repo = self.tmp / "repo"
        repo.mkdir()
        run_git(repo, ["init", "-b", "workshop"], env)
        run_git(repo, ["config", "core.autocrlf", "false"], env)
        run_git(repo, ["config", "user.email", "return-capture@example.invalid"], env)
        run_git(repo, ["config", "user.name", "Return Capture"], env)
        (repo / ".gitattributes").write_bytes(b"* -text\n")
        (repo / "README.md").write_bytes(b"origin\n")
        run_git(repo, ["add", "--", ".gitattributes", "README.md"], env)
        run_git(repo, ["commit", "-m", "origin"], env)
        self.inspect_checkout(repo, env)
        worktree = self.tmp / "wt"
        run_git(repo, ["worktree", "add", "--detach", str(worktree), "HEAD"], env)
        self.assertTrue((worktree / ".git").is_file())
        self.inspect_checkout(worktree, env)

    def inspect_checkout(self, repo: Path, env: dict[str, str]) -> None:
        book = repo / "work"
        book.mkdir()
        source = repo / "source"
        source.mkdir()
        (source / "note.txt").write_bytes(b"note\n")
        return_file = repo / "return.md"
        return_file.write_bytes(b"Did.\n")
        reserved = self.helper.reserve(
            str(book),
            "git-sub",
            "local",
            "0508.return-capture",
            "05.04.md",
            "05.04",
            ["note.txt"],
            "Grok Builder 2",
            "Codex Prime",
            "Director 2026-10-27",
        )
        self.assertEqual(reserved.code, 0, reserved.text)
        captured = self.helper.capture(
            str(book),
            "git-sub",
            str(return_file),
            str(source),
            ["note.txt|note.txt"],
        )
        self.assertEqual(captured.code, 0, captured.text)
        gitdir = git_metadata_dir(repo)
        common = gitdir
        commondir = gitdir / "commondir"
        if commondir.is_file():
            raw = commondir.read_text(encoding="utf-8").strip()
            common = Path(raw)
            if not common.is_absolute():
                common = (gitdir / common).resolve()
        before_control = {
            "gitdir": snapshot_git_control(gitdir),
            "common": snapshot_git_control(common),
        }
        before_member = snap_bytes(book / "0101.local")
        head = run_git(repo, ["rev-parse", "HEAD"], env).stdout
        observed, proc = self.observation("0101.local", book)
        self.assertEqual(proc.returncode, 0, observed)
        self.assertEqual(observed["status"], "complete")
        self.assertEqual(observed["capture"]["receipt_sha256"], self.helper.verify_member(book / "0101.local")["receipt_sha256"])
        self.assertEqual(snapshot_git_control(gitdir), before_control["gitdir"])
        self.assertEqual(snapshot_git_control(common), before_control["common"])
        self.assertEqual(run_git(repo, ["rev-parse", "HEAD"], env).stdout, head)
        self.assertEqual(snap_bytes(book / "0101.local"), before_member)
        self.assertEqual(return_file.read_bytes(), b"Did.\n")

    def test_cli_syntax_uses_stderr(self) -> None:
        proc = subprocess.run(
            [PY, "-B", str(self.lab / "return_inspect.py"), "inspect", "--book", str(self.book)],
            capture_output=True,
        )
        self.assertEqual(proc.returncode, 2)
        self.assertTrue(proc.stderr.strip())
        self.assertNotIn(b"Traceback", proc.stderr)
        self.assertEqual(proc.stdout, b"")

    def test_fresh_process_complete_and_missing(self) -> None:
        self.seal()
        complete, complete_proc = self.observation("0101.alpha")
        self.assertEqual(complete_proc.returncode, 0)
        self.assertEqual(complete["status"], "complete")
        missing, missing_proc = self.observation("0199.missing")
        self.assertEqual(missing_proc.returncode, 1)
        self.assertEqual(missing["status"], "missing")
        self.assertIsNone(missing["capture"])


if __name__ == "__main__":
    unittest.main()
