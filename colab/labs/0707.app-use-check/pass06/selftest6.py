#!/usr/bin/env python3
"""pass06 self-tests for H04, plus pass05's 20 self-tests rebound to pass06. NONPRODUCTION.

No loop, cycle, constructor, app or real candidate runs. pass05's selftest5 module is
imported (its main is never run) and its module globals are pointed at harness6,
guards6 and NEW lab05.07 evidence and scratch locations.
usage: selftest6.py   -> evidence/lab05.07/selftest/<UTC>-<hex>/ ; exit nonzero on any failure
"""

from __future__ import annotations

import datetime
import io
import json
import os
import secrets
import subprocess
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PASS05 = HERE.parent / "pass05"
sys.path.insert(0, str(HERE))
import guards6 as G  # noqa: E402
import harness6 as H  # noqa: E402
sys.path.insert(1, str(PASS05))
import selftest5 as S5  # noqa: E402  (pass05, unchanged; main never called)

STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + secrets.token_hex(3)
OUT = G.EVIDENCE_PARENT / "lab05.07" / "selftest" / STAMP
RUNS = OUT / "runs"
SCRATCH = Path(r"C:\Users\misg\AppData\Local\Temp\claude\D--Git-Librarian\313e7ce7-27d2-405b-881d-6a16a47199dc\scratchpad\lab0507-selftest") / STAMP
REAL = HERE / "candidate.config.json"
PY = sys.executable
CLI5 = str(PASS05 / "harness5.py")
CLI6 = str(HERE / "harness6.py")
RECORD: list[dict] = []


def cfg_real() -> dict:
    cfg = json.loads(REAL.read_text(encoding="utf-8"))
    cfg["output_root"] = str(SCRATCH / "out")
    return cfg


def cfg_stub() -> dict:
    cfg = cfg_real()
    data = (PASS05 / "stubs" / "STUB5.py").read_bytes()
    cfg.update(kind="stub", label="STUB self-test config; not a candidate", dependencies=[],
               candidate={"path": str(PASS05 / "stubs" / "STUB5.py"), "sha256": H.sha(data), "bytes": len(data)}, timeout_seconds=3)
    return cfg


def write_cfg(name: str, cfg) -> str:
    p = SCRATCH / "configs" / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(json.dumps(cfg, indent=2).encode("utf-8"))
    return str(p)


def cli(label: str, argv: list[str]) -> subprocess.CompletedProcess:
    p = subprocess.run(argv, capture_output=True, timeout=120, cwd=str(G.CHECKOUT))
    (OUT / "cli").mkdir(parents=True, exist_ok=True)
    (OUT / "cli" / f"{label}.stdout").write_bytes(p.stdout)
    (OUT / "cli" / f"{label}.stderr").write_bytes(p.stderr)
    RECORD.append({"label": label, "argv": argv, "exit": p.returncode,
                   "stdout_sha256": H.sha(p.stdout), "stderr_sha256": H.sha(p.stderr)})
    return p


def fixture_listing() -> list[str]:
    root = SCRATCH / "out"
    return sorted(str(p) for p in root.rglob("*")) if root.exists() else []


class H04Reproduce(unittest.TestCase):
    def test_pass05_cli_reproduces_traceback_then_pass06_refuses(self):
        cfg = cfg_real()
        cfg["output_root"] = "C:\\x\u0000y"
        path = write_cfg("nul-output-root.json", cfg)
        old = cli("pass05-preflight-nul-output-root", [PY, "-I", "-B", CLI5, "preflight", "--config", path])
        self.assertNotEqual(old.returncode, 0)
        self.assertIn(b"Traceback", old.stderr)
        self.assertIn(b"embedded null character", old.stderr)
        new = cli("pass06-preflight-nul-output-root", [PY, "-I", "-B", CLI6, "preflight", "--config", path])
        self.assertEqual(new.returncode, 2)
        self.assertNotIn(b"Traceback", new.stderr)
        self.assertIn(b"refused: config-path", new.stderr)
        before = fixture_listing()
        run = cli("pass06-run-nul-output-root", [PY, "-I", "-B", CLI6, "run", "--config", path, "--matrix", "real", "--evidence", str(RUNS)])
        self.assertEqual(run.returncode, 2)
        self.assertNotIn(b"Traceback", run.stderr)
        self.assertIn(b"REFUSED", run.stdout)
        self.assertEqual(fixture_listing(), before)


