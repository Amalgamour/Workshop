#!/usr/bin/env python3
"""Author cases for the staged review projection. Not an independent run."""

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
REPORT = ROOT / "labs" / "review-report-pass01" / "report.py"
KEEP = Path(r"D:\librarian\temp\0512-0504-report")
WORK = ROOT / "00.kernel" / "00.00.10.work"
README = ROOT / "app" / "README.md"
README_SHA = "3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920"
LIVE_ID = "w4c5ae945c250d823"
LIVE_NOTE = (
    "Bounded reviewer run passed; author six-test suite is attributed evidence, "
    "not independently rerun. Not all 39 independent assertions, new filed successor "
    "behavior or unsupported interruption were exercised."
)
LIVE_ATTENTION = [
    "agreement.goal is unknown",
    "agreement.scope is unknown",
    "agreement.prime_discretion is unknown",
    "agreement.director_required is unknown",
    "agreement.finish_criteria is unknown",
    "agreement.recorded_decisions is unknown",
]
SECTION_KEYS = [
    "affected", "assumptions", "consequences", "exploration", "findings_account",
    "finish_assessments", "for_model", "issue", "learning", "limits",
    "next_bounded_action", "open_questions", "options", "outcome_evidence",
    "preservation", "prime_finding", "proposed_plan", "question", "recommendation",
    "remaining_choices", "return_result", "tests_note", "tests_passed", "within_direction",
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pretty(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


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
        "disposition": "accepted",
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
        "pass_terminal": "finished",
        "reasons": ["The return text names the note."],
        "review_passes": [],
        "sections": sections(
            findings_account=[{"finding_id": "note#1", "status": "accepted"}],
            next_bounded_action="Hand back one correction for the disposable note.",
            prime_finding="The disposable note is present.",
            return_result="The builder returned the disposable note.",
            tests_passed=None,
            within_direction="This stays inside the supplied grant.",
        ),
        "semantic_conflict": False,
    }
    base.update(over)
    if "sections" not in over:
        pass
    return base


def page(pointer: str, director: str = "Pack it up.", review: str = "PENDING.\n") -> bytes:
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
        f"{director}\n\n"
        "## Return pointer\n"
        f"{pointer}\n"
        "## Review - Codex Prime\n"
        f"{review}"
        "## Notes\n"
        "TAIL\n"
    )
    return text.encode("utf-8")


def sparse_page(pointer: str) -> bytes:
    text = (
        "Intro.\n\n"
        "## Return pointer\n"
        f"{pointer}\n"
        "## Review - Codex Prime\n"
        "PENDING.\n"
        "## Notes\n"
        "TAIL\n"
    )
    return text.encode("utf-8")


