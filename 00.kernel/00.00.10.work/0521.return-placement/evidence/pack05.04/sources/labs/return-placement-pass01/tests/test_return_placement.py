"""Fixture tests for return-line routing and migration rehearsal."""

from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
import return_placement as rp


def _bytes(body: dict) -> bytes:
    return (json.dumps(body, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def seal(folder: Path, page: str, batch: str, submission: str,
         ret: bytes | None, payloads: list[bytes] | None = None) -> None:
    """Write a return-capture/1 package the pinned reader can accept, or a return-less source."""
    folder.mkdir(parents=True, exist_ok=True)
    number, slug = folder.name.split(".", 1)
    blobs = [] if payloads is None else payloads
    reservation = {
        "destination": {"member": number, "name": slug, "path": folder.name},
        "expected_outputs": [f"note-{index}.md" for index in range(1, len(blobs) + 1)],
        "kind": "reservation",
        "origin": {"batch": batch, "book": "00.00.10.work", "page": page},
        "release": "prepared",
        "reserved_at": "2026-10-31T00:00:00.000000Z",
        "reviewer": "codex-prime",
        "schema": "return-capture/1",
        "submission_id": submission,
        "submitter": "grok-1",
        "supersedes": None,
    }
    raw_res = _bytes(reservation)
    (folder / "reservation.json").write_bytes(raw_res)
    (folder / "01.md").write_bytes(b"index\n")
    if ret is None:
        return
    (folder / "return.md").write_bytes(ret)
    if blobs:
        (folder / "payload").mkdir()
        for index, blob in enumerate(blobs, start=1):
            (folder / "payload" / f"{index:04d}.blob").write_bytes(blob)
    sources = [
        {
            "bytes": len(blob),
            "logical": f"note-{index}.md",
            "payload": f"{index:04d}.blob",
            "sha256": _sha(blob),
        }
        for index, blob in enumerate(blobs, start=1)
    ]
    manifest = {
        "captured_at": "2026-10-31T00:00:00.000000Z",
        "kind": "manifest",
        "omitted": [],
        "required": [source["logical"] for source in sources],
        "reservation_sha256": _sha(raw_res),
        "retrospective": False,
        "return": {"bytes": len(ret), "includes_prime_review": False, "sha256": _sha(ret)},
        "schema": "return-capture/1",
        "source_commit": None,
        "sources": sources,
        "submission_id": submission,
    }
    raw_man = _bytes(manifest)
    (folder / "manifest.json").write_bytes(raw_man)
    (folder / "receipt.json").write_bytes(_bytes({
        "captured_at": "2026-10-31T00:00:00.000000Z",
        "kind": "receipt",
        "manifest_sha256": _sha(raw_man),
        "reservation_sha256": _sha(raw_res),
        "schema": "return-capture/1",
        "submission_id": submission,
    }))


class PlacementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.outer = tempfile.TemporaryDirectory()
        self.root = Path(self.outer.name) / "root"
        self.root.mkdir()

    def tearDown(self) -> None:
        self.outer.cleanup()

    def make_member(self, name: str, page: str, batch: str, submission: str,
                    ret: bytes | None = b"RETURN\n", payload: bool = True) -> Path:
        folder = self.root / name
        if ret is None:
            blobs = None
        elif payload:
            blobs = [b"payload-a", b"payload-b"]
        else:
            blobs = []
        seal(folder, page, batch, submission, ret, blobs)
        return folder

    def journal(self) -> dict:
        return json.loads((self.root / "placement-journal.json").read_text(encoding="utf-8"))

    def test_route_n5_and_n7_and_unknown(self) -> None:
        route = rp.compute_route({"book": "00.00.10.work", "page": "0504.app-entry", "batch": "05.06"})
        self.assertEqual(route["schema"], "return-placement-route/1")
        self.assertEqual(route["page_number"], "0504")
        self.assertEqual(route["target_number"], "0104")
        self.assertEqual(route["subject"], "app-entry")
        self.assertEqual(route["target_page"], "0104.app-entry")
        self.assertEqual(route["return_path"], "0104.app-entry/05.06.return.md")
        self.assertEqual(route["custody_dir"], "0104.app-entry/05.06.custody")
        self.assertFalse(route["sequential_allocation"])
        self.assertIsNone(route["pack_path"])
        second = rp.compute_route({"book": "00.00.10.work", "page": "0504.app-entry", "batch": "05.08"})
        self.assertEqual(second["target_page"], "0104.app-entry")
        self.assertEqual(second["return_path"], "0104.app-entry/05.08.return.md")
        local = rp.compute_route({"book": "00.00.10.work", "page": "0701.bench-method", "batch": "05.01"})
        self.assertEqual(local["route"], "page-local-colab")
        self.assertEqual(local["target_page"], "0701.bench-method")
        self.assertEqual(local["pack_path"], "0701.bench-method/05.01.pack.md")
        self.assertEqual(local["review_path"], "0701.bench-method/06.01.review.md")
        self.assertFalse(local["target_page"].startswith("01"))
        self.assertEqual(local["workflow_space"], "0")
        other_space = rp.compute_route({"book": "00.00.10.work", "page": "1504.app-entry", "batch": "05.04"})
        self.assertEqual(other_space["workflow_space"], "1")
        self.assertEqual(other_space["target_number"], "1104")
        self.assertEqual(other_space["target_page"], "1104.app-entry")
        self.assertEqual(other_space["return_path"], "1104.app-entry/05.04.return.md")
        ninth = rp.compute_route({"book": "00.00.10.work", "page": "9504.x", "batch": "05.01"})
        self.assertEqual(ninth["target_page"], "9104.x")
        self.assertEqual(ninth["workflow_space"], "9")
        kept = rp.compute_route({"book": "00.00.10.work", "page": "1702.design", "batch": "05.02"})
        self.assertEqual(kept["route"], "page-local-colab")
        self.assertEqual(kept["target_page"], "1702.design")
        self.assertEqual(kept["target_number"], "1702")
        self.assertEqual(kept["pack_path"], "1702.design/05.02.pack.md")
        also_local = rp.compute_route({"book": "00.00.10.work", "page": "1701.other", "batch": "05.01"})
        self.assertEqual(also_local["route"], "page-local-colab")
        self.assertEqual(also_local["target_page"], "1701.other")
        this_batch = rp.compute_route({"book": "00.00.10.work", "page": "0521.return-placement", "batch": "05.02"})
        self.assertEqual(this_batch["target_page"], "0121.return-placement")
        self.assertEqual(this_batch["workflow_space"], "0")
        for page in ("0201.alpha", "0301.beta", "0401.gamma", "0601.delta", "1201.side"):
            with self.assertRaises(rp.PlacementError) as caught:
                rp.compute_route({"book": "00.00.10.work", "page": page, "batch": "05.01"})
            self.assertEqual(caught.exception.reason, "undeclared origin")
        with self.assertRaises(rp.PlacementError) as caught:
            rp.compute_route({"book": "00.00.10.work", "page": "0504.app-entry", "batch": "06.01"})
        self.assertEqual(caught.exception.reason, "undeclared origin")

    def test_multiple_passes_share_one_line_and_preserve_bytes(self) -> None:
        first = self.make_member("0101.app-entry-0506", "0504.app-entry", "05.06", "sub-06")
        second = self.make_member("0106.entry-regression-0509", "0504.app-entry", "05.09", "sub-09", ret=b"SECOND\n")
        odd = self.make_member("0199.not-the-subject", "0504.app-entry", "05.08", "sub-08", ret=b"THIRD\n")
        result = rp.apply_run(str(self.root), [str(first), str(second), str(odd)])
        self.assertEqual(result["exit"], 0)
        self.assertTrue(result["complete"])
        page = self.root / "0104.app-entry"
        self.assertTrue((page / "05.06.return.md").is_file())
        self.assertTrue((page / "05.08.return.md").is_file())
        self.assertTrue((page / "05.09.return.md").is_file())
        self.assertEqual((page / "05.08.return.md").read_bytes(), b"THIRD\n")
        self.assertFalse((self.root / "0199.not-the-subject-placed").exists())
        custody = page / "05.06.custody"
        for name in ("01.md", "reservation.json", "manifest.json", "receipt.json", "return.md"):
            self.assertEqual((custody / name).read_bytes(), (first / name).read_bytes())
        self.assertEqual((custody / "payload" / "0001.blob").read_bytes(), b"payload-a")
        self.assertEqual((custody / "payload" / "0002.blob").read_bytes(), b"payload-b")
        relocation = json.loads((custody / "relocation.json").read_text(encoding="utf-8"))
        self.assertEqual(relocation["schema"], "return-placement-relocation/1")
        self.assertFalse(relocation["reservation_destination_rewritten"])
        self.assertEqual(relocation["statement"], rp.STATEMENT)
        self.assertIsNone(relocation["acceptance"])
        self.assertEqual(relocation["origin"]["page"], "0504.app-entry")
        self.assertEqual((custody / "reservation.json").read_bytes(), (first / "reservation.json").read_bytes())
        self.assertIn(first.name, (custody / "reservation.json").read_text(encoding="utf-8"))
        self.assertTrue(result["items"][0]["custody_valid"])
        self.assertTrue(result["items"][0]["line_adoption"])
        self.assertIsNone(result["items"][0]["acceptance"])
        names = sorted(path.name for path in self.root.iterdir() if path.is_dir() and path.name.startswith("0104."))
        self.assertEqual(names, ["0104.app-entry"])

    def test_idempotent_and_changed_bytes(self) -> None:
        source = self.make_member("0101.app-entry-0506", "0504.app-entry", "05.06", "sub-06")
        first = rp.apply_run(str(self.root), [str(source)])
        self.assertEqual(first["exit"], 0)
        tail = self.root / "0104.app-entry" / "05.06.return.md"
        before = os.lstat(tail)
        original = tail.read_bytes()
        again = rp.apply_run(str(self.root), [str(source)])
        self.assertEqual(again["exit"], 0)
        self.assertEqual(again["items"][0]["replay"], "already-placed")
        after = os.lstat(tail)
        self.assertEqual(before.st_ino, after.st_ino)
        self.assertEqual(before.st_mtime_ns, after.st_mtime_ns)
        (source / "return.md").write_bytes(b"CHANGED\n")
        refused = rp.apply_run(str(self.root), [str(source)])
        self.assertEqual(refused["exit"], 2)
        self.assertEqual(tail.read_bytes(), original)
        self.assertEqual(refused["items"][0]["replay"], "refused")

    def test_duplicate_origin_copies_neither(self) -> None:
        left = self.make_member("0101.one", "0504.app-entry", "05.06", "sub-a")
        right = self.make_member("0102.two", "0504.app-entry", "05.06", "sub-b", ret=b"OTHER\n")
        result = rp.apply_run(str(self.root), [str(left), str(right)])
        self.assertEqual(result["exit"], 1)
        self.assertFalse(result["complete"])
        self.assertFalse((self.root / "0104.app-entry").exists())
        self.assertEqual({item["status"] for item in result["items"]}, {"conflict"})

    def test_occupied_target_and_legacy_neighbor(self) -> None:
        source = self.make_member("0104.app-entry-0508", "0504.app-entry", "05.06", "sub-06")
        legacy = self.root / "0104.legacy-neighbor"
        legacy.mkdir()
        (legacy / "keep.txt").write_bytes(b"keep")
        result = rp.apply_run(str(self.root), [str(source)])
        self.assertEqual(result["exit"], 1)
        self.assertFalse(result["complete"])
        self.assertEqual(result["items"][0]["status"], "staged")
        self.assertFalse(result["items"][0]["line_adoption"])
        self.assertIsNone(result["items"][0]["acceptance"])
        self.assertTrue(result["items"][0]["custody_valid"])
        self.assertFalse((self.root / "0104.app-entry").exists())
        staged = self.root / "staging" / "0104.app-entry-0508" / "05.06.return.md"
        self.assertEqual(staged.read_bytes(), b"RETURN\n")
        self.assertEqual((legacy / "keep.txt").read_bytes(), b"keep")
        self.assertEqual((source / "reservation.json").read_bytes(),
                         (self.root / "staging" / "0104.app-entry-0508" / "05.06.custody" / "reservation.json").read_bytes())

    def test_free_line_different_tail_is_not_overwritten(self) -> None:
        source = self.make_member("0150.sample-pass", "0504.app-entry", "05.06", "sub-06")
        occupied = self.root / "0104.app-entry" / "05.06.return.md"
        occupied.parent.mkdir(parents=True)
        occupied.write_bytes(b"OTHER\n")
        before = os.lstat(occupied)
        result = rp.apply_run(str(self.root), [str(source)])
        self.assertEqual(result["items"][0]["status"], "conflict")
        self.assertEqual(occupied.read_bytes(), b"OTHER\n")
        self.assertEqual(os.lstat(occupied).st_ino, before.st_ino)
        self.assertFalse((self.root / "0104.app-entry" / "05.06.custody").exists())

    def test_unresolved_source_ignores_slug(self) -> None:
        folder = self.root / "0104.fake-subject"
        folder.mkdir()
        (folder / "01.md").write_bytes(b"no reservation\n")
        result = rp.apply_run(str(self.root), [str(folder)])
        self.assertEqual(result["items"][0]["status"], "unresolved")
        self.assertEqual(result["items"][0]["reason"], "missing reservation")
        self.assertFalse((folder / "05.01.return.md").exists())
        self.assertFalse((self.root / "0104.fake-subject" / "05.01.custody").exists())
        found = rp.lookup_run(str(self.root), member="0104.fake-subject")
        self.assertEqual(found["items"][0]["status"], "unresolved")

    def test_missing_return_stays_incomplete(self) -> None:
        source = self.make_member("0154.colab-support-first-0501", "0510.colab-tools", "05.01", "claude-0510-0501", ret=None)
        result = rp.apply_run(str(self.root), [str(source)])
        self.assertEqual(result["exit"], 1)
        self.assertFalse(result["complete"])
        self.assertEqual(result["items"][0]["status"], "incomplete")
        page = self.root / "0110.colab-tools"
        self.assertFalse((page / "05.01.return.md").exists())
        copied = page / "05.01.custody" / "reservation.json"
        self.assertEqual(copied.read_bytes(), (source / "reservation.json").read_bytes())
        found = rp.lookup_run(str(self.root), page="0510.colab-tools", batch="05.01")
        self.assertEqual(found["items"][0]["status"], "incomplete")

    def test_colab_equal_and_conflict(self) -> None:
        body = b"COLAB-RETURN\n"
        source = self.make_member("0165.bench-method-colab-0501", "0701.bench-method", "05.01", "grok-1-0701-0501", ret=body)
        tail = self.root / "0701.bench-method" / "05.01.return.md"
        tail.parent.mkdir(parents=True)
        tail.write_bytes(body)
        before = os.lstat(tail)
        result = rp.apply_run(str(self.root), [str(source)])
        self.assertEqual(result["exit"], 0)
        self.assertEqual(result["items"][0]["status"], "verified-equal")
        self.assertEqual(os.lstat(tail).st_ino, before.st_ino)
        self.assertTrue((self.root / "0701.bench-method" / "05.01.custody" / "return.md").is_file())
        self.assertFalse((self.root / "0101.bench-method").exists())
        self.assertEqual((self.root / "0701.bench-method" / "05.01.custody" / "receipt.json").read_bytes(),
                         (source / "receipt.json").read_bytes())
        other = self.root / "other"
        other.mkdir()
        conflict_root = other
        # A second fixture proves a differing tail is not overwritten.
        self.outer2 = tempfile.TemporaryDirectory()
        self.addCleanup(self.outer2.cleanup)
        root = Path(self.outer2.name)
        folder = root / "0165.bench-method-colab-0501"
        seal(folder, "0701.bench-method", "05.01", "grok-1-0701-0501", body, [])
        bad = root / "0701.bench-method" / "05.01.return.md"
        bad.parent.mkdir(parents=True)
        bad.write_bytes(b"DIFFERENT\n")
        conflict = rp.apply_run(str(root), [str(folder)])
        self.assertEqual(conflict["items"][0]["status"], "conflict")
        self.assertEqual(bad.read_bytes(), b"DIFFERENT\n")
        self.assertFalse((root / "0701.bench-method" / "05.01.custody").exists())
        self.assertFalse((root / "0101.bench-method").exists())
        del conflict_root

    def test_unknown_bands_place_nothing(self) -> None:
        sources = []
        for number, name in (("0201", "alpha"), ("0301", "beta"), ("0401", "gamma"), ("0601", "delta")):
            sources.append(self.make_member(f"01{number[-2:]}.{name}", f"{number}.{name}", "05.01", name, payload=False))
        result = rp.apply_run(str(self.root), [str(path) for path in sources])
        self.assertEqual(result["exit"], 2)
        self.assertTrue(all(item["reason"] == "undeclared origin" for item in result["items"]))
        dirs = sorted(path.name for path in self.root.iterdir() if path.is_dir())
        self.assertEqual(dirs, sorted(path.name for path in sources))

    def test_interrupt_resume_and_hash_mismatch(self) -> None:
        source = self.make_member("0101.app-entry-0506", "0504.app-entry", "05.06", "sub-06")
        stopped = rp.apply_run(str(self.root), [str(source)], interrupt_after=2)
        self.assertEqual(stopped["exit"], 3)
        self.assertFalse(stopped["complete"])
        custody = self.root / "0104.app-entry" / "05.06.custody"
        self.assertTrue((custody / "01.md").is_file())
        self.assertTrue((custody / "reservation.json").is_file())
        self.assertFalse((custody / "relocation.json").exists())
        self.assertFalse(self.journal()["complete"])
        resumed = rp.resume_run(str(self.root))
        self.assertEqual(resumed["exit"], 0)
        self.assertTrue(resumed["complete"])
        self.assertEqual((self.root / "0104.app-entry" / "05.06.return.md").read_bytes(), b"RETURN\n")
        self.assertEqual((custody / "payload" / "0001.blob").read_bytes(), b"payload-a")
        receipt = custody / "receipt.json"
        receipt.write_bytes(b"broken\n")
        mismatched = rp.resume_run(str(self.root))
        self.assertEqual(mismatched["exit"], 2)
        self.assertFalse(self.journal()["complete"])
        self.assertEqual(receipt.read_bytes(), b"broken\n")

    def test_rollback_keeps_sources_and_refuses_mismatch(self) -> None:
        source = self.make_member("0101.app-entry-0506", "0504.app-entry", "05.06", "sub-06", payload=False)
        original = (source / "reservation.json").read_bytes()
        placed = rp.apply_run(str(self.root), [str(source)])
        self.assertEqual(placed["exit"], 0)
        tail = self.root / "0104.app-entry" / "05.06.return.md"
        self.assertTrue(tail.is_file())
        rolled = rp.rollback_run(str(self.root))
        self.assertEqual(rolled["exit"], 0)
        self.assertFalse(rolled["complete"])
        self.assertFalse(tail.exists())
        self.assertEqual((source / "reservation.json").read_bytes(), original)
        self.assertEqual(self.journal()["items"][0]["status"], "rolled-back")
        rp.apply_run(str(self.root), [str(source)])
        victim = self.root / "0104.app-entry" / "05.06.custody" / "01.md"
        victim.write_bytes(b"nope\n")
        with self.assertRaises(rp.PlacementError) as caught:
            rp.rollback_run(str(self.root))
        self.assertEqual(caught.exception.reason, "hash mismatch")
        self.assertEqual(victim.read_bytes(), b"nope\n")
        self.assertTrue(tail.is_file())
        self.assertEqual((source / "return.md").read_bytes(), b"RETURN\n")

    def test_path_escape_and_door_refuse_before_journal(self) -> None:
        outside = Path(self.outer.name) / "outside"
        outside.mkdir()
        with self.assertRaises(rp.PlacementError) as caught:
            rp.apply_run(str(self.root), [str(outside)])
        self.assertEqual(caught.exception.reason, "path escapes fixture root")
        self.assertFalse((self.root / "placement-journal.json").exists())
        (self.root / "0100.band.returns").mkdir()
        with self.assertRaises(rp.PlacementError) as caught:
            rp.apply_run(str(self.root), [str(self.root)])
        self.assertEqual(caught.exception.reason, "fixture root contains 0100.band.returns")
        self.assertFalse((self.root / "placement-journal.json").exists())

    def test_lookup_by_member_origin_and_return_path(self) -> None:
        source = self.make_member("0101.app-entry-0506", "0504.app-entry", "05.06", "sub-06", payload=False)
        rp.apply_run(str(self.root), [str(source)])
        by_member = rp.lookup_run(str(self.root), member="0101.app-entry-0506")
        by_origin = rp.lookup_run(str(self.root), page="0504.app-entry", batch="05.06")
        by_return = rp.lookup_run(str(self.root), return_path="0104.app-entry/05.06.return.md")
        self.assertEqual(by_member["count"], 1)
        self.assertEqual(by_origin["items"][0]["old_member"], "0101.app-entry-0506")
        self.assertEqual(by_return["items"][0]["status"], "placed")
        checked = rp.verify_run(str(self.root))
        self.assertEqual(checked["exit"], 0)

    def test_filing_check_blocks_until_occupant_is_gone(self) -> None:
        book = self.root / "book"
        occupant = book / "0121.archive-resolution-0508"
        occupant.mkdir(parents=True)
        blocked = rp.filing_check(str(book), "0121.return-placement")
        self.assertFalse(blocked["allowed"])
        self.assertIn("0121.archive-resolution-0508", blocked["blockers"])
        self.assertFalse(blocked["creates"])
        self.assertFalse((book / "0121.return-placement").exists())
        shutil.rmtree(occupant)
        opened = rp.filing_check(str(book), "0121.return-placement")
        self.assertTrue(opened["allowed"])
        self.assertEqual(opened["blockers"], [])
        self.assertFalse((book / "0121.return-placement").exists())

    def test_plan_is_read_only_and_reports_drift(self) -> None:
        book = self.root / "book"
        book.mkdir()
        first = book / "0101.app-entry-0506"
        second = book / "0102.other-0508"
        missing = book / "0154.colab-support-first-0501"
        for folder, page, batch, submission, ret in (
            (first, "0504.app-entry", "05.06", "sub-06", b"ONE\n"),
            (second, "0504.app-entry", "05.08", "sub-08", b"TWO\n"),
            (missing, "0510.colab-tools", "05.01", "sub-154", None),
        ):
            seal(folder, page, batch, submission, ret, [] if ret is not None else None)
        files = []
        for path in sorted(book.rglob("*")):
            if path.is_file():
                data = path.read_bytes()
                rel = path.relative_to(book).as_posix()
                files.append({
                    "path": f"00.kernel/00.00.10.work/{rel}",
                    "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(),
                })
        (second / "return.md").write_bytes(b"DRIFT\n")
        records = [
            {
                "old_member": "0102.other-0508",
                "origin": {"batch": "05.08", "book": "00.00.10.work", "page": "0504.app-entry"},
                "submission": "sub-08",
                "route": "matched-workflow-return-line",
                "target_return": "0104.app-entry/05.08.return.md",
                "status": "corrected audit only; migration not applied",
                "has_receipt": False,
                "verify_exit": 0,
            },
            {
                "old_member": "0101.app-entry-0506",
                "origin": {"batch": "05.06", "book": "00.00.10.work", "page": "0504.app-entry"},
                "submission": "sub-06",
                "route": "matched-workflow-return-line",
                "target_return": "0104.app-entry/05.06.return.md",
                "status": "corrected audit only; migration not applied",
                "has_receipt": False,
                "verify_exit": 0,
            },
            {
                "old_member": "0154.colab-support-first-0501",
                "origin": {"batch": "05.01", "book": "00.00.10.work", "page": "0510.colab-tools"},
                "submission": "sub-154",
                "route": "matched-workflow-return-line",
                "target_return": "0110.colab-tools/05.01.return.md",
                "status": "corrected audit only; migration not applied",
                "has_receipt": False,
                "verify_exit": 2,
            },
        ]
        audit = {
            "schema": "return-placement-audit/2",
            "records": records,
            "files": files,
            "cross-source_collisions": {},
            "rule_source": "0417.return-placement/06.01.md",
        }
        audit_path = self.root / "audit-corrected.json"
        audit_path.write_bytes(_bytes(audit))
        before = hashlib.sha256(audit_path.read_bytes()).hexdigest()
        before_dirs = sorted(path.name for path in book.iterdir())
        plan = rp.build_plan(str(book), str(audit_path))
        self.assertEqual(hashlib.sha256(audit_path.read_bytes()).hexdigest(), before)
        self.assertEqual(sorted(path.name for path in book.iterdir()), before_dirs)
        self.assertFalse(plan["live_moves"])
        self.assertTrue(plan["verify_reexecuted"])
        self.assertEqual(plan["lowest_capture"], "0101.app-entry-0506")
        self.assertEqual([item["old_member"] for item in plan["items"]], [
            "0101.app-entry-0506",
            "0102.other-0508",
            "0154.colab-support-first-0501",
        ])
        by_name = {item["old_member"]: item for item in plan["items"]}
        self.assertEqual(by_name["0101.app-entry-0506"]["status"], "planned")
        self.assertTrue(by_name["0101.app-entry-0506"]["verify_applies"])
        self.assertTrue(by_name["0101.app-entry-0506"]["custody_valid"])
        self.assertIsNone(by_name["0101.app-entry-0506"]["acceptance"])
        self.assertFalse(by_name["0101.app-entry-0506"]["occupancy"]["staging_required"])
        self.assertEqual(by_name["0102.other-0508"]["status"], "changed")
        self.assertFalse(by_name["0102.other-0508"]["verify_applies"])
        self.assertEqual(by_name["0154.colab-support-first-0501"]["status"], "incomplete")
        self.assertEqual(by_name["0154.colab-support-first-0501"]["proposed_return_path"], "0110.colab-tools/05.01.return.md")
        self.assertTrue(any(change["kind"] == "changed" for change in plan["changes_since_audit"]))
        self.assertIn("0184", " ".join(plan["preconditions"]))
        self.assertIn("0121.return-placement", " ".join(plan["preconditions"]))
        out = self.root / "migration-plan.json"
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = rp.main(["plan", "--book", str(book), "--audit", str(audit_path), "--out", str(out)])
        self.assertEqual(code, 0)
        self.assertTrue(out.is_file())
        self.assertFalse((book / "0104.app-entry").exists())
        stderr = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(stderr):
            refused = rp.main([
                "plan", "--book", str(book), "--audit", str(audit_path),
                "--out", str(book / "0101.app-entry-0506" / "nope.json"),
            ])
        self.assertEqual(refused, 2)
        self.assertIn("capture member", stderr.getvalue())
        self.assertFalse((book / "0101.app-entry-0506" / "nope.json").exists())

    def test_cli_route(self) -> None:
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            code = rp.main(["route", "--book", "00.00.10.work", "--page", "0504.app-entry", "--batch", "05.06"])
        self.assertEqual(code, 0)
        body = json.loads(stdout.getvalue())
        self.assertEqual(body["target_page"], "0104.app-entry")
        self.assertFalse(body["sequential_allocation"])

    def test_hard_link_refused(self) -> None:
        source = self.make_member("0101.app-entry-0506", "0504.app-entry", "05.06", "sub-06")
        target = source / "payload" / "linked.txt"
        try:
            os.link(source / "payload" / "0001.blob", target)
        except OSError as exc:
            self.skipTest(f"hard link was not created: {exc}")
        result = rp.apply_run(str(self.root), [str(source)])
        self.assertEqual(result["items"][0]["status"], "refused")
        self.assertEqual(result["items"][0]["reason"], "hard link")
        self.assertFalse((self.root / "0104.app-entry").exists())

    def test_symlink_refused_or_skipped(self) -> None:
        source = self.make_member("0101.app-entry-0506", "0504.app-entry", "05.06", "sub-06")
        link = source / "payload" / "linked.txt"
        try:
            os.symlink(source / "payload" / "0001.blob", link)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                self.skipTest("symlink privilege WinError 1314")
            self.skipTest(f"symlink was not created: {exc}")
        result = rp.apply_run(str(self.root), [str(source)])
        self.assertEqual(result["items"][0]["status"], "refused")
        self.assertEqual(result["items"][0]["reason"], "reparse point")
        self.assertFalse((self.root / "0104.app-entry").exists())

    def test_module_does_not_call_reserve(self) -> None:
        text = (LAB / "return_placement.py").read_text(encoding="utf-8")
        self.assertNotIn("import return_capture", text)
        self.assertNotIn("reserve(", text)
        self.assertIn("verify_member", text)
        self.assertEqual(rp.READER_SHA256, hashlib.sha256(
            (LAB.parent / "return-capture-pass01" / "return_capture.py").read_bytes()
        ).hexdigest())


    def test_missing_receipt_is_not_complete(self) -> None:
        source = self.make_member("0160.missing-receipt", "0504.app-entry", "05.02", "missing-receipt")
        (source / "receipt.json").unlink()
        result = rp.apply_run(str(self.root), [str(source)])
        self.assertNotEqual(result["exit"], 0)
        self.assertFalse(result["complete"])
        self.assertNotEqual(result["items"][0]["status"], "placed")
        self.assertFalse(result["items"][0]["custody_valid"])
        self.assertFalse(result["items"][0]["line_adoption"])
        self.assertIsNone(result["items"][0]["acceptance"])
        self.assertIn("receipt", result["items"][0]["reason"])

    def test_malformed_receipt_wrong_hash_and_missing_manifest(self) -> None:
        malformed = self.make_member("0161.malformed-receipt", "0504.app-entry", "05.03", "malformed-receipt")
        (malformed / "receipt.json").write_bytes(b"{\n")
        bad = rp.apply_run(str(self.root), [str(malformed)])
        self.assertFalse(bad["complete"])
        self.assertFalse(bad["items"][0]["custody_valid"])
        self.assertNotEqual(bad["items"][0]["status"], "placed")
        outer = tempfile.TemporaryDirectory()
        self.addCleanup(outer.cleanup)
        root = Path(outer.name)
        hashed = root / "0162.wrong-hash"
        seal(hashed, "0504.app-entry", "05.04", "wrong-hash", b"RETURN\n", [b"payload-a"])
        blob = hashed / "payload" / "0001.blob"
        blob.write_bytes(b"payload-CHANGED")
        wrong = rp.apply_run(str(root), [str(hashed)])
        self.assertFalse(wrong["complete"])
        self.assertFalse(wrong["items"][0]["custody_valid"])
        self.assertNotEqual(wrong["exit"], 0)
        root2 = Path(outer.name) / "manifest"
        missing = root2 / "0163.missing-manifest"
        seal(missing, "0504.app-entry", "05.05", "missing-manifest", b"RETURN\n", [])
        (missing / "manifest.json").unlink()
        absent = rp.apply_run(str(root2), [str(missing)])
        self.assertFalse(absent["complete"])
        self.assertFalse(absent["items"][0]["custody_valid"])
        self.assertIn("manifest", absent["items"][0]["reason"])

    def test_valid_sealed_package_can_complete(self) -> None:
        source = self.make_member("0150.sample-pass", "0504.app-entry", "05.06", "valid-complete", payload=False)
        result = rp.apply_run(str(self.root), [str(source)])
        self.assertEqual(result["exit"], 0)
        self.assertTrue(result["complete"])
        self.assertEqual(result["items"][0]["status"], "placed")
        self.assertTrue(result["items"][0]["custody_valid"])
        self.assertTrue(result["items"][0]["line_adoption"])
        self.assertEqual(result["items"][0]["copy_progress"], "copied")
        self.assertIsNone(result["items"][0]["acceptance"])
        self.assertFalse(result["items"][0]["approved"])
        tail = self.root / "0104.app-entry" / "05.06.return.md"
        self.assertEqual(tail.read_bytes(), b"RETURN\n")

    def test_expected_incomplete_package_stays_visible(self) -> None:
        source = self.make_member("0154.colab-support-first-0501", "0510.colab-tools", "05.01", "expected-incomplete", ret=None)
        result = rp.apply_run(str(self.root), [str(source)])
        self.assertEqual(result["items"][0]["status"], "incomplete")
        self.assertFalse(result["complete"])
        self.assertFalse(result["items"][0]["custody_valid"])
        self.assertFalse(result["items"][0]["line_adoption"])
        self.assertFalse((self.root / "0110.colab-tools" / "05.01.return.md").exists())
        found = rp.lookup_run(str(self.root), member="0154.colab-support-first-0501")
        self.assertEqual(found["items"][0]["status"], "incomplete")

    def test_plan_lists_every_occupied_target_line(self) -> None:
        book = self.root / "book"
        source = book / "0104.app-entry-0508"
        seal(source, "0504.app-entry", "05.06", "sub-06", b"ONE\n", [])
        neighbor = book / "0104.legacy-neighbor"
        neighbor.mkdir(parents=True)
        (neighbor / "keep.txt").write_bytes(b"keep")
        files = []
        for path in sorted(source.rglob("*")):
            if path.is_file():
                data = path.read_bytes()
                rel = path.relative_to(book).as_posix()
                files.append({
                    "bytes": len(data),
                    "path": f"00.kernel/00.00.10.work/{rel}",
                    "sha256": hashlib.sha256(data).hexdigest(),
                })
        audit = {
            "cross-source_collisions": {},
            "files": files,
            "records": [{
                "has_receipt": True,
                "old_member": "0104.app-entry-0508",
                "origin": {"batch": "05.06", "book": "00.00.10.work", "page": "0504.app-entry"},
                "route": "matched-workflow-return-line",
                "status": "corrected audit only; migration not applied",
                "submission": "sub-06",
                "target_return": "0104.app-entry/05.06.return.md",
                "verify_exit": 0,
            }],
            "rule_source": "0417.return-placement/06.01.md",
            "schema": "return-placement-audit/2",
        }
        audit_path = self.root / "audit.json"
        audit_path.write_bytes(_bytes(audit))
        before = sorted(path.name for path in book.iterdir())
        plan = rp.build_plan(str(book), str(audit_path))
        self.assertEqual(sorted(path.name for path in book.iterdir()), before)
        self.assertFalse((book / "0104.app-entry").exists())
        self.assertEqual(plan["occupancy_conflict_count"], 1)
        conflict = plan["occupancy_conflicts"][0]
        self.assertEqual(conflict["target_page"], "0104.app-entry")
        self.assertEqual(conflict["occupants"], ["0104.app-entry-0508", "0104.legacy-neighbor"])
        self.assertEqual(conflict["retirement"], "not performed")
        self.assertFalse(conflict["overwrite"])
        self.assertTrue(any(row["kind"] == "occupied-line" for row in plan["collisions"]))
        self.assertFalse(plan["filing_0121"]["creates"])


if __name__ == "__main__":
    unittest.main()
