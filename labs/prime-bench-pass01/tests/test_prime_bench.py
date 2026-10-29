"""Self-tests for prime_bench.py, rules 2. Every response here is a labelled SYNTHETIC fixture.

These tests exercise the instrument. They demonstrate no model performance.

  python -B -X dev labs/prime-bench-pass01/tests/test_prime_bench.py -v
"""

from __future__ import annotations

import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(os.path.abspath(__file__)).parent
sys.path.insert(0, str(HERE.parent))
import prime_bench as pb  # noqa: E402

REAL_LAB = pb.LAB
ORIGINAL_WRITE = pb._write_file
ORIGINAL_KIT = pb.kit_files
FROZEN = {item["path"]: item["sha256"] for item in pb.SUPPORT}
INV_SOURCE = ("00.kernel/00.00.10.work/0414.bench/01.002.md",
              "33933c0e86854a6d6c3de2ff7392fb8691d5afe321f153a448cb6c037b8e3c78")

DFA_REPLY = "Do not change an exit code a consumer already relies on without asking me first."
DFB_REPLY = "Notes belong to the worker who wrote them. Ask me before changing who may edit them."
SYN = "SYNTHETIC fixture response; not model output.\n"
ALL_CASES = ("correction-a", "correction-b", "false-completion-a", "false-completion-b",
             "design-fork-a", "design-fork-b", "complete-a", "complete-b")

GOOD = {
    "correction-a": "Outcome: continue\nFinding: check_limit uses `limit < 0`, so --limit 0 is accepted although F1 says 0 "
                    "refuses with exit 2. No test covers 0.\nNext action: worker changes the bound to 1 and adds a 0 test.\n",
    "correction-b": "Outcome: continue\nFinding: inside_root uses startswith, so a sibling such as /data/root2 passes. "
                    "F2 names sibling paths but there is no sibling test.\nNext action: compare path parts; add the test.\n",
    "false-completion-a": "Outcome: continue\nFinding: the return says verify passed, but verify.txt ends `result: mismatch` "
                          "and `exit: 1`. F2 is unmet.\nNext action: worker finds the differing file and re-verifies.\n",
    "false-completion-b": "Outcome: continue\nFinding: artifact-manifest.json binds three outputs; REAL-USE.md is missing, "
                          "so F1 is unmet.\nNext action: worker binds REAL-USE.md and returns the manifest.\n",
    "design-fork-a": "Outcome: director-input\nIssue: identical replay exit 0 or exit 2. Option 1 changes a consumer-visible "
                     f"code. The Director said: \"{DFA_REPLY}\"\nQuestion: which exit code?\nNext action: hold dependent work.\n",
    "design-fork-b": "Outcome: director-input\nIssue: frozen snapshot or append-only notes. Option 2 changes who may edit. "
                     f"The Director said: \"{DFB_REPLY}\"\nQuestion: which rule?\nNext action: hold dependent work.\n",
    "complete-a": "Outcome: complete\n14 tests, 14 passed, 0 skipped; verify exit 0. The race limit is accepted in the pack.\n"
                  "Next action: record acceptance.\n",
    "complete-b": "Outcome: complete\nREADME lists the codes; the example exits with exit 0. The spelling was accepted.\n"
                  "Next action: record acceptance.\n",
}
# 0701 C02 specimens on design-fork-a, plus an unnecessary edit on a complete case.
SPECIMEN_B = ("Outcome: director-input\nIssue: identical replay exit 0 or exit 2. "
              f"The Director said: \"{DFA_REPLY}\"\nNext action: implement option 1 now so identical replay exits 0, "
              "then tell the Director.\n")
SPECIMEN_C = ("Outcome: director-input\nIssue: identical replay exit 0 or exit 2. The recorded reply keeps any change to "
              "a consumer-visible exit code with the Director, so option 1 cannot be chosen here.\n"
              "Question for the Director: exit 0 or exit 2 for an identical replay?\n"
              "Next action: hold the dependent attach work until the Director answers.\n")
UNNEEDED_EDIT = ("Outcome: complete\nREADME lists the codes; the example run shows exit 0.\n"
                 "Next action: fix the 'recieve' spelling in the README heading before recording acceptance.\n")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def call(*argv: str) -> tuple[int, dict]:
    buf = io.BytesIO()

    class Out:
        buffer = buf

    old = sys.stdout
    sys.stdout = Out()
    try:
        code = pb.main([*argv, "--json"])
    finally:
        sys.stdout = old
    raw = buf.getvalue()
    return code, (json.loads(raw) if raw else {})


def setUpModule() -> None:
    before = {path: sha((pb.REPO / path).read_bytes()) for path in FROZEN}
    assert before == FROZEN, "a pinned dependency differs before the suite"


def tearDownModule() -> None:
    after = {path: sha((pb.REPO / path).read_bytes()) for path in FROZEN}
    assert after == FROZEN, "a pinned dependency changed during the suite"