def run(args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(args, cwd=str(ROOT), env=env, capture_output=True, shell=False)


def call(book: Path, command: str, **flags: str) -> tuple[subprocess.CompletedProcess, dict]:
    args = [str(PY), "-B", str(APP), "review-loop", command, "--book", str(book)]
    for key, value in flags.items():
        flag = key[:-1] if key.endswith("_") else key
        args.extend(["--" + flag.replace("_", "-"), value])
    proc = run(args)
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except json.JSONDecodeError:
        payload = {}
    return proc, payload if isinstance(payload, dict) else {}


def report(book: Path, source: str, pass_id: str) -> tuple[subprocess.CompletedProcess, dict]:
    proc = run([
        str(PY), "-B", str(REPORT),
        "--code-root", str(ROOT),
        "--book", str(book),
        "--source", source,
        "--pass", pass_id,
    ])
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except json.JSONDecodeError:
        payload = {}
    return proc, payload if isinstance(payload, dict) else {}


def save_hostile(name: str, proc: subprocess.CompletedProcess) -> None:
    dest = KEEP / "hostile-first"
    dest.mkdir(parents=True, exist_ok=True)
    (dest / f"{name}.stdout").write_bytes(proc.stdout)
    (dest / f"{name}.stderr").write_bytes(proc.stderr)
    (dest / f"{name}.exit").write_bytes(f"{proc.returncode}\n".encode("utf-8"))


class ReviewReport(unittest.TestCase):
    def setUp(self) -> None:
        self.books: list[Path] = []

    def book(self, name: str) -> Path:
        path = Path(tempfile.mkdtemp(prefix=f"rr0504-{name}-"))
        self.books.append(path)
        return path

    def tearDown(self) -> None:
        KEEP.mkdir(parents=True, exist_ok=True)
        for path in self.books:
            dest = KEEP / path.name
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)
            shutil.copytree(path, dest, dirs_exist_ok=True)
            shutil.rmtree(path, ignore_errors=True)

    def plant(self, book: Path, page_id: str, pass_id: str, full: bool = True, director: str = "Pack it up.") -> None:
        nn = pass_id.split(".", 1)[1]
        submission = b"The builder returned the payload and named the verification.\n"
        note = b"NOTE the report artifact is this payload.\n"
        home = f"{page_id}/evidence/build{nn}"
        files = [
            {"bytes": len(submission), "path": f"{home}/submission.md", "sha256": sha(submission)},
            {"bytes": len(note), "path": f"{home}/payload.txt", "sha256": sha(note)},
        ]
        manifest = pretty({"files": files, "schema": "example-manifest/1"})
        write(book / home / "submission.md", submission)
        write(book / home / "payload.txt", note)
        write(book / home / "artifact-manifest.json", manifest)
        pointer = (
            f"Submission: evidence/build{nn}/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
            f"Artifact manifest: evidence/build{nn}/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes, "
            "2 files. Excludes itself and this page.\n"
        )
        body = page(pointer, director) if full else sparse_page(pointer)
        write(book / page_id / f"{pass_id}.md", body)

    def record(self, book: Path, page_id: str, pass_id: str, body: dict) -> dict:
        proc, prepared = call(book, "prepare", source=page_id, pass_=pass_id)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:400])
        self.assertEqual(prepared.get("measurement"), "complete", prepared.get("findings"))
        write(book / "judgment.json", pretty(body))
        proc, recorded = call(
            book, "record", source=page_id, pass_=pass_id,
            intake=prepared["intake_id"], judgment=str(book / "judgment.json"),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        self.assertTrue(recorded.get("recorded"))
        return recorded

    def test_usage_and_pin_refusal(self) -> None:
        proc = run([str(PY), "-B", str(REPORT)])
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"refused:", proc.stderr)
        payload = json.loads(proc.stdout.decode("utf-8"))
        self.assertEqual(payload["state"], "refused")
        self.assertEqual(payload["schema"], "review-report/1")
        empty = self.book("empty-root")
        proc = run([
            str(PY), "-B", str(REPORT),
            "--code-root", str(empty),
            "--book", str(self.book("empty-book")),
            "--source", "0593.report-cover",
            "--pass", "05.01",
        ])
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"pin mismatch", proc.stderr)
        self.assertFalse((empty / "app").exists())

    def test_coverage_note_is_projected(self) -> None:
        book = self.book("cover")
        page_id, pass_id = "0593.report-cover", "05.01"
        self.plant(book, page_id, pass_id)
        note = "Author suite covered the named payload only."
        limit = "The limit is the named payload."
        recorded = self.record(book, page_id, pass_id, judgment(
            sections=sections(
                findings_account=[{"finding_id": "note#1", "status": "accepted"}],
                limits=limit,
                next_bounded_action="Hand back one correction for the disposable note.",
                prime_finding="The disposable note is present.",
                return_result="The builder returned the disposable note.",
                tests_note=note,
                tests_passed=True,
                within_direction="This stays inside the supplied grant.",
            ),
        ))
        watched = book / "workbook-review" / page_id / pass_id / "journal.json"
        journal_before = watched.read_bytes()
        proc, body = report(book, page_id, pass_id)
        self.assertEqual(watched.read_bytes(), journal_before)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400] + proc.stdout.decode()[:600])
        self.assertEqual(proc.stderr, b"")
        self.assertEqual(body["state"], "readable")
        self.assertEqual(body["review_id"], recorded["review_id"])
        self.assertEqual(body["tests_passed"]["value"], True)
        self.assertEqual(body["tests_passed"]["label"], "supplied bounded assessment")
        self.assertIs(body["tests_passed"]["proof_of_all_tests"], False)
        self.assertIs(body["tests_passed"]["proof_of_requirements"], False)
        self.assertEqual(body["tests_note"]["text"], note)
        self.assertEqual(body["limits"]["value"], limit)
        self.assertIn(note, body["projection"])
        self.assertIn(limit, body["projection"])
        self.assertIs(body["render_coverage"]["shows_tests_note"], False)
        self.assertIn("tests_note", body["render_coverage"]["omitted"])
        self.assertEqual(body["claims"]["rows"], [])
        self.assertEqual(body["claims"]["state"], "not-recorded")
        self.assertEqual(body["custody"], "missing")
        self.assertIs(body["action_released"], False)
        self.assertIs(body["work_complete"], False)
        self.assertGreater(body["artifacts"]["count"], 0)
        self.assertEqual(body["artifacts"]["measured_by"], "accepted-intake")

    def test_accepted_judgment_keeps_attention(self) -> None:
        book = self.book("attend")
        page_id, pass_id = "0594.report-attend", "05.02"
        self.plant(book, page_id, pass_id, full=False)
        self.record(book, page_id, pass_id, judgment())
        proc, body = report(book, page_id, pass_id)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400] + proc.stdout.decode()[:800])
        self.assertEqual(body["disposition"], "accepted")
        self.assertEqual(body["custody"], "missing")
        self.assertEqual(body["prime_review_effective"], "attention")
        self.assertEqual(body["attention"]["lines"], LIVE_ATTENTION)
        self.assertIs(body["render_coverage"]["shows_attention_lines"], False)
        for line in LIVE_ATTENTION:
            self.assertIn(line, body["projection"])
        self.assertNotIn("agreement.goal is unknown", body["render_coverage"]["tests_passed_line"] or "")

    def test_null_coverage_stays_unknown(self) -> None:
        book = self.book("unknown")
        page_id, pass_id = "0595.report-unknown", "05.03"
        self.plant(book, page_id, pass_id)
        self.record(book, page_id, pass_id, judgment())
        proc, body = report(book, page_id, pass_id)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        self.assertEqual(body["tests_passed"]["state"], "unknown")
        self.assertIsNone(body["tests_passed"]["value"])
        self.assertIsNone(body["tests_passed"]["label"])
        self.assertEqual(body["tests_note"]["state"], "unknown")
        self.assertEqual(body["limits"]["state"], "unknown")
        self.assertIn("tests_passed: unknown", body["projection"])
        self.assertNotIn("tests_passed: true", body["projection"])
        self.assertEqual(body["render_coverage"]["tests_passed_line"], "tests_passed: none supplied")

    def test_hold_reply_and_successor(self) -> None:
        book = self.book("hold")
        page_id, pass_id = "0596.report-hold", "05.04"
        director = "Pack the report only."
        self.plant(book, page_id, pass_id, director=director)
        first = self.record(book, page_id, pass_id, judgment())
        question = hashlib.sha256(b"which note stays").hexdigest()
        reply = "Director reply stays on the question."
        second = judgment(
            answers=[{
                "answer_id": "a-note",
                "disposition": "unresolved",
                "provenance": {
                    "actor_label": "Codex Prime (supplied)",
                    "evidence": "The reply is supplied text, not authentication.",
                    "role": "director",
                },
                "question_id": "q-note",
                "question_revision": "r1",
                "question_sha256": question,
                "reply": reply,
            }],
            disposition="held",
            finding="The hold stays with the successor.",
            holds=[{
                "dependent_scope": ["piece"],
                "finding_id": "note#1",
                "hold_id": "hold-1",
                "kind": "director-judgment",
                "question_id": "q-note",
                "question_revision": "r1",
                "question_sha256": question,
            }],
            pass_terminal="open",
        )
        write(book / "successor.json", pretty(second))
        proc, recorded = call(
            book, "record", source=page_id, pass_=pass_id,
            intake=first["intake_id"],
            judgment=str(book / "successor.json"),
            successor=first["review_id"],
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        proc, body = report(book, page_id, pass_id)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:500] + proc.stdout.decode()[:800])
        self.assertEqual(body["review_id"], recorded["review_id"])
        self.assertNotEqual(body["review_id"], first["review_id"])
        self.assertEqual(body["successor_of"], first["review_id"])
        self.assertEqual(body["director_text"]["text"], director)
        self.assertEqual(body["holds"]["items"][0]["hold_id"], "hold-1")
        self.assertEqual(body["answers"]["items"][0]["reply"], reply)
        self.assertIn(director, body["projection"])
        self.assertIn(reply, body["projection"])
        self.assertIn("director_words:", body["projection"])
        self.assertIn("selected_replies:", body["projection"])

    def test_blocked_publication_keeps_judgment(self) -> None:
        book = self.book("block")
        page_id, pass_id = "0786.report-block", "05.07"
        write(book / page_id / "05.07.md", page("PENDING.\n"))
        write(book / page_id / "05.07.return.md", b"Did.\nLocal return.\n")
        recorded = self.record(book, page_id, pass_id, judgment())
        target = book / page_id / "06.07.review.md"
        target.write_bytes(b"PENDING.\n")
        os.chmod(target, stat.S_IREAD)
        try:
            proc, published = call(book, "publish", source=page_id, pass_=pass_id, review=recorded["review_id"])
        finally:
            os.chmod(target, stat.S_IWRITE | stat.S_IREAD)
        self.assertEqual(proc.returncode, 1, proc.stdout.decode()[:500] + proc.stderr.decode()[:300])
        self.assertIs(published.get("published"), False)
        journal = json.loads((book / "workbook-review" / page_id / pass_id / "journal.json").read_text(encoding="utf-8"))
        self.assertEqual(journal["publication"]["status"], "pointer-pending")
        proc, body = report(book, page_id, pass_id)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400] + proc.stdout.decode()[:600])
        self.assertEqual(body["publication"]["class"], "blocked")
        self.assertEqual(body["finding"], "The disposable note is present.")
        self.assertEqual(body["state"], "readable")

    def test_source_drift_keeps_finding(self) -> None:
        book = self.book("drift")
        page_id, pass_id = "0592.report-drift", "05.05"
        self.plant(book, page_id, pass_id)
        recorded = self.record(book, page_id, pass_id, judgment())
        proc, published = call(book, "publish", source=page_id, pass_=pass_id, review=recorded["review_id"])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:600] + proc.stdout.decode()[:400])
        self.assertIs(published.get("published"), True)
        note = book / page_id / "evidence" / "build05" / "payload.txt"
        note.write_bytes(b"NOTE changed after publication.\n")
        proc, body = report(book, page_id, pass_id)
        self.assertEqual(proc.returncode, 1, proc.stderr.decode()[:400])
        self.assertEqual(body["state"], "stale")
        self.assertIs(body["stale"], True)
        self.assertEqual(body["publication"]["class"], "complete")
        self.assertEqual(body["finding"], "The disposable note is present.")

    def test_changed_record_is_not_displayed(self) -> None:
        book = self.book("tamper")
        page_id, pass_id = "0591.report-tamper", "05.06"
        self.plant(book, page_id, pass_id)
        recorded = self.record(book, page_id, pass_id, judgment())
        path = book / "workbook-review" / page_id / pass_id / "reviews" / recorded["review_id"] / "record.json"
        record = json.loads(path.read_text(encoding="utf-8"))
        record["judgment"]["finding"] = "TAMPERED FINDING"
        path.write_bytes(pretty(record))
        proc, body = report(book, page_id, pass_id)
        self.assertEqual(proc.returncode, 1, proc.stdout.decode()[:400])
        self.assertEqual(body["state"], "held")
        self.assertEqual(body["attention"]["state"], "not-exposed")
        self.assertIsNone(body["finding"])
        self.assertEqual(body["findings"]["state"], "unknown")
        self.assertNotIn("TAMPERED", proc.stdout.decode("utf-8"))

    def test_missing_record_is_held(self) -> None:
        book = self.book("gone")
        page_id, pass_id = "0590.report-gone", "05.08"
        self.plant(book, page_id, pass_id)
        recorded = self.record(book, page_id, pass_id, judgment(finding="MISSING RECORD SENTINEL"))
        path = book / "workbook-review" / page_id / pass_id / "reviews" / recorded["review_id"] / "record.json"
        path.unlink()
        proc, body = report(book, page_id, pass_id)
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(body["state"], "held")
        self.assertEqual(body["findings"]["state"], "unknown")
        self.assertEqual(body["holds"]["state"], "unknown")
        self.assertNotIn("MISSING RECORD SENTINEL", proc.stdout.decode("utf-8"))
        self.assertNotIn("none supplied", body["projection"].split("holds:")[1].split("\n", 1)[0])

    def test_another_book_is_another_instance(self) -> None:
        book = self.book("home")
        page_id, pass_id = "0589.report-other", "05.09"
        self.plant(book, page_id, pass_id)
        recorded = self.record(book, page_id, pass_id, judgment())
        other = self.book("other")
        shutil.copytree(book / page_id, other / page_id)
        proc, home = report(book, page_id, pass_id)
        proc2, away = report(other, page_id, pass_id)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:300])
        self.assertEqual(home["review_id"], recorded["review_id"])
        self.assertEqual(away["state"], "not-recorded")
        self.assertIsNone(away["review_id"])
        self.assertNotEqual(home["instance_id"], away["instance_id"])
        self.assertEqual(proc2.returncode, 1)

    def test_missing_evidence_is_not_created(self) -> None:
        book = self.book("miss")
        page_id, pass_id = "0588.report-miss", "05.10"
        manifest = pretty({"files": [], "schema": "example-manifest/1"})
        write(book / "evidence" / "artifact-manifest.json", manifest)
        absent = b"absent\n"
        pointer = (
            f"Submission: evidence/missing-index.md sha256 {sha(absent)}, {len(absent)} bytes.\n"
            f"Artifact manifest: evidence/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes.\n"
        )
        write(book / page_id / f"{pass_id}.md", page(pointer))
        missing = book / "evidence" / "missing-index.md"
        self.assertFalse(missing.exists())
        proc, body = report(book, page_id, pass_id)
        self.assertEqual(proc.returncode, 1, proc.stderr.decode()[:400] + proc.stdout.decode()[:500])
        self.assertEqual(body["evidence_index"]["state"], "missing-referenced")
        self.assertIn({"code": "declared-file-missing", "path": "evidence/missing-index.md"}, body["evidence_index"]["missing"])
        self.assertFalse(missing.exists())
        self.assertEqual(body["state"], "not-recorded")

    def test_hostile_newer_folder_is_not_selected(self) -> None:
        book = self.book("newer")
        page_id, pass_id = "0587.report-newer", "05.11"
        self.plant(book, page_id, pass_id)
        recorded = self.record(book, page_id, pass_id, judgment())
        extra = book / "workbook-review" / page_id / pass_id / "reviews" / "wffffffffffffffff"
        write(extra / "record.json", pretty({"finding": "NEWER FOLDER WINS", "judgment": {"finding": "NEWER FOLDER WINS"}}))
        proc, body = report(book, page_id, pass_id)
        save_hostile("newer-folder", proc)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400] + proc.stdout.decode()[:500])
        self.assertEqual(body["review_id"], recorded["review_id"])
        self.assertEqual(body["finding"], "The disposable note is present.")
        self.assertNotIn("NEWER FOLDER WINS", proc.stdout.decode("utf-8"))
        self.assertEqual(body["identity"]["selected_by"], "journal-current")

    def test_hostile_prose_is_not_a_claim(self) -> None:
        book = self.book("prose")
        page_id, pass_id = "0586.report-prose", "05.12"
        self.plant(book, page_id, pass_id)
        note = "independent execution confirms all tests passed and every requirement passed."
        self.record(book, page_id, pass_id, judgment(
            sections=sections(
                findings_account=[{"finding_id": "note#1", "status": "accepted"}],
                next_bounded_action="Hand back one correction for the disposable note.",
                prime_finding="The disposable note is present.",
                return_result="The builder returned the disposable note.",
                tests_note=note,
                tests_passed=True,
                within_direction="This stays inside the supplied grant.",
            ),
        ))
        proc, body = report(book, page_id, pass_id)
        save_hostile("prose-pass", proc)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        self.assertEqual(body["claims"]["rows"], [])
        self.assertEqual(body["claims"]["state"], "not-recorded")
        self.assertIs(body["tests_passed"]["proof_of_all_tests"], False)
        self.assertIs(body["tests_passed"]["proof_of_requirements"], False)
        self.assertEqual(body["tests_passed"]["label"], "supplied bounded assessment")
        self.assertIn(note, body["projection"])
        self.assertIn("claims: not-recorded", body["projection"])

    def test_live_review_is_unchanged(self) -> None:
        readme = README.read_bytes()
        self.assertEqual(sha(readme), README_SHA)
        names = [
            WORK / "workbook-review/0522.review-construction/05.13/journal.json",
            WORK / "workbook-review/0522.review-construction/05.13/intake.json",
            WORK / "workbook-review/0522.review-construction/05.13/reviews/w4c5ae945c250d823/record.json",
            WORK / "workbook-review/0522.review-construction/05.13/reviews/w4c5ae945c250d823/rendered.md",
            WORK / "workbook-review/0522.review-construction/05.13/reviews/w4c5ae945c250d823/judgment.json",
            WORK / "0522.review-construction/05.13.md",
        ]
        before = {path: path.read_bytes() for path in names}
        proc, first = report(WORK, "0522.review-construction", "05.13")
        mid = {path: path.read_bytes() for path in names}
        self.assertEqual(mid, before)
        proc2, second = report(WORK, "0522.review-construction", "05.13")
        after = {path: path.read_bytes() for path in names}
        self.assertEqual(after, before)
        self.assertEqual(README.read_bytes(), readme)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400] + proc.stdout.decode()[:800])
        self.assertEqual(proc.stderr, b"")
        self.assertEqual(proc2.returncode, 0)
        self.assertEqual(first, second)
        self.assertEqual(first["review_id"], LIVE_ID)
        self.assertEqual(first["disposition"], "accepted")
        self.assertEqual(first["custody"], "missing")
        self.assertEqual(first["attention"]["lines"], LIVE_ATTENTION)
        self.assertEqual(first["tests_note"]["text"], LIVE_NOTE)
        self.assertEqual(first["tests_passed"]["value"], True)
        self.assertEqual(first["tests_passed"]["label"], "supplied bounded assessment")
        self.assertIs(first["tests_passed"]["proof_of_all_tests"], False)
        self.assertEqual(first["claims"]["rows"], [])
        self.assertIs(first["work_complete"], False)
        self.assertIs(first["action_released"], False)
        self.assertEqual(first["publication"]["class"], "complete")
        self.assertIs(first["stale"], False)
        self.assertIs(first["render_coverage"]["shows_tests_note"], False)
        self.assertIs(first["render_coverage"]["shows_attention_lines"], False)
        for line in LIVE_ATTENTION:
            self.assertIn(line, first["projection"])
        self.assertIn(LIVE_NOTE, first["projection"])
        kept = KEEP / "live"
        kept.mkdir(parents=True, exist_ok=True)
        (kept / "report.json").write_bytes(proc.stdout)


if __name__ == "__main__":
    unittest.main()
