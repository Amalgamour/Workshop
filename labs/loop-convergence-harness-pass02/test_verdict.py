#!/usr/bin/env python3
"""Harness-unit tests for the successor aggregation and coverage (0707/05.22). These test the HARNESS, not the app.
U01-U16 are the pass01 author cases, reconciled to the successor signature (aggregate(records, full_required, deps)).
U17+ are new: malformed dependency collections (06.21 H2) and partial coverage with ALL dependencies synthetically
accepted (06.21 H4), so pending rows cannot hide a coverage bug. usage: python -B test_verdict.py (exit 0 only if all pass)"""

import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from verdict import aggregate  # noqa: E402
import harness  # noqa: E402

EXPECTED_TESTS = 40


def rec(cid, verdict="pass", required=True, **kw):
    r = {"id": cid, "group": "g", "requirement": "r", "required": required, "expected": "e", "observed": "o",
         "verdict": verdict, "evidence": "x", "provenance": "unit"}
    r.update(kw)
    return r


ACC = [{"id": "G", "status": "accepted", "required": True}]
ALL_ACC = [{"id": d, "status": "accepted", "required": True} for d in ("G", "L", "K", "I", "R", "W")]


class Inherited(unittest.TestCase):
    """pass01 U01-U16, same intent; ACC rows now carry the explicit boolean 'required' the successor demands."""

    def test_u01_all_pass_is_ready(self):
        self.assertTrue(aggregate([rec("a"), rec("b")], ["a", "b"], ACC)["ready"])

    def test_u02_fail_not_ready(self):
        self.assertFalse(aggregate([rec("a"), rec("b", "fail")], ["a", "b"], ACC)["ready"])

    def test_u03_blocked_not_ready(self):
        self.assertFalse(aggregate([rec("a", "blocked")], ["a"], ACC)["ready"])

    def test_u04_not_run_record_not_ready(self):
        self.assertFalse(aggregate([rec("a", "not-run")], ["a"], ACC)["ready"])

    def test_u05_missing_record_is_not_run(self):
        out = aggregate([rec("a")], ["a", "b"], ACC)
        self.assertFalse(out["ready"])
        self.assertEqual(out["coverage_missing"], ["b"])

    def test_u06_error_anywhere_not_ready(self):
        self.assertFalse(aggregate([rec("a"), rec("x", "error", required=False)], ["a"], ACC)["ready"])

    def test_u07_known_failure_never_counts_as_pass(self):
        self.assertFalse(aggregate([rec("a", "known-failure-reproduced")], ["a"], ACC)["ready"])

    def test_u08_unknown_verdict_not_ready(self):
        self.assertFalse(aggregate([rec("a", "PASS")], ["a"], ACC)["ready"])
        self.assertFalse(aggregate([rec("a", "ok")], ["a"], ACC)["ready"])

    def test_u09_missing_field_not_ready(self):
        r = rec("a")
        del r["evidence"]
        self.assertFalse(aggregate([r], ["a"], ACC)["ready"])

    def test_u10_pending_dependency_not_ready(self):
        self.assertFalse(aggregate([rec("a")], ["a"], [{"id": "K", "status": "pending", "required": True}])["ready"])

    def test_u11_malformed_dependency_not_ready(self):
        self.assertFalse(aggregate([rec("a")], ["a"], [{"id": "K"}])["ready"])

    def test_u12_empty_suite_not_ready(self):
        self.assertFalse(aggregate([], [], ACC)["ready"])

    def test_u13_required_flag_mismatch_not_ready(self):
        self.assertFalse(aggregate([rec("a", required=False)], ["a"], ACC)["ready"])

    def test_u14_undeclared_required_record_not_ready(self):
        self.assertFalse(aggregate([rec("a"), rec("z")], ["a"], ACC)["ready"])

    def test_u15_duplicate_ids_not_ready(self):
        self.assertFalse(aggregate([rec("a"), rec("a")], ["a"], ACC)["ready"])

    def test_u16_records_not_a_list_not_ready(self):
        self.assertFalse(aggregate({"a": rec("a")}, ["a"], ACC)["ready"])


class MalformedDependencies(unittest.TestCase):
    """06.21 H2: Prime's direct probes (None, {}, 'not-a-list') returned ready true under pass01."""

    def _nr(self, deps, needle):
        out = aggregate([rec("a")], ["a"], deps)
        self.assertFalse(out["ready"], deps)
        self.assertTrue(any(needle in x for x in out["reasons"]), out["reasons"])

    def test_u17_none(self):
        self._nr(None, "dependencies is not a list")

    def test_u18_dict(self):
        self._nr({}, "dependencies is not a list")

    def test_u19_string(self):
        self._nr("not-a-list", "dependencies is not a list")

    def test_u20_empty_list(self):
        self._nr([], "no dependency rows")

    def test_u21_row_not_object(self):
        self._nr(["G"], "malformed dependency row")

    def test_u22_required_not_boolean(self):
        self._nr([{"id": "G", "status": "accepted", "required": "true"}], "boolean 'required'")
        self._nr([{"id": "G", "status": "accepted", "required": 1}], "boolean 'required'")
        self._nr([{"id": "G", "status": "accepted"}], "boolean 'required'")

    def test_u23_duplicate_dependency(self):
        self._nr(ACC + ACC, "duplicate dependency")

    def test_u24_unknown_status(self):
        self._nr([{"id": "G", "status": "Accepted", "required": True}], "unknown status")

    def test_u25_empty_id(self):
        self._nr([{"id": "", "status": "accepted", "required": True}], "malformed dependency row")

    def test_u26_full_required_wrong_shape(self):
        for bad in (None, {}, "a", ["a", "a"], ["a", 3]):
            self.assertFalse(aggregate([rec("a")], bad, ACC)["ready"], bad)


