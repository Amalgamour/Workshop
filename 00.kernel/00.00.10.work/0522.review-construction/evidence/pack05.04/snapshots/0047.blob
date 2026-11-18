"""Tests for the Prime review draft and declared-hold guard."""

from __future__ import annotations

import hashlib
import io
import json
import os
import stat
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
REPO = Path(r"D:\Git\lib-build")
sys.path.insert(0, str(LAB))
import prime_review  # noqa: E402

PAGE = "notes/page.md"
FINDING = "notes/page.md#F-01"
QUOTE = 'Director said "fresh claude is running" then "Good, the prime test is done."'
PROMPT = "Apply only the granted typo correction and return the page."
SECRET = "EXECUTABLE-FOLLOWUP-DO-NOT-COPY"


def digest(text: str) -> tuple[str, int]:
    data = text.encode("utf-8")
    return hashlib.sha256(data).hexdigest(), len(data)


def source(text: str = "Routine page note. The builder corrected a typo inside the granted pack.\n", path: str = PAGE, **updates) -> dict:
    content, size = digest(text)
    raw = {
        "kind": "page",
        "logical_path": path,
        "content_sha256": content,
        "content_bytes": size,
        "transport_sha256": content,
        "transport_bytes": size,
        "prior_content_sha256": None,
        "prior_transport_sha256": None,
        "record": text,
        "bind": False,
        "identity": {"schema": "page-bytes/1"},
    }
    raw.update(updates)
    return raw


def blank_sections() -> dict:
    return {key: None for key in prime_review.SECTION_KEYS}


def agreement(**updates) -> dict:
    content, _size = digest("grant")
    raw = {
        "goal": "Correct the typo inside the granted page.",
        "scope": "The granted pack page only.",
        "prime_discretion": "Prime may accept a wording repair inside that grant.",
        "director_required": "A design change is not in this grant.",
        "finish_criteria": [{"id": "typo", "text": "The granted typo is corrected."}],
        "recorded_decisions": [{
            "id": "D1",
            "text": "The pack was released for this repair.",
            "source_sha256": content,
        }],
    }
    raw.update(updates)
    return raw


def record(**updates) -> dict:
    sections = blank_sections()
    sections.update({
        "return_result": "The builder returned the corrected page.",
        "prime_finding": "The correction stays inside the granted wording repair.",
        "within_direction": "This is a routine repair inside the existing grant.",
        "next_bounded_action": "Hand the corrected page back for the next pack pass.",
        "for_model": {"model": "builder", "prompt": PROMPT},
    })
    raw = {
        "schema": "prime-review-record/1",
        "attribution": {
            "actor_label": "Codex Prime",
            "role": "prime",
            "evidence": "SUPPLIED EXAMPLE. The label is not authentication.",
        },
        "sources": [source()],
        "agreement": agreement(),
        "judgment": {
            "outcome": "continue",
            "finding": "The correction stays inside the granted wording repair.",
            "reasons": ["The change is the typo named in the grant."],
            "semantic_conflict": False,
            "design_fork": None,
            "next_action": "Return the corrected page on the next pack pass.",
            "sections": sections,
        },
        "holds": [],
        "answers": [],
        "review_passes": [],
        "gaps": [],
    }
    raw.update(updates)
    return raw


def run_report(body: dict, root: Path | None = None):
    return prime_review.report_from_bytes(json.dumps(body).encode("utf-8"), root)


def run_guard(body: dict, action_id: str, authorized=True, label="Check the named action"):
    payload = {
        "schema": "prime-review-guard/1",
        "review": body,
        "proposed_action": {
            "action_id": action_id,
            "label": label,
            "grant_ref": "the grant already on the work page",
            "authorized_in_grant": authorized,
        },
    }
    return prime_review.guard_from_bytes(json.dumps(payload).encode("utf-8"), None)


