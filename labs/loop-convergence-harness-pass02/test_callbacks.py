#!/usr/bin/env python3
"""Harness-unit tests of the four required callbacks and the strict/N7 judges (0707/05.22, 06.21 H1/H3).

LABELLED SCRIPTED COMMAND-RESULT FIXTURES. harness.RUN is replaced by a scripted responder, so every candidate
command returns a scripted JSON body. These tests establish HARNESS behavior only (the callback drives the right
commands and its judge passes good responses and fails bad, missing, unimplemented or crashed ones). They are NOT
app acceptance and say nothing about any real candidate. Real-candidate behavior is in the probe and suite runs.
usage: python -B test_callbacks.py (exit 0 only if all pass)"""

import copy
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness  # noqa: E402
import judges  # noqa: E402

J = harness.lifecycle.JUDGMENT
EX = {"state": "matched", "chronology": "recorded-before-return", "n1_custody": "not-applicable"}
EXPECTED_TESTS = 29
TB = "Traceback (most recent call last):\n  File \"x\"\nZeroDivisionError"


def R(code, body, stderr=""):
    return {"argv": [], "exit": code, "stdout": "" if body is None else json.dumps(body), "stderr": stderr, "body": body}


class FakeCtx:
    """A scripted-fixture context: rooms are temp dirs holding a minimal fake code layer (no app is run)."""

    def __init__(self, d: Path):
        self.rooms = d
        self.jf = d / "lab-judgment.json"
        self.jf.write_text(json.dumps(J), encoding="utf-8")
        self.open_entry = "open.py"
        self.inputs = {}

    def room(self, cid):
        r = self.rooms / cid
        (r / "app").mkdir(parents=True)
        (r / "labs").mkdir()
        (r / "app/librarian.py").write_bytes(b"# FAKE scripted-fixture dispatcher: review_loop_tools_v9.py\n")
        (r / "app/review-loop-v9.json").write_text(json.dumps({"tools": {"workbook": {"path": "labs/wb.py"}}}), encoding="utf-8")
        (r / "labs/wb.py").write_bytes(b"# FAKE workbook\n")
        return r


def parse(argv):
    a = [str(x) for x in argv]
    if a[1] == "open":
        return "open", None, {}, a
    route = a[1]
    rest = a[3:] if route == "review-loop" else a[2:]
    flags = {}
    for i, x in enumerate(rest):
        if x.startswith("--"):
            flags.setdefault(x, []).append(rest[i + 1] if i + 1 < len(rest) else None)
    return route, (a[2] if route == "review-loop" else None), flags, rest


def responder(handler):
    def run(argv, cwd):
        route, c, flags, rest = parse(argv)
        if route == "open":
            return R(0, {"opened": True})
        root = Path(cwd)
        tamper = any((root / f).read_bytes().endswith(b"# LAB tamper (RP-2)\n") for f in ("app/librarian.py", "labs/wb.py"))
        page = (flags.get("--source") or [None])[0]
        return handler(route, c, root, page, flags, rest, tamper)
    return run


# ------------------------------------------------------------------ CAP-4 script
def cap_handler(variant=None):
    def h(route, c, root, page, flags, rest, tamper):
        if variant == "unimplemented":
            return R(2, None, "unknown command")
        if c == "prepare":
            return R(0, {} if variant == "no-measurement" else {"measurement": "complete", "intake_id": "i1"})
        if c == "read":
            return R(0, {"judgment": {} if variant == "read-differs" else J, "stale": False})
        if c == "record":
            p = page[:4]
            if p == "0590":
                return R(2, {"correction": "limit sources"}) if variant == "64-refused" else R(0, {"review_id": "w"})
            if p == "0591":
                if variant == "65-records":
                    return R(0, {"review_id": "w"})
                if variant == "65-crash":
                    return R(1, None, TB)
                if variant == "65-vague":
                    return R(2, {"correction": "refused"})
                return R(2, {"correction": "limit sources"})
            if p == "0592":
                return R(0, {"review_id": "w"}) if variant == "list-accepted" else R(2, {"correction": "limit judgment.reasons"})
            if p == "0593":
                return R(0, {"review_id": "w"}) if variant == "doc-accepted" else R(2, {"correction": "judgment: input exceeds 262144 bytes"})
        return R(2, None, "unscripted")
    return h


