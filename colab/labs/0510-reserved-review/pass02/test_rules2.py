#!/usr/bin/env python3
"""Focused cases for the pass02 NONPRODUCTION rules and workflow model. SYNTHETIC data only."""

from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import examples as X  # noqa: E402
import reserved_rules2 as R  # noqa: E402
import workflow_model as W  # noqa: E402


def crlf(b: bytes) -> bytes:
    return b.replace(b"\n", b"\r\n")


def dump(v) -> bytes:
    return (json.dumps(v, indent=2, sort_keys=True) + "\n").encode("utf-8")


class Base(unittest.TestCase):
    def setUp(self):
        self.s = X.build()

    def refused(self, code, fn, *args, **kw):
        with self.assertRaises(R.Problem) as ctx:
            fn(*args, **kw)
        self.assertEqual(ctx.exception.code, code, ctx.exception.detail)

    def launch(self, d1_raw=None, expect="reserved", **over):
        s = self.s
        return R.launch(expect, over.get("trusted", s["t1"]), over.get("request", s["request1"]), over.get("binding", s["binding1"]),
                        s["d1_raw"] if d1_raw is None else d1_raw)

    def launch_with(self, mutate):
        d = copy.deepcopy(self.s["d1"])
        mutate(d)
        return self.launch(dump(d))


class ParseView(Base):
    """C03: newline-aware parsing; raw bytes hashed as received."""

    def test_lf_and_crlf_give_the_same_findings(self):
        lf, facts_lf = R.block(X.FIRST_RETURN_LF, "reserved-findings", "r")
        cr, facts_cr = R.block(crlf(X.FIRST_RETURN_LF), "reserved-findings", "r")
        self.assertEqual(lf, cr)
        self.assertNotEqual(facts_lf["raw_sha256"], facts_cr["raw_sha256"])
        self.assertEqual(facts_cr["crlf_lines"], X.FIRST_RETURN_LF.count(b"\n"))

    def test_mixed_line_endings(self):
        mixed = X.FIRST_RETURN_LF.replace(b"\n", b"\r\n", 3)
        self.assertEqual(R.block(mixed, "reserved-findings", "r")[0]["schema"], "reserved-findings/1")

    def test_lone_cr_refused(self):
        self.refused("line-endings", R.block, X.FIRST_RETURN_LF.replace(b"\n", b"\r"), "reserved-findings", "r")

    def test_bom_recorded(self):
        _, facts = R.block(b"\xef\xbb\xbf" + X.FIRST_RETURN_LF, "reserved-findings", "r")
        self.assertTrue(facts["bom"])

    def test_not_utf8(self):
        self.refused("encoding", R.block, b"\xff\xfe" + X.FIRST_RETURN_LF, "reserved-findings", "r")

    def test_missing_and_duplicate_blocks(self):
        self.refused("missing-reserved-findings", R.block, b"# no block\r\n", "reserved-findings", "r")
        self.refused("duplicate-reserved-findings", R.block, crlf(X.FIRST_RETURN_LF) * 2, "reserved-findings", "r")

    def test_strict_json(self):
        self.refused("json", R.block, X.FIRST_RETURN_LF.replace(b'"stage": "independent"', b'"stage": "independent", "stage": "x"'), "reserved-findings", "r")
        self.refused("json", R.block, X.FIRST_RETURN_LF.replace(b'"evidence": []', b'"evidence": NaN'), "reserved-findings", "r")
        self.refused("type", R.block, b"```reserved-findings\n[1, 2]\n```\n", "reserved-findings", "r")