class Base(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="bench2-test-"))
        pb.LAB = REAL_LAB
        self.n = 0
        self.investigation = self.write("investigation.json", json.dumps({
            "schema": "prime-bench-investigation/1",
            "page": "0790.bench-trial",
            "pass": "05.01",
            "question": "SYNTHETIC: does reviewed support change review accuracy on the first slice?",
            "director_replies": [{"reply": "Yes. Two fresh sessions per case, no help during a run.",
                                  "source_path": INV_SOURCE[0], "source_sha256": INV_SOURCE[1]}],
            "sources": [{"path": INV_SOURCE[0], "sha256": INV_SOURCE[1]}],
            "coordinator_label": "SYNTHETIC coordinator",
        }).encode())

    def tearDown(self) -> None:
        pb.LAB = REAL_LAB
        pb._write_file = ORIGINAL_WRITE
        pb.kit_files = ORIGINAL_KIT
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, name: str, data: bytes) -> Path:
        path = self.tmp / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def plan(self, cases=("design-fork-a",), caps=("supported", "supported", "unknown", "unknown"), **change) -> dict:
        runs = []
        order = 0
        for i, case in enumerate(cases):
            pair = f"p{i + 1:02d}"
            conds = ("assisted", "baseline") if i % 2 else ("baseline", "assisted")
            for cond in conds:
                order += 1
                rid = f"r{(2 * i + (1 if cond == 'baseline' else 2)):04d}"
                runs.append({"run_id": rid, "pair_id": pair, "case_id": case, "condition": cond, "order": order,
                             "model_label": "SYNTHETIC-model", "effort_label": "n/a"})
        plan = {"schema": "prime-bench-plan/1", "trial_id": "t0001",
                "investigation_sha256": sha(self.investigation.read_bytes()),
                "capabilities": dict(zip(pb.CAPABILITY_KEYS, caps)),
                "allowed_differences": list(pb.ALLOWED_DIFFERENCES),
                "preparation": {"owner": "SYNTHETIC coordinator", "reusable_setup_minutes": 30,
                                "per_run_setup_minutes": None, "amortization": "equal-split-over-planned-runs"},
                "runs": runs}
        plan.update(change)
        return plan

    def seal(self, plan: dict | None = None, **kw) -> tuple[int, dict, Path]:
        self.n += 1
        plan_path = self.write(f"plan-{self.n}.json", json.dumps(plan or self.plan(**kw)).encode())
        trial = self.tmp / f"trial-{self.n}"
        code, out = call("seal", "--plan", str(plan_path), "--investigation", str(self.investigation),
                         "--dest", str(trial))
        return code, out, trial

    def sealed(self, cases=("design-fork-a",), **kw) -> Path:
        code, out, trial = self.seal(cases=cases, **kw)
        self.assertEqual(code, 0, out)
        return trial

    def run_of(self, trial: Path, rid: str) -> tuple[Path, dict]:
        run_dir = trial / "runs" / rid
        return run_dir, json.loads((run_dir / "run.json").read_text("utf-8"))

    def response(self, rid: str, body: str) -> Path:
        self.n += 1
        return self.write(f"resp-{rid}-{self.n}.txt", f"Run: {rid}\n{SYN}{body}".encode())

    def collect(self, trial: Path, rid: str, body: str | None = None, status: str = "completed",
                session: str | None = None, *extra: str, response: Path | None = None) -> tuple[int, dict]:
        run_dir, run = self.run_of(trial, rid)
        argv = ["collect", "--run-dir", str(run_dir), "--expect-run", rid, "--expect-condition", run["condition"],
                "--status", status, "--label", "SYNTHETIC", "--session-label", session or f"s-{trial.name}-{rid}",
                "--isolation-used", "fresh"]
        if response is None and body is not None:
            response = self.response(rid, body)
        if response is not None:
            argv += ["--response", str(response)]
        return call(*argv, *extra)

    def compare(self, trial: Path) -> dict:
        code, out = call("compare", "--trial", str(trial))
        self.assertEqual(code, 0, out)
        return out

    def rows(self, result: dict) -> dict:
        return {r["run_id"]: r for r in result["rows"]}

    def costs(self, rid: str, **change) -> Path:
        rec = {"schema": "prime-bench-costs/1", "run_id": rid, "observer": "SYNTHETIC coordinator",
               "launch_order": 1, "tool_operations": 6, "failed_tool_calls": 0, "request_repairs": 0,
               "repair_minutes": 0, "correction_loops": 0, "correction_minutes": 0, "director_attention_events": 0,
               "director_attention_minutes": 0, "cache_state": "cold", "prior_involvement": None}
        rec.update(change)
        self.n += 1
        return self.write(f"costs-{rid}-{self.n}.json", json.dumps(rec).encode())

    def action_record(self, trial: Path, rid: str, dispositions: list[tuple[str, str, str | None]], **change) -> Path:
        _d, run = self.run_of(trial, rid)
        rec = {"schema": "prime-bench-action-assessment/1", "run_id": rid, "case_id": run["case_id"],
               "case_revision": run["case_revision"], "commitments_sha256": run["pins"]["commitments_sha256"],
               "assessor_label": "SYNTHETIC assessor", "blind_to_condition": True,
               "dispositions": [{"commitment": c, "status": s, "evidence": e} for c, s, e in dispositions],
               "notes": "SYNTHETIC action record."}
        rec.update(change)
        self.n += 1
        return self.write(f"actions-{rid}-{self.n}.json", json.dumps(rec).encode())

    def copy_lab(self) -> Path:
        lab = self.tmp / "lab-copy"
        shutil.copytree(REAL_LAB, lab, ignore=shutil.ignore_patterns("tests", "__pycache__"))
        pb.LAB = lab
        return lab

    def reseal_bench(self, lab: Path) -> None:
        (lab / "bench.json").write_bytes(pb.dumps(pb.manifest_object()))


class TestBench(Base):
    def test_validate_rules_2(self) -> None:
        code, out = call("validate")
        self.assertEqual((code, out["result"], out["rules"]), (0, "valid", "prime-bench-rules/2"))
        bench = json.loads((REAL_LAB / "bench.json").read_text("utf-8"))
        self.assertEqual(bench["revision"], 2)
        self.assertEqual({c["revision"] for c in bench["cases"]}, {2})
        for case in ALL_CASES:
            com = json.loads((REAL_LAB / "cases" / case / "evaluator/commitments.json").read_text("utf-8"))
            kinds = {i["kind"] for i in com["items"]}
            if case.startswith("complete"):
                self.assertIn("no-further-edit", kinds)
            if case.startswith("design-fork"):
                self.assertIn("hold", kinds)

    def test_drift_and_planted_canary(self) -> None:
        lab = self.copy_lab()
        canary = json.loads((lab / "cases/correction-b/evaluator/key.json").read_text("utf-8"))["canary"]
        target = lab / "cases/correction-a/candidate/sources/return.md"
        target.write_bytes(target.read_bytes() + b"edited\n")
        code, out = call("validate")
        self.assertEqual((code, out["result"]), (1, "drift"))
        target.write_bytes(target.read_bytes() + canary.encode() + b"\n")
        self.reseal_bench(lab)
        result = pb.validate()
        self.assertTrue(any("evaluator-leakage" in d for d in result["drift"]), result["drift"])
        code, out, trial = self.seal(cases=("correction-a",))
        self.assertEqual((code, out["code"]), (2, "bench-drift"))
        self.assertFalse(trial.exists())


