#!/usr/bin/env python3
"""Disposable review-loop tests. Synthetic judgment only.

Transcripts go to evidence/build05.03. This file does not rerun the
constructor suite and does not write evidence/build05.01 or evidence/build05.02.
"""

from __future__ import annotations

import hashlib
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
LOOP = ROOT / "labs" / "review-loop-pass01" / "review_loop.py"
CYCLE = ROOT / "labs" / "prime-cycle-pass02" / "prime_cycle.py"
REVIEW01 = ROOT / "labs" / "prime-review-pass01" / "prime_review.py"
REVIEW02 = ROOT / "labs" / "prime-review-pass02" / "prime_review.py"
EVIDENCE = ROOT / "00.kernel" / "00.00.10.work" / "0522.review-construction" / "evidence" / "build05.03"
LOG: list[dict] = []
SAMPLE = {"text": ""}

ASSIGNMENT = b"Synthetic assignment. Write one piece.\n"
REVISED = b"Synthetic assignment. Revised piece.\n"
PIECE = b"synthetic piece\n"
RETURN = b"Did.\nSynthetic return.\n"
RECEIPT = b'{"schema":"synthetic-receipt/1","label":"synthetic"}\n'
MANIFEST = b'{"schema":"synthetic-manifest/1"}\n'
DISSENT = "Dissent: the minority keeps the older wording — do not smooth it."
REPLY = "Director reply: keep the synthetic piece as one file."
QUESTION = "Should the older wording stay on the record?"
HELD_QUESTION = "Should the synthetic piece stay one file?"
NEXT = "Pack one bounded correction for the synthetic piece."
HELD_NEXT = "Wait for a reply to the synthetic question."
OUTSIDE = "OUTSIDE-Δ-TOKEN"
TAIL = "TAIL-Δ-TOKEN"

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
        "finish_criteria": [{"id": "piece", "text": "The synthetic piece stays one file."}],
        "goal": "Review one synthetic piece.",
        "prime_discretion": "Prime may record a judgment inside that grant.",
        "recorded_decisions": [{
            "id": "D1",
            "source_sha256": sha(b"decision"),
            "text": "The synthetic pack was supplied for this lab.",
        }],
        "scope": "The disposable fixture only.",
    }


def sections() -> dict:
    return {key: None for key in SECTION_KEYS}


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
    row["identity"] = {"schema": "supplied-text/1", "label": "SYNTHETIC"}
    return row


def source_capture(path: str, data: bytes, member: str, page_id: str, receipt_sha: str) -> dict:
    row = source_page(path, data)
    row["kind"] = "capture"
    row["identity"] = {
        "schema": "return-capture/1",
        "member": member,
        "submission_id": "synthetic-0522",
        "receipt_sha256": receipt_sha,
        "origin": {"book": "00.00.10.work", "page": page_id, "batch": "05.01"},
    }
    return row