def hold(action: str, kind: str = "director-judgment", question: str | None = None, revision: str = "r1", qid: str = "Q1", hold_id: str = "H1") -> dict:
    page = source()
    return {
        "hold_id": hold_id,
        "finding_id": FINDING,
        "kind": kind,
        "question_id": qid,
        "question_revision": revision,
        "question_sha256": question or page["content_sha256"],
        "dependent_scope": [action],
    }


def answer(question: str | None = None, revision: str = "r1", qid: str = "Q1", reply: str = "Approved for that question only.", role: str = "director", disposition: str = "brief-approval", answer_id: str = "A1") -> dict:
    page = source()
    return {
        "answer_id": answer_id,
        "question_id": qid,
        "question_revision": revision,
        "question_sha256": question or page["content_sha256"],
        "reply": reply,
        "provenance": {
            "actor_label": "Director",
            "role": role,
            "evidence": "SUPPLIED EXAMPLE reply. Not a live Director session.",
        },
        "disposition": disposition,
    }


def review_pass(pass_id: str, prior: str | None, result: str = "unresolved", retry: bool = False, finding: str = FINDING, hashed: bool = True) -> dict:
    return {
        "pass_id": pass_id,
        "finding_id": finding,
        "review_record_sha256": digest(pass_id)[0] if hashed else None,
        "result": result,
        "prior_pass_id": prior,
        "tool_retry": retry,
    }


