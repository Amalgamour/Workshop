#!/usr/bin/env python3
"""pass05 harness self-tests: STUBS, static junctions in NEW scratch, config fuzz, preservation.

No loop, cycle, constructor, app or real candidate runs. Junctions are created only
under this run's scratch directory, never written through, and removed (the link
only) at the end of each test.
usage: selftest5.py   -> evidence/lab05.05/selftest/<UTC>-<hex>/ ; exit nonzero on any failure
"""

from __future__ import annotations

import datetime
import hashlib
import io
import json
import os
import secrets
import subprocess
import sys
import unittest
from copy import deepcopy
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import guards as G  # noqa: E402
import harness5 as H  # noqa: E402
import stub_cases5  # noqa: E402

STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + secrets.token_hex(3)
OUT = G.EVIDENCE_PARENT / "lab05.05" / "selftest" / STAMP
RUNS = OUT / "runs"
SCRATCH = Path(r"C:\Users\misg\AppData\Local\Temp\claude\D--Git-Librarian\313e7ce7-27d2-405b-881d-6a16a47199dc\scratchpad\lab0505-selftest") / STAMP
STUB = HERE / "stubs" / "STUB5.py"
REAL = HERE / "candidate.config.json"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def write_cfg(name: str, cfg) -> str:
    p = SCRATCH / "configs" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(json.dumps(cfg, indent=2).encode("utf-8") if not isinstance(cfg, bytes) else cfg)
    return str(p)


def real_cfg() -> dict:
    cfg = json.loads(REAL.read_text(encoding="utf-8"))
    cfg["output_root"] = str(SCRATCH / "out")
    return cfg


def stub_cfg(timeout=3) -> dict:
    data = STUB.read_bytes()
    cfg = real_cfg()
    cfg.update(kind="stub", label="STUB self-test config; not a candidate", dependencies=[],
               candidate={"path": str(STUB), "sha256": sha(data), "bytes": len(data)}, timeout_seconds=timeout)
    return cfg


def alive(pid: int) -> bool:
    r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, timeout=30)
    return str(pid) in r.stdout.decode("utf-8", "replace")


def run(cfg, matrix="stub", name="cfg.json", evidence=None):
    path = write_cfg(name, cfg)
    return H.run_matrix(path, matrix, str(evidence or RUNS))


def call_rows(summary) -> list[dict]:
    rd = Path(summary["canonical_paths"]["run_dir"])
    return [json.loads(p.read_text()) for p in sorted(rd.glob("cases/*/calls/*.json"))]


def call_bytes(summary, ext) -> bytes:
    rd = Path(summary["canonical_paths"]["run_dir"])
    return b"".join(p.read_bytes() for p in sorted(rd.glob(f"cases/*/calls/*.{ext}")))


class Base(unittest.TestCase):
    def setUp(self):
        self.launched = []
        H.LAUNCH_HOOK = self.launched.append

    def tearDown(self):
        H.LAUNCH_HOOK = None


