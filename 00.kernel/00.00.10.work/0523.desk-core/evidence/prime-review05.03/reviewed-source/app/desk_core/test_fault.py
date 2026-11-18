"""Crash boundaries inside revision writes, then a fresh process recovers the book."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from app.desk_core.test_loop import REPO, task, write

BODY_B = "Proposal B wording.\n"


def _run(args: list[str], *, fault: str | None = None) -> tuple[int, dict]:
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    if fault is None:
        env.pop("DESK_CORE_FAULT", None)
    else:
        env["DESK_CORE_FAULT"] = fault
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "app.desk_core", *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        env=env,
    )
    try:
        payload = json.loads(proc.stdout) if proc.stdout else {}
    except json.JSONDecodeError:
        payload = {"_raw": proc.stdout, "_stderr": proc.stderr}
    return proc.returncode, payload


class FaultMatrix(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.book = str(self.root / "book")
        self.rows: list[dict[str, object]] = []

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def init_captured(self) -> str:
        code, payload = _run(["init", "--book", self.book, "--label", "synthetic"])
        self.assertEqual(code, 0, payload)
        spec = write(self.root, "task.json", task())
        code, payload = _run(["record-task", "--book", self.book, "--input", spec])
        self.assertEqual(code, 0, payload)
        binding = payload["task_binding_sha256"]
        reg = write(
            self.root,
            "register.json",
            {
                "page": "0523",
                "subject": "sample",
                "pass": "01",
                "synthetic": True,
                "release": {"who": "Director", "date": "2026-11-01", "text": "Synthetic release.\n"},
                "claim": {"worker": "synthetic-worker", "date": "2026-11-01", "text": "Synthetic claim.\n"},
            },
        )
        code, payload = _run(["register", "--book", self.book, "--input", reg])
        self.assertEqual(code, 0, payload)
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
        code, payload = _run(["submit-return", "--book", self.book, "--input", ret])
        self.assertEqual(code, 0, payload)
        return binding

    def revise_path(self, body: str, reason: str) -> str:
        return write(
            self.root,
            f"revise-{reason}.json",
            task(body=body, reason=reason, authorizing_reference="0523.sample/revision-request"),
        )

    def source(self) -> Path:
        return Path(self.book) / "0523.sample"

    def receipt(self) -> bytes:
        return (Path(self.book) / "0123.sample" / "05.01.receipt.json").read_bytes()

    def show(self) -> dict:
        code, payload = _run(["show", "--book", self.book, "--page", "0523", "--subject", "sample", "--pass", "01"])
        self.assertEqual(code, 0, payload)
        return payload

    def recover(self) -> dict:
        code, payload = _run(["recover", "--book", self.book, "--page", "0523", "--subject", "sample", "--pass", "01"])
        self.assertEqual(code, 0, payload)
        return payload

    def assert_not_fresh_b(self, shown: dict, binding_a: str) -> None:
        self.assertFalse(shown["review_fresh"])
        self.assertFalse(shown["accepted"])
        if shown["task_binding_sha256"] != binding_a:
            code, payload = _run(
                ["review", "--book", self.book, "--input", self._review_input()]
            )
            self.assertEqual(code, 2, payload)
            self.assertEqual(payload["refusal"], "stale-return")
            self.assertIn("receipt-task-identity", payload["check"])

    def _review_input(self) -> str:
        return write(
            self.root,
            "review.json",
            {
                "page": "0523",
                "subject": "sample",
                "pass": "01",
                "reviewer": "Codex Prime",
                "review_identity": "after-crash",
                "disposition": "not a fresh review of B",
                "findings": ["Keep the A return historical."],
                "dissent": "",
                "director_text": "",
                "unresolved_questions": [],
                "assessment": "Synthetic judgment. Not acceptance.\n",
                "next_action": {"actor": "prime", "action": "Do not treat the old return as fresh.\n"},
                "synthetic": True,
            },
        )

    def test_each_write_boundary_recovers_in_a_new_process(self) -> None:
        cases = [
            ("before-prior-task", "none", "A"),
            ("after-prior-task", "retained-previous", "A"),
            ("after-prior-face", "retained-previous", "A"),
            ("after-proposed-task", "retained-previous", "A"),
            ("after-proposed-face", "retained-previous", "A"),
            ("after-revision-journal", "retained-previous", "A"),
            ("after-task-replacement", "restored-previous", "A"),
            ("after-face-replacement", "completed-proposal", "B"),
        ]
        for boundary, outcome, who in cases:
            with self.subTest(boundary=boundary):
                self.tmp.cleanup()
                self.tmp = tempfile.TemporaryDirectory()
                self.root = Path(self.tmp.name)
                self.book = str(self.root / "book")
                binding = self.init_captured()
                source = self.source()
                before_task = (source / "05.01.task.json").read_bytes()
                before_face = (source / "05.01.md").read_bytes()
                receipt = self.receipt()
                spec = self.revise_path(BODY_B, f"reason-{boundary}")
                code, payload = _run(
                    ["revise-task", "--book", self.book, "--input", spec],
                    fault=boundary,
                )
                self.assertEqual(code, 91, payload)
                shown = self.show()
                self.assertFalse(shown["accepted"])
                if shown["revision_state"] in ("partial", "conflict"):
                    self.assertFalse(shown["complete"])
                self.assertFalse(shown["review_fresh"])
                recovered = self.recover()
                self.assertEqual(recovered["recovery"], outcome, recovered)
                self.assertEqual(self.receipt(), receipt)
                again = self.recover()
                self.assertEqual((source / "05.01.task.json").read_bytes(), (source / "05.01.task.json").read_bytes())
                task_after = (source / "05.01.task.json").read_bytes()
                face_after = (source / "05.01.md").read_bytes()
                if who == "A":
                    self.assertEqual(task_after, before_task)
                    self.assertEqual(face_after, before_face)
                    self.assertEqual(again["task_binding_sha256"], binding)
                else:
                    self.assertIn(b"Proposal B wording", task_after)
                    self.assertNotEqual(task_after, before_task)
                    self.assertTrue((source / "05.01.selected.json").is_file())
                    self.assertEqual(again["revision_state"], "selected")
                    self.assertFalse(again["complete"])
                self.assert_not_fresh_b(again, binding)
                self.assertEqual(self.receipt(), receipt)
                self.assertEqual((source / "05.01.task.json").read_bytes(), task_after)
                self.assertEqual((source / "05.01.md").read_bytes(), face_after)
                history = source / "05.01.history"
                if boundary == "before-prior-task":
                    self.assertFalse(history.exists())
                else:
                    self.assertIn(b"Build the disposable return.", (history / "0001" / "task.json").read_bytes())
                traces = list((source / "05.01.trace").glob("*.json"))
                self.assertTrue(any(boundary.encode() in item.read_bytes() for item in traces))
                self.rows.append(
                    {
                        "boundary": boundary,
                        "command": f"DESK_CORE_FAULT={boundary} python3.11 -B -m app.desk_core revise-task --book <book> --input revise.json",
                        "injected_exit": code,
                        "before_task_sha256": hashlib.sha256(before_task).hexdigest(),
                        "after_task_sha256": hashlib.sha256(task_after).hexdigest(),
                        "before_face_sha256": hashlib.sha256(before_face).hexdigest(),
                        "after_face_sha256": hashlib.sha256(face_after).hexdigest(),
                        "receipt_sha256": hashlib.sha256(receipt).hexdigest(),
                        "show_revision_state": shown["revision_state"],
                        "show_complete": shown["complete"],
                        "recovery": outcome,
                        "second_recovery": again["recovery"],
                        "live_pair": who,
                        "receipt_unchanged": True,
                        "expected": outcome,
                        "assertion": "passed",
                    }
                )
        self._cleanup_boundary_row()
        target = os.environ.get("DESK_CORE_MATRIX")
        if target and self.rows:
            Path(target).write_text(json.dumps(self.rows, indent=2) + "\n", encoding="utf-8")

    def _cleanup_boundary_row(self) -> None:
        self.tmp.cleanup()
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.book = str(self.root / "book")
        binding = self.init_captured()
        source = self.source()
        before_task = (source / "05.01.task.json").read_bytes()
        before_face = (source / "05.01.md").read_bytes()
        receipt = self.receipt()
        spec = self.revise_path(BODY_B, "cleanup-matrix")
        code, payload = _run(["revise-task", "--book", self.book, "--input", spec, "--interrupt"])
        self.assertEqual(code, 3, payload)
        code, payload = _run(
            ["revise-task", "--book", self.book, "--input", spec],
            fault="after-selection-before-cleanup",
        )
        self.assertEqual(code, 91, payload)
        shown = self.show()
        self.assertEqual(shown["revision_state"], "selected")
        self.assertFalse(shown["complete"])
        recovered = self.recover()
        self.assertEqual(recovered["recovery"], "cleaned-marker")
        again = self.recover()
        self.assertEqual(again["recovery"], "idempotent")
        self.assertEqual(self.receipt(), receipt)
        self.assert_not_fresh_b(again, binding)
        task_after = (source / "05.01.task.json").read_bytes()
        face_after = (source / "05.01.md").read_bytes()
        self.assertEqual((source / "05.01.history" / "0001" / "task.json").read_bytes(), before_task)
        self.rows.append(
            {
                "boundary": "after-selection-before-cleanup",
                "command": "revise-task --interrupt, then DESK_CORE_FAULT=after-selection-before-cleanup revise-task",
                "injected_exit": code,
                "before_task_sha256": hashlib.sha256(before_task).hexdigest(),
                "after_task_sha256": hashlib.sha256(task_after).hexdigest(),
                "before_face_sha256": hashlib.sha256(before_face).hexdigest(),
                "after_face_sha256": hashlib.sha256(face_after).hexdigest(),
                "receipt_sha256": hashlib.sha256(receipt).hexdigest(),
                "show_revision_state": shown["revision_state"],
                "show_complete": shown["complete"],
                "recovery": "cleaned-marker",
                "second_recovery": again["recovery"],
                "live_pair": "B",
                "receipt_unchanged": True,
                "expected": "cleaned-marker",
                "assertion": "passed",
            }
        )

    def test_selection_cleanup_and_same_request_resume(self) -> None:
        binding = self.init_captured()
        source = self.source()
        before_task = (source / "05.01.task.json").read_bytes()
        receipt = self.receipt()
        spec = self.revise_path(BODY_B, "cleanup")
        code, payload = _run(["revise-task", "--book", self.book, "--input", spec, "--interrupt"])
        self.assertEqual(code, 3, payload)
        code, payload = _run(
            ["revise-task", "--book", self.book, "--input", spec],
            fault="after-selection-before-cleanup",
        )
        self.assertEqual(code, 91, payload)
        self.assertTrue((source / "05.01.revision-partial.json").is_file())
        self.assertTrue((source / "05.01.selected.json").is_file())
        shown = self.show()
        self.assertEqual(shown["revision_state"], "selected")
        self.assertFalse(shown["complete"])
        recovered = self.recover()
        self.assertEqual(recovered["recovery"], "cleaned-marker")
        self.assertFalse((source / "05.01.revision-partial.json").exists())
        selected = (source / "05.01.selected.json").read_bytes()
        again = self.recover()
        self.assertEqual(again["recovery"], "idempotent")
        self.assertEqual((source / "05.01.selected.json").read_bytes(), selected)
        self.assertEqual(self.receipt(), receipt)
        self.assert_not_fresh_b(again, binding)
        self.assertEqual(len(list((source / "05.01.history").iterdir())), 1)
        self.assertEqual((source / "05.01.history" / "0001" / "task.json").read_bytes(), before_task)

    def test_resume_does_not_duplicate_history(self) -> None:
        self.init_captured()
        source = self.source()
        before_task = (source / "05.01.task.json").read_bytes()
        spec = self.revise_path(BODY_B, "resume")
        code, _payload = _run(["revise-task", "--book", self.book, "--input", spec], fault="after-prior-task")
        self.assertEqual(code, 91)
        self.assertFalse((source / "05.01.history" / "0001" / "revision.json").exists())
        code, payload = _run(["revise-task", "--book", self.book, "--input", spec])
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["outcome"], "selected")
        self.assertEqual(len(list((source / "05.01.history").iterdir())), 1)
        self.assertEqual((source / "05.01.history" / "0001" / "task.json").read_bytes(), before_task)
        self.assertIn(b"Proposal B wording", (source / "05.01.task.json").read_bytes())

    def test_corrupt_and_other_request_keep_the_files(self) -> None:
        self.init_captured()
        source = self.source()
        before_task = (source / "05.01.task.json").read_bytes()
        spec = self.revise_path(BODY_B, "sealed")
        code, payload = _run(["revise-task", "--book", self.book, "--input", spec, "--interrupt"])
        self.assertEqual(code, 3, payload)
        proposal = source / "05.01.history" / "0001" / "proposed-face.md"
        proposal.unlink()
        code, payload = _run(["revise-task", "--book", self.book, "--input", spec])
        self.assertEqual(code, 2, payload)
        self.assertEqual(payload["refusal"], "revision-corrupt")
        self.assertEqual(payload["missing"], "proposed-face.md")
        self.assertEqual((source / "05.01.task.json").read_bytes(), before_task)
        self.assertTrue((source / "05.01.history" / "0001" / "task.json").is_file())
        self.assertFalse(proposal.exists())
        self.assertEqual(len(list((source / "05.01.history").iterdir())), 1)

    def test_other_request_is_refused_while_one_is_open(self) -> None:
        self.init_captured()
        source = self.source()
        before_task = (source / "05.01.task.json").read_bytes()
        spec = self.revise_path(BODY_B, "open-request")
        code, payload = _run(["revise-task", "--book", self.book, "--input", spec, "--interrupt"])
        self.assertEqual(code, 3, payload)
        frozen = (source / "05.01.history" / "0001" / "revision.json").read_bytes()
        other = self.revise_path("Different proposal.\n", "other-request")
        code, payload = _run(["revise-task", "--book", self.book, "--input", other])
        self.assertEqual(code, 2, payload)
        self.assertEqual(payload["refusal"], "revision-unfinished")
        self.assertIn("next_route", payload)
        self.assertEqual((source / "05.01.task.json").read_bytes(), before_task)
        self.assertEqual((source / "05.01.history" / "0001" / "revision.json").read_bytes(), frozen)
        self.assertEqual(len(list((source / "05.01.history").iterdir())), 1)


if __name__ == "__main__":
    unittest.main()
