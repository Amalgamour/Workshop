#!/usr/bin/env python3
"""Real-capture tests for the 05.04 review loop.

Disposable books stay outside D:\\Git\\lib-build. This file does not rerun
test_construct.py and does not write evidence/build05.02 or evidence/build05.03.
"""

from __future__ import annotations

import hashlib
import importlib.util
import io
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
LOOP = ROOT / "labs" / "review-loop-pass02" / "review_loop.py"
LINES = ROOT / "labs" / "return-lines-pass01" / "return_lines.py"
CYCLE02 = ROOT / "labs" / "prime-cycle-pass02" / "prime_cycle.py"
EVIDENCE = ROOT / "00.kernel" / "00.00.10.work" / "0522.review-construction" / "evidence"
LOG: list[dict] = []

ASSIGNMENT = b"Synthetic assignment. Write one piece.\n"
NOTE = b"NOTE\n"
RETURN = "Did.\nThe disposable capture returned one note.\n"
NEXT = "Pack one bounded correction for the disposable capture."
HELD_NEXT = "Wait for a reply to the disposable question."
HELD_QUESTION = "Should the disposable note stay one file?"
DISSENT = "Dissent: the minority keeps the older wording — do not smooth it."
REPLY = "Director reply: keep the disposable note as one file."
QUESTION = "Should the older wording stay on the record?"
OUTSIDE = "OUTSIDE-Δ-TOKEN"
TAIL = "TAIL-Δ-TOKEN"
SUBMISSION = "sub-0504"

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


def sections() -> dict:
    return {key: None for key in SECTION_KEYS}