class Types(Base):
    """Every wrong type is a coded refusal, never another exception."""

    # Substitutions that are legitimately valid for an independent descriptor.
    ALLOWED = [("first_pass", None), ("first_return", None), ("environment", {}), ("unavailable", []),
               ("builder_context", []), ("authority_limits", []), ("question", "x")]

    def test_descriptor_field_fuzz(self):
        accepted = []
        for key in sorted(R.DESCRIPTOR_KEYS - {"schema"}):
            for bad in ([], {}, 5, None, True, "x"):
                d = copy.deepcopy(self.s["d1"])
                d[key] = bad
                try:
                    self.launch(dump(d))
                except R.Problem:
                    continue
                accepted.append((key, bad))
        self.assertEqual(accepted, [a for a in sorted(self.ALLOWED, key=lambda kv: kv[0]) if a in accepted])
        self.assertEqual(sorted(map(repr, accepted)), sorted(map(repr, self.ALLOWED)))

    def test_reconcile_status_list_is_enum_not_typeerror(self):
        bad = X.SECOND_RETURN_LF.replace(b'"status": "confirmed"', b'"status": ["confirmed"]')
        self.refused("enum", R.reconcile, X.FIRST_RETURN_LF, bad)

    def test_reconcile_finding_list_is_type_not_typeerror(self):
        bad = X.SECOND_RETURN_LF.replace(b'"finding": "R02"', b'"finding": ["R02"]')
        self.refused("type", R.reconcile, X.FIRST_RETURN_LF, bad)

    def test_findings_not_a_list(self):
        bad = X.FIRST_RETURN_LF.replace(b'"findings": [', b'"findings": {"x": [').replace(b"]}]}\n```", b"]}]}}\n```")
        self.refused("type", R.reconcile, bad, X.SECOND_RETURN_LF)


class Mode(Base):
    """C05: the caller's expected mode is compared with the packet."""

    def test_reserved_requested_without_descriptor_refuses(self):
        self.refused("reserved-expected-missing-descriptor", R.launch, "reserved", self.s["t1"], self.s["request1"], self.s["binding1"], None)

    def test_ordinary_job_stays_ordinary(self):
        self.assertEqual(R.launch("ordinary", self.s["t1"], self.s["request1"], self.s["binding1"], None)["result"], "ordinary-confirmed")

    def test_descriptor_in_ordinary_job_refuses(self):
        self.refused("descriptor-in-ordinary-job", self.launch, expect="ordinary")

    def test_unknown_mode_refuses(self):
        self.refused("enum", self.launch, expect="")

    def test_reserved_ready(self):
        out = self.launch()
        self.assertEqual(out["result"], "reserved-launch-ready-as-declared")
        self.assertEqual(out["first_pass_label"], "independent-fresh-declared")
        self.assertIn("reviewer session freshness, model and family", out["declared_only"])


class Verifier(Base):
    """C04: both verifiers, one expected digest."""

    def test_both_agree(self):
        t = R.verified_package(self.s["producer1"], self.s["handoff1"], self.s["digest1"])
        self.assertEqual(t["digest"], self.s["digest1"])

    def test_handoff_valid_alone_is_not_enough(self):
        rep = dict(self.s["producer1"], result="partial", findings=[{"code": "x"}])
        self.refused("producer-not-intact", R.verified_package, rep, self.s["handoff1"], self.s["digest1"])

    def test_producer_digest_differs(self):
        rep = dict(self.s["producer1"], digest="0" * 64)
        self.refused("digest", R.verified_package, rep, self.s["handoff1"], self.s["digest1"])

    def test_handoff_mismatch(self):
        self.refused("handoff-not-valid", R.verified_package, self.s["producer1"], {"result": "mismatch"}, self.s["digest1"])

    def test_identity_split(self):
        h = copy.deepcopy(self.s["handoff1"])
        h["trusted"]["investigation"] = dict(h["trusted"]["investigation"], page="0798.other")
        self.refused("identity-split", R.verified_package, self.s["producer1"], h, self.s["digest1"])

    def test_wrong_report_kind(self):
        rep = dict(self.s["producer1"], command="preview")
        self.refused("producer-not-verified", R.verified_package, rep, self.s["handoff1"], self.s["digest1"])


