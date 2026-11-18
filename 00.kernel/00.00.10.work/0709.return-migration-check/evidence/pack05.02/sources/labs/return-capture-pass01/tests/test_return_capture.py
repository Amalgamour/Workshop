"""Isolated tests for return-capture/1. Disposable books only."""

from __future__ import annotations

import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
import return_capture as rc  # noqa: E402

SCRIPT = LAB / "return_capture.py"
PY = sys.executable
PIN = "e6d6eb75538732c7eedbc840042242d386b25c2f"


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
        if not text.startswith("gitdir:"):
            raise AssertionError(text)
        gitdir = Path(text.split(":", 1)[1].strip())
        if not gitdir.is_absolute():
            gitdir = (repo / gitdir).resolve()
        return gitdir
    if marker.is_dir():
        return marker
    raise AssertionError(f"missing git metadata: {repo}")


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


def init_checkout(path: Path, env: dict[str, str]) -> None:
    path.mkdir(parents=True)
    run_git(path, ["init", "-b", "workshop"], env)
    run_git(path, ["config", "core.autocrlf", "false"], env)
    run_git(path, ["config", "user.email", "return-capture@example.invalid"], env)
    run_git(path, ["config", "user.name", "Return Capture"], env)


def snap_bytes(root: Path) -> dict[str, bytes]:
    found = {}
    if not root.exists():
        return found
    for dirpath, _dirnames, filenames in os.walk(root):
        for name in filenames:
            path = Path(dirpath) / name
            if path.is_symlink():
                continue
            rel = path.relative_to(root).as_posix()
            found[rel] = path.read_bytes()
    return found


class ReturnCaptureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="rc-pass01-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.assertTrue(outside_git(self.tmp), self.tmp)
        self.book = self.tmp / "book"
        self.book.mkdir()
        self.source = self.tmp / "source"
        self.source.mkdir()
        self.return_file = self.tmp / "return.md"

    def write_return(self, data: bytes = b"Did.\n") -> None:
        self.return_file.write_bytes(data)

    def reserve(self, **over):
        fields = {
            "book": str(self.book),
            "submission": "sub-1",
            "name": "alpha",
            "origin_book": "0504.app-entry",
            "origin_page": "05.06.md",
            "origin_batch": "05.06",
            "expected_outputs": ["note.txt"],
            "submitter": "Builder 2",
            "reviewer": "Codex Prime",
            "release": "Director 2026-10-27",
        }
        fields.update(over)
        return rc.reserve(**fields)

    def capture(self, **over):
        fields = {
            "book": str(self.book),
            "submission": "sub-1",
            "return_file": str(self.return_file),
            "source_root": str(self.source),
            "artifacts": ["note.txt|note.txt"],
        }
        fields.update(over)
        return rc.capture(**fields)

    def test_tool_imports_no_process_copy_or_database(self) -> None:
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        banned = {"subprocess", "shutil", "sqlite3"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.assertNotIn(alias.name.split(".")[0], banned)
            if isinstance(node, ast.ImportFrom) and node.module:
                self.assertNotIn(node.module.split(".")[0], banned)
        self.assertEqual(SCRIPT.read_text(encoding="utf-8").count("os.remove"), 1)

    def test_lowest_free_skips_draft_directory_and_temp_file(self) -> None:
        (self.book / "0101.draft").mkdir()
        (self.book / "0102.tmp").write_bytes(b"temp")
        before = snap_bytes(self.book)
        result = self.reserve()
        self.assertEqual(result.code, 0, result.text)
        self.assertIn("member 0103.alpha", result.text)
        self.assertIn("result reserved", result.text)
        self.assertTrue((self.book / "0103.alpha" / "reservation.json").is_file())
        self.assertEqual((self.book / "0101.draft").is_dir(), True)
        self.assertEqual((self.book / "0102.tmp").read_bytes(), b"temp")
        self.assertFalse((self.book / "0100.band.returns" / ".allocation.lock").exists())
        after = snap_bytes(self.book / "0101.draft")
        self.assertEqual(after, {})
        self.assertEqual(before["0102.tmp"], b"temp")

    def test_idempotent_reserve_writes_nothing_and_conflict_keeps_bytes(self) -> None:
        first = self.reserve()
        self.assertIn("result reserved", first.text)
        before = snap_bytes(self.book)
        second = self.reserve()
        self.assertEqual(second.code, 0, second.text)
        self.assertIn("result already-reserved", second.text)
        self.assertEqual(snap_bytes(self.book), before)
        self.assertFalse((self.book / "0102.alpha").exists())
        conflict = self.reserve(release="a different release")
        self.assertEqual(conflict.code, 2, conflict.text)
        self.assertIn("conflict submission sub-1", conflict.text)
        self.assertIn("existing 0101.alpha", conflict.text)
        self.assertEqual(snap_bytes(self.book), before)

    def test_concurrent_reserves_one_member_per_submission(self) -> None:
        barrier = threading.Barrier(2)
        results = []

        def work(submission: str, name: str) -> None:
            barrier.wait()
            results.append(self.reserve(submission=submission, name=name, expected_outputs=[]))

        threads = [
            threading.Thread(target=work, args=("sub-a", "alpha")),
            threading.Thread(target=work, args=("sub-b", "beta")),
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(sorted(item.code for item in results), [0, 0])
        names = sorted(path.name for path in self.book.iterdir() if rc.slot_number(path.name))
        self.assertEqual({name[:4] for name in names}, {"0101", "0102"})
        self.assertEqual({name.split(".", 1)[1] for name in names}, {"alpha", "beta"})

    def test_concurrent_same_submission_allocates_once(self) -> None:
        barrier = threading.Barrier(2)
        results = []

        def work() -> None:
            barrier.wait()
            results.append(self.reserve(expected_outputs=[]))

        threads = [threading.Thread(target=work) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        texts = sorted(item.text for item in results)
        self.assertTrue(any("result reserved" in text for text in texts), texts)
        self.assertTrue(any("result already-reserved" in text for text in texts), texts)
        self.assertTrue(all(item.code == 0 for item in results))
        members = sorted(path.name for path in self.book.iterdir() if rc.slot_number(path.name))
        self.assertEqual(members, ["0101.alpha"])

    def test_full_band_stops_without_0200(self) -> None:
        for number in range(101, 200):
            (self.book / f"{number:04d}.hold").mkdir()
        before = {path.name for path in self.book.iterdir()}
        result = self.reserve()
        self.assertEqual(result.code, 2, result.text)
        self.assertIn("return band is full", result.text)
        after = {path.name for path in self.book.iterdir()}
        self.assertEqual(after - before, {"0100.band.returns"})
        self.assertFalse(any(name.startswith("0200") for name in after))
        self.assertFalse((self.book / "0100.band.returns" / ".allocation.lock").exists())

    def test_clean_capture_and_fresh_process_verify(self) -> None:
        self.write_return(b"Did. The return stands.\n")
        (self.source / "note.txt").write_bytes(b"note-a\n")
        reserved = self.reserve()
        self.assertEqual(reserved.code, 0, reserved.text)
        index_before = (self.book / "0101.alpha" / "01.md").read_bytes()
        captured = self.capture()
        self.assertEqual(captured.code, 0, captured.text)
        self.assertIn("result captured", captured.text)
        self.assertEqual((self.book / "0101.alpha" / "01.md").read_bytes(), index_before)
        member = self.book / "0101.alpha"
        manifest = json.loads((member / "manifest.json").read_text(encoding="utf-8"))
        receipt = json.loads((member / "receipt.json").read_text(encoding="utf-8"))
        reservation = json.loads((member / "reservation.json").read_text(encoding="utf-8"))
        self.assertEqual(
            set(reservation),
            {
                "schema",
                "kind",
                "submission_id",
                "origin",
                "destination",
                "expected_outputs",
                "submitter",
                "reviewer",
                "release",
                "supersedes",
                "reserved_at",
            },
        )
        self.assertEqual(set(manifest), {
            "schema", "kind", "submission_id", "reservation_sha256", "return",
            "retrospective", "source_commit", "captured_at", "sources", "omitted", "required",
        })
        self.assertNotIn("manifest_sha256", manifest)
        self.assertEqual(manifest["omitted"], [])
        self.assertEqual(manifest["required"], ["note.txt"])
        self.assertIsNone(manifest["source_commit"])
        self.assertFalse(manifest["retrospective"])
        self.assertEqual(set(receipt), {
            "schema", "kind", "submission_id", "reservation_sha256",
            "manifest_sha256", "captured_at",
        })
        self.assertEqual(receipt["kind"], "receipt")
        self.assertEqual(reservation["destination"]["path"], "0101.alpha")
        self.assertEqual((member / "payload" / "0001.blob").read_bytes(), b"note-a\n")
        proc = subprocess.run(
            [PY, "-B", str(SCRIPT), "verify", "--book", str(self.book), "--member", "0101.alpha"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("result complete", proc.stdout)
        self.assertIn("not approved", proc.stdout)
        self.assertIn("not accepted", proc.stdout)
        self.assertIn("not published", proc.stdout)
        self.assertIn("payload 0001.blob ", proc.stdout)

    def test_identical_retry_writes_nothing(self) -> None:
        self.write_return(b"same\n")
        (self.source / "note.txt").write_bytes(b"same-note")
        self.reserve()
        first = self.capture()
        self.assertIn("result captured", first.text)
        before = snap_bytes(self.book)
        second = self.capture()
        self.assertEqual(second.code, 0, second.text)
        self.assertIn("result already-captured", second.text)
        self.assertEqual(snap_bytes(self.book), before)

    def test_changed_bytes_or_flags_conflict_and_keep_package(self) -> None:
        self.write_return(b"original")
        (self.source / "note.txt").write_bytes(b"payload")
        self.reserve()
        self.capture()
        before = snap_bytes(self.book)
        self.write_return(b"changed")
        changed = self.capture()
        self.assertEqual(changed.code, 2, changed.text)
        self.assertIn("conflict submission sub-1", changed.text)
        self.assertEqual(snap_bytes(self.book), before)
        self.write_return(b"original")
        (self.source / "note.txt").write_bytes(b"other")
        payload = self.capture()
        self.assertEqual(payload.code, 2, payload.text)
        self.assertEqual(snap_bytes(self.book), before)
        (self.source / "note.txt").write_bytes(b"payload")
        flagged = self.capture(
            retrospective=True,
            source_commit=PIN,
            return_includes_prime_review=True,
        )
        self.assertEqual(flagged.code, 2, flagged.text)
        self.assertIn("conflict submission sub-1", flagged.text)
        self.assertEqual(snap_bytes(self.book), before)

    def test_missing_required_file_creates_no_capture(self) -> None:
        self.write_return(b"Did.\n")
        self.reserve()
        before = snap_bytes(self.book)
        result = self.capture()
        self.assertEqual(result.code, 2, result.text)
        self.assertIn("missing note.txt", result.text)
        self.assertEqual(snap_bytes(self.book), before)
        self.assertFalse((self.book / "0101.alpha" / "return.md").exists())

    def test_bytes_changed_during_read_writes_nothing(self) -> None:
        self.write_return(b"stable")
        (self.source / "note.txt").write_bytes(b"note")
        self.reserve()
        before = snap_bytes(self.book)
        original = Path.read_bytes
        state = {"n": 0}

        def patched(path: Path) -> bytes:
            data = original(path)
            state["n"] += 1
            if state["n"] == 2:
                return data + b"X"
            return data

        Path.read_bytes = patched
        try:
            result = self.capture()
        finally:
            Path.read_bytes = original
        self.assertEqual(result.code, 2, result.text)
        self.assertIn("bytes changed before capture", result.text)
        self.assertEqual(snap_bytes(self.book), before)

    def test_interrupt_before_write_and_partial_retry(self) -> None:
        self.write_return(b"body")
        (self.source / "note.txt").write_bytes(b"note")
        self.reserve()
        before = snap_bytes(self.book)
        stopped = self.capture(interrupt="before-write")
        self.assertEqual(stopped.code, 2, stopped.text)
        self.assertEqual(snap_bytes(self.book), before)
        after_return = self.capture(interrupt="after-return")
        self.assertEqual(after_return.code, 2, after_return.text)
        self.assertIn("retained return.md", after_return.text)
        self.assertTrue((self.book / "0101.alpha" / "return.md").is_file())
        self.assertFalse((self.book / "0101.alpha" / "payload").exists())
        self.assertFalse((self.book / "0101.alpha" / "receipt.json").exists())
        kept = snap_bytes(self.book)
        retry = self.capture()
        self.assertEqual(retry.code, 2, retry.text)
        self.assertIn("partial 0101.alpha", retry.text)
        self.assertIn("retained return.md", retry.text)
        self.assertEqual(snap_bytes(self.book), kept)

    def test_interrupt_before_receipt_stays_partial(self) -> None:
        self.write_return(b"body")
        (self.source / "note.txt").write_bytes(b"note")
        self.reserve()
        stopped = self.capture(interrupt="before-receipt")
        self.assertEqual(stopped.code, 2, stopped.text)
        member = self.book / "0101.alpha"
        self.assertTrue((member / "manifest.json").is_file())
        self.assertTrue((member / "payload" / "0001.blob").is_file())
        self.assertFalse((member / "receipt.json").exists())
        before = snap_bytes(member)
        retry = self.capture()
        self.assertIn("retained manifest.json", retry.text)
        self.assertIn("retained payload/0001.blob", retry.text)
        self.assertEqual(snap_bytes(member), before)
        proc = subprocess.run(
            [PY, "-B", str(SCRIPT), "verify", "--book", str(self.book), "--member", "0101.alpha"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(proc.returncode, 2)
        self.assertNotIn("result complete", proc.stdout)

    def test_corrupt_manifest_receipt_and_duplicate_key(self) -> None:
        self.write_return(b"body")
        (self.source / "note.txt").write_bytes(b"note")
        self.reserve()
        self.capture()
        member = self.book / "0101.alpha"
        receipt = member / "receipt.json"
        receipt.write_bytes(b"{")
        broken = rc.verify(str(self.book), "0101.alpha")
        self.assertEqual(broken.code, 2, broken.text)
        self.assertIn("invalid JSON", broken.text)
        self.capture()
        self.assertEqual(receipt.read_bytes(), b"{")
        manifest = json.loads((member / "manifest.json").read_text(encoding="utf-8"))
        manifest["return"]["bytes"] = "12"
        (member / "manifest.json").write_bytes(rc.canonical(manifest))
        typed = rc.verify(str(self.book), "0101.alpha")
        self.assertEqual(typed.code, 2, typed.text)
        self.assertIn("not an integer", typed.text)
        (member / "manifest.json").write_bytes(
            b'{"schema":"return-capture/1","schema":"other"}\n'
        )
        duplicate = rc.verify(str(self.book), "0101.alpha")
        self.assertEqual(duplicate.code, 2, duplicate.text)
        self.assertIn("duplicate JSON key", duplicate.text)

    def test_traversal_links_and_crlf(self) -> None:
        self.write_return(b"a\r\n")
        (self.source / "note.txt").write_bytes(b"a\r\n")
        outside = self.tmp / "outside.txt"
        outside.write_bytes(b"secret")
        self.reserve()
        before = snap_bytes(self.book)
        escaped = self.capture(artifacts=["../outside.txt|note.txt"])
        self.assertEqual(escaped.code, 2, escaped.text)
        self.assertEqual(snap_bytes(self.book), before)
        absolute = self.capture(artifacts=[str(outside) + "|note.txt"])
        self.assertEqual(absolute.code, 2, absolute.text)
        self.assertEqual(snap_bytes(self.book), before)
        duplicated = self.capture(artifacts=["note.txt|note.txt", "note.txt|note.txt"])
        self.assertEqual(duplicated.code, 2, duplicated.text)
        self.assertIn("duplicate", duplicated.text)
        self.assertEqual(snap_bytes(self.book), before)
        target = self.source / "hard.txt"
        target.write_bytes(b"a\r\n")
        linked = self.source / "linked.txt"
        os.link(target, linked)
        self.assertGreater(linked.stat().st_nlink, 1)
        hard = self.capture(artifacts=["linked.txt|note.txt"])
        self.assertEqual(hard.code, 2, hard.text)
        self.assertIn("link-count", hard.text)
        self.assertEqual(snap_bytes(self.book), before)
        captured = self.capture()
        self.assertEqual(captured.code, 0, captured.text)
        self.assertEqual((self.book / "0101.alpha" / "return.md").read_bytes(), b"a\r\n")
        self.assertEqual(
            (self.book / "0101.alpha" / "payload" / "0001.blob").read_bytes(),
            b"a\r\n",
        )

    def test_symlink_source_refused_or_skipped(self) -> None:
        self.write_return(b"a\r\n")
        (self.source / "note.txt").write_bytes(b"a\r\n")
        link = self.source / "note.link"
        try:
            os.symlink(self.source / "note.txt", link)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                self.skipTest(f"symlink privilege: {exc}")
            raise
        self.reserve()
        before = snap_bytes(self.book)
        result = self.capture(artifacts=["note.link|note.txt"])
        self.assertEqual(result.code, 2, result.text)
        self.assertIn("link", result.text)
        self.assertEqual(snap_bytes(self.book), before)

    def test_supersedes_leaves_the_old_member_unchanged(self) -> None:
        self.reserve(submission="sub-old", name="older", expected_outputs=[])
        before = snap_bytes(self.book / "0101.older")
        missing = self.reserve(submission="sub-new", name="newer", supersedes="0199.missing", expected_outputs=[])
        self.assertEqual(missing.code, 2, missing.text)
        self.assertFalse((self.book / "0102.newer").exists())
        result = self.reserve(
            submission="sub-new",
            name="newer",
            supersedes="0101.older",
            expected_outputs=[],
        )
        self.assertEqual(result.code, 0, result.text)
        self.assertIn("member 0102.newer", result.text)
        self.assertEqual(snap_bytes(self.book / "0101.older"), before)
        body = json.loads((self.book / "0102.newer" / "reservation.json").read_text(encoding="utf-8"))
        self.assertEqual(body["supersedes"], "0101.older")
        page = (self.book / "0102.newer" / "01.md").read_text(encoding="utf-8")
        self.assertIn("supersedes: 0101.older", page)
        self.assertIn("not approval, acceptance, seating, publication, or finish", page)

    def test_index_prose_and_review_heading_do_not_decide_completion(self) -> None:
        text = "Did.\n\n## Review — Codex Prime\nDisposition: ACCEPTED\n".encode("utf-8")
        self.write_return(text)
        (self.source / "note.txt").write_bytes(b"data")
        self.reserve()
        captured = self.capture()
        self.assertEqual(captured.code, 0, captured.text)
        member = self.book / "0101.alpha"
        self.assertEqual((member / "return.md").read_bytes(), text)
        page = member / "01.md"
        page.write_bytes(b"# 01\n\naccepted\napproved\n")
        verified = rc.verify(str(self.book), "0101.alpha")
        self.assertEqual(verified.code, 0, verified.text)
        self.assertIn("not approved", verified.text)
        self.assertIn("not accepted", verified.text)
        self.assertIn("result complete", verified.text)

    def test_payload_script_is_archived_and_not_executed(self) -> None:
        self.write_return(b"Did.\n")
        marker = self.tmp / "marker.txt"
        program = self.source / "run_me.py"
        program.write_text(
            "from pathlib import Path\nPath(r%r).write_text('ran')\n" % str(marker),
            encoding="utf-8",
        )
        self.reserve(expected_outputs=["run_me.py"])
        result = self.capture(artifacts=["run_me.py|run_me.py"])
        self.assertEqual(result.code, 0, result.text)
        blob = (self.book / "0101.alpha" / "payload" / "0001.blob").read_bytes()
        self.assertEqual(blob, program.read_bytes())
        self.assertFalse(marker.exists())

    def test_writer_allows_git_checkout_and_refuses_control_and_root(self) -> None:
        """Pass-01 expected a Git-tree refusal. An ordinary directory is allowed.

        The shared work book is not a fixture. Roots and Git control paths
        are refused before a door or member is created.
        """
        repo = self.tmp / "linked"
        repo.mkdir()
        git_file = repo / ".git"
        git_file.write_bytes(b"gitdir: nowhere\n")
        inside = repo / "book"
        inside.mkdir()
        allowed = rc.reserve(
            str(inside),
            "sub-1",
            "alpha",
            "0504.app-entry",
            "05.06.md",
            "05.06",
            [],
            "Builder 2",
            "Codex Prime",
            "Director 2026-10-27",
        )
        self.assertEqual(allowed.code, 0, allowed.text)
        self.assertIn("member 0101.alpha", allowed.text)
        self.assertEqual(git_file.read_bytes(), b"gitdir: nowhere\n")
        self.assertTrue((inside / "0101.alpha" / "reservation.json").is_file())
        file_book = rc.reserve(
            str(git_file),
            "sub-file",
            "file",
            "0504.app-entry",
            "05.06.md",
            "05.06",
            [],
            "Builder 2",
            "Codex Prime",
            "Director 2026-10-27",
        )
        self.assertEqual(file_book.code, 2, file_book.text)
        self.assertIn("Git control", file_book.text)
        self.assertEqual(git_file.read_bytes(), b"gitdir: nowhere\n")
        try:
            os.symlink(inside, self.tmp / "linked-book", target_is_directory=True)
        except OSError as exc:
            self.assertEqual(getattr(exc, "winerror", None), 1314, exc)
        else:
            linked = rc.reserve(
                str(self.tmp / "linked-book"),
                "sub-link",
                "link",
                "0504.app-entry",
                "05.06.md",
                "05.06",
                [],
                "Builder 2",
                "Codex Prime",
                "Director 2026-10-27",
            )
            self.assertEqual(linked.code, 2, linked.text)
            self.assertIn("link", linked.text)
            self.assertFalse((inside / "0102.link").exists())
        control = self.tmp / "control"
        control.mkdir()
        git_dir = control / ".git"
        (git_dir / "refs").mkdir(parents=True)
        head = git_dir / "HEAD"
        head.write_bytes(b"ref: refs/heads/workshop\n")
        as_book = rc.reserve(
            str(git_dir),
            "sub-git",
            "git",
            "0504.app-entry",
            "05.06.md",
            "05.06",
            [],
            "Builder 2",
            "Codex Prime",
            "Director 2026-10-27",
        )
        self.assertEqual(as_book.code, 2, as_book.text)
        self.assertIn("Git control", as_book.text)
        self.assertFalse((git_dir / "0100.band.returns").exists())
        nested = rc.reserve(
            str(git_dir / "refs"),
            "sub-nested",
            "nested",
            "0504.app-entry",
            "05.06.md",
            "05.06",
            [],
            "Builder 2",
            "Codex Prime",
            "Director 2026-10-27",
        )
        self.assertEqual(nested.code, 2, nested.text)
        self.assertIn("Git control", nested.text)
        self.assertFalse((git_dir / "refs" / "0100.band.returns").exists())
        self.assertEqual(head.read_bytes(), b"ref: refs/heads/workshop\n")
        ordinary = control / "work"
        ordinary.mkdir()
        inside_checkout = rc.reserve(
            str(ordinary),
            "sub-2",
            "beta",
            "0504.app-entry",
            "05.06.md",
            "05.06",
            [],
            "Builder 2",
            "Codex Prime",
            "Director 2026-10-27",
        )
        self.assertEqual(inside_checkout.code, 0, inside_checkout.text)
        self.assertIn("member 0101.beta", inside_checkout.text)
        self.assertEqual(head.read_bytes(), b"ref: refs/heads/workshop\n")
        root = Path(self.tmp.anchor)
        door = root / "0100.band.returns"
        accidental = root / "0101.alpha"
        door_existed = door.exists()
        member_existed = accidental.exists()
        created: list[str] = []
        try:
            rooted = rc.reserve(
                str(root),
                "sub-1",
                "alpha",
                "0504.app-entry",
                "05.06.md",
                "05.06",
                [],
                "Builder 2",
                "Codex Prime",
                "Director 2026-10-27",
            )
            self.assertEqual(rooted.code, 2, rooted.text)
            self.assertIn("filesystem root", rooted.text)
            self.assertEqual(door.exists(), door_existed)
            self.assertEqual(accidental.exists(), member_existed)
        finally:
            if not door_existed and door.exists():
                shutil.rmtree(door, ignore_errors=True)
                created.append(str(door))
            if not member_existed and accidental.exists():
                shutil.rmtree(accidental, ignore_errors=True)
                created.append(str(accidental))
            if created:
                raise AssertionError(
                    "removed writer output on the filesystem root: " + ", ".join(created)
                )

    def test_source_commit_rules_and_overlap(self) -> None:
        self.write_return(b"Did.\n")
        self.reserve(expected_outputs=[])
        bare = self.capture(artifacts=[], source_commit=PIN)
        self.assertEqual(bare.code, 2, bare.text)
        self.assertFalse((self.book / "0101.alpha" / "return.md").exists())
        retrospective = self.capture(
            artifacts=[],
            retrospective=True,
            source_commit=PIN,
            return_includes_prime_review=True,
        )
        self.assertEqual(retrospective.code, 0, retrospective.text)
        manifest = json.loads(
            (self.book / "0101.alpha" / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertTrue(manifest["retrospective"])
        self.assertEqual(manifest["source_commit"], PIN)
        self.assertTrue(manifest["return"]["includes_prime_review"])
        self.assertFalse((self.book / "0101.alpha" / "payload").exists())
        book = self.tmp / "origin-book"
        book.mkdir()
        return_file = book / "0508.return-capture" / "05.02.md"
        return_file.parent.mkdir(parents=True)
        return_file.write_bytes(b"Did. On the work page.\n")
        note = book / "evidence" / "note.txt"
        note.parent.mkdir()
        note.write_bytes(b"from-book\n")
        reserved = rc.reserve(
            str(book),
            "sub-page",
            "page",
            "0508.return-capture",
            "05.02.md",
            "05.02",
            ["evidence/note.txt"],
            "Builder 2",
            "Codex Prime",
            "Director 2026-10-27",
        )
        self.assertEqual(reserved.code, 0, reserved.text)
        member = book / "0101.page"
        bad_return = rc.capture(
            str(book),
            "sub-page",
            str(member / "01.md"),
            str(book),
            ["evidence/note.txt|evidence/note.txt"],
        )
        self.assertEqual(bad_return.code, 2, bad_return.text)
        self.assertIn("destination member", bad_return.text)
        self.assertFalse((member / "return.md").exists())
        bad_root = rc.capture(
            str(book),
            "sub-page",
            str(return_file),
            str(member),
            ["01.md|evidence/note.txt"],
        )
        self.assertEqual(bad_root.code, 2, bad_root.text)
        self.assertIn("destination member", bad_root.text)
        self.assertFalse((member / "return.md").exists())
        bad_artifact = rc.capture(
            str(book),
            "sub-page",
            str(return_file),
            str(book),
            ["0101.page/01.md|evidence/note.txt"],
        )
        self.assertEqual(bad_artifact.code, 2, bad_artifact.text)
        self.assertIn("destination member", bad_artifact.text)
        self.assertFalse((member / "receipt.json").exists())
        bad_alias = rc.capture(
            str(book),
            "sub-page",
            str(return_file),
            str(book),
            ["0101.PAGE/01.md|evidence/note.txt"],
        )
        self.assertEqual(bad_alias.code, 2, bad_alias.text)
        self.assertIn("destination member", bad_alias.text)
        self.assertFalse((member / "manifest.json").exists())
        captured = rc.capture(
            str(book),
            "sub-page",
            str(return_file),
            str(book),
            ["evidence/note.txt|evidence/note.txt"],
        )
        self.assertEqual(captured.code, 0, captured.text)
        self.assertEqual((member / "return.md").read_bytes(), b"Did. On the work page.\n")
        self.assertEqual((member / "payload" / "0001.blob").read_bytes(), b"from-book\n")
        self.assertEqual(return_file.read_bytes(), b"Did. On the work page.\n")
        self.assertEqual(note.read_bytes(), b"from-book\n")

    def test_cli_syntax_uses_stderr(self) -> None:
        proc = subprocess.run(
            [PY, "-B", str(SCRIPT)],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(proc.returncode, 2)
        self.assertTrue(proc.stderr.strip())

    def test_control_character_and_reserved_name_write_nothing(self) -> None:
        result = self.reserve(release="bad\nrelease")
        self.assertEqual(result.code, 2, result.text)
        self.assertEqual(list(self.book.iterdir()), [])
        reserved = self.reserve(submission="CON")
        self.assertEqual(reserved.code, 2, reserved.text)
        self.assertEqual(list(self.book.iterdir()), [])

    def prove_local_checkout(self, repo: Path, env: dict[str, str]) -> None:
        code = repo / "code"
        evidence = repo / "evidence"
        page = repo / "work" / "0508.return-capture"
        code.mkdir(parents=True)
        evidence.mkdir()
        page.mkdir(parents=True)
        (repo / ".gitattributes").write_bytes(b"* -text\n")
        tool = code / "tool.py"
        note = evidence / "note.txt"
        return_file = page / "05.02.md"
        tool.write_bytes(b"print('captured')\n")
        note.write_bytes(b"evidence-bytes\n")
        return_file.write_bytes(b"Did. Captured from this checkout.\n")
        source_bytes = {
            tool: tool.read_bytes(),
            note: note.read_bytes(),
            return_file: return_file.read_bytes(),
        }
        run_git(
            repo,
            [
                "add",
                "--",
                ".gitattributes",
                "code/tool.py",
                "evidence/note.txt",
                "work/0508.return-capture/05.02.md",
            ],
            env,
        )
        run_git(repo, ["commit", "-m", "originating page"], env)
        book = repo / "work"
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
        git_file = repo / ".git"
        git_file_bytes = git_file.read_bytes() if git_file.is_file() else None
        head_before = run_git(repo, ["rev-parse", "HEAD"], env).stdout.strip()
        artifacts = ["code/tool.py|code/tool.py", "evidence/note.txt|evidence/note.txt"]
        reserved = rc.reserve(
            str(book),
            "page-0502",
            "local",
            "0508.return-capture",
            "05.02.md",
            "05.02",
            ["code/tool.py", "evidence/note.txt"],
            "Grok Builder 2",
            "Codex Prime",
            "Director 2026-10-27",
        )
        self.assertEqual(reserved.code, 0, reserved.text)
        self.assertIn("member 0101.local", reserved.text)
        member = book / "0101.local"
        bad_return = rc.capture(str(book), "page-0502", str(member / "01.md"), str(repo), artifacts)
        self.assertEqual(bad_return.code, 2, bad_return.text)
        self.assertIn("return file is inside the destination member", bad_return.text)
        self.assertFalse((member / "return.md").exists())
        bad_root = rc.capture(str(book), "page-0502", str(return_file), str(member), ["01.md|code/tool.py"])
        self.assertEqual(bad_root.code, 2, bad_root.text)
        self.assertIn("source root is inside the destination member", bad_root.text)
        self.assertFalse((member / "return.md").exists())
        bad_artifact = rc.capture(
            str(book),
            "page-0502",
            str(return_file),
            str(repo),
            ["work/0101.local/01.md|code/tool.py", "evidence/note.txt|evidence/note.txt"],
        )
        self.assertEqual(bad_artifact.code, 2, bad_artifact.text)
        self.assertIn("artifact is inside the destination member", bad_artifact.text)
        self.assertFalse((member / "receipt.json").exists())
        bad_alias = rc.capture(
            str(book),
            "page-0502",
            str(return_file),
            str(repo),
            ["work/0101.LOCAL/01.md|code/tool.py", "evidence/note.txt|evidence/note.txt"],
        )
        self.assertEqual(bad_alias.code, 2, bad_alias.text)
        self.assertIn("artifact is inside the destination member", bad_alias.text)
        self.assertFalse((member / "manifest.json").exists())
        captured = rc.capture(str(book), "page-0502", str(return_file), str(repo), artifacts)
        self.assertEqual(captured.code, 0, captured.text)
        self.assertIn("result captured", captured.text)
        self.assertEqual((member / "return.md").read_bytes(), source_bytes[return_file])
        self.assertEqual((member / "payload" / "0001.blob").read_bytes(), source_bytes[tool])
        self.assertEqual((member / "payload" / "0002.blob").read_bytes(), source_bytes[note])
        sealed = snap_bytes(member)
        retry = rc.capture(str(book), "page-0502", str(return_file), str(repo), artifacts)
        self.assertEqual(retry.code, 0, retry.text)
        self.assertIn("result already-captured", retry.text)
        self.assertEqual(snap_bytes(member), sealed)
        return_file.write_bytes(b"changed\n")
        conflict = rc.capture(str(book), "page-0502", str(return_file), str(repo), artifacts)
        self.assertEqual(conflict.code, 2, conflict.text)
        self.assertIn("conflict submission page-0502", conflict.text)
        self.assertEqual(snap_bytes(member), sealed)
        return_file.write_bytes(source_bytes[return_file])
        for path, data in source_bytes.items():
            self.assertEqual(path.read_bytes(), data)
        after_control = {
            "gitdir": snapshot_git_control(gitdir),
            "common": snapshot_git_control(common),
        }
        self.assertEqual(after_control, before_control)
        if git_file_bytes is not None:
            self.assertEqual(git_file.read_bytes(), git_file_bytes)
        head_after = run_git(repo, ["rev-parse", "HEAD"], env).stdout.strip()
        self.assertEqual(head_after, head_before)
        status = run_git(repo, ["status", "--porcelain=v1", "--untracked-files=all"], env)
        lines = [line for line in status.stdout.splitlines() if line.strip()]
        self.assertTrue(lines)
        for line in lines:
            self.assertTrue(line.startswith("?? "), line)
            relative = line[3:].replace("\\", "/")
            self.assertTrue(relative.startswith("work/0101.local/"), relative)
        proc = subprocess.run(
            [PY, "-B", str(SCRIPT), "verify", "--book", str(book), "--member", "0101.local"],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("result complete", proc.stdout)
        self.assertIn("not approved", proc.stdout)
        self.assertIn("not accepted", proc.stdout)
        self.assertIn("not published", proc.stdout)
        run_git(repo, ["add", "--", "work/0101.local"], env)
        run_git(repo, ["commit", "-m", "local capture"], env)
        self.assertNotEqual(run_git(repo, ["rev-parse", "HEAD"], env).stdout.strip(), head_before)
        for relative, data in sealed.items():
            blob = run_git(repo, ["rev-parse", f"HEAD:work/0101.local/{relative}"], env).stdout.strip()
            shown = subprocess.run(
                ["git", "cat-file", "blob", blob],
                cwd=repo,
                env=env,
                capture_output=True,
            )
            self.assertEqual(shown.returncode, 0, shown.stderr)
            self.assertEqual(shown.stdout, data)
        for path, data in source_bytes.items():
            self.assertEqual(path.read_bytes(), data)
        if common != gitdir:
            self.assertEqual(snapshot_git_control(common), before_control["common"])

    def test_capture_in_regular_git_checkout(self) -> None:
        repo = self.tmp / "checkout"
        env = git_env()
        init_checkout(repo, env)
        self.assertTrue((repo / ".git").is_dir())
        self.prove_local_checkout(repo, env)

    def test_capture_in_git_file_worktree(self) -> None:
        main = self.tmp / "main"
        worktree = self.tmp / "wt"
        env = git_env()
        init_checkout(main, env)
        (main / "README").write_bytes(b"seed\n")
        run_git(main, ["add", "--", "README"], env)
        run_git(main, ["commit", "-m", "seed"], env)
        main_control = snapshot_git_control(main / ".git")
        run_git(main, ["worktree", "add", "--detach", str(worktree), "HEAD"], env)
        self.assertTrue((worktree / ".git").is_file())
        self.prove_local_checkout(worktree, env)
        after = snapshot_git_control(main / ".git")
        self.assertEqual(after["HEAD"], main_control["HEAD"])
        self.assertEqual(after["refs/heads/workshop"], main_control["refs/heads/workshop"])
        self.assertEqual(after["index"], main_control["index"])


if __name__ == "__main__":
    unittest.main()