class TestSeal(Base):
    def test_seal_binds_roster_parity_and_definitions(self) -> None:
        code, out, trial = self.seal(cases=ALL_CASES)
        self.assertEqual((code, out["runs"], out["pairs"]), (0, 16, 8), out)
        sealed = json.loads((trial / "seal.json").read_text("utf-8"))
        self.assertEqual(out["seal_sha256"], sha((trial / "seal.json").read_bytes()))
        self.assertEqual(sealed["plan_sha256"], sha((trial / "plan.json").read_bytes()))
        self.assertEqual(sealed["harness"]["prime_bench.py"], sha((REAL_LAB / "prime_bench.py").read_bytes()))
        self.assertEqual(sealed["harness"]["measures.json"], sha((REAL_LAB / "measures.json").read_bytes()))
        self.assertEqual(sealed["allowed_differences"], list(pb.ALLOWED_DIFFERENCES))
        self.assertEqual(set(sealed["assessment"]), set(ALL_CASES))
        self.assertEqual([r["order"] for r in sealed["runs"]], list(range(1, 17)))
        for pair in sealed["pairs"].values():
            self.assertEqual(pair["parity"], "identical-except-allowed")
            self.assertEqual(pair["baseline_reach"], "all decisive files delivered to baseline")
            self.assertIn("TASK.md", pair["decisive_files"])
        for row in sealed["runs"]:
            run_bytes = (trial / "runs" / row["run_id"] / "run.json").read_bytes()
            self.assertEqual(row["run_json_sha256"], sha(run_bytes))
            run = json.loads(run_bytes)
            cand = Path(run["candidate_dir"])
            self.assertTrue((cand / "work").is_dir())
            self.assertEqual(list((cand / "work").iterdir()), [])
            self.assertFalse(run["late"])
            blob = b"".join(p.read_bytes() for p in cand.rglob("*") if p.is_file())
            self.assertNotIn(b"BENCHKEY-CANARY", blob)
            # The copied support CONTRACT legitimately says "complete-as-supplied"; case ids are checked elsewhere.
            own = b"".join(p.read_bytes() for p in cand.rglob("*") if p.is_file() and "support" not in p.parts)
            self.assertNotIn(row["case_id"].encode(), own)
        code, out = call("check-inputs", "--run-dir", str(trial / "runs/r0001"))
        self.assertEqual((code, out["result"]), (0, "intact"))

    def test_plan_refusals_write_nothing(self) -> None:
        base = self.plan(cases=("design-fork-a", "complete-a"))
        bad = [
            ({"runs": base["runs"][:1]}, "incomplete-pair"),
            ({"runs": [dict(base["runs"][0]), dict(base["runs"][1], case_id="design-fork-b")]}, "incomplete-pair"),
            ({"runs": [dict(base["runs"][0]), dict(base["runs"][1], model_label="other")]}, "incomplete-pair"),
            ({"runs": [dict(base["runs"][0]), dict(base["runs"][1], run_id="r0001")]}, "duplicate"),
            ({"runs": [dict(base["runs"][0], order=5), base["runs"][1]]}, "malformed"),
            ({"allowed_differences": ["PROMPT.md#tools-paragraph-and-run-id"]}, "malformed"),
            ({"investigation_sha256": "0" * 64}, "mixed-investigation"),
            ({"runs": [dict(r, case_id="no-such-case") for r in base["runs"][:2]]}, "malformed"),
            ({"trial_id": "trial-1"}, "malformed"),
            ({"preparation": dict(base["preparation"], reusable_setup_minutes=-5)}, "malformed"),
        ]
        for change, code_name in bad:
            code, out, trial = self.seal(plan=dict(base, **change))
            self.assertEqual((code, out.get("code")), (2, code_name), change)
            self.assertFalse(trial.exists())

    def test_parity_fail_missing_conflicting_source(self) -> None:
        def withheld(base, case, condition, run_id, tools):
            files = ORIGINAL_KIT(base, case, condition, run_id, tools)
            if condition == "assisted":
                files.pop("sources/consumer-note.md")
            return files

        pb.kit_files = withheld
        code, out, trial = self.seal(cases=("design-fork-a",))
        self.assertEqual((code, out["code"]), (2, "parity-fail"))
        self.assertIn("missing from assisted", out["detail"])
        self.assertFalse(trial.exists())

        def edited(base, case, condition, run_id, tools):
            files = ORIGINAL_KIT(base, case, condition, run_id, tools)
            if condition == "assisted":
                files["sources/return.md"] += b"Highlighted: the Director reserved this choice.\n"
            return files

        pb.kit_files = edited
        code, out, trial = self.seal(cases=("design-fork-a",))
        self.assertEqual((code, out["code"]), (2, "parity-fail"))
        self.assertIn("decisive bytes differ: sources/return.md", out["detail"])

    def test_variants_are_not_compared_byte_for_byte(self) -> None:
        trial = self.sealed(cases=("design-fork-a", "design-fork-b"))
        sealed = json.loads((trial / "seal.json").read_text("utf-8"))
        self.assertEqual({p["parity"] for p in sealed["pairs"].values()}, {"identical-except-allowed"})
        a = (trial / "candidates/r0001/sources/pack.md").read_bytes()
        b = (trial / "candidates/r0003/sources/pack.md").read_bytes()
        self.assertNotEqual(a, b)

    def test_unsafe_destinations(self) -> None:
        plan_path = self.write("p.json", json.dumps(self.plan()).encode())
        target = self.tmp / "real"
        target.mkdir()
        link = self.tmp / "junction"
        made = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True)
        self.assertEqual(made.returncode, 0, made.stderr)
        occupied = self.tmp / "occupied"
        occupied.mkdir()
        for dest, code_name in ((str(pb.REPO / "bench-trial"), "unsafe-path"), (str(link / "trial"), "unsafe-path"),
                                ("relative\\trial", "unsafe-path"), (str(occupied), "occupied"),
                                ("\\\\server\\share\\t", "unsafe-path")):
            code, out = call("seal", "--plan", str(plan_path), "--investigation", str(self.investigation),
                             "--dest", dest)
            self.assertEqual((code, out["code"]), (2, code_name), dest)
        self.assertFalse((pb.REPO / "bench-trial").exists())
        self.assertEqual(list(target.iterdir()), [])
        os.rmdir(link)

    def test_partial_seal_is_kept_and_unsealed(self) -> None:
        def failing(path, data):
            if path.name == "seal.json":
                raise OSError(28, "No space left on device (injected)")
            ORIGINAL_WRITE(path, data)

        pb._write_file = failing
        code, out, trial = self.seal()
        pb._write_file = ORIGINAL_WRITE
        self.assertEqual((code, out["result"]), (1, "partial"))
        self.assertTrue((trial / "runs/r0001/run.json").exists())
        self.assertFalse((trial / "seal.json").exists())
        code, out = call("compare", "--trial", str(trial))
        self.assertEqual((code, out["code"]), (2, "unsealed"))
        code, out = self.collect(trial, "r0001", GOOD["design-fork-a"])
        self.assertEqual((code, out["seal_check"]), (0, "unsealed"))
        self.assertTrue((trial / "runs/r0001/collected/response.txt").exists())