def page_bytes(body: str = "PENDING.\n") -> bytes:
    text = (
        f"Intro {OUTSIDE}\n\n"
        "## Return pointer\n"
        "PENDING.\n\n"
        "## Review — Codex Prime\n"
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
        raise AssertionError(proc.stderr.decode("utf-8", errors="replace")[:800]) from exc


def write_json(path: Path, payload: dict) -> None:
    path.write_bytes(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")


class Fixture:
    def __init__(self, kind: str = "N5NN", page_id: str = "0599.synth-lab", body: str = "PENDING.\n"):
        self.root = Path(tempfile.mkdtemp(prefix="reviewloop-"))
        self.kind = kind
        self.page_id = page_id
        self.pass_id = "05.01"
        tail = "01"
        if kind == "N5NN":
            space, nn, subject = page_id[0], page_id[2:4], page_id.split(".", 1)[1]
            self.member = f"{space}1{nn}.{subject}"
            self.target = f"{page_id}/{self.pass_id}.md"
            self.kernel = f"00.kernel/00.00.10.work/{page_id}/{self.pass_id}.md"
            self.route = "matched-workflow-return-line"
        else:
            self.member = None
            self.target = f"{page_id}/06.{tail}.review.md"
            self.kernel = f"00.kernel/00.00.10.work/{page_id}/{self.pass_id}.pack.md"
            self.route = "page-local-colab"
        self.page = self.root / self.target
        self.page.parent.mkdir(parents=True)
        self.page.write_bytes(page_bytes(body))
        (self.root / "assignment.txt").write_bytes(ASSIGNMENT)
        (self.root / "piece.txt").write_bytes(PIECE)
        (self.root / "return.md").write_bytes(RETURN)
        (self.root / "receipt.json").write_bytes(RECEIPT)
        (self.root / "manifest.json").write_bytes(MANIFEST)
        (self.root / "custody.txt").write_bytes(b"synthetic custody pointer\n")
        (self.root / "verification.txt").write_bytes(b"synthetic observation\n")
        self.descriptor = self._descriptor("complete")
        write_json(self.root / "descriptor.json", self.descriptor)
        self.registration = self._registration()
        write_json(self.root / "registration.json", self.registration)
        write_json(self.root / "request.json", {
            "schema": "review-loop-request/1",
            "registration_path": "registration.json",
        })

    def _descriptor(self, state: str) -> dict:
        receipt_sha = sha(RECEIPT) if state == "complete" else None
        return_sha = sha(RETURN) if state == "complete" else None
        return_bytes = len(RETURN) if state == "complete" else None
        return {
            "schema": "return-line-descriptor/1",
            "origin": {"book": "00.00.10.work", "page": self.page_id, "batch": self.pass_id},
            "route": self.route,
            "target_page": self.target,
            "return_path": "return.md",
            "custody_path": "custody.txt",
            "receipt_path": "receipt.json",
            "manifest_path": "manifest.json",
            "submission_id": "synthetic-0522",
            "custody_format": "return-line-capture/1",
            "receipt_sha256": receipt_sha,
            "return_sha256": return_sha,
            "return_bytes": return_bytes,
            "state": state,
            "verification": {
                "tool_path": "scratch/verifier.txt",
                "tool_sha256": sha(b"synthetic-verifier"),
                "result": "synthetic-observed",
                "evidence_path": "verification.txt",
            },
        }

    def _registration(self) -> dict:
        return {
            "schema": "prime-cycle-registration/2",
            "book": "00.00.10.work",
            "work_id": "synth-0599",
            "source_kind": self.kind,
            "page_id": self.page_id,
            "pass": self.pass_id,
            "kernel_page": self.kernel,
            "target": self.target,
            "descriptor_path": "descriptor.json",
            "agreement": agreement(),
            "task_id": "synth-task",
            "assignment_path": "assignment.txt",
            "evidence": [{"label": "synthetic", "logical_path": "piece.txt"}],
            "submission_id": "synthetic-0522",
            "receipt_label": "synthetic",
            "review_identity": "r1",
            "review_location": "cycle",
            "goal": {
                "goal_id": "g-synth",
                "statement": "Review one synthetic piece.",
                "terminal": "open",
                "evidence": [],
            },
            "bounds": {"max_output_bytes": 2097152},
        }

    def args(self, command: str, *extra: str) -> list[str]:
        return [command, "--fixture-root", str(self.root), "--request", "request.json", *extra]

    def call(self, name: str, command: str, *extra: str) -> tuple[subprocess.CompletedProcess, dict]:
        proc = run(name, LOOP, self.args(command, *extra))
        return proc, as_json(proc)

    def record_body(self, kind: str) -> dict:
        body = sections()
        body["return_result"] = "The builder returned the synthetic piece."
        body["prime_finding"] = "The synthetic piece is present."
        body["within_direction"] = "This stays inside the synthetic grant."
        body["next_bounded_action"] = "Hand back one correction pack."
        record = {
            "schema": "prime-review-record/1",
            "attribution": {
                "actor_label": "Codex Prime (SUPPLIED)",
                "role": "prime",
                "evidence": "SUPPLIED synthetic judgment. The label is not authentication.",
            },
            "sources": [
                source_page("assignment.txt", (self.root / "assignment.txt").read_bytes()),
                source_text("piece.txt", (self.root / "piece.txt").read_bytes()),
            ],
            "agreement": self.registration["agreement"],
            "holds": [],
            "answers": [],
            "review_passes": [],
            "gaps": [],
            "judgment": {
                "outcome": "continue",
                "finding": "The synthetic piece is present.",
                "reasons": ["The supplied return names the piece."],
                "semantic_conflict": False,
                "design_fork": None,
                "next_action": NEXT,
                "sections": body,
            },
        }
        if self.kind == "N5NN":
            record["sources"].append(source_capture("return.md", RETURN, self.member, self.page_id, sha(RECEIPT)))
        else:
            record["sources"].append(source_text("return.md", RETURN))
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
            body["question"] = {
                "id": "Q-store",
                "revision": "r1",
                "content_sha256": held_sha,
                "text": HELD_QUESTION,
            }
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
            body["limits"] = "Synthetic judgment. This render is not acceptance."
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
                    "evidence": "SUPPLIED synthetic reply. The label is not authentication.",
                },
                "disposition": "brief-approval",
            }]
        return record

    def judgment_for(self, record: dict) -> dict:
        supplied = record["judgment"]
        goal = self.registration["goal"]
        if supplied["outcome"] == "director-input":
            disposition = "held"
        else:
            disposition = "accepted"
        return {
            "outcome": supplied["outcome"],
            "disposition": disposition,
            "pass_terminal": "open",
            "goal": {
                "terminal": "open",
                "goal_id": goal["goal_id"],
                "goal_sha256": sha(goal["statement"].encode("utf-8")),
                "evidence": [],
            },
            "finding": supplied["finding"],
            "reasons": supplied["reasons"],
            "source_refs": ["assignment.txt"],
            "next_action": {
                "action_id": "pack-correction" if supplied["outcome"] == "continue" else "wait-reply",
                "text": supplied["next_action"],
                "authorized_in_grant": False,
            },
            "unresolved": [],
            "semantic_conflict": supplied["semantic_conflict"],
            "design_fork": supplied["design_fork"],
            "holds": record["holds"],
            "answers": record["answers"],
            "sections": supplied["sections"],
        }

    def decide(self, kind: str = "clean") -> dict:
        proc, view = self.call(f"{self.page_id}-prepare", "prepare")
        if proc.returncode != 0 or view.get("view", {}).get("template") is None:
            raise AssertionError(proc.stderr.decode("utf-8", errors="replace")[:800] + proc.stdout.decode()[:800])
        decision = deepcopy(view["view"]["template"])
        record = self.record_body(kind)
        decision["attribution"] = record["attribution"]
        decision["judgment"] = self.judgment_for(record)
        decision["supplied_record"] = record
        write_json(self.root / "decision.json", decision)
        self.prepared = view
        return decision

    def close(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)


