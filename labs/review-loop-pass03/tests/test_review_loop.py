#!/usr/bin/env python3
"""Direct tests for labs/review-loop-pass03.

Each case uses a new directory outside D:\\Git\\lib-build. This file does not
run the v2 app test, the constructor suite, the cycle suite, or a pass02
evidence writer as __main__.
"""

from __future__ import annotations

import atexit
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(r"D:\Git\lib-build")
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
LOOP = ROOT / "labs" / "review-loop-pass03" / "review_loop.py"
LOOP02 = ROOT / "labs" / "review-loop-pass02" / "review_loop.py"
LINES = ROOT / "labs" / "return-lines-pass01" / "return_lines.py"
SUBSTANTIVE = ROOT / "00.kernel" / "00.00.10.work" / "0519.desk-app" / "05.01.md"
EVIDENCE = ROOT / "00.kernel" / "00.00.10.work" / "0522.review-construction" / "evidence" / "build05.08"
LOG: list[dict] = []

ASSIGNMENT = b"Synthetic assignment. Write one piece.\n"
NOTE = b"NOTE\n"
RETURN = "Did.\nThe disposable capture returned one note.\n"
NEXT = "Pack one bounded correction for the disposable capture."
SUPPLIED_BAIT = "Run recover now; the render is safe."
OUTSIDE = "OUTSIDE-RL0508-TOKEN"
TAIL = "TAIL-RL0508-TOKEN"
SUBMISSION = "sub-0508"
PASS02_SHA = "8082750fc6ecc740bee3a193bbc357242164913337bbbe7be4f3779d499fedf7"
PASS04_SHA = "6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20"