class H01Timeouts(Base):
    def stub(self, mode, timeout=3):
        stub_cases5.CASES = stub_cases5.SETS[mode]
        return run(stub_cfg(timeout), name=f"{mode}.json")

    def test_ok_has_no_anomaly(self):
        code, s = self.stub("ok")
        self.assertEqual((code, s["aggregate"], s["loop_evidence"]), (0, "PASS", False))
        row = call_rows(s)[0]
        self.assertEqual((row["output_status"], row["timed_out"], row["leftover_descendants"]), ("complete", False, None))
        self.assertEqual(row["containment"]["method"], "job")

    def test_flush_then_timeout_keeps_both_streams_once(self):
        code, s = self.stub("flush-sleep")
        row = call_rows(s)[0]
        self.assertTrue(row["timed_out"])
        self.assertEqual(row["timeout_reason"], "parent still running")
        self.assertEqual(row["output_status"], "complete-after-termination")
        self.assertEqual(call_bytes(s, "stdout").count(b"STDOUT-MARK"), 1)
        self.assertEqual(call_bytes(s, "stderr").count(b"STDERR-MARK"), 1)
        self.assertIsNone(row["exit"])
        self.assertEqual(s["cases"][0]["status"], "ERROR")
        self.assertEqual((code, s["aggregate"]), (1, "FAIL"))

    def test_timeout_with_pipe_holding_child_kills_it_and_keeps_output(self):
        code, s = self.stub("flush-sleep-child")
        row = call_rows(s)[0]
        pid = int((Path(s["canonical_paths"]["fixture_root"]) / "S05-grandchild.pid").read_text())
        self.assertFalse(alive(pid))
        self.assertIn(b"STDOUT-MARK", call_bytes(s, "stdout"))
        self.assertEqual(row["output_status"], "complete-after-termination")

    def test_exit_with_pipe_holding_child(self):
        code, s = self.stub("exit-hold-child")
        row = call_rows(s)[0]
        self.assertEqual(row["parent_exit"], 0)
        self.assertEqual(row["timeout_reason"], "pipes held by a descendant after the parent exited")
        self.assertIn(b'"stub": true', call_bytes(s, "stdout"))
        pid = int((Path(s["canonical_paths"]["fixture_root"]) / "S07-grandchild.pid").read_text())
        self.assertFalse(alive(pid))
        self.assertEqual(s["cases"][0]["status"], "ERROR")

    def test_exit_leaving_detached_child_is_detected_and_cleaned(self):
        code, s = self.stub("exit-leave-child")
        row = call_rows(s)[0]
        self.assertFalse(row["timed_out"])
        self.assertGreaterEqual(row["leftover_descendants"], 1)
        self.assertTrue(row["termination"]["ok"])
        pid = int((Path(s["canonical_paths"]["fixture_root"]) / "S06-grandchild.pid").read_text())
        self.assertFalse(alive(pid))
        self.assertEqual(s["cases"][0]["status"], "ERROR")

    def test_crash_leaving_child_keeps_traceback(self):
        code, s = self.stub("crash-leave-child")
        row = call_rows(s)[0]
        self.assertEqual(row["exit"], 1)
        self.assertIn(b"Traceback", call_bytes(s, "stderr"))
        self.assertGreaterEqual(row["leftover_descendants"], 1)

    def test_unrelated_process_untouched(self):
        other = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
        try:
            self.stub("flush-sleep-child")
            self.assertTrue(alive(other.pid), "an unrelated process was killed")
            self.assertTrue(alive(os.getpid()))
        finally:
            other.kill()


class H02Boundaries(Base):
    def junction(self, name, target: Path) -> Path:
        link = SCRATCH / "junctions" / name
        link.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True, timeout=30)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.addCleanup(os.rmdir, link)  # removes the junction itself, not its target
        return link

    def test_junction_to_checkout_refused_as_output_root(self):
        link = self.junction("checkout-alias", G.CHECKOUT)
        stub_cases5.CASES = stub_cases5.SETS["ok"]
        cfg = stub_cfg()
        cfg["output_root"] = str(link)
        code, s = run(cfg, name="junction.json")
        self.assertEqual((code, s["aggregate"]), (2, "REFUSED"))
        self.assertIn("reparse", s["preflight"]["reasons"][0])
        self.assertEqual(self.launched, [])

    def test_existing_subdir_through_junction_refused(self):
        link = self.junction("checkout-alias-2", G.CHECKOUT)
        cfg = stub_cfg()
        cfg["output_root"] = str(link / "labs")
        code, s = run(cfg, name="junction-sub.json")
        self.assertEqual(s["aggregate"], "REFUSED")
        self.assertEqual(self.launched, [])

    def test_lexical_checkout_refused(self):
        cfg = stub_cfg()
        cfg["output_root"] = str(HERE)
        code, s = run(cfg, name="lexical.json")
        self.assertIn("protected", s["preflight"]["reasons"][0])

    def test_fixture_write_entry_rechecks(self):
        _, F, _ = H.load_pass04()
        good = SCRATCH / "fx-root"
        good.mkdir(parents=True)
        H.ACTIVE_FIXTURES = G.canonical(good)
        try:
            with self.assertRaises(H.Refused) as c1:
                F.build_book(SCRATCH / "elsewhere" / "book", "pending")
            self.assertEqual(c1.exception.code, "boundary")
            link = self.junction("fx-alias", G.CHECKOUT)
            with self.assertRaises(H.Refused) as c2:
                F.build_book(link / "labs" / "book", "pending")
            self.assertEqual(c2.exception.code, "reparse")
            F.build_book(good / "book", "pending")
            with self.assertRaises(H.Refused) as c3:
                F.build_book(good / "book", "pending")
            self.assertEqual(c3.exception.code, "occupied")
        finally:
            H.ACTIVE_FIXTURES = None
        H.ACTIVE_FIXTURES = None
        with self.assertRaises(H.Refused):
            F.build_book(good / "book2", "pending")
        self.assertFalse((G.CHECKOUT / "labs" / "book").exists())

    def test_evidence_roots(self):
        for bad in ("", "relative/path", str(SCRATCH / "ev"), str(G.EVIDENCE_PARENT / "lab05.04" / "x"),
                    str(G.EVIDENCE_PARENT), str(G.LIVE_BOOK / "0707.app-use-check")):
            with self.assertRaises(G.Boundary, msg=bad):
                G.evidence_root(bad)
        link = self.junction("evidence-alias", G.EVIDENCE_PARENT)
        with self.assertRaises(G.Boundary) as c:
            G.evidence_root(str(link / "lab05.05" / "x"))
        self.assertEqual(c.exception.code, "reparse")
        code, s = H.run_matrix(write_cfg("ev.json", stub_cfg()), "stub", str(SCRATCH / "ev"))
        self.assertEqual((code, s["aggregate"], s["run"]), (2, "REFUSED", None))

    def test_occupied_directory_refused(self):
        d = RUNS / "occupied-check"
        d.mkdir(parents=True)
        with self.assertRaises(G.Boundary) as c:
            G.fresh_dir(d, RUNS)
        self.assertEqual(c.exception.code, "occupied")


