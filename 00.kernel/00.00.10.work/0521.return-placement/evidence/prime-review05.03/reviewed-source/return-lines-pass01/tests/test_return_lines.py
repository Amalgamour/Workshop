"""Fixture tests for the line/pass route and staged migration."""

from __future__ import annotations

import hashlib
import io
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
import return_lines as rl


def _bytes(body: dict) -> bytes:
    return (json.dumps(body, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def seal(folder: Path, page: str, batch: str, submission: str,
         ret: bytes | None, payloads: list[bytes] | None = None) -> None:
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


def record_for(name: str, page: str, batch: str, submission: str, verify_exit: int) -> dict:
    route = rl.route_for("00.00.10.work", page, batch)
    return {
        "has_receipt": verify_exit == 0,
        "old_member": name,
        "origin": {"batch": batch, "book": "00.00.10.work", "page": page},
        "route": route["route"],
        "submission": submission,
        "target_return": route["return_path"],
        "verify_exit": verify_exit,
    }


def write_audit(root: Path, book: Path, records: list[dict]) -> Path:
    files = []
    for rec in records:
        member = book / rec["old_member"]
        for dirpath, _dirnames, filenames in os.walk(member):
            for filename in filenames:
                path = Path(dirpath) / filename
                data = path.read_bytes()
                rel = path.relative_to(member).as_posix()
                files.append({
                    "bytes": len(data),
                    "path": f"book/{rec['old_member']}/{rel}",
                    "sha256": _sha(data),
                })
    body = {
        "files": files,
        "order": "ascending old member",
        "records": records,
        "rule_source": "0417.return-placement/06.01.md",
        "schema": "return-placement-audit/2",
    }
    path = root / "audit.json"
    path.write_bytes(_bytes(body))
    return path


class ReturnLineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.outer = tempfile.TemporaryDirectory()
        self.root = Path(self.outer.name)
        self.book = self.root / "book"
        self.backup = self.root / "backup"
        self.book.mkdir()
        os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

    def tearDown(self) -> None:
        self.outer.cleanup()

    def init(self) -> None:
        result = rl.init_run(str(self.book), "00.00.10.work")
        self.assertEqual(result["exit"], 0, result)

    def test_source_does_not_call_allocator(self) -> None:
        text = (LAB / "return_lines.py").read_text(encoding="utf-8")
        self.assertNotIn("import return_capture", text)
        self.assertNotIn("reserve(", text)
        placement = LAB.parents[1] / "labs" / "return-placement-pass01" / "return_placement.py"
        reader = LAB.parents[1] / "labs" / "return-capture-pass01" / "return_capture.py"
        self.assertEqual(_sha(placement.read_bytes()), rl.PLACEMENT_SHA)
        self.assertEqual(placement.stat().st_size, rl.PLACEMENT_BYTES)
        self.assertEqual(_sha(reader.read_bytes()), rl.READER_SHA)
        self.assertEqual(reader.stat().st_size, rl.READER_BYTES)

    def test_routes_and_two_passes_and_local(self) -> None:
        self.init()
        cases = [
            ("0504.app-entry", "05.21", "0104.app-entry", "matched-workflow-return-line"),
            ("1504.app-entry", "05.04", "1104.app-entry", "matched-workflow-return-line"),
            ("9504.x", "05.01", "9104.x", "matched-workflow-return-line"),
            ("0701.bench-method", "05.01", "0701.bench-method", "page-local-colab"),
            ("1701.other", "05.01", "1701.other", "page-local-colab"),
            ("1702.design", "05.02", "1702.design", "page-local-colab"),
            ("0521.return-placement", "05.03", "0121.return-placement", "matched-workflow-return-line"),
        ]
        for page, batch, target, route_name in cases:
            result = rl.reserve_run(
                str(self.book), page, batch, f"sub-{batch}-{page[:4]}", ["note.md"],
                "grok-1", "codex-prime", "prepared", None,
            )
            self.assertEqual(result["exit"], 1, result)
            self.assertEqual(result["descriptor"]["target_page"], target)
            self.assertEqual(result["descriptor"]["route"], route_name)
            self.assertEqual(result["descriptor"]["state"], "reserved")
            self.assertIsNone(result["descriptor"]["return_sha256"])
            self.assertIsNone(result["descriptor"]["return_bytes"])
        refused = rl.reserve_run(
            str(self.book), "0201.nope", "05.01", "sub-bad", ["note.md"],
            "grok-1", "codex-prime", "prepared", None,
        )
        self.assertEqual(refused["exit"], 2)
        self.assertEqual(refused["state"], "refused")
        self.assertIn("0417.return-placement/06.01.md", refused["correction"])
        for page in ("0301.nope", "0401.nope", "0601.nope", "1201.nope"):
            again = rl.reserve_run(
                str(self.book), page, "05.01", "sub-bad", ["note.md"],
                "grok-1", "codex-prime", "prepared", None,
            )
            self.assertEqual(again["exit"], 2, page)
        first = self.book / "0104.app-entry"
        second = rl.reserve_run(
            str(self.book), "0504.app-entry", "05.22", "sub-second", ["note.md"],
            "grok-1", "codex-prime", "prepared", None,
        )
        self.assertEqual(second["exit"], 1, second)
        self.assertEqual(second["descriptor"]["target_page"], "0104.app-entry")
        names = [path.name for path in self.book.iterdir() if path.name.startswith("0104.")]
        self.assertEqual(names, ["0104.app-entry"])
        self.assertTrue((first / "05.21.custody" / "reservation.json").is_file())
        self.assertTrue((first / "05.22.custody" / "reservation.json").is_file())

    def test_capture_verify_conflict_and_descriptor(self) -> None:
        self.init()
        reserved = rl.reserve_run(
            str(self.book), "0504.app-entry", "05.21", "grok-1-0521-0503-synthetic", ["note.md"],
            "grok-1", "codex-prime", "prepared", None,
        )
        self.assertEqual(reserved["descriptor"]["state"], "reserved")
        checked = rl.verify_run(str(self.book), "0504.app-entry", "05.21")
        self.assertEqual(checked["exit"], 1)
        self.assertEqual(checked["descriptor"]["state"], "reserved")
        wrong = rl.capture_run(
            str(self.book), "0504.app-entry", "05.21", "grok-1-0521-0503-synthetic",
            self.write_bytes("return.md", b"SYNTHETIC RETURN\n"),
            [("other.md", self.write_bytes("other.md", b"NO\n"))],
        )
        self.assertEqual(wrong["exit"], 2)
        custody = self.book / "0104.app-entry" / "05.21.custody"
        self.assertEqual(sorted(path.name for path in custody.iterdir()), ["reservation.json"])
        note = self.write_bytes("note.md", b"SYNTHETIC NEW WORK\n")
        ret = self.write_bytes("return.md", b"SYNTHETIC RETURN\n")
        captured = rl.capture_run(
            str(self.book), "0504.app-entry", "05.21", "grok-1-0521-0503-synthetic", ret, [("note.md", note)],
        )
        self.assertEqual(captured["exit"], 0, captured)
        self.assertEqual(captured["descriptor"]["state"], "complete")
        self.assertEqual(set(captured["descriptor"]), rl.DESCRIPTOR_KEYS)
        self.assertEqual(set(captured["descriptor"]["origin"]), {"book", "page", "batch"})
        self.assertEqual(set(captured["descriptor"]["verification"]), rl.VERIFICATION_KEYS)
        self.assertNotIn("acceptance", captured["descriptor"])
        receipt = json.loads((custody / "receipt.json").read_text(encoding="utf-8"))
        self.assertIsNone(receipt["acceptance"])
        self.assertFalse(receipt["approved"])
        self.assertFalse(receipt["accepted"])
        self.assertFalse(receipt["published"])
        self.assertEqual(captured["descriptor"]["receipt_sha256"], _sha((custody / "receipt.json").read_bytes()))
        self.assertEqual((self.book / "0104.app-entry" / "05.21.return.md").read_bytes(), b"SYNTHETIC RETURN\n")
        again = rl.reserve_run(
            str(self.book), "0504.app-entry", "05.21", "grok-1-0521-0503-synthetic", ["note.md"],
            "grok-1", "codex-prime", "prepared", None,
        )
        self.assertEqual(again["exit"], 0, again)
        self.assertEqual(_sha((custody / "reservation.json").read_bytes()), _sha((custody / "reservation.json").read_bytes()))
        recaptured = rl.capture_run(
            str(self.book), "0504.app-entry", "05.21", "grok-1-0521-0503-synthetic", ret, [("note.md", note)],
        )
        self.assertEqual(recaptured["exit"], 0, recaptured)
        self.assertEqual(recaptured["descriptor"]["receipt_sha256"], captured["descriptor"]["receipt_sha256"])
        conflict = rl.capture_run(
            str(self.book), "0504.app-entry", "05.21", "grok-1-0521-0503-synthetic",
            self.write_bytes("other-return.md", b"OTHER\n"), [("note.md", note)],
        )
        self.assertEqual(conflict["exit"], 2, conflict)
        self.assertEqual(conflict["state"], "conflict")
        self.assertEqual((self.book / "0104.app-entry" / "05.21.return.md").read_bytes(), b"SYNTHETIC RETURN\n")
        refused = list((self.book / "0104.app-entry" / "05.21.refused").glob("attempt-*"))
        self.assertEqual(len(refused), 1)
        original = (custody / "receipt.json").read_bytes()
        (custody / "receipt.json").write_bytes(original.replace(b"false", b"true1", 1))
        tampered = rl.verify_run(str(self.book), "0504.app-entry", "05.21")
        self.assertNotEqual(tampered["descriptor"]["state"], "complete")
        self.assertEqual(tampered["exit"], 2)

    def test_live_book_and_door_refused(self) -> None:
        live = Path(rl.live_book_path())
        layout = live / "return-line-layout.json"
        self.assertFalse(layout.exists())
        refused = rl.init_run(str(live), "00.00.10.work")
        self.assertEqual(refused["exit"], 2)
        self.assertEqual(refused["check"], "live book")
        self.assertFalse(layout.exists())
        self.init()
        (self.book / "0100.band.returns").mkdir()
        door = rl.reserve_run(
            str(self.book), "0504.app-entry", "05.21", "sub", ["note.md"],
            "grok-1", "codex-prime", "prepared", None,
        )
        self.assertEqual(door["exit"], 2)
        self.assertEqual(door["check"], "live book")

    def test_stage_interrupt_stale_adopt_rollback_and_incomplete(self) -> None:
        self.init()
        seal(self.book / "0101.app-entry-0506", "0504.app-entry", "05.06", "sub-a", b"RETURN-A\n", [b"payload-a", b"payload-b"])
        seal(self.book / "0104.app-entry-0508", "0504.app-entry", "05.08", "sub-b", b"RETURN-B\n", [b"payload-c"])
        seal(self.book / "0154.colab-support-first-0501", "0510.colab-tools", "05.01", "sub-154", None, None)
        seal(self.book / "0165.bench-method-colab-0501", "0701.bench-method", "05.01", "sub-n7", b"LOCAL\n", [b"local"])
        tail = self.book / "0701.bench-method" / "05.01.return.md"
        tail.parent.mkdir()
        tail.write_bytes(b"LOCAL\n")
        records = [
            record_for("0101.app-entry-0506", "0504.app-entry", "05.06", "sub-a", 0),
            record_for("0104.app-entry-0508", "0504.app-entry", "05.08", "sub-b", 0),
            record_for("0154.colab-support-first-0501", "0510.colab-tools", "05.01", "sub-154", 1),
            record_for("0165.bench-method-colab-0501", "0701.bench-method", "05.01", "sub-n7", 0),
        ]
        audit = write_audit(self.root, self.book, records)
        stale_path = self.book / "0101.app-entry-0506" / "return.md"
        original = stale_path.read_bytes()
        stale_path.write_bytes(b"STALE\n")
        stale = rl.stage_run(str(self.book), str(self.backup), str(audit))
        self.assertEqual(stale["exit"], 2, stale)
        self.assertFalse((self.backup / "stage-complete.json").exists())
        self.assertEqual(stale_path.read_bytes(), b"STALE\n")
        stale_path.write_bytes(original)
        interrupted = rl.stage_run(str(self.book), str(self.backup), str(audit), interrupt_after=1)
        self.assertEqual(interrupted["exit"], 3, interrupted)
        self.assertFalse((self.backup / "stage-complete.json").exists())
        resumed = rl.stage_run(str(self.book), str(self.backup), str(audit), resume=True)
        self.assertEqual(resumed["exit"], 0, resumed)
        self.assertTrue((self.backup / "stage-complete.json").is_file())
        self.assertTrue((self.book / "0104.app-entry-0508").is_dir())
        adopted = rl.adopt_run(str(self.book), str(self.backup), str(audit))
        self.assertEqual(adopted["exit"], 0, adopted)
        self.assertFalse((self.book / "0104.app-entry-0508").exists())
        self.assertTrue((self.backup / "retired" / "0104.app-entry-0508").is_dir())
        self.assertTrue((self.book / "0101.app-entry-0506").is_dir())
        line = self.book / "0104.app-entry"
        self.assertEqual((line / "05.06.return.md").read_bytes(), b"RETURN-A\n")
        self.assertEqual((line / "05.08.return.md").read_bytes(), b"RETURN-B\n")
        self.assertEqual((line / "05.06.custody" / "return.md").read_bytes(), b"RETURN-A\n")
        reservation = (line / "05.06.custody" / "reservation.json").read_bytes()
        self.assertEqual(reservation, (self.backup / "sources" / "0101.app-entry-0506" / "reservation.json").read_bytes())
        relocation = json.loads((line / "05.06.custody" / "relocation.json").read_text(encoding="utf-8"))
        self.assertFalse(relocation["reservation_destination_rewritten"])
        self.assertEqual(relocation["custody_format"], "legacy-relocated/1")
        by_member = rl.lookup_run(str(self.book), member="0101.app-entry-0506")
        by_origin = rl.lookup_run(str(self.book), page="0504.app-entry", batch="05.06")
        self.assertEqual(by_member["exit"], 0, by_member)
        self.assertEqual(by_origin["exit"], 0, by_origin)
        self.assertEqual(by_member["descriptor"]["return_sha256"], by_origin["descriptor"]["return_sha256"])
        self.assertEqual(by_member["descriptor"]["return_sha256"], _sha(b"RETURN-A\n"))
        incomplete = rl.lookup_run(str(self.book), member="0154.colab-support-first-0501")
        self.assertEqual(incomplete["exit"], 1, incomplete)
        self.assertEqual(incomplete["descriptor"]["state"], "incomplete")
        self.assertIsNone(incomplete["descriptor"]["return_sha256"])
        self.assertFalse((self.book / "0110.colab-tools" / "05.01.return.md").exists())
        self.assertEqual((self.book / "0701.bench-method" / "05.01.return.md").read_bytes(), b"LOCAL\n")
        rolled = rl.rollback_adopt_run(str(self.book), str(self.backup))
        self.assertEqual(rolled["exit"], 0, rolled)
        self.assertTrue((self.book / "0104.app-entry-0508").is_dir())
        self.assertFalse((self.book / "0104.app-entry").exists())
        self.assertEqual((self.book / "0101.app-entry-0506" / "return.md").read_bytes(), b"RETURN-A\n")
        self.assertEqual((self.book / "0701.bench-method" / "05.01.return.md").read_bytes(), b"LOCAL\n")

    def test_tail_changed_after_stage_blocks_adopt(self) -> None:
        self.init()
        seal(self.book / "0165.bench-method-colab-0501", "0701.bench-method", "05.01", "sub-n7", b"LOCAL\n", [b"local"])
        tail = self.book / "0701.bench-method" / "05.01.return.md"
        tail.parent.mkdir()
        tail.write_bytes(b"LOCAL\n")
        audit = write_audit(self.root, self.book, [
            record_for("0165.bench-method-colab-0501", "0701.bench-method", "05.01", "sub-n7", 0),
        ])
        staged = rl.stage_run(str(self.book), str(self.backup), str(audit))
        self.assertEqual(staged["exit"], 0, staged)
        tail.write_bytes(b"DIFFERENT\n")
        adopted = rl.adopt_run(str(self.book), str(self.backup), str(audit))
        self.assertEqual(adopted["exit"], 2, adopted)
        self.assertEqual(tail.read_bytes(), b"DIFFERENT\n")
        self.assertFalse((self.backup / "adopt-complete.json").exists())
        self.assertTrue((self.book / "0165.bench-method-colab-0501").is_dir())

    def test_cli_descriptor_shape(self) -> None:
        self.init()
        note = self.write_bytes("note.md", b"SYNTHETIC NEW WORK\n")
        ret = self.write_bytes("return.md", b"SYNTHETIC RETURN\n")
        self.assertEqual(rl.reserve_run(
            str(self.book), "0504.app-entry", "05.21", "grok-1-0521-0503-synthetic", ["note.md"],
            "grok-1", "codex-prime", "prepared", None,
        )["exit"], 1)
        self.assertEqual(rl.capture_run(
            str(self.book), "0504.app-entry", "05.21", "grok-1-0521-0503-synthetic", ret, [("note.md", note)],
        )["exit"], 0)
        buffer = io.BytesIO()
        wrapper = io.TextIOWrapper(buffer, encoding="utf-8", newline="\n")
        stdout = sys.stdout
        sys.stdout = wrapper
        try:
            code = rl.main([
                "descriptor", "--book", str(self.book), "--page", "0504.app-entry", "--batch", "05.21",
            ])
            wrapper.flush()
        finally:
            sys.stdout = stdout
            wrapper.detach()
        self.assertEqual(code, 0)
        body = json.loads(buffer.getvalue().decode("utf-8"))
        self.assertEqual(set(body), rl.DESCRIPTOR_KEYS)
        self.assertEqual(body["state"], "complete")
        self.assertEqual(body["custody_format"], "return-line-capture/1")

    def write_bytes(self, name: str, data: bytes) -> str:
        path = self.root / name
        path.write_bytes(data)
        return str(path)


if __name__ == "__main__":
    unittest.main()