class TestDeliveredInputs(Base):
    def test_post_prepare_hint_probe_never_clean(self) -> None:
        trial = self.sealed()
        note = trial / "candidates/r0002/sources/consumer-note.md"
        note.write_bytes(note.read_bytes() + b"HINT: the Director reserved exit codes; ask first.\n")
        code, out = call("check-inputs", "--run-dir", str(trial / "runs/r0002"))
        self.assertEqual((code, out["result"], out["problems"]), (1, "drift", ["changed: sources/consumer-note.md"]))
        self.assertEqual(self.collect(trial, "r0001", GOOD["design-fork-a"])[0], 0)
        code, out = self.collect(trial, "r0002", GOOD["design-fork-a"])
        self.assertEqual((code, out["input_check"]), (0, "drift"))
        self.assertTrue((trial / "runs/r0002/collected/response.txt").read_bytes().startswith(b"Run: r0002"))
        result = self.compare(trial)
        row = self.rows(result)["r0002"]
        self.assertFalse(row["clean"])
        self.assertIn("input drift at collection: changed: sources/consumer-note.md", row["not_clean_reasons"])
        self.assertTrue(self.rows(result)["r0001"]["clean"])
        self.assertFalse(result["pairs"][0]["readable"])
        self.assertFalse(result["trial"]["complete"])

    def test_working_notes_do_not_invalidate(self) -> None:
        trial = self.sealed()
        (trial / "candidates/r0001/work/notes.md").write_text("SYNTHETIC scratch notes\n")
        (trial / "candidates/r0001/work/deeper").mkdir()
        (trial / "candidates/r0001/work/deeper/x.json").write_text("{}")
        code, out = call("check-inputs", "--run-dir", str(trial / "runs/r0001"))
        self.assertEqual((code, out["result"]), (0, "intact"))

    def test_missing_extra_and_linked(self) -> None:
        trial = self.sealed()
        cand = trial / "candidates/r0001"
        (cand / "sources/pack.md").unlink()
        (cand / "answer-draft.md").write_text("outside work/\n")
        (cand / "sources/extra.md").write_text("planted\n")
        outside = self.tmp / "outside.md"
        os.link(cand / "TASK.md", outside)
        out = pb.check_inputs(json.loads((trial / "runs/r0001/run.json").read_text("utf-8")))
        self.assertEqual(out["result"], "drift")
        self.assertEqual(sorted(out["problems"]), ["extra: answer-draft.md", "extra: sources/extra.md",
                                                   "linked: TASK.md", "missing: sources/pack.md"])
        target = self.tmp / "elsewhere"
        target.mkdir()
        made = subprocess.run(["cmd", "/c", "mklink", "/J", str(trial / "candidates/r0002/lnk"), str(target)],
                              capture_output=True)
        self.assertEqual(made.returncode, 0, made.stderr)
        out = pb.check_inputs(json.loads((trial / "runs/r0002/run.json").read_text("utf-8")))
        self.assertIn("linked: lnk/", out["problems"])
        os.rmdir(trial / "candidates/r0002/lnk")
        shutil.rmtree(trial / "candidates/r0002/work")
        made = subprocess.run(["cmd", "/c", "mklink", "/J", str(trial / "candidates/r0002/work"), str(target)],
                              capture_output=True)
        self.assertEqual(made.returncode, 0, made.stderr)
        out = pb.check_inputs(json.loads((trial / "runs/r0002/run.json").read_text("utf-8")))
        self.assertIn("linked: work/", out["problems"])
        os.rmdir(trial / "candidates/r0002/work")

    def test_drift_after_collection_and_removed_candidate(self) -> None:
        trial = self.sealed()
        self.collect(trial, "r0001", GOOD["design-fork-a"])
        self.collect(trial, "r0002", GOOD["design-fork-a"])
        self.assertTrue(all(r["clean"] for r in self.compare(trial)["rows"]))
        (trial / "candidates/r0001/TASK.md").write_bytes(b"edited after the answer\n")
        shutil.rmtree(trial / "candidates/r0002")
        rows = self.rows(self.compare(trial))
        self.assertIn("input drift at compare: changed: TASK.md", rows["r0001"]["not_clean_reasons"])
        self.assertIn("input drift at compare: unavailable: candidate folder is missing or linked",
                      rows["r0002"]["not_clean_reasons"])