class ReviewLoopTests(unittest.TestCase):
    def test_sealed_tools_and_prior_evidence(self) -> None:
        pins = {
            ROOT / "labs/review-construction-pass01/construct.py": (
                "8b9d4a6eda460f594404042f7ee232a7ac55fcc09af38905de364defa189ea8a", 35956,
            ),
            ROOT / "labs/prime-review-pass01/prime_review.py": (
                "805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0", 58324,
            ),
            ROOT / "labs/prime-cycle-pass01/prime_cycle.py": (
                "19ede9c2125307595d0be867bae1a3cb71bf3db0515ad83e7c04d3333e17861d", 77846,
            ),
            EVIDENCE.parent / "build05.02" / "transcript.json": (
                "b8a07fe1bb6a00fc561b82297694ddd3b520bf004bf4742ca166816ee960e210", 86883,
            ),
            EVIDENCE.parent / "build05.02" / "sample-review.md": (
                "ede86bcbbbd5768cbc81d858fdeee39497a81fd5fed6a262cb366690b890ee51", 4406,
            ),
        }
        for path, (digest, size) in pins.items():
            blob = path.read_bytes()
            self.assertEqual(len(blob), size, path.name)
            self.assertEqual(sha(blob), digest, path.name)
        cycle = CYCLE.read_text(encoding="utf-8")
        loop = LOOP.read_text(encoding="utf-8")
        self.assertNotIn("return-capture-pass01", cycle)
        self.assertNotIn("return-capture-pass01", loop)
        self.assertNotIn("return_capture.reserve", cycle)
        self.assertNotIn("return_capture.reserve", loop)

    def test_zero_space_loop_survives_restart(self) -> None:
        fix = Fixture()
        try:
            decision = fix.decide("clean")
            binding = decision["binding"]["task_binding_sha256"]
            token_before = decision["binding"]["write_token"]["sha256"]
            recorded, record_view = fix.call("zero-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 0, recorded.stderr.decode())
            self.assertTrue(record_view["full_success"])
            self.assertFalse(record_view["accepted"])
            self.assertEqual(record_view["custody"], "not-established")
            pending, pending_view = fix.call("zero-read-pending", "read")
            self.assertEqual(pending.returncode, 0)
            self.assertEqual(pending_view["pass_state"], "render-pending")
            self.assertFalse(pending_view["full_success"])
            self.assertEqual(pending_view["current"]["next_action"]["text"], NEXT)
            rendered, render_view = fix.call("zero-render", "render")
            self.assertEqual(rendered.returncode, 0, rendered.stderr.decode() + rendered.stdout.decode()[:500])
            self.assertTrue(render_view["full_success"])
            page = fix.page.read_bytes()
            text = page.decode("utf-8")
            self.assertIn(OUTSIDE, text)
            self.assertIn(TAIL, text)
            self.assertIn("authority: none", text)
            self.assertIn(f"task_binding: {binding}", text)
            self.assertIn(NEXT, text)
            self.assertNotEqual(sha(page), token_before)
            fresh, fresh_view = fix.call("zero-read-new-process", "read")
            self.assertEqual(fresh.returncode, 0)
            self.assertEqual(fresh_view["pass_state"], "reviewed")
            self.assertEqual(fresh_view["current"]["render_state"], "rendered")
            self.assertTrue(fresh_view["current"]["current"])
            self.assertEqual(fresh_view["current"]["next_action"]["text"], NEXT)
            self.assertEqual(fresh_view["current"]["task_binding_sha256"], binding)
            self.assertNotEqual(fresh_view["current"]["write_token"]["sha256"], token_before)
            self.assertTrue(fresh_view["full_success"])
            again, again_view = fix.call("zero-recover", "recover")
            self.assertEqual(again.returncode, 0, again.stderr.decode())
            self.assertEqual(again_view["render"]["result"], "already-rendered")
            self.assertFalse(again_view["render"]["apply_called"])
            self.assertEqual(sha(fix.page.read_bytes()), sha(page))
            replay, replay_view = fix.call("zero-replay", "record", "--decision", "decision.json")
            self.assertEqual(replay.returncode, 0)
            self.assertEqual(replay_view["record"]["result"], "already-recorded")
        finally:
            fix.close()

    def test_changed_inputs_stale_the_review(self) -> None:
        fix = Fixture()
        try:
            fix.decide("clean")
            recorded, _view = fix.call("stale-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 0, recorded.stderr.decode())
            rendered, _render = fix.call("stale-render", "render")
            self.assertEqual(rendered.returncode, 0, rendered.stderr.decode())
            record_path = fix.root / "cycle" / "05.01-r1" / "record.json"
            record_hash = sha(record_path.read_bytes())
            cases = {}
            cases["evidence"] = self._mutate_copy(fix, lambda copy: (copy / "piece.txt").write_bytes(b"synthetic piece revised\n"))
            cases["task"] = self._mutate_copy(fix, lambda copy: (copy / "assignment.txt").write_bytes(REVISED))

            def change_agreement(copy: Path) -> None:
                reg = json.loads((copy / "registration.json").read_text(encoding="utf-8"))
                reg["agreement"]["goal"] = "Review a revised synthetic piece."
                write_json(copy / "registration.json", reg)

            cases["agreement"] = self._mutate_copy(fix, change_agreement)

            def change_receipt(copy: Path) -> None:
                blob = b'{"schema":"synthetic-receipt/1","label":"revised"}\n'
                (copy / "receipt.json").write_bytes(blob)
                desc = json.loads((copy / "descriptor.json").read_text(encoding="utf-8"))
                desc["receipt_sha256"] = sha(blob)
                write_json(copy / "descriptor.json", desc)

            cases["receipt"] = self._mutate_copy(fix, change_receipt)
            for label, copy in cases.items():
                proc = run(f"stale-{label}", LOOP, ["read", "--fixture-root", str(copy), "--request", "request.json"])
                view = as_json(proc)
                self.assertEqual(proc.returncode, 0, label)
                self.assertEqual(view["pass_state"], "review-stale", label)
                self.assertFalse(view["current"]["current"], label)
                self.assertEqual(view["historical"]["review_id"], "05.01-r1", label)
                self.assertEqual(sha((copy / "cycle" / "05.01-r1" / "record.json").read_bytes()), record_hash, label)
                shutil.rmtree(copy, ignore_errors=True)
        finally:
            fix.close()

    def test_revised_task_does_not_rebind(self) -> None:
        fix = Fixture()
        try:
            decision = fix.decide("clean")
            self.assertEqual(fix.call("rebind-record", "record", "--decision", "decision.json")[0].returncode, 0)
            self.assertEqual(fix.call("rebind-render", "render")[0].returncode, 0)
            copy = self._mutate_copy(fix, lambda path: (path / "assignment.txt").write_bytes(REVISED))
            try:
                view = as_json(run("rebind-read", LOOP, ["read", "--fixture-root", str(copy), "--request", "request.json"]))
                self.assertEqual(view["pass_state"], "review-stale")
                prior = view["historical"]
                revised = json.loads((copy / "decision.json").read_text(encoding="utf-8"))
                revised["review_id"] = "05.01-r2"
                revised["supersedes"] = {"review_id": prior["review_id"], "record_sha256": prior["record_sha256"]}
                revised["binding"]["expected_prior"] = revised["supersedes"]
                write_json(copy / "decision-b.json", revised)
                refused = run(
                    "rebind-record-b",
                    LOOP,
                    ["record", "--fixture-root", str(copy), "--request", "request.json", "--decision", "decision-b.json"],
                )
                self.assertEqual(refused.returncode, 2)
                self.assertIn("task binding changed since read", refused.stderr.decode("utf-8"))
                self.assertFalse((copy / "cycle" / "05.01-r2").exists())
                self.assertEqual(
                    sha((copy / "cycle" / "05.01-r1" / "record.json").read_bytes()),
                    sha((fix.root / "cycle" / "05.01-r1" / "record.json").read_bytes()),
                )
            finally:
                shutil.rmtree(copy, ignore_errors=True)
            self.assertEqual(decision["review_id"], "05.01-r1")
        finally:
            fix.close()

    def test_director_question_is_recovered(self) -> None:
        fix = Fixture()
        try:
            fix.decide("held")
            recorded, _view = fix.call("held-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 1, recorded.stderr.decode() + recorded.stdout.decode()[:600])
            rendered, render_view = fix.call("held-render", "render")
            self.assertIn(rendered.returncode, {0, 1}, rendered.stderr.decode())
            self.assertFalse(render_view["accepted"])
            text = fix.page.read_text(encoding="utf-8")
            self.assertIn(HELD_QUESTION, text)
            self.assertIn(OUTSIDE, text)
            fresh, view = fix.call("held-read", "read")
            self.assertEqual(fresh.returncode, 0)
            self.assertEqual(view["current"]["next_action"]["text"], HELD_NEXT)
            self.assertIn(HELD_QUESTION, view["current"]["questions"])
        finally:
            fix.close()

    def test_duplicate_judgment_keeps_the_first(self) -> None:
        fix = Fixture()
        try:
            fix.decide("clean")
            first, first_view = fix.call("dup-record", "record", "--decision", "decision.json")
            self.assertEqual(first.returncode, 0, first.stderr.decode())
            digest = sha((fix.root / "cycle" / "05.01-r1" / "record.json").read_bytes())
            second, second_view = fix.call("dup-replay", "record", "--decision", "decision.json")
            self.assertEqual(second.returncode, 0)
            self.assertEqual(second_view["record"]["result"], "already-recorded")
            revised = json.loads((fix.root / "decision.json").read_text(encoding="utf-8"))
            revised["judgment"]["finding"] = "A different finding."
            revised["supplied_record"]["judgment"]["finding"] = "A different finding."
            write_json(fix.root / "decision-conflict.json", revised)
            refused = run(
                "dup-conflict",
                LOOP,
                ["record", "--fixture-root", str(fix.root), "--request", "request.json", "--decision", "decision-conflict.json"],
            )
            self.assertEqual(refused.returncode, 2)
            self.assertIn("conflict: a different review is already committed", refused.stderr.decode("utf-8"))
            self.assertEqual(sha((fix.root / "cycle" / "05.01-r1" / "record.json").read_bytes()), digest)
            self.assertEqual(first_view["record"]["review_id"], "05.01-r1")
        finally:
            fix.close()

    def test_unknown_origin_and_wrong_destination(self) -> None:
        fix = Fixture()
        try:
            desc = json.loads((fix.root / "descriptor.json").read_text(encoding="utf-8"))
            desc["origin"]["page"] = "0588.other-page"
            write_json(fix.root / "descriptor.json", desc)
            proc, view = fix.call("bad-origin", "prepare")
            self.assertEqual(proc.returncode, 0)
            self.assertEqual(view["pass_state"], "conflict")
            self.assertIn("origin does not match the source", view["observation"]["reason"])
            self.assertFalse((fix.root / "cycle").exists())
        finally:
            fix.close()
        wrong = Fixture()
        try:
            reg = json.loads((wrong.root / "registration.json").read_text(encoding="utf-8"))
            reg["target"] = "0599.synth-lab/05.02.md"
            write_json(wrong.root / "registration.json", reg)
            proc = run("bad-target", LOOP, wrong.args("prepare"))
            self.assertEqual(proc.returncode, 2)
            self.assertTrue(proc.stderr.decode("utf-8").startswith("refused:"))
            self.assertIn("target is not the derived review destination", proc.stderr.decode("utf-8"))
            self.assertFalse((wrong.root / "cycle").exists())
        finally:
            wrong.close()

    def test_substantive_section_recovers_without_a_second_partial(self) -> None:
        fix = Fixture(body="A different substantive review.\n")
        try:
            fix.decide("clean")
            self.assertEqual(fix.call("conflict-record", "record", "--decision", "decision.json")[0].returncode, 0)
            before = sha(fix.page.read_bytes())
            first = run("conflict-recover", LOOP, fix.args("recover"))
            view = as_json(first)
            self.assertEqual(first.returncode, 2, first.stdout.decode()[:500])
            self.assertEqual(view["pass_state"], "render-conflict")
            self.assertEqual(view["render"]["apply_called"], True)
            partials = list((fix.root / "partial").glob("*.md"))
            self.assertEqual(len(partials), 1)
            self.assertEqual(sha(fix.page.read_bytes()), before)
            second = run("conflict-recover-again", LOOP, fix.args("recover"))
            again = as_json(second)
            self.assertEqual(second.returncode, 2)
            self.assertFalse(again["render"]["apply_called"])
            self.assertEqual(list((fix.root / "partial").glob("*.md")), partials)
            self.assertEqual(sha(fix.page.read_bytes()), before)
            self.assertTrue((fix.root / "cycle" / "05.01-r1" / "COMMITTED.json").is_file())
        finally:
            fix.close()

    def test_nonzero_origin_stops_at_the_constructor_pin(self) -> None:
        fix = Fixture(page_id="1599.synth-lab")
        try:
            self.assertEqual(fix.member, "1199.synth-lab")
            decision = fix.decide("clean")
            self.assertEqual(decision["binding"]["member"], "1199.synth-lab")
            recorded, record_view = fix.call("nonzero-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 0, recorded.stderr.decode() + recorded.stdout.decode()[:700])
            self.assertEqual(record_view["record"]["result"], "recorded")
            before = sha(fix.page.read_bytes())
            rendered, render_view = fix.call("nonzero-render", "render")
            self.assertEqual(rendered.returncode, 1)
            self.assertFalse(render_view["full_success"])
            self.assertEqual(render_view["render"]["result"], "render-pending")
            self.assertIn("bad member", render_view["render"]["rule"])
            self.assertIn("prime-review-pass02", render_view["next"])
            self.assertEqual(sha(fix.page.read_bytes()), before)
            self.assertFalse((fix.root / "partial").exists())
            again, again_view = fix.call("nonzero-recover", "recover")
            self.assertEqual(again.returncode, 1)
            self.assertEqual(again_view["render"]["result"], "render-pending")
            self.assertEqual(sha(fix.page.read_bytes()), before)
            record_path = fix.root / "scratch" / "supplied-record.json"
            pass01 = run("nonzero-pass01", REVIEW01, ["report", "--input", str(record_path), "--json"])
            pass02 = run("nonzero-pass02", REVIEW02, ["report", "--input", str(record_path), "--json"])
            self.assertEqual(pass01.returncode, 2)
            self.assertIn("bad member", pass01.stderr.decode("utf-8"))
            self.assertIn(pass02.returncode, {0, 1})
            self.assertEqual(record_view["custody"], "not-established")
        finally:
            fix.close()

    def test_n7nn_renders_on_its_own_tail(self) -> None:
        fix = Fixture(kind="N7NN", page_id="1799.synth-colab")
        try:
            fix.decide("clean")
            proc, view = fix.call("n7-run", "run", "--decision", "decision.json")
            self.assertEqual(proc.returncode, 0, proc.stderr.decode() + proc.stdout.decode()[:700])
            self.assertTrue(view["full_success"])
            text = fix.page.read_text(encoding="utf-8")
            self.assertTrue(str(fix.page).endswith("06.01.review.md"))
            self.assertIn("authority: none", text)
            self.assertIn(OUTSIDE, text)
            self.assertIn(TAIL, text)
            self.assertIn(NEXT, text)
            self.assertIsNone(view["view"]["member"])
            fresh, read_view = fix.call("n7-read", "read")
            self.assertEqual(fresh.returncode, 0)
            self.assertEqual(read_view["current"]["next_action"]["text"], NEXT)
        finally:
            fix.close()

    def test_descriptor_states_stay_distinct(self) -> None:
        missing = Fixture()
        try:
            (missing.root / "descriptor.json").unlink()
            _proc, view = missing.call("state-missing", "prepare")
            self.assertEqual(view["pass_state"], "missing")
            self.assertIsNone(view["observation"]["measured"]["receipt_sha256"])
            self.assertIsNone(view["observation"]["measured"]["return_bytes"])
        finally:
            missing.close()
        reserved = Fixture()
        try:
            write_json(reserved.root / "descriptor.json", reserved._descriptor("reserved"))
            (reserved.root / "receipt.json").unlink()
            _proc, view = reserved.call("state-reserved", "prepare")
            self.assertEqual(view["pass_state"], "reserved")
            self.assertNotEqual(view["pass_state"], "missing")
        finally:
            reserved.close()
        incomplete = Fixture()
        try:
            write_json(incomplete.root / "descriptor.json", incomplete._descriptor("incomplete"))
            _proc, view = incomplete.call("state-incomplete", "prepare")
            self.assertEqual(view["pass_state"], "incomplete")
        finally:
            incomplete.close()
        failed = Fixture()
        try:
            (failed.root / "descriptor.json").write_bytes(b"{torn")
            _proc, view = failed.call("state-failed", "prepare")
            self.assertEqual(view["pass_state"], "observation-failed")
        finally:
            failed.close()

    def test_old_records_keep_their_historical_reading(self) -> None:
        legacy = Fixture()
        try:
            self._plant(legacy, "prime-cycle-review/1", "05.01-legacy", {"schema": "prime-cycle-decision/1"})
            _proc, view = legacy.call("legacy-read", "prepare")
            self.assertEqual(view["pass_state"], "review-unusable")
            self.assertEqual(view["historical"]["interpretation"], "legacy-binding")
            self.assertFalse(view["current"]["current"])
        finally:
            legacy.close()
        old = Fixture()
        try:
            prepared, template = old.call("old-prepare", "prepare")
            self.assertEqual(prepared.returncode, 0, prepared.stderr.decode())
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
            _proc, view = old.call("old-read", "read")
            self.assertEqual(view["pass_state"], "reviewed")
            self.assertEqual(view["interpretation"] if "interpretation" in view else view["current"]["interpretation"], "historical-page-hash")
            self.assertEqual(view["current"]["latest_review"]["schema"], "prime-cycle-review/2")
            stored = sha((old.root / "cycle" / "05.01-old" / "record.json").read_bytes())
            blob = old.page.read_bytes().replace(OUTSIDE.encode("utf-8"), b"OUTSIDE-CHANGED")
            old.page.write_bytes(blob)
            _proc, stale = old.call("old-stale", "read")
            self.assertEqual(stale["pass_state"], "review-stale")
            self.assertEqual(stale["historical"]["schema"], "prime-cycle-review/2")
            self.assertEqual(sha((old.root / "cycle" / "05.01-old" / "record.json").read_bytes()), stored)
        finally:
            old.close()

    def test_partial_review_is_kept(self) -> None:
        fix = Fixture()
        try:
            partial = fix.root / "cycle" / "05.01-part"
            partial.mkdir(parents=True)
            (partial / "record.json").write_bytes(b'{"schema":"prime-cycle-review/3"}\n')
            _proc, view = fix.call("partial-read", "prepare")
            self.assertTrue(any("partial review 05.01-part" in item for item in view["view"]["attention"]))
            decision = deepcopy(view["view"]["template"])
            record = fix.record_body("clean")
            decision["attribution"] = record["attribution"]
            decision["judgment"] = fix.judgment_for(record)
            decision["supplied_record"] = record
            decision["recovers"] = "05.01-part"
            write_json(fix.root / "decision.json", decision)
            recorded, _recorded_view = fix.call("partial-record", "record", "--decision", "decision.json")
            self.assertEqual(recorded.returncode, 0, recorded.stderr.decode() + recorded.stdout.decode()[:500])
            self.assertTrue((partial / "record.json").is_file())
            self.assertTrue((fix.root / "cycle" / decision["review_id"] / "COMMITTED.json").is_file())
        finally:
            fix.close()

    def test_full_wording_is_preserved(self) -> None:
        fix = Fixture()
        try:
            fix.decide("full")
            recorded, _view = fix.call("full-record", "record", "--decision", "decision.json")
            self.assertIn(recorded.returncode, {0, 1}, recorded.stderr.decode() + recorded.stdout.decode()[:700])
            rendered, _render = fix.call("full-render", "render")
            self.assertIn(rendered.returncode, {0, 1}, rendered.stderr.decode())
            text = fix.page.read_text(encoding="utf-8")
            self.assertIn(DISSENT, text)
            self.assertIn(REPLY, text)
            self.assertIn(OUTSIDE, text)
            self.assertIn(TAIL, text)
            self.assertIn("authority: none", text)
            SAMPLE["text"] = text
            descriptor = json.loads((fix.root / "descriptor.json").read_text(encoding="utf-8"))
            (EVIDENCE / "synthetic-descriptor.json").write_bytes(
                json.dumps(descriptor, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n"
            )
        finally:
            fix.close()

    def _mutate_copy(self, fix: Fixture, change) -> Path:
        copy = Path(tempfile.mkdtemp(prefix="reviewloop-copy-"))
        shutil.rmtree(copy)
        shutil.copytree(fix.root, copy)
        change(copy)
        return copy

    def _plant(self, fix: Fixture, schema: str, review_id: str, decision: dict) -> None:
        directory = fix.root / "cycle" / review_id
        directory.mkdir(parents=True)
        record = {
            "schema": schema,
            "work_id": "synth-0599",
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


def load_tests(_loader, tests, _pattern):
    suite = unittest.TestSuite()
    order = [
        "test_sealed_tools_and_prior_evidence",
        "test_zero_space_loop_survives_restart",
        "test_changed_inputs_stale_the_review",
        "test_revised_task_does_not_rebind",
        "test_director_question_is_recovered",
        "test_duplicate_judgment_keeps_the_first",
        "test_unknown_origin_and_wrong_destination",
        "test_substantive_section_recovers_without_a_second_partial",
        "test_nonzero_origin_stops_at_the_constructor_pin",
        "test_n7nn_renders_on_its_own_tail",
        "test_descriptor_states_stay_distinct",
        "test_old_records_keep_their_historical_reading",
        "test_partial_review_is_kept",
        "test_full_wording_is_preserved",
    ]
    for name in order:
        suite.addTest(ReviewLoopTests(name))
    return suite


if __name__ == "__main__":
    result = unittest.main(verbosity=2, exit=False)
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    transcript = {
        "schema": "review-loop-transcript/1",
        "runs": LOG,
    }
    (EVIDENCE / "transcript.json").write_bytes(
        json.dumps(transcript, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"
    )
    if SAMPLE["text"]:
        (EVIDENCE / "sample-review.md").write_text(SAMPLE["text"], encoding="utf-8", newline="\n")
    raise SystemExit(0 if result.result.wasSuccessful() else 1)
