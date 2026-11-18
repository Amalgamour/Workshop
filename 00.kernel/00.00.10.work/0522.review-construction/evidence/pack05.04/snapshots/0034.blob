"""Tests for the 05.02 corrections: PC-01 (stale review declarations stay historical), PC-02 (decision templates bind the
review direction) and the operation journal with its day view. Disposable books; real pinned dependencies; synthetic
SUPPLIED decisions only. No model, no shared checkout write.

  python -B -X dev tests/test_binding_log.py -v
"""
import contextlib
import copy
import hashlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import fixture as F  # noqa: E402
import prime_cycle as pc  # noqa: E402
from test_prime_cycle import A, Cycle  # noqa: E402

TERMS = ("disposition", "pass_terminal", "goal_terminal")


def in_process(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = pc.main([str(a) for a in argv])
    return code, out.getvalue(), err.getvalue()


class Base(Cycle):
    def completed(self):
        """A work with an accepted review r1 and an explicit goal completion r2."""
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        _, v = self.d.read(reg)
        self.assertEqual(self.record(reg, F.fill(self.tmpl(v), "accept-finished-open"), "r1.json")[0], 0)
        _, v = self.d.read(reg)
        self.assertEqual(self.record(reg, F.fill(self.tmpl(v), "complete"), "r2.json")[0], 0)
        _, v = self.d.read(reg)
        self.assertEqual((v["works"][0]["goal_terminal"], v["summary"]["completed_goals"]), ("completed", 1))
        return m, w, reg

    def assert_historical(self, reg, reason, state):
        code, v = self.d.read(reg)
        it = v["works"][0]
        self.assertEqual(it["pass_state"], state)
        self.assertEqual(tuple(it[k] for k in TERMS), ("unknown",) * 3)
        self.assertIsNone(it["next_action"])
        self.assertEqual(it["historical"]["reason"], reason)
        self.assertFalse(it["latest_review"]["current"])
        self.assertEqual((v["summary"]["finished_passes"], v["summary"]["completed_goals"]), (0, 0))
        _, text, _ = self.d.cli("read", "--registration", reg)
        self.assertNotIn(": completed\n", text)
        self.assertNotIn("pass terminal: finished\n", text)
        self.assertIn("unknown (historical ", text)
        self.assertIn("completed goals 0", text)
        return it


class TestStaleHistorical(Base):
    def test_13_page_change_keeps_completion_historical_until_a_fresh_successor(self):
        m, w, reg = self.completed()
        self.d.page(A, "05.01", F.page_text(m, self.d.receipt(m), extra="\nEdited after completion."))
        it = self.assert_historical(reg, "review-stale", "review-stale")
        self.assertEqual((it["historical"]["goal_terminal"], it["historical"]["pass_terminal"], it["historical"]["review_id"]),
                         ("completed", "finished", "05.01-r2"))
        rdir = self.d.repo / w["review_location"]
        self.assertEqual(sorted(p.name for p in rdir.iterdir()), ["05.01-r1", "05.01-r2"])  # nothing erased
        _, v = self.d.read(reg)
        succ = F.fill(self.tmpl(v), "complete")
        self.assertEqual(succ["supersedes"]["review_id"], "05.01-r2")
        self.assertEqual(self.record(reg, succ, "r3.json")[0], 0)
        _, v = self.d.read(reg)
        it = v["works"][0]
        self.assertEqual((it["pass_state"], it["goal_terminal"], it["historical"], v["summary"]["completed_goals"]),
                         ("reviewed", "completed", None, 1))

    def test_14_custody_change_makes_declarations_and_next_action_historical(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        _, v = self.d.read(reg)
        self.assertEqual(self.record(reg, F.fill(self.tmpl(v), "accept-finished-open"))[0], 0)
        receipt = self.d.book / m / "receipt.json"
        receipt.write_bytes(receipt.read_bytes() + b" ")  # disposable member: custody no longer verifies
        it = self.assert_historical(reg, "review-stale", "review-stale")
        self.assertIn("receipt_sha256", " ".join(it["attention"]))
        self.assertEqual(it["historical"]["next_action"]["action_id"], "next-pass")
        _, text, _ = self.d.cli("read", "--registration", reg)
        self.assertIn("historical next action (not current;", text)
        self.assertNotIn("recorded next action (", text)

    def test_15_altered_latest_review_is_not_replaced_by_its_predecessor(self):
        m, w, reg = self.completed()
        r2 = self.d.repo / w["review_location"] / "05.01-r2" / "REVIEW.md"
        r2.write_bytes(r2.read_bytes() + b"edited\n")
        it = self.assert_historical(reg, "altered-review", "review-unusable")
        self.assertEqual(it["historical"]["review_id"], "05.01-r1")
        p = [x for x in it["reviews"]["partial"] if x["review_id"] == "05.01-r2"][0]
        self.assertEqual(p["marker"], "hash-mismatch")
        _, v = self.d.read(reg)
        succ = F.fill(self.tmpl(v), "accept-finished-open")
        succ["recovers"] = "05.01-r2"
        self.assertEqual(self.record(reg, succ, "r3.json")[0], 0)
        _, v = self.d.read(reg)
        self.assertEqual((v["works"][0]["pass_state"], v["works"][0]["pass_terminal"]), ("reviewed", "finished"))

    def test_16_legacy_record_is_never_current_under_the_stronger_contract(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        _, v = self.d.read(reg)
        self.assertEqual(self.record(reg, F.fill(self.tmpl(v), "complete"))[0], 0)
        rdir = self.d.repo / w["review_location"] / "05.01-r1"  # rewrite into the 05.01 shape, as an old record would be
        rec = json.loads((rdir / "record.json").read_text(encoding="utf-8"))
        rec["schema"] = "prime-cycle-review/1"
        rec["decision"]["schema"] = "prime-cycle-decision/1"
        for b in (rec["decision"]["binding"], rec["observed_binding"]):
            del b["direction"]
        rb = pc.canonical(rec)
        (rdir / "record.json").unlink()
        (rdir / "record.json").write_bytes(rb)
        (rdir / "COMMITTED.json").unlink()
        (rdir / "COMMITTED.json").write_bytes(pc.canonical({"record_sha256": pc.sha(rb), "review_md_sha256": pc.sha((rdir / "REVIEW.md").read_bytes())}))
        it = self.assert_historical(reg, "legacy-binding", "review-unusable")
        self.assertEqual(it["historical"]["goal_terminal"], "completed")

    def test_17_goal_change_behaviour_is_kept_separate(self):
        m, w, reg = self.completed()
        w2 = copy.deepcopy(w)
        w2["goal"] = {"goal_id": "g2", "statement": "A NEW, larger SUPPLIED FIXTURE goal."}
        _, v = self.d.read(self.d.registration([w2], name="reg2.json"))
        it = v["works"][0]
        self.assertEqual((it["pass_state"], it["pass_terminal"], it["historical"]), ("reviewed", "finished", None))
        self.assertTrue(it["goal_terminal"].startswith("open (prior completion bound to goal g1"))
        self.assertEqual(v["summary"]["completed_goals"], 0)


class TestDirectionBinding(Base):
    def test_18_changed_direction_refuses_the_old_template_and_a_new_read_records(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        _, v = self.d.read(reg)
        dec = F.fill(self.tmpl(v), "accept-finished-open")
        raw = json.loads(reg.read_text())
        for field, value in (("scope", "CHANGED SCOPE."), ("finish_criteria", [{"id": "other", "text": "x"}]),
                             ("director_required", "Something new."), ("extra_key", "x")):
            with self.subTest(field=field):
                changed = copy.deepcopy(raw)
                changed["works"][0]["agreement"][field] = value
                p = self.d.tmp / f"reg-{field}.json"
                p.write_text(json.dumps(changed))
                code, out, _ = self.record(p, dec, f"d-{field}.json")
                self.assertEqual(code, 2, out)
                self.assertIn("direction changed since read: " + (f"agreement.{field}" if field != "extra_key" else "agreement (other keys)"), out)
        self.assertFalse((self.d.repo / w["review_location"]).exists())
        unbound = copy.deepcopy(raw)  # output_root, bounds and other works are not part of the direction
        unbound["bounds"]["max_works"] = 8
        other = self.d.member("other", "0598.cycle-b", "05.01")
        self.d.page("0598.cycle-b", "05.01", F.page_text(other, self.d.receipt(other)))
        unbound["works"].append(self.d.work("B", "0598.cycle-b", "05.01", other))
        pu = self.d.tmp / "reg-unbound.json"
        pu.write_text(json.dumps(unbound))
        self.assertEqual(self.record(pu, dec, "d-unbound.json")[0], 0)
        self.assertEqual(self.record(pu, dec, "d-unbound.json")[1].split()[0], "already-recorded")  # identical replay
        changed = copy.deepcopy(unbound)
        changed["works"][0]["agreement"]["scope"] = "CHANGED AFTER RECORD."
        pc2 = self.d.tmp / "reg-after.json"
        pc2.write_text(json.dumps(changed))
        code, out, _ = self.record(pc2, dec, "d-replay.json")
        self.assertEqual(code, 2)
        self.assertIn("direction changed", out)  # no replay of an old decision under changed direction
        _, v2 = self.d.read(pc2)
        it = v2["works"][0]
        self.assertEqual((it["pass_state"], it["historical"]["reason"]), ("review-stale", "review-stale"))
        succ = F.fill(self.tmpl(v2), "accept-finished-open")
        self.assertNotEqual(succ["binding"]["direction"], dec["binding"]["direction"])
        self.assertEqual(self.record(pc2, succ, "d-new.json")[0], 0)
        _, v3 = self.d.read(pc2)
        self.assertEqual(v3["works"][0]["pass_state"], "reviewed")

    def test_19_old_template_schema_is_refused(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        _, v = self.d.read(reg)
        old = F.fill(self.tmpl(v), "accept-finished-open")
        old["schema"] = "prime-cycle-decision/1"
        del old["binding"]["direction"]
        code, out, _ = self.record(reg, old)
        self.assertEqual(code, 2)
        self.assertIn("older read; read again", out)


class TestJournal(Base):
    def setUp(self):
        super().setUp()
        self.J = self.d.tmp / "journal"

    def j(self, *args, caller="Codex Prime (SUPPLIED FIXTURE)"):
        return self.d.cli(*args, "--journal-root", self.J, "--caller", caller)

    def day(self, reg=None):
        date = next(self.J.iterdir()).name
        args = ["day", "--journal-root", self.J, "--date", date, "--json"] + (["--registration", reg] if reg else [])
        code, out, err = self.d.cli(*args)
        self.assertEqual(err, "")
        return code, json.loads(out)

    def ops(self):
        return sorted(p for day in self.J.iterdir() for p in day.iterdir())

    def test_20_read_record_read_is_logged_with_machine_facts_and_review_pointer(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        code, out, _ = self.j("read", "--registration", reg, "--json")
        self.assertEqual(json.loads(out)["journal"]["enabled"], True)
        tmpl = json.loads(out)["works"][0]["template"]
        code, out, _ = self.j("record", "--registration", reg, "--decision", self.d.write_decision(F.fill(tmpl, "accept-finished-open"), "d.json"))
        self.assertEqual(code, 0, out)
        self.assertIn(f"journal: {self.J}", out)
        self.assertEqual(self.j("read", "--registration", reg)[0], 0)
        ops = self.ops()
        self.assertEqual(len(ops), 3)
        starts = [json.loads((p / "start.json").read_text(encoding="utf-8")) for p in ops]
        ends = [json.loads((p / "end.json").read_text(encoding="utf-8")) for p in ops]
        self.assertEqual([s["operation"] for s in starts], ["read", "record", "read"])
        self.assertEqual([e["machine"]["status"] for e in ends], ["ok-attention", "recorded", "ok"])
        s = starts[1]
        self.assertEqual(s["supplied"]["caller_label"], "Codex Prime (SUPPLIED FIXTURE)")
        self.assertRegex(s["machine"]["started_at_local"], r"[+-]\d\d:\d\d$")
        self.assertEqual(s["machine"]["tool_sha256"], hashlib.sha256(Path(pc.__file__).read_bytes()).hexdigest())
        self.assertEqual(s["machine"]["inputs"]["decision"]["sha256"], hashlib.sha256((ops[1] / "decision.json").read_bytes()).hexdigest())
        self.assertEqual((ops[1] / "registration.json").read_bytes(), reg.read_bytes())
        rv = ends[1]["machine"]["result"]["review"]
        rec = self.d.repo / w["review_location"] / "05.01-r1" / "record.json"
        self.assertEqual(rv["record_sha256"], hashlib.sha256(rec.read_bytes()).hexdigest())
        self.assertEqual(ends[1]["machine"]["stdout"]["sha256"], hashlib.sha256((ops[1] / "stdout.txt").read_bytes()).hexdigest())
        code, dv = self.day(reg)
        self.assertEqual((code, len(dv["unique_reviews"]), dv["unique_reviews"][0]["current_head"]), (0, 1, True))
        self.assertEqual(dv["current"]["finished_passes"], ["A"])
        self.assertNotIn("day", [s["operation"] for s in starts])

    def test_21_refusal_replay_and_completion_are_counted_once(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        _, v = self.d.read(reg)
        dec = F.fill(self.tmpl(v), "complete")
        bad = copy.deepcopy(dec)
        bad["judgment"]["goal"]["evidence"] = []
        self.assertEqual(self.j("record", "--registration", reg, "--decision", self.d.write_decision(bad, "bad.json"))[0], 2)
        path = self.d.write_decision(dec, "dec.json")
        for _ in range(3):
            self.assertEqual(self.j("record", "--registration", reg, "--decision", path)[0], 0)
        code, dv = self.day(reg)
        self.assertEqual(dv["counts"]["record"], {"recorded": 1, "refused": 1, "replay": 2})
        self.assertEqual((len(dv["unique_reviews"]), dv["record_invocations"], dv["unique_reviews"][0]["replays"]), (1, 3, 2))
        self.assertEqual(dv["declared"]["completed_goals"], 1)
        self.assertEqual(dv["current"]["completed_goals"], ["A"])
        refused = [o for o in dv["operations"] if o["status"] == "refused"][0]
        self.assertIn("evidence", refused["detail"][0])
        self.d.page(A, "05.01", F.page_text(m, self.d.receipt(m), extra="\nEdited."))  # no false completion once stale
        code, dv = self.day(reg)
        self.assertEqual((dv["declared"]["completed_goals"], dv["current"]["completed_goals"], dv["current"]["not_current"]), (1, [], ["A"]))
        _, text, _ = self.d.cli("day", "--journal-root", self.J, "--date", next(self.J.iterdir()).name)
        self.assertIn("current: not checked (no --registration)", text)
        self.assertIn("no totals or productivity are derived", text)
        _, v = self.d.read(reg)  # a second completion review of the same goal is one goal completion, not two
        self.assertEqual(self.j("record", "--registration", reg, "--decision", self.d.write_decision(F.fill(self.tmpl(v), "complete"), "r2.json"))[0], 0)
        code, dv = self.day(reg)
        self.assertEqual((len(dv["unique_reviews"]), dv["declared"]["completed_goals"], dv["declared"]["finished_passes"]), (2, 1, 1))
        self.assertEqual(dv["current"]["completed_goals"], ["A"])

    def test_22_interrupted_review_and_missing_end_stay_incomplete(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        _, v = self.d.read(reg)
        path = self.d.write_decision(F.fill(self.tmpl(v), "accept-finished-open"), "d.json")
        real = pc.write_file

        def torn(p, data):
            if p.name == "REVIEW.md":
                with open(p, "xb") as h:
                    h.write(data[:10])
                raise OSError("injected interruption")
            return real(p, data)
        with mock.patch.object(pc, "write_file", torn):
            code, out, err = in_process("record", "--registration", reg, "--decision", path, "--journal-root", self.J)
        self.assertEqual(code, 3, out)
        end = json.loads((self.ops()[0] / "end.json").read_text(encoding="utf-8"))
        self.assertEqual(end["machine"]["status"], "partial")
        self.assertEqual(sorted(end["machine"]["result"]["review"]["files"]), ["REVIEW.md", "record.json"])
        with mock.patch.object(pc, "operate", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                in_process("read", "--registration", reg, "--journal-root", self.J)
        code, dv = self.day()
        self.assertEqual(code, 1)
        self.assertEqual(len(dv["incomplete"]), 1)
        inc = [o for o in dv["operations"] if o["status"] == "incomplete"][0]
        self.assertEqual((inc["operation"], inc["duration_seconds"], inc["exit"]), ("read", None, None))
        self.assertEqual(dv["unique_reviews"], [])  # the partial is not a review
        self.assertTrue((self.d.repo / w["review_location"] / "05.01-r1" / "record.json").exists())  # the partial is kept

    def test_23_journal_failures_never_run_blind_or_hide_a_committed_review(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        _, v = self.d.read(reg)
        path = self.d.write_decision(F.fill(self.tmpl(v), "accept-finished-open"), "d.json")
        blocker = self.d.tmp / "not-a-dir"
        blocker.write_bytes(b"x")
        for root in (blocker, self.d.repo / "journal-in-repo", self.d.book / "j"):
            with self.subTest(root=root.name):
                code, out, _ = self.d.cli("record", "--registration", reg, "--decision", path, "--journal-root", root)
                self.assertEqual(code, 4, out)
                self.assertIn("nothing was run", out)
                self.assertFalse((self.d.repo / w["review_location"]).exists())
        self.assertFalse((self.d.repo / "journal-in-repo").exists())
        with mock.patch.object(pc.Journal, "end", side_effect=OSError("disk full (injected)")):
            code, out, err = in_process("record", "--registration", reg, "--decision", path, "--journal-root", self.J)
        self.assertEqual(code, 5)
        self.assertIn("recorded ", out)
        self.assertIn("end event FAILED", err)
        self.assertIn("the review IS committed at", err)
        self.assertTrue((self.d.repo / w["review_location"] / "05.01-r1" / "COMMITTED.json").exists())
        code, dv = self.day(reg)
        self.assertEqual((code, len(dv["incomplete"]), dv["current"]["finished_passes"]), (1, 1, ["A"]))
        jo = self.d.out / "journal"  # a journal under output_root may not receive templates
        code, out, _ = self.d.cli("read", "--registration", reg, "--templates", jo / "t", "--journal-root", jo)
        self.assertEqual(code, 2)
        self.assertIn("must not lie inside the journal root", out)

    def test_24_disabled_journal_is_visible(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        code, out, _ = self.d.cli("read", "--registration", reg)
        self.assertIn("journal: disabled (no --journal-root; this operation is not logged)", out)
        code, out, _ = self.d.cli("inspect", "--registration", reg, "--work", "A")
        self.assertEqual(json.loads(out)["journal"]["enabled"], False)
        self.assertFalse(self.J.exists())


if __name__ == "__main__":
    unittest.main()
