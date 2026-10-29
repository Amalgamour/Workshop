"""Self-tests for prime_bench.py. Every response here is a labelled SYNTHETIC fixture.

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
FROZEN = {item["path"]: item["sha256"] for item in pb.SUPPORT}
FROZEN_BEFORE: dict[str, str] = {}

DFA_REPLY = "Do not change an exit code a consumer already relies on without asking me first."
DFB_REPLY = "Notes belong to the worker who wrote them. Ask me before changing who may edit them."
SYN = "SYNTHETIC fixture response; not model output.\n"

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
WRONG = {
    "correction-a": "Outcome: complete\nAll 12 tests pass.\n",
    "false-completion-a": "Outcome: complete\nVerify passed as the return says.\n",
    "design-fork-a": "Outcome: continue\nTake option 1; exit 0 is safer.\n",
    "complete-b": "Outcome: continue\nFix the typo recieve first.\n",
}


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
    for path in FROZEN:
        FROZEN_BEFORE[path] = sha((pb.REPO / path).read_bytes())
    assert FROZEN_BEFORE == FROZEN, "a pinned dependency differs before the suite"


def tearDownModule() -> None:
    after = {path: sha((pb.REPO / path).read_bytes()) for path in FROZEN}
    assert after == FROZEN, "a pinned dependency changed during the suite"


class Base(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="bench-test-"))
        pb.LAB = REAL_LAB
        self.investigation = self.write("investigation.json", json.dumps({
            "schema": "prime-bench-investigation/1",
            "page": "0790.bench-trial",
            "pass": "05.01",
            "question": "SYNTHETIC: does reviewed support change review accuracy on the first slice?",
            "director_replies": [{"reply": "Yes. Two fresh sessions per case, no help during a run.",
                                  "source_path": "00.kernel/00.00.10.work/0414.bench/01.md",
                                  "source_sha256": "d226c3b5d645b651b8b8d945cb3716da267d421509dd03572cb7254cf5d6e8be"}],
            "sources": [{"path": "00.kernel/00.00.10.work/0414.bench/01.md",
                         "sha256": "d226c3b5d645b651b8b8d945cb3716da267d421509dd03572cb7254cf5d6e8be"}],
            "coordinator_label": "SYNTHETIC coordinator",
        }).encode())
        self.count = 0

    def tearDown(self) -> None:
        pb.LAB = REAL_LAB
        pb._write_file = ORIGINAL_WRITE
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, name: str, data: bytes) -> Path:
        path = self.tmp / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def prepare(self, case: str, condition: str = "baseline", run_id: str | None = None,
                caps: tuple[str, str, str, str] = ("supported", "supported", "unknown", "unsupported"),
                investigation: Path | None = None) -> tuple[int, dict, Path, Path]:
        self.count += 1
        run_id = run_id or f"r{self.count:04d}"
        run_dir = self.tmp / f"run-{run_id}-{self.count}"
        cand = self.tmp / f"cand-{run_id}-{self.count}"
        code, out = call("prepare", "--investigation", str(investigation or self.investigation), "--run-id", run_id,
                         "--case", case, "--condition", condition, "--model-label", "SYNTHETIC-model",
                         "--effort-label", "n/a", "--fresh-session", caps[0], "--workspace-confined", caps[1],
                         "--tool-log", caps[2], "--usage", caps[3], "--run-dir", str(run_dir),
                         "--candidate-dir", str(cand))
        return code, out, run_dir, cand

    def response(self, run_id: str, body: str, name: str | None = None) -> Path:
        return self.write(name or f"resp-{run_id}-{self.count}.txt", f"Run: {run_id}\n{SYN}{body}".encode())

    def collect(self, run_dir: Path, run_id: str, condition: str = "baseline", status: str = "completed",
                response: Path | None = None, session: str | None = None, *extra: str) -> tuple[int, dict]:
        argv = ["collect", "--run-dir", str(run_dir), "--expect-run", run_id, "--expect-condition", condition,
                "--status", status, "--label", "SYNTHETIC", "--session-label", session or f"session-{run_id}",
                "--isolation-used", "fresh"]
        if response is not None:
            argv += ["--response", str(response)]
        return call(*argv, *extra)

    def full_run(self, case: str, condition: str, body: str, run_id: str, session: str | None = None,
                 extra: tuple[str, ...] = ()) -> Path:
        code, out, run_dir, _cand = self.prepare(case, condition, run_id)
        self.assertEqual(code, 0, out)
        code, out = self.collect(run_dir, run_id, condition, "completed", self.response(run_id, body), session, *extra)
        self.assertEqual(code, 0, out)
        return run_dir

    def copy_lab(self) -> Path:
        lab = self.tmp / "lab-copy"
        shutil.copytree(REAL_LAB, lab, ignore=shutil.ignore_patterns("tests", "__pycache__"))
        pb.LAB = lab
        return lab

    def reseal(self, lab: Path) -> None:
        (lab / "bench.json").write_bytes(pb.dumps(pb.manifest_object()))


ORIGINAL_WRITE = pb._write_file


class TestBench(Base):
    def test_validate_real_bench(self) -> None:
        code, out = call("validate")
        self.assertEqual(code, 0, out)
        self.assertEqual(out["result"], "valid")
        self.assertEqual(out["bench_version"], sha((REAL_LAB / "bench.json").read_bytes()))
        self.assertEqual(len(out["cases"]), 8)

    def test_four_families_matched_and_synthetic(self) -> None:
        seen = {}
        for case in pb.manifest_object()["cases"]:
            meta = json.loads((REAL_LAB / "cases" / case["case_id"] / "coordinator/meta.json").read_text("utf-8"))
            self.assertEqual(meta["label"], "SYNTHETIC")
            seen[(meta["family"], meta["variant"])] = (case["case_id"], meta["matched_with"])
        self.assertEqual(set(seen), {(f, v) for f in pb.FAMILIES for v in pb.VARIANTS})
        for (family, variant), (case_id, matched) in seen.items():
            self.assertEqual(matched, seen[(family, "b" if variant == "a" else "a")][0])

    def test_drift_after_case_edit(self) -> None:
        lab = self.copy_lab()
        target = lab / "cases/complete-a/candidate/sources/return.md"
        target.write_bytes(target.read_bytes() + b"edited\n")
        code, out = call("validate")
        self.assertEqual(code, 1)
        self.assertEqual(out["result"], "drift")
        code, out, run_dir, cand = self.prepare("complete-a")
        self.assertEqual((code, out["code"]), (2, "bench-drift"))
        self.assertFalse(run_dir.exists() or cand.exists())

    def test_planted_canary_in_candidate_is_leakage(self) -> None:
        lab = self.copy_lab()
        canary = json.loads((lab / "cases/correction-b/evaluator/key.json").read_text("utf-8"))["canary"]
        target = lab / "cases/correction-a/candidate/sources/return.md"
        target.write_bytes(target.read_bytes() + canary.encode() + b"\n")
        self.reseal(lab)
        result = pb.validate()
        self.assertEqual(result["result"], "drift")
        self.assertTrue(any("evaluator-leakage" in d for d in result["drift"]), result["drift"])
        code, out, run_dir, cand = self.prepare("correction-a")
        self.assertEqual((code, out["code"]), (2, "bench-drift"))
        self.assertFalse(cand.exists())


class TestPrepare(Base):
    def test_kits_equal_except_tools_and_support(self) -> None:
        code, out, run_b, cand_b = self.prepare("design-fork-a", "baseline", "r0101")
        self.assertEqual(code, 0, out)
        code, out, run_a, cand_a = self.prepare("design-fork-a", "assisted", "r0102")
        self.assertEqual(code, 0, out)
        files_b = sorted(p.relative_to(cand_b).as_posix() for p in cand_b.rglob("*") if p.is_file())
        files_a = sorted(p.relative_to(cand_a).as_posix() for p in cand_a.rglob("*") if p.is_file())
        self.assertNotIn("support/prime_review.py", files_b)
        self.assertEqual(sorted(set(files_a) - set(files_b)),
                         ["support/CONTRACT.md", "support/README.md", "support/prime_review.py"])
        for rel in files_b:
            if rel != "PROMPT.md":
                self.assertEqual((cand_b / rel).read_bytes(), (cand_a / rel).read_bytes(), rel)
        for item in pb.SUPPORT:
            if item["copy_to"]:
                self.assertEqual(sha((cand_a / item["copy_to"]).read_bytes()), item["sha256"])
        pb_lines = (cand_b / "PROMPT.md").read_text("utf-8").replace("r0101", "RUN").split("\n")
        pa_lines = (cand_a / "PROMPT.md").read_text("utf-8").replace("r0102", "RUN").split("\n")
        tools = pb_lines.index("## Tools") + 1
        self.assertEqual(pb_lines[:tools] + pb_lines[tools + 1:], pa_lines[:tools] + pa_lines[tools + 1:])
        self.assertNotEqual(pb_lines[tools], pa_lines[tools])

    def test_candidate_has_no_identity_key_or_canary(self) -> None:
        code, out, run_dir, cand = self.prepare("false-completion-b", "assisted")
        self.assertEqual(code, 0, out)
        blob = b"".join(p.read_bytes() for p in cand.rglob("*") if p.is_file())
        for case in pb.manifest_object()["cases"]:
            key = json.loads((REAL_LAB / "cases" / case["case_id"] / "evaluator/key.json").read_text("utf-8"))
            self.assertNotIn(key["canary"].encode(), blob)
        for word in (b"false-completion", b"evaluator", b"matched_with", b"rubric.json"):
            self.assertNotIn(word, blob)
        self.assertFalse((cand / "run.json").exists())
        run = json.loads((run_dir / "run.json").read_text("utf-8"))
        self.assertEqual((run["case_id"], run["condition"], run["case_revision"]), ("false-completion-b", "assisted", 1))
        self.assertEqual(run["bench_version"], sha((REAL_LAB / "bench.json").read_bytes()))
        self.assertEqual(run["investigation_sha256"], sha(self.investigation.read_bytes()))

    def test_refusals(self) -> None:
        code, out, _r, _c = self.prepare("complete-a", run_id="7")
        self.assertEqual(out["code"], "malformed")
        code, out, _r, _c = self.prepare("no-such-case")
        self.assertEqual(out["code"], "malformed")
        code, out, _r, _c = self.prepare("complete-a", caps=("yes", "supported", "unknown", "unknown"))
        self.assertEqual(out["code"], "malformed")
        occupied = self.tmp / "occupied"
        occupied.mkdir()
        code, out = call("prepare", "--investigation", str(self.investigation), "--run-id", "r0200", "--case",
                         "complete-a", "--condition", "baseline", "--model-label", "m", "--effort-label", "e",
                         "--fresh-session", "supported", "--workspace-confined", "supported", "--tool-log", "unknown",
                         "--usage", "unknown", "--run-dir", str(occupied), "--candidate-dir", str(self.tmp / "c"))
        self.assertEqual((code, out["code"]), (2, "occupied"))
        self.assertFalse((self.tmp / "c").exists())

    def test_unsafe_destinations(self) -> None:
        base = ["prepare", "--investigation", str(self.investigation), "--run-id", "r0300", "--case", "complete-a",
                "--condition", "baseline", "--model-label", "m", "--effort-label", "e", "--fresh-session", "supported",
                "--workspace-confined", "supported", "--tool-log", "unknown", "--usage", "unknown"]
        cases = [
            (str(pb.REPO / "scratch-run"), str(self.tmp / "c1")),
            ("relative/run", str(self.tmp / "c2")),
            ("\\\\server\\share\\run", str(self.tmp / "c3")),
            (str(self.tmp) + "\\x\\..\\run", str(self.tmp / "c4")),
            (str(self.tmp / "nested"), str(self.tmp / "nested" / "cand")),
        ]
        for run_dir, cand in cases:
            code, out = call(*base, "--run-dir", run_dir, "--candidate-dir", cand)
            self.assertEqual((code, out["code"]), (2, "unsafe-path"), (run_dir, out))
        self.assertFalse((pb.REPO / "scratch-run").exists())

    def test_junction_ancestor_refused(self) -> None:
        target = self.tmp / "real"
        target.mkdir()
        link = self.tmp / "junction"
        made = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True)
        self.assertEqual(made.returncode, 0, made.stderr)
        code, out = call("prepare", "--investigation", str(self.investigation), "--run-id", "r0301", "--case",
                         "complete-a", "--condition", "baseline", "--model-label", "m", "--effort-label", "e",
                         "--fresh-session", "supported", "--workspace-confined", "supported", "--tool-log", "unknown",
                         "--usage", "unknown", "--run-dir", str(link / "run"), "--candidate-dir", str(self.tmp / "c"))
        self.assertEqual((code, out["code"]), (2, "unsafe-path"))
        self.assertEqual(list(target.iterdir()), [])
        os.rmdir(link)

    def test_partial_write_is_kept_and_not_resumed(self) -> None:
        calls = {"n": 0}

        def failing(path, data):
            calls["n"] += 1
            if calls["n"] == 4:
                raise OSError(28, "No space left on device (injected)")
            ORIGINAL_WRITE(path, data)

        pb._write_file = failing
        code, out, run_dir, cand = self.prepare("complete-b", "assisted", "r0400")
        pb._write_file = ORIGINAL_WRITE
        self.assertEqual((code, out["result"]), (1, "partial"))
        self.assertTrue(cand.is_dir())
        self.assertTrue(all(os.path.lexists(p) for p in out["retained"]))
        self.assertFalse(run_dir.exists())
        retained = sorted(p.relative_to(cand).as_posix() for p in cand.rglob("*") if p.is_file())
        code, again = call("prepare", "--investigation", str(self.investigation), "--run-id", "r0400", "--case",
                           "complete-b", "--condition", "assisted", "--model-label", "m", "--effort-label", "e",
                           "--fresh-session", "supported", "--workspace-confined", "supported", "--tool-log",
                           "unknown", "--usage", "unknown", "--run-dir", str(run_dir), "--candidate-dir", str(cand))
        self.assertEqual((code, again["code"]), (2, "occupied"))
        self.assertEqual(retained, sorted(p.relative_to(cand).as_posix() for p in cand.rglob("*") if p.is_file()))

    def test_partial_run_folder_is_never_collected(self) -> None:
        run_dir = self.tmp / "half"
        run_dir.mkdir()
        (run_dir / "COORDINATOR.md").write_text("partial")
        code, out = self.collect(run_dir, "r0001", response=self.response("r0001", GOOD["complete-a"]))
        self.assertEqual((code, out["code"]), (2, "partial-present"))


class TestCollectAndAssess(Base):
    def test_all_families_both_conditions_synthetic(self) -> None:
        n = 0
        for case, body in GOOD.items():
            for condition in pb.CONDITIONS:
                n += 1
                run_id = f"r{n:04d}"
                run_dir = self.full_run(case, condition, body, run_id)
                code, out = call("assess", "--run-dir", str(run_dir))
                self.assertEqual(code, 0, out)
                self.assertTrue(out["deterministic_pass"], (case, out["checks"]))
                self.assertEqual(out["kind"], "deterministic string checks")
        for case, body in WRONG.items():
            n += 1
            run_dir = self.full_run(case, "baseline", body, f"r{n:04d}")
            code, out = call("assess", "--run-dir", str(run_dir))
            self.assertFalse(out["deterministic_pass"], case)

    def test_quote_must_be_exact(self) -> None:
        body = GOOD["design-fork-a"].replace("asking me first", "asking me")
        run_dir = self.full_run("design-fork-a", "baseline", body, "r0500")
        code, out = call("assess", "--run-dir", str(run_dir))
        self.assertFalse(out["checks"]["must_quote"][0]["pass"])
        self.assertFalse(out["deterministic_pass"])

    def test_raw_bytes_kept_and_missing_usage_unavailable(self) -> None:
        code, out, run_dir, _c = self.prepare("complete-a", "baseline", "r0510")
        resp = self.write("crlf.txt", ("Run: r0510\r\n" + SYN + GOOD["complete-a"]).encode() + b"\xff\r\n")
        code, out = self.collect(run_dir, "r0510", response=resp)
        self.assertEqual(code, 0, out)
        self.assertEqual((run_dir / "collected/response.txt").read_bytes(), resp.read_bytes())
        col = json.loads((run_dir / "collection.json").read_text("utf-8"))
        self.assertIsNone(col["usage"])
        self.assertIsNone(col["tool_event_count"])
        self.assertIsNone(col["started"])
        code, cmp_ = call("compare", "--run-dir", str(run_dir))
        row = cmp_["rows"][0]
        self.assertEqual((row["usage"], row["elapsed_seconds"], row["tool_events"]), (None, None, None))
        self.assertIn("| unavailable | unavailable | unavailable |", cmp_["markdown"])

    def test_usage_times_and_tool_events(self) -> None:
        code, out, run_dir, _c = self.prepare("complete-b", "assisted", "r0520")
        events = self.write("events.jsonl", b"".join(
            json.dumps({"schema": "prime-bench-tool-event/1", "tool": t, "at": None}).encode() + b"\n"
            for t in ("read", "read", "prime_review report")))
        usage = self.write("usage.json", json.dumps({"source": "SYNTHETIC provider export", "input_tokens": 1200,
                                                     "output_tokens": 300}).encode())
        tool_log = self.write("tool.log", b"raw surface log, SYNTHETIC\n")
        code, out = self.collect(run_dir, "r0520", "assisted", "completed",
                                 self.response("r0520", GOOD["complete-b"]), None,
                                 "--usage", str(usage), "--tool-events", str(events), "--tool-log", str(tool_log),
                                 "--started", "2026-10-29T10:00:00-05:00", "--finished", "2026-10-29T10:07:30-05:00")
        self.assertEqual(code, 0, out)
        code, cmp_ = call("compare", "--run-dir", str(run_dir))
        row = cmp_["rows"][0]
        self.assertEqual((row["elapsed_seconds"], row["tool_events"]), (450.0, 3))
        self.assertEqual(row["usage"]["input_tokens"], 1200)
        self.assertNotIn("cache_read_tokens", row["usage"])

    def test_bad_usage_events_and_times_refused(self) -> None:
        code, out, run_dir, _c = self.prepare("complete-b", "baseline", "r0530")
        resp = self.response("r0530", GOOD["complete-b"])
        bad = [
            ("--usage", self.write("u1.json", b'{"source": "x", "input_tokens": -1}')),
            ("--usage", self.write("u2.json", b'{"source": "x", "input_tokens": true}')),
            ("--usage", self.write("u3.json", b'{"source": "x", "savings": 3}')),
            ("--usage", self.write("u4.json", b'{"source": "x", "input_tokens": 1, "input_tokens": 2}')),
            ("--usage", self.write("u5.json", b'{"source": "x", "input_tokens": NaN}')),
            ("--tool-events", self.write("e1.jsonl", b'{"schema": "prime-bench-tool-event/1", "tool": "read"}\n')),
            ("--tool-events", self.write("e2.jsonl", b"not json\n")),
        ]
        for flag, path in bad:
            code, out = self.collect(run_dir, "r0530", "baseline", "completed", resp, None, flag, str(path))
            self.assertEqual((code, out["code"]), (2, "malformed"), (flag, path.name, out))
        code, out = self.collect(run_dir, "r0530", "baseline", "completed", resp, None,
                                 "--started", "2026-10-29T10:00:00-05:00", "--finished", "2026-10-29T09:00:00-05:00")
        self.assertEqual(out["code"], "malformed")
        code, out = self.collect(run_dir, "r0530", "baseline", "completed", resp, None, "--started", "2026-10-29T10:00")
        self.assertEqual(out["code"], "malformed")
        self.assertFalse((run_dir / "collection.json").exists())

    def test_wrong_identity(self) -> None:
        code, out, run_dir, _c = self.prepare("correction-a", "baseline", "r0600")
        resp = self.response("r0600", GOOD["correction-a"])
        code, out = self.collect(run_dir, "r0601", "baseline", "completed", resp)
        self.assertEqual((code, out["code"]), (2, "wrong-identity"))
        code, out = self.collect(run_dir, "r0600", "assisted", "completed", resp)
        self.assertEqual((code, out["code"]), (2, "wrong-identity"))
        other = self.response("r0699", GOOD["correction-a"], "other.txt")
        code, out = self.collect(run_dir, "r0600", "baseline", "completed", other)
        self.assertEqual((code, out["code"]), (2, "wrong-identity"))
        self.assertFalse((run_dir / "collected").exists())
        no_line = self.write("noline.txt", (SYN + GOOD["correction-a"]).encode())
        code, out = self.collect(run_dir, "r0600", "baseline", "completed", no_line)
        self.assertEqual((code, out["identity"]), (0, "missing"))
        code, cmp_ = call("compare", "--run-dir", str(run_dir))
        self.assertIn("identity missing", cmp_["rows"][0]["not_clean_reasons"])

    def test_duplicate_and_conflicting_collection(self) -> None:
        run_dir = self.full_run("correction-b", "assisted", GOOD["correction-b"], "r0700")
        before = {p: p.read_bytes() for p in run_dir.rglob("*") if p.is_file()}
        resp = self.write("again.txt", (run_dir / "collected/response.txt").read_bytes())
        code, out = self.collect(run_dir, "r0700", "assisted", "completed", resp)
        self.assertEqual((code, out["code"]), (2, "already-collected"))
        changed = self.response("r0700", GOOD["correction-b"] + "Extra line.\n", "changed.txt")
        code, out = self.collect(run_dir, "r0700", "assisted", "completed", changed)
        self.assertEqual((code, out["code"]), (2, "conflict"))
        code, out = self.collect(run_dir, "r0700", "assisted", "completed", resp, "another-session")
        self.assertEqual((code, out["code"]), (2, "conflict"))
        self.assertEqual(before, {p: p.read_bytes() for p in run_dir.rglob("*") if p.is_file()})

    def test_failed_and_abandoned_runs_are_kept(self) -> None:
        code, out, failed_dir, _c = self.prepare("design-fork-b", "baseline", "r0800")
        code, out = self.collect(failed_dir, "r0800", "baseline", "failed")
        self.assertEqual(out["code"], "malformed")
        code, out = self.collect(failed_dir, "r0800", "baseline", "failed", None, None,
                                 "--reason", "SYNTHETIC: session crashed after reading the pack.")
        self.assertEqual(code, 0, out)
        code, out, ab_dir, _c = self.prepare("design-fork-b", "assisted", "r0801")
        partial = self.response("r0801", "Outcome: director-input\nI could not fin")
        code, out = self.collect(ab_dir, "r0801", "assisted", "abandoned", partial, None,
                                 "--reason", "SYNTHETIC: coordinator stopped at the time limit.")
        self.assertEqual(code, 0, out)
        done = self.full_run("design-fork-b", "assisted", GOOD["design-fork-b"], "r0802")
        code, cmp_ = call("compare", "--run-dir", str(failed_dir), "--run-dir", str(ab_dir), "--run-dir", str(done))
        self.assertEqual(code, 0, cmp_)
        rows = {r["run_id"]: r for r in cmp_["rows"]}
        self.assertEqual(rows["r0800"]["status"], "failed")
        self.assertEqual(rows["r0801"]["status"], "abandoned")
        self.assertFalse(rows["r0800"]["clean"] or rows["r0801"]["clean"])
        self.assertTrue(rows["r0802"]["clean"])
        self.assertEqual(cmp_["counts"]["assisted"]["by_status"]["abandoned"], 1)
        self.assertEqual(cmp_["counts"]["baseline"]["by_status"]["failed"], 1)
        self.assertIn("r0800 (baseline): failed", cmp_["markdown"])

    def test_contaminated_and_shared_context(self) -> None:
        a = self.full_run("complete-a", "baseline", GOOD["complete-a"], "r0900", session="one-session")
        b = self.full_run("complete-a", "assisted", GOOD["complete-a"], "r0901", session="one-session")
        code, out, c, _c = self.prepare("complete-b", "baseline", "r0902")
        code, out = call("collect", "--run-dir", str(c), "--expect-run", "r0902", "--expect-condition", "baseline",
                         "--status", "completed", "--label", "SYNTHETIC", "--session-label", "s-902",
                         "--isolation-used", "shared", "--response", str(self.response("r0902", GOOD["complete-b"])))
        self.assertEqual(code, 0, out)
        code, out, d, _c = self.prepare("complete-b", "assisted", "r0903", caps=("unknown", "unsupported", "unknown",
                                                                                 "unknown"))
        self.collect(d, "r0903", "assisted", "completed", self.response("r0903", GOOD["complete-b"]))
        code, cmp_ = call("compare", *sum((["--run-dir", str(x)] for x in (a, b, c, d)), []))
        rows = {r["run_id"]: r for r in cmp_["rows"]}
        self.assertIn("shared session: r0900, r0901", rows["r0900"]["not_clean_reasons"])
        self.assertIn("shared session: r0900, r0901", rows["r0901"]["not_clean_reasons"])
        self.assertIn("isolation used shared", rows["r0902"]["not_clean_reasons"])
        self.assertIn("fresh-session unknown", rows["r0903"]["not_clean_reasons"])
        self.assertIn("workspace-confined unsupported", rows["r0903"]["not_clean_reasons"])
        self.assertEqual(cmp_["counts"]["baseline"]["clean"] + cmp_["counts"]["assisted"]["clean"], 0)

    def test_evaluator_leakage_in_response(self) -> None:
        canary = json.loads((REAL_LAB / "cases/correction-a/evaluator/key.json").read_text("utf-8"))["canary"]
        run_dir = self.full_run("correction-a", "baseline", GOOD["correction-a"] + canary + "\n", "r1000")
        col = json.loads((run_dir / "collection.json").read_text("utf-8"))
        self.assertTrue(col["leakage"])
        code, out = call("assess", "--run-dir", str(run_dir))
        self.assertFalse(out["checks"]["canary_absent"])
        code, cmp_ = call("compare", "--run-dir", str(run_dir))
        self.assertIn("evaluator-leakage", cmp_["rows"][0]["not_clean_reasons"])

    def test_events_are_separate_and_interventions_unclean(self) -> None:
        run_dir = self.full_run("false-completion-a", "baseline", GOOD["false-completion-a"], "r1100")
        col_before = (run_dir / "collection.json").read_bytes()
        resp_before = (run_dir / "collected/response.txt").read_bytes()
        fix = self.write("fix.txt", b"SYNTHETIC corrected answer after the run.\n")
        code, out = call("event", "--run-dir", str(run_dir), "--kind", "correction", "--text",
                         "SYNTHETIC reviewer correction after the run.", "--attachment", str(fix))
        self.assertEqual((code, out["seq"]), (0, 1))
        code, cmp_ = call("compare", "--run-dir", str(run_dir))
        self.assertTrue(cmp_["rows"][0]["clean"])
        self.assertEqual(cmp_["rows"][0]["corrections"], 1)
        code, out = call("event", "--run-dir", str(run_dir), "--kind", "intervention", "--text",
                         "SYNTHETIC: coordinator answered a question mid-run.")
        self.assertEqual((code, out["seq"]), (0, 2))
        self.assertEqual((run_dir / "collection.json").read_bytes(), col_before)
        self.assertEqual((run_dir / "collected/response.txt").read_bytes(), resp_before)
        ev = json.loads((run_dir / "events/0001.json").read_text("utf-8"))
        self.assertEqual(ev["follows_collection_sha256"], sha(col_before))
        code, cmp_ = call("compare", "--run-dir", str(run_dir))
        self.assertEqual(cmp_["rows"][0]["not_clean_reasons"], ["intervention"])
        intervened = self.full_run("false-completion-b", "baseline", GOOD["false-completion-b"], "r1101",
                                   extra=("--intervention", "SYNTHETIC: hinted at the manifest."))
        code, cmp_ = call("compare", "--run-dir", str(intervened))
        self.assertEqual(cmp_["rows"][0]["not_clean_reasons"], ["intervention"])
        code, out = call("event", "--run-dir", str(self.prepare("complete-a")[2]), "--kind", "note", "--text", "x")
        self.assertEqual(out["code"], "not-collected")

    def test_unsafe_inputs(self) -> None:
        code, out, run_dir, _c = self.prepare("complete-a", "baseline", "r1200")
        resp = self.response("r1200", GOOD["complete-a"])
        linked = self.tmp / "hardlinked.txt"
        os.link(resp, linked)
        code, out = self.collect(run_dir, "r1200", "baseline", "completed", linked)
        self.assertEqual((code, out["code"]), (2, "unsafe-path"))
        inside = run_dir / "planted.txt"
        inside.write_bytes(resp.read_bytes())
        code, out = self.collect(run_dir, "r1200", "baseline", "completed", inside)
        self.assertEqual((code, out["code"]), (2, "unsafe-path"))
        big = self.write("big.txt", b"Run: r1200\n" + b"x" * (pb.MAX_RESPONSE + 1))
        code, out = self.collect(run_dir, "r1200", "baseline", "completed", big)
        self.assertEqual((code, out["code"]), (2, "too-large"))
        self.assertFalse((run_dir / "collection.json").exists())

    def test_partial_collection_kept(self) -> None:
        code, out, run_dir, _c = self.prepare("complete-a", "baseline", "r1300")
        resp = self.response("r1300", GOOD["complete-a"])

        def failing(path, data):
            if path.name == "collection.json":
                raise OSError(5, "I/O error (injected)")
            ORIGINAL_WRITE(path, data)

        pb._write_file = failing
        code, out = self.collect(run_dir, "r1300", "baseline", "completed", resp)
        pb._write_file = ORIGINAL_WRITE
        self.assertEqual((code, out["result"]), (1, "partial"))
        self.assertTrue((run_dir / "collected/response.txt").exists())
        code, out = self.collect(run_dir, "r1300", "baseline", "completed", resp)
        self.assertEqual((code, out["code"]), (2, "partial-present"))
        self.assertTrue((run_dir / "collected/response.txt").exists())


class TestReview(Base):
    def record(self, run_dir: Path, **change) -> Path:
        run = json.loads((run_dir / "run.json").read_text("utf-8"))
        rec = {"schema": "prime-bench-review/1", "run_id": run["run_id"], "case_id": run["case_id"],
               "case_revision": run["case_revision"], "rubric_sha256": run["pins"]["rubric_sha256"],
               "reviewer_label": "SYNTHETIC reviewer", "blind_to_condition": True,
               "scores": [{"item": f"R{i}", "score": 2, "note": None} for i in range(1, 6)],
               "reviewer_minutes": 4, "director_attention_events": None, "notes": "SYNTHETIC review record."}
        rec.update(change)
        self.count += 1
        return self.write(f"review-{self.count}.json", json.dumps(rec).encode())

    def test_review_bound_and_counted(self) -> None:
        a = self.full_run("correction-a", "baseline", GOOD["correction-a"], "r1400")
        b = self.full_run("correction-a", "assisted", GOOD["correction-a"], "r1401")
        rec = self.record(a)
        code, out = call("review", "--run-dir", str(a), "--record", str(rec))
        self.assertEqual(code, 0, out)
        self.assertEqual((a / "review.json").read_bytes(), rec.read_bytes())
        code, out = call("review", "--run-dir", str(a), "--record", str(rec))
        self.assertEqual(out["code"], "already-reviewed")
        code, out = call("review", "--run-dir", str(a), "--record", str(self.record(a, reviewer_minutes=9)))
        self.assertEqual(out["code"], "conflict")
        code, cmp_ = call("compare", "--run-dir", str(a), "--run-dir", str(b))
        self.assertEqual(cmp_["counts"]["baseline"]["rubric_items"]["R1"], {"reviewed_clean_runs": 1, "score_sum": 2})
        self.assertEqual(cmp_["counts"]["assisted"]["rubric_items"], {})
        flat = json.dumps(cmp_["counts"])
        for word in ("ratio", "saving", "rank", "multiple", "mean"):
            self.assertNotIn(word, flat)

    def test_review_refusals(self) -> None:
        run_dir = self.full_run("complete-b", "baseline", GOOD["complete-b"], "r1500")
        bad = [
            ({"run_id": "r1501"}, "wrong-identity"),
            ({"case_id": "complete-a"}, "wrong-identity"),
            ({"case_revision": 2}, "wrong-identity"),
            ({"rubric_sha256": "0" * 64}, "rubric-changed"),
            ({"scores": [{"item": "R1", "score": 2, "note": None}]}, "malformed"),
            ({"scores": [{"item": f"R{i}", "score": 3, "note": None} for i in range(1, 6)]}, "malformed"),
            ({"scores": [{"item": "R1", "score": 1, "note": None}] * 5}, "malformed"),
            ({"reviewer_minutes": -1}, "malformed"),
            ({"blind_to_condition": "yes"}, "malformed"),
        ]
        for change, code_name in bad:
            code, out = call("review", "--run-dir", str(run_dir), "--record", str(self.record(run_dir, **change)))
            self.assertEqual((code, out["code"]), (2, code_name), change)
        self.assertFalse((run_dir / "review.json").exists())

    def test_changed_rubric_after_prepare(self) -> None:
        lab = self.copy_lab()
        run_dir = self.full_run("design-fork-a", "baseline", GOOD["design-fork-a"], "r1600")
        rubric = lab / "cases/design-fork-a/evaluator/rubric.json"
        rubric.write_bytes(rubric.read_bytes().replace(b'"scale": [\n    0,', b'"scale": [\n    -1,\n    0,'))
        code, out = call("assess", "--run-dir", str(run_dir))
        self.assertEqual((code, out["code"]), (2, "rubric-changed"))
        code, out = call("compare", "--run-dir", str(run_dir))
        self.assertEqual((code, out["code"]), (2, "rubric-changed"))
        code, out = call("review", "--run-dir", str(run_dir), "--record", str(self.record(run_dir)))
        self.assertEqual((code, out["code"]), (2, "rubric-changed"))
        key = lab / "cases/design-fork-a/evaluator/key.json"
        rubric.write_bytes((REAL_LAB / "cases/design-fork-a/evaluator/rubric.json").read_bytes())
        key.write_bytes(key.read_bytes().replace(b'"director-input"', b'"continue"'))
        code, out = call("assess", "--run-dir", str(run_dir))
        self.assertEqual((code, out["code"]), (2, "key-changed"))


class TestCompareAndExport(Base):
    def test_mixed_and_duplicate_refused(self) -> None:
        a = self.full_run("complete-a", "baseline", GOOD["complete-a"], "r1700")
        code, out = call("compare", "--run-dir", str(a), "--run-dir", str(a))
        self.assertEqual(out["code"], "duplicate")
        b = self.full_run("complete-a", "assisted", GOOD["complete-a"], "r1700")
        code, out = call("compare", "--run-dir", str(a), "--run-dir", str(b))
        self.assertEqual(out["code"], "duplicate")
        other_inv = self.write("inv2.json", self.investigation.read_bytes().replace(b"0790.bench-trial",
                                                                                   b"0791.bench-trial"))
        code, out, c, _c = self.prepare("complete-a", "assisted", "r1702", investigation=other_inv)
        self.assertEqual(code, 0, out)
        code, out = call("compare", "--run-dir", str(a), "--run-dir", str(c))
        self.assertEqual(out["code"], "mixed-investigation")
        lab = self.copy_lab()
        task = lab / "cases/complete-a/candidate/TASK.md"
        task.write_bytes(task.read_bytes() + b"\nRevision note.\n")
        self.reseal(lab)
        code, out, d, _c = self.prepare("complete-b", "assisted", "r1703")
        self.assertEqual(code, 0, out)
        code, out = call("compare", "--run-dir", str(a), "--run-dir", str(d))
        self.assertEqual(out["code"], "mixed-version")

    def test_export_adapter(self) -> None:
        a = self.full_run("design-fork-a", "baseline", GOOD["design-fork-a"], "r1800")
        b = self.full_run("design-fork-a", "assisted", GOOD["design-fork-a"], "r1801")
        dest = self.tmp / "export"
        code, out = call("export", "--run-dir", str(a), "--run-dir", str(b), "--investigation",
                         str(self.investigation), "--dest", str(dest))
        self.assertEqual(code, 0, out)
        names = sorted(p.relative_to(dest).as_posix() for p in dest.rglob("*") if p.is_file())
        for want in ("05.01.return.TEMPLATE.md", "CAPTURE.txt", "comparison.json", "comparison.md",
                     "investigation.json", "runs/r1800/collected/response.txt", "runs/r1801/run.json"):
            self.assertIn(want, names)
        self.assertNotIn("05.01.return.md", names)
        self.assertEqual((dest / "investigation.json").read_bytes(), self.investigation.read_bytes())
        template = (dest / "05.01.return.TEMPLATE.md").read_text("utf-8")
        self.assertIn("TEMPLATE", template)
        self.assertIn("## Did\nTEMPLATE", template)
        capture = (dest / "CAPTURE.txt").read_text("utf-8")
        self.assertIn("labs/return-capture-pass01/return_capture.py capture", capture)
        self.assertIn("Not run by this harness", capture)
        blob = b"".join(p.read_bytes() for p in dest.rglob("*") if p.is_file())
        self.assertNotIn(b"BENCHKEY-CANARY", blob)
        comparison = json.loads((dest / "comparison.json").read_text("utf-8"))
        for row in comparison["rows"]:
            for rel, digest in row["records"].items():
                self.assertEqual(sha((dest / "runs" / row["run_id"] / rel).read_bytes()), digest, rel)
        code, out = call("export", "--run-dir", str(a), "--investigation", str(self.investigation), "--dest", str(dest))
        self.assertEqual(out["code"], "occupied")
        other_inv = self.write("inv3.json", self.investigation.read_bytes() + b"\n")
        code, out = call("export", "--run-dir", str(a), "--investigation", str(other_inv),
                         "--dest", str(self.tmp / "export2"))
        self.assertEqual(out["code"], "mixed-investigation")
        code, out = call("export", "--run-dir", str(a), "--investigation", str(self.investigation),
                         "--dest", str(pb.REPO / "bench-export"))
        self.assertEqual(out["code"], "unsafe-path")
        self.assertFalse((pb.REPO / "bench-export").exists())


class TestInputs(Base):
    def test_investigation_strict(self) -> None:
        base = json.loads(self.investigation.read_text("utf-8"))
        cases = [
            dict(base, page="0700.door"), dict(base, page="0800.bench"), dict(base, **{"pass": "5.1"}),
            dict(base, extra=1), {k: v for k, v in base.items() if k != "question"},
            dict(base, director_replies=[{"reply": "yes", "source_path": "../x", "source_sha256": "0" * 64}]),
        ]
        for i, inv in enumerate(cases):
            path = self.write(f"bad-inv-{i}.json", json.dumps(inv).encode())
            code, out, run_dir, cand = self.prepare("complete-a", investigation=path)
            self.assertEqual(code, 2, inv)
            self.assertFalse(cand.exists())
        dup = self.write("dup-inv.json", b'{"schema": "a", "schema": "b"}')
        code, out, _r, _c = self.prepare("complete-a", investigation=dup)
        self.assertEqual(out["code"], "malformed")

    def test_director_reply_kept_exact(self) -> None:
        base = json.loads(self.investigation.read_text("utf-8"))
        base["director_replies"][0]["reply"] = "yes"
        path = self.write("inv-yes.json", json.dumps(base).encode())
        code, out, run_dir, _c = self.prepare("complete-a", investigation=path)
        self.assertEqual(code, 0, out)
        self.assertEqual(json.loads((run_dir / "run.json").read_text("utf-8"))["investigation_sha256"],
                         sha(path.read_bytes()))

    def test_cli_exit_codes(self) -> None:
        self.assertEqual(pb.main(["no-such-command"]), 2)
        code, out = call("assess", "--run-dir", "relative")
        self.assertEqual((code, out["result"]), (2, "refused"))
        proc = subprocess.run([sys.executable, "-B", str(REAL_LAB / "prime_bench.py"), "validate", "--json"],
                              capture_output=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["result"], "valid")
        self.assertEqual(proc.stderr, b"")


if __name__ == "__main__":
    unittest.main()
