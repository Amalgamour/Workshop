"""Batch 0503.worker-bridge/05.01 #03: transport, failure and recovery boundaries, against PROTOCOL TEST WORKERS.

  python -B tests/test_bridge.py -v        (from the lab folder)

Every run lives under scratch/tests/ (ignored). An expected refusal is a passing test.
"""
import hashlib, json, os, subprocess, sys, tempfile, unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
from bridge.adapter import LocalProcessAdapter, StoreError  # noqa: E402
from bridge.canon import canonical  # noqa: E402

SCRATCH = LAB / "scratch" / "tests"
PROFILES = {k: v for k, v in json.loads((LAB / "profiles.json").read_text(encoding="utf-8")).items() if not k.startswith("_")}
TEXT = "alpha\n\n  \nbeta\n\tgamma\n".encode("utf-8")   # 3 non-blank lines


class Bridge(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.base = Path(tempfile.mkdtemp(prefix=self._testMethodName[:24] + "-", dir=SCRATCH))
        self.inp, self.out, self.store = self.base / "in", self.base / "out", self.base / "store"
        for d in (self.inp, self.out):
            d.mkdir()
        (self.inp / "input.txt").write_bytes(TEXT)
        self.ad = LocalProcessAdapter(self.store, PROFILES, LAB)

    def env(self, backend="fixture-ok", delivery="d-001", **over):
        e = {"schema": "worker-bridge/request@1", "delivery_id": delivery, "job_id": "job-count-lines", "role": "builder",
             "work_ref": "00.kernel/00.00.10.work/0503.worker-bridge/05.01.md#02",
             "inputs": [{"name": "text", "path": "input.txt", "sha256": hashlib.sha256(TEXT).hexdigest(), "bytes": len(TEXT)}],
             "input_root": str(self.inp), "output_root": str(self.out),
             "limits": {"timeout_s": 20, "max_stdout_bytes": 100000, "max_stderr_bytes": 100000},
             "release": {"by": "fixture producer (lab only)", "ref": "test"}, "backend": backend}
        e.update(over)
        return e

    def launches(self):
        p = self.out / "launches.log"
        return p.read_text(encoding="utf-8").splitlines() if p.exists() else []

    # ---- success ----
    def test_success_collected_and_fresh_process_reads_receipt(self):
        r = self.ad.deliver(self.env())
        self.assertEqual((r["transport"], r["collection"], r["claimed_outcome"]), ("delivered", "collected", "done"), r)
        self.assertEqual(json.loads((self.out / "result.json").read_bytes()), {"count": 3})
        self.assertEqual(r["worker_kind"], "protocol test worker")
        self.assertEqual(r["review"], "not performed")
        fresh = subprocess.run([sys.executable, "-B", "-m", "bridge.cli", "status", "--store", str(self.store), "--delivery", "d-001"],
                               cwd=LAB, capture_output=True, text=True)
        self.assertEqual(json.loads(fresh.stdout)["collection"], "collected", fresh.stdout + fresh.stderr)

    # ---- identity and shape ----
    def test_wrong_result_identity(self):
        r = self.ad.deliver(self.env("fixture-wrong-id"))
        self.assertEqual(r["transport"], "malformed")
        self.assertIn("delivery_id", r["reason"])
        self.assertTrue(r["outcome_uncertain"])

    def test_altered_input_hash_refused_before_launch(self):
        e = self.env()
        e["inputs"][0]["sha256"] = "0" * 64
        r = self.ad.deliver(e)
        self.assertEqual(r["transport"], "refused")
        self.assertFalse((self.store / "d-001" / "launch.json").exists())
        self.assertEqual(self.launches(), [])

    def test_invalid_result_shape(self):
        r = self.ad.deliver(self.env("fixture-bad-shape"))
        self.assertEqual(r["transport"], "malformed")
        self.assertIn("outcome", r["reason"])

    def test_invalid_envelope_and_unknown_backend_refused(self):
        self.assertEqual(self.ad.deliver({**self.env(), "approved": True})["transport"], "refused")
        r = self.ad.deliver(self.env(backend="python -c evil"))
        self.assertEqual(r["transport"], "refused")
        self.assertIn("not an allowlisted profile", r["reason"])
        self.assertEqual(self.launches(), [])

    # ---- process failures ----
    def test_crash_nonzero(self):
        r = self.ad.deliver(self.env("fixture-crash"))
        self.assertEqual((r["transport"], r["returncode"]), ("crashed", 3))
        self.assertTrue(r["outcome_uncertain"])
        self.assertIn(b"simulated crash", (self.store / "d-001" / "attempt" / "stderr.bin").read_bytes())

    def test_malformed_and_partial_output(self):
        for i, b in enumerate(("fixture-garbage", "fixture-partial")):
            with self.subTest(backend=b):
                r = self.ad.deliver(self.env(b, delivery=f"d-m{i}"))
                self.assertEqual(r["transport"], "malformed")
                self.assertIn("not one JSON value", r["reason"])

    def test_excessive_output(self):
        r = self.ad.deliver(self.env("fixture-flood"))
        self.assertEqual(r["transport"], "output-limit")
        self.assertTrue(r["outcome_uncertain"])
        self.assertLessEqual(r["diagnostics"]["stdout"]["bytes"], 100000)

    def test_timeout_uncertain_and_not_relaunched(self):
        e = self.env("fixture-sleep", limits={"timeout_s": 1.5, "max_stdout_bytes": 1000, "max_stderr_bytes": 1000})
        r = self.ad.deliver(e)
        self.assertEqual(r["transport"], "timeout")
        self.assertTrue(r["outcome_uncertain"])
        self.assertTrue((self.out / "started.marker").exists(), "work had started before the kill")
        again = self.ad.deliver(e)
        self.assertTrue(again.get("replayed"))
        self.assertEqual(len(self.launches()), 1, "the ambiguous task was not relaunched")

    # ---- duplicates and reuse ----
    def test_duplicate_identical_applies_once(self):
        r1 = self.ad.deliver(self.env())
        m1 = (self.out / "result.json").stat().st_mtime_ns
        r2 = self.ad.deliver(self.env())
        self.assertTrue(r2.get("replayed"))
        self.assertEqual({k: v for k, v in r2.items() if k != "replayed"}, r1)
        self.assertEqual(len(self.launches()), 1)
        self.assertEqual((self.out / "result.json").stat().st_mtime_ns, m1)

    def test_conflicting_identity_reuse_refused(self):
        self.ad.deliver(self.env())
        r = self.ad.deliver(self.env(job_id="job-other"))
        self.assertEqual(r["transport"], "refused")
        self.assertIn("reused with a different request", r["reason"])
        self.assertEqual(len(self.launches()), 1)

    # ---- interrupted recording and recovery ----
    def test_crash_before_receipt_then_recover_without_relaunch(self):
        with self.assertRaises(StoreError):
            self.ad.deliver(self.env(), _test_crash_before_receipt=True)
        st = self.ad.status("d-001")
        self.assertEqual(st["state"], "uncertain")
        again = self.ad.deliver(self.env())
        self.assertEqual(again["transport"], "uncertain")
        self.assertEqual(len(self.launches()), 1, "no automatic repeat")
        rec = self.ad.recover("d-001")
        self.assertEqual((rec["recovered"], rec["collection"]), (True, "collected"))
        self.assertEqual(len(self.launches()), 1)

    def test_interrupted_receipt_write_leaves_tmp_and_recovers(self):
        with self.assertRaises(OSError):
            self.ad.deliver(self.env(), _test_crash_in_receipt=True)
        d = self.store / "d-001"
        self.assertTrue((d / "receipt.json.tmp").exists())
        self.assertFalse((d / "receipt.json").exists())
        self.assertEqual(self.ad.status("d-001")["state"], "uncertain")
        rec = self.ad.recover("d-001")
        self.assertTrue(rec["recovered"])
        self.assertTrue((d / "receipt.json").exists())

    def test_launch_record_without_attempt_stays_uncertain(self):
        d = self.store / "d-001"
        d.mkdir(parents=True)
        (d / "request.json").write_bytes(canonical(self.env()))
        (d / "launch.json").write_bytes(b'{"note": "another launcher got here first"}')
        r = self.ad.deliver(self.env())
        self.assertEqual(r["transport"], "uncertain")
        self.assertFalse(self.ad.recover("d-001")["recovered"])
        self.assertEqual(self.launches(), [])

    # ---- artifacts ----
    def test_missing_artifact(self):
        r = self.ad.deliver(self.env("fixture-missing-artifact"))
        self.assertEqual((r["transport"], r["collection"]), ("delivered", "uncollected"))
        self.assertIn("artifact missing", r["reason"])

    def test_wrong_artifact_hash(self):
        r = self.ad.deliver(self.env("fixture-bad-hash"))
        self.assertEqual(r["collection"], "uncollected")
        self.assertIn("bytes differ", r["reason"])

    def test_artifact_escaping_root(self):
        r = self.ad.deliver(self.env("fixture-escape"))
        self.assertEqual(r["collection"], "uncollected")
        self.assertIn("not a safe relative path", r["reason"])

    def test_artifact_through_junction_refused(self):
        if os.name != "nt":
            self.skipTest("junctions are Windows-only")
        outside = self.base / "outside"
        outside.mkdir()
        j = subprocess.run(["cmd", "/c", "mklink", "/J", str(self.out / "link"), str(outside)], capture_output=True, text=True)
        if j.returncode:
            self.skipTest("could not create a junction")
        (outside / "result.json").write_bytes(b'{"count":3}')
        from bridge import verify
        ok, bad = verify.collect({"artifacts": [{"path": "link/result.json", "sha256": hashlib.sha256(b'{"count":3}').hexdigest(), "bytes": 11}]}, self.out)
        self.assertEqual(ok, [])
        self.assertIn("link or reparse point", bad[0])


if __name__ == "__main__":
    unittest.main()
