#!/usr/bin/env python3
"""Harness-unit tests: inputs-manifest shape refusal (0707/05.22, 06.21 H2). These test the HARNESS, not the app.
Each case mutates a copy of the declared proto-l inputs and requires harness.validate() to REFUSE before any room
or candidate command exists. The unmutated base must validate (positive control).
usage: python -B test_shapes.py (exit 0 only if all pass)"""

import copy
import json
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402

BASE = json.loads((HERE / "inputs/inputs-proto-l.json").read_text(encoding="utf-8"))
CAND = Path(r"D:\librarian\temp\lch2-0522\cand-proto-l")
EXPECTED_TESTS = 24


def dep(doc, did):
    return next(d for d in doc["dependencies"] if d["id"] == did)


class Shapes(unittest.TestCase):
    def refused(self, mutate, needle):
        doc = copy.deepcopy(BASE)
        mutate(doc)            # run01: 'doc = mutate(doc) or doc' replaced doc with pop()'s return value (helper bug, kept in evidence)
        with self.assertRaises(harness.Refused) as cm:
            harness.validate(doc, CAND)
        self.assertIn(needle, str(cm.exception))

    def test_s00_base_validates_control(self):
        harness.validate(copy.deepcopy(BASE), CAND)

    def test_s01_deps_none(self):
        self.refused(lambda d: d.update(dependencies=None), "dependencies is not a list")

    def test_s02_deps_dict(self):
        self.refused(lambda d: d.update(dependencies={}), "dependencies is not a list")

    def test_s03_deps_string(self):
        self.refused(lambda d: d.update(dependencies="G,L"), "dependencies is not a list")

    def test_s04_deps_empty(self):
        self.refused(lambda d: d.update(dependencies=[]), "dependencies is empty")

    def test_s05_row_missing(self):
        self.refused(lambda d: d.update(dependencies=[x for x in d["dependencies"] if x["id"] != "K"]), "missing rows: ['K']")

    def test_s06_row_duplicate(self):
        self.refused(lambda d: d["dependencies"].append(copy.deepcopy(dep(d, "G"))), "dependency G: duplicate")

    def test_s07_unknown_id(self):
        self.refused(lambda d: d["dependencies"].append({"id": "Z", "status": "pending", "required": True, "review": "x", "files": "PENDING"}), "unknown id 'Z'")

    def test_s08_required_missing(self):
        self.refused(lambda d: dep(d, "K").pop("required"), "'required' must be the boolean true")

    def test_s09_required_string(self):
        self.refused(lambda d: dep(d, "K").update(required="true"), "'required' must be the boolean true")

    def test_s10_required_false(self):
        self.refused(lambda d: dep(d, "K").update(required=False), "'required' must be the boolean true")

    def test_s11_status_unknown(self):
        self.refused(lambda d: dep(d, "K").update(status="done"), "unknown status 'done'")

    def test_s12_accepted_without_review_ref(self):
        self.refused(lambda d: dep(d, "G").pop("review_ref"), "dependency G.review_ref: pin is not an object")

    def test_s13_accepted_review_ref_wrong_hash(self):
        self.refused(lambda d: dep(d, "G")["review_ref"].update(sha256="0" * 64), "frozen review reference differs")

    def test_s14_accepted_unchecked_string_promotion(self):
        # a pending row flipped to 'accepted' by editing a string, without frozen files or review: refused
        self.refused(lambda d: dep(d, "K").update(status="accepted"), "dependency K.files: not a non-empty list")

    def test_s15_pending_with_pins(self):
        self.refused(lambda d: dep(d, "I").update(files=[{"path": "labs/x.py", "sha256": "0" * 64, "bytes": 1}]), "must say files 'PENDING'")

    def test_s16_pending_with_review_ref(self):
        self.refused(lambda d: dep(d, "I").update(review_ref={"path": "x", "sha256": "0" * 64, "bytes": 1}), "carry no review_ref")

    def test_s17_accepted_R_without_interface(self):
        def m(d):
            g = dep(d, "G")
            dep(d, "R").update(status="accepted", files=copy.deepcopy(g["files"]), review_ref=copy.deepcopy(g["review_ref"]))
        self.refused(m, "interface.route 'review-report'")

    def test_s18_bytes_bool(self):
        self.refused(lambda d: dep(d, "G")["files"][0].update(bytes=True), "bad bytes")

    def test_s19_files_dict(self):
        self.refused(lambda d: dep(d, "G").update(files={"path": "x"}), "not a non-empty list")

    def test_s20_judgments_wrong(self):
        self.refused(lambda d: d.update(judgments=d["judgments"][:2]), "judgments must be exactly")

    def test_s21_candidate_files_not_list(self):
        self.refused(lambda d: d["candidate"].update(files="all"), "candidate.files: not a non-empty list")

    def test_s22_schema_v1(self):
        self.refused(lambda d: d.update(schema="harness-inputs/1"), "schema is not harness-inputs/2")

    def test_s23_inputs_not_object(self):
        with self.assertRaises(harness.Refused):
            harness.validate([], CAND)


if __name__ == "__main__":
    res = unittest.main(exit=False, verbosity=2).result
    print(f"ran {res.testsRun}, expected {EXPECTED_TESTS}")
    sys.exit(0 if res.wasSuccessful() and res.testsRun == EXPECTED_TESTS else 1)
