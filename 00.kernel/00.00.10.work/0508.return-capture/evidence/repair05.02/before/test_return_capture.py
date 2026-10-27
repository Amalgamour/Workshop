"""Isolated tests for return-capture/1. Disposable books only."""

from __future__ import annotations

import ast
import hashlib
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
REAL_BOOK = Path(r"D:\Git\lib-build\00.kernel\00.00.10.work")
PIN = "e6d6eb75538732c7eedbc840042242d386b25c2f"


def outside_git(path: Path) -> bool:
    current = path.resolve()
    while True:
        if (current / ".git").exists():
            return False
        if current.parent == current:
            return True
        current = current.parent


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

    def test_writer_refuses_git_and_real_book_is_unchanged(self) -> None:
        repo = self.tmp / "repo"
        repo.mkdir()
        (repo / ".git").write_text("gitdir: nowhere\n", encoding="utf-8")
        inside = repo / "book"
        inside.mkdir()
        refused = rc.reserve(
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
        self.assertEqual(refused.code, 2, refused.text)
        self.assertIn("Git working tree", refused.text)
        self.assertEqual(list(inside.iterdir()), [])
        sibling = self.tmp / "sibling"
        sibling.mkdir()
        (self.tmp / "other").mkdir()
        (self.tmp / "other" / ".git").mkdir()
        ok = rc.reserve(
            str(sibling),
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
        self.assertEqual(ok.code, 0, ok.text)
        if not REAL_BOOK.is_dir():
            self.skipTest("real work book is not on this machine")
        door = REAL_BOOK / "0100.band.returns" / "01.md"
        before_hash = hashlib.sha256(door.read_bytes()).hexdigest()
        before_names = set(os.listdir(REAL_BOOK))
        try:
            real = rc.reserve(
                str(REAL_BOOK),
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
            self.assertEqual(real.code, 2, real.text)
            self.assertIn("Git working tree", real.text)
            self.assertEqual(hashlib.sha256(door.read_bytes()).hexdigest(), before_hash)
            self.assertEqual(set(os.listdir(REAL_BOOK)), before_names)
            self.assertFalse((REAL_BOOK / "0100.band.returns" / ".allocation.lock").exists())
            self.assertFalse(any(name.startswith("0101") for name in os.listdir(REAL_BOOK)))
        finally:
            lock = REAL_BOOK / "0100.band.returns" / ".allocation.lock"
            if lock.is_file():
                os.remove(lock)
                raise AssertionError(f"removed an allocation lock left on the real door: {lock}")
            accidental = REAL_BOOK / "0101.alpha"
            if "0101.alpha" not in before_names and accidental.exists():
                shutil.rmtree(accidental)
                raise AssertionError("removed accidental real member 0101.alpha")

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
        overlap = self.tmp / "overlap-book"
        overlap.mkdir()
        nested = overlap / "source"
        nested.mkdir()
        refused = rc.capture(
            str(overlap),
            "sub-1",
            str(self.return_file),
            str(overlap),
            [],
        )
        self.assertEqual(refused.code, 2, refused.text)

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


if __name__ == "__main__":
    unittest.main()
