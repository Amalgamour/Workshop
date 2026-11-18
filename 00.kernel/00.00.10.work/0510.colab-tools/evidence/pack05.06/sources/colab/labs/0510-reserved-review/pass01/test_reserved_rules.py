#!/usr/bin/env python3
"""Focused cases for the NONPRODUCTION reserved-review rules, on SYNTHETIC examples.

Each test mutates one fact and expects one specific refusal code or recorded
difference. These are design acceptance cases, not active review jobs.
"""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import reserved_rules as R  # noqa: E402

EX = HERE / "examples"


def load(name):
    return json.loads((EX / name).read_text(encoding="utf-8"))


def raw(name):
    return (EX / name).read_bytes()


class Base(unittest.TestCase):
    def setUp(self):
        self.d1 = load("descriptor-05.01-independent.json")
        self.d2 = load("descriptor-05.02-informed.json")
        self.t1 = load("trusted-05.01.json")
        self.t2 = load("trusted-05.02.json")
        self.req = load("request-05.01-withheld.json")
        self.binding = load("binding-05.01.json")
        self.cap = load("capture-05.01.json")
        self.r1 = raw("05.01.return.SYNTHETIC.md")
        self.r2 = raw("05.02.return.SYNTHETIC.md")

    def refused(self, code, fn, *args):
        with self.assertRaises(R.Problem) as ctx:
            fn(*args)
        self.assertEqual(ctx.exception.code, code, ctx.exception.detail)


class Launch(Base):
    def test_valid_independent(self):
        out = R.launch_check(self.t1, self.req, self.binding, self.d1)
        self.assertEqual(out["result"], "launch-ready-as-declared")
        self.assertEqual(out["first_pass_label"], "independent-fresh-declared")
        self.assertEqual(out["same_family_declared"], "unknown")

    def test_ordinary_has_no_descriptor(self):
        self.assertEqual(R.launch_check(self.t1, self.req, self.binding, None)["result"], "ordinary")

    def test_descriptor_found_through_source_map(self):
        path = R.descriptor_path(self.t1["investigation"])
        self.assertIsNotNone(R.find_descriptor(self.t1, path))

    def test_absent_trigger(self):
        self.d1["trigger"] = {"kind": None, "named_by": "", "statement": ""}
        self.refused("no-trigger", R.launch_check, self.t1, self.req, self.binding, self.d1)

    def test_target_hash_not_supplied_is_unready(self):
        self.d1["artifact_cut"]["targets"][0]["sha256"] = None
        self.refused("launch-unready", R.launch_check, self.t1, self.req, self.binding, self.d1)

    def test_mismatched_cut(self):
        self.d1["artifact_cut"]["targets"][0]["sha256"] = "0" * 64
        self.refused("cut-mismatch", R.launch_check, self.t1, self.req, self.binding, self.d1)

    def test_context_bundled_into_first_packet(self):
        ctx_row = load("trusted-05.02.json")["source_map"][4]
        self.t1["source_map"].append(ctx_row)
        self.refused("context-in-first-packet", R.launch_check, self.t1, self.req, self.binding, self.d1)

    def test_context_bytes_under_another_name(self):
        ctx_row = copy.deepcopy(load("trusted-05.02.json")["source_map"][4])
        ctx_row["source_path"] = "renamed/notes.md"
        self.t1["source_map"].append(ctx_row)
        self.refused("context-in-first-packet", R.launch_check, self.t1, self.req, self.binding, self.d1)

    def test_requirement_omitted_to_manufacture_failure(self):
        self.t1["source_map"] = [r for r in self.t1["source_map"] if not r["source_path"].endswith("05.01.md")]
        self.refused("requirement-missing", R.launch_check, self.t1, self.req, self.binding, self.d1)

    def test_authority_limits_must_travel(self):
        self.t1["source_map"] = [r for r in self.t1["source_map"] if not r["source_path"].endswith("AUTHORITY.md")]
        self.refused("authority-missing", R.launch_check, self.t1, self.req, self.binding, self.d1)

    def test_withhold_not_declared_to_reviewer(self):
        self.req["withheld"] = []
        self.refused("withhold-undeclared", R.launch_check, self.t1, self.req, self.binding, self.d1)

    def test_continuing_session_cannot_be_independent(self):
        self.d1["reviewer_assignment"]["session"] = "continuing"
        self.refused("not-fresh", R.launch_check, self.t1, self.req, self.binding, self.d1)

    def test_unknown_session_is_labelled_not_refused(self):
        self.d1["reviewer_assignment"]["session"] = "unknown"
        self.assertEqual(R.launch_check(self.t1, self.req, self.binding, self.d1)["first_pass_label"], "independent-freshness-unknown")

    def test_same_model_fresh_session_is_valid_and_disclosed(self):
        self.d1["reviewer_assignment"].update({"model": "claude-opus-5-5", "family": "Claude", "session": "new"})
        out = R.launch_check(self.t1, self.req, self.binding, self.d1)
        self.assertEqual(out["first_pass_label"], "independent-fresh-declared")
        self.assertEqual(out["same_family_declared"], "true")

    def test_unknown_model_is_kept_unknown(self):
        out = R.launch_check(self.t1, self.req, self.binding, self.d1)
        self.assertEqual(self.d1["reviewer_assignment"]["model"], "unknown")
        self.assertIn("declared facts only", out["notes"][0])

    def test_wrong_version(self):
        self.d1["schema"] = "reserved-review/2"
        self.refused("version", R.launch_check, self.t1, self.req, self.binding, self.d1)


