"""Batch 0503.worker-bridge/05.02 regressions: one deadline over all child I/O (#01), delivery-id and store
containment at every entry (#02), finite usable numeric limits and strict JSON (#03).
PROTOCOL TEST WORKERS only. Every run lives under scratch/tests-pass02/ (ignored).

  python -B -X dev tests/test_pass02.py -v        (from the lab folder)
"""
import hashlib, json, math, os, subprocess, sys, tempfile, time, unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
from bridge.adapter import CLEANUP_ALLOWANCE_S, LocalProcessAdapter, StoreError  # noqa: E402
from bridge.canon import StrictJSONError, canonical, strict_loads  # noqa: E402
from bridge.envelope import MAX_CAPTURE_BYTES, MAX_TIMEOUT_S  # noqa: E402

SCRATCH = LAB / "scratch" / "tests-pass02"
PROFILES = {k: v for k, v in strict_loads((LAB / "profiles.json").read_bytes()).items() if not k.startswith("_")}
TEXT = "alpha\n\n  \nbeta\n\tgamma\n".encode("utf-8")
SPAWN_MARGIN_S = 1.5   # documented allowance for process start-up on this machine, on top of the cleanup allowance


class Base(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.base = Path(tempfile.mkdtemp(prefix=self._testMethodName[:24] + "-", dir=SCRATCH))
        self.inp, self.out, self.store, self.outside = (self.base / n for n in ("in", "out", "store", "outside"))
        for d in (self.inp, self.out, self.store, self.outside):
            d.mkdir()
        (self.inp / "input.txt").write_bytes(TEXT)
        self.sentinel = self.outside / "receipt.json"
        self.sentinel.write_bytes(b'{"sentinel":"outside the configured store"}')
        self.sentinel_hash = hashlib.sha256(self.sentinel.read_bytes()).hexdigest()
        self.ad = LocalProcessAdapter(self.store, PROFILES, LAB)

    def env(self, backend="fixture-ok", delivery="d-001", limits=None, **over):
        e = {"schema": "worker-bridge/request@1", "delivery_id": delivery, "job_id": "job-count-lines", "role": "builder",
             "work_ref": "00.kernel/00.00.10.work/0503.worker-bridge/05.02.md",
             "inputs": [{"name": "text", "path": "input.txt", "sha256": hashlib.sha256(TEXT).hexdigest(), "bytes": len(TEXT)}],
             "input_root": str(self.inp), "output_root": str(self.out),
             "limits": limits or {"timeout_s": 20, "max_stdout_bytes": 100000, "max_stderr_bytes": 100000},
             "release": {"by": "fixture producer (lab only)", "ref": "pass02 test"}, "backend": backend}
        e.update(over)
        return e

    def launches(self):
        p = self.out / "launches.log"
        return p.read_text(encoding="utf-8").splitlines() if p.exists() else []

    def outside_untouched(self):
        self.assertEqual(sorted(p.name for p in self.outside.iterdir()), ["receipt.json"])
        self.assertEqual(hashlib.sha256(self.sentinel.read_bytes()).hexdigest(), self.sentinel_hash)

    def cli(self, *args):
        return subprocess.run([sys.executable, "-B", "-m", "bridge.cli", *args], cwd=LAB, capture_output=True, text=True, timeout=60)


class Deadline(Base):
    """#01: stdin writing, reading, waiting and cleanup all obey one deadline."""

    def driver(self, env, watchdog=40):
        req = self.base / "request.json"
        req.write_bytes(canonical(env))
        r = subprocess.run([sys.executable, "-B", str(LAB / "tests" / "_deliver_driver.py"), str(self.store), str(req)],
                           capture_output=True, text=True, timeout=watchdog)   # outer watchdog
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)

    def test_child_that_never_reads_stdin_and_a_large_valid_envelope(self):
        lim = {"timeout_s": 0.3, "max_stdout_bytes": 1000, "max_stderr_bytes": 1000}
        e = self.env("fixture-no-stdin-reader", limits=lim, work_ref="x" * 2_000_000)   # far larger than a pipe buffer
        res = self.driver(e)
        rec = res["receipt"]
        bound = lim["timeout_s"] + CLEANUP_ALLOWANCE_S + SPAWN_MARGIN_S
        self.assertLess(res["elapsed_s"], bound, f"adapter blocked past the deadline: {res['elapsed_s']} s")
        self.assertEqual(rec["transport"], "timeout")
        self.assertTrue(rec["outcome_uncertain"])
        self.assertIn("allowance_s", rec["cleanup"])
        self.assertEqual(len(self.launches()), 1)
        again = self.driver(e)
        self.assertTrue(again["receipt"].get("replayed"))
        self.assertEqual(len(self.launches()), 1, "no second launch on retry")
        (self.base / "timing.json").write_text(json.dumps({"first": res["elapsed_s"], "bound": bound}), encoding="utf-8")

    def test_small_successful_request_still_collected(self):
        rec = self.driver(self.env())["receipt"]
        self.assertEqual((rec["transport"], rec["collection"]), ("delivered", "collected"))
        self.assertTrue(rec["cleanup"]["complete"])

    def test_stdout_and_stderr_output_limits(self):
        for i, b in enumerate(("fixture-flood", "fixture-flood-stderr")):
            with self.subTest(backend=b):
                rec = self.ad.deliver(self.env(b, delivery=f"d-flood-{i}"))
                self.assertEqual(rec["transport"], "output-limit")
                self.assertTrue(rec["outcome_uncertain"])
                stream = "stdout" if b == "fixture-flood" else "stderr"
                self.assertLessEqual(rec["diagnostics"][stream]["bytes"], 100000)


