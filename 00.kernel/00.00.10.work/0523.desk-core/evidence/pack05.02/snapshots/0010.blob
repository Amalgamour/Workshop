"""Subprocess proof of the disposable desk-core loop. Expected refusals are successes."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

EVIDENCE = {
    "name": "pack",
    "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "bytes": 4,
}


def run(args: list[str]) -> tuple[int, dict, str]:
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "app.desk_core", *args],
        cwd=REPO,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
    )
    try:
        payload = json.loads(proc.stdout) if proc.stdout else {}
    except json.JSONDecodeError:
        payload = {"_raw": proc.stdout}
    return proc.returncode, payload, proc.stderr


def task(page: str = "0523", subject: str = "sample", pass_id: str = "01", **over: object) -> dict:
    body = {
        "page": page,
        "subject": subject,
        "pass": pass_id,
        "title": "Synthetic task",
        "body": "Build the disposable return.\n",
        "expected_outputs": ["return text", "notes artifact"],
        "scope": {"in": ["disposable book"], "out": ["live work book"]},
        "agreement": "Synthetic agreement v1.\n",
        "bound_evidence": [EVIDENCE],
        "synthetic": True,
    }
    body.update(over)
    return body


def write(directory: Path, name: str, payload: dict) -> str:
    path = directory / name
    path.write_text(json.dumps(payload), encoding="utf-8")
    return str(path)


class DeskCoreLoop(unittest.TestCase):
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
        self.assertFalse(payload["accepted"])

    def seed(self, page: str = "0523", subject: str = "sample", pass_id: str = "01") -> str:
        self.init()
        path = write(self.root, f"task-{page}-{pass_id}.json", task(page, subject, pass_id))
        code, payload, err = run(["record-task", "--book", self.book, "--input", path])
        self.assertEqual(err, "")
        self.assertEqual(code, 0, payload)
        binding = payload["task_binding_sha256"]
        reg = write(
            self.root,
            f"reg-{page}-{pass_id}.json",
            {
                "page": page,
                "subject": subject,
                "pass": pass_id,
                "synthetic": True,
                "release": {
                    "who": "Director",
                    "date": "2026-10-31",
                    "text": "Synthetic release for this disposable book only.\n",
                },
                "claim": {
                    "worker": "synthetic-worker",
                    "date": "2026-10-31",
                    "text": "Synthetic claim. Not a real session.\n",
                },
            },
        )
        code, payload, err = run(["register", "--book", self.book, "--input", reg])
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["task_binding_sha256"], binding)
        return binding

    def ret(self, binding: str, text: str = "Synthetic return.\n", page: str = "0523", subject: str = "sample", pass_id: str = "01") -> str:
        return write(
            self.root,
            f"return-{page}-{pass_id}-{abs(hash(text))}.json",
            {
                "page": page,
                "subject": subject,
                "pass": pass_id,
                "worker": "synthetic-worker",
                "return_text": text,
                "unresolved_questions": ["Which sentinel stays?"],
                "artifacts": [{"logical": "notes.md", "text": "synthetic notes\n"}],
                "synthetic": True,
                "task_binding_sha256": binding,
            },
        )

    def judge(self, page: str = "0523", subject: str = "sample", pass_id: str = "01", **over: object) -> str:
        body = {
            "page": page,
            "subject": subject,
            "pass": pass_id,
            "reviewer": "Codex Prime",
            "review_identity": f"synthetic-review-{pass_id}",
            "disposition": "prototype observed; not production acceptance",
            "findings": [],
            "dissent": "",
            "director_text": "Director text preserved verbatim.\n",
            "unresolved_questions": ["Where does migration land?"],
            "assessment": "Full synthetic assessment. Compute constructed the page.\n",
            "next_action": {"actor": "director", "action": "Review the branch before integration.\n"},
            "synthetic": True,
        }
        body.update(over)
        return write(self.root, f"review-{page}-{pass_id}.json", body)

    def show(self, page: str = "0523", subject: str = "sample", pass_id: str = "01") -> tuple[int, dict]:
        code, payload, err = run(
            ["show", "--book", self.book, "--page", page, "--subject", subject, "--pass", pass_id]
        )
        self.assertEqual(err, "")
        return code, payload

    def test_pins_and_live_book_and_undeclared(self) -> None:
        code, payload, err = run(["pins"])
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["matched"], 33)
        self.assertEqual(payload["runtime_imports"], [])
        live = str(REPO / "00.kernel" / "00.00.10.work")
        code, payload, _err = run(["init", "--book", live, "--label", "synthetic"])
        self.assertEqual(code, 2)
        self.assertEqual(payload["refusal"], "live-book-refused")
        self.init()
        for page in ("0417", "0201", "0601", "0123", "1523"):
            path = write(self.root, f"{page}.json", task(page, "sample", "01"))
            code, payload, _err = run(["record-task", "--book", self.book, "--input", path])
            self.assertEqual(code, 2, page)
            self.assertIn(payload["refusal"], {"undeclared-source-kind", "undeclared-source-shape"})
            self.assertFalse(any(self.root.joinpath("book").glob(f"{page}.*")))

    def test_full_loop_restart_and_binding(self) -> None:
        binding = self.seed()
        code, shown = self.show()
        self.assertEqual(code, 0)
        self.assertEqual(shown["state"], "claimed")
        self.assertEqual(shown["body"], "Build the disposable return.\n")
        self.assertEqual(shown["expected_outputs"], ["return text", "notes artifact"])
        self.assertEqual(shown["scope"]["out"], ["live work book"])
        self.assertFalse(shown["complete"])
        path = self.ret(binding)
        code, payload, _err = run(["submit-return", "--book", self.book, "--input", path])
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["task_binding_sha256"], binding)
        code, payload, _err = run(["submit-return", "--book", self.book, "--input", path])
        self.assertEqual(code, 0, payload)
        self.assertTrue(payload["idempotent"])
        code, got, _err = run(
            ["retrieve", "--book", self.book, "--page", "0523", "--subject", "sample", "--pass", "01"]
        )
        self.assertEqual(code, 0, got)
        self.assertEqual(got["return_text"], "Synthetic return.\n")
        self.assertIn("Which sentinel stays?", got["unresolved_questions"])
        self.assertFalse(got["accepted"])
        face_path = Path(self.book) / "0523.sample" / "05.01.md"
        before = face_path.read_bytes()
        review_at = before.index(b"## Review - Codex Prime")
        note_at = before.index(b"## Record note")
        code, payload, _err = run(["review", "--book", self.book, "--input", self.judge()])
        self.assertEqual(code, 0, payload)
        after = face_path.read_bytes()
        self.assertEqual(after[:review_at], before[:review_at])
        self.assertEqual(after[after.index(b"## Record note") :], before[note_at:])
        self.assertIn(b"(none)", after)
        self.assertIn(b"Director text preserved verbatim.", after)
        self.assertIn(b"Where does migration land?", after)
        self.assertIn(b"Full synthetic assessment.", after)
        self.assertIn(b"TAIL-SENTINEL", after)
        self.assertEqual(payload["task_binding_sha256"], binding)
        code, recovered, err = run(
            ["recover", "--book", self.book, "--page", "0523", "--subject", "sample", "--pass", "01"]
        )
        self.assertEqual(err, "")
        self.assertEqual(code, 0, recovered)
        self.assertEqual(recovered["state"], "reviewed")
        self.assertEqual(recovered["next_actor"], "director")
        self.assertFalse(recovered["derived"])
        self.assertIn("Review the branch", recovered["next_action"])
        self.assertFalse(recovered["accepted"])
        self.assertTrue(recovered["complete"])
        record = json.loads((Path(self.book) / "0523.sample" / "05.01.review.json").read_text())
        self.assertEqual(record["findings"], [])
        self.assertEqual(record["director_text"], "Director text preserved verbatim.\n")
        self.assertEqual(record["not_acceptance"], True)
        line = Path(self.book) / "0123.sample"
        self.assertTrue((line / "05.01.receipt.json").is_file())
        self.assertEqual([p.name for p in Path(self.book).glob("0123.*")], ["0123.sample"])

    def test_said_done_without_capture(self) -> None:
        self.seed()
        code, payload, _err = run(
            [
                "assert-done",
                "--book",
                self.book,
                "--page",
                "0523",
                "--subject",
                "sample",
                "--pass",
                "01",
                "--worker",
                "synthetic-worker",
            ]
        )
        self.assertEqual(code, 0, payload)
        self.assertFalse(payload["complete"])
        code, shown = self.show()
        self.assertEqual(shown["state"], "said-done-without-capture")
        self.assertFalse(shown["complete"])
        self.assertFalse(shown["accepted"])
        self.assertFalse((Path(self.book) / "0123.sample" / "05.01.receipt.json").exists())

    def test_changed_bytes_wrong_line_and_hash(self) -> None:
        binding = self.seed()
        path = self.ret(binding)
        code, _payload, _err = run(["submit-return", "--book", self.book, "--input", path])
        self.assertEqual(code, 0)
        receipt = (Path(self.book) / "0123.sample" / "05.01.receipt.json").read_bytes()
        changed = self.ret(binding, text="Different synthetic return.\n")
        code, payload, _err = run(["submit-return", "--book", self.book, "--input", changed])
        self.assertEqual(code, 2)
        self.assertEqual(payload["refusal"], "receipt-conflict")
        self.assertEqual((Path(self.book) / "0123.sample" / "05.01.receipt.json").read_bytes(), receipt)
        code, shown = self.show()
        self.assertIn("receipt-conflict", shown["conflicts"])
        self.assertFalse(shown["accepted"])
        wrong_line = self.ret(binding, text="Synthetic return.\n")
        code, payload, _err = run(
            ["submit-return", "--book", self.book, "--input", wrong_line, "--force-line", "0199.sample"]
        )
        self.assertEqual(code, 2)
        self.assertEqual(payload["refusal"], "wrong-return-line")
        code, payload, _err = run(
            ["submit-return", "--book", self.book, "--input", path, "--force-pass", "02"]
        )
        self.assertEqual(code, 2)
        self.assertEqual(payload["refusal"], "wrong-pass")
        bad = json.loads(Path(path).read_text())
        bad["task_binding_sha256"] = "b" * 64
        bad_path = write(self.root, "bad-hash.json", bad)
        code, payload, _err = run(["submit-return", "--book", self.book, "--input", bad_path])
        self.assertEqual(code, 2)
        self.assertEqual(payload["refusal"], "wrong-source-hash")

    def test_stale_claim_and_review_binding(self) -> None:
        binding = self.seed()
        code, _payload, _err = run(["submit-return", "--book", self.book, "--input", self.ret(binding)])
        self.assertEqual(code, 0)
        code, _payload, _err = run(["review", "--book", self.book, "--input", self.judge()])
        self.assertEqual(code, 0)
        before = (Path(self.book) / "0523.sample" / "05.01.md").read_bytes()
        code, shown = self.show()
        self.assertEqual(shown["task_binding_sha256"], binding)
        self.assertTrue(shown["review_fresh"])
        revised = task(agreement="Synthetic agreement v2.\n")
        path = write(self.root, "revise.json", revised)
        code, payload, _err = run(["revise-task", "--book", self.book, "--input", path])
        self.assertEqual(code, 0, payload)
        self.assertNotEqual(payload["task_binding_sha256"], binding)
        after = (Path(self.book) / "0523.sample" / "05.01.md").read_bytes()
        release_at = before.index(b"## Release")
        self.assertEqual(after[after.index(b"## Release") :], before[release_at:])
        code, shown = self.show()
        self.assertEqual(shown["state"], "review-stale")
        self.assertIn("claim-stale", shown["conflicts"])
        self.assertIn("review-stale", shown["conflicts"])
        self.assertFalse(shown["accepted"])
        self.assertIn("Where does migration land?", shown["unresolved_questions"])
        code, payload, _err = run(
            ["submit-return", "--book", self.book, "--input", self.ret(payload["task_binding_sha256"])]
        )
        self.assertEqual(code, 2)
        self.assertEqual(payload["refusal"], "release-stale")

    def test_each_binding_field_and_interrupt(self) -> None:
        from app.desk_core.identity import task_binding

        base = task()
        base_fields = {
            "title": base["title"],
            "body": base["body"],
            "expected_outputs": base["expected_outputs"],
            "scope": base["scope"],
            "agreement": base["agreement"],
            "bound_evidence": base["bound_evidence"],
        }
        original = task_binding(base_fields)
        for key, value in (
            ("body", "Changed task body.\n"),
            ("agreement", "Changed agreement.\n"),
            (
                "bound_evidence",
                [
                    {
                        "name": "pack",
                        "sha256": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
                        "bytes": 5,
                    }
                ],
            ),
        ):
            changed = dict(base_fields)
            changed[key] = value
            self.assertNotEqual(task_binding(changed), original)
        binding = self.seed()
        code, payload, _err = run(
            ["submit-return", "--book", self.book, "--input", self.ret(binding), "--interrupt"]
        )
        self.assertEqual(code, 3, payload)
        self.assertFalse(payload["complete"])
        self.assertEqual(payload["state"], "partial")
        code, shown = self.show()
        self.assertEqual(shown["state"], "partial")
        self.assertFalse(shown["complete"])
        self.assertFalse((Path(self.book) / "0123.sample" / "05.01.receipt.json").exists())
        code, payload, _err = run(["submit-return", "--book", self.book, "--input", self.ret(binding)])
        self.assertEqual(code, 0, payload)
        code, shown = self.show()
        self.assertEqual(shown["state"], "awaiting-review")
        self.assertTrue(shown["complete"])
        self.assertFalse(shown["accepted"])

    def test_two_passes_one_line_and_colab_and_occupant(self) -> None:
        binding = self.seed()
        code, _payload, _err = run(["submit-return", "--book", self.book, "--input", self.ret(binding)])
        self.assertEqual(code, 0)
        second = self.seed_pass("02")
        code, _payload, _err = run(
            ["submit-return", "--book", self.book, "--input", self.ret(second, pass_id="02")]
        )
        self.assertEqual(code, 0)
        line = Path(self.book) / "0123.sample"
        self.assertTrue((line / "05.01.receipt.json").is_file())
        self.assertTrue((line / "05.02.receipt.json").is_file())
        names = sorted(p.name for p in Path(self.book).iterdir())
        self.assertEqual([name for name in names if name.startswith("0123.")], ["0123.sample"])
        self.assertNotIn("0124.sample", names)
        colab_binding = self.seed_pass("01", page="0702", subject="colab-sample")
        pack = Path(self.book) / "0702.colab-sample" / "05.01.pack.md"
        self.assertTrue(pack.is_file())
        code, _payload, _err = run(
            [
                "submit-return",
                "--book",
                self.book,
                "--input",
                self.ret(colab_binding, page="0702", subject="colab-sample"),
            ]
        )
        self.assertEqual(code, 0)
        before = pack.read_bytes()
        code, payload, _err = run(
            [
                "review",
                "--book",
                self.book,
                "--input",
                self.judge(page="0702", subject="colab-sample"),
            ]
        )
        self.assertEqual(code, 0, payload)
        self.assertEqual(pack.read_bytes(), before)
        page = Path(self.book) / "0702.colab-sample"
        self.assertTrue((page / "05.01.return.md").is_file())
        self.assertTrue((page / "06.01.review.md").is_file())
        self.assertFalse(any(Path(self.book).glob("0102.*")))
        other = str(self.root / "occupied")
        code, _payload, _err = run(["init", "--book", other, "--label", "synthetic"])
        self.assertEqual(code, 0)
        (Path(other) / "0123.old-occupant").mkdir()
        (Path(other) / "0123.old-occupant" / "keep.txt").write_text("keep\n", encoding="utf-8")
        path = write(self.root, "occ-task.json", task())
        code, payload, _err = run(["record-task", "--book", other, "--input", path])
        self.assertEqual(code, 2)
        self.assertEqual(payload["refusal"], "return-line-occupied")
        self.assertEqual((Path(other) / "0123.old-occupant" / "keep.txt").read_text(), "keep\n")
        self.assertFalse((Path(other) / "0123.sample").exists())

    def seed_pass(self, pass_id: str, page: str = "0523", subject: str = "sample") -> str:
        path = write(self.root, f"task-{page}-{subject}-{pass_id}.json", task(page, subject, pass_id))
        code, payload, _err = run(["record-task", "--book", self.book, "--input", path])
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
        code, payload, _err = run(["register", "--book", self.book, "--input", reg])
        self.assertEqual(code, 0, payload)
        return binding

    def test_review_without_return_duplicate_key_and_projection(self) -> None:
        self.seed()
        code, payload, _err = run(["review", "--book", self.book, "--input", self.judge()])
        self.assertEqual(code, 2)
        self.assertEqual(payload["refusal"], "return-missing")
        raw = self.root / "dup.json"
        raw.write_text('{"page":"0523","page":"0523"}\n', encoding="utf-8")
        code, payload, _err = run(["record-task", "--book", self.book, "--input", str(raw)])
        self.assertEqual(code, 2)
        self.assertEqual(payload["refusal"], "duplicate-key")
        face_path = Path(self.book) / "0523.sample" / "05.01.md"
        text = face_path.read_text(encoding="utf-8")
        face_path.write_text(text.replace("Build the disposable return.", "Tampered assignment.", 1), encoding="utf-8")
        code, shown = self.show()
        self.assertEqual(code, 0)
        self.assertEqual(shown["state"], "assignment-conflict")
        self.assertFalse(shown["accepted"])
        self.assertFalse(shown["complete"])
        self.assertEqual(shown["body"], "Build the disposable return.\n")
        code, payload, _err = run(["pending", "--book", self.book])
        self.assertEqual(code, 0, payload)
        self.assertEqual(payload["task_ledger"], False)
        self.assertEqual(payload["items"][0]["accepted"], False)

    def test_claim_conflict_visible(self) -> None:
        self.seed()
        reg = write(
            self.root,
            "other-claim.json",
            {
                "page": "0523",
                "subject": "sample",
                "pass": "01",
                "synthetic": True,
                "release": {"who": "Director", "date": "2026-10-31", "text": "Synthetic release for this disposable book only.\n"},
                "claim": {"worker": "other-worker", "date": "2026-10-31", "text": "A different claim.\n"},
            },
        )
        code, payload, _err = run(["register", "--book", self.book, "--input", reg])
        self.assertEqual(code, 2)
        self.assertEqual(payload["refusal"], "claim-conflict")
        code, shown = self.show()
        self.assertEqual(shown["state"], "claimed")
        self.assertIn("claim-conflict", shown["conflicts"])
        self.assertFalse(shown["accepted"])


if __name__ == "__main__":
    unittest.main()
