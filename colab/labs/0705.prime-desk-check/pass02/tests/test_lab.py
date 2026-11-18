"""Self-tests for the 0705 pass02 checker, using SYNTHETIC observations only. Not desk evidence.

  python -I -B tests/test_lab.py --pack-manifest ABS [--report ABS]

Builds fixtures from pack05.02 snapshots into a new temp directory, materializes synthetic observations,
plants faults in copies, and runs check.py in separate processes. Expected refusals are passes here.
"""
import argparse
import copy
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
PY = [sys.executable, "-I", "-B"]
ARGS = {}
RUNS = []


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(label, argv):
    p = subprocess.run(PY + [str(a) for a in argv], capture_output=True, timeout=300,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    RUNS.append({"label": label, "argv": [Path(sys.executable).name, "-I", "-B"] + [str(a).replace(str(Base.tmp), "<tmp>") for a in argv],
                 "exit": p.returncode, "stdout_sha256": hashlib.sha256(p.stdout).hexdigest(),
                 "stderr": p.stderr.decode("utf-8", "replace")[:400]})
    return p


class Base(unittest.TestCase):
    tmp = None

    @classmethod
    def setUpClass(cls):
        Base.tmp = Path(tempfile.mkdtemp(prefix="desk-0705-"))
        tmp = Base.tmp
        cls.addClassCleanup(lambda: shutil.rmtree(tmp, onexc=lambda f, p, e: (os.chmod(p, stat.S_IWRITE), f(p))))  # also after a failed setUpClass
        cls.fix = Base.tmp / "fixtures"
        p = run("build all fixtures", [LAB / "build_fixture.py", "--cases", LAB / "cases.json", "--manifest", ARGS["manifest"], "--out", cls.fix])
        assert p.returncode == 0, p.stderr
        cls.pos = Base.tmp / "obs-positive"
        p = run("materialize synthetic observations", [LAB / "synth_obs.py", "--expected", LAB / "expected.json", "--fixtures", cls.fix, "--out", cls.pos])
        assert p.returncode == 0, p.stderr
        cls.exp_sha = sha(LAB / "expected.json")
        cls.n = 0

    def variant(self, edit=None, drop=(), raw=None):
        """Copy the positive observations, apply an edit(name -> obs) and drops, return the dir."""
        type(self).n += 1
        d = Base.tmp / f"obs-{type(self).n:03d}"
        shutil.copytree(self.pos, d)
        for name in drop:
            (d / name).unlink()
        for name, text in (raw or {}).items():
            (d / name).write_bytes(text.encode("utf-8"))
        if edit:
            for name, fn in edit.items():
                o = json.loads((d / name).read_bytes())
                fn(o)
                (d / name).write_bytes(json.dumps(o).encode("utf-8"))
        return d

    def check(self, label, obs, manual=None, results=None, expected=None, exp_sha=None):
        argv = [LAB / "check.py", "--expected", expected or LAB / "expected.json", "--expected-sha256", exp_sha or self.exp_sha,
                "--fixtures", self.fix, "--observations", obs]
        if manual:
            argv += ["--manual-checklist", manual]
        if results:
            argv += ["--manual-results", results]
        p = run(label, argv)
        rep = json.loads(p.stdout.decode("utf-8"))
        return p.returncode, rep

    def status(self, rep, aid):
        return next(r["status"] for r in rep["rows"] if r["id"] == aid)


def work(o, ref):
    return next(w for w in o["works"] if w["work_ref"] == ref)


R03, R04, R24 = "0522.review-construction/05.03", "0522.review-construction/05.04", "0524.prime-desk/05.01"


class Verdicts(Base):
    def test_01_synthetic_positive_all_pass_but_not_desk_evidence(self):
        code, rep = self.check("synthetic positive", self.pos)
        self.assertEqual(rep["assertions"]["by_status"]["pass"], rep["assertions"]["defined"])
        self.assertEqual(rep["run_class"], "synthetic-self-test")
        self.assertEqual(rep["desk_verdict"], "not-applicable (synthetic self-test)")
        self.assertEqual(code, 1)

    def test_02_candidate_label_without_connected_adapter_or_manual_is_not_passed(self):
        def as_candidate(o):
            o["producer"]["kind"] = "candidate"
        d = self.variant({f: as_candidate for f in os.listdir(self.pos)})
        code, rep = self.check("candidate label, adapter not connected", d, manual=LAB / "manual-checklist.json")
        self.assertEqual(rep["desk_verdict"], "not-passed")
        self.assertIn("adapter-not-connected", rep["blocking"])
        self.assertTrue(any(b.startswith("manual:") for b in rep["blocking"]))
        self.assertEqual(rep["manual"]["by_status"]["needs-human-assessment"], rep["manual"]["defined"])

    def test_03_verdict_logic_requires_everything_and_one_missing_attribution_blocks(self):
        def connected(o):
            o["producer"]["kind"] = "candidate"
            o["producer"]["adapter"] = {"id": "VERDICT-LOGIC-TEST (not a real adapter)", "sha256": "0" * 64, "status": "connected"}
        d = self.variant({f: connected for f in os.listdir(self.pos)})
        items = json.loads((LAB / "manual-checklist.json").read_bytes())["items"]
        res = Base.tmp / "manual-all-yes.json"
        res.write_bytes(json.dumps({"schema": "desk-manual-results/1", "items": [{"id": i["id"], "answer": "yes", "by": "TEST", "date": "2026-11-01", "note": "verdict-logic test"} for i in items]}).encode())
        code, rep = self.check("verdict logic: all gates satisfied (forged labels in a test)", d, LAB / "manual-checklist.json", res)
        self.assertEqual((code, rep["desk_verdict"]), (0, "pass"))
        res2 = Base.tmp / "manual-one-unattributed.json"
        bad = json.loads(res.read_bytes())
        bad["items"][0]["by"] = None
        res2.write_bytes(json.dumps(bad).encode())
        code, rep = self.check("verdict logic: one manual item unattributed", d, LAB / "manual-checklist.json", res2)
        self.assertEqual((code, rep["desk_verdict"]), (1, "not-passed"))
        self.assertEqual(rep["manual"]["by_status"]["needs-human-assessment"], 1)


class PlantedFaults(Base):
    def expect(self, label, edit, cases):
        code, rep = self.check(label, self.variant(edit))
        for aid, st in cases.items():
            self.assertEqual(self.status(rep, aid), st, f"{label}: {aid}")
        self.assertNotEqual(rep["desk_verdict"], "pass")
        return rep

    def test_wrong_selected_work(self):
        self.expect("wrong selected work", {"C01.json": lambda o: o["selected"].update(work_ref=R04)}, {"A-C01-01": "wrong"})

    def test_omitted_hold(self):
        self.expect("omitted hold H1", {"C07.json": lambda o: o.update(holds=[])}, {"A-C07-01": "wrong"})
        self.expect("omitted hold H9", {"C10.json": lambda o: o.update(holds=[])}, {"A-C10-01": "wrong"})

    def test_unattributed_director_wording(self):
        def f(o):
            for q in o["quotes"]:
                if q["kind"] == "verbatim":
                    q["attributed_to"] = "Codex Prime"
        self.expect("Director words attributed to Prime", {"C05.json": f}, {"A-C05-01": "wrong"})

    def test_false_verified_running(self):
        self.expect("supplied running shown as observed", {"C09.json": lambda o: o["workers"][0].update(basis="observed")}, {"A-C09-01": "wrong"})

    def test_missing_receipt_shown_complete(self):
        self.expect("custody shown complete", {"C06.json": lambda o: work(o, R03)["custody"].update(state="complete"),
                                               "C04.json": lambda o: work(o, "0521.return-placement/05.03")["custody"].update(state="complete")},
                    {"A-C06-01": "wrong", "A-C04-01": "wrong"})

    def test_silent_unsupported_coverage(self):
        def f(o):
            o["works"] = [w for w in o["works"] if w["work_ref"] not in (R24, "1524.prime-desk/05.01")]
            o["coverage"] = []
        rep = self.expect("return form silently dropped", {"C17.json": f, "C08.json": lambda o: o.update(coverage=[])}, {"A-C08-01": "wrong"})
        self.assertIn(self.status(rep, "A-C17-01"), ("missing", "wrong"))
        self.assertIn(self.status(rep, "A-C17-02"), ("missing", "wrong"))

    def test_unmapped_is_unsupported_not_pass(self):
        rep = self.expect("adapter declares holds unmapped", {"C07.json": lambda o: o["producer"].update(unmapped=["holds"])}, {"A-C07-01": "unsupported"})
        self.assertGreaterEqual(rep["assertions"]["by_status"]["unsupported"], 1)

    def test_changed_source_hash_reported_ok(self):
        self.expect("changed hash reported ok", {"C13.json": lambda o: o["sources"][0].update(status="ok")}, {"A-C13-01": "wrong"})

    def test_wrong_book_instance(self):
        self.expect("wrong instance selected", {"C03.json": lambda o: o["instance"].update(selected="instance-B")}, {"A-C03-01": "wrong"})

    def test_hidden_overflow(self):
        def f(o):
            o["attention"].update(total=40, shown=10, items=[{"kind": "awaiting-review", "ref": f"x{i}"} for i in range(10)], overflow_route=None)
        self.expect("overflow hidden without route", {"C10.json": f}, {"A-C10-03": "wrong"})

    def test_absent_and_malformed_output(self):
        code, rep = self.check("C02 absent, C18 malformed", self.variant(drop=["C02.json"], raw={"C18.json": "{not json"}))
        self.assertTrue(all(r["status"] == "not-run" for r in rep["rows"] if r["case"] == "C02"))
        self.assertTrue(all(r["status"] == "wrong" for r in rep["rows"] if r["case"] == "C18"))
        self.assertTrue(any("cases not observed" in b for b in rep["blocking"]))

    def test_restart_second_absent_or_different(self):
        code, rep = self.check("C14 second absent", self.variant(drop=["C14.second.json"]))
        self.assertEqual(self.status(rep, "A-C14-01"), "not-run")
        code, rep = self.check("C14 second differs", self.variant({"C14.second.json": lambda o: o.update(identity_fingerprint="other")}))
        self.assertEqual(self.status(rep, "A-C14-01"), "wrong")


class OracleIntegrity(Base):
    def test_tampered_expected_is_checker_error(self):
        e = json.loads((LAB / "expected.json").read_bytes())
        e["assertions"] = e["assertions"][1:]
        p = Base.tmp / "expected-tampered.json"
        p.write_bytes(json.dumps(e).encode())
        code, rep = self.check("tampered expected, old pin", self.pos, expected=p)
        self.assertEqual((code, rep["result"]), (2, "checker-error"))
        code, rep = self.check("tampered expected, new pin (visible)", self.pos, expected=p, exp_sha=sha(p))
        self.assertEqual(rep["assertions"]["defined"], 53)
        self.assertNotEqual(rep["expected_sha256"], self.exp_sha)

    def test_changed_expected_value_fails_honest_observation(self):
        e = json.loads((LAB / "expected.json").read_bytes())
        for x in e["assertions"]:
            if x["id"] == "A-C01-01":
                x["value"] = R04
        p = Base.tmp / "expected-changed.json"
        p.write_bytes(json.dumps(e).encode())
        code, rep = self.check("changed expected value", self.pos, expected=p, exp_sha=sha(p))
        self.assertEqual(self.status(rep, "A-C01-01"), "wrong")

    def test_missing_fixture_manifest_is_checker_error(self):
        f2 = Base.tmp / "fixtures-partial"
        shutil.copytree(self.fix, f2)
        (f2 / "C08" / "fixture-manifest.json").unlink()
        argv = [LAB / "check.py", "--expected", LAB / "expected.json", "--expected-sha256", self.exp_sha, "--fixtures", f2, "--observations", self.pos]
        rep = json.loads(run("fixture manifest missing", argv).stdout)
        self.assertEqual(self.status(rep, "A-C08-01"), "checker-error")

    def test_builder_refuses_occupied_output_and_checkout(self):
        p = run("builder: occupied output", [LAB / "build_fixture.py", "--cases", LAB / "cases.json", "--manifest", ARGS["manifest"], "--out", self.fix])
        self.assertEqual(p.returncode, 2)
        inside = LAB / "SHOULD-NOT-EXIST"
        p = run("builder: output inside checkout", [LAB / "build_fixture.py", "--cases", LAB / "cases.json", "--manifest", ARGS["manifest"], "--out", inside])
        self.assertEqual(p.returncode, 2)
        self.assertFalse(inside.exists())

    def test_fixture_bytes_equal_snapshots_except_generated(self):
        man_path = Path(ARGS["manifest"])
        pins = {r["path"]: r["sha256"] for r in json.loads(man_path.read_bytes())["sources"]}
        for fm_path in self.fix.glob("*/fixture-manifest.json"):
            fm = json.loads(fm_path.read_bytes())
            gen = set(fm["generated"])
            for inst, data in fm["instances"].items():
                for rel, h in data["files"].items():
                    if f"{inst}/{rel}" not in gen:
                        self.assertEqual(h, pins[rel], f"{fm['case']} {inst}/{rel}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack-manifest", required=True)
    ap.add_argument("--report")
    a, rest = ap.parse_known_args()
    ARGS["manifest"] = a.pack_manifest
    prog = unittest.main(argv=[sys.argv[0], "-v"] + rest, exit=False)
    res = prog.result
    if a.report:
        Path(a.report).write_bytes((json.dumps({"schema": "desk-lab-selftest/1", "label": "SYNTHETIC checker self-tests; not desk evidence",
                                                "python": sys.version.split()[0], "tests_run": res.testsRun,
                                                "failures": len(res.failures), "errors": len(res.errors), "skipped": len(res.skipped),
                                                "runs": RUNS}, indent=1) + "\n").encode("utf-8"))
    sys.exit(0 if res.wasSuccessful() else 1)
