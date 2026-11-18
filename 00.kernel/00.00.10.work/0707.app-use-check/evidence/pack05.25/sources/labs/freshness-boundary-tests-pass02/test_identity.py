#!/usr/bin/env python3
"""Adapter unit controls (0707/05.24). EQUIPMENT TESTS ONLY.
SCRIPTED DUMMY ENTRIES: the dummy candidates below are tiny labelled scripts that print fixed JSON. They test the
identity reader and the execution-proof gate; they are NEVER a repaired combined app and prove nothing about one.
Rooms are explicit directories under D:/librarian/temp/fbt2-0524/unit-* (no system temp cleanup).
usage: python -B test_identity.py (exit 0 only if all pass and the count matches)"""

import copy
import hashlib
import json
import sys
import unittest
import uuid
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import identity as I  # noqa: E402
import run as A  # noqa: E402   (loads the pinned pass01 runner)

EXPECTED_TESTS = 26
LIVE = I.LIVE
BASE = json.loads((LIVE / "labs/loop-convergence-harness-pass02/inputs/inputs-proto-l.json").read_text(encoding="utf-8"))
SHAPE = A.R1.load_inputs_check().shape_problems
TMP = Path(r"D:\librarian\temp\fbt2-0524")
BASELINES = {k: TMP / f"cand-{k}" for k in ("proto-l", "staged-g")}
OLD_COPY = Path(r"D:\librarian\temp\prime-night-0517-0723\combined-copy")
OLD_V2 = LIVE / "00.kernel/00.00.10.work/0522.review-construction/evidence/prime-review05.17/combined-measured-inputs.json"

DUMMY_ENTRY = '''#!/usr/bin/env python3
"""SCRIPTED DUMMY ENTRY (0707/05.24 adapter unit test). Not an app. Imports WB and prints fixed JSON."""
import importlib.util, json, sys
from pathlib import Path
WB = "{wb}"
spec = importlib.util.spec_from_file_location("dummy_wb", Path(__file__).resolve().parents[1] / WB)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
print(json.dumps({{"dummy": True, "command": sys.argv[1:3], "wb": mod.NAME}}))
'''
DUMMY_WB = 'NAME = "{name}"  # SCRIPTED DUMMY workbook\n'
DUMMY_OPEN = 'import sys\nprint("{{\\"dummy_open\\": true}}")\nsys.exit({code})\n'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def dummy(executes="labs/wb/workbook.py", declares="labs/wb/workbook.py", open_code=0, extra=()):
    """Build a scripted dummy root + harness-inputs/3 doc. 'executes' is what the dummy entry really imports."""
    root = TMP / f"unit-{uuid.uuid4().hex[:10]}"
    files = {"app/librarian.py": DUMMY_ENTRY.format(wb=executes), "labs/wb/workbook.py": DUMMY_WB.format(name="declared"),
             "labs/real/workbook.py": DUMMY_WB.format(name="real"), "labs/wb/open.py": DUMMY_OPEN.format(code=open_code)}
    for rel, txt in list(files.items()) + [(e, "# unused dependency\n") for e in extra]:
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_bytes(txt.encode())
    (root / "CANDIDATE.json").write_bytes(b'{"kind": "dummy", "note": "SCRIPTED DUMMY"}\n')
    role = {"app/librarian.py": "entry", declares: "workbook", "labs/wb/open.py": "open"}
    rows = []
    for rel in sorted(set(files) | set(extra)):
        b = (root / rel).read_bytes()
        rows.append({"path": rel, "sha256": sha(b), "bytes": len(b), "role": role.get(rel, "dependency" if rel in extra else "data")})
    doc = copy.deepcopy(BASE)
    doc["schema"] = "harness-inputs/3"
    doc["candidate"] = {"schema": "candidate-identity/1", "name": "dummy", "kind": "dummy", "entry": "app/librarian.py",
                        "workbook_entry": declares, "open_entry": "labs/wb/open.py", "reporter_entry": None,
                        "candidate_json_sha256": sha((root / "CANDIDATE.json").read_bytes()), "files": rows,
                        "lab_differences": [{"path": "*", "differs": "SCRIPTED DUMMY for adapter tests"}]}
    return root, doc


def probe_wb(root):
    return A.R1.run([root / "app/librarian.py", "review-loop", "prepare"], root)


def probe_open(root):
    return A.R1.run([root / "labs/wb/open.py", "open"], root)