class Coverage(unittest.TestCase):
    """06.21 H4: with EVERY dependency synthetically accepted, a passing subset is still not readiness."""

    def test_u27_subset_all_pass_not_ready(self):
        out = aggregate([rec("a"), rec("b")], ["a", "b", "c", "d"], ALL_ACC, selected_required=["a", "b"])
        self.assertFalse(out["ready"])
        self.assertEqual(out["scope"], "subset")
        self.assertTrue(out["subset"]["all_selected_required_pass"])
        self.assertEqual(out["coverage_missing"], ["c", "d"])

    def test_u28_full_with_all_accepted_is_ready_control(self):
        out = aggregate([rec("a"), rec("b")], ["a", "b"], ALL_ACC, selected_required=["a", "b"])
        self.assertTrue(out["ready"])
        self.assertEqual(out["scope"], "full")

    def test_u29_selected_outside_baseline(self):
        self.assertFalse(aggregate([rec("a"), rec("q")], ["a"], ALL_ACC, selected_required=["a", "q"])["ready"])

    def test_u30_selected_wrong_shape(self):
        self.assertFalse(aggregate([rec("a")], ["a"], ALL_ACC, selected_required="a")["ready"])


def fake_registry(results):
    reg = []
    for i, (cid, group, verdict) in enumerate(results):
        reg.append({"id": cid, "group": group, "requirement": "unit", "needs": ["G"], "required": True,
                    "fn": (lambda v: (lambda ctx: ("e", "o", v)))(verdict)})
    return reg


class Driver(unittest.TestCase):
    """The real harness driver (select/run_cases/decide) over a FAKE registry with all dependencies accepted.
    Harness-unit only: the fake case functions do not run any app."""

    def _run(self, reg, suite):
        sel = harness.select(reg, suite)
        with tempfile.TemporaryDirectory() as d:
            recs = harness.run_cases(sel, ALL_ACC, object(), Path(d), {"kind": "unit"})
        return harness.decide(reg, sel, recs, ALL_ACC)

    def test_u31_full_suite_all_pass_exit0(self):
        agg, code = self._run(fake_registry([("c1", "g1", "pass"), ("c2", "g2", "pass")]), "all")
        self.assertEqual((agg["ready"], code), (True, 0))

    def test_u32_subset_pass_exit4_not_ready(self):
        agg, code = self._run(fake_registry([("c1", "g1", "pass"), ("c2", "g2", "pass")]), "g1")
        self.assertEqual((agg["ready"], code, agg["coverage_missing"]), (False, 4, ["c2"]))

    def test_u33_subset_fail_exit1(self):
        agg, code = self._run(fake_registry([("c1", "g1", "fail"), ("c2", "g2", "pass")]), "g1")
        self.assertEqual((agg["ready"], code), (False, 1))

    def test_u34_full_with_one_fail_exit1(self):
        agg, code = self._run(fake_registry([("c1", "g1", "pass"), ("c2", "g2", "fail")]), "all")
        self.assertEqual((agg["ready"], code), (False, 1))

    def test_u35_unknown_group_refused(self):
        with self.assertRaises(harness.Refused):
            harness.select(fake_registry([("c1", "g1", "pass")]), "nope")
        with self.assertRaises(harness.Refused):
            harness.select(fake_registry([("c1", "g1", "pass")]), "")

    def test_u36_pending_dep_blocks_case_and_readiness(self):
        reg = fake_registry([("c1", "g1", "pass")])
        deps = [dict(d, status="pending") if d["id"] == "G" else d for d in ALL_ACC]
        with tempfile.TemporaryDirectory() as d:
            recs = harness.run_cases(reg, deps, object(), Path(d), {})
        agg, code = harness.decide(reg, reg, recs, deps)
        self.assertEqual((recs[0]["verdict"], agg["ready"], code), ("blocked", False, 1))

    def test_u37_crash_is_error_not_ready(self):
        reg = fake_registry([("c1", "g1", "pass")])
        reg[0]["fn"] = lambda ctx: 1 / 0
        with tempfile.TemporaryDirectory() as d:
            recs = harness.run_cases(reg, ALL_ACC, object(), Path(d), {})
        agg, code = harness.decide(reg, reg, recs, ALL_ACC)
        self.assertEqual((recs[0]["verdict"], agg["ready"], code), ("error", False, 1))

    def test_u38_real_registry_baseline_is_immutable(self):
        full = harness.full_required(harness.CASES)
        self.assertEqual(len(full), 37)
        self.assertEqual(harness.full_required(harness.select(harness.CASES, "capacity")), ["CAP-0", "CAP-1", "CAP-2", "CAP-3", "CAP-4"])
        self.assertEqual(harness.full_required(harness.CASES), full)

    def test_u39_real_registry_subset_all_pass_not_ready(self):
        sel = harness.select(harness.CASES, "capacity")
        recs = [rec(c["id"], "pass", required=c["required"]) for c in sel]
        agg, code = harness.decide(harness.CASES, sel, recs, ALL_ACC)
        self.assertEqual((agg["ready"], code, len(agg["coverage_missing"])), (False, 4, 32))

    def test_u40_no_stub_returns_not_run(self):
        import inspect
        for cid in ("CAP-4", "RP-1", "RP-2", "IN-2"):
            src = inspect.getsource(next(c for c in harness.CASES if c["id"] == cid)["fn"])
            self.assertNotIn('"not-run"', src, cid)


if __name__ == "__main__":
    res = unittest.main(exit=False, verbosity=2).result
    print(f"ran {res.testsRun}, expected {EXPECTED_TESTS}")
    sys.exit(0 if res.wasSuccessful() and res.testsRun == EXPECTED_TESTS else 1)
