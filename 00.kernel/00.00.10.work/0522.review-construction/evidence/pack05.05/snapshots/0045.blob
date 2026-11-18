"""Tests for the 05.03 correction: failed observation is distinct from observed absent custody, reader diagnostics are
kept (bounded, with retained full output under a journal), invalid bindings never become reviews, and packet coverage is
exposed. Disposable books; real pinned dependencies; synthetic SUPPLIED decisions only. No model, no shared checkout write.

  python -B -X dev tests/test_observation.py -v
"""
import hashlib
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import fixture as F  # noqa: E402
import prime_cycle as pc  # noqa: E402
from test_prime_cycle import A, Cycle  # noqa: E402

LAB_DIRS = ("prime-cycle-pass01", "batch-observation-pass01", "prime-review-pass01", "review-packet-pass01",
            "return-capture-pass01", "prime-support-pass01")


class Base(Cycle):
    def labs_copy(self, name, drop=()):
        root = self.d.tmp / name
        for d in LAB_DIRS:
            if d not in drop:
                shutil.copytree(F.LABS / d, root / d, ignore=shutil.ignore_patterns("__pycache__", "tests", "colab", "evidence"))
        return root / "prime-cycle-pass01" / "prime_cycle.py"

    def cli_with(self, tool, *args):
        r = subprocess.run([sys.executable, "-B", str(tool), *map(str, args)], capture_output=True, timeout=600)
        return r.returncode, r.stdout.decode("utf-8"), r.stderr.decode("utf-8")

    def absent_work(self, batch="05.02", wid="N"):
        self.d.page(A, batch, F.page_text(None))
        return self.d.work(wid, A, batch, None)

    def fake_reader(self, stdout=b"", stderr=b"", code=0):
        real = pc.run

        def fake(name, args, timeout=300):
            if name == "batch_observe":
                return subprocess.CompletedProcess(args, code, stdout, stderr)
            return real(name, args, timeout)
        return mock.patch.object(pc, "run", fake)


