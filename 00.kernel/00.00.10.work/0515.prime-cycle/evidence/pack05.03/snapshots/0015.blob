"""Tests for prime_cycle.py (0515.prime-cycle/05.01). Disposable repositories and books; real pinned reader, inspector,
helper, prime_review and review_packet; synthetic SUPPLIED decisions only. No model, no shared checkout write.

  python -B -X dev tests/test_prime_cycle.py -v
"""
import copy
import hashlib
import json
import shutil
import sys
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import fixture as F  # noqa: E402
import prime_cycle as pc  # noqa: E402

A, B = "0599.cycle-a", "0598.cycle-b"


def tree(root: Path):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob("*")) if p.is_file()}


class Cycle(unittest.TestCase):
    def setUp(self):
        self.d = F.Desk(prefix="pcy-" + self._testMethodName[5:20] + "-")

    def tearDown(self):
        self.d.close()

    def work_with_return(self, lane=A, batch="05.01", name=None, wid="A", **page):
        m = self.d.member(name or f"m{lane[-1]}{batch[-1]}", lane, batch)
        self.d.page(lane, batch, F.page_text(m, self.d.receipt(m), **page))
        return m, self.d.work(wid, lane, batch, m)

    def record(self, reg, decision, name="dec.json"):
        return self.d.cli("record", "--registration", reg, "--decision", self.d.write_decision(decision, name))

    def tmpl(self, view, i=0):
        return view["works"][i]["template"]