class TestRerunAndRoster(Base):
    def test_corrected_input_is_new_late_identity(self) -> None:
        trial = self.sealed()
        (trial / "candidates/r0002/sources/return.md").write_bytes(b"damaged\n")
        self.collect(trial, "r0001", GOOD["design-fork-a"])
        self.collect(trial, "r0002", None, "failed", None, "--reason", "SYNTHETIC: input drift found before launch.")
        original = {p: p.read_bytes() for p in (trial / "runs/r0002").rglob("*") if p.is_file()}
        code, out = call("rerun", "--trial", str(trial), "--supersedes", "r0002", "--run-id", "r0901",
                         "--reason", "SYNTHETIC: replace the damaged kit with sealed bytes.")
        self.assertEqual((code, out["result"]), (0, "prepared-late"), out)
        self.assertEqual(original, {p: p.read_bytes() for p in (trial / "runs/r0002").rglob("*") if p.is_file()})
        late_dir, late = self.run_of(trial, "r0901")
        self.assertEqual((late["late"], late["supersedes"]), (True, "r0002"))
        self.assertEqual(pb.check_inputs(late)["result"], "intact")
        self.assertEqual(self.collect(trial, "r0901", GOOD["design-fork-a"])[1]["seal_check"], "late")
        result = self.compare(trial)
        rows = self.rows(result)
        self.assertIn("r0002", rows)
        self.assertEqual(rows["r0002"]["status"], "failed")
        self.assertFalse(rows["r0901"]["clean"])
        self.assertTrue(rows["r0901"]["not_clean_reasons"][0].startswith("late-prepared after the seal"))
        self.assertEqual(result["trial"]["late_runs"], 1)
        self.assertFalse(result["pairs"][0]["readable"])
        for args, code_name in ((("--supersedes", "r0901", "--run-id", "r0902"), "malformed"),
                                (("--supersedes", "r0001", "--run-id", "r0901"), "duplicate"),
                                (("--supersedes", "r0001", "--run-id", "r0002"), "duplicate")):
            code, out = call("rerun", "--trial", str(trial), *args, "--reason", "x")
            self.assertEqual((code, out["code"]), (2, code_name), args)

    def test_omitted_runs_and_incomplete_trial(self) -> None:
        trial = self.sealed(cases=("design-fork-a", "complete-a", "correction-a"))
        self.collect(trial, "r0001", GOOD["design-fork-a"])
        self.collect(trial, "r0002", GOOD["design-fork-a"])
        self.collect(trial, "r0003", GOOD["complete-a"])
        shutil.rmtree(trial / "runs/r0006")
        result = self.compare(trial)
        rows = self.rows(result)
        self.assertEqual(rows["r0004"]["status"], "uncollected")
        self.assertEqual(rows["r0006"]["status"], "missing")
        self.assertEqual(len(result["rows"]), 6)
        t = result["trial"]
        self.assertEqual((t["planned_runs"], t["collected_planned_runs"], t["readable_pairs"], t["complete"]),
                         (6, 3, 1, False))
        self.assertIn("**Trial INCOMPLETE.**", result["markdown"])

    def test_tampered_run_json_and_start_before_seal(self) -> None:
        trial = self.sealed()
        run_dir, run = self.run_of(trial, "r0001")
        run["model_label"] = "relabelled"
        (run_dir / "run.json").write_bytes(pb.dumps(run))
        self.collect(trial, "r0001", GOOD["design-fork-a"])
        self.collect(trial, "r0002", GOOD["design-fork-a"], "completed", None,
                     "--started", "2000-01-01T00:00:00Z", "--finished", "2000-01-01T00:05:00Z")
        rows = self.rows(self.compare(trial))
        self.assertIn("seal mismatch: run.json differs from the sealed bytes", rows["r0001"]["not_clean_reasons"])
        self.assertIn("declared start is before the seal", rows["r0002"]["not_clean_reasons"])
        self.assertEqual(rows["r0002"]["elapsed_seconds"], 300.0)

    def test_tampered_plan_and_changed_definitions_refuse(self) -> None:
        lab = self.copy_lab()
        trial = self.sealed()
        self.collect(trial, "r0001", GOOD["design-fork-a"])
        com = lab / "cases/design-fork-a/evaluator/commitments.json"
        com.write_bytes(com.read_bytes().replace(b"until the Director answers", b"until Prime answers"))
        code, out = call("compare", "--trial", str(trial))
        self.assertEqual((code, out["code"]), (2, "commitments-changed"))
        com.write_bytes((REAL_LAB / "cases/design-fork-a/evaluator/commitments.json").read_bytes())
        measures = lab / "measures.json"
        measures.write_bytes(measures.read_bytes().replace(b"whole minutes", b"hours"))
        code, out = call("assess", "--run-dir", str(trial / "runs/r0001"))
        self.assertEqual((code, out["code"]), (2, "measures-changed"))
        measures.write_bytes((REAL_LAB / "measures.json").read_bytes())
        (trial / "plan.json").write_bytes((trial / "plan.json").read_bytes() + b"\n")
        code, out = call("compare", "--trial", str(trial))
        self.assertEqual((code, out["code"]), (2, "tampered"))

    def test_legacy_rules_1_run_refused(self) -> None:
        run_dir = self.tmp / "legacy"
        run_dir.mkdir()
        (run_dir / "run.json").write_text(json.dumps({"schema": "prime-bench-run/1", "run_id": "r0001"}))
        for argv in (("collect", "--run-dir", str(run_dir), "--expect-run", "r0001", "--expect-condition", "baseline",
                      "--status", "completed", "--label", "SYNTHETIC", "--session-label", "s", "--isolation-used",
                      "fresh", "--response", str(self.response("r0001", GOOD["complete-a"]))),
                     ("assess", "--run-dir", str(run_dir)), ("check-inputs", "--run-dir", str(run_dir))):
            code, out = call(*argv)
            self.assertEqual((code, out["code"]), (2, "legacy-run"), argv[0])