class TestFailedVersusAbsent(Base):
    def test_25_missing_adapter_is_observation_failed_with_retained_diagnostic(self):
        m, w = self.work_with_return()
        wn = self.absent_work()
        reg = self.d.registration([w, wn])
        broken = self.labs_copy("labs-noadapter", drop=("prime-support-pass01",))
        J = self.d.out / "journal"
        code, out, err = self.cli_with(broken, "read", "--registration", reg, "--json", "--journal-root", J)
        self.assertEqual((code, err), (1, ""))
        v = json.loads(out)
        for it in v["works"]:
            with self.subTest(work=it["work_id"]):
                ob = it["observation"]
                self.assertEqual((it["pass_state"], ob["state"], ob["part"], ob["kind"], it["custody"]["state"]),
                                 ("observation-failed", "failed", "source", "reader-exit-2", "unknown"))
                d = ob["diagnostic"]
                self.assertIn("missing clerk_adapter.py", d["excerpt"])
                self.assertEqual(d["source"], "batch_observe stderr")
                kept = Path(d["retained"]["stderr"])
                self.assertEqual(hashlib.sha256(kept.read_bytes()).hexdigest(), d["stderr_sha256"])
                self.assertTrue(kept.parent.parent.parent == J)  # inside this operation's journal folder
                self.assertIn(str(kept), " ".join(it["attention"]))
        self.assertEqual((v["summary"]["observation_failed"], v["summary"]["finished_passes"]), (2, 0))
        code, text, _ = self.cli_with(broken, "read", "--registration", reg)
        self.assertNotIn("no-return", text)
        self.assertIn("observation-failed (source): reader-exit-2: missing clerk_adapter.py; not retained: no --journal-root", text)
        bad_template = v["works"][0]["template"]
        self.assertIsNone(bad_template["binding"]["source"]["page_sha256"])
        code, out, _ = self.record(reg, F.fill(bad_template, "accept-finished-open"), "bad.json")  # full labs: fresh read works
        self.assertEqual(code, 2)
        self.assertIn("template binding has no observed source identity", out)
        _, good = self.d.read(reg)
        dec = self.d.write_decision(F.fill(good["works"][0]["template"], "accept-finished-open"), "good.json")
        code, out, _ = self.cli_with(broken, "record", "--registration", reg, "--decision", dec)
        self.assertEqual(code, 2)
        self.assertIn("refused: observation failed (source): reader-exit-2: missing clerk_adapter.py", out)
        self.assertIn("nothing was recorded", out)
        self.assertIn("not retained: no --journal-root", out)
        self.assertFalse((self.d.repo / w["review_location"]).exists())

    def test_26_invalid_reader_results_are_classified_and_bounded(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w], bounds={"max_works": 16, "max_page_bytes": 262144, "max_output_bytes": 200000})
        noisy = ("line one\r\n\tTAB \x07bell " + "x" * 5000).encode()
        cases = {"reader-report-invalid": dict(stdout=b"{not json", stderr=b""),
                 "no-source-identity": dict(stdout=b'{"source": {}}', stderr=b"", code=1),
                 "reader-output-over-bound": dict(stdout=b"{" + b" " * 200001 + b"}", stderr=b""),
                 "reader-exit-3": dict(stdout=b"", stderr=noisy, code=3)}
        for kind, kw in cases.items():
            with self.subTest(kind=kind), self.fake_reader(**kw):
                v = pc.read(reg)
                it = v["works"][0]
                ob = it["observation"]
                self.assertEqual((it["pass_state"], ob["kind"]), ("observation-failed", kind))
                d = ob["diagnostic"]
                self.assertLessEqual(len(d["excerpt"]), pc.JSON_EXCERPT + len("…[truncated]"))
                self.assertEqual(d["stdout_bytes"], len(kw["stdout"]))
                line = [a for a in it["attention"] if a.startswith("observation-failed (source)")][0]
                shown = line.split(": ", 2)[2].split("; not retained")[0]
                self.assertLessEqual(len(shown), pc.TEXT_EXCERPT)
                self.assertNotIn("\n", line)
                self.assertNotIn("\x07", line)
                if kind == "reader-exit-3":
                    self.assertIn("\\x07bell", line)
                    self.assertTrue(d["excerpt"].endswith("…[truncated]"))
                    self.assertEqual(d["source"], "batch_observe stderr")
                else:
                    self.assertEqual(d["source"], "prime_cycle reason (reader stderr was empty)")

    def test_27_observed_absent_present_and_unresolved_stay_distinct(self):
        m, w = self.work_with_return()
        wn = self.absent_work()
        self.d.page(A, "05.03", F.page_text(None))
        wu = self.d.work("U", A, "05.03", m)  # registered member the page does not name
        m2, wt = self.work_with_return(lane="0598.cycle-b", wid="T")
        blob = self.d.book / m2 / "payload" / "0001.blob"
        blob.write_bytes(blob.read_bytes() + b"x")  # the inspector reports incomplete (hash mismatch payload)
        code, v = self.d.read(self.d.registration([w, wn, wu, wt]))
        got = {it["work_id"]: (it["pass_state"], it["observation"]["state"], it["custody"]["state"]) for it in v["works"]}
        self.assertEqual(got["A"], ("awaiting-review", "observed", "present"))
        self.assertEqual(got["N"], ("no-return", "observed", "absent"))
        self.assertEqual(got["U"], ("custody-unresolved", "observed", "unresolved"))
        self.assertEqual(got["T"], ("custody-unresolved", "observed", "unresolved"))  # observed, but not absence
        t = [it for it in v["works"] if it["work_id"] == "T"][0]
        self.assertEqual(t["custody"]["role"], "incomplete")
        self.assertIn("role incomplete", t["custody"]["state_reason"])
        self.assertEqual(v["summary"]["custody_unresolved"], sum(g[0] == "custody-unresolved" for g in got.values()))
        u = [it for it in v["works"] if it["work_id"] == "U"][0]
        self.assertTrue(any(a.startswith("custody-unresolved: registered member") for a in u["attention"]))

    def test_28_failed_custody_observation_is_failed_not_absent(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        args = ["observe", "--json", "--repo", str(self.d.repo), "--live", "--path", w["page"], "--members-book", str(self.d.book)]
        real = subprocess.run([sys.executable, "-B", str(pc.pin_path("batch_observe")), *args], capture_output=True)
        o = json.loads(real.stdout)
        for x in o["custody"]["observations"]:
            x["role"], x["exit"], x["attention"] = "observation-failed", 2, ["observation-failed"]
        o["custody"]["primary"] = None
        with self.fake_reader(stdout=json.dumps(o).encode(), code=1):
            v = pc.read(reg)
            it = v["works"][0]
            self.assertEqual((it["pass_state"], it["observation"]["part"], it["observation"]["kind"]),
                             ("observation-failed", "custody", "member-observation-failed"))
            self.assertIn("inspect exit 2", it["observation"]["diagnostic"]["excerpt"])
            _, good = self.d.read(reg)
            path = self.d.write_decision(F.fill(good["works"][0]["template"], "accept-finished-open"), "d.json")
            with self.assertRaises(pc.Refusal) as ctx:
                pc.record(reg, path)
            self.assertIn("observation failed (custody): member-observation-failed", str(ctx.exception))
        self.assertFalse((self.d.repo / w["review_location"]).exists())


class TestHistoryUnderFailure(Base):
    def test_29_completed_review_and_hold_under_failed_observation(self):
        m, w = self.work_with_return()
        mb, wb = self.work_with_return(lane="0598.cycle-b", wid="B")
        reg = self.d.registration([w, wb])
        _, v = self.d.read(reg)
        self.assertEqual(self.record(reg, F.fill(self.tmpl(v, 0), "complete"), "c.json")[0], 0)
        self.assertEqual(self.record(reg, F.fill(self.tmpl(v, 1), "director-input"), "h.json")[0], 1)
        broken = self.labs_copy("labs-noadapter", drop=("prime-support-pass01",))
        code, out, _ = self.cli_with(broken, "read", "--registration", reg, "--json")
        v2 = json.loads(out)
        a, b = v2["works"]
        self.assertEqual((a["pass_state"], a["goal_terminal"], a["pass_terminal"], a["historical"]["reason"], a["historical"]["goal_terminal"]),
                         ("observation-failed", "unknown", "unknown", "observation-failed", "completed"))
        self.assertFalse(a["latest_review"]["current"])
        self.assertNotIn("review-stale", " ".join(a["attention"]))
        self.assertEqual((v2["summary"]["completed_goals"], v2["summary"]["finished_passes"]), (0, 0))
        self.assertEqual((b["holds"][0]["hold_id"], b["holds"][0]["status"]), ("H1", "unresolved"))
        self.assertTrue(any("still blocking" in x for x in b["attention"]))
        _, text, _ = self.cli_with(broken, "read", "--registration", reg)
        self.assertNotIn(": completed\n", text)
        self.assertIn("unknown (historical completed in 05.01-r1, observation-failed)", text)
        _, v3 = self.d.read(reg)  # full labs again: the same review is current again, nothing was rewritten
        self.assertEqual((v3["works"][0]["pass_state"], v3["works"][0]["goal_terminal"]), ("reviewed", "completed"))


class TestPacketCoverage(Base):
    def test_30_packet_reports_its_own_coverage(self):
        m, w = self.work_with_return()
        reg = self.d.registration([w])
        J = self.d.tmp / "journal"
        code, out, _ = self.d.cli("packet", "--registration", reg, "--work", "A", "--out", self.d.out / "p1", "--journal-root", J)
        self.assertEqual(code, 0, out)
        self.assertIn("coverage (this packet's own request; not a complete artifact inventory):", out)
        self.assertIn("page included: no (not requested: the default request adds the page only for a git-blob registration)", out)
        self.assertIn("member captured payloads not gathered: 1 - note.txt", out)
        self.assertIn("artifact checks requested: 0", out)
        end = json.loads(next(J.glob("*/*/end.json")).read_text(encoding="utf-8"))
        cov = end["machine"]["result"]["coverage"]
        self.assertEqual((cov["gathered"], cov["page_included"], cov["member_payloads_not_gathered"]), (["receipt", "return"], False, ["note.txt"]))
        self.assertEqual(sorted(p.name for p in (self.d.out / "p1").iterdir() if p.is_file()),
                         ["PACKET.md", "assembly-status.json", "custody-stderr.txt", "custody.json", "helper-verify-stderr.txt",
                          "helper-verify.txt", "manifest.json", "packet.json"])  # nothing added to the packet folder
        commit = self.d.commit()
        regg = self.d.registration([w], source={"kind": "git-blob", "commit": commit}, name="regg.json")
        code, out, _ = self.d.cli("packet", "--registration", regg, "--work", "A", "--out", self.d.out / "p2")
        self.assertEqual(code, 0, out)
        self.assertIn("page included: yes", out)
        self.assertIn("page (git-blob) present", out)
        code, out, _ = self.d.cli("packet", "--registration", reg, "--work", "A", "--out", self.d.tmp / "elsewhere")
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