class Launch(Base):
    def test_absent_trigger(self):
        self.refused("no-trigger", self.launch_with, lambda d: d.update(trigger={"kind": "", "named_by": "", "statement": ""}))

    def test_unready_cut(self):
        self.refused("launch-unready", self.launch_with, lambda d: d["artifact_cut"]["targets"][0].update(sha256=None))

    def test_cut_mismatch(self):
        self.refused("cut-mismatch", self.launch_with, lambda d: d["artifact_cut"]["targets"][0].update(sha256="0" * 64))

    def test_context_bytes_renamed(self):
        t = copy.deepcopy(self.s["t1"])
        row = copy.deepcopy(self.s["t2"]["source_map"][4])
        row["source_path"] = "renamed/notes.md"
        t["source_map"].append(row)
        self.refused("context-in-first-packet", self.launch, trusted=t)

    def test_requirement_and_authority_must_travel(self):
        for suffix, code in (("05.01.md", "requirement-missing"), ("AUTHORITY.md", "authority-missing")):
            t = copy.deepcopy(self.s["t1"])
            t["source_map"] = [r for r in t["source_map"] if not r["source_path"].endswith(suffix)]
            self.refused(code, self.launch, trusted=t)

    def test_withhold_undeclared(self):
        self.refused("withhold-undeclared", self.launch, request={"withheld": []})

    def test_continuing_session(self):
        self.refused("not-fresh", self.launch_with, lambda d: d["reviewer_assignment"].update(session="continuing"))


class Stage(Base):
    """C01/C02: page-local seal, recorded order, dependency, declared exposure."""

    def run_stage(self, s=None, **over):
        s = s or self.s
        return R.stage(over.get("d2_raw", s["d2_raw"]), s["d1_raw"], over.get("t2", s["t2"]), over.get("chain", s["record"]["transitions"]),
                       over.get("first", s["first_return"]))

    def test_valid(self):
        out = self.run_stage()
        self.assertEqual(out["result"], "informed-launch-ready-as-declared")
        self.assertEqual(out["verified"]["recorded_order"], [2, 3, 4, 5])
        self.assertIn("wall-clock time of sealing or preparation", out["not_proved"])
        self.assertIn("when any person or model saw builder context", out["not_proved"])

    def test_crlf_first_return_end_to_end(self):
        s = X.build(crlf(X.FIRST_RETURN_LF))
        self.assertEqual(self.run_stage(s)["result"], "informed-launch-ready-as-declared")

    def test_no_n1nn_member_anywhere(self):
        self.assertNotIn("member", json.dumps(self.s["record"]))
        self.assertNotIn("member", self.s["d2_raw"].decode())

    def test_not_sealed(self):
        chain = [t for t in self.s["record"]["transitions"] if t["action"] != "seal-return"]
        self.refused("chain", self.run_stage, chain=chain)

    def test_descriptor_names_other_seal(self):
        d = copy.deepcopy(self.s["d2"])
        d["first_return"]["seal_seq"] = 2
        self.refused("first-not-sealed", self.run_stage, d2_raw=dump(d))

    def test_first_return_bytes_differ(self):
        self.refused("first-not-sealed", self.run_stage, first=self.s["first_return"] + b"edited\n")

    def test_first_packet_digest_differs(self):
        d = copy.deepcopy(self.s["d2"])
        d["first_return"]["package_digest"] = "0" * 64
        self.refused("first-packet", self.run_stage, d2_raw=dump(d))

    def test_review_did_not_request_this_pass(self):
        rec = W.open_page(X.BOOK, X.PAGE, "05.01")
        rec = W.attach(rec, "05.01", self.s["digest1"])
        rec = W.seal_return_local(rec, "05.01", self.s["first_return"], "x")
        rec = W.review(rec, "05.01", "hold", None, b"hold\n")
        with self.assertRaises(W.Refuse) as ctx:
            W.open_pass(rec, "05.02")
        self.assertEqual(ctx.exception.reason, "next pass not requested")

    def test_already_attached_informed(self):
        rec = W.attach(self.s["record"], "05.02", self.s["digest2"])
        self.refused("stage-order", self.run_stage, chain=rec["transitions"])

    def test_chain_tamper(self):
        chain = copy.deepcopy(self.s["record"]["transitions"])
        chain[2]["return_sha256"] = "0" * 64
        self.refused("chain", self.run_stage, chain=chain)

    def test_packet_lacks_first_return(self):
        t = copy.deepcopy(self.s["t2"])
        t["source_map"] = [r for r in t["source_map"] if not r["source_path"].endswith("05.01.return.md")]
        self.refused("dependency", self.run_stage, t2=t)

    def test_cut_changed(self):
        d = copy.deepcopy(self.s["d2"])
        d["artifact_cut"]["commit"] = "2" * 40
        self.refused("target-changed", self.run_stage, d2_raw=dump(d))

    def test_missing_first_findings(self):
        bare = b"# SYNTHETIC return without findings\r\n"
        s = X.build(bare)
        self.refused("missing-reserved-findings", self.run_stage, s)

    def test_environment_difference_recorded(self):
        d = copy.deepcopy(self.s["d2"])
        d["environment"]["os"] = "linux"
        self.assertEqual(self.run_stage(d2_raw=dump(d))["condition_differences"], ["os"])


