#!/usr/bin/env python3
"""Execution-proof v2 equipment tests (0707/05.25). EQUIPMENT ONLY.
SCRIPTED DUMMY ENTRIES: each dummy is a tiny labelled script that prints fixed output. They test the proof classes;
they are never a candidate app. Rooms are explicit dirs under D:/librarian/temp/fbt3-0525/unit-*.
P01 reproduces Prime's checked-only false positive against the FROZEN pass02 proof (executed=true) and shows v2 says
verified-pin-check. usage: python -B test_proof.py (exit 0 only if all pass and the count matches)"""

import copy
import hashlib
import json
import os
import subprocess
import sys
import unittest
import uuid
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import identity3 as I  # noqa: E402
import run as A  # noqa: E402

EXPECTED_TESTS = 14
TMP = Path(r"D:\librarian\temp\fbt3-0525")
TARGET = "labs/wb/workbook.py"
HEAD = '#!/usr/bin/env python3\n"""SCRIPTED DUMMY ENTRY (0707/05.25 proof unit test). Not an app."""\nimport hashlib, importlib.util, json, os, subprocess, sys, time\nfrom pathlib import Path\nR = Path(__file__).resolve().parents[1]\nT = R / "labs/wb/workbook.py"\n'
BODIES = {
    "genuine": 'spec = importlib.util.spec_from_file_location("w", T); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\nprint(json.dumps({"wb": m.NAME}))\n',
    "subprocess": 'p = subprocess.run([sys.executable, "-B", str(T)], capture_output=True, text=True)\nprint(json.dumps({"child": p.stdout.strip(), "exit": p.returncode}))\nsys.exit(p.returncode)\n',
    "checked-only": 'want = "{digest}"\nif hashlib.sha256(T.read_bytes()).hexdigest() != want:\n    print("refused pin mismatch: labs/wb/workbook.py", file=sys.stderr); sys.exit(2)\nprint(json.dumps({"ok": True}))\n',
    "decoy": 'spec = importlib.util.spec_from_file_location("w", R / "labs/real/workbook.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\nprint(json.dumps({"wb": m.NAME}))\n',
    "nondeterministic": 'print(json.dumps({"t": time.time_ns()}))\n',
    "unattributed": 'print(json.dumps({"size": os.stat(T).st_size}))\n',
    "contradictory": 'subprocess.run([sys.executable, "-B", str(T)], capture_output=True)\nprint(json.dumps({"ok": True}))\n',
}
WB = 'NAME = "declared"  # SCRIPTED DUMMY workbook\nprint("workbook ran") if __name__ == "__main__" else None\n'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def dummy(kind):
    root = TMP / f"unit-{kind}-{uuid.uuid4().hex[:8]}"
    (root / "app").mkdir(parents=True)
    (root / "labs/wb").mkdir(parents=True)
    (root / "labs/real").mkdir(parents=True)
    (root / TARGET).write_bytes(WB.encode())
    (root / "labs/real/workbook.py").write_bytes(b'NAME = "real"\n')
    body = BODIES[kind].replace("{digest}", sha(WB.encode()))
    (root / "app/librarian.py").write_bytes((HEAD + body).encode())
    (root / "CANDIDATE.json").write_bytes(b'{"kind": "dummy", "note": "SCRIPTED DUMMY"}\n')
    files = [{"path": p, "sha256": sha((root / p).read_bytes()), "bytes": len((root / p).read_bytes()), "role": r}
             for p, r in (("app/librarian.py", "entry"), (TARGET, "workbook"), ("labs/real/workbook.py", "data"))]
    ident = {"mode": "explicit", "kind": "dummy", "entry": "app/librarian.py", "workbook_entry": TARGET, "open_entry": None,
             "reporter_entry": None, "files": files, "candidate_json_sha256": sha((root / "CANDIDATE.json").read_bytes())}
    return root, ident


def probe(root, env):
    return I.run([root / "app/librarian.py", "review-loop", "prepare"], root, env)


def probe_untraced(root, env):
    clean = {k: v for k, v in env.items() if not k.startswith("LAB_AUDIT")}
    return I.run([root / "app/librarian.py"], root, clean)