def write_json(path: Path, payload: dict) -> None:
    path.write_bytes(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")


def page_bytes(body: str = "PENDING.\n") -> bytes:
    text = (
        f"Intro {OUTSIDE}\n\n"
        "## Return pointer\n"
        "PENDING.\n\n"
        "## Review - Codex Prime\n"
        f"{body}"
        "## Notes\n"
        f"{TAIL}\n"
    )
    return text.encode("utf-8")


def run(name: str, script: Path, args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([str(PY), "-B", str(script), *args], cwd=str(ROOT), capture_output=True, env=env)
    LOG.append({
        "name": name,
        "script": script.name,
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


def seal(folder: Path, page: str, batch: str, submission: str, ret: bytes, payloads: list[bytes]) -> None:
    folder.mkdir(parents=True)
    number, slug = folder.name.split(".", 1)
    reservation = {
        "destination": {"member": number, "name": slug, "path": folder.name},
        "expected_outputs": [f"note-{index}.md" for index in range(1, len(payloads) + 1)],
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
    raw_res = (json.dumps(reservation, indent=2, sort_keys=True) + "\n").encode("utf-8")
    (folder / "reservation.json").write_bytes(raw_res)
    (folder / "01.md").write_bytes(b"index\n")
    (folder / "return.md").write_bytes(ret)
    if payloads:
        (folder / "payload").mkdir()
        for index, blob in enumerate(payloads, start=1):
            (folder / "payload" / f"{index:04d}.blob").write_bytes(blob)
    sources = [
        {"bytes": len(blob), "logical": f"note-{index}.md", "payload": f"{index:04d}.blob", "sha256": sha(blob)}
        for index, blob in enumerate(payloads, start=1)
    ]
    manifest = {
        "captured_at": "2026-10-31T00:00:00.000000Z",
        "kind": "manifest",
        "omitted": [],
        "required": [source["logical"] for source in sources],
        "reservation_sha256": sha(raw_res),
        "retrospective": False,
        "return": {"bytes": len(ret), "includes_prime_review": False, "sha256": sha(ret)},
        "schema": "return-capture/1",
        "source_commit": None,
        "sources": sources,
        "submission_id": submission,
    }
    raw_man = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    (folder / "manifest.json").write_bytes(raw_man)
    (folder / "receipt.json").write_bytes((json.dumps({
        "captured_at": "2026-10-31T00:00:00.000000Z",
        "kind": "receipt",
        "manifest_sha256": sha(raw_man),
        "reservation_sha256": sha(raw_res),
        "schema": "return-capture/1",
        "submission_id": submission,
    }, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def write_audit(root: Path, book: Path, records: list[dict]) -> Path:
    files = []
    for rec in records:
        member = book / rec["old_member"]
        for dirpath, _dirnames, filenames in os.walk(member):
            for filename in filenames:
                path = Path(dirpath) / filename
                data = path.read_bytes()
                rel = path.relative_to(member).as_posix()
                files.append({"bytes": len(data), "path": f"book/{rec['old_member']}/{rel}", "sha256": sha(data)})
    body = {
        "files": files,
        "order": "ascending old member",
        "records": records,
        "rule_source": "0417.return-placement/06.01.md",
        "schema": "return-placement-audit/2",
    }
    path = root / "audit.json"
    path.write_bytes((json.dumps(body, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return path


def snapshot(root: Path) -> dict[str, str]:
    found = {}
    for dirpath, _dirnames, filenames in os.walk(root):
        for filename in filenames:
            path = Path(dirpath) / filename
            found[path.relative_to(root).as_posix()] = sha(path.read_bytes())
    return found


class Book:
    def __init__(self, page_id: str = "0599.synth-lab", kind: str = "N5NN", body: str = "PENDING.\n", submission: str = SUBMISSION):
        self.root = Path(tempfile.mkdtemp(prefix="rc0504-"))
        self.page_id = page_id
        self.kind = kind
        self.pass_id = "05.01"
        self.submission = submission
        self.return_text = RETURN
        if kind == "N5NN":
            space, nn, subject = page_id[0], page_id[2:4], page_id.split(".", 1)[1]
            self.member = f"{space}1{nn}.{subject}"
            self.target = f"{page_id}/{self.pass_id}.md"
            self.kernel = f"00.kernel/00.00.10.work/{page_id}/{self.pass_id}.md"
        else:
            self.member = None
            self.target = f"{page_id}/06.01.review.md"
            self.kernel = f"00.kernel/00.00.10.work/{page_id}/{self.pass_id}.pack.md"
        self.return_home = self.member or page_id
        self.return_rel = f"{self.return_home}/{self.pass_id}.return.md"
        self.custody_rel = f"{self.return_home}/{self.pass_id}.custody"
        self.page = self.root / self.target
        self.page.parent.mkdir(parents=True)
        self.page.write_bytes(page_bytes(body))
        (self.root / "assignment.txt").write_bytes(ASSIGNMENT)
        (self.root / "note.md").write_bytes(NOTE)

    def producer(self, name: str, args: list[str], allowed: set[int]) -> subprocess.CompletedProcess:
        proc = run(name, LINES, args)
        if proc.returncode not in allowed:
            raise AssertionError(f"{name} exit {proc.returncode}\n{proc.stdout.decode()[:800]}\n{proc.stderr.decode()[:400]}")
        return proc

    def capture(self, name: str) -> None:
        inputs = self.root / "_inputs"
        inputs.mkdir()
        (inputs / "return.md").write_bytes(self.return_text.encode("utf-8"))
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
        self.save_descriptor(name)

    def save_descriptor(self, name: str) -> None:
        proc = self.producer(f"{name}-descriptor", [
            "descriptor", "--book", str(self.root), "--page", self.page_id, "--batch", self.pass_id,
        ], {0, 1, 2})
        self.descriptor_bytes = proc.stdout
        (self.root / "descriptor.json").write_bytes(proc.stdout)
        self.descriptor = json.loads(proc.stdout.decode("utf-8"))
        self.write_registration()

    def write_registration(self) -> None:
        write_json(self.root / "registration.json", {
            "schema": "prime-cycle-registration/2",
            "book": "00.00.10.work",
            "work_id": "synth-" + self.page_id[:4],
            "source_kind": self.kind,
            "page_id": self.page_id,
            "pass": self.pass_id,
            "kernel_page": self.kernel,
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

    def call(self, name: str, command: str, *extra: str) -> tuple[subprocess.CompletedProcess, dict]:
        proc = run(name, LOOP, [command, "--fixture-root", str(self.root), "--request", "request.json", *extra])
        return proc, as_json(proc)

    def record_body(self, kind: str) -> dict:
        body = sections()
        body["return_result"] = "The builder returned the disposable note."
        body["prime_finding"] = "The disposable note is present."
        body["within_direction"] = "This stays inside the supplied grant."
        body["next_bounded_action"] = "Hand back one correction pack."
        return_bytes = (self.root / self.descriptor["return_path"]).read_bytes()
        receipt_sha = sha((self.root / self.descriptor["receipt_path"]).read_bytes())
        sources = [
            source_page("assignment.txt", (self.root / "assignment.txt").read_bytes()),
            source_text("note.md", (self.root / "note.md").read_bytes()),
        ]
        if self.kind == "N5NN":
            sources.append(source_capture(
                self.descriptor["return_path"], return_bytes, self.member, self.page_id, receipt_sha, self.submission,
            ))
        else:
            sources.append(source_text(self.descriptor["return_path"], return_bytes))
        record = {
            "schema": "prime-review-record/1",
            "attribution": {
                "actor_label": "Codex Prime (SUPPLIED)",
                "role": "prime",
                "evidence": "SUPPLIED demonstration judgment. The label is not authentication.",
            },
            "sources": sources,
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
                "next_action": NEXT,
                "sections": body,
            },
        }
        if kind == "held":
            held_sha = sha(HELD_QUESTION.encode("utf-8"))
            record["judgment"]["outcome"] = "director-input"
            record["judgment"]["finding"] = "Storage of the reply is unresolved."
            record["judgment"]["reasons"] = ["The example declares the choice instead of guessing it."]
            record["judgment"]["next_action"] = HELD_NEXT
            body["issue"] = "The reply storage shape is unresolved."
            body["consequences"] = "Choosing a shape now would freeze the other one."
            body["options"] = ["Keep the reply on the work page.", "Leave the choice for a later design."]
            body["recommendation"] = "Keep the reply on the work page until a later design says otherwise."
            body["question"] = {"id": "Q-store", "revision": "r1", "content_sha256": held_sha, "text": HELD_QUESTION}
            body["affected"] = [{"action_id": "store-reply", "dependency": "the open storage choice"}]
            record["holds"] = [{
                "hold_id": "H1",
                "finding_id": "assignment.txt#F-01",
                "kind": "director-judgment",
                "question_id": "Q-store",
                "question_revision": "r1",
                "question_sha256": held_sha,
                "dependent_scope": ["store-reply"],
            }]
        elif kind == "full":
            q_sha = sha(QUESTION.encode("utf-8"))
            body["limits"] = "Supplied demonstration. This render is not acceptance."
            body["tests_passed"] = False
            body["tests_note"] = "Optional check encoding-probe failed. The required shape check is separate."
            body["findings_account"] = [{"finding_id": "assignment.txt#F-01", "status": "accepted"}]
            record["judgment"]["semantic_conflict"] = True
            record["judgment"]["design_fork"] = {"id": "fork-1", "text": DISSENT}
            record["holds"] = [{
                "hold_id": "H1",
                "finding_id": "assignment.txt#F-fork",
                "kind": "design-fork",
                "question_id": "Q-wording",
                "question_revision": "r1",
                "question_sha256": q_sha,
                "dependent_scope": ["keep-wording"],
            }]
            record["answers"] = [{
                "answer_id": "A1",
                "question_id": "Q-wording",
                "question_revision": "r1",
                "question_sha256": q_sha,
                "reply": REPLY,
                "provenance": {
                    "actor_label": "Director (SUPPLIED)",
                    "role": "director",
                    "evidence": "SUPPLIED demonstration reply. The label is not authentication.",
                },
                "disposition": "brief-approval",
            }]
        return record

    def judgment_for(self, record: dict) -> dict:
        supplied = record["judgment"]
        disposition = "held" if supplied["outcome"] == "director-input" else "accepted"
        action = "wait-reply" if supplied["outcome"] == "director-input" else "pack-correction"
        return {
            "outcome": supplied["outcome"],
            "disposition": disposition,
            "pass_terminal": "open",
            "goal": {
                "terminal": "open",
                "goal_id": "g-synth",
                "goal_sha256": sha(goal()["statement"].encode("utf-8")),
                "evidence": [],
            },
            "finding": supplied["finding"],
            "reasons": supplied["reasons"],
            "source_refs": ["assignment.txt"],
            "next_action": {"action_id": action, "text": supplied["next_action"], "authorized_in_grant": False},
            "unresolved": [],
            "semantic_conflict": supplied["semantic_conflict"],
            "design_fork": supplied["design_fork"],
            "holds": record["holds"],
            "answers": record["answers"],
            "sections": supplied["sections"],
        }

    def decide(self, name: str, kind: str = "clean") -> dict:
        proc, view = self.call(f"{name}-prepare", "prepare")
        if proc.returncode != 0 or view.get("view", {}).get("template") is None:
            raise AssertionError(proc.stderr.decode()[:600] + proc.stdout.decode()[:600])
        decision = deepcopy(view["view"]["template"])
        record = self.record_body(kind)
        decision["attribution"] = record["attribution"]
        decision["judgment"] = self.judgment_for(record)
        decision["supplied_record"] = record
        write_json(self.root / "decision.json", decision)
        self.prepared = view
        return decision

    def copy(self) -> Path:
        dest = Path(tempfile.mkdtemp(prefix="rc0504-copy-"))
        shutil.rmtree(dest)
        return Path(shutil.copytree(self.root, dest))

    def close(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)


def reproduce_decision() -> dict:
    body = sections()
    body["return_result"] = "The builder returned the disposable note."
    body["prime_finding"] = "The disposable note is present."
    body["within_direction"] = "This stays inside the supplied grant."
    body["next_bounded_action"] = "Hand back one correction pack."
    record_judgment = {
        "outcome": "continue",
        "finding": "The disposable note is present.",
        "reasons": ["The captured return names the note."],
        "semantic_conflict": False,
        "design_fork": None,
        "next_action": NEXT,
        "sections": body,
    }
    judgment = {
        "outcome": "continue",
        "disposition": "accepted",
        "pass_terminal": "open",
        "goal": {
            "terminal": "open",
            "goal_id": "g-synth",
            "goal_sha256": sha(goal()["statement"].encode("utf-8")),
            "evidence": [],
        },
        "finding": record_judgment["finding"],
        "reasons": record_judgment["reasons"],
        "source_refs": ["assignment.txt"],
        "next_action": {"action_id": "pack-correction", "text": NEXT, "authorized_in_grant": False},
        "unresolved": [],
        "semantic_conflict": False,
        "design_fork": None,
        "holds": [],
        "answers": [],
        "sections": body,
    }
    return {
        "schema": "review-loop-reproduce-decision/1",
        "task_id": "repro-task",
        "return_text": RETURN,
        "note_text": NOTE.decode("utf-8"),
        "assignment_text": ASSIGNMENT.decode("utf-8"),
        "agreement": agreement(),
        "goal": goal(),
        "attribution": {
            "actor_label": "Codex Prime (SUPPLIED)",
            "role": "prime",
            "evidence": "SUPPLIED demonstration judgment. The label is not authentication and this is not acceptance.",
        },
        "judgment": judgment,
        "record_judgment": record_judgment,
        "holds": [],
        "answers": [],
    }


class ReviewLoopTests(unittest.TestCase):
    def test_pins_and_sealed_evidence(self) -> None:
        pins = {
            ROOT / "labs/return-lines-pass01/return_lines.py": (
                "863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a", 100897,
            ),
            ROOT / "labs/review-construction-pass01/construct.py": (
                "8b9d4a6eda460f594404042f7ee232a7ac55fcc09af38905de364defa189ea8a", 35956,
            ),
            ROOT / "labs/review-construction-pass02/construct.py": (
                "b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc", 36188,
            ),
            ROOT / "labs/prime-cycle-pass02/prime_cycle.py": (
                "689d63d26b0dfb59363563effa50acbd69856ffcc2ee728b7f54615f16fabd50", 58448,
            ),
            ROOT / "labs/prime-review-pass02/prime_review.py": (
                "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e", 58560,
            ),
            ROOT / "labs/review-loop-pass01/review_loop.py": (
                "fac0881d1e7e991b630d1deab688a3e28745e2f7b2075c7eb5148251b8ac5595", 26028,
            ),
            EVIDENCE / "build05.03" / "transcript.json": (
                "5f1732a2dd2b346cf6de8b215f2ec2797492585eca00a94f0e8040304e3d7f98", 726570,
            ),
            EVIDENCE / "build05.03" / "sample-review.md": (
                "eb3794681c7f7162a3ffe59c65191cf7f8bb3c7d5c516f8a88ecf0d40237fef4", 4119,
            ),
            EVIDENCE / "build05.02" / "transcript.json": (
                "b8a07fe1bb6a00fc561b82297694ddd3b520bf004bf4742ca166816ee960e210", 86883,
            ),
        }
        for path, (digest, size) in pins.items():
            blob = path.read_bytes()
            self.assertEqual(len(blob), size, path.name)
            self.assertEqual(sha(blob), digest, path.name)
        self.assertFalse((ROOT / "00.kernel/00.00.10.work/return-line-layout.json").exists())

    def test_real_zero_space_capture_round_trip(self) -> None:
        book = Book()
        try:
            book.capture("zero")
            self.assertEqual((book.root / "descriptor.json").read_bytes(), book.descriptor_bytes)
            self.assertEqual(book.descriptor["schema"], "return-line-descriptor/1")
            self.assertEqual(book.descriptor["target_page"], "0199.synth-lab")
            self.assertTrue((book.root / book.descriptor["custody_path"]).is_dir())
            self.assertNotEqual(book.descriptor["target_page"], book.target)
            decision = book.decide("zero")
            self.assertFalse(book.prepared["full_success"])
            self.assertEqual(book.prepared["pass_state"], "awaiting-review")
            self.assertEqual(book.prepared["observation"]["state"], "complete")
            self.assertTrue(book.prepared["observation"]["custody_verified"])
            self.assertFalse(book.prepared["observation"]["filing_claimed"])
            self.assertEqual(book.prepared["observation"]["placement_status"], "final")
            self.assertEqual(book.prepared["observation"]["task_association"], "not-established")
            self.assertIn(
                "task association is not established by the custody records",
                book.prepared["view"]["attention"],
            )
            self.assertFalse(book.prepared["accepted"])
            binding = decision["binding"]["task_binding_sha256"]
            recorded, record_view = book.call("zero-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 0, recorded.stderr.decode()[:800])
            self.assertEqual(record_view["record"]["result"], "recorded")
            self.assertFalse(record_view["accepted"])
            rendered, render_view = book.call("zero-render", "render")
            self.assertEqual(rendered.returncode, 0, rendered.stderr.decode()[:800] + rendered.stdout.decode()[:400])
            self.assertTrue(render_view["full_success"])
            self.assertFalse(render_view["accepted"])
            text = book.page.read_text(encoding="utf-8")
            self.assertIn(OUTSIDE, text)
            self.assertIn(TAIL, text)
            self.assertIn(NEXT, text)
            self.assertIn("authority: none", text)
            self.assertIn(f"task_binding: {binding}", text)
            self.assertIn("The disposable note is present.", text)
            fresh, fresh_view = book.call("zero-read", "read")
            self.assertEqual(fresh.returncode, 0)
            self.assertEqual(fresh_view["pass_state"], "reviewed")
            self.assertEqual(fresh_view["current"]["render_state"], "rendered")
            self.assertEqual(fresh_view["current"]["next_action"]["text"], NEXT)
            self.assertEqual(fresh_view["current"]["task_binding_sha256"], binding)
            self.assertTrue(fresh_view["full_success"])
            self.assertEqual((book.root / "descriptor.json").read_bytes(), book.descriptor_bytes)
        finally:
            book.close()

    def test_nonzero_and_local_captures_render(self) -> None:
        nonzero = Book(page_id="1599.synth-lab")
        try:
            nonzero.capture("nonzero")
            self.assertEqual(nonzero.member, "1199.synth-lab")
            self.assertEqual(nonzero.descriptor["target_page"], "1199.synth-lab")
            decision = nonzero.decide("nonzero")
            self.assertEqual(decision["binding"]["member"], "1199.synth-lab")
            recorded, _view = nonzero.call("nonzero-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 0, recorded.stderr.decode()[:800])
            rendered, render_view = nonzero.call("nonzero-render", "render")
            self.assertEqual(rendered.returncode, 0, rendered.stderr.decode()[:800] + rendered.stdout.decode()[:500])
            self.assertTrue(render_view["full_success"])
            self.assertNotIn("bad member", rendered.stderr.decode())
            self.assertIn(NEXT, nonzero.page.read_text(encoding="utf-8"))
        finally:
            nonzero.close()
        local = Book(page_id="1799.synth-colab", kind="N7NN")
        try:
            local.capture("local")
            self.assertEqual(local.descriptor["target_page"], "1799.synth-colab")
            self.assertEqual(local.descriptor["route"], "page-local-colab")
            self.assertTrue(str(local.page).endswith("06.01.review.md"))
            local.decide("local")
            proc, view = local.call("local-run", "run", "--decision", "decision.json")
            self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:500])
            self.assertTrue(view["full_success"])
            self.assertFalse(view["accepted"])
            text = local.page.read_text(encoding="utf-8")
            self.assertIn(NEXT, text)
            self.assertIn(OUTSIDE, text)
            self.assertIn(TAIL, text)
            fresh, read_view = local.call("local-read", "read")
            self.assertEqual(fresh.returncode, 0)
            self.assertEqual(read_view["current"]["next_action"]["text"], NEXT)
        finally:
            local.close()

    def test_duplicate_interrupt_and_existing_section(self) -> None:
        book = Book()
        try:
            book.capture("dup")
            book.decide("dup")
            first, _first_view = book.call("dup-record", "record", "--decision", "decision.json")
            self.assertEqual(first.returncode, 0, first.stderr.decode()[:600])
            digest = sha((book.root / "cycle" / "05.01-r1" / "record.json").read_bytes())
            replay, replay_view = book.call("dup-replay", "record", "--decision", "decision.json")
            self.assertEqual(replay.returncode, 0)
            self.assertEqual(replay_view["record"]["result"], "already-recorded")
            revised = json.loads((book.root / "decision.json").read_text(encoding="utf-8"))
            revised["judgment"]["finding"] = "A different finding."
            revised["supplied_record"]["judgment"]["finding"] = "A different finding."
            write_json(book.root / "decision-conflict.json", revised)
            refused = run("dup-conflict", LOOP, [
                "record", "--fixture-root", str(book.root), "--request", "request.json", "--decision", "decision-conflict.json",
            ])
            self.assertEqual(refused.returncode, 2)
            self.assertIn("conflict: a different review is already committed", refused.stderr.decode())
            self.assertEqual(sha((book.root / "cycle" / "05.01-r1" / "record.json").read_bytes()), digest)
            rendered, _render_view = book.call("dup-render", "render")
            self.assertEqual(rendered.returncode, 0, rendered.stderr.decode()[:600])
            page_hash = sha(book.page.read_bytes())
            (book.root / "cycle" / "05.01-r1" / "rendered.json").unlink()
            interrupted = run("dup-interrupt", LOOP, ["recover", "--fixture-root", str(book.root), "--request", "request.json"])
            self.assertEqual(interrupted.returncode, 2)
            self.assertIn("write token changed since read", interrupted.stderr.decode())
            self.assertEqual(sha(book.page.read_bytes()), page_hash)
            self.assertEqual(sha((book.root / "cycle" / "05.01-r1" / "record.json").read_bytes()), digest)
        finally:
            book.close()
        conflict = Book(body="A different substantive review.\n")
        try:
            conflict.capture("section")
            conflict.decide("section")
            self.assertEqual(conflict.call("section-record", "record", "--decision", "decision.json")[0].returncode, 0)
            before = sha(conflict.page.read_bytes())
            first = run("section-recover", LOOP, ["recover", "--fixture-root", str(conflict.root), "--request", "request.json"])
            view = as_json(first)
            self.assertEqual(first.returncode, 2, first.stdout.decode()[:500])
            self.assertEqual(view["render"]["result"], "render-conflict")
            self.assertTrue(view["render"]["apply_called"])
            partials = list((conflict.root / "partial").glob("*.md"))
            self.assertEqual(len(partials), 1)
            second = run("section-again", LOOP, ["recover", "--fixture-root", str(conflict.root), "--request", "request.json"])
            again = as_json(second)
            self.assertFalse(again["render"]["apply_called"])
            self.assertEqual(list((conflict.root / "partial").glob("*.md")), partials)
            self.assertEqual(sha(conflict.page.read_bytes()), before)
        finally:
            conflict.close()

    def test_held_question_on_a_real_capture(self) -> None:
        book = Book()
        try:
            book.capture("held")
            book.decide("held", "held")
            recorded, _view = book.call("held-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 1, recorded.stderr.decode()[:600])
            rendered, render_view = book.call("held-render", "render")
            self.assertIn(rendered.returncode, {0, 1}, rendered.stderr.decode()[:600])
            self.assertFalse(render_view["full_success"])
            self.assertFalse(render_view["accepted"])
            text = book.page.read_text(encoding="utf-8")
            self.assertIn(HELD_QUESTION, text)
            self.assertIn(OUTSIDE, text)
            self.assertIn(TAIL, text)
            fresh, view = book.call("held-read", "read")
            self.assertEqual(fresh.returncode, 0)
            self.assertEqual(view["current"]["next_action"]["text"], HELD_NEXT)
            self.assertIn(HELD_QUESTION, view["current"]["questions"])
        finally:
            book.close()

    def test_changed_task_evidence_and_agreement_stay_stale(self) -> None:
        book = Book()
        try:
            book.capture("stale")
            book.decide("stale")
            self.assertEqual(book.call("stale-record", "record", "--decision", "decision.json")[0].returncode, 0)
            self.assertEqual(book.call("stale-render", "render")[0].returncode, 0)
            record_hash = sha((book.root / "cycle" / "05.01-r1" / "record.json").read_bytes())

            def changed_task(path: Path) -> None:
                (path / "assignment.txt").write_bytes(b"Synthetic assignment. Revised piece.\n")

            def changed_evidence(path: Path) -> None:
                (path / "note.md").write_bytes(b"NOTE revised\n")

            def changed_agreement(path: Path) -> None:
                reg = json.loads((path / "registration.json").read_text(encoding="utf-8"))
                reg["agreement"]["goal"] = "Review a revised disposable capture."
                write_json(path / "registration.json", reg)

            for label, change in (("task", changed_task), ("evidence", changed_evidence), ("agreement", changed_agreement)):
                copy = book.copy()
                try:
                    change(copy)
                    proc = run(f"stale-{label}", LOOP, ["read", "--fixture-root", str(copy), "--request", "request.json"])
                    view = as_json(proc)
                    reason = (view.get("observation") or {}).get("reason")
                    self.assertEqual(view["pass_state"], "review-stale", f"{label} {reason} {view.get('pass_state')}")
                    self.assertFalse(view["current"]["current"], label)
                    self.assertEqual(sha((copy / "cycle" / "05.01-r1" / "record.json").read_bytes()), record_hash, label)
                finally:
                    shutil.rmtree(copy, ignore_errors=True)
        finally:
            book.close()

    def test_negative_descriptors_do_not_claim_success(self) -> None:
        book = Book()
        try:
            book.capture("neg")
            base = book.descriptor

            def prepare_copy(name: str, change) -> dict:
                copy = book.copy()
                try:
                    change(copy)
                    proc = run(name, LOOP, ["prepare", "--fixture-root", str(copy), "--request", "request.json"])
                    view = as_json(proc)
                    self.assertFalse(view["full_success"], name)
                    self.assertFalse(view["accepted"], name)
                    return view
                finally:
                    shutil.rmtree(copy, ignore_errors=True)

            wrong = prepare_copy("neg-origin", lambda path: self._rewrite(path, lambda desc: desc["origin"].update(page="0598.other-lab") or desc))
            self.assertEqual(wrong["pass_state"], "conflict")
            self.assertIn("origin does not match the source", wrong["observation"]["reason"])
            submission = prepare_copy("neg-submission", lambda path: self._rewrite(path, lambda desc: desc.update(submission_id="other-sub")))
            self.assertEqual(submission["pass_state"], "conflict")
            self.assertIn("submission_id", submission["observation"]["reason"])
            cheat = prepare_copy("neg-receipt", self._bad_receipt)
            self.assertNotEqual(cheat["pass_state"], "complete")
            self.assertNotEqual(cheat["observation"]["state"], "complete")
            self.assertIn("pinned validator", cheat["observation"]["reason"])
            payload = prepare_copy("neg-payload", self._flip_payload)
            self.assertNotEqual(payload["observation"]["state"], "complete")
            manifest = prepare_copy("neg-manifest", self._flip_manifest)
            self.assertEqual(manifest["pass_state"], "conflict")
            custody = prepare_copy("neg-custody-file", self._custody_file)
            self.assertEqual(custody["pass_state"], "conflict")
            self.assertIn("not a directory", custody["observation"]["reason"])
            copy = book.copy()
            try:
                self._sentinel(copy)
                proc = run("neg-tool", LOOP, ["prepare", "--fixture-root", str(copy), "--request", "request.json"])
                sentinel = as_json(proc)
                self.assertEqual(sentinel["pass_state"], "conflict")
                self.assertIn("verification tool_path is not the pinned validator", sentinel["observation"]["reason"])
                self.assertFalse((copy / "scratch" / "ran.txt").exists())
                self.assertFalse(sentinel["full_success"])
            finally:
                shutil.rmtree(copy, ignore_errors=True)
            staged = prepare_copy("neg-staged", self._staged)
            self.assertEqual(staged["pass_state"], "unsupported")
            self.assertIn("staged-seal/1", staged["observation"]["reason"])
            variant = prepare_copy("neg-variant", self._bad_variant)
            self.assertEqual(variant["pass_state"], "unsupported")
            final = prepare_copy("neg-final-v2", self._final_v2)
            self.assertEqual(final["observation"]["state"], "complete", final["observation"])
            self.assertEqual(final["observation"]["placement_status"], "final")
            self.assertFalse(final["full_success"])
            self.assertEqual(base["state"], "complete")
        finally:
            book.close()
        reserved = Book(submission="sub-reserved")
        try:
            reserved.producer("reserved-init", ["init", "--book", str(reserved.root), "--name", "00.00.10.work"], {0})
            reserved.producer("reserved-reserve", [
                "reserve", "--book", str(reserved.root), "--page", reserved.page_id, "--batch", "05.01",
                "--submission", reserved.submission, "--output", "note.md",
                "--submitter", "grok-1", "--reviewer", "codex-prime", "--release", "prepared",
            ], {1})
            reserved.save_descriptor("reserved")
            self.assertEqual(reserved.descriptor["state"], "reserved")
            proc, view = reserved.call("reserved-prepare", "prepare")
            self.assertEqual(proc.returncode, 0)
            self.assertEqual(view["pass_state"], "reserved")
            self.assertIsNone(view["view"]["template"])
            self.assertFalse(view["full_success"])
            (reserved.root / reserved.custody_rel / "return.md").write_bytes(b"partial\n")
            reserved.save_descriptor("incomplete")
            self.assertEqual(reserved.descriptor["state"], "incomplete")
            _proc, incomplete = reserved.call("incomplete-prepare", "prepare")
            self.assertEqual(incomplete["pass_state"], "incomplete")
            self.assertNotEqual(incomplete["pass_state"], "reserved")
            (reserved.root / "descriptor.json").unlink()
            _proc, missing = reserved.call("missing-prepare", "prepare")
            self.assertEqual(missing["pass_state"], "missing")
            (reserved.root / "descriptor.json").write_bytes(b"{torn")
            _proc, failed = reserved.call("torn-prepare", "prepare")
            self.assertEqual(failed["pass_state"], "observation-failed")
        finally:
            reserved.close()
        wrong_target = Book()
        try:
            wrong_target.capture("target")
            reg = json.loads((wrong_target.root / "registration.json").read_text(encoding="utf-8"))
            reg["target"] = "0599.synth-lab/05.02.md"
            write_json(wrong_target.root / "registration.json", reg)
            proc = run("bad-target", LOOP, ["prepare", "--fixture-root", str(wrong_target.root), "--request", "request.json"])
            self.assertEqual(proc.returncode, 2)
            self.assertIn("target is not the derived review destination", proc.stderr.decode())
        finally:
            wrong_target.close()

    def test_legacy_in_place_stays_pending(self) -> None:
        book = Book(submission="sub-legacy")
        try:
            seal(book.root / "0101.hist-lab", "0599.synth-lab", "05.01", "sub-legacy", RETURN.encode("utf-8"), [b"legacy-note"])
            before = snapshot(book.root)
            proc = run("legacy-describe", LOOP, ["describe-legacy", "--book", str(book.root), "--member", "0101.hist-lab"])
            self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:600] + proc.stdout.decode()[:600])
            described = as_json(proc)
            self.assertEqual(snapshot(book.root), before)
            self.assertEqual(described["schema"], "review-loop-legacy-description/1")
            self.assertTrue(described["placement_pending"])
            self.assertFalse(described["final_filing"])
            self.assertFalse(described["filing_claimed"])
            self.assertEqual(described["state"], "complete")
            self.assertEqual(described["descriptor"]["schema"], "return-line-descriptor/2")
            self.assertEqual(described["descriptor"]["custody_format"], "legacy-in-place/1")
            self.assertEqual(described["descriptor"]["placement"]["status"], "pending")
            self.assertEqual(described["descriptor"]["target_page"], "0101.hist-lab")
            self.assertEqual(described["descriptor"]["placement"]["intended_target_page"], "0199.synth-lab")
            self.assertIsNone(described["descriptor"]["placement"]["relocation_record_path"])
            (book.root / "descriptor.json").write_bytes(json.dumps(described["descriptor"], indent=2, sort_keys=True).encode("utf-8") + b"\n")
            book.descriptor = described["descriptor"]
            book.descriptor_bytes = (book.root / "descriptor.json").read_bytes()
            book.write_registration()
            member_hashes = {
                name: sha((book.root / "0101.hist-lab" / name).read_bytes())
                for name in ("return.md", "receipt.json", "manifest.json", "reservation.json")
            }
            prepared_proc, prepared = book.call("legacy-prepare", "prepare")
            self.assertEqual(prepared_proc.returncode, 0, prepared_proc.stderr.decode()[:800])
            self.assertEqual(prepared["observation"]["state"], "complete", prepared["observation"])
            self.assertEqual(prepared["observation"]["placement_status"], "pending")
            self.assertFalse(prepared["observation"]["filing_claimed"])
            self.assertEqual(prepared["observation"]["member"], "0199.synth-lab")
            self.assertEqual(prepared["observation"]["custody_member"], "0101.hist-lab")
            self.assertEqual(prepared["observation"]["task_association"], "not-established")
            self.assertFalse(prepared["full_success"])
            book.decide("legacy")
            recorded, _record_view = book.call("legacy-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 0, recorded.stderr.decode()[:800])
            rendered, render_view = book.call("legacy-render", "render")
            self.assertEqual(rendered.returncode, 0, rendered.stderr.decode()[:800] + rendered.stdout.decode()[:400])
            self.assertTrue(render_view["full_success"])
            self.assertFalse(render_view["accepted"])
            self.assertIn(NEXT, book.page.read_text(encoding="utf-8"))
            for name, digest in member_hashes.items():
                self.assertEqual(sha((book.root / "0101.hist-lab" / name).read_bytes()), digest, name)
            unknown = run("legacy-prefix", LOOP, ["describe-legacy", "--book", str(book.root), "--member", "0201.nope"])
            prefix = as_json(unknown)
            self.assertEqual(prefix["state"], "unsupported")
            self.assertIn("unsupported member prefix", prefix["reason"])
            self.assertFalse(prefix["final_filing"])
        finally:
            book.close()

    def test_legacy_relocated_descriptor_is_consumed(self) -> None:
        outer = Path(tempfile.mkdtemp(prefix="rc0504-reloc-"))
        book = Book(submission="sub-reloc")
        try:
            shutil.rmtree(book.root, ignore_errors=True)
            book.root = outer / "book"
            book.root.mkdir()
            book.page = book.root / book.target
            book.page.parent.mkdir(parents=True)
            book.page.write_bytes(page_bytes())
            (book.root / "assignment.txt").write_bytes(ASSIGNMENT)
            (book.root / "note.md").write_bytes(NOTE)
            book.producer("reloc-init", ["init", "--book", str(book.root), "--name", "00.00.10.work"], {0})
            seal(book.root / "0101.hist-lab", "0599.synth-lab", "05.01", "sub-reloc", RETURN.encode("utf-8"), [b"reloc-note"])
            audit = write_audit(outer, book.root, [{
                "has_receipt": True,
                "old_member": "0101.hist-lab",
                "origin": {"batch": "05.01", "book": "00.00.10.work", "page": "0599.synth-lab"},
                "route": "matched-workflow-return-line",
                "submission": "sub-reloc",
                "target_return": "0199.synth-lab/05.01.return.md",
                "verify_exit": 0,
            }])
            backup = outer / "backup"
            staged = run("reloc-stage", LINES, ["stage", "--book", str(book.root), "--backup", str(backup), "--audit", str(audit)])
            self.assertEqual(staged.returncode, 0, staged.stdout.decode()[:1000] + staged.stderr.decode()[:400])
            adopted = run("reloc-adopt", LINES, ["adopt", "--book", str(book.root), "--backup", str(backup), "--audit", str(audit)])
            self.assertEqual(adopted.returncode, 0, adopted.stdout.decode()[:1000] + adopted.stderr.decode()[:400])
            self.assertTrue(backup.is_dir())
            book.save_descriptor("reloc")
            self.assertEqual(book.descriptor["custody_format"], "legacy-relocated/1")
            self.assertEqual(book.descriptor["state"], "complete")
            self.assertEqual(book.descriptor["target_page"], "0199.synth-lab")
            book.decide("reloc")
            proc, view = book.call("reloc-run", "run", "--decision", "decision.json")
            self.assertEqual(proc.returncode, 0, proc.stderr.decode()[:800] + proc.stdout.decode()[:500])
            self.assertTrue(view["full_success"])
            self.assertFalse(view["accepted"])
            self.assertEqual(view["observation"]["validator"]["tool"], "labs/return-lines-pass01/return_lines.py")
            self.assertIn(NEXT, book.page.read_text(encoding="utf-8"))
            self.assertTrue((backup / "sources" / "0101.hist-lab").is_dir())
        finally:
            book.close()
            shutil.rmtree(outer, ignore_errors=True)

    def test_historical_cycle_records_keep_their_reading(self) -> None:
        legacy = Book()
        try:
            legacy.capture("hist1")
            self._plant(legacy, "prime-cycle-review/1", "05.01-legacy", {"schema": "prime-cycle-decision/1"})
            _proc, view = legacy.call("hist1-read", "read")
            self.assertEqual(view["pass_state"], "review-unusable")
            self.assertEqual(view["current"]["interpretation"], "legacy-binding")
            self.assertFalse(view["current"]["current"])
        finally:
            legacy.close()
        old = Book()
        try:
            old.capture("hist2")
            prepared, template = old.call("hist2-prepare", "prepare")
            self.assertEqual(prepared.returncode, 0, prepared.stderr.decode()[:500])
            binding = template["view"]["template"]["binding"]
            decision = {
                "schema": "prime-cycle-decision/2",
                "review_id": "05.01-old",
                "supersedes": None,
                "recovers": None,
                "binding": {
                    "source": {"page_sha256": binding["write_token"]["sha256"], "page_bytes": binding["write_token"]["bytes"]},
                    "member": binding["member"],
                    "receipt_sha256": binding["receipt_sha256"],
                    "submission_id": binding["submission_id"],
                    "origin": binding["origin"],
                    "direction": binding["direction"],
                },
                "attribution": {
                    "actor_label": "historical",
                    "role": "prime",
                    "evidence": "SUPPLIED historical record. The label is not authentication.",
                },
                "judgment": {
                    "outcome": "continue",
                    "next_action": {"action_id": "old-action", "text": "Historical next action.", "authorized_in_grant": False},
                    "unresolved": [],
                    "sections": {},
                },
            }
            self._plant(old, "prime-cycle-review/2", "05.01-old", decision)
            _proc, view = old.call("hist2-read", "read")
            self.assertEqual(view["pass_state"], "reviewed", view.get("observation"))
            self.assertEqual(view["current"]["interpretation"], "historical-page-hash")
            self.assertEqual(view["current"]["latest_review"]["schema"], "prime-cycle-review/2")
            stored = sha((old.root / "cycle" / "05.01-old" / "record.json").read_bytes())
            old.page.write_bytes(old.page.read_bytes().replace(OUTSIDE.encode("utf-8"), b"OUTSIDE-CHANGED"))
            _proc, stale = old.call("hist2-stale", "read")
            self.assertEqual(stale["pass_state"], "review-stale")
            self.assertEqual(stale["historical"]["schema"], "prime-cycle-review/2")
            self.assertEqual(sha((old.root / "cycle" / "05.01-old" / "record.json").read_bytes()), stored)
        finally:
            old.close()

    def test_pass01_cycle_refuses_descriptor_v2_by_exact_keys(self) -> None:
        book = Book()
        try:
            book.capture("v1reader")
            described = dict(book.descriptor)
            described["schema"] = "return-line-descriptor/2"
            described["placement"] = {
                "status": "final",
                "intended_target_page": described["target_page"],
                "intended_return_path": described["return_path"],
                "relocation_record_path": None,
                "occupancy": None,
            }
            write_json(book.root / "descriptor.json", described)
            proc = run("v1-read", CYCLE02, ["read", "--fixture-root", str(book.root), "--registration", "registration.json"])
            view = as_json(proc)
            self.assertNotEqual(view.get("pass_state"), "awaiting-review")
            self.assertNotEqual(view.get("observation", {}).get("state"), "complete")
            self.assertIn("unknown key", json.dumps(view))
        finally:
            book.close()

    def test_reproduce_uses_the_real_producer(self) -> None:
        missing_dest = Path(tempfile.mkdtemp(prefix="rc0504-missing-"))
        shutil.rmtree(missing_dest)
        refused = run("repro-missing", LOOP, [
            "reproduce", "--destination", str(missing_dest), "--decision", str(missing_dest / "absent.json"),
        ])
        self.assertEqual(refused.returncode, 2)
        self.assertIn("decision file is absent", refused.stderr.decode())
        self.assertFalse(missing_dest.exists())
        destination = Path(tempfile.mkdtemp(prefix="rc0504-repro-"))
        decision = destination / "supplied-decision.json"
        write_json(decision, reproduce_decision())
        proc = run("repro", LOOP, ["reproduce", "--destination", str(destination), "--decision", str(decision)])
        if proc.returncode != 0:
            transcript = destination / "transcript.json"
            detail = transcript.read_text(encoding="utf-8")[:1500] if transcript.exists() else ""
            self.fail(proc.stderr.decode()[:800] + proc.stdout.decode()[:800] + detail)
        view = as_json(proc)
        self.assertTrue(view["full_success"])
        self.assertFalse(view["accepted"])
        self.assertEqual(view["custody"], "not-established")
        described = json.loads((destination / "descriptor.json").read_text(encoding="utf-8"))
        self.assertEqual(described["schema"], "return-line-descriptor/1")
        self.assertEqual(described["target_page"], "0199.synth-lab")
        self.assertEqual(described["state"], "complete")
        text = (destination / "sample-review.md").read_text(encoding="utf-8")
        self.assertIn(NEXT, text)
        self.assertIn(OUTSIDE, text)
        self.assertIn("authority: none", text)
        shutil.rmtree(destination, ignore_errors=True)

    def test_predecessor_loop_without_its_writer(self) -> None:
        before = {
            path: sha(path.read_bytes())
            for path in (
                EVIDENCE / "build05.03" / "transcript.json",
                EVIDENCE / "build05.03" / "sample-review.md",
                EVIDENCE / "build05.03" / "synthetic-descriptor.json",
            )
        }
        spec = importlib.util.spec_from_file_location(
            "review_loop_pass01_tests",
            ROOT / "labs" / "review-loop-pass01" / "test_review_loop.py",
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        suite = unittest.TestSuite()
        for name in unittest.defaultTestLoader.getTestCaseNames(module.ReviewLoopTests):
            if name == "test_full_wording_is_preserved":
                continue
            suite.addTest(module.ReviewLoopTests(name))
        stream = io.StringIO()
        result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
        self.assertTrue(result.wasSuccessful(), stream.getvalue()[-1500:])
        for path, digest in before.items():
            self.assertEqual(sha(path.read_bytes()), digest, path.name)

    def _rewrite(self, path: Path, change) -> None:
        desc = json.loads((path / "descriptor.json").read_text(encoding="utf-8"))
        change(desc)
        write_json(path / "descriptor.json", desc)

    def _bad_receipt(self, path: Path) -> None:
        blob = b'{"schema":"synthetic-receipt/1","label":"unrelated"}\n'
        desc = json.loads((path / "descriptor.json").read_text(encoding="utf-8"))
        (path / desc["receipt_path"]).write_bytes(blob)
        desc["receipt_sha256"] = sha(blob)
        desc["state"] = "complete"
        write_json(path / "descriptor.json", desc)

    def _flip_payload(self, path: Path) -> None:
        desc = json.loads((path / "descriptor.json").read_text(encoding="utf-8"))
        payload = path / desc["custody_path"] / "payload" / "0001.blob"
        payload.write_bytes(payload.read_bytes() + b"x")

    def _flip_manifest(self, path: Path) -> None:
        desc = json.loads((path / "descriptor.json").read_text(encoding="utf-8"))
        manifest = path / desc["manifest_path"]
        manifest.write_bytes(manifest.read_bytes().replace(b"note.md", b"nope.md", 1))

    def _custody_file(self, path: Path) -> None:
        desc = json.loads((path / "descriptor.json").read_text(encoding="utf-8"))
        custody = path / desc["custody_path"]
        shutil.rmtree(custody)
        custody.write_bytes(b"not a directory\n")

    def _sentinel(self, path: Path) -> None:
        scratch = path / "scratch"
        scratch.mkdir(exist_ok=True)
        flag = scratch / "ran.txt"
        (scratch / "sentinel.py").write_text(
            "from pathlib import Path\nPath(r'" + str(flag) + "').write_text('ran')\n",
            encoding="utf-8",
        )
        desc = json.loads((path / "descriptor.json").read_text(encoding="utf-8"))
        desc["verification"]["tool_path"] = "scratch/sentinel.py"
        write_json(path / "descriptor.json", desc)

    def _staged(self, path: Path) -> None:
        desc = json.loads((path / "descriptor.json").read_text(encoding="utf-8"))
        desc["schema"] = "return-line-descriptor/2"
        desc["custody_format"] = "staged-seal/1"
        desc["placement"] = {
            "status": "pending",
            "intended_target_page": desc["target_page"],
            "intended_return_path": desc["return_path"],
            "relocation_record_path": None,
            "occupancy": None,
        }
        write_json(path / "descriptor.json", desc)

    def _bad_variant(self, path: Path) -> None:
        desc = json.loads((path / "descriptor.json").read_text(encoding="utf-8"))
        desc["schema"] = "return-line-descriptor/2"
        desc["placement"] = {
            "status": "final",
            "intended_target_page": "0198.other",
            "intended_return_path": desc["return_path"],
            "relocation_record_path": None,
            "occupancy": None,
        }
        write_json(path / "descriptor.json", desc)

    def _final_v2(self, path: Path) -> None:
        desc = json.loads((path / "descriptor.json").read_text(encoding="utf-8"))
        desc["schema"] = "return-line-descriptor/2"
        desc["placement"] = {
            "status": "final",
            "intended_target_page": desc["target_page"],
            "intended_return_path": desc["return_path"],
            "relocation_record_path": None,
            "occupancy": None,
        }
        write_json(path / "descriptor.json", desc)

    def _plant(self, book: Book, schema: str, review_id: str, decision: dict) -> None:
        directory = book.root / "cycle" / review_id
        directory.mkdir(parents=True)
        record = {
            "schema": schema,
            "work_id": "synth-" + book.page_id[:4],
            "review_id": review_id,
            "decision": decision,
        }
        record_bytes = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        review = f"# Historical {review_id}\n\nThis planted record is not approval.\n".encode("utf-8")
        marker = json.dumps(
            {"record_sha256": sha(record_bytes), "review_md_sha256": sha(review)},
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        (directory / "record.json").write_bytes(record_bytes)
        (directory / "REVIEW.md").write_bytes(review)
        (directory / "COMMITTED.json").write_bytes(marker)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ReviewLoopTests)
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    EVIDENCE.joinpath("build05.04").mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "build05.04" / "suite.log").write_bytes(stream.getvalue().encode("utf-8"))
    (EVIDENCE / "build05.04" / "commands.json").write_bytes(
        json.dumps(LOG, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
