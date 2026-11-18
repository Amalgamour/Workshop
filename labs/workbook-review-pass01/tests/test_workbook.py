#!/usr/bin/env python3
"""Operator cycle for workbook review, through app/librarian.py."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(r"D:\Git\lib-build")
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
APP = ROOT / "app" / "librarian.py"
LINES = ROOT / "labs" / "return-lines-pass01" / "return_lines.py"
KEEP = Path(os.environ.get("WORKBOOK_KEEP", r"D:\librarian\temp\0522-0511"))
SECTION_KEYS = [
    "affected", "assumptions", "consequences", "exploration", "findings_account",
    "finish_assessments", "for_model", "issue", "learning", "limits",
    "next_bounded_action", "open_questions", "options", "outcome_evidence",
    "preservation", "prime_finding", "proposed_plan", "question", "recommendation",
    "remaining_choices", "return_result", "tests_note", "tests_passed", "within_direction",
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def sections(**over) -> dict:
    body = {key: None for key in SECTION_KEYS}
    body.update(over)
    return body


def judgment(**over) -> dict:
    base = {
        "answers": [],
        "design_fork": None,
        "disposition": "held",
        "finding": "The disposable note is present.",
        "findings": [{
            "disposition": "answered",
            "finding_id": "note#1",
            "text": "The note is named by the return.",
        }],
        "gaps": [],
        "goal_terminal": "open",
        "holds": [],
        "next_action": "Hand back one correction for the disposable note.",
        "operation": "continue",
        "pass_terminal": "open",
        "reasons": ["The return text names the note."],
        "review_passes": [],
        "sections": sections(
            findings_account=[{"finding_id": "note#1", "status": "accepted"}],
            next_bounded_action="Hand back one correction for the disposable note.",
            prime_finding="The disposable note is present.",
            return_result="The builder returned the disposable note.",
            within_direction="This stays inside the supplied grant.",
        ),
        "semantic_conflict": False,
    }
    base.update(over)
    return base


def page(pointer: str, review: str = "PENDING.\n") -> bytes:
    text = (
        "Intro OUTSIDE\n\n"
        "## Goal\n"
        "Review one disposable capture.\n\n"
        "## Scope\n"
        "The disposable book only.\n\n"
        "## Prime discretion\n"
        "Prime may record a judgment inside that grant.\n\n"
        "## Director required\n"
        "A design change is not in this grant.\n\n"
        "## Finish\n"
        "- piece: The disposable note stays one file.\n\n"
        "## Director - verbatim\n"
        "Pack it up.\n\n"
        "## Return pointer\n"
        f"{pointer}\n"
        "## Review - Codex Prime\n"
        f"{review}"
        "## Notes\n"
        "TAIL\n"
    )
    return text.encode("utf-8")


def run_app(args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [str(PY), "-B", str(APP), *args],
        cwd=str(ROOT),
        env=env,
        capture_output=True,
        shell=False,
    )


def call(book: Path, command: str, **flags: str) -> tuple[subprocess.CompletedProcess, dict]:
    args = ["review-loop", command, "--book", str(book)]
    for key, value in flags.items():
        flag = key[:-1] if key.endswith("_") else key
        args.extend(["--" + flag.replace("_", "-"), value])
    proc = run_app(args)
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except json.JSONDecodeError:
        payload = {}
    return proc, payload if isinstance(payload, dict) else {}


def seed_lines(book: Path, page_id: str, pass_id: str, submission: str, note: bytes, returned: bytes) -> subprocess.CompletedProcess:
    inputs = book / "_inputs"
    write(inputs / "return.md", returned)
    write(inputs / "note.md", note)
    write(book / "note.md", note)
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    last = None
    commands = [
        ["init", "--book", str(book), "--name", "00.00.10.work"],
        [
            "reserve", "--book", str(book), "--page", page_id, "--batch", pass_id,
            "--submission", submission, "--output", "note.md",
            "--submitter", "grok-1", "--reviewer", "codex-prime", "--release", "prepared",
        ],
        [
            "capture", "--book", str(book), "--page", page_id, "--batch", pass_id,
            "--submission", submission, "--return-file", str(inputs / "return.md"),
            "--artifact", "note.md", str(inputs / "note.md"),
        ],
    ]
    allowed = {0: {0}, 1: {0, 1}, 2: {0}}
    for index, args in enumerate(commands):
        last = subprocess.run([str(PY), "-B", str(LINES), *args], cwd=str(ROOT), env=env, capture_output=True)
        if last.returncode not in allowed[index]:
            raise AssertionError(f"seed {args[0]} exit {last.returncode}\n{last.stderr.decode()[:500]}\n{last.stdout.decode()[:500]}")
    return last


class WorkbookCycle(unittest.TestCase):
    def setUp(self) -> None:
        self.books = []

    def book(self, name: str) -> Path:
        path = Path(tempfile.mkdtemp(prefix=f"wb0511-{name}-"))
        self.books.append(path)
        return path

    def tearDown(self) -> None:
        KEEP.mkdir(parents=True, exist_ok=True)
        for path in self.books:
            dest = KEEP / path.name
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)
            shutil.copytree(path, dest, dirs_exist_ok=True)

    def test_unfiled_cycle_and_cases(self) -> None:
        book = self.book("n5")
        page_id = "0599.synth-review"
        returned = b"Did.\nThe disposable capture returned one note.\n"
        note = b"NOTE the disposable artifact is this file.\n"
        verification = pretty({"schema": "example-verification/1", "passed": None})
        submission = (
            "The builder returned one note and one artifact. "
            "The verification file is measured separately so this submission is not the whole packet.\n"
            f"Verification: evidence/verification.json sha256 {sha(verification)}, {len(verification)} bytes.\n"
        ).encode("utf-8")
        manifest_body = {
            "files": [{"bytes": len(note), "path": "note.md", "sha256": sha(note)}],
            "schema": "example-manifest/1",
        }
        manifest = pretty(manifest_body)
        write(book / "evidence" / "verification.json", verification)
        write(book / "evidence" / "submission.md", submission)
        write(book / "evidence" / "artifact-manifest.json", manifest)
        write(book / "note.md", note)
        pointer = (
            f"Submission: evidence/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
            f"Artifact manifest: evidence/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes.\n"
        )
        write(book / page_id / "05.01.md", page(pointer))
        write(book / "0199.synth-review" / "05.01.return.md", returned)

        proc, prepared = call(book, "prepare", source=page_id, pass_="05.01")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800])
        self.assertEqual(prepared["custody"], "missing")
        codes = [item["code"] for item in prepared["findings"]]
        self.assertIn("custody-missing", codes)
        self.assertNotIn("return-missing", codes)
        self.assertTrue(any(row["role"] == "return" for row in prepared["form"]["bindings"]["rows"]))
        self.assertFalse(prepared["accepted"])
        proc, formed = call(book, "form", source=page_id, pass_="05.01")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        self.assertEqual(formed["form"]["form_id"], "workbook-review-v1")
        intake = prepared["intake_id"]
        form_path = book / "judgment.json"
        write(form_path, pretty(judgment()))
        before = set(os.listdir(book))
        proc, recorded = call(
            book, "record", source=page_id, pass_="05.01", intake=intake, judgment=str(form_path),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        self.assertEqual(recorded["mode"], "preliminary")
        self.assertTrue(recorded["recorded"])
        self.assertFalse(recorded["eligible_for_custody_completion"])
        review = recorded["review_id"]
        self.assertTrue(review.startswith("w"))
        proc, inspected = call(book, "inspect", source=page_id, pass_="05.01")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        self.assertEqual(inspected["judgment"]["finding"], "The disposable note is present.")
        self.assertIn(review, inspected["rendered"])
        proc, again = call(
            book, "record", source=page_id, pass_="05.01", intake=intake, judgment=str(form_path),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        self.assertEqual(again["review_id"], review)
        self.assertTrue(again["already_recorded"])
        other = judgment(finding="A different finding.")
        other_path = book / "judgment-conflict.json"
        write(other_path, pretty(other))
        proc, conflict = call(
            book, "record", source=page_id, pass_="05.01", intake=intake, judgment=str(other_path),
        )
        self.assertEqual(proc.returncode, 2)
        self.assertFalse(conflict.get("recorded"))
        stored = json.loads((book / "workbook-review" / page_id / "05.01" / "reviews" / review / "record.json").read_text(encoding="utf-8"))
        self.assertEqual(stored["judgment"]["finding"], "The disposable note is present.")
        proc, published = call(book, "publish", source=page_id, pass_="05.01", review=review)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        self.assertIn(review, (book / page_id / "05.01.md").read_text(encoding="utf-8"))
        self.assertIn("TAIL", (book / page_id / "05.01.md").read_text(encoding="utf-8"))
        self.assertIn("OUTSIDE", (book / page_id / "05.01.md").read_text(encoding="utf-8"))
        proc, read = call(book, "read", source=page_id, pass_="05.01")
        self.assertEqual(read["judgment"]["finding"], stored["judgment"]["finding"])
        self.assertEqual(read["next_action"], stored["next_action"])
        proc, recovered = call(book, "recover", source=page_id, pass_="05.01")
        self.assertEqual(proc.returncode, 0, proc.stdout.decode()[:600])
        self.assertEqual(recovered["judgment"]["operation"], "continue")
        self.assertFalse(recovered["stale"])
        page_path = book / page_id / "05.01.md"
        blob = page_path.read_bytes().replace(b"Intro OUTSIDE", b"Intro CHANGED", 1)
        page_path.write_bytes(blob)
        proc, stale = call(book, "recover", source=page_id, pass_="05.01")
        self.assertEqual(proc.returncode, 1)
        self.assertTrue(stale["stale"])
        self.assertEqual(stale["judgment"]["finding"], "The disposable note is present.")
        page_path.write_bytes(page(pointer))
        self.assertNotIn("workbook-review", before)

    def test_director_successor_and_blocks(self) -> None:
        book = self.book("hold")
        page_id = "0598.synth-hold"
        write(book / page_id / "05.02.md", page("PENDING.\n"))
        proc, prepared = call(book, "prepare", source=page_id, pass_="05.02")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        codes = [item["code"] for item in prepared["findings"]]
        self.assertIn("return-pending", codes)
        self.assertIn("return-missing", codes)
        question = "Should the next pack stay on this page?"
        digest = sha(question.encode("utf-8"))
        hold = {
            "dependent_scope": ["pack-next"],
            "finding_id": "scope#1",
            "hold_id": "h1",
            "kind": "director-judgment",
            "question_id": "q1",
            "question_revision": "r1",
            "question_sha256": digest,
        }
        first = judgment(
            finding="The scope question is open.",
            findings=[{"disposition": "elevated", "finding_id": "scope#1", "text": "Director input is required."}],
            holds=[hold],
            operation="director-input",
            reasons=["The grant does not choose the next page."],
            sections=sections(
                affected=[{"action_id": "pack-next", "dependency": "The next pack."}],
                consequences="The dependent pack waits.",
                findings_account=[{"finding_id": "scope#1", "status": "open"}],
                issue="The next page is not in the grant.",
                options=["Stay on this page.", "Open a new page."],
                question={"content_sha256": digest, "id": "q1", "revision": "r1", "text": question},
                recommendation="Stay on this page.",
            ),
        )
        path = book / "hold.json"
        write(path, pretty(first))
        proc, recorded = call(book, "record", source=page_id, pass_="05.02", intake=prepared["intake_id"], judgment=str(path))
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        self.assertEqual(recorded["judgment"]["operation"], "director-input")
        reply = "Stay on this page."
        second = judgment(
            answers=[{
                "answer_id": "a1",
                "disposition": "brief-approval",
                "provenance": {
                    "actor_label": "Director (supplied)",
                    "evidence": "The reply is the supplied sentence.",
                    "role": "director",
                },
                "question_id": "q1",
                "question_revision": "r1",
                "question_sha256": digest,
                "reply": reply,
            }],
            finding="The Director reply is recorded and the finding stays open until a later review says otherwise.",
            findings=[{"disposition": "answered", "finding_id": "scope#1", "text": "The reply is recorded."}],
            holds=[hold],
            sections=sections(
                findings_account=[{"finding_id": "scope#1", "status": "open"}],
                next_bounded_action="Keep the finding open.",
                prime_finding="The reply does not close the finding.",
                return_result="No return file is filed.",
                within_direction="The reply is stored and is not a release.",
            ),
        )
        second_path = book / "successor.json"
        write(second_path, pretty(second))
        proc, followed = call(
            book, "record", source=page_id, pass_="05.02", intake=prepared["intake_id"],
            judgment=str(second_path), successor=recorded["review_id"],
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        self.assertNotEqual(followed["review_id"], recorded["review_id"])
        self.assertEqual(followed["judgment"]["answers"][0]["reply"], reply)
        self.assertFalse(followed["closes_work"])
        old = json.loads((book / "workbook-review" / page_id / "05.02" / "reviews" / recorded["review_id"] / "record.json").read_text(encoding="utf-8"))
        self.assertEqual(old["judgment"]["answers"], [])
        self.assertEqual(old["judgment"]["findings"][0]["disposition"], "elevated")
        proc, published = call(book, "publish", source=page_id, pass_="05.02", review=followed["review_id"])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:600] + proc.stdout.decode()[:400])
        text = (book / page_id / "05.02.md").read_text(encoding="utf-8")
        self.assertIn(reply, text)
        self.assertIn("TAIL", text)
        proc, recovered = call(book, "recover", source=page_id, pass_="05.02")
        self.assertEqual(recovered["judgment"]["operation"], "continue")
        self.assertEqual(recovered["holds"][0]["question_id"], "q1")

    def test_bad_input_manual_interrupt_drift(self) -> None:
        book = self.book("bad")
        page_id = "0597.synth-bad"
        write(book / page_id / "05.03.md", page("PENDING.\n", review="Manual note stays.\n"))
        proc, prepared = call(book, "prepare", source=page_id, pass_="05.03")
        self.assertEqual(proc.returncode, 0)
        bad = judgment()
        del bad["finding"]
        path = book / "bad.json"
        write(path, pretty(bad))
        proc, failed = call(book, "record", source=page_id, pass_="05.03", intake=prepared["intake_id"], judgment=str(path))
        self.assertEqual(proc.returncode, 2)
        self.assertIn("finding", failed.get("correction", ""))
        self.assertTrue((book / failed["failed_input"]).is_file())
        good = book / "good.json"
        write(good, pretty(judgment()))
        proc, recorded = call(book, "record", source=page_id, pass_="05.03", intake=prepared["intake_id"], judgment=str(good))
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:500])
        before = (book / page_id / "05.03.md").read_bytes()
        proc, blocked = call(book, "publish", source=page_id, pass_="05.03", review=recorded["review_id"])
        self.assertEqual(proc.returncode, 1)
        self.assertEqual((book / page_id / "05.03.md").read_bytes(), before)
        self.assertFalse(blocked["published"])
        proc, read = call(book, "read", source=page_id, pass_="05.03")
        self.assertEqual(read["judgment"]["finding"], "The disposable note is present.")
        target = book / page_id / "05.04.md"
        write(target, page("PENDING.\n"))
        proc, prepared4 = call(book, "prepare", source=page_id, pass_="05.04")
        proc, recorded4 = call(book, "record", source=page_id, pass_="05.04", intake=prepared4["intake_id"], judgment=str(good))
        self.assertEqual(proc.returncode, 0, proc.stdout.decode()[:400])
        os.chmod(target, stat.S_IREAD)
        proc, interrupted = call(book, "publish", source=page_id, pass_="05.04", review=recorded4["review_id"])
        os.chmod(target, stat.S_IWRITE | stat.S_IREAD)
        self.assertEqual(proc.returncode, 1, proc.stdout.decode()[:500])
        self.assertFalse(interrupted["published"])
        journal = json.loads((book / "workbook-review" / page_id / "05.04" / "journal.json").read_text(encoding="utf-8"))
        self.assertEqual(journal["publication"]["status"], "pointer-pending")
        proc, recovered = call(book, "recover", source=page_id, pass_="05.04")
        self.assertEqual(recovered["judgment"]["next_action"], judgment()["next_action"])
        self.assertEqual(recovered["target_state"], "pointer-pending")
        changed = page("PENDING.\n").replace(b"Review one disposable capture.", b"Review one changed capture.")
        write(book / page_id / "05.03.md", changed)
        proc, drifted = call(book, "record", source=page_id, pass_="05.03", intake=prepared["intake_id"], judgment=str(good))
        self.assertEqual(proc.returncode, 2)
        self.assertTrue(drifted["stale"])
        kept = json.loads((book / "workbook-review" / page_id / "05.03" / "reviews" / recorded["review_id"] / "record.json").read_text(encoding="utf-8"))
        self.assertEqual(kept["judgment"]["finding"], "The disposable note is present.")

    def test_ambiguous_and_n7_and_complete_refused(self) -> None:
        book = self.book("n7")
        page_id = "0799.synth-face"
        write(book / page_id / "05.02.md", page("Submission: a sha256 ab, 1 bytes.\nSubmission: b sha256 cd, 1 bytes.\n"))
        write(book / page_id / "05.02.pack.md", b"other\n")
        proc, prepared = call(book, "prepare", source=page_id, pass_="05.02")
        self.assertEqual(proc.returncode, 0)
        codes = [item["code"] for item in prepared["findings"]]
        self.assertIn("ambiguous-assignment", codes)
        self.assertIn("ambiguous-submission", codes)
        self.assertFalse(any(row["role"] == "assignment" for row in prepared["form"]["bindings"]["rows"]))
        write(book / "0798.synth-local" / "05.03.md", page("PENDING.\n"))
        returned = b"Did.\nThe page-local return has a substantive note.\n"
        write(book / "0798.synth-local" / "05.03.return.md", returned)
        before_return = sha(returned)
        proc, local = call(book, "prepare", source="0798.synth-local", pass_="05.03")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        self.assertEqual(local["kind"], "N7NN")
        self.assertEqual(local["custody"], "missing")
        path = book / "local.json"
        write(path, pretty(judgment()))
        proc, recorded = call(book, "record", source="0798.synth-local", pass_="05.03", intake=local["intake_id"], judgment=str(path))
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:600] + proc.stdout.decode()[:400])
        proc, published = call(book, "publish", source="0798.synth-local", pass_="05.03", review=recorded["review_id"])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:600])
        self.assertTrue((book / "0798.synth-local" / "06.03.review.md").is_file())
        self.assertEqual(sha((book / "0798.synth-local" / "05.03.return.md").read_bytes()), before_return)
        complete = judgment(
            disposition="accepted",
            goal_terminal="completed",
            operation="complete",
            pass_terminal="finished",
        )
        complete_path = book / "complete.json"
        write(complete_path, pretty(complete))
        proc, refused = call(book, "record", source="0798.synth-local", pass_="05.03", intake=local["intake_id"], judgment=str(complete_path), successor=recorded["review_id"])
        self.assertEqual(proc.returncode, 2)
        self.assertFalse(refused.get("recorded"))
        self.assertIn("ineligible", refused.get("correction", ""))

    def test_filed_cycle(self) -> None:
        book = self.book("filed")
        page_id = "0596.synth-filed"
        pass_id = "05.01"
        submission = "sub-0511"
        note = b"NOTE the filed artifact is substantive.\n"
        returned = b"Did.\nThe filed capture returned one substantive note.\n"
        seed_lines(book, page_id, pass_id, submission, note, returned)
        verification = pretty({"note": "measured", "schema": "example-verification/1"})
        submission_text = (
            "The filed capture returned the note. This submission points at the verification and is not the only packet.\n"
            f"Verification: evidence/verification.json sha256 {sha(verification)}, {len(verification)} bytes.\n"
        ).encode("utf-8")
        manifest = pretty({"files": [{"bytes": len(note), "path": "note.md", "sha256": sha(note)}], "schema": "example-manifest/1"})
        write(book / "evidence" / "verification.json", verification)
        write(book / "evidence" / "submission.md", submission_text)
        write(book / "evidence" / "artifact-manifest.json", manifest)
        pointer = (
            f"Submission: evidence/submission.md sha256 {sha(submission_text)}, {len(submission_text)} bytes.\n"
            f"Artifact manifest: evidence/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes.\n"
        )
        write(book / page_id / "05.01.md", page(pointer))
        proc, prepared = call(book, "prepare", source=page_id, pass_=pass_id)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        self.assertEqual(prepared["custody"], "complete-descriptor", prepared.get("findings"))
        path = book / "filed.json"
        write(path, pretty(judgment()))
        proc, recorded = call(book, "record", source=page_id, pass_=pass_id, intake=prepared["intake_id"], judgment=str(path))
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:1200])
        self.assertEqual(recorded["mode"], "cycle-committed", recorded.get("cycle"))
        proc, published = call(book, "publish", source=page_id, pass_=pass_id, review=recorded["review_id"])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        text = (book / page_id / "05.01.md").read_text(encoding="utf-8")
        self.assertIn("OUTSIDE", text)
        self.assertIn("TAIL", text)
        proc, recovered = call(book, "recover", source=page_id, pass_=pass_id)
        self.assertEqual(proc.returncode, 0, proc.stdout.decode()[:600])
        self.assertEqual(recovered["judgment"]["finding"], "The disposable note is present.")
        self.assertFalse(recovered["closes_work"])

    def test_route_and_pins(self) -> None:
        book = self.book("route")
        write(book / "0499.other" / "05.01.md", b"x\n")
        proc, payload = call(book, "prepare", source="0499.other", pass_="05.01")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("route", payload.get("missing", []))
        proc = run_app(["review-loop", "describe-legacy", "--book", str(book)])
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"stop:", proc.stderr)
        v4 = (ROOT / "app" / "review_loop_tools_v4.py").read_bytes()
        self.assertEqual(sha(v4), "0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296")
        self.assertEqual(len(v4), 13381)
        declared = (ROOT / "app" / "review-loop-v4.json").read_bytes()
        self.assertEqual(sha(declared), "769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723")
        authoring = (ROOT / "app" / "authoring-v2.json").read_bytes()
        self.assertEqual(sha(authoring), "14965030b2344f77e196a1d6a29b8cb74400cc3cf237e4f5ecc44c2adf332d11")
        returns = (ROOT / "app" / "return-lines-v2.json").read_bytes()
        self.assertEqual(sha(returns), "9fc16cc49d87c7455cc56aebb87897252807a426654dbe45d7e575df5f081e52")
        proc = run_app(["return-lines", "status", "--book", str(book)])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        body = json.loads(proc.stdout.decode("utf-8"))
        self.assertFalse(body["accepted"])
        self.assertEqual(body["task_association"], "not-established")
        for rel in (
            "00.kernel/00.00.10.work/0423.dev-authoring/01.md",
            "00.kernel/00.00.10.work/0423.dev-authoring/06.01.md",
            "00.kernel/00.00.10.work/0423.dev-authoring/06.02.md",
            "00.kernel/00.00.10.work/0423.dev-authoring/templates/build-pack-v1.draft.md",
            "00.kernel/00.00.10.work/0526.dev-authoring/01.md",
        ):
            dest = book / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((ROOT / rel).read_bytes())
        proc = run_app(["authoring", "form", "--book", str(book), "--profile", "0423-to-0526", "--kind", "intent", "--json"])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400] + proc.stdout.decode()[:200])
        formed = json.loads(proc.stdout.decode("utf-8"))
        self.assertEqual(formed["schema"], "authoring-form/1")
        self.assertEqual(formed["kind"], "intent")


def pretty(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


if __name__ == "__main__":
    unittest.main()
