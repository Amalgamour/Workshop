#!/usr/bin/env python3
"""Focused checks for the isolated constructor pass03.

Synthetic fixtures only. The predecessor constructor is imported and not edited.
prime_review is called only through the constructor's existing preview and apply
path. These tests do not run the cycle.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(r"D:\Git\lib-build")
PASS02 = ROOT / "labs" / "review-construction-pass02" / "construct.py"
PASS03 = ROOT / "labs" / "review-construction-pass03" / "construct.py"
PY = Path(sys.executable)
SECTION_KEYS = [
    "return_result",
    "prime_finding",
    "within_direction",
    "next_bounded_action",
    "for_model",
    "issue",
    "consequences",
    "options",
    "recommendation",
    "question",
    "affected",
    "proposed_plan",
    "exploration",
    "assumptions",
    "open_questions",
    "outcome_evidence",
    "limits",
    "tests_note",
    "tests_passed",
    "learning",
    "preservation",
    "remaining_choices",
    "findings_account",
    "finish_assessments",
]


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


OLD = load(PASS02, "construct_pass02")
NEW = load(PASS03, "construct_pass03")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_row(path: str, data: bytes, kind: str, identity: dict) -> dict:
    digest = sha(data)
    text = data.decode("utf-8")
    return {
        "bind": False,
        "content_bytes": len(data),
        "content_sha256": digest,
        "identity": identity,
        "kind": kind,
        "logical_path": path,
        "prior_content_sha256": None,
        "prior_transport_sha256": None,
        "record": text,
        "transport_bytes": len(data),
        "transport_sha256": digest,
    }


def sections() -> dict:
    out = {key: None for key in SECTION_KEYS}
    out["return_result"] = "SYNTHETIC return result."
    out["prime_finding"] = "SYNTHETIC finding."
    out["within_direction"] = "SYNTHETIC direction."
    out["next_bounded_action"] = "SYNTHETIC next."
    return out


def report() -> dict:
    return {
        "supplied_outcome": "continue",
        "effective": "attention",
        "finding": "sample finding",
        "supplied_semantic_conflict": False,
        "reasons": ["one reason"],
        "answers": [],
        "next_action": "look again",
        "sections": {"findings_account": None, "tests_passed": None, "tests_note": None},
        "markdown": "# Report\nbody\n",
    }


def measured() -> dict:
    return {
        "binding_sha256": "ab" * 32,
        "agreement_sha256": "cd" * 32,
        "binding": {
            "receipt": {
                "placement": "n5nn-matching-line",
                "member": "0199.synth-lab",
                "page_local": None,
                "status": "complete",
                "label": "synthetic",
                "receipt_sha256": "11" * 32,
                "return_sha256": "22" * 32,
                "manifest_sha256": "33" * 32,
            }
        },
    }


def render_spec(decisions, schema: str, supplied: dict | None) -> dict:
    return {
        "review_identity": "r1",
        "envelope_schema": schema,
        "supplied_review_state": supplied,
        "agreement": {
            "goal": "Review the synthetic copy.",
            "scope": "The synthetic copy only.",
            "prime_discretion": "Prime may replace this text.",
            "director_required": "A live review is not in this fixture.",
            "finish_criteria": None,
            "recorded_decisions": decisions,
        },
        "record": {"judgment": {"design_fork": None}},
    }


def supplied(disposition: str = "held", pass_terminal: str = "open", goal_terminal: str = "open", outcome: str = "continue") -> dict:
    return {
        "schema": "supplied-review-state/1",
        "source": "cycle decision judgment",
        "disposition": disposition,
        "pass_terminal": pass_terminal,
        "goal_terminal": goal_terminal,
        "outcome": outcome,
    }


def tree_digest(root: Path) -> list[tuple[str, str, int]]:
    rows = []
    for path in sorted(root.rglob("*")):
        if path.is_file():
            data = path.read_bytes()
            rows.append((path.relative_to(root).as_posix(), sha(data), len(data)))
    return rows


class Render(unittest.TestCase):
    def test_v1_section_matches_pass02(self) -> None:
        decision = {
            "id": "D1",
            "text": "The disposable copy was supplied for this pilot.",
            "source_sha256": "b8" * 32,
        }
        for decisions in (None, [], [decision]):
            spec = render_spec(decisions, NEW.SCHEMA_V1, None)
            old = OLD.render_review(spec, measured(), report(), "ef" * 32)
            new = NEW.render_review(spec, measured(), report(), "ef" * 32)
            self.assertEqual(old, new)
            self.assertNotIn("### Supplied review state", new)
            self.assertNotIn("source sha256", new)
            self.assertIn("recorded_decisions:\nnone supplied" if not decisions else "D1: The disposable copy was supplied for this pilot.\n", new)

    def test_v2_states_and_decision_text(self) -> None:
        text = "Director reply bytes stay verbatim: café — line."
        decision = {"id": "D7", "text": text, "source_sha256": sha(text.encode("utf-8"))}
        base = OLD.render_review(render_spec(None, NEW.SCHEMA_V1, None), measured(), report(), "ef" * 32)
        for disposition in ("held", "correction-required", "accepted"):
            state = supplied(disposition)
            rendered = NEW.render_review(render_spec(None, NEW.SCHEMA_V2, state), measured(), report(), "ef" * 32)
            self.assertIn("outcome: continue", rendered)
            self.assertIn("authority: none", rendered)
            self.assertIn(f"review_disposition (supplied): {disposition}", rendered)
            self.assertIn("pass_terminal (supplied): open", rendered)
            self.assertIn("goal_terminal (supplied): open", rendered)
            self.assertIn("It is not Director acceptance, approval, seating or authority", rendered)
            self.assertNotIn("Director accepted", rendered)
            self.assertIn("recorded_decisions:\nnone supplied", rendered)
        empty = NEW.render_review(render_spec([], NEW.SCHEMA_V2, supplied()), measured(), report(), "ef" * 32)
        self.assertIn("recorded_decisions:\nnone recorded", empty)
        kept = NEW.render_review(render_spec([decision], NEW.SCHEMA_V2, supplied("accepted", "finished", "completed", "complete")), measured(), report(), "ef" * 32)
        self.assertIn(f"- D7: {text} (source sha256 {decision['source_sha256']})", kept)
        self.assertIn("review_disposition (supplied): accepted", kept)
        self.assertTrue(base.startswith("authority: none"))
        self.assertNotIn("none recorded", base)

    def test_v2_rejects_bad_values(self) -> None:
        bad = supplied()
        bad["disposition"] = "approved"
        with self.assertRaises(NEW.Refusal) as caught:
            NEW.parse_supplied(bad)
        self.assertIn("bad supplied_review_state.disposition", caught.exception.message)
        extra = supplied()
        extra["seat"] = True
        with self.assertRaises(NEW.Refusal) as caught:
            NEW.parse_supplied(extra)
        self.assertIn("unknown key seat", caught.exception.message)
        missing = supplied()
        del missing["outcome"]
        with self.assertRaises(NEW.Refusal) as caught:
            NEW.parse_supplied(missing)
        self.assertIn("missing key outcome", caught.exception.message)
        held_finished = supplied("held", "finished", "open", "continue")
        self.assertEqual(NEW.parse_supplied(held_finished)["pass_terminal"], "finished")


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="0522-0506-"))
        self.page = (
            "# Synthetic page café\r\n\r\n"
            "## Return pointer\r\n"
            "OUTSIDE-BEFORE\r\n\r\n"
            "## Review - Codex Prime\r\n"
            "PENDING.\r\n\r\n"
            "## Notes\r\n"
            "OUTSIDE-AFTER\r\n"
        ).encode("utf-8")
        self.assignment = b"SYNTHETIC assignment for constructor pass03.\n"
        self.note = b"SYNTHETIC evidence note for constructor pass03.\n"
        self.returned = b"SYNTHETIC return bytes for constructor pass03.\n"
        self.receipt = b'{"schema":"return-capture/1","label":"synthetic"}\n'
        self.manifest = b'{"schema":"synthetic-manifest/1"}\n'
        member = self.root / "0199.synth-lab"
        member.mkdir()
        (member / "return.md").write_bytes(self.returned)
        (member / "receipt.json").write_bytes(self.receipt)
        (member / "manifest.json").write_bytes(self.manifest)
        target = self.root / "0599.synth-lab"
        target.mkdir()
        (target / "05.01.md").write_bytes(self.page)
        (self.root / "assignment.txt").write_bytes(self.assignment)
        (self.root / "note.md").write_bytes(self.note)

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def agreement(self, decisions):
        return {
            "goal": "Review the synthetic copy.",
            "scope": "The synthetic copy only.",
            "prime_discretion": "Prime may replace this text.",
            "director_required": "A live review is not in this fixture.",
            "finish_criteria": None,
            "recorded_decisions": decisions,
        }

    def record(self, decisions):
        agreement = self.agreement(decisions)
        sources = [
            source_row("assignment.txt", self.assignment, "page", {"schema": "page-bytes/1"}),
            source_row("note.md", self.note, "supplied-text", {"schema": "supplied-text/1", "label": "SYNTHETIC"}),
            source_row(
                "0199.synth-lab/return.md",
                self.returned,
                "capture",
                {
                    "schema": "return-capture/1",
                    "member": "0199.synth-lab",
                    "submission_id": "synth-0506",
                    "receipt_sha256": sha(self.receipt),
                    "origin": {"book": "00.00.10.work", "page": "0599.synth-lab", "batch": "05.01"},
                },
            ),
        ]
        return {
            "schema": "prime-review-record/1",
            "attribution": {
                "actor_label": "Grok-2 synthetic fixture",
                "role": "prime",
                "evidence": "SYNTHETIC fixture. The actor label is not authentication.",
            },
            "sources": sources,
            "agreement": agreement,
            "judgment": {
                "outcome": "continue",
                "finding": "SYNTHETIC finding for the constructor fixture.",
                "reasons": ["The fixture is synthetic."],
                "semantic_conflict": False,
                "design_fork": None,
                "next_action": "Stop after this constructor check.",
                "sections": sections(),
            },
            "holds": [],
            "answers": [],
            "review_passes": [],
            "gaps": [],
        }

    def envelope(self, decisions, version: str, state: dict | None):
        body = {
            "schema": version,
            "source_kind": "N5NN",
            "page": "00.kernel/00.00.10.work/0599.synth-lab/05.01.md",
            "pass": "05.01",
            "target": "0599.synth-lab/05.01.md",
            "expect_sha256": sha(self.page),
            "permit_create": False,
            "review_identity": "r1",
            "task": {"task_id": "synth-0506-task", "assignment_path": "assignment.txt"},
            "evidence": [{"logical_path": "note.md", "label": "synthetic"}],
            "agreement": self.agreement(decisions),
            "receipt": {
                "placement": "n5nn-matching-line",
                "member": "0199.synth-lab",
                "page_local": None,
                "submission_id": "synth-0506",
                "receipt_path": "0199.synth-lab/receipt.json",
                "return_path": "0199.synth-lab/return.md",
                "manifest_path": "0199.synth-lab/manifest.json",
                "status": "complete",
                "label": "synthetic",
            },
            "record": self.record(decisions),
        }
        if state is not None:
            body["supplied_review_state"] = state
        return body

    def write_input(self, name: str, payload: dict) -> str:
        path = self.root / name
        path.write_bytes((json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        return name

    def invoke(self, tool: Path, args: list[str]) -> subprocess.CompletedProcess:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        return subprocess.run(
            [str(PY), "-B", str(tool), *args],
            cwd=str(ROOT),
            capture_output=True,
            env=env,
        )

    def test_v1_preview_and_apply_match_pass02_and_keep_outside_bytes(self) -> None:
        rel = self.write_input("envelope.json", self.envelope(None, "review-construction/1", None))
        before = (self.root / "0599.synth-lab" / "05.01.md").read_bytes()
        old = self.invoke(PASS02, ["preview", "--fixture-root", str(self.root), "--input", rel])
        new = self.invoke(PASS03, ["preview", "--fixture-root", str(self.root), "--input", rel])
        self.assertEqual(old.returncode, 0, old.stderr)
        self.assertEqual(new.returncode, 0, new.stderr)
        self.assertEqual(old.stdout, new.stdout)
        self.assertEqual(old.stderr, b"")
        self.assertEqual(new.stderr, b"")
        self.assertEqual((self.root / "0599.synth-lab" / "05.01.md").read_bytes(), before)
        copy = Path(tempfile.mkdtemp(prefix="0522-0506-apply-"))
        other = Path(tempfile.mkdtemp(prefix="0522-0506-apply-"))
        try:
            shutil.copytree(self.root, copy, dirs_exist_ok=True)
            shutil.copytree(self.root, other, dirs_exist_ok=True)
            applied_old = self.invoke(PASS02, ["apply", "--fixture-root", str(copy), "--input", rel])
            applied_new = self.invoke(PASS03, ["apply", "--fixture-root", str(other), "--input", rel])
            self.assertEqual(applied_old.returncode, 0, applied_old.stderr)
            self.assertEqual(applied_new.returncode, 0, applied_new.stderr)
            old_page = (copy / "0599.synth-lab" / "05.01.md").read_bytes()
            new_page = (other / "0599.synth-lab" / "05.01.md").read_bytes()
            self.assertEqual(old_page, new_page)
            self.assertTrue(old_page.startswith("# Synthetic page café\r\n".encode("utf-8")))
            self.assertTrue(old_page.endswith("## Notes\r\nOUTSIDE-AFTER\r\n".encode("utf-8")))
            self.assertIn(b"OUTSIDE-BEFORE", old_page)
            shown_old = self.invoke(PASS02, ["show", "--fixture-root", str(copy), "--target", "0599.synth-lab/05.01.md"])
            shown_new = self.invoke(PASS03, ["show", "--fixture-root", str(other), "--target", "0599.synth-lab/05.01.md"])
            self.assertEqual(shown_old.stdout, shown_new.stdout)
        finally:
            shutil.rmtree(copy, ignore_errors=True)
            shutil.rmtree(other, ignore_errors=True)

    def test_bind_equality_and_source_change(self) -> None:
        rel = self.write_input("envelope.json", self.envelope(None, "review-construction/1", None))
        old = self.invoke(PASS02, ["bind", "--fixture-root", str(self.root), "--input", rel])
        new = self.invoke(PASS03, ["bind", "--fixture-root", str(self.root), "--input", rel])
        self.assertEqual(old.returncode, 0, old.stderr)
        self.assertEqual(old.stdout, new.stdout)
        v2 = self.envelope([{"id": "D7", "text": "café — kept", "source_sha256": "aa" * 32}], "review-construction/2", supplied())
        # The /1 record's agreement has recorded_decisions null. Binding equality for
        # the same semantic files uses the same agreement object.
        v2["agreement"] = self.agreement(None)
        v2["record"]["agreement"] = v2["agreement"]
        rel2 = self.write_input("envelope-v2.json", v2)
        bound = self.invoke(PASS03, ["bind", "--fixture-root", str(self.root), "--input", rel2])
        self.assertEqual(bound.returncode, 0, bound.stderr)
        self.assertEqual(json.loads(bound.stdout)["binding_sha256"], json.loads(old.stdout)["binding_sha256"])
        assignment = self.root / "assignment.txt"
        assignment.write_bytes(self.assignment + b"x")
        changed = self.invoke(PASS03, ["bind", "--fixture-root", str(self.root), "--input", rel])
        self.assertEqual(changed.returncode, 0, changed.stderr)
        self.assertNotEqual(json.loads(changed.stdout)["binding_sha256"], json.loads(old.stdout)["binding_sha256"])
        self.assertNotEqual(
            json.loads(changed.stdout)["binding"]["assignment_sha256"],
            json.loads(old.stdout)["binding"]["assignment_sha256"],
        )
        refused = self.invoke(PASS03, ["preview", "--fixture-root", str(self.root), "--input", rel])
        self.assertEqual(refused.returncode, 2)
        self.assertIn(b"assignment hash mismatch", refused.stderr)

    def test_v2_preview_keeps_outside_bytes(self) -> None:
        text = "The actual supplied sentence stays: café — end."
        decision = {"id": "D7", "text": text, "source_sha256": sha(text.encode("utf-8"))}
        payload = self.envelope([decision], "review-construction/2", supplied("correction-required"))
        rel = self.write_input("envelope-v2.json", payload)
        before = (self.root / "0599.synth-lab" / "05.01.md").read_bytes()
        proc = self.invoke(PASS03, ["preview", "--fixture-root", str(self.root), "--input", rel])
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual((self.root / "0599.synth-lab" / "05.01.md").read_bytes(), before)
        body = json.loads(proc.stdout)["review"]
        self.assertIn(f"- D7: {text} (source sha256 {decision['source_sha256']})", body)
        self.assertIn("review_disposition (supplied): correction-required", body)
        self.assertIn("authority: none", body)
        self.assertNotIn("approved", body.lower())

    def test_same_binding_is_not_permission_to_replace(self) -> None:
        page = self.root / "0599.synth-lab" / "05.01.md"
        binding = "ab" * 32
        existing = (
            "# Synthetic page café\n\n"
            "## Review - Codex Prime\n"
            "authority: none\n"
            f"task_binding: {binding}\n"
            "different judgment body\n\n"
            "## Notes\n"
            "OUTSIDE-AFTER\n"
        ).encode("utf-8")
        page.write_bytes(existing)
        payload = self.envelope(None, "review-construction/2", supplied())
        payload["expect_sha256"] = sha(existing)
        rel = self.write_input("envelope-conflict.json", payload)
        inspected = self.invoke(PASS03, ["inspect", "--fixture-root", str(self.root), "--target", "0599.synth-lab/05.01.md", "--binding", binding])
        self.assertEqual(inspected.returncode, 0, inspected.stderr)
        self.assertEqual(json.loads(inspected.stdout)["state"], "constructed-same-binding")
        preview = self.invoke(PASS03, ["preview", "--fixture-root", str(self.root), "--input", rel])
        self.assertEqual(preview.returncode, 2)
        self.assertIn(b"existing review conflicts", preview.stderr)
        self.assertEqual(page.read_bytes(), existing)
        self.assertFalse((self.root / "partial").exists())
        applied = self.invoke(PASS03, ["apply", "--fixture-root", str(self.root), "--input", rel])
        self.assertEqual(applied.returncode, 2)
        self.assertIn(b"existing review conflicts", applied.stderr)
        self.assertEqual(page.read_bytes(), existing)
        self.assertTrue((self.root / "partial").is_dir())

    def test_bad_envelope_writes_nothing(self) -> None:
        payload = self.envelope(None, "review-construction/2", supplied())
        payload["supplied_review_state"]["disposition"] = "approved"
        rel = self.write_input("bad.json", payload)
        before = tree_digest(self.root)
        proc = self.invoke(PASS03, ["bind", "--fixture-root", str(self.root), "--input", rel])
        self.assertEqual(proc.returncode, 2)
        self.assertIn(b"bad supplied_review_state.disposition", proc.stderr)
        self.assertEqual(tree_digest(self.root), before)
        v1 = self.envelope(None, "review-construction/1", None)
        v1["supplied_review_state"] = supplied()
        rel_v1 = self.write_input("bad-v1.json", v1)
        refused = self.invoke(PASS02, ["bind", "--fixture-root", str(self.root), "--input", rel_v1])
        also = self.invoke(PASS03, ["bind", "--fixture-root", str(self.root), "--input", rel_v1])
        self.assertEqual(refused.returncode, 2)
        self.assertEqual(also.returncode, 2)
        self.assertIn(b"unknown key supplied_review_state", also.stderr)


class Inspect(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="0522-0506-inspect-"))
        self.binding = "cd" * 32

    def tearDown(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)

    def write(self, rel: str, data: bytes | None) -> None:
        path = self.root / rel
        if data is None:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def classify(self, rel: str, binding: str | None = None) -> dict:
        return NEW.inspect_target(self.root, rel, binding)

    def test_shapes_newlines_and_writes_none(self) -> None:
        pending = "# x\r\n\r\n## Review - Codex Prime\r\nPENDING\r\n## Notes\r\nT\r\n".encode("utf-8")
        pending_dot = "# café\n\n## Review — Codex Prime\nPENDING.\n\n## Notes\n尾\n".encode("utf-8")
        self.write("pending.md", pending)
        self.write("dot.md", pending_dot)
        self.write("none.md", b"# x\n\n## Return pointer\nPENDING.\n")
        self.write("dup.md", b"# x\n\n## Review - Codex Prime\nPENDING.\n\n## Review - Codex Prime\nPENDING.\n")
        self.write("mixed.md", b"# x\r\n\n## Review - Codex Prime\r\nPENDING\r\n")
        self.write("bad-utf.md", b"\xff\xfe not utf-8")
        self.write("existing.md", b"# x\n\n## Review - Codex Prime\nsubstantive review\n")
        same = f"# x\n\n## Review - Codex Prime\nauthority: none\ntask_binding: {self.binding}\nother body\n".encode("utf-8")
        self.write("same.md", same)
        before = tree_digest(self.root)
        cases = {
            "missing.md": "absent",
            "pending.md": "pending",
            "dot.md": "pending",
            "none.md": "unsupported",
            "dup.md": "unsupported",
            "mixed.md": "unsupported",
            "bad-utf.md": "unsupported",
            "existing.md": "existing-review",
            "same.md": "constructed-same-binding",
        }
        for rel, state in cases.items():
            got = self.classify(rel, self.binding)
            self.assertEqual(got["state"], state, rel)
            self.assertEqual(got["schema"], "review-target-inspection/1")
        self.assertEqual(self.classify("none.md", self.binding)["rule"], "missing review heading")
        self.assertEqual(self.classify("dup.md", self.binding)["rule"], "duplicate review heading")
        self.assertIn("mixed newlines", self.classify("mixed.md", self.binding)["rule"])
        self.assertIn("not utf-8", self.classify("bad-utf.md", self.binding)["rule"])
        self.assertIsNone(self.classify("pending.md", self.binding)["rule"])
        self.assertEqual(self.classify("same.md", "ab" * 32)["state"], "existing-review")
        self.assertIn("idempotent only if the body is identical", self.classify("same.md", self.binding)["rule"])
        self.assertEqual(self.classify("dot.md", self.binding)["target_sha256"], sha(pending_dot))
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        proc = subprocess.run(
            [str(PY), "-B", str(PASS03), "inspect", "--fixture-root", str(self.root), "--target", "pending.md"],
            cwd=str(ROOT),
            capture_output=True,
            env=env,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["state"], "pending")
        self.assertEqual(tree_digest(self.root), before)
        self.assertFalse((self.root / "partial").exists())
        self.assertFalse((self.root / "support").exists())

    def test_checkout_root_is_refused(self) -> None:
        with self.assertRaises(NEW.Refusal) as caught:
            NEW.fixture_root(str(ROOT))
        self.assertIn("fixture root must stay outside", caught.exception.message)

    def test_symlink_is_refused(self) -> None:
        self.write("page.md", b"# x\n\n## Review - Codex Prime\nPENDING.\n")
        link = self.root / "link.md"
        try:
            os.symlink(self.root / "page.md", link)
        except OSError as exc:
            self.skipTest(f"symlink not created: {exc}")
        with self.assertRaises(NEW.Refusal) as caught:
            NEW.inspect_target(self.root, "link.md", None)
        self.assertIn("symlink refused", caught.exception.message)


if __name__ == "__main__":
    unittest.main(verbosity=2)
