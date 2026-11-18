#!/usr/bin/env python3
"""Harness unit tests (0707/05.21): failed, blocked, unrun, crashed, malformed or pending input can never be READY.
These test the HARNESS aggregation, not the app. usage: python -B test_verdict.py  (exit 0 only if all pass)"""

import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from verdict import aggregate  # noqa: E402


def rec(cid, verdict="pass", required=True, **kw):
    r = {"id": cid, "group": "g", "requirement": "r", "required": required, "expected": "e", "observed": "o",
         "verdict": verdict, "evidence": "x", "provenance": "unit"}
    r.update(kw)
    return r


ACC = [{"id": "G", "status": "accepted"}]


class Aggregate(unittest.TestCase):
    def test_all_pass_is_ready(self):
        self.assertTrue(aggregate([rec("a"), rec("b")], ["a", "b"], ACC)["ready"])

    def test_fail_not_ready(self):
        self.assertFalse(aggregate([rec("a"), rec("b", "fail")], ["a", "b"], ACC)["ready"])

    def test_blocked_not_ready(self):
        self.assertFalse(aggregate([rec("a", "blocked")], ["a"], ACC)["ready"])

    def test_not_run_record_not_ready(self):
        self.assertFalse(aggregate([rec("a", "not-run")], ["a"], ACC)["ready"])

    def test_missing_record_is_not_run(self):
        out = aggregate([rec("a")], ["a", "b"], ACC)
        self.assertFalse(out["ready"])
        self.assertTrue(any("b has no record" in x for x in out["reasons"]))

    def test_error_anywhere_not_ready(self):
        self.assertFalse(aggregate([rec("a"), rec("x", "error", required=False)], ["a"], ACC)["ready"])

    def test_known_failure_never_counts_as_pass(self):
        self.assertFalse(aggregate([rec("a", "known-failure-reproduced")], ["a"], ACC)["ready"])

    def test_unknown_verdict_not_ready(self):
        self.assertFalse(aggregate([rec("a", "PASS")], ["a"], ACC)["ready"])
        self.assertFalse(aggregate([rec("a", "ok")], ["a"], ACC)["ready"])

    def test_missing_field_not_ready(self):
        r = rec("a")
        del r["evidence"]
        self.assertFalse(aggregate([r], ["a"], ACC)["ready"])

    def test_pending_dependency_not_ready(self):
        self.assertFalse(aggregate([rec("a")], ["a"], [{"id": "K", "status": "pending"}])["ready"])

    def test_malformed_dependency_not_ready(self):
        self.assertFalse(aggregate([rec("a")], ["a"], [{"id": "K"}])["ready"])

    def test_empty_suite_not_ready(self):
        self.assertFalse(aggregate([], [], ACC)["ready"])

    def test_required_flag_mismatch_not_ready(self):
        self.assertFalse(aggregate([rec("a", required=False)], ["a"], ACC)["ready"])

    def test_undeclared_required_record_not_ready(self):
        self.assertFalse(aggregate([rec("a"), rec("z")], ["a"], ACC)["ready"])

    def test_duplicate_ids_not_ready(self):
        self.assertFalse(aggregate([rec("a"), rec("a")], ["a"], ACC)["ready"])

    def test_records_not_a_list_not_ready(self):
        self.assertFalse(aggregate({"a": rec("a")}, ["a"], ACC)["ready"])


if __name__ == "__main__":
    res = unittest.main(exit=False, verbosity=2).result
    sys.exit(0 if res.wasSuccessful() and res.testsRun == 16 else 1)
