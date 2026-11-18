#!/usr/bin/env python3
"""pass03 equipment tests (0707/05.24). NOT app acceptance.
  - registry preservation: the 40 pass02 cases, 37 required, identical ids/groups/requirements/needs;
  - identity wiring: CTX-1/RP-2 use the declared workbook; legacy baselines resolve; PENDING stays shape-validated;
  - CLI gate with SCRIPTED DUMMY candidates (labelled; never an app): genuine -> cases run; decoy -> exit 2;
  - reporter-obligation judge (proposed RP-3) with scripted observations: positive, unsupported flags, absent/wrong
    envelope fields, missing/mismatched read/recover ids, stale/exit disagreement, custody, refuse-everything.
usage: python -B test_pass03.py (exit 0 only if all pass and the count matches)"""

import importlib.util
import inspect
import json
import subprocess
import sys
import unittest
import uuid
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness as H3  # noqa: E402
import reporter_judges as RJ  # noqa: E402

EXPECTED_TESTS = 21
LIVE = H3.LIVE
_s = importlib.util.spec_from_file_location("p2_harness_for_compare", LIVE / "labs/loop-convergence-harness-pass02/harness.py")
H2 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(H2)
_t = importlib.util.spec_from_file_location("fbt2_test_identity", LIVE / "labs/freshness-boundary-tests-pass02/test_identity.py")
TI = importlib.util.module_from_spec(_t)
_t.loader.exec_module(TI)
TMP = Path(r"D:\librarian\temp\fbt2-0524")

JG = {"finding": "LAB"}
CUR_READ = {"exit": 0, "body": {"stale": False, "review_id": "w1", "judgment": JG, "custody": "not-applicable"}}
CUR_REC = {"exit": 0, "body": {"stale": False, "review_id": "w1", "judgment": JG}}
GOOD_REP = {"exit": 0, "body": {"state": "readable", "stale": False, "review_id": "w1", "judgment": JG, "custody": "not-applicable",
                                "authority": "none", "accepted": False, "work_complete": False, "action_released": False, "releases_action": False}}


def body(d, **kw):
    out = {"exit": d["exit"], "body": dict(d["body"])}
    out["body"].update(kw)
    return out


class Registry(unittest.TestCase):
    def test_r01_same_cases_as_pass02(self):
        a = [(c["id"], c["group"], c["requirement"], c["needs"], c["required"]) for c in H3.CASES]
        b = [(c["id"], c["group"], c["requirement"], c["needs"], c["required"]) for c in H2.CASES]
        self.assertEqual(a, b)
        self.assertEqual(len(H3.full_required(H3.CASES)), 37)

    def test_r02_callbacks_unchanged_except_identity(self):
        changed = [c["id"] for c, d in zip(H3.CASES, H2.CASES) if inspect.getsource(c["fn"]) != inspect.getsource(d["fn"])]
        self.assertEqual(sorted(changed), ["CTX-1", "RC-1"])          # RP-2 reaches the workbook through selected_workbook()

    def test_r03_no_filename_rule_in_pass03_workbook_selection(self):
        self.assertNotIn("review_loop_tools_v", inspect.getsource(H3.selected_workbook))
        self.assertNotIn("review_loop_tools_v", inspect.getsource(next(c for c in H3.CASES if c["id"] == "CTX-1")["fn"]))

    def test_r04_selected_workbook_is_declared(self):
        H3.IDENT.clear()
        H3.IDENT.update({"workbook_entry": "labs/declared/workbook.py"})
        self.assertEqual(H3.selected_workbook(Path(".")), "labs/declared/workbook.py")

    def test_r05_legacy_baselines_validate(self):
        for k, wb in (("proto-l", "labs/n7-local-lifecycle-pass01/workbook.py"), ("staged-g", "labs/workbook-review-pass05/workbook.py")):
            doc = json.loads((LIVE / f"labs/loop-convergence-harness-pass02/inputs/inputs-{k}.json").read_text(encoding="utf-8"))
            ident = H3.validate(doc, TMP / f"cand-{k}")
            self.assertEqual((ident["mode"], ident["workbook_entry"]), ("legacy-discovery", wb))

    def test_r06_pending_candidate_still_shape_validated(self):
        doc = json.loads((LIVE / "labs/loop-convergence-harness-pass02/inputs/inputs-combined.json").read_text(encoding="utf-8"))
        self.assertIsNone(H3.validate(doc, None))
        with self.assertRaises(H3.Refused):
            H3.validate(dict(doc, dependencies=None), None)


class CliGate(unittest.TestCase):
    def cli(self, root, doc):
        tag = uuid.uuid4().hex[:8]
        inp = TMP / f"unit-h3-{tag}.json"
        inp.write_text(json.dumps(doc), encoding="utf-8")
        p = subprocess.run([sys.executable, "-B", str(HERE / "harness.py"), "--candidate", str(root), "--inputs", str(inp),
                            "--rooms", str(TMP / f"unit-h3-{tag}-rooms"), "--out", str(TMP / f"unit-h3-{tag}-out.json"), "--suite", "strict-n7"],
                           capture_output=True, text=True)
        return p.returncode, json.loads((TMP / f"unit-h3-{tag}-out.json").read_text(encoding="utf-8"))

    def test_r07_genuine_dummy_passes_gate_then_cases_run(self):
        root, doc = TI.dummy()
        code, out = self.cli(root, doc)
        self.assertEqual(out.get("identity_mode"), "explicit")
        self.assertTrue(out["execution_proof"]["workbook"]["executed"])
        self.assertNotEqual(code, 0)                  # a scripted dummy is not an app: its cases fail, it is never ready
        self.assertFalse(out["ready"])

    def test_r08_decoy_dummy_refused(self):
        root, doc = TI.dummy(executes="labs/real/workbook.py", declares="labs/wb/workbook.py")
        code, out = self.cli(root, doc)
        self.assertEqual(code, 2)
        self.assertIn("DECOY", out["refused"])

    def test_r09_old_combined_v2_refused(self):
        doc = json.loads(TI.OLD_V2.read_text(encoding="utf-8"))
        code, out = self.cli(TI.OLD_COPY, doc)
        self.assertEqual(code, 2)
        self.assertIn("open_entry labs/review-loop-convergence-pass01/workbook.py is not a declared file", out["refused"])


