#!/usr/bin/env python3
"""Focused operator cases for the 05.13 return-intake repair, through app/librarian.py."""

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
KEEP = Path(os.environ.get("WORKBOOK_KEEP", r"D:\librarian\temp\0522-0513-pass03"))
WORK = ROOT / "00.kernel" / "00.00.10.work"
LIVE = WORK / "0521.return-placement" / "05.10.md"
FIXTURE = WORK / "0522.review-construction" / "evidence" / "prime-review05.12" / "reproducer"
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
    return found if isinstance(found, list) else []


def declared(payload: dict, code: str) -> dict:
    for item in payload.get("findings", []):
        if isinstance(item, dict) and item.get("code") == code:
            return item
    return {}


class IntakeRepair(unittest.TestCase):
    def setUp(self) -> None:
        self.books = []

    def book(self, name: str) -> Path:
        path = Path(tempfile.mkdtemp(prefix=f"wb0513-{name}-"))
        self.books.append(path)
        return path

    def tearDown(self) -> None:
        KEEP.mkdir(parents=True, exist_ok=True)
        for path in self.books:
            dest = KEEP / path.name
            if dest.exists():
                shutil.rmtree(dest, ignore_errors=True)
            shutil.copytree(path, dest, dirs_exist_ok=True)

    def test_pins_and_doors(self) -> None:
        pins = {
            "labs/workbook-review-pass02/workbook.py": ("6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a", 52574),
            "labs/workbook-review-pass02/forms/workbook-review-v1.json": ("66b3f8f70f8e5d2f940296918767ff0e712e7e144378ad8653259e83d3284645", 4532),
            "labs/workbook-review-pass01/workbook.py": ("60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a", 79131),
            "labs/workbook-review-pass01/forms/workbook-review-v1.json": ("152b436bda8e19d15f252bb5208791c8eefd9a658789e2ab6e9789ffa362b49f", 4532),
            "app/review_loop_tools_v6.py": ("e2a5df36efe29f9dad8abd8fa0f842fd98941d58ca1eb3cd4be5227e20420a94", 9175),
            "app/review-loop-v6.json": ("c7f95d16f91644c6465fd3483e3db4d6fb9b9115aa6e20fc09a194fc5bb1f0aa", 2743),
            "app/review_loop_tools_v5.py": ("b1192daf5d265c66f10adfe2125ff0c92a08ccd3c797d229698ecc20e2fdeed9", 7875),
            "app/review-loop-v5.json": ("eaa9120bba2c7274f2218c875ec3ecfc84d291188557049240c30a1c2a430de3", 1964),
            "app/review_loop_tools_v4.py": ("0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296", 13381),
            "app/review-loop-v4.json": ("769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723", 2519),
        }
        for rel, (digest, size) in pins.items():
            data = (ROOT / rel).read_bytes()
            self.assertEqual((len(data), sha(data)), (size, digest), rel)
        door = (ROOT / "app" / "review_loop_tools_v7.py").read_bytes()
        workbook = (ROOT / "labs" / "workbook-review-pass03" / "workbook.py").read_bytes()
        declaration = json.loads((ROOT / "app" / "review-loop-v7.json").read_text(encoding="utf-8"))
        self.assertEqual(declaration["schema"], "review-loop-pins/5")
        pinned = declaration["tools"]["workbook"]
        self.assertEqual(pinned["path"], "labs/workbook-review-pass03/workbook.py")
        self.assertEqual((pinned["bytes"], pinned["sha256"]), (len(workbook), sha(workbook)))
        self.assertNotIn(sha(workbook).encode("ascii"), door)
        self.assertIn(b"6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a", door)
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
        proc = run_app([
            "review-loop", "record", "--book", str(ROOT), "--source", "0599.synth-review",
            "--pass", "05.01", "--intake", "ab", "--judgment", str(book / "missing.json"),
        ])
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"checkout", proc.stderr.lower() + proc.stdout)
        proc = run_app(["return-lines", "status", "--book", str(book)])
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        body = json.loads(proc.stdout.decode("utf-8"))
        self.assertFalse(body["accepted"])
        self.assertEqual(body["task_association"], "not-established")
        left = self.book("id-a")
        right = self.book("id-b")
        write(left / "0592.id-left" / "05.01.md", page("PENDING.\n"))
        write(right / "0592.id-left" / "05.01.md", page("PENDING.\n"))
        _, one = call(left, "prepare", source="0592.id-left", pass_="05.01")
        _, two = call(right, "prepare", source="0592.id-left", pass_="05.01")
        self.assertNotEqual(one["instance_id"], two["instance_id"])
        link = book / "linked-book"
        try:
            subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(ROOT / "labs")], check=True, capture_output=True)
        except (OSError, subprocess.CalledProcessError):
            return
        proc = run_app([
            "review-loop", "record", "--book", str(link), "--source", "0599.synth-review",
            "--pass", "05.01", "--intake", "ab", "--judgment", str(book / "missing.json"),
        ])
        self.assertEqual(proc.returncode, 2)
        self.assertFalse((ROOT / "labs" / "workbook-review").exists())
        os.rmdir(link)

    def test_exact_copy_and_live_book(self) -> None:
        book = self.book("realcopy")
        home = book / "0521.return-placement"
        for rel in (
            "05.10.md",
            "evidence/build05.10/submission.md",
            "evidence/build05.10/artifact-manifest.json",
            "evidence/build05.10/verification.json",
        ):
            source = WORK / "0521.return-placement" / rel
            write(home / rel, source.read_bytes())
        proc, prepared = call(book, "prepare", source="0521.return-placement", pass_="05.10")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:600] + proc.stdout.decode()[:600])
        found = codes(prepared)
        self.assertIn("ambiguous-declared-root", found)
        self.assertIn("verification-declared", found)
        self.assertNotIn("manifest-count-mismatch", found)
        self.assertNotIn("unparsed-return-line", found)
        self.assertEqual(prepared["measurement"], "incomplete")
        bound = rows(prepared)
        submission = next(row for row in bound if row["role"] == "submission")
        self.assertEqual(submission["root"], "book")
        self.assertEqual(submission["path"], "0521.return-placement/evidence/build05.10/submission.md")
        self.assertEqual(submission["sha256"], "ddccb9110a02d82df300adffc25870c8ebf24d0815dab2651c67ececfaf36de8")
        verification = next(row for row in bound if row["role"] == "verification")
        self.assertEqual(verification["root"], "book")
        self.assertEqual(verification["sha256"], "99497147811cdd4009cfafca11be8594c943971ac63add170b032f9408d81f45")
        self.assertTrue(any(row["role"] == "artifact-manifest" and row["root"] == "book" for row in bound))
        qualified = "00.kernel/00.00.10.work/0521.return-placement/evidence/build05.10/submission.md"
        self.assertFalse(any(row.get("declared_path") == qualified and row.get("role") == "artifact" for row in bound))
        code_row = next(row for row in bound if row.get("declared_path") == "00.kernel/00.00.10.work/0521.return-placement/06.20.md")
        self.assertEqual(code_row["root"], "code")
        coverage = declared(prepared, "verification-declared")
        self.assertFalse(coverage["successful_run"])
        self.assertTrue(coverage["measured"])
        self.assertTrue(coverage["hash_match"])
        self.assertEqual(coverage["sources"], ["submission-lines"])
        self.assertEqual(coverage["schema"], "return-route-readiness-verification/0510")

        before = LIVE.read_bytes()
        store = WORK / "workbook-review" / "0521.return-placement"
        existed = store.exists()
        proc, live = call(WORK, "prepare", source="0521.return-placement", pass_="05.10")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        self.assertEqual(proc.stderr, b"")
        self.assertEqual(LIVE.read_bytes(), before)
        self.assertEqual(store.exists(), existed)
        self.assertEqual(live["measurement"], "complete")
        self.assertEqual(live["custody"], "missing")
        self.assertIsNone(live["director_text"])
        live_codes = codes(live)
        self.assertIn("verification-declared", live_codes)
        self.assertIn("index-context-bounded", live_codes)
        self.assertIn("custody-missing", live_codes)
        self.assertIn("return-missing", live_codes)
        for absent in (
            "unparsed-return-line", "declared-file-missing", "verification-not-measured",
            "manifest-count-mismatch", "source-identity-conflict", "ambiguous-declared-root",
        ):
            self.assertNotIn(absent, live_codes)
        live_rows = rows(live)
        artifacts = [row for row in live_rows if row["role"] == "artifact"]
        self.assertEqual(len(artifacts), 16)
        for row in artifacts:
            if str(row["declared_path"]).startswith("00.kernel/00.00.10.work/"):
                self.assertEqual(row["root"], "book", row["declared_path"])
            if str(row["declared_path"]).startswith("labs/"):
                self.assertEqual(row["root"], "code", row["declared_path"])
        live_sub = next(row for row in live_rows if row["role"] == "submission")
        self.assertEqual(live_sub["root"], "book")
        self.assertEqual(live_sub["path"], "0521.return-placement/evidence/build05.10/submission.md")
        live_ver = next(row for row in live_rows if row["role"] == "verification")
        self.assertEqual(live_ver["path"], "0521.return-placement/evidence/build05.10/verification.json")
        live_cover = declared(live, "verification-declared")
        self.assertFalse(live_cover["successful_run"])
        self.assertEqual(live_cover["sources"], ["submission-lines", "artifact-index"])
        self.assertEqual(live["unknowns"], ["agreement.goal", "agreement.scope", "recorded_decisions", "receipt"])
        artifact_cuts = [item for item in live["cuts"] if item.get("role") == "artifact"]
        self.assertEqual(len(artifact_cuts), 12)

    def test_overlap_alias_and_positive_record(self) -> None:
        book = self.book("overlap")
        shutil.copytree(FIXTURE / "0599.fixture-review", book / "0599.fixture-review")
        proc, prepared = call(book, "prepare", source="0599.fixture-review", pass_="05.01")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:600])
        self.assertEqual(prepared["measurement"], "complete")
        bound = rows(prepared)
        sub_path = "0599.fixture-review/evidence/build05.01/submission.md"
        ver_path = "0599.fixture-review/evidence/build05.01/VERIFICATION.md"
        self.assertTrue(any(row["role"] == "submission" and row["path"] == sub_path for row in bound))
        self.assertTrue(any(row["role"] == "artifact" and row["path"] == sub_path for row in bound))
        self.assertTrue(any(row["role"] == "verification" and row["path"] == ver_path for row in bound))
        self.assertTrue(any(row["role"] == "artifact" and row["path"] == ver_path for row in bound))
        proc, recorded = call(
            book, "record", source="0599.fixture-review", pass_="05.01",
            intake=prepared["intake_id"], judgment=str(FIXTURE / "judgment.json"),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        self.assertTrue(recorded["recorded"])
        self.assertFalse(recorded["closes_work"])
        prime = json.loads((book / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))
        paths = [item["logical_path"] for item in prime["sources"]]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertIn(sub_path, paths)
        self.assertIn(ver_path, paths)
        for item in prime["sources"]:
            if item["kind"] == "supplied-text":
                self.assertEqual(set(item["identity"]), {"schema", "label"})
                self.assertEqual(item["identity"]["label"], "SUPPLIED")

        page_id = "0591.intake-repair"
        positive = self.book("positive")
        payload = b"NOTE the overlap artifact is this payload.\n"
        verification = b'{"schema":"example-verification/1","passed":false}\n'
        home = f"{page_id}/evidence/build05.01"
        submission = (
            "The builder returned the payload and named the verification.\n"
            f"Verification: `{home}/verification.json`\n"
            "Schema: `example-verification/1`\n"
            f"sha256: `{sha(verification)}`\n"
            f"bytes: {len(verification)}\n"
        ).encode("utf-8")
        files = [
            {"bytes": len(submission), "path": f"{home}/submission.md", "sha256": sha(submission)},
            {"bytes": len(verification), "path": f"{home}/verification.json", "sha256": sha(verification)},
            {"bytes": len(payload), "path": f"{home}/payload.txt", "sha256": sha(payload)},
        ]
        manifest = pretty({"files": files, "schema": "example-manifest/1"})
        write(positive / home / "submission.md", submission)
        write(positive / home / "verification.json", verification)
        write(positive / home / "payload.txt", payload)
        write(positive / home / "artifact-manifest.json", manifest)
        pointer = (
            f"Submission: evidence/build05.01/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
            f"Artifact manifest: evidence/build05.01/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes, "
            "3 files. Excludes itself and this page.\n"
        )
        write(positive / page_id / "05.01.md", page(pointer))
        proc, prepared = call(positive, "prepare", source=page_id, pass_="05.01")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        self.assertEqual(prepared["measurement"], "complete")
        self.assertEqual(prepared["director_text"], "Pack it up.")
        cover = declared(prepared, "verification-declared")
        self.assertEqual(cover["sources"], ["submission-lines", "artifact-index"])
        self.assertFalse(cover["successful_run"])
        self.assertNotIn("verification-not-measured", codes(prepared))
        proc, formed = call(positive, "form", source=page_id, pass_="05.01")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        self.assertEqual(formed["form"]["form_id"], "workbook-review-v1")
        write(positive / "judgment.json", pretty(judgment()))
        proc, recorded = call(
            positive, "record", source=page_id, pass_="05.01",
            intake=prepared["intake_id"], judgment=str(positive / "judgment.json"),
        )
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        prime = json.loads((positive / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))
        paths = [item["logical_path"] for item in prime["sources"]]
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(paths.count(f"{home}/submission.md"), 1)
        kept = rows(prepared)
        self.assertTrue(any(row["role"] == "submission" and row["path"] == f"{home}/submission.md" for row in kept))
        self.assertTrue(any(row["role"] == "artifact" and row["path"] == f"{home}/submission.md" for row in kept))
        review = recorded["review_id"]
        proc, published = call(positive, "publish", source=page_id, pass_="05.01", review=review)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:600])
        self.assertTrue(published["published"])
        proc, read = call(positive, "read", source=page_id, pass_="05.01")
        self.assertEqual(proc.returncode, 0, proc.stdout.decode()[:500])
        self.assertIs(read["stale"], False)
        proc, recovered = call(positive, "recover", source=page_id, pass_="05.01")
        self.assertEqual(proc.returncode, 0)
        self.assertIs(recovered["stale"], False)
        self.assertEqual(recovered["judgment"]["finding"], "The disposable note is present.")

        alias = self.book("alias")
        alias_page = "0590.alias-file"
        note = b"NOTE one shared file.\n"
        alias_home = f"{alias_page}/evidence"
        write(alias / alias_home / "note.md", note)
        manifest = pretty({"files": [{"bytes": len(note), "path": f"{alias_home}/note.md", "sha256": sha(note)}], "schema": "example-manifest/1"})
        write(alias / "evidence" / "artifact-manifest.json", manifest)
        submission = b"The alias submission names one note and is long enough to be a packet.\n" * 3
        write(alias / "evidence" / "submission.md", submission)
        pointer = (
            f"Submission: evidence/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
            f"Artifact manifest: evidence/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes, 1 files.\n"
        )
        write(alias / alias_page / "05.02.md", page(pointer))
        # The manifest entry is the page path. The same bytes also sit only at that path.
        proc, prepared = call(alias, "prepare", source=alias_page, pass_="05.02")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:500])
        self.assertEqual(prepared["measurement"], "complete")
        write(alias / "j.json", pretty(judgment()))
        proc, recorded = call(alias, "record", source=alias_page, pass_="05.02", intake=prepared["intake_id"], judgment=str(alias / "j.json"))
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:600] + proc.stdout.decode()[:400])
        prime = json.loads((alias / "workbook-review" / "tmp" / "prime-input.json").read_text(encoding="utf-8"))
        paths = [item["logical_path"] for item in prime["sources"]]
        self.assertEqual(paths.count(f"{alias_home}/note.md"), 1)

        clash = self.book("clash")
        clash_page = "0589.two-roots"
        write(clash / "evidence" / "note.md", b"ROOT\n")
        write(clash / clash_page / "evidence" / "note.md", b"PAGE\n")
        submission = b"A submission that points at an ambiguous note and is not a short label.\n"
        manifest = pretty({"files": [], "schema": "example-manifest/1"})
        write(clash / "evidence" / "submission.md", submission)
        write(clash / "evidence" / "artifact-manifest.json", manifest)
        pointer = (
            f"Submission: evidence/note.md sha256 {sha(b'ROOT\n')}, {len(b'ROOT\n')} bytes.\n"
            f"Artifact manifest: evidence/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes.\n"
        )
        write(clash / clash_page / "05.03.md", page(pointer))
        proc, prepared = call(clash, "prepare", source=clash_page, pass_="05.03")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        self.assertIn("ambiguous-declared-root", codes(prepared))
        self.assertEqual(prepared["measurement"], "incomplete")
        self.assertFalse(any(row["role"] == "submission" for row in rows(prepared)))

    def test_grammar_holds(self) -> None:
        book = self.book("grammar")
        page_id = "0588.grammar-hold"
        submission = b"A substantive submission that stays bound beside a bad extra line.\n"
        note = b"NOTE kept.\n"
        manifest = pretty({"files": [{"bytes": len(note), "path": "note.md", "sha256": sha(note)}], "schema": "example-manifest/1"})
        write(book / "evidence" / "submission.md", submission)
        write(book / "evidence" / "artifact-manifest.json", manifest)
        write(book / "note.md", note)
        pointer = (
            f"Submission: evidence/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
            "Note: this line stays a finding.\n"
            f"Artifact manifest: evidence/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes.\n"
        )
        write(book / page_id / "05.04.md", page(pointer))
        proc, prepared = call(book, "prepare", source=page_id, pass_="05.04")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        self.assertIn("unparsed-return-line", codes(prepared))
        self.assertTrue(any(row["role"] == "submission" for row in rows(prepared)))
        self.assertTrue(any(row["role"] == "artifact-manifest" for row in rows(prepared)))

        dup = "0587.dup-label"
        pointer = (
            f"Submission: evidence/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
            f"Submission: evidence/submission.md sha256 {sha(b'other')}, 5 bytes.\n"
            f"Artifact manifest: evidence/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes.\n"
        )
        write(book / dup / "05.05.md", page(pointer))
        proc, prepared = call(book, "prepare", source=dup, pass_="05.05")
        self.assertIn("ambiguous-submission", codes(prepared))
        self.assertFalse(any(row["role"] == "submission" for row in rows(prepared)))
        self.assertTrue(any(row["role"] == "artifact-manifest" for row in rows(prepared)))

        missing = "0586.missing-file"
        pointer = (
            f"Submission: evidence/missing.md sha256 {sha(b'nope')}, 4 bytes.\n"
            f"Artifact manifest: evidence/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes.\n"
        )
        write(book / missing / "05.06.md", page(pointer))
        proc, prepared = call(book, "prepare", source=missing, pass_="05.06")
        self.assertIn("declared-file-missing", codes(prepared))
        self.assertFalse(any(row["role"] == "submission" for row in rows(prepared)))

        counted = "0585.count-mismatch"
        pointer = (
            f"Submission: evidence/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
            f"Artifact manifest: evidence/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes, 2 files.\n"
        )
        write(book / counted / "05.07.md", page(pointer))
        proc, prepared = call(book, "prepare", source=counted, pass_="05.07")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        self.assertIn("manifest-count-mismatch", codes(prepared))
        self.assertEqual(prepared["measurement"], "incomplete")
        self.assertTrue(any(row["role"] == "artifact" and row["path"] == "note.md" for row in rows(prepared)))
        write(book / "good.json", pretty(judgment()))
        proc, refused = call(book, "record", source=counted, pass_="05.07", intake=prepared["intake_id"], judgment=str(book / "good.json"))
        self.assertEqual(proc.returncode, 2)
        self.assertIn("incomplete", refused.get("correction", ""))
        self.assertFalse(refused.get("recorded"))

        conflict = "0584.hash-conflict"
        conflict_manifest = pretty({
            "files": [{"bytes": len(note), "path": "evidence/submission.md", "sha256": sha(b"not the submission")}],
            "schema": "example-manifest/1",
        })
        write(book / "evidence" / "conflict-manifest.json", conflict_manifest)
        pointer = (
            f"Submission: evidence/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
            f"Artifact manifest: evidence/conflict-manifest.json sha256 {sha(conflict_manifest)}, {len(conflict_manifest)} bytes.\n"
        )
        write(book / conflict / "05.08.md", page(pointer))
        proc, prepared = call(book, "prepare", source=conflict, pass_="05.08")
        self.assertIn("source-identity-conflict", codes(prepared))
        self.assertEqual(prepared["measurement"], "incomplete")
        self.assertTrue(any(row["role"] == "submission" and row["path"] == "evidence/submission.md" for row in rows(prepared)))
        self.assertTrue(any(row["role"] == "artifact" and row["path"] == "evidence/submission.md" for row in rows(prepared)))
        proc, refused = call(book, "record", source=conflict, pass_="05.08", intake=prepared["intake_id"], judgment=str(book / "good.json"))
        self.assertEqual(proc.returncode, 2)
        self.assertFalse(refused.get("recorded"))

    def test_publish_seams(self) -> None:
        book = self.book("fresh")
        page_id = "0583.source-stale"
        submission = b"Substantive submission for the freshness case. It names verification in prose only.\n"
        note = b"NOTE one\n"
        manifest = pretty({"files": [{"bytes": len(note), "path": "note.md", "sha256": sha(note)}], "schema": "example-manifest/1"})
        write(book / "evidence" / "submission.md", submission)
        write(book / "evidence" / "artifact-manifest.json", manifest)
        write(book / "note.md", note)
        pointer = (
            f"Submission: evidence/submission.md sha256 {sha(submission)}, {len(submission)} bytes.\n"
            f"Artifact manifest: evidence/artifact-manifest.json sha256 {sha(manifest)}, {len(manifest)} bytes.\n"
        )
        write(book / page_id / "05.03.md", page(pointer))
        proc, prepared = call(book, "prepare", source=page_id, pass_="05.03")
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:500])
        write(book / "judgment.json", pretty(judgment()))
        proc, recorded = call(book, "record", source=page_id, pass_="05.03", intake=prepared["intake_id"], judgment=str(book / "judgment.json"))
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:700] + proc.stdout.decode()[:400])
        review = recorded["review_id"]
        proc, published = call(book, "publish", source=page_id, pass_="05.03", review=review)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:700] + proc.stdout.decode()[:400])
        proc, read = call(book, "read", source=page_id, pass_="05.03")
        self.assertEqual(proc.returncode, 0)
        self.assertIs(read["stale"], False)
        write(book / "note.md", b"NOTE changed\n")
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
        self.assertEqual(inspected["next_action"], judgment()["next_action"])

        tamper = self.book("tamper")
        tamper_page = "0788.synth-local"
        write(tamper / tamper_page / "05.04.md", page("PENDING.\n"))
        write(tamper / tamper_page / "05.04.return.md", b"Did.\nLocal return.\n")
        proc, prepared = call(tamper, "prepare", source=tamper_page, pass_="05.04")
        write(tamper / "local.json", pretty(judgment()))
        proc, recorded = call(tamper, "record", source=tamper_page, pass_="05.04", intake=prepared["intake_id"], judgment=str(tamper / "local.json"))
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:500])
        review = recorded["review_id"]
        proc, published = call(tamper, "publish", source=tamper_page, pass_="05.04", review=review)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:500])
        target = tamper / tamper_page / "06.04.review.md"
        target_before = target.read_bytes()
        rendered = tamper / "workbook-review" / tamper_page / "05.04" / "reviews" / review / "rendered.md"
        rendered.write_bytes(rendered.read_bytes() + b"\nUNRECORDED ALTERATION\n")
        proc, blocked = call(tamper, "publish", source=tamper_page, pass_="05.04", review=review)
        self.assertEqual(proc.returncode, 1, proc.stdout.decode()[:500])
        self.assertFalse(blocked["published"])
        self.assertEqual(target.read_bytes(), target_before)

        pending = self.book("pending")
        pending_page = "0787.synth-local"
        write(pending / pending_page / "05.07.md", page("PENDING.\n"))
        write(pending / pending_page / "05.07.return.md", b"Did.\nInterrupt return.\n")
        proc, prepared = call(pending, "prepare", source=pending_page, pass_="05.07")
        write(pending / "j.json", pretty(judgment()))
        proc, recorded = call(pending, "record", source=pending_page, pass_="05.07", intake=prepared["intake_id"], judgment=str(pending / "j.json"))
        self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:400])
        review_file = pending / pending_page / "06.07.review.md"
        review_file.parent.mkdir(parents=True, exist_ok=True)
        review_file.write_bytes(b"PENDING.\n")
        os.chmod(review_file, stat.S_IREAD)
        proc, interrupted = call(pending, "publish", source=pending_page, pass_="05.07", review=recorded["review_id"])
        os.chmod(review_file, stat.S_IWRITE | stat.S_IREAD)
        self.assertEqual(proc.returncode, 1, proc.stdout.decode()[:500] + proc.stderr.decode()[:300])
        self.assertFalse(interrupted["published"])
        journal = json.loads((pending / "workbook-review" / pending_page / "05.07" / "journal.json").read_text(encoding="utf-8"))
        self.assertEqual(journal["publication"]["status"], "pointer-pending")
        proc, recovered = call(pending, "recover", source=pending_page, pass_="05.07")
        self.assertEqual(recovered["target_state"], "pointer-pending")
        self.assertEqual(recovered["judgment"]["next_action"], judgment()["next_action"])

    def test_filed_sources_stay_scoped(self) -> None:
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
            proc, recorded = call(
                book, "record", source=page_id, pass_=pass_id,
                intake=prepared["intake_id"], judgment=str(book / f"{pass_id}.json"),
            )
            self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:1200])
            self.assertEqual(recorded["mode"], "cycle-committed", recorded.get("cycle"))
            self.assertNotIn("-wb", recorded["cycle"].get("cycle_review_id", ""))
            self.assertTrue(recorded["cycle"]["cycle_review_id"].endswith(recorded["review_id"]))
            proc, published = call(book, "publish", source=page_id, pass_=pass_id, review=recorded["review_id"])
            self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
            self.assertTrue(published["published"])
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
        self.assertFalse(followed["closes_work"])
        proc, published = call(book, "publish", source="0596.synth-filed", pass_=first_pass, review=followed["review_id"])
        self.assertEqual(proc.returncode, 1, proc.stdout.decode()[:800] + proc.stderr.decode()[:400])
        self.assertFalse(published["published"])
        self.assertEqual((book / "0596.synth-filed" / f"{first_pass}.md").read_bytes(), first_bytes)
        proc, recovered = call(book, "recover", source="0595.synth-filed", pass_=second_pass)
        self.assertEqual(proc.returncode, 0, proc.stdout.decode()[:600])
        self.assertEqual(recovered["judgment"]["finding"], "The disposable note is present.")
        self.assertFalse(recovered["closes_work"])


if __name__ == "__main__":
    unittest.main()