class Containment(Base):
    """#02: one identity and path validator at every entry; nothing outside the store is read or changed."""

    BAD = ["../outside", "..\\outside", "../outside/receipt.json", "C:\\outside", "C:/outside", "D:outside", "/outside",
           "\\\\server\\share", "", "a/b", "a\\b", "CON", "con", "con.txt", "nul", "lpt1", "com9.x", "abc.", "abc ",
           ".hidden", "Upper", "a..b", "a:b", "x" * 65]

    def test_valid_status_and_recover_still_work(self):
        self.ad.deliver(self.env())
        self.assertEqual(self.ad.status("d-001")["collection"], "collected")
        with self.assertRaises(StoreError):
            self.ad.deliver(self.env(delivery="d-002"), _test_crash_before_receipt=True)
        self.assertTrue(self.ad.recover("d-002")["recovered"])

    def test_library_refuses_bad_ids_before_touching_files(self):
        for bad in self.BAD + [None, 5, ["d-001"], b"d-001"]:
            with self.subTest(id=bad):
                for call in (self.ad.status, self.ad.recover):
                    r = call(bad)
                    self.assertEqual(r["transport"], "refused", r)
                    self.assertNotIn("sentinel", json.dumps(r))
                r = self.ad.deliver(self.env(delivery=bad))
                self.assertEqual(r["transport"], "refused")
        self.outside_untouched()
        self.assertEqual(list(self.store.iterdir()), [])

    def test_cli_refuses_bad_ids(self):
        for bad in ("../outside", str(self.outside), "CON"):
            for cmd in ("status", "recover"):
                with self.subTest(cmd=cmd, id=bad):
                    r = self.cli(cmd, "--store", str(self.store), "--delivery", bad)
                    self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
                    self.assertIn('"refused"', r.stdout)
                    self.assertNotIn("sentinel", r.stdout)
        self.outside_untouched()

    def test_junction_inside_the_store_is_refused(self):
        if os.name != "nt":
            self.skipTest("junctions are Windows-only")
        (self.outside / "launch.json").write_bytes(b'{"x":1}')
        before = {p.name: p.read_bytes() for p in self.outside.iterdir()}
        j = subprocess.run(["cmd", "/c", "mklink", "/J", str(self.store / "evil"), str(self.outside)], capture_output=True, text=True)
        if j.returncode:
            self.skipTest("could not create a junction")
        for call in (self.ad.status, self.ad.recover):
            r = call("evil")
            self.assertEqual(r["transport"], "refused")
            self.assertIn("link or reparse point", r["reason"])
        self.assertEqual(self.ad.deliver(self.env(delivery="evil"))["transport"], "refused")
        r = self.cli("status", "--store", str(self.store), "--delivery", "evil")
        self.assertEqual(r.returncode, 2)
        self.assertEqual({p.name: p.read_bytes() for p in self.outside.iterdir()}, before)