class Explicit(unittest.TestCase):
    def res(self, doc, root):
        return I.resolve(doc, root, SHAPE)

    def refused(self, doc, root, needle):
        with self.assertRaises(I.Refused) as cm:
            self.res(doc, root)
        self.assertIn(needle, str(cm.exception))

    def test_u01_genuine_dummy_resolves_and_executes(self):
        root, doc = dummy()
        ident = self.res(doc, root)
        self.assertEqual((ident["mode"], ident["workbook_entry"]), ("explicit", "labs/wb/workbook.py"))
        p = I.tamper_proof(root, ident, ident["workbook_entry"], probe_wb, TMP / f"unit-proof-{uuid.uuid4().hex[:8]}", "wb")
        self.assertTrue(p["executed"])

    def test_u02_unused_workbook_is_decoy(self):
        root, doc = dummy(executes="labs/real/workbook.py", declares="labs/wb/workbook.py")
        ident = self.res(doc, root)
        p = I.tamper_proof(root, ident, ident["workbook_entry"], probe_wb, TMP / f"unit-proof-{uuid.uuid4().hex[:8]}", "wb")
        self.assertFalse(p["executed"])
        self.assertIn("DECOY", p["verdict"])

    def test_u03_gate_refuses_decoy(self):
        root, doc = dummy(executes="labs/real/workbook.py", declares="labs/wb/workbook.py")
        ident = self.res(doc, root)
        ident = dict(ident, entry="app/librarian.py")
        with self.assertRaises(I.Refused) as cm:
            A.gate(dict(ident), root, TMP / f"unit-gate-{uuid.uuid4().hex[:8]}")
        self.assertIn("DECOY", str(cm.exception))

    def test_u04_open_not_executable_refused(self):
        root, doc = dummy(open_code=2)
        ident = self.res(doc, root)
        p = I.tamper_proof(root, ident, "labs/wb/open.py", probe_open, TMP / f"unit-proof-{uuid.uuid4().hex[:8]}", "open")
        self.assertEqual(p["control"]["exit"], 2)

    def test_u05_unused_copied_dependency_flagged(self):
        root, doc = dummy(extra=("labs/copied/dep.py",))
        ident = self.res(doc, root)
        p = I.tamper_proof(root, ident, "labs/copied/dep.py", probe_wb, TMP / f"unit-proof-{uuid.uuid4().hex[:8]}", "dep")
        self.assertFalse(p["executed"])

    def test_u06_absent_entry(self):
        root, doc = dummy()
        doc["candidate"]["files"] = [f for f in doc["candidate"]["files"] if f["path"] != "app/librarian.py"]
        self.refused(doc, root, "candidate.entry 'app/librarian.py' is not a declared file")

    def test_u07_wrong_entry(self):
        root, doc = dummy()
        doc["candidate"]["entry"] = "app/other.py"
        self.refused(doc, root, "candidate.entry must be")

    def test_u08_workbook_not_declared(self):
        root, doc = dummy()
        doc["candidate"]["workbook_entry"] = "labs/nowhere/workbook.py"
        self.refused(doc, root, "is not a declared file")

    def test_u09_false_hash(self):
        root, doc = dummy()
        doc["candidate"]["files"][0]["sha256"] = "0" * 64
        self.refused(doc, root, "declared file differs")

    def test_u10_duplicate_path(self):
        root, doc = dummy()
        doc["candidate"]["files"].append(dict(doc["candidate"]["files"][0]))
        self.refused(doc, root, "duplicate path")

    def test_u11_external_paths(self):
        for bad in ("../x.py", "/abs.py", "C:/x.py", "labs\\x.py", "labs/./x.py", "labs//x.py"):
            root, doc = dummy()
            doc["candidate"]["files"][0]["path"] = bad
            self.refused(doc, root, "explicit identity malformed")

    def test_u12_declared_file_absent(self):
        root, doc = dummy()
        (root / "labs/real/workbook.py").unlink()
        self.refused(doc, root, "declared file absent")

    def test_u13_two_workbook_roles(self):
        root, doc = dummy()
        next(f for f in doc["candidate"]["files"] if f["path"] == "labs/real/workbook.py")["role"] = "workbook"
        self.refused(doc, root, "exactly one file must carry role 'workbook'")

    def test_u14_unsupported_schemas(self):
        root, doc = dummy()
        self.refused(dict(doc, schema="harness-inputs/9"), root, "unsupported inputs schema")
        doc["candidate"]["schema"] = "candidate-identity/2"
        self.refused(doc, root, "is not supported")

    def test_u15_pending_candidate(self):
        root, doc = dummy()
        self.refused(dict(doc, candidate="PENDING"), root, "PENDING")

    def test_u16_root_inside_live(self):
        root, doc = dummy()
        self.refused(doc, LIVE, "inside the live repo")

    def test_u17_dependencies_wrong_shape(self):
        for bad in (None, {}, "G"):
            root, doc = dummy()
            self.refused(dict(doc, dependencies=bad), root, "explicit identity malformed")

    def test_u18_wrong_review_ref(self):
        root, doc = dummy()
        next(d for d in doc["dependencies"] if d["id"] == "G")["review_ref"]["sha256"] = "0" * 64
        with self.assertRaises(I.Refused):
            I.verify_dependencies(doc)

    def test_u19_role_without_key(self):
        root, doc = dummy()
        doc["candidate"]["open_entry"] = None
        self.refused(doc, root, "declare role 'open'")

    def test_u20_wrong_types(self):
        root, doc = dummy()
        doc["candidate"]["files"][0]["bytes"] = True
        self.refused(doc, root, "bad bytes")
        root, doc = dummy()
        doc["candidate"]["files"] = {"app/librarian.py": {}}
        self.refused(doc, root, "candidate.files is not a non-empty list")