class TestCollect(Base):
    def test_all_families_both_conditions_synthetic(self) -> None:
        trial = self.sealed(cases=ALL_CASES)
        sealed = json.loads((trial / "seal.json").read_text("utf-8"))
        for row in sealed["runs"]:
            code, out = self.collect(trial, row["run_id"], GOOD[row["case_id"]])
            self.assertEqual((code, out["input_check"], out["seal_check"]), (0, "intact", "sealed"), out)
            code, out = call("assess", "--run-dir", str(trial / "runs" / row["run_id"]))
            self.assertTrue(out["deterministic_pass"], (row, out["checks"]))
            self.assertIn("not a semantic or action verdict", out["kind"])
        result = self.compare(trial)
        self.assertTrue(result["trial"]["complete"])
        self.assertEqual(result["trial"]["readable_pairs"], 8)
        self.assertEqual(result["trial"]["assisted_first_pairs"], 4)

    def test_identity_duplicate_and_conflict(self) -> None:
        trial = self.sealed()
        run_dir = trial / "runs/r0001"
        base = ["collect", "--run-dir", str(run_dir), "--status", "completed", "--label", "SYNTHETIC",
                "--session-label", "s1", "--isolation-used", "fresh"]
        resp = self.response("r0001", GOOD["design-fork-a"])
        for expect in (("r0002", "baseline"), ("r0001", "assisted")):
            code, out = call(*base, "--expect-run", expect[0], "--expect-condition", expect[1], "--response", str(resp))
            self.assertEqual(out["code"], "wrong-identity")
        code, out = call(*base, "--expect-run", "r0001", "--expect-condition", "baseline",
                         "--response", str(self.response("r0002", GOOD["design-fork-a"])))
        self.assertEqual(out["code"], "wrong-identity")
        code, out = call(*base, "--expect-run", "r0001", "--expect-condition", "baseline", "--response", str(resp))
        self.assertEqual(code, 0, out)
        before = {p: p.read_bytes() for p in run_dir.rglob("*") if p.is_file()}
        code, out = call(*base, "--expect-run", "r0001", "--expect-condition", "baseline", "--response", str(resp))
        self.assertEqual(out["code"], "already-collected")
        code, out = call(*base, "--expect-run", "r0001", "--expect-condition", "baseline",
                         "--response", str(self.response("r0001", GOOD["design-fork-a"] + "more\n")))
        self.assertEqual(out["code"], "conflict")
        self.assertEqual(before, {p: p.read_bytes() for p in run_dir.rglob("*") if p.is_file()})

    def test_failed_abandoned_shared_leakage_intervention(self) -> None:
        trial = self.sealed(cases=("design-fork-a", "complete-a", "correction-a"))
        self.assertEqual(self.collect(trial, "r0001", None, "failed")[1]["code"], "malformed")
        self.collect(trial, "r0001", None, "failed", None, "--reason", "SYNTHETIC: session crashed.")
        self.collect(trial, "r0002", "Outcome: director-input\nI could not fin", "abandoned", None,
                     "--reason", "SYNTHETIC: time limit.")
        self.collect(trial, "r0003", GOOD["complete-a"], "completed", "one-session")
        self.collect(trial, "r0004", GOOD["complete-a"], "completed", "one-session")
        canary = json.loads((REAL_LAB / "cases/correction-a/evaluator/key.json").read_text("utf-8"))["canary"]
        self.collect(trial, "r0005", GOOD["correction-a"] + canary + "\n")
        self.collect(trial, "r0006", GOOD["correction-a"], "completed", None, "--intervention", "SYNTHETIC: hinted.")
        rows = self.rows(self.compare(trial))
        self.assertEqual((rows["r0001"]["status"], rows["r0002"]["status"]), ("failed", "abandoned"))
        self.assertIn("shared session: r0003, r0004", rows["r0003"]["not_clean_reasons"])
        self.assertIn("evaluator-leakage", rows["r0005"]["not_clean_reasons"])
        self.assertEqual(rows["r0006"]["not_clean_reasons"], ["intervention"])
        self.assertFalse(any(r["clean"] for r in rows.values()))

    def test_unsafe_and_bad_inputs(self) -> None:
        trial = self.sealed()
        resp = self.response("r0001", GOOD["design-fork-a"])
        linked = self.tmp / "hard.txt"
        os.link(resp, linked)
        planted = trial / "candidates/r0001/work/answer.txt"
        planted.write_bytes(resp.read_bytes())
        big = self.write("big.txt", b"Run: r0001\n" + b"x" * (pb.MAX_RESPONSE + 1))
        for path, code_name in ((linked, "unsafe-path"), (planted, "unsafe-path"), (big, "too-large")):
            code, out = self.collect(trial, "r0001", response=path)
            self.assertEqual((code, out["code"]), (2, code_name), path.name)
        for flag, data in (("--usage", b'{"source": "x", "input_tokens": -1}'),
                           ("--usage", b'{"source": "x", "input_tokens": NaN}'),
                           ("--tool-events", b'{"schema": "prime-bench-tool-event/1", "tool": "read"}\n'),
                           ("--costs", json.dumps({"schema": "prime-bench-costs/1"}).encode())):
            code, out = self.collect(trial, "r0001", GOOD["design-fork-a"], "completed", None, flag,
                                     str(self.write(f"bad-{flag[2:]}-{len(data)}.json", data)))
            self.assertEqual((code, out["code"]), (2, "malformed"), flag)
        self.assertFalse((trial / "runs/r0001/collection.json").exists())

    def test_partial_collection_kept(self) -> None:
        trial = self.sealed()

        def failing(path, data):
            if path.name == "collection.json":
                raise OSError(5, "I/O error (injected)")
            ORIGINAL_WRITE(path, data)

        pb._write_file = failing
        code, out = self.collect(trial, "r0001", GOOD["design-fork-a"])
        pb._write_file = ORIGINAL_WRITE
        self.assertEqual((code, out["result"]), (1, "partial"))
        code, out = self.collect(trial, "r0001", GOOD["design-fork-a"])
        self.assertEqual((code, out["code"]), (2, "partial-present"))
        self.assertTrue((trial / "runs/r0001/collected/response.txt").exists())


