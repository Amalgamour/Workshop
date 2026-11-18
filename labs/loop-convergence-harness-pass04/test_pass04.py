#!/usr/bin/env python3
"""pass04 equipment tests (0707/05.25). NOT app acceptance. Labelled SCRIPTED fixtures and dummies only.
  registry: the 37 required ids/groups/needs/requirements equal pass02's; DD-1..4 are non-required; the changed
            callbacks are exactly N5-1..3, PR-7, CTX-1, RC-1 (vs pass03);
  N5 fixtures: v7 closure install (added / present / collision), baseline_ok, field-by-field explanation;
  RC-1: run_builder with a clean dummy builder, a side-effect dummy builder and an occupied output root;
  reporter v2: Prime's three controlled observations, positives, held reports, wrong types; pass03 judge untouched.
usage: python -B test_pass04.py (exit 0 only if all pass and the count matches)"""

import hashlib
import importlib.util
import inspect
import json
import sys
import unittest
import uuid
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness as H4  # noqa: E402
import reporter_judges2 as RJ2  # noqa: E402

EXPECTED_TESTS = 17
LIVE = H4.LIVE
TMP = Path(r"D:\librarian\temp\fbt3-0525")


def load(name, rel):
    s = importlib.util.spec_from_file_location(name, LIVE / rel)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


H2 = load("h2_cmp", "labs/loop-convergence-harness-pass02/harness.py")
H3 = load("h3_cmp", "labs/loop-convergence-harness-pass03/harness.py")
JG = {"finding": "LAB"}
READ = {"exit": 0, "body": {"stale": False, "review_id": "w1", "judgment": JG, "custody": "not-applicable"}}
REC = {"exit": 0, "body": {"stale": False, "review_id": "w1", "judgment": JG}}
INS = {"exit": 0, "body": {"current": "w1", "stale": False, "publication": {"review_id": "w1", "status": "published"}}}
PREP = {"exit": 0, "body": {"measurement": "complete"}}
REP = {"exit": 0, "body": {"state": "readable", "stale": False, "review_id": "w1", "judgment": JG, "custody": "not-applicable", **RJ2.SAFE}}
HELD = {"exit": 0, "body": {"state": "held", "stale": None, "custody": "not-applicable", **RJ2.SAFE}}


def mod(d, **kw):
    return {"exit": kw.pop("exit", d["exit"]), "body": dict(d["body"], **kw)}


class Registry(unittest.TestCase):
    def test_t01_required_set_equals_pass02(self):
        a = [(c["id"], c["group"], c["requirement"], c["needs"]) for c in H4.CASES if c["required"]]
        b = [(c["id"], c["group"], c["requirement"], c["needs"]) for c in H2.CASES if c["required"]]
        self.assertEqual(a, b)
        self.assertEqual(len(a), 37)

    def test_t02_proposed_doors_not_required(self):
        self.assertEqual([c["id"] for c in H4.CASES if c["group"] == "door-proposed"], ["DD-1", "DD-2", "DD-3", "DD-4"])
        self.assertTrue(all(not c["required"] for c in H4.CASES if c["group"] == "door-proposed"))

    def test_t03_changed_callbacks_vs_pass03(self):
        old = {c["id"]: inspect.getsource(c["fn"]) for c in H3.CASES}
        changed = sorted(c["id"] for c in H4.CASES if c["id"] in old and inspect.getsource(c["fn"]) != old[c["id"]])
        self.assertEqual(changed, ["CTX-1", "N5-1", "N5-2", "N5-3", "PR-7", "RC-1"])


class Fixtures(unittest.TestCase):
    def test_t04_closure_added_then_present(self):
        root = TMP / f"unit-closure-{uuid.uuid4().hex[:8]}"
        root.mkdir(parents=True)
        a = H4.install_v7_closure(root)
        self.assertEqual(len(a["added"]), 18)
        self.assertIn("labs/workbook-review-pass03/forms/workbook-review-v1.json", a["added"])
        b = H4.install_v7_closure(root)
        self.assertEqual((len(b["present"]), b["added"]), (18, []))

    def test_t05_closure_collision_recorded_not_overwritten(self):
        root = TMP / f"unit-closure-{uuid.uuid4().hex[:8]}"
        f = root / "labs/workbook-review-pass03/forms/workbook-review-v1.json"
        f.parent.mkdir(parents=True)
        f.write_bytes(b"{}\n")
        a = H4.install_v7_closure(root)
        self.assertIn("labs/workbook-review-pass03/forms/workbook-review-v1.json", a["collisions"])
        self.assertEqual(f.read_bytes(), b"{}\n")

    def test_t06_baseline_ok_and_explain(self):
        self.assertFalse(H4.baseline_ok({"exit": 2, "measurement": None, "intake_id": None}))
        self.assertFalse(H4.baseline_ok({"exit": 0, "measurement": None, "intake_id": "x"}))
        self.assertTrue(H4.baseline_ok({"exit": 0, "measurement": "complete", "intake_id": "x"}))
        d = H4.explain({"codes": ["a"], "rows_sha": "1"}, {"codes": ["a", "b"], "rows_sha": "1"}, ("codes", "rows_sha"))
        self.assertEqual(d["codes"]["only_candidate"], ["b"])
        self.assertNotIn("rows_sha", d)