# ------------------------------------------------------------------ RP script
FLAGS = dict(judges.SAFE_FLAGS)
PASS = re.compile(r"^05\.\d\d$")


def rp_handler(variant=None):
    def h(route, c, root, page, flags, rest, tamper):
        name = root.name
        if route == "review-loop":
            if c == "prepare":
                return R(0, {"measurement": "incomplete" if name.endswith("held") else "complete", "intake_id": "i1", "exchange": EX})
            if c == "record":
                return R(0, {"review_id": "w1"})
            if c == "inspect":
                return R(0, {"rendered": "LAB rendered"})
            if c == "publish":
                return R(0, {"published": True})
            if c == "read":
                if name.endswith("held"):
                    return R(2, {})
                return R(0, {"stale": name.endswith("stale"), "review_id": "w1", "custody": "not-applicable"})
            return R(2, None, "unscripted")
        # review-report
        if variant == "no-route":
            return R(2, None, "librarian: unknown command review-report")
        if variant == "always-refuse":
            return R(2, {"state": "refused"})
        bad_env = (any(k not in ("--book", "--source", "--pass") for k in flags) or any(len(v) > 1 for v in flags.values())
                   or "--source" not in flags or not Path(flags.get("--book", [""])[0] or "").is_absolute()
                   or not PASS.match(flags.get("--pass", [""])[0] or ""))
        if bad_env:
            if variant == "crash-on-envelope":
                return R(1, None, TB)
            return R(2, {"state": "refused"})
        if tamper and variant != "accept-tampered":
            return R(2, {"state": "refused"})
        state, stale = ("held", None) if name.endswith("held") else (("stale", True) if name.endswith("stale") else ("readable", False))
        if variant == "stale-as-readable" and name.endswith("stale"):
            state, stale = "readable", False
        body = dict(FLAGS, state=state, stale=stale, review_id="w1", exchange=dict(EX), custody="not-applicable")
        if variant == "missing-authority":
            body.pop("authority")
        if variant == "releases":
            body["action_released"] = True
        if variant == "no-exchange":
            body.pop("exchange")
        if variant == "exchange-differs":
            body["exchange"]["chronology"] = "unverified"
        return R(0, body)
    return h


# ------------------------------------------------------------------ IN-2 script
def in_handler(variant=None):
    def h(route, c, root, page, flags, rest, tamper):
        copy_ = root.name.endswith("bookB")
        if c == "prepare":
            return R(0, {"measurement": "complete", "intake_id": "i1"})
        if c == "record":
            return R(0, {"review_id": "w1"})
        if c == "read":
            if not copy_:
                return R(0, {"stale": variant == "original-stale", "judgment": J})
            if variant == "copy-current":
                return R(0, {"stale": False, "judgment": J})
            if variant == "copy-no-fields":
                return R(0, {"judgment": J})
            if variant == "history-lost":
                return R(2, {})
            if variant == "copy-crash":
                return R(1, None, TB)
            return R(0, {"stale": True, "applicable": False, "judgment": J})
        if c == "recover":
            return R(2, {}) if variant == "history-lost" else R(0, {"judgment": J})
        if c == "publish":
            if variant == "copy-publishes":
                (root / harness.BOOK / harness.N5P / "06.01.md").write_bytes(b"published in the copy\n")
                return R(0, {"published": True})
            return R(2, {"correction": "instance held"})
        return R(2, None, "unscripted")
    return h