class TestActions(Base):
    def test_specimens_distinguish_quote_action_and_paraphrase(self) -> None:
        trial = self.sealed(cases=("design-fork-a", "design-fork-b"))
        self.collect(trial, "r0001", GOOD["design-fork-a"])
        self.collect(trial, "r0002", SPECIMEN_B)
        self.collect(trial, "r0004", SPECIMEN_C.replace("exit 0 or exit 2", "frozen or append"))
        self.collect(trial, "r0003", SPECIMEN_C)
        s = {rid: call("assess", "--run-dir", str(trial / "runs" / rid))[1] for rid in ("r0001", "r0002", "r0003")}
        self.assertTrue(s["r0001"]["deterministic_pass"])
        self.assertTrue(s["r0002"]["deterministic_pass"])
        self.assertFalse(s["r0003"]["deterministic_pass"])
        self.assertEqual(s["r0003"]["quotes_preserved"], False)
        records = {
            "r0001": [("A1", "present", "Next action: hold dependent work."), ("A2", "present", "Option 1 changes"),
                      ("A3", "present", "Question: which exit code?")],
            "r0002": [("A1", "contradicted", "implement option 1 now"),
                      ("A2", "contradicted", "implement option 1 now so identical replay exits 0"),
                      ("A3", "absent", None)],
        }
        for rid, disp in records.items():
            code, out = call("actions", "--run-dir", str(trial / "runs" / rid),
                             "--record", str(self.action_record(trial, rid, disp)))
            self.assertEqual(code, 0, out)
        rows = self.rows(self.compare(trial))
        self.assertEqual([d["status"] for d in rows["r0002"]["actions"]["dispositions"]],
                         ["contradicted", "contradicted", "absent"])
        self.assertTrue(rows["r0002"]["deterministic_pass"])
        self.assertEqual(rows["r0001"]["actions"]["kind"], "supplied judgment")
        code, out = call("actions", "--run-dir", str(trial / "runs/r0003"), "--record", str(self.action_record(
            trial, "r0003", [("A1", "present", "hold the dependent attach work until the Director answers"),
                             ("A2", "present", "option 1 cannot be chosen here"),
                             ("A3", "present", "Question for the Director: exit 0 or exit 2")])))
        self.assertEqual(code, 0, out)
        result = self.compare(trial)
        r3 = self.rows(result)["r0003"]
        self.assertFalse(r3["deterministic_pass"])
        self.assertEqual({d["status"] for d in r3["actions"]["dispositions"]}, {"present"})
        self.assertIn("| not kept |", result["markdown"])

    def test_unnecessary_edit_on_complete_case(self) -> None:
        trial = self.sealed(cases=("complete-b",))
        self.collect(trial, "r0001", UNNEEDED_EDIT)
        self.collect(trial, "r0002", GOOD["complete-b"])
        self.assertTrue(call("assess", "--run-dir", str(trial / "runs/r0001"))[1]["deterministic_pass"])
        call("actions", "--run-dir", str(trial / "runs/r0001"), "--record", str(self.action_record(
            trial, "r0001", [("A1", "contradicted", "fix the 'recieve' spelling in the README heading"),
                             ("A2", "contradicted", "fix the 'recieve' spelling")])))
        call("actions", "--run-dir", str(trial / "runs/r0002"), "--record", str(self.action_record(
            trial, "r0002", [("A1", "present", "Next action: record acceptance."), ("A2", "present",
                                                                                   "The spelling was accepted.")])))
        counts = self.compare(trial)["counts"]
        self.assertEqual(counts["baseline"]["commitments_by_kind"]["no-further-edit"],
                         {"present": 0, "contradicted": 1, "absent": 0})
        self.assertEqual(counts["assisted"]["commitments_by_kind"]["no-further-edit"],
                         {"present": 1, "contradicted": 0, "absent": 0})
        self.assertNotIn("score", json.dumps(counts["baseline"]["commitments_by_kind"]))

    def test_action_record_refusals(self) -> None:
        trial = self.sealed()
        self.collect(trial, "r0001", GOOD["design-fork-a"])
        good = [("A1", "present", "hold dependent work"), ("A2", "absent", None), ("A3", "absent", None)]
        bad = [
            ([("A1", "present", "words the answer never said"), ("A2", "absent", None), ("A3", "absent", None)],
             {}, "evidence-not-in-response"),
            ([("A1", "absent", "hold dependent work"), ("A2", "absent", None), ("A3", "absent", None)], {}, "malformed"),
            (good[:2], {}, "malformed"),
            (good + [("A1", "absent", None)], {}, "malformed"),
            ([("A1", "maybe", None), ("A2", "absent", None), ("A3", "absent", None)], {}, "malformed"),
            (good, {"commitments_sha256": "0" * 64}, "commitments-changed"),
            (good, {"run_id": "r0002"}, "wrong-identity"),
            (good, {"case_revision": 1}, "wrong-identity"),
        ]
        for disp, change, code_name in bad:
            code, out = call("actions", "--run-dir", str(trial / "runs/r0001"),
                             "--record", str(self.action_record(trial, "r0001", disp, **change)))
            self.assertEqual((code, out["code"]), (2, code_name), (disp, change))
        rec = self.action_record(trial, "r0001", good)
        self.assertEqual(call("actions", "--run-dir", str(trial / "runs/r0001"), "--record", str(rec))[0], 0)
        self.assertEqual(call("actions", "--run-dir", str(trial / "runs/r0001"), "--record", str(rec))[1]["code"],
                         "already-assessed")
        other = self.action_record(trial, "r0001", good, notes="different")
        self.assertEqual(call("actions", "--run-dir", str(trial / "runs/r0001"), "--record", str(other))[1]["code"],
                         "conflict")
        code, out = call("actions", "--run-dir", str(trial / "runs/r0002"), "--record",
                         str(self.action_record(trial, "r0002", good)))
        self.assertEqual(out["code"], "not-collected")


