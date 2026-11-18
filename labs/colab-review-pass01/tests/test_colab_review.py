"""Tests for colab_review.py (0518.colab-review 05.01). Disposable source repositories and books; the real pinned producer v2,
workflow v2, helper and inspector through their CLIs; SYNTHETIC reviewer results only. No model, reviewer or session is launched.

  python -B -X dev tests/test_colab_review.py -v
"""
import copy
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import fixture as F  # noqa: E402
import colab_review as cr  # noqa: E402


class Prepared(unittest.TestCase):
    """One staged, prepared and bound package per class; each test captures into its own fresh book."""

    @classmethod
    def setUpClass(cls):
        cls.d = F.Desk(prefix="crv-" + cls.__name__[:10] + "-")
        cls.pp, cls.pb, cls.req, cls.out, cls.digest, cls.bdir = F.route(cls.d)

    @classmethod
    def tearDownClass(cls):
        cls.d.close()

    def book(self):
        return self.d.new_book(self._testMethodName[5:30])

    def captured(self, book, specs):
        return [self.d.capture(self.out, f"r{self._testMethodName[5:7]}-{n:02d}", r, book=book) for n, r in enumerate(specs, 1)]

    def intake(self, book, members):
        return self.d.intake(self.bdir, self.pp, members, name=f"intake-{self._testMethodName[5:30]}", book=book)

    def full_results(self):
        pb, R = self.pb, self.d.result
        return [R(pb, "R01", "S01"), R(pb, "R02", "S01"),
                R(pb, "R01", "S02", ["SYNTHETIC: section 2 conflates two terms."], comprehension=False),
                R(pb, "R02", "S02", ["SYNTHETIC: section 2 conflates two terms.", "SYNTHETIC: the fallback path is untested."], comprehension=False),
                R(pb, "R01", "S03", [], comprehension=False,
                  simplicity={"added_complexity": "SYNTHETIC: one extra state", "addresses_failure": "SYNTHETIC: the false-ready case",
                              "reuse_or_duplication": "SYNTHETIC: reuses the existing check", "accepted_limitations": ["SYNTHETIC: no race safety"]})]