class Callbacks(unittest.TestCase):
    def go(self, fn, handler):
        keep = harness.RUN
        harness.RUN = responder(handler)
        try:
            with tempfile.TemporaryDirectory() as d:
                return fn(FakeCtx(Path(d)))
        finally:
            harness.RUN = keep

    # CAP-4
    def test_c01_cap4_good(self):
        self.assertEqual(self.go(harness.cap_4, cap_handler())[2], "pass")

    def test_c02_cap4_bad_variants(self):
        for v in ("64-refused", "65-records", "65-crash", "65-vague", "read-differs", "list-accepted", "doc-accepted", "unimplemented", "no-measurement"):
            e, o, verdict = self.go(harness.cap_4, cap_handler(v))
            self.assertEqual(verdict, "fail", v)
            self.assertTrue(o["judge_reasons"], v)

    def test_c03_cap4_fixture_counts(self):
        e, o, v = self.go(harness.cap_4, cap_handler())
        self.assertEqual([o[k]["harness_count"] for k in ("at_bound", "over_bound", "list25", "doc")], [64, 65, 3, 3])
        self.assertGreater(o["doc"]["judgment_bytes"], 262144)

    # RP-1
    def test_c04_rp1_good(self):
        self.assertEqual(self.go(harness.rp_1, rp_handler())[2], "pass")

    def test_c05_rp1_bad_variants(self):
        for v in ("no-route", "always-refuse", "missing-authority", "releases", "stale-as-readable", "no-exchange", "exchange-differs"):
            e, o, verdict = self.go(harness.rp_1, rp_handler(v))
            self.assertEqual(verdict, "fail", v)
            self.assertTrue(o["judge_reasons"], v)

    # RP-2
    def test_c06_rp2_good(self):
        e, o, v = self.go(harness.rp_2, rp_handler())
        self.assertEqual(v, "pass", o["judge_reasons"])

    def test_c07_rp2_bad_variants(self):
        for v in ("no-route", "always-refuse", "accept-tampered", "crash-on-envelope"):
            e, o, verdict = self.go(harness.rp_2, rp_handler(v))
            self.assertEqual(verdict, "fail", v)

    def test_c08_rp2_tamper_restored(self):
        # the scripted reporter refuses whenever a file ends with the tamper marker; control_after succeeding proves
        # the callback restored both tampered files
        e, o, v = self.go(harness.rp_2, rp_handler())
        self.assertEqual(o["control_after"]["exit"], 0)

    # IN-2
    def test_c09_in2_good(self):
        e, o, v = self.go(harness.in_2, in_handler())
        self.assertEqual(v, "pass", o["judge_reasons"])

    def test_c10_in2_bad_variants(self):
        for v in ("copy-current", "copy-no-fields", "history-lost", "copy-publishes", "copy-crash", "original-stale"):
            e, o, verdict = self.go(harness.in_2, in_handler(v))
            self.assertEqual(verdict, "fail", v)
            self.assertTrue(o["judge_reasons"], v)


# ------------------------------------------------------------------ pure judges (strict / N7-3)
GOOD_STRICT = {"measurement": "incomplete", "codes": ["custody-missing", "malformed-n7-declaration", "unparsed-return-line"],
               "bound_rows": [{"role": "assignment", "path": "0707.app-use-check/05.15.pack.md"}],
               "record_exit": 2, "publish_exit": 2, "destination_unchanged": True}
ALT1 = ({"artifact-manifest"}, "evidence/design05.15/artifact-manifest.json,")
ALT2 = ({"submission", "return"}, "06.15.notes.md")


class StrictJudge(unittest.TestCase):
    def test_j01_good(self):
        self.assertEqual(judges.strict(GOOD_STRICT, ALT1)[2], "pass")

    def test_j02_pass01_st2_on_proto_l_fails(self):
        # the actual 05.21 proto-l ST-2 observation: refused for the local pair rule, no malformed code
        o = dict(GOOD_STRICT, codes=["attribution-not-descriptive", "index-context-bounded", "n1-not-applicable", "n7-exchange-return-not-local", "unparsed-return-line"])
        self.assertEqual(judges.strict(o, ALT2)[2], "fail")

    def test_j03_alternative_bound_fails(self):
        o = dict(GOOD_STRICT, bound_rows=[{"role": "artifact-manifest", "path": "0707.app-use-check/evidence/design05.15/artifact-manifest.json,"}])
        self.assertEqual(judges.strict(o, ALT1)[2], "fail")

    def test_j04_alternative_same_path_other_role_ok(self):
        o = dict(GOOD_STRICT, bound_rows=[{"role": "artifact", "path": "0707.app-use-check/06.15.notes.md"}])
        self.assertEqual(judges.strict(o, ALT2)[2], "pass")

    def test_j05_missing_fields_fail(self):
        for k in ("codes", "bound_rows", "record_exit", "publish_exit", "destination_unchanged", "measurement"):
            o = dict(GOOD_STRICT)
            o.pop(k)
            self.assertEqual(judges.strict(o, ALT1)[2], "fail", k)

    def test_j06_published_fails(self):
        self.assertEqual(judges.strict(dict(GOOD_STRICT, publish_exit=0, destination_unchanged=False), None)[2], "fail")


