"""Adapter self-tests for 0705 pass03. They use small SYNTHETIC raw outputs written by the test, never candidate
evidence, to check that the adapter refuses tampering and never invents or upgrades facts.

  python -I -B tests/test_adapter.py [--report ABS]
"""
import argparse
import hashlib
import inspect
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
import adapter as A  # noqa: E402

CAND = "c" * 64
B = "00.kernel/00.00.10.work/"


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Fake:
    """A synthetic fixture dir plus a run dir with a recorded raw view."""

    def __init__(self, tmp: Path, view: dict, catalog_works=("0522.review-construction/05.04",)):
        self.fix = tmp / "fixture"
        (self.fix / "instance-A").mkdir(parents=True)
        files = {}
        for w in catalog_works:
            p = self.fix / "instance-A" / (B + w + ".md")
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(f"SYNTHETIC {w}\n".encode())
            files[B + w + ".md"] = sha(p.read_bytes())
        sel = self.fix / "instance-A" / (B + "0401.goal/06.01.md")
        sel.parent.mkdir(parents=True, exist_ok=True)
        sel.write_bytes(b"current_work: " + (B + "0522.review-construction/05.03.md").encode() + b"\n")
        cat = {"selector": B + "0401.goal/06.01.md", "works": [{"work_ref": w, "path": B + w + ".md"} for w in catalog_works],
               "parallel": [], "workers": [], "observer_sources": [], "declared_sources": []}
        (self.fix / "catalog.json").write_text(json.dumps(cat))
        fm = {"instances": {"instance-A": {"root": str(self.fix / "instance-A"), "files": files}}}
        (self.fix / "fixture-manifest.json").write_text(json.dumps(fm))
        self.run = tmp / "run"
        shutil.copytree(self.fix / "instance-A", self.run / "book")
        prep = A.prepare_request(self.fix, self.run / "book", tmp, "0522.review-construction/05.04")
        raw = json.dumps(view).encode()
        (self.run / "view.stdout").write_bytes(raw)
        self.rec = {"case": "CX", "candidate_sha256": CAND, "request_sha256": prep["request_sha256"],
                    "fixture_manifest_sha256": sha((self.fix / "fixture-manifest.json").read_bytes()),
                    "view": {"stdout_file": "view.stdout", "stdout_sha256": sha(raw)}}
        self.write_rec()

    def write_rec(self):
        (self.run / "run-record.json").write_text(json.dumps(self.rec))

    def normalize(self):
        return A.normalize(self.run, CAND, self.fix)


def view(**over):
    v = {"schema": "prime-desk-view/1", "instance": {"root": None}, "selected": {"id": "w-x", "address": "0522.review-construction/05.04",
         "basis": "observed", "source": {"path": B + "0522.review-construction/05.04.md", "status": "matched", "basis": "observed", "sha256": "a" * 64, "bytes": 1}},
         "not_selected": [], "attention": [], "gaps": [], "record": {"references": [], "assignment_reader": []}, "foreign": [],
         "inspectability": {"fingerprint": "f" * 64}}
    v.update(over)
    return v


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="adapter-0705-"))
        self.addCleanup(shutil.rmtree, self.tmp, True)

    def test_altered_raw_output_refused(self):
        f = Fake(self.tmp, view())
        (f.run / "view.stdout").write_bytes(b'{"tampered": true}')
        with self.assertRaises(A.AdapterRefused):
            f.normalize()

    def test_wrong_candidate_identity_refused(self):
        f = Fake(self.tmp, view())
        f.rec["candidate_sha256"] = "d" * 64
        f.write_rec()
        with self.assertRaises(A.AdapterRefused):
            f.normalize()

    def test_altered_request_refused(self):
        f = Fake(self.tmp, view())
        (f.run / "book" / A.REQUEST_FILE).write_bytes(b"{}")
        with self.assertRaises(A.AdapterRefused):
            f.normalize()

    def test_missing_selected_key_is_unmapped_not_invented(self):
        v = view()
        del v["selected"]
        obs, trace, conf = Fake(self.tmp, v).normalize()
        self.assertIn("selected", obs["producer"]["unmapped"])
        self.assertIsNone(obs["selected"]["work_ref"])
        self.assertIsNone(obs["selected"]["basis"])

    def test_basis_copied_never_upgraded(self):
        v = view()
        v["selected"]["basis"] = "supplied"
        obs, _, _ = Fake(self.tmp, v).normalize()
        self.assertEqual(obs["selected"]["basis"], "supplied")

    def test_conflicts_reported(self):
        v = view(record={"references": [
            {"source": {"path": B + "x.md", "status": "matched", "sha256": "1" * 64}},
            {"source": {"path": B + "x.md", "status": "matched", "sha256": "2" * 64}}],
            "assignment_reader": [{"fields": {"current_work": B + "0522.review-construction/05.03.md"}}]})
        obs, _, conf = Fake(self.tmp, v, ("0522.review-construction/05.04", "0522.review-construction/05.03")).normalize()
        kinds = sorted(c["kind"] for c in conf["conflicts"])
        self.assertEqual(kinds, ["same-path-different-hash", "selection-vs-canonical"])

    def test_unknown_gap_kind_is_coverage_gap_not_dropped(self):
        v = view(gaps=[{"kind": "brand-new-kind", "path": None, "check": "x"}])
        obs, _, _ = Fake(self.tmp, v).normalize()
        self.assertEqual(obs["attention"]["items"][0]["kind"], "coverage-gap")

    def test_prepare_request_has_no_expectation_input_and_fixed_shadow(self):
        params = list(inspect.signature(A.prepare_request).parameters)
        self.assertEqual(params, ["fixture_case_dir", "run_book", "tools_root", "shadow_work_ref"])
        import ast
        fn = ast.parse(inspect.getsource(A.prepare_request)).body[0]
        body = fn.body[1:] if isinstance(fn.body[0], ast.Expr) and isinstance(getattr(fn.body[0], "value", None), ast.Constant) else fn.body
        code = "\n".join(ast.unparse(s) for s in body)  # code only; the docstring may mention expected.json
        self.assertNotIn("expected", code)
        f1 = Fake(self.tmp / "a", view())
        f2 = Fake(self.tmp / "b", view(), ("0522.review-construction/05.03", "0522.review-construction/05.04"))
        s1 = json.loads((f1.run / "book" / A.SELECTOR_FILE).read_bytes())
        s2 = json.loads((f2.run / "book" / A.SELECTOR_FILE).read_bytes())
        self.assertEqual(s1["selected_work_id"], s2["selected_work_id"])

    def test_labels_are_not_authentication(self):
        obs, _, _ = Fake(self.tmp, view()).normalize()
        self.assertEqual(obs["producer"]["kind"], "candidate")
        self.assertEqual(obs["producer"]["adapter"]["status"], "connected")
        self.assertNotIn("authenticated", json.dumps(obs))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--report")
    a, rest = ap.parse_known_args()
    prog = unittest.main(argv=[sys.argv[0], "-v"] + rest, exit=False)
    r = prog.result
    if a.report:
        Path(a.report).write_text(json.dumps({"schema": "adapter-selftest/1", "label": "SYNTHETIC adapter self-tests; not candidate evidence",
                                              "python": sys.version.split()[0], "tests_run": r.testsRun, "failures": len(r.failures),
                                              "errors": len(r.errors), "skipped": len(r.skipped)}, indent=1) + "\n")
    sys.exit(0 if r.wasSuccessful() else 1)