def proof(kind, p=probe):
    root, ident = dummy(kind)
    return I.execution_proof(root, ident, TARGET, p, TMP / f"unit-proof-{uuid.uuid4().hex[:8]}", "wb")


class Classes(unittest.TestCase):
    def test_p01_checked_only_false_positive_reproduced_then_fixed(self):
        root, ident = dummy("checked-only")
        old = I.I2.tamper_proof(root, ident, TARGET, lambda r: I.run([r / "app/librarian.py"], r, dict(os.environ)),
                                TMP / f"unit-old-{uuid.uuid4().hex[:8]}", "wb")
        self.assertTrue(old["executed"])                         # the frozen pass02 proof: false positive (06.24.review)
        self.assertIn("checked", old["evidence"])
        new = I.execution_proof(root, ident, TARGET, probe, TMP / f"unit-proof-{uuid.uuid4().hex[:8]}", "wb")
        self.assertEqual((new["class"], new["executed"]), ("verified-pin-check", False))

    def test_p02_genuine_import_executed(self):
        p = proof("genuine")
        self.assertEqual((p["class"], p["executed"]), ("executed", True))
        self.assertEqual(p["binding"][0]["event"], "exec")

    def test_p03_subprocess_run_executed(self):
        p = proof("subprocess")
        self.assertEqual(p["class"], "executed")
        self.assertEqual(p["binding"][0]["event"], "run_file")

    def test_p04_decoy(self):
        self.assertEqual(proof("decoy")["class"], "decoy")

    def test_p05_nondeterministic(self):
        self.assertEqual(proof("nondeterministic")["class"], "nondeterministic")

    def test_p06_unattributed_change(self):
        self.assertEqual(proof("unattributed")["class"], "unattributed-change")

    def test_p07_contradictory(self):
        self.assertEqual(proof("contradictory")["class"], "contradictory")

    def test_p08_no_audit_evidence_fails_closed(self):
        p = proof("genuine", probe_untraced)
        self.assertEqual((p["class"], p["executed"]), ("no-audit-evidence", False))

    def test_p09_only_executed_is_executed(self):
        for k in ("checked-only", "decoy", "nondeterministic", "unattributed", "contradictory"):
            self.assertFalse(proof(k)["executed"], k)

    def test_p10_target_must_be_declared(self):
        root, ident = dummy("genuine")
        with self.assertRaises(I.Refused):
            I.execution_proof(root, ident, "labs/undeclared.py", probe, TMP / f"unit-proof-{uuid.uuid4().hex[:8]}", "x")


class Gate(unittest.TestCase):
    def gate(self, kind):
        root, ident = dummy(kind)
        keep = A.probes
        A.probes = lambda R, ident: {"workbook": probe}
        try:
            return A.gate(ident, root, TMP / f"unit-gate-{uuid.uuid4().hex[:8]}")
        finally:
            A.probes = keep

    def test_p11_gate_passes_executed(self):
        self.assertTrue(self.gate("genuine")["workbook"]["executed"])

    def test_p12_gate_refuses_checked_only_by_name(self):
        with self.assertRaises(I.Refused) as cm:
            self.gate("checked-only")
        self.assertIn("verified-pin-check", str(cm.exception))

    def test_p13_gate_refuses_unattributed_and_decoy(self):
        for k in ("unattributed", "decoy"):
            with self.assertRaises(I.Refused):
                self.gate(k)


class Pins(unittest.TestCase):
    def test_p14_pinned_inputs_unchanged(self):
        rows = {r["path"]: r for r in json.loads(I.PACK25.read_bytes())["files"]}
        for rel, r in rows.items():
            if rel.startswith(("labs/freshness-boundary-tests-pass01/", "labs/freshness-boundary-tests-pass02/", "labs/loop-convergence-harness-pass0")):
                self.assertEqual(sha((I.LIVE / rel).read_bytes()), r["sha256"], rel)
        self.assertEqual((len(A.R1.CASES), sum(c["required"] for c in A.R1.CASES)), (34, 32))


if __name__ == "__main__":
    res = unittest.main(exit=False, verbosity=2).result
    print(f"ran {res.testsRun}, expected {EXPECTED_TESTS}")
    sys.exit(0 if res.wasSuccessful() and res.testsRun == EXPECTED_TESTS else 1)