GOOD_N73 = {"record_exit": 0, "read_custody": "not-applicable", "rendered": "x\ncustody: not-applicable\n", "exchange": dict(EX), "n5_control_custody": "missing"}


class N7CustodyJudge(unittest.TestCase):
    def test_j07_good(self):
        self.assertEqual(judges.n7_custody(GOOD_N73)[2], "pass")

    def test_j08_proto_l_observed_fails(self):
        # the 05.21 LC-1 room: record custody 'missing', rendered 'custody: missing'
        o = dict(GOOD_N73, read_custody="missing", rendered="custody: missing\n")
        self.assertEqual(judges.n7_custody(o)[2], "fail")

    def test_j09_missing_render_fails(self):
        self.assertEqual(judges.n7_custody(dict(GOOD_N73, rendered=None))[2], "fail")

    def test_j10_n5_control_takes_n7_value_fails(self):
        self.assertEqual(judges.n7_custody(dict(GOOD_N73, n5_control_custody="not-applicable"))[2], "fail")

    def test_j11_no_exchange_fails(self):
        self.assertEqual(judges.n7_custody(dict(GOOD_N73, exchange=None))[2], "fail")


class JudgeShapes(unittest.TestCase):
    """Wrong types never pass: bools are not exits, strings are not lists, absent observations fail."""

    def test_j12_cap4_empty(self):
        self.assertEqual(judges.cap4({})[2], "fail")

    def test_j13_rp1_empty(self):
        self.assertEqual(judges.rp1({})[2], "fail")

    def test_j14_rp2_empty(self):
        self.assertEqual(judges.rp2({})[2], "fail")

    def test_j15_in2_empty(self):
        self.assertEqual(judges.in2({}, J)[2], "fail")

    def test_j16_exit_true_is_not_a_refusal(self):
        self.assertFalse(judges._failed_cleanly({"exit": True, "stderr": ""}))
        self.assertFalse(judges._failed_cleanly({"exit": "2", "stderr": ""}))
        self.assertFalse(judges._failed_cleanly({"exit": 2, "stderr": TB}))
        self.assertTrue(judges._failed_cleanly({"exit": 2, "stderr": "refused"}))

    def test_j17_strict_codes_string(self):
        self.assertEqual(judges.strict(dict(GOOD_STRICT, codes="malformed-n7-declaration"), None)[2], "fail")

    def test_j18_rp1_report_body_list(self):
        o = {"current": {"core": {"exit": 0, "stale": False}, "report": {"exit": 0, "body": []}}}
        self.assertEqual(judges.rp1(o)[2], "fail")

    def test_j19_in2_stale_string(self):
        good = {"a_record_exit": 0, "a_read_before": {"exit": 0, "stale": False}, "a_read_after": {"exit": 0, "stale": False},
                "a_bytes_unchanged": True, "b_read": {"exit": 0, "stale": "true", "judgment": J}, "b_recover": {"judgment": J},
                "b_publish": {"exit": 2, "stderr": ""}, "b_destination_created": False}
        self.assertEqual(judges.in2(good, J)[2], "fail")


if __name__ == "__main__":
    res = unittest.main(exit=False, verbosity=2).result
    print(f"ran {res.testsRun}, expected {EXPECTED_TESTS}")
    sys.exit(0 if res.wasSuccessful() and res.testsRun == EXPECTED_TESTS else 1)