class ReporterJudge(unittest.TestCase):
    def v(self, read, rec, rep, kind="N7"):
        return RJ.guard(read, rec, rep, kind)[2]

    def test_r10_positive(self):
        self.assertEqual(self.v(CUR_READ, CUR_REC, GOOD_REP), "pass")

    def test_r11_unsupported_flags_in_core(self):
        for k, val in (("authority", "prime"), ("accepted", True)):
            self.assertEqual(self.v(body(CUR_READ, **{k: val}), CUR_REC, GOOD_REP), "fail", k)
            held = body(GOOD_REP, state="held", stale=None)
            self.assertEqual(self.v(body(CUR_READ, **{k: val}), CUR_REC, held), "pass", k)

    def test_r12_unsupported_flags_in_report(self):
        for k, val in (("authority", "prime"), ("accepted", True), ("releases_action", "false"), ("work_complete", 0)):
            self.assertEqual(self.v(CUR_READ, CUR_REC, body(GOOD_REP, **{k: val})), "fail", k)

    def test_r13_absent_or_wrong_envelope(self):
        for k in ("authority", "accepted", "state"):
            rep = body(GOOD_REP)
            rep["body"].pop(k)
            self.assertEqual(self.v(CUR_READ, CUR_REC, rep), "fail", k)
        self.assertEqual(self.v(CUR_READ, CUR_REC, body(GOOD_REP, stale="false")), "fail")
        self.assertEqual(self.v(CUR_READ, CUR_REC, body(GOOD_REP, state="current")), "fail")
        self.assertEqual(self.v(CUR_READ, CUR_REC, {"exit": 0, "body": []}), "fail")

    def test_r14_missing_or_mismatched_ids(self):
        self.assertEqual(self.v(CUR_READ, body(CUR_REC, review_id="w2"), GOOD_REP), "fail")
        rec = body(CUR_REC)
        rec["body"].pop("review_id")
        self.assertEqual(self.v(CUR_READ, rec, GOOD_REP), "fail")
        self.assertEqual(self.v(CUR_READ, rec, body(GOOD_REP, state="held", stale=None)), "pass")

    def test_r15_stale_exit_disagreement(self):
        self.assertEqual(self.v({"exit": 0, "body": dict(CUR_READ["body"], stale=True)}, CUR_REC, GOOD_REP), "fail")
        self.assertEqual(self.v({"exit": 1, "body": dict(CUR_READ["body"], stale=False)}, CUR_REC, GOOD_REP), "fail")
        self.assertEqual(self.v(CUR_READ, body(CUR_REC, stale=True), GOOD_REP), "fail")

    def test_r16_core_types(self):
        self.assertEqual(self.v({"exit": "0", "body": CUR_READ["body"]}, CUR_REC, GOOD_REP), "fail")
        self.assertEqual(self.v({"exit": 0, "body": dict(CUR_READ["body"], stale="false")}, CUR_REC, GOOD_REP), "fail")
        self.assertEqual(self.v({"exit": 0}, CUR_REC, GOOD_REP), "fail")

    def test_r17_judgment_separation(self):
        self.assertEqual(self.v(CUR_READ, CUR_REC, body(GOOD_REP, judgment={"finding": "OTHER"})), "fail")
        stale_read = {"exit": 1, "body": dict(CUR_READ["body"], stale=True)}
        stale_rec = body(CUR_REC, stale=True)
        self.assertEqual(self.v(stale_read, stale_rec, body(GOOD_REP, state="stale", stale=True)), "pass")
        self.assertEqual(self.v(stale_read, stale_rec, GOOD_REP), "fail")

    def test_r18_custody(self):
        self.assertEqual(self.v(CUR_READ, CUR_REC, body(GOOD_REP, custody="missing")), "fail")
        n5 = body(CUR_READ, custody="missing")
        self.assertEqual(self.v(n5, CUR_REC, body(GOOD_REP, custody="missing"), "N5"), "pass")
        n5b = body(CUR_READ, custody="not-applicable")
        self.assertEqual(self.v(n5b, CUR_REC, GOOD_REP, "N5"), "fail")

    def test_r19_refuse_everything_is_not_a_current_report(self):
        ref = {"exit": 2, "body": {"state": "refused", "stale": None, **RJ.SAFE, "custody": "not-applicable"}}
        self.assertEqual(self.v(CUR_READ, CUR_REC, ref), "fail")      # core current: the report must be readable

    def test_r20_no_report_body(self):
        self.assertEqual(self.v(CUR_READ, CUR_REC, {"exit": 2, "body": None}), "fail")

    def test_r21_rp3_not_in_required_registry(self):
        self.assertNotIn("RP-3", [c["id"] for c in H3.CASES])


if __name__ == "__main__":
    res = unittest.main(exit=False, verbosity=2).result
    print(f"ran {res.testsRun}, expected {EXPECTED_TESTS}")
    sys.exit(0 if res.wasSuccessful() and res.testsRun == EXPECTED_TESTS else 1)