class Limits(Base):
    """#03: limits must be usable, finite and of the right type; refused before launch, through deliver."""

    def refused_before_launch(self, lim, delivery):
        r = self.ad.deliver(self.env(delivery=delivery, limits=lim))
        self.assertEqual(r["transport"], "refused", (lim, r))
        self.assertIn("envelope", r["reason"])
        self.assertFalse((self.store / delivery).exists())
        return r

    def test_invalid_limits(self):
        good = {"timeout_s": 5, "max_stdout_bytes": 1000, "max_stderr_bytes": 1000}
        cases = [("timeout_s", math.inf), ("timeout_s", -math.inf), ("timeout_s", math.nan), ("timeout_s", True), ("timeout_s", False),
                 ("timeout_s", 0), ("timeout_s", -1), ("timeout_s", "5"), ("timeout_s", None), ("timeout_s", MAX_TIMEOUT_S + 1),
                 ("max_stdout_bytes", 1.5), ("max_stdout_bytes", 1000.0), ("max_stdout_bytes", True), ("max_stdout_bytes", 0),
                 ("max_stdout_bytes", -5), ("max_stdout_bytes", "1000"), ("max_stdout_bytes", MAX_CAPTURE_BYTES + 1),
                 ("max_stderr_bytes", math.inf), ("max_stderr_bytes", False), ("max_stderr_bytes", 2.5)]
        for i, (k, v) in enumerate(cases):
            with self.subTest(key=k, value=v):
                self.refused_before_launch({**good, k: v}, f"d-lim-{i}")
        self.refused_before_launch({"timeout_s": True, "max_stdout_bytes": True, "max_stderr_bytes": True}, "d-lim-bools")
        self.refused_before_launch({"timeout_s": 5, "max_stdout_bytes": 1000}, "d-lim-missing")
        self.assertEqual(self.launches(), [])

    def test_valid_boundary_values(self):
        r = self.ad.deliver(self.env(delivery="d-top", limits={"timeout_s": MAX_TIMEOUT_S, "max_stdout_bytes": MAX_CAPTURE_BYTES,
                                                                "max_stderr_bytes": MAX_CAPTURE_BYTES}))
        self.assertEqual((r["transport"], r["collection"]), ("delivered", "collected"))
        r = self.ad.deliver(self.env(delivery="d-float", limits={"timeout_s": 7.5, "max_stdout_bytes": 100000, "max_stderr_bytes": 1}))
        self.assertEqual(r["transport"], "delivered")
        r = self.ad.deliver(self.env(delivery="d-one", limits={"timeout_s": 20, "max_stdout_bytes": 1, "max_stderr_bytes": 1}))
        self.assertEqual(r["transport"], "output-limit", "a 1-byte cap is valid; the result simply does not fit")

    def test_strict_json_in_messages(self):
        for text in ('{"a": NaN}', '{"a": Infinity}', '{"a": -Infinity}', '{"a": 1, "a": 2}'):
            with self.subTest(text=text):
                with self.assertRaises(StrictJSONError):
                    strict_loads(text)
        with self.assertRaises(ValueError):
            canonical({"timeout_s": math.inf})
        req = self.base / "nan-request.json"
        req.write_bytes(canonical(self.env())[:-1].replace(b'"timeout_s":20', b'"timeout_s":NaN') + b"}")
        r = self.cli("deliver", "--store", str(self.store), "--request", str(req))
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("non-standard JSON number NaN", r.stdout)
        dup = self.base / "dup-request.json"
        dup.write_bytes(canonical(self.env())[:-1] + b',"backend":"fixture-crash"}')
        r = self.cli("deliver", "--store", str(self.store), "--request", str(dup))
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("duplicate key 'backend'", r.stdout)
        self.assertEqual(self.launches(), [])
        rec = self.ad.deliver(self.env("fixture-dup-keys", delivery="d-dup"))
        self.assertEqual(rec["transport"], "malformed")
        self.assertIn("duplicate key 'outcome'", rec["reason"])


if __name__ == "__main__":
    unittest.main()