class WorkflowModel(Base):
    def test_seal_replay_and_conflict(self):
        rec = self.s["record"]
        self.assertIs(W.seal_return_local(rec, "05.01", self.s["first_return"], "SYNTHETIC: pasted by Prime from the reviewer's chat"), rec)
        with self.assertRaises(W.Refuse) as ctx:
            W.seal_return_local(rec, "05.01", self.s["first_return"] + b"x", "y")
        self.assertEqual(ctx.exception.reason, "occupied different content")

    def test_review_before_return(self):
        rec = W.attach(W.open_page(X.BOOK, X.PAGE, "05.01"), "05.01", self.s["digest1"])
        with self.assertRaises(W.Refuse):
            W.review(rec, "05.01", "request-next", "05.02", b"r")

    def test_attach_unopened_pass(self):
        rec = W.attach(W.open_page(X.BOOK, X.PAGE, "05.01"), "05.01", self.s["digest1"])
        with self.assertRaises(W.Refuse) as ctx:
            W.attach(rec, "05.02", self.s["digest2"])
        self.assertEqual(ctx.exception.reason, "missing investigation")

    def test_history_rewrite(self):
        old = self.s["record"]
        new = copy.deepcopy(old)
        new["transitions"] = new["transitions"][:2]
        with self.assertRaises(W.Refuse):
            W.extends(old, new)
        W.extends(old, W.attach(old, "05.02", self.s["digest2"]))


class Reconcile(Base):
    def test_unresolved_and_unique_stay_visible(self):
        out = R.reconcile(X.FIRST_RETURN_LF, crlf(X.SECOND_RETURN_LF))
        self.assertEqual(out["result"], "reconciled-as-declared")
        self.assertEqual(out["unresolved"], [{"finding": "R03", "reason": "builder and requirement disagree on who filters"}])
        self.assertEqual([u["id"] for u in out["unique"]], ["U01"])
        self.assertEqual(out["disagreements"], ["whether the requirement binds make() or its callers"])
        self.assertIn("acceptance", out["not_established"])

    def test_incomplete(self):
        bad = X.SECOND_RETURN_LF.replace(b'  {"finding": "R02", "status": "confirmed", "reason": "", "evidence": []},\n', b"")
        out = R.reconcile(X.FIRST_RETURN_LF, bad)
        self.assertEqual((out["result"], out["undispositioned"]), ("incomplete", ["R02"]))

    def test_unknown_finding(self):
        bad = X.SECOND_RETURN_LF.replace(b'"finding": "R02"', b'"finding": "R09"')
        self.refused("unknown-finding", R.reconcile, X.FIRST_RETURN_LF, bad)

    def test_reason_required(self):
        bad = X.SECOND_RETURN_LF.replace(b'"reason": "builder and requirement disagree on who filters"', b'"reason": ""')
        self.refused("empty", R.reconcile, X.FIRST_RETURN_LF, bad)


if __name__ == "__main__":
    unittest.main(verbosity=2)