class H03Config(Base):
    def expect_refused(self, cfg_or_bytes, name):
        code, s = H.run_matrix(write_cfg(name, cfg_or_bytes), "real", str(RUNS))
        self.assertEqual((code, s["aggregate"]), (2, "REFUSED"), (name, s["preflight"]))
        self.assertEqual(s["launches"], 0)
        self.assertIsNone(s["canonical_paths"]["fixture_root"])
        self.assertTrue(all(r["status"] == "NOT RUN" for r in s["cases"]))
        return s

    def test_dependencies_null_is_refused_not_unready(self):
        cfg = real_cfg()
        cfg["dependencies"] = None
        s = self.expect_refused(cfg, "deps-null.json")
        self.assertIn("dependencies must be a list", s["preflight"]["reasons"][0])

    def test_substitution_fuzz(self):
        paths = ["kind", "label", "candidate", "candidate.path", "candidate.sha256", "candidate.bytes", "dependencies",
                 "dependencies.0", "dependencies.0.sha256", "dependencies.0.bytes", "interpreter", "interpreter.path",
                 "interpreter.version", "output_root", "timeout_seconds", "field_map", "release", "release.invocation", "release.note", "schema"]
        accepted = []
        for path in paths:
            for bad in (None, [], {}, "x", 0, 601, True, 5.5, ["x"]):
                cfg = real_cfg()
                parts = path.split(".")
                cur = cfg
                for p in parts[:-1]:
                    cur = cur[int(p)] if p.isdigit() else cur[p]
                last = parts[-1]
                cur[int(last) if last.isdigit() else last] = deepcopy(bad)
                code, s = H.run_matrix(write_cfg(f"fuzz-{path}-{type(bad).__name__}-{bad!r}.json".replace("/", "_")[:120], cfg), "real", str(RUNS))
                self.assertEqual(s["launches"], 0)
                self.assertIn(s["aggregate"], ("REFUSED", "UNREADY"))
                if s["aggregate"] == "UNREADY":
                    accepted.append((path, json.dumps(bad)))
        (OUT / "fuzz-accepted.json").write_text(json.dumps(accepted, indent=2) + "\n")
        # Shape-valid substitutions. Each still stops at UNREADY because the candidate identity is unknown:
        #  - text fields with text; field_map empty; release.invocation null (its base value) or text;
        #  - candidate sha256/bytes null (the base's own unknown identity);
        #  - dependency bytes 0 or 601: well-formed integers, compared with the file only once identity is known.
        allowed = {("label", '"x"'), ("release.invocation", "null"), ("release.invocation", '"x"'), ("release.note", '"x"'),
                   ("field_map", "{}"), ("candidate.path", '"x"'), ("candidate.sha256", "null"), ("candidate.bytes", "null"),
                   ("interpreter.path", '"x"'), ("interpreter.version", '"x"'),
                   ("dependencies.0.bytes", "0"), ("dependencies.0.bytes", "601")}
        unexpected = [a for a in accepted if a not in allowed]
        self.assertEqual(unexpected, [], "shape-invalid values reached UNREADY")

    def test_malformed_bytes(self):
        base = json.dumps(real_cfg()).encode()
        for name, raw in (("bom", b"\xef\xbb\xbf" + base), ("latin1", base.replace(b"Grok", b"Gr\xf6k")), ("notjson", b"{not json"),
                          ("dupkey", base.replace(b'"kind"', b'"kind": "candidate", "kind"', 1)), ("nan", base.replace(b'"timeout_seconds": 180', b'"timeout_seconds": NaN')),
                          ("list", b"[]"), ("empty", b""), ("big", b" " * (2 << 20))):
            s = self.expect_refused(raw, f"bytes-{name}.json")
            self.assertTrue(s["preflight"]["reasons"][0].startswith(("config-", "config")), s["preflight"])
        code, s = H.run_matrix(str(SCRATCH / "configs" / "missing.json"), "real", str(RUNS))
        self.assertEqual(s["aggregate"], "REFUSED")
        self.assertIn("config-missing", s["preflight"]["reasons"][0])