class TestIntegration(Prepared):
    def test_01_prompts_survive_the_whole_supported_route_with_preserved_paraphrase(self):
        book = self.d.book
        snaps = json.loads((self.out / "package" / "source-manifest.json").read_text(encoding="utf-8"))
        paths = {s["path"] for s in snaps["sources"]}
        self.assertTrue({"reviews/plan-1/review-plan.json", "reviews/plan-1/COMPREHENSION.md", "reviews/plan-1/SIMPLICITY.md",
                         "reviews/plan-1/RESULT-TEMPLATE.json"} <= paths)
        (oc, ob, oe), (ac, ab, ae) = self.d.open_attach(self.req, self.out, self.digest)
        self.assertEqual((oc, ob["result"], ac, ab["result"]), (0, "complete", 0, "complete"), (oe, ae))
        members = self.captured(book, self.full_results())
        pc, pbody, perr = F.run(F.WORKFLOW, "place-return", "--book", book, "--page", F.PAGE, "--pass", F.PASS, "--member", members[0], "--config", self.d.config)
        self.assertEqual((pc, pbody["result"]), (0, "complete"), perr)
        page = book / F.PAGE
        self.assertEqual((page / "05.01.return.md").read_bytes(), (book / members[0] / "return.md").read_bytes())
        code, i, err = self.intake(book, members)
        self.assertEqual((code, i["status"], i["incomplete"], i["findings"]), (0, "complete", [], []), err)
        r02 = next(x["result"] for x in i["results"] if x["result"]["reviewer"] == "R02" and x["result"]["stage"] == "S01")
        self.assertEqual((r02["findings"], r02["comprehension"]["proposed"]), ([], "SYNTHETIC R02: the page proposes a fixture design."))
        synth = {"schema": "colab-review-synthesis/1", "plan_id": "plan-1", "intake_sha256": hashlib.sha256((self.d.path(f"intake-{self._testMethodName[5:30]}") / "intake.json").read_bytes()).hexdigest(),
                 "by": "Codex Prime (SYNTHETIC)", "label": "SYNTHETIC",
                 "items": [{"id": "X01", "title": "SYNTHETIC: terminology", "findings": ["R01-S02-F01", "R02-S02-F01"], "recommendation": "SYNTHETIC: define both terms."}],
                 "retained": [{"finding": "R02-S02-F02", "disposition": "minority", "reason": "SYNTHETIC: one reader only; kept open", "of": None}],
                 "disagreements": [{"findings": ["R02-S02-F02"], "text": "SYNTHETIC: R01 did not see this risk."}], "incomplete": [],
                 "residual_uncertainty": ["SYNTHETIC: isolation is unknown for both readers."], "acceptance": None}
        code, rep, err = self.d.synthesize(self.d.path(f"intake-{self._testMethodName[5:30]}"), synth)
        self.assertEqual((code, rep["status"], rep["round"]["cap_reached"]), (0, "consistent", False), err)
        md = (self.d.path("report") / "REPORT.md").read_text(encoding="utf-8")
        self.assertIn("SYNTHETIC R02: the page proposes a fixture design.", md)  # zero-findings paraphrase kept verbatim
        self.assertIn("R02-S02-F02: minority", md)
        self.assertIn("not a review, not acceptance", md)
        review = {"schema": "colab-exchange-review/1", "by": "Codex Prime (SYNTHETIC)", "on": "2026-10-31",
                  "assessment": "SYNTHETIC review record; it cites report " + rep["report_digest"][:16] + ".",
                  "findings": [{"id": "F01", "consequential": False, "observation": "SYNTHETIC: X01 terminology", "source_binding": "T01",
                                "disposition": "adopted", "director_reply": "hypothetical-fixture: none sought", "pending": False, "reason": "SYNTHETIC"}],
                  "pending_questions": [], "route": "hold", "next_pass": None}
        rc, rb, re_ = F.run(F.WORKFLOW, "record-review", "--book", book, "--page", F.PAGE, "--pass", F.PASS, "--review", self.d.write("review.json", review))
        self.assertEqual((rc, rb["result"]), (0, "complete"), re_)
        self.assertIn("SYNTHETIC: X01 terminology", (page / "06.01.review.md").read_text(encoding="utf-8"))
        self.assertEqual((page / "05.01.return.md").read_bytes(), (book / members[0] / "return.md").read_bytes())  # return bytes unchanged


class TestCompatibility(Prepared):
    def test_02_old_package_and_old_return_remain_readable(self):
        d = self.d
        old_req = d.write("old-request.json", d.base_request())
        out, digest = d.prepare(old_req, name="old-out")
        code, b, err = d.bind(out, digest, None, name="old-binding")
        self.assertEqual((code, b["status"]), (0, "legacy-no-review-plan"), err)
        code, b2, _ = d.bind(self.out, self.digest, None, name="no-plan-but-review-files")
        self.assertEqual(code, 2)
        self.assertIn("pass --plan", b2)
        book = self.book()
        m = d.capture(self.out, "old-01", b"legacy artifact, not a review result\n", book=book, artifact="note.txt")
        code, i, _ = self.intake(book, [m])
        self.assertEqual(i["results"][0]["result"], "legacy-no-result")