class Legacy(unittest.TestCase):
    def test_u21_two_baselines_resolve_labelled(self):
        want = {"proto-l": "labs/n7-local-lifecycle-pass01/workbook.py", "staged-g": "labs/workbook-review-pass05/workbook.py"}
        for k, root in BASELINES.items():
            doc = json.loads((LIVE / f"labs/loop-convergence-harness-pass02/inputs/inputs-{k}.json").read_text(encoding="utf-8"))
            ident = I.resolve(doc, root, SHAPE)
            self.assertEqual((ident["mode"], ident["kind"], ident["workbook_entry"]), ("legacy-discovery", k, want[k]))

    def test_u22_v2_for_non_baseline_refused(self):
        root, doc = dummy()
        with self.assertRaises(I.Refused) as cm:
            I.resolve(dict(doc, schema="harness-inputs/2"), root, SHAPE)
        self.assertIn("only for the two frozen baselines", str(cm.exception))

    def test_u23_old_combined_v2_refused_for_real_reasons(self):
        doc = json.loads(OLD_V2.read_text(encoding="utf-8"))
        with self.assertRaises(I.Refused) as cm:
            I.resolve(doc, OLD_COPY, SHAPE)
        msg = str(cm.exception)
        for needle in ("only for the two frozen baselines", "open_entry labs/review-loop-convergence-pass01/workbook.py is not a declared file",
                       "no workbook_entry"):
            self.assertIn(needle, msg)

    def test_u24_legacy_tampered_baseline_refused(self):
        doc = json.loads((LIVE / "labs/loop-convergence-harness-pass02/inputs/inputs-proto-l.json").read_text(encoding="utf-8"))
        doc["candidate"]["files"][0]["sha256"] = "0" * 64
        with self.assertRaises(I.Refused):
            I.resolve(doc, BASELINES["proto-l"], SHAPE)


class Pinning(unittest.TestCase):
    def test_u25_pass01_cases_unchanged(self):
        self.assertEqual(len(A.R1.CASES), 34)
        self.assertEqual(sum(c["required"] for c in A.R1.CASES), 32)
        for cid in ("F1", "F1b", "E1", "E2", "C4"):
            self.assertTrue(next(c for c in A.R1.CASES if c["id"] == cid)["required"], cid)

    def test_u26_old_inputs_byte_identical(self):
        rows = {r["path"]: r for r in json.loads(A.PACK24.read_bytes())["files"]}
        for rel, r in rows.items():
            if rel.startswith(("labs/loop-convergence-harness-pass0", "labs/freshness-boundary-tests-pass01/")):
                self.assertEqual(sha((LIVE / rel).read_bytes()), r["sha256"], rel)


if __name__ == "__main__":
    res = unittest.main(exit=False, verbosity=2).result
    print(f"ran {res.testsRun}, expected {EXPECTED_TESTS}")
    sys.exit(0 if res.wasSuccessful() and res.testsRun == EXPECTED_TESTS else 1)