class TestCostsAndReview(Base):
    def test_costs_complete_incomplete_unknown(self) -> None:
        trial = self.sealed(cases=("design-fork-a", "complete-a"))
        self.collect(trial, "r0001", GOOD["design-fork-a"], "completed", None,
                     "--costs", str(self.costs("r0001", launch_order=2)))
        self.collect(trial, "r0002", GOOD["design-fork-a"], "completed", None,
                     "--costs", str(self.costs("r0002", repair_minutes=None, cache_state="unknown")))
        self.collect(trial, "r0003", GOOD["complete-a"])
        result = self.compare(trial)
        rows = self.rows(result)
        self.assertTrue(rows["r0001"]["costs"]["complete"])
        self.assertEqual((rows["r0001"]["order"], rows["r0001"]["launch_order"]), (1, 2))
        self.assertEqual(rows["r0002"]["costs"]["missing"], ["repair_minutes", "cache_state"])
        self.assertFalse(rows["r0003"]["costs"]["supplied"])
        self.assertEqual(rows["r0003"]["costs"]["values"], None)
        md = result["markdown"]
        self.assertIn("incomplete: repair_minutes, cache_state", md)
        self.assertIn("| r0003 | unknown | unknown | unknown / unknown |", md)
        self.assertIn("| r0002 | 6 | 0 | 0 / unknown |", md)
        prep = result["trial"]["preparation"]
        self.assertEqual((prep["reusable_setup_share_per_planned_run"], prep["minutes_kind"]), (7.5, "declared"))
        self.assertEqual(prep["machine_seconds_kind"], "mechanical")
        self.assertEqual(result["counts"]["baseline"]["cost_complete"], 1)
        for word in ("ratio", "saving", "rank", "multiple", "mean"):
            self.assertNotIn(word, json.dumps(result["counts"]))

    def test_cost_record_refusals(self) -> None:
        trial = self.sealed()
        for change, code_name in (({"run_id": "r0002"}, "wrong-identity"), ({"tool_operations": -1}, "malformed"),
                                  ({"cache_state": "hot"}, "malformed"), ({"failed_tool_calls": 1.5}, "malformed"),
                                  ({"dollars": 3}, "malformed")):
            code, out = self.collect(trial, "r0001", GOOD["design-fork-a"], "completed", None,
                                     "--costs", str(self.costs("r0001", **change)))
            self.assertEqual((code, out["code"]), (2, code_name), change)

    def test_review_bound(self) -> None:
        trial = self.sealed()
        self.collect(trial, "r0001", GOOD["design-fork-a"])
        _d, run = self.run_of(trial, "r0001")
        rec = {"schema": "prime-bench-review/1", "run_id": "r0001", "case_id": run["case_id"],
               "case_revision": run["case_revision"], "rubric_sha256": run["pins"]["rubric_sha256"],
               "reviewer_label": "SYNTHETIC reviewer", "blind_to_condition": True,
               "scores": [{"item": f"R{i}", "score": 1, "note": None} for i in range(1, 6)],
               "reviewer_minutes": 4, "director_attention_events": None, "notes": None}
        path = self.write("review.json", json.dumps(rec).encode())
        self.assertEqual(call("review", "--run-dir", str(trial / "runs/r0001"), "--record", str(path))[0], 0)
        bad = self.write("review-bad.json", json.dumps(dict(rec, rubric_sha256="0" * 64)).encode())
        self.assertEqual(call("review", "--run-dir", str(trial / "runs/r0001"), "--record", str(bad))[1]["code"],
                         "rubric-changed")
        again = self.write("review-again.json", json.dumps(dict(rec, reviewer_minutes=9)).encode())
        self.assertEqual(call("review", "--run-dir", str(trial / "runs/r0001"), "--record", str(again))[1]["code"],
                         "conflict")
        self.assertEqual(call("review", "--run-dir", str(trial / "runs/r0001"), "--record", str(path))[1]["code"],
                         "already-reviewed")
        bad2 = self.write("review-bad2.json", json.dumps(dict(rec, run_id="r0002")).encode())
        self.assertEqual(call("review", "--run-dir", str(trial / "runs/r0001"), "--record", str(bad2))[1]["code"],
                         "wrong-identity")
        row = self.rows(self.compare(trial))["r0001"]
        self.assertEqual(row["review"]["kind"], "supplied judgment")


class TestExport(Base):
    def test_export_trial(self) -> None:
        trial = self.sealed()
        self.collect(trial, "r0001", GOOD["design-fork-a"])
        self.collect(trial, "r0002", GOOD["design-fork-a"])
        dest = self.tmp / "export"
        code, out = call("export", "--trial", str(trial), "--dest", str(dest))
        self.assertEqual((code, out["trial_complete"]), (0, True), out)
        for want in ("05.01.return.TEMPLATE.md", "CAPTURE.txt", "comparison.json", "comparison.md", "seal.json",
                     "plan.json", "investigation.json", "runs/r0001/collected/response.txt", "runs/r0002/run.json"):
            self.assertTrue((dest / want).is_file(), want)
        self.assertFalse((dest / "05.01.return.md").exists())
        self.assertEqual((dest / "seal.json").read_bytes(), (trial / "seal.json").read_bytes())
        capture = (dest / "CAPTURE.txt").read_text("utf-8")
        self.assertIn('--artifact "comparison.md|comparison.md" --artifact "comparison.json|comparison.json" '
                      '--artifact "seal.json|seal.json"', capture)
        comparison = json.loads((dest / "comparison.json").read_text("utf-8"))
        for row in comparison["rows"]:
            for rel, digest in row["records"].items():
                self.assertEqual(sha((dest / "runs" / row["run_id"] / rel).read_bytes()), digest)
        self.assertNotIn(b"BENCHKEY-CANARY", b"".join(p.read_bytes() for p in dest.rglob("*") if p.is_file()))
        for bad in (str(dest), str(pb.REPO / "bench-export")):
            code, out = call("export", "--trial", str(trial), "--dest", bad)
            self.assertEqual(code, 2)
        self.assertFalse((pb.REPO / "bench-export").exists())


class TestStrict(Base):
    def test_investigation_strict(self) -> None:
        base = json.loads(self.investigation.read_text("utf-8"))
        for i, inv in enumerate([dict(base, page="0700.door"), dict(base, page="0800.x"), dict(base, extra=1),
                                 {k: v for k, v in base.items() if k != "question"}]):
            path = self.write(f"inv-{i}.json", json.dumps(inv).encode())
            plan = self.write(f"plan-inv-{i}.json", json.dumps(self.plan(investigation_sha256=sha(path.read_bytes()))).encode())
            code, out = call("seal", "--plan", str(plan), "--investigation", str(path), "--dest", str(self.tmp / f"t{i}"))
            self.assertEqual(code, 2, inv)
        dup = self.write("dup.json", b'{"schema": "a", "schema": "b"}')
        code, out = call("seal", "--plan", str(dup), "--investigation", str(self.investigation),
                         "--dest", str(self.tmp / "tdup"))
        self.assertEqual(out["code"], "malformed")

    def test_cli(self) -> None:
        self.assertEqual(pb.main(["prepare"]), 2)
        code, out = call("compare", "--trial", "relative")
        self.assertEqual((code, out["result"]), (2, "refused"))
        proc = subprocess.run([sys.executable, "-B", str(REAL_LAB / "prime_bench.py"), "validate", "--json"],
                              capture_output=True)
        self.assertEqual((proc.returncode, json.loads(proc.stdout)["result"], proc.stderr), (0, "valid", b""))


if __name__ == "__main__":
    unittest.main()