class TestPlanChecks(Prepared):
    def test_03_mode_context_and_isolation_rules(self):
        cold = self.d.plan(mode="cold-comprehension")
        cold["reviewers"][1]["context"]["conversation_supplied"] = "summary"
        cp = self.d.write("cold.json", cold)
        code, out, _ = F.run(F.ADAPTER, "stage", "--plan", cp, "--request", self.d.write("rq.json", self.d.base_request()), "--repo", self.d.repo,
                             "--out-request", self.d.path("cold-req.json"))
        self.assertEqual(code, 2)
        self.assertIn("a cold plan supplies no prior conversation", out)
        verified = self.d.plan()
        verified["reviewers"][0]["context"]["isolation"] = "verified"
        with self.assertRaises(cr.Refusal) as ctx:
            cr.check_plan(verified)
        self.assertIn("never verified", str(ctx.exception))
        book = self.book()
        r = self.d.result(self.pb, "R01", "S01")
        r["context"]["conversation_supplied"] = "full"
        m = self.captured(book, [r])
        code, i, _ = self.intake(book, m)
        self.assertIn("context-mismatch", [f["finding"] for f in i["findings"]])

    def test_04_empty_stage_and_simplicity_declarations(self):
        p = self.d.plan()
        p["stages"][1]["reviewers"] = []
        with self.assertRaises(cr.Refusal) as ctx:
            cr.check_plan(p)
        self.assertIn("needs at least one reviewer", str(ctx.exception))
        p = self.d.plan(simplicity=None)
        with self.assertRaises(cr.Refusal):
            cr.check_plan(p)


class TestResults(Prepared):
    def test_05_missing_comprehension_absent_and_failed_reviewers_are_incomplete(self):
        book = self.book()
        R = self.d.result
        specs = [R(self.pb, "R01", "S01", comprehension=False), R(self.pb, "R02", "S01"),
                 R(self.pb, "R01", "S02", ["SYNTHETIC finding"], comprehension=False),
                 R(self.pb, "R02", "S02", [], status="failed", comprehension=False)]
        code, i, _ = self.intake(book, self.captured(book, specs))
        self.assertEqual((code, i["status"]), (1, "incomplete"))
        self.assertIn("missing-comprehension", [f["finding"] for f in i["findings"]])
        self.assertEqual(i["incomplete"], [{"reviewer": "R02", "stage": "S02", "status": "failed"}])  # failed is not zero findings

    def test_06_sequence_violation_and_duplicate_or_bad_ids(self):
        book = self.book()
        R = self.d.result
        bad = R(self.pb, "R01", "S02", ["SYNTHETIC one", "SYNTHETIC two"], comprehension=False)
        bad["findings"][1]["id"] = bad["findings"][0]["id"]
        wrong = R(self.pb, "R02", "S02", ["SYNTHETIC x"], comprehension=False)
        wrong["findings"][0]["id"] = "R01-S02-F09"  # another reviewer's prefix
        specs = [bad, wrong, R(self.pb, "R01", "S01"), R(self.pb, "R02", "S01")]  # S02 captured before S01
        code, i, _ = self.intake(book, self.captured(book, specs))
        names = [f["finding"] for f in i["findings"]]
        self.assertIn("sequence-violation", names)
        self.assertIn("duplicate-finding-id", names)
        self.assertIn("bad-finding-id", names)

    def test_07_altered_source_identity_in_result_and_in_binding(self):
        book = self.book()
        r = self.d.result(self.pb, "R01", "S01", plan_sha256="0" * 64)
        code, i, _ = self.intake(book, self.captured(book, [r]))
        self.assertIn("source-identity-altered", [f["finding"] for f in i["findings"]])
        other = self.d.plan(finish_boundary="SYNTHETIC: a different boundary than the one packaged")
        op = self.d.write("other-plan.json", F.canonical(other))
        code, b, _ = self.d.bind(self.out, self.digest, op, name="altered-binding")
        self.assertEqual((code, b["status"]), (1, "mismatch"))
        self.assertIn("review-file-differs", [f["finding"] for f in b["findings"]])
        code, b, _ = self.d.bind(self.out, "0" * 64, self.pp, name="stale-digest")
        self.assertEqual(code, 2)