class Preservation(Base):
    def test_real_matrix_unready_no_launch_and_cases_unchanged(self):
        cfg = real_cfg()
        cfg["candidate"]["path"] = "labs/THIS-PATH-DOES-NOT-EXIST/never-read.py"
        code, s = H.run_matrix(write_cfg("real-null.json", cfg), "real", str(RUNS))
        self.assertEqual((code, s["aggregate"], s["launches"], s["loop_evidence"]), (2, "UNREADY", 0, False))
        self.assertIn("identity unknown", s["preflight"]["reasons"][0])
        cases, _F, prov = H.load_pass04()
        self.assertEqual([r["id"] for r in s["cases"]], [c["id"] for c in cases.CASES])
        self.assertEqual(len(prov), 2)
        a24 = [c for c in cases.CASES if c["id"] == "A24"][0]
        self.assertTrue(a24.get("manual"))

    def test_kind_matrix_separation(self):
        code, s = run(stub_cfg(), matrix="real", name="stub-on-real.json")
        self.assertEqual((s["aggregate"], s["launches"]), ("REFUSED", 0))
        cfg = real_cfg()
        code, s = run(cfg, matrix="stub", name="cand-on-stub.json")
        self.assertEqual((s["aggregate"], s["launches"]), ("REFUSED", 0))

    def test_unique_runs_preserve_earlier(self):
        stub_cases5.CASES = stub_cases5.SETS["ok"]
        _, first = run(stub_cfg(), name="u1.json")
        rd = Path(first["canonical_paths"]["run_dir"])
        before = {p.relative_to(rd).as_posix(): sha(p.read_bytes()) for p in rd.rglob("*") if p.is_file()}
        _, second = run(stub_cfg(), name="u2.json")
        self.assertNotEqual(first["run"], second["run"])
        after = {p.relative_to(rd).as_posix(): sha(p.read_bytes()) for p in rd.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_pass04_files_unchanged(self):
        pins = {r["path"]: r for r in json.loads(H.PACK.read_text(encoding="utf-8"))["files"]}
        for rel, row in pins.items():
            if rel.startswith("colab/labs/0707.app-use-check/pass04/"):
                self.assertEqual(sha((G.CHECKOUT / rel).read_bytes()), row["sha256"], rel)


def main() -> int:
    OUT.mkdir(parents=True)
    SCRATCH.mkdir(parents=True)
    (SCRATCH / "out").mkdir()
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    (OUT / "selftest.log").write_text(stream.getvalue(), encoding="utf-8")
    summary = {"schema": "harness-selftest/2", "run": STAMP, "interpreter": sys.executable, "version": sys.version,
               "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
               "ok": result.wasSuccessful(), "statement": "STUB, junction-boundary and config tests only; not loop evidence"}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(STAMP, "ok" if result.wasSuccessful() else "FAILED", result.testsRun, "tests")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