class H04CliNegatives(unittest.TestCase):
    """Real malformed inputs through the public CLI. Each must refuse with exit 2, no traceback, no launch."""

    def run_cfg(self, label, cfg, matrix="real"):
        path = write_cfg(f"{label}.json", cfg)
        before = fixture_listing()
        p = cli(label, [PY, "-I", "-B", CLI6, "run", "--config", path, "--matrix", matrix, "--evidence", str(RUNS)])
        self.assertEqual(p.returncode, 2, p.stdout + p.stderr)
        self.assertNotIn(b"Traceback", p.stderr)
        self.assertEqual(fixture_listing(), before)
        name = p.stdout.decode().split()[0]
        summary = json.loads((RUNS / name / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual((summary["aggregate"], summary["launches"]), ("REFUSED", 0))
        return summary["preflight"]["reasons"][0]

    def test_output_root_invalid_windows_name(self):
        cfg = cfg_real()
        cfg["output_root"] = "C:\\bad<>|name"
        self.assertTrue(self.run_cfg("output-invalid-name", cfg).startswith("path-os"))

    def test_output_root_overlong(self):
        cfg = cfg_real()
        cfg["output_root"] = "C:\\" + "a" * 40000
        self.assertTrue(self.run_cfg("output-overlong", cfg).startswith("config-path"))

    def test_candidate_path_nul_unknown_identity(self):
        cfg = cfg_real()
        cfg["candidate"]["path"] = "labs/x\u0000y.py"
        self.assertTrue(self.run_cfg("candidate-nul-unknown", cfg).startswith("config-path"))

    def test_candidate_path_nul_known_identity(self):
        cfg = cfg_stub()
        cfg["candidate"]["path"] = "C:\\x\u0000y.py"
        self.assertTrue(self.run_cfg("candidate-nul-known", cfg, matrix="stub").startswith("config-path"))

    def test_dependency_invalid_name_with_known_stub(self):
        cfg = cfg_stub()
        cfg["dependencies"] = [{"path": "labs\\bad<>|.py", "sha256": "0" * 64, "bytes": 1}]
        self.assertTrue(self.run_cfg("dependency-invalid-name", cfg, matrix="stub").startswith("pin"))

    def test_interpreter_nul(self):
        cfg = cfg_stub()
        cfg["interpreter"]["path"] = "C:\\py\u0000.exe"
        self.assertTrue(self.run_cfg("interpreter-nul", cfg, matrix="stub").startswith("config-path"))

    def test_interpreter_not_executable(self):
        fake = SCRATCH / "not-an-interpreter.exe"
        fake.write_bytes(b"this is not a program\n")
        cfg = cfg_stub()
        cfg["interpreter"]["path"] = str(fake)
        self.assertTrue(self.run_cfg("interpreter-not-executable", cfg, matrix="stub").startswith("interpreter"))

    def test_config_path_invalid_name(self):
        p = cli("config-invalid-name", [PY, "-I", "-B", CLI6, "run", "--config", "C:\\bad<>|.json", "--matrix", "real", "--evidence", str(RUNS)])
        self.assertEqual(p.returncode, 2)
        self.assertNotIn(b"Traceback", p.stderr)
        self.assertIn(b"REFUSED", p.stdout)

    def test_evidence_invalid_name_writes_nothing(self):
        lab = G.EVIDENCE_PARENT / "lab05.07"
        before = sorted(x.name for x in lab.iterdir())
        p = cli("evidence-invalid-name", [PY, "-I", "-B", CLI6, "run", "--config", write_cfg("ev.json", cfg_real()),
                                          "--matrix", "real", "--evidence", str(lab / "bad<>|")])
        self.assertEqual(p.returncode, 2)
        self.assertNotIn(b"Traceback", p.stderr)
        self.assertIn(b"path-os", p.stdout)
        self.assertEqual(sorted(x.name for x in lab.iterdir()), before)

    def test_evidence_relative(self):
        p = cli("evidence-relative", [PY, "-I", "-B", CLI6, "run", "--config", write_cfg("ev2.json", cfg_real()),
                                      "--matrix", "real", "--evidence", "lab05.07"])
        self.assertEqual(p.returncode, 2)
        self.assertNotIn(b"Traceback", p.stderr)


class H04Direct(unittest.TestCase):
    """NUL cannot travel in Windows argv; these call the public functions directly."""

    def test_config_path_nul(self):
        with self.assertRaises(H.Refused) as c:
            H.read_config("C:\\a\u0000b.json")
        self.assertEqual(c.exception.code, "config-path")

    def test_run_matrix_config_nul_records_refusal(self):
        code, s = H.run_matrix("C:\\a\u0000b.json", "real", str(RUNS))
        self.assertEqual((code, s["aggregate"], s["launches"]), (2, "REFUSED", 0))
        self.assertIn("config-path", s["preflight"]["reasons"][0])

    def test_evidence_nul_writes_nothing(self):
        code, s = H.run_matrix(write_cfg("ev3.json", cfg_real()), "real", str(G.EVIDENCE_PARENT / "lab05.07" / "x\u0000y"))
        self.assertEqual((code, s["aggregate"], s["run"]), (2, "REFUSED", None))

    def test_guard_helpers(self):
        for fn in (G.output_root, G.evidence_root):
            with self.assertRaises(G.Boundary):
                fn("C:\\a\u0000b")
        with self.assertRaises(G.Boundary) as c:
            G.chain_without_links(Path("C:\\bad<>|name"))
        self.assertEqual(c.exception.code, "path-os")


class H04Mocked(unittest.TestCase):
    """MOCKED filesystem failure (not a real malformed path): lstat raises PermissionError for one directory."""

    def test_mocked_permission_error_is_refused(self):
        target = SCRATCH / "mocked-denied"
        target.mkdir()
        real = os.lstat

        def fake(p, *a, **k):
            if os.path.normcase(str(p)) == os.path.normcase(str(target)):
                raise PermissionError(13, "MOCKED access denied", str(p))
            return real(p, *a, **k)

        with mock.patch.object(G.os, "lstat", side_effect=fake):
            with self.assertRaises(G.Boundary) as c:
                G.output_root(str(target))
        self.assertEqual(c.exception.code, "path-os")
        self.assertIn("MOCKED", c.exception.detail)

    def test_programming_error_is_not_swallowed(self):
        with mock.patch.object(G, "canonical", side_effect=TypeError("planted bug")):
            with self.assertRaises(TypeError):
                H.run_matrix(write_cfg("bug.json", cfg_real()), "real", str(RUNS))


def rebind_pass05_suite() -> list[type]:
    """Point pass05's unchanged test module at pass06 and NEW locations, then return its test classes."""
    S5.H, S5.G = H, G
    S5.OUT = OUT / "pass05-suite"
    S5.RUNS = S5.OUT / "runs"
    S5.SCRATCH = SCRATCH / "pass05-suite"
    S5.REAL = REAL
    S5.OUT.mkdir(parents=True)
    (S5.SCRATCH / "out").mkdir(parents=True)
    return [S5.H01Timeouts, S5.H02Boundaries, S5.H03Config, S5.Preservation]


def main() -> int:
    OUT.mkdir(parents=True)
    (SCRATCH / "out").mkdir(parents=True)
    loader = unittest.defaultTestLoader
    suite = unittest.TestSuite()
    for cls in (H04Reproduce, H04CliNegatives, H04Direct, H04Mocked):
        suite.addTests(loader.loadTestsFromTestCase(cls))
    for cls in rebind_pass05_suite():
        suite.addTests(loader.loadTestsFromTestCase(cls))
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    (OUT / "selftest.log").write_text(stream.getvalue(), encoding="utf-8")
    (OUT / "cli-commands.json").write_text(json.dumps(RECORD, indent=2) + "\n", encoding="utf-8")
    summary = {"schema": "harness-selftest/3", "run": STAMP, "interpreter": sys.executable, "version": sys.version,
               "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors), "skipped": len(result.skipped),
               "ok": result.wasSuccessful(), "pass05_suite_rebound": True,
               "statement": "H04 path tests, MOCKED-labelled filesystem failure, and pass05's stub/boundary/config tests rebound to pass06; not loop evidence"}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(STAMP, "ok" if result.wasSuccessful() else "FAILED", result.testsRun, "tests")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
