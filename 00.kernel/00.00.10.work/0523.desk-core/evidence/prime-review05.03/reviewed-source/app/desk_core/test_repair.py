"""Regressions for the desk-core/2 preservation repair. Expected refusals pass."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from app.desk_core.bookio import atomic_write, file_lock
from app.desk_core.identity import Refused, task_binding, task_binding_v1
from app.desk_core.test_loop import REPO, run, task, write

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


class Repair(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.book = str(self.root / "book")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def init(self) -> None:
        code, payload, err = run(["init", "--book", self.book, "--label", "synthetic"])
        self.assertEqual(err, "")
        self.assertEqual(code, 0, payload)

    def seed(self, page: str = "0523", subject: str = "sample", pass_id: str = "01") -> str:
        path = write(self.root, f"task-{page}-{subject}-{pass_id}.json", task(page, subject, pass_id))
        code, payload, err = run(["record-task", "--book", self.book, "--input", path])
        self.assertEqual(err, "")
        self.assertEqual(code, 0, payload)
        binding = payload["task_binding_sha256"]
        reg = write(
            self.root,
            f"reg-{page}-{subject}-{pass_id}.json",
            {
                "page": page,
                "subject": subject,
                "pass": pass_id,
                "synthetic": True,
                "release": {"who": "Director", "date": "2026-10-31", "text": "Synthetic release.\n"},
                "claim": {"worker": "synthetic-worker", "date": "2026-10-31", "text": "Synthetic claim.\n"},
            },
        )
        code, payload, err = run(["register", "--book", self.book, "--input", reg])
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["task_binding_sha256"], binding)
        return binding

    def revise(self, body: str, *, interrupt: bool = False, reason: str = "Supplied synthetic reason.") -> tuple[int, dict]:
        path = write(
            self.root,
            f"revise-{abs(hash((body, interrupt, reason)))}.json",
            task(
                body=body,
                reason=reason,
                authorizing_reference="0523.sample/revision-request",
            ),
        )
        args = ["revise-task", "--book", self.book, "--input", path]
        if interrupt:
            args.append("--interrupt")
        code, payload, err = run(args)
        self.assertEqual(err, "")
        return code, payload

    def test_binary_roundtrip_and_occupied_temp(self) -> None:
        target = self.root / "exact.bin"
        payload = "keep-lf\nkeep-crlf\r\n café — \n".encode("utf-8")
        atomic_write(target, payload)
        self.assertEqual(target.read_bytes(), payload)
        occupied = self.root / "next.bin.tmp"
        occupied.write_bytes(b"prior partial\r\n")
        with self.assertRaises(Refused) as caught:
            atomic_write(self.root / "next.bin", b"replacement\n")
        self.assertEqual(caught.exception.code, "temp-occupied")
        self.assertEqual(occupied.read_bytes(), b"prior partial\r\n")
        self.assertFalse((self.root / "next.bin").exists())

    def test_lock_is_held_and_windows_lock_is_not_a_no_op(self) -> None:
        source = (REPO / "app" / "desk_core" / "bookio.py").read_text(encoding="utf-8")
        self.assertIn("msvcrt.locking", source)
        self.assertIn("LK_LOCK", source)
        self.assertNotIn("nullcontext", source)
        probe = (REPO / "app" / "desk_core" / "test_repair.py").read_text(encoding="utf-8")
        self.assertIn("LK_NBLCK", probe)
        lock_path = self.root / "desk.lock"
        if os.name == "nt":
            script = (
                "import msvcrt, os, sys\n"
                "fd = os.open(sys.argv[1], os.O_RDWR)\n"
                "os.lseek(fd, 0, os.SEEK_SET)\n"
                "try:\n"
                "    msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)\n"
                "except OSError:\n"
                "    sys.exit(0)\n"
                "else:\n"
                "    msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)\n"
                "    sys.exit(1)\n"
            )
        else:
            script = (
                "import fcntl, os, sys\n"
                "fd = os.open(sys.argv[1], os.O_RDWR)\n"
                "try:\n"
                "    fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)\n"
                "except BlockingIOError:\n"
                "    sys.exit(0)\n"
                "sys.exit(1)\n"
            )
        with file_lock(lock_path):
            proc = subprocess.run(
                [sys.executable, "-B", "-c", script, str(lock_path)],
                capture_output=True,
                text=True,
            )
        self.assertEqual(proc.returncode, 0, proc.stderr)

    def test_revision_preserves_bytes_and_interrupt_does_not_replace(self) -> None:
        self.init()
        self.seed()
        source = Path(self.book) / "0523.sample"
        before_task = (source / "05.01.task.json").read_bytes()
        before_face = (source / "05.01.md").read_bytes()
        code, payload = self.revise("Replacement wording that must not land.\n", interrupt=True)
        self.assertEqual(code, 3, payload)
        self.assertFalse(payload["complete"])
        self.assertEqual(payload["outcome"], "partial")
        self.assertEqual((source / "05.01.task.json").read_bytes(), before_task)
        self.assertEqual((source / "05.01.md").read_bytes(), before_face)
        self.assertFalse((source / "05.01.selected.json").exists())
        history = source / "05.01.history" / "0001"
        self.assertEqual((history / "task.json").read_bytes(), before_task)
        self.assertEqual((history / "face.md").read_bytes(), before_face)
        self.assertIn(b"Build the disposable return.", (history / "task.json").read_bytes())
        revision = json.loads((history / "revision.json").read_text(encoding="utf-8"))
        self.assertEqual(revision["selected"], False)
        self.assertEqual(revision["reason"], "Supplied synthetic reason.")
        self.assertEqual(revision["authorizing_reference"], "0523.sample/revision-request")
        frozen = (history / "revision.json").read_bytes()
        code, payload = self.revise("Replacement wording that must not land.\n", interrupt=True)
        self.assertEqual(code, 3, payload)
        self.assertTrue(payload["idempotent"])
        self.assertEqual(len(list((source / "05.01.history").iterdir())), 1)
        code, payload = self.revise("Replacement wording that must not land.\n")
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["outcome"], "selected")
        self.assertEqual(len(list((source / "05.01.history").iterdir())), 1)
        self.assertEqual((history / "revision.json").read_bytes(), frozen)
        self.assertEqual((history / "task.json").read_bytes(), before_task)
        self.assertIn("Replacement wording", (source / "05.01.task.json").read_text(encoding="utf-8"))
        self.assertIn(b"Replacement wording", (source / "05.01.md").read_bytes())
        self.assertIn(b"## Release", (source / "05.01.md").read_bytes())
        self.assertNotIn("Replacement wording", (history / "task.json").read_text(encoding="utf-8"))
        selected = json.loads((source / "05.01.selected.json").read_text(encoding="utf-8"))
        self.assertEqual(selected["request_sha256"], payload["request_sha256"])
        self.assertFalse((source / "05.01.revision-partial.json").exists())
        code, again = self.revise("Replacement wording that must not land.\n")
        self.assertEqual(code, 0, again)
        self.assertTrue(again["idempotent"])
        self.assertEqual(len(list((source / "05.01.history").iterdir())), 1)
        code, shown, err = run(["show", "--book", self.book, "--page", "0523", "--subject", "sample", "--pass", "01"])
        self.assertEqual(err, "")
        self.assertEqual(code, 0, shown)
        self.assertEqual(shown["revision_state"], "selected")
        self.assertIn("claim-stale", shown["conflicts"])

    def test_stale_return_is_not_a_fresh_review(self) -> None:
        self.init()
        binding = self.seed()
        ret = write(
            self.root,
            "return.json",
            {
                "page": "0523",
                "subject": "sample",
                "pass": "01",
                "worker": "synthetic-worker",
                "return_text": "Return for task A.\n",
                "unresolved_questions": [],
                "artifacts": [],
                "synthetic": True,
                "task_binding_sha256": binding,
            },
        )
        code, payload, err = run(["submit-return", "--book", self.book, "--input", ret])
        self.assertEqual(code, 0, payload)
        self.assertEqual(err, "")
        review = write(
            self.root,
            "review.json",
            {
                "page": "0523",
                "subject": "sample",
                "pass": "01",
                "reviewer": "Codex Prime",
                "review_identity": "synthetic-review-01",
                "disposition": "observed",
                "findings": ["Keep this finding."],
                "dissent": "",
                "director_text": "Director text preserved verbatim.\n",
                "unresolved_questions": ["still open"],
                "assessment": "Assessment of task A.\n",
                "next_action": {"actor": "director", "action": "Read task A.\n"},
                "synthetic": True,
            },
        )
        code, payload, err = run(["review", "--book", self.book, "--input", review])
        self.assertEqual(code, 0, payload)
        self.assertFalse(payload["derived"])
        receipt = (Path(self.book) / "0123.sample" / "05.01.receipt.json").read_bytes()
        claim = (Path(self.book) / "0523.sample" / "05.01.claim.json").read_bytes()
        code, payload = self.revise("Task B body.\n", reason="Revise after capture.")
        self.assertEqual(code, 0, payload)
        self.assertNotEqual(payload["task_binding_sha256"], binding)
        code, payload, err = run(["review", "--book", self.book, "--input", review])
        self.assertEqual(err, "")
        self.assertEqual(code, 2, payload)
        self.assertEqual(payload["refusal"], "stale-return")
        self.assertEqual(payload["check"], "receipt-task-identity")
        self.assertEqual(payload["contract"], "desk-core/2")
        self.assertEqual(payload["next_route"], "keep historical return")
        self.assertEqual((Path(self.book) / "0123.sample" / "05.01.receipt.json").read_bytes(), receipt)
        self.assertEqual((Path(self.book) / "0523.sample" / "05.01.claim.json").read_bytes(), claim)
        code, shown, err = run(["recover", "--book", self.book, "--page", "0523", "--subject", "sample", "--pass", "01"])
        self.assertEqual(code, 0, shown)
        self.assertEqual(err, "")
        self.assertFalse(shown["review_fresh"])
        self.assertTrue(shown["derived"])
        self.assertFalse(shown["complete"])
        self.assertFalse(shown["return_matches_task"])
        self.assertEqual(shown["state"], "return-stale")
        review_record = json.loads((Path(self.book) / "0523.sample" / "05.01.review.json").read_text(encoding="utf-8"))
        self.assertEqual(review_record["findings"], ["Keep this finding."])
        self.assertEqual(review_record["director_text"], "Director text preserved verbatim.\n")
        self.assertIn("still open", shown["unresolved_questions"])
        trace = payload["trace_path"]
        refusal = payload["refusal_path"]
        proc = subprocess.run(
            [
                sys.executable,
                "-B",
                "-c",
                (
                    "import json,sys\n"
                    "trace=json.load(open(sys.argv[1],encoding='utf-8'))\n"
                    "refusal=json.load(open(sys.argv[2],encoding='utf-8'))\n"
                    "assert trace['schema']=='desk-core-trace/1'\n"
                    "assert trace['contract']=='desk-core/2'\n"
                    "assert trace['check']=='receipt-task-identity'\n"
                    "assert trace['outcome']=='stale-return'\n"
                    "assert trace['next_route']=='keep historical return'\n"
                    "assert refusal['request']['review_identity']=='synthetic-review-01'\n"
                    "print(trace['prev_sha256'])\n"
                ),
                trace,
                refusal,
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(len(proc.stdout.strip()), 64)

    def test_prefix_and_distinct_source_identity(self) -> None:
        self.init()
        first = self.seed("0523", "sample", "01")
        second = self.seed("0524", "sample", "01")
        self.assertNotEqual(first, second)
        code, shown, err = run(["show", "--book", self.book, "--page", "0523", "--subject", "sample", "--pass", "01"])
        self.assertEqual(code, 0, shown)
        self.assertEqual(err, "")
        self.assertEqual(shown["body"], "Build the disposable return.\n")
        widened = self.seed("1523", "sample", "01")
        self.assertNotEqual(widened, first)
        code, payload, err = run(
            [
                "submit-return",
                "--book",
                self.book,
                "--input",
                write(
                    self.root,
                    "wide-return.json",
                    {
                        "page": "1523",
                        "subject": "sample",
                        "pass": "01",
                        "worker": "synthetic-worker",
                        "return_text": "Wide prefix return.\n",
                        "unresolved_questions": [],
                        "artifacts": [],
                        "synthetic": True,
                        "task_binding_sha256": widened,
                    },
                ),
            ]
        )
        self.assertEqual(code, 0, payload)
        self.assertEqual(err, "")
        self.assertTrue((Path(self.book) / "1123.sample" / "05.01.receipt.json").is_file())
        self.assertFalse((Path(self.book) / "0123.sample").exists())
        colab = self.seed("1702", "colab-sample", "01")
        code, payload, err = run(
            [
                "submit-return",
                "--book",
                self.book,
                "--input",
                write(
                    self.root,
                    "colab-return.json",
                    {
                        "page": "1702",
                        "subject": "colab-sample",
                        "pass": "01",
                        "worker": "synthetic-worker",
                        "return_text": "Page local return.\n",
                        "unresolved_questions": [],
                        "artifacts": [],
                        "synthetic": True,
                        "task_binding_sha256": colab,
                    },
                ),
            ]
        )
        self.assertEqual(code, 0, payload)
        self.assertTrue((Path(self.book) / "1702.colab-sample" / "05.01.return.md").is_file())
        self.assertEqual(list(Path(self.book).glob("1102.*")), [])
        self.assertEqual(list(Path(self.book).glob("0102.*")), [])
        content = {
            "title": "Synthetic task",
            "body": "Build the disposable return.\n",
            "expected_outputs": ["return text", "notes artifact"],
            "scope": {"in": ["disposable book"], "out": ["live work book"]},
            "agreement": "Synthetic agreement v1.\n",
            "bound_evidence": [
                {
                    "name": "pack",
                    "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                    "bytes": 4,
                }
            ],
        }
        self.assertNotEqual(
            task_binding({**content, "page": "0523", "subject": "sample", "pass": "01", "kind": "N5NN"}),
            task_binding_v1(content),
        )

    def test_version1_task_preimage_still_recomputes(self) -> None:
        self.init()
        self.seed()
        path = Path(self.book) / "0523.sample" / "05.01.task.json"
        stored = json.loads(path.read_text(encoding="utf-8"))
        content = {
            "title": stored["title"],
            "body": stored["body"],
            "expected_outputs": stored["expected_outputs"],
            "scope": stored["scope"],
            "agreement": stored["agreement"],
            "bound_evidence": stored["bound_evidence"],
        }
        stored["schema"] = "desk-core-task/1"
        stored["binding_schema"] = "desk-core-task-binding/1"
        stored["task_binding_sha256"] = task_binding_v1(content)
        path.write_text(json.dumps(stored), encoding="utf-8")
        code, shown, err = run(["show", "--book", self.book, "--page", "0523", "--subject", "sample", "--pass", "01"])
        self.assertEqual(err, "")
        self.assertEqual(code, 0, shown)
        self.assertNotEqual(shown.get("refusal"), "task-binding")
        stored["task_binding_sha256"] = "c" * 64
        path.write_text(json.dumps(stored), encoding="utf-8")
        code, payload, err = run(["show", "--book", self.book, "--page", "0523", "--subject", "sample", "--pass", "01"])
        self.assertEqual(code, 2, payload)
        self.assertEqual(payload["refusal"], "task-binding")

    def test_crlf_utf8_preserves_outside_bytes(self) -> None:
        from app.desk_core import face

        self.init()
        path = write(self.root, "cafe.json", task(body="Build the café return.\n"))
        code, payload, err = run(["record-task", "--book", self.book, "--input", path])
        self.assertEqual(err, "")
        self.assertEqual(code, 0, payload)
        face_path = Path(self.book) / "0523.sample" / "05.01.md"
        original = face_path.read_bytes()
        self.assertIn("café".encode("utf-8"), original)
        crlf = original.replace(b"\n", b"\r\n")
        face_path.write_bytes(crlf)
        code, shown, err = run(["show", "--book", self.book, "--page", "0523", "--subject", "sample", "--pass", "01"])
        self.assertEqual(err, "")
        self.assertEqual(code, 0, shown)
        self.assertEqual(shown["body"], "Build the café return.\n")
        self.assertNotIn("assignment-projection-conflict", shown["conflicts"])
        self.assertEqual(face_path.read_bytes(), crlf)
        claim_at = crlf.find(b"## Claim\r\n")
        pointer_at = crlf.find(b"## Return pointer\r\n")
        updated = face.replace_body(crlf, face.CLAIM, "worker: still-outside\n")
        self.assertEqual(updated[:claim_at], crlf[:claim_at])
        self.assertEqual(updated[updated.find(b"## Return pointer\r\n") :], crlf[pointer_at:])
        self.assertIn(b"## Release\r\n", updated)
        self.assertIn(b"\r\n", updated)

    def test_cr_only_heading_names_the_format(self) -> None:
        self.init()
        self.seed()
        face_path = Path(self.book) / "0523.sample" / "05.01.md"
        face_path.write_bytes(face_path.read_bytes().replace(b"\n", b"\r"))
        code, payload, err = run(["show", "--book", self.book, "--page", "0523", "--subject", "sample", "--pass", "01"])
        self.assertEqual(err, "")
        self.assertEqual(code, 2, payload)
        self.assertEqual(payload["refusal"], "face-format")
        self.assertEqual(payload["format"], "cr-only")
        self.assertNotIn("missing", payload["message"])


if __name__ == "__main__":
    unittest.main()
