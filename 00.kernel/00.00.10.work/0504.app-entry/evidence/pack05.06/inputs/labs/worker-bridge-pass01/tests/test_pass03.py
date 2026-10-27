"""Batch 0503.worker-bridge/05.03 regression (BR-01b): a descendant that inherits stdout/stderr must not hold the
adapter past the deadline plus the cleanup allowance. PROTOCOL TEST WORKERS only; the descendant exits by
itself after 5 s. Runs under scratch/tests-pass03/ (ignored), each delivery inside an outer watchdog process.

  python -B -X dev tests/test_pass03.py -v        (from the lab folder)
"""
import hashlib, json, subprocess, sys, tempfile, time, unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
from bridge.adapter import CLEANUP_ALLOWANCE_S  # noqa: E402
from bridge.canon import canonical  # noqa: E402

SCRATCH = LAB / "scratch" / "tests-pass03"
TEXT = b"one\ntwo\n"
TIMEOUT_S = 0.2
STARTUP_MARGIN_S = 1.5   # documented allowance for process start-up; the reviewed blockage was 5.078 s
BOUND_S = TIMEOUT_S + CLEANUP_ALLOWANCE_S + STARTUP_MARGIN_S   # 3.7 s


class InheritedPipes(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.base = Path(tempfile.mkdtemp(prefix=self._testMethodName[:24] + "-", dir=SCRATCH))
        self.inp, self.out, self.store = self.base / "in", self.base / "out", self.base / "store"
        for d in (self.inp, self.out):
            d.mkdir()
        (self.inp / "input.txt").write_bytes(TEXT)

    def env(self, backend, delivery):
        return {"schema": "worker-bridge/request@1", "delivery_id": delivery, "job_id": "job-count-lines", "role": "builder",
                "work_ref": "00.kernel/00.00.10.work/0503.worker-bridge/05.03.md",
                "inputs": [{"name": "text", "path": "input.txt", "sha256": hashlib.sha256(TEXT).hexdigest(), "bytes": len(TEXT)}],
                "input_root": str(self.inp), "output_root": str(self.out),
                "limits": {"timeout_s": TIMEOUT_S, "max_stdout_bytes": 100000, "max_stderr_bytes": 100000},
                "release": {"by": "fixture producer (lab only)", "ref": "pass03 test"}, "backend": backend}

    def drive(self, env):
        req = self.base / f"{env['delivery_id']}.json"
        req.write_bytes(canonical(env))
        r = subprocess.run([sys.executable, "-B", str(LAB / "tests" / "_driver_pass03.py"), str(self.store), str(req)],
                           capture_output=True, text=True, timeout=40)   # outer watchdog
        self.assertEqual(r.returncode, 0, r.stderr)
        res = json.loads(r.stdout)
        self.calls = getattr(self, "calls", 0) + 1
        (self.base / f"{env['delivery_id']}.call{self.calls}.result.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
        return res

    def launches(self):
        p = self.out / "launches.log"
        return p.read_text(encoding="utf-8").splitlines() if p.exists() else []

    def check_bounded_incomplete(self, res):
        rec = res["receipt"]
        self.assertLess(res["elapsed_s"], BOUND_S, f"deliver() held for {res['elapsed_s']} s; bound {BOUND_S} s")
        self.assertEqual(rec["transport"], "incomplete-output", rec)
        self.assertTrue(rec["outcome_uncertain"])
        self.assertEqual(rec["collection"], "not attempted")
        self.assertIsNone(rec["claimed_outcome"], "partial or late output is never promoted to a result")
        self.assertFalse(rec["cleanup"]["complete"])
        self.assertTrue(rec["cleanup"]["retained"], "the threads still waiting on the descendant are named")

    def test_descendant_holds_pipes_returns_within_bound(self):
        res = self.drive(self.env("fixture-inherit-pipes", "d-inherit"))
        self.check_bounded_incomplete(res)
        self.assertIsNotNone(res["background_finished_after_s"], "the retained readers finished once the descendant exited")
        self.assertEqual(len(self.launches()), 1)
        again = self.drive(self.env("fixture-inherit-pipes", "d-inherit"))
        self.assertTrue(again["receipt"].get("replayed"))
        self.assertEqual(len(self.launches()), 1, "no automatic relaunch")

    def test_complete_result_followed_by_descendant_is_not_promoted(self):
        res = self.drive(self.env("fixture-inherit-pipes-after-result", "d-inherit-result"))
        self.check_bounded_incomplete(res)
        self.assertFalse((self.store / "d-inherit-result" / "attempt" / "stdout.bin").read_bytes() == b"",
                         "the partial snapshot is kept as diagnostics")
        self.assertFalse(self.out.joinpath("result.json").exists() and res["receipt"].get("artifacts"),
                         "no artifact is reported collected")


if __name__ == "__main__":
    unittest.main()