class Stage(Base):
    def test_valid_informed(self):
        out = R.stage_check(self.d1, self.d2, self.t2, self.cap, self.r1)
        self.assertEqual(out["result"], "informed-launch-ready-as-declared")
        self.assertEqual(out["builder_context_not_supplied"], [])

    def test_missing_first_findings(self):
        bare = b"# SYNTHETIC first return without a findings block\n"
        import hashlib
        self.cap["return_sha256"] = self.d2["first_return"]["return_sha256"] = hashlib.sha256(bare).hexdigest()
        for row in self.t2["source_map"]:
            if row["source_path"].endswith("05.01.return.md"):
                row["sha256"] = self.cap["return_sha256"]
        self.refused("missing-reserved-findings", R.stage_check, self.d1, self.d2, self.t2, self.cap, bare)

    def test_first_return_not_captured(self):
        self.cap["status"] = "reserved"
        self.refused("first-not-sealed", R.stage_check, self.d1, self.d2, self.t2, self.cap, self.r1)

    def test_replaced_first_return_bytes(self):
        self.refused("first-not-sealed", R.stage_check, self.d1, self.d2, self.t2, self.cap, self.r1 + b"edited\n")

    def test_informed_packet_lacks_sealed_first_return(self):
        self.t2["source_map"] = [r for r in self.t2["source_map"] if not r["source_path"].endswith("05.01.return.md")]
        self.refused("order", R.stage_check, self.d1, self.d2, self.t2, self.cap, self.r1)

    def test_changed_target_is_new_comparison(self):
        self.d2["artifact_cut"] = copy.deepcopy(self.d2["artifact_cut"])
        self.d2["artifact_cut"]["commit"] = "2" * 40
        self.refused("target-changed", R.stage_check, self.d1, self.d2, self.t2, self.cap, self.r1)

    def test_different_environment_is_recorded(self):
        self.d2["environment"] = dict(self.d2["environment"], os="linux")
        out = R.stage_check(self.d1, self.d2, self.t2, self.cap, self.r1)
        self.assertEqual(out["condition_differences"], ["os"])

    def test_informed_before_independent(self):
        self.d2["first_pass"] = "05.03"
        self.refused("stage-order", R.stage_check, self.d1, self.d2, self.t2, self.cap, self.r1)

    def test_builder_context_missing_is_recorded(self):
        self.t2["source_map"] = [r for r in self.t2["source_map"] if not r["source_path"].endswith("06.01.md")]
        out = R.stage_check(self.d1, self.d2, self.t2, self.cap, self.r1)
        self.assertEqual(len(out["builder_context_not_supplied"]), 1)


class Reconcile(Base):
    def test_valid(self):
        out = R.reconcile(self.r1, self.r2)
        self.assertEqual(out["result"], "reconciled-as-declared")
        self.assertEqual(out["counts"]["confirmed"], 1)
        self.assertEqual(out["counts"]["different-conditions"], 1)
        self.assertEqual(out["unique"], ["U01"])
        self.assertIn("acceptance", out["not_established"])

    def edited(self, fn):
        text = self.r2.decode("utf-8")
        start = text.index("```reserved-reconciliation\n") + len("```reserved-reconciliation\n")
        end = text.index("\n```", start)
        block = json.loads(text[start:end])
        fn(block)
        return (text[:start] + json.dumps(block) + text[end:]).encode("utf-8")

    def test_undispositioned_finding(self):
        r2 = self.edited(lambda b: b["dispositions"].pop())
        out = R.reconcile(self.r1, r2)
        self.assertEqual(out["result"], "incomplete")
        self.assertEqual(out["undispositioned"], ["R02"])

    def test_invented_finding(self):
        self.refused("unknown-finding", R.reconcile, self.r1, self.edited(lambda b: b["dispositions"].append({"finding": "R09", "status": "confirmed"})))

    def test_withdrawn_needs_reason(self):
        def f(b):
            b["dispositions"][0].update(status="withdrawn", reason="")
        self.refused("reason", R.reconcile, self.r1, self.edited(f))

    def test_two_blocks_refused(self):
        self.refused("duplicate-reserved-reconciliation", R.reconcile, self.r1, self.r2 + self.r2)

    def test_duplicate_key_refused(self):
        bad = self.r2.replace(b'"stage": "informed"', b'"stage": "informed", "stage": "informed"')
        self.refused("json", R.reconcile, self.r1, bad)


if __name__ == "__main__":
    unittest.main(verbosity=2)
