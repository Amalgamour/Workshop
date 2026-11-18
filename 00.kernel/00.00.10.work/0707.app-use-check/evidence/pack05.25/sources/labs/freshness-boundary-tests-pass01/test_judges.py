#!/usr/bin/env python3
"""Equipment tests (0707/05.23): judges and the identity gate. These test the TEST EQUIPMENT, never the app.
Every judge gets positive, negative, absent-field, wrong-type and refuse-everything observations.
usage: python -B test_judges.py (exit 0 only if all pass and the count matches)"""

import copy
import json
import shutil
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import judges as J  # noqa: E402
import run as R  # noqa: E402

EXPECTED_TESTS = 30
JG = R.JUDGMENT
CUR = {"exit": 0, "stale": False, "judgment": JG, "message": "", "stderr": ""}
STALE = {"exit": 1, "stale": True, "judgment": JG, "message": "", "stderr": ""}
REF = {"exit": 2, "stale": None, "judgment": None, "message": "refused: stored intake is not strict json", "stderr": "refused"}
CRASH = {"exit": 1, "stale": None, "judgment": None, "message": "", "stderr": "Traceback (most recent call last):\n boom"}
EVERYTHING_REFUSED = {"exit": 2, "stale": None, "judgment": None, "message": "refused", "stderr": "refused"}


def m_good(variant):
    o = {"record_exit": 0, "control_read": CUR, "after_read": STALE, "after_recover": {"exit": 0, "judgment": JG},
         "publish": REF, "destination_created": False}
    if variant == "M1":
        o["restored_read"] = CUR
    return o


class Meanings(unittest.TestCase):
    def test_t01_meanings(self):
        self.assertTrue(J.is_current(CUR))
        self.assertTrue(J.not_current(STALE) and J.not_current(REF))
        self.assertFalse(J.not_current(CRASH) or J.is_current(CRASH))

    def test_t02_wrong_types(self):
        self.assertFalse(J.is_current({"exit": False, "stale": False}))       # bool is not an exit
        self.assertFalse(J.is_current({"exit": 0, "stale": "false"}))
        self.assertFalse(J.not_current({"exit": "2"}))
        self.assertFalse(J.not_current({"exit": 0, "stale": "true"}))
        self.assertFalse(J.not_current(None) or J.is_current([]))


class Missing(unittest.TestCase):
    def test_t03_positive_each_variant(self):
        for v in ("M0", "M1", "M2", "M3", "M4"):
            self.assertEqual(J.missing(m_good(v), v, JG)[2], "pass", v)

    def test_t04_reads_current_after_change_fails(self):
        for v in ("M0", "M1", "M2", "M3", "M4"):
            self.assertEqual(J.missing(dict(m_good(v), after_read=CUR), v, JG)[2], "fail", v)

    def test_t05_crash_is_not_a_hold(self):
        self.assertEqual(J.missing(dict(m_good("M4"), after_read=CRASH, after_recover=CRASH), "M4", JG)[2], "fail")

    def test_t06_refuse_everything_fails(self):
        o = {"record_exit": 2, "control_read": EVERYTHING_REFUSED, "after_read": EVERYTHING_REFUSED, "after_recover": EVERYTHING_REFUSED,
             "publish": EVERYTHING_REFUSED, "destination_created": False, "restored_read": EVERYTHING_REFUSED}
        for v in ("M0", "M1", "M2", "M3", "M4"):
            self.assertEqual(J.missing(o, v, JG)[2], "fail", v)

    def test_t07_publish_succeeds_fails(self):
        self.assertEqual(J.missing(dict(m_good("M1"), publish=CUR, destination_created=True), "M1", JG)[2], "fail")

    def test_t08_history_lost_without_message_fails(self):
        o = dict(m_good("M1"), after_read={"exit": 2, "stale": None, "judgment": None, "message": " ", "stderr": ""},
                 after_recover={"exit": 2, "judgment": None})
        self.assertEqual(J.missing(o, "M1", JG)[2], "fail")

    def test_t09_clean_refusal_with_message_keeps_history_rule(self):
        self.assertEqual(J.missing(dict(m_good("M4"), after_read=REF, after_recover=REF), "M4", JG)[2], "pass")

    def test_t10_restore_required_for_m1(self):
        o = m_good("M1")
        o.pop("restored_read")
        self.assertEqual(J.missing(o, "M1", JG)[2], "fail")

    def test_t11_absent_fields_fail(self):
        for k in ("control_read", "after_read", "publish", "destination_created", "record_exit"):
            o = m_good("M3")
            o.pop(k)
            self.assertEqual(J.missing(o, "M3", JG)[2], "fail", k)

    def test_t12_m5(self):
        good = {"prepare_measurement": "complete", "after_read": REF, "publish": REF, "destination_created": False}
        self.assertEqual(J.missing(good, "M5", JG)[2], "pass")
        self.assertEqual(J.missing(dict(good, after_read=CUR), "M5", JG)[2], "fail")
        self.assertEqual(J.missing(dict(good, prepare_measurement="incomplete"), "M5", JG)[2], "fail")


