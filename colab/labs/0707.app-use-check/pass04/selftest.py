#!/usr/bin/env python3
"""Harness self-tests (STUBS and fixture builders only; no loop, cycle, constructor or app runs).

usage: selftest.py   writes evidence/lab05.04/selftest/<UTC>-<hex>/ and exits nonzero on any failure.
"""

from __future__ import annotations

import datetime
import io
import json
import os
import secrets
import shutil
import sys
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import fixtures as F  # noqa: E402
import harness as H  # noqa: E402
import stub_cases  # noqa: E402

STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + secrets.token_hex(3)
OUT = H.LIVE_BOOK / "0707.app-use-check" / "evidence" / "lab05.04" / "selftest" / STAMP
SCRATCH = Path(r"C:\Users\misg\AppData\Local\Temp\claude\D--Git-Librarian\313e7ce7-27d2-405b-881d-6a16a47199dc\scratchpad\lab0504-selftest") / STAMP
STUB = HERE / "stubs" / "STUB_loop.py"
REAL_CONFIG = HERE / "candidate.config.json"


def stub_config(**over) -> tuple[dict, bytes]:
    data = STUB.read_bytes()
    cfg = json.loads(REAL_CONFIG.read_text(encoding="utf-8"))
    cfg.update(kind="stub", label="STUB self-test config; not a candidate",
               candidate={"path": str(STUB), "sha256": H.sha(data), "bytes": len(data)},
               output_root=str(SCRATCH), timeout_seconds=3)
    cfg.update(over)
    raw = json.dumps(cfg, indent=2, sort_keys=True).encode("utf-8")
    return cfg, raw


def pid_alive(pid: int) -> bool:
    if os.name == "nt":
        import subprocess
        r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, timeout=30)
        return str(pid) in r.stdout.decode("utf-8", "replace")
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


class Preflight(unittest.TestCase):
    def setUp(self):
        self.launched = []
        H.LAUNCH_HOOK = self.launched.append

    def tearDown(self):
        H.LAUNCH_HOOK = None

    def test_unknown_candidate_is_unready_and_unread(self):
        cfg = json.loads(REAL_CONFIG.read_text(encoding="utf-8"))
        cfg["output_root"] = str(SCRATCH)
        cfg["candidate"]["path"] = "labs/THIS-PATH-DOES-NOT-EXIST/never-read.py"
        pre = H.preflight(cfg, "real")
        self.assertEqual(pre["status"], "UNREADY")
        self.assertIn("identity unknown", pre["reasons"][0])

    def test_real_matrix_with_null_candidate_runs_nothing(self):
        cfg = json.loads(REAL_CONFIG.read_text(encoding="utf-8"))
        cfg["output_root"] = str(SCRATCH)
        raw = json.dumps(cfg).encode()
        code, summary = H.run_matrix(cfg, raw, "real", OUT / "runs")
        self.assertEqual((code, summary["aggregate"]), (2, "UNREADY"))
        self.assertEqual(self.launched, [])
        self.assertTrue(all(r["status"] == "NOT RUN" for r in summary["cases"]))
        self.assertFalse(summary["loop_evidence"])

    def test_candidate_pin_mismatch_refused(self):
        cfg, _ = stub_config()
        cfg["candidate"]["sha256"] = "0" * 64
        self.assertEqual(H.preflight(cfg, "stub")["status"], "REFUSED")

    def test_dependency_pin_mismatch_refused(self):
        cfg, _ = stub_config()
        cfg["dependencies"] = [dict(cfg["dependencies"][0], sha256="0" * 64)]
        pre = H.preflight(cfg, "stub")
        self.assertEqual(pre["status"], "REFUSED")
        self.assertIn("dependency 0", pre["reasons"][0])

    def test_interpreter_version_mismatch_refused(self):
        cfg, _ = stub_config(interpreter={"path": sys.executable, "version": "0.0.0"})
        self.assertEqual(H.preflight(cfg, "stub")["status"], "REFUSED")

    def test_output_root_inside_checkout_refused(self):
        cfg, _ = stub_config(output_root=str(HERE))
        self.assertEqual(H.preflight(cfg, "stub")["status"], "REFUSED")

    def test_stub_kind_cannot_run_real_matrix(self):
        cfg, raw = stub_config()
        code, summary = H.run_matrix(cfg, raw, "real", OUT / "runs")
        self.assertEqual((code, summary["aggregate"]), (2, "REFUSED"))
        self.assertEqual(self.launched, [])