class PrimeReviewTests(unittest.TestCase):
    def test_routine_correction_without_escalation(self) -> None:
        report, code = run_report(record())
        self.assertEqual(code, 0)
        self.assertEqual(report["effective"], "continue")
        self.assertEqual(report["attention"], [])
        self.assertFalse(report["closes_work"])
        self.assertFalse(report["releases_action"])
        self.assertFalse(report["authenticates_actor"])
        self.assertEqual(report["tasks_added"], [])
        self.assertEqual(report["permission"], "recorded-only")
        self.assertIn(PROMPT, report["markdown"])
        self.assertIn("## For builder", report["markdown"])
        self.assertTrue(report["prompt"]["emitted"])
        again, _code = run_report(record())
        self.assertEqual(again["markdown"], report["markdown"])
        self.assertEqual(again["markdown_sha256"], report["markdown_sha256"])

    def test_design_fork_and_director_hold_block_only_dependents(self) -> None:
        body = record()
        body["judgment"]["semantic_conflict"] = True
        body["judgment"]["design_fork"] = {"id": "fork-1", "text": "Two storage shapes are both still open."}
        body["holds"] = [
            hold("appoint-candidate", kind="design-fork", hold_id="H-fork"),
            hold("choose-storage", kind="director-judgment", hold_id="H-dir", qid="Q2"),
        ]
        blocked, blocked_code = run_guard(body, "appoint-candidate")
        other, other_code = run_guard(body, "choose-storage")
        free, free_code = run_guard(body, "read-record")
        self.assertEqual(blocked_code, 1)
        self.assertEqual(blocked["result"], "blocked")
        self.assertFalse(blocked["releases_action"])
        self.assertEqual(other["result"], "blocked")
        self.assertEqual(other_code, 1)
        self.assertEqual(free_code, 0)
        self.assertEqual(free["result"], "independent-of-holds")
        self.assertFalse(free["releases_action"])
        self.assertEqual([item["hold_id"] for item in free["other_holds"]], ["H-fork", "H-dir"])

    def test_continue_label_loses_to_unresolved_hold(self) -> None:
        body = record()
        body["holds"] = [hold("hand-back")]
        report, code = run_report(body)
        self.assertEqual(code, 1)
        self.assertEqual(report["supplied_outcome"], "continue")
        self.assertEqual(report["effective"], "hold")
        self.assertIn("hold overrides the continue label", report["attention"])
        self.assertNotIn(PROMPT, report["markdown"])
        self.assertFalse(report["prompt"]["emitted"])
        self.assertIn("withheld: no executable prompt is included.", report["markdown"])
        guard, guard_code = run_guard(body, "hand-back")
        self.assertEqual(guard_code, 1)
        self.assertEqual(guard["result"], "blocked")

    def test_unrelated_authorized_work_is_not_frozen(self) -> None:
        body = record()
        body["holds"] = [hold("appoint-candidate")]
        guard, code = run_guard(body, "read-record", authorized=True)
        self.assertEqual(code, 0)
        self.assertEqual(guard["result"], "independent-of-holds")
        self.assertIn("This check does not release the action.", guard["markdown"])
        unknown, unknown_code = run_guard(body, "read-record", authorized=None)
        self.assertEqual(unknown_code, 1)
        self.assertEqual(unknown["result"], "attention")
        outside, outside_code = run_guard(body, "read-record", authorized=False)
        self.assertEqual(outside_code, 1)
        self.assertEqual(outside["result"], "outside-declared-grant")

    def test_exact_director_reply_binds_without_release(self) -> None:
        body = record()
        body["holds"] = [hold("ship-code")]
        body["answers"] = [answer(reply="yes")]
        report, code = run_report(body)
        guard, guard_code = run_guard(body, "ship-code")
        self.assertEqual(code, 0)
        self.assertEqual(report["holds"][0]["status"], "reply-bound")
        self.assertEqual(report["answers"][0]["reply"], "yes")
        self.assertIn("yes", report["markdown"])
        self.assertEqual(guard_code, 1)
        self.assertEqual(guard["result"], "not-released")
        self.assertFalse(guard["releases_action"])
        self.assertFalse(report["closes_work"])

    def test_yes_without_disposition_does_not_approve(self) -> None:
        body = record()
        body["holds"] = [hold("ship-code")]
        body["answers"] = [answer(reply="yes", disposition=None)]
        report, code = run_report(body)
        self.assertEqual(code, 1)
        self.assertEqual(report["holds"][0]["status"], "unresolved")
        self.assertIn("disposition is unknown: A1", report["attention"])
        self.assertEqual(report["answers"][0]["reply"], "yes")

    def test_wrong_stale_and_ambiguous_answers(self) -> None:
        wrong = record()
        wrong["holds"] = [hold("ship-code")]
        wrong["answers"] = [answer(qid="Q-other")]
        wrong_report, _code = run_report(wrong)
        self.assertEqual(wrong_report["answers"][0]["binding"], "unmatched")
        self.assertEqual(wrong_report["holds"][0]["status"], "unresolved")

        stale = record()
        stale["holds"] = [hold("ship-code", revision="r2")]
        stale["answers"] = [answer(revision="r1")]
        stale_report, _code = run_report(stale)
        self.assertEqual(stale_report["holds"][0]["status"], "stale")
        self.assertIn("answer is stale: A1", stale_report["attention"])

        ambiguous = record()
        ambiguous["holds"] = [hold("ship-code")]
        ambiguous["answers"] = [answer(answer_id="A1"), answer(answer_id="A2", reply="A second yes.")]
        ambiguous_report, _code = run_report(ambiguous)
        self.assertEqual(ambiguous_report["holds"][0]["status"], "ambiguous")
        self.assertIn("answer lineage is ambiguous: Q1", ambiguous_report["attention"])
        self.assertEqual(
            [item["reply"] for item in ambiguous_report["answers"]],
            ["Approved for that question only.", "A second yes."],
        )

    def test_substantive_change_reconciles_and_transport_change_does_not(self) -> None:
        page = source()
        moved = source(
            prior_content_sha256="a" * 64,
            prior_transport_sha256="b" * 64,
        )
        self.assertEqual(moved["content_sha256"], page["content_sha256"])
        body = record(sources=[moved])
        body["holds"] = [hold("ship-code", question="a" * 64)]
        body["answers"] = [answer(question="a" * 64)]
        report, _code = run_report(body)
        self.assertEqual(report["sources"][0]["change"], "substantive")
        self.assertEqual(report["holds"][0]["status"], "reconciliation-required")
        self.assertFalse(any(item["binding"] == "reply-bound" for item in report["answers"]))

        transport_hash = digest("wrapper-only")[0]
        carried = source(
            prior_content_sha256=page["content_sha256"],
            prior_transport_sha256=transport_hash,
            transport_sha256=digest("other-wrapper")[0],
            transport_bytes=3,
        )
        carried_body = record(sources=[carried])
        carried_body["holds"] = [hold("ship-code")]
        carried_body["answers"] = [answer(reply="yes")]
        carried_report, code = run_report(carried_body)
        self.assertEqual(carried_report["sources"][0]["change"], "transport")
        self.assertEqual(carried_report["holds"][0]["status"], "reply-bound")
        self.assertEqual(code, 0)

    def test_new_detail_stays_open(self) -> None:
        body = record()
        body["holds"] = [hold("ship-code")]
        body["answers"] = [answer(reply="Yes, and also change the storage layout.", disposition="new-detail")]
        report, _code = run_report(body)
        self.assertEqual(report["holds"][0]["status"], "open-new-detail")
        self.assertIn("also change the storage layout.", report["markdown"])
        guard, code = run_guard(body, "ship-code")
        self.assertEqual(code, 1)
        self.assertEqual(guard["result"], "blocked")

    def test_two_linked_reviews_elevate_and_retries_do_not(self) -> None:
        linked = record()
        linked["review_passes"] = [review_pass("P1", None), review_pass("P2", "P1")]
        report, code = run_report(linked)
        self.assertEqual(code, 1)
        self.assertTrue(report["elevation"][0]["elevate"])
        self.assertEqual(len(report["elevation"][0]["attempts"]), 2)
        self.assertNotIn(PROMPT, report["markdown"])
        self.assertIn("elevation indicated:", " ".join(report["attention"]))

        retries = record()
        retries["review_passes"] = [
            review_pass("T1", None, retry=True),
            review_pass("T2", "T1", retry=True),
        ]
        retry_report, retry_code = run_report(retries)
        self.assertEqual(retry_code, 0)
        self.assertFalse(retry_report["elevation"][0]["elevate"])
        self.assertEqual(retry_report["elevation"][0]["reason"], "tool retries are not review passes")

        other = record()
        other["review_passes"] = [
            review_pass("P1", None, finding="notes/page.md#F-01"),
            review_pass("P2", None, finding="notes/page.md#F-02"),
        ]
        other_report, other_code = run_report(other)
        self.assertEqual(other_code, 0)
        self.assertEqual([row["elevate"] for row in other_report["elevation"]], [False, False])

        broken = record()
        broken["review_passes"] = [review_pass("P1", None), review_pass("P2", None)]
        broken_report, broken_code = run_report(broken)
        self.assertEqual(broken_code, 1)
        self.assertFalse(broken_report["elevation"][0]["elevate"])
        self.assertIn("lineage is ambiguous", broken_report["elevation"][0]["reason"])
        self.assertEqual(len(broken_report["elevation"][0]["attempts"]), 2)

    def test_develop_proposal_does_not_authorize(self) -> None:
        sections = blank_sections()
        sections.update({
            "exploration": "Push the storage notes back and forth. #04 stays a proposal in this text.",
            "assumptions": ["The current grant does not choose a storage shape."],
            "open_questions": ["Which stored form should the next design use?"],
            "for_model": {"model": "builder", "prompt": SECRET},
        })
        body = record()
        body["judgment"]["outcome"] = "develop"
        body["judgment"]["sections"] = sections
        report, code = run_report(body)
        self.assertEqual(code, 1)
        self.assertEqual(report["effective"], "develop")
        self.assertIn("#04 stays a proposal in this text.", report["markdown"])
        self.assertNotIn(SECRET, json.dumps(report))
        self.assertIn("authorizes_task: false", report["markdown"])
        self.assertFalse(report["releases_action"])
        self.assertEqual(report["tasks_added"], [])

    def test_complete_requires_accounted_findings_and_criteria(self) -> None:
        ready = self.complete_body()
        report, code = run_report(ready)
        self.assertEqual(code, 0)
        self.assertEqual(report["effective"], "complete-as-supplied")
        self.assertFalse(report["closes_work"])
        self.assertIn("tasks_added: none", report["markdown"])

        unresolved = self.complete_body()
        unresolved["judgment"]["sections"]["findings_account"] = [{"finding_id": FINDING, "status": "unresolved"}]
        unresolved["judgment"]["sections"]["tests_passed"] = True
        open_report, open_code = run_report(unresolved)
        self.assertEqual(open_code, 1)
        self.assertEqual(open_report["effective"], "not-closed")
        self.assertEqual(open_report["tasks_added"], [])
        self.assertIn("Tests do not close this work.", open_report["markdown"])
        self.assertNotIn("improvement", open_report["markdown"])

        missing = self.complete_body()
        missing["judgment"]["sections"]["finish_assessments"] = []
        missing_report, missing_code = run_report(missing)
        self.assertEqual(missing_code, 1)
        self.assertEqual(missing_report["effective"], "not-closed")
        self.assertIn("finish criterion not assessed: recorded", missing_report["attention"])

        tests_only = self.complete_body()
        tests_only["judgment"]["sections"]["findings_account"] = None
        tests_only["judgment"]["sections"]["finish_assessments"] = None
        tests_only["judgment"]["sections"]["tests_passed"] = True
        tests_only["agreement"]["finish_criteria"] = []
        tests_report, tests_code = run_report(tests_only)
        self.assertEqual(tests_code, 1)
        self.assertEqual(tests_report["effective"], "not-closed")
        self.assertEqual(tests_report["tasks_added"], [])

    def complete_body(self) -> dict:
        sections = blank_sections()
        sections.update({
            "outcome_evidence": "The pinned page records the trial result.",
            "limits": "Authority none. The candidate is not appointed.",
            "tests_note": "Mechanical checks are evidence in the record, not closure.",
            "tests_passed": None,
            "learning": "A protocol miss remains visible.",
            "preservation": "Keep the page bytes and this draft.",
            "remaining_choices": ["Prime reviews the draft."],
            "findings_account": [{"finding_id": FINDING, "status": "accepted"}],
            "finish_assessments": [{"criterion_id": "recorded", "assessment": "met"}],
        })
        body = record()
        body["agreement"] = agreement(
            goal="Record the already-run trial.",
            scope="The pinned trial page only.",
            prime_discretion="How to phrase the recorded result.",
            director_required="Appointment and reopening stay with the Director.",
            finish_criteria=[{"id": "recorded", "text": "The result and its limits are on the page."}],
            recorded_decisions=[],
        )
        body["judgment"]["outcome"] = "complete"
        body["judgment"]["finding"] = "The page records not-oriented and authority none."
        body["judgment"]["reasons"] = ["The page states the judge line."]
        body["judgment"]["next_action"] = "Stop at the recorded result."
        body["judgment"]["sections"] = sections
        return body

    def test_unknown_agreement_withholds_permission(self) -> None:
        body = record()
        body["agreement"] = agreement(goal=None, scope=None)
        report, code = run_report(body)
        self.assertEqual(code, 1)
        self.assertEqual(report["effective"], "attention")
        self.assertEqual(report["permission"], "withheld")
        self.assertIn("agreement.goal is unknown", report["attention"])
        self.assertIn("agreement.scope is unknown", report["attention"])
        self.assertNotIn(PROMPT, report["markdown"])

    def test_attribution_quote_and_model_reply_are_preserved(self) -> None:
        body = record()
        body["attribution"]["actor_label"] = "Codex Prime"
        body["judgment"]["finding"] = QUOTE
        body["judgment"]["sections"]["prime_finding"] = QUOTE
        body["holds"] = [hold("appoint-candidate")]
        body["answers"] = [answer(reply="yes", role="model", disposition="brief-approval")]
        report, _code = run_report(body)
        self.assertIn("actor_label: Codex Prime", report["markdown"])
        self.assertIn(QUOTE, report["markdown"])
        self.assertIn("yes", report["markdown"])
        self.assertEqual(report["holds"][0]["status"], "model-blocked")
        self.assertIn("model cannot answer for the Director: A1", report["attention"])
        self.assertIn("This module does not prove that identity.", report["markdown"])

    def test_duplicate_type_nonfinite_limit_and_unsafe_paths(self) -> None:
        with self.assertRaises(prime_review.Refusal) as duplicate:
            prime_review.strict_json(b'{"schema":"prime-review-record/1","schema":"x"}', "input")
        self.assertIn("duplicate key schema", str(duplicate.exception))

        body = record()
        body["sources"][0]["content_bytes"] = True
        with self.assertRaises(prime_review.Refusal) as bad_type:
            run_report(body)
        self.assertIn("bad type", str(bad_type.exception))

        with self.assertRaises(prime_review.Refusal) as nonfinite:
            prime_review.strict_json(b'{"n": NaN}', "input")
        self.assertIn("nonfinite", str(nonfinite.exception))

        limited = record()
        limited["judgment"]["reasons"] = [f"reason {index}" for index in range(25)]
        with self.assertRaises(prime_review.Refusal) as overflow:
            run_report(limited)
        self.assertIn("limit", str(overflow.exception))

        for path in ("../secret", "foo/../../x", "C:/Windows/notepad.exe", "//server/share", "foo\\bar", "/tmp/x"):
            unsafe = record()
            unsafe["sources"][0]["logical_path"] = path
            with self.assertRaises(prime_review.Refusal):
                run_report(unsafe)

        rated = record()
        rated["continue_rate"] = 0.8
        with self.assertRaises(prime_review.Refusal) as unknown:
            run_report(rated)
        self.assertIn("unknown key continue_rate", str(unknown.exception))

    def test_report_command_is_read_only(self) -> None:
        before = {path.name for path in LAB.iterdir()}
        law = (REPO / "00.kernel/00.00.01.law/0063.role-prime/01.001.md").read_bytes()
        with tempfile.TemporaryDirectory() as folder:
            incoming = Path(folder) / "record.json"
            incoming.write_text(json.dumps(record()), encoding="utf-8")
            stdout = io.StringIO()
            with redirect_stdout(stdout):
                code = prime_review.main(["report", "--input", str(incoming), "--json"])
            self.assertEqual(code, 0)
            self.assertIn('"effective": "continue"', stdout.getvalue())
            self.assertEqual(list(Path(folder).iterdir()), [incoming])
        self.assertEqual({path.name for path in LAB.iterdir()}, before)
        self.assertEqual((REPO / "00.kernel/00.00.01.law/0063.role-prime/01.001.md").read_bytes(), law)

    def test_draft_writer_is_digest_bound_and_external(self) -> None:
        report, _code = run_report(record())
        payload = json.dumps(record()).encode("utf-8")
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            repo = root / "repo"
            outside = root / "outside"
            repo.mkdir()
            outside.mkdir()
            dest = outside / "draft.md"
            prime_review.write_draft(payload, dest, repo, report["markdown_sha256"], None)
            self.assertEqual(dest.read_bytes(), report["markdown"].encode("utf-8"))
            with self.assertRaises(prime_review.Refusal):
                prime_review.write_draft(payload, dest, repo, report["markdown_sha256"], None)
            self.assertEqual(dest.read_bytes(), report["markdown"].encode("utf-8"))
            missing = outside / "nope.md"
            with self.assertRaises(prime_review.Refusal) as mismatch:
                prime_review.write_draft(payload, missing, repo, "a" * 64, None)
            self.assertIn("digest mismatch", str(mismatch.exception))
            self.assertFalse(missing.exists())
            inside = repo / "live.md"
            with self.assertRaises(prime_review.Refusal) as nested:
                prime_review.write_draft(payload, inside, repo, report["markdown_sha256"], None)
            self.assertIn("destination inside repository", str(nested.exception))
            self.assertFalse(inside.exists())

            partial = outside / "partial.md"

            def boom(fd: int, data: bytes) -> None:
                os.write(fd, data[:4])
                raise OSError("disk")

            original = prime_review._write_fd
            prime_review._write_fd = boom
            try:
                with self.assertRaises(prime_review.Refusal):
                    prime_review.write_draft(payload, partial, repo, report["markdown_sha256"], None)
            finally:
                prime_review._write_fd = original
            self.assertEqual(partial.read_bytes(), report["markdown"].encode("utf-8")[:4])
            with self.assertRaises(prime_review.Refusal):
                prime_review.write_draft(payload, partial, repo, report["markdown_sha256"], None)
            self.assertEqual(partial.read_bytes(), report["markdown"].encode("utf-8")[:4])

        forbidden = REPO / "labs" / "prime-review-pass01" / "DO-NOT-WRITE.md"
        self.assertFalse(forbidden.exists())
        with self.assertRaises(prime_review.Refusal):
            prime_review.write_draft(payload, forbidden, REPO, report["markdown_sha256"], None)
        self.assertFalse(forbidden.exists())

    def test_bound_file_checks_and_link_refusal(self) -> None:
        text = "bound page\n"
        content, size = digest(text)
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / "notes"
            target.mkdir()
            page = target / "page.md"
            page.write_bytes(text.encode("utf-8"))
            body = record(sources=[source(text, "notes/page.md", bind=True)])
            report, code = run_report(body, root)
            self.assertEqual(code, 0)
            self.assertEqual(report["sources"][0]["content_sha256"], content)
            self.assertEqual(size, len(text.encode("utf-8")))
            page.write_bytes(b"changed ok\n")
            with self.assertRaises(prime_review.Refusal) as changed:
                run_report(body, root)
            self.assertIn("hash mismatch", str(changed.exception))

            page.write_bytes(text.encode("utf-8"))
            linked = target / "linked.md"
            try:
                os.link(page, linked)
            except OSError as exc:
                self.skipTest(f"hard link skipped: {exc}")
            linked_body = record(sources=[source(text, "notes/linked.md", bind=True)])
            with self.assertRaises(prime_review.Refusal) as hard:
                run_report(linked_body, root)
            self.assertIn("hard link", str(hard.exception))

    def test_file_symlink_is_refused_when_creation_is_allowed(self) -> None:
        text = "bound page\n"
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            target = root / "notes"
            target.mkdir()
            page = target / "page.md"
            page.write_bytes(text.encode("utf-8"))
            pointer = target / "sym.md"
            try:
                os.symlink(page, pointer)
            except OSError as exc:
                self.skipTest(f"file symlink skipped: {exc}")
            sym_body = record(sources=[source(text, "notes/sym.md", bind=True)])
            with self.assertRaises(prime_review.Refusal) as link:
                run_report(sym_body, root)
            self.assertIn("symlink or junction", str(link.exception))

    def test_check_next_matches_guard_and_pins_stay(self) -> None:
        body = record()
        body["holds"] = [hold("appoint-candidate")]
        payload = {
            "schema": "prime-review-guard/1",
            "review": body,
            "proposed_action": {
                "action_id": "read-record",
                "label": "Read the page",
                "grant_ref": "existing grant",
                "authorized_in_grant": True,
            },
        }
        with tempfile.TemporaryDirectory() as folder:
            incoming = Path(folder) / "guard.json"
            incoming.write_text(json.dumps(payload), encoding="utf-8")
            first = io.StringIO()
            second = io.StringIO()
            with redirect_stdout(first):
                left = prime_review.main(["guard", "--input", str(incoming), "--json"])
            with redirect_stdout(second):
                right = prime_review.main(["check-next", "--input", str(incoming), "--json"])
            self.assertEqual(left, 0)
            self.assertEqual(first.getvalue(), second.getvalue())
            self.assertEqual(right, 0)
        pins = {
            "labs/prime-support-pass01/prime_support.py": "700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70",
            "labs/prime-brief-pass01/prime_brief.py": "302ed832d2fa955a591420f13d3b22ce91e4a7669c69a778d443fc82627580d7",
            "labs/state-projection-pass01/state_projection.py": "b349da5cef5178296a069c354002a600ba4e168c2710aa5d87789724d4951ecb",
            "labs/return-capture-pass01/return_capture.py": "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac",
            "labs/return-capture-pass01/return_inspect.py": "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b",
        }
        for relative, expected in pins.items():
            data = (REPO / relative).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), expected)
        source_text = (LAB / "prime_review.py").read_text(encoding="utf-8")
        self.assertNotIn("subprocess", source_text)
        self.assertNotIn("prime_support", source_text)
        self.assertNotIn("importlib", source_text)

    def test_director_input_and_capture_identity(self) -> None:
        content, size = digest("captured return bytes\n")
        sections = blank_sections()
        sections.update({
            "issue": "The design forks on where the reply is stored.",
            "consequences": "Choosing now would freeze the other shape.",
            "options": ["Keep replies on the work page.", "Wait for a later page."],
            "recommendation": "Keep the reply on the work page.",
            "question": {
                "id": "Q-store",
                "revision": "r1",
                "content_sha256": content,
                "text": "Should this reply stay on the work page?",
            },
            "affected": [{"action_id": "store-reply", "dependency": "the open storage fork"}],
            "proposed_plan": {"label": "proposed-plan", "text": "A later page could index the reply."},
            "for_model": {"model": "builder", "prompt": SECRET},
        })
        body = record()
        body["sources"] = [{
            "kind": "capture",
            "logical_path": "members/0157.prime-review-0501",
            "content_sha256": content,
            "content_bytes": size,
            "transport_sha256": content,
            "transport_bytes": size,
            "prior_content_sha256": None,
            "prior_transport_sha256": None,
            "record": "captured return bytes\n",
            "bind": False,
            "identity": {
                "schema": "return-capture/1",
                "member": "0157.prime-review-0501",
                "submission_id": "grok-2-0512-0501",
                "receipt_sha256": None,
                "origin": {"book": "00.00.10.work", "page": "0512.prime-review", "batch": "05.01"},
            },
        }]
        body["judgment"]["outcome"] = "director-input"
        body["judgment"]["semantic_conflict"] = True
        body["judgment"]["design_fork"] = {"id": "store", "text": "Reply storage is unresolved."}
        body["judgment"]["sections"] = sections
        body["holds"] = [hold("store-reply", kind="design-fork", question=content, qid="Q-store")]
        report, code = run_report(body)
        self.assertEqual(code, 1)
        self.assertEqual(report["effective"], "hold")
        self.assertEqual(report["sources"][0]["identity_schema"], "return-capture/1")
        self.assertIn("This block is not executable.", report["markdown"])
        self.assertNotIn(SECRET, json.dumps(report))
        self.assertEqual(report["sources"][0]["change"], "unspecified")


class JunctionTests(unittest.TestCase):
    def test_directory_junction_is_refused(self) -> None:
        text = "bound page\n"
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            real = root / "real"
            real.mkdir()
            (real / "page.md").write_text(text, encoding="utf-8")
            link = root / "jump"
            created = subprocess.run(
                ["cmd", "/c", "mklink", "/J", str(link), str(real)],
                capture_output=True,
                text=True,
            )
            if created.returncode != 0 or not link.exists():
                self.skipTest(f"junction skipped: {created.stderr.strip() or created.stdout.strip()}")
            info = os.lstat(link)
            if not (getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
                self.skipTest("junction was not a reparse point")
            body = record(sources=[source(text, "jump/page.md", bind=True)])
            with self.assertRaises(prime_review.Refusal) as refused:
                run_report(body, root)
            self.assertIn("symlink or junction", str(refused.exception))


if __name__ == "__main__":
    unittest.main()