class Region(unittest.TestCase):
    def test_t13_positive(self):
        self.assertEqual(J.region({"reached": True, "pre_read": CUR, "post_read": CUR}, "current")[2], "pass")
        self.assertEqual(J.region({"reached": True, "pre_read": CUR, "post_read": STALE}, "not-current")[2], "pass")

    def test_t14_negative(self):
        self.assertEqual(J.region({"reached": True, "pre_read": CUR, "post_read": STALE}, "current")[2], "fail")
        self.assertEqual(J.region({"reached": True, "pre_read": CUR, "post_read": CUR}, "not-current")[2], "fail")

    def test_t15_not_reached_is_never_credited(self):
        self.assertEqual(J.region({"reached": False}, "not-current")[2], "not-reached")
        self.assertEqual(J.region({}, "not-current")[2], "not-reached")
        self.assertEqual(J.region({"reached": "yes", "pre_read": CUR, "post_read": STALE}, "not-current")[2], "not-reached")

    def test_t16_refuse_everything_fails(self):
        self.assertEqual(J.region({"reached": True, "pre_read": EVERYTHING_REFUSED, "post_read": EVERYTHING_REFUSED}, "not-current")[2], "fail")

    def test_t17_absent_post_and_bad_expectation(self):
        self.assertEqual(J.region({"reached": True, "pre_read": CUR}, "not-current")[2], "fail")
        self.assertEqual(J.region({"reached": True, "pre_read": CUR, "post_read": STALE}, "stale")[2], "fail")


class Composition(unittest.TestCase):
    def test_t18_instance(self):
        good = {"a_read_before": CUR, "b_read": STALE, "a_read_after": CUR, "a_unchanged": True}
        self.assertEqual(J.instance(good)[2], "pass")
        self.assertEqual(J.instance(dict(good, b_read=CUR))[2], "fail")
        self.assertEqual(J.instance(dict(good, a_unchanged="yes"))[2], "fail")
        self.assertEqual(J.instance({k: EVERYTHING_REFUSED for k in good} | {"a_unchanged": True})[2], "fail")

    def test_t19_n7_body(self):
        good = {"pre_read": CUR, "review_edit_read": CUR, "task_edit_read": STALE}
        self.assertEqual(J.n7_body(good)[2], "pass")
        self.assertEqual(J.n7_body(dict(good, review_edit_read=STALE))[2], "fail")
        self.assertEqual(J.n7_body(dict(good, task_edit_read=CUR))[2], "fail")
        self.assertEqual(J.n7_body({k: EVERYTHING_REFUSED for k in good})[2], "fail")
        self.assertEqual(J.n7_body({})[2], "fail")

    def test_t20_row_change(self):
        self.assertEqual(J.row_change({"pre_read": CUR, "post_read": STALE})[2], "pass")
        self.assertEqual(J.row_change({"pre_read": CUR, "post_read": CUR})[2], "fail")
        self.assertEqual(J.row_change({"pre_read": EVERYTHING_REFUSED, "post_read": EVERYTHING_REFUSED})[2], "fail")
        self.assertEqual(J.row_change({"pre_read": CUR, "post_read": CRASH})[2], "fail")


# ------------------------------------------------------------------ identity gate (refusal before execution)
CAND = Path(r"D:\librarian\temp\fbt-0523\cand-proto-l")
IDENT = json.loads((R.LIVE / "labs/loop-convergence-harness-pass02/inputs/inputs-proto-l.json").read_text(encoding="utf-8"))


class Identity(unittest.TestCase):
    def refused(self, doc, root=CAND, needle=""):
        with self.assertRaises(R.Refused) as cm:
            R.verify(doc, root)
        self.assertIn(needle, str(cm.exception))

    def test_t21_control_verifies(self):
        self.assertEqual(R.verify(copy.deepcopy(IDENT), CAND)["kind"], "proto-l")

    def test_t22_dependencies_wrong_shape(self):
        for bad in (None, {}, "G,L"):
            self.refused(dict(copy.deepcopy(IDENT), dependencies=bad), needle="malformed")

    def test_t23_pending_candidate(self):
        self.refused(dict(copy.deepcopy(IDENT), candidate="PENDING"), needle="PENDING")

    def test_t24_root_inside_live_repo(self):
        self.refused(copy.deepcopy(IDENT), root=R.LIVE, needle="inside the live repo")

    def test_t25_wrong_candidate_json(self):
        d = copy.deepcopy(IDENT)
        d["candidate"]["candidate_json_sha256"] = "0" * 64
        self.refused(d, needle="CANDIDATE.json")

    def test_t26_entry_not_declared(self):
        d = copy.deepcopy(IDENT)
        d["candidate"]["files"] = [f for f in d["candidate"]["files"] if f["path"] != "app/librarian.py"]
        self.refused(d, needle="entry")

    def test_t27_tampered_file(self):
        tmp = Path(r"D:\librarian\temp\fbt-0523\test-identity-tamper")
        if tmp.exists():
            shutil.rmtree(tmp)
        shutil.copytree(CAND, tmp)
        f = tmp / "app/review_loop_tools_v8.py"
        f.write_bytes(f.read_bytes() + b"\n# tamper\n")
        self.refused(copy.deepcopy(IDENT), root=tmp, needle="candidate file differs")

    def test_t28_accepted_dep_wrong_review(self):
        d = copy.deepcopy(IDENT)
        next(x for x in d["dependencies"] if x["id"] == "G")["review_ref"]["sha256"] = "0" * 64
        self.refused(d, needle="accepted dependency G differs")

    def test_t29_status_promotion_refused(self):
        d = copy.deepcopy(IDENT)
        next(x for x in d["dependencies"] if x["id"] == "K")["status"] = "accepted"
        self.refused(d, needle="malformed")

    def test_t30_case_registry_shape(self):
        ids = [c["id"] for c in R.CASES]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual([c["id"] for c in R.CASES if not c["required"]], ["F4", "D1"])


if __name__ == "__main__":
    res = unittest.main(exit=False, verbosity=2).result
    print(f"ran {res.testsRun}, expected {EXPECTED_TESTS}")
    sys.exit(0 if res.wasSuccessful() and res.testsRun == EXPECTED_TESTS else 1)