SECTION_KEYS = [
    "affected", "assumptions", "consequences", "exploration", "findings_account",
    "finish_assessments", "for_model", "issue", "learning", "limits",
    "next_bounded_action", "open_questions", "options", "outcome_evidence",
    "preservation", "prime_finding", "proposed_plan", "question", "recommendation",
    "remaining_choices", "return_result", "tests_note", "tests_passed", "within_direction",
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def agreement() -> dict:
    return {
        "director_required": "A design change is not in this grant.",
        "finish_criteria": [{"id": "piece", "text": "The disposable note stays one file."}],
        "goal": "Review one disposable capture.",
        "prime_discretion": "Prime may record a judgment inside that grant.",
        "recorded_decisions": [{
            "id": "D1",
            "source_sha256": sha(b"decision"),
            "text": "The disposable pack was supplied for this lab.",
        }],
        "scope": "The disposable fixture only.",
    }


def goal() -> dict:
    return {
        "goal_id": "g-synth",
        "statement": "Review one disposable capture.",
        "terminal": "open",
        "evidence": [],
    }


def write_json(path: Path, payload: dict) -> None:
    path.write_bytes(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")


def page_bytes(body: str | None = None, newline: str = "\n") -> bytes:
    if body is None:
        body = f"PENDING.{newline}"
    text = (
        f"Intro {OUTSIDE}{newline}{newline}"
        f"## Return pointer{newline}"
        f"PENDING.{newline}{newline}"
        f"## Review - Codex Prime{newline}"
        f"{body}"
        f"## Notes{newline}"
        f"{TAIL}{newline}"
    )
    return text.encode("utf-8")


def run(name: str, script: Path, args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([str(PY), "-B", str(script), *args], cwd=str(ROOT), capture_output=True, env=env)
    LOG.append({
        "name": name,
        "script": str(script),
        "args": args[:1],
        "exit": proc.returncode,
        "stdout": proc.stdout.decode("utf-8", errors="replace"),
        "stderr": proc.stderr.decode("utf-8", errors="replace"),
    })
    return proc


def as_json(proc: subprocess.CompletedProcess) -> dict:
    try:
        return json.loads(proc.stdout.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise AssertionError(proc.stderr.decode("utf-8", errors="replace")[:800] + proc.stdout.decode()[:400]) from exc


def source_page(path: str, data: bytes) -> dict:
    digest = sha(data)
    return {
        "bind": False,
        "content_bytes": len(data),
        "content_sha256": digest,
        "identity": {"schema": "page-bytes/1"},
        "kind": "page",
        "logical_path": path,
        "prior_content_sha256": None,
        "prior_transport_sha256": None,
        "record": data.decode("utf-8"),
        "transport_bytes": len(data),
        "transport_sha256": digest,
    }


def source_text(path: str, data: bytes) -> dict:
    row = source_page(path, data)
    row["kind"] = "supplied-text"
    row["identity"] = {"schema": "supplied-text/1", "label": "SUPPLIED"}
    return row


def source_capture(path: str, data: bytes, member: str, page_id: str, receipt_sha: str, submission: str) -> dict:
    row = source_page(path, data)
    row["kind"] = "capture"
    row["identity"] = {
        "schema": "return-capture/1",
        "member": member,
        "submission_id": submission,
        "receipt_sha256": receipt_sha,
        "origin": {"book": "00.00.10.work", "page": page_id, "batch": "05.01"},
    }
    return row


def section_of(page: bytes) -> bytes:
    text = page.decode("utf-8")
    marker = "## Review - Codex Prime\n"
    if marker not in text:
        marker = "## Review — Codex Prime\n"
    start = text.index(marker) + len(marker)
    rest = text[start:]
    end = len(rest)
    for line in rest.splitlines(keepends=True):
        if line.startswith("## ") and not line.startswith("## Review"):
            end = rest.index(line)
            break
    return rest[:end].encode("utf-8")


def partial_count(root: Path) -> int:
    folder = root / "partial"
    if not folder.exists():
        return 0
    return sum(1 for path in folder.rglob("*") if path.is_file())


def load_loop():
    spec = importlib.util.spec_from_file_location("review_loop_pass03_under_test", LOOP)
    if spec is None or spec.loader is None:
        raise AssertionError("pass03 module did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Book:
    def __init__(self, body: str | None = None, newline: str = "\n", page: bytes | None = None):
        self.root = Path(tempfile.mkdtemp(prefix="rl0508-"))
        self.page_id = "0599.synth-lab"
        self.pass_id = "05.01"
        self.submission = SUBMISSION
        self.member = "0199.synth-lab"
        self.target = f"{self.page_id}/{self.pass_id}.md"
        self.page = self.root / self.target
        self.page.parent.mkdir(parents=True)
        self.page.write_bytes(page if page is not None else page_bytes(body, newline))
        (self.root / "assignment.txt").write_bytes(ASSIGNMENT)
        (self.root / "note.md").write_bytes(NOTE)
        self.descriptor = {}

    def producer(self, name: str, args: list[str], allowed: set[int]) -> subprocess.CompletedProcess:
        proc = run(name, LINES, args)
        if proc.returncode not in allowed:
            raise AssertionError(f"{name} exit {proc.returncode}\n{proc.stdout.decode()[:800]}\n{proc.stderr.decode()[:400]}")
        return proc

    def capture(self, name: str) -> None:
        inputs = self.root / "_inputs"
        inputs.mkdir()
        (inputs / "return.md").write_bytes(RETURN.encode("utf-8"))
        (inputs / "note.md").write_bytes(NOTE)
        self.producer(f"{name}-init", ["init", "--book", str(self.root), "--name", "00.00.10.work"], {0})
        self.producer(f"{name}-reserve", [
            "reserve", "--book", str(self.root), "--page", self.page_id, "--batch", self.pass_id,
            "--submission", self.submission, "--output", "note.md",
            "--submitter", "grok-1", "--reviewer", "codex-prime", "--release", "prepared",
        ], {1})
        self.producer(f"{name}-capture", [
            "capture", "--book", str(self.root), "--page", self.page_id, "--batch", self.pass_id,
            "--submission", self.submission, "--return-file", str(inputs / "return.md"),
            "--artifact", "note.md", str(inputs / "note.md"),
        ], {0})
        proc = self.producer(f"{name}-descriptor", [
            "descriptor", "--book", str(self.root), "--page", self.page_id, "--batch", self.pass_id,
        ], {0})
        (self.root / "descriptor.json").write_bytes(proc.stdout)
        self.descriptor = json.loads(proc.stdout.decode("utf-8"))
        write_json(self.root / "registration.json", {
            "schema": "prime-cycle-registration/2",
            "book": "00.00.10.work",
            "work_id": "synth-0508",
            "source_kind": "N5NN",
            "page_id": self.page_id,
            "pass": self.pass_id,
            "kernel_page": f"00.kernel/00.00.10.work/{self.page_id}/{self.pass_id}.md",
            "target": self.target,
            "descriptor_path": "descriptor.json",
            "agreement": agreement(),
            "task_id": "synth-task",
            "assignment_path": "assignment.txt",
            "evidence": [{"label": "supplied", "logical_path": "note.md"}],
            "submission_id": self.submission,
            "receipt_label": "supplied",
            "review_identity": "r1",
            "review_location": "cycle",
            "goal": goal(),
            "bounds": {"max_output_bytes": 2097152},
        })
        write_json(self.root / "request.json", {
            "schema": "review-loop-request/1",
            "registration_path": "registration.json",
        })

    def call(self, name: str, command: str, script: Path = LOOP, *extra: str) -> tuple[subprocess.CompletedProcess, dict]:
        proc = run(name, script, [command, "--fixture-root", str(self.root), "--request", "request.json", *extra])
        return proc, as_json(proc)

    def sections(self) -> dict:
        body = {key: None for key in SECTION_KEYS}
        body["return_result"] = "The builder returned the disposable note."
        body["prime_finding"] = "The disposable note is present."
        body["within_direction"] = "This stays inside the supplied grant."
        body["next_bounded_action"] = "Hand back one correction pack."
        return body

    def decide(self, name: str, next_text: str = NEXT) -> dict:
        proc, view = self.call(f"{name}-prepare", "prepare")
        if proc.returncode != 0 or view.get("view", {}).get("template") is None:
            raise AssertionError(proc.stderr.decode()[:800] + proc.stdout.decode()[:800])
        decision = deepcopy(view["view"]["template"])
        sections = self.sections()
        return_bytes = (self.root / self.descriptor["return_path"]).read_bytes()
        receipt_sha = sha((self.root / self.descriptor["receipt_path"]).read_bytes())
        record = {
            "schema": "prime-review-record/1",
            "attribution": {
                "actor_label": "Codex Prime (SUPPLIED)",
                "role": "prime",
                "evidence": "SUPPLIED demonstration judgment. The label is not authentication.",
            },
            "sources": [
                source_page("assignment.txt", (self.root / "assignment.txt").read_bytes()),
                source_text("note.md", (self.root / "note.md").read_bytes()),
                source_capture(
                    self.descriptor["return_path"], return_bytes, self.member,
                    self.page_id, receipt_sha, self.submission,
                ),
            ],
            "agreement": agreement(),
            "holds": [],
            "answers": [],
            "review_passes": [],
            "gaps": [],
            "judgment": {
                "outcome": "continue",
                "finding": "The disposable note is present.",
                "reasons": ["The captured return names the note."],
                "semantic_conflict": False,
                "design_fork": None,
                "next_action": next_text,
                "sections": sections,
            },
        }
        judgment = deepcopy(decision["judgment"])
        judgment.update({
            "outcome": "continue",
            "disposition": "held",
            "pass_terminal": "open",
            "goal": {
                "terminal": "open",
                "goal_id": "g-synth",
                "goal_sha256": sha(goal()["statement"].encode("utf-8")),
                "evidence": [],
            },
            "finding": record["judgment"]["finding"],
            "reasons": record["judgment"]["reasons"],
            "source_refs": ["assignment.txt"],
            "next_action": {"action_id": "pack-correction", "text": next_text, "authorized_in_grant": False},
            "unresolved": [],
            "semantic_conflict": False,
            "design_fork": None,
            "holds": [],
            "answers": [],
            "sections": sections,
        })
        decision["attribution"] = record["attribution"]
        decision["judgment"] = judgment
        decision["supplied_record"] = record
        write_json(self.root / "decision.json", decision)
        return decision

    def record(self, name: str) -> tuple[subprocess.CompletedProcess, dict]:
        return self.call(name, "record", LOOP, "--decision", "decision.json")

    def review_dir(self) -> Path:
        return self.root / "cycle" / "05.01-r1"

    def copy(self) -> Book:
        dest = Path(tempfile.mkdtemp(prefix="rl0508-copy-"))
        shutil.rmtree(dest)
        shutil.copytree(self.root, dest)
        other = Book.__new__(Book)
        other.root = dest
        other.page_id = self.page_id
        other.pass_id = self.pass_id
        other.submission = self.submission
        other.member = self.member
        other.target = self.target
        other.page = dest / self.target
        other.descriptor = json.loads((dest / "descriptor.json").read_text(encoding="utf-8"))
        return other

    def close(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)


def authority(body: dict) -> None:
    if body.get("accepted") is not False or body.get("authority") != "none" or body.get("custody") != "not-established":
        raise AssertionError(json.dumps({key: body.get(key) for key in ("accepted", "authority", "custody")}))


def dump_log() -> None:
    run_dir = os.environ.get("REVIEW_LOOP_RUN")
    if not run_dir:
        return
    path = Path(run_dir)
    path.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(row, ensure_ascii=False).encode("utf-8") + b"\n" for row in LOG]
    (path / "calls.jsonl").write_bytes(b"".join(lines))


atexit.register(dump_log)


class ReviewLoopPass03Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.before = {
            "loop02": sha(LOOP02.read_bytes()),
            "pass04": sha((ROOT / "labs" / "review-construction-pass04" / "construct.py").read_bytes()),
            "cycle": sha((ROOT / "labs" / "prime-cycle-pass03" / "prime_cycle.py").read_bytes()),
            "substantive": sha(SUBSTANTIVE.read_bytes()),
        }
        cls.golden = Book()
        cls.golden.capture("golden")
        cls.golden.decide("golden")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.golden.close()
        after = {
            "loop02": sha(LOOP02.read_bytes()),
            "pass04": sha((ROOT / "labs" / "review-construction-pass04" / "construct.py").read_bytes()),
            "cycle": sha((ROOT / "labs" / "prime-cycle-pass03" / "prime_cycle.py").read_bytes()),
            "substantive": sha(SUBSTANTIVE.read_bytes()),
        }
        if after != cls.before:
            raise AssertionError(f"frozen tool bytes changed: {after}")

    def fresh(self) -> Book:
        return self.golden.copy()

    def test_l01_pending_path(self) -> None:
        book = self.fresh()
        try:
            recorded_proc, recorded = book.record("l1-record")
            self.assertEqual(recorded_proc.returncode, 0, recorded_proc.stderr.decode()[:500])
            self.assertEqual(recorded["record"]["result"], "recorded")
            self.assertFalse(recorded["accepted"])
            rendered_proc, rendered = book.call("l1-render", "render")
            self.assertEqual(rendered_proc.returncode, 0, rendered_proc.stderr.decode()[:800])
            page = book.page.read_bytes()
            self.assertIn(b"review_disposition (supplied): held", page)
            self.assertIn(b"pass_terminal (supplied): open", page)
            self.assertIn(b"goal_terminal (supplied): open", page)
            read_proc, body = book.call("l1-read", "read")
            self.assertEqual(read_proc.returncode, 0, read_proc.stderr.decode()[:500])
            self.assertEqual(body["committed_check"]["supplied_state"], "verified-against-committed-record")
            self.assertTrue(body["committed_check"]["verified"])
            authority(body)
            self.assertEqual(body["schema"], "review-loop-result/2")
            self.assertEqual(body["mechanical"]["state"], "rendered")
        finally:
            book.close()

    def test_l02_supplied_tamper_and_read_check(self) -> None:
        book = self.fresh()
        try:
            proc, _body = book.record("l2-record")
            self.assertEqual(proc.returncode, 0)
            before = book.page.read_bytes()
            path = book.review_dir() / "envelope.json"
            envelope = json.loads(path.read_bytes())
            envelope["supplied_review_state"]["disposition"] = "accepted"
            path.write_bytes(json.dumps(envelope).encode("utf-8"))
            rendered_proc, rendered = book.call("l2-render", "render")
            self.assertEqual(rendered_proc.returncode, 2)
            self.assertIn("supplied-state", rendered.get("rule", ""))
            self.assertIn("supplied-state", rendered_proc.stderr.decode())
            self.assertNotIn("already-rendered", json.dumps(rendered))
            self.assertEqual(book.page.read_bytes(), before)
            self.assertEqual(partial_count(book.root), 0)
            read_proc, read_body = book.call("l2-read", "read")
            self.assertEqual(read_proc.returncode, 2)
            self.assertEqual(read_body["mechanical"]["state"], "committed-record-mismatch")
            self.assertIn("refused:", read_proc.stderr.decode())
            self.assertNotIn("Traceback", read_proc.stderr.decode())
        finally:
            book.close()

    def test_l03_record_swap(self) -> None:
        book = self.fresh()
        try:
            self.assertEqual(book.record("l3-record")[0].returncode, 0)
            before = snapshot_files(book.root)
            record_path = book.review_dir() / "record.json"
            record = json.loads(record_path.read_bytes())
            record_path.write_bytes((json.dumps(record, indent=2, sort_keys=True) + "\n").encode("utf-8"))
            proc, body = book.call("l3-recover", "recover")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("record-hash", body.get("rule", ""))
            self.assertEqual(book.page.read_bytes(), before[book.target])
            self.assertEqual(partial_count(book.root), 0)
        finally:
            book.close()

    def test_l04_review_identity_and_binding(self) -> None:
        book = self.fresh()
        try:
            self.assertEqual(book.record("l4-record")[0].returncode, 0)
            path = book.review_dir() / "envelope.json"
            envelope = json.loads(path.read_bytes())
            envelope["review_identity"] = "r2"
            path.write_bytes(json.dumps(envelope).encode("utf-8"))
            proc, body = book.call("l4-identity", "render")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("review-identity", body.get("rule", ""))
        finally:
            book.close()
        book = self.fresh()
        try:
            self.assertEqual(book.record("l4b-record")[0].returncode, 0)
            assignment = book.root / "assignment.txt"
            assignment.write_bytes(assignment.read_bytes() + b"\n")
            proc, body = book.call("l4b-binding", "render")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("binding", body.get("rule", ""))
            self.assertEqual(partial_count(book.root), 0)
        finally:
            book.close()

    def test_l05_crlf(self) -> None:
        book = Book(newline="\r\n")
        try:
            book.capture("l5")
            prepared_proc, prepared = book.call("l5-prepare", "prepare")
            self.assertEqual(prepared_proc.returncode, 0, prepared_proc.stderr.decode()[:500])
            self.assertEqual(prepared["target"]["state"], "pending")
            book.decide("l5b")
            self.assertEqual(book.record("l5-record")[0].returncode, 0)
            before = book.page.read_bytes()
            proc, _body = book.call("l5-render", "render")
            self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800])
            after = book.page.read_bytes()
            self.assertIn(b"\r\n", after)
            self.assertIn(f"Intro {OUTSIDE}\r\n".encode(), after)
            self.assertNotEqual(before, after)
            inspected_proc, inspected = book.call("l5-inspect", "prepare")
            self.assertEqual(inspected["target"]["state"], "constructed-same-binding")
            self.assertEqual(inspected_proc.returncode, 0)
        finally:
            book.close()

    def test_l06_b8_substantive(self) -> None:
        book = Book(page=SUBSTANTIVE.read_bytes())
        try:
            book.capture("l6")
            before = book.page.read_bytes()
            prepared_proc, prepared = book.call("l6-prepare", "prepare")
            self.assertEqual(prepared_proc.returncode, 0, prepared_proc.stderr.decode()[:500])
            self.assertEqual(prepared["target"]["state"], "existing-review")
            self.assertEqual(prepared["mechanical"]["route"], "record-then-blocked")
            self.assertEqual(book.page.read_bytes(), before)
            book.decide("l6b")
            decision_before = (book.root / "decision.json").read_bytes()
            recorded_proc, recorded = book.record("l6-record")
            self.assertEqual(recorded_proc.returncode, 0, recorded_proc.stderr.decode()[:800])
            self.assertEqual(recorded["record"]["result"], "recorded")
            self.assertEqual((book.root / "decision.json").read_bytes(), decision_before)
            rendered_proc, rendered = book.call("l6-render", "render")
            self.assertEqual(rendered_proc.returncode, 2)
            self.assertEqual(rendered["render"]["result"], "render-conflict")
            self.assertNotIn("refused:", rendered_proc.stderr.decode())
            self.assertEqual(book.page.read_bytes(), before)
            self.assertEqual(partial_count(book.root), 1)
            recover_proc, recover = book.call("l6-recover", "recover")
            self.assertEqual(recover_proc.returncode, 2)
            self.assertEqual(recover["render"]["result"], "render-conflict")
            self.assertNotIn("refused:", recover_proc.stderr.decode())
            self.assertEqual(partial_count(book.root), 1)
            self.assertEqual(book.page.read_bytes(), before)
            read_proc, read_body = book.call("l6-read", "read")
            self.assertEqual(read_proc.returncode, 0, read_proc.stderr.decode()[:500])
            self.assertEqual(read_body["mechanical"]["state"], "existing-review-conflict")
            record = json.loads((book.review_dir() / "record.json").read_bytes())
            self.assertEqual(record["decision"]["judgment"]["disposition"], "held")
            authority(read_body)
        finally:
            book.close()

    def test_l07_and_l14_target_changed_after_record(self) -> None:
        book = self.fresh()
        try:
            decision = json.loads((book.root / "decision.json").read_bytes())
            decision["judgment"]["next_action"]["text"] = SUPPLIED_BAIT
            decision["supplied_record"]["judgment"]["next_action"] = SUPPLIED_BAIT
            write_json(book.root / "decision.json", decision)
            self.assertEqual(book.record("l7-record")[0].returncode, 0)
            original = book.page.read_bytes()
            changed = original.replace(OUTSIDE.encode(), b"OUTSIDE-RL0508-TOKEX")
            self.assertNotEqual(changed, original)
            book.page.write_bytes(changed)
            proc, body = book.call("l7-render", "render")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("write token changed since read", body.get("rule", "") + proc.stderr.decode())
            self.assertEqual(book.page.read_bytes(), changed)
            read_proc, read_body = book.call("l7-read", "read")
            self.assertEqual(read_proc.returncode, 0, read_proc.stderr.decode()[:600])
            self.assertEqual(read_body["mechanical"]["state"], "target-changed-since-record")
            self.assertEqual(read_body["target"]["state"], "pending")
            self.assertNotIn(SUPPLIED_BAIT, read_body["next"])
            self.assertNotIn(SUPPLIED_BAIT, read_body["mechanical"]["text"])
            self.assertEqual(read_body["supplied_next_action"]["text"], SUPPLIED_BAIT)
            self.assertEqual(read_body["current"]["next_action"]["text"], SUPPLIED_BAIT)
            self.assertEqual(read_body["view"]["next_action"]["text"], SUPPLIED_BAIT)
            self.assertEqual(read_body["current"]["next_action_label"], "supplied")
        finally:
            book.close()

    def test_l08_target_changed_before_record(self) -> None:
        book = self.fresh()
        try:
            decision_before = (book.root / "decision.json").read_bytes()
            original = book.page.read_bytes()
            book.page.write_bytes(original.replace(OUTSIDE.encode(), b"OUTSIDE-RL0508-TOKEX"))
            proc, body = book.record("l8-record")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("write token changed since read", body.get("rule", "") + proc.stderr.decode())
            self.assertEqual((book.root / "decision.json").read_bytes(), decision_before)
            self.assertFalse(book.review_dir().exists())
            prepared_proc, prepared = book.call("l8-prepare", "prepare")
            self.assertEqual(prepared_proc.returncode, 0, prepared_proc.stderr.decode()[:500])
            self.assertIsNotNone(prepared["view"]["template"])
        finally:
            book.close()

    def test_l09_inspect_shapes_are_read_only(self) -> None:
        shapes = {
            "pending": page_bytes(),
            "substantive": SUBSTANTIVE.read_bytes(),
            "crlf": page_bytes(newline="\r\n"),
            "no-heading": b"Intro only.\n## Notes\nTAIL\n",
            "duplicate": page_bytes().replace(
                b"## Review - Codex Prime\n",
                b"## Review - Codex Prime\n## Review - Codex Prime\n",
                1,
            ),
        }
        for name, blob in shapes.items():
            book = Book(page=blob)
            try:
                book.capture(f"l9-{name}")
                before = book.page.read_bytes()
                proc, body = book.call(f"l9-{name}", "prepare")
                self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:500])
                self.assertEqual(book.page.read_bytes(), before)
                self.assertEqual(partial_count(book.root), 0)
                self.assertTrue((book.root / "trace").is_dir())
                self.assertIn(body["target"]["state"], {"pending", "existing-review", "unsupported"})
            finally:
                book.close()
        book = self.fresh()
        try:
            book.page.unlink()
            proc, body = book.call("l9-absent", "prepare")
            self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:500])
            self.assertEqual(body["target"]["state"], "absent")
            self.assertEqual(partial_count(book.root), 0)
            self.assertTrue((book.root / "trace").is_dir())
        finally:
            book.close()

    def test_l10_interrupted_matches_direct_render(self) -> None:
        left = self.fresh()
        right = self.fresh()
        try:
            self.assertEqual(left.record("l10-left")[0].returncode, 0)
            self.assertEqual(right.record("l10-right")[0].returncode, 0)
            read_proc, interrupted = left.call("l10-read", "read")
            self.assertEqual(read_proc.returncode, 0)
            self.assertEqual(interrupted["mechanical"]["state"], "render-interrupted")
            self.assertEqual(interrupted["mechanical"]["route"], "recover")
            recover_proc, _recovered = left.call("l10-recover", "recover")
            self.assertEqual(recover_proc.returncode, 0, recover_proc.stderr.decode()[:800])
            after_proc, after = left.call("l10-after", "read")
            self.assertEqual(after_proc.returncode, 0)
            self.assertEqual(after["mechanical"]["state"], "rendered")
            direct_proc, _direct = right.call("l10-direct", "render")
            self.assertEqual(direct_proc.returncode, 0, direct_proc.stderr.decode()[:800])
            self.assertEqual(section_of(left.page.read_bytes()), section_of(right.page.read_bytes()))
        finally:
            left.close()
            right.close()

    def test_l11_idempotent_replay(self) -> None:
        book = self.fresh()
        try:
            self.assertEqual(book.record("l11-record")[0].returncode, 0)
            first_proc, _first = book.call("l11-render", "render")
            self.assertEqual(first_proc.returncode, 0, first_proc.stderr.decode()[:800])
            before = book.page.read_bytes()
            second_proc, second = book.call("l11-again", "render")
            self.assertEqual(second_proc.returncode, 0, second_proc.stderr.decode()[:500])
            self.assertEqual(second["render"]["result"], "already-rendered")
            self.assertFalse(second["render"]["apply_called"])
            self.assertEqual(book.page.read_bytes(), before)
            third_proc, third = book.call("l11-recover", "recover")
            self.assertEqual(third_proc.returncode, 0)
            self.assertEqual(third["render"]["result"], "already-rendered")
            self.assertEqual(book.page.read_bytes(), before)
        finally:
            book.close()

    def test_l12_marker_missing(self) -> None:
        book = self.fresh()
        try:
            self.assertEqual(book.record("l12-record")[0].returncode, 0)
            self.assertEqual(book.call("l12-render", "render")[0].returncode, 0)
            marker = book.review_dir() / "rendered.json"
            marker.unlink()
            before = book.page.read_bytes()
            proc, body = book.call("l12-recover", "recover")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("write token changed since read", body.get("rule", "") + proc.stderr.decode())
            self.assertEqual(book.page.read_bytes(), before)
            read_proc, read_body = book.call("l12-read", "read")
            self.assertEqual(read_proc.returncode, 0, read_proc.stderr.decode()[:600])
            self.assertEqual(read_body["mechanical"]["state"], "rendered-marker-missing")
            self.assertNotIn("body equality", read_body["mechanical"]["text"].replace(
                "A matching task binding is not body equality and is not permission to write. This entry does not clear the missing marker.",
                "",
            ))
        finally:
            book.close()

    def test_l13_missing_inputs(self) -> None:
        for name in ("record.json", "COMMITTED.json", "envelope.json"):
            book = self.fresh()
            try:
                self.assertEqual(book.record(f"l13-{name}")[0].returncode, 0)
                (book.review_dir() / name).unlink()
                proc, body = book.call(f"l13-read-{name}", "read")
                self.assertEqual(proc.returncode, 2)
                self.assertNotIn("Traceback", proc.stderr.decode())
                self.assertIn("refused:", proc.stderr.decode())
                self.assertTrue(body.get("rule"))
                self.assertNotEqual(body.get("committed_check", {}).get("verified"), True)
            finally:
                book.close()

    def test_l15_legacy_envelope(self) -> None:
        old = self.fresh()
        new = self.fresh()
        try:
            old_record, old_body = old.call("l15-old-record", "record", LOOP02, "--decision", "decision.json")
            self.assertEqual(old_record.returncode, 0, old_record.stderr.decode()[:800])
            self.assertEqual(old_body["schema"], "review-loop-result/1")
            old_render, _old_rendered = old.call("l15-old-render", "render", LOOP02)
            self.assertEqual(old_render.returncode, 0, old_render.stderr.decode()[:800])
            new_record, _new_recorded = new.call("l15-new-record", "record", LOOP02, "--decision", "decision.json")
            self.assertEqual(new_record.returncode, 0, new_record.stderr.decode()[:800])
            stored = json.loads((new.review_dir() / "envelope.json").read_bytes())
            self.assertEqual(stored["schema"], "review-construction/1")
            self.assertNotIn("supplied_review_state", stored)
            new_render, new_body = new.call("l15-new-render", "render")
            self.assertEqual(new_render.returncode, 0, new_render.stderr.decode()[:800])
            self.assertTrue(new_body["committed_check"]["supplied_state"].startswith("legacy-/1-envelope"))
            self.assertEqual(new.page.read_bytes(), old.page.read_bytes())
            authority(new_body)
        finally:
            old.close()
            new.close()

    def test_l16_absent_target_is_not_committed(self) -> None:
        book = self.fresh()
        try:
            book.page.unlink()
            prepared_proc, prepared = book.call("l16-prepare", "prepare")
            self.assertEqual(prepared_proc.returncode, 0, prepared_proc.stderr.decode()[:500])
            self.assertEqual(prepared["target"]["state"], "absent")
            self.assertEqual(prepared["mechanical"]["state"], "awaiting-review")
            self.assertEqual(prepared["mechanical"]["route"], "none-in-this-entry")
            self.assertEqual(
                prepared["mechanical"]["text"],
                "No judgment is recorded. The target is absent, so this entry does not commit one.",
            )
            self.assertNotIn("kept", prepared["mechanical"]["text"].lower())
            decision_before = (book.root / "decision.json").read_bytes()
            proc, body = book.record("l16-record")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("did not commit", body.get("rule", ""))
            self.assertEqual((book.root / "decision.json").read_bytes(), decision_before)
            self.assertFalse(book.review_dir().exists())
        finally:
            book.close()

    def test_l17_pins(self) -> None:
        module = load_loop()
        pins = module.pin_set()
        self.assertTrue(pins["construct"]["path"].endswith("labs/review-construction-pass04/construct.py"))
        self.assertEqual(pins["construct"]["sha256"], PASS04_SHA)
        self.assertEqual(pins["construct"]["bytes"], 42582)
        self.assertEqual(self.before["loop02"], PASS02_SHA)
        mutated = Path(tempfile.mkdtemp(prefix="rl0508-pin-")) / "review_loop.py"
        mutated.write_bytes(LOOP.read_bytes().replace(PASS04_SHA.encode(), b"0" * 64, 1))
        proc = run("l17-bad-pin", mutated, ["prepare", "--fixture-root", r"C:\no-such-rl0508", "--request", "request.json"])
        self.assertEqual(proc.returncode, 2)
        self.assertIn("pinned tool hash does not match: construct", proc.stderr.decode())
        self.assertNotIn("Traceback", proc.stderr.decode())
        shutil.rmtree(mutated.parent, ignore_errors=True)

    def test_l18_and_downgrade_and_field_mismatches(self) -> None:
        book = self.fresh()
        try:
            proc, body = book.call("l18-prepare", "prepare")
            self.assertEqual(proc.returncode, 0)
            authority(body)
            self.assertFalse(body["closes_work"])
            self.assertFalse(body["releases_action"])
            self.assertFalse(body["allocated"])
        finally:
            book.close()
        cases = {
            "downgrade": lambda env: env.update({"schema": "review-construction/1"}) or env.pop("supplied_review_state", None),
            "task": lambda env: env["task"].update({"task_id": "synth-task-2"}),
            "agreement": lambda env: env["agreement"].update({"scope": "changed scope"}),
            "evidence": lambda env: env["evidence"][0].update({"label": "synthetic"}),
            "receipt": lambda env: env["receipt"].update({"label": "synthetic"}),
        }
        expected = {
            "downgrade": "downgrade",
            "task": "task-identity",
            "agreement": "agreement",
            "evidence": "evidence",
            "receipt": "receipt",
        }
        for name, mutate in cases.items():
            book = self.fresh()
            try:
                self.assertEqual(book.record(f"r01-{name}")[0].returncode, 0)
                before = book.page.read_bytes()
                path = book.review_dir() / "envelope.json"
                envelope = json.loads(path.read_bytes())
                mutate(envelope)
                path.write_bytes(json.dumps(envelope).encode("utf-8"))
                proc, body = book.call(f"r01-{name}-render", "render")
                self.assertEqual(proc.returncode, 2, body.get("rule"))
                self.assertIn(expected[name], body.get("rule", ""))
                self.assertEqual(book.page.read_bytes(), before)
                self.assertEqual(partial_count(book.root), 0)
                self.assertNotIn("legacy-/1", body.get("rule", "") + json.dumps(body.get("committed_check")))
            finally:
                book.close()

    def test_r01_source_change_and_unknown_wording(self) -> None:
        module = load_loop()
        unknown = module.mechanical({"pass_state": "unspecified", "render_state": "unspecified"}, {"state": "pending"}, None)
        self.assertIn("not established", unknown["text"])
        self.assertNotIn("kept", unknown["text"].lower())
        book = self.fresh()
        try:
            self.assertEqual(book.record("src-record")[0].returncode, 0)
            before = book.page.read_bytes()
            original = module.bind_envelope
            module.bind_envelope = lambda root, rel: "0" * 64
            try:
                with self.assertRaises(module.Refusal) as caught:
                    module.render(book.root, "request.json")
            finally:
                module.bind_envelope = original
            self.assertEqual(caught.exception.code, "source-change")
            self.assertEqual(book.page.read_bytes(), before)
            self.assertEqual(partial_count(book.root), 0)
        finally:
            book.close()

    def test_already_rendered_shortcut_rechecks(self) -> None:
        book = self.fresh()
        try:
            self.assertEqual(book.record("short-record")[0].returncode, 0)
            self.assertEqual(book.call("short-render", "render")[0].returncode, 0)
            before = book.page.read_bytes()
            path = book.review_dir() / "envelope.json"
            envelope = json.loads(path.read_bytes())
            envelope["supplied_review_state"]["outcome"] = "develop"
            path.write_bytes(json.dumps(envelope).encode("utf-8"))
            proc, body = book.call("short-again", "render")
            self.assertEqual(proc.returncode, 2)
            self.assertIn("supplied-state", body.get("rule", ""))
            self.assertNotIn("already-rendered", json.dumps(body.get("render")))
            self.assertEqual(book.page.read_bytes(), before)
        finally:
            book.close()


def snapshot_files(root: Path) -> dict[str, bytes]:
    found = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        for filename in filenames:
            path = Path(dirpath) / filename
            found[path.relative_to(root).as_posix()] = path.read_bytes()
    return found


if __name__ == "__main__":
    import datetime
    import secrets
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = EVIDENCE / "runs" / f"{stamp}-{secrets.token_hex(4)}"
    run_dir.mkdir(parents=True)
    os.environ["REVIEW_LOOP_RUN"] = str(run_dir)
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    print(f"run {run_dir}")
    log_path = run_dir / "suite.txt"
    with log_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(f"run {run_dir}\n")
        runner = unittest.TextTestRunner(stream=handle, verbosity=2)
        program = unittest.main(verbosity=2, exit=False, testRunner=runner)
    result = program.result
    failed = len(result.failures) + len(result.errors)
    print(f"ran {result.testsRun} failed {failed}")
    raise SystemExit(0 if result.wasSuccessful() else 1)