BUILDER_CLEAN = 'import argparse, pathlib\na = argparse.ArgumentParser(); a.add_argument("--root"); r = pathlib.Path(a.parse_args().root)\nr.mkdir(parents=True)\n(r / "x.txt").write_text("built")\n'
BUILDER_DIRTY = BUILDER_CLEAN + '(pathlib.Path(__file__).parent / "scratch.txt").write_text("side effect")\n'


class Builder(unittest.TestCase):
    def mk(self, src):
        d = TMP / f"unit-builder-{uuid.uuid4().hex[:8]}"
        d.mkdir(parents=True)
        (d / "make_candidate.py").write_text(src, encoding="utf-8")
        return d

    def test_t07_clean_builder(self):
        d = self.mk(BUILDER_CLEAN)
        out = d.parent / (d.name + "-out")
        r = H4.run_builder(d / "make_candidate.py", [], out, [d])
        self.assertEqual((r["exit"], r["side_effects"]), (0, []))
        self.assertTrue((out / "x.txt").is_file())

    def test_t08_side_effect_reported(self):
        d = self.mk(BUILDER_DIRTY)
        r = H4.run_builder(d / "make_candidate.py", [], d.parent / (d.name + "-out"), [d])
        self.assertEqual(r["side_effects"], [f"{d}/scratch.txt: created"])

    def test_t09_occupied_output_refused(self):
        d = self.mk(BUILDER_CLEAN)
        out = d.parent / (d.name + "-out")
        out.mkdir()
        self.assertIn("occupied", H4.run_builder(d / "make_candidate.py", [], out, [d])["why"])


class Reporter(unittest.TestCase):
    def v(self, ins=INS, prep=PREP, rep=REP, read=READ, rec=REC, kind="N7"):
        return RJ2.guard_v2(read, rec, ins, prep, rep, kind)[2]

    def test_t10_positive(self):
        self.assertEqual(self.v(), "pass")

    def test_t11_inspect_current_differs(self):
        self.assertEqual(self.v(ins=mod(INS, current="w2")), "fail")
        self.assertEqual(self.v(ins=mod(INS, current="w2"), rep=HELD), "pass")

    def test_t12_inspect_stale(self):
        self.assertEqual(self.v(ins=mod(INS, stale=True)), "fail")
        self.assertEqual(self.v(ins=mod(INS, stale="false")), "fail")
        self.assertEqual(self.v(ins=mod(INS, stale=True), rep=HELD), "pass")

    def test_t13_prepare_nonzero_complete(self):
        self.assertEqual(self.v(prep=mod(PREP, exit=1)), "fail")
        self.assertEqual(self.v(prep=mod(PREP, exit=1), rep=HELD), "pass")

    def test_t14_inspect_and_prepare_types(self):
        self.assertEqual(self.v(ins={"exit": "0", "body": INS["body"]}), "fail")
        self.assertEqual(self.v(ins={"exit": 0, "body": None}), "fail")
        self.assertEqual(self.v(prep={"exit": None, "body": PREP["body"]}), "fail")
        self.assertEqual(self.v(prep=mod(PREP, measurement="incomplete")), "fail")
        ins = {"exit": 0, "body": {"stale": False}}
        self.assertEqual(self.v(ins=ins), "fail")

    def test_t15_held_never_current_and_custody(self):
        self.assertEqual(self.v(rep=HELD), "fail")                      # no anomaly: the core is current, report must be readable
        self.assertEqual(self.v(rep=mod(REP, custody="missing")), "fail")

    def test_t16_pass03_judge_unchanged(self):
        row = {r["path"]: r for r in json.loads((LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.25/source-manifest.json").read_bytes())["files"]}
        rel = "labs/loop-convergence-harness-pass03/reporter_judges.py"
        self.assertEqual(hashlib.sha256((LIVE / rel).read_bytes()).hexdigest(), row[rel]["sha256"])
        self.assertEqual(RJ2.RJ.guard(READ, REC, REP, "N7")[2], "pass")

    def test_t17_rp3_not_in_registry(self):
        self.assertNotIn("RP-3", [c["id"] for c in H4.CASES])


if __name__ == "__main__":
    res = unittest.main(exit=False, verbosity=2).result
    print(f"ran {res.testsRun}, expected {EXPECTED_TESTS}")
    sys.exit(0 if res.wasSuccessful() and res.testsRun == EXPECTED_TESTS else 1)