class TestStates(Cycle):
    def test_01_new_return_without_review_is_awaiting_review(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        code, v = self.d.read(reg)
        it = v["works"][0]
        self.assertEqual((code, it["pass_state"], it["disposition"], it["goal_terminal"]), (1, "awaiting-review", "unknown", "unknown"))
        self.assertEqual(it["custody"]["role"], "primary-current-candidate")
        b = it["template"]["binding"]
        self.assertEqual((b["member"], b["receipt_sha256"], b["expected_prior"]), (m, self.d.receipt(m), None))
        self.assertIsNone(v["elected"])
        self.assertTrue(all(val is None for k, val in it["template"]["judgment"].items()
                            if k not in ("goal", "reasons", "source_refs", "unresolved", "holds", "answers", "sections")))

    def test_02_accepted_pass_finished_goal_open(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        _, v = self.d.read(reg)
        code, out, err = self.record(reg, F.fill(self.tmpl(v), "accept-finished-open"))
        self.assertEqual((code, err), (0, ""), out)
        _, v2 = self.d.read(reg)
        it = v2["works"][0]
        self.assertEqual((it["pass_state"], it["disposition"], it["pass_terminal"], it["goal_terminal"]),
                         ("reviewed", "accepted", "finished", "open"))
        self.assertEqual(it["next_action"]["author"], "Codex Prime (SUPPLIED FIXTURE)")
        self.assertIn("record.json", it["next_action"]["source"])
        rdir = self.d.repo / w["review_location"] / "05.01-r1"
        self.assertEqual(sorted(p.name for p in rdir.iterdir()), ["COMMITTED.json", "REVIEW.md", "record.json"])
        marker = json.loads((rdir / "COMMITTED.json").read_text())
        self.assertEqual(marker["record_sha256"], hashlib.sha256((rdir / "record.json").read_bytes()).hexdigest())
        self.assertIn(f"sha256 {marker['record_sha256']}", (rdir / "REVIEW.md").read_text(encoding="utf-8"))

    def test_03_explicit_goal_completion_survives_a_new_process_and_not_a_new_goal(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        _, v = self.d.read(reg)
        self.record(reg, F.fill(self.tmpl(v), "accept-finished-open"), "d1.json")
        _, v2 = self.d.read(reg)
        code, out, _ = self.record(reg, F.fill(self.tmpl(v2), "complete"), "d2.json")
        self.assertEqual(code, 0, out)
        _, v3 = self.d.read(reg)
        self.assertEqual(v3["works"][0]["goal_terminal"], "completed")
        w2 = copy.deepcopy(w)
        w2["goal"] = {"goal_id": "g2", "statement": "A NEW, larger SUPPLIED FIXTURE goal."}
        reg2 = self.d.registration([w2], name="reg2.json")
        _, v4 = self.d.read(reg2)
        self.assertTrue(v4["works"][0]["goal_terminal"].startswith("open (prior completion bound to goal g1"))
        same_id = copy.deepcopy(w)
        same_id["goal"]["statement"] = "Changed statement under the old id."
        _, v5 = self.d.read(self.d.registration([same_id], name="reg3.json"))
        self.assertTrue(v5["works"][0]["goal_terminal"].startswith("open (prior completion"))

    def test_03b_completion_rules_refuse_contradictions(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        _, v = self.d.read(reg)
        t = self.tmpl(v)
        bad = {"complete-without-goal": F.fill(t, "complete", goal=dict(F.fill(t, "complete")["judgment"]["goal"], terminal="open")),
               "goal-without-complete": F.fill(t, "accept-finished-open", goal=dict(t["judgment"]["goal"], terminal="completed", evidence=["x"])),
               "held-but-finished": F.fill(t, "held", pass_terminal="finished"),
               "complete-no-evidence": F.fill(t, "complete", goal=dict(F.fill(t, "complete")["judgment"]["goal"], evidence=[])),
               "wrong-goal": F.fill(t, "complete", goal=dict(F.fill(t, "complete")["judgment"]["goal"], goal_id="other")),
               "director-input-accepted": F.fill(t, "director-input", disposition="accepted")}
        for name, dec in bad.items():
            with self.subTest(case=name):
                code, out, _ = self.record(reg, dec, f"{name}.json")
                self.assertEqual(code, 2, out)
        self.assertFalse((self.d.repo / w["review_location"]).exists())


class TestHolds(Cycle):
    def test_04_director_hold_blocks_only_affected_and_keeps_exact_reply(self):
        ma, wa = self.work_with_return(A, "05.01", wid="A")
        mb, wb = self.work_with_return(B, "05.01", wid="B")
        reg = self.d.registration([wa, wb])
        _, v = self.d.read(reg)
        self.assertEqual(self.record(reg, F.fill(self.tmpl(v, 0), "director-input"), "a.json")[0], 1)
        dep = F.fill(self.tmpl(v, 1), "accept-finished-open",
                     next_action={"action_id": "design-change", "text": "Apply the design change.", "authorized_in_grant": True})
        self.assertEqual(self.record(reg, dep, "b.json")[0], 0)
        code, v2 = self.d.read(reg)
        a, b = v2["works"]
        self.assertEqual((a["disposition"], a["holds"][0]["status"]), ("held", "unresolved"))
        self.assertEqual(b["next_action_guard"][0]["result"], "blocked")
        _, v3 = self.d.read(reg)
        indep = F.fill(self.tmpl(v3, 1), "accept-finished-open")  # successor for B with an independent action
        indep["review_id"] = "05.01-r2"
        self.assertEqual(self.record(reg, indep, "b2.json")[0], 0)
        _, v4 = self.d.read(reg)
        self.assertEqual(v4["works"][1]["next_action_guard"][0]["result"], "independent-of-holds")
        q = F.fill(self.tmpl(v4, 0), "director-input")
        reply = 'Yes — keep the design. "Exactly this."'
        q["judgment"]["answers"] = [{"answer_id": "A1", "question_id": "Q1", "question_revision": "r1",
                                     "question_sha256": q["judgment"]["holds"][0]["question_sha256"], "reply": reply,
                                     "provenance": {"actor_label": "Director (SUPPLIED FIXTURE)", "role": "director", "evidence": "fixture"},
                                     "disposition": "brief-approval"}]
        q["review_id"] = "05.01-r2"
        self.record(reg, q, "a2.json")
        _, v5 = self.d.read(reg)
        a5 = v5["works"][0]
        self.assertEqual(a5["holds"][0]["status"], "reply-bound")
        rec = json.loads((self.d.repo / wa["review_location"] / "05.01-r2" / "record.json").read_text(encoding="utf-8"))
        self.assertEqual(rec["decision"]["judgment"]["answers"][0]["reply"], reply)
        self.assertTrue((self.d.repo / wa["review_location"] / "05.01-r1" / "COMMITTED.json").exists())


class TestChanges(Cycle):
    def test_05_source_receipt_origin_and_prior_changes_refuse(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        _, v = self.d.read(reg)
        t = self.tmpl(v)
        self.d.page(A, "05.01", F.page_text(m, self.d.receipt(m), extra="\nEdited after read."))
        code, out, _ = self.record(reg, F.fill(t, "accept-finished-open"), "page.json")
        self.assertEqual(code, 2)
        self.assertIn("source changed since read: source", out)
        _, v = self.d.read(reg)
        t = self.tmpl(v)
        forged = F.fill(t, "accept-finished-open")
        forged["binding"]["receipt_sha256"] = "f" * 64
        code, out, _ = self.record(reg, forged, "receipt.json")
        self.assertIn("source changed since read", out)
        refreshed = F.fill(t, "accept-finished-open")
        refreshed["binding"]["fingerprint"] = "e" * 64
        self.assertIn("fingerprint", self.record(reg, refreshed, "fp.json")[1])
        first, second = F.fill(t, "accept-finished-open"), F.fill(t, "held")
        second["review_id"] = "05.01-r9"
        self.assertEqual(self.record(reg, first, "first.json")[0], 0)
        code, out, _ = self.record(reg, second, "second.json")
        self.assertEqual(code, 2)
        self.assertIn("expected_prior", out)
        other = self.d.member("orig", B, "05.07")
        self.d.page(A, "05.02", F.page_text(other, self.d.receipt(other)))
        wo = self.d.work("O", A, "05.02", other)
        rego = self.d.registration([wo], name="rego.json")
        _, vo = self.d.read(rego)
        self.assertEqual((vo["works"][0]["pass_state"], vo["works"][0]["custody"]["role"]), ("no-return", "origin-mismatch"))
        self.assertIn("bound captured return", self.record(rego, F.fill(self.tmpl(vo), "accept-finished-open"), "o.json")[1])

    def test_06_replay_conflict_and_successor_lineage(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        _, v = self.d.read(reg)
        dec = F.fill(self.tmpl(v), "accept-finished-open")
        self.assertEqual(self.record(reg, dec, "d.json")[0], 0)
        before = tree(self.d.repo / w["review_location"])
        code, out, _ = self.record(reg, dec, "d.json")
        self.assertEqual((code, out.split()[0]), (0, "already-recorded"))
        changed = copy.deepcopy(dec)
        changed["judgment"]["finding"] = "A different finding under the same id."
        code, out, _ = self.record(reg, changed, "c.json")
        self.assertEqual(code, 2)
        self.assertIn("conflict", out)
        self.assertEqual(tree(self.d.repo / w["review_location"]), before)
        _, v2 = self.d.read(reg)
        succ = F.fill(self.tmpl(v2), "held")
        self.assertEqual(succ["supersedes"]["review_id"], "05.01-r1")
        self.assertEqual(self.record(reg, succ, "s.json")[0], 0)
        _, v3 = self.d.read(reg)
        it = v3["works"][0]
        self.assertEqual((it["latest_review"]["review_id"], it["disposition"], sorted(it["reviews"]["committed"])),
                         ("05.01-r2", "held", ["05.01-r1", "05.01-r2"]))
        no_sup = F.fill(self.tmpl(v3), "accept-finished-open")
        no_sup["supersedes"] = None
        self.assertIn("supersedes", self.record(reg, no_sup, "ns.json")[1])


class TestInterruption(Cycle):
    def test_07_partial_writes_never_read_as_finished_and_recover_explicitly(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        _, v = self.d.read(reg)
        dec = F.fill(self.tmpl(v), "accept-finished-open")
        for fail_on in ("record.json", "REVIEW.md", "COMMITTED.json"):
            with self.subTest(fail_on=fail_on):
                d = copy.deepcopy(dec)
                d["review_id"] = f"05.01-p-{fail_on[:6].lower().replace('.', '')}"
                path = self.d.write_decision(d, f"p-{fail_on}.json")
                real = pc.write_file

                def flaky(p, data, fail_on=fail_on):
                    if p.name == fail_on:
                        with open(p, "xb") as h:
                            h.write(data[: len(data) // 2])
                        raise OSError("injected interruption")
                    return real(p, data)
                with mock.patch.object(pc, "write_file", flaky):
                    with self.assertRaises(pc.PartialWrite):
                        pc.record(reg, path)
                _, rv = self.d.read(reg)
                it = rv["works"][0]
                self.assertEqual((it["pass_state"], it["disposition"]), ("awaiting-review", "unknown"))
                self.assertTrue(any(d["review_id"] in a and "partial" in a for a in it["attention"]))
                code, out, _ = self.record(reg, d, f"retry-{fail_on}.json")
                self.assertEqual(code, 2)
                self.assertIn("partial review present", out)
        code, out, _ = self.d.cli("inspect", "--registration", reg, "--work", "A")
        ins = json.loads(out)
        phases = {r["review_id"]: r["phase"] for r in ins["reviews"]}
        self.assertEqual(code, 1)
        self.assertEqual(phases, {"05.01-p-record": "partial-no-marker", "05.01-p-review": "partial-no-marker",
                                  "05.01-p-commit": "partial-marker-mismatch"})  # a torn marker is present but does not bind
        rec = copy.deepcopy(dec)
        rec["recovers"] = "05.01-p-review"
        self.assertEqual(self.record(reg, rec, "recover.json")[0], 0)
        _, rv = self.d.read(reg)
        self.assertEqual(rv["works"][0]["pass_state"], "reviewed")
        self.assertEqual(len(rv["works"][0]["reviews"]["partial"]), 3)
        tamper = self.d.repo / w["review_location"] / dec["review_id"] / "REVIEW.md"
        tamper.write_bytes(tamper.read_bytes() + b"edited\n")
        _, rv2 = self.d.read(reg)
        self.assertEqual(rv2["works"][0]["pass_state"], "awaiting-review")
        self.assertTrue(any("partial-marker-mismatch" in a for a in rv2["works"][0]["attention"]))


class TestCoverage(Cycle):
    def test_08_missing_legacy_unknown_worker_and_bounded_coverage(self):
        self.d.page(A, "05.03", F.page_text(None, review="Accepted within scope, 2026-10-30. Manual review prose."))
        w_none = self.d.work("N", A, "05.03", None)
        m, w = self.work_with_return(B, "05.01", wid="L", review="Accepted as a bounded lab helper. (legacy prose)")
        unreg_m = self.d.member("unreg", A, "05.09")
        self.d.page(A, "05.09", F.page_text(unreg_m, self.d.receipt(unreg_m)))
        reg = self.d.registration([w_none, w])
        code, v = self.d.read(reg)
        n, l = v["works"]
        self.assertEqual(n["pass_state"], "no-return")
        self.assertTrue(any(a.startswith("legacy-review-unmapped") for a in l["attention"]))
        self.assertIn("legacy prose", l["legacy_review_text"])
        self.assertEqual(l["disposition"], "unknown")
        self.assertEqual([x["work_id"] for x in v["works"]], ["N", "L"])
        text = json.dumps(v)
        self.assertNotIn("unreg", text)
        for word in ('"worker"', "available", "assigned_to"):
            self.assertNotIn(word, text)

    def test_08b_git_blob_basis_is_commit_bound(self):
        m, w = self.work_with_return()
        commit = self.d.commit()
        reg = self.d.registration([w], source={"kind": "git-blob", "commit": commit})
        _, v = self.d.read(reg)
        self.assertEqual(v["works"][0]["template"]["binding"]["source"]["commit"], commit)
        self.assertEqual(self.record(reg, F.fill(self.tmpl(v), "accept-finished-open"))[0], 0)
        self.d.page(A, "05.01", F.page_text(m, self.d.receipt(m), extra="\nLive edit after the commit."))
        _, v2 = self.d.read(reg)
        self.assertEqual(v2["works"][0]["pass_state"], "reviewed")


class TestSafety(Cycle):
    def test_09_unsafe_inputs_occupied_destinations_pin_drift_and_bounds(self):
        m, w = self.work_with_return()
        bad_works = {"outside-evidence": dict(w, review_location=f"{F.BOOK}/{A}/reviews"),
                     "other-lane": dict(w, review_location=f"{F.BOOK}/{B}/evidence/x"),
                     "dotdot": dict(w, review_location=f"{F.BOOK}/{A}/evidence/../../x"),
                     "page-shape": dict(w, page=f"{F.BOOK}/{A}/notes.md"),
                     "member-form": dict(w, member="9999.bad"),
                     "dup-id": None}
        for name, bw in bad_works.items():
            with self.subTest(case=name):
                works = [w, w] if bw is None else [bw]
                code, out = self.d.read(self.d.registration(works, name=f"bad-{name}.json"))
                self.assertEqual(code, 2, out)
                self.assertTrue(out.startswith("refused: "))
        reg = self.d.registration([w])
        raw = json.loads(reg.read_text())
        for name, change in {"unknown-key": dict(raw, extra=1), "schema": dict(raw, schema="prime-cycle-registration/2"),
                             "cap": dict(raw, bounds=dict(raw["bounds"], max_works=99)),
                             "output-in-review": dict(raw, output_root=str(self.d.repo / w["review_location"]))}.items():
            with self.subTest(reg=name):
                p = self.d.tmp / f"r-{name}.json"
                p.write_text(json.dumps(change))
                self.assertEqual(self.d.read(p)[0], 2)
        tdir = self.d.out / "templates"
        self.assertEqual(self.d.cli("read", "--registration", reg, "--templates", tdir)[0], 1)
        code, out, _ = self.d.cli("read", "--registration", reg, "--templates", tdir)
        self.assertEqual(code, 2)
        self.assertEqual(self.d.cli("read", "--registration", reg, "--templates", self.d.tmp / "elsewhere")[0], 2)
        tiny = self.d.registration([w], name="tiny.json", bounds={"max_works": 16, "max_page_bytes": 262144, "max_output_bytes": 100})
        self.assertEqual(self.d.read(tiny)[0], 2)
        small = self.d.registration([w], name="small.json", bounds={"max_works": 16, "max_page_bytes": 50, "max_output_bytes": 2097152})
        _, sv = self.d.read(small)
        self.assertTrue(any("max_page_bytes" in a for a in sv["works"][0]["attention"]))
        for dep in ("batch_observe", "prime_review", "return_inspect"):
            with self.subTest(drift=dep):
                labs = self.d.tmp / f"labs-{dep}"
                for name in ("batch-observation-pass01", "prime-review-pass01", "return-capture-pass01", "prime-support-pass01", "review-packet-pass01"):
                    shutil.copytree(F.LABS / name, labs / name, ignore=shutil.ignore_patterns("tests", "__pycache__", "examples", "evidence"))
                with open(labs / pc.PINS[dep][0], "ab") as h:
                    h.write(b"\n# drift\n")
                with mock.patch.object(pc, "LABS", labs), mock.patch.object(pc.subprocess, "run") as run:
                    with self.assertRaises(pc.Refusal):
                        if dep == "prime_review":
                            pc.run("prime_review", ["report"])
                        else:
                            pc.read(reg)
                    run.assert_not_called()

    def test_10_protected_sources_and_git_unchanged(self):
        m, w = self.work_with_return()
        commit = self.d.commit()
        live = self.d.repo / "00.kernel" / "00.live.md"
        live.write_bytes(b"protected\n")
        goal = self.d.book / "0401.goal" / "06.01.md"
        goal.parent.mkdir(parents=True)
        goal.write_bytes(b"record: current-assignment\n")
        page = self.d.repo / w["page"]
        member = self.d.book / m
        snap = lambda: (tree(member), page.read_bytes(), live.read_bytes(), goal.read_bytes(), self.d.git("rev-parse", "HEAD"),
                        self.d.git("diff", "--cached", "--name-only"))
        before = snap()
        reg = self.d.registration([w], source={"kind": "git-blob", "commit": commit})
        _, v = self.d.read(reg)
        self.record(reg, F.fill(self.tmpl(v), "accept-finished-open"))
        self.d.read(reg)
        self.assertEqual(snap(), before)
        self.assertEqual(self.d.git("rev-parse", "HEAD"), commit)

    def test_11_packet_uses_the_accepted_assembler_under_output_root(self):
        m, w = self.work_with_return()
        commit = self.d.commit()
        reg = self.d.registration([w], source={"kind": "git-blob", "commit": commit})
        code, out, err = self.d.cli("packet", "--registration", reg, "--work", "A", "--out", self.d.out / "packet-A")
        self.assertEqual((code, err), (0, ""), out)
        self.assertTrue((self.d.out / "packet-A" / "assembly-status.json").is_file())
        self.assertEqual(self.d.cli("packet", "--registration", reg, "--work", "A", "--out", self.d.tmp / "not-output")[0], 2)


class TestFullPath(Cycle):
    def test_12_read_fill_record_new_process_read_transcript(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        tdir = self.d.out / "t"
        transcript = []
        code, out, err = self.d.cli("read", "--registration", reg, "--templates", tdir)
        transcript.append(("read", code, out))
        tmpl = json.loads((tdir / "template-A.json").read_text(encoding="utf-8"))
        filled = F.fill(tmpl, "accept-finished-open")
        manual = [k for k, val in filled["judgment"].items() if tmpl["judgment"][k] != val] + ["attribution"]
        code, out, err = self.record(reg, filled)
        transcript.append(("record", code, out))
        code, out, err = self.d.cli("read", "--registration", reg)
        transcript.append(("read", code, out))
        self.assertEqual([t[1] for t in transcript], [1, 0, 0])
        self.assertIn("pass state: reviewed", transcript[2][2])
        self.assertIn("goal g1: open", transcript[2][2])
        self.assertIn("pass terminal: finished", transcript[2][2])
        self.assertGreater(len(manual), 3)
        self.assertNotIn("binding", manual)


if __name__ == "__main__":
    unittest.main()
