#!/usr/bin/env python3
"""Operator cases for the 05.12 workbook repair, through app/librarian.py."""

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
KEEP = Path(os.environ.get("WORKBOOK_KEEP", r"D:\librarian\temp\0522-0512-pass02"))
WORK = ROOT / "00.kernel" / "00.00.10.work"
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
            tests_passed=None,
            within_direction="This stays inside the supplied grant.",
        ),
        "semantic_conflict": False,
    }
    base.update(over)
    return base


def page(pointer: str, review: str = "PENDING.\n", newline: str = "\n") -> bytes:
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
    if newline != "\n":
        text = text.replace("\n", newline)
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


def codes(payload: dict) -> list:
    return [item.get("code") for item in payload.get("findings", []) if isinstance(item, dict)]


def rows(payload: dict) -> list:
    form = payload.get("form") if isinstance(payload.get("form"), dict) else {}
    bindings = form.get("bindings") if isinstance(form.get("bindings"), dict) else {}
    found = bindings.get("rows")
    if isinstance(found, list):
        return found
    found = payload.get("rows")
    return found if isinstance(found, list) else []


class WorkbookRepair(unittest.TestCase):
    def setUp(self) -> None:
        self.books = []

    def book(self, name: str) -> Path:
        path = Path(tempfile.mkdtemp(prefix=f"wb0512-{name}-"))
        self.books.append(path)
        return path

    def tearDown(self) -> None:
        KEEP.mkdir(parents=True, exist_ok=True)
        for path in self.books:
            dest = KEEP / path.name
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)
            shutil.copytree(path, dest, dirs_exist_ok=True)

    def test_predecessors_and_doors(self) -> None:
        pins = {
            "labs/workbook-review-pass01/workbook.py": ("60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a", 79131),
            "labs/workbook-review-pass01/forms/workbook-review-v1.json": ("152b436bda8e19d15f252bb5208791c8eefd9a658789e2ab6e9789ffa362b49f", 4532),
            "app/review_loop_tools_v5.py": ("b1192daf5d265c66f10adfe2125ff0c92a08ccd3c797d229698ecc20e2fdeed9", 7875),
            "app/review-loop-v5.json": ("eaa9120bba2c7274f2218c875ec3ecfc84d291188557049240c30a1c2a430de3", 1964),
            "app/review_loop_tools_v4.py": ("0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296", 13381),
            "app/review-loop-v4.json": ("769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723", 2519),
            "app/authoring-v2.json": ("14965030b2344f77e196a1d6a29b8cb74400cc3cf237e4f5ecc44c2adf332d11", 2106),
            "app/return-lines-v2.json": ("9fc16cc49d87c7455cc56aebb87897252807a426654dbe45d7e575df5f081e52", 1598),
        }
        for rel, (digest, size) in pins.items():
            data = (ROOT / rel).read_bytes()
            self.assertEqual(len(data), size, rel)
            self.assertEqual(sha(data), digest, rel)
        book = self.book("doors")
        proc = run_app(["review-loop", "describe-legacy", "--book", str(book)])
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"stop:", proc.stderr)
        proc = run_app([
            "review-loop", "prepare", "--book", str(book), "--fixture-root", str(book),
            "--source", "0599.synth-review", "--pass", "05.01",
        ])
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"stop:", proc.stderr)
        proc = run_app(["review-loop", "record", "--book", str(ROOT), "--source", "0599.synth-review", "--pass", "05.01", "--intake", "ab", "--judgment", str(book / "missing.json")])
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"checkout", proc.stderr.lower() + proc.stdout)
        write(book / "0499.other" / "05.01.md", b"x\n")
        proc, payload = call(book, "prepare", source="0499.other", pass_="05.01")
        self.assertEqual(proc.returncode, 2, proc.stderr.decode()[:400])
        self.assertIn("route", payload.get("missing", []))
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
        link = book / "linked-book"
        target = ROOT / "labs"
        made = False
        try:
            subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], check=True, capture_output=True)
            made = True
        except (OSError, subprocess.CalledProcessError):
            made = False
        if made:
            proc = run_app([
                "review-loop", "record", "--book", str(link), "--source", "0599.synth-review",
                "--pass", "05.01", "--intake", "ab", "--judgment", str(book / "missing.json"),
            ])
            self.assertEqual(proc.returncode, 2)
            self.assertFalse((target / "workbook-review").exists())
            os.rmdir(link)

    def test_real_format_binding(self) -> None:
        book = self.book("fmt")
        page_id = "0599.synth-review"
        note = b"NOTE the disposable artifact is this file.\n"
        returned = b"Did.\nThe disposable capture returned one note.\n"
        qualified = b"qualified book file\n"
        write(book / "0596.synth-root" / "note.md", qualified)
        extras = []
        for index in range(13):
            blob = f"artifact {index}\n".encode("utf-8")
            rel = f"extra/n{index}.txt"
            write(book / rel, blob)
            extras.append({"bytes": len(blob), "path": rel, "sha256": sha(blob)})
        code_rel = "app/review-loop-v5.json"
        code_bytes = (ROOT / code_rel).read_bytes()
        extras.append({"bytes": len(code_bytes), "path": code_rel, "sha256": sha(code_bytes)})
        qualified_declared = "00.kernel/00.00.10.work/0596.synth-root/note.md"
        extras.append({"bytes": len(qualified), "path": qualified_declared, "sha256": sha(qualified)})
        submission = (
            "The builder returned one note and one artifact. "
            "The verification file is mentioned in prose and is not a measured verification line. "
            "This sentence is repeated so the submission is a substantive packet rather than a short label. "
        ).encode("utf-8") * 4
        manifest = pretty({"files": [{"bytes": len(note), "path": "note.md", "sha256": sha(note)}, *extras], "schema": "example-manifest/1"})
        write(book / "evidence" / "submission.md", submission)
        write(book / "evidence" / "artifact-manifest.json", manifest)
        write(book / "note.md", note)
        write(book / "0199.synth-review" / "05.01.return.md", returned)
        pointer = (
            f"Submission: evidence/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
            f"Artifact manifest: evidence/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes. "
            "The manifest lists the files and excludes itself.\n"
            "Note: this line stays a finding.\n"
        )
        write(book / page_id / "05.01.md", page(pointer, newline="\r\n"))
        proc, prepared = call(book, "prepare", source=page_id, pass_="05.01")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        self.assertEqual(prepared["custody"], "missing")
        self.assertEqual(prepared["director_text"], "Pack it up.")
        self.assertNotIn("\r", prepared["director_text"])
        self.assertEqual(prepared["measurement"], "complete")
        found = codes(prepared)
        self.assertIn("unparsed-return-line", found)
        self.assertIn("verification-not-measured", found)
        self.assertIn("index-context-bounded", found)
        self.assertNotIn("thin-submission", found)
        bound = rows(prepared)
        roles = {}
        for row in bound:
            roles.setdefault(row["role"], []).append(row)
        self.assertEqual(len(roles["artifact"]), 16)
        self.assertTrue(any(row["root"] == "code" and row["declared_path"] == code_rel for row in roles["artifact"]))
        qualified_row = next(row for row in roles["artifact"] if row["declared_path"] == qualified_declared)
        self.assertEqual(qualified_row["root"], "book")
        self.assertEqual(qualified_row["path"], "0596.synth-root/note.md")
        self.assertTrue(any(row["role"] == "submission" and row["sha256"] == sha(submission) for row in bound))
        artifact_cuts = [item for item in prepared["cuts"] if item.get("role") == "artifact"]
        self.assertLessEqual(len(artifact_cuts), 12)
        form_path = book / "judgment.json"
        write(form_path, pretty(judgment()))
        proc, recorded = call(book, "record", source=page_id, pass_="05.01", intake=prepared["intake_id"], judgment=str(form_path))
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        self.assertIsNone(recorded["judgment"]["sections"]["tests_passed"])
        proc, again = call(book, "record", source=page_id, pass_="05.01", intake=prepared["intake_id"], judgment=str(form_path))
        self.assertEqual(proc.returncode, 0)
        self.assertTrue(again["already_recorded"])
        self.assertEqual(again["review_id"], recorded["review_id"])
        thin_page = "0594.synth-thin"
        thin_src = (ROOT / "00.kernel/00.00.10.work/0521.return-placement/evidence/build05.06/submission.md").read_bytes()
        write(book / "evidence" / "thin-submission.md", thin_src)
        thin_manifest = pretty({"files": [], "schema": "example-manifest/1"})
        write(book / "evidence" / "thin-manifest.json", thin_manifest)
        thin_pointer = (
            f"Submission: evidence/thin-submission.md sha256 {sha(thin_src)}, {len(thin_src)} bytes.\n"
            f"Artifact manifest: evidence/thin-manifest.json sha256 {sha(thin_manifest)}, {len(thin_manifest)} bytes.\n"
        )
        write(book / thin_page / "05.08.md", page(thin_pointer))
        proc, thin = call(book, "prepare", source=thin_page, pass_="05.08")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        thin_rows = [row for row in rows(thin) if row["role"] == "submission"]
        self.assertEqual(thin_rows[0]["sha256"], sha(thin_src))
        if len(thin_src) < 400:
            self.assertIn("thin-submission", codes(thin))
        else:
            self.assertNotIn("thin-submission", codes(thin))
        clash = book / "app" / "review-loop-v4.json"
        write(clash, b"not the repo file\n")
        clash_manifest = pretty({
            "files": [{"bytes": len((ROOT / "app/review-loop-v4.json").read_bytes()), "path": "app/review-loop-v4.json", "sha256": sha((ROOT / "app/review-loop-v4.json").read_bytes())}],
            "schema": "example-manifest/1",
        })
        write(book / "evidence" / "clash-manifest.json", clash_manifest)
        clash_pointer = (
            f"Submission: evidence/thin-submission.md sha256 {sha(thin_src)}, {len(thin_src)} bytes.\n"
            f"Artifact manifest: evidence/clash-manifest.json sha256 {sha(clash_manifest)}, {len(clash_manifest)} bytes.\n"
        )
        write(book / "0593.synth-clash" / "05.09.md", page(clash_pointer))
        proc, clashed = call(book, "prepare", source="0593.synth-clash", pass_="05.09")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        self.assertIn("ambiguous-declared-root", codes(clashed))
        self.assertEqual(clashed["measurement"], "incomplete")
        self.assertFalse(any(row["role"] == "artifact" and row.get("declared_path") == "app/review-loop-v4.json" for row in rows(clashed)))

    def test_ambiguous_incomplete_and_omission(self) -> None:
        book = self.book("badptr")
        page_id = "0598.synth-hold"
        submission = b"A substantive submission with enough bytes to be more than a label.\n"
        manifest = pretty({"files": [{"bytes": 1, "path": "missing-artifact.txt", "sha256": "ab", }], "schema": "example-manifest/1"})
        # hash length will mismatch and the file is missing; use a real digest of absent bytes by pointing at a missing path
        missing = {"bytes": 4, "path": "missing-artifact.txt", "sha256": sha(b"nope")}
        manifest = pretty({"files": [missing], "schema": "example-manifest/1"})
        write(book / "evidence" / "submission.md", submission)
        write(book / "evidence" / "artifact-manifest.json", manifest)
        pointer = (
            f"Submission: evidence/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
            f"Submission: evidence/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
            f"Artifact manifest: evidence/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes.\n"
        )
        write(book / page_id / "05.02.md", page(pointer))
        proc, prepared = call(book, "prepare", source=page_id, pass_="05.02")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:600])
        found = codes(prepared)
        self.assertIn("ambiguous-submission", found)
        self.assertIn("artifact-missing", found)
        self.assertFalse(any(row["role"] == "submission" for row in rows(prepared)))
        self.assertTrue(any(row["role"] == "artifact-manifest" for row in rows(prepared)))
        self.assertEqual(prepared["measurement"], "incomplete")
        bad = judgment()
        del bad["semantic_conflict"]
        path = book / "omitted.json"
        write(path, pretty(bad))
        proc, failed = call(book, "record", source=page_id, pass_="05.02", intake=prepared["intake_id"], judgment=str(path))
        self.assertEqual(proc.returncode, 2)
        self.assertIn("semantic_conflict", failed.get("correction", ""))
        self.assertTrue((book / failed["failed_input"]).is_file())
        good = book / "good.json"
        write(good, pretty(judgment()))
        proc, refused = call(book, "record", source=page_id, pass_="05.02", intake=prepared["intake_id"], judgment=str(good))
        self.assertEqual(proc.returncode, 2)
        self.assertIn("incomplete", refused.get("correction", ""))
        self.assertFalse(refused.get("recorded"))

    def test_publish_freshness_and_tamper(self) -> None:
        book = self.book("fresh")
        page_id = "0597.synth-bad"
        submission = b"Substantive submission for the freshness case. It names verification in prose only.\n"
        note = b"NOTE one\n"
        manifest = pretty({"files": [{"bytes": len(note), "path": "note.md", "sha256": sha(note)}], "schema": "example-manifest/1"})
        write(book / "evidence" / "submission.md", submission)
        write(book / "evidence" / "artifact-manifest.json", manifest)
        write(book / "note.md", note)
        write(book / "0197.synth-bad" / "05.03.return.md", b"Did.\nReturn one.\n")
        pointer = (
            f"Submission: evidence/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
            f"Artifact manifest: evidence/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes.\n"
        )
        write(book / page_id / "05.03.md", page(pointer))
        proc, prepared = call(book, "prepare", source=page_id, pass_="05.03")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:500])
        path = book / "judgment.json"
        write(path, pretty(judgment()))
        proc, recorded = call(book, "record", source=page_id, pass_="05.03", intake=prepared["intake_id"], judgment=str(path))
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:400])
        review = recorded["review_id"]
        proc, published = call(book, "publish", source=page_id, pass_="05.03", review=review)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:400])
        self.assertTrue(published["published"])
        proc, read = call(book, "read", source=page_id, pass_="05.03")
        self.assertEqual(proc.returncode, 0, proc.stdout.decode()[:500])
        self.assertIs(read["stale"], False)
        self.assertEqual(read["judgment"]["finding"], "The disposable note is present.")
        proc, recovered = call(book, "recover", source=page_id, pass_="05.03")
        self.assertEqual(proc.returncode, 0)
        self.assertIs(recovered["stale"], False)
        proc, inspected = call(book, "inspect", source=page_id, pass_="05.03")
        self.assertEqual(proc.returncode, 0)
        self.assertIs(inspected["stale"], False)
        page_path = book / page_id / "05.03.md"
        before = page_path.read_bytes()
        page_path.write_bytes(before.replace(b"Intro OUTSIDE", b"Intro CHANGED", 1))
        proc, read = call(book, "read", source=page_id, pass_="05.03")
        self.assertEqual(proc.returncode, 1)
        self.assertIs(read["stale"], True)
        self.assertEqual(read["judgment"]["finding"], "The disposable note is present.")
        proc, recovered = call(book, "recover", source=page_id, pass_="05.03")
        self.assertEqual(proc.returncode, 1)
        self.assertIs(recovered["stale"], True)
        proc, inspected = call(book, "inspect", source=page_id, pass_="05.03")
        self.assertEqual(proc.returncode, 0)
        self.assertIs(inspected["stale"], True)
        page_path.write_bytes(before)

        other = self.book("tamper")
        other_page = "0798.synth-local"
        write(other / other_page / "05.04.md", page("PENDING.\n"))
        write(other / other_page / "05.04.return.md", b"Did.\nLocal return.\n")
        proc, prepared = call(other, "prepare", source=other_page, pass_="05.04")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        write(other / "local.json", pretty(judgment()))
        proc, recorded = call(other, "record", source=other_page, pass_="05.04", intake=prepared["intake_id"], judgment=str(other / "local.json"))
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:600] + proc.stdout.decode()[:400])
        review = recorded["review_id"]
        proc, published = call(other, "publish", source=other_page, pass_="05.04", review=review)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:600])
        target = other / other_page / "06.04.review.md"
        target_before = target.read_bytes()
        rendered = other / "workbook-review" / other_page / "05.04" / "reviews" / review / "rendered.md"
        rendered.write_bytes(rendered.read_bytes() + b"UNRECORDED ALTERATION\n")
        proc, tampered = call(other, "publish", source=other_page, pass_="05.04", review=review)
        self.assertEqual(proc.returncode, 1, proc.stdout.decode()[:600])
        self.assertFalse(tampered["published"])
        self.assertEqual(target.read_bytes(), target_before)
        self.assertNotIn(b"UNRECORDED ALTERATION", target.read_bytes())
        self.assertEqual(tampered["judgment"]["finding"], "The disposable note is present.")

        changed = self.book("source")
        changed_page = "0797.synth-local"
        write(changed / changed_page / "05.05.md", page("PENDING.\n"))
        return_path = changed / changed_page / "05.05.return.md"
        write(return_path, b"Did.\nReturn before.\n")
        proc, prepared = call(changed, "prepare", source=changed_page, pass_="05.05")
        write(changed / "c.json", pretty(judgment()))
        proc, recorded = call(changed, "record", source=changed_page, pass_="05.05", intake=prepared["intake_id"], judgment=str(changed / "c.json"))
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:500])
        proc, published = call(changed, "publish", source=changed_page, pass_="05.05", review=recorded["review_id"])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:500])
        return_path.write_bytes(b"Did.\nReturn after publication.\n")
        proc, inspected = call(changed, "inspect", source=changed_page, pass_="05.05")
        self.assertEqual(proc.returncode, 0)
        self.assertIs(inspected["stale"], True)
        proc, recovered = call(changed, "recover", source=changed_page, pass_="05.05")
        self.assertEqual(proc.returncode, 1)
        self.assertIs(recovered["stale"], True)
        proc, read = call(changed, "read", source=changed_page, pass_="05.05")
        self.assertEqual(proc.returncode, 1)
        self.assertIs(read["stale"], True)
        self.assertEqual(read["next_action"], judgment()["next_action"])

    def test_interrupt_conflict_and_manual(self) -> None:
        book = self.book("block")
        page_id = "0796.synth-local"
        write(book / page_id / "05.06.md", page("PENDING.\n", review="Manual note stays.\n"))
        write(book / page_id / "05.06.return.md", b"Did.\nManual return.\n")
        proc, prepared = call(book, "prepare", source=page_id, pass_="05.06")
        self.assertEqual(proc.returncode, 0)
        # N7 with both md and pack is a different page. This page has only md, so it is the assignment.
        # The review body is manual. Publish must keep it.
        write(book / "j.json", pretty(judgment()))
        proc, recorded = call(book, "record", source=page_id, pass_="05.06", intake=prepared["intake_id"], judgment=str(book / "j.json"))
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:500])
        # N7 publishes a new review file, not the assignment section. Use a second pass for the read-only file.
        target_page = "0795.synth-local"
        target = book / target_page / "05.07.md"
        write(target, page("PENDING.\n"))
        write(book / target_page / "05.07.return.md", b"Did.\nInterrupt return.\n")
        proc, prepared = call(book, "prepare", source=target_page, pass_="05.07")
        proc, recorded = call(book, "record", source=target_page, pass_="05.07", intake=prepared["intake_id"], judgment=str(book / "j.json"))
        self.assertEqual(proc.returncode, 0, proc.stdout.decode()[:400])
        review_file = book / target_page / "06.07.review.md"
        review_file.parent.mkdir(parents=True, exist_ok=True)
        review_file.write_bytes(b"PENDING.\n")
        os.chmod(review_file, stat.S_IREAD)
        proc, interrupted = call(book, "publish", source=target_page, pass_="05.07", review=recorded["review_id"])
        os.chmod(review_file, stat.S_IWRITE | stat.S_IREAD)
        self.assertEqual(proc.returncode, 1, proc.stdout.decode()[:500] + proc.stderr.decode()[:300])
        self.assertFalse(interrupted["published"])
        journal = json.loads((book / "workbook-review" / target_page / "05.07" / "journal.json").read_text(encoding="utf-8"))
        self.assertEqual(journal["publication"]["status"], "pointer-pending")
        proc, recovered = call(book, "recover", source=target_page, pass_="05.07")
        self.assertEqual(recovered["target_state"], "pointer-pending")
        self.assertEqual(recovered["judgment"]["next_action"], judgment()["next_action"])
        other = judgment(finding="A different finding.")
        write(book / "other.json", pretty(other))
        proc, conflict = call(book, "record", source=target_page, pass_="05.07", intake=prepared["intake_id"], judgment=str(book / "other.json"))
        self.assertEqual(proc.returncode, 2)
        self.assertFalse(conflict.get("recorded"))

    def test_filed_two_sources_and_successor(self) -> None:
        book = self.book("filed")
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        init = subprocess.run(
            [str(PY), "-B", str(LINES), "init", "--book", str(book), "--name", "00.00.10.work"],
            cwd=str(ROOT), env=env, capture_output=True,
        )
        self.assertEqual(init.returncode, 0, init.stderr.decode()[:400])
        specs = [
            ("0596.synth-filed", "05.01", "sub-filed-a", b"NOTE the first filed artifact is substantive.\n", b"Did.\nThe first filed capture returned one substantive note.\n"),
            ("0595.synth-filed", "05.02", "sub-filed-b", b"NOTE the second filed artifact is substantive.\n", b"Did.\nThe second filed capture returned one substantive note.\n"),
        ]
        reviews = {}
        for page_id, pass_id, submission_id, note, returned in specs:
            inputs = book / f"_inputs-{pass_id}"
            note_rel = f"notes/note-{pass_id}.md"
            evidence_home = f"evidence/{pass_id}"
            write(inputs / "return.md", returned)
            write(inputs / "note.md", note)
            write(book / note_rel, note)
            reserve = subprocess.run(
                [str(PY), "-B", str(LINES), "reserve", "--book", str(book), "--page", page_id, "--batch", pass_id,
                 "--submission", submission_id, "--output", note_rel, "--submitter", "grok-1",
                 "--reviewer", "codex-prime", "--release", "prepared"],
                cwd=str(ROOT), env=env, capture_output=True,
            )
            self.assertIn(reserve.returncode, {0, 1}, reserve.stderr.decode()[:500] + reserve.stdout.decode()[:500])
            capture = subprocess.run(
                [str(PY), "-B", str(LINES), "capture", "--book", str(book), "--page", page_id, "--batch", pass_id,
                 "--submission", submission_id, "--return-file", str(inputs / "return.md"),
                 "--artifact", note_rel, str(inputs / "note.md")],
                cwd=str(ROOT), env=env, capture_output=True,
            )
            self.assertEqual(capture.returncode, 0, capture.stderr.decode()[:600] + capture.stdout.decode()[:600])
            verification = pretty({"note": pass_id, "schema": "example-verification/1"})
            submission_text = (
                "The filed capture returned the note. This submission points at the verification and is not the only packet.\n"
                f"Verification: {evidence_home}/verification.json sha256 {sha(verification)}, {len(verification)} bytes.\n"
            ).encode("utf-8")
            manifest = pretty({"files": [{"bytes": len(note), "path": note_rel, "sha256": sha(note)}], "schema": "example-manifest/1"})
            write(book / evidence_home / "verification.json", verification)
            write(book / evidence_home / "submission.md", submission_text)
            write(book / evidence_home / "artifact-manifest.json", manifest)
            pointer = (
                f"Submission: {evidence_home}/submission.md sha256 {sha(submission_text)}, {len(submission_text)} bytes.\n"
                f"Artifact manifest: {evidence_home}/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes.\n"
            )
            write(book / page_id / f"{pass_id}.md", page(pointer))
            proc, prepared = call(book, "prepare", source=page_id, pass_=pass_id)
            self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
            self.assertEqual(prepared["custody"], "complete-descriptor", prepared.get("findings"))
            write(book / f"{pass_id}.json", pretty(judgment()))
            proc, recorded = call(book, "record", source=page_id, pass_=pass_id, intake=prepared["intake_id"], judgment=str(book / f"{pass_id}.json"))
            self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:1200])
            self.assertEqual(recorded["mode"], "cycle-committed", recorded.get("cycle"))
            self.assertNotIn("-wb", recorded["cycle"].get("cycle_review_id", ""))
            self.assertTrue(recorded["cycle"]["cycle_review_id"].endswith(recorded["review_id"]))
            proc, published = call(book, "publish", source=page_id, pass_=pass_id, review=recorded["review_id"])
            self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
            self.assertTrue(published["published"])
            self.assertIn("TAIL", (book / page_id / f"{pass_id}.md").read_text(encoding="utf-8"))
            reviews[page_id] = (pass_id, recorded, prepared["intake_id"], (book / page_id / f"{pass_id}.md").read_bytes())
        self.assertFalse((book / "workbook-review" / "cycle" / "decision.json").exists())
        first_pass, first, intake_id, first_bytes = reviews["0596.synth-filed"]
        second_pass, second, _intake_b, _bytes_b = reviews["0595.synth-filed"]
        self.assertNotEqual(first["review_id"], second["review_id"])
        self.assertNotEqual(first["cycle"]["request"], second["cycle"]["request"])
        reply = "Stay on this page. The reply is not a release."
        successor = judgment(
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
                "question_sha256": sha(reply.encode("utf-8")),
                "reply": reply,
            }],
            finding="The Director reply is recorded and the finding stays open.",
        )
        write(book / "successor.json", pretty(successor))
        proc, followed = call(
            book, "record", source="0596.synth-filed", pass_=first_pass, intake=intake_id,
            judgment=str(book / "successor.json"), successor=first["review_id"],
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:1200])
        self.assertNotEqual(followed["review_id"], first["review_id"])
        self.assertEqual(followed["judgment"]["answers"][0]["reply"], reply)
        self.assertFalse(followed["closes_work"])
        old = json.loads((book / "workbook-review" / "0596.synth-filed" / first_pass / "reviews" / first["review_id"] / "record.json").read_text(encoding="utf-8"))
        self.assertEqual(old["judgment"]["finding"], "The disposable note is present.")
        self.assertEqual(old["judgment"]["answers"], [])
        proc, published = call(book, "publish", source="0596.synth-filed", pass_=first_pass, review=followed["review_id"])
        self.assertEqual(proc.returncode, 1, proc.stdout.decode()[:800] + proc.stderr.decode()[:400])
        self.assertFalse(published["published"])
        self.assertEqual((book / "0596.synth-filed" / f"{first_pass}.md").read_bytes(), first_bytes)
        self.assertIn(reply, json.dumps(followed["judgment"]))
        second_record = book / "workbook-review" / "0595.synth-filed" / second_pass / "reviews" / second["review_id"] / "record.json"
        self.assertTrue(second_record.is_file())
        proc, recovered = call(book, "recover", source="0595.synth-filed", pass_=second_pass)
        self.assertEqual(proc.returncode, 0, proc.stdout.decode()[:600])
        self.assertEqual(recovered["judgment"]["finding"], "The disposable note is present.")
        self.assertFalse(recovered["closes_work"])


if __name__ == "__main__":
    unittest.main()