class TestSynthesis(Prepared):
    def intake_for_synthesis(self):
        book = self.book()
        R = self.d.result
        specs = [R(self.pb, "R01", "S01"), R(self.pb, "R02", "S01"),
                 R(self.pb, "R01", "S02", ["SYNTHETIC a"], comprehension=False), R(self.pb, "R02", "S02", ["SYNTHETIC b", "SYNTHETIC c"], comprehension=False)]
        name = f"intake-{self._testMethodName[5:30]}"
        self.intake(book, self.captured(book, specs))
        ip = self.d.path(name) / "intake.json"
        return self.d.path(name), hashlib.sha256(ip.read_bytes()).hexdigest()

    def synth(self, isha, **over):
        s = {"schema": "colab-review-synthesis/1", "plan_id": "plan-1", "intake_sha256": isha, "by": "SYNTHETIC", "label": "SYNTHETIC",
             "items": [{"id": "X01", "title": "SYNTHETIC", "findings": ["R01-S02-F01", "R02-S02-F01"], "recommendation": "SYNTHETIC"}],
             "retained": [{"finding": "R02-S02-F02", "disposition": "dissent", "reason": "SYNTHETIC: kept", "of": None}],
             "disagreements": [], "incomplete": [], "residual_uncertainty": [], "acceptance": None}
        s.update(over)
        return s

    def test_08_every_original_finding_is_mapped_and_dissent_is_kept(self):
        idir, isha = self.intake_for_synthesis()
        code, r, _ = self.d.synthesize(idir, self.synth(isha), name="ok")
        self.assertEqual((code, r["status"]), (0, "consistent"))
        self.assertEqual(r["retained"][0]["original"]["text"], "SYNTHETIC c")
        lost = self.synth(isha, retained=[])
        code, r, _ = self.d.synthesize(idir, lost, name="lost")
        self.assertEqual(([f["finding"] for f in r["findings"]], code), (["lost-finding"], 1))
        twice = self.synth(isha, items=[{"id": "X01", "title": "S", "findings": ["R01-S02-F01", "R02-S02-F01", "R02-S02-F02"], "recommendation": "S"}])
        self.assertIn("double-mapped", [f["finding"] for f in self.d.synthesize(idir, twice, name="twice")[1]["findings"]])
        ghost = self.synth(isha, disagreements=[{"findings": ["R09-S09-F01"], "text": "SYNTHETIC"}])
        self.assertIn("unknown-finding", [f["finding"] for f in self.d.synthesize(idir, ghost, name="ghost")[1]["findings"]])
        miss = self.synth(isha, incomplete=[{"reviewer": "R01", "stage": "S03", "status": "absent"}])
        self.assertIn("incomplete-mismatch", [f["finding"] for f in self.d.synthesize(idir, miss, name="miss")[1]["findings"]])

    def test_09_cap_never_creates_acceptance(self):
        idir, isha = self.intake_for_synthesis()
        code, out, _ = self.d.synthesize(idir, self.synth(isha, acceptance={"by": "SYNTHETIC", "state": "accepted"}), name="acc")
        self.assertEqual(code, 2)
        self.assertIn("acceptance must be null", out)
        i = json.loads((idir / "intake.json").read_text(encoding="utf-8"))
        i["round"] = {"number": 2, "cap": 2}
        capped = self.d.write("capped-intake.json", F.canonical(i))
        cdir = self.d.path("capped")
        cdir.mkdir()
        (cdir / "intake.json").write_bytes(capped.read_bytes())
        code, r, _ = self.d.synthesize(cdir, self.synth(hashlib.sha256(capped.read_bytes()).hexdigest()), name="capped-report")
        self.assertEqual((r["round"]["cap_reached"], r["round"]["meaning"].split(":")[0]), (True, "cap-reached"))
        self.assertIn("not acceptance", (self.d.path("capped-report") / "REPORT.md").read_text(encoding="utf-8"))

    def test_10_output_conflict_and_partial_state(self):
        idir, isha = self.intake_for_synthesis()
        s = self.d.write("s.json", self.synth(isha))
        taken = self.d.path("taken")
        taken.mkdir()
        code, out, _ = F.run(F.ADAPTER, "synthesize", "--intake", idir / "intake.json", "--synthesis", s, "--out", taken)
        self.assertEqual(code, 2)
        self.assertIn("already exists", out)
        real = cr.write_file

        def flaky(p, data):
            if p.name == "REPORT.md":
                raise OSError("injected interruption")
            return real(p, data)
        with mock.patch.object(cr, "write_file", flaky):
            with self.assertRaises(cr.PartialWrite):
                cr.cmd_synthesize(str(idir / "intake.json"), str(s), str(self.d.path("partial")))
        self.assertEqual(sorted(p.name for p in self.d.path("partial").iterdir()), ["report.json"])  # kept, not removed