class StubRuns(unittest.TestCase):
    def test_stub_pass_is_never_loop_evidence(self):
        cfg, raw = stub_config()
        stub_cases.CASES = stub_cases.SETS["pass"]
        code, summary = H.run_matrix(cfg, raw, "stub", OUT / "runs")
        self.assertEqual((code, summary["aggregate"]), (0, "PASS"))
        self.assertFalse(summary["loop_evidence"])
        self.assertEqual(summary["kind"], "stub")

    def test_mixed_failures_aggregate_and_timeout_kills_only_its_tree(self):
        cfg, raw = stub_config()
        stub_cases.CASES = stub_cases.SETS["mixed"]
        code, summary = H.run_matrix(cfg, raw, "stub", OUT / "runs")
        status = {r["id"]: r["status"] for r in summary["cases"]}
        self.assertEqual(status, {"S01": "PASS", "S02": "FAIL", "S03": "ERROR", "S04": "FAIL"})
        self.assertEqual((code, summary["aggregate"]), (1, "FAIL"))
        run = OUT / "runs" / summary["run"]
        crash = run / "cases" / "S04" / "calls" / "01-stub-crash.stderr"
        self.assertIn(b"Traceback", crash.read_bytes())
        sleep_row = json.loads((run / "cases" / "S03" / "calls" / "01-stub-sleep.json").read_text())
        self.assertTrue(sleep_row["timed_out"])
        self.assertIsNotNone(sleep_row["killed"])
        pid = int((SCRATCH / summary["run"] / "STUB-grandchild.pid").read_text())
        self.assertFalse(pid_alive(pid), "grandchild of the launched stub survived")
        self.assertTrue(pid_alive(os.getpid()))

    def test_unique_runs_preserve_earlier_evidence(self):
        cfg, raw = stub_config()
        stub_cases.CASES = stub_cases.SETS["pass"]
        _, first = H.run_matrix(cfg, raw, "stub", OUT / "runs")
        first_dir = OUT / "runs" / first["run"]
        before = F.tree(first_dir)
        _, second = H.run_matrix(cfg, raw, "stub", OUT / "runs")
        self.assertNotEqual(first["run"], second["run"])
        self.assertEqual(F.tree(first_dir), before)


class CaseCodeSmoke(unittest.TestCase):
    """Run every REAL case function against a canned STUB result (no launch). Not loop evidence:
    it only shows the case code itself has no Python errors before activation."""

    def test_real_cases_have_no_code_errors(self):
        import cases
        cfg, raw = stub_config()
        run = H.Run(cfg, raw, "case-code-smoke", OUT / "case-code-smoke")
        canned = {"exit": 0, "json": {"stub": True}, "stderr": "", "timed_out": False, "killed": None}
        run.call = lambda case_dir, label, argv: dict(canned, label=label, argv=argv)
        bugs, outcomes = [], {}
        for case in cases.CASES:
            if not case["fn"]:
                outcomes[case["id"]] = "MANUAL"
                continue
            ctx = H.Ctx(run, case["id"])
            try:
                case["fn"](ctx)
                outcomes[case["id"]] = "checks-recorded" if ctx.checks else "no-checks"
            except F.FixtureError as exc:
                outcomes[case["id"]] = f"fixture-stop: {exc}"
            except Exception as exc:  # noqa: BLE001
                bugs.append(f"{case['id']}: {type(exc).__name__}: {exc}")
        (run.dir / "outcomes.json").write_text(json.dumps({"bugs": bugs, "outcomes": outcomes}, indent=2) + "\n")
        self.assertEqual(bugs, [])
        self.assertNotIn("no-checks", outcomes.values())


class Fixtures(unittest.TestCase):
    def test_books(self):
        for kind in ("pending", "pending-crlf", "substantive", "no-heading", "duplicate-heading", "absent", "legacy-v1-recorded"):
            root = SCRATCH / "books" / kind
            F.build_book(root, kind)
            if kind == "absent":
                self.assertFalse((root / F.TARGET).exists())
            elif kind != "legacy-v1-recorded":
                self.assertEqual((root / F.TARGET).read_bytes(), F.page_bytes(kind))
        crlf = (SCRATCH / "books" / "pending-crlf" / F.TARGET).read_bytes()
        self.assertEqual(crlf.count(b"\n"), crlf.count(b"\r\n"))
        self.assertTrue((SCRATCH / "books" / "legacy-v1-recorded" / "cycle").is_dir())

    def test_decide_recipe_reproduces_recorded_0501_decision(self):
        src = F.OLD / "runs" / "run1" / "books" / "A.after-prepare"
        tree = json.loads(F.old_artifact("books/A.after-prepare.tree.json").read_text(encoding="utf-8"))
        root = SCRATCH / "decide-check"
        shutil.copytree(src, root)
        self.assertEqual(F.tree(root), tree)
        template = json.loads(F.old_artifact("A-prepare-template.json").read_text(encoding="utf-8"))
        decision = F.write_decision(root, template)
        self.assertEqual(decision, F.old_artifact("A-decision.json").read_bytes())

    def test_existing_book_is_refused(self):
        root = SCRATCH / "books" / "twice"
        F.build_book(root, "pending")
        with self.assertRaises(FileExistsError):
            F.build_book(root, "pending")


def main() -> int:
    OUT.mkdir(parents=True)
    SCRATCH.mkdir(parents=True)
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    (OUT / "selftest.log").write_text(stream.getvalue(), encoding="utf-8")
    summary = {"schema": "harness-selftest/1", "run": STAMP, "interpreter": sys.executable, "version": sys.version,
               "tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
               "skipped": len(result.skipped), "ok": result.wasSuccessful(),
               "statement": "STUB and fixture-builder tests only; not loop evidence"}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(STAMP, "ok" if result.wasSuccessful() else "FAILED", result.testsRun, "tests")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
