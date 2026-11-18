#!/usr/bin/env python3
"""Disposable route tests for the review constructor. Synthetic judgment only.

Transcripts and the sample review are written under evidence/build05.02.
evidence/build05.01 stays untouched.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

ROOT = Path(r"D:\Git\lib-build")
SCRIPT = Path(__file__).resolve().parent / "construct.py"
TOOL = ROOT / "labs" / "prime-review-pass01" / "prime_review.py"
EVIDENCE = ROOT / "00.kernel" / "00.00.10.work" / "0522.review-construction" / "evidence" / "build05.02"
LOG: list[dict] = []
SAMPLE = {"text": ""}

ASSIGNMENT = b"Synthetic assignment. Write one piece.\n"
PIECE = b"synthetic piece\n"
RETURN = b"Did.\nSynthetic return.\n"
RECEIPT = b'{"schema":"synthetic-receipt/1","label":"synthetic"}\n'
MANIFEST = b'{"schema":"synthetic-manifest/1"}\n'
DISSENT = "Dissent: the minority keeps the older wording — do not smooth it."
REPLY = "Director reply: keep the synthetic piece as one file."
OPTIONAL = "Optional check encoding-probe failed. The required shape check is separate."
QUESTION = "Should the older wording stay on the record?"
HELD_QUESTION = "Should the synthetic piece stay one file?"

SECTION_KEYS = [
    "affected",
    "assumptions",
    "consequences",
    "exploration",
    "findings_account",
    "finish_assessments",
    "for_model",
    "issue",
    "learning",
    "limits",
    "next_bounded_action",
    "open_questions",
    "options",
    "outcome_evidence",
    "preservation",
    "prime_finding",
    "proposed_plan",
    "question",
    "recommendation",
    "remaining_choices",
    "return_result",
    "tests_note",
    "tests_passed",
    "within_direction",
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sections() -> dict:
    return {key: None for key in SECTION_KEYS}


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


def source_capture(path: str, data: bytes, receipt_sha: str) -> dict:
    row = source_page(path, data)
    row["kind"] = "capture"
    row["identity"] = {
        "schema": "return-capture/1",
        "member": "0199.synth-lab",
        "submission_id": "synthetic-0522",
        "receipt_sha256": receipt_sha,
        "origin": {"book": "00.00.10.work", "page": "0599.synth-lab", "batch": "05.01"},
    }
    return row


def base_record(kind: str, receipt_sha: str) -> dict:
    q_sha = sha(QUESTION.encode("utf-8"))
    held_sha = sha(HELD_QUESTION.encode("utf-8"))
    body = sections()
    body["return_result"] = "The builder returned the synthetic piece."
    body["prime_finding"] = "The synthetic piece is present."
    body["within_direction"] = "This stays inside the synthetic grant."
    body["next_bounded_action"] = "Hand back one correction pack."
    record = {
        "schema": "prime-review-record/1",
        "attribution": {
            "actor_label": "Grok-2 lab (SUPPLIED)",
            "role": "prime",
            "evidence": "SUPPLIED synthetic judgment. The label is not authentication.",
        },
        "sources": [
            source_page("assignment.txt", ASSIGNMENT),
            source_text("piece.txt", PIECE),
            source_capture("return.md", RETURN, receipt_sha),
        ],
        "agreement": agreement(),
        "holds": [],
        "answers": [],
        "review_passes": [],
        "gaps": [],
        "judgment": {
            "outcome": "continue",
            "finding": "One finding: the synthetic piece is present.",
            "reasons": ["The supplied return names the piece."],
            "semantic_conflict": False,
            "design_fork": None,
            "next_action": "Pack one bounded correction for the synthetic piece.",
            "sections": body,
        },
    }
    if kind == "full":
        body["limits"] = "Synthetic judgment. This render is not acceptance."
        body["tests_passed"] = False
        body["tests_note"] = OPTIONAL
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
        record["review_passes"] = [{
            "pass_id": "p1",
            "finding_id": "assignment.txt#F-opt",
            "review_record_sha256": sha(b"optional-check"),
            "result": "unresolved",
            "prior_pass_id": None,
            "tool_retry": False,
        }]
    elif kind == "none":
        record["judgment"]["finding"] = "No findings."
        body["prime_finding"] = "No findings."
    elif kind == "held":
        record["judgment"]["outcome"] = "director-input"
        record["judgment"]["finding"] = "Storage of the reply is unresolved."
        record["judgment"]["reasons"] = ["The example declares the choice instead of guessing it."]
        record["judgment"]["next_action"] = "Wait for a reply to the synthetic question."
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
    elif kind == "incomplete":
        record["judgment"]["outcome"] = "complete"
        record["judgment"]["finding"] = "The finish criterion is unmet."
        record["judgment"]["next_action"] = "Leave the unmet criterion visible."
        body["outcome_evidence"] = "The synthetic return is on disk."
        body["limits"] = "Synthetic judgment. This render is not acceptance."
        body["tests_note"] = "The required finish criterion was assessed unmet."
        body["tests_passed"] = False
        body["learning"] = "An unmet criterion stays open."
        body["preservation"] = "The earlier bytes stay in the fixture."
        body["remaining_choices"] = ["Whether to keep the unmet criterion open."]
        body["findings_account"] = [{"finding_id": "assignment.txt#F-01", "status": "accepted"}]
        body["finish_assessments"] = [{"criterion_id": "piece", "assessment": "unmet"}]
    else:
        raise AssertionError(kind)
    return record


def page_bytes(body: str = "PENDING.\n", crlf: bool = False) -> bytes:
    text = (
        "Intro OUTSIDE-Δ-TOKEN\n\n"
        "## Return pointer\n"
        "PENDING.\n\n"
        "## Review — Codex Prime\n"
        f"{body}"
        "## Notes\n"
        "TAIL-Δ-TOKEN\n"
    )
    data = text.encode("utf-8")
    if crlf:
        data = data.replace(b"\n", b"\r\n")
    return data


class World:
    def __init__(self, kind: str = "full", body: str = "PENDING.\n", crlf: bool = False, create: bool = False):
        self.root = Path(tempfile.mkdtemp(prefix="reviewconstr-"))
        self.page = self.root / "0599.synth-lab" / "05.01.md"
        self.page.parent.mkdir(parents=True)
        (self.root / "assignment.txt").write_bytes(ASSIGNMENT)
        (self.root / "piece.txt").write_bytes(PIECE)
        (self.root / "return.md").write_bytes(RETURN)
        (self.root / "receipt.json").write_bytes(RECEIPT)
        (self.root / "manifest.json").write_bytes(MANIFEST)
        self.record = base_record(kind, sha(RECEIPT))
        self.envelope = {
            "schema": "review-construction/1",
            "source_kind": "N5NN",
            "page": "00.kernel/00.00.10.work/0599.synth-lab/05.01.md",
            "pass": "05.01",
            "target": "0599.synth-lab/05.01.md",
            "expect_sha256": "absent",
            "permit_create": False,
            "review_identity": "r1",
            "task": {"task_id": "synth-task", "assignment_path": "assignment.txt"},
            "evidence": [{"logical_path": "piece.txt", "label": "synthetic"}],
            "agreement": agreement(),
            "receipt": {
                "placement": "n5nn-matching-line",
                "member": "0199.synth-lab",
                "page_local": None,
                "submission_id": "synthetic-0522",
                "receipt_path": "receipt.json",
                "return_path": "return.md",
                "manifest_path": "manifest.json",
                "status": "complete",
                "label": "synthetic",
            },
            "record": self.record,
        }
        if not create:
            blob = page_bytes(body, crlf)
            self.page.write_bytes(blob)
            self.envelope["expect_sha256"] = sha(blob)
        self.save()

    def save(self) -> None:
        (self.root / "input.json").write_text(
            json.dumps(self.envelope, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def close(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)


def run(name: str, args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, "-B", str(SCRIPT), *args],
        cwd=str(ROOT),
        capture_output=True,
        env=env,
    )
    LOG.append({
        "name": name,
        "args": args[0],
        "exit": proc.returncode,
        "stdout": proc.stdout.decode("utf-8", errors="replace"),
        "stderr": proc.stderr.decode("utf-8", errors="replace"),
    })
    return proc


def as_json(proc: subprocess.CompletedProcess) -> dict:
    if proc.returncode != 0:
        raise AssertionError(proc.stderr.decode("utf-8", errors="replace"))
    return json.loads(proc.stdout.decode("utf-8"))


def refused(proc: subprocess.CompletedProcess, fragment: str) -> str:
    err = proc.stderr.decode("utf-8", errors="replace")
    if proc.returncode != 2 or fragment not in err or not err.startswith("refused:"):
        raise AssertionError(f"exit {proc.returncode}\n{err}\n{proc.stdout.decode('utf-8', errors='replace')[:400]}")
    return err


def point_n5(world: World, page_id: str, pass_id: str = "05.01") -> str:
    head, subject = page_id.split(".", 1)
    member = f"{head[0]}1{head[2:]}.{subject}"
    world.envelope["source_kind"] = "N5NN"
    world.envelope["page"] = f"00.kernel/00.00.10.work/{page_id}/{pass_id}.md"
    world.envelope["pass"] = pass_id
    world.envelope["target"] = f"{page_id}/{pass_id}.md"
    world.envelope["receipt"]["placement"] = "n5nn-matching-line"
    world.envelope["receipt"]["member"] = member
    world.envelope["receipt"]["page_local"] = None
    identity = world.envelope["record"]["sources"][2]["identity"]
    identity["member"] = member
    identity["origin"] = {"book": "00.00.10.work", "page": page_id, "batch": pass_id}
    return member


def point_n7(world: World, page_id: str, pass_id: str = "05.01") -> None:
    tail = pass_id.split(".", 1)[1]
    world.envelope["source_kind"] = "N7NN"
    world.envelope["page"] = f"00.kernel/00.00.10.work/{page_id}/{pass_id}.pack.md"
    world.envelope["pass"] = pass_id
    world.envelope["target"] = f"{page_id}/06.{tail}.review.md"
    world.envelope["receipt"]["placement"] = "n7nn-page-local"
    world.envelope["receipt"]["member"] = None
    world.envelope["receipt"]["page_local"] = f"05.{tail}.return.md"
    world.envelope["record"]["sources"][2] = source_text("return.md", RETURN)


def place_page(world: World, page_id: str, pass_id: str = "05.01") -> bytes:
    blob = page_bytes()
    path = world.root / page_id / f"{pass_id}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(blob)
    world.page = path
    world.envelope["expect_sha256"] = sha(blob)
    return blob


def edges(blob: bytes) -> tuple[bytes, bytes]:
    head = "## Review — Codex Prime".encode("utf-8")
    start = blob.index(head)
    newline = b"\r\n" if blob.startswith(b"Intro") and b"\r\n" in blob[:80] else b"\n"
    prefix = blob[: start + len(head) + len(newline)]
    suffix = blob[blob.index(b"## Notes") :]
    return prefix, suffix


class ConstructorTest(unittest.TestCase):
    def test_full_review_preserves_outside_bytes_and_binding(self) -> None:
        world = World("full")
        try:
            before = world.page.read_bytes()
            prefix, suffix = edges(before)
            preview = as_json(run("preview-full", ["preview", "--fixture-root", str(world.root), "--input", "input.json"]))
            self.assertEqual(preview["result"], "preview")
            self.assertFalse(preview["written"])
            self.assertEqual(world.page.read_bytes(), before)
            self.assertFalse((world.root / "support").exists())
            bound = as_json(run("bind-before", ["bind", "--fixture-root", str(world.root), "--input", "input.json"]))
            self.assertFalse(bound["target_read"])
            self.assertEqual(bound["schema"], "review-task-binding/2")
            self.assertEqual(bound["binding"]["schema"], "review-task-binding/2")
            self.assertEqual(bound["binding"]["source"], {
                "book": "00.00.10.work",
                "page": "0599.synth-lab",
                "pass": "05.01",
            })
            self.assertEqual(bound["binding"]["assignment_path"], "assignment.txt")
            self.assertEqual(bound["binding"]["receipt"]["member"], "0199.synth-lab")
            applied = as_json(run("apply-full", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]))
            after = world.page.read_bytes()
            self.assertEqual(applied["result"], "applied")
            self.assertTrue(applied["written"])
            self.assertEqual(applied["prime_review_exit"], 0)
            self.assertEqual(applied["effective"], "continue")
            self.assertEqual(applied["custody"], "not-established")
            self.assertFalse(applied["allocated"])
            self.assertEqual(applied["binding_sha256"], bound["binding_sha256"])
            self.assertNotEqual(applied["target_sha256_before"], applied["target_sha256_after"])
            self.assertEqual(sha(after), applied["target_sha256_after"])
            self.assertTrue(after.startswith(prefix))
            self.assertTrue(after.endswith(suffix))
            self.assertIn(b"OUTSIDE-\xce\x94-TOKEN", prefix)
            self.assertIn(b"TAIL-\xce\x94-TOKEN", suffix)
            review = applied["review"]
            for fragment in (DISSENT, REPLY, OPTIONAL, "tests_passed: false", "assignment.txt#F-01 accepted", "No findings."):
                if fragment == "No findings.":
                    self.assertNotIn(fragment, review)
                else:
                    self.assertIn(fragment, review)
            self.assertIn("authority: none", review)
            self.assertIn("closes_work: false", review)
            self.assertIn("This line is not a release.", review)
            self.assertIn(applied["binding_sha256"], review)
            self.assertIn("member: 0199.synth-lab", review)
            self.assertNotIn(applied["target_sha256_before"], review)
            record = (world.root / "support" / "r1" / "record.json").read_bytes()
            self.assertEqual(sha(record), applied["record_sha256"])
            stored = json.loads((world.root / "support" / "r1" / "binding.json").read_text(encoding="utf-8"))
            self.assertEqual(stored["schema"], "review-task-binding/2")
            self.assertEqual(stored["binding"]["source"]["page"], "0599.synth-lab")
            self.assertFalse(stored["target_read"])
            self.assertFalse((world.page.name + ".review-construct.tmp") in os.listdir(world.page.parent))
            SAMPLE["text"] = review
            world.envelope["expect_sha256"] = applied["target_sha256_after"]
            world.save()
            again = as_json(run("replay", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]))
            self.assertEqual(again["result"], "idempotent")
            self.assertFalse(again["written"])
            self.assertEqual(world.page.read_bytes(), after)
            self.assertEqual(again["binding_sha256"], bound["binding_sha256"])
            world.envelope["expect_sha256"] = applied["target_sha256_before"]
            world.save()
            stale = run("stale-after", ["apply", "--fixture-root", str(world.root), "--input", "input.json"])
            refused(stale, "is not the expected")
            self.assertEqual(world.page.read_bytes(), after)
            shown = as_json(run("show", ["show", "--fixture-root", str(world.root), "--target", "0599.synth-lab/05.01.md"]))
            self.assertEqual(shown["binding_sha256"], bound["binding_sha256"])
            self.assertIn(REPLY, shown["section"])
            self.assertIn(DISSENT, shown["section"])
        finally:
            world.close()

    def test_binding_changes_for_task_evidence_agreement_and_receipt_only(self) -> None:
        world = World("full")
        try:
            first = as_json(run("bind-base", ["bind", "--fixture-root", str(world.root), "--input", "input.json"]))
            base = first["binding_sha256"]
            judged = deepcopy(world.envelope)
            judged["record"]["judgment"]["finding"] = "A different supplied finding."
            (world.root / "input.json").write_text(json.dumps(judged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            changed_judgment = as_json(run("bind-judgment", ["bind", "--fixture-root", str(world.root), "--input", "input.json"]))
            self.assertEqual(changed_judgment["binding_sha256"], base)
            self.assertEqual(changed_judgment["binding"]["source"], first["binding"]["source"])
            world.save()
            (world.root / "assignment.txt").write_bytes(ASSIGNMENT + b"changed\n")
            task = as_json(run("bind-task", ["bind", "--fixture-root", str(world.root), "--input", "input.json"]))
            self.assertNotEqual(task["binding_sha256"], base)
            (world.root / "assignment.txt").write_bytes(ASSIGNMENT)
            (world.root / "piece.txt").write_bytes(PIECE + b"changed\n")
            evidence = as_json(run("bind-evidence", ["bind", "--fixture-root", str(world.root), "--input", "input.json"]))
            self.assertNotEqual(evidence["binding_sha256"], base)
            (world.root / "piece.txt").write_bytes(PIECE)
            agreed = deepcopy(world.envelope)
            agreed["agreement"]["goal"] = "A different synthetic goal."
            agreed["record"]["agreement"]["goal"] = agreed["agreement"]["goal"]
            (world.root / "input.json").write_text(json.dumps(agreed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            agreement_row = as_json(run("bind-agreement", ["bind", "--fixture-root", str(world.root), "--input", "input.json"]))
            self.assertNotEqual(agreement_row["binding_sha256"], base)
            world.save()
            (world.root / "receipt.json").write_bytes(RECEIPT + b"changed\n")
            receipt = as_json(run("bind-receipt", ["bind", "--fixture-root", str(world.root), "--input", "input.json"]))
            self.assertNotEqual(receipt["binding_sha256"], base)
        finally:
            world.close()

    def test_no_findings_held_and_incomplete_render(self) -> None:
        for kind, effective, code, fragment in (
            ("none", "continue", 0, "No findings."),
            ("held", "hold", 1, HELD_QUESTION),
            ("incomplete", "not-closed", 1, "finish criterion unmet"),
        ):
            world = World(kind)
            try:
                applied = as_json(run(f"apply-{kind}", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]))
                self.assertEqual(applied["effective"], effective)
                self.assertEqual(applied["prime_review_exit"], code)
                self.assertTrue(applied["written"])
                self.assertIn(fragment, applied["review"])
                if kind == "none":
                    self.assertIn("Findings account: none supplied", applied["review"])
                    self.assertIn("### Dissent\nnone supplied", applied["review"])
                    self.assertIn("### Director replies\nnone supplied", applied["review"])
                if kind == "held":
                    self.assertIn("status unresolved", applied["review"])
                    self.assertNotIn(REPLY, applied["review"])
            finally:
                world.close()

    def test_refusals_leave_the_target_unchanged(self) -> None:
        world = World("full")
        try:
            original = world.page.read_bytes()
            missing = deepcopy(world.envelope)
            del missing["agreement"]
            (world.root / "input.json").write_text(json.dumps(missing) + "\n", encoding="utf-8")
            refused(run("missing-field", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "missing key agreement")
            unknown = deepcopy(world.envelope)
            unknown["custody_ok"] = True
            (world.root / "input.json").write_text(json.dumps(unknown) + "\n", encoding="utf-8")
            refused(run("unknown-field", ["preview", "--fixture-root", str(world.root), "--input", "input.json"]), "unknown key custody_ok")
            mismatch = deepcopy(world.envelope)
            mismatch["record"]["sources"][2]["identity"]["receipt_sha256"] = "0" * 64
            (world.root / "input.json").write_text(json.dumps(mismatch) + "\n", encoding="utf-8")
            refused(run("receipt-mismatch", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "receipt hash mismatch")
            bad_record = deepcopy(world.envelope)
            del bad_record["record"]["judgment"]["finding"]
            (world.root / "input.json").write_text(json.dumps(bad_record) + "\n", encoding="utf-8")
            refused(run("missing-judgment", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "missing key finding")
            self.assertEqual(world.page.read_bytes(), original)
            self.assertFalse((world.root / "support").exists())
        finally:
            world.close()

    def test_heading_hash_and_conflict(self) -> None:
        world = World("full")
        try:
            original = world.page.read_bytes()
            world.envelope["pass"] = "05.02"
            world.save()
            refused(run("wrong-pass", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "pass does not match page")
            world.envelope["pass"] = "05.01"
            world.envelope["page"] = "00.kernel/00.00.10.work/0122.review-construction/05.01.md"
            world.save()
            refused(run("wrong-page", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "page does not match N5NN")
            world.envelope["page"] = "00.kernel/00.00.10.work/0599.synth-lab/05.01.md"
            world.envelope["expect_sha256"] = "ab" * 32
            world.save()
            refused(run("stale-hash", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "is not the expected")
            self.assertEqual(world.page.read_bytes(), original)
            self.assertFalse((world.root / "support").exists())
            duplicate = original.replace(
                b"## Notes\n",
                "## Review — Codex Prime\nPENDING.\n## Notes\n".encode("utf-8"),
                1,
            )
            world.page.write_bytes(duplicate)
            world.envelope["expect_sha256"] = sha(duplicate)
            world.save()
            refused(run("duplicate-heading", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "duplicate review heading")
            self.assertEqual(world.page.read_bytes(), duplicate)
            missing_head = b"Intro only\n## Notes\nTAIL\n"
            world.page.write_bytes(missing_head)
            world.envelope["expect_sha256"] = sha(missing_head)
            world.save()
            refused(run("missing-heading", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "missing review heading")
            conflict = page_bytes("Earlier substantive review.\n")
            world.page.write_bytes(conflict)
            world.envelope["expect_sha256"] = sha(conflict)
            world.save()
            err = refused(run("conflict", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "successor process is required")
            self.assertIn("partial evidence:", err)
            self.assertEqual(world.page.read_bytes(), conflict)
            partials = list((world.root / "partial").glob("*.md"))
            self.assertEqual(len(partials), 1)
            self.assertIn(DISSENT, partials[0].read_text(encoding="utf-8"))
            refused(run("conflict-preview", ["preview", "--fixture-root", str(world.root), "--input", "input.json"]), "successor process is required")
            self.assertEqual(len(list((world.root / "partial").glob("*.md"))), 1)
            self.assertFalse((world.root / "support").exists())
        finally:
            world.close()

    def test_line_endings_and_unicode_refusal(self) -> None:
        world = World("full", crlf=True)
        try:
            before = world.page.read_bytes()
            prefix, suffix = edges(before)
            applied = as_json(run("apply-crlf", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]))
            after = world.page.read_bytes()
            self.assertTrue(after.startswith(prefix))
            self.assertTrue(after.endswith(suffix))
            self.assertNotIn(b"\n", after.replace(b"\r\n", b""))
            self.assertIn(DISSENT.encode("utf-8"), after)
            self.assertEqual(applied["binding_sha256"], as_json(run("bind-crlf", ["bind", "--fixture-root", str(world.root), "--input", "input.json"]))["binding_sha256"])
        finally:
            world.close()
        world = World("full")
        try:
            mixed = world.page.read_bytes().replace(b"TAIL-\xce\x94-TOKEN\n", b"TAIL-\xce\x94-TOKEN\r\n")
            world.page.write_bytes(mixed)
            world.envelope["expect_sha256"] = sha(mixed)
            world.save()
            refused(run("mixed-newlines", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "mixed newlines")
            self.assertEqual(world.page.read_bytes(), mixed)
            bad = b"## Review - Codex Prime\nPENDING.\n\xff"
            world.page.write_bytes(bad)
            world.envelope["expect_sha256"] = sha(bad)
            world.save()
            refused(run("bad-utf8", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "not utf-8")
            self.assertEqual(world.page.read_bytes(), bad)
        finally:
            world.close()

    def test_create_n5_and_n7_and_refuse_other_kinds(self) -> None:
        world = World("full", create=True)
        try:
            refused(run("create-without-permission", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "permit_create")
            self.assertFalse(world.page.exists())
            world.envelope["permit_create"] = True
            world.save()
            created = as_json(run("create-n5", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]))
            blob = world.page.read_bytes()
            self.assertTrue(blob.startswith("## Review — Codex Prime\n".encode("utf-8")))
            self.assertNotIn(b"Synthetic assignment. Write one piece.", blob)
            self.assertEqual(created["result"], "applied")
            self.assertEqual(created["race_limitation"], RACE)
        finally:
            world.close()
        world = World("none", create=True)
        try:
            world.envelope["source_kind"] = "N7NN"
            world.envelope["page"] = "00.kernel/00.00.10.work/0799.synth-colab/05.01.pack.md"
            world.envelope["target"] = "0799.synth-colab/06.01.review.md"
            world.envelope["permit_create"] = True
            world.envelope["receipt"]["placement"] = "n7nn-page-local"
            world.envelope["receipt"]["member"] = None
            world.envelope["receipt"]["page_local"] = "05.01.return.md"
            world.record["sources"][2] = source_text("return.md", RETURN)
            world.save()
            applied = as_json(run("create-n7", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]))
            self.assertIsNone(applied["member"])
            self.assertFalse(applied["allocated"])
            self.assertEqual(applied["placement"], "n7nn-page-local")
            text = (world.root / "0799.synth-colab" / "06.01.review.md").read_text(encoding="utf-8")
            self.assertNotIn("0199.synthetic-review", text)
            self.assertNotIn("0199.synth-lab", text)
            self.assertNotIn("0122.review-construction", text)
            self.assertIn("No findings.", text)
            world.envelope["source_kind"] = "N6NN"
            world.save()
            refused(run("kind-n6", ["preview", "--fixture-root", str(world.root), "--input", "input.json"]), "unsupported source kind N6NN")
            world.envelope["source_kind"] = "N1NN"
            world.save()
            refused(run("kind-n1", ["preview", "--fixture-root", str(world.root), "--input", "input.json"]), "unsupported source kind N1NN")
        finally:
            world.close()

    def test_live_checkout_and_pins_are_untouched(self) -> None:
        tool_before = sha(TOOL.read_bytes())
        self.assertEqual(tool_before, "805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0")
        self.assertEqual(TOOL.stat().st_size, 58324)
        source = SCRIPT.read_text(encoding="utf-8")
        for banned in ("return-placement", "return_capture", "return_inspect", "prime_cycle", "desk_lab"):
            self.assertNotIn(banned, source)
        proc = run("live-root", ["preview", "--fixture-root", str(ROOT), "--input", "input.json"])
        refused(proc, "outside D:\\Git\\lib-build")
        self.assertEqual(sha(TOOL.read_bytes()), tool_before)
        work = ROOT / "00.kernel" / "00.00.10.work"
        for name in ("0199.synthetic-review", "0199.synth-lab", "1199.synth-lab", "0188.unrelated-subject"):
            self.assertFalse((work / name).exists(), name)

    def test_wrong_target_page_is_refused(self) -> None:
        world = World("none")
        try:
            original = world.page.read_bytes()
            wrong = world.root / "0588.wrong-page" / "05.01.md"
            wrong.parent.mkdir()
            wrong.write_bytes(original)
            world.envelope["target"] = "0588.wrong-page/05.01.md"
            world.save()
            refused(run("wrong-target", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "target is not the derived review destination")
            self.assertEqual(world.page.read_bytes(), original)
            self.assertEqual(wrong.read_bytes(), original)
            self.assertFalse((world.root / "support").exists())
            self.assertFalse((world.root / "partial").exists())
        finally:
            world.close()
        world = World("none", create=True)
        try:
            point_n7(world, "0799.synth-colab")
            world.envelope["target"] = "0788.wrong-page/06.01.review.md"
            world.envelope["permit_create"] = True
            world.envelope["expect_sha256"] = "absent"
            world.save()
            wrong = world.root / "0788.wrong-page" / "06.01.review.md"
            wrong.parent.mkdir(parents=True)
            marker = b"WRONG-PAGE-MARKER\n"
            wrong.write_bytes(marker)
            refused(run("wrong-target-n7", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "target is not the derived review destination")
            self.assertEqual(wrong.read_bytes(), marker)
            self.assertFalse((world.root / "0799.synth-colab" / "06.01.review.md").exists())
            self.assertFalse((world.root / "support").exists())
        finally:
            world.close()

    def test_wrong_return_line_and_subject_are_refused(self) -> None:
        world = World("none")
        try:
            original = world.page.read_bytes()
            world.envelope["receipt"]["member"] = "0188.unrelated-subject"
            world.envelope["record"]["sources"][2]["identity"]["member"] = "0188.unrelated-subject"
            world.save()
            refused(run("wrong-return-line", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "member is not the derived matching line")
            self.assertEqual(world.page.read_bytes(), original)
            self.assertFalse((world.root / "support").exists())
            world.envelope["receipt"]["member"] = "0199.synth-lab"
            world.envelope["record"]["sources"][2]["identity"]["member"] = "0199.other-subject"
            world.save()
            refused(run("wrong-capture-member", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "capture member is not the derived matching line")
            self.assertEqual(world.page.read_bytes(), original)
            self.assertFalse((world.root / "support").exists())
        finally:
            world.close()
        world = World("none")
        try:
            original = world.page.read_bytes()
            world.envelope["receipt"]["member"] = "0199.other-subject"
            world.envelope["record"]["sources"][2]["identity"]["member"] = "0199.other-subject"
            world.save()
            refused(run("wrong-same-nn-subject", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "member is not the derived matching line")
            self.assertEqual(world.page.read_bytes(), original)
            self.assertFalse((world.root / "support").exists())
            self.assertFalse((world.root / "partial").exists())
        finally:
            world.close()

    def test_wrong_typed_origin_is_refused(self) -> None:
        cases = (
            ("origin-page", "page", "0588.wrong-page"),
            ("origin-book", "book", "00.00.99.other"),
            ("origin-batch", "batch", "05.02"),
        )
        for name, key, value in cases:
            world = World("none")
            try:
                original = world.page.read_bytes()
                world.envelope["record"]["sources"][2]["identity"]["origin"][key] = value
                world.save()
                refused(run(name, ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "origin does not match the source")
                self.assertEqual(world.page.read_bytes(), original)
                self.assertFalse((world.root / "support").exists())
            finally:
                world.close()
        world = World("none")
        try:
            original = world.page.read_bytes()
            del world.envelope["record"]["sources"][2]["identity"]["origin"]
            world.save()
            refused(run("origin-missing", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "origin does not match the source")
            self.assertEqual(world.page.read_bytes(), original)
            self.assertFalse((world.root / "support").exists())
        finally:
            world.close()

    def test_nonzero_workflow_space(self) -> None:
        world = World("none", create=True)
        try:
            point_n7(world, "1799.synth-colab")
            world.envelope["permit_create"] = True
            world.save()
            applied = as_json(run("apply-n7-nonzero", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]))
            self.assertEqual(applied["result"], "applied")
            self.assertIsNone(applied["member"])
            self.assertEqual(applied["placement"], "n7nn-page-local")
            text = (world.root / "1799.synth-colab" / "06.01.review.md").read_text(encoding="utf-8")
            self.assertIn("No findings.", text)
            self.assertNotIn("0199.synth-lab", text)
            bound = as_json(run("bind-n7-nonzero", ["bind", "--fixture-root", str(world.root), "--input", "input.json"]))
            self.assertEqual(bound["binding"]["source"]["page"], "1799.synth-colab")
            self.assertEqual(bound["binding_sha256"], applied["binding_sha256"])
            self.assertIsNone(bound["binding"]["receipt"]["member"])
        finally:
            world.close()
        world = World("none")
        try:
            kept = world.page
            kept_bytes = kept.read_bytes()
            point_n5(world, "1599.synth-lab")
            blob = place_page(world, "1599.synth-lab")
            world.save()
            bound = as_json(run("bind-n5-nonzero", ["bind", "--fixture-root", str(world.root), "--input", "input.json"]))
            self.assertEqual(bound["binding"]["source"], {
                "book": "00.00.10.work",
                "page": "1599.synth-lab",
                "pass": "05.01",
            })
            self.assertEqual(bound["binding"]["receipt"]["member"], "1199.synth-lab")
            self.assertEqual(bound["binding"]["assignment_path"], "assignment.txt")
            preview = run("preview-n5-nonzero", ["preview", "--fixture-root", str(world.root), "--input", "input.json"])
            err = refused(preview, "bad member")
            self.assertNotIn("page does not match N5NN", err)
            applied = run("apply-n5-nonzero", ["apply", "--fixture-root", str(world.root), "--input", "input.json"])
            refused(applied, "bad member")
            self.assertEqual(world.page.read_bytes(), blob)
            self.assertEqual(kept.read_bytes(), kept_bytes)
            self.assertFalse((world.root / "support").exists())
            self.assertFalse((world.root / "partial").exists())
        finally:
            world.close()

    def test_same_task_text_at_two_sources(self) -> None:
        world = World("none")
        try:
            first = as_json(run("bind-source-a", ["bind", "--fixture-root", str(world.root), "--input", "input.json"]))
            point_n5(world, "0588.synth-lab")
            world.save()
            second = as_json(run("bind-source-b", ["bind", "--fixture-root", str(world.root), "--input", "input.json"]))
            self.assertNotEqual(first["binding_sha256"], second["binding_sha256"])
            self.assertEqual(first["binding"]["assignment_sha256"], second["binding"]["assignment_sha256"])
            self.assertEqual(first["binding"]["source"]["page"], "0599.synth-lab")
            self.assertEqual(second["binding"]["source"]["page"], "0588.synth-lab")
            self.assertEqual(second["binding"]["receipt"]["member"], "0188.synth-lab")
            self.assertEqual(first["binding"]["task_id"], second["binding"]["task_id"])
            (world.root / "task").mkdir()
            (world.root / "task" / "assignment.txt").write_bytes(ASSIGNMENT)
            world.envelope["task"]["assignment_path"] = "task/assignment.txt"
            world.envelope["record"]["sources"][0]["logical_path"] = "task/assignment.txt"
            world.save()
            third = as_json(run("bind-assignment-path", ["bind", "--fixture-root", str(world.root), "--input", "input.json"]))
            self.assertNotEqual(third["binding_sha256"], second["binding_sha256"])
            self.assertEqual(third["binding"]["assignment_sha256"], second["binding"]["assignment_sha256"])
            self.assertEqual(third["binding"]["assignment_path"], "task/assignment.txt")
            self.assertEqual(third["binding"]["source"]["page"], "0588.synth-lab")
        finally:
            world.close()

    def test_old_binding_preimage_is_not_replaced(self) -> None:
        world = World("none")
        try:
            original = world.page.read_bytes()
            folder = world.root / "support" / "r1"
            folder.mkdir(parents=True)
            record = folder / "record.json"
            binding = folder / "binding.json"
            record.write_bytes(b'{"schema":"review-task-binding/1"}\n')
            binding.write_bytes(b'{"schema":"review-task-binding/1","binding_sha256":"00"}\n')
            before_record = record.read_bytes()
            before_binding = binding.read_bytes()
            refused(run("old-binding", ["apply", "--fixture-root", str(world.root), "--input", "input.json"]), "support record conflicts")
            self.assertEqual(world.page.read_bytes(), original)
            self.assertEqual(record.read_bytes(), before_record)
            self.assertEqual(binding.read_bytes(), before_binding)
        finally:
            world.close()

    def test_sealed_prior_evidence_stays(self) -> None:
        sealed = {
            "00.kernel/00.00.10.work/0522.review-construction/05.01.md": ("41ca788e4516ddf58270d47f6b0405e775e7d79ef1431bc9c63bdb27a553833a", 10349),
            "00.kernel/00.00.10.work/0522.review-construction/06.01.md": ("0b64cb61b6095c2e3e7f7e86d92b480abf349736b08b2c6c520217feafb98abb", 4553),
            "00.kernel/00.00.10.work/0522.review-construction/06.02.md": ("27ca699ca9839e1f030e8a48794c122b26bb204a71612d890b805884376adea1", 445),
            "00.kernel/00.00.10.work/0522.review-construction/evidence/build05.01/CONTRACT.md": ("c50f75c9c66cca7430eed671aa6cc2a69aa163b3a6fc4ea4d710f4886f792fc5", 8319),
            "00.kernel/00.00.10.work/0522.review-construction/evidence/build05.01/INTEGRATION.md": ("fa2a5df906097dd304a5f0a05e0532aaea08719f56dd193b4b316e640310dba0", 3642),
            "00.kernel/00.00.10.work/0522.review-construction/evidence/build05.01/artifact-manifest.json": ("4f781fa9d520378bff1f3fb858a036316a2843be5e471b33625327acf812ac37", 2222),
            "00.kernel/00.00.10.work/0522.review-construction/evidence/build05.01/submission.md": ("22ffb265d6e4c205013fd2942c0ea38902fd1a50aee03dfcb27c32eb4af9f10f", 2217),
            "00.kernel/00.00.10.work/0522.review-construction/evidence/build05.01/sample-review.md": ("a9e7afd376aa0996de6f06101597e3b307787a7906f371a2d0fe2a91561cde72", 4413),
            "00.kernel/00.00.10.work/0522.review-construction/evidence/build05.01/transcript.json": ("85c5ea990fe16ff5b8dc86a48bfe86807857b1440c617463f9e0b29256bfcdfb", 70457),
            "00.kernel/00.00.10.work/0522.review-construction/evidence/build05.01/verification.json": ("d0fe2237654f0feb9f1cc67042f3cadf5159ca78c27bf00221e917222c3ded62", 4392),
            "00.kernel/00.00.10.work/0522.review-construction/evidence/prime-review05.01/REVIEW.md": ("a847ab26f0b505dfcfd57e9dc12efa4994cff5cbe3da83e8a16997ec9f0b57bb", 3447),
            "00.kernel/00.00.10.work/0522.review-construction/evidence/prime-review05.01/independent-checks/probes.json": ("8774b8cf677e740247de74458d59e0cce057d6e20b680e9572e3601d838883b4", 9944),
            "labs/prime-review-pass01/prime_review.py": ("805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0", 58324),
        }
        for rel, (digest, size) in sealed.items():
            blob = (ROOT / rel).read_bytes()
            self.assertEqual(len(blob), size, rel)
            self.assertEqual(sha(blob), digest, rel)

    @classmethod
    def tearDownClass(cls) -> None:
        EVIDENCE.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema": "review-construction-transcript/1",
            "runs": LOG,
        }
        (EVIDENCE / "transcript.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        if SAMPLE["text"]:
            (EVIDENCE / "sample-review.md").write_text(SAMPLE["text"], encoding="utf-8")


RACE = "compare-then-rename narrows a stale write and is not proof of race freedom"


if __name__ == "__main__":
    unittest.main(verbosity=2)