class TestPreservation(Prepared):
    """The three Prime probes, plus required and optional stage visibility. Synthetic results only."""

    ORIGINAL = "SYNTHETIC ORIGINAL: return recording may lose its evidence."

    def required(self):
        R = self.d.result
        return [R(self.pb, "R01", "S01"), R(self.pb, "R02", "S01"),
                R(self.pb, "R01", "S02", [], comprehension=False), R(self.pb, "R02", "S02", [], comprehension=False)]

    def walk(self, name, specs):
        book = self.d.new_book(name)
        members = [self.d.capture(self.out, f"{name}-{n:02d}", r, book=book) for n, r in enumerate(specs, 1)]
        code, intake, err = self.d.intake(self.bdir, self.pp, members, name=name + "-intake", book=book)
        ip = self.d.path(name + "-intake") / "intake.json"
        known = intake["findings_index"]
        synth = {"schema": "colab-review-synthesis/1", "plan_id": "plan-1",
                 "intake_sha256": hashlib.sha256(ip.read_bytes()).hexdigest(),
                 "by": "SYNTHETIC preservation", "label": "SYNTHETIC", "items": [],
                 "retained": [{"finding": f, "disposition": "minority", "reason": "Keep this concern visible", "of": None} for f in known],
                 "disagreements": [], "incomplete": intake["incomplete"], "residual_uncertainty": [], "acceptance": None}
        rc, report, rerr = self.d.synthesize(self.d.path(name + "-intake"), synth, name=name + "-report")
        md = (self.d.path(name + "-report") / "REPORT.md").read_text(encoding="utf-8")
        return code, intake, err, rc, report, rerr, md

    def test_12_context_mismatch_stays_visible_when_the_mapping_is_consistent(self):
        specs = self.required()
        specs[0]["context"]["conversation_supplied"] = "full"
        code, intake, err, rc, report, rerr, md = self.walk("context-error", specs)
        self.assertEqual((code, intake["status"], intake["incomplete"]), (1, "incomplete", []), err)
        self.assertEqual(intake["findings"][0]["finding"], "context-mismatch")
        self.assertEqual((rc, report["status"], report["findings"], report["schema"]), (0, "consistent", [], "colab-review-report/2"), rerr)
        self.assertEqual(report["intake_findings"], intake["findings"])
        self.assertEqual(report["distinctions"], {"mapping": "consistent", "required_review": "incomplete", "acceptance": None})
        self.assertIn("Investigation is incomplete. A consistent mapping does not resolve these diagnostics.", md)
        self.assertIn('"finding": "context-mismatch"', md)
        self.assertIn('"conversation_supplied": "none"', md)
        self.assertIn('"conversation_supplied": "full"', md)
        self.assertIn("Acceptance: none.", md)
        self.assertNotIn("colab-review-report/1", md)

    def test_13_optional_statuses_stay_visible_and_do_not_block_required_completion(self):
        R = self.d.result
        cases = [("optional-failed", "failed"), ("optional-partial", "partial"), ("optional-not-run", "not-run")]
        for name, status in cases:
            specs = self.required() + [R(self.pb, "R01", "S03", [], status=status, comprehension=False)]
            code, intake, err, rc, report, rerr, md = self.walk(name, specs)
            self.assertEqual((code, intake["status"], intake["incomplete"], rc, report["status"]), (0, "complete", [], 0, "consistent"), (name, err, rerr))
            row = next(x for x in report["stage_status"] if x["stage"] == "S03")
            self.assertEqual((row["reviewer"], row["required"], row["status"]), ("R01", False, status))
            self.assertIsNotNone(row["member"])
            self.assertIn(f"R01 S03 optional {status} (member {row['member']}, receipt {row['receipt_sha256']})", md)
            self.assertEqual(report["distinctions"]["required_review"], "complete")
            self.assertIn("Optional status does not by itself change required review completion.", md)
        code, intake, err, rc, report, rerr, md = self.walk("optional-absent", self.required())
        self.assertEqual((code, intake["status"], intake["incomplete"]), (0, "complete", []), err)
        row = next(x for x in intake["stage_status"] if x["stage"] == "S03")
        self.assertEqual((row["required"], row["status"], row["member"], row["receipt_sha256"]), (False, "absent", None, None))
        self.assertIn("R01 S03 optional absent (absent)", md)
        self.assertEqual((rc, report["intake_findings"]), (0, []), rerr)

    def test_14_retained_original_text_target_location_and_custody_are_quoted(self):
        specs = self.required()
        specs[2]["findings"] = [{"id": "R01-S02-F01", "target": "T01", "location": "section 2", "text": self.ORIGINAL}]
        code, intake, _, rc, report, rerr, md = self.walk("retained-text", specs)
        self.assertEqual((code, intake["status"], rc, report["status"]), (0, "complete", 0, "consistent"), rerr)
        original = report["retained"][0]["original"]
        self.assertEqual(original["text"], self.ORIGINAL)
        self.assertIn(f"- R01-S02-F01: minority: Keep this concern visible", md)
        self.assertIn(f"  - text: {self.ORIGINAL}", md)
        self.assertIn("  - target: T01", md)
        self.assertIn("  - location: section 2", md)
        self.assertIn(f"  - custody: member {original['member']}, receipt {original['receipt_sha256']}", md)
        self.assertEqual(md.count(self.ORIGINAL), 1)

    def test_15_normal_success_quotes_consolidated_and_retained_originals(self):
        book = self.book()
        members = self.captured(book, self.full_results())
        code, intake, err = self.d.intake(self.bdir, self.pp, members, name="normal-intake", book=book)
        self.assertEqual((code, intake["status"], intake["findings"], intake["incomplete"]), (0, "complete", [], []), err)
        self.assertEqual([x["status"] for x in intake["stage_status"]], ["completed"] * 5)
        self.assertEqual([x["required"] for x in intake["stage_status"]], [True, True, True, True, False])
        ip = self.d.path("normal-intake") / "intake.json"
        isha = hashlib.sha256(ip.read_bytes()).hexdigest()
        synth = {"schema": "colab-review-synthesis/1", "plan_id": "plan-1", "intake_sha256": isha,
                 "by": "SYNTHETIC preservation", "label": "SYNTHETIC",
                 "items": [{"id": "X01", "title": "SYNTHETIC: terminology", "findings": ["R01-S02-F01", "R02-S02-F01"],
                            "recommendation": "SYNTHETIC: define both terms."}],
                 "retained": [{"finding": "R02-S02-F02", "disposition": "minority", "reason": "SYNTHETIC: one reader only; kept open", "of": None}],
                 "disagreements": [], "incomplete": [], "residual_uncertainty": [], "acceptance": None}
        rc, report, rerr = self.d.synthesize(self.d.path("normal-intake"), synth, name="normal-report")
        md = (self.d.path("normal-report") / "REPORT.md").read_text(encoding="utf-8")
        self.assertEqual((rc, report["status"], report["distinctions"]["acceptance"]), (0, "consistent", None), rerr)
        self.assertIn("## Intake diagnostics\n- none", md)
        self.assertIn("SYNTHETIC: section 2 conflates two terms.", md)
        self.assertIn("    target: T01", md)
        self.assertIn("    location: SYNTHETIC section", md)
        self.assertIn("  - text: SYNTHETIC: the fallback path is untested.", md)
        self.assertIn("R02-S02-F02: minority", md)
        self.assertIn("Mapping consistency: consistent. Required review: complete. Acceptance: none.", md)

    def test_16_required_missing_and_failed_reviewers_remain_incomplete(self):
        R = self.d.result
        missing = [R(self.pb, "R01", "S01"), R(self.pb, "R02", "S01"), R(self.pb, "R01", "S02", [], comprehension=False)]
        code, intake, err, rc, report, rerr, md = self.walk("required-missing", missing)
        self.assertEqual((code, intake["status"]), (1, "incomplete"), err)
        self.assertIn({"reviewer": "R02", "stage": "S02", "status": "absent"}, intake["incomplete"])
        self.assertEqual((rc, report["status"], report["distinctions"]["required_review"]), (0, "consistent", "incomplete"), rerr)
        self.assertIn("- R02 S02: absent", md)
        self.assertIn("R02 S02 required absent (absent)", md)
        self.assertIn("Investigation is incomplete.", md)
        failed = self.required()
        failed[3] = R(self.pb, "R02", "S02", [], status="failed", comprehension=False)
        code, intake, err, rc, report, rerr, md = self.walk("required-failed", failed)
        self.assertEqual((code, intake["status"], intake["incomplete"]),
                         (1, "incomplete", [{"reviewer": "R02", "stage": "S02", "status": "failed"}]), err)
        self.assertIn("- R02 S02: failed", md)
        self.assertIn("R02 S02 required failed", md)
        self.assertEqual(report["findings"], [])
        self.assertEqual((rc, report["intake_status"]), (0, "incomplete"), rerr)

    def test_17_a_version_1_intake_still_synthesizes_without_an_invented_inventory(self):
        code, intake, err, rc, report, rerr, md = self.walk("old-intake", self.required())
        self.assertEqual(code, 0, err)
        ip = self.d.path("old-intake-intake") / "intake.json"
        old = json.loads(ip.read_text(encoding="utf-8"))
        self.assertEqual(old["schema"], "colab-review-intake/2")
        old["schema"] = "colab-review-intake/1"
        old.pop("stage_status")
        folder = self.d.path("old-v1")
        folder.mkdir()
        raw = F.canonical(old)
        (folder / "intake.json").write_bytes(raw)
        synth = {"schema": "colab-review-synthesis/1", "plan_id": "plan-1", "intake_sha256": hashlib.sha256(raw).hexdigest(),
                 "by": "SYNTHETIC preservation", "label": "SYNTHETIC", "items": [], "retained": [],
                 "disagreements": [], "incomplete": old["incomplete"], "residual_uncertainty": [], "acceptance": None}
        rc, report, rerr = self.d.synthesize(folder, synth, name="old-v1-report")
        md = (self.d.path("old-v1-report") / "REPORT.md").read_text(encoding="utf-8")
        note = "not recorded: intake is colab-review-intake/1 and has no reviewer/stage inventory"
        self.assertEqual((rc, report["schema"], report["stage_status"], report["stage_status_note"]), (0, "colab-review-report/2", None, note), rerr)
        self.assertEqual(report["intake_findings"], old["findings"])
        self.assertIn(note, md)
        self.assertNotIn("R01 S03", md)
        broken = dict(old, schema="colab-review-intake/2")
        bdir = self.d.path("broken-v2")
        bdir.mkdir()
        (bdir / "intake.json").write_bytes(F.canonical(broken))
        code, out, _ = F.run(F.ADAPTER, "synthesize", "--intake", bdir / "intake.json",
                             "--synthesis", self.d.write("broken-synthesis.json", synth), "--out", self.d.path("broken-report"))
        self.assertEqual(code, 2)
        self.assertIn("stage_status must be a list", out)


class TestPins(unittest.TestCase):
    def test_11_pin_mismatch_launches_nothing(self):
        d = F.Desk(prefix="crv-pin-")
        try:
            fake = d.write("fake_producer.py", b"print('should never run')\n")
            with mock.patch.object(cr.subprocess, "run") as run:
                with self.assertRaises(cr.Refusal) as ctx:
                    cr.launch(cr.load_config(str(d.config)), "producer", str(fake), ["verify"])
                run.assert_not_called()
            self.assertIn("not the pinned code", str(ctx.exception))
            code, out, _ = F.run(F.ADAPTER, "stage", "--plan", d.write("p.json", d.plan()), "--request", d.write("r.json", d.base_request()),
                                 "--repo", str(F.WS), "--out-request", d.path("x.json"))
            self.assertEqual(code, 2)
            self.assertIn("outside the workshop tree", out)
        finally:
            d.close()


if __name__ == "__main__":
    unittest.main()
